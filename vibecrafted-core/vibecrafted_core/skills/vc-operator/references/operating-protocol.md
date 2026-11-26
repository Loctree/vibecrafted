# vc-operator — Operating Protocol, Brief-Gate, Dispatch Law, Anti-Patterns & Output Shape

## The Brief-Gate — never dispatch a shell (scaffold-doctor)

Before firing ANY wave, the plan MUST pass the **scaffold-doctor** gate: every cut in the wave
atlas has a rendered `briefs/<wave>-<slot>_<slug>.md` with all 12 sections, atomic verifier-backed
acceptance, and a design doc for every `needs_design` cut.

- A thin `master-dispatch.md` with no per-cut briefs is a **shell (wydmuszka)** — refuse to dispatch it.
- If any cut lacks a brief, do NOT improvise it at fire time and do NOT fire without it. Return to
  `vc-scaffold` (Phase 5) to render the missing briefs, then re-gate.
- The gate is **machine-checked, not agent-promised** (`vibecrafted-server/control-core`) — the same
  artifact-as-truth gate every read-write cadence handoff (scaffold→implement, marbles→audit…) uses.

This is the operator-side half of the brief-per-cut rule: scaffold renders the briefs, operator
refuses to conduct without them. Together they make "the flow does not deliver" structurally
impossible — not a discipline the agent must remember.

## Operating Loop

1. Run or consume fresh `vc-init` evidence.
2. Read the plan and all cited files in full.
3. Reshape through `vc-scaffold` if the plan is not dispatchable.
4. Build the wave atlas.
5. Verify each cut against Loctree.
6. Pick agents through `WHY_MATRIX_TABLE.md`.
7. Render worker briefs from `DISPATCH_TEMPLATE.md`.
8. Scan each brief for insecure commands and hard-stop triggers.
9. Fire one wave at a time through `vibecrafted <skill> <agent>`.
10. Await durable artifacts.
11. Verify reports, gates, branch, and SHA.
12. Scan landed commits for secrets, personal data, local-only paths, local
    network topology, IP addresses, and internal documents.
13. Use recovery dispatch on stalls; never blind restart.
14. Update the tracker and append material decisions to the canonical journal.
15. Synthesize wave close-out.
16. Continue or stop at the unpermitted operator button.

## Dispatch Law

Every external worker dispatch goes through the framework launcher:

```bash
vibecrafted <skill> <agent> --file <brief>
```

No native subagents for fleet dispatch in operator mode. Native delegation is
allowed for parallel recon or small bounded research inside the operator
session, but dispatched worker slices need telemetry, launch cards, reports,
transcripts, meta, and awaitable state.

### Headless Worker Boundary

The vc-frame operator session is the **User Session**, not the worker process
host. Every ordinary fleet dispatch defaults to `headless`, including attended
work launched while `VC_FRAME_SESSION_NAME` is set. The worker owns durable run
state and transcript; vc-frame may project those surfaces, and closing a
projection must not stop the run.

- **CLI and MCP agree.** `vibecrafted <skill> <agent> --file <brief>` and
  `vc_run_launch` / `vc_launch` default to a detached headless worker.
- **Observation is explicit and durable.** Use `observe`, `await`, transcripts,
  run state, and Guardian settlement instead of treating a pane as liveness.
- **Terminal is an exception.** Pass `runtime="visible"` or
  `--runtime terminal` only for a provider path proven to require a TTY. Until a
  daemon-owned PTY broker exists, that compatibility path remains coupled to
  the terminal and does not inherit the survival guarantee of a headless run.
- **Interactive PTY stays human-owned.** `init`, `operator`, and bare
  interactive `resume` remain true User Session tabs.

## Anti-Patterns

- Acting like a solo implementer after the operator asked for orchestration.
- Dispatching before the plan is readable as a wave atlas.
- Re-firing a stalled wave instead of reading artifacts and issuing recovery.
- Spawning native subagents as substitutes for telemetry-backed worker dispatch.
- Silently downgrading model tier or violating agent fairness.
- Claiming wave green without report, gate, branch, and SHA evidence.
- Authoring worker commits or close-outs as if the operator did their work.
- Making a vc-frame tab or session the process owner for an ordinary worker.
- Pushing, merging, deploying, or publishing without written plan/session
  permission or an explicit operator button press.

## Output Shape

For progress:

1. Current state - wave, prompt, agent, run ID, branch/SHA if landed.
2. Evidence - report/gate/artifact status.
3. Decision - continue, recover, pause, or stop.
4. Next move - exactly one.

For final handoff:

1. Plan and wave coverage.
2. Worker outputs and SHAs.
3. Gates and unresolved risks.
4. Recovery actions taken.
5. Stop-point handoff: what button remains for the operator.
