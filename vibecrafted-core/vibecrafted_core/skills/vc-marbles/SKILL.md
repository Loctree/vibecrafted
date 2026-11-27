---
name: vc-marbles
version: 7.0.0
description: >
  WRITE step that floods every crack with deliberate over-correction.
  Single workers see one round, one truth-forcing cut, one commit;
  the skill at swarm level produces an intentional excess of fixes —
  marbles in every hole — which `vc-polarize` then strips back to one
  axis. Use when implementation already exists but the codebase still
  lies: overgenerated surfaces, drift between runtime paths, false
  certainty from one-shot agent output, or a product that "works"
  while remaining fragile. Each worker invocation is isolated and
  blind to prior marble history. Trigger phrases: "marbles", "kulki",
  "stabilize", "stabilizacja", "loop until done", "reduce chaos",
  "fortify the foundation", "adultification", "rzuć kulki",
  "wypełnij pęknięcia".
default: vc-marbles
aliases:
  - vc-fortify
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
  - loctree
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Invocation for `vc-marbles` (launcher `marbles`)**
>
> Same three-path _shape_ as the fleet, with **this** skill's literals — see the
> canonical [Delegation Matrix](../DELEGATION_MATRIX.md):
>
> - [Shared three paths](../DELEGATION_MATRIX.md#shared-three-paths)
> - [Launcher catalogue](../DELEGATION_MATRIX.md#launcher-catalogue-core-runtime)
> - [Per-launcher rule](../DELEGATION_MATRIX.md#per-launcher-rule-the-semantic-delta)
> - [Native vs external](../DELEGATION_MATRIX.md#native-subagents-vs-external-workers)
>
> | Path                    | Literal for this skill                                                                                                                   |
> | ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
> | 1. User-launched worker | `vibecrafted marbles <agent>`                                                                                                            |
> | 2. Interactive          | `/vc-marbles` — execute **in this session**; use native subagents when required; do **not** externalize merely because a launcher exists |
> | 3. Agent-operator       | may dispatch the worker form above via `vc-dispatch` / operator lines while preserving this skill's identity                             |

> Freer native on some runs ≠ abandon external fleet. `vc-dispatch` and `vc-ship` keep their own identities.

<!-- /fleet-imperative -->

# vc-marbles — Deliberate Excess (Worker-Blind, Swarm-Wide)

> The `WRITE` step at the centre of the pipeline. Where `vc-followup` says
> **"falsify the spec claim, never touch the code"** and `vc-polarize`
> says **"cut back to one truth"**, this one says **"the worker sees
> the tree, not the factory — one round, one truth-forcing cut, one
> report; the swarm produces the excess that polarize then strips."**

---

## Operator Entry

### Living Tree / Worktree Rule

Runs in the operator's current checkout and current branch. Do not
move into a worktree unless explicitly asked. Re-read files before
editing, adapt to concurrent changes (other workers may have written
between your dispatches). The one sanctioned second mode is a Fleet Worktree dispatch (written plan, pre-committed verifiers, disjoint domains, single-thread integrator — see Living Tree Rule, Mode B); outside that formation, stay in the shared tree. See [Living Tree Rule](../LIVING_TREE_RULE.md).

## Canonical Orientation Gate

Every round begins with `vc-init`. No exceptions. Perceive through
live instruments before touching code: `Loctree:loctree` builds the
Code-Derived Application Map (structural map, dependencies, dead
code, hotspots); **aicx-steer** (project intentions, not prior round
reports); **semgrep / linters** (current quality surface); **git
status / recent commits**. Without `vc-init`, the agent invents its
own reality.

Standard launcher: `vibecrafted marbles <agent> --count <n> --prompt '...'` (or `--file <plan>` / `--depth <n>`). After dispatch, arm `vibecrafted await <agent> --run-id <id>` immediately using 3-signal liveness (await verdict, terminal run meta, dead PID + promised report) — never hedge with ad-hoc pollers (`docs/runtime/AGENT_OPS.md`). Unlike `implement`, `marbles` runs fresh agents in a convergence loop after code exists.

Full launcher examples and await liveness details: [references/launcher-and-await.md](references/launcher-and-await.md).
---

## Repository Work Doctrine

For repository work, start with Loctree as the map: use `loct context`,
`loct occurrences`, `loct body`, and `loct find --literal` before broad manual
search. Use AICX for intent and session context. Use rg/grep as fallback or
local magnifier, not as a replacement for structural mapping. If Loctree fails
or misses a surface, append feedback to `~/.vibecrafted/loctree/loctree-fail.md`.

## Purpose

`vc-marbles` is the COMPLETION step that turns the naturally overgenerated
output of agentic coding into a hardened, testable foundation. Each
individual worker is disciplined: one round, one bounded set of
targets, one commit. But the **swarm** of workers/rounds across an
initiative deliberately over-applies — marbles in every crack, even
the ones that perhaps should not be filled. The excess is the point.
`vc-polarize` later strips back to one truth.

Marbles does **not** attempt to solve product-level conceptual smear
(conflicting docs, split product directions). It exposes those
product decisions hiding behind "code issues" and leaves them for
`vc-polarize` to resolve and pick the single-truth final shape.

## Cost Awareness: Cold Start, Hot Loop

Cold start is expensive; repeated hot rounds over the same repository, task surface, failing gates, architectural intent, and prompt exploit cache heat to buy convergence pressure and completeness. Keep the substrate stable across rounds so `vc-polarize` can cut back to one truth with evidence.

Full cost model and cache-heat rules: [references/cost-and-cache-model.md](references/cost-and-cache-model.md).

## When To Use It

Use `vc-marbles` when:

- implementation exists but the codebase still lies (drift, fragile
  paths, swallowed errors, overgenerated wrappers)
- failing gates need to be driven to P0/P1=0
- the operator wants a convergence loop with `--count` outer iterations
- multiple agents need to fire across a fragile surface in a swarm

Do **not** use this skill when:

- the implementation doesn't exist yet — that's `vc-workflow` or
  `vc-implement`
- the question is "did the plan actually land?" — that's `vc-audit`
  (READ-ONLY)
- the question is "which competing truth wins?" — that's `vc-polarize`
- the diff just needs review without modification — that's `vc-review`

---

## Pipeline Position

`vc-marbles` is one of the WRITE steps in the quality cycle (example):

```
... → implement (W) → review (R) → workflow (W) → followup (R) → marbles (W) → audit (R) → polarize (W) → ...
```

The swarm's deliberate excess produces a surface that needs to be
falsified (`vc-audit`) and then cut back to one truth (`vc-polarize`).
Marbles is the **flood**; polarize is the **decisive cut**. Audit
sits between as READ-ONLY perception.

---

## Worker Doctrine & Instruments vs Gates

Workers are intentionally **blind to prior marble history**, acting only on the live tree while [`RECEPTION.md`](RECEPTION.md) tracks open findings and convergence across rounds. Run **instruments** (`loctree`, `semgrep`, `aicx-steer`) at the **beginning** to accuse fragile surfaces with evidence, and **tests** at the **end** as verification gates.

Full worker doctrine and instruments-vs-gates rationale: [references/worker-doctrine-and-instruments.md](references/worker-doctrine-and-instruments.md).
---

## Operating Model, Lenses & Commit Rule

One invocation = one bounded round: accuse the present tree with evidence, pick at most **3 targets** along the weakest stabilization lens (`Access & Isolation`, `Data Health`, `Errors & Observability`, `Release & Runtime Resilience`), fortify, gate, make exactly **one** `marble:` commit, and write the round report to `$VIBECRAFTED_HOME/artifacts/.../marbles/reports/`. **The worker stops here** — do not self-extend or instruct your successor (see [`FLOW.md`](FLOW.md) and [`RECEPTION.md`](RECEPTION.md)).

Full 6-step round protocol, stabilization lenses, and commit format: [references/round-protocol-and-lenses.md](references/round-protocol-and-lenses.md).

## Branch and Tree Guard

**HARD RULE: Never change branches. Never create branches in the
user's repo-root. Never create or move to a worktree during a marbles
run.** The operator chose the current branch — that decision is not
yours to revisit. If the path is too poisoned to continue safely,
return control to operator / runtime and name the substrate failure
in the report.

---

## Composition & Anti-Patterns

`vc-marbles` pairs with `vc-init` (required entry), `vc-audit` (downstream READ-ONLY falsification), `vc-polarize` (downstream WRITE cut to one truth), `vc-review`, and `vc-followup`. Avoid historical self-awareness, convergence cosplay, surface-area vanity, narrative inflation, parallel contamination, solving product smear in the worker, or self-extension.

Full composition notes, anti-pattern catalogue, and closing rail: [references/composition-and-antipatterns.md](references/composition-and-antipatterns.md).

## Finish Condition

Stop after the commit and report. After that **do not** self-extend.
If the implementation is complete but has high conceptual smear (competing
truths, fragmented product surface), it will be handed off to
`vc-audit` for falsification and `vc-polarize` to get a release candidate
grade sharpness and single-truth shape.

---

## Call to Action

Read [`FLOW.md`](FLOW.md) before your first round — it carries the
single-round protocol detail and the convergence loop semantics. Read
[`RECEPTION.md`](RECEPTION.md) before running as an operator /
orchestrator — it carries the swarm-level discipline and the
parallel-round routing. Then accuse the present tree.

---

## Closing Rail

The worker sees the tree, never the factory: one round, one commit, one report, then leave. See [references/composition-and-antipatterns.md](references/composition-and-antipatterns.md).

## Verify before the handoff

Before you report "done", walk around the truck — see [Verification Rule](../VERIFICATION_RULE.md): run the REAL artifact (launch the app/binary, not just `--version`), re-verify runtime, never trust upstream verification as proof, and check your own check. Gates green ≠ works.

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
