---
name: vc-polarize
version: 2.0.0
description: >
  WRITE step that strips back the marbles excess to one truth. Where
  the swarm of marble workers plastered every crack in deliberate
  over-application, polarize picks one axis, rejects the competing
  ones, and aligns runtime, tests, docs, artifacts, and public
  promises so they all agree. Gated on Loctree `loct prism` bands —
  `0..4 abort`, `5..8 memo`, `9..12 pass`, `13..15 doctrine`. Emits
  DoU / release handoff. Trigger phrases: "polarize", "vc-polarize",
  "wyostrz", "one sharp truth", "code smear", "prism score", "after
  marbles", "choose one axis", "decisive cut".
default: vc-polarize
aliases:
  - vc-cut
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
  - loctree (prism support)
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Wywołanie dla `vc-polarize` (launcher `polarize`)**
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
> | 1. Worker użytkownika | `vibecrafted polarize <agent>`                                                                                                  |
> | 2. Interactive        | `/vc-polarize` — wykonaj **w tej sesji**; native subagenty gdy trzeba; **nie** zewnętrzniaj tylko dlatego, że launcher istnieje |
> | 3. Agent-operator     | może odpalić formę workera powyżej przez `vc-dispatch` / linie operatora, zachowując tożsamość tego skilla                      |

> Swobodniejszy native na niektórych biegach ≠ porzucenie floty external. `vc-dispatch` i `vc-ship` zachowują własne tożsamości.

<!-- /fleet-imperative -->

# vc-polarize — Decydujące cięcie po marbles

> Konwergencyjny krok WRITE. Tam gdzie `vc-marbles` mówi **„zaszpachluj
> każde pęknięcie z nadmiarem"**, a `vc-audit` mówi **„falsyfikuj, nigdy
> nie dotykaj"**, ten mówi **„zedrzyj do jednej prawdy, odrzuć
> konkurencyjne powierzchnie, wyrównaj świat"**.

---

## Wejście operatora

### Reguła Living Tree / Worktree

Działa w bieżącym checkoucie i na bieżącej gałęzi operatora. Nie
przenoś się do worktree, chyba że wprost o to poproszono. Jedyny usankcjonowany drugi tryb to dispatch Fleet Worktrees (pisany plan, zacommitowane wcześniej verifiery, rozłączne domeny plików, jednowątkowy integrator — patrz Reguła Living Tree, Tryb B); poza tą formacją zostań we wspólnym drzewie. Czytaj pliki
ponownie przed edycją. Zobacz [Reguła Living Tree](../LIVING_TREE_RULE.md).

## Checkpoint orientacji

Zanim polarize się uruchomi, skonsumuj świeże evidence z `vc-init`. Użyj
`Loctree:loctree` (repo-view, focus, slice, impact, find, follow),
aby odświeżyć Mapę Aplikacji Wyprowadzoną z Kodu (Code-Derived Application
Map) przed twierdzeniami z grepa / docs / „pamiętam, że". Polarize wolno
czytać niedawne raporty marbles — to celowe. Workery zostały na ślepo;
polarize to krok syntezy, który potrzebuje wcześniejszego evidence
zbieżności.

Standardowy launcher:

```bash
vibecrafted polarize codex --task 'marbles versus polarize skills: polarize them'
vc-polarize codex --task 'installer public contract'
vc-polarize claude --file /path/to/prism-pack.md
vibecrafted polarize agy --prompt 'Choose one launch thesis after marbles'
```

Gdy obecne jest `--task`, runner wykonuje świeży prism preflight i
dispatchuje agenta tylko dla pasm `pass` i `doctrine`:

```bash
loct prism --with-aicx \
  --task '<operator task>' \
  --task '<operator task> code truth' \
  --task '<operator task> product truth' \
  --json
```

`--with-aicx` jest domyślne. `--no-aicx` tylko wtedy, gdy wprost
potrzebujesz prism packu opartego wyłącznie na repo. `--no-context-corpus`
pomija opcjonalną emisję retention packu. **Żadnego `--count`.** To nie
jest kolejny silnik marbles.

