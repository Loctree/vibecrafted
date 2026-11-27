# `vc-canary` — Skrypty pomocnicze, zależności i częste błędy

## Skrypty pomocnicze

```bash
CLI="uv run --python 3.12 …/vc-canary/scripts/canary_cli.py"

$CLI snapshot-path --root .
$CLI repo-view --root .
$CLI atlas --root . --refresh
$CLI coverage --root .
```

Wszystkie zapisy idą pod `./.loctree/` (atlas + canary). Status na stdout;
dane w plikach.

## Zależności

| Skill / narzędzie           | Po co                                |
| --------------------------- | ------------------------------------ |
| `loct` / loctree            | snapshot, organy, prism, occurrences |
| `vc-loctree`                | doktryna strukturalna                |
| `vc-dispatch` await-arming  | budzenie floty, nie pliki logów      |
| `vc-delegate` / `vc-agents` | hybryda natywni vs zewnętrzni        |

## Częste błędy

- Traktowanie każdej wielowładzy jako defektu (`INTENTIONAL_VARIANT`
  z udowodnioną granicą to zdrowa odpowiedź)
- Proponowanie refaktorów albo tronów wewnątrz przebiegu canary
- Twierdzenie o nieobecności z wyszukiwania semantycznego bez literal
  coverage
- Raport na nieświeżym snapshocie albo ignorowanie stanu dirty/worktree
- Nadpisywanie journala zamiast dopisywania
- Używanie `loct-context-full.json` jako inwentarza plików
- Stała liczba agentów zamiast osi z Phase I
- Liczenie definicji zamiast referencji (cenzus definicji ukrył kiedyś
  141 miejsc wywołań)
- Rekonstruowanie albo interpolowanie brakujących historycznych punktów
  kontrolnych zamiast zapisania `MISSING`
- Dispatch wycofanego briefu docstring-WRITE katalogera — canary nie
  mutuje kodu (kontrakt wycofany 2026-08-24)
