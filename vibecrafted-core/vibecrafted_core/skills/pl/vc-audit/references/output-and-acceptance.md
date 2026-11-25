# vc-audit — Kontrakt wyjścia, antywzorce i kryteria akceptacji

## Kontrakt wyjścia

`vc-audit` produkuje dokładnie trzy pliki w katalogu raportu:

1. **`audit_report.md`** — najpierw executive verdict, tabela per-task,
   self-attack pass, model check
2. **`audit_requirements_matrix.jsonl`** — jeden rekord JSON na
   wymaganie: verdict, stopień evidence, lokalizacje w kodzie, evidence
   z testów, wynik negative check
3. **`audit_trace.log`** — zwarty trace per-faza (`BEGIN`,
   `READ_CONTEXT_PACK`, `READ_TASK`, `EXTRACT_REQUIREMENTS`,
   `INSPECT_CODE`, `VERIFY_TESTS`, `NEGATIVE_CHECK`, `DEPENDENCY_CHECK`,
   `STAGE_CHECK`, `CLASSIFY`, `SELF_ATTACK`, `WRITE_REPORT`, `END`)

Executive verdict MUSI zawierać liczby tasków per verdict, liczby
P0/P1/P2/P3, top 5 ryzyk, kolejne 5 akcji oraz `model_confidence: high |
medium | low`.

Szablon operator dispatch żyje w [`DISPATCH.md`](DISPATCH.md).

## Antywzorce

W trybie auditu nie:

- naprawiaj kodu podczas auditu („tylko mały refactor przy okazji")
- oznaczaj PASS na podstawie commit messages, frontmattera czy wcześniejszych raportów
- zwijaj wszystkich tasków w ogólne podsumowanie
- pomijaj negative check („nowy kod jest, to wystarczy")
- pomijaj adversarial pass ani self-attack
- traktuj wylądowanego Stage 1 jako PASS całego planu
- traktuj odroczonego Stage 2 jako FAIL całego planu
- produkuj samego raportu bez matrycy + trace
- ufaj AICX / kronice / memory slices jako prawdzie repo
- omijaj Loctree przy pytaniach o graf importerów / zasięg zmiany / martwy kod
- broń swojego pierwszego verdictu podczas self-attacku zamiast go obniżyć

## Kryteria akceptacji

Przebieg auditu jest **gotowy**, gdy:

- [ ] Każdy plik taska / planu ma `task_read_status: FULL_READ`
- [ ] Każde wymaganie ma stopień evidence + verdict
- [ ] Każde wymaganie ma wyniki positive + negative check
- [ ] Self-attack wykonany na każdym PASS / PASS_WITH_GAPS
- [ ] Model check wyemitowany z oceną confidence
- [ ] Wszystkie trzy pliki wyjściowe zapisane
- [ ] `git diff` pusty dla ścieżek poza raportem (kod nietknięty)
- [ ] Executive verdict odwołuje się do konkretnego kolejnego ruchu
