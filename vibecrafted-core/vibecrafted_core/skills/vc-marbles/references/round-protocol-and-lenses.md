# vc-marbles — Operating Model, Stabilization Lenses & Commit Rule

## Operating Model (Single Round)

One invocation = one bounded round.

1. **Accuse the present tree.** Every target traces to: tool output,
   failing gate, structural audit, or production-risk counterexample.
   **No evidence, no target.**
2. **Pick the smallest high-impact surface.** At most **3 targets**
   per round. Prefer high-severity breakage, high-frequency paths,
   silent failure modes, weak boundaries, issues that close a class
   of failure. When multiple surfaces disagree about reality or code
   forces a hidden product decision, **expose it but do not decide
   it** — that's `vc-polarize`'s job.
3. **Fortify.** Smallest set of changes that materially increases
   truth. Add missing scoping/auth, missing indexes, replace
   swallowed exceptions with actionable handling, add smoke tests,
   collapse duplicated contracts, delete rotten wrappers. Vetcoders
   axiom: **move on over backward compatibility** — cut cleanly if
   a local abstraction is rotten and blocks stabilization.
4. **Gate.** Narrowest credible gates first; broader if warranted.
   Minimum: syntax / lint for touched surfaces, tests covering the
   fortified path, relevant build/bundle checks. If a gate fails:
   report plainly, count regression, do not bury under narrative.
5. **Commit.** Exactly one round commit with the convention below.
6. **Report.** Save to
   `$VIBECRAFTED_HOME/artifacts/<org>/<repo>/<YYYY_MMDD>/marbles/reports/<ts>_marble_<run_or_round_id>_<agent>.md`.

**The worker stops here.** Do not self-extend into the next round.
Do not write instructions to your successor. The reception layer
decides what fires next.

Full single-round detail (instruments, lenses, locker-room rule)
lives in [`FLOW.md`](FLOW.md). Reception / convergence routing lives
in [`RECEPTION.md`](RECEPTION.md).

---

## Stabilization Lenses

If there is no exact task description pick the one matching the weakest live surface:

- **Access & Isolation** — auth, tenant scoping, role checks, permission boundaries
- **Data Health** — indexes, query plans, N+1s, schema hotspots, God tables
- **Errors & Observability** — swallowed exceptions, silent failures, missing alerts
- **Release & Runtime Resilience** — CI/CD gates, smoke tests, rollout safety, config drift

A round may touch one lens or a tightly coupled cluster. Do not force
pillar order if evidence says otherwise.

---

## Commit Rule

**One round = one commit.** No partial commits. No squashing across
rounds. No mining git history to decide your subject line.

Format:

```
marble: <one-line summary>

- <file>: <what changed and why>

Gate: <pass|fail>
Tests: <what ran>
Regressions: <count>
Round-ID: <opaque-id-if-provided>
```

---
