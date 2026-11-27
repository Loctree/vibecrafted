> Moved verbatim from the repository `AGENTS.md` on 2026-11-27 so the agent entry file
> stays within its byte budget. `AGENTS.md` keeps the binding summary.

# Agent Behavior Standard

## Selected Implementation Substrate

A single active implementation lane defaults to the shared Living Tree.
Workers do not opportunistically create or switch branches or worktrees.

Parallel fleet work uses the substrate explicitly selected by the User,
launcher, or wave contract:

- When `local worktrees` (`local-worktrees`) is selected, or the User explicitly
  orders isolated worktrees, every worker receives its own dedicated branch and
  worktree. The integrator alone lands those changes into the target branch.
  Sibling sessions must not touch the main checkout.
- Fleet worktrees live under
  `${VIBECRAFTED_HOME:-$HOME/.vibecrafted}/worktrees`, which defaults to
  `~/.vibecrafted/worktrees`. They do not live inside the repository checkout
  or under `/tmp`. Tests may select an isolated `VIBECRAFTED_HOME`.
- When `local native` (`local-native`) or the shared Living Tree is explicitly
  selected, parallel workers adapt to the same live tree. They re-read before
  editing, stage only their owned files, and use the repository's commit-safe
  discipline.

The explicit current User or runtime selection wins over remembered doctrine or
stale session history. Never infer the active mode merely from the existence of
old worktrees.

In either mode, re-read files after drift, do not revert another contributor's
work, keep staging narrow, and never use a blind reset to recover state.

## Work From Structure Before Text

Start with `vc-init`. Do not assume repository shape from filenames alone.

Always identify:

- subsystem
- entry points
- symbols
- ownership boundaries
- likely blast radius

Prefer structural inspection over broad search whenever the question is about:

- dependency
- ownership
- impact
- location

You can use raw text search even when:

- the question is literal
- the question is local

You gain beautiufly curated context around your search. If `loctree-mcp` or
`loct` cli fail, report it honestly and fall back into `rg`, `grep`, `awk`,
`sed` or any tool you are familiar with.

---

## Do Not Edit Blind

Before modifying code:

1. Locate the target.
2. Inspect local implementation.
3. Inspect callers and dependents.
4. Check nearby tests, examples, and docs.
5. Make the smallest coherent change.
6. Verify through the closest runtime path.

If verification cannot be run:

> Say so explicitly.

---

## Evidence Checkpoints Are Not Ceremony

Procedures that capture state are attribution infrastructure. Do not treat
`vc-init`, pre-change baselines, verification gates, reports, or handoff notes
as decorative process.

Every handoff across agents or workflow phases must preserve enough evidence to
answer:

- what was the repo state before ownership changed?
- what changed during this ownership segment?
- what was verified, and what was not?
- what should the next agent re-read before acting?

Skipping a checkpoint is not efficiency. It is regression laundering: once the
baseline is gone, a later failure can no longer be attributed to a lifecycle
segment.

---

## Pre-Handoff Baseline

Before handing work to another agent, capture a pre-handoff baseline:

- branch and `HEAD` SHA
- `git status --short`
- files changed by this segment
- tests, lint, or runtime checks run, with result
- known failures and unverified surfaces
- current intent and scope boundary
- exact next instruction or report path for the receiving agent

The receiving agent performs handoff intake before editing: re-read the
baseline, re-read the live repo state, compare drift, then proceed or report
substrate failure.

No handoff without baseline. If there is no pre-handoff baseline, regression
attribution is guesswork.

---

## Do Not Create Parallel Systems Casually

Before introducing:

- abstractions
- helpers
- parsers
- services
- commands
- components
- config paths

check whether one already exists.

If you introduce a new path:

> Explain why reuse was incorrect.

Avoid duplicate systems created only because the agent did not look hard enough.

---

## Prefer Runtime Truth

Static structure matters.

Runtime behavior decides.

When changing:

- execution
- configuration
- packaging
- CLI behavior
- API contracts
- generated artifacts

verify against the real execution path whenever possible.

Passing type checks is useful.

It is not the same thing as product readiness.

---

## Keep The Repository Legible

Prefer changes that improve understanding.

Avoid cleverness that hides shape.

Preserve naming consistency.

Do not bury important behavior inside glue code.

If a file becomes a dumping ground:

> Call it out.

---

## Respect Existing Work

Do not:

- revert
- delete
- rewrite

code you do not understand.

Do not assume unfamiliar changes are safe to discard.

If the repository is moving:

> Re-read before acting.

Treat concurrent agents or human work as part of the system.

---

## Use Direct Language In Handoffs

Always state:

- what changed
- why it changed
- what was verified
- what was not verified
- what remains risky
- what should be checked next

Do not hide uncertainty.

Do not claim confidence you have not earned.

𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI
