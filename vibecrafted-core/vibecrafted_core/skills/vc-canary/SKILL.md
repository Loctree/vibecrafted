---
name: canary
version: 2.1.0
description: >
  Truth-competition radar for a repo: detect components competing for the
  same class of truth (identity, authorship, reduction, finality, delivery,
  configuration) before they poison the runtime. Four phases: authority &
  freshness, structural candidates, parallel-implementation radar,
  ownership polarization. Evidence and classification only — never
  refactors. Use when the user asks to "canary", "truth radar",
  "parallel implementation radar", "truth collision", "semantic twins",
  "kto jest właścicielem prawdy", "skataloguj repo", "ownership catalog",
  or runs /vc-canary / vibecrafted canary.
---

<!-- fleet-imperative: v3 -->

> **Invocation for `vc-canary` (launcher `canary`)**
>
> Same three-path _shape_ as the fleet — see
> [DELEGATION_MATRIX.md](../DELEGATION_MATRIX.md):
>
> | Path                    | Literal                                    |
> | ----------------------- | ------------------------------------------ |
> | 1. User-launched worker | `vibecrafted canary <agent>`               |
> | 2. Interactive          | `/vc-canary` — execute **in this session** |
> | 3. Agent-operator       | `vibecrafted canary <agent>` via dispatch  |
>
> Root defaults to **`$PWD`**. Do not invent `vibecrafted workflow` as a stand-in.

<!-- /fleet-imperative -->

# vc-canary — truth-competition radar

## Mission

Agent-generated software fails in a specific way: **locally correct modules
appear faster than the system establishes global ownership of semantics.**
The result is not duplicate code — it is components competing for the same
class of truth: five identity concepts, two document reducers, five sources
of configuration, twenty active participants between input and delivery.

Canary answers one question, per decision axis:

> **How many places in this repo can answer the same runtime question —
> and which of them is the writer, the arbiter, the observer, the projection?**

Canary **detects** multi-authority. It does not presume multi-authority is
wrong: two implementations can be legal (runtime vs replay) — the agent
must **prove** that boundary, never assume it. Canary produces evidence and
classification, **never refactors and never proposes throne decisions as
findings** — implementation comes after QC, in cut skills, on the operator's
word.

Empirical basis: two independent production systems built by agents showed
the same disease (one: 5 identity concepts, 5 settings sources, 2 document
reducers, prism 11/12), found by the same protocol.

## Canonical Orientation Gate

Consume fresh `vc-init` evidence for the repo; if absent, run `vc-init`
first. Use `Loctree:loctree` (repo-view, focus, slice, impact, find,
follow) to materialize the Code-Derived Application Map that seeds the
axis candidates. Sensing planes via raw grep, docs, or "I remember this
repo" instead of Loctree organs is a process failure.

**Forbidden as inventory:** `loct context --full` `structural.files` (hub
ranking only). **Forbidden:** loading raw multi‑MB `snapshot.json` into the
model context.

## One-instrument law

Loctree is the **sole anatomical instrument**: `repo-view`, `focus`,
`slice`, `impact`, `find` (discover/literal), occurrences, `body`,
`follow`, `twins`, `crowd`, `hotspots` and `prism` are readouts of the same
instrument. `canary_cli` may only aggregate, validate completeness and
preserve Loctree evidence — never act as an independent source of
architectural truth. `grep`/`rg`/`awk`/`sed`/filesystem `find`/raw snapshot
rummaging are forbidden as inventory or absence evidence. When Loctree
cannot answer a required question: append the exact failure to the target
repo's `.loctree/loctree-fail.md`, classify the claim `UNRESOLVED`, and
never paper over the gap with fallback evidence.

## Phase 0 — Authority & freshness

No radar on a stale tree. Record, with receipts:

- exact repo, root, HEAD SHA; dirty-tree status; worktrees and nested repos;
- Loctree snapshot coverage: `canary_cli atlas --refresh` →
  `./.loctree/atlas/` (`repo-atlas.json`, `inventory.jsonl`,
  `coverage.json`); coverage `pass: true` required to proceed;
- commits reachable locally but absent from HEAD genealogy (`git cherry`,
  local/remote-only branches) — orphaned semantics is a radar input, not
  trivia.

## Phase I — Structural semantic candidates

High-scale pass: `loct repo-view`, tree, `focus`, `twins`, `crowd`,
`hotspots`. Goal is **not** findings — it is the list of candidate
**decision axes**: classes of truth this repo decides, and the files whose
names/roles suggest more than one component decides them.

Axis classes that recur (derive the repo's own; do not copy this list
blindly): identity, correction/text authorship, engine/orchestration
selection, document/state reduction, formatting, finality/seal, delivery,
configuration precedence, epistemic competitors (verifiers/replayers/reports
that judge similar truth without writing daily runtime).

## Phase II — Parallel Implementation Radar

