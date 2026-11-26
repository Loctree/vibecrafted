---
name: vc-prview
description: >
  Bounded PR, branch, commit-range, or artifact-pack review pipeline: generate
  prview-rs artifacts then produce a findings-max audit. Use when the user asks
  to "review PR", "analyze branch", "run prview", "sprawdź PR", "zrób review",
  "audit PR", "daj findings", "zbadaj branch", "artifact pack", "PR quality
  check", "merge gate", "findings-max", "deep review", or needs structured diff
  artifacts with line-level analysis for AI review pipelines.
metadata:
  short-description: "Generate + audit PR artifacts, findings-max (v1)"
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

# vc-prview — Bounded Review Pipeline (Generate + Audit)

Two-phase skill: **Phase 1** generates structured artifacts with prview-rs,
**Phase 2** squeezes maximum findings from them. Output: P-leveled findings
with evidence + before-merge TODO checklist.

## Canonical Orientation Gate

Before using prview artifacts as release or merge truth, run or consume the
`vc-init` procedure for the assigned repo. `Loctree:loctree` is the default
structural perception skill for that pass and must produce or refresh the
Code-Derived Application Map.

If fresh `vc-init` evidence is absent, perform the init pass first and treat
review conclusions as blocked until repo truth exists.

Use Loctree to identify load-bearing files and blast radius; use prview to
audit the requested diff or artifact pack against that current structure.

Binary: `prview` (installed at `~/.cargo/bin/prview`)
Source: `https://github.com/LibraxisAI/prview-rs`
Author: Vetcoders

---

## Repository Work Doctrine

For repository work, start with Loctree as the map: use `loct context`,
`loct occurrences`, `loct body`, and `loct find --literal` before broad manual
search. Use AICX for intent and session context. Use rg/grep as fallback or
local magnifier, not as a replacement for structural mapping. If Loctree fails
or misses a surface, append feedback to `~/.vibecrafted/loctree/loctree-fail.md`.

## Phase 1 — Generate Artifacts

Generate structured review packs for local branches (`prview --pr <NUMBER>`), remote branches (`prview -R --remote-only <branch> <base>`), GitHub PRs (`prview --pr <NUMBER> --with-tests --with-lint`), or full gates (`prview --deep`). **Default: do not use `--quick` for PR review** (and do not use quick shell aliases `prv`, `prvpr`, `prvjson` for review-quality output).

Other modes (`--ci`, `--json --quiet`, `--update`, `--tui`), the full 23-flag table, auto-detected profiles (`rust`/`js`/`python`/`mixed`/`generic`), and `.prview-policy.yml` (`shadow`/`warn`/`block`) live in [references/cli-and-artifacts.md](references/cli-and-artifacts.md).

---

## Artifact Pack Layout

Output lands in `.tools/pr-artifacts/<branch>/<timestamp>/` (symlinked at `latest`); always select the **newest** `<timestamp>` (empty or missing directory → **P0**). Parse `report.json`, `00_summary/MERGE_GATE.json`, `SANITY.json`, `20_quality/*`, `30_context/INLINE_FINDINGS.sarif`, and `10_diff/per-file-diffs/`. Full tree & pipeline bootstrap: [references/cli-and-artifacts.md](references/cli-and-artifacts.md).

---

## Phase 2 — Analyze Artifacts (Findings-Max)

### Philosophy

Tryb: **Findings-max**. Nie kończ na "kilku punktach". Jeśli widać 25 osobnych
problemów, wypisz 25. Lepiej 20 celnych findingów niż 5 ogólników.

Każdy finding MUSI mieć **Dowód** (artefakt + ścieżka + 1–2 linie), **Komentarz** (dlaczego ważne + co grozi), i **Rekomendację** (co zrobić / jak zweryfikować). Nie łącz różnych tematów w 1 punkt; oznacz niepotwierdzone **[VERIFY]** i oddziel błędy kodu od **[TOOLING]**.

### P-Level Scale

| P-level | Definicja                                                          | Przykłady                                                              |
| ------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| **P0**  | Blocker merge / security / data loss / failing blocking check      | Failing tsc, leaked credentials, missing artifacts                     |
| **P1**  | Wysoki risk regresji w core flow, niekompatybilne zmiany kontraktu | Breaking API, duże zmiany bez testów, import cycles in critical module |
| **P2**  | Średni risk: edge-cases, a11y, telemetria, częściowy brak testów   | Missing i18n keys, hardcoded URLs, no error handling on external call  |
| **P3**  | Niskie ryzyko / higiena / drobne niespójności                      | Empty doc titles, test setup duplication, cosmetic naming              |

---

## Reading Order, Pattern Scans & Minimum Coverage

Follow the mandatory 8-step reading order (`AI_INDEX.md` → `report.json` → `MERGE_GATE.json`/`SANITY.json` → metadata/status/commits → `INLINE_FINDINGS.sarif` → `20_quality/*` → `changed-tests.txt` → selective `per-file-diffs/`). Scan patches for Rust, TS/JS, Security/PII, and Data/Performance patterns, cover all SARIF entries, top-10 churn files, risk paths, `NO_TEST_CHANGE`, `BREAKING_CHANGES.md`, and handle special tooling cases (`cargo-geiger`, timeouts, gate inconsistencies, branch drift). Full checklists: [references/audit-rubric.md](references/audit-rubric.md).

---

## Output Format & Pipeline Integration

Every audit emits two mandatory sections in order: numbered **1) Findings (P0/P1/P2/P3)** with Evidence/Comment/Recommendation/Owner, and **2) Before-Merge TODO** checkboxes referencing finding IDs (plus optional Executive Summary, Coverage Matrix, QA Plan). For `vc-followup`, subagent bootstrap, and `jq` JSON pipelines, see [references/cli-and-artifacts.md](references/cli-and-artifacts.md) and [references/audit-rubric.md](references/audit-rubric.md).

---

## Anti-Patterns

Never default to `--quick`, read `full.patch` blindly on large PRs, ignore `report.json`/`MERGE_GATE.json`, omit `--update` after amend/force-push, stop early when more findings exist, emit findings without evidence, merge distinct problems, skip pattern scans, or ignore tooling failures. Full list: [references/audit-rubric.md](references/audit-rubric.md).

---

_Created by Vetcoders (c)2026_
