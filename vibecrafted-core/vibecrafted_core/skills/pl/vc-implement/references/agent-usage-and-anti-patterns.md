# `vc-implement` — Użycie agentów i antywzorce

## Użycie agentów

| Sytuacja                               | Akcja                                 |
| -------------------------------------- | ------------------------------------- |
| Jedno skupione zadanie, < 200 LOC      | Zrób sam                              |
| Dwa niezależne strumienie pracy        | Zespawnuj 2 agentów przez `vc-agents` |
| Szybki review własnej pracy            | `vc-delegate` jeden reviewer          |
| Recon potrzebny dla nieznanego API/lib | Jeden agent recon, pracuj dalej       |
| Wszystko jest sekwencyjne              | Zrób sam; agenci dokładają latencji   |

Narzut spawnu/kontekstu/syntezy jest realny. Paralelizuj tylko wtedy, gdy
oszczędza więcej czasu, niż kosztuje.

## Antywzorce

- Zadawanie 5 pytań doprecyzowujących przed startem
- Pisanie dokumentu z planem i proszenie o zatwierdzenie
- Ogłaszanie „Faza 1 ukończona, wchodzę w Fazę 2"
- Pomijanie followup, bo „wygląda dobrze"
- Pomijanie marbles, bo „został tylko jeden P1"
- Spawnowanie 4 agentów do zadania, które jeden agent skończy w 20 minut
- Dowożenie bez uruchomienia bramek jakości
- Zostawianie użytkownika, żeby sam dochodził, co się zmieniło
- Naprawianie niepowiązanego kodu, podczas gdy zamówiony feature jest niekompletny
- Cisza przez 30 minut bez żadnego sygnału postępu
- Traktowanie tego skilla jako zamiennika `vc-justdo`
