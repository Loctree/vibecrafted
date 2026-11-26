# `vc-followup` — Kształt wyjścia i antywzorce

## Kształt wyjścia

Domyślna struktura wyjścia:

1. **Bieżący stan** — co istnieje teraz i co się zmieniło od ostatniego pushu implementacyjnego
2. **Co wciąż jest nie tak** — luki, dryf, kruchość, niedokończone powierzchnie
3. **Verdict kierunku** — czy praca zmierza w dobrym kierunku, czy nie
4. **Następny ruch** — kontynuacja o największej dźwigni

Jeśli to istotne, jawnie rozdziel:

- luka w kodzie
- luka w runtime
- luka w UX
- luka w dokumentacji/pakowaniu

## Antywzorce

Nie:

- sprowadzaj `vc-followup` do synonimu `vc-review`
- zmuszaj go do zależności od PR lub zakresu commitów, gdy prawdziwe pytanie jest kierunkowe
- zwracaj samych findingów bez powiedzenia, czy bieżąca trajektoria jest zdrowa
- myl „wciąż są luki" z „kierunek jest zły"
- pomijaj followup powierzchni produktu i patrz tylko na kod
