"""Vibecrafted 4.5.4 -> 4.6.x handoff: the newer carrier performs the upgrade.

Integrator acceptance for wave runtime-handoff-20261120 (decision of Maciej,
2026-11-20: three products with three lifecycles, fix the shape). Each test
names the invariant of the shared wire contract it falsifies. They are written
against the contract, not against a worker's implementation, and every one of
them is expected RED on the wave base 40ca87d0 unless it says it is a control.
"""

from __future__ import annotations

import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest

from scripts import vetcoders_install as installer

REPO_ROOT = Path(__file__).resolve().parents[2]
PACK_INSTALLER = REPO_ROOT / "scripts/install-runtime-pack.sh"
FOUNDATIONS = REPO_ROOT / "scripts/install-foundations.sh"
POLICY = (
    REPO_ROOT / "vibecrafted-app/shell-agent/app/Vibecrafted/ServerMenuPolicy.swift"
)
COMPONENTS = REPO_ROOT / "config/source-components.json"

DARWIN_ONLY = pytest.mark.skipif(
    sys.platform != "darwin", reason="independent Darwin product launchers"
)


def _executable(path: Path, body: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    path.chmod(0o755)
    return path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _last_line(stream: str) -> str:
    lines = [line for line in stream.splitlines() if line.strip()]
    return lines[-1] if lines else ""


# --- S1 / G3: flag arity of the carrier installer ------------------------------


def _run_pack_installer(
    tmp_path: Path, *flags: str
) -> subprocess.CompletedProcess[str]:
    pack = tmp_path / "Vibecrafted_RuntimePack_test.tar.gz"
    pack.write_bytes(b"")
    return subprocess.run(
        ["bash", str(PACK_INSTALLER), "--pack", str(pack), *flags],
        cwd=REPO_ROOT,
        env={
            "HOME": str(tmp_path / "home"),
            "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
            "TMPDIR": str(tmp_path),
        },
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )


def test_app_root_alone_is_an_admitted_b2_invocation(tmp_path: Path) -> None:
    """G3 (ii): the 4.6 App sends --app-root alone; arity must not refuse it.

    RED on 40ca87d0: the carrier refused its own App with "must be supplied
    together" before it ever looked at the pack.
    """
    app = tmp_path / "Vibecrafted.app"
    app.mkdir()

    result = _run_pack_installer(tmp_path, "--app-root", str(app))

    assert "must be supplied together" not in result.stderr, result.stderr
    assert "--app-root alone" not in result.stderr, result.stderr


def test_a_partial_helper_pair_is_refused_with_one_actionable_line(
    tmp_path: Path,
) -> None:
    """Control for G3 (iii): two of the three paired flags still refuse (I5)."""
    app = tmp_path / "Vibecrafted.app"
    app.mkdir()
    host = _executable(tmp_path / "vc-terminal", "#!/bin/sh\nexit 0\n")

    result = _run_pack_installer(
        tmp_path, "--app-root", str(app), "--terminal-host", str(host)
    )

    assert result.returncode != 0
    last = _last_line(result.stderr)
    assert "--app-root" in last and "--frame-helper" in last, result.stderr


# --- I8 / G1: reclaim never removes vc-frame before the product is admitted ----


def _legacy_frame_receipt(tmp_path: Path) -> tuple[Path, Path, Path, dict, dict]:
    runtime = tmp_path / "runtime"
    generation_bin = runtime / "releases/4.6.0+gcarrier/bin"
    generation_bin.mkdir(parents=True)
    launcher_home = tmp_path / "launchers"
    shim = _executable(
        launcher_home / "vc-frame", '#!/bin/sh\nexec 4.5.4-generation/vc-frame "$@"\n'
    )
    backup = _executable(
        runtime / ".installer-backups/original/vc-frame",
        "#!/bin/sh\necho pre-vibecrafted-vc-frame\n",
    )
    receipt = {
        "owned_files": {str(shim): _sha256(shim)},
        "owned_symlinks": {},
        "backups": {str(shim): str(backup)},
    }
    return (
        runtime,
        generation_bin,
        launcher_home,
        receipt,
        json.loads(json.dumps(receipt)),
    )


@DARWIN_ONLY
def test_the_legacy_vc_frame_shim_survives_until_the_product_is_admitted(
    tmp_path: Path,
) -> None:
    """I8: without an admitted standalone vc-frame the 4.5.4 name keeps working.

    RED on 40ca87d0: reclaim removed the shim (and restored an older backup)
    before foundations had provisioned the product — the G1 deadlock.
    """
    runtime, generation_bin, launcher_home, receipt, previous = _legacy_frame_receipt(
        tmp_path
    )
    shim = launcher_home / "vc-frame"
    before = shim.read_bytes()

    installer._reclaim_foreign_launcher_names(
        generation_bin,
        launcher_home,
        runtime_home=runtime,
        receipt=receipt,
        previous=previous,
    )

    assert shim.exists() and not shim.is_symlink()
    assert shim.read_bytes() == before


@DARWIN_ONLY
def test_the_admitted_vc_frame_takes_the_name_in_one_rename(tmp_path: Path) -> None:
    """I8 + I6: once admitted, the name points at the product and 4.5.4 lets go.

    RED on 40ca87d0 by API absence: the base reclaim cannot be told which
    product was admitted, so it can only delete the name.
    """
    runtime, generation_bin, launcher_home, receipt, previous = _legacy_frame_receipt(
        tmp_path
    )
    product = _executable(
        tmp_path / "home/.local/share/vc-frame/4.5.1-abc/vc-frame",
        "#!/bin/sh\necho 'vc-frame 4.5.1'\n",
    )
    shim = launcher_home / "vc-frame"
    backup = Path(receipt["backups"][str(shim)])
    backup_bytes = backup.read_bytes()

    installer._reclaim_foreign_launcher_names(
        generation_bin,
        launcher_home,
        runtime_home=runtime,
        receipt=receipt,
        previous=previous,
        admitted_frame=product,
    )

    assert shim.is_symlink()
    assert shim.resolve() == product.resolve()
    assert str(shim) not in receipt["owned_files"]
    assert str(shim) not in receipt.get("owned_symlinks", {})
    assert str(shim) not in receipt["backups"]
    # The pre-Vibecrafted copy is history, never restored over the product.
    assert backup.read_bytes() == backup_bytes
    assert not list(launcher_home.glob(".frame-handoff-*"))


# --- S4 / S2: foundations replaces only the receipted legacy shim --------------


def _frame_release(tmp_path: Path) -> str:
    target = {
        ("Darwin", "arm64"): "aarch64-apple-darwin",
        ("Darwin", "x86_64"): "x86_64-apple-darwin",
        ("Linux", "x86_64"): "x86_64-unknown-linux-musl",
        ("Linux", "aarch64"): "aarch64-unknown-linux-musl",
    }.get((platform.system(), platform.machine()), "unpublished-host")
    version = json.loads(COMPONENTS.read_text(encoding="utf-8"))["components"][
        "vc-frame"
    ]["version"]
    staged = _executable(
        tmp_path / "frame-staged/vc-frame", f"#!/bin/sh\necho 'vc-frame {version}'\n"
    )
    release = tmp_path / "frame-release"
    release.mkdir()
    asset = release / f"vc-frame-{target}.tar.gz"
    with tarfile.open(asset, "w:gz") as archive:
        archive.add(staged, arcname="vc-frame")
    (release / f"{asset.name}.sha256").write_text(
        f"{_sha256(asset)}  {asset.name}\n", encoding="utf-8"
    )
    return target


def _run_frame_target(tmp_path: Path, **extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(FOUNDATIONS), "vc-frame"],
        cwd=REPO_ROOT,
        env={
            "HOME": str(tmp_path / "home"),
            "PATH": ":".join(
                [str(tmp_path / "bin"), "/usr/bin", "/bin", "/usr/sbin", "/sbin"]
            ),
            "TMPDIR": str(tmp_path),
            "UV_RELEASE_BASE": f"file://{tmp_path / 'no-uv-release'}",
            "VCFRAME_RELEASE_BASE": f"file://{tmp_path / 'frame-release'}",
            **extra,
        },
        text=True,
        capture_output=True,
        timeout=300,
        check=False,
    )


