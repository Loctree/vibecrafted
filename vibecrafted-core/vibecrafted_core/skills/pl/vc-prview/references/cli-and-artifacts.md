# vc-prview — Tryby CLI, flagi, układ paczki artefaktów i polityki

## Faza 1 — Generowanie artefaktów (pełne CLI i tryby)

### Najczęstszy przypadek: review lokalnej gałęzi

```bash
prview --pr <NUMBER>
```

Analizuje HEAD bieżącej gałęzi vs develop/main. Szybkie (<20s). Najlepsze do codziennej pracy.

### Zdalna gałąź (bez checkoutu)

```bash
prview -R --remote-only <branch> <base>
```

- `<branch>`: nazwa bez `origin/` (np. `feat/x`)
- `<base>`: domyślnie `develop`

Ścieżki fallbackowe:

- `~/Git/prview-rs/target/release/prview -R --remote-only <branch> <base>`
- `prview --use-bash-full -R --remote-only <branch> <base>` (mostek kompatybilności)

### PR z GitHuba po numerze

```bash
prview --pr <NUMBER> --with-tests --with-lint
```

Dodaj `--gh-repo owner/repo`, jeśli origin jest niejednoznaczny.

Domyślnie dla tego skilla: **nie używaj `--quick` do review PR-a**.
Używaj `--quick` tylko do jawnego szybkiego triage'u, odświeżenia artefaktów pod
presją czasu albo gdy ciężkie bramki są niemożliwe w bieżącym środowisku.

### Deep review (wszystkie bramki)

```bash
prview --deep
# albo selektywnie:
prview --with-tests --with-lint --with-security
```

### Inne tryby

| Komenda                      | Cel                                                             |
| ---------------------------- | --------------------------------------------------------------- |
| `prview --ci`                | Tryb CI: wszystkie sprawdzenia, bez koloru, exit 1 przy porażce |
| `prview --json --quiet`      | Wyjście JSON do automatyzacji / pipowania przez jq              |
| `prview --update`            | Inkrementalnie: regeneruj tylko zmienione artefakty             |
| `prview --tui`               | Interaktywny terminalowy UI                                     |
| `prview feat/x develop main` | Jawny target + gałęzie bazowe                                   |

### Referencja flag

| Flaga                  | Co                                                 |
| ---------------------- | -------------------------------------------------- |
| `--quick`              | Pomiń testy/lint/bundle/heurystyki; tylko triage   |
| `--deep`               | Wszystkie sprawdzenia włączone                     |
| `--ci`                 | Tryb CI (ścisły exit)                              |
| `--pr N`               | Analizuj PR #N z GitHuba                           |
| `--gh-repo owner/repo` | Jawne repo dla --pr                                |
| `--with-tests`         | Włącz runner testów                                |
| `--with-lint`          | Włącz lintery                                      |
| `--with-security`      | Włącz cargo geiger                                 |
| `--update`             | Inkrementalna regeneracja                          |
| `--json`               | Wyjście JSON                                       |
| `-q, --quiet`          | Minimalne wyjście                                  |
| `--tui`                | Interaktywny TUI                                   |
| `--watch`              | Monitoruj + regeneruj przy zmianach                |
| `-R, --remote`         | Zdalna gałąź, bez checkoutu                        |
| `--no-fetch`           | Pomiń git fetch                                    |
| `--no-cache`           | Wyłącz cache'owanie sprawdzeń                      |
| `--no-zip`             | Pomiń tworzenie ZIP-a                              |
| `--soft-exit`          | Zawsze exit 0                                      |
| `--profile <P>`        | Wymuś profil języka (rust/js/python/mixed/generic) |
| `--policy-mode <M>`    | Nadpisz politykę (shadow/warn/block)               |
| `--breaking-change`    | Oznacz PR jako breaking                            |
| `-v, --verbose`        | Wyjście verbose                                    |

Istnieją aliasy shellowe (`prv`, `prvpr`, `prvjson`), ale ten skill nie powinien
używać szybkich aliasów do wyjścia o jakości review.

---

## Układ artifact packa

