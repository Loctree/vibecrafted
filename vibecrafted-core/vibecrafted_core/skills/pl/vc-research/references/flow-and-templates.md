# vc-research — Szablon planu, zbieranie raportów, warstwowe czytanie i antywzorce

## Wywołanie przez command deck

Wejdź w sesję frameworka przez `vibecrafted start` (lub `vc-start`). Następnie uruchamiaj przez command deck — nigdy przez surowe ścieżki `skills/.../*.sh`:

```bash
vibecrafted research --prompt 'Compare auth libraries for Tauri desktop'
vc-research --prompt 'State of the art for MCP streaming transports'
vibecrafted research --file /path/to/research-plan.md
```

Research domyślnie uruchamia odłączone lane'y headless zarówno wewnątrz, jak i
poza vc-frame. Preferuj `--file` dla istniejącego planu, a `--prompt` dla
intencji inline. Jawnego runtime'u terminal używaj tylko dla kompatybilnościowej
lane'y, która wymaga TTY.

---

## Krok 2 — Szablon planu researchu

Utwórz jeden plik planu. Każdy agent dostaje ten plan:

```markdown
---
run_id: <generated-unique-id>
agent: <claude|codex|gemini|cursor>
skill: vc-research
project: <repo-name>
status: in-progress
---

# Research Plan: <title>

## Problem

<co-defined problem statement>

## Questions

1. <specific, answerable question>
2. ...

## Mandatory tools

- loctree MCP (repo-view, slice, find, impact) — for codebase questions
- Brave Search or WebSearch — for external ground truth

## Encouraged tools (agent's choice)

- Context7 (resolve-library-id → query-docs) — for library docs
- WebFetch — for URLs found via search
- Codebase grep — for internal patterns (only after loctree mapping)

## Report format

Each question answered with: **Sources**, **Finding**, **Confidence** (high/medium/low), **Evidence**.
Conclude with **Synthesis**: recommended approach, alternatives, open questions, implementation notes.

## Constraints

- Append current year to search queries for freshness
- Prefer primary sources (official docs, RFCs, source code) over blog posts
- If two sources disagree, note the disagreement explicitly
- Do not hallucinate API signatures — verify them
```

`vc-research` zapisuje efektywny plan pod `$VIBECRAFTED_HOME/artifacts/<org>/<repo>/<YYYY_MMDD>/research/<run_id>/plans/<ts>_<slug>_research-plan.md`. Plany można rozdzielić na osobne domeny, ale każdy agent dostaje WSZYSTKIE plany — to niezależni researcherzy, nie specjaliści.

---

## Krok 3 — Zespawnuj research swarm

```bash
PLAN="$VIBECRAFTED_HOME/artifacts/<org>/<repo>/<YYYY_MMDD>/research/<run_id>/plans/<ts>_<slug>_research-plan.md"
vc-research --file "$PLAN"
```

Skrypty spawnu należące do repo pozostają wewnętrznym silnikiem. Nie dokumentuj surowych ścieżek `bash skills/...spawn.sh` jako entrypointu operatora.

Launcher utrzymuje jeden wspólny `run_id` i uruchamia skonfigurowane lane'y
headless na tym samym planie. Domyślne lane'y to claude + codex + agy. vc-frame
może wyświetlić run; jawna kompatybilnościowa lane terminalowa używa jednej
współdzielonej karty `research.kdl`. Rozbieżność między raportami ujawnia
martwe punkty.

Zaraz po spawnie operator dostaje launch card ze współdzielonym `run_id`, katalogiem runu, katalogiem raportów, ścieżką podsumowania i dokładną komendą oczekiwania. **Launch card to domyślna powierzchnia.** `observe --last` to narzędzie do drilldownu, nie podstawowe źródło prawdy.

---

## Krok 4 — Zbierz raporty

Raporty lądują w:

```
$VIBECRAFTED_HOME/artifacts/<org>/<repo>/<YYYY_MMDD>/research/<run_id>/reports/{claude,codex,gemini}.md
```

