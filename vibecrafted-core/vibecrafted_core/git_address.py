"""Work addresses: one written form for every piece of work ``vc-git`` handles.

A branch, a commit, a stash entry, a saved patch, a dirty worktree, a pull
request and an agent run are all *a piece of work that lives somewhere*.
Commands that find work print addresses; commands that measure or move work
accept them. Addresses printed by a query are pinned to the tip they saw
(``feat-x@1a2b3c4d5e``) so a later act cannot silently act on different work.

Grammar (one address per argument, or ``-`` to read one per line from stdin)::

    feat-x  feat-x@1a2b3c4d5e          local branch, optionally pinned
    origin/feat-x@1a2b3c4d5e           remote-tracking branch
    1a2b3c4d5e6f                       any commit
    stash@{2}  stash@{2}@1a2b3c4d5e    stash entry (the pin survives renumbering)
    saved:NAME@1a2b3c4d5e              copy kept by ``vc-git save --to commit``
    wt:/path/to/worktree  wt:.         a checkout, including uncommitted files
    patch:/path/to/file.patch          a unified diff on disk
    run:RUN_ID                         a Vibecrafted run (its worktree or branch)
    pr:412                             a GitHub pull request head (read via gh)

Everything here only *reads* the repository. Content is taken from Git objects
and from the working tree without writing objects, refs or the index.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .git import _require_git_root
from .git_worktrees import _path_key, _run, refuse_repo_env_overrides

EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
SHORT = 10
TRUNK_NAMES = ("main", "master", "develop", "trunk", "dev")
_HEX = re.compile(r"[0-9a-f]{4,64}")
_PINNED = re.compile(r"^(?P<name>.+?)@(?P<pin>[0-9a-f]{7,64})$")
_STASH = re.compile(r"^stash@\{(?P<n>\d+)\}(?:@(?P<pin>[0-9a-f]{7,64}))?$")
_SAFE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*")
DIFF_FLAGS = (
    "--no-ext-diff",
    "--no-textconv",
    "--no-color",
    "--no-renames",
    "--binary",
    "--full-index",
)


class AddressError(RuntimeError):
    """The text is not an address, or names something that does not exist."""


class Unestablished(RuntimeError):
    """The address is valid but its content cannot be read right now."""


@dataclass
class FileChange:
    """One path changed by a piece of work, and what the work makes of it."""

    path: str
    status: str  # A, M, D, T (Git letters); U for unknown
    # (mode, oid) after the work; None when the work deletes the path;
    # the string "unknown" when the post-image cannot be named without writing.
    post: tuple[str, str] | None | str
    patch_index: str | None = None  # for patch files: the section's text


@dataclass
class Work:
    """A resolved address: where the work lives and what it carries."""

    address: str
    kind: str
    label: str
    root: Path
    tip: str | None = None
    worktree: Path | None = None
    patch_file: Path | None = None
    stash_base: str | None = None
    stash_untracked: str | None = None
    when: int | None = None
    subject: str = ""
    # (commit, reason) a source knows the work started from, e.g. a run
    # receipt's baseline or the reflog boundary of an orphaned commit.
    base_hint: tuple[str, str] | None = None
    notes: list[dict[str, str]] = field(default_factory=list)

    def note(self, source: str, claim: str) -> None:
        self.notes.append({"source": source, "claim": claim})


@dataclass
class Changes:
    """What a piece of work changes, measured from an explicit base."""

    work: Work
    base: str | None
    base_reason: str
    files: list[FileChange]
    commits: list[str]

    def is_empty(self) -> bool:
        return not self.files


# Host configuration must not change what vc-git parses: mnemonic or missing
# diff prefixes, forced colour, rename guesses, quoted paths or signature /
# decoration output in logs.
_STABLE_OUTPUT = (
    "-c",
    "diff.mnemonicPrefix=false",
    "-c",
    "diff.noprefix=false",
    "-c",
    "diff.renames=false",
    "-c",
    "color.ui=false",
    "-c",
    "core.quotePath=false",
    "-c",
    "log.showSignature=false",
    "-c",
    "log.decorate=no",
)


def git(root: Path, *args: str, **kwargs: Any) -> subprocess.CompletedProcess[str]:
    """Run Git with the hardened read-only environment shared by vc-git."""
    return _run(root, *_STABLE_OUTPUT, *args, **kwargs)


def git_out(root: Path, *args: str, **kwargs: Any) -> str:
    result = git(root, *args, **kwargs)
    if result.returncode:
        detail = (result.stderr or result.stdout).strip().splitlines()
        raise Unestablished(
            f"git {args[0]} failed" + (f": {detail[-1]}" if detail else "")
        )
    return result.stdout


def repo_root(project: str | Path) -> Path:
    refuse_repo_env_overrides()
    return _require_git_root(Path(project).expanduser().resolve())


def common_dir(root: Path) -> str:
    return _path_key(
        git_out(root, "rev-parse", "--path-format=absolute", "--git-common-dir").strip()
    )


def repo_name(root: Path) -> str:
    """Name of the repository behind every worktree (not the worktree folder)."""
    common = Path(common_dir(root))
    return (common.parent if common.name == ".git" else common).name or "repo"


def commit_of(root: Path, rev: str) -> str | None:
    if rev.startswith("-"):
        return None
    result = git(root, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    return result.stdout.strip() if result.returncode == 0 else None


def resolve_target(root: Path, target: str | None) -> tuple[str, str]:
    """Name and commit of what "landed" and "safe" are measured against.

    Default: the remote's default branch (``origin/HEAD``), else a local trunk.
    """
    if target:
        sha = commit_of(root, target)
        if not sha:
            raise AddressError(f"target is not a commit or branch: {target}")
        return target, sha
    remotes = git_out(root, "remote").split()
    for remote in sorted(remotes, key=lambda name: name != "origin"):
        head = git(
            root, "symbolic-ref", "--quiet", "--short", f"refs/remotes/{remote}/HEAD"
        )
        name = head.stdout.strip()
        if head.returncode == 0 and name:
            sha = commit_of(root, name)
            if sha:
                return name, sha
    for name in TRUNK_NAMES:
        sha = commit_of(root, f"refs/heads/{name}")
        if sha:
            return name, sha
    raise AddressError("no default target: pass --target REF")


def primary_branch(root: Path) -> str | None:
    """Branch checked out in the primary checkout, where integration happens."""
    listed = git(root, "worktree", "list", "--porcelain", "-z")
    for field_text in listed.stdout.split("\0"):
        if field_text.startswith("branch "):
            return field_text.removeprefix("branch ")
        if not field_text:
            break
    return None


def integration_lines(
    root: Path, target: str, target_sha: str
) -> list[tuple[str, str]]:
    """Lines work is integrated into, target first.

    The target, the branch of the primary checkout (where the integrator
    lands work), and conventional trunk names locally and on each remote.
    """
    lines = [(target, target_sha)]
    seen = {target_sha}
    names = [f"refs/heads/{name}" for name in TRUNK_NAMES]
    primary = primary_branch(root)
    if primary:
        names.insert(0, primary)
    for remote in git_out(root, "remote").split():
        names += [f"refs/remotes/{remote}/{name}" for name in TRUNK_NAMES]
    for ref in names:
        sha = commit_of(root, ref)
        if sha and sha not in seen:
            seen.add(sha)
            short = ref.removeprefix("refs/heads/").removeprefix("refs/remotes/")
            lines.append((short, sha))
    return lines


def nearest_base(
    root: Path, tip: str, lines: list[tuple[str, str]]
) -> tuple[str | None, str]:
    """Measure work from the integration line it most recently left.

    A line that already contains the tip carries the work and cannot be its
    base, unless it is the target itself (then nothing is left to measure).
    """
    best: tuple[int, int, str, str] | None = None
    for order, (name, sha) in enumerate(lines):
        result = git(root, "merge-base", sha, tip)
        base = result.stdout.strip()
        if result.returncode or not base:
            continue
        if base == tip and order:
            continue
        count = git(root, "rev-list", "--count", f"{base}..{tip}")
        distance = int(count.stdout.strip() or 0) if count.returncode == 0 else 1 << 30
        candidate = (distance, order, base, name)
        if best is None or candidate[:2] < best[:2]:
            best = candidate
    if best is None:
        return None, "no common history with any integration line"
    distance, _, base, name = best
    return base, f"left {name} {distance} commit(s) ago at {base[:SHORT]}"


def creation_point(root: Path, work: Work) -> tuple[str | None, str]:
    """Where a branch was created, read from its reflog (an explicit trace).

    Tried for the work's own local branch and, for a remote branch or a
    checkout, the local branch of the same name. Returns ``(None, "")``
    when the reflog no longer records the creation or the branch was reset
    away from it.
    """
    if not work.tip:
        return None, ""
    names: list[str] = []
    if work.kind == "branch":
        names.append(work.label)
    elif work.kind == "remote" and "/" in work.label:
        names.append(work.label.split("/", 1)[1])
    elif work.worktree is not None:
        branch = git(
            work.worktree, "symbolic-ref", "--quiet", "--short", "HEAD"
        ).stdout.strip()
        if branch:
            names.append(branch)
    for name in names:
        log = git(root, "reflog", "show", "--format=%H%x00%gs", f"refs/heads/{name}")
        entries = [line for line in log.stdout.splitlines() if "\0" in line]
        if log.returncode or not entries:
            continue
        sha, _, message = entries[-1].partition("\0")
        if not message.startswith("branch: Created from"):
            continue
        if git(root, "merge-base", "--is-ancestor", sha, work.tip).returncode == 0:
            count = git(
                root, "rev-list", "--count", f"{sha}..{work.tip}"
            ).stdout.strip()
            return (
                sha,
                f"branch {name} was created at {sha[:SHORT]} ({count} commit(s) since, per its reflog)",
            )
    return None, ""


def unreachable_part(
    root: Path, sha: str
) -> tuple[str | None, list[tuple[str, str, str]]]:
    """History only ``sha`` holds: no branch, tag, remote or stash entry does.

    Returns ``(boundary, own)`` where ``own`` lists ``(commit, author e-mail,
    author time)`` along the first-parent line and ``boundary`` is the first
    commit a ref still holds. Empty ``own`` means a ref already holds ``sha``.
    """
    stashes = git(root, "stash", "list", "--format=%H").stdout.split()
    listed = git(
        root,
        "rev-list",
        "--first-parent",
        "--boundary",
        "--no-commit-header",
        "--format=%m%x00%H%x00%ae%x00%at",
        sha,
        "--not",
        "--all",
        *stashes,
    )
    own: list[tuple[str, str, str]] = []
    boundary = None
    for line in listed.stdout.splitlines():
        fields = line.split("\0")
        if len(fields) != 4:
            continue
        mark, commit, email, stamp = fields
        if mark == "-":  # boundary: the first commit a ref still holds
            boundary = boundary or commit
        else:
            own.append((commit, email, stamp))
    return boundary, own


def _commit_meta(work: Work) -> None:
    if not work.tip:
        return
    shown = git(work.root, "show", "-s", "--format=%ct%x00%s", work.tip)
    if shown.returncode == 0 and "\0" in shown.stdout:
        stamp, _, subject = shown.stdout.strip().partition("\0")
        work.when = int(stamp) if stamp.isdecimal() else None
        work.subject = subject


def _resolve_pinned(root: Path, text: str) -> Work:
    match = _PINNED.match(text)
    name, pin = (match["name"], match["pin"]) if match else (text, None)
    if name.startswith("-") or not name:
        raise AddressError(f"not an address: {text}")
    current = commit_of(root, name)
    full = git(root, "rev-parse", "--symbolic-full-name", name).stdout.strip()
    tip = current
    work_note: tuple[str, str] | None = None
    if pin:
        pinned = commit_of(root, pin)
        if not pinned:
            raise AddressError(f"{text}: commit {pin} is not in this repository")
        if current and current != pinned:
            work_note = (
                "git",
                f"{name} has moved to {current[:SHORT]} since this address was printed; measuring the pinned tip",
            )
        tip = pinned
    if not tip:
        raise AddressError(f"no branch, ref or commit named {name}")
    if full.startswith("refs/heads/"):
        kind, label = "branch", full.removeprefix("refs/heads/")
    elif full.startswith("refs/remotes/"):
        kind, label = "remote", full.removeprefix("refs/remotes/")
    elif full.startswith("refs/vc-git/saved/"):
        kind, label = "saved", full.removeprefix("refs/vc-git/saved/")
    elif full.startswith("refs/tags/"):
        kind, label = "tag", full.removeprefix("refs/tags/")
    else:
        kind, label = "commit", tip[:SHORT]
    if kind == "commit":
        address = tip[:12]
    elif kind == "saved":
        address = f"saved:{label}@{tip[:SHORT]}"
    else:
        address = f"{label}@{tip[:SHORT]}"
    work = Work(address=address, kind=kind, label=label, root=root, tip=tip)
    if work_note:
        work.note(*work_note)
    if kind == "commit":
        boundary, own = unreachable_part(root, tip)
        if own and boundary:
            work.base_hint = (
                boundary,
                f"its {len(own)} commit(s) that no branch, tag or stash holds, since {boundary[:SHORT]}",
            )
            work.note(
                "git",
                "no branch, tag, remote or stash holds this commit; only a reflog does, until it expires",
            )
    return work


def _resolve_stash(root: Path, text: str) -> Work:
    match = _STASH.match(text)
    assert match
    entries = git_out(root, "stash", "list", "--format=%H%x00%gd").splitlines()
    shas = [line.split("\0", 1)[0] for line in entries if "\0" in line]
    index = int(match["n"])
    pin = match["pin"]
    work_note = None
    if pin:
        hits = [i for i, sha in enumerate(shas) if sha.startswith(pin)]
        if not hits:
            raise Unestablished(f"{text}: that stash entry no longer exists")
        if hits[0] != index:
            work_note = (
                f"the entry has moved from stash@{{{index}}} to stash@{{{hits[0]}}}"
            )
        index = hits[0]
    if index >= len(shas):
        raise AddressError(f"no stash entry stash@{{{index}}}")
    tip = shas[index]
    parents = git_out(root, "rev-list", "--parents", "-n1", tip).split()
    work = Work(
        address=f"stash@{{{index}}}@{tip[:SHORT]}",
        kind="stash",
        label=f"stash@{{{index}}}",
        root=root,
        tip=tip,
        stash_base=parents[1] if len(parents) > 1 else None,
        stash_untracked=parents[3] if len(parents) > 3 else None,
    )
    if work_note:
        work.note("git", work_note)
    return work


def _resolve_worktree(root: Path, raw: str, *, kind: str = "worktree") -> Work:
    location = Path(raw).expanduser()
    if not location.is_absolute():
        location = (Path.cwd() / location).resolve()
    if not location.is_dir():
        raise Unestablished(f"worktree directory is gone: {location}")
    try:
        actual = _require_git_root(location)
    except RuntimeError as exc:
        raise AddressError(f"not a Git checkout: {location}") from exc
    if common_dir(actual) != common_dir(root):
        raise AddressError(
            f"{actual} belongs to a different repository; pass --repo {actual}"
        )
    head = commit_of(actual, "HEAD")
    branch = git(actual, "symbolic-ref", "--quiet", "--short", "HEAD").stdout.strip()
    work = Work(
        address=f"wt:{actual}",
        kind=kind,
        label=f"{actual.name} [{branch or 'detached'}]",
        root=root,
        tip=head,
        worktree=actual,
    )
    return work


def _resolve_run(root: Path, run_id: str) -> Work:
    if not _SAFE_ID.fullmatch(run_id):
        raise AddressError(f"invalid run id: {run_id}")
    from .control_plane import lookup_runtime_run_meta

    meta = lookup_runtime_run_meta(run_id)
    if not isinstance(meta, dict):
        raise Unestablished(f"run:{run_id}: no runtime receipt found")
    for key in ("worktree_path", "root"):
        location = meta.get(key)
        if isinstance(location, str) and location and Path(location).is_dir():
            try:
                work = _resolve_worktree(root, location, kind="run")
            except AddressError:
                continue
            work.address = f"run:{run_id}"
            work.label = f"run {run_id} ({work.label})"
            baseline = meta.get("worktree_baseline_sha") or meta.get("baseline_sha")
            if (
                isinstance(baseline, str)
                and work.tip
                and commit_of(root, baseline)
                and git(
                    root, "merge-base", "--is-ancestor", baseline, work.tip
                ).returncode
                == 0
            ):
                work.base_hint = (
                    baseline,
                    f"the run's recorded baseline {baseline[:SHORT]}",
                )
            work.note(
                "control-plane",
                f"run receipt names checkout {location} (status {meta.get('status')})",
            )
            return work
    branch = meta.get("branch") or meta.get("worktree_branch")
    if isinstance(branch, str) and commit_of(root, f"refs/heads/{branch}"):
        work = _resolve_pinned(root, branch)
        work.kind = "run"
        work.label = f"run {run_id} (branch {branch})"
        work.address = f"run:{run_id}"
        work.note(
            "control-plane", f"run receipt names branch {branch}; its checkout is gone"
        )
        return work
    raise Unestablished(
        f"run:{run_id}: its checkout and branch are not present in this repository"
    )


def _resolve_pr(root: Path, number: str) -> Work:
    if not number.isdecimal():
        raise AddressError(f"invalid pull request number: {number}")
    try:
        viewed = subprocess.run(
            [
                "gh",
                "pr",
                "view",
                number,
                "--json",
                "headRefOid,headRefName,title,url,state",
            ],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise Unestablished(f"pr:{number}: GitHub CLI unavailable ({exc})") from exc
    if viewed.returncode:
        raise Unestablished(
            f"pr:{number}: GitHub did not answer: {viewed.stderr.strip()}"
        )
    data = json.loads(viewed.stdout)
    tip = commit_of(root, data.get("headRefOid", ""))
    if not tip:
        raise Unestablished(
            f"pr:{number}: head {str(data.get('headRefOid'))[:SHORT]} is not in the local object store "
            f"(fetch it first: git fetch origin pull/{number}/head)"
        )
    work = Work(
        address=f"pr:{number}",
        kind="pr",
        label=f"PR #{number} {data.get('headRefName', '')}".strip(),
        root=root,
        tip=tip,
    )
    work.note(
        "github",
        f"PR #{number} ({data.get('state')}) head is {tip[:SHORT]}: {data.get('title')}",
    )
    return work


def resolve(root: Path, text: str) -> Work:
    """Turn one address into a :class:`Work` record, reading only."""
    text = text.strip()
    if not text:
        raise AddressError("empty address")
    if text.startswith("patch:"):
        path = Path(text.removeprefix("patch:")).expanduser().resolve()
        if not path.is_file():
            raise Unestablished(f"patch file is gone: {path}")
        work = Work(
            address=f"patch:{path}",
            kind="patch",
            label=path.name,
            root=root,
            patch_file=path,
        )
        work.when = int(path.stat().st_mtime)
    elif text.startswith("wt:"):
        work = _resolve_worktree(root, text.removeprefix("wt:"))
    elif text.startswith("run:"):
        work = _resolve_run(root, text.removeprefix("run:"))
    elif text.startswith("pr:"):
        work = _resolve_pr(root, text.removeprefix("pr:"))
    elif text.startswith("saved:"):
        name = text.removeprefix("saved:")
        match = _PINNED.match(name)
        ref = f"refs/vc-git/saved/{match['name'] if match else name}"
        work = _resolve_pinned(root, ref + (f"@{match['pin']}" if match else ""))
    elif _STASH.match(text):
        work = _resolve_stash(root, text)
    else:
        work = _resolve_pinned(root, text)
    _commit_meta(work)
    return work


# ---------------------------------------------------------------------------
# What a piece of work changes (read-only)
# ---------------------------------------------------------------------------


def _name_status(raw: str) -> list[tuple[str, str]]:
    fields = raw.split("\0")
    pairs: list[tuple[str, str]] = []
    index = 0
    while index + 1 < len(fields):
        status, path = fields[index], fields[index + 1]
        if not status:
            break
        pairs.append((status[0], path))
        index += 2
    return pairs


def tree_entries(
    root: Path, rev: str, paths: list[str] | None = None
) -> dict[str, tuple[str, str]]:
    """``path -> (mode, oid)`` for blobs, links and gitlinks in one tree."""
    entries: dict[str, tuple[str, str]] = {}
    chunks = (
        [None]
        if paths is None
        else [paths[i : i + 500] for i in range(0, len(paths), 500)]
    )
    for chunk in chunks:
        if chunk == []:
            continue
        args = ["ls-tree", "-r", "-z", "--full-tree", rev]
        if chunk is not None:
            args += ["--", *[f":(literal){p}" for p in chunk]]
        for record in git_out(root, *args).split("\0"):
            if not record:
                continue
            meta, _, path = record.partition("\t")
            mode, _kind, oid = meta.split()
            entries[path] = (mode, oid)
    return entries


def _worktree_post(
    location: Path, paths: list[str]
) -> dict[str, tuple[str, str] | None | str]:
    """Hash working-tree files exactly as ``git add`` would, without writing."""
    post: dict[str, tuple[str, str] | None | str] = {}
    regular: list[str] = []
    for path in paths:
        full = location / path
        if full.is_symlink():
            link = os.readlink(full)
            oid = git(location, "hash-object", "--stdin", input=link).stdout.strip()
            post[path] = ("120000", oid) if oid else "unknown"
        elif not full.exists():
            post[path] = None
        elif full.is_dir():
            post[path] = "unknown"  # submodule or nested repository
        else:
            regular.append(path)
    if regular:
        hashed = git(
            location, "hash-object", "--stdin-paths", input="\n".join(regular) + "\n"
        )
        oids = hashed.stdout.split() if hashed.returncode == 0 else []
        for index, path in enumerate(regular):
            if index >= len(oids):
                post[path] = "unknown"
                continue
            mode = "100755" if os.access(location / path, os.X_OK) else "100644"
            post[path] = (mode, oids[index])
    return post


def split_patch(text: str) -> list[tuple[str, str, str, str | None]]:
    """Split a unified diff into ``(path, status, section, post_oid)`` per file."""
    sections: list[list[str]] = []
    for line in text.splitlines(keepends=True):
        if line.startswith("diff --git "):
            sections.append([line])
        elif sections:
            sections[-1].append(line)
    result = []
    for lines in sections:
        body = "".join(lines)
        old = new = None
        status = "M"
        post_oid = None
        for line in lines:
            if line.startswith("--- "):
                old = line[4:].rstrip("\n")
            elif line.startswith("+++ "):
                new = line[4:].rstrip("\n")
            elif line.startswith("new file mode"):
                status = "A"
            elif line.startswith("deleted file mode"):
                status = "D"
            elif line.startswith("index ") and ".." in line:
                after = line.split()[1].split("..", 1)[1]
                post_oid = (
                    after if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", after) else None
                )
        header = lines[0].rstrip("\n").removeprefix("diff --git ").split(" ", 1)
        path = header[1].split("/", 1)[-1] if len(header) == 2 else ""
        for candidate in (new, old):
            if candidate and candidate != "/dev/null":
                # Strip one leading component, exactly like ``git apply -p1``
                # (covers a/ b/ and mnemonic c/ i/ w/ o/ prefixes).
                path = candidate.split("/", 1)[1] if "/" in candidate else candidate
                break
        result.append((path.strip('"'), status, body, post_oid))
    return result


def changes(
    work: Work,
    lines: list[tuple[str, str]],
    *,
    base_override: str | None = None,
) -> Changes:
    """Describe what ``work`` changes, measured from an explicit base."""
    root = work.root
    if work.kind == "patch":
        assert work.patch_file
        text = work.patch_file.read_text(encoding="utf-8", errors="surrogateescape")
        files = []
        for path, status, body, post_oid in split_patch(text):
            post: tuple[str, str] | None | str
            if status == "D":
                post = None
            elif post_oid:
                post = ("unknown-mode", post_oid)
            else:
                post = "unknown"
            files.append(FileChange(path, status, post, patch_index=body))
        if not files:
            raise Unestablished(f"{work.address}: no file sections in this patch")
        return Changes(work, None, "a patch carries no base", files, [])

    if base_override:
        base = commit_of(root, base_override)
        if not base:
            raise AddressError(f"--base is not a commit: {base_override}")
        reason = f"--base {base_override}"
    elif work.kind == "stash":
        base, reason = work.stash_base, "the commit the stash was made on"
    elif work.base_hint:
        base, reason = work.base_hint
    elif work.tip:
        base, reason = creation_point(root, work)
        if not base:
            base, reason = nearest_base(root, work.tip, lines)
    else:
        base, reason = None, "unborn branch: measured from an empty tree"

    old = base or EMPTY_TREE
    commits: list[str] = []
    if work.worktree is not None:
        location = work.worktree
        # Plumbing on purpose: porcelain ``git diff`` refreshes and rewrites
        # the index on stat-only changes, even with GIT_OPTIONAL_LOCKS=0.
        raw = git_out(
            location, "diff-index", "--name-status", "-z", "--no-renames", old
        )
        pairs = _name_status(raw)
        untracked = [
            p
            for p in git_out(
                location, "ls-files", "-z", "--others", "--exclude-standard"
            ).split("\0")
            if p
        ]
        pairs += [("A", p) for p in untracked]
        post = _worktree_post(location, [p for _, p in pairs])
        # diff-index reports stat-only changes too; drop files whose content
        # is exactly what the base already has.
        before = tree_entries(location, old, [p for _, p in pairs]) if base else {}
        files = [
            FileChange(p, s, post.get(p, "unknown"))
            for s, p in pairs
            if not (isinstance(post.get(p), tuple) and before.get(p) == post.get(p))
        ]
        if base and work.tip:
            commits = git_out(
                root, "rev-list", "--no-merges", f"{base}..{work.tip}"
            ).split()
        return Changes(work, base, reason, sorted(files, key=lambda f: f.path), commits)

    assert work.tip
    pairs = _name_status(
        git_out(root, "diff", "--name-status", "-z", "--no-renames", old, work.tip)
    )
    tip_tree = tree_entries(root, work.tip, [p for _, p in pairs])
    files = [
        FileChange(p, s, None if s == "D" else tip_tree.get(p, "unknown"))
        for s, p in pairs
    ]
    if work.stash_untracked:
        extra = tree_entries(root, work.stash_untracked)
        files += [FileChange(p, "A", entry) for p, entry in extra.items()]
    if base and work.kind != "stash":
        commits = git_out(
            root, "rev-list", "--no-merges", f"{base}..{work.tip}"
        ).split()
    return Changes(work, base, reason, sorted(files, key=lambda f: f.path), commits)


def file_patch(change: Changes, paths: list[str]) -> str:
    """Unified diff (binary-safe, full index) for ``paths`` of one piece of work."""
    work = change.work
    if work.kind == "patch":
        wanted = set(paths)
        return "".join(f.patch_index or "" for f in change.files if f.path in wanted)
    old = change.base or EMPTY_TREE
    if not paths:
        return ""
    if work.worktree is not None:
        location = work.worktree
        tracked = {
            p
            for p in git_out(
                location, "ls-files", "-z", "--", *[f":(literal){p}" for p in paths]
            ).split("\0")
            if p
        }
        in_base = (
            set(tree_entries(location, old, paths)) if old != EMPTY_TREE else set()
        )
        known = tracked | in_base
        parts = []
        listed = [p for p in paths if p in known]
        if listed:
            parts.append(
                git_out(
                    location,
                    "diff-index",
                    *DIFF_FLAGS,
                    old,
                    "--",
                    *[f":(literal){p}" for p in listed],
                )
            )
        for path in paths:
            if path in known:
                continue
            result = git(
                location, "diff", "--no-index", *DIFF_FLAGS, "--", "/dev/null", path
            )
            if result.returncode not in (0, 1):
                raise Unestablished(f"cannot diff untracked file {path}")
            parts.append(result.stdout)
        return "".join(parts)
    untracked = (
        set(tree_entries(work.root, work.stash_untracked, paths))
        if work.stash_untracked
        else set()
    )
    parts = []
    tracked_paths = [p for p in paths if p not in untracked]
    if tracked_paths:
        parts.append(
            git_out(
                work.root,
                "diff",
                *DIFF_FLAGS,
                old,
                work.tip or EMPTY_TREE,
                "--",
                *[f":(literal){p}" for p in tracked_paths],
            )
        )
    extra = [p for p in paths if p in untracked]
    if extra and work.stash_untracked:
        parts.append(
            git_out(
                work.root,
                "diff",
                *DIFF_FLAGS,
                EMPTY_TREE,
                work.stash_untracked,
                "--",
                *[f":(literal){p}" for p in extra],
            )
        )
    return "".join(parts)


def read_addresses(values: list[str], stdin_text: str | None) -> list[str]:
    """Expand ``-`` into the addresses piped on stdin (one per line)."""
    result: list[str] = []
    for value in values:
        if value == "-":
            for line in (stdin_text or "").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    result.append(line)
        else:
            result.append(value)
    return result


def is_hex(text: str) -> bool:
    return bool(_HEX.fullmatch(text))
