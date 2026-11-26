# vc-justdo — Posture, Launcher Modes & Ownership Reference

## Taxonomy

```yaml
vc-justdo:
  kind: standalone_posture_skill
  pipeline: none # NON-pipeline — not a VC-ship cadence phase (vc-implement is)
  posture: vc-ownership
  task_type: defined_by_prompt # implement | review | audit | research | fix | anything
  scope: interactive_or_headless_session
  questions: none # interactive: explore instead of interrogating
```

Skill invocation ≠ runtime invocation. `$vc-justdo` in chat = agent adopts the
Just Do posture. `vibecrafted justdo <agent>` / `vc-justdo <agent>` = separate
runtime run with skill id `justdo`.

## Two Modes & Launcher Invocations

**1. Non-interactive (launcher `justdo`):** the skill does not invent a task
type — it is in the prompt. Treat the prompt as closed for questions and execute.

```bash
vc-justdo claude --prompt 'Review my last five commits for X'
vc-justdo codex  --file  <broad-implementation-plan>.md
vibecrafted justdo gemini --prompt 'Audit the install path only'
```

**2. Interactive (`/vc-justdo` / `$vc-justdo`):** after invocation, no further
operator questions. Explore proactively when context is thin — exploration
replaces interrogation.

## `vc-ownership` Boundaries

From [`../../vc-ownership/SKILL.md`](../../vc-ownership/SKILL.md):

- **Move immediately (reversible):** edits, tests, docs, scoped refactors,
  local smoke runs, recovery commits.
- **Pause and realign (irreversible):** destructive git (`--force`, `reset --hard`),
  trunk merge, deploy/publish, spend, secrets/auth changes, production data mutations.

## Matrix Position & Verification

- `vc-justdo` stands **beside** the VC-ship pipeline (non-pipeline, ADR-0001).
  Use `vc-implement` when you want the structured VC-ship WRITE stage.
- Removing ceremony never removes proof: close with `[x]` via measure-core /
  walk-around / DoU rather than `[~]` on words alone. See
  [Verification Rule](../../VERIFICATION_RULE.md).
