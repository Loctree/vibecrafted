"""Linux release receipt boundaries. Fabricated carriers never become a channel."""

from __future__ import annotations

import hashlib
import io
import json
import subprocess
import tarfile
from pathlib import Path

import pytest
import yaml

from scripts import linux_release_manifest as release

SOURCE = "1" * 40
TERMINAL = "2" * 40
FRAME = "3" * 40
CONTROLLER = "4" * 40
REQUEST = "a" * 24
GATES = {"ubuntu_native": "success", "debian_12": "success"}


@pytest.fixture(scope="module")
def signing(tmp_path_factory):
    directory = tmp_path_factory.mktemp("linux-receipt-test-key")
    key, public = directory / "fixture.key", directory / "fixture.pub"
    subprocess.run(
        [
            "openssl",
            "genpkey",
            "-algorithm",
            "RSA",
            "-pkeyopt",
            "rsa_keygen_bits:2048",
            "-out",
            str(key),
        ],
        check=True,
    )
    subprocess.run(
        ["openssl", "pkey", "-in", str(key), "-pubout", "-out", str(public)],
        check=True,
    )
    return key, public


def _sign(key: Path, path: Path) -> None:
    subprocess.run(
        [
            "openssl",
            "dgst",
            "-sha256",
            "-sign",
            str(key),
            "-out",
            f"{path}.sig",
            str(path),
        ],
        check=True,
    )


def _carrier(directory: Path, key: Path, *, platform: str = "linux-x64") -> Path:
    architecture = "x64" if platform == "linux-x64" else "arm64"
    name = f"Vibecrafted_RuntimePack_4.6.0-20261124-{SOURCE[:8]}-{platform}.tar.gz"
    pack = directory / name
    provenance = {
        "schema": "io.vetcoders.vibecrafted.runtime-pack-provenance.v1",
        "version": "4.6.0",
        "platform": platform,
        "architecture": architecture,
        "carrier_basename": name,
        "source_revisions": {
            "vibecrafted": SOURCE,
            "vc-terminal": TERMINAL,
            "vc-frame": FRAME,
        },
    }
    body = json.dumps(provenance).encode()
    with tarfile.open(pack, "w:gz") as archive:
        member = tarfile.TarInfo("VibecraftedRuntime/runtime-pack-provenance.json")
        member.size = len(body)
        archive.addfile(member, io.BytesIO(body))
    digest = hashlib.sha256(pack.read_bytes()).hexdigest()
    Path(f"{pack}.sha256").write_text(f"{digest}  {pack.name}\n", encoding="ascii")
    _sign(key, pack)
    return pack


def _manifest(directory: Path, public: Path, **overrides):
    values = {
        "platform": "linux-x64",
        "source_sha": SOURCE,
        "terminal_sha": TERMINAL,
        "frame_sha": FRAME,
        "controller_sha": CONTROLLER,
        "repository": "vetcoders/vibecrafted",
        "run_id": 7,
        "run_attempt": 1,
        "request_id": REQUEST,
        "verification": GATES,
    }
    values.update(overrides)
    return release.build_manifest(directory, public, **values)


def test_product_signed_pack_becomes_a_linux_x64_receipt(signing, tmp_path):
    key, public = signing
    _carrier(tmp_path, key)
    receipt = _manifest(tmp_path, public)
    assert receipt["schema"] == release.SCHEMA
    assert receipt["product"] == {
        "version": "4.6.0",
        "platform": "linux-x64",
        "architecture": "x64",
    }
    assert receipt["signing"] == {"runtime_pack": "product-key"}
    assert receipt["verification"] == GATES
    assert receipt["runtime_pack"]["path"].endswith("-linux-x64.tar.gz")


def test_rehearsal_key_and_failed_gate_are_refused(signing, tmp_path):
    key, public = signing
    _carrier(tmp_path, key)
    (tmp_path / "ci-signing.pub").write_text("rehearsal\n", encoding="ascii")
    with pytest.raises(ValueError, match="rehearsal"):
        _manifest(tmp_path, public)
    (tmp_path / "ci-signing.pub").unlink()
    with pytest.raises(ValueError, match="native Linux install"):
        _manifest(
            tmp_path,
            public,
            verification={"ubuntu_native": "success", "debian_12": "failure"},
        )


def test_wrong_key_and_wrong_repository_are_refused(signing, tmp_path):
    key, public = signing
    pack = _carrier(tmp_path, key)
    other = tmp_path / "other.key"
    subprocess.run(
        [
            "openssl",
            "genpkey",
            "-algorithm",
            "RSA",
            "-pkeyopt",
            "rsa_keygen_bits:2048",
            "-out",
            str(other),
        ],
        check=True,
    )
    Path(f"{pack}.sig").unlink()
    _sign(other, pack)
    with pytest.raises(ValueError, match="product key"):
        _manifest(tmp_path, public)
    Path(f"{pack}.sig").unlink()
    _sign(key, pack)
    with pytest.raises(ValueError, match="workflow identity"):
        _manifest(tmp_path, public, repository="Loctree/vibecrafted")


def test_install_linux_workflow_publishes_x64_and_keeps_arm64_optional():
    workflow = Path(__file__).resolve().parents[2] / ".github/workflows/install-linux.yml"
    text = workflow.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    dispatch = data[True]["workflow_dispatch"]["inputs"]
    assert dispatch["release_signing"]["default"] is True
    assert dispatch["include_arm64"]["default"] is False
    jobs = data["jobs"]
    release_job = jobs["linux-x64-release"]
    assert release_job["needs"] == [
        "linux-runtime-pack",
        "ubuntu-native",
        "debian-bookworm-container",
    ]
    assert "include_arm64" not in release_job["if"]
    assert "inputs.include_arm64" in jobs["linux-arm64-runtime-pack"]["if"]
    assert "secrets.VC_SIGNING_KEY" in text
    assert "scripts/build-linux-runtime-pack.sh" in text
    assert "build-linux-arm64-runtime-pack.sh" not in text
    assert "Vibecrafted_RuntimePack_linux-x64.tar.gz" in text
    assert "openssl dgst -sha256 -sign" in text
    assert "openssl dgst -sha256 -verify" in text
    assert "genpkey -algorithm RSA" in text
    assert "genpkey -algorithm ED25519" not in text
    assert "openssl pkeyutl -sign -rawin" not in text
    installer = Path(__file__).resolve().parents[2] / "install.sh"
    assert (
        "No prebuilt Runtime Pack available for $channel_platform on channel $ref"
        in installer.read_text(encoding="utf-8")
    )
