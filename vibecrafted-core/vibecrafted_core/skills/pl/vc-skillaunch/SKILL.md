---
name: vc-skillaunch
description: >
  Distills a completed user workflow, session interaction or pattern
  into a reusable agent skill. Use when the user asks to turn their workflow,
  interaction, or multi-step process into a skill, or when they say "make
  this a skill", "create a skill from what we just did", "package this
  workflow" or similar.
  Do not use for creating skills from scratch without an existing workflow
  (use a generic skill-creator for that).
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Wywołanie dla `vc-skillaunch` (skill fundamentu)**
>
> To nie jest core worker `vibecrafted skillaunch <agent>`. Ładuj interaktywnie
> i wykonuj w sesji. Pakuj inne skille pod
> [Matrycę Delegacji](../DELEGATION_MATRIX.md) — literały per launcher, bez paste
> workflow, swobodniejszy native gdy trzeba głębi, flota external bez zmian.

<!-- /fleet-imperative -->

# Workflow-to-Skill Distiller

Zamienia ukończony workflow w wielokrotnego użytku skill agenta. Konkretnie ten skill
wyciąga wzorce z interakcji lub workflow, który **już się wydarzył**, i je pakuje.

## Checkpoint orientacji

Jeśli destylowany workflow zależy od repozytorium, uruchom lub skonsumuj procedurę
`vc-init`, zanim napiszesz kontrakt skilla. `Loctree:loctree` to domyślny skill percepcji
strukturalnej dla tego przebiegu i musi wyprodukować lub odświeżyć Mapę Aplikacji
Wyprowadzoną z Kodu (Code-Derived Application Map).

Jeśli brakuje świeżych dowodów z `vc-init`, najpierw wykonaj przebieg init i traktuj
pisanie skilla zależnego od repo jako zablokowane, dopóki nie ma aktualnej prawdy repo.

Jeśli workflow nie jest specyficzny dla repo, zadeklaruj wyjątek „bez repo" i destyluj
evidence z interakcji bezpośrednio.

> [!CAUTION] **MUSISZ ukończyć Fazę 1 (Brainstorming), zanim napiszesz jakikolwiek kod
> lub treść SKILL.md.** Pominięcie brainstormingu produkuje skille, które są albo
> zbyt sztywne, albo zbyt mgliste. Rozmowa brainstormingowa to najważniejsza
> część tego procesu.

## Doktryna pracy z repozytorium

W pracy z repozytorium zacznij od Loctree jako mapy: użyj `loct context`,
`loct occurrences`, `loct body` i `loct find --literal` przed szerokim ręcznym
przeszukiwaniem. Używaj AICX do kontekstu intencji i sesji. Używaj rg/grep jako
fallbacku lub lokalnej lupy, nie jako zamiennika mapowania strukturalnego. Jeśli Loctree
zawiedzie lub przeoczy jakąś powierzchnię, dopisz feedback do `~/.vibecrafted/loctree/loctree-fail.md`.

## Faza 1: Brainstorming (OBOWIĄZKOWA)

Przeprowadź z użytkownikiem iteracyjną rozmowę (2–3 pytania na rundę, nigdy wszystkie naraz) w pięciu rundach: (1) zrozumienie workflow, wejść/wyjść i częstotliwości, (2) sztywność kroków i obsługa błędów, (3) istniejące skille, limity API i pliki kontekstowe, (4) zakres, klasa Matrycy Delegacji (`core` / `meta` / `fundament` z dokładnymi literałami), decyzja kod-vs-instruction-only oraz nazwa, (5) opcjonalne zapytanie/odpowiedź walidacyjne. Przejdź do Fazy 2 dopiero po uzyskaniu odpowiedzi na wszystkie 10 kryteriów ukończenia.

Pełny bank pytań i checklista ukończenia: [references/brainstorming-bank.md](references/brainstorming-bank.md).

