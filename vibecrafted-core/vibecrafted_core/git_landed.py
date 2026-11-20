"""Did that work land? Content comparison with graded, sourced answers.

Git answers "is this commit an ancestor of that one". After a squash merge, a
cherry-pick or a plain file copy the honest answer is *yes* while ancestry says
*no*. This module answers the question people ask, from the cheapest strong
evidence to the most detailed:

1. ancestry                      -> yes (git)
2. patch identity per commit     -> yes when every commit was cherry-picked
3. patch identity of the whole   -> yes when one target commit is the squash
4. per file, against the target  -> identical / present / absent / unknown

Per file, the change is checked in both directions against an index built from
the target tree (a temporary index file; the repository is never written):

* ``identical`` - the target holds exactly the content the work produces;
* ``present``   - the reverse patch applies, the forward patch does not:
                  the target already contains the change;
* ``absent``    - the forward patch applies, the reverse does not:
                  the target lacks the change;
* ``unknown``   - both apply (ambiguous) or neither (the file diverged).

The answer has three values that are never folded into each other:
``yes`` (everything measured as there), ``no`` (at least one file measured as
missing, possibly "partly") and ``unknown`` (cannot be established).
Explicit traces such as ``(cherry picked from commit X)`` are *declared*
evidence: they are reported, but measured content decides the answer.
"""

from __future__ import annotations

import re
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Self

from .git_address import (
    DIFF_FLAGS,
    EMPTY_TREE,
    SHORT,
    AddressError,
    FileChange,
    Unestablished,
    Work,
    _name_status,
    changes,
    commit_of,
    creation_point,
    file_patch,
    git,
    git_out,
    split_patch,
    tree_entries,
)
from .git_worktrees import _git_env

YES, NO, UNKNOWN = "yes", "no", "unknown"
PER_COMMIT_LIMIT = 300
TARGET_HISTORY = 5000
_CHERRY = re.compile(r"cherry picked from commit ([0-9a-f]{7,64})")
_APPLY_ERROR = re.compile(
    r"^error: (?:patch failed: (?P<a>.+):\d+|(?P<b>.+): (?:patch does not apply|already exists in index|does not exist in index|does not match index))$"
)


