---
name: loctree
description: Structural and literal repository perception before edits, deletes, refactors, or unfamiliar-code work. Loctree maps scope, dependencies, consumers, exact occurrences, and blast radius; AICX supplies historical intent.
metadata:
  version: "3.1.0"
  loctree_value: "primary repo map for structural/literal repository work"
  aicx_value: "intent, session, and decision-context retrieval"
  dogfooding: "required for repo-impacting work"
---

# Loctree — imaging before surgery

Loctree supplies structural sight: repository shape, indexed literal occurrences,
dependency neighborhoods, definition sites, runtime bridges, and blast radius.
AICX supplies historical intent. Neither replaces direct source, manifests, tests,
or a real runtime probe.

## Canonical Structural Gate

For repo-specific work, this skill is the structural half of the `vc-init`
procedure. `Loctree:loctree` must produce or refresh the Code-Derived Application Map before implementation, review, release, pruning, or deletion.

If fresh `vc-init` evidence is absent, perform the init pass first and treat
workflow-specific repo work as blocked until repo truth exists. If a task is not
repo-specific, say so instead of pretending a map exists.

## Route by question (12 MCP tools ↔ `loct` CLI)

| Need                                       | `loctree-mcp`                                                                                          | `loct` CLI                                                      |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------- |
| Broad task / repo orientation              | `context(project, file?, task?, scope?, scope_mode?, aicx_project?, format?, section?)`                | `loct context --task "..." [--scope ... --scope-mode all\|any]` |
| Quick repository overview                  | `repo-view(project)`                                                                                   | `loct repo-view`                                                |
| Directory layout & LOC scan                | `tree(project, depth?, loc_threshold?)`                                                                | `loct tree [--files --match 'pat']`                             |
| Directory wiring                           | `focus(project, directory, depth?, no_consumers?, rescan?)`                                            | `loct focus path/ [--depth N] [--no-consumers]`                 |
| File dependencies and consumers            | `slice(project, file, depth?, no_consumers?, rescan?)`                                                 | `loct slice path/file [--depth N] [--no-consumers] [--rescan]`  |
| Complete symbol / range source             | `body(project, symbol, file?, line_cap?, max_chars?, no_limit?, rescan?)`                              | `loct body Symbol [--max-lines N] [--max-chars N]`              |
| Exact identifier occurrences               | `find(project, name, mode="literal", file?, whole_token?, no_generated?, group_by_file?, count_only?)` | `loct find Identifier`                                          |
| Definition and re-export sites             | `find(project, name, mode="where-symbol", file?)`                                                      | `loct find Identifier --where-symbol`                           |
| Broad symbol/parameter candidates          | `find(project, name, mode="discover", lang?, exported_only?, similar?)`                                | `loct find --discover Terms`                                    |
| Paged/terse literal evidence               | `find(project, name, mode="literal", offset?, limit?)`                                                 | `loct occurrences Identifier --compact`                         |
| Dead/cycles/twins/hotspots/runtime flow    | `follow(project, scope, handler?, class?, limit?, offset?)`                                            | `loct follow <scope>`                                           |
| Structural delta vs Git ref                | `diff(project, since, to?, with_aicx?, aicx_project?)`                                                 | `loct diff --since HEAD~1 [--with-aicx]`                        |
| Source-side silencer inventory             | `suppressions(project, kinds?, include_fixtures?)`                                                     | `loct suppressions`                                             |
| Conceptual smear (`0..15`) before polarize | `prism(project, task=["a", "b"], aicx_project?)`                                                       | `loct prism --task "a" --task "b"`                              |

CLI-only surfaces: `loct env-truth`, `loct findings`, `loct audit`, `loct coverage`, `loct doctor`, `loct routes`, `loct hotspots`, `loct query`. See [references/commands-and-flags.md](references/commands-and-flags.md).

Plain CLI `loct find` is exact identifier-boundary literal search. `--literal`
is an explicit alias. `--discover` is opt-in broad AST/parameter/regex/fuzzy
candidate discovery. Do not report discovery candidates as literal matches. Over MCP, pass `mode="literal"` explicitly when seeking exact occurrences (`find` defaults to `mode="symbols"`).

`context`, `body`, `env-truth`, `query where-symbol`, `crowd`, `focus`, `impact`,
`find`, and `follow` emit complete results by default; caps (`--limit`, `--max-lines`, `--max-chars`, `LOCT_CONTEXT_LIKELY_TESTS_LIMIT`, `LOCT_CONTEXT_MEMORY_LIMIT`) are opt-in only.

## Execution contract

1. Confirm repo root, branch/HEAD, dirty state, snapshot scope, and freshness (`--no-scan` / `--fail-stale` / `--fresh`).
2. Use `context` for broad work or route directly to the bounded structural tool.
3. Before editing a file, inspect `slice`. Before delete/rename, inspect `impact`.
4. Before creating a symbol, run literal find plus where-symbol, then read definitions with `body`.
5. Read exact source and run the closest real product gate before claiming success.
6. For destructive decisions, independently inspect manifests, generated wiring,
   dynamic loading/reflection, entrypoints, tests, and installed/live behavior.

## What Loctree does especially well

- Identifier boundaries avoid substring noise such as `LOCT_OPEN_BROWSER` versus
  `LOCT_OPEN_BROWSER_ENV`, or `hotspot` versus `hotspots`.
- Literal search can include tracked indexed files hidden by default recursive
  ignore rules while still declaring its snapshot universe.
- In live AICX and Vibecrafted checks, plain find matched independent exact-word
  counts (38/38 and 22/22); `where-symbol` narrowed them to the two meaningful
  definition/re-export sites.
- `slice`, `impact`, and `follow trace` connect a matching line to its role in the
  larger system. On Screenscribe, impact exposed 5 direct and 12 transitive
  represented consumers and trace joined the frontend/backend handler path.

These are demonstrated examples, not universal latency or coverage promises.

## Evidence boundaries

- A zero-consumer/dead result is a candidate, never permission to delete.
- Impact traverses edges represented in the current snapshot graph.
- Literal absence applies only to the stated indexed universe.
- Empty runtime/structural cards require a coverage check; they can be legitimate
  or evidence of a missing analyzer surface.
- Warm-cache speed says nothing about a cold rescan after tree drift.
- Large MCP payloads spill intact to `.loctree/mcp-response-payloads/*.full.json`; `context(format="markdown")` paginates whole `## ` sections via `next_section` without mid-section truncation.
- AICX memory is historical evidence, not current code truth.

Direct text search and file reads remain valid complementary tools for prose,
local detail, ignored/generated surfaces, and independent count verification.

If Loctree is wrong, stale, noisy, unsupported, or forces a fallback, append a
reproducible note to `~/.vibecrafted/loctree/loctree-fail.md`.

Report: snapshot/HEAD, scope and coverage, decisive evidence, what was verified
independently, residual uncertainty, and the next safe move.
