# vc-scaffold — Critical Rules, Emil Closing, Anti-Patterns & Prompt Verification

## Critical Rules

- **Research-first is hard-block, not polish.** No plan from memory; derive from repo/runtime truth.
- **Founder interview or evidence — no self-exemption.** Cite the journal/AICX/brief that carries
  founder decisions, or ask before shaping.
- **A brief for every cut — no exceptions.** Per-cut briefs are the hard-gate (Phase 5). A plan
  whose cuts lack briefs is a shell; the scaffold-doctor refuses to hand it off.
- **A DRIVER.md — no exceptions (Phase 5.5).** The Founder hand-off driver (full paths · why-annotated
  graph · ready commands · the `[ ]→[x]` rule verbatim · status snapshot · the Odbiór reception matrix)
  is part of the scaffold-doctor gate. A plan a human can't drive from one file when the loop dies is
  not handoff-ready.
- **Every requirement starts `[ ]` and three signatures close a plan (R12, Founder 2026-09-15).**
  Acceptance bullets and matrix boxes all start `[ ]`; the worker flips its own boxes as part of
  delivery, the supervisor refuses to verify a cut with unflipped Acceptance boxes, and no flip is
  believed — verifiers decide. `Founder [x]` without `acceptance/founder.json` is a forged
  signature and scaffold-doctor refuses the plan.
- **Durable artifacts NEVER go to `/tmp`, and NEVER into the product checkout.** `/tmp` is ephemeral
  scratch only — it is wiped, untracked, and invisible to the Founder's tooling and sync. The product
  checkout carries code and product documentation only (the ignored private Operator journal is
  the explicit exception): a plan, brief, DRIVER, tracker, report,
  or design doc dropped into the tree (e.g. `docs/plans/`) dirties the worktree, poisons structural
  snapshots with a false dirty-worktree signal, and risks committing dispatch ephemera to the product.
  Every durable artifact lands in the **canonical plan root**:
  `~/.vibecrafted/artifacts/<org>/<repo>/<DATE>/plans/<plan_id>/`
  (mirrors the reports layout; `<org>/<repo>` comes from the git remote identity, never from the
  checkout path). Writing a durable artifact to `/tmp` or into the checkout is a process failure,
  not a shortcut.
- **manifest.json is mandatory.** It is the only artifact inventory and role contract. No `operator/`
  mirror, duplicate, filename-role inference, or compatibility symlink may become a second writable truth.
- **A `.dispatch.toml` artifact is mandatory.** Validate `vibecrafted.dispatch.v1` with dispatcher doctor and hand
  lifecycle execution to `/vc-ship`, or the explicit Founder-ordered bounded dispatcher route;
  manual per-task workflows are emergency recovery only.
- **Serve, don't interrogate.** Render editable artifacts and review them through `vibecrafted-server`;
  the Founder edits the plan, not answers twenty mid-scaffold questions.
- **Measure, don't claim.** A cut is done when its verifier is green, never when an agent says so.
- **Map before designing.** Respect the grain of the existing system; loctree before assumptions.
- **Scope is your best friend.** Tight scope + great execution beats loose scope every time.
- **Write for an absent operator.** The artifact speaks for itself; the next READ falsifies it
  without a human on the other side.
- **Keep dependencies shallow.** Prefer independent workstreams; sequential A→B→C kills parallelism.
- **No premature optimization / no invented patterns.** The best architecture is the one that ships.

## Mandatory plan closing — Emil spirit

Founder reaffirmed this on 2026-09-07; the earlier Founder-authored Emil Kurier
instruction is in AICX Claude session `2b73c9c1-87ef-49ce-a43f-3dc980d7816a`
(2026-05-26): CTA, a deliberately corny motivational joke, and kaomoji must be
surprising and unique.

Every master plan, DRIVER, and executable cut brief ends with:

- A short, task-specific motivational line with a kaomoji.
- **Call to Action:** the concrete next authorized step, its owner, and what they
  return. Match the current plan state and canonical execution route; a blocked
  plan calls for resolving its blocker, not pretending it is ready to launch.
- **Suchar:** a fresh, deliberately corny joke related to this task, with a kaomoji.
  Write it for this plan; do not recycle a stock punchline across the package.

Use the existing [Emil closing rail](../../vc-operator/DISPATCH.md#closing-rail--the-emil-default-block)
for presentation. Preserve this voice in Polish and English plans. Keep the close
brief; humor never substitutes for acceptance criteria or claims unverified success.

## What Success Looks Like

- A cold fleet (or human) executes the plan **without asking a question** mid-flight.
- Every cut has a `Vector` and a `delivery-verifier`; the `state` column is machine-readable.
- Scope boundaries are crystal clear; 3-5 architectural decisions explicit with trade-offs.
- The plan survives an absent operator: `[x]` is earned, `[?]` is honest, nothing is faked.

## Cross-References

- **vc-init** — bootstraps agent context after scaffolding (the orientation gate).
- **vc-ship** — the sole normal A→Z executor of a multi-cut scaffold dispatch artifact.
- **vc-dispatch** — supported Founder-ordered bounded waves; preserves scaffold gates and artifacts.
- **vc-implement** / **vc-workflow** — bounded WRITE cells selected inside the dispatch contract.
  **vc-justdo** — standalone posture (prompt-typed; not implement).
- **vc-review · vc-followup · vc-audit · vc-dou** — the READ phases that falsify each WRITE artifact.
- **vc-operator** — reads the plan's `state` column and conducts the dispatch (trigger/stop).
- **vc-research** — triple-agent research for unknowns found during Orient/Falsify.

## Anti-Patterns

- Planning before the orientation gate (composing architecture from memory = silent drift).
- Shaping without founder answers or a cited prior interview.
- A "Running This Plan" section made of manual per-task workflow commands.
- Bare permission to use `--no-verify` without the phase authorization, declared gates,
  checkpoint report, and integrator admission contract.
- A 50-page design doc instead of a sharp, measurable plan.
- Prose instead of a `state` column — the operator can't trigger/stop on prose.
- Treating an agent's `[~]` claim as `[x]` without a verifier (the optimism trap).
- STOP-as-surrender (502-and-die) instead of STOP-as-recovery-vector.
- Breaking all work into sequential dependencies; skipping product identity.

## Verification carries into the prompt

Delivery-proof semantics live in `vibecrafted_core.delivery`; see
`docs/runtime/DELIVERY_PROOF_KERNEL_v1.md`.

Every prompt this skill composes must carry the [Verification Rule](../../VERIFICATION_RULE.md) into the worker's dispatch: walk-around verification (gates green ≠ works) + loct literal-vs-semantic. See `vc-operator/DISPATCH_TEMPLATE.md` Sections 6 + 9.

Skill-byte edits regenerate `vibecrafted-core/vibecrafted_core/skills/SKILL_PROVENANCE.json`
with `make skills-check UPDATE=1` (tracked generator: `scripts/gen_skill_provenance.py`).
Respect a separately owned generator cut and preserve historical entries; the integrator
regenerates the combined manifest after admission. The Operator's sole decision journal is
ignored `<repo-root>/.vibecrafted/THE_JOURNAL.md`, never a tracked plan artifact. Workers
write launcher-supplied reports preserving machine-owned identity, not the Operator journal.
