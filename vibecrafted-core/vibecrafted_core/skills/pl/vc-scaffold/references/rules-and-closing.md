# vc-scaffold — Krytyczne reguły, zamknięcie Emila, antywzorce i weryfikacja

## Critical Rules

- **Research-first to hard-block, nie poprawka.** Żadnego planu z pamięci; wyprowadź z prawdy repo/runtime.
- **Wywiad z founderem albo dowód — bez samowyłączenia.** Wskaż journal/AICX/brief z decyzjami
  foundera albo zapytaj przed Shape.
- **Brief na każde cięcie — bez wyjątków.** Briefy per cięcie to hard-gate (Faza 5). Plan,
  którego cięcia nie mają briefów, to wydmuszka; scaffold-doctor odmawia przekazania.
- **DRIVER.md — bez wyjątków (Faza 5.5).** Driver przekazania Foundera (pełne ścieżki · graf z adnotacją
  why · gotowe komendy · reguła `[ ]→[x]` verbatim · snapshot statusu · matryca odbioru) jest częścią
  bramki scaffold-doctor. Plan, którego człowiek nie poprowadzi z jednego pliku, gdy pętla umrze, nie
  jest gotowy do przekazania.
- **Każde wymaganie startuje `[ ]`, a plan zamykają trzy podpisy (R12, Founder 2026-09-15).**
  Bullety Acceptance i pola matrycy startują jako `[ ]`; worker przerzuca własne pola w ramach
  dostawy, supervisor odmawia weryfikacji cięcia z nieprzerzuconymi polami, a żadnemu przerzuceniu
  się nie wierzy — decydują verifiery. `Founder [x]` bez `acceptance/founder.json` to sfałszowany
  podpis i scaffold-doctor odrzuca plan.
- **Trwałe artefakty NIGDY nie idą do `/tmp` i NIGDY do checkoutu produktu.** `/tmp` to tylko ulotny
  scratch — jest wymazywany, nieśledzony i niewidoczny dla tooling-u i synca Foundera. Checkout
  produktu niesie kod i dokumentację produktu (ignored prywatny journal Operatora
  jest jawnym wyjątkiem): plan, brief, DRIVER, tracker, raport
  czy design doc wrzucony do drzewa (np. `docs/plans/`) brudzi worktree, zatruwa snapshoty strukturalne
  fałszywym sygnałem dirty-worktree i ryzykuje commit efemer dyspozytury do produktu. Każdy trwały
  artefakt ląduje w **kanonicznym root planu**:
  `~/.vibecrafted/artifacts/<org>/<repo>/<DATE>/plans/<plan_id>/`
  (lustro layoutu raportów; `<org>/<repo>` z tożsamości git remote, nigdy ze ścieżki checkoutu).
  Zapis trwałego artefaktu do `/tmp` lub do checkoutu to porażka procesu, nie skrót.
- **manifest.json jest obowiązkowy.** To jedyny inwentarz artefaktów i kontrakt ról. Żadne lustro
  `operator/`, duplikat, inferencja roli z nazwy ani symlink kompatybilności nie może stać się drugą
  zapisywalną prawdą.
- **Artefakt `.dispatch.toml` jest obowiązkowy.** Zwaliduj `vibecrafted.dispatch.v1` przez dispatcher doctor i
  przekaż wykonanie lifecycle do `/vc-ship` albo jawnej ograniczonej drogi
  dispatchu zarządzonej przez Foundera; ręczne workflow per task to tylko awaryjne recovery.
- **Serwuj, nie przesłuchuj.** Renderuj edytowalne artefakty i przeglądaj je przez `vibecrafted-server`;
  Founder edytuje plan, a nie odpowiada na dwadzieścia pytań w trakcie scaffoldu.
- **Mierz, nie twierdź.** Cięcie jest gotowe, gdy jego verifier jest zielony, nigdy gdy agent tak mówi.
- **Mapuj przed projektowaniem.** Szanuj ziarno istniejącego systemu; loctree przed założeniami.
- **Scope to twój najlepszy przyjaciel.** Ciasny scope + świetne wykonanie bije luźny scope za każdym razem.
- **Pisz dla nieobecnego operatora.** Artefakt mówi sam za siebie; następny READ go falsyfikuje
  bez człowieka po drugiej stronie.
- **Trzymaj zależności płytkie.** Preferuj niezależne strumienie pracy; sekwencyjne A→B→C zabija równoległość.
- **Żadnej przedwczesnej optymalizacji / żadnych wymyślonych wzorców.** Najlepsza architektura to ta, która dowozi.

## Mandatory plan closing — Emil spirit

