---
name: loctree
description: Strukturalna i literalna percepcja repozytorium przed edycją, usunięciem, refaktorem lub pracą w nieznanym kodzie. Loctree mapuje zakres, zależności, konsumentów, dokładne wystąpienia i blast radius; AICX dostarcza historię intencji.
metadata:
  version: "3.1.0"
  loctree_value: "primary repo map for structural/literal repository work"
  aicx_value: "intent, session, and decision-context retrieval"
  dogfooding: "required for repo-impacting work"
---

# Loctree — obrazowanie przed operacją

Loctree daje wzrok strukturalny: kształt repo, indeksowane literalne wystąpienia,
sąsiedztwo zależności, miejsca definicji, mosty runtime i blast radius. AICX daje
historię intencji. Żadne z nich nie zastępuje źródła, manifestów, testów ani
rzeczywistej próby runtime.

## Checkpoint strukturalny

W pracy repozytoryjnej ten skill jest strukturalną połową procedury `vc-init`.
`Loctree:loctree` musi utworzyć lub odświeżyć Mapę Aplikacji Wyprowadzoną z Kodu (Code-Derived Application Map) przed implementacją, review, releasem, porządkowaniem lub usunięciem.

Jeżeli nie ma świeżego dowodu `vc-init`, najpierw wykonaj init i traktuj dalszą
pracę repozytoryjną jako zablokowaną. Jeżeli zadanie nie dotyczy repo, powiedz to
wprost zamiast udawać, że mapa istnieje.

## Dobierz narzędzie do pytania (12 MCP ↔ `loct` CLI)

| Potrzeba                                    | `loctree-mcp`                                                                                          | `loct` CLI                                                      |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------- |
| Szeroka orientacja zadania                  | `context(project, file?, task?, scope?, scope_mode?, aicx_project?, format?, section?)`                | `loct context --task "..." [--scope ... --scope-mode all\|any]` |
| Szybki obraz repo                           | `repo-view(project)`                                                                                   | `loct repo-view`                                                |
| Struktura katalogów i LOC                   | `tree(project, depth?, loc_threshold?)`                                                                | `loct tree [--files --match 'pat']`                             |
| Powiązania katalogu                         | `focus(project, directory, depth?, no_consumers?, rescan?)`                                            | `loct focus path/ [--depth N] [--no-consumers]`                 |
| Zależności i konsumenci pliku               | `slice(project, file, depth?, no_consumers?, rescan?)`                                                 | `loct slice path/file [--depth N] [--no-consumers] [--rescan]`  |
| Pełne źródło definicji / zakresu            | `body(project, symbol, file?, line_cap?, max_chars?, no_limit?, rescan?)`                              | `loct body Symbol [--max-lines N] [--max-chars N]`              |
| Dokładne wystąpienia identyfikatora         | `find(project, name, mode="literal", file?, whole_token?, no_generated?, group_by_file?, count_only?)` | `loct find Identifier`                                          |
| Definicje i re-exporty                      | `find(project, name, mode="where-symbol", file?)`                                                      | `loct find Identifier --where-symbol`                           |
| Szerokie kandydaty symboli/parametrów       | `find(project, name, mode="discover", lang?, exported_only?, similar?)`                                | `loct find --discover Terms`                                    |
| Stronicowane/zwięzłe dowody literalne       | `find(project, name, mode="literal", offset?, limit?)`                                                 | `loct occurrences Identifier --compact`                         |
| Dead/cycles/twins/hotspots/runtime flow     | `follow(project, scope, handler?, class?, limit?, offset?)`                                            | `loct follow <scope>`                                           |
| Różnice strukturalne vs Git ref             | `diff(project, since, to?, with_aicx?, aicx_project?)`                                                 | `loct diff --since HEAD~1 [--with-aicx]`                        |
| Inwentarz wyciszeń w kodzie (literal-only)  | `suppressions(project, kinds?, include_fixtures?)`                                                     | `loct suppressions`                                             |
| Smear pojęciowy (`0..15`) przed polaryzacją | `prism(project, task=["a", "b"], aicx_project?)`                                                       | `loct prism --task "a" --task "b"`                              |