Launch card żyje pod `research/<run_id>/summary.md`. Metadane, transkrypty, surowe strumienie, prompty, launchery, layout Zellij zostają wewnątrz `research/<run_id>/logs/` i `research/<run_id>/tmp/`.

Poczekaj na wszystkie trzy przez dedykowany helper runtime'u:

```bash
vc-research-await --run-id <run_id>
vc-research-await --last     # newest swarm
```

Do inspekcji na poziomie transkryptu, gdy swarm jest w trakcie:

```bash
vibecrafted observe claude --last
vibecrafted observe codex --last
vibecrafted observe gemini --last
```

Nie traktuj ręcznych wywołań `observe --last` jako wystarczającej obserwowalności. Stan workflow domyślnie przechodzi przez metadane launchu, helper oczekiwania i trwałe ścieżki raportów.

---

## Krok 5 — Syntetyzuj (warstwowe slicowanie i reguły)

**Zanim zacytujesz choćby jedną linię któregokolwiek z raportów źródłowych, MUSISZ przeczytać każdy raport w całości przez warstwowe slicowanie.** Bez negocjacji.

Większość raportów ma 30-100KB. Narzędzia obcinają wyjście na ~25KB i zrzucają resztę do pliku z ostrzeżeniem „see path: ...". Pominięcie tego pliku, bo jest „długi", albo praca wyłącznie z tekstem ostrzeżenia to dokładnie ten tryb porażki, któremu ten skill ma zapobiegać. Synteza zbudowana z ostrzeżeń o obcięciu to halucynacja przebrana za eksperckość.

Per raport źródłowy:

1. Przeczytaj w całości przez slicowanie offset/limit w odcinkach ~1500-2000 linii (albo ~80 000 znaków).
2. Odnotuj pokrycie w sekcji syntezy „0. Coverage statement" — linie/bajty per raport źródłowy.
3. Jeśli raport jest zbyt duży na dostępny budżet, **PRZERWIJ (HALT)** i zgłoś granicę. NIE cytuj zakresów linii, których faktycznie nie przeczytałeś.

**Synteza = ekspercka opinia operatora zbudowana NA tych trzech raportach, NIE kopia.** Dwie sekcje: **A. Convergent (zdeduplikowane)** oraz **B. Signals (findingi pojedynczego agenta — potencjalnie kluczowe insighty)**. Reguły głosowania/większości jawnie odrzucone.

- **A. Convergent (Zbieżne)** — findingi, w których dwa lub trzy raporty się pokrywają, zredukowane do jednego stwierdzenia. Cytuj zgodne raporty z file:line. Jeśli jeden nie poruszył danego pytania, zaznacz to wprost (cisza ≠ niezgoda).
- **B. Signals (sygnały)** — findingi wyniesione tylko przez jednego agenta. NIE niższego priorytetu. Często to faktyczny kierunek, którego praca potrzebowała. Per sygnał: co (file:line) + dlaczego inni przeoczyli + verdict operatora (amplify / flag / acknowledge & reject) + uzasadnienie.

---

## Antywzorce

- Przekazywanie `claude|codex|gemini` do `vc-research` (niweczy sens — launcher jest swarmem)
- Dawanie każdemu agentowi innych pytań (muszą odpowiadać na TE SAME pytania dla triangulacji)
- Pomijanie syntezy i konkatenowanie raportów (wartość jest w delcie)
- Researchowanie rzeczy, które możesz zweryfikować przez przeczytanie jednego pliku (użyj loctree slice)
- Pisanie planu researchu bez użytkownika (Krok 1 jest wspólny)
- Ufanie blog postom ponad oficjalną dokumentacją
- Pozwalanie agentom researchować bez kontekstu loctree (zadają złe pytania)
- Przeskakiwanie do surowych wywołań `*_spawn.sh`, gdy `*-research` istnieje na realnej powierzchni helperów shellowych
- Patchworkowa synteza meta-artefaktu (konkatenacja verbatim 3 raportów)
- Synteza w trybie skompresowanym (sama parafraza operatora, bez referencji file:line)
