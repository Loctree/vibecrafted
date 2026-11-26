# `vc-ship` — Antywzorce

## Antywzorce

- Odpalanie bez pliku misji osadzonego w prawdzie z vc-init (prompt jest
  hipotezą, nie ground truth).
- Pilnowanie bramek albo workerów z wnętrza subagenta — awaria klasy gate-nap
  (`docs/runtime/AGENT_OPS.md`, klasa 1); watchery mieszkają przy nadzorcy.
- Ufanie ciszy: brakujący raport jest nie do odróżnienia od martwego workera,
  dopóki nie sprawdzisz żywotności (klasa 2) — użyj `status`/`stage_worker`, nie
  wysiaduj budżetów przy zwłokach.
- Ręczne edycje `state.json` zamiast czasowników — ślad JEST produktem.
- Zatwierdzanie etapu bez przeczytania jego raportu albo samodzielne ogłaszanie
  „gotowe" zamiast oddania werdyktu bramce.
