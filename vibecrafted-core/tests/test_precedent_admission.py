import asyncio
import json

import pytest
from vibecrafted_core import dispatcher, workflow
from vibecrafted_core.precedent_admission import HOOK_ENV, require_precedent


@pytest.fixture
def hook(tmp_path, monkeypatch):
    path = tmp_path / "hook.py"
    receipt = tmp_path / "payload.json"
    path.write_text(
        "import json, sys\n"
        "from pathlib import Path\n"
        "payload = json.load(sys.stdin)\n"
        f"Path({str(receipt)!r}).write_text(json.dumps(payload))\n"
        "brief = payload['tool_input']['prompt']\n"
        "if 'Precedens:' not in brief:\n"
        "    print(json.dumps({'hookSpecificOutput': {'permissionDecision': 'deny',\n"
        "          'permissionDecisionReason': 'fixture receipt missing'}}))\n"
    )
    monkeypatch.setenv(HOOK_ENV, str(path))
    monkeypatch.setenv("VIBECRAFTED_PRECEDENS_SESSION_ID", "fixture-caller")
    return receipt


def test_workflow_gate_uses_original_brief_before_mutations(
    tmp_path, monkeypatch, hook
):
    reached = []
    monkeypatch.setattr(workflow, "_sweep_stale_runs", lambda: reached.append(True))
    spec = workflow.WorkflowLaunchSpec(
        skill="implement",
        agent="codex",
        mode="prompt",
        file="",
        runtime="headless",
        root=str(tmp_path),
        prompt="Rendered wrapper that must not be checked",
        plan_source="Fix the synthetic regression",
    )
    with pytest.raises(ValueError, match="fixture receipt missing"):
        workflow.launch_workflow(spec, source_dir=tmp_path)
    assert not reached
    payload = json.loads(hook.read_text())
    assert payload["tool_input"]["prompt"] == spec.plan_source
    assert payload["session_id"] == "fixture-caller"
    assert payload["cwd"] == str(tmp_path.resolve())


@pytest.mark.parametrize(
    "brief, expected", [(None, "--prompt-file"), ("Fix fixture", "receipt missing")]
)
def test_public_dispatch_run_checks_before_signal_server(
    tmp_path, monkeypatch, hook, brief, expected
):
    def unexpected_start(*args, **kwargs):
        pytest.fail("a denied dispatch reached the signal server")

    monkeypatch.setattr(dispatcher, "RunSignalServer", unexpected_start)
    argv = ["run", "--check-precedent", "--run-id", "fixture", "--root", str(tmp_path)]
    if brief is not None:
        path = tmp_path / "brief.md"
        path.write_text(brief)
        argv.extend(["--prompt-file", str(path)])
    args = dispatcher._build_parser().parse_args([*argv, "--", "true"])
    with pytest.raises(ValueError, match=expected):
        asyncio.run(dispatcher._run(args))


def test_hook_accepts_receipt_and_rejects_an_invalid_reply(tmp_path, hook):
    require_precedent("Fix fixture\nPrecedens: P-ab12cd", tmp_path)
    assert json.loads(hook.read_text())["tool_name"] == "Agent"
    hook_path = tmp_path / "hook.py"
    hook_path.write_text("print('not a hook response')")
    with pytest.raises(ValueError, match="invalid hook response"):
        require_precedent("Fix fixture", tmp_path)


def test_codex_caller_session_requires_a_consistent_context(
    tmp_path, monkeypatch, hook
):
    monkeypatch.delenv("VIBECRAFTED_PRECEDENS_SESSION_ID")
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    monkeypatch.setenv("CODEX_THREAD_ID", "codex-fixture")
    monkeypatch.setenv("CODEX_SESSION_ID", "codex-fixture")
    require_precedent("Fix fixture\nPrecedens: P-ab12cd", tmp_path)
    assert json.loads(hook.read_text())["session_id"] == "codex-fixture"
    monkeypatch.setenv("CODEX_SESSION_ID", "another-session")
    with pytest.raises(ValueError, match="provider IDs differ"):
        require_precedent("Fix fixture\nPrecedens: P-ab12cd", tmp_path)


def test_hook_error_with_empty_stdout_refuses_launch(tmp_path, monkeypatch, hook):
    (tmp_path / "hook.py").write_text(
        "import sys; print('internal error', file=sys.stderr)"
    )
    with pytest.raises(ValueError, match="hook reported an error"):
        require_precedent("Fix fixture", tmp_path)


def test_raw_dispatch_delivers_exact_admitted_bytes(tmp_path, monkeypatch, hook):
    source = tmp_path / "brief.md"
    brief = b"Fix the fixture\r\nPrecedens: P-ab12cd\r\n"
    source.write_bytes(brief)

    async def receive_worker_input(args, worker, prompt_file):
        source.write_bytes(b"Changed after admission")
        assert prompt_file.read_bytes() == brief
        return 0

    monkeypatch.setattr(dispatcher, "_run_worker", receive_worker_input)
    args = dispatcher._build_parser().parse_args(
        [
            "run",
            "--check-precedent",
            "--run-id",
            "fixture",
            "--root",
            str(tmp_path),
            "--prompt-file",
            str(source),
            "--",
            "true",
        ]
    )
    assert asyncio.run(dispatcher._run(args)) == 0
