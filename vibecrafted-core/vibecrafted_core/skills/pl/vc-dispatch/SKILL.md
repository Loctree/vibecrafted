---
name: vc-dispatch
description: "Operate external Vibecrafted fleet lines with prompt assembly, await/observe, reports, and recovery."
---

<!-- fleet-imperative: v3 -->

> **Wywołanie dla `vc-dispatch` (launcher `dispatch`)**
>
> Ten sam _kształt_ trzech ścieżek floty, z **literałami tego** skilla — zobacz
> kanoniczną [Matrycę Delegacji](../DELEGATION_MATRIX.md):
>
> - [Wspólne trzy ścieżki](../DELEGATION_MATRIX.md#shared-three-paths)
> - [Katalog launcherów](../DELEGATION_MATRIX.md#launcher-catalogue-core-runtime)
> - [Reguła per-launcher](../DELEGATION_MATRIX.md#per-launcher-rule-the-semantic-delta)
> - [Native vs external](../DELEGATION_MATRIX.md#native-subagents-vs-external-workers)
>
> | Ścieżka               | Literał tego skilla                                                                                                                                             |
> | --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | 1. Worker użytkownika | `vibecrafted dispatch …` / `vc-dispatch`                                                                                                                        |
> | 2. Interactive        | załaduj `vc-dispatch` (skill metody operatora) — wykonaj **w tej sesji**; native subagenty gdy trzeba; **nie** zewnętrzniaj tylko dlatego, że launcher istnieje |
> | 3. Agent-operator     | może odpalić formę workera powyżej przez `vc-dispatch` / linie operatora, zachowując tożsamość tego skilla                                                      |
>
> **Uwaga:** External fleet **dyspozytura** — runs lines/plans; does not become implement/workflow.

> Swobodniejszy native na niektórych biegach ≠ porzucenie floty external. `vc-dispatch` i `vc-ship` zachowują własne tożsamości.

<!-- /fleet-imperative -->

# 𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. Dispatch — the dyspozytura

**Jesteś dyspozytorem (rola vc-operator), NIE workerem.** Flota: zewnętrzni
agenci (codex, agy, …) launchowani przez launcher `vibecrafted`. Jeden mózg,
wiele rąk. Ten skill definiuje _metodę i rygor_ prowadzenia linii
cięć — nie posiada własnej fazy pipeline'u i można go wywołać z dowolnego punktu dowolnego
workflow.

`vc-ship` pozostaje normalną klamrą lifecycle. **Ograniczony dispatch zarządzony
przez Foundera** jest również wspieranym wywołaniem: prowadź ukształtowaną falę
napraw przez `vibecrafted dispatch <plan.dispatch.toml>`, z aktualną orientacją,
pełnymi briefami, doctor/dry-run, pinami modeli i verifierami. Nie wymaga to
jedenastu etapów lifecycle ani fikcyjnej wcześniejszej awarii `vc-ship`.
Przy konsumowaniu wyjścia scaffoldu zachowaj jego wymagania artefaktów,
DRIVER-a, manifestu i briefów.

## Posture

- Sesja interaktywna → **vc-partner**: opisuj Founderowi przejścia stanów,
  ujawniaj decyzje, przyjmuj korekty w locie.
- Sesja nieinteraktywna → **vc-ownership**: ta sama pętla, decyzje zapisane w
  journalu Operatora w autoryzowanym zakresie. Przyciski Foundera nadal obowiązują.
- W OBU postawach: stall-kill i recovery są autonomiczne, bez ceremonii (zobacz
  niżej). Odpowiedzialność za dostawę przebija uprzejmość wobec procesu.

## Boundary contracts

Aktualne `AGENTS.md` i `docs/public/dispatch/dispatch-schema.md` mają pierwszeństwo przed historycznymi poradami przy rozbieżnościach substratu, ownership, journali lub zgód:

- **Wejście**: briefy + tracker z `vc-scaffold` — albo zwięzłe briefy pisane przez dispatchera w **szybkiej fali**.
- **Wyczuwanie kontekstu**: wyczuj skill nadrzędny, `AGENTS.md`/`CLAUDE.md`, evidence `vc-init` i artefakty planu; sprawdź przez [references/prompt-checklist.md](references/prompt-checklist.md).
- **Wyjście**: ograniczone commity i raporty workerów, receipty verifierów supervisora, stan trackera i jawny integration disposition. Izolowana dostawa ≠ admission do Living Tree; wyznaczony integrator przyjmuje commity i uruchamia szerokie bramki.
- **Journal i artefakty**: tylko Operator dopisuje `<repo-root>/.vibecrafted/THE_JOURNAL.md`; trwałe artefakty żyją pod `${VIBECRAFTED_HOME:-$HOME/.vibecrafted}/artifacts/<org>/<repo>/<YYYY_MMDD>/` przez `VIBECRAFTED_REPORT_PATH`.

Pełne kontrakty brzegowe: [references/dispatch-loop.md](references/dispatch-loop.md).

## Canonical Orientation Gate

`vc-dispatch` wymaga aktualnego evidence z `vc-init`, zanim poprowadzi linię.
Żaden dyspozytor nie powinien odpalać workera, przekształcać fali ani flipować stanu trackera
ze stale pamięci repozytorium.

`Loctree:loctree` to domyślna warstwa percepcji strukturalnej dla tej
orientacji. Użyj jej, by wyprodukować lub odświeżyć Mapę Aplikacji Wyprowadzoną z Kodu (Code-Derived Application Map),
zanim zbudujesz kolejność fal, ułożysz briefy workerów, ocenisz nakładanie się plików albo
przyjmiesz baton z poprzedniego cięcia. Brak evidence z Loctree oznacza, że linia
jest ślepa, nie tylko słabo udokumentowana.

## Repository Work Doctrine

W pracy z repozytorium zacznij od Loctree jako mapy: użyj `loct context`,
`loct occurrences`, `loct body` i `loct find --literal` przed szerokim ręcznym
przeszukiwaniem. Używaj AICX do kontekstu intencji i sesji. Używaj rg/grep jako
fallbacku lub lokalnej lupy, nie jako zamiennika mapowania strukturalnego. Jeśli Loctree
zawiedzie lub przeoczy jakąś powierzchnię, dopisz feedback do `~/.vibecrafted/loctree/loctree-fail.md`.

## The loop

```
pre-flight → DISPATCH → SPANKO → SPRAWDZENIE → FLIP → BATON → next cut
                ↑           |  (pulse ticks; stall → recovery-dispatch)
                └── refire ←┘  (partial delivery / convergence pressure)
```

Każdy cut deklaruje jawny pin `model` zgodny ze swoją klasą (`--model` dla claude/cursor, `-m` dla codex); nigdy cicho nie podmieniaj pinu Foundera.

1. **Pre-flight:** udowodnij niepuste komendy verify (`--collect-only`, sondy semantyczne, `--doctor` → `--dry-run` z bramką placeholderów wg [references/toml-plan-preflight.md](references/toml-plan-preflight.md)).
2. **Dispatch:** jeden plik promptu (`--file <p.md>`, nigdy argv) pod `ulimit -f unlimited`; domyślnie headless, bramki na pierwszym planie + raport + commit w turze workera; zapisz receipt.
3. **Spanko:** natychmiast uzbrój po stronie supervisora `vibecrafted await <agent> --run-id <id>` (bez ad-hoc pollingu); pogódź 3 sygnały liveness (await verdict, terminalny stan meta, martwy pid + obiecany raport); zero ingerencji w żywego workera.
4. **Sprawdzenie:** potwierdź SHA commita, diff względem briefu, wyniki raportu i uruchom zadeklarowane verifiery supervisora.
5. **Flip:** pojedynczy zapis `[~]→[x]` wyłącznie na dowodzie verifiera (`references/ledger.md`); checkboxy workera są tylko claimem.
6. **Baton:** przenieś wylądowane commity, przesunięte pliki i nakaz ponownego odczytu do kolejnego promptu.

Pełne komendy pętli i reguły `SKILL_PROVENANCE.json`: [references/dispatch-loop.md](references/dispatch-loop.md).

## Fast wave (blitz) — Founder-ordered bounded dispatch

Gdy Founder zarządza falę na N zweryfikowanych ustaleniach, dispatcher sam pisze zwięzłe, idempotentne briefy (bez `vc-scaffold` i bez `DRIVER`), utrzymuje świeży baseline SHA, rozłączne domeny plików i dosłowne piny modeli Foundera, startuje równolegle z awaitami supervisora i integruje jednowątkowo po osadzeniu. Checklista min: [references/fast-wave-brief.md](references/fast-wave-brief.md); pełne zasady: [references/waves-and-recovery.md](references/waves-and-recovery.md).

## Parallel waves are an obligation

Gdy cięcia zajmują niezależne obszary kodu, MUSISZ zaplanować fale pod maksymalną
wieloworkerową równoległość — uruchamianie jednego workera naraz ze strachu przed konfliktem
jest przeciwwskazane. Sekwencjonuj WYŁĄCZNIE twarde nakładania plików (ten sam plik/region).

**Szanuj jawny substrat.** Wybór Foundera, planu lub launchera wygrywa:
Living Tree / `local-native`, Fleet Worktrees / `local-worktrees`, Fleet VM local
oraz Fleet VM cloud to osobne runtime'y. Nie przenoś workera dla wygody.
Pojedyncza interaktywna linia domyślnie używa Living Tree, jeśli nie wybrano
innego runtime'u.

Dla typowanego `.dispatch.toml` supervisor tworzy dedykowany worktree każdego
nie-integratora pod `${VIBECRAFTED_HOME:-$HOME/.vibecrafted}/worktrees/<org>/<repo>/<YYYY_MMDD>/<cut-id>`
na `cut/<cut-id>` z rozwiązanego baseline'u. `{repo}` jest efektywnym rootem
workera. Workerzy go dziedziczą; nie tworzą drugiej gałęzi ani worktree, nie
piszą w checkoucie nadrzędnym i nie integrują siebie. `depends_on` porządkuje
czas; `base = "cut:<cut-id>"` dostarcza ancestry poprzednika, gdy jest potrzebna.
Tylko wyznaczony integrator przyjmuje commity. Zobacz
`docs/public/dispatch/dispatch-schema.md`.

W każdym runtime czytaj ponownie przed edycją i stage'uj wyłącznie własne ścieżki
lub hunki: `git add -- <owned-path>` (albo selekcja hunków). Nigdy `git add -A`,
`git add .`, stash, discard ani commit cudzej pracy. Jeśli overlap uniemożliwia
uczciwą izolację, zachowaj diff i zgłoś substrate failure.

Zapisuj runtime class, parent/effective roots, baseline branch/full SHA, worker
branch/tip, artefakty, integration disposition i sprawdzony stan celu.
Fast-forward push feature brancha po własnym commicie jest dozwolony przez
Charter, chyba że bieżąca fala go zabrania. Trunk merge, force-push, PR merge/close,
kasowanie tagów/gałęzi i deploy pozostają przyciskami Foundera.

Regeneracja `skills/SKILL_PROVENANCE.json`: [references/dispatch-loop.md](references/dispatch-loop.md).

## Refire, Cadence, Pulse & Corrections

- **Refire = mini-marbles:** ponowne odpalenie tego samego idempotentnego promptu `--file` wykorzystuje cache heat do kumulatywnych delt.
- **Read/Write cadence:** odczyty ciągłe; zapisy na granicach pętli (tracker/journal/prompty/commity; bez duplikatów lintów i przygodnych fixów w zakresie workera).
- **Pulse & stall:** używaj `vibecrafted loop spanko` / `loop` / `cron` jako standardu (`/loop` tylko ostatecznie). Oceniaj 3 sygnały liveness wg [references/pulse-and-stall.md](references/pulse-and-stall.md); ≥10 min ciszy na wszystkich trzech → zabij drzewo launchera, sprawdź orphany, recovery-dispatch z evidence w BATON.
- **Korekty w locie i wzorce porażek:** kolejkuj cięcia korygujące (`C2b`), bramkuj znane tokeny placeholderów (nie naiwne `grep -c '{'`), nie przekazuj promptu w argv ani nie powtarzaj bramek workera „dla pewności". Pełne zasady: [references/waves-and-recovery.md](references/waves-and-recovery.md).

## Dependencies

Semantyka delivery-proof żyje w `vibecrafted_core.delivery`; zobacz
`docs/runtime/DELIVERY_PROOF_KERNEL_v1.md`.
`vc-marbles` · `vc-scaffold` · `vc-init` · `vc-followup` / `vc-audit` / `vc-dou` · `vc-polarize` · `Loctree`.

---

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
