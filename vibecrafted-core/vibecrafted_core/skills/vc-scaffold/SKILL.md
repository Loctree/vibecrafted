---
name: vc-scaffold
version: 0.2.0
description: >
  Founder-first main brainstorm + planwriting — the armored lighthouse (pancerna
  latarnia) that carries a single cut, multiple cuts, or a whole project into the
  autonomous VC-ship pipeline. The WRITE entry of the read/write cadence: produces a
  measurable, self-sufficient plan a fleet executes with the Founder absent mid-flight.
  This skill should be used when the user asks to "scaffold", "plan this", "architect
  this", "break this down", "I have an idea", "design the system", "vc-scaffold",
  "zaplanuj to", "rozrysuj architekturę", "mam pomysł".
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Invocation for `vc-scaffold` (launcher `scaffold`)**
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
> | 1. User-launched worker | `vibecrafted scaffold <agent>`                                                                                                            |
> | 2. Interactive          | `/vc-scaffold` — execute **in this session**; use native subagents when required; do **not** externalize merely because a launcher exists |
> | 3. Agent-operator       | may dispatch the worker form above via `vc-dispatch` / operator lines while preserving this skill's identity                              |

> Freer native on some runs ≠ abandon external fleet. `vc-dispatch` and `vc-ship` keep their own identities.

<!-- /fleet-imperative -->

# vc-scaffold: Founder-First Planning — Pancerna Latarnia

## What this is

Scaffold is the **main brainstorm + planwriting** surface: take a vague idea and produce
a scoped, **measurable** build plan. It scales across one gate: a **single cut**, **multiple
cuts**, or a **whole project**. It is the **WRITE entry of the VC-ship read/write cadence** —
the plan it emits must be **self-sufficient and falsifiable** because in autonomous delivery
the Founder is absent mid-flight and sees only intermediate artifacts. Plan as if no one will
answer a question after dispatch. Front-load every decision here. See `references/cadence.md`.

The lighthouse orients before the fleet sails; the armor is the verification each cut carries.

## Operator Entry

Current `AGENTS.md` and `docs/public/dispatch/dispatch-schema.md` outrank historical advice on substrate, ownership, journals, or approvals. Honor the selected runtime (`local-native`, `local-worktrees`, VM); typed dispatch assigns non-integrators a supervisor-created `cut/<cut-id>` worktree (workers inherit, never create a second branch/worktree or integrate). Launch via `vibecrafted start` + `vibecrafted scaffold <agent> --prompt|--file`. Full rules & examples: [references/phases-and-operator.md](references/phases-and-operator.md).

## Canonical Orientation Gate (HARD-BLOCK — safety-critical)

Before any repo-specific analysis or planning, run or consume `vc-init` for the assigned repo.
**This is not a polish step — it is a safety bezpiecznik.** In autonomous VC-ship an agent that
composes from memory injects silent drift the Founder cannot catch live. Therefore: **no plan
until repo/runtime truth exists.** Missing `vc-init`/Loctree evidence is a process failure, not a
warning.

`Loctree:loctree` is the default structural perception. Use it before grep or docs-driven claims
to produce or refresh the **Code-Derived Application Map**:
`repo-view`, `focus`, `slice` (before edit), `impact` (before delete), `find` / `find --literal`
(before create), `follow` (dead/cycles/twins/hotspots). Find load-bearing hubs, twins, dead code,
drift, runtime entrypoints, blast-radius traps. If the task is explicitly non-repo/greenfield,
declare the **no-repo exception** in the report and name the orientation source used instead.

## Repository Work Doctrine

For repository work, start with Loctree as the map: use `loct context`,
`loct occurrences`, `loct body`, and `loct find --literal` before broad manual
search. Use AICX for intent and session context. Use rg/grep as fallback or
local magnifier, not as a replacement for structural mapping. If Loctree fails
or misses a surface, append feedback to `~/.vibecrafted/loctree/loctree-fail.md`.

## Founder Interview Gate (HARD-BLOCK)

Before Shape, record in frontmatter and Orient either (1) an existing interview source (journal, AICX session/extract, or founder brief with path/session ID + recovered decisions) or (2) founder answers from this conversation. Otherwise ask missing product questions first — no self-exemptions ("task was clear"). Full gate: [references/phases-and-operator.md](references/phases-and-operator.md).

## Pipeline Position

`[SCAFFOLD] → init → implement → review → workflow → followup → marbles → audit → polarize → dou → hydrate → release`
Scaffold is the WRITE entry (`references/cadence.md`). Clear bounded tasks skip to `vc-init`; `vc-ship` is the normal lifecycle umbrella, while a Founder-ordered bounded dispatch via `vc-dispatch` is supported when DRIVER preserves all artifact/manifest/brief gates. Full details: [references/phases-and-operator.md](references/phases-and-operator.md).

