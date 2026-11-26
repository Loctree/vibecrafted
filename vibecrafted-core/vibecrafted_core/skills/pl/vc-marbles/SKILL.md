---
name: vc-marbles
version: 7.0.0
description: >
  WRITE step that floods every crack with deliberate over-correction.
  Single workers see one round, one truth-forcing cut, one commit;
  the skill at swarm level produces an intentional excess of fixes —
  marbles in every hole — which `vc-polarize` then strips back to one
  axis. Use when implementation already exists but the codebase still
  lies: overgenerated surfaces, drift between runtime paths, false
  certainty from one-shot agent output, or a product that "works"
  while remaining fragile. Each worker invocation is isolated and
  blind to prior marble history. Trigger phrases: "marbles", "kulki",
  "stabilize", "stabilizacja", "loop until done", "reduce chaos",
  "fortify the foundation", "adultification", "rzuć kulki",
  "wypełnij pęknięcia".
default: vc-marbles
aliases:
  - vc-fortify
compatibility:
  tools:
    - Skill
    - TaskCreate
    - TaskUpdate
    - Bash
    - Read
    - Write
    - Edit
requires:
  - vc-init
  - loctree
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Wywołanie dla `vc-marbles` (launcher `marbles`)**
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
> | 1. Worker użytkownika | `vibecrafted marbles <agent>`                                                                                                  |
> | 2. Interactive        | `/vc-marbles` — wykonaj **w tej sesji**; native subagenty gdy trzeba; **nie** zewnętrzniaj tylko dlatego, że launcher istnieje |
> | 3. Agent-operator     | może odpalić formę workera powyżej przez `vc-dispatch` / linie operatora, zachowując tożsamość tego skilla                     |

> Swobodniejszy native na niektórych biegach ≠ porzucenie floty external. `vc-dispatch` i `vc-ship` zachowują własne tożsamości.

<!-- /fleet-imperative -->

# vc-marbles — Deliberate Excess (Worker-Blind, Swarm-Wide)

> Krok `WRITE` w samym centrum pipeline'u. Tam gdzie `vc-followup` mówi
> **„falsyfikuj twierdzenie ze speca, nigdy nie dotykaj kodu"**, a `vc-polarize`
> mówi **„tnij z powrotem do jednej prawdy"**, ten mówi **„worker widzi
> drzewo, nie fabrykę — jedna runda, jedno cięcie wymuszające prawdę, jeden
> raport; swarm produkuje nadmiar, który polarize potem zdziera."**

---

## Wejście operatora

### Reguła Living Tree / Worktree

Działa w bieżącym checkoucie i na bieżącej gałęzi operatora. Nie przenoś się
do worktree, chyba że wprost o to poproszono. Jedyny usankcjonowany drugi tryb to dispatch Fleet Worktrees (pisany plan, zacommitowane wcześniej verifiery, rozłączne domeny plików, jednowątkowy integrator — patrz Reguła Living Tree, Tryb B); poza tą formacją zostań we wspólnym drzewie. Czytaj pliki ponownie przed
edycją, dostosowuj się do równoległych zmian (inni workerzy mogli zapisać
między twoimi dispatchami). Zobacz [Reguła Living Tree](../LIVING_TREE_RULE.md).

## Checkpoint orientacji

Każda runda zaczyna się od `vc-init`. Bez wyjątków. Zanim dotkniesz kodu, zbierz aktualny obraz repo
przez dostępne narzędzia: `Loctree:loctree` buduje
Mapę Aplikacji Wyprowadzoną z Kodu (Code-Derived Application Map — mapa
strukturalna, zależności, martwy kod, hotspoty); **aicx-steer** (intencje
projektu, nie raporty z poprzedniej rundy); **semgrep / lintery** (bieżąca
powierzchnia jakości); **git status / ostatnie commity**. Bez `vc-init` agent
wymyśla własną rzeczywistość.

