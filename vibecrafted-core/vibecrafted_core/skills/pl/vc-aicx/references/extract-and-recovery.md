# vc-aicx — Struktura wyjścia i odzyskiwanie logów (`aicx extract`)

## Struktura wyjścia:

```
[1-100/100 <score_range>] <org>/<repo> | <agent> | <date>
session(s): <session_id>
cwd: <cwd>
search result:
  > <result>
  > - <file_path>
  > [HH:MM:SS] assistant: <result>
  > [HH:MM:SS] user: <result>
source file(s):
$HOME/.aicx/store/<org>/<repo>/<date>/<type>/<agent>/<session_id>.md
```

## Narzędzie extract — użyj, gdy nie możesz odczytać wyniku agenta bezpośrednio:

- Wyjście zbyt duże dla narzędzia Read (>10k tokenów)
- Plik z wynikami narzędzi to surowy JSONL, nieczytelny dla człowieka
- Subagent się wykrzaczył, ale zostawił częściowy log
- Potrzebny kontekst poprzedniej sesji przed rozpoczęciem pracy

1.  Komenda

```bash
aicx extract --format {claude,codex,gemini,ollama} <INPUT_FILE> -o /tmp/aicx-extract-<basename>.md
```

`--format claude` parsuje JSONL z Claude Code, jak również strukturę json Gemini.
Rozszerzenie pliku nie ma znaczenia — `.jsonl`, `.txt`, `.output` działają
tak samo.

**Ścieżka wyjściowa**: Wyprowadź z nazwy pliku wejściowego. Użyj basename pliku wejściowego (bez rozszerzenia) jako nazwy wyjścia:
`/tmp/aicx-extract-<basename>.md`. Nigdy nie pytaj użytkownika o ścieżkę wyjściową.

## Gdzie znaleźć pliki wejściowe

```
$HOME/.claude/projects/<project>/<session-id>/tool-results/<hash>.txt     # Agent result (most common)
$HOME/.claude/projects/<project>/<session-id>/subagents/agent-<id>.jsonl  # Subagent session
/private/tmp/claude-<uid>/<project>/tasks/<task-id>.output               # Background task
$HOME/.claude/projects/<project>/<uuid>.jsonl                             # Full session
```

## Przydatne flagi

| Flaga                      | Efekt                                    |
| -------------------------- | ---------------------------------------- |
| `--conversation`           | Tylko user/assistant, bez szumu narzędzi |
| `--max-message-chars 8000` | Przycina długie wiadomości               |
| `--user-only`              | Tylko wiadomości użytkownika             |

## Przykładowy flow odzyskiwania

```bash
# 1. Extract (output path derived automatically from input basename)
aicx extract --format claude \
  $HOME/.claude/projects/-Users-foo-myrepo/abc123/tool-results/xy9z.txt \
  -o /tmp/aicx-extract-xy9z.md

# 2. Read the result
Read /tmp/aicx-extract-xy9z.md
```
