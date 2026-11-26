# vc-operator — Taxonomy, Supporting Surfaces & Adjacent Skills

## Taxonomy

```yaml
vc-operator:
  kind: orchestration_posture
  scope: interactive_session
  meaning: dispatch, await, synthesize, recover, close waves
  autonomy: orchestration
```

`vc-operator` is not an implementation skill. It is the conductor posture for
a planned chain of work.

- `vc-partner` preserves and co-steers the original shape before or during
  strategy work.
- `vc-ownership` drives one product slice end-to-end.
- `vc-operator` conducts a fleet through a plan and stops at the operator
  button.
- `vc-init` opens the session with repo/runtime/intention truth; it is not a
  posture.

Skill invocation is not runtime invocation. If the operator says
`$vc-operator` inside the current conversation, the current agent adopts this
orchestration posture. A separate runtime run exists only when the operator or
framework launches `vibecrafted operator <agent> ...`.

See [CONTRACT.md](../CONTRACT.md) for the binding posture/runtime split.

## Supporting Surfaces (Mandatory Entrypoint)

Read [RUNNER.md](../RUNNER.md) first.

`SKILL.md` defines the posture. `RUNNER.md` is the deterministic runbook. The
other documents are supporting surfaces:

- [FLOW.md](../FLOW.md) - orchestration loop and artifacts.
- [TAXONOMY.md](../TAXONOMY.md) - operator posture vs runtime taxonomy.
- [FRAME.md](../FRAME.md) - Worker / Owner / Operator role boundaries.
- [GUIDE.md](../GUIDE.md) - wave atlas structure.
- [DISPATCH.md](../DISPATCH.md) and [DISPATCH_TEMPLATE.md](../DISPATCH_TEMPLATE.md) -
  worker brief contract.
- [AWAIT.md](../AWAIT.md) - await/recovery discipline.
- [AUTONOMY.md](../AUTONOMY.md) - autonomy boundaries and the operator button.
- [JOURNAL.md](../JOURNAL.md) - append-only operator journal.
- [RUNTIME.md](../RUNTIME.md) - runtime launch and artifact contract.
- [WHY_MATRIX_TABLE.md](../WHY_MATRIX_TABLE.md) - agent routing.

## Adjacent Skills

- `vc-init` - required orientation gate.
- `vc-scaffold` - plan authoring or reshaping before dispatch.
- `vc-ownership` - each worker may operate with ownership inside its slice; the
  operator owns the chain.
- `vc-partner` - shared strategy before a plan is dispatchable.
- `vc-marbles` - convergence when a slice fails on truth drift.
- `vc-audit` / `vc-review` / `vc-followup` - verification surfaces after waves.
- `vc-release` - outward ship once release actions are permitted by plan/session
  or the operator button has been pressed.
