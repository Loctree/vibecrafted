# vc-dispatch — Kontrakty brzegowe i pętla wykonania

## Boundary contracts

Aktualne `AGENTS.md` i `docs/public/dispatch/dispatch-schema.md` mają pierwszeństwo
przed historycznymi poradami, gdy rozchodzą się substrat, ownership, journale lub
semantyka zgód.

- **Wejście**: briefy + tracker z upstreamu (vc-scaffold / nadrzędny workflow)
  — ALBO, w **szybkiej fali** (`references/waves-and-recovery.md`), napisane przez dispatchera w sesji z
  żywych ustaleń. Wracaj do scaffoldu tylko przy nieukształtowanej pracy;
  Founder zarządzający falę na posiadanych już dowodach to inny przypadek.
- **Wyczuwanie kontekstu**: skill nie niesie kanonicznego szablonu promptu.
  Przed układaniem promptów wyczuj skill nadrzędny, repo CLAUDE.md / AGENTS.md,
  evidence vc-init i istniejące artefakty planu; sprawdź pokrycie odwrotną
  checklistą (`references/prompt-checklist.md`).
- **Wyjście**: ograniczone commity i raporty workerów, receipty verifierów
  supervisora, stan trackera i jawny integration disposition. Izolowana dostawa
  nie jest admission do Living Tree. Wyznaczony integrator dowodzi ancestry,
  tożsamości merge-parent lub dokładnej patch equivalence i ponownie sprawdza
  drzewo docelowe. Workerzy uruchamiają skupione bramki; supervisor zadeklarowane
  verifiery. Szerokie bramki integracji należą do integratora. Formalny `vc-audit`
  uruchamia się na prośbę Foundera, nie przy każdym ograniczonym dispatchu.
- **Journal i artefakty**: tylko Operator dopisuje istotne decyzje do
  `<repo-root>/.vibecrafted/THE_JOURNAL.md` (ignored, prywatny, nigdy commitowany).
  Workerzy zwracają raporty, nie wpisy journala. Plany, briefy, trackery i raporty
  żyją pod `${VIBECRAFTED_HOME:-$HOME/.vibecrafted}/artifacts/<org>/<repo>/<YYYY_MMDD>/`.
  Używaj `VIBECRAFTED_REPORT_PATH` od launchera; zachowaj maszynowe `run_id` i
  `session_id` oraz uczciwy status raportu.

## The loop

```
pre-flight → DISPATCH → SPANKO → SPRAWDZENIE → FLIP → BATON → next cut
                ↑           |  (pulse ticks; stall → recovery-dispatch)
                └── refire ←┘  (partial delivery / convergence pressure)
```

**Pin modelu per cut (pre-flight):** każdy cut deklaruje pin `model` zgodny ze
swoją klasą — cut mechaniczny, w pełni rozpisany, jedzie na tańszym,
szybszym tierze; cut chirurgiczny albo niosący decyzje — na mocniejszym
tierze. Pin jedzie z planem do launchera (`Cut.model` →
`WorkflowLaunchSpec.model` → flaga modelu agenta: `--model` dla claude i
cursor, `-m` dla codex). Cut bez pinu leci na defaulcie
konta — a to NIE-decyzja, nie bezpieczny default: pinuj świadomie, a brak
pinu traktuj jako smell do rozwiązania przed startem.

1. **Pre-flight (raz na linię)**: testuj komendy verify z briefów przed startem;
   bramka pasująca do 0 testów jest trywialnie zielona; żądaj ≥1 nowego
   nietrywialnego testu w EXTRA. `grep -c` zwraca 1 przy 0 trafień (`|| true`);
   licz WSZYSTKIE linie `test result:` (wiele binarek — `tail -1` kłamie);
   `cargo test` bierze JEDEN filtr pozycyjny. Dla pytest dowiedź niepustej
   selekcji `-k` (`--collect-only -q` ≥1); preferuj **sondy semantyczne**, które
   dziś drukują STARĄ wartość, a NOWĄ dopiero po cięciu — uruchom je w pre-flight.
   Dla linii `.dispatch.toml`: `--doctor` → sonda/collect → `--dry-run` z bramką
   placeholderów wyrenderowanych promptów → launch. Pełne reguły z pola:
   `references/toml-plan-preflight.md`.
