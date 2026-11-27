# vc-dispatch — Szybka fala, refire, cadence, puls i wzorce porażek

## Fast wave (blitz) — Founder-ordered bounded dispatch

Gdy Founder wskazuje N zweryfikowanych ustaleń i zarządza falę („dispatchuj
falę na te pakiety”, „blitzkrieg, nie partyzantka”), dispatcher JEST autorem
briefów. Nie kieruj przez vc-scaffold, nie buduj DRIVERA, nie odpytuj rundami —
ustalenia z dowodami są planem.

Kształt (polowo sprawdzony, loctree-suite findings-wave-2, 2026-08-22):

1. **Pre-flight zostaje**: świeży baseline SHA (fetch — HEAD przesuwa się między
   twoją diagnozą a rozkazem), rozłączne domeny plików per cięcie, regiony
   plików współdzielonych zadeklarowane jawnie w briefach, wiszące siostrzane
   gałęzie wymienione jako do-not-touch.
2. **Zwięzły brief per cięcie**, pisany przez dispatchera w minuty, nie godziny:
   frontmatter + misja + dowody verbatim (komendy repro, kotwice linii) +
   pliki + akceptacja (≥2 nietrywialne testy) + bramki + poza-zakresem +
   blok substratu + zasady commit/trailer + ścieżka raportu + klauzula
   idempotencji. Checklist a min z pola: `references/fast-wave-brief.md`.
3. **Piny Foundera jadą dosłownie**: agenci i modele nazwane przez Foundera
   (`gpt-5.6-sol | grok-4.6 | claude-opus-5`) idą wprost do flag `--model`
   launchera i do tabeli trackera. Żadnych cichych podmian.
4. **Wszystkie cięcia startują równolegle**, awaity uzbrojone natychmiast
   supervisor-side, zwięzły tracker (cięcie | worker@model | run_id | gałąź | stan).
5. **Dispatcher integruje**: jednowątkowo, po osadzeniu, po diffach — szybka
   fala zmienia autorstwo briefów, nigdy rygor SPRAWDZENIE/FLIP.

Szybka fala to nadal linia: tracker, evidence ledgera, zadeklarowane verifiery
oraz receipty integracji pozostają wymagane. Domknij ograniczoną acceptance,
bez twierdzenia, że cały lifecycle został ukończony.

## Refire = mini-marbles

