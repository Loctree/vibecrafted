# `vc-implement` — Playbook wykonania (Kroki 1–7)

## Jak pracujesz

### 1. Zrozum zadanie

Jeśli jest na tyle jasne, by działać — działaj. Jeśli jest naprawdę
niejednoznaczne (dwie wiarygodne interpretacje prowadzące do różnych architektur),
zadaj **JEDNO** pytanie doprecyzowujące. Nie trzy. Jedno.

Jeśli zadanie jest na tyle ogólnikowe, że wymaga określenia scope'u architektury
(nowy produkt, greenfield, „mam pomysł"), użyj najpierw `vc-scaffold`, a potem
wykonaj. Implement konsumuje plany scaffold bezpośrednio.

Jeśli użytkownik powiedział „I'm tired" lub cokolwiek sugerującego niski poziom
energii, nie zadawaj pytań w ogóle. Podejmij rozsądną decyzję i działaj.

### 2. Zorientuj się

Zbootstrapuj kontekst po cichu. Żadnego raportu init dla użytkownika. Użyj
narzędzi fundamentowych (loctree, aicx, prview, screenscribe):

- `repo-view` / `focus` / `slice` / `impact` — struktura i ryzyko
- `aicx extract` — jeśli poprzednie wyjście jest zbyt duże
- `prview` — jeśli pracujesz na istniejącym PR
- `screenscribe` — jeśli zadanie wymaga wizualnego dowodu demo
- Czytaj istniejący kod przed pisaniem nowego
- Sprawdź git log pod kątem ostatnich zmian w docelowym obszarze

30 sekund, nie 5 minut. Nie zmieniaj recon w projekt badawczy.

### 3. Zaplanuj wewnętrznie

Wybierz swoje podejście. Nie przedstawiaj planu do zatwierdzenia. Pomyśl:

- Najprostsza architektura, która działa?
- Istniejące wzorce, których używa ta baza kodu?
- Punkty integracji?
- Jakie testy istnieją? Jakie testy są potrzebne?
- Zasięg zmiany, jeśli się pomylisz?

Jeśli zasięg zmiany jest duży, a podejście nieoczywiste, powiedz użytkownikowi
swój plan w 3 punktach i poczekaj na skinienie głową. W przeciwnym razie wykonaj.

### 4. Implementuj

Używaj agentów, gdy praca równoległa kupuje realną prędkość:

- Dwa niezależne moduły → dwóch agentów
- Podział frontend + backend → dwóch agentów
- Jeden sekwencyjny feature → zrób sam, agenci dokładają narzut

Użyj `vc-agents` do realnej paralelizacji. Użyj `vc-delegate` do lekkich
zadań w obrębie sesji. Nie spawnuj agentów do zmiany na 50 linii.

Podczas implementacji:

- Trzymaj się istniejących wzorców
- Pisz testy równolegle, nie po fakcie
- Nie refactoruj niepowiązanego kodu
- Nie dodawaj feature'ów, o które użytkownik nie prosił
- Commituj logiczne kawałki, nie jeden megadiff
- W rundach `decorate` zachowuj postęp przyrostowo jak marbles —
  numerowane lokalne commity (`decorate 1: ...`, `decorate 2: ...`), w miarę jak
  zweryfikowane szwy twardnieją.

### 5. Followup (obowiązkowy)

Gdy implementacja wydaje się kompletna, uruchom audyt followup na samym sobie.
Nie opcjonalnie. To tu faza ship zarabia na zaufanie.

- Czy bramki jakości przechodzą? Uruchom je.
- Czy nowy kod integruje się czysto z istniejącym kodem?
- Nieprzetestowane ścieżki?
- Wprowadzone regresje?
- Czy reviewer oflagowałby coś oczywistego?

Wyprodukuj wewnętrznie listę findingów P0/P1/P2. Nie musisz formatować raportu —
musisz znać prawdę.

### 6. Marbles (obowiązkowe, gdy istnieją findingi)

**REGUŁA BEZ WYJĄTKÓW:** jeśli followup znalazł JAKIEKOLWIEK problemy P0 lub P1,
natychmiast wywołaj `vc-marbles`, żeby zrobić loop i je naprawić. Nie poprzestawaj
na zaraportowaniu ich.

Jeśli followup znalazł tylko P2: napraw te oczywiste, resztę udokumentuj.

Pętla marbles pod implement jest ciasna:

```
dopóki P0 > 0 lub P1 > 0:
    napraw najważniejszy problem
    uruchom ponownie dotknięte bramki
    przeoceń findingi
```

Nie ogłaszaj iteracji. Po prostu naprawiaj rzeczy, dopóki nie będą naprawione.
Jeśli utknąłeś na tym samym problemie po 3 próbach, zatrzymaj się i powiedz
użytkownikowi, co blokuje. Nie kręć się w kółko.

### 7. Dowieź

Gdy P0=0 i P1=0, jesteś gotowy. Domknij pętlę:

- Kod zacommitowany w czystych kawałkach
- Feature działa end-to-end (nie tylko testy jednostkowe)
- Zwięzłe podsumowanie dla użytkownika

Podsumowanie to nie raport. To handoff:

```
Zrobione:   [co zbudowałeś]
Zmienione:  [N plików, kluczowe obszary]
Testowane:  [jakie bramki przeszły]
Otwarte:    [pozostałe P2 lub znane ograniczenia, jeśli są]
Dalej:      [co użytkownik powinien wypróbować najpierw]
```

Użytkownik otwiera laptopa, czyta 5 linijek, próbuje feature.
