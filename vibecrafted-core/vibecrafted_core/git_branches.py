"""Branch cleanup for the person at the terminal.

A branch is removable only when its tip is already an ancestor of the target,
so deleting the name loses no commit. Everything else is listed and kept.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .git import _require_git_root
from .git_worktrees import _registered, _run

_PROTECTED = ("main", "master", "develop", "trunk")
_PROTECTED_PREFIXES = ("release/", "recovery/", "archive/")


def _protected(name: str) -> bool:
    return name in _PROTECTED or name.startswith(_PROTECTED_PREFIXES)


def _refs(root: Path, prefix: str) -> dict[str, str]:
    result = _run(root, "for-each-ref", "--format=%(refname)%00%(objectname)", prefix)
    if result.returncode:
        raise RuntimeError(f"cannot list {prefix}: {result.stderr.strip()}")
    pairs = (line.split("\0") for line in result.stdout.splitlines() if line)
    return {ref.removeprefix(prefix): sha for ref, sha in pairs}


def branch_cleanup_view(
    project: str | Path = ".",
    *,
    target: str | None = None,
    also_remote: bool = False,
    remote: str = "origin",
) -> dict[str, Any]:
    """Sort local (and optionally remote) branches into removable and kept."""
    root = _require_git_root(Path(project).expanduser().resolve())
    resolved = _run(root, "rev-parse", "--verify", f"{target or 'HEAD'}^{{commit}}")
    if resolved.returncode:
        raise RuntimeError(f"target is not a commit: {target or 'HEAD'}")
    target_sha = resolved.stdout.strip()
    current = _run(root, "symbolic-ref", "-q", "--short", "HEAD").stdout.strip()
    target_name = (target or current).removeprefix(f"{remote}/")
    checked_out = {
        entry["branch"].removeprefix("refs/heads/"): entry["worktree"]
        for entry in _registered(root)
        if entry.get("branch", "").startswith("refs/heads/")
    }

    def merged(sha: str) -> bool:
        return (
            _run(root, "merge-base", "--is-ancestor", sha, target_sha).returncode == 0
        )

    def verdict(name: str, sha: str, *, local: bool) -> tuple[str, str]:
        if _protected(name) or name == target_name:
            return "protected", "trunk, release or target branch"
        if local and name in checked_out:
            return "in_use", f"checked out in {checked_out[name]}"
        if not local and name in checked_out:
            return "in_use", "its local branch is checked out in a worktree"
        if merged(sha):
            return "removable", "fully contained in the target"
        return "keep", "has commits the target does not contain"

    rows: list[dict[str, Any]] = []
    for name, sha in sorted(_refs(root, "refs/heads/").items()):
        kind, why = verdict(name, sha, local=True)
        rows.append(
            {"scope": "local", "name": name, "head": sha, "verdict": kind, "why": why}
        )
    if also_remote:
        fetched = _run(root, "fetch", "--prune", remote)
        if fetched.returncode:
            raise RuntimeError(f"cannot refresh {remote}: {fetched.stderr.strip()}")
        for name, sha in sorted(_refs(root, f"refs/remotes/{remote}/").items()):
            if name == "HEAD":
                continue
            kind, why = verdict(name, sha, local=False)
            rows.append(
                {
                    "scope": remote,
                    "name": name,
                    "head": sha,
                    "verdict": kind,
                    "why": why,
                }
            )
    return {
        "schema": "vibecrafted.branch-cleanup-view.v1",
        "root": str(root),
        "target": target or current or "HEAD",
        "target_sha": target_sha,
        "remote": remote if also_remote else None,
        "branches": rows,
    }


def remove_branches(project: str | Path, view: dict[str, Any]) -> dict[str, Any]:
    """Delete the removable branches of a view, pinned to the tips it showed."""
    root = _require_git_root(Path(project).expanduser().resolve())
    removed: list[str] = []
    refused: list[dict[str, str]] = []
    for row in view["branches"]:
        if row["verdict"] != "removable":
            continue
        label = f"{row['scope']}:{row['name']}"
        if row["scope"] == "local":
            # The expected old value makes Git refuse a branch that moved.
            result = _run(
                root, "update-ref", "-d", f"refs/heads/{row['name']}", row["head"]
            )
        else:
            result = _run(
                root,
                "push",
                row["scope"],
                f"--force-with-lease=refs/heads/{row['name']}:{row['head']}",
                f":refs/heads/{row['name']}",
            )
        if result.returncode:
            refused.append({"branch": label, "reason": result.stderr.strip()})
        else:
            removed.append(label)
    return {
        "schema": "vibecrafted.branch-cleanup-result.v1",
        "removed": removed,
        "refused": refused,
    }
