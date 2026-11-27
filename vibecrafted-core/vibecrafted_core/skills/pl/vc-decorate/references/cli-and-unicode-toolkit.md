# vc-decorate — Referencja powierzchni CLI i zestawu Unicode

## CLI to też interfejs

Terminal to nie wysypisko. Wyjście CLI to UI. Zasługuje na tę samą spójność, rytm i celowość co strona internetowa.
Paskudne, surowe, niesformatowane wyjście terminala nie jest „przyjazne dla developera" — jest obraźliwe dla operatora.

Decorate stosuje się również do powierzchni CLI. Jeśli produkt ma interfejs terminalowy, ten interfejs jest częścią
powierzchni produktu. Zrób na nim decorate. Oczywiste obszary to:

- wyjście instalatora (wyrównanie, kolory, sygnały postępu)
- główny runtime (z brandingiem, zwięzły, informatywny)
- po wykonaniu (spinnery, paski postępu, podsumowania per krok)
- wyjścia help/--help (uporządkowane sekcje, kolory, kolumny)
- doctor/health checks (czytelne podsumowania pass/fail, czytelne minimalne logi)
- komunikaty błędów (rozdzielenie wersji dla maszyny i dla człowieka)

Jeśli dostępny jest `screenscribe`, vc-decorate może skonsumować narrację z nagrania ekranu UI (screencast), aby wykryć
dryf, niezgrabne przejścia i przerwy w spójności w obrębie rzeczywistego flow — przydatne, gdy statyczne zrzuty ekranu
są zbyt ubogie.

### Zestaw narzędzi Unicode dla CLI

𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. dostarcza bazę danych Unicode (2601 znaków, 13 kategorii) oraz serwer
`unicode-puzzles-mcp`. Używaj ich do dekoracji CLI zamiast zgadywać code pointy czy
hardkodować sekwencje ucieczki ANSI.

**Pipeline: czysty tekst → transformacja unicode → decorate_text**

1. Najpierw napisz treść jako czysty tekst
2. Przekształć etykiety/tytuły przez `rewrite_using_unicode` (wybierz styl)
3. Owiń finalny układ w `decorate_text` dla box artu (jeśli potrzeba)

Nigdy nie dobieraj code pointów z pamięci. Używaj MCP — zwraca zweryfikowane,
spójne znaki z tego samego bloku Unicode.

**Dostępne style** (`rewrite_using_unicode`):

| Styl           | Wygląd   | Najlepsze do                            |
| -------------- | -------- | --------------------------------------- |
| `squared`      | 🄵🅁🄰🄼🄴    | Stemple brandingowe, plakietki w stopce |
| `vaporwave`    | Ｖｉｂｅ | Rozstrzelone nagłówki                   |
| `monospace`    | 𝚟𝚒𝚋𝚎     | Podnagłówki CLI, ciągi wersji           |
| `smallCaps`    | Vɪʙᴇ     | Wyróżnienie inline                      |
| `fraktur`      | 𝔙𝔦𝔟𝔢     | Ozdobne tytuły sekcji                   |
| `doubleStruck` | 𝕍𝕚𝕓𝕖     | Etykiety matematyczne / formalne        |
| `bubble`       | Ⓥⓘⓑⓔ     | Plakietki statusu, tagi                 |

**Elementy dekoracji CLI** (baza Unicode):

| Potrzeba    | Znaki                | Źródło                   |
| ----------- | -------------------- | ------------------------ |
| Ramki       | `╭─╮│╰─╯`            | Box Drawing              |
| Separatory  | `·` `─` `━` `┄`      | Box Drawing, Punctuation |
| Znaczniki   | `✓` `✗` `⚠`          | Dingbats                 |
| Punktory    | `▸` `▪` `◆` `›`      | Geometric Shapes         |
| Postęp      | `⣿⣶⣤⣀` `█▓▒░`        | Braille, Block Elements  |
| Sparkline'y | `⣀⣤⣶⣿` (8px/komórkę) | Braille (256 kombinacji) |
| Strzałki    | `→` `←` `↑` `↓` `⟶`  | Arrows                   |
| Status      | `⚒` `⚡` `⚙` `⟳`     | Misc Symbols             |
| Marki       | `🄵·🅁·🄰·🄼·🄴·🅆·🄾·🅁·🄺`  | Enclosed Alphanumerics   |

**Sparkline'y Braille'a** zasługują na uwagę. Pojedynczy znak Braille'a koduje 8 kropek
w siatce 2×4 (256 kombinacji) — 40 znaków = krzywa zbieżności o 320 punktach w terminalu,
bez biblioteki graficznej. Używaj do: zużycia tokenów w czasie · findingów P0/P1/P2
w pętlach marbles · osi czasu aktywności agentów · dowolnych danych trendowych.

**Zasady:**

- Zero kodów ucieczki ANSI do stylowania tekstu — czysty unicode renderuje się wszędzie.
- Kolory ANSI (`\033[32m` itd.) dopuszczalne wyłącznie do kolorowania statusu.
- Nigdy nie mieszaj bloków Unicode w obrębie jednej etykiety (kwadratowe F obok negatywowego kwadratowego R
  wygląda jak bug, nie jak wybór — chyba że to celowy znak firmowy w stylu
  `🅵·🅁·🄰·🄼·🄴·🅆·🄾·🅁·🄺`).
- Testuj renderowanie na co najmniej dwóch terminalach (macOS Terminal + domyślny terminal Linuksa).
- Użyj `search_unicode`, aby znaleźć konkretny symbol — nie zgaduj.
