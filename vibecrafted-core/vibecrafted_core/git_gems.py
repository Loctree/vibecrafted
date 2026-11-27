"""Gems: valuable work that never reached the target, wherever it lives.

Sources: local and remote branches, stash entries, checkouts with uncommitted
files or detached commits, commits reachable only from a reflog, and copies
kept by ``vc-git save``. Every result is an address.

A gem is work whose content is *not* in the target, measured with
:func:`~vibecrafted_core.git_landed.landed` - a squash-merged branch is not a
gem even though Git calls it unmerged. Work held by another ref is reported
with that carrier instead of as a separate gem. Ranking puts work that exists
in only one copy first, because a single mistake can destroy it.
"""

from __future__ import annotations

import fnmatch
import json
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from .git_address import (
    SHORT,
    AddressError,
    Unestablished,
    Work,
    git,
    git_out,
    integration_lines,
    repo_name,
    resolve,
    unreachable_part,
)
from .git_landed import UNKNOWN, YES, TargetView, landed
from .git_worktrees import _registered

# Higher rank = more urgent. The reason names what a single mistake costs.
TIERS = {
    "reflog-only": (4, "only in the reflog: Git deletes it when the reflog expires"),
    "uncommitted": (
        3,
        "uncommitted files: one checkout, reset or worktree removal destroys them",
    ),
    "stash": (3, "only in the stash: one drop or clear destroys it"),
    "unpushed": (2, "commits on no remote: deleting the branch loses them"),
    "pushed": (1, "a copy exists on a remote"),
}


def harbor_root() -> Path:
    from .runtime_paths import vibecrafted_home

    return vibecrafted_home() / "harbor"


def harbor_copies(repo: str) -> dict[str, list[str]]:
    """``patch-id or tip -> [patch addresses]`` for copies kept in the harbor."""
    copies: dict[str, list[str]] = {}
    folder = harbor_root() / repo
    if not folder.is_dir():
        return copies
    for manifest in folder.rglob("*.json"):
        try:
            doc = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if (
            not isinstance(doc, dict)
            or doc.get("schema") != "vibecrafted.vc-git.saved-patch.v1"
        ):
            continue
        for key in ("patch_id", "tip"):
            value = doc.get(key)
            if isinstance(value, str) and value:
                copies.setdefault(value, []).append(f"patch:{doc.get('patch')}")
    return copies


def _short(ref: str) -> str:
    return ref.removeprefix("refs/heads/").removeprefix("refs/remotes/")


def _reachable(root: Path, *rev_args: str) -> set[str]:
    result = git(root, "rev-list", *rev_args)
    if result.returncode:
        raise Unestablished(f"rev-list failed: {result.stderr.strip()}")
    return set(result.stdout.split())


def _branch_candidates(
    root: Path, target_sha: str, lines: list[tuple[str, str]], remote: str | None
) -> tuple[list[tuple[str, list[str]]], int, int]:
    """Independent unmerged tips with every ref that points at them.

    Returns ``([(tip, refs)], carried_by_refs, carried_by_lines)``.
    """
    patterns = ["refs/heads"] + (
        [f"refs/remotes/{remote}"] if remote else ["refs/remotes"]
    )
    raw = git_out(
        root,
        "for-each-ref",
        f"--no-merged={target_sha}",
        "--format=%(refname)%00%(objectname)%00%(symref)",
        *patterns,
    )
    ref_sha = {}
    for line in raw.splitlines():
        parts = line.split("\0")
        if len(parts) == 3 and not parts[2]:
            ref_sha[parts[0]] = parts[1]
    carried_by_line = set()
    for _name, line_sha in lines[1:]:
        merged = git_out(
            root,
            "for-each-ref",
            f"--merged={line_sha}",
            "--format=%(refname)",
            *patterns,
        )
        carried_by_line.update(
            ref for ref in merged.split() if ref in ref_sha and ref_sha[ref] != line_sha
        )
    by_tip: dict[str, list[str]] = {}
    for ref, sha in ref_sha.items():
        if ref not in carried_by_line:
            by_tip.setdefault(sha, []).append(ref)
    tips = sorted(by_tip)
    independent = (
        set(git_out(root, "merge-base", "--independent", *tips).split())
        if len(tips) > 1
        else set(tips)
    )
    result = []
    carried = 0
    for tip in tips:
        refs = sorted(by_tip[tip], key=lambda r: (not r.startswith("refs/heads/"), r))
        if tip in independent:
            result.append((tip, refs))
        else:
            carried += len(refs)
    return result, carried, len(carried_by_line)


def _haystack(root: Path, work: Work, lines: list[tuple[str, str]]) -> str:
    """Names, subjects and paths a query can match, read cheaply."""
    parts = [work.label, work.address, work.subject]
    if work.worktree is not None:
        status = git(work.worktree, "status", "--porcelain=v1", "--untracked-files=all")
        parts.append(status.stdout)
    if work.kind == "stash" and work.tip:
        parts.append(
            git(
                root, "stash", "show", "--name-only", "--include-untracked", work.tip
            ).stdout
        )
    if work.tip and work.kind != "stash":
        log = git(
            root,
            "log",
            "--format=%s%n%b",
            "--name-only",
            "-n200",
            work.tip,
            "--not",
            *[sha for _, sha in lines],
        )
        parts.append(log.stdout)
    return "\n".join(parts).lower()