---

## Doktryna pracy z repozytorium

W pracy z repozytorium zacznij od Loctree jako mapy: użyj `loct context`,
`loct occurrences`, `loct body` i `loct find --literal` przed szerokim
ręcznym przeszukiwaniem. Używaj AICX do kontekstu intencji i sesji. Używaj
rg/grep jako fallbacku lub lokalnej lupy, nie jako zamiennika mapowania
strukturalnego. Jeśli Loctree zawiedzie lub przeoczy jakąś powierzchnię,
dopisz feedback do `~/.vibecrafted/loctree/loctree-fail.md`.

## Cel

`vc-marbles` ustanawia **prawdę kodu (Code Truth)**, pytając _„co jest
wciąż technicznie fałszywe, kruche albo nieprzetestowane?"_ — jego swarm
(rój) produkuje celowe nadmiarowe aplikowanie w każde pęknięcie.

`vc-polarize` ustanawia **prawdę produktu (Product Truth)**, pytając
_„który jeden koncept albo która granica produktu powinna teraz stać się
autorytatywna?"_ — zdziera nadmiar do jednej osi i wyrównuje powierzchnie.

Zadanie to skolapsowanie niejednoznaczności do jawnego kontraktu:

- jedna granica
- jeden owner
- jedna ścieżka dowodu runtime'u
- jedna prawda artefaktu / raportu
- jedna publiczna obietnica, gdy koncept dotrze do użytkowników
- jawnie odrzucone alternatywy

Ten skill **pisze kod** — ale tylko po to, by wyrównać powierzchnie do
wybranej prawdy. Nie wymyśla nowych powierzchni. Tnie.

---

## Kiedy używać

Użyj `vc-polarize`, gdy:

- wynik `loct prism` ląduje w paśmie `pass` (9..12) albo `doctrine`
  (13..15)
- `vc-marbles` się zbiegł, ale pozostaje wiele wykonalnych prawd
- koncept albo powierzchnia produktu jest rozmazana po runtimie, testach,
  docs, artefaktach i publicznym copy
- release jest zablokowany, bo publiczne powierzchnie sobie przeczą

**Nie** używaj tego skilla, gdy:

- wynik prism to `abort` (0..4) — stop, żadnego polarize
- wynik prism to `memo` (5..8) — wyemituj tylko lokalne memo, bez dispatchu
- kod jest wciąż technicznie fałszywy / kruchy — to `vc-marbles`
- spec wymaga tylko weryfikacji, nie selekcji — to `vc-audit`

---

## Pozycja w pipelinie

`vc-polarize` to krok WRITE typu **decydujące cięcie**:

```
... → marbles (WRITE: excess) → audit (READ) → [POLARIZE: WRITE: cut] → dou (READ) → ...
```

Marbles produkuje nadmiarowo zaaplikowaną powierzchnię. Audit weryfikuje,
co wylądowało. Polarize zdziera do jednej osi.

---

## Słownik podstawowy