For **each** axis, descend with receipts:

```
find --discover → exact occurrences (literal coverage) → body
→ slice / consumers → follow (trace / pipelines / events) → impact (when needed)
```

**Falsification of absence is mandatory.** Broad/semantic search yields
candidates; only the literal-coverage line ("scanned X of Y files") proves
where a decision does _not_ live. "I searched semantically and it looks
like one place" is an unproven claim — the exact failure mode this phase
exists to prevent.

An absence claim is admissible only when the quoted coverage receipt shows
**all** of: `offset == 0` · `emitted == total` · `truncated == false` ·
`universe.scan_complete == true` · relevant trust flags true. Census counts
**references** (call sites, consumers), never definitions alone — a
definition census once hid 141 call sites. No count may be quoted without
its pinned snapshot fingerprint.

Classify every competing pair:

| Verdict                | Meaning                                                   |
| ---------------------- | --------------------------------------------------------- |
| `SAME_SOURCE_OF_TRUTH` | both resolve to one authority; no competition             |
| `INTENTIONAL_VARIANT`  | legal parallel (e.g. runtime vs replay) — boundary proven |
| `DRIFTED_DUPLICATE`    | started equal, semantics diverged                         |
| `BYPASS_PATH`          | second path skips the authority on some inputs            |
| `FALSE_PARALLEL`       | looked parallel structurally; evidence dissolved it       |

Mark runtime weight with the legend:

- 🔥 direct collision in daily runtime
- ⚠ same responsibility in another stage or mode
- ◌ offline/test/alternate competitor

## Phase III — Ownership polarization

`loct prism` on the axis framings + manual adjudication. For each axis:
how many places can answer the runtime question; who is **writer**, who
**arbiter**, who **observer**, who **projection**. Findings are born here —
nowhere earlier — and each carries a classification:

| Class          | Meaning                                             |
| -------------- | --------------------------------------------------- |
| `CUT_BLOCKER`  | poisons daily runtime; blocks planned cuts          |
| `CUT_COHERENT` | fix folds naturally into an already-planned cut     |
| `FOLLOW_UP`    | real, not urgent; goes to backlog with evidence     |
| `OBSERVATION`  | multi-authority proven legal or dormant; watch only |

Every examined row additionally gets exactly one disposition:
`authority_edge` (resolves to the presumed authority) ·
`proven_non_runtime` (observer/projection/diagnostic with a proven
boundary) · `obsolete_residue` (dead competitor; candidate for a later
cut) · `UNRESOLVED` (Loctree evidence insufficient — recorded, never
silently dropped). Do not invent an owner to make the graph complete.

## Evidence, Verdict & Journal Contract

Every finding requires the full evidence schema (axis, competitors, pair verdict, legend, classification, loct proof, absence receipt), every run exits with one strict verdict (`AXES_CLOSED_CANDIDATE`, `AXES_OPEN`, `INSTRUMENT_INCOMPLETE`, or `LAUNCHER_CONTRACT_CONFLICT`) ending with `BUILD/LINT/TEST/RUNTIME=NOT_ASSESSED`, and history appends to `./.loctree/canary/JOURNAL.md`. See [references/evidence-and-journal.md](references/evidence-and-journal.md) for full schemas and verdict criteria.

## Report → discuss → decide (QC stop)

Canary mutates **no code** and seeds no memex/aicx silently. Output is the
journal entry + a report for the operator. Throne decisions, cut plans and
deletions happen after discussion, in their own skills, with canary's
evidence attached. Acceptance test for any canary change: re-run on a known
case study and reproduce previously manual findings **without being told
where to look**.

## Fleet mode (large repos)

Scale N dynamically from Phase I axes (N=1 Living Tree; N>1 Fleet Worktrees Mode B with worker-created frozen worktrees, per-scope scratchpads, pinned snapshot fingerprints, and N≤8 native / N>8 external dispatch). See [references/fleet-mode.md](references/fleet-mode.md) for the full substrate and dispatch rules.

## Scripts, Dependencies & Common Mistakes

Use `canary_cli.py` (`snapshot-path`, `repo-view`, `atlas --refresh`, `coverage`) with Loctree, `vc-loctree`, `vc-dispatch`, and `vc-delegate`/`vc-agents`. Never propose refactors, invent owners, claim absence without literal coverage, or overwrite the journal. See [references/scripts-and-mistakes.md](references/scripts-and-mistakes.md) for commands, dependency table, and full mistake catalogue.

## Verify before the handoff

See [VERIFICATION_RULE.md](../VERIFICATION_RULE.md). Green gates ≠ true
radar. Coverage `pass: true`, every finding carrying its full evidence
schema, and an appended (never rewritten) journal entry — required.

---

_v2 field evidence: 5 identity concepts, 5 settings sources, 20 active
participants between capture and delivery — found in a production
agent-built system by this protocol, 2026-08._
