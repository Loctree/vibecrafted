"""External product resolution is versioned, read-only, and never falls back."""

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from vibecrafted_core import external_products as products

from tests._apple_trust_fixture import double_apple_trust


def frame(directory: Path, version: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    binary = directory / "vc-frame"
    binary.write_text(f"#!/bin/sh\nprintf '%s\\n' 'vc-frame {version}'\n")
    binary.chmod(0o755)
    return binary.resolve()


@pytest.mark.parametrize("version", ["4.5.1", "4.5.2+g04d10480", "4.99.0"])
def test_frame_admits_declared_range(tmp_path: Path, monkeypatch, version: str) -> None:
    binary = frame(tmp_path / "host", version)
    answered = double_apple_trust(monkeypatch, products, trusted=(binary,))
    assert products.resolve_frame(search_path=str(binary.parent)) == binary
    if sys.platform == "darwin":
        assert answered == [("developer-id", str(binary))]


@pytest.mark.skipif(sys.platform != "darwin", reason="Developer ID is a macOS boundary")
def test_an_unsigned_frame_is_refused_before_it_runs(tmp_path: Path) -> None:
    binary = frame(tmp_path / "host", "4.5.1")
    marker = tmp_path / "ran"
    binary.write_text(f"#!/bin/sh\ntouch {marker}\nprintf '%s\\n' 'vc-frame 4.5.1'\n")
    with pytest.raises(
        products.ProductUnavailable, match="Developer ID team MW223P3NPX"
    ):
        products.resolve_frame(search_path=str(binary.parent))
    assert not marker.exists()


@pytest.mark.parametrize("version", ["4.5.0", "5.0.0", "garbage", "4.5.1 extra"])
def test_incompatible_first_path_hit_is_final(
    tmp_path: Path, monkeypatch, version: str
) -> None:
    rejected = frame(tmp_path / "first", version)
    good = frame(tmp_path / "second", "4.5.1")
    # Trust both so the version, not the signature, is what refuses the first hit.
    double_apple_trust(monkeypatch, products, trusted=(rejected, good))
    with pytest.raises(products.ProductUnavailable, match="incompatible vc-frame"):
        products.resolve_frame(search_path=f"{rejected.parent}:{good.parent}")


def test_frame_skips_current_generation_and_old_runtime_launchers(
    tmp_path: Path, monkeypatch
) -> None:
    runtime = tmp_path / "runtime"
    carried = frame(runtime / "bin", "4.5.1")
    old = frame(tmp_path / "old", "4.5.1")
    old.write_text('#!/bin/sh\nexport VIBECRAFTED_RUNTIME_ROOT="/old"\nexit 99\n')
    good = frame(tmp_path / "host", "4.5.1")
    double_apple_trust(monkeypatch, products, trusted=(good,))
    assert (
        products.resolve_frame(
            search_path=f".:{carried.parent}:{old.parent}:{good.parent}",
            runtime=runtime,
        )
        == good
    )


def test_missing_frame_has_one_line_install_hint() -> None:
    with pytest.raises(
        products.ProductUnavailable,
        match="missing from PATH.*https://github.com/vetcoders/vc-frame/releases",
    ):
        products.resolve_frame(search_path="")


def test_frame_probe_timeout_is_a_clear_refusal(tmp_path: Path, monkeypatch) -> None:
    binary = frame(tmp_path / "host", "4.5.1")

    def timeout(*args, **kwargs):
        raise products.subprocess.TimeoutExpired(args[0], 10)

    monkeypatch.setattr(products.subprocess, "run", timeout)
    with pytest.raises(products.ProductUnavailable, match="Install vc-frame"):
        products.resolve_frame(search_path=str(binary.parent))


@pytest.mark.parametrize("team,adhoc", [("wrong", False), (products.TEAM_ID, True)])
def test_terminal_requires_founder_signing_team(
    tmp_path: Path, monkeypatch, team, adhoc
) -> None:
    host = tmp_path / "vc-terminal.app/Contents/MacOS/vc-terminal"
    host.parent.mkdir(parents=True)
    host.write_bytes(b"fake")
    host.chmod(0o755)
    monkeypatch.setattr(products.terminal_host, "STANDALONE_HOST", str(host))
    monkeypatch.setattr(
        products.terminal_host, "require_standalone_bundle_metadata", lambda _: None
    )
    monkeypatch.setattr(
        products.terminal_host,
        "static_code_identity",
        lambda _: SimpleNamespace(team=team, adhoc=adhoc),
    )
    with pytest.raises(
        products.ProductUnavailable, match="MW223P3NPX.*Install vc-terminal"
    ):
        products.resolve_terminal()


def test_terminal_admits_independent_code_without_generation_hash(
    tmp_path: Path, monkeypatch
) -> None:
    host = tmp_path / "vc-terminal.app/Contents/MacOS/vc-terminal"
    host.parent.mkdir(parents=True)
    host.write_bytes(b"independent terminal code")
    host.chmod(0o755)
    monkeypatch.setattr(products.terminal_host, "STANDALONE_HOST", str(host))
    monkeypatch.setattr(
        products.terminal_host, "require_standalone_bundle_metadata", lambda _: None
    )
    checked = []

    def identity(path):
        checked.append(path)
        return SimpleNamespace(team=products.TEAM_ID, adhoc=False)

    monkeypatch.setattr(products.terminal_host, "static_code_identity", identity)
    answered = double_apple_trust(monkeypatch, products, trusted=(host.parents[2],))
    assert products.resolve_terminal() == host
    assert checked == [str(host), str(host.parents[2])]
    # Developer ID and Gatekeeper both ran against the bundle, in that order.
    assert answered == [
        ("developer-id", str(host.parents[2])),
        ("gatekeeper", str(host.parents[2])),
    ]


def test_status_reports_missing_products_without_installing(monkeypatch) -> None:
    def missing():
        raise products.ProductUnavailable("install independently")

    monkeypatch.setattr(products, "resolve_terminal", missing)
    monkeypatch.setattr(products, "resolve_frame", missing)
    assert all(
        item["status"] == "unavailable" for item in products.product_status().values()
    )
