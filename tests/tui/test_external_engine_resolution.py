"""A Darwin generation finds vc-frame and vc-terminal as external products.

A Darwin Runtime Pack carries no native engine under ``libexec``: the installer
refuses one that does. The shell facade must therefore accept such a generation
when its own product resolver vouches for the engine, and must say why when the
resolver refuses instead of advising a Runtime Pack reinstall.

𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI
"""

from __future__ import annotations

import shlex
import subprocess
import sys
from pathlib import Path

import pytest

from tests.tui import _generation_fixture as gen

FACADE = gen.REPO_ROOT / "vibecrafted-core/vibecrafted_core/runtime/shell/vetcoders.sh"

pytestmark = pytest.mark.skipif(
    sys.platform != "darwin", reason="external products are the Darwin contract"
)

# Stand-in for the generation's resolver: the real one proves Developer ID and
# Gatekeeper on host installs. This one answers from a marker file.
_RESOLVER = """import sys
from pathlib import Path

marker = Path(__file__).with_name(f"{sys.argv[1]}.available")
if not marker.is_file():
    print(f"vc-{sys.argv[1]} missing from PATH. fixture hint", file=sys.stderr)
    raise SystemExit(69)
print(marker.read_text().strip())
"""


def _darwin_pack(tmp_path: Path, *, available: tuple[str, ...]) -> Path:
    """A generation shaped like an installed Darwin pack: entries, no libexec."""
    generation = tmp_path / "generation"
    for entry in ("vc-frame", "vc-terminal"):
        gen.write_executable(generation / "bin" / entry, "#!/bin/sh\nexit 0\n")
    gen.write_executable(
        generation / "bin" / "python3",
        f'#!/bin/sh\nexec {shlex.quote(sys.executable)} "$@"\n',
    )
    core = generation / "vibecrafted-core/vibecrafted_core"
    core.mkdir(parents=True)
    (core / "external_products.py").write_text(_RESOLVER, encoding="utf-8")
    for product in available:
        (core / f"{product}.available").write_text(f"/external/vc-{product}\n")
    return generation


def _resolve(generation: Path, function: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "bash",
            "--noprofile",
            "--norc",
            "-c",
            (
                f"source {shlex.quote(str(FACADE))} >/dev/null 2>&1; "
                f"{gen.loaded_root_prelude(generation)}; {function}"
            ),
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )


def test_darwin_pack_without_libexec_resolves_both_entries(tmp_path: Path) -> None:
    generation = _darwin_pack(tmp_path, available=("frame", "terminal"))
    assert not (generation / "libexec").exists()

    frame = _resolve(generation, "_vetcoders_vc_frame_bin")
    terminal = _resolve(generation, "_vetcoders_vc_terminal_bin")

    assert frame.returncode == 0, frame.stderr
    assert frame.stdout.strip() == str(generation / "bin/vc-frame")
    assert terminal.returncode == 0, terminal.stderr
    assert terminal.stdout.strip() == str(generation / "bin/vc-terminal")


def test_darwin_pack_refusal_names_the_resolvers_reason(tmp_path: Path) -> None:
    generation = _darwin_pack(tmp_path, available=())

    frame = _resolve(generation, "_vetcoders_vc_frame_bin")
    terminal = _resolve(
        generation,
        "_vetcoders_vc_terminal_bin || _vetcoders_vc_terminal_missing_message",
    )

    assert frame.returncode == 1
    assert "vc-frame missing from PATH. fixture hint" in frame.stderr
    assert "vc-terminal missing from PATH. fixture hint" in terminal.stderr
    # Reinstalling the Runtime Pack cannot supply an external product.
    for refusal in (frame, terminal):
        assert "Install explicitly" not in refusal.stderr
        assert "{bin,libexec}" not in refusal.stderr