## Faza 2: Projekt skilla

Wyprodukuj **dokument projektowy** (jako artefakt / plan wdrożenia) i przedstaw
go użytkownikowi do zatwierdzenia. Dokument musi zawierać:

1.  **Nazwę i opis skilla** (zgodnie z regułami frontmatteru YAML: name ≤64
    znaki, małe litery + myślniki; description ≤1024 znaki).
2.  **Strukturę katalogów** pokazującą wszystkie planowane pliki.
3.  **Istniejące skille, do których są odwołania**, wraz z uzasadnieniem każdego.
4.  **Nowe skrypty** (jeśli są) z proponowanymi subkomendami i argumentami.
5.  **Strategię rate limitingu** dla każdego API niepokrytego przez istniejące skille.
6.  **Strategię obsługi błędów** per krok.

**Poczekaj na wyraźne zatwierdzenie użytkownika, zanim przejdziesz do Fazy 3.**

## Faza 3: Implementacja

### Zasady przewodnie

Ogólne wytyczne dla implementacji skilla:

- Używaj `uv run`, nigdy `python` ani `python3`.
- Preferuj biblioteki stdlib dostarczane z domyślną instalacją Pythona 3
  (`urllib` preferowane); unikaj bibliotek wymagających dodatkowej instalacji, jeśli
  to możliwe.
- Limity zapytań (rate limits) muszą być udokumentowane i respektowane w kodzie. Preferuj
  **rate limiting oparty na file-locku**, tak by współbieżni subagenci współdzielący
  tę samą maszynę wspólnie respektowali limit. Zobacz inne skille w bundlu Science
  Skills po kanoniczną implementację bezpieczną międzyprocesowo.
- Wyjście skilla musi mieć <500 linii lub być przekierowane do pliku. Długie pliki wyjściowe
  należy przetwarzać programistycznie, aby wyciągnąć istotne pola.
- Dla nazwy skilla i pola YAML `name:` zaleca się myślniki.

### Reguła 1: Wykorzystuj istniejące skille ponownie

Gdy workflow korzysta z funkcjonalności pokrytej przez istniejący zainstalowany skill, nowy
SKILL.md **MUSI** odwołać się do niego po nazwie, zamiast go reimplementować. Dołącz
sekcję **Dependencies** w SKILL.md, listującą wymagane skille z krótkim
uzasadnieniem każdego.

### Reguła 2: Rate limiting dla nowych API

Dla każdej interakcji z API **niepokrytej** przez istniejący skill wygenerowany skrypt CLI
**MUSI** zaimplementować rate limiting. Zanim napiszesz jakikolwiek kod rate-limitingu,
**sprawdź oficjalne wytyczne dotyczące limitów zapytań danego API**: przejrzyj dokumentację,
którą użytkownik dostarczył podczas brainstormingu, a następnie poszukaj publicznej
dokumentacji API online. Jeśli nie da się znaleźć udokumentowanego limitu, **domyślnie przyjmij 1
zapytanie na sekundę**. Wzorzec rate-limitingu jest wbudowany bezpośrednio w szablon CLI
w `references/cli_script_template.py` — zobacz klasę `RateLimitError`
oraz metodę `_request` klienta API.

Kluczowe wymagania:

