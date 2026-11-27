#!/usr/bin/env python3
"""Bind one tested Linux Runtime Pack to a product source and workflow run.

The receipt is the Linux counterpart of windows-release.json: a product-key
signature over the carrier, the closed provenance inside it, and the native
install jobs that had to succeed before publication. A CI rehearsal key is
never a website trust anchor.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tarfile
from pathlib import Path

SCHEMA = "io.vetcoders.vibecrafted.linux-release-output.v1"
_SHA = re.compile(r"[0-9a-f]{40}\Z")
_PLATFORMS = {
    "linux-x64": "x64",
    "linux-arm64": "arm64",
}
_GATES = {
    "linux-x64": {"ubuntu_native": "success", "debian_12": "success"},
    "linux-arm64": {"native_install": "success"},
}


def _regular(path: Path) -> None:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"missing or non-regular release artifact: {path.name}")


def _record(path: Path) -> dict:
    _regular(path)
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    return {"path": path.name, "sha256": digest, "size": path.stat().st_size}


def _checksummed(path: Path) -> dict:
    record = _record(path)
    sidecar = Path(f"{path}.sha256")
    _regular(sidecar)
    if sidecar.stat().st_size > 4096:
        raise ValueError(f"oversized checksum: {sidecar.name}")
    line = sidecar.read_text(encoding="ascii").strip().split()
    if line != [record["sha256"], path.name]:
        raise ValueError(f"checksum mismatch: {path.name}")
    return record


def _one(directory: Path, pattern: str) -> Path:
    matches = list(directory.glob(pattern))
    if len(matches) != 1:
        raise ValueError(f"expected exactly one {pattern} artifact")
    _regular(matches[0])
    return matches[0]


def build_manifest(
    directory: Path,
    public_key: Path,
    *,
    platform: str,
    source_sha: str,
    terminal_sha: str,
    frame_sha: str,
    controller_sha: str,
    repository: str,
    run_id: int,
    run_attempt: int,
    request_id: str,
    verification: dict[str, str],
) -> dict:
    architecture = _PLATFORMS.get(platform)
    if architecture is None:
        raise ValueError("Linux release platform must be linux-x64 or linux-arm64")
    for value in (source_sha, terminal_sha, frame_sha, controller_sha):
        if not _SHA.fullmatch(value):
            raise ValueError("release revisions must be full lowercase Git SHAs")
    if repository != "vetcoders/vibecrafted" or run_id < 1 or run_attempt < 1:
        raise ValueError("invalid workflow identity")
    if not re.fullmatch(r"[0-9a-f]{24}", request_id):
        raise ValueError("release request_id must be 24 lowercase hex characters")
    if verification != _GATES[platform]:
        raise ValueError("native Linux install jobs must succeed")
    if any(directory.glob("*.rehearsal.*")) or (directory / "ci-signing.pub").exists():
        raise ValueError("rehearsal signing material cannot enter a release")
    pack = _one(directory, f"Vibecrafted_RuntimePack_*-{platform}.tar.gz")
    match = re.fullmatch(
        rf"Vibecrafted_RuntimePack_(\d+\.\d+\.\d+)-(\d{{8}})-([0-9a-f]{{8}})-{re.escape(platform)}\.tar\.gz",
        pack.name,
    )
    if not match or match[3] != source_sha[:8]:
        raise ValueError("Linux Runtime Pack name disagrees with product source")
    version = match[1]
    record = _checksummed(pack)
    signature = Path(f"{pack}.sig")
    _regular(signature)
    _regular(public_key)
    result = subprocess.run(
        [
            "openssl",
            "dgst",
            "-sha256",
            "-verify",
            str(public_key),
            "-signature",
            str(signature),
            str(pack),
        ],
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise ValueError("Linux Runtime Pack is not signed by the product key")
    with tarfile.open(pack, "r:gz") as archive:
        manifests = [
            member
            for member in archive
            if member.name == "VibecraftedRuntime/runtime-pack-provenance.json"
        ]
        if (
            len(manifests) != 1
            or not manifests[0].isfile()
            or not 0 < manifests[0].size <= 2_000_000
        ):
            raise ValueError("missing or ambiguous Runtime Pack provenance")
        extracted = archive.extractfile(manifests[0])
        if extracted is None:
            raise ValueError("missing or ambiguous Runtime Pack provenance")
        provenance = json.load(extracted)
    expected = {
        "vibecrafted": source_sha,
        "vc-terminal": terminal_sha,
        "vc-frame": frame_sha,
    }
    if (
        not isinstance(provenance, dict)
        or provenance.get("schema")
        != "io.vetcoders.vibecrafted.runtime-pack-provenance.v1"
        or provenance.get("source_revisions") != expected
        or provenance.get("platform") != platform
        or provenance.get("architecture") != architecture
        or provenance.get("carrier_basename") != pack.name
        or provenance.get("version") not in (version, f"{version}+g{source_sha[:8]}")
    ):
        raise ValueError(
            "Linux Runtime Pack provenance disagrees with the release request"
        )
    return {
        "schema": SCHEMA,
        "product": {
            "version": version,
            "platform": platform,
            "architecture": architecture,
        },
        "source_revisions": expected,
        "runtime_pack": record,
        "workflow": {
            "repository": repository,
            "run_id": run_id,
            "run_attempt": run_attempt,
            "controller_sha": controller_sha,
            "source_sha": source_sha,
            "request_id": request_id,
        },
        "verification": verification,
        "signing": {"runtime_pack": "product-key"},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", required=True, type=Path)
    parser.add_argument("--public-key", required=True, type=Path)
    parser.add_argument("--platform", required=True, choices=tuple(_PLATFORMS))
    for name in (
        "source-sha",
        "terminal-sha",
        "frame-sha",
        "controller-sha",
        "repository",
        "request-id",
    ):
        parser.add_argument(f"--{name}", required=True)
    parser.add_argument("--run-id", required=True, type=int)
    parser.add_argument("--run-attempt", required=True, type=int)
    parser.add_argument("--ubuntu-native")
    parser.add_argument("--debian-12")
    parser.add_argument("--native-install")
    args = parser.parse_args()
    if args.platform == "linux-x64":
        verification = {
            "ubuntu_native": args.ubuntu_native,
            "debian_12": args.debian_12,
        }
    else:
        verification = {"native_install": args.native_install}
    try:
        receipt = build_manifest(
            args.directory,
            args.public_key,
            platform=args.platform,
            source_sha=args.source_sha,
            terminal_sha=args.terminal_sha,
            frame_sha=args.frame_sha,
            controller_sha=args.controller_sha,
            repository=args.repository,
            run_id=args.run_id,
            run_attempt=args.run_attempt,
            request_id=args.request_id,
            verification=verification,
        )
        output = args.directory / f"{args.platform}-release.json"
        if output.exists() or output.is_symlink():
            raise ValueError("release receipt already exists")
        output.write_text(
            json.dumps(receipt, sort_keys=True, indent=2) + "\n", encoding="utf-8"
        )
    except (OSError, ValueError, tarfile.TarError) as exc:
        parser.exit(1, f"Linux release refused: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
