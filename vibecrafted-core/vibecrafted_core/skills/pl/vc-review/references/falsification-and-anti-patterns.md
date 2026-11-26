# vc-review — Reguły falsyfikacji, skale ocen i antywzorce

## Domyślna postawa: falsyfikacja

Domyślny verdict dla każdego twierdzenia ze speca, jakie czyni diff, to
**UNVERIFIED**. Opisy PR-ów, komunikaty commitów, markery „fixes #123" i
wcześniejsze raporty agentów to _twierdzenia_, nie dowody. `vc-review`
konwertuje te twierdzenia na dowody, inspekcjonując kod + testy.

### Twarde reguły braku zaufania

NIE WOLNO ci ufać punktom z opisu PR-a, komunikatom commitów nazywającym
fix, inline'owym komentarzom `// done` / `# implemented`, wcześniejszym
raportom `vc-followup` lub `vc-review`, statusowi we frontmatterze
podlinkowanych plików tasków, slice'om AICX / dziennika projektu / pamięci ani
adnotacjom „fixes #123" / „closes #456" — chyba że są **niezależnie
potwierdzone w bieżącym kodzie/testach**.

### Taksonomia dowodów

Każdy finding niesie jawny stopień dowodu:

| Stopień | Kryteria                                                                                            |
| ------- | --------------------------------------------------------------------------------------------------- |
| STRONG  | Kod w diffie + test asertujący dokładne zachowanie + negatywne sprawdzenie (stara ścieżka usunięta) |
| MEDIUM  | Kod w diffie + słaby/ogólny test, lub wymuszony przez system typów                                  |
| WEAK    | Tylko kod w diffie, bez testu, bez negatywnego sprawdzenia                                          |
| NONE    | Brak bezpośredniego dowodu — finding otagowany `[VERIFY]`, severity ograniczone do P3               |

Rekomendacja „ready to merge" jest ważna tylko wtedy, gdy każdy kandydat
na finding P0/P1 dostał ocenę STRONG lub MEDIUM. WEAK na kandydacie P0
oznacza, że samo review jest UNVERIFIED na tej osi.

### Werdykty świadome etapu

Większość PR-ów jest mid-stage. PR lądujący Etap 1 z 3 NIE może być
oznaczony jako P1-blocking dlatego, że Etap 2 jest w kolejce. Otaguj każdy
finding jawnie:

- `[STAGE-OK-DEFERRED]` — luka jest jawnie poza zakresem tego PR-a
- `[STAGE-PARTIAL]` — wylądowany etap ma realną lukę wewnątrz swojego scope
- `[STAGE-DRIFT]` — PR miesza odroczony i wylądowany scope, nie mówiąc o tym

Tagi etapu jadą obok poziomu P: `[P2][STAGE-OK-DEFERRED]` to nota
higieniczna, nie blokada merge'a.

### Skala poziomów P

| Poziom P | Definicja                                                      | Przykłady                                                  |
| -------- | -------------------------------------------------------------- | ---------------------------------------------------------- |
| **P0**   | Blocker merge / security / utrata danych / czerwona bramka     | Padający tsc, wyciekłe credentiale, brak artefaktów        |
| **P1**   | Wysokie ryzyko regresji w core flow, łamanie kontraktu         | Łamiące API, duże nieprzetestowane zmiany, krytyczne cykle |
| **P2**   | Średnie: przypadki brzegowe, a11y, telemetria, częściowe testy | Brak kluczy i18n, hardcodowane URL-e, brak obsługi błędów  |
| **P3**   | Niskie ryzyko / higiena / drobny dryf                          | Puste tytuły docs, duplikacja setupu testów, nazewnictwo   |

## Antywzorce

Użycie narzędzi:

- Używanie `--quick` jako domyślnego dla review PR-a (gubi sygnał test/lint/security)
- Uruchamianie `--deep` na każdym PR-ze, gdy `--with-tests --with-lint` wystarcza
- Czytanie całego `full.patch` dla dużych PR-ów (użyj `per-file-diffs/`)
- Ignorowanie `report.json` / `MERGE_GATE.json` (najpierw parsuj ustrukturyzowane)
- Nieużywanie `--update` po amendzie/force-pushu (zduplikowane zestawy artefaktów)

Analiza:

- Zatrzymanie się na 5 findings, gdy widać 25 (findings-max = wyczerpująco)
- Findingi bez stopnia dowodu (STRONG / MEDIUM / WEAK / NONE obowiązkowe)
- Findingi bez negatywnego sprawdzenia („stara ścieżka usunięta" musi być zweryfikowane)
- Mieszanie osobnych problemów w jeden finding (jeden punkt = jeden problem)
- Pomijanie skanów wzorców (`.unwrap()` / `any` / checklista PII obowiązkowe)
- Pomijanie przebiegu adwersaryjnego (Faza 2.5 jest obowiązkowa)
- Pomijanie autoataku na verdictach STRONG
- Modyfikowanie kodu podczas review (READ-ONLY — fixy należą do marbles)
- Ufanie opisowi PR-a / commitom / `// done` bez weryfikacji w kodzie
- Rekomendowanie „merge", gdy `model_confidence` ≠ `high`
- Traktowanie PR-ów mid-stage jako fully-staged (użyj `[STAGE-OK-DEFERRED]`)
