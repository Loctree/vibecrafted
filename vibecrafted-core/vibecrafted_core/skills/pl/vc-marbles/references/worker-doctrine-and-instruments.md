# vc-marbles — Doktryna workera i instrumenty vs bramki

## Doktryna workera (ślepy z premedytacją)

Worker jest celowo **ślepy na wcześniejszą historię marbles**, pracując
wyłącznie przeciw **bieżącemu stanowi workspace'u**. Ciężar kontekstu zabija
jakość — agent pracujący 90 minut podejmuje gorsze decyzje w 91. minucie niż
świeży agent w 1. minucie, broniąc kosztu utopionego zamiast widzieć drzewo.
Każda runda dostaje świeży umysł. To nie obejście — to projekt.

**Warstwa odbioru wyników (reception)** (operator / orchestrator) trzyma rejestr otwartych
findingów, porównuje kandydatów między równoległymi rundami i decyduje, czy
uznać zbieżność, czy odpalić kolejną falę. Zobacz
[`RECEPTION.md`](RECEPTION.md). Nie ładuj warstwy odbioru do kontekstu workera.

---

## Instrumenty vs bramki

**Instrumenty** (loctree, semgrep, aicx-steer) idą na **początek**
— kierują, gdzie patrzeć (oskarżasz drzewo dowodami, nie przeczuciem).

**Testy** (pytest, cargo test, build) idą na **koniec** — weryfikują
fix (bramka).

Start od testów zawęża pole widzenia do „co pada", zamiast pokazać „co jest kruche".
Czerwone testy krzyczą najgłośniej, ale prawdziwa strukturalna słabość
często jest cicha.
