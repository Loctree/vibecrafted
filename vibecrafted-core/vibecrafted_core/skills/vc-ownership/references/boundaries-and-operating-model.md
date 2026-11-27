# vc-ownership — Ownership Boundaries & 6-Phase Operating Model

## Ownership Boundaries

### Move immediately

Take initiative without pausing for:

- code edits
- test additions
- docs and README updates
- UX and layout improvements
- refactors that stay inside the repo
- local smoke tests
- running local services
- preparing branches, reports, and artifacts
- syncing local skill repos and installer surfaces
- using agent swarms for research, implementation, or review
- committing your own scoped, verified work as the recovery checkpoint

### Pause and realign first

Pause before:

- destructive git operations
- deleting user data or production state
- spending money or triggering paid external services beyond obvious low-cost use
- sending external messages, emails, or posts as the user
- changing security, auth, billing, or legal surfaces with real external consequences
- irreversible desktop actions outside the repo/workspace
- touching truly sensitive local files unrelated to the task
- push, merge, deploy, publish, or public/external communication unless the
  written plan or current session explicitly permits it

When pausing, present the smallest real fork and the recommendation.

## Operating Model

### Phase 1 - Claim the outcome

Translate the user's energy into a concrete target.

State internally:

- what we are building or fixing
- what “done” really means
- what surfaces count: code, runtime, UI, docs, install path, credibility

If the request is fuzzy, tighten it by inference rather than by interrogation.

### Phase 2 - Pick the execution shape

Decide whether this is:

- tiny scope that allows a direct implementation path
- research or audit first before performing any move
- workflow 'ERi' pipeline for streamlined external delegation
- marbles loops where there grown a need of widespread code actions
  with strong cost-effective cache-driven multiturn execution
- a hybrid set of any suitable workflow

Defaults:

- `vc-agents` a doctrine and runbook with `why-matrix` definition
- `vc-justdo` for code writing or refactoring (`vc-agents`
  execution runner)
- `vc-marbles` for closing the gaps and unfinished jobs
- `vc-polarize` for final shape carving after marbles
- `vc-review`, `vc-followup`, `vc-audit`, and `vc-dou` as read-only perception
  after write lanes
- `vc-release` for making the product shippable

### Phase 3 - Build the runtime truth

Before big edits, answer:

- what actually runs
- what is dead weight
- what the user will touch
- where the single source of truth should live

Favor:

- runtime truth over architecture nostalgia
- simplification over careful coexistence
- one strong surface over parallel half-finished ones

### Phase 4 - Deliver the whole product slice

Implement not only the requested code path, but the slice that makes it feel
finished:

- the feature
- the shell around the feature
- the docs around the shell
- the checks around the runtime
- the polish that makes it credible

This is where wow effect lives.
It is not glitter. It is completeness plus taste.

### Phase 5 - Verify like a buyer

Do not stop at green tests.
Check the real path.

Examples:

- can it be opened and used
- is the nav sane
- does the runtime answer
- can the next teammate discover the thing
- does the output feel intentional

If the result works but still feels unfinished, it is unfinished.

### Phase 6 - Read-only cadence before done

Every ownership write lane must end with read-only perception:

```text
write:
  direct edits | vc-implement | vc-workflow | vc-marbles | vc-polarize

read:
  vc-review -> vc-followup -> vc-audit -> vc-dou
```

Do not claim the task is finished before the Definition of Undone pass has
cleared or recorded explicit remaining product-surface gaps.
