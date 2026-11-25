# vc-polarize — Kontrakt wyjścia, złożenie i antywzorce

## Kontrakt wyjścia

Rekomendowane artefakty:

```
$VIBECRAFTED_HOME/artifacts/<org>/<repo>/<YYYY_MMDD>/polarize/
  thesis.md
  concept-contract.md
  surface-map.json
  decision-ledger.md
  dou-handoff.md
  release-brief.md
```

Jeśli runtime nie ma jeszcze dedykowanego katalogu artefaktów `polarize/`,
napisz tylko normalny wstrzyknięty raport i zawrzyj te sekcje wewnątrz niego.

### Sekcje raportu (obowiązkowa kolejność)

1. **Polarized Thesis** — jedno zdanie, bez słów asekuracyjnych
2. **Mode** — `concept` albo `product`
3. **Prism Evidence** — framingi taska, ścieżki context packów, osie wyniku
4. **Primary Boundary / Audience** — co teraz wygrywa
5. **Rejected Alternatives** — co teraz przegrywa i dlaczego
6. **Runtime Proof** — konkretne evidence z repo / runtime'u
7. **Surface Alignment** — bieżące twierdzenie/ścieżka → problem → wybrane zastąpienie
8. **Edits Made** — jeśli implementacja była w scope
9. **Gates Run** — komendy, status wyjścia, co dowodzą
10. **DoU Handoff** — co DoU powinno audytować dalej
11. **Release Handoff** — co release może uczciwie dowieźć i co pozostaje zablokowane

## Złożenie z sąsiednimi skillami

- **`vc-init`** — wymagana bramka. Polarize bez evidence z init jest ślepy.
- **`vc-marbles`** — wymagany upstream. Bez nadmiaru z marbles do
  zdarcia polarize nie ma czego ciąć.
- **`vc-audit`** — sąsiedni falsyfikator READ-ONLY. Macierz verdictów
  audytu może być bezpośrednim wejściem do polarize, gdy pytanie brzmi
  „które twierdzenia UNVERIFIED przyjąć, a które odrzucić?".
- **`vc-dou`** — downstreamowy sprawdzian gotowości do dowiezienia
  READ-ONLY. Polarize emituje sekcję handoffu DoU.
- **`vc-release`** — downstreamowy WRITE do dowiezienia. Polarize emituje
  brief release'u.

## Antywzorce

- Framing „każdy może tego użyć" (rozszczepiona grupa odbiorców nigdy się nie polaryzuje)
- Jeszcze jeden wrapper zamiast jednego kontraktu
- Zmiana copy bez dowodu z runtime'u
- Punktowanie liczby plików zamiast dryfu autorytetu
- Traktowanie Prism Score jako awarii CI / wstydliwego KPI
- Traktowanie starych context packów jako żywej prawdy kodu
- Ukrywanie wyboru produktowego za technicznym sprzątaniem
- Uśrednianie dwóch wykonalnych osi zamiast wybrania jednej
- Uruchamianie polarize na paśmie `abort` / `memo` (dispatchuj tylko na
  `pass` / `doctrine`)
- Kontynuowanie w DoU / hydrate / decorate / release bez prośby operatora
- Ładowanie nieświeżych prism packów jako autorytatywnych
