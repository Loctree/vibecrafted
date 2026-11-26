---
name: vc-research
version: 1.3.0
description: >
  Standalone triple-agent research skill. Co-define the problem with the user,
  write a research plan, then spawn claude + codex + gemini simultaneously on the
  same questions. Three independent reports come back. Synthesize into one
  gap-free research document ready for implementation. Use whenever the team
  needs ground truth before coding: unknown APIs, architecture decisions, library
  assessment, protocol research, best-practice survey, competitive analysis,
  or any situation where one agent's perspective is not enough. Trigger phrases:
  "research this", "zbadaj to", "triple research", "research swarm", "3 agenty
  research", "gap-free research", "zbadaj przed implementacją", "co mówi
  dokumentacja", "state of the art", "SoTA research", "porównaj podejścia",
  "analyze options", "research plan", "plan researchu".
compatibility:
  tools:
    - Bash
    - Read
    - Write
    - Agent
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Wywołanie dla `vc-research` (launcher `research`)**
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
> | 1. Worker użytkownika | `vibecrafted research <agent(s)>`                                                                                               |
> | 2. Interactive        | `/vc-research` — wykonaj **w tej sesji**; native subagenty gdy trzeba; **nie** zewnętrzniaj tylko dlatego, że launcher istnieje |
> | 3. Agent-operator     | może odpalić formę workera powyżej przez `vc-dispatch` / linie operatora, zachowując tożsamość tego skilla                      |
>
> **Uwaga:** May default to multi-agent swarm; interactive still must not no-op into empty re-dispatch.

> Swobodniejszy native na niektórych biegach ≠ porzucenie floty external. `vc-dispatch` i `vc-ship` zachowują własne tożsamości.

<!-- /fleet-imperative -->

# vc-research — Triple-Agent Research Swarm

> Jedna perspektywa to opinia. Trzy perspektywy to dowód.

## Wejście operatora

### Reguła Living Tree / Worktree

Ten workflow działa w bieżącym checkoucie i na bieżącej gałęzi operatora. Nie twórz worktree gita, nie przełączaj się na niego ani nie przenoś do niego wykonania, chyba że operator wprost poprosi o worktree w tym prompcie. Ogólne słowa w stylu „isolate", „parallel" czy „clean branch" to za mało. Jedyny usankcjonowany drugi tryb to dispatch Fleet Worktrees (pisany plan, zacommitowane wcześniej verifiery, rozłączne domeny plików, jednowątkowy integrator — patrz Reguła Living Tree, Tryb B); poza tą formacją zostań we wspólnym drzewie. Czytaj pliki ponownie przed edycją, dostosowuj się do równoległych zmian i zgłoś awarię podłoża (substrate failure), jeśli bieżące drzewo jest zbyt zatrute, by bezpiecznie kontynuować.

Zobacz [Reguła Living Tree](../LIVING_TREE_RULE.md).

## Canonical Orientation Gate

Zanim ten workflow wykona analizę specyficzną dla repo, planowanie, implementację, review, release lub delegację, MUSI uruchomić lub skonsumować procedurę `vc-init` dla przypisanego repo. Jeśli brakuje świeżych dowodów z `vc-init`, wykonaj najpierw przebieg init i traktuj pracę specyficzną dla workflow jako zablokowaną, dopóki nie ma aktualnej prawdy repo.

`Loctree:loctree` to domyślny skill do mapowania struktury repo dla tej procedury. Użyj Loctree przed grepem lub twierdzeniami opartymi na dokumentacji, aby wyprodukować lub odświeżyć Mapę Aplikacji Wyprowadzoną z Kodu (Code-Derived Application Map): repo-view, focus, slice, impact, find i follow w odpowiednim zakresie. Szukaj istniejących symboli i kontraktów, zanim utworzysz nowe; uruchom impact przed usunięciem lub dużym refactorem; uruchom slice przed edycją.

Chodzi o znalezienie zaczepów: węzłów nośnych, twins (duplikaty), martwego kodu, dryfu, entrypointów runtime'u oraz pułapek o dużym zasięgu zmiany. Jeśli task jest jawnie nie-repo lub bez kodu, zadeklaruj w raporcie wyjątek no-repo. W przeciwnym razie brak dowodów z `vc-init`/Loctree to awaria procesu.

Uruchamiaj przez `vibecrafted start` (lub `vc-start`) i command deck (`vibecrafted research --prompt/--file ...` lub `vc-research ...`, domyślnie headless; nigdy surowe `skills/.../*.sh`). Przykłady i szczegóły CLI: [references/flow-and-templates.md](references/flow-and-templates.md).

<details>
<summary>Foundation Dependencies</summary>

- [vc-loctree](../foundations/vc-loctree/SKILL.md) — świadomość strukturalna
- [vc-aicx](../foundations/vc-aicx/SKILL.md) — intencje i sterowalność