Standardowy launcher: `vibecrafted marbles <agent> --count <n> --prompt '...'` (lub `--file <plan>` / `--depth <n>`). W odróżnieniu od `implement`, `marbles` uruchamia świeżych agentów w pętli zbieżności na istniejącym kodzie (`--count` steruje iteracjami).

Pełne przykłady wywołań launchera: [references/launcher-and-await.md](references/launcher-and-await.md).
---

## Doktryna pracy z repozytorium

W pracy z repozytorium zacznij od Loctree jako mapy: użyj `loct context`,
`loct occurrences`, `loct body` i `loct find --literal` przed szerokim ręcznym
przeszukiwaniem. Używaj AICX do kontekstu intencji i sesji. Używaj rg/grep jako
fallbacku lub lokalnej lupy, nie jako zamiennika mapowania strukturalnego. Jeśli Loctree
zawiedzie lub przeoczy jakąś powierzchnię, dopisz feedback do `~/.vibecrafted/loctree/loctree-fail.md`.

## Cel

`vc-marbles` to krok COMPLETION, który zamienia naturalnie przegenerowany
output kodowania agentycznego w utwardzony, testowalny fundament. Każdy
pojedynczy worker jest zdyscyplinowany: jedna runda, jeden bounded target,
jeden commit. Ale **swarm** (rój agentów) workerów/rund w obrębie
inicjatywy celowo przesadza z fixami — marbles w każdej rysie, nawet w tych,
których być może nie powinno się wypełniać. Nadmiar jest sednem.
`vc-polarize` później zdziera z powrotem do jednej prawdy.

Marbles **nie** próbuje rozwiązać konceptualnego rozmazu na poziomie
produktu (sprzeczne dokumenty, rozjeżdżające się kierunki produktu).
Eksponuje te decyzje produktowe chowające się za „problemami kodu" i
zostawia je `vc-polarize` do rozstrzygnięcia oraz wyboru finalnego kształtu
o jednej prawdzie.

## Świadomość kosztu: zimny start, gorąca pętla

Zimny start jest drogi; powtarzane gorące rundy na tym samym repo, powierzchni zadania, padających bramkach, intencji architektonicznej i prompcie wykorzystują rozgrzany cache do budowania nacisku zbieżności. Utrzymuj podłoże stabilne, aby `vc-polarize` mógł ciąć do jednej prawdy na bazie evidence.

Pełny model kosztu i zasady rozgrzanego cache'u: [references/cost-and-cache-model.md](references/cost-and-cache-model.md).

## Kiedy używać

Użyj `vc-marbles`, gdy:

- implementacja istnieje, ale baza kodu wciąż kłamie (dryf, kruche
  ścieżki, połknięte błędy, przegenerowane wrappery)
- padające bramki trzeba dopchnąć do P0/P1=0
- operator chce gorącą pętlę zbieżności z `--count` iteracjami pętli zewnętrznej
- trzeba puścić swarm agentów na kruchej powierzchni

**Nie** używaj tego skilla, gdy:

- implementacja jeszcze nie istnieje — to `vc-workflow` lub
  `vc-implement`
- pytanie brzmi „czy plan faktycznie wylądował?" — to `vc-audit`
  (READ-ONLY)
- pytanie brzmi „która konkurująca prawda wygrywa?" — to `vc-polarize`
- diff potrzebuje tylko review bez modyfikacji — to `vc-review`

---

## Pozycja w pipelinie

`vc-marbles` to jeden z kroków WRITE w cyklu jakości (przykład):

```
... → implement (W) → review (R) → workflow (W) → followup (R) → marbles (W) → audit (R) → polarize (W) → ...
```

Celowy nadmiar swarmu produkuje powierzchnię, którą trzeba sfalsyfikować
(`vc-audit`), a potem przyciąć do jednej prawdy (`vc-polarize`).
Marbles to **zalew**; polarize to **decydujące cięcie**. Audit
siedzi pomiędzy jako READ-ONLY warstwa falsyfikacji.

---

