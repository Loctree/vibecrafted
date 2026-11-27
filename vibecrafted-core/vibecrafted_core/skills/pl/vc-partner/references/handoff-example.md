# `vc-partner` — Przykład komendy „pstryk”

### Przykład „pstryk”

„Pstryk” oznacza: oddeleguj przygotowane zadanie i od razu wracaj do rozmowy.
Działanie synchroniczne trwa tylko tyle, ile uruchomienie workera, zachowanie
receiptu i uzbrojenie odbioru ukończenia. Worker wykonuje zadanie, a partner
pozostaje obecny i zachowuje odpowiedzialność za odbiór oraz domknięcie wyniku.
Dla uzgodnionego zadania Codex / `gpt-6-sol` w osobnym worktree wykonaj:

```bash
PROMPT="${VIBECRAFTED_HOME:-$HOME/.vibecrafted}/artifacts/<org>/<repo>/$(date +%Y_%m%d)/plans/<plan_file>.md"
vc-workflow codex \
  --model gpt-6-sol \
  --repo "$(pwd)" \
  --worktree true \
  --file "$PROMPT" \
  --json
```

Zastąp placeholdery ścieżką rzeczywiście zapisanego briefu i zachowaj
uzgodnionego providera, model oraz runtime. Ustaw `PROMPT` przed komendą startu:
przypisanie przy tej samej komendzie nie zasila jej rozwinięcia `$PROMPT`.
`--file` wczytuje brief, a `--prompt` przyjmuje tekst inline. Zachowaj zwrócony
receipt runu i uzbrój odbiór ukończenia, zanim wrócisz do wspólnego myślenia.