Wyjście: `.tools/pr-artifacts/<branch>/<timestamp>/`
Symlink: `.tools/pr-artifacts/<branch>/latest`

Zawsze wybieraj **najnowszy** `<timestamp>`. Pusty lub brakujący katalog → **P0**.

```
.tools/pr-artifacts/<branch>/<timestamp>/
├── dashboard.html                # Interactive HTML report
├── AI_INDEX.md                   # Artifact map + suggested reading order
├── report.json                   # Canonical structured report (PARSE FIRST)
├── 00_summary/
│   ├── MERGE_GATE.json           # Machine-readable merge decision
│   ├── MERGE_GATE.md             # Human-readable merge decision
│   ├── RUN.json                  # Run metadata (timing, config, version)
│   ├── MANIFEST.json             # SHA256 hashes of all generated files
│   ├── SANITY.json               # Post-generation integrity checks
│   ├── pr-metadata.txt           # Branch/base/profile metadata
│   ├── file-status.txt           # A/M/D + file paths
│   └── commit-list.txt           # hash date author message
├── 10_diff/
│   ├── full.patch                # Full diff with diff-stat header
│   ├── per-commit-diffs/         # Batched commit patches + 00-SUMMARY.md
│   └── per-file-diffs/           # Hotspot files (>80 lines changed) + 00-INDEX.txt
├── 20_quality/
│   ├── <gate>.result.json        # Per-gate result + provenance
│   ├── <gate>.log                # Per-gate raw output
│   ├── full-checks.log           # All check output concatenated
│   ├── checks-errors.log         # Filtered: errors/warnings only (±2 context)
│   ├── coverage-delta.txt        # Source↔test mapping with change status
│   └── BREAKING_CHANGES.md       # Removed pub symbols, changed signatures
├── 30_context/
│   ├── INLINE_FINDINGS.sarif     # Machine-readable SARIF findings
│   ├── changed-tests.txt         # Test files modified in this PR
│   └── <tooling>.txt             # cargo-tree, tsc-trace, etc.
└── artifacts.zip                 # Everything zipped
```

Uwaga: niektóre przebiegi mają duplikaty w podkatalogu `artifacts/` — preferuj
pliki w roocie.

---

## System polityk

Utwórz `.prview-policy.yml` w roocie repo:

```yaml
version: 1
mode: warn # shadow | warn | block
default_severity: warn
checks:
  cargo_audit: block
  vitest: warn
  eslint: ignore
```

Nadpisanie w CLI: `--policy-mode block`

Tryby:

- **shadow**: nigdy nie blokuje (tylko obserwowalność)
- **warn**: blokuje tylko przy porażkach o severity `block`
- **block**: blokuje przy porażkach o severity `block` ORAZ `warn`

---

## Profile

Auto-wykrywane z zawartości repo. Nadpisanie: `--profile <PROFILE>`.

| Profil  | Wykrywanie                    | Sprawdzenia                                   |
| ------- | ----------------------------- | --------------------------------------------- |
| rust    | Cargo.toml                    | cargo test, clippy, cargo audit, cargo geiger |
| js      | package.json + pliki źródłowe | vitest, eslint, tsc, pnpm build               |
| python  | pyproject.toml                | pytest, ruff, mypy                            |
| mixed   | wykryto kilka                 | wszystkie pasujące                            |
| generic | fallback                      | podstawowa analiza plików                     |

---

## Vibecrafted. Integracja z pipelinem

### Jako wejście do vc-followup

```bash
prview --pr $PR_NUMBER --with-tests --with-lint
ARTIFACTS=".tools/pr-artifacts/<branch>/latest"
```

### Kontekst delegacji do subagenta

```
## Context Bootstrap
- prview artifacts at: .tools/pr-artifacts/<branch>/latest/
- Parse report.json first (default)
- Read 00_summary/MERGE_GATE.json for quick verdict
- Read 20_quality/checks-errors.log for error details
- Read 10_diff/per-file-diffs/ for hotspot patches
```

### Pipeline JSON

```bash
prview --json --quiet | jq '.checks[] | select(.status == "Failed")'
```
