# vc-marbles — Model operacyjny, soczewki stabilizacji i reguła commita

## Model operacyjny (pojedyncza runda)

Jedno wywołanie = jedna bounded round.

1. **Oskarż obecne drzewo.** Każdy cel śledzi się do: outputu narzędzia,
   padającej bramki, audytu strukturalnego lub kontrprzykładu z ryzyka
   produkcyjnego. **Bez evidence nie ma celu.**
2. **Wybierz najmniejszą powierzchnię o dużym wpływie.** Najwyżej **3 cele**
   na rundę. Preferuj awarie o wysokim severity, ścieżki o wysokiej
   częstotliwości, ciche tryby awarii, słabe granice, problemy zamykające
   klasę awarii. Gdy wiele powierzchni nie zgadza się co do rzeczywistości
   albo kod wymusza ukrytą decyzję produktową, **wyeksponuj ją, ale jej nie
   rozstrzygaj** — to zadanie `vc-polarize`.
3. **Utwardź.** Najmniejszy zbiór zmian, który materialnie zwiększa
   prawdę. Dodaj brakujący scope/auth, brakujące indeksy, zamień
   połknięte wyjątki na obsługę, po której da się działać, dodaj smoke testy,
   scal zduplikowane kontrakty, usuń zgniłe wrappery. Aksjomat
   Vetcoders: **idź dalej ponad wsteczną kompatybilność** — tnij czysto, jeśli
   lokalna abstrakcja jest zgniła i blokuje stabilizację.
4. **Bramkuj.** Najwęższe wiarygodne bramki najpierw; szersze, jeśli zasadne.
   Minimum: składnia / lint dla dotkniętych powierzchni, testy pokrywające
   utwardzoną ścieżkę, odpowiednie sprawdzenia build/bundle. Jeśli bramka
   pada: raportuj wprost, podaj liczbę regresji, nie zagrzebuj jej pod narracją.
5. **Commit.** Dokładnie jeden commit rundy z konwencją poniżej.
6. **Raport.** Zapisz do
   `$VIBECRAFTED_HOME/artifacts/<org>/<repo>/<YYYY_MMDD>/marbles/reports/<ts>_marble_<run_or_round_id>_<agent>.md`.

**Worker zatrzymuje się tutaj.** Nie rozszerzaj się samodzielnie na następną
rundę. Nie pisz instrukcji dla swojego następcy. Warstwa odbioru wyników
decyduje, co odpala następne.

Pełny detal pojedynczej rundy (instrumenty, soczewki, zasada z szatni)
mieszka w [`FLOW.md`](FLOW.md). Routing odbioru wyników / zbieżności mieszka w
[`RECEPTION.md`](RECEPTION.md).

---

## Soczewki stabilizacji (Stabilization Lenses)

Jeśli nie ma dokładnego opisu taska, wybierz tę pasującą do najsłabszej żywej powierzchni:

- **Access & Isolation** — auth, scope per tenant, sprawdzenia ról, granice uprawnień
- **Data Health** — indeksy, plany zapytań, N+1, hotspoty schematu, God Tables
- **Errors & Observability** — połknięte wyjątki, ciche awarie, brakujące alerty
- **Release & Runtime Resilience** — bramki CI/CD, smoke testy, bezpieczeństwo rolloutu, dryf konfiguracji

Runda może dotknąć jednej soczewki lub ściśle sprzężonego klastra. Nie wymuszaj
kolejności filarów, jeśli evidence mówi inaczej.

---

## Reguła commita

**Jedna runda = jeden commit.** Bez częściowych commitów. Bez squashowania
między rundami. Bez kopania w historii gita, żeby ustalić subject line.

Format:

```
marble: <one-line summary>

- <file>: <what changed and why>

Gate: <pass|fail>
Tests: <what ran>
Regressions: <count>
Round-ID: <opaque-id-if-provided>
```

---
