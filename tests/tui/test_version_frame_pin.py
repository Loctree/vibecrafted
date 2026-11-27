"""The Frame source pin names a vc-frame the runtime accepts on PATH."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "version_bump.py"


def layout(tmp_path: Path, product: str, frame: str) -> Path:
    (tmp_path / "VERSION").write_text(product + "\n", encoding="utf-8")
    pins = tmp_path / "config" / "source-components.json"
    pins.parent.mkdir()
    pins.write_text(
        json.dumps({"components": {"vc-frame": {"version": frame}}}), encoding="utf-8"
    )
    return tmp_path / "VERSION"


@pytest.mark.parametrize(
    ("frame", "accepted"),
    [
        ("4.5.1", True),
        ("4.6.0", True),
        ("4.9.3", True),
        ("4.5.0", False),
        ("5.0.0", False),
        ("4.6", False),
    ],
)
def test_version_gate_keeps_the_frame_pin_in_the_required_range(
    tmp_path: Path, frame: str, accepted: bool
) -> None:
    # Frame keeps its own SemVer: the product version does not bind it.
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--check",
            "--file",
            str(layout(tmp_path, "4.6.0", frame)),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert (result.returncode == 0) is accepted, result.stderr
    if not accepted:
        assert f"source-components.json#vc-frame={frame}" in result.stderr
        assert "Install vc-frame >=4.5.1,<5.0.0" in result.stderr


def test_repository_frame_pin_is_in_range() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--check", "--file", str(ROOT / "VERSION")],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