Definiuje **Code Smear** (rozsmarowanie tworzące konkurencyjne prawdy), **Prism Score** (załamanie konceptu w `loct context --task` — nigdy awaria CI ani kara za liczbę plików) oraz **Polaryzację** (zbieżność runtime'u, testów, docs, artefaktów i powierzchni publicznych na jednej osi). Pełne definicje w [references/concepts-and-modes.md](references/concepts-and-modes.md).

---

## Tryby

- **Tryb konceptu (Concept Mode)** — rozmazany koncept architektoniczny/runtime'u → jeden kontrakt konceptu i ścieżka dowodu.
- **Tryb produktu (Product Mode)** — rozmazana powierzchnia produktu/publiczna → jedna teza produktu i handoff DoU / release.

Pełne przykłady i zakres w [references/concepts-and-modes.md](references/concepts-and-modes.md).

---

## Pasma Prism Score

Oceń każdą oś 0..3 (Spread, Runtime Centrality, Authority Diversity,
Drift Risk, Closure Evidence). Suma 0..15.

| Pasmo    | Zakres wyniku | Działanie                                                              |
| -------- | ------------- | ---------------------------------------------------------------------- |
| abort    | 0..4          | Stop przed dispatchem agenta. Pokaż ścieżkę prism JSON.                |
| memo     | 5..8          | Wyemituj lokalne memo + cienki przykład context-corpus. Bez dispatchu. |
| pass     | 9..12         | Uruchom pełny przebieg polarize z wstrzykniętym payloadem prism.       |
| doctrine | 13..15        | Uruchom pełny przebieg doctrine z oczekiwaniem regression-contract.    |

Pełne kryteria osi, cykl życia, bramki i kontrakt context-corpus żyją
w [`PROCEDURE.md`](PROCEDURE.md).

---

## Kontrakt wyjścia

Zapisz artefakty w `$VIBECRAFTED_HOME/artifacts/<org>/<repo>/<YYYY_MMDD>/polarize/` (`thesis.md`, `concept-contract.md`, `surface-map.json`, `decision-ledger.md`, `dou-handoff.md`, `release-brief.md`) lub zawrzyj 11 obowiązkowych sekcji raportu (od `Polarized Thesis` do `Release Handoff`) we wstrzykniętym raporcie. Pełny układ i lista sekcji w [references/output-and-anti-patterns.md](references/output-and-anti-patterns.md).

---

## Złożenie z sąsiednimi skillami

Wymaga `vc-init` i upstreamu `vc-marbles`, konsumuje macierz verdictów `vc-audit` przy rozstrzyganiu twierdzeń UNVERIFIED i emituje handoffy dla `vc-dou` oraz `vc-release`. Szczegóły złożenia w [references/output-and-anti-patterns.md](references/output-and-anti-patterns.md).

---

## Antywzorce

Nie uśredniaj dwóch wykonalnych osi, nie dispatchuj na pasmach `abort` / `memo`, nie rozszczepiaj grupy odbiorców, nie zmieniaj copy bez dowodu z runtime'u, nie traktuj starych context packów jako żywej prawdy kodu i nie przechodź dalej do DoU/hydrate/decorate/release bez prośby operatora. Pełna lista w [references/output-and-anti-patterns.md](references/output-and-anti-patterns.md).

---

## Warunek zakończenia

Po przebiegu polarize:

- teza napisana, jedno zdanie
- odrzucone alternatywy zapisane z uzasadnieniem
- powierzchnie wyrównane tam, gdzie dowód z runtime'u wspiera wybraną oś
- bramki zielone dla dotkniętych powierzchni
- handoffy DoU + release napisane

Stop. Nie kontynuuj w DoU, hydrate, decorate ani release, chyba że
operator wprost poprosił o ten łańcuch.

---

## Wezwanie do działania

Przeczytaj [`PROCEDURE.md`](PROCEDURE.md) przed pierwszym przebiegiem
polarize — niesie pełny cykl życia, szczegół punktowania osi pryzmatu,
kontrakt context-corpus i listę minimalnych bramek. Potem uruchom
prism preflight, sprawdź pasmo i dispatchuj tylko dla `pass` /
`doctrine`.

---

## Klamra końcowa

```text
=======================
Pamiętaj: tryb polarize to pozwolenie na wybranie jednej prawdy, nie
pozwolenie na wymyślanie nowych. Zalew marbles jest twój do zdarcia,
nie do rozszerzania. Jedna teza, odrzucone alternatywy nazwane, powierzchnie
wyrównane, bramki zielone. Stop na handoffie.
( •̀ω•́ )✧
=======================

Suchar: Dlaczego polarize nigdy nie uśrednia dwóch prawd? Bo średnia
z dwóch gwiazd to pył.  (._.)
```

---

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