## Doktryna workera i instrumenty vs bramki

Worker jest celowo **ślepy na wcześniejszą historię marbles**, pracując na bieżącym stanie drzewa, podczas gdy [`RECEPTION.md`](RECEPTION.md) utrzymuje rejestr findingów i decyzje o zbieżności. **Instrumenty** (`loctree`, `semgrep`, `aicx-steer`) idą na **początek**, a **testy** na **koniec** jako bramka weryfikacyjna.

Pełna doktryna workera i rozróżnienie instrumenty vs bramki: [references/worker-doctrine-and-instruments.md](references/worker-doctrine-and-instruments.md).
---

## Model operacyjny, soczewki i reguła commita

Jedno wywołanie = jedna bounded round: oskarż obecne drzewo dowodami, wybierz najwyżej **3 cele** według najsłabszej soczewki (`Access & Isolation`, `Data Health`, `Errors & Observability`, `Release & Runtime Resilience`), utwardź, bramkuj, zrób dokładnie **jeden** commit `marble:` i zapisz raport w `$VIBECRAFTED_HOME/artifacts/.../marbles/reports/`. **Worker zatrzymuje się tutaj** — nie rozszerzaj się na następną rundę (zobacz [`FLOW.md`](FLOW.md) i [`RECEPTION.md`](RECEPTION.md)).

Pełny 6-krokowy protokół rundy, soczewki stabilizacji i format commita: [references/round-protocol-and-lenses.md](references/round-protocol-and-lenses.md).

## Strażnik gałęzi i drzewa

**TWARDA ZASADA: Nigdy nie zmieniaj gałęzi. Nigdy nie twórz gałęzi w
repo-root użytkownika. Nigdy nie twórz worktree ani nie przenoś się do niego
podczas runu marbles.** Operator wybrał bieżącą gałąź — to nie twoja decyzja
do rewizji. Jeśli ścieżka jest zbyt zatruta, by bezpiecznie kontynuować,
zwróć kontrolę operatorowi / runtime'owi i nazwij awarię podłoża (substrate
failure) w raporcie.

---

## Złożenie ze skillami i antywzorce

`vc-marbles` współdziała z `vc-init` (wymagane wejście), `vc-audit` (downstreamowe READ-ONLY), `vc-polarize` (downstreamowe cięcie WRITE do jednej prawdy), `vc-review` oraz `vc-followup`. Unikaj historycznej samoświadomości, cosplayu zbieżności, próżności powierzchni, inflacji narracyjnej, kontaminacji równoległej, rozstrzygania rozmazu produktu w workerze oraz samorozszerzania.

Pełne złożenie ze skillami sąsiednimi, katalog antywzorców i klamra końcowa: [references/composition-and-antipatterns.md](references/composition-and-antipatterns.md).

## Warunek zakończenia

Zatrzymaj się po commicie i raporcie. Potem **nie** rozszerzaj się samodzielnie.
Jeśli implementacja jest kompletna, ale ma wysoki konceptualny rozmaz (konkurujące
prawdy, pofragmentowana powierzchnia produktu), zostanie przekazana do
`vc-audit` po falsyfikację i `vc-polarize`, by uzyskać klarowność na poziomie release
candidate i kształt o jednej prawdzie.

---

## Wezwanie do działania

Przeczytaj [`FLOW.md`](FLOW.md) przed pierwszą rundą — zawiera szczegóły
protokołu pojedynczej rundy i semantykę gorącej pętli zbieżności. Przeczytaj
[`RECEPTION.md`](RECEPTION.md) przed uruchomieniem jako operator /
orchestrator — opisuje dyscyplinę na poziomie swarmu i routing
równoległych rund. Potem oskarż obecne drzewo.

---

## Klamra końcowa

Worker widzi drzewo, nigdy fabrykę: jedna runda, jeden commit, jeden raport, potem wychodzi. Zobacz [references/composition-and-antipatterns.md](references/composition-and-antipatterns.md).

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