@dataclass
class TargetView:
    """Everything about the target that is reused across many questions."""

    root: Path
    name: str
    sha: str
    tmp: tempfile.TemporaryDirectory[str] = field(init=False)
    index: str = field(init=False)
    _tree: dict[str, tuple[str, str]] | None = field(default=None, init=False)
    _patch_ids: dict[str, str] | None = field(default=None, init=False)
    _traces: dict[str, str] | None = field(default=None, init=False)
    _blobs: dict[str, list[str]] | None = field(default=None, init=False)
    _history: dict[tuple[str, str], str] | None = field(default=None, init=False)
    _trees: dict[str, str] | None = field(default=None, init=False)
    history_truncated: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="vc-git-target-")
        self.index = str(Path(self.tmp.name) / "target.index")
        built = git(
            self.root, "read-tree", self.sha, env={"GIT_INDEX_FILE": self.index}
        )
        if built.returncode:
            raise Unestablished(
                f"cannot read target tree {self.name}: {built.stderr.strip()}"
            )

    def close(self) -> None:
        self.tmp.cleanup()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    @property
    def tree(self) -> dict[str, tuple[str, str]]:
        if self._tree is None:
            self._tree = tree_entries(self.root, self.sha)
        return self._tree

    @property
    def patch_ids(self) -> dict[str, str]:
        """``patch-id -> commit`` for target history (non-merge commits)."""
        if self._patch_ids is None:
            log = git_out(
                self.root,
                "log",
                "-p",
                "--no-merges",
                "--no-color",
                "--no-ext-diff",
                "--no-renames",
                f"-n{TARGET_HISTORY}",
                self.sha,
            )
            self.history_truncated = (
                int(
                    git_out(
                        self.root, "rev-list", "--count", "--no-merges", self.sha
                    ).strip()
                    or 0
                )
                > TARGET_HISTORY
            )
            ids = git_out(self.root, "patch-id", "--stable", input=log)
            self._patch_ids = {}
            for line in ids.splitlines():
                parts = line.split()
                if len(parts) == 2:
                    self._patch_ids.setdefault(parts[0], parts[1])
        return self._patch_ids

    @property
    def traces(self) -> dict[str, str]:
        """Declared traces in target history: source commit -> target commit."""
        if self._traces is None:
            self._traces = {}
            log = git_out(
                self.root,
                "log",
                f"-n{TARGET_HISTORY}",
                "--format=%H%x00%B%x1e",
                self.sha,
            )
            for record in log.split("\x1e"):
                sha, _, body = record.strip().partition("\0")
                for match in _CHERRY.finditer(body):
                    self._traces.setdefault(match.group(1), sha)
        return self._traces

    def applies(self, patch: str, *, reverse: bool) -> bool | None:
        """Does ``patch`` apply to the target tree? ``None`` if Git could not tell."""
        if not patch.strip():
            return None
        result = self._check(patch, reverse)
        if result.returncode == 0:
            return True
        return False if result.returncode == 1 else None

    def _check(self, patch: str, reverse: bool) -> Any:
        args = ["apply", "--cached", "--check", "--whitespace=nowarn"]
        if reverse:
            args.append("--reverse")
        return git(
            self.root, *args, "-", input=patch, env={"GIT_INDEX_FILE": self.index}
        )

    def applies_each(
        self, sections: dict[str, str], *, reverse: bool
    ) -> dict[str, bool | None]:
        """Per-path apply result for many file sections in one Git call.

        ``git apply --check`` reports every failing path; any failure line that
        cannot be mapped to a known path falls back to one call per path.
        """
        verdicts: dict[str, bool | None] = {}
        live = {path: text for path, text in sections.items() if text.strip()}
        for path in sections.keys() - live.keys():
            verdicts[path] = None
        if not live:
            return verdicts
        result = self._check("".join(live.values()), reverse)
        if result.returncode == 0:
            verdicts.update({path: True for path in live})
            return verdicts
        failing: set[str] = set()
        mapped = result.returncode == 1
        for line in result.stderr.splitlines():
            match = _APPLY_ERROR.match(line)
            path = match.group("a") or match.group("b") if match else None
            if path in live:
                failing.add(path)
            elif line.startswith("error:"):
                mapped = False
        if mapped and failing:
            verdicts.update({path: path not in failing for path in live})
            return verdicts
        for path, text in live.items():
            verdicts[path] = self.applies(text, reverse=reverse)
        return verdicts

    @property
    def history(self) -> dict[tuple[str, str], str]:
        """``(path, blob) -> first target commit that held it`` over target history.

        Lets a file count as landed when the target held exactly the work's
        content at some point and has changed it since.
        """
        if self._history is None:
            self._history = {}
            log = git_out(
                self.root,
                "log",
                "--format=%x00%H",
                "--raw",
                "--no-abbrev",
                "--no-renames",
                "--no-merges",
                f"-n{TARGET_HISTORY}",
                self.sha,
            )
            commit = ""
            for line in log.splitlines():
                if line.startswith("\0"):
                    commit = line[1:]
                elif line.startswith(":") and "\t" in line:
                    meta, _, path = line.partition("\t")
                    parts = meta.split()
                    if len(parts) >= 4:
                        # Older commits come later; keep the earliest holder.
                        self._history[(path, parts[3])] = commit
        return self._history

    @property
    def trees(self) -> dict[str, str]:
        """``tree -> target commit`` for every commit in target history."""
        if self._trees is None:
            self._trees = {}
            log = git_out(
                self.root, "log", "--format=%T %H", f"-n{TARGET_HISTORY}", self.sha
            )
            for line in log.splitlines():
                tree, _, commit = line.partition(" ")
                self._trees[tree] = commit
        return self._trees

    @property
    def blobs(self) -> dict[str, list[str]]:
        """``oid -> [paths]`` in the target, to recognise moved content."""
        if self._blobs is None:
            self._blobs = {}
            for path, (_mode, oid) in self.tree.items():
                self._blobs.setdefault(oid, []).append(path)
        return self._blobs

    def contents(self, oids: list[str]) -> dict[str, str]:
        """Read target blobs in one ``cat-file --batch`` call (text, lossy)."""
        if not oids:
            return {}
        result = subprocess.run(
            [
                "git",
                "-c",
                "core.fsmonitor=false",
                "-c",
                "core.untrackedCache=false",
                "cat-file",
                "--batch",
            ],
            cwd=self.root,
            input=("\n".join(oids) + "\n").encode(),
            capture_output=True,
            check=False,
            env=_git_env(),
        )
        data = result.stdout
        texts: dict[str, str] = {}
        position = 0
        while position < len(data):
            newline = data.index(b"\n", position)
            header = data[position:newline].decode(errors="replace").split()
            position = newline + 1
            if len(header) < 3 or header[1] == "missing":
                continue
            size = int(header[2])
            texts[header[0]] = data[position : position + size].decode(
                "utf-8", errors="replace"
            )
            position += size + 1
        return texts