Powierzchnie tylko w CLI: `loct env-truth`, `loct findings`, `loct audit`, `loct coverage`, `loct doctor`, `loct routes`, `loct hotspots`, `loct query`. Zobacz [references/commands-and-flags.md](references/commands-and-flags.md).

Zwykłe CLI `loct find` jest dokładnym wyszukiwaniem literalnym z granicami
identyfikatora; `--literal` to jawny alias. `--discover` włącza szerokie kandydaty
AST/parametr/regex/fuzzy. Kandydat discovery nie jest dowodem literalnym. Przez MCP podawaj jawnie `mode="literal"`, gdy szukasz dokładnych wystąpień (`find` ma domyślne `mode="symbols"`).

`context`, `body`, `env-truth`, `query where-symbol`, `crowd`, `focus`, `impact`,
`find` i `follow` zwracają domyślnie pełne wyniki bez cichego ucinania; limity (`--limit`, `--max-lines`, `--max-chars`, `LOCT_CONTEXT_LIKELY_TESTS_LIMIT`, `LOCT_CONTEXT_MEMORY_LIMIT`) są wyłącznie opt-in.

## Kontrakt pracy

1. Potwierdź root repo, branch/HEAD, dirty state, zakres i świeżość snapshotu (`--no-scan` / `--fail-stale` / `--fresh`).
2. Użyj `context` dla szerokiego zadania albo od razu właściwego narzędzia.
3. Przed edycją zobacz `slice`; przed delete/rename zobacz `impact`.
4. Przed stworzeniem symbolu uruchom literal find i where-symbol, a potem przeczytaj definicję przez `body`.
5. Przeczytaj dokładne źródło i wykonaj najbliższą realną bramę produktu.
6. Przed destrukcją osobno sprawdź manifesty, generated/dynamic wiring,
   reflection, entrypointy, testy oraz installed/live runtime.

## Udowodnione mocne strony

- Granice identyfikatora oddzielają `LOCT_OPEN_BROWSER` od
  `LOCT_OPEN_BROWSER_ENV` oraz `hotspot` od `hotspots`.
- Literalne wyszukiwanie może widzieć śledzone, indeksowane pliki ukryte przez
  domyślne reguły ignore, jednocześnie deklarując swój universe.
- W żywych testach AICX i Vibecrafted zwykły find zgodził się z niezależnymi
  licznikami dokładnych słów (38/38 i 22/22), a `where-symbol` zawęził wynik do
  dwóch istotnych miejsc definicji/re-exportu.
- `slice`, `impact` i `follow trace` łączą znalezioną linię z rolą systemową.
  Na Screenscribe impact pokazał 5 bezpośrednich i 12 tranzytywnych
  reprezentowanych konsumentów, a trace połączył handler frontend/backend.

To przykłady kontraktu, nie uniwersalne obietnice wydajności ani pokrycia.

## Granice dowodu

- Zero konsumentów/dead to kandydat, nigdy zgoda na usunięcie.
- Impact przechodzi tylko po krawędziach reprezentowanych w snapshot graph.
- Brak literalnego wyniku dotyczy tylko zadeklarowanego indexed universe.
- Puste karty runtime/structural wymagają audytu pokrycia.
- Ciepły cache nie mówi nic o zimnym rescanie po zmianie drzewa.
- Duże odpowiedzi MCP zrzucają pełny payload do `.loctree/mcp-response-payloads/*.full.json`; `context(format="markdown")` stronicuje całe sekcje `## ` przez `next_section` bez cięcia w środku.
- Pamięć AICX to dowód historyczny, nie aktualna prawda kodu.

Bezpośredni search tekstowy i czytanie plików pozostają poprawnym uzupełnieniem
dla prozy, lokalnego detalu, powierzchni ignored/generated i niezależnej kontroli.

Jeżeli Loctree jest błędne, stare, hałaśliwe, nieobsługiwane albo wymusza fallback,
dopisuj reprodukcję do `~/.vibecrafted/loctree/loctree-fail.md`.

Raportuj: snapshot/HEAD, zakres i pokrycie, rozstrzygający dowód, niezależną
weryfikację, pozostałą niepewność i następny bezpieczny ruch.
