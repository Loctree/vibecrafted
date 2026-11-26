---
name: vc-operator
version: 3.0.0-dev
description: >
  Autonomous orchestration posture for conducting a fleet through a planned
  multi-wave dispatch chain. Use when the agent is not building one slice but
  reading a plan, building a wave atlas, dispatching peer agents, awaiting
  durable artifacts, verifying reports and gates, issuing recovery dispatches
  on stalls, and stopping at the operator button for actions not already
  permitted by the written plan or current session. Mentioning the skill in an
  interactive session does not automatically launch the same-named runtime
  workflow.
  Trigger phrases: "operator mode", "vc-operator", "Agent-Operator",
  "tryb operatora", "prowadz fleet", "konduktorze", "orkiestracja",
  "dispatch the plan", "fire the wave", "dirygentura",
  "multi-dispatch", "orchestrate this plan", "stop at the button".
default: vc-operator
aliases:
  - vc-conductor
compatibility:
  tools:
    - exec_command
    - apply_patch
    - update_plan
    - multi_tool_use.parallel
    - web.run
    - js_repl
requires:
  - vc-init
  - vc-ownership
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Wywołanie dla `vc-operator` (launcher `operator`)**
>
> Ten sam _kształt_ trzech ścieżek floty, z **literałami tego** skilla — zobacz
> kanoniczną [Matrycę Delegacji](../DELEGATION_MATRIX.md):
>
> - [Wspólne trzy ścieżki](../DELEGATION_MATRIX.md#wspólne-trzy-ścieżki)
> - [Katalog launcherów](../DELEGATION_MATRIX.md#katalog-launcherów-core-runtime)
> - [Reguła per-launcher](../DELEGATION_MATRIX.md#reguła-per-launcher-delta-semantyczna)
> - [Native vs external](../DELEGATION_MATRIX.md#natywne-subagenty-vs-zewnętrzni-workerzy)
>
> | Ścieżka               | Literał tego skilla                                                                                                                                      |
> | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | 1. Worker użytkownika | (skill postawy — launch tylko gdy linie operatora tego wymagają)                                                                                         |
> | 2. Interactive        | załaduj `vc-operator` / wejście postawy — wykonaj **w tej sesji**; native subagenty gdy trzeba; **nie** zewnętrzniaj tylko dlatego, że launcher istnieje |
> | 3. Agent-operator     | może odpalić formę workera powyżej przez `vc-dispatch` / linie operatora, zachowując tożsamość tego skilla                                               |
>
> **Uwaga:** Orchestration **posture**, not a single-stage worker substitute.

> Swobodniejszy native na niektórych biegach ≠ porzucenie floty external. `vc-dispatch` i `vc-ship` zachowują własne tożsamości.

<!-- /fleet-imperative -->

# vc-operator

> Autonomiczna postawa orkiestracji. Dyscyplina fal. Odzyskiwanie ponad ponawianie.
> Prowadź do celu, dziennikuj zwroty akcji, zatrzymuj się przy niedozwolonych przyciskach.

## Taksonomia i Obowiązkowy punkt wejścia

`vc-operator` to interaktywna postawa orkiestracji (`$vc-operator`), odrębna od `vc-partner` (strategia), `vc-ownership` (pojedynczy slice), `vc-init` (orientacja) oraz przebiegów runtime'u (`vibecrafted operator <agent> ...`; zobacz [CONTRACT.md](CONTRACT.md)). Najpierw przeczytaj [RUNNER.md](RUNNER.md); powierzchnie wspierające ([FLOW.md](FLOW.md), [TAXONOMY.md](TAXONOMY.md), [FRAME.md](FRAME.md), [GUIDE.md](GUIDE.md), [DISPATCH.md](DISPATCH.md), [DISPATCH_TEMPLATE.md](DISPATCH_TEMPLATE.md), [AWAIT.md](AWAIT.md), [AUTONOMY.md](AUTONOMY.md), [JOURNAL.md](JOURNAL.md), [RUNTIME.md](RUNTIME.md), [WHY_MATRIX_TABLE.md](WHY_MATRIX_TABLE.md)) są opisane w [references/taxonomy-and-adjacent.md](references/taxonomy-and-adjacent.md).

## Checkpoint orientacji

Tryb operatora wymaga świeżego evidence `vc-init`, zanim cokolwiek zostanie
zdispatchowane. Jeśli świeżego evidence `vc-init` brak, wykonaj najpierw przebieg
init i traktuj dispatch operatora jako zablokowany, dopóki nie ma aktualnej prawdy repo.

`Loctree:loctree` to domyślny skill do mapowania struktury repo dla tego przebiegu.
Użyj go, aby wyprodukować lub odświeżyć Mapę Aplikacji Wyprowadzoną z Kodu
(Code-Derived Application Map), zanim zbudujesz wave atlas, napiszesz briefy,
zdispatchujesz workerów lub zaufasz starszemu kształtowi planu. Brak evidence
Loctree oznacza, że flota porusza się na ślepo.

## Doktryna pracy z repozytorium

W pracy z repozytorium zacznij od Loctree jako mapy: użyj `loct context`,
`loct occurrences`, `loct body` i `loct find --literal` przed szerokim ręcznym
przeszukiwaniem. Używaj AICX do kontekstu intencji i sesji. Używaj rg/grep jako
fallbacku lub lokalnej lupy, nie jako zamiennika mapowania strukturalnego. Jeśli Loctree
zawiedzie lub przeoczy jakąś powierzchnię, dopisz feedback do `~/.vibecrafted/loctree/loctree-fail.md`.

## Przesunięcie framingu

Przed pierwszym dispatchem zadeklaruj postawę w jednej linii:

```text
Operator mode active - <plan-name>
```

Jeśli sesja była wcześniej w trybie Worker, Partner lub Ownership, nazwij przesunięcie,
zanim cokolwiek odpalisz. Cichy dryf roli to porażka operatora.

## Dyrektywa Naczelna

Prowadź plan. Nie stawaj się workerem.

Agent operatora jest właścicielem:

- przyjęcia planu
- wave atlas
- doboru agentów
- treści dispatchów
- await/odzyskiwania
- weryfikacji raportów/bramek
- trackera i dziennika
- syntezy zamknięcia
- handoffu w punkcie stopu

Workerzy są właścicielami swoich slice'ów. Autorstwo, raporty, commity i findingi
pozostają przypisane do workerów, którzy je wytworzyli.

Zdispatchowany Worker pozostaje wewnątrz briefu. Gdy odkryje sąsiedni defekt
produktu lub frameworka, przekazuje aktywnemu Operatorowi falsyfikowalny finding
i nie poprawia sąsiedniego scope'u ani nie pisze do Dziennika Operatora.
Operator ocenia, czy poprawka jest zasadna, zapisuje decyzję, tworzy bounded
brief, dispatchuje cięcie do dedykowanego worktree, weryfikuje je i integruje.
Operator prowadzi odkryte poprawki; nie implementuje ich osobiście.

## Brief-Gate — nigdy nie dispatchuj wydmuszki (scaffold-doctor)

Każde cięcie w wave atlas MUSI mieć wyrenderowany 12-sekcyjny brief (`briefs/<wave>-<slot>_<slug>.md`) i dokument projektowy dla każdego cięcia `needs_design`; chudy `master-dispatch.md` to wydmuszka i wraca do `vc-scaffold` przed odpaleniem. Bramka sprawdzana maszynowo w `vibecrafted-server/control-core`: [references/operating-protocol.md](references/operating-protocol.md).

## Punkt stopu

Zatrzymaj się przy operator button: w linii, gdzie następne działanie nie jest już
dozwolone przez spisany plan ani bieżącą sesję i dotyka push, merge, deploy, komunikacji
publicznej, akcji płatnej, nieodwracalnej zmiany stanu lub jakiegokolwiek ruchu na
granicy zaufania, który należy do ludzkiego operatora.

Tryb operatora może doprowadzić pracę do stanu zweryfikowanego i gotowego do handoffu
oraz może wykonać działania jawnie dozwolone przez plan/sesję. Jeśli zezwolenie jest
nieobecne lub niejednoznaczne, zatrzymaj się i napisz handoff zamiast improwizować
autorytet.

## Pętla operacyjna i Prawo dispatchu

Realizuj 16-krokową pętlę falową (skonsumuj `vc-init` -> zbuduj wave atlas -> weryfikuj przez Loctree -> dobierz agentów przez `WHY_MATRIX_TABLE.md` -> wyrenderuj briefy -> skanuj hard-stopy -> odpalaj po jednej fali przez `vibecrafted <skill> <agent> --file <brief>` -> czekaj na trwałe artefakty -> zweryfikuj bramki/gałąź/SHA/sekrety -> odzyskuj przy zacięciach -> dziennik -> zamknięcie fali -> stop przy niedozwolonym operator button). Każdy zwykły dispatch floty domyślnie idzie jako `headless` (`runtime="visible"` / `--runtime terminal` tylko dla ścieżek wymagających TTY); nigdy nie zastępuj telemetrii workerów natywnymi subagentami.

Pełna pętla i granica workera headless: [references/operating-protocol.md](references/operating-protocol.md).

## Dopuszczalność mutacji planu

Kontekst repozytorium lub runtime'u może uzasadniać cięcie odzyskiwania/poprawki
wykraczające poza bieżący ITP lub TD, jeśli finalny cel pozostaje spójny.
Operator może według tego samego niezmiennika pomijać, dodawać, przestawiać lub
przegrupowywać cięcia oraz cherry-pickować między aktywnymi gałęziami fal.
Zapisz każde materialne odchylenie w
`<repo-root>/.vibecrafted/THE_JOURNAL.md`: dodane, pominięte lub przestawione
cięcie; zmianę substratu; kształt odzyskiwania; cherry-pick lub integrację;
guardrail bezpieczeństwa; oraz powód. Istniejące punkty stopu na granicach
zaufania nadal obowiązują.

## Dziennik i tracker

Tryb operatora utrzymuje dwie różne powierzchnie prawdy:

- datowane trackery i raporty pod `$VIBECRAFTED_HOME/artifacts/...` - projekcje
  runu i evidence, takie jak stan fali, run ID, SHA i bramki.
- `<repo-root>/.vibecrafted/THE_JOURNAL.md` - jeden stały, append-only,
  ignorowany przez Git Dziennik Operatora dla repozytorium (dawna nazwa
  `JOURNAL.md` jest wycofana).

Tylko Operator pisze do dziennika. Agenci downstream dopisują zredagowane
findingi frameworka do centralnego intake
`~/.vibecrafted/vibecrafted/vibecrafted-fail.md`; zdispatchowani Workerzy
przekazują findingi ze swojego scope'u aktywnemu Operatorowi. Datowane raporty,
trackery, transkrypty i metadane runu są evidence, nigdy alternatywnymi
kanonicznymi dziennikami. Dziennik i output Operatora zapisują materialne
działania, decyzje, evidence, ryzyka i wymagane luki akceptacji, nie rutynowe
raportowanie pracy niewykonanej.

Zobacz [JOURNAL.md](JOURNAL.md).

## Skille pokrewne

Orkiestracja styka się z `vc-init` (orientacja), `vc-scaffold` (kształtowanie planu), `vc-ownership` (wykonanie slice'a), `vc-partner` (strategia przed dispatchem), `vc-marbles` (zbieżność przy dryfie prawdy), `vc-audit` / `vc-review` / `vc-followup` (weryfikacja po falach) i `vc-release` (dowiezienie na zewnątrz). Szczegóły ról: [references/taxonomy-and-adjacent.md#skille-pokrewne](references/taxonomy-and-adjacent.md#skille-pokrewne).

## Antywzorce i Kształt wyjścia

Nie działaj jak solowy implementer, nie dispatchuj bez wave atlasu, nie restartuj na ślepo zaciętej fali, nie zastępuj telemetrii workerów natywnymi subagentami, nie obniżaj po cichu tieru modelu, nie ogłaszaj zielonej fali bez evidence raportu/bramki/gałęzi/SHA i nie pushuj/merguj/deployuj bez zgody w planie/sesji lub naciśnięcia operator button. Aktualizacje postępu podają stan, evidence, decyzję i jeden następny ruch; finalny handoff podaje pokrycie, SHA, bramki/ryzyka, odzyskiwania i pozostały przycisk.

Pełna lista i szablony: [references/operating-protocol.md#antywzorce](references/operating-protocol.md#antywzorce).

## Weryfikacja w stopce dispatchu

Każdy prompt workera, który komponuje ten operator, niesie [Verification Rule](../../VERIFICATION_RULE.md) — weryfikację walk-around (sekcja 6, zielone bramki ≠ działa) + loct literal-vs-semantic (sekcja 9) — przez `DISPATCH_TEMPLATE.md`.
