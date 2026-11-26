# vc-dispatch — Boundary Contracts & Execution Loop Reference

## Boundary contracts

Current `AGENTS.md` and `docs/public/dispatch/dispatch-schema.md` outrank historical
reference advice when substrate, ownership, journals, or approval semantics disagree.

- **Input**: briefs + tracker produced upstream (vc-scaffold / parent
  workflow) — OR, in a **fast wave** (see `references/waves-and-recovery.md`), authored by the dispatcher
  in-session from live findings. Hand back to the scaffold flow only when the
  work is genuinely unshaped; a Founder ordering a wave on evidence you
  already hold is not that case.
- **Context sensing**: this skill carries no canonical prompt template.
  Before composing prompts, sense the embedding context — parent skill,
  repo CLAUDE.md / AGENTS.md, vc-init evidence, existing plan artifacts —
  and verify coverage with the reverse checklist
  (`references/prompt-checklist.md`).
- **Output**: scoped worker commits and reports, supervisor verifier receipts,
  tracker state, and explicit integration disposition. Isolated delivery is not
  admission to the Living Tree. The designated integrator proves ancestry,
  merge-parent identity, or exact patch equivalence and rechecks the destination.
  Workers run their focused gates; the supervisor executes declared verifiers.
  Broad integration gates belong to the integrator. Formal `vc-audit` is invoked
  when the Founder requests it, not automatically for every bounded dispatch.
- **Journal and artifacts**: the Operator alone appends material decisions to
  `<repo-root>/.vibecrafted/THE_JOURNAL.md` (ignored, private, never committed).
  Workers return reports, not journal writes. Plans, briefs, trackers and reports
  live under `${VIBECRAFTED_HOME:-$HOME/.vibecrafted}/artifacts/<org>/<repo>/<YYYY_MMDD>/`.
  Use the launcher-supplied `VIBECRAFTED_REPORT_PATH`; preserve machine-owned
  `run_id` and `session_id` and honest report status.

## The loop

```
pre-flight → DISPATCH → SPANKO → SPRAWDZENIE → FLIP → BATON → next cut
                ↑           |  (pulse ticks; stall → recovery-dispatch)
                └── refire ←┘  (partial delivery / convergence pressure)
```

**Model pin per cut (pre-flight):** every cut declares a `model` pin that
matches its class — a mechanical, fully-briefed cut runs on a cheaper, faster
tier, a surgical or decision-bearing cut on a stronger tier. The pin
rides the plan into the launcher (`Cut.model` → `WorkflowLaunchSpec.model` →
the agent's model flag: `--model` for claude and cursor, `-m` for codex). An unpinned
cut runs on the account default — which is a non-decision, not a safe default:
pin deliberately, and treat a missing pin as a smell to resolve before launch.

1. **Pre-flight (once per line)**: test the verify commands from the briefs
   before the line moves — a gate that matches 0 tests is trivially green;
   demand ≥1 new non-trivial test in EXTRA. `grep -c` exits 1 on 0 hits
   (`|| true`); count ALL `test result:` lines (multiple binaries — `tail -1`
   lies); `cargo test` takes ONE positional filter, not two. For pytest
   gates, prove the `-k` selection is non-empty (`--collect-only -q` ≥1);
   prefer **semantic probe** verifiers that print the OLD value today and
   the NEW value only after the cut — run them live pre-flight. For a
   `.dispatch.toml` line: `--doctor` → probe/collect pre-flight → `--dry-run`
   with rendered-prompt placeholder gate → launch. Full field-learned rules:
   `references/toml-plan-preflight.md`.
2. **Dispatch**: one prompt file (never argv — `ps`-public, ARG_MAX, broken
   newlines), four layers per the checklist. Launch:
   `bash -c 'ulimit -f unlimited; vibecrafted <skill> <agent> --model <pin> --file <p.md>'`
   (shells may carry soft `ulimit -f` → SIGXFSZ/exit 153). **Headless by
   default:** CLI and MCP workers run in a detached process session even when a
   vc-frame User Session is live. Observe them through run state, transcript,
   `observe`, and `await`; a vc-frame tab may project those surfaces but must not
   own the worker process. Use `--runtime terminal` / `runtime="visible"` only
   for an explicit provider TTY exception, with the known compatibility cost
   that the worker remains coupled to that terminal. Record the receipt
   (run_id, report, transcript, meta) in the tracker.
   Never substitute a Founder model pin silently. A headless Worker runs gates
   in the foreground and finishes work, report and commit in its current turn;
   background completions cannot wake it. Supervisor-side await is a separate role.
3. **Spanko**: await through artifacts, never by staring at a pane. Use the
   dedicated command as the standard dispatcher loop. Canonical supervisor
   contract (see `docs/runtime/AGENT_OPS.md`): After dispatch, arm
   `vibecrafted await <agent> --run-id <id>` immediately, supervisor-side.
   Control-plane JSON, report files, transcripts, panes, and scheduled wakeups
   are diagnostic only, not wake signals. Hedging await with ad-hoc
   pollers/watchers is a Class 3 violation; fix `control_plane.await_run`, do
   not normalize the hedge.
   3-signal liveness: before declaring done, reconcile await verdict, terminal
   run meta, and worker pid dead; if a report is promised, confirm it exists.
   Two agreeing signals are enough to act, three to declare done; disagreement
   means treat as live and re-arm await. Known skew: rc=0-on-live and meta stuck
   `active`/`stalled` after real completion.
   `vibecrafted loop spanko --run-id <id> --agent <a> --verify '<cmd>' --tracker <tracker.md> --cut-id <cut> --then '<next dispatch>'`
   (framework cron heartbeat → control-plane await → verify → flip → baton),
   the lower-level `vibecrafted loop await-run --run-id <id> --agent <a> --then-cmd '<next>'`,
   or the await-watch probe
   (`vibecrafted-await-watch.sh --meta <meta.json>` — tail-await-die) as a
   visibility aid subordinate to the canonical await. A living worker gets ZERO
   interference; interrupting during its gate phase is pure loss.
4. **Sprawdzenie** (on worker exit): commit SHA exists → diff essence matches
   the brief → worker report's gate results and acceptance read → declared
   supervisor verifiers run. Avoid incidental duplicate builds, but a worker
   report or hook result never substitutes for required independent verification.
5. **Flip**: `[~]→[x]` only by the dispatcher (single writer), evidence =
   SHA + verifier receipts + who verified + integration disposition. Worker
   Acceptance checkboxes are a claim; they never sign for Operator or Founder.
   Source-green is not installed/live acceptance. Ledger rules: `references/ledger.md`.
6. **Baton**: next cut's prompt carries the line state — which cuts landed,
   which commits, which files moved, what the next worker must re-read.

## Skill Provenance Regeneration

Skill-byte changes require regenerating `skills/SKILL_PROVENANCE.json` via
`make skills-check UPDATE=1`; its tracked owner is `scripts/gen_skill_provenance.py`.
Preserve historical entries. Respect any generator-owner cut; consume its admitted
dependency without editing its code. After admission the integrator regenerates
the combined manifest once, rather than choosing a sibling's manifest wholesale.
