# vc-scaffold — Operator Entry, Pipeline & Phases 1–5 Reference

## Operator Entry

Current `AGENTS.md` and `docs/public/dispatch/dispatch-schema.md` outrank historical
reference advice when substrate, ownership, journals, or approval semantics disagree.

### Living Tree / Worktree Rule

Use the runtime selected by the Founder, plan, or launcher: Living Tree / `local-native`,
Fleet Worktrees / `local-worktrees`, Fleet VM local, or Fleet VM cloud. A single interactive
lane defaults to the current Living Tree when no other substrate was selected. Generic words
like "isolate" or "parallel" do not authorize moving it. Typed dispatch assigns each non-integrator
a supervisor-created worktree on `cut/<cut-id>` from the resolved baseline; workers inherit it,
never create a second branch/worktree or integrate themselves. Record parent/effective roots,
baseline and terminal SHAs, artifacts and integration disposition. Re-read before editing,
stage only owned paths/hunks, preserve foreign work, and report unresolvable overlap.

See [Living Tree Rule](../../LIVING_TREE_RULE.md).

### Dispatch

Enter the framework session, then launch through the command deck (not raw `skills/.../*.sh`):

```bash
vibecrafted start            # or: vc-start
vibecrafted scaffold claude --prompt 'Design the payment system'
vc-scaffold agy --prompt 'Plan migration from NextAuth to custom auth'
vibecrafted scaffold codex --file /path/to/idea-brief.md
```

Prefer `--file` for an existing plan/artifact and `--prompt` for inline intent.

---

## Pipeline Position

```
[SCAFFOLD] → init → implement → review → workflow → followup → marbles → audit → polarize → dou → hydrate → release
^^^^^^^^^^   WRITE entry of the read/write cadence (WRITE produces an artifact, READ falsifies it)
```

Scaffold is the WRITE entry. If the task is already clear and bounded, skip scaffold and start at
`vc-init`. The full cadence and the WRITE/READ classification live in `references/cadence.md`.

`vc-ship` remains the normal lifecycle umbrella. A **Founder-ordered bounded dispatch**
of an already shaped repair is a supported invocation through `vc-dispatch`; it does not
require all lifecycle stages or an emergency first. Preserve current orientation, complete
briefs, pinned models, doctor/dry-run, declared verifiers, and truthful receipts. When that
bounded dispatch consumes a scaffold package, all artifact/manifest/DRIVER/brief requirements
still apply; the selected execution route must be explicit in DRIVER.

---

## The Six Phases (1–5 Detailed)

### 1. Orient (research-first)

Pass the Canonical Orientation Gate. Map the existing landscape: `repo-view` for size/health,
`focus` on suspect modules, `slice` critical files, `tree` for hotspots, `follow` for dead/cycles.
Capture the **constraint space** — tech (stack/versions/infra), team (who builds, which languages),
business (time budget, deadline), scope (MVP vs full vision). Constraints shape everything.

### 2. Falsify (adversarial premise check)

Before committing to a shape, try to **break** the founding assumption. Ask "how would I know this
is a lie?" The 0-byte-passes-exit-0 lesson: every "it works" must survive a real probe, never a
green checkmark alone. Surface the failure modes the plan must defend against.

### 3. Shape (scale-adaptive)

Decide architecture by **boundaries and decisions** (3-5 that matter, not a thousand details), set
**scope** (in / out / explicitly out — be ruthless), and define **product identity** (material
metaphor, color roles, typography, tone, dark/light) — identity is an architectural decision that
feeds DoU and Decorate later. Then pick the **output shape by scale**: single-cut brief · wave-atlas+tracker · project read/write pipeline. See `references/output-shapes.md`.

### 4. Defend (gates first-class)

Break work into agent-sized cuts (30-120 min). **Every cut carries the measure-core**: a `Vector`
(stabilize/implement/recon/e2e), the four-term delta (`intent | baseline | claim | delivery`), a
`state` marker `[ ] [~] [?] [!] [x]`, and a **delivery-verifier** — the non-fakeable test that flips
`[~]→[x]`. A cut without a verifier ships as `[?]`, never `[x]`. See `references/measure-core.md`.

### 5. Brief every cut (HARD-GATE — this is the delivery mechanism)

Produce the plan from `references/plan-template.md` (master-dispatch: wave atlas + dependency
graph + the `state` column). **Then — non-negotiable — render a brief for EVERY cut.** A cut
without a rendered, well-formed brief does not exist as far as the plan is concerned. This is the
rule that turns a plan from a shell (wydmuszka) into something a fleet can execute.

For each cut, write `briefs/<wave>-<slot>_<slug>.md` from the 12-section dispatch template
(`references/output-shapes.md`): mission · context · files · acceptance · gates · out-of-scope ·
Living Tree etiquette (verbatim) · Loctree-first · recovery hint · branch+commit · report path.

**Enforcement (ported from `/brainstorming`, the flow that leads the agent by the hand):**

- **Checklist→TODOs:** create one TodoWrite item per cut-brief; complete them in order. The
  scaffold is not "done" while any cut-brief todo is open.
- **Hard-gate:** do NOT hand off to `vc-operator`, dispatch, or claim the scaffold complete until
  EVERY cut in the wave atlas has a matching brief with all 12 sections present.
- **Loop to green:** missing or malformed brief → loop back and render it. Single terminal state:
  all briefs rendered AND the scaffold-doctor gate passes.
- **Anti-pattern pre-emption (FORBIDDEN rationalizations):** "this cut is too small to need a
  brief", "we are 1:1 so no briefs needed", "the master-dispatch table is enough". A plan without
  per-cut briefs is a shell, not a plan. No exceptions, regardless of perceived simplicity.

---

## Founder Interview Gate (HARD-BLOCK)

Scaffold is founder-first, so it must not invent the founder's intent. Before Shape, record one of
these two forms of evidence in the plan frontmatter and Orient section:

1. a concrete existing interview source (operator journal, AICX session/extract, or founder brief),
   with its path/session ID and the decisions actually recovered from it; or
2. the founder's answers gathered in the current conversation.

If neither exists, ask the founder the missing product questions before writing the architecture
plan. "No interview was needed", "the task was clear", and "not asking did no harm" are forbidden
self-exemptions. This gate is the discovery intake; it does not authorize twenty mid-scaffold
questions after the decisions are captured.
