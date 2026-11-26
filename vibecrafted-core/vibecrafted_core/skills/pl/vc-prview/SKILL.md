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

# vc-prview — Ograniczony pipeline review (generowanie + audyt)

Skill dwufazowy: **Faza 1** generuje ustrukturyzowane artefakty przez prview-rs,
**Faza 2** wyciska z nich maksimum findingów. Wyjście: findingi z poziomami P
i z evidence + checklista TODO przed mergem.

## Canonical Orientation Gate

Zanim użyjesz artefaktów prview jako prawdy o release'ie lub mergu, uruchom lub
skonsumuj procedurę `vc-init` dla przydzielonego repo. `Loctree:loctree` to
domyślny skill do mapowania struktury repo dla tego przebiegu i musi wyprodukować lub
odświeżyć Mapę Aplikacji Wyprowadzoną z Kodu (Code-Derived Application Map).

Jeśli brakuje świeżego evidence z `vc-init`, najpierw wykonaj przebieg init i
traktuj wnioski z review jako zablokowane, dopóki nie ma aktualnej prawdy repo.

Użyj Loctree do zidentyfikowania plików nośnych i zasięgu zmiany; użyj prview do
zaudytowania żądanego diffa lub artifact packa względem tej aktualnej struktury.

Binarka: `prview` (zainstalowana w `~/.cargo/bin/prview`)
Źródło: `https://github.com/LibraxisAI/prview-rs`
Autor: Vetcoders

---

## Doktryna pracy z repozytorium

W pracy z repozytorium zacznij od Loctree jako mapy: użyj `loct context`,
`loct occurrences`, `loct body` i `loct find --literal` przed szerokim ręcznym
przeszukiwaniem. Używaj AICX do kontekstu intencji i sesji. Używaj rg/grep jako
fallbacku lub lokalnej lupy, nie jako zamiennika mapowania strukturalnego. Jeśli
Loctree zawiedzie lub przeoczy jakąś powierzchnię, dopisz feedback do
`~/.vibecrafted/loctree/loctree-fail.md`.

## Faza 1 — Generowanie artefaktów

Generuj ustrukturyzowane paczki review dla lokalnych gałęzi (`prview --pr <NUMBER>`), zdalnych gałęzi (`prview -R --remote-only <branch> <base>`), PR-ów z GitHuba (`prview --pr <NUMBER> --with-tests --with-lint`) lub pełnych bramek (`prview --deep`). **Domyślnie nie używaj `--quick` do review PR-a** (ani szybkich aliasów `prv`, `prvpr`, `prvjson` dla wyjścia o jakości review).

Inne tryby (`--ci`, `--json --quiet`, `--update`, `--tui`), pełna tabela 23 flag, auto-wykrywane profile (`rust`/`js`/`python`/`mixed`/`generic`) i `.prview-policy.yml` (`shadow`/`warn`/`block`) znajdują się w [references/cli-and-artifacts.md](references/cli-and-artifacts.md).

---

## Układ artifact packa

Wyjście ląduje w `.tools/pr-artifacts/<branch>/<timestamp>/` (symlink `latest`); zawsze wybieraj **najnowszy** `<timestamp>` (pusty lub brakujący katalog → **P0**). Parsuj `report.json`, `00_summary/MERGE_GATE.json`, `SANITY.json`, `20_quality/*`, `30_context/INLINE_FINDINGS.sarif` i `10_diff/per-file-diffs/`. Pełne drzewo i bootstrap pipeline'u: [references/cli-and-artifacts.md](references/cli-and-artifacts.md).

---

## Faza 2 — Analiza artefaktów (Findings-Max)

### Filozofia

Tryb: **Findings-max**. Nie kończ na "kilku punktach". Jeśli widać 25 osobnych
problemów, wypisz 25. Lepiej 20 celnych findingów niż 5 ogólników.

Każdy finding MUSI mieć **Dowód** (artefakt + ścieżka + 1–2 linie), **Komentarz** (dlaczego ważne + co grozi) oraz **Rekomendację** (co zrobić / jak zweryfikować). Nie łącz różnych tematów w 1 punkt; niepotwierdzone oznacz **[VERIFY]** i rozdziel błędy kodu od **[TOOLING]**.

### Skala poziomów P

| P-level | Definicja                                                          | Przykłady                                                              |
| ------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| **P0**  | Blocker merge / security / data loss / failing blocking check      | Failing tsc, leaked credentials, missing artifacts                     |
| **P1**  | Wysoki risk regresji w core flow, niekompatybilne zmiany kontraktu | Breaking API, duże zmiany bez testów, import cycles in critical module |
| **P2**  | Średni risk: edge-cases, a11y, telemetria, częściowy brak testów   | Missing i18n keys, hardcoded URLs, no error handling on external call  |
| **P3**  | Niskie ryzyko / higiena / drobne niespójności                      | Empty doc titles, test setup duplication, cosmetic naming              |

---

## Kolejność czytania, skany wzorców i pokrycie

Stosuj obowiązkową 8-krokową kolejność czytania (`AI_INDEX.md` → `report.json` → `MERGE_GATE.json`/`SANITY.json` → metadane/status/commity → `INLINE_FINDINGS.sarif` → `20_quality/*` → `changed-tests.txt` → selektywne `per-file-diffs/`). Skanuj patche pod kątem Rust, TS/JS, Security/PII i Dane/Wydajność; pokryj wszystkie wpisy SARIF, top 10 churnu, ścieżki ryzyka, `NO_TEST_CHANGE`, `BREAKING_CHANGES.md` i przypadki specjalne toolingu (`cargo-geiger`, timeouty, niespójności bramki, dryf gałęzi). Pełne checklisty: [references/audit-rubric.md](references/audit-rubric.md).

---

## Format wyjścia i integracja z pipelinem

Każdy audyt zwraca dwie obowiązkowe sekcje w kolejności: numerowane **1) Findingi (P0/P1/P2/P3)** z Evidence/Komentarzem/Rekomendacją/Ownerem oraz **2) TODO przed mergem** (checkboxy z ID findingów; opcjonalnie Executive Summary, Macierz pokrycia, QA Plan). Integracja z `vc-followup`, bootstrap subagenta i pipeline `jq`: [references/cli-and-artifacts.md](references/cli-and-artifacts.md) oraz [references/audit-rubric.md](references/audit-rubric.md).

---

## Antywzorce

Nie używaj `--quick` jako domyślnego, nie czytaj ślepo całego `full.patch` na dużych PR-ach, nie ignoruj `report.json`/`MERGE_GATE.json`, nie pomijaj `--update` po amend/force-push, nie przerywaj na 5 findingach, nie pisz findingów bez dowodów, nie mieszaj osobnych problemów, nie pomijaj skanów wzorców ani błędów toolingu. Pełna lista: [references/audit-rubric.md](references/audit-rubric.md).

---

_Created by Vetcoders (c)2026_