Founder potwierdził to ponownie 2026-09-07; wcześniejsza, napisana przez Foundera
instrukcja Emil Kurier leży w sesji AICX Claude `2b73c9c1-87ef-49ce-a43f-3dc980d7816a`
(2026-05-26): CTA, celowo suchy żart motywacyjny i kaomoji mają być zaskakujące
i unikalne.

Każdy master plan, DRIVER i wykonawczy brief cięcia kończy się:

- Krótką, związaną z zadaniem linijką motywacyjną z kaomoji.
- **Call to Action:** konkretny następny autoryzowany krok, jego właściciel i to, co
  ma zwrócić. Dopasuj do bieżącego stanu planu i kanonicznej trasy wykonania; plan
  zablokowany woła o rozwiązanie blokera, a nie udaje, że jest gotowy do startu.
- **Suchar:** świeży, celowo suchy żart związany z tym zadaniem, z kaomoji.
  Napisz go pod ten plan; nie recyklinguj gotowej puenty w całej paczce.

Do prezentacji użyj istniejącej
[klamry końcowej Emila](../../vc-operator/DISPATCH.md#closing-rail--the-emil-default-block).
Zachowaj ten głos w planach polskich i angielskich. Trzymaj zamknięcie krótko;
humor nigdy nie zastępuje kryteriów akceptacji ani nie ogłasza niezweryfikowanego sukcesu.

## What Success Looks Like

- Zimna flota (albo człowiek) wykonuje plan **bez zadawania pytania** w locie.
- Każde cięcie ma `Vector` i `delivery-verifier`; kolumna `state` jest czytelna maszynowo.
- Granice scope'u są krystalicznie jasne; 3-5 decyzji architektonicznych jawnych z trade-offami.
- Plan przetrwa nieobecnego operatora: `[x]` jest zasłużone, `[?]` jest uczciwe, nic nie jest fałszowane.

## Cross-References

- **vc-init** — bootstrapuje kontekst agenta po scaffoldowaniu (checkpoint orientacji).
- **vc-ship** — jedyny normalny wykonawca A→Z wielocięciowego artefaktu dispatch scaffoldu.
- **vc-dispatch** — wspierane ograniczone fale zarządzone przez Foundera;
  zachowują bramki i artefakty scaffoldu.
- **vc-implement** / **vc-workflow** — ograniczone komórki WRITE wybierane wewnątrz kontraktu dispatchu.
  **vc-justdo** — samodzielna postawa (prompt-typed; nie implement).
- **vc-review · vc-followup · vc-audit · vc-dou** — fazy READ, które falsyfikują każdy artefakt WRITE.
- **vc-operator** — czyta kolumnę `state` planu i prowadzi dispatch (trigger/stop).
- **vc-research** — triple-agentowy research dla niewiadomych znalezionych podczas Orient/Falsify.

## Anti-Patterns

- Planowanie przed checkpointem orientacji (komponowanie architektury z pamięci = cichy dryf).
- Shape bez odpowiedzi foundera albo wskazanego wcześniejszego wywiadu.
- Sekcja „Running This Plan" złożona z ręcznych komend workflow per task.
- Gołe pozwolenie na `--no-verify` bez autoryzacji fazy, zadeklarowanych bramek, raportu
  checkpointu i kontraktu admission integratora.
- 50-stronicowy design doc zamiast ostrego, mierzalnego planu.
- Proza zamiast kolumny `state` — operator nie odpali trigger/stop na prozie.
- Traktowanie twierdzenia `[~]` agenta jak `[x]` bez verifiera (pułapka optymizmu).
- STOP-jako-kapitulacja (502-i-umrzyj) zamiast STOP-jako-recovery-vector.
- Rozbijanie całej pracy na sekwencyjne zależności; pomijanie tożsamości produktu.

## Verification carries into the prompt

Semantyka delivery-proof żyje w `vibecrafted_core.delivery`; zobacz
`docs/runtime/DELIVERY_PROOF_KERNEL_v1.md`.

Każdy prompt tego skilla musi nieść [Verification Rule](../../VERIFICATION_RULE.md)
do dispatchu workera: walk-around verification (zielone bramki ≠ działa) + loct
literal-vs-semantic. Zobacz `vc-operator/DISPATCH_TEMPLATE.md`, sekcje 6 + 9.

Zmiany bajtów skillów regenerują `vibecrafted-core/vibecrafted_core/skills/SKILL_PROVENANCE.json`
przez `make skills-check UPDATE=1` (tracked generator: `scripts/gen_skill_provenance.py`).
Szanuj osobno posiadany cut generatora i zachowaj historyczne wpisy; integrator
regeneruje wspólny manifest po admission. Jedyny journal decyzji Operatora to
ignored `<repo-root>/.vibecrafted/THE_JOURNAL.md`, nigdy tracked artefakt planu.
Workerzy piszą raporty od launchera zachowujące maszynową tożsamość, nie journal
Operatora.