2. **Dispatch**: jeden plik promptu (nigdy argv — publiczne `ps`, ARG_MAX,
   połamane nowe linie), cztery warstwy checklisty. Launch:
   `bash -c 'ulimit -f unlimited; vibecrafted <skill> <agent> --model <pin> --file <p.md>'`
   (shelle mogą nieść miękki `ulimit -f` → SIGXFSZ/exit 153). **Domyślnie headless:**
   workerzy CLI i MCP działają w odłączonej sesji procesu nawet przy żywej vc-frame
   User Session. Obserwuj przez stan runu, transcript, `observe` i `await`;
   zakładka vc-frame może projektować te powierzchnie, ale nie posiada procesu
   workera. `--runtime terminal` / `runtime="visible"` wyłącznie przy jawnym
   wyjątku TTY providera, z kosztem sprzężenia workera z terminalem. Zapisz receipt
   (run_id, report, transcript, meta) w trackerze.
   Nigdy cicho nie podmieniaj pinu modelu Foundera. Headless Worker kończy bramki
   na pierwszym planie, pracę, raport i commit w bieżącej turze; zakończenia w tle
   nie mogą go wybudzić. Await po stronie supervisora to osobna rola.

3. **Spanko**: czekaj przez artefakty, nigdy przez gapienie się w pane. Użyj
   dedykowanej komendy jako standardowej pętli dyspozytora. Kanoniczny kontrakt
   supervisora (zobacz `docs/runtime/AGENT_OPS.md`): po dispatchu uzbrój
   `vibecrafted await <agent> --run-id <id>` natychmiast, po stronie supervisora.
   JSON control-plane, pliki raportów, transkrypty, karty terminala i
   zaplanowane wybudzenia są wyłącznie diagnostyczne, nie są sygnałem
   wybudzenia. Hedge'owanie await ad-hoc pollerami/watcherami to naruszenie
   Class 3; napraw `control_plane.await_run`, nie normalizuj hedge'u.
   Liveness jest zawsze 3-sygnałowy: przed "done" pogódź await verdict,
   terminalny stan w run meta i martwy worker pid; gdy raport jest obiecany,
   sprawdź obecność raportu. Dwa zgodne sygnały wystarczą do działania, trzy do
   deklaracji done; rozjazd = traktuj jako live i uzbrój await ponownie. Znany
   skew: rc=0-on-live oraz meta `active`/`stalled` po realnym zakończeniu.
   `vibecrafted loop spanko --run-id <id> --agent <a> --verify '<cmd>' --tracker <tracker.md> --cut-id <cut> --then '<next dispatch>'`
   (heartbeat cron frameworka → control-plane await → sprawdzenie → flip → baton),
   niższopoziomowego `vibecrafted loop await-run --run-id <id> --agent <a> --then-cmd '<next>'`,
   albo probe await-watch
   (`vibecrafted-await-watch.sh --meta <meta.json>` — tail-await-die) jako
   warstwy widoczności podporządkowanej kanonicznemu await. Żywy worker dostaje
   ZERO ingerencji; przerywanie mu w fazie bramki to czysta strata.
4. **Sprawdzenie** (po wyjściu workera): SHA commita istnieje → esencja diffa
   odpowiada briefowi → odczytane bramki i acceptance z raportu → uruchomione
   zadeklarowane verifiery supervisora. Unikaj przypadkowych powtórnych buildów;
   raport workera lub wynik hooka nie zastępuje wymaganej niezależnej weryfikacji.
5. **Flip**: `[~]→[x]` tylko przez dispatchera (jeden zapisujący), evidence =
   SHA + receipty verifierów + kto zweryfikował + integration disposition.
   Pola Acceptance workera są claimem; nigdy nie podpisują za Operatora ani
   Foundera. Source-green nie jest installed/live acceptance. Zasady ledgera:
   `references/ledger.md`.

6. **Baton**: prompt kolejnego cięcia niesie stan linii — które cięcia wylądowały,
   które commity, które pliki się przesunęły, co następny worker musi przeczytać ponownie.

## Regeneracja Skill Provenance

Zmiany bajtów skillów wymagają regeneracji `skills/SKILL_PROVENANCE.json` przez
`make skills-check UPDATE=1`; tracked owner to `scripts/gen_skill_provenance.py`.
Zachowaj historyczne wpisy. Szanuj cut właściciela generatora; konsumuj jego
przyjętą zależność bez edycji kodu. Po admission integrator regeneruje wspólny
manifest raz, zamiast brać manifest siostrzanego workera w całości.