- Używaj `time.monotonic()` do pomiaru czasu (nie `time.time()`).
- Wyliczaj opóźnienie z udokumentowanych limitów zapytań.
- Zaimplementuj retry z wykładniczym backoffem dla błędów przejściowych (5xx).
- Rzucaj dedykowany `RateLimitError`, gdy otrzymasz HTTP 429.
- Loguj próby retry na stderr, aby agent mógł obserwować postęp.
- Dołączaj URL i wartość limitu zapytań do komunikatów błędów.
- Przy nieretrowalnych błędach HTTP (np. 400, 403, 404) odczytaj i dołącz
  ciało odpowiedzi do komunikatu błędu — nie tylko kod statusu. Ciała odpowiedzi
  API zawierają konkretne detale (np. „Invalid parameter"), które pozwalają
  agentowi się samoskorygować.

### Reguła 3: Wzorzec skryptu CLI (domyślny, gdy kod jest potrzebny)

**To jest domyślny wybór.** Jeśli **jakikolwiek** krok workflow wiąże się z wywołaniami
API, przetwarzaniem danych, I/O plików, obliczeniami lub jakąkolwiek inną pracą
programistyczną, wyprodukuj wielokomendowy skrypt CLI używający `argparse` z subkomendami. Trzymaj się
szablonu w `references/cli_script_template.py`.

Kluczowe wymagania:

- Każdy ważny krok workflow staje się subkomendą.
- Wszystkie subkomendy przyjmują `--output` do zapisu wyników do pliku.
- Używaj `json.dump` z `indent=2` dla wyjścia JSON.
- Wypisuj komunikat sukcesu ze ścieżką pliku wyjściowego.
- Wychodź z kodem 1 przy błędach.
- Czyń argumenty w stylu `--limit` **wymaganymi** (żadnych cichych wartości domyślnych). To zmusza
  agenta do jawnego podania wartości i zapobiega zakładaniu, że pobrał „wszystkie"
  wyniki, gdy w rzeczywistości został po cichu ograniczony.

### Reguła 4: Domyślnie wyjście do pliku

Wszystkie skrypty i workflow **MUSZĄ** zapisywać wyjście do plików, nie na stdout. Stdout
powinno zawierać tylko krótkie komunikaty statusu (np. „Success! Data written to:
results.json"). To krytyczne, ponieważ:

- Odpowiedzi API mogą być bardzo duże i ulegną obcięciu w wyjściu terminala.
- Wyjście do pliku jest oszczędne tokenowo — agent czyta tylko potrzebne mu pola,
  używając `jp` lub jednolinijkowców w Pythonie.
- Duże wyjście na stdout marnuje przestrzeń okna kontekstu.

### Reguła 5: Wzorzec instruction-only (tylko gdy kod nie jest potrzebny)

Używaj tego wzorca **wyłącznie** wtedy, gdy workflow wymaga **zera** pracy
programistycznej — tj. każdy krok dotyczy wyłącznie orkiestracji, rozumowania,
koordynacji wielu skilli lub trzymania się spisanego protokołu. Jeśli jakiś krok potrzebuje kodu (wywołania
API, przetwarzanie danych, I/O plików itd.), użyj zamiast tego wzorca CLI z Reguły 3.
Wyprodukuj SKILL.md z ustrukturyzowaną sekcją workflow:

```markdown
## Workflow

### 1. Step Name

- Description of what to do
- Which skill to use and how

### 2. Next Step

...
```

### Reguła 6: Struktura SKILL.md

Każdy wygenerowany SKILL.md musi trzymać się tej struktury:

```markdown
---
name: { skill-name }
description: >-
  {description}
---

# {Skill Title}

## Overview

{Brief description of what the skill does.}

## Dependencies

{List of required skills, if any.}

## Quick Start

{Minimal example to get started.}

## Utility Scripts (if CLI-based)

{Document each subcommand with examples.}

## Workflow (if instruction-only)

{Numbered steps with clear instructions.}

## Rate Limiting (if applicable)

{Document rate limits and how they are enforced.}

## Common Mistakes

{List 2-3 common pitfalls.}
```

## Faza 4: Walidacja

Po ukończeniu implementacji:

1.  **Przetestuj skilla ręcznie**, wywołując agenta promptem w języku
    naturalnym, który powinien wyzwolić nowego skilla.

2.  **Jeśli podczas brainstormingu podano przykładowe zapytanie/odpowiedź**, przepuść je
    przez skilla i zweryfikuj, czy wyjście odpowiada oczekiwaniom.
