---
name: vc-hydrate
version: 1.0.0
description: >
  Packaging and go-to-market hydration skill. Takes DoU audit findings and
  executes the non-code work that bridges the gap between "it works" and
  "someone can buy this." Generates marketplace listings, SEO fixes,
  distribution artifacts, onboarding flows, landing page content, and
  representation surfaces for products that do not naturally have a public web UI.
  Trigger phrases: "hydrate", "package for market", "prepare for launch",
  "przygotuj do launchu", "fix the packaging gap", "marketplace listing",
  "nawodnij", "make it shippable", "go-to-market", "distribution",
  "SEO fix", "landing page", "onboarding", "completion sprint".
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Wywołanie dla `vc-hydrate` (launcher `hydrate`)**
>
> Ten sam _kształt_ trzech ścieżek floty, z **literałami tego** skilla — zobacz
> kanoniczną [Matrycę Delegacji](../DELEGATION_MATRIX.md):
>
> - [Wspólne trzy ścieżki](../DELEGATION_MATRIX.md#wspólne-trzy-ścieżki)
> - [Katalog launcherów](../DELEGATION_MATRIX.md#katalog-launcherów-core-runtime)
> - [Reguła per-launcher](../DELEGATION_MATRIX.md#reguła-per-launcher-delta-semantyczna)
> - [Native vs external](../DELEGATION_MATRIX.md#natywne-subagenty-vs-zewnętrzni-workerzy)
>
> | Ścieżka               | Literał tego skilla                                                                                                            |
> | --------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
> | 1. Worker użytkownika | `vibecrafted hydrate <agent>`                                                                                                  |
> | 2. Interactive        | `/vc-hydrate` — wykonaj **w tej sesji**; native subagenty gdy trzeba; **nie** zewnętrzniaj tylko dlatego, że launcher istnieje |
> | 3. Agent-operator     | może odpalić formę workera powyżej przez `vc-dispatch` / linie operatora, zachowując tożsamość tego skilla                     |

> Swobodniejszy native na niektórych biegach ≠ porzucenie floty external. `vc-dispatch` i `vc-ship` zachowują własne tożsamości.

<!-- /fleet-imperative -->

# vc-hydrate — Antidotum na Always-in-Production

> „Kod działa, ale brakuje mu warstwy, która pozwala dotrzeć do użytkowników. Hydrate oznacza: spraw, by droga od obcego do użytkownika była możliwie bez tarcia."

## Wejście operatora

### Reguła Living Tree / Worktree

Ten workflow działa w bieżącym checkoucie i na bieżącej gałęzi operatora. Nie twórz worktree gita, nie przełączaj się na niego ani nie przenoś do niego wykonania, chyba że operator wprost poprosi o worktree w tym prompcie. Ogólne słowa w stylu „isolate", „parallel" czy „clean branch" to za mało. Jedyny usankcjonowany drugi tryb to dispatch Fleet Worktrees (pisany plan, zacommitowane wcześniej verifiery, rozłączne domeny plików, jednowątkowy integrator — patrz Reguła Living Tree, Tryb B); poza tą formacją zostań we wspólnym drzewie. Czytaj pliki ponownie przed edycją, dostosowuj się do równoległych zmian i zgłoś awarię podłoża (substrate failure), jeśli bieżące drzewo jest zbyt zatrute, by bezpiecznie kontynuować.

Zobacz [Reguła Living Tree](../LIVING_TREE_RULE.md).

## Checkpoint orientacji

Zanim ten workflow wykona analizę specyficzną dla repo, planowanie, implementację, przegląd, release lub delegowanie, MUSI uruchomić lub skonsumować procedurę `vc-init` dla przypisanego repo. Jeśli brakuje świeżych dowodów z `vc-init`, najpierw wykonaj przebieg init i traktuj pracę specyficzną dla workflow jako zablokowaną, dopóki nie ma aktualnej prawdy repo.

`Loctree:loctree` to domyślny skill do mapowania struktury repo dla tego przebiegu. Używaj Loctree przed grepem lub twierdzeniami opartymi na dokumentacji, aby wygenerować lub odświeżyć Mapę Aplikacji Wyprowadzoną z Kodu (Code-Derived Application Map): repo-view, focus, slice, impact, find i follow w odpowiednim zakresie. Szukaj istniejących symboli i kontraktów, zanim utworzysz nowe; uruchom impact przed usunięciem lub dużym refactorem; uruchom slice przed edycją.

Chodzi o znalezienie zaczepów: węzłów nośnych, twins (duplikaty), martwego kodu, dryfu, entrypointów runtime'u oraz pułapek o dużym zasięgu zmiany. Jeśli zadanie jawnie nie dotyczy repo lub nie dotyczy kodu, odnotuj w raporcie wyjątek „bez repo". W przeciwnym razie brak dowodów z `vc-init`/Loctree to błąd procesu.

Zacznij od `vibecrafted start` (lub `vc-start`). Następnie uruchom z Command Deck:

```bash
vibecrafted hydrate codex --prompt 'Package for marketplace'
vc-hydrate claude --prompt 'Generate missing SEO and landing page'
vibecrafted hydrate gemini --file /path/to/dou-report.md
```

Hydrate to skill od pakowania produktu, którego wzywa DoU. Traktuje „stwórz instalator DMG" i „napisz copy przyjazne SEO" jako pełnoprawne zadania inżynieryjne, nie jako sprawy drugorzędne.

**Zasada nadrzędna:** każdy poważny produkt potrzebuje powierzchni prezentacji, nawet jeśli sam nie jest produktem webowym. Aplikacje desktopowe, narzędzia CLI, serwery MCP, lokalne runtime'y i systemy wewnętrzne nadal potrzebują zewnętrznej powierzchni prezentacji, która pozwala obcemu odkryć, zrozumieć, zobaczyć, ocenić i przyjąć produkt.

## Doktryna pracy z repozytorium

W pracy z repozytorium zacznij od Loctree jako mapy: użyj `loct context`,
`loct occurrences`, `loct body` i `loct find --literal` przed szerokim ręcznym
przeszukiwaniem. Używaj AICX do kontekstu intencji i sesji. Używaj rg/grep jako
fallbacku lub lokalnej lupy, nie jako zamiennika mapowania strukturalnego. Jeśli Loctree
zawiedzie lub przeoczy jakąś powierzchnię, dopisz feedback do `~/.vibecrafted/loctree/loctree-fail.md`.

## Pozycja w pipelinie

```
scaffold → init → workflow → followup → marbles → dou → decorate → [HYDRATE] → release
```

## Podłoga powierzchni publicznej

`vc-hydrate --floor` sprawdza checkout: zgodność wersji, sekcję instalacji w README i pisownię marki (`Vetcoders`, bez wielkiego C w środku). Nie odpytuje rejestrów. Kontrakt: [`../../vc-dou/references/public-surface-floor.md`](../../vc-dou/references/public-surface-floor.md).

## Kiedy używać

- Po tym, jak audyt `vc-dou` zidentyfikuje luki w pakowaniu
- Przed jakimkolwiek zgłoszeniem do marketplace lub publicznym launchem
- Gdy zespół mówi „działa, teraz spraw, by dało się je znaleźć/zainstalować/kupić"
- Okresowy sprint hydrate (zalecane: w parze z DoU co 2 tygodnie)
- Gdy Plague Score > 40

## Domeny hydrate (1–6)

Hydrate domyka luki w sześciu domenach: **1. Repo** (`LICENSE`, `CONTRIBUTING.md`, `CHANGELOG.md`, `SECURITY.md`, CI, sync wersji), **2. Dystrybucja** (binarki CLI/Homebrew, podpisane/notaryzowane `.app`/DMG, Docker/healthcheck), **3. Odkrywalność** (SSR/pre-rendering, tagi SEO/OG, nagłówki bezpieczeństwa, `robots.txt`/`sitemap.xml`), **4. Powierzchnia komercyjna** (landing page, obowiązkowy scaffold reprezentacji dla produktów nie-webowych, listingi marketplace), **5. Onboarding** (pierwsze 5 minut / quick win w 60s) oraz **6. Warstwa reprezentacji** (minimalna zewnętrzna powierzchnia produktu).

Pełne specyfikacje i szablony per domena: [references/hydration-domains.md](references/hydration-domains.md).

## Protokół sprintu, delegacja i antywzorce

Wczytaj findingi P0/P1 z `vc-dou`, zmapuj na Domeny 1–6 (przy dużych sprintach rozbij między subagentów `vc-agents`), wygeneruj brakujące artefakty pakowania i reprezentacji, zweryfikuj przez ponowny przebieg DoU (cel: redukcja Plague Score o ≥20 pkt) i zaraportuj wyniki przed/po oraz kroki ręczne. Nie rób hydrate bez audytu DoU i nie pomijaj warstwy reprezentacji.

Pełny protokół sprintu, integracja z pipeline'em, podział na subagentów i katalog antywzorców: [references/sprint-protocol-and-antipatterns.md](references/sprint-protocol-and-antipatterns.md).

## Definicja „zrobione-zrobione"

Projekt jest po hydrate pass, gdy:

- Obcy może go **ODKRYĆ** (wyszukiwarki, marketplace, poczta pantoflowa)
- Obcy może go **ZROZUMIEĆ** (landing, README, value prop jasny w 30s)
- Obcy może go **ZOBACZYĆ** (powierzchnia reprezentacji istnieje, nawet jeśli produkt nie jest web-native)
- Obcy może go **ZAINSTALOWAĆ** (jedna komenda, bez dev toolchaina, <5 minut)
- Obcy może go **UŻYĆ** (onboarding, quick win w ciągu 60 sekund)
- Obcy może za niego **ZAPŁACIĆ** (cennik, rejestracja, trial — jeśli komercyjny)
- Obcy może **WSPÓŁTWORZYĆ** (CONTRIBUTING.md, szablony issue, CI — jeśli open source)

Dopóki wszystkie te warunki nie są prawdą, projekt jest w stanie Always-in-Production. Hydrate jest antidotum.

---

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