def _patch_id(root: Path, patch: str) -> str | None:
    if not patch.strip():
        return None
    result = git(root, "patch-id", "--stable", input=patch)
    parts = result.stdout.split()
    return parts[0] if result.returncode == 0 and parts else None


def _commit_patch_ids(root: Path, commits: list[str]) -> dict[str, str | None]:
    if not commits:
        return {}
    log = git_out(
        root,
        "log",
        "-p",
        "--no-walk=unsorted",
        "--no-color",
        "--no-ext-diff",
        "--no-renames",
        *commits,
    )
    ids: dict[str, str | None] = {sha: None for sha in commits}
    for line in git_out(root, "patch-id", "--stable", input=log).splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1] in ids:
            ids[parts[1]] = parts[0]
    return ids


def _same(post: Any, target: tuple[str, str] | None) -> bool | None:
    if post == "unknown":
        return None
    if post is None or target is None:
        return post is None and target is None
    mode, oid = post
    if mode == "unknown-mode":
        return oid == target[1] or None
    return (mode, oid) == target


def _containment(section: str, target_text: str | None) -> dict[str, Any]:
    """How many of the change's added lines already appear in the target file.

    A hint, never a verdict: it explains a diverged file, it does not settle it.
    """
    added = [
        line[1:].strip()
        for line in section.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    ]
    removed = [
        line[1:].strip()
        for line in section.splitlines()
        if line.startswith("-") and not line.startswith("---")
    ]
    added = [line for line in added if len(line) > 3]
    removed = [line for line in removed if len(line) > 3]
    present = {line.strip() for line in (target_text or "").splitlines()}
    found = sum(1 for line in added if line in present)
    still = sum(1 for line in removed if line in present)
    return {
        "added_found": found,
        "added": len(added),
        "removed_still_there": still,
        "removed": len(removed),
    }


