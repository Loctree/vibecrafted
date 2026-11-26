---
name: vc-decorate
version: 2.1.0
description: >
  Late-stage visual finishing and experience coherence skill. Detects the user's
  existing design language, audits system consistency, distinguishes identity
  from drift, upgrades weak patterns, and proposes tasteful polish that works
  WITHIN the user's system. Never imposes the agent's taste. Never decorates
  chaos. First make the system coherent. Then make it feel premium.
  Trigger phrases: "decorate", "make it look good", "add polish", "smaczki",
  "micro-interactions", "udekoruj", "dopracuj wizualnie", "curb appeal",
  "premium pass", "finish the experience", "make it feel intentional",
  "coherence audit", "design system cleanup", "interactive demo", "animate",
  "add hover effects", "make it feel nice", "visual polish".
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Wywołanie dla `vc-decorate` (launcher `decorate`)**
>
> Ten sam _kształt_ trzech ścieżek floty, z **literałami tego** skilla — zobacz
> kanoniczną [Matrycę Delegacji](../DELEGATION_MATRIX.md):
>
> - [Wspólne trzy ścieżki](../DELEGATION_MATRIX.md#wspólne-trzy-ścieżki)
> - [Katalog launcherów](../DELEGATION_MATRIX.md#katalog-launcherów-core-runtime)
> - [Reguła per-launcher](../DELEGATION_MATRIX.md#reguła-per-launcher-delta-semantyczna)
> - [Native vs external](../DELEGATION_MATRIX.md#natywne-subagenty-vs-zewnętrzni-workerzy)
>
> | Ścieżka               | Literał tego skilla                                                                                                             |
> | --------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
> | 1. Worker użytkownika | `vibecrafted decorate <agent>`                                                                                                  |
> | 2. Interactive        | `/vc-decorate` — wykonaj **w tej sesji**; native subagenty gdy trzeba; **nie** zewnętrzniaj tylko dlatego, że launcher istnieje |
> | 3. Agent-operator     | może odpalić formę workera powyżej przez `vc-dispatch` / linie operatora, zachowując tożsamość tego skilla                      |

> Swobodniejszy native na niektórych biegach ≠ porzucenie floty external. `vc-dispatch` i `vc-ship` zachowują własne tożsamości.

<!-- /fleet-imperative -->

# vc-decorate — Najpierw spójność. Premium na drugim miejscu.

## Wejście dla operatora (człowieka)

### Reguła Living Tree / Worktree

Ten workflow działa w bieżącym checkoucie i na bieżącej gałęzi operatora. Nie twórz worktree gita, nie przełączaj się
na niego ani nie przenoś do niego wykonania, chyba że operator wprost poprosi o worktree w tym prompcie. Ogólne słowa w
stylu „isolate", „parallel" czy „clean branch" to za mało. Jedyny usankcjonowany drugi tryb to dispatch Fleet Worktrees (pisany plan, zacommitowane wcześniej verifiery, rozłączne domeny plików, jednowątkowy integrator — patrz Reguła Living Tree, Tryb B); poza tą formacją zostań we wspólnym drzewie. Czytaj pliki ponownie przed edycją, dostosowuj się do
równoległych zmian i zgłoś awarię podłoża (substrate failure), jeśli bieżące drzewo jest zbyt zatrute, by bezpiecznie
kontynuować.

Zobacz [Reguła Living Tree](../LIVING_TREE_RULE.md).

## Checkpoint orientacji

Zanim ten workflow wykona analizę specyficzną dla repo, planowanie, implementację, przegląd, release lub delegowanie,
MUSI uruchomić lub skonsumować procedurę `vc-init` dla przypisanego repo. Jeśli brakuje świeżych dowodów z `vc-init`,
najpierw wykonaj przebieg init i traktuj pracę specyficzną dla workflow jako zablokowaną, dopóki nie ma aktualnej
prawdy repo.

`Loctree:loctree` to domyślny skill do mapowania struktury repo dla tego przebiegu. Używaj Loctree przed grepem lub
twierdzeniami opartymi na dokumentacji, aby wygenerować lub odświeżyć Mapę Aplikacji Wyprowadzoną z Kodu (Code-Derived
Application Map): repo-view, focus, slice, impact, find i follow w odpowiednim zakresie. Szukaj istniejących symboli i
kontraktów, zanim utworzysz nowe; uruchom impact przed usunięciem lub dużym refactorem; uruchom slice przed edycją.

Chodzi o znalezienie zaczepów: węzłów nośnych, twins (duplikaty), martwego kodu, dryfu, entrypointów runtime'u oraz pułapek
o dużym zasięgu zmiany. Jeśli zadanie jawnie nie dotyczy repo lub nie dotyczy kodu, odnotuj w raporcie wyjątek „bez
repo". W przeciwnym razie brak dowodów z `vc-init`/Loctree to błąd procesu.

Standardowy launcher (`vibecrafted start` / `vc-start`, następnie `vc-<launcher> <agent> [--prompt|--file ...]`).

```bash
vibecrafted decorate agy --prompt 'Polish the landing page'
vc-decorate claude --prompt 'Coherence audit on the CLI output surface'
vibecrafted decorate codex --file /path/to/decorate-plan.md
```

> „Nie dekoruj chaosu. Najpierw spraw, by system był spójny. Dopiero potem spraw, by sprawiał wrażenie premium."

Decorate to **nie** jest skill typu „zrób ładnie". To skill **późnego wykańczania produktu**. Jego zadanie:
wziąć działający produkt i przekształcić go w **spójne, zamierzone, premium doświadczenie**.

Oznacza to:

- Wykrycie rzeczywistego języka wizualnego użytkownika (kolory, fonty, motyw, spacing, rytm interakcji)
- Oddzielenie tożsamości od dryfu
- Zachowanie tego, co wyróżniające
- Ulepszenie tego, co słabe, przestarzałe lub niespójne
- Weryfikację wrażenia end-to-end
- **Dopiero potem** dodanie gustownego szlifu wizualnego i mikrointerakcji

Decorate **nie** narzuca gustu agenta, nie nadpisuje marki użytkownika ani nie dodaje przypadkowego rozmycia, poświaty,
parallaksy czy „ładności rodem z AI". Jej zadaniem jest sprawić, by istniejący system sprawiał wrażenie: bardziej
przemyślanego, nowocześniejszego, stabilniejszego, precyzyjniejszego, pełniejszego.

**Premium to nie ornament. Premium to spójność.**

---

## Doktryna pracy z repozytorium

W pracy z repozytorium zacznij od Loctree jako mapy: użyj `loct context`,
`loct occurrences`, `loct body` i `loct find --literal` przed szerokim ręcznym
przeszukiwaniem. Używaj AICX do kontekstu intencji i sesji. Używaj rg/grep jako
fallbacku lub lokalnej lupy, nie jako zamiennika mapowania strukturalnego. Jeśli Loctree
zawiedzie lub przeoczy jakąś powierzchnię, dopisz feedback do `~/.vibecrafted/loctree/loctree-fail.md`.

## Główna zasada: wykrywaj, nie dyktuj

Zanim zaczniesz decorate, uruchom wykrywanie stylu i audyt systemu:

```text
1. SKANUJ istniejące zmienne CSS, pliki motywów, kolory marki, fonty, spacing, komponenty
2. ZIDENTYFIKUJ paletę, stos fontów, tryb motywu, logikę powierzchni, rytm interakcji
3. ZAUDYTUJ pod kątem dryfu wizualnego, słabych wzorców, niespójnych stanów, pozostałości prototypu
4. ODDZIEL tożsamość od dryfu:
   - zachowaj to, co wyróżniające
   - popraw to, co słabe, przestarzałe lub niespójne
   - usuń rozproszenie stylu, konkurujące prawdy
   - wyeliminuj obszary konfliktu przez twardy prune duplikatów lub wyścigów
5. ZAPROPONUJ ulepszenia używając ICH tokenów, ICH języka, ICH stosu
6. ZAPYTAJ, które zmiany wdrożyć
7. WDRÓŻ tylko zatwierdzone zmiany
8. ZWERYFIKUJ doświadczenie end-to-end
```

Jeśli nie wykryto istniejącego stylu, zaproponuj zbudowanie (scaffold) odpowiedniego systemu projektowego — przedstaw
opcje, nie zakładaj gustu, nie narzucaj tożsamości wizualnej.

---

## CLI to też interfejs

Wyjście terminala jest częścią UI produktu — stosuj decorate dla instalatorów, podsumowań runtime, `--help`, `doctor` i komunikatów błędów (oraz screencastów UI przez `screenscribe`, gdy jest dostępny). Używaj `unicode-puzzles-mcp` (`rewrite_using_unicode`, `decorate_text`, `search_unicode`) i sparkline'ów Braille'a zamiast stylowania ANSI lub zgadywania code pointów; pełne tabele stylów, glifów i reguł w [references/cli-and-unicode-toolkit.md](references/cli-and-unicode-toolkit.md).

---

## Kiedy używać

- Produkt działa, ale sprawia wrażenie płaskiego, prototypowego, niedokończonego
- Użytkownik prosi o szlif wizualny, smaczki, atrakcyjność na wejściu, wrażenie premium
- UI jest funkcjonalnie poprawne, ale brakuje mu spójności między powierzchniami
- Dobre składniki, słabe wrażenie systemowe
- Niespójne karty, przyciski, spacing, stany focus, czasy animacji
- Strona pokazowa, demo, landing page lub aplikacja potrzebuje przebiegu wykańczającego
- Zespół chce, by produkt sprawiał wrażenie zamierzonego, a nie tylko upiększonego
- **Wyjście CLI jest funkcjonalne, ale brzydkie, bez brandingu, trudne do skanowania wzrokiem**

---

## Pozycja w pipelinie

```text
scaffold → init → workflow → followup → marbles → dou → [DECORATE] → hydrate → release
```

Decorate znajduje się po `dou`, zapewniając, że już kompletna powierzchnia produktu jest spójna wizualnie przed
finalnym pakowaniem (`hydrate`) i wysyłką (`release`).

---

## Tożsamość vs Dryf

Jedno z najważniejszych zadań decorate:

- **Tożsamość** — rzeczywisty język wizualny użytkownika: wybrana paleta, typografia, rytm spacingu, formy komponentów,
  styl interakcji.
- **Dryf** — rzeczy, które po prostu się nazbierały: niespójne promienie zaokrągleń, niedopasowany spacing, sprzeczne
  style przycisków, przypadkowe zachowania hover, artefakty prototypu.

Zachowuj tożsamość. Redukuj dryf.

---

## Wzorzec implementacji

```text
1. Wykryj    — skanuj tokeny, arkusze stylów, konfigurację frameworka, wzorce komponentów
2. Audytuj   — zidentyfikuj tożsamość vs dryf oraz słabe wzorce
3. Zaproponuj — przedstaw poprawki spójności, ulepszenia premium, smaczki
4. Wdróż     — zastosuj zatwierdzone zmiany, używając tokenów i struktury użytkownika
5. Zweryfikuj — przejrzyj „przed/po" pod kątem integralności doświadczenia
```

---

## Antywzorce

- Decorate na zepsutej strukturze
- Utrzymywanie złych wzorców, bo „użytkownik już je miał"
- Zastępowanie ich stylu naszym
- Dodawanie ruchu bez celu interakcyjnego
- Dodawanie rozmycia/poświaty, bo „premium"

---

_Faza 3 — Ship (dou → decorate → hydrate → release)_

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
