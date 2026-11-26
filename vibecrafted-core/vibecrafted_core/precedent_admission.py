"""Delegate launch-time precedent policy to the configured fleet hook."""

import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

HOOK_ENV = "VIBECRAFTED_PRECEDENS_HOOK"


def _caller_session() -> str:
    explicit = os.environ.get("VIBECRAFTED_PRECEDENS_SESSION_ID", "").strip()
    if explicit:
        return explicit
    candidates = {
        value
        for key in ("CLAUDE_CODE_SESSION_ID", "CODEX_THREAD_ID", "CODEX_SESSION_ID")
        if (value := os.environ.get(key, "").strip())
    }
    if len(candidates) > 1:
        raise ValueError(
            "precedens admission needs an explicit caller session when provider IDs differ"
        )
    return candidates.pop() if candidates else str(uuid.uuid4())


def require_precedent(brief: str, root: str | Path) -> None:
    """Check the source brief before launch, using the operator's environment."""
    configured = os.environ.get(HOOK_ENV)
    if not configured:
        return
    hook = Path(configured)
    if not hook.is_absolute() or not hook.is_file():
        raise ValueError("precedens admission requires an existing absolute hook path")
    payload = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Agent",
        "tool_input": {"subagent_type": "vibecrafted-worker", "prompt": brief},
        "session_id": _caller_session(),
        "cwd": str(Path(root).resolve()),
        "permission_mode": "default",
    }
    try:
        response = subprocess.run(
            [sys.executable, str(hook)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=15,
            check=True,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ValueError(f"precedens admission could not run the hook: {exc}") from exc
    if response.stderr.strip():
        raise ValueError(
            "precedens admission hook reported an error; check the hook configuration"
        )
    if not response.stdout.strip():
        return
    try:
        outcome = json.loads(response.stdout)["hookSpecificOutput"]
        decision = outcome["permissionDecision"]
    except (ValueError, KeyError, TypeError) as exc:
        raise ValueError(
            "precedens admission received an invalid hook response"
        ) from exc
    if decision != "allow":
        reason = outcome.get("permissionDecisionReason") or "approval was not granted"
        raise ValueError(f"precedens admission refused launch: {reason}")
