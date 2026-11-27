# `vc-ship` — Supervisor Protocol & Lifecycle Verbs

## How To Fly (supervisor protocol)

1. **Mission first.** Compose the mission as a durable `.md` file under
   `~/.vibecrafted/artifacts/<org>/<repo>/<date>/plans/` — grounded in a real
   vc-init pass (Loctree atlas + AICX intents + git/risk truth), with explicit
   deliverables, hard constraints, and gates. `--file` delivers it verbatim to
   every stage worker.
2. **Launch** with the standard launcher above. Verify the launch receipt:
   run_id (`life-ship-…`), context atlas loaded, stage 1 accepted.
3. **Arm await immediately, supervisor-side** (never inside a subagent — see
   `docs/runtime/AGENT_OPS.md`): After dispatch, arm
   `vibecrafted await <agent> --run-id <id>` immediately, supervisor-side.
   Control-plane JSON, report files, transcripts, panes, and scheduled wakeups
   are diagnostic only, not wake signals. Hedging await with ad-hoc
   pollers/watchers is a Class 3 violation; fix `control_plane.await_run`, do
   not normalize the hedge. Stage report checks and `ship status --json` are
   diagnostics subordinate to that canonical await; `ship status --json`
   exposes `stage_worker` with `worker_dead_without_report` — the actionable
   death signal; the dispatcher also writes `worker_exit` /
   `stage_worker_exit` into `state.json` push-side when a worker dies.
   3-signal liveness: before declaring done, reconcile await verdict, terminal
   run meta, and worker pid dead; if a report is promised, confirm it exists.
   Two agreeing signals are enough to act, three to declare done; disagreement
   means treat as live and re-arm await. Known skew: rc=0-on-live and meta stuck
   `active`/`stalled` after real completion.
4. **Verify before every button.** Read the report; for WRITE stages confirm
   the commits and gates actually exist; for READ stages confirm no
   `read_phase_violation`. Honor worker steering from report frontmatter
   (`next_stage`, `next_agent`, `dou_index`) unless it is nonsense — then
   override with a verb.
5. **Drive with verbs, never with manual state surgery:**

   ```bash
   vibecrafted ship runs                       # list lifecycle runs
   vibecrafted ship status <run_id> --json     # truth before any button
   vibecrafted ship approve <run_id>           # baton → next stage (cargo-gated)
   vibecrafted ship approve <run_id> --force   # traced override of the cargo gate
   vibecrafted ship interrupt <run_id>         # stop a blind/dead continuation
   vibecrafted ship fallback <run_id> --stage <s>  # rewind the baton WITH cargo
   vibecrafted ship force-audit <run_id>       # suspicious WRITE output
   vibecrafted ship accept-dou <run_id> --finding "…"  # conscious, traced gap
   ```

   Dead worker recovery is always: `interrupt` → `fallback --stage <stage>` →
   `approve [--force]`. No baton cargo is lost.

6. **Report at the end, not along the way** (unless the operator asks
   otherwise): stages flown, corrections made, commits, gate colours,
   dou_index, and what release honestly did NOT verify.
