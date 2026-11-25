---
name: aicx
version: 3.0.0
description: >
  An Intention Retrieval Engine for Agents' sessions. aicx (formerly
  ai-contexters) is a sophisticated parser tool that recovers and keeps the
  central history of agents' sessions in both human- and agent-readable format.
  Additionally it provides ad-hoc mode to recover agent output that is too large to
  read or is unreadable. Works on any Claude Code, OpenAI Codex, Gemini JSON,
  JSONL-format file regardless of extension (.jsonl, .txt, .output). Generates 
  output path automatically — no -o flag needed.
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

## Kiedy używać

Pozyskaj historyczny kontekst z poprzednich sesji AI dla tego projektu. Szukamy
_dlaczego_, nie ślepego zrzutu _jak_.

## Checkpoint orientacji

W pracy specyficznej dla repo uruchom lub skonsumuj procedurę `vc-init`, zanim
zamienisz pamięć AICX w rekomendację. `Loctree:loctree` to domyślny skill percepcji
strukturalnej dla tego przebiegu; użyj go, aby wygenerować lub odświeżyć
Mapę Aplikacji Wyprowadzoną z Kodu (Code-Derived Application Map), zanim zaufasz
starszym intencjom.

Jeśli brakuje świeżych dowodów z `vc-init`, najpierw wykonaj przebieg init i traktuj
rekomendacje specyficzne dla repo jako zablokowane, dopóki nie ma aktualnej prawdy repo.

AICX wyjaśnia, dlaczego wcześniejsi agenci tak postąpili. Loctree i bieżące bramki repo
decydują, czy ta intencja jest nadal prawdziwa.

## Doktryna pracy z repozytorium

W pracy z repozytorium zacznij od Loctree jako mapy: użyj `loct context`,
`loct occurrences`, `loct body` i `loct find --literal` przed szerokim ręcznym
przeszukiwaniem. Używaj AICX do kontekstu intencji i sesji. Używaj rg/grep jako
fallbacku lub lokalnej lupy, nie jako zamiennika mapowania strukturalnego. Jeśli Loctree
zawiedzie lub przeoczy jakąś powierzchnię, dopisz feedback do `~/.vibecrafted/loctree/loctree-fail.md`.

## Zestaw narzędzi:

1. `aicx` (cli) oraz `aicx-mcp` (stdio i streamable-http):
   a) referencja mcp: - `mcp_aicx_aicx_rank`
   Ranguje przechowywane chunki sesji AI wg jakości treści. Pokazuje gęstość sygnału, współczynnik szumu i etykiety jakości (HIGH/MEDIUM/LOW/NOISE) per chunk. Użyj --strict,
   aby odfiltrować szum. - `mcp_aicx_aicx_search`
   Fuzzy search po przechowywanych chunkach sesji AI. Zwraca wyniki z oceną jakości
   i dopasowanymi liniami. Wspiera normalizację polskich znaków diakrytycznych oraz opcjonalne
   filtrowanie po projekcie. - `mcp_aicx_aicx_steer`
   Pozyskuje przechowywane chunki po metadanych sterujących (pola frontmattera).
   Filtruje po run_id, prompt_id, agent, kind, project i/lub zakresie dat, używając
   metadanych sidecar — bez potrzeby grepowania systemu plików. Zwraca ścieżki chunków wraz z ich
   metadanymi sidecar do selektywnego ponownego wejścia.
   b) referencja cli: - pełną dokumentację można pozyskać, wywołując `aicx --help`.
   c) starsze metody - **`aicx_refs(hours=<retrieval_hours>, project="<project>", strict=true)`** — wylistuj przechowywane pliki kontekstu - **`aicx_rank(project=<project>, hours=168, strict=true, top=5)`** — priorytetyzuj najgęstsze chunki

   > To starsze punkty wejścia. Preferuj `aicx_search`; daje tę samą funkcjonalność i więcej.

2. `aicx intents` (cli):
   Wyciąga z historii sesji intencje projektu, wyniki, taski i decyzje architektoniczne do ustrukturyzowanych formatów.
   - Przykładowa ekstrakcja: `aicx intents -p <ProjectName> --emit json | tee intents.json`
   - Podsumowanie przez jq: `jq 'map(.kind) | group_by(.) | map({kind: .[0], count: length})' intents.json`
   - Lista ostatnich intencji: `jq -r '.[] | select(.kind == "intent") | "[\\(.date)] \(.agent): \(.summary[0:150])..." ' intents.json | sort -r | head -n 15`

## Co zrozumieć:

- Jaka była pierwotna intencja stojąca za architekturą?
- Jaką prowizorkę nałożono późną nocą, żeby „po prostu zadziałało"?

## Dyscyplina:

AICX to silnik pozyskiwania intencji, nie ślepe działo RAG.
Pozyskaj kontekst decyzji, a potem zweryfikuj ich aktualną prawdziwość w Zmyśle 2.

## Struktura wyjścia i odzyskiwanie logów (`aicx extract`)

Wyniki wyszukiwania zwracają nagłówki chunków z oceną (`[1-100/100]`, `session(s)`, `cwd`, dopasowane linie i ścieżki źródłowe `$HOME/.aicx/store/...`). Gdy wynik agenta lub surowy log JSONL jest zbyt duży (`>10k` tokenów) lub nieczytelny, uruchom `aicx extract --format {claude,codex,gemini,ollama} <INPUT_FILE> -o /tmp/aicx-extract-<basename>.md`, aby uzyskać czytelny zapis Markdown.

Pełna struktura wyjścia, lokalizacje plików wejściowych Claude/tasków, flagi CLI (`--conversation`, `--max-message-chars`, `--user-only`) i przykładowy flow odzyskiwania: [references/extract-and-recovery.md](references/extract-and-recovery.md).

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
