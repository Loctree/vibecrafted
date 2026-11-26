# `vc-canary` — Schemat dowodowy, werdykt i kontrakt journala

## Schemat dowodowy (per finding)

Oś · konkurenci (`file:line`, LOC) · walczące symbole · werdykt pary ·
znak legendy · klasyfikacja · dowód (wyjścia loct cytowane per organ) ·
pokwitowanie falsyfikacji nieobecności (linia literal coverage). Finding
bez któregokolwiek elementu jest kandydatem, nie findingiem.

## Werdykt przebiegu i uczciwe wyjście

Każdy przebieg zwraca dokładnie jeden werdykt:

| Werdykt                      | Warunek                                                                                                                                                            |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `AXES_CLOSED_CANDIDATE`      | zero wierszy `UNRESOLVED`; każda zachowana krawędź wykonywalna sprowadza się do jednej władzy; zero bypassów; kompletne, nieucięte dowody pod jednym fingerprintem |
| `AXES_OPEN`                  | cokolwiek mniej — powiedz to wprost                                                                                                                                |
| `INSTRUMENT_INCOMPLETE`      | Loctree nie pokrył wymaganych pytań (fail-log dopisany)                                                                                                            |
| `LAUNCHER_CONTRACT_CONFLICT` | odziedziczone instrukcje żądały mutacji lub commitów — stop, zostań przy N=1, raportuj                                                                             |

Brakujące historyczne punkty kontrolne pozostają `MISSING` — nigdy nie są
rekonstruowane ani interpolowane. Raport kończy się linią uczciwego stanu
`BUILD/LINT/TEST/RUNTIME=NOT_ASSESSED`: canary jest radarem bez mutacji,
a zielone bramki leżą poza jego jurysdykcją.

## Kontrakt journala

Append-only `./.loctree/canary/JOURNAL.md` w docelowym repo. Każdy
przebieg dopisuje: SHA HEAD, pokwitowania Phase 0, zbadane osie, findingi
z dowodami, wyniki prism. Przebiegi nigdy nie nadpisują historii —
journal pokazuje, co radar widział _na tym SHA_, nawet gdy późniejszy
przebieg wie lepiej.
