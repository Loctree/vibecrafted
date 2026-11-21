"""Doubles for the Apple trust boundary of ``external_products``.

Production admits ``vc-terminal`` and ``vc-frame`` only after ``codesign``
proves the Developer ID requirement and, for the app, Gatekeeper accepts it.
Fixture binaries cannot carry that signature, so tests double exactly these
two checks, and only for the paths a fixture owns. Every other path still
meets the real ``codesign`` and ``spctl`` checks, so a test cannot widen
admission by accident.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_SOURCE = REPO_ROOT / "vibecrafted-core/vibecrafted_core/external_products.py"
_MAIN_GUARD = '\n\nif __name__ == "__main__":\n'


def _names(trusted: Iterable[Path | str]) -> frozenset[str]:
    names = set()
    for path in trusted:
        names.add(str(Path(path)))
        names.add(str(Path(path).resolve()))
    return frozenset(names)


def double_apple_trust(monkeypatch, products, *, trusted) -> list[tuple[str, str]]:
    """Double the boundary in this process; returns the calls the doubles answered."""
    names = _names(trusted)
    answered: list[tuple[str, str]] = []
    real_developer_id = products._require_developer_id
    real_gatekeeper = products._require_gatekeeper

    def developer_id(path, identifier):
        if str(path) in names:
            answered.append(("developer-id", str(path)))
            return None
        return real_developer_id(path, identifier)

    def gatekeeper(app):
        if str(app) in names:
            answered.append(("gatekeeper", str(app)))
            return None
        return real_gatekeeper(app)

    monkeypatch.setattr(products, "_require_developer_id", developer_id)
    monkeypatch.setattr(products, "_require_gatekeeper", gatekeeper)
    return answered


def bind_apple_trust_in_copy(products_file: Path, *, trusted) -> None:
    """Double the boundary inside a private copy that a child runs as a script.

    Shell installers and runtime wrappers execute ``external_products.py`` in a
    new interpreter, where no monkeypatch reaches. The binding is inserted just
    before the script entry point of a copy staged under a test tree; the
    repository's own resolver is never rewritten.
    """
    products_file = Path(products_file)
    if products_file.resolve() == PRODUCTS_SOURCE.resolve():
        raise ValueError("refusing to rewrite the repository's product resolver")
    source = products_file.read_text(encoding="utf-8")
    if source.count(_MAIN_GUARD) != 1:
        raise AssertionError(f"{products_file} has no single script entry point")
    binding = f"""

# Test binding: the Apple trust boundary answers for fixture paths only.
_vc_fixture_trusted = frozenset({sorted(_names(trusted))!r})
_vc_fixture_real_developer_id = _require_developer_id
_vc_fixture_real_gatekeeper = _require_gatekeeper


def _require_developer_id(path, identifier):
    if str(path) in _vc_fixture_trusted:
        return None
    return _vc_fixture_real_developer_id(path, identifier)


def _require_gatekeeper(app):
    if str(app) in _vc_fixture_trusted:
        return None
    return _vc_fixture_real_gatekeeper(app)
"""
    products_file.write_text(
        source.replace(_MAIN_GUARD, binding + _MAIN_GUARD), encoding="utf-8"
    )


def doubled_products_source(root: Path, *, trusted) -> Path:
    """A minimal ``VIBECRAFTED_SOURCE`` whose resolver trusts fixture paths only.

    It carries what the foundations installer reads from its source: the
    product resolver (with its terminal owner) and the pinned components.
    """
    core = root / "vibecrafted-core/vibecrafted_core"
    core.mkdir(parents=True, exist_ok=True)
    for name in ("external_products.py", "terminal_host.py"):
        (core / name).write_bytes((PRODUCTS_SOURCE.parent / name).read_bytes())
    bind_apple_trust_in_copy(core / "external_products.py", trusted=trusted)
    config = root / "config"
    config.mkdir(exist_ok=True)
    components = REPO_ROOT / "config/source-components.json"
    (config / "source-components.json").write_bytes(components.read_bytes())
    return root
