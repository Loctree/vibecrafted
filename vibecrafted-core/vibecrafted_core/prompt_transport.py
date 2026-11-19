"""Provider stdin transports: how a private prompt file reaches a worker.

Every headless lane writes the operator prompt to a 0600 file and hands that
file to the worker on stdin (never argv: ``ps`` and ARG_MAX). Most providers
read that text verbatim. Agy's print mode has no text stdin lane at all; its
only private input is ``--input-format stream-json`` — one NDJSON user turn
per line, requiring ``--output-format stream-json``. Kimi's print mode has no
stdin lane of any kind (kimi 0.42.0: ``-p`` takes the prompt as its argv
value, and bare ``-p`` is a parse error, so nothing is read from stdin): the
prompt is inlined into the launch argv by the command builder — a deliberate
ps/ARG_MAX tradeoff, since kimi offers no private alternative. This module
owns both shapes so the async supervisor, the shell launcher and the tests
agree on one encoder.

It also owns the print-mode time limit (:func:`print_limit_flags`), for the
same reason: the supervisor and the shell launcher must bound a turn the same
way, or not at all.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path

STREAM_JSON_AGENTS = frozenset({"agy"})
# kimi print mode cannot consume a prompt from stdin at all; its launch argv
# carries the prompt as the ``-p`` value (inlined by the command builder from
# the same 0600 prompt file every lane writes).
ARGV_PROMPT_AGENTS = frozenset({"kimi"})
TEXT_TRANSPORT = "text"
STREAM_JSON_TRANSPORT = "stream-json"
ARGV_TRANSPORT = "argv"

# Operator-set wall-clock limit for one agy print-mode turn. Unset means no
# limit: agy then waits for the turn to complete, as every other provider does.
AGY_PRINT_TIMEOUT_ENV = "VIBECRAFTED_AGY_PRINT_TIMEOUT"
# Go duration syntax, as agy's ``--print-timeout`` parses it: 45m, 1h30m, 90s.
_GO_DURATION_RE = re.compile(r"(?:\d+(?:\.\d+)?(?:ns|us|µs|ms|s|m|h))+")


def stdin_transport(agent: str) -> str:
    """Name the stdin encoding a provider's headless argv expects.

    ``argv`` means the provider has no stdin prompt lane: the prompt rides
    the launch argv (kimi ``-p``) and the wired stdin is ignored.
    """
    if agent in STREAM_JSON_AGENTS:
        return STREAM_JSON_TRANSPORT
    if agent in ARGV_PROMPT_AGENTS:
        return ARGV_TRANSPORT
    return TEXT_TRANSPORT


def print_limit_flags(
    agent: str, environ: Mapping[str, str] | None = None
) -> list[str]:
    """Argv flags bounding one print-mode turn of *agent*; empty when unbounded.

    The launcher imposes no limit of its own. When agy's print limit fires, the
    turn is cut mid-work: the process still exits 0 and reports ``SUCCESS``,
    but nothing was committed and no report was written. An operator who
    wants agy bounded sets ``VIBECRAFTED_AGY_PRINT_TIMEOUT`` to a Go duration;
    ``0`` and an empty value mean unbounded. Anything else is refused, so a
    typo cannot silently remove or change the bound.
    """
    if agent != "agy":
        return []
    source = os.environ if environ is None else environ
    raw = str(source.get(AGY_PRINT_TIMEOUT_ENV, "")).strip()
    if raw in {"", "0", "0s"}:
        return []
    if not _GO_DURATION_RE.fullmatch(raw):
        raise ValueError(
            f"{AGY_PRINT_TIMEOUT_ENV}={raw!r} is not a duration such as 45m or 1h30m"
        )
    return ["--print-timeout", raw]


def encode_stream_json_user_turn(prompt: str) -> bytes:
    """Encode one prompt as a single stream-json user turn (one NDJSON line)."""
    payload = {"event": "user", "message": {"role": "user", "content": prompt}}
    return (json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8")


def stream_json_sibling(prompt_file: Path) -> Path:
    """``prompt.md`` -> ``prompt.ndjson`` next to it (any suffix, or none)."""
    stem = prompt_file.stem if prompt_file.suffix else prompt_file.name
    return prompt_file.with_name(f"{stem}.ndjson")


def write_stream_json_file(prompt_file: Path, target: Path) -> Path:
    """Write *prompt_file*'s text as one user turn into a 0600 *target*."""
    text = prompt_file.read_text(encoding="utf-8")
    descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(encode_stream_json_user_turn(text))
    os.chmod(target, 0o600)
    return target


def materialize_stdin_file(
    agent: str, prompt_file: Path, target: Path | None = None
) -> Path:
    """Return the file to open as *agent*'s stdin for this prompt file.

    Text-transport providers get the prompt file itself. Stream-json providers
    get a 0600 sibling (or *target*) holding the encoded user turn; it is
    rewritten on every call so a re-launch never replays a stale turn.
    """
    if stdin_transport(agent) != STREAM_JSON_TRANSPORT:
        return prompt_file
    return write_stream_json_file(
        prompt_file, target if target is not None else stream_json_sibling(prompt_file)
    )


def main(argv: Sequence[str] | None = None) -> int:
    """``python -m vibecrafted_core.prompt_transport AGENT PROMPT_FILE [TARGET]``.

    Shell launchers call this instead of carrying their own encoder. Prints the
    materialized stdin path. With ``--print-limit-flags AGENT`` it prints that
    provider's print-mode limit flags instead (an empty line when unbounded).
    """
    parser = argparse.ArgumentParser(prog="vibecrafted_core.prompt_transport")
    parser.add_argument("--print-limit-flags", action="store_true")
    parser.add_argument("agent")
    parser.add_argument("prompt_file", nargs="?")
    parser.add_argument("target", nargs="?")
    args = parser.parse_args(list(sys.argv[1:] if argv is None else argv))
    if args.print_limit_flags:
        try:
            print(" ".join(print_limit_flags(args.agent)))
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        return 0
    if not args.prompt_file:
        parser.error("prompt_file is required")
    target = Path(args.target) if args.target else None
    print(materialize_stdin_file(args.agent, Path(args.prompt_file), target))
    return 0


if __name__ == "__main__":  # module entry
    raise SystemExit(main())