</details>

## Doktryna pracy z repozytorium

W pracy z repozytorium zacznij od Loctree jako mapy: użyj `loct context`,
`loct occurrences`, `loct body` i `loct find --literal` przed szerokim ręcznym
przeszukiwaniem. Używaj AICX do kontekstu intencji i sesji. Używaj rg/grep jako
fallbacku lub lokalnej lupy, nie jako zamiennika mapowania strukturalnego. Jeśli Loctree
zawiedzie lub przeoczy jakąś powierzchnię, dopisz feedback do `~/.vibecrafted/loctree/loctree-fail.md`.

## Cel

Zbadaj problem z trzech niezależnych perspektyw, zanim zaczniesz pisać kod. Orkiestrujący agent współdefiniuje problem z użytkownikiem, pisze plan, spawnuje claude + codex + gemini na te same pytania, a potem syntetyzuje findingi w jeden dokument bez luk. To faza Research z `vc-workflow`, wydzielona jako samodzielny skill i ulepszona o triangulację triple-agent.

## Kiedy używać

- Nieznane API, protokół lub biblioteka; decyzja architektoniczna; aktualne best practices; ocena bibliotek lub integracji.
- **NIE używaj do:** pytań z jednego pliku (`loctree slice` + grep < 30s) ani czystej implementacji (`vc-workflow` / `vc-delegate`).

## Bezpieczeństwo researchu

Tryb research jest **read-only** dla źródłowego repozytorium.

- **Marker domknięcia = artefakty filesystemu**, nie git (`$VIBECRAFTED_HOME/artifacts/<org>/<repo>/<YYYY_MMDD>/research/<run_id>/` z `report.md` + `meta.json` + `transcript.log`).
- **Brak mutacji źródła i zapisów do gita:** drzewo robocze pozostaje niezmienione; proponowane fixy wpisuj do raportu; workery codex zapisują pełny raport markdown w systemie plików przed wyjściem.

## Sześciokrokowy flow researchu

1. **Współdefiniuj problem** z użytkownikiem (3–5 zdań: co, dlaczego, priors, granice) przed napisaniem planu.
2. **Napisz jeden wspólny plan researchu** (`.../research/<run_id>/plans/<ts>_<slug>_research-plan.md`) z jednakowymi pytaniami, narzędziami Loctree/Search i ograniczeniami źródeł pierwotnych — każdy agent dostaje WSZYSTKIE plany.
3. **Zespawnuj swarm jednym wywołaniem** (`vc-research --file "$PLAN"`) z `summary.md` (launch card, wspólny `run_id`) jako domyślną powierzchnią.
4. **Zbierz raporty** w `reports/{claude,codex,gemini}.md` przez `vc-research-await --run-id <run_id>` (lub `--last`), używając `vibecrafted observe` tylko do drilldownu.
5. **Syntetyzuj** dopiero po przeczytaniu każdego raportu źródłowego **w całości przez warstwowe slicowanie** (~1500–2000 linii / ~80k znaków; HALT przy przekroczeniu budżetu). Rozdziel **A. Convergent (zdeduplikowane)** i **B. Signals (findingi jednego agenta)** z werdyktem operatora; odrzuć głosowanie większościowe.
6. **Wyprodukuj `synthesis.md`** (zwykle 3–8KB): raporty źródłowe zostają jako osobne pliki, każda nietrywialna teza i zdanie odrębne mają cytowanie `file:line`, bez treści verbatim z raportów.

Szablon planu Kroku 2, szczegóły Kroku 3–5 i reguły czytania: [references/flow-and-templates.md](references/flow-and-templates.md). Szablon syntezy: [references/synthesis-template.md](references/synthesis-template.md).

## Integracja z pipelinem

vc-research można użyć:

- **Samodzielnie** — research bez pełnego pipeline'u ERi
- **Jako Faza 2 workflow** — `vc-workflow` deleguje tutaj zamiast researchu pojedynczego agenta
- **Przed vc-partner** — gdy tryb partner potrzebuje twardych faktów (ground truth) przed debugiem
- **Przed vc-runtime/vc-delegate** — research zasila plany implementacji

```
         ┌─── claude ──→ report ───┐
research │                         │
  plan ──├─── codex  ──→ report ───├──→ synthesis.md
         │                         │
         └─── gemini ──→ report ───┘
```

## Antywzorce

Nigdy nie przekazuj `claude|codex|gemini` osobno, nie dawaj agentom różnych pytań, nie pomijaj syntezy ani nie sklejaj raportów verbatim, nie czytaj po obcięciu, nie pomijaj Kroku 1 ani Loctree, nie ufaj blogom ponad dokumentację i nie wołaj surowych `*_spawn.sh`. Pełna lista: [references/flow-and-templates.md](references/flow-and-templates.md).

---

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
