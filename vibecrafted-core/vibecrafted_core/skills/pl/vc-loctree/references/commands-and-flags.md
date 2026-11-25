# Loctree CLI ↔ MCP — flagi i bezstratne domyślne wartości (`0.15.1+`)

## Bezstratne domyślne zachowanie

`context`, `body`, `env-truth`, `query where-symbol`, `crowd`, `focus`, `impact`, `find` oraz `follow` zwracają pełne wyniki domyślnie, dopóki jawnie nie podasz limitu (`--limit`, `--max-lines`, `--max-chars`, `LOCT_CONTEXT_LIKELY_TESTS_LIMIT`, `LOCT_CONTEXT_MEMORY_LIMIT`).

## Zsynchronizowane parametry

- `context`: `scope[]`, `scope_mode` (`all`\|`any`), `aicx_project`, `format` (`json`\|`markdown`), `section`, `fresh`, `no_scan`, `fail_stale`.
- `slice` i `focus`: `consumers`, `no_consumers`, `depth`, `rescan`.
- `body`: `symbol` (albo w CLI `FILE:START-END`), `file`, `line_cap` / `--max-lines`, `max_chars`, `no_limit`, `rescan`.
- `find`: `mode` (`symbols`, `discover`, `literal`, `regex`, `where-symbol`, `who-imports`, `tagmap`, `crowd`), `whole_token`, `no_generated`, `group_by_file`, `count_only`/`slim`, `limit`, `offset`, `with_aicx`, `aicx_project`.
- `follow`: `scope` (`all`, `dead`, `cycles`, `twins`, `hotspots`, `trace`, `commands`, `events`, `pipelines`), `handler`, `class`, `limit`, `offset`.

## Komendy tylko w CLI

- `loct occurrences <IDENT> [--compact | -c | --paths-only | --limit N --offset M]`
- `loct query <who-imports|where-symbol|component-of|swift-types> <TARGET> [--limit N --all --json]`
- `loct crowd [PAT] [--min-size N --include-tests --limit N]`
- `loct env-truth [--all] [--name VAR] [--paths P1,P2] [--fail-on KIND] [--json]`
- `loct findings [--summary]` · `loct doctor --cache --scope` · `loct routes` · `loct hotspots`
