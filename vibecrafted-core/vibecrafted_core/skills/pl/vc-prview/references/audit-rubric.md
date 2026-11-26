# vc-prview — Kolejność czytania, skany wzorców, format wyjścia i antywzorce

## Kolejność czytania (Obowiązkowy)

Czytaj artefakty w tej kolejności. Dla każdego: co wyciągnąć.

### 1) `AI_INDEX.md` (jeśli istnieje)

- Zweryfikuj, czy wskazuje na prawdziwe ścieżki. Kłamliwy indeks → finding P3 [TOOLING].

### 2) `report.json` (domyślne źródło prawdy)

- `meta`: PR url, branch, base
- `gate`: allow_merge + policy_mode + reasons
- `checks[]`: status (PASS/WARN/FAIL/ERROR), log_path, command
- `diff.stats` + `diff.files[]`: skala, churn, hotspoty, patch_path
- `quality`: breaking / coverage / sarif / heuristics

### 3) `00_summary/MERGE_GATE.json` + `SANITY.json`

- Sprawdź krzyżowo z `report.json`. Niespójność → finding P2 [TOOLING].
- Uwaga: "All checks passed" przy obecnym WARN/INLINE_FINDINGS = mylące.

### 4) `00_summary/pr-metadata.txt` + `file-status.txt` + `commit-list.txt`

