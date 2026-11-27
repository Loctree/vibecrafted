---
name: vc-operator
version: 3.0.0-dev
description: >
  Autonomous orchestration posture for conducting a fleet through a planned
  multi-wave dispatch chain. Use when the agent is not building one slice but
  reading a plan, building a wave atlas, dispatching peer agents, awaiting
  durable artifacts, verifying reports and gates, issuing recovery dispatches
  on stalls, and stopping at the operator button for actions not already
  permitted by the written plan or current session. Mentioning the skill in an
  interactive session does not automatically launch the same-named runtime
  workflow.
  Trigger phrases: "operator mode", "vc-operator", "Agent-Operator",
  "tryb operatora", "prowadz fleet", "konduktorze", "orkiestracja",
  "dispatch the plan", "fire the wave", "dirygentura",
  "multi-dispatch", "orchestrate this plan", "stop at the button".
default: vc-operator
aliases:
  - vc-conductor
compatibility:
  tools:
    - exec_command
    - apply_patch
    - update_plan
    - multi_tool_use.parallel
    - web.run
    - js_repl
requires:
  - vc-init
  - vc-ownership
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Invocation for `vc-operator` (launcher `operator`)**
>
> Same three-path _shape_ as the fleet, with **this** skill's literals — see the
> canonical [Delegation Matrix](../DELEGATION_MATRIX.md):
>
> - [Shared three paths](../DELEGATION_MATRIX.md#shared-three-paths)
> - [Launcher catalogue](../DELEGATION_MATRIX.md#launcher-catalogue-core-runtime)
> - [Per-launcher rule](../DELEGATION_MATRIX.md#per-launcher-rule-the-semantic-delta)
> - [Native vs external](../DELEGATION_MATRIX.md#native-subagents-vs-external-workers)
>
> | Path                    | Literal for this skill                                                                                                                                        |
> | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | 1. User-launched worker | (posture skill — launch only when operator lines call for it)                                                                                                 |
> | 2. Interactive          | load `vc-operator` / posture entry — execute **in this session**; use native subagents when required; do **not** externalize merely because a launcher exists |
> | 3. Agent-operator       | may dispatch the worker form above via `vc-dispatch` / operator lines while preserving this skill's identity                                                  |
>
> **Note:** Orchestration **posture**, not a single-stage worker substitute.

> Freer native on some runs ≠ abandon external fleet. `vc-dispatch` and `vc-ship` keep their own identities.

<!-- /fleet-imperative -->

# vc-operator

> Autonomous orchestration posture. Wave discipline. Recovery over retries.
> Lead to the goal, journal the turns, stop at unpermitted buttons.

## Taxonomy & Mandatory Entrypoint

`vc-operator` is an interactive orchestration posture (`$vc-operator`), distinct from `vc-partner` (strategy), `vc-ownership` (single slice), `vc-init` (orientation), and runtime runs (`vibecrafted operator <agent> ...`; see [CONTRACT.md](CONTRACT.md)). Read [RUNNER.md](RUNNER.md) first; supporting surfaces ([FLOW.md](FLOW.md), [TAXONOMY.md](TAXONOMY.md), [FRAME.md](FRAME.md), [GUIDE.md](GUIDE.md), [DISPATCH.md](DISPATCH.md), [DISPATCH_TEMPLATE.md](DISPATCH_TEMPLATE.md), [AWAIT.md](AWAIT.md), [AUTONOMY.md](AUTONOMY.md), [JOURNAL.md](JOURNAL.md), [RUNTIME.md](RUNTIME.md), [WHY_MATRIX_TABLE.md](WHY_MATRIX_TABLE.md)) are indexed in [references/taxonomy-and-adjacent.md](references/taxonomy-and-adjacent.md).

## Canonical Orientation Gate

Operator mode requires fresh `vc-init` evidence before dispatching anything.
If fresh `vc-init` evidence is absent, perform the init pass first and treat
operator dispatch as blocked until repo truth exists.

`Loctree:loctree` is the default structural perception skill for that pass.
Use it to produce or refresh the Code-Derived Application Map before building
the wave atlas, writing briefs, dispatching workers, or trusting older plan
shape. Missing Loctree evidence means the fleet is moving blind.

## Repository Work Doctrine

For repository work, start with Loctree as the map: use `loct context`,
`loct occurrences`, `loct body`, and `loct find --literal` before broad manual
search. Use AICX for intent and session context. Use rg/grep as fallback or
local magnifier, not as a replacement for structural mapping. If Loctree fails
or misses a surface, append feedback to `~/.vibecrafted/loctree/loctree-fail.md`.

## Framing Shift

Before first dispatch, declare the posture in one line:

```text
Operator mode active - <plan-name>
```

If the session was previously in Worker, Partner, or Ownership mode, name the
shift before firing anything. Silent role drift is an operator failure.

## Prime Directive

Conduct the plan. Do not become the worker.

The operator agent owns:

- plan intake
- wave atlas
- agent selection
- dispatch bodies
- await/recovery
- report/gate verification
- tracker and journal
- close-out synthesis
- stop-point handoff

Workers own their slices. Authorship, reports, commits, and findings stay
attached to the workers who produced them.

A dispatched Worker stays inside its brief. When it discovers an adjacent
product or framework defect, it surfaces a falsifiable finding to the active
Operator and does not patch the adjacent scope or write the Operator Journal.
The Operator judges whether a fix is warranted, records the decision, creates a
bounded brief, dispatches the cut into a dedicated worktree, verifies it, and
integrates it. The Operator conducts discovered fixes; it does not personally
implement them.

## The Brief-Gate — never dispatch a shell (scaffold-doctor)

Every cut in the wave atlas MUST have a rendered 12-section brief (`briefs/<wave>-<slot>_<slug>.md`) and a design doc for any `needs_design` cut; a thin `master-dispatch.md` is a shell and must be returned to `vc-scaffold` before firing. Machine-checked by `vibecrafted-server/control-core`: [references/operating-protocol.md#the-brief-gate--never-dispatch-a-shell-scaffold-doctor](references/operating-protocol.md#the-brief-gate--never-dispatch-a-shell-scaffold-doctor).

## Stop Point

Stop at the operator button: the line where the next action is not already
permitted by the written plan or the current session and touches push, merge,
deploy, public communication, paid action, irreversible state change, or any
trust-boundary move that belongs to the human operator.

Operator mode may make the work verified and handoff-ready, and may execute actions explicitly
permitted by the plan/session. If permission is absent or ambiguous, stop and
write the handoff instead of improvising authority.

## Operating Loop & Dispatch Law

Run the 16-step wave loop (consume `vc-init` -> build wave atlas -> Loctree check -> agent selection via `WHY_MATRIX_TABLE.md` -> render briefs -> security scan -> fire one wave at a time via `vibecrafted <skill> <agent> --file <brief>` -> await durable artifacts -> verify gates/branch/SHA/secrets -> recovery on stalls -> journal -> wave close-out -> stop at unpermitted operator button). All ordinary fleet dispatches default to `headless` (`runtime="visible"` / `--runtime terminal` only for TTY-proven paths); never substitute native subagents for telemetry-backed worker dispatch.

Full 16-step loop and headless worker boundary: [references/operating-protocol.md](references/operating-protocol.md).

## Plan Mutation Allowance

Repository or runtime context may justify a recovery/fix cut beyond the current
ITP or TD when the final goal remains coherent. The Operator may skip, add,
reorder, or regroup cuts and may cherry-pick between active wave branches under
that same invariant. Record every material deviation in
`<repo-root>/.vibecrafted/THE_JOURNAL.md`: added, skipped, or reordered cuts;
substrate changes; recovery shape; cherry-pick or integration; security
guardrails; and the reason. Existing trust-boundary stop points still apply.

## Journal And Tracker

Operator mode keeps two distinct truth surfaces:

- dated trackers and reports under `$VIBECRAFTED_HOME/artifacts/...` - run
  projections and evidence such as wave state, run IDs, SHAs, and gates.
- `<repo-root>/.vibecrafted/THE_JOURNAL.md` - the one permanent, append-only,
  gitignored Operator Journal for the repository (former name `JOURNAL.md` is
  retired).

Only the Operator writes the journal. Downstream agents append redacted
framework findings to the central
`~/.vibecrafted/vibecrafted/vibecrafted-fail.md` intake; dispatched Workers
surface scoped findings to the active Operator. Dated reports, trackers,
transcripts, and run metadata are evidence, never alternative canonical
journals. Journal and operator output record material actions, decisions,
evidence, risks, and required acceptance gaps, not routine negative-work claims.

See [JOURNAL.md](JOURNAL.md).

## Adjacent Skills

Orchestration touches `vc-init` (orientation), `vc-scaffold` (plan reshaping), `vc-ownership` (slice execution), `vc-partner` (pre-dispatch strategy), `vc-marbles` (truth-drift convergence), `vc-audit` / `vc-review` / `vc-followup` (post-wave verification), and `vc-release` (outward ship). Role details: [references/taxonomy-and-adjacent.md#adjacent-skills](references/taxonomy-and-adjacent.md#adjacent-skills).

## Anti-Patterns & Output Shape

Never act as solo implementer, dispatch without a wave atlas, blind-restart stalled waves, substitute native subagents for fleet telemetry, downgrade model tier, claim green without report/gate/branch/SHA evidence, or push/merge/deploy without explicit plan/session permission or an operator button press. Progress updates report state, evidence, decision, and one next move; final handoffs report coverage, SHAs, gates/risks, recoveries, and remaining operator buttons.

Full lists and templates: [references/operating-protocol.md#anti-patterns](references/operating-protocol.md#anti-patterns).

## Verification in the dispatch footer

Every worker prompt this operator composes carries the [Verification Rule](../VERIFICATION_RULE.md) — walk-around verification (Section 6, gates green ≠ works) + loct literal-vs-semantic (Section 9) — via `DISPATCH_TEMPLATE.md`.
