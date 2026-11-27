---
name: vc-research
version: 1.3.0
description: >
  Standalone triple-agent research skill. Co-define the problem with the user,
  write a research plan, then spawn claude + codex + agy simultaneously on the
  same questions. Three independent reports come back. Synthesize into one
  gap-free research document ready for implementation. Use whenever the team
  needs ground truth before coding: unknown APIs, architecture decisions, library
  assessment, protocol research, best-practice survey, competitive analysis,
  or any situation where one agent's perspective is not enough. Trigger phrases:
  "research this", "zbadaj to", "triple research", "research swarm", "3 agenty
  research", "gap-free research", "zbadaj przed implementacją", "co mówi
  dokumentacja", "state of the art", "SoTA research", "porównaj podejścia",
  "analyze options", "research plan", "plan researchu".
compatibility:
  tools:
    - Bash
    - Read
    - Write
    - Agent
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Invocation for `vc-research` (launcher `research`)**
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
> | 1. User-launched worker | `vibecrafted research <agent(s)>`                                                                                                         |
> | 2. Interactive          | `/vc-research` — execute **in this session**; use native subagents when required; do **not** externalize merely because a launcher exists |
> | 3. Agent-operator       | may dispatch the worker form above via `vc-dispatch` / operator lines while preserving this skill's identity                              |
>
> **Note:** May default to multi-agent swarm; interactive still must not no-op into empty re-dispatch.

> Freer native on some runs ≠ abandon external fleet. `vc-dispatch` and `vc-ship` keep their own identities.

<!-- /fleet-imperative -->

# vc-research — Triple-Agent Research Swarm

> One perspective is an opinion. Three perspectives are evidence.

## Operator Entry

### Living Tree / Worktree Rule

This workflow runs in the operator's current checkout and current branch. Do not create, switch to, or move execution into a git worktree unless the operator explicitly asks for a worktree in this prompt. Generic words like "isolate", "parallel", or "clean branch" are not enough. The one sanctioned second mode is a Fleet Worktree dispatch (written plan, pre-committed verifiers, disjoint domains, single-thread integrator — see Living Tree Rule, Mode B); outside that formation, stay in the shared tree. Re-read files before editing, adapt to concurrent changes, and report a substrate failure if the current tree is too poisoned to continue safely.

See [Living Tree Rule](../LIVING_TREE_RULE.md).

## Canonical Orientation Gate

Before this workflow performs repo-specific analysis, planning, implementation, review, release, or delegation, it MUST run or consume the `vc-init` procedure for the assigned repo. If fresh `vc-init` evidence is absent, perform the init pass first and treat workflow-specific work as blocked until repo truth exists.

`Loctree:loctree` is the default structural perception skill for that pass. Use Loctree before grep or docs-driven claims to produce or refresh the Code-Derived Application Map: repo-view, focus, slice, impact, find, and follow as relevant. Search for existing symbols and contracts before creating new ones; run impact before delete or major refactor; run slice before editing.

The point is to find the hooks: load-bearing hubs, twins, dead code, drift, runtime entrypoints, and blast-radius traps. If the task is explicitly non-repo or no-code, state the no-repo exception in the report. Otherwise, missing `vc-init`/Loctree evidence is a process failure.

Launch via `vibecrafted start` (or `vc-start`) and the command deck (`vibecrafted research --prompt/--file ...` or `vc-research ...`, headless by default; never raw `skills/.../*.sh`). **Critical swarm semantics:** one invocation launches the whole swarm (`claude` + `codex` + `agy` from `${VIBECRAFTED_HOME:-$HOME/.vibecrafted}/config/research.yaml`); `vc-research <agent1> [agent2 agent3] ...` overrides lanes with the first agent (or `--synthesizer`) synthesizing. CLI forms and YAML schema: [references/flow-and-templates.md](references/flow-and-templates.md).

<details>
<summary>Foundation Dependencies</summary>