def _legacy_shim(tmp_path: Path) -> Path:
    return _executable(
        tmp_path / "home/.local/bin/vc-frame",
        '#!/bin/sh\nexec "$HOME/.local/share/vibecrafted/releases/4.5.4/libexec/vc-frame" "$@"\n',
    )


def test_the_receipted_legacy_shim_is_replaceable(tmp_path: Path) -> None:
    """S4: the hash from the previous receipt authorizes replacing the 4.5.4 shim.

    RED on 40ca87d0: the shim "belongs to another install" and the upgrade
    deadlocks. On macOS the unsigned test release is then refused by the
    publisher check, so the shim must still be byte-identical afterwards.
    """
    target = _frame_release(tmp_path)
    shim = _legacy_shim(tmp_path)
    before = shim.read_bytes()

    result = _run_frame_target(
        tmp_path, VIBECRAFTED_LEGACY_VCFRAME_SHA256=_sha256(shim)
    )
    output = result.stdout + result.stderr

    assert "belongs to another install" not in output, output
    if target.endswith("apple-darwin"):
        assert "Developer ID team" in output, output
        assert shim.read_bytes() == before
    elif target != "unpublished-host":
        assert shim.is_symlink(), output


def test_a_foreign_vc_frame_is_never_replaced(tmp_path: Path) -> None:
    """Control for S4 / I10: a file whose hash the receipt does not vouch for stays."""
    _frame_release(tmp_path)
    shim = _legacy_shim(tmp_path)
    before = shim.read_bytes()

    result = _run_frame_target(tmp_path, VIBECRAFTED_LEGACY_VCFRAME_SHA256="0" * 64)

    assert result.returncode != 0
    assert shim.read_bytes() == before
    assert not shim.is_symlink()


