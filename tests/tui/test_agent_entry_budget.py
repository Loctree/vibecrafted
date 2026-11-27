"""Agent entry files stay within one byte budget.

Every agent reads ``AGENTS.md`` and the ``SKILL.md`` it loads on every turn.
Codex caps project instructions (``project_doc_max_bytes``, 32 768 bytes by
default) together with the user's global instructions and silently trims the
project file past the cap; on 2026-11-27 that dropped the repository-specific
rules from the end of a 27 KB ``AGENTS.md``. Doctrine that does not bind every
turn belongs in ``docs/agents/`` or a skill's ``references/``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

ENTRY_BUDGET_BYTES = 12_000

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = REPO_ROOT / "vibecrafted-core" / "vibecrafted_core" / "skills"


def _entry_files() -> list[Path]:
    return [REPO_ROOT / "AGENTS.md", *sorted(SKILLS_ROOT.rglob("SKILL.md"))]


def test_entry_files_exist() -> None:
    files = _entry_files()
    assert files[0].is_file()
    assert len(files) > 1, "no SKILL.md found under the skill store"


@pytest.mark.parametrize(
    "entry", _entry_files(), ids=lambda path: str(path.relative_to(REPO_ROOT))
)
def test_entry_file_fits_the_budget(entry: Path) -> None:
    size = entry.stat().st_size
    assert size <= ENTRY_BUDGET_BYTES, (
        f"{entry.relative_to(REPO_ROOT)} is {size} bytes, over the "
        f"{ENTRY_BUDGET_BYTES}-byte agent entry budget; move material that "
        "does not bind every turn into docs/agents/ or references/"
    )


def test_agents_md_keeps_the_managed_doctrine_block() -> None:
    text = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert text.count("<!-- loctree-advise: v1 -->") == 1
    assert text.count("<!-- /loctree-advise -->") == 1


@pytest.mark.parametrize(
    "reference",
    [
        "docs/agents/BEHAVIOR_STANDARD.md",
        "docs/agents/MANIFESTO.md",
        "docs/agents/SCAFFOLD_EDITOR_IA.md",
        "docs/runtime/OMNI_OBSERVER_SLACK_GATEWAY.md",
    ],
)
def test_agents_md_pointers_resolve(reference: str) -> None:
    assert reference in (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert (REPO_ROOT / reference).is_file()
