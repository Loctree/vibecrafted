---
name: vc-trust
version: 1.0.0
description: >
  Post-hoc falsification of commit claims on a Living Tree, including agent
  fairness (Authored-By matches subject agent; no vendor footers; no foreign
  envelope lies) and completeness claims. Produces pass, pass-with-gaps, or
  block verdicts, appends evidence to the trust journal, and projects explicit
  verdicts onto the canonical f/x/n settlement axis. Trust observes and judges;
  it never blocks dispatch or mutates code. Enforcement is vc-guard.
loctree_value: "commit scope, consumers, blast radius, and runtime paths"
aicx_value: "why the commit exists and which prior attempts shaped it"
dogfooding: "required"
---

# vc-trust — sędzia po fakcie

`vc-trust` to spokojny sędzia po fakcie dla commitów zrobionych na wspólnym
Living Tree lub jawnie wskazanego fleet-worktree. Wiadomości commitów są
hipotezami. Trust falsyfikuje ich claimy
wobec diffu, konsumentów, testów, runtime'u i historycznej intencji, zanim
wyda:

- `pass` — każdy materialny claim przetrwał falsyfikację **z mocnym evidence**
  (sama legalność formatu/trailerów nigdy nie wystarcza).
- `pass-with-gaps` — rdzeń claimu przetrwał, ale zostają nazwane luki w evidence
  albo w pokryciu.
- `block` — materialny claim jest fałszywy, zaprzeczony, niebezpieczny albo nie
  jest w stanie sprostać wymaganemu progowi evidence (łącznie z naruszeniami
  agent fairness).

### Agent fairness (pierwszorzędna oś claimów)

Przy każdym commicie traktuj co najmniej te rzeczy jako materialne claimy:

1. Subject pasuje do `[<agent>/<runtime>] <type>: …`.
2. `Authored-By: <agent> <agents@vetcoders.io>` jest obecne i **równa się**
   agentowi z subjectu (Agent Fairness — autentyczność wykonawcy).
3. Brak vendorowych `Co-Authored-By` / `noreply@` / vendorowych maili.
4. Przed trailerami istnieje wyjaśniające body (kształt jest konieczny, nie
   wystarczający).
5. Koperta commita wymienia prawdziwe pliki; niezapracowane „done/fixed" bez
   nazwanych testów/bramek to luka, nie pass.

Ekstraktory mechaniczne:

```bash
python -m vibecrafted_core.trust inspect <sha>
```

Inspect nigdy nie notuje automatycznie i nigdy nie sugeruje passa. Journal i
settlement zapisuje wyłącznie jawne `note`.

Mapowanie na settlement jest zamknięte i kanoniczne (nie otwieraj liter na
nowo):

| Werdykt trustu   | Settlement      | TUI |
| ---------------- | --------------- | --- |
| `pass`           | Finalized       | `f` |
| `pass-with-gaps` | Needs attention | `n` |
| `block`          | Failed          | `x` |

## Checkpoint orientacji

Zanim zbadasz, osądzisz albo zanotujesz commit, uruchom lub skonsumuj procedurę
`vc-init` dla przypisanego repozytorium. Ustal repozytorium, branch, baseline,
zakres review, stan dirty i ścieżkę trust journala. `trust inspect` to
mechaniczny ekstraktor, nie zamiennik tej orientacji, i nigdy nie jest
wystarczającym evidence pod werdykt.

Użyj `Loctree:loctree`, żeby wyprodukować lub odświeżyć Code-Derived Application
Map dla recenzowanego zakresu: zmienione pliki, konsumenci, entrypointy
runtime'u, testy, twinsy i zasięg zmiany. Sięgaj po `slice`, `impact`, `find` i
`follow` tam, gdzie wymaga tego dany claim, a potem niezależnie obejrzyj diff i
prawdziwą ścieżkę runtime'u. Mapa ogranicza falsyfikację; nie przyznaje zaufania.
Trust pozostaje read-only wobec kodu i pisze wyłącznie po jawnych powierzchniach
journala/settlementu wymienionych niżej.

## Wywołanie

- Worker: `vibecrafted trust <claude|codex|agy|junie|grok|cursor|kimi|copilot|omp> --prompt ...`
- Interactive: `/vc-trust`
- Linia operatora: `vibecrafted trust <agent> --file <brief.md>`

Ustrukturyzowany helper to:

```bash
python -m vibecrafted_core.trust --help
```

## Twarda granica

Trust jest READ-only wobec repozytorium. Może pisać wyłącznie:

- append-only trust journal;
- jawny trust settlement na istniejącym runie;
- zawężoną projekcję control plane'u dla tego samego runu;
- swój raport i transcript.

Trust nigdy nie edytuje kodu, nie amenduje ani nie rewertuje commitów, nie
blokuje dispatchu, nie pushuje i nie merguje. Egzekucja należy do `vc-guard`
(inwentarz bramek + odmowa przy trust `block`). Nie implementuj tu zachowania
guarda.

Po pauzy, stopy, operator buttons i granice autonomii idź do
[`vc-operator/AUTONOMY.md`](../vc-operator/AUTONOMY.md); nie forkuj tego
kontraktu.

## Protokół

1. **Orientacja i enumeracja** (`vc-init`, Loctree, AICX, `enumerate <author> --since ...`).
2. **Zamiana prozy na falsyfikowalne claimy** (testy, ścieżka runtime'u, fail-closed, zakres diffu).
3. **Ocena evidence per claim** (`strong` / `medium` / `weak`; słabe nigdy nie daje materialnego passa).
4. **Falsyfikacja** przez Loctree `slice`/`impact`/`find`/`follow`, diff i ponowne uruchomienie bramek (`vc-trust` osądza strumień commitów na żywym drzewie; odrębny od `vc-review` i `vc-audit`).
5. **Zapis werdyktu** przez jawne `note <sha> <verdict> --claim ... --grade ... --evidence ...` (`$VIBECRAFTED_HOME/trust/journal.jsonl`).
6. **Await i triage** przez `await-primary` (nigdy `guard=await`) oraz `triage` (liczniki `f/x/n`).

Pełne komendy, definicje skali i flagi journala: [references/protocol.md](references/protocol.md).

## Kontrakt raportu

Raport końcowy musi zawierać:

- branch/HEAD baseline'u i recenzowany zakres commitów;
- macierz claimów z oceną evidence i dokładnymi komendami/artefaktami;
- jeden werdykt per commit oraz zbiorczy wynik na poziomie runu;
- ścieżkę journala i rezultat zapisu settlementu;
- weryfikacje wykonane i niewykonane;
- luki resztkowe i następny bezpieczny ruch.

Nigdy nie mów „zaufane", nie pokazując, który claim został zaatakowany i co
przetrwało.
