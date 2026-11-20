"""One grammar for the ``vc-git`` work families: ``landed``, ``gems``, ``save``.

Shape::

    vc-git <family> [action] [ADDRESS | QUERY ...] [flags]

A single ``-`` in place of addresses reads them from stdin, one per line, so
``vc-git gems --addresses | vc-git save - --to patch`` composes.

Flags mean the same thing in every family (scope: ``--repo``, ``--target``,
``--base``, ``--remote``, ``--since``, ``--until``, ``--author``, ``--agent``,
``--path``, ``--limit``; output: ``--json``, ``--addresses``, ``--why``;
change: ``--to``, ``--dry-run``).

Exit status, identical everywhere:

    0  yes / done          1  no, partly, or refused
    2  usage or runtime    3  cannot be established

With several addresses the batch exits 1 if any answer is "no", else 3 if
any cannot be established, else 0. "Cannot be established" is never folded
into yes or no - not in text, not in JSON, not in the exit status.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

from .git_address import (
    AddressError,
    Unestablished,
    integration_lines,
    read_addresses,
    repo_root,
    resolve,
    resolve_target,
)

EXIT_YES, EXIT_NO, EXIT_ERROR, EXIT_UNKNOWN = 0, 1, 2, 3
FAMILIES = ("landed", "gems", "save")
SCHEMA = {
    "landed": "vibecrafted.vc-git.landed.v1",
    "save": "vibecrafted.vc-git.save.v1",
}


def _when(text: str | None) -> int | None:
    """``2026-11-01`` or a relative age such as ``3d``, ``2w``, ``12h``."""
    if not text:
        return None
    match = re.fullmatch(r"(\d+)([hdw])", text.strip())
    if match:
        unit = {"h": 3600, "d": 86400, "w": 604800}[match[2]]
        return int(time.time()) - int(match[1]) * unit
    try:
        moment = _dt.datetime.fromisoformat(text)
    except ValueError as exc:
        raise AddressError(
            f"not a date or age: {text} (use 2026-11-01, 12h, 3d or 2w)"
        ) from exc
    if moment.tzinfo is None:
        moment = moment.astimezone()
    return int(moment.timestamp())


def _scope(
    parser: argparse.ArgumentParser, *, base: bool = False, people: bool = False
) -> None:
    group = parser.add_argument_group("scope (same meaning in every vc-git family)")
    group.add_argument(
        "--repo",
        default=".",
        metavar="PATH",
        help="repository (default: the one you are in)",
    )
    group.add_argument(
        "--target",
        metavar="REF",
        help="what 'landed' and 'safe' are measured against (default: the remote's default branch)",
    )
    if base:
        group.add_argument(
            "--base",
            metavar="REF",
            help="measure the work from REF instead of the integration line it left",
        )
    if people:
        group.add_argument(
            "--remote", metavar="NAME", help="only this remote's branches"
        )
        group.add_argument(
            "--since", metavar="WHEN", help="newer than a date (2026-11-01) or age (3d)"
        )
        group.add_argument("--until", metavar="WHEN", help="older than a date or age")
        group.add_argument("--author", help="whose work (name or e-mail fragment)")
        group.add_argument(
            "--agent", help="which agent (Authored-By trailer or [agent/...] subject)"
        )
        group.add_argument(
            "--path", metavar="GLOB", help="only work touching these paths"
        )
        group.add_argument(
            "--limit",
            type=int,
            default=20,
            metavar="N",
            help="how many results (0 = all)",
        )


def _output(parser: argparse.ArgumentParser) -> None:
    group = parser.add_argument_group("output")
    exclusive = group.add_mutually_exclusive_group()
    exclusive.add_argument(
        "--json", action="store_true", help="stable, versioned structure"
    )
    exclusive.add_argument(
        "--addresses",
        dest="bare",
        action="store_true",
        help="bare addresses, one per line, for piping",
    )
    group.add_argument(
        "--why",
        action="store_true",
        help="show the evidence behind each answer, labelled by source",
    )


def build_parser(family: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=f"vc-git {family}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Addresses: BRANCH[@SHA]  REMOTE/BRANCH[@SHA]  SHA  stash@{N}[@SHA]  saved:NAME  "
            "wt:PATH  patch:FILE  run:RUN_ID  pr:N  - (read from stdin)\n"
            "Exit: 0 yes/done · 1 no/partly · 2 usage or runtime error · 3 cannot be established"
        ),
    )
    if family == "landed":
        parser.description = (
            "Did this work land? Compares content, so squash merges, cherry-picks and "
            "plain copies count. Answers yes, no (possibly partly) or cannot be established."
        )
        parser.add_argument("addresses", nargs="+", metavar="ADDRESS")
        parser.add_argument(
            "--only",
            metavar="ANSWERS",
            help="comma-separated filter of answers to emit: yes,no,unknown",
        )
        _scope(parser, base=True)
        _output(parser)
    elif family == "gems":
        parser.description = (
            "Find work that never reached the target: branches, remotes, stashes, "
            "uncommitted checkouts and reflog-only commits. Work that exists in only one copy comes first."
        )
        parser.add_argument(
            "action", nargs="?", choices=("list", "search"), default="list"
        )
        parser.add_argument(
            "query",
            nargs="*",
            metavar="QUERY",
            help="words that must all appear (search)",
        )
        _scope(parser, people=True)
        _output(parser)
    elif family == "save":
        parser.description = "Put work somewhere it will survive, without touching it. The result is an address."
        parser.add_argument(
            "addresses",
            nargs="*",
            metavar="ADDRESS",
            help="default: the checkout given by --repo (wt:.)",
        )
        parser.add_argument(
            "--to",
            choices=("patch", "git-apply", "commit", "stash"),
            default="patch",
            help="patch (default: survives repo deletion) · git-apply (patch proven to apply on --target) · "
            "commit (pushable ref under refs/vc-git/saved/) · stash",
        )
        parser.add_argument(
            "--harbor",
            metavar="DIR",
            help="where patches go (default: $VIBECRAFTED_HOME/harbor)",
        )
        parser.add_argument(
            "--dry-run", action="store_true", help="show what would be written and stop"
        )
        _scope(parser, base=True)
        _output(parser)
    return parser


def _exit_for(answers: list[str]) -> int:
    if "no" in answers or "refused" in answers:
        return EXIT_NO
    if "unknown" in answers:
        return EXIT_UNKNOWN
    return EXIT_YES


def _evidence(rows: list[dict[str, str]], indent: str = "    ") -> list[str]:
    return [f"{indent}[{row['source']}] {row['claim']}" for row in rows]


def render_landed(results: list[dict[str, Any]], why: bool) -> str:
    out: list[str] = []
    for row in results:
        if row["answer"] == "error":
            out.append(f"Cannot be established. {row['address']}: {row['sentence']}")
            continue
        where = row["target"]
        if row["answer"] == "yes":
            out.append(f"Yes. {row['address']} is in {where}: {row['sentence']}.")
        elif row["answer"] == "no":
            extent = "only partly" if row.get("extent") == "partial" else "not"
            out.append(
                f"No. {row['address']} is {extent} in {where}: {row['sentence']}."
            )
        else:
            out.append(
                f"Cannot be established. {row['address']} vs {where}: {row['sentence']}."
            )
        missing = [
            f["path"]
            for f in row.get("files", [])
            if f.get("state") in {"absent", "absent-or-ambiguous"}
        ]
        unclear = [f for f in row.get("files", []) if f.get("state") == "unknown"]
        if missing and not why:
            shown = ", ".join(missing[:8]) + (
                f" and {len(missing) - 8} more" if len(missing) > 8 else ""
            )
            out.append(f"  not in {where}: {shown}")
        if unclear and not why:
            shown = ", ".join(f["path"] for f in unclear[:5]) + (
                f" and {len(unclear) - 5} more" if len(unclear) > 5 else ""
            )
            out.append(f"  undetermined: {shown}")
        if why:
            out.extend(_evidence(row.get("evidence", [])))
            for item in row.get("files", []):
                out.append(f"    {item['state']:<10} {item['path']}  ({item['why']})")
    return "\n".join(out)


def _age(when: int | None) -> str:
    if not when:
        return "age unknown"
    days = (time.time() - when) / 86400
    if days < 1:
        return f"{max(1, int(days * 24))}h old"
    if days < 60:
        return f"{int(days)}d old"
    return f"{int(days / 30)}mo old"


def render_gems(payload: dict[str, Any], why: bool) -> str:
    target = payload["target"]
    searched = payload["searched"]
    total = payload["total_gems"]
    lines = []
    if total == 0:
        lines.append(f"Nothing found that is missing from {target}.")
    else:
        single = payload["single_copy"]
        lines.append(
            f"{total} piece(s) of work are not in {target}"
            + (
                f"; {single} exist in only one copy."
                if single
                else "; every one has a second copy somewhere."
            )
        )
    hidden = searched["landed_by_content"]
    if hidden:
        lines.append(
            f"{hidden} more look unmerged to Git, but their content is already in {target} "
            "(squash, cherry-pick or copy): not gems."
        )
    if searched.get("superseded_rewrites"):
        lines.append(
            f"{searched['superseded_rewrites']} reflog-only commit(s) are earlier versions of "
            "rewritten commits (same author and author date on a branch): not gems."
        )
    if searched.get("recreatable_merges"):
        lines.append(
            f"{searched['recreatable_merges']} reflog-only merge commit(s) join lines that all survive "
            "in branches; Git can redo them: not gems."
        )
    carried = (
        searched["carried_by_other_branches"] + searched["carried_by_integration_lines"]
    )
    if carried:
        lines.append(
            f"{carried} branch name(s) are carried by another branch or integration line and are not listed separately."
        )
    for problem in payload["unreadable"]:
        lines.append(f"Could not read {problem['source']}: {problem['error']}")
    lines.append("")
    for number, row in enumerate(payload["gems"], start=1):
        marker = (
            "ONLY COPY"
            if row["single_copy"]
            else "has copy "
            if row["copies"]
            else "         "
        )
        state = {"no": "not in target", "unknown": "cannot be established"}.get(
            row["answer"], row["answer"]
        )
        detail = row.get("shortstat") or row.get("sentence", "")
        kind = {
            "reflog-only": "  [reflog only]",
            "stash": "  [stash]",
            "uncommitted": "  [uncommitted]",
        }.get(row["tier"], "")
        lines.append(f"{number:>3}. {marker}  {row['address']}{kind}")
        lines.append(f"            {state} · {detail} · {_age(row.get('when'))}")
        if row.get("subject"):
            lines.append(f'            "{row["subject"][:90]}"')
        if row.get("aliases"):
            lines.append(f"            also at: {', '.join(row['aliases'][:4])}")
        if row["copies"]:
            lines.append(f"            copies: {', '.join(row['copies'])}")
        else:
            lines.append(f"            risk: {row['risk']}")
        if why:
            lines.extend(_evidence(row.get("evidence", []), indent="            "))
    if payload["gems"]:
        lines += [
            "",
            "Keep one safe without touching it:  vc-git save ADDRESS --to patch",
        ]
    if total > len(payload["gems"]):
        lines.append(
            f"Showing {len(payload['gems'])} of {total}; use --limit 0 for all."
        )
    lines.append(
        f"(searched {searched['candidates']} candidates in {searched['seconds']}s)"
    )
    return "\n".join(lines)


def render_save(results: list[dict[str, Any]], why: bool) -> str:
    out = []
    for row in results:
        if row["answer"] == "error":
            out.append(f"Not saved. {row['source']}: {row['sentence']}")
            continue
        if row["answer"] == "nothing":
            out.append(f"Nothing to save. {row['sentence']}.")
            continue
        if row["answer"] == "dry-run":
            out.append(f"Dry run. {row['source']}: {row['sentence']}.")
            continue
        lead = "Saved." if row["answer"] == "done" else "Saved, with a warning."
        for address in row["saved"]:
            out.append(f"{lead} {row['source']} -> {address}")
        out.append(
            f"  {row['files']} file(s), measured from {row['base_reason']}. The source was not touched."
        )
        applies = row.get("applies_to")
        if row["answer"] != "done":
            out.append(f"  {row['sentence']}.")
        elif applies:
            out.append(
                f"  It applies cleanly onto {applies['target']} ({applies['target_sha'][:10]}), checked now."
            )
        for warning in row.get("warnings", []):
            out.append(f"  note: {warning}")
        if row.get("push_hint"):
            out.append(f"  to publish it yourself: {row['push_hint']}")
        if why:
            out.extend(_evidence(row.get("evidence", [])))
            if row.get("undo"):
                out.append(f"    [vc-git] to remove this copy: {row['undo']}")
    return "\n".join(out)


def run(family: str, argv: list[str], stdin: Any = None) -> int:
    try:
        return _run(family, argv, stdin)
    except BrokenPipeError:
        # A reader such as ``head`` closed the pipe; that is not a failure.
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        return EXIT_YES


def _run(family: str, argv: list[str], stdin: Any = None) -> int:
    parser = build_parser(family)
    args = parser.parse_args(argv)
    stdin = stdin if stdin is not None else sys.stdin
    try:
        root = repo_root(args.repo)
        target_name, target_sha = resolve_target(root, args.target)
        lines = integration_lines(root, target_name, target_sha)
        if family == "gems":
            from .git_gems import find_gems

            if args.action == "search" and not args.query:
                parser.error("search needs at least one QUERY word")
            payload = find_gems(
                root,
                target_name,
                target_sha,
                query=args.query or None,
                remote=args.remote,
                since=_when(args.since),
                until=_when(args.until),
                author=args.author,
                agent=args.agent,
                path_glob=args.path,
                limit=args.limit,
            )
            if args.json:
                print(json.dumps(payload, indent=2, sort_keys=True, default=str))
            elif args.bare:
                for row in payload["gems"]:
                    print(row["address"])
            else:
                print(render_gems(payload, args.why))
            return (
                EXIT_UNKNOWN
                if payload["unreadable"] and not payload["gems"]
                else EXIT_YES
            )

        raw = getattr(args, "addresses", []) or (
            [f"wt:{root}"] if family == "save" else []
        )
        wanted = read_addresses(raw, stdin.read() if "-" in raw else None)
        if not wanted:
            parser.error("no addresses given (stdin was empty)")
        results: list[dict[str, Any]] = []
        if family == "landed":
            from .git_landed import TargetView, landed

            with TargetView(root, target_name, target_sha) as view:
                for text in wanted:
                    try:
                        results.append(
                            landed(
                                resolve(root, text),
                                view,
                                lines,
                                base_override=args.base,
                            )
                        )
                    except AddressError as exc:
                        results.append(
                            {
                                "address": text,
                                "answer": "error",
                                "sentence": str(exc),
                                "usage": True,
                            }
                        )
                    except Unestablished as exc:
                        results.append(
                            {
                                "address": text,
                                "answer": "unknown",
                                "target": target_name,
                                "sentence": str(exc),
                                "files": [],
                                "evidence": [{"source": "git", "claim": str(exc)}],
                            }
                        )
            answers = [r["answer"] for r in results]
        else:
            from .git_save import save

            for text in wanted:
                try:
                    results.append(
                        save(
                            resolve(root, text),
                            to=args.to,
                            lines=lines,
                            target=(target_name, target_sha),
                            base_override=args.base,
                            harbor=Path(args.harbor).expanduser()
                            if args.harbor
                            else None,
                            dry_run=args.dry_run,
                        )
                    )
                except AddressError as exc:
                    results.append(
                        {
                            "source": text,
                            "answer": "error",
                            "sentence": str(exc),
                            "usage": True,
                        }
                    )
                except Unestablished as exc:
                    results.append(
                        {"source": text, "answer": "unknown", "sentence": str(exc)}
                    )
            answers = [
                {"done": "yes", "nothing": "yes", "dry-run": "yes"}.get(
                    r["answer"], r["answer"]
                )
                for r in results
            ]
        only_answers: set[str] | None = None
        if family == "landed" and getattr(args, "only", None):
            parts = [
                part.strip().lower()
                for part in str(args.only).split(",")
                if part.strip()
            ]
            invalid = [p for p in parts if p not in {"yes", "no", "unknown"}]
            if not parts or invalid:
                parser.error(
                    "--only must be a comma-separated subset of yes,no,unknown"
                )
            only_answers = set(parts)

        display_results = (
            [r for r in results if r.get("answer") in only_answers]
            if only_answers is not None
            else results
        )
        if args.json:
            payload_out: dict[str, Any] = {
                "schema": SCHEMA[family],
                "results": display_results,
            }
            if only_answers is not None:
                payload_out["only"] = sorted(only_answers)
            print(
                json.dumps(
                    payload_out,
                    indent=2,
                    sort_keys=True,
                    default=str,
                )
            )
        elif args.bare:
            for row in display_results:
                if family == "landed" and (
                    only_answers is not None or row["answer"] in {"no", "unknown"}
                ):
                    print(row["address"])
                for address in row.get("saved", []):
                    print(address)
        elif family == "landed":
            if display_results:
                print(render_landed(display_results, args.why))
        else:
            print(render_save(display_results, args.why))
        if any(r.get("usage") for r in results):
            return EXIT_ERROR
        return _exit_for(answers)
    except AddressError as exc:
        print(f"vc-git {family}: {exc}", file=sys.stderr)
        return EXIT_ERROR
    except Unestablished as exc:
        print(f"vc-git {family}: cannot be established: {exc}", file=sys.stderr)
        return EXIT_UNKNOWN
    except (RuntimeError, OSError) as exc:
        print(f"vc-git {family}: {exc}", file=sys.stderr)
        return EXIT_ERROR