Ponowne uruchomienie TEGO SAMEGO promptu (vc-frame: `<ENTER> re-run` na pane spawnu, albo
re-launch `--file` z tą samą ścieżką) to najtańszy prymityw zbieżności
— gorące podłoże, worker płaci mniej za archeologię i wydaje
budżet na delty (vc-marbles: „Marbles exploits cache heat").

- **Warunek wstępny**: briefy muszą być IDEMPOTENTNE — napisane tak, że re-run na drzewie,
  gdzie praca już wylądowała, weryfikuje i zatrzymuje się („nothing to do"), nigdy
  nie duplikuje.
- **Używaj refire, gdy**: task może być za wielki na jedną rundę workera; raport
  mówi, że pod-element nie został zrobiony; chcesz presji zbieżności w stylu marbles
  na kruchej powierzchni.
- Preferuj dispatch przez launcher nad pracą inline właśnie DLATEGO, że refire sprawia,
  że częściowy postęp jest kumulatywny.

## Read/Write cadence

- Odczyty (puls, artefakty, loct) są tanie i ciągłe; zapisy dzieją się na
  granicach pętli: tracker/journal po każdym przejściu, pliki promptów przed
  dispatchem, własne commity natychmiast (jedna jednostka = jeden commit, ukształtowany przez hooka,
  z prawdziwym trailerem session_id).
- W trakcie fal: bez przypadkowych duplikatów lintów/testów przez dispatchera,
  bez przygodnych fixów w zakresie workera. Zadeklarowane verifiery i admission
  integratora rozliczają dostawę; formalny audyt na prośbę Foundera.
- Ręce dispatchera dotykają repo tylko dla księgowości linii, ograniczonych
  napraw bookkeeping przydzielonych wprost przez Foundera (wtedy własny commit
  obowiązkowy) i zbierania evidence recovery.

## Pulse & stall (hard rule, both postures)

Heartbeat jest FRAMEWORK-FIRST — mechanika loop/cron jest już zautomatyzowana
w vibecrafted; nie sklecaj ręcznie timerów, gdy te istnieją:

- `vibecrafted loop spanko --run-id <id> --agent <a> --verify '<cmd>'
--tracker <tracker.md> --cut-id <cut> --then '<next dispatch>'` — komenda
  rangi dyspozytorskiej dla pętli await: SPANKO → SPRAWDZENIE → FLIP → BATON;
- `vibecrafted loop start|next|status|complete` — maszyna stanów linii z
  `--max-iterations` i `--completion-promise`;
- `vibecrafted cron line --root <repo> --every-minutes 10 --then-cmd
'vibecrafted loop next'` — heartbeat na prawdziwym crontabie, który łapie kontekst Loctree +
  AICX na każdy tick;
- `vibecrafted cron tick --after-idle-minutes 10 --then-cmd <cmd>` — wznawia
  zatwierdzoną następną komendę po oknie bezczynności.

Prowadź await dedykowaną komendą (NASZ vc-loop / cron) jako STANDARD nawet z
sesji interaktywnej — dispatchowany run MA CLI. Harness `/loop` to prawdziwy
last-resort, tylko gdy CLI vibecrafted jest faktycznie niedostępne.

Na każdym ticku oceniaj liveness po trzech niezależnych sygnałach wg
`references/pulse-and-stall.md`: status control-plane, mtime+rozmiar pliku sesji
agenta, delty `git status`. **≥10 min ciszy na wszystkich trzech → zabij
drzewo launchera, sprawdź proces osierocony (orphan) (orphan często DOWOZI), potem
recovery-dispatch z evidence wpisanym w aktualizację BATON** —
możliwie inny agent. Nigdy ślepy restart; nigdy kill na jednym sygnale
(sygnał matchujący znaną awarię ≠ ta awaria).

## In-flight corrections

Founder obala politykę dowiezionego cięcia w trakcie linii → napisz brief
korygujący (sufiks `b`, np. C2→C2b), zakolejkuj go z poszanowaniem nakładań plików, ponieś
decyzję Foundera wiernie co do ducha w BATON. Mechanika starego
cięcia zostaje; korygowana jest tylko polityka. Findingi po linii (smoke bugi,
życzenia featurowe) idą do pliku backtrackera z kotwicami w prawdzie kodu, stają się
cięciami backlogowymi na guzik Foundera.

## Failure patterns (do not repeat)

- Prompt w argv; nierenderowane placeholdery. Bramkuj **znane tokeny placeholderów**
  (`grep -E '\{(repo|id|agent|workflow|resolved_workflow|reports_dir|tracker|baton)\}'`
  na promptach dry-run, oczekuj pustego wyniku). Naiwne `grep -c '{'` daje false
  positive na wyrenderowanym JSON `{baton}`, który legalnie niesie klamry
  (zobacz `references/toml-plan-preflight.md`).
- Zabicie supervisora ścigającego własną pętlę — sprawdź dzieci `ps` i
  `git log` po fakcie; orphan często dowozi.
- Heredoc Foundera wpisany w chat zamiast w shell — zweryfikuj, że plik istnieje,
  zanim się do niego odwołasz.
- Re-run bramek workera „dla pewności" — claim kontra proof zostaje ustalony przez SHA +
  hooki + warstwę audytu, nie przez twój zduplikowany build.
- Traktowanie rąk kolegi z zespołu w „twoim" pliku jako zagrożenia — na Living
  Tree zlądowany commit należy do linii, nie do ciebie; rozjazd między rundami jest
  sygnałem dla vc-polarize, nie szkodą.
