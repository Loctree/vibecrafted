# vc-operator — Protokół operacyjny, Brief-Gate, Prawo dispatchu, Antywzorce i Kształt wyjścia

## Brief-Gate — nigdy nie dispatchuj wydmuszki (scaffold-doctor)

Przed odpaleniem JAKIEJKOLWIEK fali plan MUSI przejść bramkę **scaffold-doctor**: każde
cięcie w wave atlas ma wyrenderowany `briefs/<wave>-<slot>_<slug>.md` ze wszystkimi 12
sekcjami, atomową akceptacją popartą weryfikatorem oraz dokumentem projektowym dla
każdego cięcia `needs_design`.

- Chudy `master-dispatch.md` bez briefów per cięcie to **wydmuszka** — odmów jego
  dispatchu.
- Jeśli któremuś cięciu brakuje briefu, NIE improwizuj go w chwili odpalenia i NIE
  odpalaj bez niego. Wróć do `vc-scaffold` (Faza 5), aby wyrenderować brakujące briefy,
  a potem ponownie przejdź bramkę.
- Bramka jest **sprawdzana maszynowo, nie obiecywana przez agenta**
  (`vibecrafted-server/control-core`) — to ta sama bramka artefakt-jako-prawda, której
  używa każdy handoff kadencji read-write (scaffold→implement, marbles→audit…).

To operatorska połowa reguły brief-na-cięcie: scaffold renderuje briefy, operator
odmawia prowadzenia bez nich. Razem czynią „flow nie dowozi" strukturalnie niemożliwym —
a nie dyscypliną, którą agent musi pamiętać.

## Pętla operacyjna

1. Uruchom lub skonsumuj świeże evidence `vc-init`.
2. Przeczytaj plan i wszystkie cytowane pliki w całości.
3. Przekształć przez `vc-scaffold`, jeśli plan nie jest dispatchowalny.
4. Zbuduj wave atlas.
5. Zweryfikuj każde cięcie względem Loctree.
6. Wybierz agentów przez `WHY_MATRIX_TABLE.md`.
7. Wyrenderuj briefy workerów z `DISPATCH_TEMPLATE.md`.
8. Przeskanuj każdy brief pod kątem niebezpiecznych komend i triggerów hard-stop.
9. Odpalaj po jednej fali naraz przez `vibecrafted <skill> <agent>`.
10. Czekaj na trwałe artefakty.
11. Zweryfikuj raporty, bramki, gałąź i SHA.
12. Przeskanuj wylądowane commity pod kątem sekretów, danych osobowych, ścieżek
    lokalnych, lokalnej topologii sieci, adresów IP i dokumentów wewnętrznych.
13. Przy zacięciach użyj dispatchu odzyskiwania; nigdy nie restartuj na ślepo.
14. Zaktualizuj tracker i dopisz materialne decyzje do kanonicznego dziennika.
15. Zsyntetyzuj zamknięcie fali.
16. Kontynuuj lub zatrzymaj się przy niedozwolonym operator button.

## Prawo dispatchu

Każdy dispatch zewnętrznego workera idzie przez launcher frameworka:

```bash
vibecrafted <skill> <agent> --file <brief>
```

Żadnych natywnych subagentów do dispatchu floty w trybie operatora. Natywna delegacja
jest dozwolona dla równoległego zwiadu lub małego bounded researchu wewnątrz sesji
operatora, ale zdispatchowane slice'y workerów potrzebują telemetrii, kart uruchomienia,
raportów, transkryptów, meta i awaitowalnego stanu.

### Granica workera headless

Sesja operatora vc-frame to **User Session**, nie host procesu workera. Każdy zwykły
dispatch floty domyślnie idzie jako `headless` — również praca prowadzona przy
operatorze, odpalona przy ustawionym `VC_FRAME_SESSION_NAME`. To worker jest
właścicielem trwałego stanu runu i transkryptu; vc-frame może te powierzchnie
projektować, a zamknięcie projekcji nie może zatrzymać runu.

- **CLI i MCP są zgodne.** `vibecrafted <skill> <agent> --file <brief>` oraz
  `vc_run_launch` / `vc_launch` domyślnie odpalają odłączonego workera headless.
- **Obserwacja jest jawna i trwała.** Używaj `observe`, `await`, transkryptów, stanu
  runu i settlementu Guardiana zamiast traktować panel jako dowód, że coś żyje.
- **Terminal jest wyjątkiem.** `runtime="visible"` albo `--runtime terminal` podawaj
  tylko dla ścieżki providera, o której wiadomo, że wymaga TTY. Dopóki nie ma brokera
  PTY prowadzonego przez daemona, ta ścieżka kompatybilności zostaje przywiązana do
  terminala i nie dziedziczy gwarancji przeżycia runu headless.
- **Interaktywne PTY zostaje po stronie człowieka.** `init`, `operator` i samo
  interaktywne `resume` pozostają prawdziwymi zakładkami User Session.

## Antywzorce

- Zachowywanie się jak solowy implementer po tym, jak operator poprosił o orkiestrację.
- Dispatchowanie, zanim plan będzie czytelny jako wave atlas.
- Ponowne odpalanie zaciętej fali zamiast czytania artefaktów i wydania odzyskiwania.
- Spawnowanie natywnych subagentów jako zamienników dla dispatchu workerów popartego
  telemetrią.
- Ciche obniżanie tieru modelu lub naruszanie sprawiedliwości agentów.
- Ogłaszanie fali jako zielonej bez evidence raportu, bramki, gałęzi i SHA.
- Autorstwo commitów lub zamknięć workera, jakby operator wykonał ich pracę.
- Czynienie zakładki lub sesji vc-frame właścicielem procesu zwykłego workera.
- Push, merge, deploy lub publikacja bez spisanego zezwolenia plan/sesja lub jawnego
  naciśnięcia operator button.

## Kształt wyjścia

Dla postępu:

1. Bieżący stan - fala, prompt, agent, run ID, gałąź/SHA jeśli wylądowała.
2. Evidence - status raportu/bramki/artefaktu.
3. Decyzja - kontynuuj, odzyskuj, pauzuj lub stop.
4. Następny ruch - dokładnie jeden.

Dla finalnego handoffu:

1. Pokrycie planu i fal.
2. Wyjścia workerów i SHA.
3. Bramki i nierozwiązane ryzyka.
4. Podjęte działania odzyskiwania.
5. Handoff w punkcie stopu: jaki przycisk pozostaje dla operatora.