def find_gems(
    root: Path,
    target: str,
    target_sha: str,
    *,
    query: list[str] | None = None,
    remote: str | None = None,
    since: int | None = None,
    until: int | None = None,
    author: str | None = None,
    agent: str | None = None,
    path_glob: str | None = None,
    limit: int = 20,
    workers: int = 8,
) -> dict[str, Any]:
    """Search every place work can hide and rank what has not landed."""
    started = time.monotonic()
    unreadable: list[dict[str, str]] = []

    def read(source: str, action: Any, default: Any = None) -> Any:
        try:
            return action()
        except (Unestablished, AddressError, RuntimeError, OSError) as exc:
            unreadable.append({"source": source, "error": str(exc)})
            return default

    lines = integration_lines(root, target, target_sha)
    branch_tips, carried_refs, carried_lines = read(
        "branches",
        lambda: _branch_candidates(root, target_sha, lines, remote),
        ([], 0, 0),
    )
    on_remote = read(
        "remote copies",
        lambda: _reachable(root, "--remotes", "--not", target_sha),
        set(),
    )
    saved = read(
        "saved copies",
        lambda: _reachable(root, "--glob=refs/vc-git/saved/*", "--not", target_sha),
        set(),
    )

    # Each source yields (address text, tier, aliases).
    pending: list[tuple[str, str, list[str]]] = []
    for tip, refs in branch_tips:
        tier = "pushed" if tip in on_remote else "unpushed"
        pending.append((f"{refs[0]}@{tip}", tier, [_short(r) for r in refs[1:]]))

    stash_shas = read(
        "stash", lambda: git_out(root, "stash", "list", "--format=%H").split(), []
    )
    for index in range(len(stash_shas)):
        pending.append((f"stash@{{{index}}}", "stash", []))

    def worktree_state(entry: dict[str, str]) -> tuple[str, str] | None:
        location = Path(entry.get("worktree", ""))
        if "prunable" in entry or not location.is_dir():
            return None
        status = git(
            location, "status", "--porcelain=v1", "-z", "--untracked-files=all"
        )
        if status.returncode:
            unreadable.append(
                {"source": f"wt:{location}", "error": "git status failed"}
            )
            return None
        if status.stdout.strip("\0"):
            return f"wt:{location}", "uncommitted"
        tip = entry.get("HEAD", "")
        if (
            not entry.get("branch")
            and tip
            and tip not in on_remote
            and git(root, "merge-base", "--is-ancestor", tip, target_sha).returncode
            == 1
        ):
            return f"wt:{location}", "unpushed"
        return None

    entries = read("worktrees", lambda: _registered(root), [])
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        for found in pool.map(worktree_state, entries):
            if found:
                pending.append((found[0], found[1], []))

    # Commits reachable only from a reflog: amend and rebase leave the old
    # version behind with the same author and author date. Those are
    # superseded rewrites, not lost work.
    authored = read(
        "rewrite detection",
        lambda: {
            tuple(line.split("\0")[1:]): line.split("\0")[0]
            for line in git_out(
                root, "log", "--all", "--format=%H%x00%ae%x00%at"
            ).splitlines()
            if line.count("\0") == 2
        },
        {},
    )
    reflog = read(
        "reflog",
        lambda: git_out(
            root, "rev-list", "--reflog", "--parents", "--not", "--all", *stash_shas
        ),
        "",
    )
    shas: set[str] = set()
    parents: set[str] = set()
    for row in reflog.splitlines():
        ids = row.split()
        if ids:
            shas.add(ids[0])
            parents.update(ids[1:])
    superseded = 0
    recreatable = 0
    for sha in sorted(shas - parents):
        if git(root, "merge-base", "--is-ancestor", sha, target_sha).returncode != 1:
            continue
        _boundary, own = unreachable_part(root, sha)
        rewritten = [authored.get((email, stamp)) for _, email, stamp in own]
        if own and all(rewritten):
            superseded += 1
            continue
        own_ids = {commit for commit, _, _ in own}
        merges_only = bool(own)
        for commit, _, _ in own:
            parents_of = git(
                root, "rev-list", "--parents", "-n1", commit
            ).stdout.split()[1:]
            if len(parents_of) < 2 or any(parent in own_ids for parent in parents_of):
                merges_only = False
                break
        if merges_only:
            # Only a merge of lines that all survive in refs: Git can redo it.
            recreatable += 1
            continue
        pending.append((sha, "reflog-only", []))

    def admit(
        item: tuple[str, str, list[str]],
    ) -> tuple[Work, str, list[str], list[str]] | None:
        text, tier, aliases = item
        try:
            work = resolve(root, text)
        except (Unestablished, AddressError) as exc:
            unreadable.append({"source": text, "error": str(exc)})
            return None
        if tier == "reflog-only":
            work.label = f"reflog-only {work.tip[:SHORT] if work.tip else ''}"
        if since and work.when and work.when < since:
            return None
        if until and work.when and work.when > until:
            return None
        if (author or agent) and work.tip:
            info = git(
                root, "show", "-s", "--format=%an%x00%ae%x00%B", work.tip
            ).stdout.lower()
            if author and author.lower() not in info:
                return None
            if (
                agent
                and f"authored-by: {agent.lower()}" not in info
                and f"[{agent.lower()}/" not in info
            ):
                return None
        matched: list[str] = []
        if query:
            hay = _haystack(root, work, lines)
            if not all(term.lower() in hay for term in query):
                return None
            matched = [f"'{term}'" for term in query]
        return work, tier, aliases, matched

    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        admitted = [a for a in pool.map(admit, pending) if a is not None]

    harbor = harbor_copies(repo_name(root))

    def evaluate(item: tuple[Work, str, list[str], list[str]]) -> dict[str, Any] | None:
        work, tier, aliases, matched = item
        try:
            verdict = landed(work, view, lines)
        except (Unestablished, AddressError, RuntimeError) as exc:
            verdict = {
                "address": work.address,
                "kind": work.kind,
                "label": work.label,
                "subject": work.subject,
                "tip": work.tip,
                "when": work.when,
                "answer": UNKNOWN,
                "extent": "unknown",
                "sentence": f"cannot be established: {exc}",
                "files": [],
                "evidence": [{"source": "git", "claim": str(exc)}],
            }
        not_there = [
            f["path"]
            for f in verdict["files"]
            if f.get("state") not in {"identical", "present"}
        ]
        if (
            path_glob
            and verdict["answer"] != YES
            and not any(fnmatch.fnmatch(p, path_glob) for p in not_there)
        ):
            return None
        if work.tip and verdict.get("base") and work.worktree is None:
            verdict["shortstat"] = git(
                root, "diff", "--shortstat", verdict["base"], work.tip
            ).stdout.strip()
        copies = []
        if work.tip and work.tip in on_remote and work.worktree is None:
            copies.append("remote")
        if work.tip and work.tip in saved and work.worktree is None:
            copies.append("saved")
        harbored = sorted(
            {
                a
                for key in (
                    verdict.get("patch_id"),
                    work.tip if work.worktree is None else None,
                )
                if key
                for a in harbor.get(key, [])
            }
        )
        if harbored:
            copies.append("harbor")
            verdict["harbor"] = harbored
        verdict.update(
            tier=tier, copies=copies, aliases=aliases, matched=matched, when=work.when
        )
        return verdict

    with TargetView(root, target, target_sha) as view:
        _ = (
            view.tree,
            view.patch_ids,
            view.traces,
            view.history,
            view.trees,
            view.blobs,
        )  # warm caches before threads
        with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
            results = [r for r in pool.map(evaluate, admitted) if r is not None]

    landed_by_content = [r for r in results if r["answer"] == YES]
    gems = [r for r in results if r["answer"] != YES]
    now = time.time()

    def size(row: dict[str, Any]) -> int:
        digits = [
            int(p)
            for p in row.get("shortstat", "").replace(",", " ").split()
            if p.isdecimal()
        ]
        if len(digits) > 1:
            return sum(digits[1:])
        return 10 * len(
            [
                f
                for f in row.get("files", [])
                if f.get("state") not in {"identical", "present"}
            ]
        )

    for row in gems:
        rank, reason = TIERS.get(row["tier"], (0, "unknown"))
        row["risk"] = reason
        row["single_copy"] = rank >= 2 and not row["copies"]
        age_days = max(0.0, (now - (row.get("when") or now)) / 86400)
        row["score"] = round(
            (rank if row["single_copy"] or rank < 2 else 1) * 1000
            + min(size(row), 5000) / (1 + age_days / 30),
            1,
        )
    gems.sort(key=lambda r: (-r["score"], r["address"]))
    return {
        "schema": "vibecrafted.vc-git.gems.v1",
        "repo": str(root),
        "target": target,
        "target_sha": target_sha,
        "integration_lines": [{"name": n, "sha": s} for n, s in lines],
        "query": query or [],
        "searched": {
            "candidates": len(admitted),
            "carried_by_other_branches": carried_refs,
            "carried_by_integration_lines": carried_lines,
            "landed_by_content": len(landed_by_content),
            "superseded_rewrites": superseded,
            "recreatable_merges": recreatable,
            "seconds": round(time.monotonic() - started, 1),
        },
        "landed_by_content": [
            {
                "address": r["address"],
                "sentence": r["sentence"],
                "evidence": r["evidence"][-1:],
            }
            for r in landed_by_content
        ],
        "unreadable": unreadable,
        "total_gems": len(gems),
        "single_copy": sum(1 for r in gems if r["single_copy"]),
        "gems": gems[:limit] if limit else gems,
    }