def _classify(
    view: TargetView,
    files: list[FileChange],
    sections: dict[str, str],
    *,
    base_tree: dict[str, tuple[str, str]] | None = None,
) -> dict[str, dict[str, Any]]:
    """Per-file verdicts for files not already proven identical."""
    verdicts: dict[str, dict[str, Any]] = {}
    pending: list[FileChange] = []
    for item in files:
        post = item.post
        held = (
            view.history.get((item.path, post[1])) if isinstance(post, tuple) else None
        )
        # Only count historical presence as landed when the target did not revert
        # the path right back to the work's pre-image.
        reverted_to_base = base_tree is not None and view.tree.get(
            item.path
        ) == base_tree.get(item.path)
        if held and not reverted_to_base:
            verdicts[item.path] = {
                "state": "present",
                "why": f"the target held exactly this content at {held[:SHORT]} and has changed it since",
            }
            continue
        if isinstance(post, tuple) and item.path not in view.tree:
            elsewhere = [p for p in view.blobs.get(post[1], []) if p != item.path]
            if elsewhere:
                verdicts[item.path] = {
                    "state": "absent",
                    "why": (
                        f"the target has no {item.path} "
                        f"(same content lives at {elsewhere[0]}, not at this path)"
                    ),
                    "elsewhere": elsewhere[0],
                }
                continue
            if item.status != "D":
                verdicts[item.path] = {
                    "state": "absent",
                    "why": "the target has no such file",
                }
                continue
        pending.append(item)
    if not pending:
        return verdicts
    sections = {item.path: sections.get(item.path, "") for item in pending}
    back = view.applies_each(sections, reverse=True)
    forward = view.applies_each(sections, reverse=False)
    diverged: list[FileChange] = []
    for item in pending:
        b, f = back.get(item.path), forward.get(item.path)
        if not sections[item.path].strip():
            verdicts[item.path] = {
                "state": "unknown",
                "why": "no textual change could be produced (mode-only, submodule or unreadable)",
            }
        elif b and not f:
            verdicts[item.path] = {
                "state": "present",
                "why": "the target already contains this change (reverse patch applies)",
            }
        elif f and not b:
            verdicts[item.path] = {
                "state": "absent",
                "why": "this change still applies cleanly, so the target lacks it",
            }
        elif b and f:
            verdicts[item.path] = {
                "state": "unknown",
                "why": "ambiguous: the change both applies and reverses",
            }
        elif b is None or f is None:
            verdicts[item.path] = {
                "state": "unknown",
                "why": "Git could not check this file",
            }
        elif item.path not in view.tree:
            verdicts[item.path] = {
                "state": "absent",
                "why": "the target has no such file",
            }
        else:
            diverged.append(item)
    texts = view.contents([view.tree[item.path][1] for item in diverged])
    for item in diverged:
        hint = _containment(sections[item.path], texts.get(view.tree[item.path][1]))
        if hint["added"] and hint["added_found"] == hint["added"]:
            likely = "present"
        elif hint["added"] and hint["added_found"] == 0:
            likely = "absent"
        elif not hint["added"] and hint["removed"]:
            likely = (
                "present"
                if hint["removed_still_there"] == 0
                else "absent"
                if hint["removed_still_there"] == hint["removed"]
                else "mixed"
            )
        else:
            likely = "mixed"
        verdicts[item.path] = {
            "state": "unknown",
            "why": (
                "the file has since diverged in the target; the change neither applies nor reverses "
                f"({hint['added_found']} of {hint['added']} added lines are there, "
                f"{hint['removed_still_there']} of {hint['removed']} removed lines remain)"
            ),
            "likely": likely,
            "lines": hint,
        }
    return verdicts


def _merged_base(
    root: Path,
    work: Work,
    target_sha: str,
    base_override: str | None,
) -> tuple[str | None, str]:
    """Find the pre-image baseline of a work tip that is already an ancestor of target."""
    if base_override:
        base = commit_of(root, base_override)
        if not base:
            raise AddressError(f"--base is not a commit: {base_override}")
        return base, f"--base {base_override}"
    if work.base_hint and work.base_hint[0] != work.tip:
        return work.base_hint
    cp_sha, cp_reason = creation_point(root, work)
    if cp_sha and cp_sha != work.tip:
        return cp_sha, cp_reason
    assert work.tip
    merges = git(
        root,
        "rev-list",
        "--merges",
        "--ancestry-path",
        "--reverse",
        f"{work.tip}..{target_sha}",
    ).stdout.split()
    for merge_sha in merges[:5]:
        first_parent = commit_of(root, f"{merge_sha}^1")
        if not first_parent:
            continue
        mb = git(root, "merge-base", first_parent, work.tip).stdout.strip()
        if mb and mb != work.tip:
            return mb, f"branched from {mb[:SHORT]} before merge {merge_sha[:SHORT]}"
    parents = git(root, "rev-list", "--parents", "-n1", work.tip).stdout.split()
    if len(parents) == 2:
        return parents[1], f"parent {parents[1][:SHORT]} of {work.tip[:SHORT]}"
    if len(parents) == 1:
        return EMPTY_TREE, "root commit"
    return None, ""


