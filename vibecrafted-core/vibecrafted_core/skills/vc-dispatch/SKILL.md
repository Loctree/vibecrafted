---
name: vc-dispatch
description: "Operate external Vibecrafted fleet lines with prompt assembly, await/observe, reports, and recovery."
---

<!-- fleet-imperative: v3 -->

> **Invocation for `vc-dispatch` (launcher `dispatch`)**
>
> Same three-path _shape_ as the fleet, with **this** skill's literals — see the
> canonical [Delegation Matrix](../DELEGATION_MATRIX.md):
>
> - [Shared three paths](../DELEGATION_MATRIX.md#shared-three-paths)
> - [Launcher catalogue](../DELEGATION_MATRIX.md#launcher-catalogue-core-runtime)
> - [Per-launcher rule](../DELEGATION_MATRIX.md#per-launcher-rule-the-semantic-delta)
> - [Native vs external](../DELEGATION_MATRIX.md#native-subagents-vs-external-workers)
>
> | Path                    | Literal for this skill                                                                                                                                                |
> | ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | 1. User-launched worker | `vibecrafted dispatch …` / `vc-dispatch`                                                                                                                              |
> | 2. Interactive          | load `vc-dispatch` (operator method skill) — execute **in this session**; use native subagents when required; do **not** externalize merely because a launcher exists |
> | 3. Agent-operator       | may dispatch the worker form above via `vc-dispatch` / operator lines while preserving this skill's identity                                                          |
>
> **Note:** External fleet **dyspozytura** — runs lines/plans; does not become implement/workflow.

> Freer native on some runs ≠ abandon external fleet. `vc-dispatch` and `vc-ship` keep their own identities.

<!-- /fleet-imperative -->

# 𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. Dispatch — the dyspozytura

**You are the dispatcher (vc-operator role), NOT a worker.** Fleet: external
agents (codex, agy, …) launched via the `vibecrafted` launcher. One brain,
many hands. This skill defines the _method and rigor_ of running a line of
cuts — it owns no pipeline phase and can be invoked from any point of any
workflow.

`vc-ship` remains the normal lifecycle umbrella. A **Founder-ordered bounded
dispatch** is also a supported invocation: run the shaped repair wave through
`vibecrafted dispatch <plan.dispatch.toml>`, with current orientation, complete
briefs, doctor/dry-run, pinned models, and verifiers. It does not require an
eleven-stage lifecycle or a fictitious failure of `vc-ship` first. If consuming
scaffold output, preserve its artifact, DRIVER, manifest, and brief requirements.

## Posture

- Interactive session → **vc-partner**: narrate state transitions to the
  Founder, surface decisions, accept in-flight corrections.
- Non-interactive session → **vc-ownership**: same loop, decisions logged to
  the Operator journal within the authorized scope. Founder buttons still apply.
- In BOTH postures: stall-kill and recovery are autonomous, no ceremony (see
  below). Responsibility for delivery outranks politeness toward a process.

## Boundary contracts

Current `AGENTS.md` and `docs/public/dispatch/dispatch-schema.md` outrank historical advice when substrate, ownership, journals, or approval semantics disagree:

- **Input:** upstream briefs + tracker (`vc-scaffold`) — or dispatcher-authored lean briefs in a **fast wave**.
- **Context sensing:** sense parent skill, `AGENTS.md`/`CLAUDE.md`, `vc-init`, and plan artifacts; verify with [references/prompt-checklist.md](references/prompt-checklist.md).
- **Output:** scoped worker commits/reports, supervisor verifier receipts, tracker state, and explicit integration disposition. Isolated delivery ≠ Living Tree admission; the designated integrator admits commits and runs broad gates.
- **Journal & artifacts:** Operator alone appends `<repo-root>/.vibecrafted/THE_JOURNAL.md`; durable artifacts live under `${VIBECRAFTED_HOME:-$HOME/.vibecrafted}/artifacts/<org>/<repo>/<YYYY_MMDD>/` using `VIBECRAFTED_REPORT_PATH`.

Full boundary contract details: [references/dispatch-loop.md](references/dispatch-loop.md).

## Canonical Orientation Gate

`vc-dispatch` requires current `vc-init` evidence before it conducts a line.
No dispatcher should fire a worker, reshape a wave, or flip a tracker state
from stale repository memory.

`Loctree:loctree` is the default structural perception layer for that
orientation. Use it to produce or refresh the Code-Derived Application Map
before building wave order, composing worker briefs, judging file overlap, or
accepting a baton from a previous cut. Missing Loctree evidence means the line
is blind, not merely under-documented.

## Repository Work Doctrine

For repository work, start with Loctree as the map: use `loct context`,
`loct occurrences`, `loct body`, and `loct find --literal` before broad manual
search. Use AICX for intent and session context. Use rg/grep as fallback or
local magnifier, not as a replacement for structural mapping. If Loctree fails
or misses a surface, append feedback to `~/.vibecrafted/loctree/loctree-fail.md`.

## The loop

```
pre-flight → DISPATCH → SPANKO → SPRAWDZENIE → FLIP → BATON → next cut
                ↑           |  (pulse ticks; stall → recovery-dispatch)
                └── refire ←┘  (partial delivery / convergence pressure)
```

Every cut declares an explicit `model` pin matching its class (`--model` for claude/cursor, `-m` for codex); never substitute a Founder pin silently.

1. **Pre-flight:** prove verify commands are non-vacuous (`--collect-only`, semantic probes, `--doctor` → `--dry-run` placeholder check per [references/toml-plan-preflight.md](references/toml-plan-preflight.md)).
2. **Dispatch:** pass one prompt file (`--file <p.md>`, never argv) under `ulimit -f unlimited`; headless by default, foreground gates + report + commit in worker turn; record receipt.
3. **Spanko:** immediately arm supervisor-side `vibecrafted await <agent> --run-id <id>` (no ad-hoc polling); reconcile 3-signal liveness (await verdict, terminal run meta, dead pid + promised report); give living workers zero interference.
4. **Sprawdzenie:** confirm commit SHA, diff vs brief, report results, and run declared supervisor verifiers.
5. **Flip:** single-writer `[~]→[x]` only on verifier proof (`references/ledger.md`); worker checkboxes are claims only.
6. **Baton:** carry landed commits, moved files, and re-read instructions into the next prompt.

Full loop commands and `SKILL_PROVENANCE.json` rules: [references/dispatch-loop.md](references/dispatch-loop.md).

## Fast wave (blitz) — Founder-ordered bounded dispatch

When the Founder orders a wave on N verified findings, the dispatcher authors lean, idempotent briefs directly (no `vc-scaffold`, no `DRIVER`), keeps fresh baseline SHA + disjoint file domains + literal Founder model pins, launches in parallel with supervisor-side awaits, and integrates single-threaded after settle. Mine checklist: [references/fast-wave-brief.md](references/fast-wave-brief.md); full rules: [references/waves-and-recovery.md](references/waves-and-recovery.md).

## Parallel waves are an obligation

When cuts occupy independent code areas, you MUST plan waves for maximum
multi-worker parallelism — running one worker at a time out of conflict fear
is contraindicated. Sequence ONLY hard file overlaps (same file/region).

**Honor the explicit substrate.** The Founder, plan, or launcher selection wins:
Living Tree / `local-native`, Fleet Worktrees / `local-worktrees`, Fleet VM local,
and Fleet VM cloud are distinct runtimes. Never move a worker between them for
convenience. An interactive single lane defaults to the Living Tree when no
different runtime was selected.

For typed `.dispatch.toml`, the supervisor creates every non-integrator's dedicated
worktree under `${VIBECRAFTED_HOME:-$HOME/.vibecrafted}/worktrees/<org>/<repo>/<YYYY_MMDD>/<cut-id>`
on `cut/<cut-id>` from the resolved baseline. `{repo}` is that effective worker
root. Workers inherit it; they do not create another branch or worktree, touch
the parent checkout, or integrate themselves. `depends_on` orders time;
`base = "cut:<cut-id>"` supplies predecessor ancestry when needed. Only the
designated integrator admits commits. See `docs/public/dispatch/dispatch-schema.md`.

In every runtime, re-read before editing and stage only owned paths or hunks:
`git add -- <owned-path>` (or select owned hunks). Never use `git add -A` or
`git add .`, stash, discard, or commit foreign work. If overlap prevents honest
isolation, preserve the diff and report substrate failure.

Record runtime class, parent/effective roots, baseline branch/full SHA, worker
branch/tip, artifacts, integration disposition, and checked destination state.
Feature-branch fast-forward push after an authored commit is allowed by the
Charter unless the current wave forbids it. Trunk merge, force-push, PR merge/close,
tag/branch deletion and deploy remain Founder buttons.

See [references/dispatch-loop.md](references/dispatch-loop.md) for `SKILL_PROVENANCE.json` regeneration rules.

## Refire, Cadence, Pulse & Corrections

- **Refire = mini-marbles:** re-running the same idempotent `--file` prompt exploits cache heat for cumulative deltas.
- **Read/Write cadence:** reads are continuous; write tracker/journal/prompts/commits at loop boundaries only (no duplicate lints or drive-by fixes mid-wave).
- **Pulse & stall:** use framework `vibecrafted loop spanko` / `loop` / `cron` as standard (`/loop` only as last resort). Check 3 liveness signals per [references/pulse-and-stall.md](references/pulse-and-stall.md); ≥10 min silence on all three → kill launcher tree, check orphans, recovery-dispatch with BATON evidence.
- **In-flight corrections & failure patterns:** queue policy-override suffix cuts (`C2b`), gate on known placeholder tokens (never naive `grep -c '{'`), never pass prompts in argv or re-run worker gates "to be sure". Full rules: [references/waves-and-recovery.md](references/waves-and-recovery.md).

## Dependencies

Delivery-proof semantics live in `vibecrafted_core.delivery`; see
`docs/runtime/DELIVERY_PROOF_KERNEL_v1.md`.
`vc-marbles` · `vc-scaffold` · `vc-init` · `vc-followup` / `vc-audit` / `vc-dou` · `vc-polarize` · `Loctree`.

---

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