## The Six Phases

Run in order; each phase feeds the next. Detailed phase procedures & enforcement live in [references/phases-and-operator.md](references/phases-and-operator.md) and [references/artifacts-and-gates.md](references/artifacts-and-gates.md):

1. **Orient:** pass the Orientation Gate, map hubs/twins/cycles with Loctree, capture tech/team/time/scope constraints.
2. **Falsify:** try to break founding assumptions before shaping; every "it works" must survive a real probe.
3. **Shape:** decide 3–5 architectural boundaries, ruthless in/out scope, product identity, and scale shape ([references/output-shapes.md](references/output-shapes.md)).
4. **Defend:** split into 30–120 min cuts, each with `Vector`, 4-term delta, `state` marker, and non-fakeable `delivery-verifier` ([references/measure-core.md](references/measure-core.md)).
5. **Brief every cut (HARD-GATE):** emit master plan ([references/plan-template.md](references/plan-template.md)) AND render every `briefs/<wave>-<slot>_<slug>.md` with all 12 sections (`references/output-shapes.md`). No cut exists without a brief; no forbidden "too small" excuses.
   - **5.5 `DRIVER.md` (HARD-GATE):** self-sufficient Founder handoff with (1) full absolute paths, (2) why-annotated DAG + `⛔ Founder-button STOP`s, (3) `scaffold-doctor` + one `<plan-id>.dispatch.toml` validation + `/vc-ship` (or Founder-ordered `vibecrafted dispatch`) route, (4) verbatim `[ ]→[x]` rule, (5) status snapshot + `dou-index`, (6) R12 `## Odbiór (matryca wyników)` (all `[ ]`; `Founder [x]` only with `acceptance/founder.json`).
   - **5.6 `manifest.json` (HARD-GATE):** mandatory schema `"1"` inventory under `${VIBECRAFTED_HOME:-$HOME/.vibecrafted}/artifacts/<org>/<repo>/<YYYY_MMDD>/plans/<plan_id>/`; register every artifact; no `operator/` mirror or alias.
   - **5.7 YAML frontmatter (HARD-GATE):** every markdown artifact opens with YAML frontmatter (`plan_id`, `run_id`, `session_id`, `role`, `author`, optional `agent`, `date`, `project`). Never infer executor from `author`.
   - **5.8 `<plan-id>.dispatch.toml` (HARD-GATE):** `vibecrafted.dispatch.v1` contract covering every cut once; validate with `--doctor` and `--dry-run --json` before handoff; preserve model pins and headless workers.
   - **Compile-embargo plans:** follow [references/compile-embargo.md](references/compile-embargo.md); `--no-verify` covers local worker checkpoints only (never push), with integrator structural admission and full closure gates later.
6. **Serve & review:** serve multi-tab editable artifacts via `vibecrafted-server`, then pass `vibecrafted scaffold-doctor --plan <root> --repo <git-root>` (REFUSE = no handoff).

## Measurement (the armor)

Every plan unit is claim/outcome-addressable. **Only a verifier flips `[~]→[x]`; a claim never reaches `[x]` on its own.** `dou-index = |[x]| / total`; `[!]`/`[?]` → STOP → recovery-vector. Full alphabet + markers: [references/measure-core.md](references/measure-core.md).

## Critical Rules, Emil Closing & Prompt Verification

- **Hard gates:** research-first (`vc-init` + Loctree), founder interview/AICX evidence, per-cut briefs, `DRIVER.md`, `manifest.json`, `.dispatch.toml` (`vibecrafted.dispatch.v1`), `scaffold-doctor`, and three-signature R12 closure (`Founder [x]` only with `acceptance/founder.json`).
- **Storage hygiene:** durable artifacts NEVER go to `/tmp` or into the product checkout — only to `~/.vibecrafted/artifacts/<org>/<repo>/<DATE>/plans/<plan_id>/`. Operator's sole journal is ignored `.vibecrafted/THE_JOURNAL.md`.
- **Emil closing & verification:** every master plan, DRIVER, and brief ends with a unique motivational line, concrete CTA, and task-specific suchar + kaomoji ([Emil rail](../vc-operator/DISPATCH.md#closing-rail--the-emil-default-block)). Carry [Verification Rule](../VERIFICATION_RULE.md) into worker prompts; skill edits regenerate `SKILL_PROVENANCE.json` (`make skills-check UPDATE=1`).

Full rules, Emil closing, cross-references, anti-patterns & prompt verification: [references/rules-and-closing.md](references/rules-and-closing.md).

## Additional Resources

- **`references/measure-core.md`** · **`references/cadence.md`** · **`references/output-shapes.md`** · **`references/plan-template.md`** · **`references/compile-embargo.md`**
- **`references/phases-and-operator.md`** · **`references/artifacts-and-gates.md`** · **`references/rules-and-closing.md`**

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