def _check_reverted_ancestor(
    work: Work,
    view: TargetView,
    base_override: str | None,
) -> dict[str, Any] | None:
    """Return file-level revert findings if an ancestor work was reverted in target."""
    assert work.tip
    if work.tip == view.sha:
        return None
    base, base_reason = _merged_base(view.root, work, view.sha, base_override)
    if not base or base == work.tip:
        return None
    pairs = _name_status(
        git_out(
            view.root, "diff", "--name-status", "-z", "--no-renames", base, work.tip
        )
    )
    if not pairs:
        return None
    paths = [path for _, path in pairs]
    tip_tree = tree_entries(view.root, work.tip, paths)
    base_tree = tree_entries(view.root, base, paths) if base != EMPTY_TREE else {}
    file_rows: list[dict[str, Any]] = []
    ambiguous: list[tuple[str, str]] = []
    for status, path in pairs:
        post = None if status == "D" else tip_tree.get(path)
        pre = base_tree.get(path)
        actual = view.tree.get(path)
        if actual == post:
            file_rows.append(
                {
                    "path": path,
                    "status": status,
                    "state": "identical",
                    "why": "the target still holds this content",
                }
            )
        elif actual == pre:
            file_rows.append(
                {
                    "path": path,
                    "status": status,
                    "state": "absent",
                    "why": "reverted back to its pre-image in the target",
                }
            )
        else:
            ambiguous.append((status, path))
    if ambiguous:
        ambiguous_paths = [path for _, path in ambiguous]
        patch_text = git_out(
            view.root,
            "diff",
            *DIFF_FLAGS,
            base,
            work.tip,
            "--",
            *[f":(literal){p}" for p in ambiguous_paths],
        )
        sections: dict[str, str] = {}
        for path, _st, body, _oid in split_patch(patch_text):
            sections[path] = sections.get(path, "") + body
        forward = view.applies_each(sections, reverse=False)
        backward = view.applies_each(sections, reverse=True)
        for status, path in ambiguous:
            if forward.get(path) is True and not backward.get(path):
                file_rows.append(
                    {
                        "path": path,
                        "status": status,
                        "state": "absent",
                        "why": "change still applies cleanly onto target (reverted after merge)",
                    }
                )
            else:
                file_rows.append(
                    {
                        "path": path,
                        "status": status,
                        "state": "present",
                        "why": "in target history and evolved since merge",
                    }
                )
    reverted = [row for row in file_rows if row["state"] == "absent"]
    if not reverted:
        return None
    counts: dict[str, int] = {}
    for row in file_rows:
        counts[row["state"]] = counts.get(row["state"], 0) + 1
    return {
        "base": base,
        "base_reason": base_reason,
        "files": sorted(file_rows, key=lambda r: r["path"]),
        "counts": counts,
        "reverted": len(reverted),
        "total": len(file_rows),
    }


