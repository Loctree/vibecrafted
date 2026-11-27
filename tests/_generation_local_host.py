"""Run the entry logic against the generation-local product contract on any host.

Since 2026-11-23 a Darwin generation does not read ``libexec``:
``bin/vc-frame`` and ``bin/vc-terminal`` exec what the external product
resolver returns. That resolver finds ``vc-terminal`` only at the fixed
``/Applications/vc-terminal.app`` and admits nothing without the publisher's
Developer ID. A fixture cannot stand there. Doubling the location would
aim a test at the real application on a developer Mac.

Tests about the public entries (start, resume, declaration, escalation) are
not tests of Darwin product admission. They run the generation-local contract
that Linux ships, on every host: the shell runtime's ``uname -s`` answers
``Linux``, and every other ``uname`` question reaches the real tool. On macOS
the entries still run under the host's own bash 3.2, zsh and BSD userland.
Darwin admission keeps its own coverage in ``test_external_products`` and in
the ``external`` mode of ``test_product_entry_policy``.
"""

from __future__ import annotations

import os
import shlex
import shutil
from pathlib import Path

_REAL_UNAME = shutil.which("uname", path="/usr/bin:/bin") or "/usr/bin/uname"


def generation_local_host_bin(root: Path) -> Path:
    """A directory whose ``uname`` presents the generation-local (Linux) host."""
    bin_dir = Path(root) / "generation-local-host"
    bin_dir.mkdir(parents=True, exist_ok=True)
    uname = bin_dir / "uname"
    uname.write_text(
        "#!/bin/sh\n"
        'if [ "$#" -eq 0 ] || { [ "$#" -eq 1 ] && [ "$1" = "-s" ]; }; then\n'
        "  echo Linux\n"
        "  exit 0\n"
        "fi\n"
        f'exec {shlex.quote(_REAL_UNAME)} "$@"\n',
        encoding="utf-8",
    )
    uname.chmod(0o755)
    return bin_dir


def present_generation_local_host(monkeypatch, root: Path) -> Path:
    """Put the generation-local host first on this test's ``PATH``.

    Every child environment the test derives from ``os.environ`` inherits it;
    ``monkeypatch`` restores the host's own ``PATH`` afterwards.
    """
    bin_dir = generation_local_host_bin(root)
    monkeypatch.setenv(
        "PATH",
        os.pathsep.join(
            part for part in (str(bin_dir), os.environ.get("PATH", "")) if part
        ),
    )
    return bin_dir
