# vc-marbles — Świadomość kosztu: zimny start, gorąca pętla

## Świadomość kosztu: zimny start, gorąca pętla

`vc-marbles` wygląda na drogi tylko wtedy, gdy każdy run agenta liczy się jako
świeże zdarzenie. To zły model rozliczania.

Drogi jest zimny start: czytanie repo, rekonstrukcja intencji, znalezienie
prawdziwej powierzchni awarii i nauczenie się, gdzie system kłamie. Gdy ten
kontekst jest już gorący, powtarzane runy marbles po tej samej bounded
powierzchni to nie marnotrawstwo. To kompresja.

Marbles wykorzystuje rozgrzany cache.

Dobra pętla marbles trzyma podłoże stabilne:

- to samo repozytorium
- ten sam obszar zadania
- te same padające bramki
- ta sama intencja architektoniczna
- ten sam lub porównywalny prompt
- mały dystans czasowy między runami

Dzięki temu każdy nowy worker płaci mniej za archeologię i wydaje więcej
swojego budżetu na delty: przeoczone rysy, fałszywe fixy, kruche założenia
oraz spory między agentami.

Celem nie są tanie runy. Celem są gęstsze runy.

Jedno izolowane wywołanie agenta daje ci jedną interpretację. Gorąca pętla
marbles daje ci nacisk zbieżności. Gdy kilku workerów wciąż napiera na tę
samą powierzchnię, pozostałe spory stają się sygnałem: albo kod wciąż kłamie,
albo prawda produktu jest rozmazana.

I tu przejmuje pałeczkę `vc-polarize`.

Zasada kosztu:

- jeden zimny run odkrywa kształt
- powtarzane gorące runy eksponują zbieżność
- stale pętle generują szum
- rozproszone pętle niszczą rozgrzany cache
- `vc-polarize` decyduje, co przetrwa

Nie rozpraszaj runów marbles po niepowiązanych inicjatywach. Nie przepisuj
bez przerwy powierzchni docelowej, chyba że operator celowo resetuje
eksperyment. Marbles działa, bo swarm wciąż napiera na te same rysy, aż
fałszywe naprawy, przepełnione luki i prawdziwe decyzje strukturalne staną
się widoczne.

Krótko: marbles nie zaczyna od zera przy każdym runie. Trzyma ten sam
kontekst pracy, tę samą powierzchnię problemu i te same bramki, dzięki czemu
kolejne workery mniej czasu tracą na archeologię repo, a więcej na brakujące
luki, fałszywe fixy i kruche założenia. To daje gęstsze, łatwiejsze do
porównania runy.

Nadmiar jest celowy. Marbles wypełnia za dużo, żeby `vc-polarize` mógł
ciąć z powrotem do jednej prawdy na podstawie evidence, nie gustu.
