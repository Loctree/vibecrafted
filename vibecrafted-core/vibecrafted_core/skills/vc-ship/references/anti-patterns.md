# `vc-ship` — Anti-Patterns

## Anti-Patterns

- Launching without a mission file grounded in vc-init truth (the prompt is a
  hypothesis, not the ground truth).
- Watching gates or workers from inside a subagent — gate-nap class failure
  (`docs/runtime/AGENT_OPS.md`, Class 1); watchers live with the supervisor.
- Trusting silence: a missing report is indistinguishable from a dead worker
  until you check liveness (Class 2) — use `status`/`stage_worker`, don't
  wait out budgets on a corpse.
- Manual edits to `state.json` instead of verbs — the trace IS the product.
- Approving a stage without reading its report, or pronouncing "ready"
  yourself instead of handing the verdict to the gate.
