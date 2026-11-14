"""Founder-facing cleanup: worktrees and branches are separate, loss-free cuts."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from vibecrafted_core import git as vc_git
from vibecrafted_core.git_branches import branch_cleanup_view, remove_branches
from vibecrafted_core.git_worktrees import remove_worktrees, worktree_cleanup_view


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
    ).stdout.strip()


@pytest.fixture
def repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setenv("VIBECRAFTED_HOME", str(tmp_path / "home"))
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        monkeypatch.delenv(name, raising=False)
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-b", "main")
    _git(root, "config", "user.email", "t@example.invalid")
    _git(root, "config", "user.name", "t")
    (root / ".gitignore").write_text("target/\nnotes.local\n")
    (root / "a.txt").write_text("a\n")
    _git(root, "add", ".")
    _git(root, "commit", "-m", "base")
    monkeypatch.chdir(root)
    return root


def _add(repo: Path, name: str, *, commit: bool = False) -> Path:
    path = repo.parent / name
    _git(repo, "worktree", "add", "-b", f"cut/{name}", str(path))
    if commit:
        (path / f"{name}.txt").write_text("work\n")
        _git(path, "add", ".")
        _git(path, "commit", "-m", name)
    return path


def _verdicts(repo: Path) -> dict[str, str]:
    view = worktree_cleanup_view(repo)
    return {Path(row["path"]).name: row["verdict"] for row in view["worktrees"]}


def test_worktree_view_sorts_by_what_would_be_lost(repo: Path) -> None:
    merged = _add(repo, "merged")
    (merged / "target").mkdir()
    (merged / "target" / "out.bin").write_text("x")
    _add(repo, "ahead", commit=True)
    dirty = _add(repo, "dirty")
    (dirty / "wip.txt").write_text("unsaved\n")
    local = _add(repo, "local")
    (local / "notes.local").write_text("mine\n")

    assert _verdicts(repo) == {
        "repo": "in_use",
        "merged": "removable",
        "ahead": "removable",
        "dirty": "keep",
        "local": "local_files",
    }


def test_worktree_removal_keeps_branches_and_unsaved_work(repo: Path) -> None:
    ahead = _add(repo, "ahead", commit=True)
    dirty = _add(repo, "dirty")
    (dirty / "wip.txt").write_text("unsaved\n")
    local = _add(repo, "local")
    (local / "notes.local").write_text("mine\n")

    result = remove_worktrees(repo, [str(ahead), str(dirty), str(local)])

    assert [Path(p).name for p in result["removed"]] == ["ahead"]
    assert not ahead.exists() and dirty.exists() and local.exists()
    assert "cut/ahead" in _git(repo, "branch", "--list", "cut/ahead")
    assert remove_worktrees(repo, [str(local)], with_ignored=True)["removed"]
    assert not local.exists()


def test_worktree_cleanup_cli_never_removes_without_consent(
    repo: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    merged = _add(repo, "merged")

    assert vc_git.main(["worktrees", "cleanup", str(repo), "--dry-run"]) == 0
    assert vc_git.main(["worktrees", "cleanup", str(repo)]) == 0  # no tty, no --yes
    assert merged.exists()
    assert "Re-run with --yes" in capsys.readouterr().out

    assert vc_git.main(["worktrees", "prune", str(repo), "--yes"]) == 0
    assert not merged.exists()
    assert "cut/merged" in _git(repo, "branch", "--list", "cut/merged")


def test_worktree_cleanup_drops_registrations_of_deleted_directories(
    repo: Path,
) -> None:
    gone = _add(repo, "gone")
    subprocess.run(["rm", "-rf", str(gone)], check=True)

    assert _verdicts(repo)["gone"] == "missing"
    assert vc_git.main(["worktrees", "cleanup", str(repo), "--yes"]) == 0
    assert str(gone) not in _git(repo, "worktree", "list")


def test_branch_cleanup_removes_only_fully_merged_names(repo: Path) -> None:
    _git(repo, "branch", "done")
    _git(repo, "branch", "release/v1")
    _git(repo, "checkout", "-q", "-b", "unmerged")
    (repo / "u.txt").write_text("u\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "u")
    _git(repo, "checkout", "-q", "main")
    held = _add(repo, "held")

    view = branch_cleanup_view(repo)
    verdicts = {row["name"]: row["verdict"] for row in view["branches"]}
    assert verdicts == {
        "main": "protected",
        "release/v1": "protected",
        "done": "removable",
        "unmerged": "keep",
        "cut/held": "in_use",
    }

    assert remove_branches(repo, view)["removed"] == ["local:done"]
    assert _git(repo, "branch", "--format=%(refname:short)").split() == [
        "cut/held",
        "main",
        "release/v1",
        "unmerged",
    ]
    assert held.exists()


def test_branch_cleanup_refuses_a_branch_that_moved_after_listing(repo: Path) -> None:
    _git(repo, "branch", "done")
    view = branch_cleanup_view(repo)
    (repo / "late.txt").write_text("late\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "late")
    _git(repo, "branch", "-f", "done", "HEAD")

    result = remove_branches(repo, view)

    assert result["removed"] == [] and result["refused"]
    assert _git(repo, "branch", "--list", "done")


def test_branch_cleanup_touches_the_remote_only_when_asked(
    repo: Path, tmp_path: Path
) -> None:
    origin = tmp_path / "origin.git"
    _git(tmp_path, "init", "--bare", "-b", "main", str(origin))
    _git(repo, "remote", "add", "origin", str(origin))
    _git(repo, "branch", "done")
    _git(repo, "push", "-q", "origin", "main", "done")

    assert vc_git.main(["branches", "cleanup", str(repo), "--yes"]) == 0
    assert "done" in _git(origin, "branch", "--list", "done")

    assert (
        vc_git.main(["branches", "cleanup", str(repo), "--also-remote", "--yes"]) == 0
    )
    assert _git(origin, "branch", "--format=%(refname:short)").split() == ["main"]
