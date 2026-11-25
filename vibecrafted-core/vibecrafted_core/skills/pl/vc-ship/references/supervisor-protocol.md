# `vc-ship` — Protokół nadzorcy i czasowniki cyklu życia

## Jak lecieć (protokół nadzorcy)

1. **Najpierw misja.** Ułóż misję jako trwały plik `.md` pod
   `~/.vibecrafted/artifacts/<org>/<repo>/<date>/plans/` — osadzoną w
   prawdziwym przebiegu vc-init (atlas Loctree + intencje AICX + prawda o
   git/ryzyku), z jawnymi deliverables, twardymi ograniczeniami i bramkami.
   `--file` dostarcza ją verbatim każdemu workerowi etapu.
2. **Odpal** standardowym launcherem powyżej. Zweryfikuj potwierdzenie startu:
   run_id (`life-ship-…`), wczytany atlas kontekstu, etap 1 przyjęty.
3. **Uzbrój await natychmiast, po stronie nadzorcy** (nigdy wewnątrz subagenta —
   patrz `docs/runtime/AGENT_OPS.md`): po dispatchu uzbrój
   `vibecrafted await <agent> --run-id <id>` natychmiast, po stronie nadzorcy.
   JSON control plane'u, pliki raportów, transcripty, pane'y i zaplanowane
   pobudki są wyłącznie diagnostyczne, nie są sygnałem wybudzenia.
   Asekurowanie awaita doraźnymi pollerami/watcherami to naruszenie klasy 3;
   napraw `control_plane.await_run`, nie normalizuj asekuracji. Sprawdzanie
   raportów etapów i `ship status --json` to diagnostyka podporządkowana temu
   kanonicznemu awaitowi; `ship status --json` wystawia `stage_worker` z
   `worker_dead_without_report` — sygnał śmierci, na który da się zareagować;
   dispatcher zapisuje też `worker_exit` / `stage_worker_exit` do `state.json`
   po stronie push, gdy worker umiera.
   Żywotność na 3 sygnałach: zanim ogłosisz zakończenie, uzgodnij werdykt
   awaita, meta runu z terminala i martwy pid workera; jeśli obiecano raport,
   potwierdź, że istnieje. Dwa zgodne sygnały wystarczą do działania, trzy do
   ogłoszenia końca; niezgodność oznacza „traktuj jak żywy" i ponowne uzbrojenie
   awaita. Znany rozjazd: rc=0 przy żywym oraz meta zawieszona na
   `active`/`stalled` po faktycznym zakończeniu.
4. **Weryfikuj przed każdym guzikiem.** Przeczytaj raport; dla etapów WRITE
   potwierdź, że commity i bramki naprawdę istnieją; dla etapów READ potwierdź
   brak `read_phase_violation`. Uszanuj sterowanie workera z frontmattera
   raportu (`next_stage`, `next_agent`, `dou_index`), chyba że to bzdura —
   wtedy nadpisz czasownikiem.
5. **Steruj czasownikami, nigdy ręczną operacją na stanie:**

   ```bash
   vibecrafted ship runs                       # list lifecycle runs
   vibecrafted ship status <run_id> --json     # truth before any button
   vibecrafted ship approve <run_id>           # baton → next stage (cargo-gated)
   vibecrafted ship approve <run_id> --force   # traced override of the cargo gate
   vibecrafted ship interrupt <run_id>         # stop a blind/dead continuation
   vibecrafted ship fallback <run_id> --stage <s>  # rewind the baton WITH cargo
   vibecrafted ship force-audit <run_id>       # suspicious WRITE output
   vibecrafted ship accept-dou <run_id> --finding "…"  # conscious, traced gap
   ```

   Odzyskiwanie martwego workera zawsze wygląda tak: `interrupt` →
   `fallback --stage <stage>` → `approve [--force]`. Żaden ładunek pałeczki nie
   ginie.

6. **Raportuj na końcu, nie po drodze** (chyba że operator prosi inaczej):
   przelecione etapy, wprowadzone korekty, commity, kolory bramek, dou_index
   oraz to, czego release uczciwie NIE zweryfikował.
