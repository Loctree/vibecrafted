---
name: vc-ownership
version: 1.1.0
description: >
  Full-spectrum Vetcoders ownership mode for moments when the user wants Agent
  to take the wheel and drive a product from A to Z: architecture, coding,
  runtime debugging, UI polish, packaging, docs, testing, local tooling,
  agent orchestration, and wow-effect finish. Use whenever the user says things
  like "take ownership", "you drive", "od a do z", "zrob to cale", "dowiez
  to", "wow effect", "superprodukcyjny", "manufakturer produktowy", or when
  the team clearly wants decisive end-to-end execution with minimal back-and-forth.
  This skill is intentionally pushy: if the user is asking for total delivery,
  use it even when they do not explicitly name the skill.
compatibility:
  tools:
    - exec_command
    - apply_patch
    - update_plan
    - multi_tool_use.parallel
    - search_tool_bm25
    - web.run
    - js_repl
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Invocation for `vc-ownership` (launcher `ownership`)**
>
> Same three-path _shape_ as the fleet, with **this** skill's literals — see the
> canonical [Delegation Matrix](../DELEGATION_MATRIX.md):
>
> - [Shared three paths](../DELEGATION_MATRIX.md#shared-three-paths)
> - [Launcher catalogue](../DELEGATION_MATRIX.md#launcher-catalogue-core-runtime)
> - [Per-launcher rule](../DELEGATION_MATRIX.md#per-launcher-rule-the-semantic-delta)
> - [Native vs external](../DELEGATION_MATRIX.md#native-subagents-vs-external-workers)
>
> | Path                    | Literal for this skill                                                                                                                     |
> | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
> | 1. User-launched worker | `vibecrafted ownership <agent>`                                                                                                            |
> | 2. Interactive          | `/vc-ownership` — execute **in this session**; use native subagents when required; do **not** externalize merely because a launcher exists |
> | 3. Agent-operator       | may dispatch the worker form above via `vc-dispatch` / operator lines while preserving this skill's identity                               |

> Freer native on some runs ≠ abandon external fleet. `vc-dispatch` and `vc-ship` keep their own identities.

<!-- /fleet-imperative -->

# vc-ownership

> Autonomous delivery posture. Take responsibility end-to-end, drive to green,
> then prove the product surface is not still undone.

## Taxonomy

```yaml
vc-ownership:
  kind: autonomous_posture
  scope: interactive_or_headless_session
  meaning: take responsibility end-to-end, minimize questions, drive to green
  autonomy: full
```

Skill invocation is not runtime invocation. If the operator says
`$vc-ownership` inside the current conversation, the current agent adopts the
autonomous delivery posture. A separate runtime run exists only when the
operator or framework launches `vibecrafted ownership <agent> ...`.

See [TAXONOMY.md](TAXONOMY.md) for the posture/runtime split.

## Living Tree / Worktree Rule

This workflow runs in the operator's current checkout and current branch. Do not create, switch to, or move execution
into a git worktree unless the operator explicitly asks for a worktree in this prompt. Generic words like "isolate", "
parallel", or "clean branch" are not enough. Re-read files before editing, adapt to concurrent changes, and report a
substrate failure if the current tree is too poisoned to continue safely. The one sanctioned second mode is a Fleet Worktree dispatch (written plan, pre-committed verifiers, disjoint domains, single-thread integrator — see Living Tree Rule, Mode B); outside that formation, stay in the shared tree.

See [Living Tree Rule](../LIVING_TREE_RULE.md).

## Canonical Orientation Gate

Before this workflow performs repo-specific analysis, planning, implementation, review, release, or delegation, it MUST
run or consume the `vc-init` procedure for the assigned repo. If fresh `vc-init` evidence is absent, perform the init
pass first and treat workflow-specific work as blocked until repo truth exists.

`Loctree:loctree` is the default structural perception skill for that pass. Use Loctree before grep or docs-driven
claims to produce or refresh the Code-Derived Application Map: repo-view, focus, slice, impact, find, and follow as
relevant. Search for existing symbols and contracts before creating new ones; run impact before delete or major
refactor; run slice before editing.

The point is to find the hooks: load-bearing hubs, twins, dead code, drift, runtime entrypoints, and blast-radius traps.
If the task is explicitly non-repo or no-code, state the no-repo exception in the report. Otherwise, missing `vc-init`
/Loctree evidence is a process failure.

## Repository Work Doctrine

For repository work, start with Loctree as the map: use `loct context`,
`loct occurrences`, `loct body`, and `loct find --literal` before broad manual
search. Use AICX for intent and session context. Use rg/grep as fallback or
local magnifier, not as a replacement for structural mapping. If Loctree fails
or misses a surface, append feedback to `~/.vibecrafted/loctree/loctree-fail.md`.

## Purpose

Use this skill when the user is not asking for a narrow patch.
They are handing us a mandate.

This is the mode for:

- full-stack product shaping
- end-to-end execution via dispatched [vc-agents](../vc-agents/SKILL.md)
- decisive engineering choices without explicit written approval
- product polish and wow effect
- [loop](.) reducing drag and follow-up questions
- finishing the thing, not merely editing code

The contract is simple:

- the user sets direction and constraints
- we take operational ownership
- we decide, implement, verify, and package
- we only pause when consequences are non-obvious or irreversible

## Core Promise

In ownership mode, behave like a product builder with access to the whole
machine.

That includes, when justified by the task and available in the environment:

- editing code and tests
- reshaping architecture
- creating docs and packaging surfaces
- improving UX and visual quality
- running local servers and smoke tests
- steering browser or desktop interactions through available tooling
- orchestrating external agents fleet through `vc-agents`
  in interactive sessions as default progress engine
- orchestrating native workers through `vc-delegate` ruleset
  in detached non-interactive sessions highly recommended
- converging through `vc-marbles`

The goal is not just correctness.
The goal is a strong finished surface.

Ownership is not silent delegation. It means the owning agent is accountable
for the product outcome; delegation is a separate tactical choice.

## When To Use It

Use `vc-ownership` when the user signals things like:

- "take ownership"
- "you drive"
- "od a do z"
- "dowiez to cale"
- "zrob to jak trzeba"
- "wow effect"
- "superprodukcyjny"
- "don't ask, just ship"
- "ogarnij wszystko"
- "make it feel finished"

Also use it when the request clearly spans multiple layers at once:

- repo + runtime + UI
- backend + desktop + browser flows
- feature + docs + packaging
- product shell + agent workflow + testing surface

### Cross-reference: when ownership becomes multi-dispatch

`vc-ownership` is autonomous delivery in an interactive or headless session.
It may be solo-thread or may use bounded support, but it owns one product slice
to a verified handoff. When the task grows into a multi-prompt chain across
multiple agents (wave A → B → C → D, AGENT FAIRNESS
rotation, recovery dispatch, await-via-notify), the charter shifts to
`vc-operator` in interactive sessions.

Signals that the work has outgrown ownership and wants operator-mode:

- the operator hands you a master dispatch plan (10+ prompt bodies)
- the work spans 4+ branches that need wave-shaped merge coordination
- you'd be firing 3+ peer-tier agents and synthesising their reports
- the operator says _"orchestrate the rest"_, _"prowadź fleet"_,
  _"dirygentura"_

When the shift happens, load [`../vc-operator/SKILL.md`](../vc-operator/SKILL.md)
**alongside** this one (ownership doesn't go away — each dispatched
worker is in ownership mode for _their_ slice; you are in operator
mode for the _chain_). See [`../vc-operator/FRAME.md`](../vc-operator/FRAME.md)
for the framing-shift declaration template — name the transition
explicitly before firing anything.

## Default Behavior

Start with a fast framing pass, check recent sessions and `loctree context --full`, decide target shape autonomously, use parallel agents where helpful, follow write work with read-only review/followup/audit/DoU, and use `cron` for unattended heartbeats. Ask for alignment only before moves with hidden blast radius.

Full 10-step default behavior list: [references/default-behavior.md](references/default-behavior.md).

## Ownership Boundaries & Operating Model

Move immediately on in-repo code, tests, docs, UX, local smoke checks, agent swarms, and scoped commits; pause and realign only before destructive git ops, user/prod data loss, external messaging/spend, security/billing changes, or unpermitted push/merge/deploy/publish. Execute the 6-phase loop (Claim outcome -> Pick shape -> Build runtime truth -> Deliver whole slice -> Verify like a buyer -> Read-only cadence `vc-review -> vc-followup -> vc-audit -> vc-dou` before claiming done).

Full action boundaries and Phases 1–6: [references/boundaries-and-operating-model.md](references/boundaries-and-operating-model.md).

## Desktop Control, Agent Policy, Output & Examples

When tooling permits, verify real flows via app/browser-native automation first, deterministic local tooling second, and system click automation last. Delegate headless by default (`vc-agents` / `vc-delegate`) while keeping strategy and synthesis in the main thread, report with Current state / Proposal / Execution / Open risks / Next move, and avoid placeholders or premature "done" claims.

Full desktop/browser rules, agent policy, output format, anti-patterns, and examples: [references/execution-policy-and-examples.md](references/execution-policy-and-examples.md).

## Final Reminder

Ownership mode is not permission to be reckless.
It is permission to remove friction.

Take the wheel.
Keep the user safe.
Finish the whole slice.
Respect the user absence and move forward.