- [vc-loctree](../foundations/vc-loctree/SKILL.md) — structural awareness
- [vc-aicx](../foundations/vc-aicx/SKILL.md) — intentions and steerability

</details>

## Repository Work Doctrine

For repository work, start with Loctree as the map: use `loct context`,
`loct occurrences`, `loct body`, and `loct find --literal` before broad manual
search. Use AICX for intent and session context. Use rg/grep as fallback or
local magnifier, not as a replacement for structural mapping. If Loctree fails
or misses a surface, append feedback to `~/.vibecrafted/loctree/loctree-fail.md`.

## Purpose

Research a problem from three independent angles before writing code. The orchestrating agent co-defines the problem with the user, writes a plan, spawns claude + codex + agy on the same questions, then synthesizes findings into one gap-free document. This is the Research phase from `vc-workflow`, extracted as a standalone skill and upgraded with triple-agent triangulation.

## When To Use

- Unknown API, protocol, or library; architecture tradeoffs; best-practice or library assessment; integration research; any moment guessing costs more than verifying.
- **Do NOT use for:** single-file lookups (`loctree slice` + grep < 30s) or pure implementation (`vc-workflow` / `vc-delegate`).

## Research Safety

Research mode is **read-only** for the source repository.

- **Closure marker = filesystem artifacts**, not git (`$VIBECRAFTED_HOME/artifacts/<org>/<repo>/<YYYY_MMDD>/research/<run_id>/` with `report.md` + `meta.json` + `transcript.log`). No git commits needed.
- **No source mutation & no git writes:** leave working tree unchanged; write proposed fixes to the report artifact; Codex workers write the full markdown report to the given report path before exiting.

## The 6-Step Research Flow

1. **Co-define the problem** with the user (3–5 sentence statement: what, why, priors, boundaries) before writing a plan.
2. **Write one shared research plan** (`.../research/<run_id>/plans/<ts>_<slug>_research-plan.md`) with identical questions, Loctree/Search tools, and primary-source constraints — every agent gets ALL plans.
3. **Spawn the swarm once** (`vc-research --file "$PLAN"`) using the launch card (`summary.md`, shared `run_id`) as the default surface.
4. **Collect reports** in `reports/{claude,codex,agy}.md` via `vc-research-await --run-id <run_id>` (or `--last`), using `vibecrafted observe` only for drilldown.
5. **Synthesize** only after reading every source report **in full via layered slicing** (~1500–2000 lines / ~80k chars; HALT if budget exceeded). Separate **A. Convergent (deduplicated)** and **B. Signals (single-agent findings)** with operator verdicts; reject majority voting.
6. **Produce `synthesis.md`** (usually 3–8KB): keep the three source reports as separate files, cite `file:line` for every nontrivial thesis and dissent, never paste verbatim report blocks.

Full Step 2 plan template, Step 3 invocation forms/YAML schema/precedence, Step 4 await/observe commands, and Step 5 slicing rules: [references/flow-and-templates.md](references/flow-and-templates.md). Synthesis template: [references/synthesis-template.md](references/synthesis-template.md).

## Pipeline Integration

vc-research can be used:

- **Standalone** — research without a full ERi pipeline
- **As workflow Phase 2** — `vc-workflow` delegates here instead of single-agent research
- **Before vc-partner** — when partner mode needs ground truth before debug
- **Before vc-runtime/vc-delegate** — research feeds implementation plans

```
         ┌─── claude ──→ report ───┐
research │                         │
  plan ──├─── codex  ──→ report ───├──→ synthesis.md
         │                         │
         └────── agy ──→ report ───┘
```

## Anti-Patterns

Never run `vc-research` three times per agent, give agents divergent questions, skip synthesis or concatenate verbatim reports, skip layered reading, write plans without Step 1 alignment or Loctree context, trust blogs over primary docs, or call raw `*_spawn.sh`. Full list: [references/flow-and-templates.md](references/flow-and-templates.md).

---

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
