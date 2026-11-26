# vc-polarize — Słownik podstawowy i tryby

## Słownik podstawowy

### Rozmaz kodu (Code Smear)

Koncept runtime'u albo produktu, którego prawda jest rozsmarowana po wielu
plikach, warstwach, docs, testach, artefaktach, publicznych powierzchniach
i pamięci operatora. Rozmaz nie jest automatycznie zły — staje się
groźny, gdy rozsmarowanie tworzy **konkurencyjne** prawdy.

### Prism Score (wynik pryzmatu)

Diagnostyczny wynik tego, jak bardzo koncept załamuje się przez framingi
`loct context --task`. Wysoki Prism Score oznacza:

- jeden lokalny slice zmyli przyszłych agentów
- koncept zasługuje na wpis w korpusie
- przed releasem może być potrzebny przebieg polaryzacji

**Nie** oznacza: złego kodu, awarii CI, wstydliwego KPI, kary za liczbę
plików.

### Polaryzacja

Ruch przeciwny do rozmazu. Wybierz jedną oś / fasetę i spraw, by runtime,
testy, docs, artefakty i publiczne powierzchnie się zgadzały.

## Tryby

### Tryb konceptu (Concept Mode)

Użyj, gdy rozmazany jest koncept architektoniczny / runtime'u. Przykłady:
cykl życia marbles, powierzchnia release'u, publiczny kontrakt instalatora,
synteza research swarmu, granica auth, kontekst memory/search.

Wyjście: jeden kontrakt konceptu i ścieżka dowodu.

### Tryb produktu (Product Mode)

Użyj, gdy rozmazana jest powierzchnia produktu / publiczna. Przykłady: za
dużo grup odbiorców, rozszczepione CTA, landing page kłócący się ze ścieżką
instalacji, docs obiecujące za dużo względem runtime'u, brief release'u bez
jednej dowiezialnej tezy.

Wyjście: jedna teza produktu i handoff DoU / release.
