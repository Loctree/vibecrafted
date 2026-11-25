# Vibecraftsmanship — Referencja autonomicznego samodzielnego tempa

## Domyślny tryb operacyjny — autonomiczne samodzielne tempo (natywne dla Claude Code)

**TWARDA ZASADA (egzekwowanie osi Siły, druga kanoniczna powierzchnia):** Gdy agent
wchodzi w zachowanie autonomiczne — operator nieobecny, decyzje odroczone, cykliczny
monitoring, wieloturowe wykonanie bez ręcznych re-promptów — domyślnym mechanizmem jest
natywny dla Claude Code skill **`/loop`** (odpowiednik: `ScheduleWakeup` z sentinelem
`<<autonomous-loop-dynamic>>` dla trybu dynamicznego tempa). NIE ciche czekanie. NIE
polling w ciasnych sleepach Basha. NIE „po prostu odpowiem w następnej turze, kiedy
operator wróci".

**Powód:** `/loop` to kanoniczna power-funkcja Claude Code do autonomicznego samodzielnego
tempa — wypełnia lukę między „operator prowadzi każdą turę" a „agent odpala i zapomina".
Bez wejścia w `/loop` agent cofa się do jednoturowej bierności: operator musi
re-promptować, żeby kontynuować pracę, nawet gdy kolejne kroki są oczywiste. `/loop`
czyni autonomiczny ogon agenta obserwowalnym i ograniczonym (interwał heartbeat,
harmonogram fallback, jawny warunek stopu).

**Kiedy wejść w `/loop`:**

- Operator zadeklarował „bez odbioru" / „decyduj autonomicznie" / „wychodzę"
- Oczekiwanie na pracę zewnętrzną (CI, zdispatchowana flota, długo trwający build)
- Wielofalowy dispatch, gdzie fale kończą się asynchronicznie
- Operacja na podłożu ze znanym oknem oczekiwania (rebase, instalacja, sync)
- Cykliczna obserwacja (niańczenie PR-ów, monitoring deploya)

**Kiedy NIE wchodzić w `/loop`:**

- Jednoturowa odpowiedź bez kontynuacji
- Operator aktywnie zaangażowany w rozmowę
- Praca jawnie zawężona do „zrób tę jedną rzecz i stop"

**Złożenie z zewnętrznym dispatchem:**

- Zewnętrzny dispatch (`vibecrafted <launcher> <agent>`) produkuje pracę asynchroniczną,
  która wymaga `await`. Wejdź w `/loop`, aby utrzymać heartbeat między zdarzeniami
  `task-notification` z harnessu.
- `/loop` + `vibecrafted` = kanoniczny wzorzec autonomicznego operatora. Jeden deklaruje
  „pozostaję zaangażowany"; drugi deklaruje „używam obserwowalnej powierzchni
  zewnętrznej". Oba razem = w pełni zrealizowana oś Siły vibecraftsmanship.

**Sygnał wykrycia (STOP i wejdź w loop):** jeśli łapiesz się na kończeniu tury słowami
„ruch należy do operatora" lub „czekam na odpowiedź", podczas gdy istnieje już
autoryzowana praca w kolejce, która mieści się w bieżącym zakresie i warunkach stopu —
to przeoczone wejście w `/loop`. Przemyśl od nowa: zaplanuj samodzielnie tempowany check,
zadeklaruj, co zrobisz na każdym ticku, zatrzymaj się, gdy warunek stopu zostanie spełniony.