def landed(
    work: Work,
    view: TargetView,
    lines: list[tuple[str, str]],
    *,
    base_override: str | None = None,
) -> dict[str, Any]:
    """Answer "is ``work`` in the target?" with evidence labelled by source."""
    evidence: list[dict[str, str]] = list(work.notes)
    result: dict[str, Any] = {
        "address": work.address,
        "kind": work.kind,
        "label": work.label,
        "subject": work.subject,
        "tip": work.tip,
        "when": work.when,
        "target": view.name,
        "target_sha": view.sha,
        "evidence": evidence,
        "files": [],
    }

    def answer(value: str, extent: str, sentence: str) -> dict[str, Any]:
        result.update(answer=value, extent=extent, sentence=sentence)
        return result

    clean_tip = (
        work.tip and work.worktree is None and work.kind not in {"patch", "stash"}
    )
    if clean_tip:
        ancestor = git(view.root, "merge-base", "--is-ancestor", work.tip, view.sha)
        if ancestor.returncode == 0:
            reverted_info = _check_reverted_ancestor(work, view, base_override)
            if reverted_info is not None:
                result["base"] = reverted_info["base"]
                result["base_reason"] = reverted_info["base_reason"]
                result["files"] = reverted_info["files"]
                result["counts"] = reverted_info["counts"]
                evidence.append(
                    {
                        "source": "git",
                        "claim": (
                            f"{work.tip[:SHORT]} is an ancestor of {view.name}, "
                            f"but {reverted_info['reverted']} of {reverted_info['total']} "
                            f"changed file(s) were reverted in {view.name}"
                        ),
                    }
                )
                if reverted_info["reverted"] == reverted_info["total"]:
                    return answer(
                        NO,
                        "none",
                        (
                            f"it entered {view.name}'s history, then was reverted "
                            f"({reverted_info['reverted']} of {reverted_info['total']} file(s) reverted)"
                        ),
                    )
                return answer(
                    NO,
                    "partial",
                    (
                        f"it entered {view.name}'s history, then "
                        f"{reverted_info['reverted']} of {reverted_info['total']} file(s) were reverted"
                    ),
                )
            evidence.append(
                {
                    "source": "git",
                    "claim": f"{work.tip[:SHORT]} is an ancestor of {view.name}",
                }
            )
            return answer(YES, "all", "it is part of the target's history")
        if ancestor.returncode != 1:
            evidence.append({"source": "git", "claim": "ancestry check failed"})

    change = changes(work, lines, base_override=base_override)
    result["base"] = change.base
    result["base_reason"] = change.base_reason
    evidence.append({"source": "git", "claim": f"measured from {change.base_reason}"})
    if work.worktree is not None and work.tip:
        ahead = git(view.root, "merge-base", "--is-ancestor", work.tip, view.sha)
        if ahead.returncode == 0:
            evidence.append(
                {
                    "source": "git",
                    "claim": "its HEAD is already in the target; only uncommitted files are measured",
                }
            )
    if change.is_empty():
        return answer(YES, "empty", "it changes nothing relative to its base")

    # Guard against tree/cherry-pick/squash-then-revert: if any changed file is
    # back at its exact pre-image in target, fall through to per-file checks.
    base_tree_for_change = (
        tree_entries(view.root, change.base, [f.path for f in change.files])
        if change.base
        else {}
    )
    reverted_to_base_any = any(
        view.tree.get(item.path) == base_tree_for_change.get(item.path)
        and not _same(item.post, view.tree.get(item.path))
        for item in change.files
    )

    if clean_tip and not reverted_to_base_any:
        tree = git(view.root, "rev-parse", f"{work.tip}^{{tree}}").stdout.strip()
        holder = view.trees.get(tree)
        if holder:
            subject = git(view.root, "show", "-s", "--format=%s", holder).stdout.strip()
            evidence.append(
                {
                    "source": "git",
                    "claim": f'its tree is exactly the tree of {holder[:SHORT]} "{subject}"',
                }
            )
            result["landed_as"] = holder
            return answer(
                YES, "all", f'its exact tree arrived as {holder[:SHORT]} "{subject}"'
            )

    # Declared traces: reported, never decisive on their own.
    declared = {sha: view.traces[sha] for sha in change.commits if sha in view.traces}
    for source, target_commit in declared.items():
        evidence.append(
            {
                "source": "git-trailer",
                "claim": f"{target_commit[:SHORT]} declares it cherry-picked {source[:SHORT]}",
            }
        )

    # Patch identity: every commit, or the whole change as one squash.
    if (
        change.commits
        and work.worktree is None
        and len(change.commits) <= PER_COMMIT_LIMIT
    ):
        try:
            ids = _commit_patch_ids(view.root, change.commits)
        except Unestablished:
            ids = {}
        matched = {sha: view.patch_ids.get(pid) for sha, pid in ids.items() if pid}
        hits = {sha: target for sha, target in matched.items() if target}
        if ids and len(hits) == len(ids) and not reverted_to_base_any:
            evidence.append(
                {
                    "source": "git",
                    "claim": f"all {len(ids)} commit(s) have an identical patch in {view.name} (cherry-picked)",
                }
            )
            return answer(
                YES,
                "all",
                f"every one of its {len(ids)} commit(s) was cherry-picked into the target",
            )
        if hits:
            evidence.append(
                {
                    "source": "git",
                    "claim": (
                        f"{len(hits)} of {len(ids)} commit(s) have an identical patch in {view.name}"
                        + (
                            " (reverted in target)"
                            if len(hits) == len(ids) and reverted_to_base_any
                            else ""
                        )
                    ),
                }
            )
    full = file_patch(change, [f.path for f in change.files])
    whole = _patch_id(view.root, full)
    result["patch_id"] = whole
    if whole and whole in view.patch_ids and not reverted_to_base_any:
        squash = view.patch_ids[whole]
        subject = git(view.root, "show", "-s", "--format=%s", squash).stdout.strip()
        evidence.append(
            {
                "source": "git",
                "claim": f'{squash[:SHORT]} "{subject}" carries exactly this change (squash or copy)',
            }
        )
        result["landed_as"] = squash
        return answer(
            YES, "all", f'its whole change arrived as {squash[:SHORT]} "{subject}"'
        )

    # Per file: identical content first, then both-direction apply checks.
    states: dict[str, dict[str, Any]] = {}
    pending: list[FileChange] = []
    for item in change.files:
        if _same(item.post, view.tree.get(item.path)):
            states[item.path] = {
                "state": "identical",
                "why": "the target holds exactly this content",
            }
        else:
            pending.append(item)
    if pending:
        sections: dict[str, str] = {}
        for path, _status, body, _oid in split_patch(full):
            sections[path] = sections.get(path, "") + body
        base_tree = (
            tree_entries(view.root, change.base, [item.path for item in pending])
            if change.base
            else {}
        )
        states.update(_classify(view, pending, sections, base_tree=base_tree))

    result["files"] = [
        {"path": item.path, "status": item.status, **states[item.path]}
        for item in change.files
    ]
    counts: dict[str, int] = {}
    likely: dict[str, int] = {}
    for verdict in states.values():
        counts[verdict["state"]] = counts.get(verdict["state"], 0) + 1
        if "likely" in verdict:
            likely[verdict["likely"]] = likely.get(verdict["likely"], 0) + 1
    result["counts"] = counts
    result["likely"] = likely
    total = len(change.files)
    there = counts.get("identical", 0) + counts.get("present", 0)
    missing = counts.get("absent", 0)
    unclear = counts.get("unknown", 0)
    evidence.append(
        {
            "source": "git",
            "claim": f"per file: {there} in target, {missing} missing, {unclear} undetermined of {total}",
        }
    )
    if likely:
        evidence.append(
            {
                "source": "git",
                "claim": "line containment on diverged files (a hint, not a verdict): "
                + ", ".join(
                    f"{count} look {name}" for name, count in sorted(likely.items())
                ),
            }
        )
    hint = ""
    if unclear and likely.get("present"):
        hint = f" ({likely['present']} of those look present by their lines)"
    if there == total:
        return answer(
            YES, "all", f"all {total} changed file(s) are in the target (content match)"
        )
    if missing:
        if there:
            sentence = f"{there} of {total} files landed; {missing} did not" + (
                f"; {unclear} cannot be established{hint}" if unclear else ""
            )
            return answer(NO, "partial", sentence)
        return answer(
            NO,
            "none",
            f"none of its {total} file(s) are in the target"
            + (f"; {unclear} cannot be established{hint}" if unclear else ""),
        )
    if declared:
        evidence.append(
            {
                "source": "git-trailer",
                "claim": "a trace claims it landed, but content could not confirm it",
            }
        )
    return answer(
        UNKNOWN,
        "unknown",
        f"{there} of {total} files are in the target; {unclear} have diverged, so it cannot be established{hint}",
    )