def test_a_missing_vc_frame_cannot_be_waived_by_require_foundations(
    tmp_path: Path,
) -> None:
    """S2: the carrier must not publish without its products.

    RED on 40ca87d0: REQUIRE_FOUNDATIONS=0 turned a refused vc-frame into a
    warning and exit 0, so the caller could not tell admission had failed.
    """
    _frame_release(tmp_path)
    shim = _legacy_shim(tmp_path)

    result = _run_frame_target(tmp_path, REQUIRE_FOUNDATIONS="0")

    assert result.returncode != 0, result.stdout + result.stderr
    assert _last_line(result.stderr), "a refusal ends with one actionable line"
    assert shim.read_bytes().startswith(b"#!/bin/sh")


# --- I1 / I5: the App offers Upgrade, Repair or a downgrade refusal -------------

PRESENTATION_MAIN = r"""
import Foundation

func check(_ ok: Bool, _ message: String) {
  if !ok { print("FAIL: " + message); exit(1) }
}

let carrier = "4.6.0+g40ca87d0"
let older = runtimeReinstallPresentation(
  resolution: .ready("4.5.4+g9af7de19"), carrierGeneration: carrier, configuration: "")
check(older.actionTitle?.hasPrefix("Upgrade to Vibecrafted 4.6.0") == true,
  "an older active runtime must offer Upgrade to the carrier: \(String(describing: older.actionTitle))")

let newer = runtimeReinstallPresentation(
  resolution: .ready("4.7.0+gabcdef12"), carrierGeneration: carrier, configuration: "")
check(newer.actionTitle == nil,
  "a newer active runtime must get no carrier action: \(String(describing: newer.actionTitle))")
check(newer.detail.contains("4.7.0"), "the downgrade refusal names the active runtime")

let same = runtimeReinstallPresentation(
  resolution: .ready(carrier), carrierGeneration: carrier, configuration: "")
check(same.title == "Vibecrafted runtime already current", "same generation: \(same.title)")

print("RuntimeCarrierPresentation passed")
"""


def test_the_app_offers_upgrade_and_refuses_a_downgrade(tmp_path: Path) -> None:
    """I1 + I5 in the App's presentation policy.

    RED on 40ca87d0: an older active runtime got "Use this App's runtime?"
    (no Upgrade), and a newer one was offered the older carrier.
    """
    swiftc = shutil.which("swiftc")
    if swiftc is None or sys.platform != "darwin":
        pytest.skip("swiftc on macOS is required for the App presentation policy")
    main = tmp_path / "main.swift"
    main.write_text(PRESENTATION_MAIN, encoding="utf-8")
    binary = tmp_path / "runtime-carrier-presentation"
    subprocess.run(
        [swiftc, str(POLICY), str(main), "-o", str(binary)],
        check=True,
        cwd=REPO_ROOT,
        timeout=300,
    )
    completed = subprocess.run(
        [str(binary)], capture_output=True, text=True, timeout=30, check=False
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "RuntimeCarrierPresentation passed" in completed.stdout
