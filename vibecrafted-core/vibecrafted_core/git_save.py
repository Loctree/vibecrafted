"""Save: put a piece of work somewhere it will survive, without touching it.

Destinations (``--to``):

* ``patch``     - a binary-safe patch in the harbor with a SHA-256 manifest.
                  Survives deletion of the branch, the worktree and the whole
                  repository; travels to another machine. The default.
* ``git-apply`` - the same patch, plus proof that it applies cleanly onto
                  ``--target`` right now.
* ``commit``    - a ref under ``refs/vc-git/saved/``: a commit that can be
                  pushed, invisible to ``git branch``.
* ``stash``     - a regular stash entry (tracked, staged and untracked parts).

The source is never modified: a checkout is snapshotted through a temporary
index, so its files, its real index, HEAD and its branch stay exactly as they
were. Every save is additive (objects, one new ref or stash entry, harbor
files) and is appended to the harbor ledger.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any

from .git_address import (
    DIFF_FLAGS,
    EMPTY_TREE,
    SHORT,
    AddressError,
    Unestablished,
    Work,
    changes,
    commit_of,
    git,
    git_out,
    repo_name,
)
from .git_gems import harbor_root
from .git_landed import TargetView, _patch_id

DESTINATIONS = ("patch", "git-apply", "commit", "stash")


def _slug(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", text).strip("-.")
    return (slug or "work")[:60]


def _now() -> _dt.datetime:
    return _dt.datetime.now(_dt.UTC).astimezone()


def _snapshot(location: Path) -> dict[str, Any]:
    """Trees for a checkout's staged, tracked and untracked state, read-only.

    Uses a copy of the real index so the checkout and its index stay untouched.
    """
    head = commit_of(location, "HEAD")
    with tempfile.TemporaryDirectory(prefix="vc-git-save-") as tmp:
        index = Path(tmp) / "index"
        real = Path(git_out(location, "rev-parse", "--git-path", "index").strip())
        if not real.is_absolute():
            real = location / real
        if real.is_file():
            shutil.copyfile(real, index)
        env = {"GIT_INDEX_FILE": str(index)}
        if not real.is_file() and head:
            git_out(location, "read-tree", head, env=env)
        staged = git(location, "write-tree", env=env)
        index_tree = staged.stdout.strip() if staged.returncode == 0 else None
        git_out(location, "add", "-u", "--", ".", env=env)
        tracked_tree = git_out(location, "write-tree", env=env).strip()
        untracked = [
            p
            for p in git_out(
                location, "ls-files", "-z", "--others", "--exclude-standard"
            ).split("\0")
            if p
        ]
        untracked_tree = None
        if untracked:
            git_out(
                location,
                "add",
                "--pathspec-from-file=-",
                "--pathspec-file-nul",
                env=env,
                input="\0".join(untracked),
            )
            only = Path(tmp) / "untracked-index"
            only_env = {"GIT_INDEX_FILE": str(only)}
            git_out(
                location,
                "add",
                "--pathspec-from-file=-",
                "--pathspec-file-nul",
                env=only_env,
                input="\0".join(untracked),
            )
            untracked_tree = git_out(location, "write-tree", env=only_env).strip()
        full_tree = git_out(location, "write-tree", env=env).strip()
    ignored = [
        p
        for p in git_out(
            location,
            "ls-files",
            "-z",
            "--others",
            "--ignored",
            "--exclude-standard",
            "--directory",
        ).split("\0")
        if p
    ]
    hidden = [
        record[2:]
        for record in git_out(location, "ls-files", "-v", "-z").split("\0")
        if record and (record[0].islower() or record[0] == "S")
    ]
    return {
        "head": head,
        "index_tree": index_tree,
        "tracked_tree": tracked_tree,
        "untracked_tree": untracked_tree,
        "full_tree": full_tree,
        "untracked": untracked,
        "ignored": ignored,
        "hidden": hidden,
    }


def _commit(root: Path, tree: str, parents: list[str | None], message: str) -> str:
    args = ["commit-tree", tree]
    for parent in parents:
        if parent:
            args += ["-p", parent]
    return git_out(root, *args, "-m", message).strip()


def _write_exclusive(path: Path, data: bytes) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    candidate = path
    for attempt in range(1, 100):
        try:
            with candidate.open("xb") as handle:
                handle.write(data)
            return candidate
        except FileExistsError:
            candidate = path.with_name(f"{path.stem}-{attempt}{path.suffix}")
    raise Unestablished(f"cannot find a free file name next to {path}")


def save(
    work: Work,
    *,
    to: str,
    lines: list[tuple[str, str]],
    target: tuple[str, str] | None,
    base_override: str | None = None,
    harbor: Path | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Copy ``work`` to ``to``; return the new address and how it was made."""
    if to not in DESTINATIONS:
        raise AddressError(f"--to must be one of {', '.join(DESTINATIONS)}")
    root = work.root
    stamp = _now()
    result: dict[str, Any] = {
        "source": work.address,
        "kind": work.kind,
        "label": work.label,
        "to": to,
        "dry_run": dry_run,
        "saved": [],
        "evidence": list(work.notes),
        "warnings": [],
    }
    if work.kind == "patch" and to in {"commit", "stash"}:
        raise AddressError("a patch file can be saved --to patch or --to git-apply")
    if work.kind == "stash" and to == "stash":
        raise AddressError(
            "this is already a stash entry; --to commit makes it durable, --to patch takes it off this machine"
        )

    change = changes(work, lines, base_override=base_override)
    result["base"] = change.base
    result["base_reason"] = change.base_reason
    result["files"] = len(change.files)
    if change.is_empty() and work.kind != "patch":
        result.update(
            answer="nothing",
            sentence=f"{work.address} changes nothing relative to its base; there is nothing to save",
        )
        return result
    if dry_run:
        where = {
            "patch": f"a new patch under {(harbor or harbor_root()) / repo_name(root)}",
            "git-apply": f"a new patch under {(harbor or harbor_root()) / repo_name(root)}, checked against {target[0] if target else 'the target'}",
            "commit": "a new ref under refs/vc-git/saved/",
            "stash": "a new stash entry (stash@{0}; existing entries shift by one)",
        }[to]
        result.update(
            answer="dry-run",
            sentence=f"would copy {len(change.files)} file(s) of {work.address} into {where}; nothing was written",
        )
        return result

    snapshot: dict[str, Any] | None = None
    base = change.base
    if work.worktree is not None:
        snapshot = _snapshot(work.worktree)
        tip_tree = snapshot["full_tree"]
        if snapshot["ignored"]:
            result["warnings"].append(
                f"{len(snapshot['ignored'])} ignored path(s) are not included (build output and deliberately ignored files)"
            )
        if snapshot["hidden"]:
            result["warnings"].append(
                f"{len(snapshot['hidden'])} file(s) are marked assume-unchanged or skip-worktree; local edits to them are NOT in this copy: "
                + ", ".join(snapshot["hidden"][:5])
            )
    elif work.tip:
        tip_tree = git_out(root, "rev-parse", f"{work.tip}^{{tree}}").strip()
    else:
        tip_tree = None
    source_line = f"Saved-From: {work.address}"
    # A short, readable name: the branch of a checkout, else the label.
    name_hint = work.label
    if work.worktree is not None:
        branch = git(
            work.worktree, "symbolic-ref", "--quiet", "--short", "HEAD"
        ).stdout.strip()
        name_hint = branch or work.worktree.name

    if to in {"patch", "git-apply"}:
        if work.kind == "patch":
            assert work.patch_file
            body = work.patch_file.read_text(encoding="utf-8", errors="surrogateescape")
        elif snapshot is not None:
            assert work.worktree is not None and tip_tree
            body = git_out(
                work.worktree, "diff", *DIFF_FLAGS, base or EMPTY_TREE, tip_tree
            )
        else:
            assert work.tip
            body = git_out(root, "diff", *DIFF_FLAGS, base or EMPTY_TREE, work.tip)
            if work.stash_untracked:
                body += git_out(
                    root, "diff", *DIFF_FLAGS, EMPTY_TREE, work.stash_untracked
                )
        applies = None
        if to == "git-apply":
            if target is None:
                raise AddressError("--to git-apply needs a target to check against")
            with TargetView(root, *target) as view:
                applies = view.applies(body, reverse=False)
            result["applies_to"] = {
                "target": target[0],
                "target_sha": target[1],
                "clean": applies,
            }
        header = (
            "vc-git save\n"
            f"{source_line}\n"
            f"Base: {base or 'none (a patch file or an unborn branch)'}\n"
            f"Tip: {work.tip or '-'}\n"
            f"Created: {stamp.isoformat(timespec='seconds')}\n"
            + (
                f"Applies-To: {target[0]} {target[1]} {'clean' if applies else 'NOT clean' if applies is False else 'unchecked'}\n"
                if to == "git-apply" and target
                else ""
            )
            + "\n"
        )
        data = (header + body).encode("utf-8", errors="surrogateescape")
        folder = (
            (harbor or harbor_root()) / repo_name(root) / stamp.strftime("%Y-%m-%d")
        )
        name = f"{stamp.strftime('%H%M%S')}-{_slug(name_hint)}.patch"
        written = _write_exclusive(folder / name, data)
        manifest = {
            "schema": "vibecrafted.vc-git.saved-patch.v1",
            "patch": str(written),
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
            "source": work.address,
            "kind": work.kind,
            "repo": str(root),
            "base": base,
            "tip": work.tip,
            "tree": tip_tree,
            "files": len(change.files),
            "patch_id": _patch_id(root, body),
            "applies_to": result.get("applies_to"),
            "created_at": stamp.isoformat(timespec="seconds"),
        }
        manifest_path = _write_exclusive(
            written.with_suffix(".json"),
            (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode(),
        )
        address = f"patch:{written}"
        result.update(
            manifest=str(manifest_path),
            sha256=manifest["sha256"],
            patch_id=manifest["patch_id"],
        )
        result["evidence"].append(
            {
                "source": "harbor",
                "claim": f"wrote {len(data)} bytes, sha256 {manifest['sha256'][:16]}…, manifest {manifest_path.name}",
            }
        )
        result["undo"] = f"remove {written} and {manifest_path}"
        if to == "git-apply" and applies is not True:
            sentence = f"saved, but it does {'not' if applies is False else 'not provably'} apply cleanly onto {target[0] if target else 'the target'}"
            result.update(answer="no", sentence=sentence)
        else:
            result.update(
                answer="done",
                sentence="saved"
                + (
                    f"; it applies cleanly onto {target[0]}"
                    if to == "git-apply" and target
                    else ""
                ),
            )
    elif to == "commit":
        if snapshot is not None:
            assert tip_tree
            sha = _commit(
                root,
                tip_tree,
                [snapshot["head"]],
                f"vc-git save of {work.label}\n\n{source_line}\nSaved-Base: {base or '-'}\n",
            )
        else:
            sha = (
                work.tip
            )  # the work is already a commit: keep it alive under a new name
        assert sha
        name = f"{_slug(name_hint)}/{stamp.strftime('%Y%m%d-%H%M%S')}"
        ref = f"refs/vc-git/saved/{name}"
        if git(root, "check-ref-format", ref).returncode:
            raise AddressError(f"cannot form a valid ref name from {work.label}")
        git_out(root, "update-ref", "-m", f"vc-git save {work.address}", ref, sha, "")
        address = f"saved:{name}@{sha[:SHORT]}"
        result["evidence"].append(
            {
                "source": "git",
                "claim": f"created {ref} -> {sha[:SHORT]} (create-only; an existing ref is never moved)",
            }
        )
        result["undo"] = f"git update-ref -d {ref} {sha}"
        result["push_hint"] = f"git push <remote> {ref}:refs/heads/saved/{name}"
        result.update(answer="done", sentence="saved")
    else:  # stash
        head = snapshot["head"] if snapshot is not None else base
        if snapshot is not None:
            index_tree = snapshot["index_tree"] or (
                git_out(root, "rev-parse", f"{head}^{{tree}}").strip()
                if head
                else EMPTY_TREE
            )
            worktree_tree = snapshot["tracked_tree"]
            untracked_tree = snapshot["untracked_tree"]
        else:
            index_tree = worktree_tree = tip_tree or EMPTY_TREE
            untracked_tree = None
        label = work.label
        i_commit = _commit(root, index_tree, [head], f"index on {label}: vc-git save")
        u_commit = (
            _commit(
                root, untracked_tree, [], f"untracked files on {label}: vc-git save"
            )
            if untracked_tree
            else None
        )
        w_commit = _commit(
            root,
            worktree_tree,
            [head, i_commit, u_commit],
            f"On {label}: vc-git save {work.address}",
        )
        git_out(
            root,
            "stash",
            "store",
            "-m",
            f"On {label}: vc-git save {work.address}",
            w_commit,
        )
        address = f"stash@{{0}}@{w_commit[:SHORT]}"
        result["evidence"].append(
            {
                "source": "git",
                "claim": f"stored stash commit {w_commit[:SHORT]}; the pin keeps this address valid after other entries shift it",
            }
        )
        result["undo"] = (
            f"git stash drop <the entry whose commit is {w_commit[:SHORT]}>"
        )
        result.update(answer="done", sentence="saved")

    result["saved"].append(address)
    record = {
        "time": stamp.isoformat(timespec="seconds"),
        "op": "save",
        "from": work.address,
        "to": to,
        "address": address,
        "base": base,
        "tip": work.tip,
        "tree": tip_tree,
        "repo": str(root),
    }
    ledger = (harbor or harbor_root()) / repo_name(root) / "ledger.jsonl"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    result["ledger"] = str(ledger)
    return result
