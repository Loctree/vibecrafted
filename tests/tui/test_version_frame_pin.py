"""The Frame pinned into the product reports the product's version."""

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


@pytest.mark.parametrize(("frame", "accepted"), [("4.5.4", True), ("4.5.1", False)])
def test_version_gate_binds_the_frame_pin(
    tmp_path: Path, frame: str, accepted: bool
) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--check",
            "--file",
            str(layout(tmp_path, "4.5.4", frame)),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert (result.returncode == 0) is accepted, result.stderr
    if not accepted:
        assert "source-components.json#vc-frame=4.5.1" in result.stderr


def test_repository_frame_pin_matches_version() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--check", "--file", str(ROOT / "VERSION")],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
