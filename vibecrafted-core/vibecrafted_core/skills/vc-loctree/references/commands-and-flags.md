# Loctree CLI ↔ MCP Flags & Lossless Defaults (`0.15.1+`)

## Lossless Defaults

`context`, `body`, `env-truth`, `query where-symbol`, `crowd`, `focus`, `impact`, `find`, and `follow` emit full results by default unless an explicit cap (`--limit`, `--max-lines`, `--max-chars`, `LOCT_CONTEXT_LIKELY_TESTS_LIMIT`, `LOCT_CONTEXT_MEMORY_LIMIT`) is requested.

## Synced Parameters

- `context`: `scope[]`, `scope_mode` (`all`\|`any`), `aicx_project`, `format` (`json`\|`markdown`), `section`, `fresh`, `no_scan`, `fail_stale`.
- `slice` & `focus`: `consumers`, `no_consumers`, `depth`, `rescan`.
- `body`: `symbol` (or CLI `FILE:START-END`), `file`, `line_cap` / `--max-lines`, `max_chars`, `no_limit`, `rescan`.
- `find`: `mode` (`symbols`, `discover`, `literal`, `regex`, `where-symbol`, `who-imports`, `tagmap`, `crowd`), `whole_token`, `no_generated`, `group_by_file`, `count_only`/`slim`, `limit`, `offset`, `with_aicx`, `aicx_project`.
- `follow`: `scope` (`all`, `dead`, `cycles`, `twins`, `hotspots`, `trace`, `commands`, `events`, `pipelines`), `handler`, `class`, `limit`, `offset`.

## CLI-Only Operational Commands

- `loct occurrences <IDENT> [--compact | -c | --paths-only | --limit N --offset M]`
- `loct query <who-imports|where-symbol|component-of|swift-types> <TARGET> [--limit N --all --json]`
- `loct crowd [PAT] [--min-size N --include-tests --limit N]`
- `loct env-truth [--all] [--name VAR] [--paths P1,P2] [--fail-on KIND] [--json]`
- `loct findings [--summary]` · `loct doctor --cache --scope` · `loct routes` · `loct hotspots`
