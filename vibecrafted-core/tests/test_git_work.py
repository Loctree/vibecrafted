"""vc-git work families: addresses, landed, gems and save.

Every scenario is one where Git's own answer is misleading (squash merge,
cherry-pick, plain copy, rewritten history) or where work is easy to lose
(stash, uncommitted files, reflog-only commits).
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
from pathlib import Path

import pytest
from vibecrafted_core import git as vc_git
from vibecrafted_core import git_address as address
from vibecrafted_core import git_cli
from vibecrafted_core.control_plane import control_plane_home
from vibecrafted_core.git_gems import harbor_root

_CLOCK = {"t": 1_760_000_000}


def git_cmd(root: Path, *args: str, input: str | None = None) -> str:
    _CLOCK["t"] += 60
    stamp = f"{_CLOCK['t']} +0000"
    env = {
        **os.environ,
        "GIT_AUTHOR_DATE": stamp,
        "GIT_COMMITTER_DATE": stamp,
    }
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(key, None)
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        input=input,
        env=env,
    ).stdout.strip()


def write(root: Path, name: str, text: str) -> None:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def commit_all(root: Path, message: str) -> str:
    git_cmd(root, "add", "-A")
    git_cmd(root, "commit", "-qm", message)
    return git_cmd(root, "rev-parse", "HEAD")


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    git_cmd(root, "init", "-q", "-b", "main")
    git_cmd(root, "config", "user.name", "Test")
    git_cmd(root, "config", "user.email", "test@example.com")
    git_cmd(root, "config", "core.logAllRefUpdates", "true")
    # Hostile but real host settings: vc-git must not parse what they change.
    git_cmd(root, "config", "diff.mnemonicPrefix", "true")
    git_cmd(root, "config", "color.ui", "always")
    write(root, "app.py", "".join(f"line {n}\n" for n in range(1, 21)))
    write(root, "docs/guide.md", "# Guide\n\nIntro.\n")
    write(root, ".gitignore", "build/\n")
    commit_all(root, "base")
    return root


def run_cli(*argv: str, stdin: str = "") -> tuple[int, str]:
    out = io.StringIO()
    import contextlib

    with contextlib.redirect_stdout(out):
        code = git_cli.run(argv[0], list(argv[1:]), stdin=io.StringIO(stdin))
    return code, out.getvalue()


def landed(repo: Path, text: str, target: str = "main", **kwargs) -> dict:
    from vibecrafted_core.git_landed import TargetView
    from vibecrafted_core.git_landed import landed as measure

    name, sha = address.resolve_target(repo, target)
    lines = address.integration_lines(repo, name, sha)
    with TargetView(repo, name, sha) as view:
        return measure(address.resolve(repo, text), view, lines, **kwargs)


def feature(repo: Path, name: str = "feat") -> list[str]:
    git_cmd(repo, "checkout", "-qb", name)
    write(
        repo,
        "app.py",
        (repo / "app.py").read_text().replace("line 3\n", "line three\n"),
    )
    first = commit_all(repo, "spell out three")
    write(repo, "docs/guide.md", "# Guide\n\nIntro.\n\nUsage: run it.\n")
    second = commit_all(repo, "document usage")
    git_cmd(repo, "checkout", "-q", "main")
    return [first, second]


def snapshot_state(root: Path) -> dict:
    """Everything a read-only command must leave exactly as it was."""
    git_dir = Path(git_cmd(root, "rev-parse", "--absolute-git-dir"))
    index = git_dir / "index"
    return {
        "refs": git_cmd(root, "for-each-ref", "--format=%(refname) %(objectname)"),
        "stash": git_cmd(root, "stash", "list", "--format=%H"),
        "status": git_cmd(root, "status", "--porcelain=v1", "--untracked-files=all"),
        "index": hashlib.sha256(index.read_bytes()).hexdigest()
        if index.exists()
        else None,
        "objects": git_cmd(root, "count-objects", "-v"),
    }


# --------------------------------------------------------------------- landed


def test_squash_merge_lands_although_ancestry_says_no(repo: Path) -> None:
    commits = feature(repo)
    git_cmd(repo, "merge", "--squash", "feat")
    squash = commit_all(repo, "feat (squashed)")
    assert (
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", commits[-1], "main"],
            cwd=repo,
            check=False,
        ).returncode
        == 1
    )
    result = landed(repo, "feat")
    assert result["answer"] == "yes"
    assert result["landed_as"] == squash
    assert any("squash" in item["claim"] for item in result["evidence"])
    code, text = run_cli("landed", "--repo", str(repo), "--target", "main", "feat")
    assert code == git_cli.EXIT_YES
    assert text.startswith("Yes. feat@")


def test_every_commit_cherry_picked_lands(repo: Path) -> None:
    commits = feature(repo)
    write(repo, "other.txt", "main moves on\n")
    commit_all(repo, "unrelated main work")
    git_cmd(repo, "cherry-pick", *commits)
    result = landed(repo, "feat")
    assert result["answer"] == "yes"
    assert "cherry-picked" in result["sentence"]


def test_plain_copy_of_one_file_is_partly_landed(repo: Path) -> None:
    feature(repo)
    git_cmd(repo, "checkout", "-q", "feat", "--", "app.py")
    commit_all(repo, "copy only the app change by hand")
    result = landed(repo, "feat")
    assert result["answer"] == "no"
    assert result["extent"] == "partial"
    states = {f["path"]: f["state"] for f in result["files"]}
    assert states == {"app.py": "identical", "docs/guide.md": "absent"}
    code, text = run_cli("landed", "--repo", str(repo), "--target", "main", "feat")
    assert code == git_cli.EXIT_NO
    assert "only partly" in text and "docs/guide.md" in text


def test_landed_then_changed_in_target_still_counts(repo: Path) -> None:
    feature(repo)
    git_cmd(repo, "merge", "--squash", "feat")
    commit_all(repo, "squash")
    write(
        repo,
        "app.py",
        (repo / "app.py")
        .read_text()
        .replace("line three\n", "line THREE (renamed later)\n"),
    )
    write(repo, "docs/guide.md", "# Guide v2\n\nRewritten.\n")
    commit_all(repo, "later edits on main")
    result = landed(repo, "feat")
    assert result["answer"] == "yes", result
    assert all(f["state"] == "present" for f in result["files"])
    assert all("held exactly this content" in f["why"] for f in result["files"])


def test_diverged_change_cannot_be_established_and_is_not_folded(repo: Path) -> None:
    git_cmd(repo, "checkout", "-qb", "feat")
    write(
        repo, "app.py", (repo / "app.py").read_text().replace("line 10\n", "line ten\n")
    )
    commit_all(repo, "feature edits line 10")
    git_cmd(repo, "checkout", "-q", "main")
    write(
        repo,
        "app.py",
        (repo / "app.py")
        .read_text()
        .replace("line 9\nline 10\nline 11\n", "nine\nTEN\neleven\n"),
    )
    commit_all(repo, "main rewrites the same lines")
    result = landed(repo, "feat")
    assert result["answer"] == "unknown"
    assert result["files"][0]["state"] == "unknown"
    assert result["files"][0]["likely"] == "absent"
    code, text = run_cli("landed", "--repo", str(repo), "--target", "main", "feat")
    assert code == git_cli.EXIT_UNKNOWN
    assert text.startswith("Cannot be established.")


def test_batch_exit_prefers_no_over_unknown(repo: Path) -> None:
    feature(repo)
    git_cmd(repo, "checkout", "-qb", "clash", "main")
    write(
        repo, "app.py", (repo / "app.py").read_text().replace("line 3\n", "line tres\n")
    )
    commit_all(repo, "clash edits line 3")
    git_cmd(repo, "checkout", "-q", "main")
    git_cmd(repo, "merge", "--squash", "clash")
    commit_all(repo, "squash clash")
    code, _ = run_cli(
        "landed", "--repo", str(repo), "--target", "main", "feat", "clash"
    )
    first = landed(repo, "feat")
    assert first["answer"] in {"no", "unknown"}
    assert code == (
        git_cli.EXIT_NO if first["answer"] == "no" else git_cli.EXIT_UNKNOWN
    )


def test_uncommitted_worktree_work_is_measured_without_writing(repo: Path) -> None:
    write(
        repo,
        "app.py",
        (repo / "app.py").read_text().replace("line 20\n", "line twenty\n"),
    )
    write(repo, "notes/new.txt", "fresh idea\n")
    before = snapshot_state(repo)
    result = landed(repo, f"wt:{repo}")
    assert result["answer"] == "no"
    assert {f["path"] for f in result["files"]} == {"app.py", "notes/new.txt"}
    assert snapshot_state(repo) == before, "a read must not change the repository"


def test_ancestor_is_yes_and_empty_work_is_yes(repo: Path) -> None:
    git_cmd(repo, "branch", "old", "HEAD")
    assert landed(repo, "old")["answer"] == "yes"


def test_patch_file_address_is_compared_per_file(repo: Path, tmp_path: Path) -> None:
    feature(repo)
    patch = tmp_path / "feat.patch"
    # Mnemonic prefixes (c/ w/) stay on: a valid -p1 patch must still parse.
    patch.write_text(
        git_cmd(repo, "-c", "color.ui=false", "diff", "--full-index", "main", "feat")
        + "\n"
    )
    result = landed(repo, f"patch:{patch}")
    assert result["answer"] == "no"
    assert {f["state"] for f in result["files"]} == {"absent"}


# ------------------------------------------------------------------ addresses


def test_pinned_branch_address_reports_that_the_branch_moved(repo: Path) -> None:
    commits = feature(repo)
    git_cmd(repo, "checkout", "-q", "feat")
    write(repo, "late.txt", "late\n")
    commit_all(repo, "late")
    git_cmd(repo, "checkout", "-q", "main")
    work = address.resolve(repo, f"feat@{commits[-1][:10]}")
    assert work.tip == commits[-1]
    assert any("has moved" in note["claim"] for note in work.notes)


def test_stash_pin_survives_renumbering(repo: Path) -> None:
    write(repo, "app.py", "first stash\n")
    git_cmd(repo, "stash", "push", "-qm", "one")
    pinned = address.resolve(repo, "stash@{0}").address
    write(repo, "app.py", "second stash\n")
    git_cmd(repo, "stash", "push", "-qm", "two")
    again = address.resolve(repo, pinned)
    assert again.label == "stash@{1}"
    assert any("has moved" in note["claim"] for note in again.notes)


def test_unknown_address_is_a_usage_error(repo: Path) -> None:
    code, _ = run_cli(
        "landed", "--repo", str(repo), "--target", "main", "no-such-branch"
    )
    assert code == git_cli.EXIT_ERROR


def test_run_address_resolves_through_the_runtime_receipt(
    repo: Path, tmp_path: Path
) -> None:
    base = git_cmd(repo, "rev-parse", "HEAD")
    tree = tmp_path / "worker"
    git_cmd(repo, "worktree", "add", "-qb", "cut/worker", str(tree))
    write(tree, "app.py", "worker rewrite\n")
    commit_all(tree, "worker change")
    receipt = control_plane_home() / "runtime_runs" / "run-77" / "meta.json"
    receipt.parent.mkdir(parents=True)
    receipt.write_text(
        json.dumps(
            {
                "run_id": "run-77",
                "status": "completed",
                "root": str(tree),
                "branch": "cut/worker",
                "worktree_baseline_sha": base,
            }
        )
    )
    work = address.resolve(repo, "run:run-77")
    assert work.address == "run:run-77"
    assert work.base_hint and work.base_hint[0] == base
    assert landed(repo, "run:run-77")["answer"] == "no"


def test_pr_address_without_github_cannot_be_established(
    repo: Path, monkeypatch
) -> None:
    real = subprocess.run

    def no_gh(cmd, *args, **kwargs):
        if cmd and cmd[0] == "gh":
            raise FileNotFoundError("gh")
        return real(cmd, *args, **kwargs)

    monkeypatch.setattr(address.subprocess, "run", no_gh)
    code, text = run_cli("landed", "--repo", str(repo), "--target", "main", "pr:7")
    assert code == git_cli.EXIT_UNKNOWN
    assert "GitHub CLI unavailable" in text


# ----------------------------------------------------------------------- save


def test_save_to_patch_never_touches_the_checkout(repo: Path, tmp_path: Path) -> None:
    write(repo, "app.py", (repo / "app.py").read_text() + "tracked edit\n")
    git_cmd(repo, "add", "app.py")
    write(repo, "app.py", (repo / "app.py").read_text() + "unstaged edit\n")
    write(repo, "notes/untracked.txt", "only here\n")
    write(repo, "build/out.bin", "regenerable\n")
    before = {k: v for k, v in snapshot_state(repo).items() if k != "objects"}
    files_before = {
        p: (repo / p).read_text() for p in ("app.py", "notes/untracked.txt")
    }
    code, text = run_cli(
        "save", "--repo", str(repo), "--target", "main", "--to", "patch", "--json"
    )
    assert code == git_cli.EXIT_YES
    result = json.loads(text)["results"][0]
    assert {k: v for k, v in snapshot_state(repo).items() if k != "objects"} == before
    assert {p: (repo / p).read_text() for p in files_before} == files_before
    saved = Path(result["saved"][0].removeprefix("patch:"))
    manifest = json.loads(Path(result["manifest"]).read_text())
    assert manifest["sha256"] == hashlib.sha256(saved.read_bytes()).hexdigest()
    assert saved.is_relative_to(harbor_root())
    assert any("ignored" in warning for warning in result["warnings"])
    # The patch rebuilds the work on a fresh copy of its base.
    clone = tmp_path / "clone"
    git_cmd(tmp_path, "clone", "-q", str(repo), str(clone))
    git_cmd(clone, "apply", "--index", str(saved))
    assert (clone / "notes/untracked.txt").read_text() == "only here\n"
    assert (clone / "app.py").read_text() == files_before["app.py"]


def test_save_to_commit_creates_a_ref_and_moves_nothing(repo: Path) -> None:
    write(repo, "notes/idea.txt", "keep me\n")
    head = git_cmd(repo, "rev-parse", "HEAD")
    code, text = run_cli(
        "save",
        f"wt:{repo}",
        "--repo",
        str(repo),
        "--target",
        "main",
        "--to",
        "commit",
        "--addresses",
    )
    assert code == git_cli.EXIT_YES
    saved = text.strip()
    assert saved.startswith("saved:")
    assert git_cmd(repo, "rev-parse", "HEAD") == head
    assert git_cmd(repo, "status", "--porcelain") == "?? notes/"
    work = address.resolve(repo, saved)
    assert git_cmd(repo, "show", f"{work.tip}:notes/idea.txt") == "keep me"


def test_save_to_stash_keeps_untracked_and_leaves_checkout(
    repo: Path, tmp_path: Path
) -> None:
    write(repo, "app.py", "changed\n")
    write(repo, "notes/new.txt", "untracked\n")
    status = git_cmd(repo, "status", "--porcelain")
    code, text = run_cli(
        "save", "--repo", str(repo), "--target", "main", "--to", "stash", "--addresses"
    )
    assert code == git_cli.EXIT_YES
    assert git_cmd(repo, "status", "--porcelain") == status
    stash = address.resolve(repo, text.strip())
    assert stash.stash_untracked, "untracked files must be in the stash"
    # The entry restores everything in a clean checkout.
    git_cmd(repo, "stash", "push", "-qu", "-m", "move the live work aside")
    git_cmd(repo, "stash", "apply", "-q", stash.tip)
    assert (repo / "notes/new.txt").read_text() == "untracked\n"
    assert (repo / "app.py").read_text() == "changed\n"


def test_save_git_apply_proves_or_refuses_clean_application(repo: Path) -> None:
    feature(repo)
    code, text = run_cli(
        "save",
        "feat",
        "--repo",
        str(repo),
        "--target",
        "main",
        "--to",
        "git-apply",
        "--json",
    )
    assert code == git_cli.EXIT_YES
    assert json.loads(text)["results"][0]["applies_to"]["clean"] is True
    write(repo, "docs/guide.md", "# Totally different\n")
    commit_all(repo, "main rewrites the guide")
    code, text = run_cli(
        "save",
        "feat",
        "--repo",
        str(repo),
        "--target",
        "main",
        "--to",
        "git-apply",
        "--json",
    )
    result = json.loads(text)["results"][0]
    assert code == git_cli.EXIT_NO
    assert result["applies_to"]["clean"] is False
    assert Path(result["saved"][0].removeprefix("patch:")).is_file(), (
        "a refused check still keeps the copy"
    )


def test_save_dry_run_writes_nothing(repo: Path) -> None:
    write(repo, "notes/x.txt", "x\n")
    before = snapshot_state(repo)
    code, text = run_cli(
        "save", "--repo", str(repo), "--target", "main", "--to", "commit", "--dry-run"
    )
    assert code == git_cli.EXIT_YES
    assert text.startswith("Dry run.")
    assert snapshot_state(repo) == before
    assert not harbor_root().exists()


def test_saving_a_clean_checkout_says_nothing_to_save(repo: Path) -> None:
    code, text = run_cli("save", "--repo", str(repo), "--target", "main")
    assert code == git_cli.EXIT_YES
    assert text.startswith("Nothing to save.")


# ----------------------------------------------------------------------- gems


@pytest.fixture
def scattered(repo: Path, tmp_path: Path) -> Path:
    """Work hidden in every place a fleet leaves it."""
    origin = tmp_path / "origin.git"
    git_cmd(tmp_path, "init", "-q", "--bare", str(origin))
    git_cmd(repo, "remote", "add", "origin", str(origin))
    git_cmd(repo, "push", "-q", "origin", "main")
    git_cmd(repo, "remote", "set-head", "origin", "main")
    # 1. squash-merged: Git says unmerged, content says landed.
    feature(repo, "squashed")
    git_cmd(repo, "merge", "--squash", "squashed")
    commit_all(repo, "squash it")
    git_cmd(repo, "push", "-q", "origin", "main")
    # 2. pushed but never merged.
    git_cmd(repo, "checkout", "-qb", "pushed")
    write(repo, "pushed.txt", "on the remote\n")
    commit_all(repo, "pushed work")
    git_cmd(repo, "push", "-q", "origin", "pushed")
    # 3. local only, with a second name carried inside it.
    git_cmd(repo, "checkout", "-qb", "local-only", "main")
    write(repo, "local.txt", "one\n")
    commit_all(repo, "local step one")
    git_cmd(repo, "branch", "local-only-early")
    write(repo, "local.txt", "one\ntwo\n")
    commit_all(repo, "local step two")
    # 4. reflog only: reset away. 5. amended: superseded rewrite.
    write(repo, "lost.txt", "reset away\n")
    commit_all(repo, "lost by reset")
    git_cmd(repo, "reset", "-q", "--hard", "HEAD~1")
    write(repo, "amend.txt", "v1\n")
    commit_all(repo, "amend me")
    write(repo, "amend.txt", "v2\n")
    git_cmd(repo, "add", "-A")
    git_cmd(repo, "commit", "-q", "--amend", "--no-edit")
    git_cmd(repo, "checkout", "-q", "main")
    # 6. a stash. 7. uncommitted files in a worktree.
    write(repo, "app.py", "stashed edit\n")
    git_cmd(repo, "stash", "push", "-qm", "parked")
    tree = tmp_path / "dirty-tree"
    git_cmd(repo, "worktree", "add", "-qb", "dirty", str(tree))
    write(tree, "draft.txt", "uncommitted draft\n")
    return repo


def test_gems_finds_hidden_work_and_skips_what_landed(scattered: Path) -> None:
    before = snapshot_state(scattered)
    code, text = run_cli("gems", "--repo", str(scattered), "--json", "--limit", "0")
    assert code == git_cli.EXIT_YES
    payload = json.loads(text)
    assert snapshot_state(scattered) == before, "gems must not change the repository"
    rows = {
        row["address"].split("@")[0]
        if "@" in row["address"] and not row["address"].startswith("stash")
        else row["address"]: row
        for row in payload["gems"]
    }
    found = " ".join(row["address"] + " " + row["label"] for row in payload["gems"])
    assert "squashed" not in found
    assert payload["searched"]["landed_by_content"] >= 1
    assert "pushed" in rows and rows["pushed"]["single_copy"] is False
    assert "local-only" in rows and rows["local-only"]["single_copy"] is True
    assert "local-only-early" not in rows
    assert payload["searched"]["carried_by_other_branches"] >= 1
    assert any(row["tier"] == "stash" for row in payload["gems"])
    assert any(
        row["tier"] == "uncommitted" and "dirty-tree" in row["address"]
        for row in payload["gems"]
    )
    reflog = [row for row in payload["gems"] if row["tier"] == "reflog-only"]
    assert len(reflog) == 1 and reflog[0]["subject"] == "lost by reset"
    assert payload["searched"]["superseded_rewrites"] == 1
    order = [row["tier"] for row in payload["gems"]]
    assert order[0] == "reflog-only" and order[-1] == "pushed"


def test_gems_search_and_pipe_into_save(scattered: Path) -> None:
    code, text = run_cli(
        "gems", "search", "lost", "--repo", str(scattered), "--addresses"
    )
    assert code == git_cli.EXIT_YES
    addresses = text.split()
    assert len(addresses) == 1
    code, saved = run_cli(
        "save",
        "-",
        "--repo",
        str(scattered),
        "--to",
        "patch",
        "--addresses",
        stdin=text,
    )
    assert code == git_cli.EXIT_YES
    assert saved.strip().startswith("patch:")
    # The harbor copy now counts: the reflog-only work is no longer an only copy.
    code, again = run_cli("gems", "search", "lost", "--repo", str(scattered), "--json")
    row = json.loads(again)["gems"][0]
    assert row["copies"] == ["harbor"] and row["single_copy"] is False


def test_vc_git_main_routes_families(repo: Path, capsys) -> None:
    assert vc_git.main(["landed", "--repo", str(repo), "--target", "main", "main"]) == 0
    assert capsys.readouterr().out.startswith("Yes.")


def _touch_without_change(root: Path, name: str) -> bytes:
    """Give a tracked file a new mtime but the same content; return the index."""
    path = root / name
    stamp = path.stat().st_mtime + 120
    os.utime(path, (stamp, stamp))
    return (
        Path(git_cmd(root, "rev-parse", "--absolute-git-dir")) / "index"
    ).read_bytes()


def test_reading_a_checkout_never_rewrites_its_index(repo: Path) -> None:
    write(repo, "notes/new.txt", "real change\n")
    index = _touch_without_change(repo, "app.py")
    result = landed(repo, f"wt:{repo}")
    assert [f["path"] for f in result["files"]] == ["notes/new.txt"]
    code, _ = run_cli("save", "--repo", str(repo), "--target", "main", "--dry-run")
    assert code == git_cli.EXIT_YES
    git_dir = Path(git_cmd(repo, "rev-parse", "--absolute-git-dir"))
    assert (git_dir / "index").read_bytes() == index, (
        "porcelain git diff refreshed and rewrote the index"
    )


def test_repo_overview_does_not_rewrite_worktree_indexes(
    repo: Path, tmp_path: Path
) -> None:
    tree = tmp_path / "side"
    git_cmd(repo, "worktree", "add", "-qb", "side", str(tree))
    index = _touch_without_change(tree, "app.py")
    vc_git.repo_full(repo)
    git_dir = Path(git_cmd(tree, "rev-parse", "--absolute-git-dir"))
    assert (git_dir / "index").read_bytes() == index, (
        "git status refreshed another checkout's index"
    )


def test_reflog_only_work_is_measured_from_where_refs_stop(scattered: Path) -> None:
    code, text = run_cli("gems", "--repo", str(scattered), "--json", "--limit", "0")
    assert code == git_cli.EXIT_YES
    row = next(r for r in json.loads(text)["gems"] if r["tier"] == "reflog-only")
    assert "1 commit(s) that no branch, tag or stash holds" in row["base_reason"]
    assert [f["path"] for f in row["files"]] == ["lost.txt"]
    # The same address measured directly answers the same way.
    direct = landed(scattered, row["address"])
    assert [f["path"] for f in direct["files"]] == ["lost.txt"]
    assert direct["base"] == row["base"]


def test_merged_then_reverted_answers_no_even_without_reflog(repo: Path) -> None:
    git_cmd(repo, "checkout", "-qb", "reverted-feature")
    write(repo, "reverted.txt", "temporary work\n")
    commit_all(repo, "add reverted work")
    git_cmd(repo, "checkout", "-q", "main")
    git_cmd(
        repo,
        "merge",
        "-q",
        "--no-ff",
        "-m",
        "merge reverted-feature",
        "reverted-feature",
    )
    merge_sha = git_cmd(repo, "rev-parse", "HEAD")
    git_cmd(repo, "revert", "--no-edit", "-m", "1", merge_sha)

    result = landed(repo, "reverted-feature")
    assert result["answer"] == "no"
    assert "reverted" in result["sentence"]

    # Must still answer "no" after reflogs are expired (cloned repo scenario).
    git_cmd(repo, "reflog", "expire", "--expire=now", "--all")
    after_expire = landed(repo, "reverted-feature")
    assert after_expire["answer"] == "no"
    assert "reverted" in after_expire["sentence"]


def test_cherry_picked_then_reverted_answers_no(repo: Path) -> None:
    git_cmd(repo, "checkout", "-qb", "picked-reverted")
    write(repo, "picked.txt", "hello\n")
    tip = commit_all(repo, "add picked.txt")
    git_cmd(repo, "checkout", "-q", "main")
    git_cmd(repo, "cherry-pick", tip)
    picked_sha = git_cmd(repo, "rev-parse", "HEAD")
    git_cmd(repo, "revert", "--no-edit", picked_sha)

    result = landed(repo, "picked-reverted")
    assert result["answer"] == "no"


def test_same_content_at_another_path_is_not_counted_as_landed(repo: Path) -> None:
    git_cmd(repo, "checkout", "-qb", "moved-work")
    write(repo, "lib/helper.py", "def helper():\n    return 42\n")
    commit_all(repo, "add lib/helper.py")
    git_cmd(repo, "checkout", "-q", "main")
    write(repo, "src/helper.py", "def helper():\n    return 42\n")
    commit_all(repo, "add src/helper.py")

    result = landed(repo, "moved-work")
    assert result["answer"] == "no"
    assert result["files"][0]["state"] == "absent"
    assert result["files"][0]["elsewhere"] == "src/helper.py"


def test_landed_immune_to_hostile_git_config(
    repo: Path, tmp_path: Path, monkeypatch
) -> None:
    git_cmd(repo, "checkout", "-qb", "unlanded-hostile")
    write(repo, "never.txt", "never merged\n")
    commit_all(repo, "never merged")
    git_cmd(repo, "checkout", "-q", "main")

    hostile = tmp_path / "hostile.gitconfig"
    hostile.write_text(
        "[color]\n\tui = always\n"
        "[diff]\n\tmnemonicPrefix = true\n\tnoprefix = true\n\trenames = copies\n"
        "[log]\n\tshowSignature = true\n\tdecorate = full\n"
        "[core]\n\tquotePath = false\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(hostile))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")

    code, out = run_cli(
        "landed", "--repo", str(repo), "--target", "main", "unlanded-hostile"
    )
    assert code == git_cli.EXIT_NO
    assert out.startswith("No.")


def test_landed_only_filter_controls_emitted_answers(repo: Path) -> None:
    git_cmd(repo, "checkout", "-qb", "only-yes")
    write(repo, "yes.txt", "yes\n")
    commit_all(repo, "yes work")
    git_cmd(repo, "checkout", "-q", "main")
    git_cmd(repo, "merge", "-q", "--ff-only", "only-yes")

    git_cmd(repo, "checkout", "-qb", "only-no")
    write(repo, "no.txt", "no\n")
    commit_all(repo, "no work")
    git_cmd(repo, "checkout", "-q", "main")

    code_yes, out_yes = run_cli(
        "landed",
        "--repo",
        str(repo),
        "--target",
        "main",
        "--addresses",
        "--only",
        "yes",
        "only-yes",
        "only-no",
    )
    assert code_yes == git_cli.EXIT_NO
    assert out_yes.strip().startswith("only-yes@")
    assert "only-no" not in out_yes

    code_no, out_no = run_cli(
        "landed",
        "--repo",
        str(repo),
        "--target",
        "main",
        "--addresses",
        "--only",
        "no",
        "only-yes",
        "only-no",
    )
    assert code_no == git_cli.EXIT_NO
    assert out_no.strip().startswith("only-no@")
    assert "only-yes" not in out_no
