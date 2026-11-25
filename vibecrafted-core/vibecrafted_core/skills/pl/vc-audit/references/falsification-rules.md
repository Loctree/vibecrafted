# vc-audit — Reguły falsyfikacji i taksonomia dowodów

## Postawa domyślna: falsyfikacja

Domyślny verdict dla każdego wymagania to **UNVERIFIED**. Wymaganie
zarabia PASS tylko przy wszystkich czterech:

1. **Evidence z taska** — zacytowane acceptance criterion lub non-goal
2. **Evidence z kodu** — ścieżka pliku, nazwa funkcji/typu/testu, zakres linii
3. **Evidence z testów** — nazwa testu + output uruchomienia, albo uzasadniona luka testowa
4. **Negative check** — stare/zabronione zachowanie nie jest już obecne

### Twarde reguły nie-ufania

NIE WOLNO ci ufać statusowi z frontmattera taska, raportom wcześniejszych
agentów, commit messages, wpisom AICX, memory slices (wycinkom pamięci),
notatkom z dziennika projektu, adnotacjom „completed", opisom PR-ów, inline'owym
komentarzom `// done` ani wcześniejszym raportom `vc-followup` /
`vc-review` — chyba że **niezależnie potwierdzone w bieżącym kodzie/testach**.
Każde z nich to _twierdzenie_, nie evidence. Audit zamienia twierdzenia
w evidence, sprawdzając kod.

### Taksonomia evidence

| Stopień | Kryteria                                                   |
| ------- | ---------------------------------------------------------- |
| STRONG  | Kod + ukierunkowany test + negative check OK               |
| MEDIUM  | Kod + słaby/ogólny test + negative check OK                |
| WEAK    | Tylko kod, brak testu lub brak negative check              |
| NONE    | Brak bezpośredniego evidence — verdict musi być UNVERIFIED |

**PASS wymaga STRONG lub MEDIUM na wszystkich kluczowych wymaganiach.**