- Scope: ile plików, jakie kategorie (A/M/D), progresja commitów
- Wypatruj dryfu gałęzi (pliki infra spoza scope'u PR-a)

### 5) `30_context/INLINE_FINDINGS.sarif`

- Każdy wynik SARIF = gotowy finding. Przenieś wszystkie na listę findingów.

### 6) `20_quality/*` (logi + wyniki)

- Bramki PASS: wyciągnij warningi z logów (cargo warns, tsc non-errors)
- Bramki WARN/ERROR/FAIL: przyczyna źródłowa + rekomendacja
- `checks-errors.log`: przefiltrowane błędy o wysokim sygnale
- `BREAKING_CHANGES.md`: oceń realną wagę (P?)
- `coverage-delta.txt`: oflaguj krytyczne wpisy "NO_TEST_CHANGE"

### 7) `30_context/changed-tests.txt`

- Skonfrontuj ze zmianami w źródłach — nieprzetestowane pliki źródłowe → finding

### 8) Diffy (selektywnie, nie wyczerpująco)

- `10_diff/per-file-diffs/00-INDEX.txt` → pliki o największym churnie
- Patche per plik dla hotspotów
- `10_diff/per-commit-diffs/00-SUMMARY.md` → commity o największym wpływie
- Batche per commit do analizy na poziomie linii

---

## Obowiązkowe skany wzorców

W patchach per plik i/lub w `full.patch` przeskanuj te wzorce:

### Rust

- `.unwrap()`, `.expect(` — nieobsłużone paniki
- `panic!`, `todo!` — niekompletny kod
- `unsafe` — sprawdź uzasadnienie
- `dbg!`, `println!` — pozostałości po debugu
- `#[allow(` — wyciszone warningi

### TypeScript / JavaScript

- `any` — ucieczka od typów
- `as unknown as` — podwójny cast (pranie typów)
- `@ts-ignore`, `@ts-expect-error` — wyciszanie typów
- `eslint-disable` — wyciszanie linta
- `// TODO`, `// FIXME`, `// HACK` — odłożona robota
- Puste `catch {}` lub `catch (e) {}` bez logu/rethrow
- Asercja non-null `!` na niepewnych wartościach
- `console.log`, `console.warn`, `console.error` — powinno używać secureLogger (example-app)

### Security / PII

- Logowanie tokenów, e-maili, haseł, ID osobowych
- Nowe zdarzenia telemetrii bez privacy review
- Nowe endpointy / handlery komend bez sprawdzeń auth
- Hardkodowane URL-e, klucze API, sekrety

### Dane / Wydajność

- Query w pętli (N+1)
- Brak batchowania operacji masowych
- Duże payloady bez paginacji
- Niepotrzebne I/O na gorących ścieżkach

Każde "trafienie" w diffie = potencjalny finding z evidence.

---

## Minimalne wymagania pokrycia

Żeby zapobiec lakonicznym raportom:

- **Wszystkie** wpisy w `INLINE_FINDINGS.sarif`
- **Top 10** plików wg churnu (z `report.json` lub `file-status.txt`) — przeczytaj patch per plik
- **Wszystkie** pliki w kluczowych kategoriach ryzyka (po ścieżce): auth, payments, database, session, security, encryption, middleware
- **Wszystkie** krytyczne wpisy "NO_TEST_CHANGE" z `coverage-delta.txt`
- **Wszystkie** wpisy w `BREAKING_CHANGES.md` z ocenionym poziomem P
- **Progresja per commit** dla PR-ów z >5 commitami — zidentyfikuj fazy, ryzykowne przejścia

---

## Przypadki specjalne (Tooling)

### Panika Cargo Geiger

`Matching variant not found` = tooling/misconfig (case-sensitive `--output-format`).
→ Finding **P1 [TOOLING]**, jeśli blokuje sygnał jakości. Rekomendacja: napraw flagę albo przypnij/zaktualizuj.

### Timeouty / "killed"

`killed (>timeout)` dla tsc trace / eslint json:
→ Finding **P2 [TOOLING]** (brakujący sygnał jakości). Rekomendacja: zwiększ timeout albo wyłącz z uzasadnieniem.

### Niespójności bramki

`MERGE_GATE.json` mówi "All checks passed", ale istnieją WARN/findingi:
→ Finding **P2 [TOOLING]** z rekomendacją: "All blocking checks passed" vs "Non-blocking issues present".

### Dryf gałęzi

Pliki zmienione poza scope'em PR-a (CI, infra, niezwiązany config):
→ Finding **P1**, jeśli >10 plików. Rekomendacja: rebase na gałąź bazową.

---

## Format wyjścia (Obowiązkowy)

Finalne wyjście ZAWSZE ma te 2 obowiązkowe sekcje (w tej kolejności):

### 1) Findingi (P0/P1/P2/P3)

Każdy finding w tym formacie:

```
- **[P?] <Title>** (opcjonalnie: [VERIFY] lub [TOOLING])
  - **Evidence:** `<artifact-path>` + `<file:line>` + krótki fragment (1-2 linie)
  - **Komentarz:** 1 zdanie o ryzyku/wpływie
  - **Rekomendacja:** konkretne "co zrobić" / "jak zweryfikować"
  - **Owner:** `author` / `reviewer` / `infra` (opcjonalnie)
```

Numeruj findingi do odsyłaczy krzyżowych: P1-01, P1-02, P2-01 itd.

### 2) TODO przed mergem (markdownowe checkboxy)

```markdown
- [ ] **(P0)** ... (ref: P0-01)
- [ ] **(P1)** ... (ref: P1-01, P1-02)
- [ ] **(P2)** ... (ref: P2-01)
- [ ] **(P3)** ... (ref: P3-01)
```

Każde TODO odsyła do ID findingów. Dołączaj komendy weryfikacyjne w code fence'ach tam, gdzie to zasadne.

### 3) Sekcje opcjonalne (zalecane)

Dodaj, gdy wnoszą wartość:

- **Executive Summary** (max 8 punktów): verdict bramki, top 3 ryzyka, sygnał testów, najważniejsze hotspoty, delta scope'u
- **Architecture Context**: diagram lub opis dotkniętego podsystemu
- **Scope / Co się zmieniło**: na bazie `diff.stats` + topowe katalogi + topowe pliki
- **Progresja commitów**: fazy pracy dla PR-ów wielocommitowych
- **Macierz pokrycia testami**: plik źródłowy → plik testowy → liczba nowych testów
- **Security & Privacy Check**: PII w logach, przepływy danych, filtrowanie zdarzeń
- **QA Plan**: 5-15 rekomendacji testów manualnych + automatycznych
- **Evidence Index**: linki do kluczowych użytych artefaktów

---

## Antywzorce

### Użycie narzędzia

- Używanie `--quick` jako domyślnego do review PR-a w tym skillu (gubi sygnał test/lint/security)
- Odpalanie `--deep` na każdym PR-ze, gdy `--with-tests --with-lint` wystarcza (zostaw `--deep` na merge gate / PR-y wysokiego ryzyka)
- Czytanie całego `full.patch` przy dużych PR-ach (użyj `per-file-diffs/` do skupionego review)
- Ignorowanie `report.json` i `MERGE_GATE.json` (najpierw parsuj dane ustrukturyzowane)
- Niekorzystanie z `--update` po amendzie/force-pushu (generuje zduplikowane zestawy artefaktów)
- Uruchamianie bez `--no-fetch` na wolnych sieciach

### Analiza

- Zatrzymywanie się na 5 findingach, gdy widać 25 (findings-max znaczy wyczerpująco)
- Findingi bez evidence (każdy punkt potrzebuje ścieżki artefaktu + fragmentu kodu)
- Mieszanie osobnych problemów w jeden finding (jeden punkt = jeden problem)
- Ignorowanie problemów narzędziowych (crash narzędzia ≠ problem kodu, ale wciąż finding)
- Pomijanie skanów wzorców (checklista `.unwrap()` / `any` / PII jest obowiązkowa)
- Brak skonfrontowania coverage-delta ze zmienionymi plikami źródłowymi
