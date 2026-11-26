---
name: vc-polarize
version: 2.0.0
description: >
  WRITE step that strips back the marbles excess to one truth. Where
  the swarm of marble workers plastered every crack in deliberate
  over-application, polarize picks one axis, rejects the competing
  ones, and aligns runtime, tests, docs, artifacts, and public
  promises so they all agree. Gated on Loctree `loct prism` bands —
  `0..4 abort`, `5..8 memo`, `9..12 pass`, `13..15 doctrine`. Emits
  DoU / release handoff. Trigger phrases: "polarize", "vc-polarize",
  "wyostrz", "one sharp truth", "code smear", "prism score", "after
  marbles", "choose one axis", "decisive cut".
default: vc-polarize
aliases:
  - vc-cut
compatibility:
  tools:
    - Skill
    - TaskCreate
    - TaskUpdate
    - Bash
    - Read
    - Write
    - Edit
requires:
  - vc-init
  - loctree (prism support)
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Invocation for `vc-polarize` (launcher `polarize`)**
>
> Same three-path _shape_ as the fleet, with **this** skill's literals — see the
> canonical [Delegation Matrix](../DELEGATION_MATRIX.md):
>
> - [Shared three paths](../DELEGATION_MATRIX.md#shared-three-paths)
> - [Launcher catalogue](../DELEGATION_MATRIX.md#launcher-catalogue-core-runtime)
> - [Per-launcher rule](../DELEGATION_MATRIX.md#per-launcher-rule-the-semantic-delta)
> - [Native vs external](../DELEGATION_MATRIX.md#native-subagents-vs-external-workers)
>
> | Path                    | Literal for this skill                                                                                                                    |
> | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
> | 1. User-launched worker | `vibecrafted polarize <agent>`                                                                                                            |
> | 2. Interactive          | `/vc-polarize` — execute **in this session**; use native subagents when required; do **not** externalize merely because a launcher exists |
> | 3. Agent-operator       | may dispatch the worker form above via `vc-dispatch` / operator lines while preserving this skill's identity                              |

> Freer native on some runs ≠ abandon external fleet. `vc-dispatch` and `vc-ship` keep their own identities.

<!-- /fleet-imperative -->

# vc-polarize — Decisive Cut After Marbles

> The convergence WRITE step. Where `vc-marbles` says **"plaster
> every crack in excess"** and `vc-audit` says **"falsify, never
> touch"**, this one says **"strip back to one truth, reject the
> competing surfaces, align the world"**.

---

## Operator Entry

### Living Tree / Worktree Rule

Runs in the operator's current checkout and current branch. Do not
move into a worktree unless explicitly asked. Re-read files before
editing. The one sanctioned second mode is a Fleet Worktree dispatch (written plan, pre-committed verifiers, disjoint domains, single-thread integrator — see Living Tree Rule, Mode B); outside that formation, stay in the shared tree. See [Living Tree Rule](../LIVING_TREE_RULE.md).

## Canonical Orientation Gate

Before polarize runs, consume fresh `vc-init` evidence. Use
`Loctree:loctree` (repo-view, focus, slice, impact, find, follow)
to refresh the Code-Derived Application Map before grep / docs /
"I remember" claims. Polarize is allowed to read recent marbles
reports — this is deliberate. Workers stayed blind; polarize is the
synthesis step that needs prior convergence evidence.

Standard launcher:

```bash
vibecrafted polarize codex --task 'marbles versus polarize skills: polarize them'
vc-polarize codex --task 'installer public contract'
vc-polarize claude --file /path/to/prism-pack.md
vibecrafted polarize agy --prompt 'Choose one launch thesis after marbles'
```

When `--task` is present, the runner executes a fresh prism preflight
and only dispatches an agent for `pass` and `doctrine` bands:

```bash
loct prism --with-aicx \
  --task '<operator task>' \
  --task '<operator task> code truth' \
  --task '<operator task> product truth' \
  --json
```

`--with-aicx` is the default. `--no-aicx` only when explicitly needing
a repo-only prism pack. `--no-context-corpus` skips optional retention
pack emission. **No `--count`.** This is not another marbles engine.

---

## Repository Work Doctrine

For repository work, start with Loctree as the map: use `loct context`,
`loct occurrences`, `loct body`, and `loct find --literal` before broad manual
search. Use AICX for intent and session context. Use rg/grep as fallback or
local magnifier, not as a replacement for structural mapping. If Loctree fails
or misses a surface, append feedback to `~/.vibecrafted/loctree/loctree-fail.md`.

## Purpose

`vc-marbles` establishes **Code Truth** by asking _"what is still
technically false, fragile, or untested?"_ — its swarm produces
deliberate over-application across every crack.

`vc-polarize` establishes **Product Truth** by asking _"which one
concept or product boundary should now become authoritative?"_ — it
strips the excess back to one axis and aligns surfaces.

The job is to collapse ambiguity into an explicit contract:

- one boundary
- one owner
- one runtime proof path
- one artifact / report truth
- one public promise when the concept reaches users
- explicit rejected alternatives

This skill **does write code** — but only to align surfaces with the
chosen truth. It does not invent new surfaces. It cuts.

---

## When To Use It

Use `vc-polarize` when:

- a `loct prism` score lands in the `pass` (9..12) or `doctrine`
  (13..15) band
- `vc-marbles` has converged but multiple viable truths remain
- a concept or product surface is smeared across runtime, tests,
  docs, artifacts, and public copy
- a release is blocked because public surfaces contradict each other

Do **not** use this skill when:

- the prism score is `abort` (0..4) — stop, no polarize
- the prism score is `memo` (5..8) — emit a local memo only, no dispatch
- code is still technically false / fragile — that's `vc-marbles`
- the spec just needs verification, not selection — that's `vc-audit`

---

## Pipeline Position

`vc-polarize` is the **decisive-cut** WRITE step:

```
... → marbles (WRITE: excess) → audit (READ) → [POLARIZE: WRITE: cut] → dou (READ) → ...
```

Marbles produces the over-applied surface. Audit verifies what
landed. Polarize strips back to one axis.

---

## Core Vocabulary

Defines **Code Smear** (spread creating competing truths), **Prism Score** (how much a concept refracts across `loct context --task` framings — never a CI failure or file-count penalty), and **Polarization** (converging runtime, tests, docs, artifacts, and public surfaces onto one axis). Full definitions in [references/concepts-and-modes.md](references/concepts-and-modes.md).

---

## Modes

- **Concept Mode** — smeared architectural/runtime concept → one concept contract and proof path.
- **Product Mode** — smeared product/public surface → one product thesis and DoU / release handoff.

Full examples and scope in [references/concepts-and-modes.md](references/concepts-and-modes.md).

---

## Prism Score Bands

Score each axis 0..3 (Spread, Runtime Centrality, Authority Diversity,
Drift Risk, Closure Evidence). Total 0..15.

| Band     | Score range | Action                                                           |
| -------- | ----------- | ---------------------------------------------------------------- |
| abort    | 0..4        | Stop before agent dispatch. Show prism JSON path.                |
| memo     | 5..8        | Emit local memo + thin context-corpus example only. No dispatch. |
| pass     | 9..12       | Run full polarize pass with prism payload injected.              |
| doctrine | 13..15      | Run full doctrine pass with a regression-contract expectation.   |

Full axis criteria, lifecycle, gates, and context-corpus contract live
in [`PROCEDURE.md`](PROCEDURE.md).

---

## Output Contract

Write artifacts under `$VIBECRAFTED_HOME/artifacts/<org>/<repo>/<YYYY_MMDD>/polarize/` (`thesis.md`, `concept-contract.md`, `surface-map.json`, `decision-ledger.md`, `dou-handoff.md`, `release-brief.md`) or include the 11 mandatory report sections (`Polarized Thesis` through `Release Handoff`) in the injected report. Full layout and section order live in [references/output-and-anti-patterns.md](references/output-and-anti-patterns.md).

---

## Composition with adjacent skills

Requires `vc-init` and upstream `vc-marbles`, consumes `vc-audit` verdicts when resolving UNVERIFIED claims, and emits handoffs to `vc-dou` and `vc-release`. Full composition notes in [references/output-and-anti-patterns.md](references/output-and-anti-patterns.md).

---

## Anti-Patterns

Never average two viable axes, dispatch on `abort` / `memo` bands, split the audience, change copy without runtime proof, trust stale prism packs, or chain into downstream skills without an explicit ask. Full list in [references/output-and-anti-patterns.md](references/output-and-anti-patterns.md).

---

## Finish Condition

After the polarize pass:

- thesis written, single sentence
- rejected alternatives recorded with reasons
- surfaces aligned where runtime proof supports the chosen axis
- gates green for touched surfaces
- DoU + release handoffs written

Stop. Do not continue into DoU, hydrate, decorate, or release unless
the operator explicitly asked for that chain.

---

## Call to Action

Read [`PROCEDURE.md`](PROCEDURE.md) before your first polarize pass —
it carries the full lifecycle, the prism axis scoring detail, the
context-corpus contract, and the minimum-gates list. Then run a
prism preflight, check the band, and only dispatch for `pass` /
`doctrine`.

---

## Closing Rail

```text
=======================
Remember: polarize mode is permission to choose one truth, not
permission to invent new ones. The marbles flood is yours to strip,
not yours to extend. One thesis, rejected alternatives named, surfaces
aligned, gates green. Stop at the handoff.
( •̀ω•́ )✧
=======================

Suchar: Why does polarize never average two truths? Because the
average of two stars is dust.  (._.)
```

---

## Verify before the handoff

Before you report "done", walk around the truck — see [Verification Rule](../VERIFICATION_RULE.md): run the REAL artifact (launch the app/binary, not just `--version`), re-verify runtime, never trust upstream verification as proof, and check your own check. Gates green ≠ works.

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
