<!-- loctree-advise: v1 -->

# Loctree + AICX + Vibecrafted Agent Operating Guide

> Loctree gives **sight**.
>
> AICX gives **insight**.
>
> 𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. gives **hands to craft products**.

This repository should be treated as a living system, not as a loose pile of files.

Before making structural assumptions, inspect the map.

Before changing behavior, understand impact.

Before creating new symbols, check whether the shape already exists.

Loctree is the default structural map for repository work. Skipping it usually costs time: dependencies, blast radius, symbols, runtime entry points, dead surfaces, duplicates, and exact occurrences are visible faster through Loctree than through manual rummaging.

AICX preserves intent history and decision context.

Vibecrafted closes the loop with proof, discipline, and shipping pressure.

---

# Operating Rule

For structural questions, start with Loctree (**NEW!** `v0.11.3` Now also for
literal occurrences).

### Preferred order

1. Loctree MCP
2. Loct CLI
3. Local tools (`rg`, `grep`, `awk`, `sed`, `cat`)
4. Manual inspection

### Before editing

| Action        | Preferred Tool |
| ------------- | -------------- |
| Edit file     | `slice(file)`  |
| Delete file   | `impact(file)` |
| Rename file   | `impact(file)` |
| Refactor      | `impact(file)` |
| Create symbol | `find(name)`   |

### Literal truth before assumptions

Use:

- `find --literal`
- `loct occurrences IDENTIFIER`
- `loct body SYMBOL`

before broad text search.

### Fallbacks are allowed

Use:

- `rg`
- `grep`
- `awk`
- `sed`
- `cat`

when Loctree cannot answer cleanly.

---

# Loctree Feedback Loop

If Loctree is:

- wrong
- stale
- slow
- awkward
- missing language support
- missing an important surface
- suggesting an obvious improvement

append a note to:

`~/.vibecrafted/loctree/loctree-fail.md`

### Rules

- Never recreate the file.
- Never overwrite the file.
- Always append.

### Valid entries

- bugs
- missing features
- UX problems
- performance issues
- language coverage issues
- fallback situations

Repeated reports are signal, not noise.

---

# Vibecrafted Feedback Loop

For external users and downstream adopters, the canonical intake channel for
Vibecrafted failures is:

`~/.vibecrafted/vibecrafted/vibecrafted-fail.md`

Use it for framework bugs, runtime mismatches, packaging or install failures,
missing agent or provider support, observability gaps, UX problems, misleading
help or documentation, and cases that forced a fallback. Append enough redacted
evidence for the Vibecrafted team to reproduce and prioritize the failure.

Inside this repository, the route depends on the agent role, not on whether the
finding happens to fit the current task:

- A dispatched Worker stays inside its brief. It captures enough evidence to
  make the failure falsifiable and surfaces the finding to the active Operator;
  it does not opportunistically patch adjacent scope, launch another fleet, or
  append the downstream intake log.
- The Operator autonomously decides whether the finding warrants a repair,
  using the wider repository, runtime, plan, and User context available in the
  current thread. If it does, the Operator records the decision in the
  canonical operator `journal.md`, creates a bounded brief, actively dispatches
  the repair into a dedicated worktree, verifies the result, and integrates it.
  The Operator conducts the fix; it does not implement the discovered product
  repair personally. This recovery cut may extend the active plan when the
  Operator judges it necessary, while normal trust-boundary stop points still
  apply.
- Agents working in downstream repositories use this file as intake. They do
  not enter the Vibecrafted checkout and patch it incidentally.

Before logging, capture the active `vibecrafted --version`, active runtime root
and generation, source checkout SHA when relevant, exact command and error, and
whether the failure belongs to source, installed-runtime, packaging, or
substrate truth. Verify executable and runtime provenance first; do not let PATH
shadowing create a false report.

### Rules

- Never recreate, truncate, overwrite, reorganize, or deduplicate the log.
- Always append at the end. Repeated reports are prioritization signal.
- On macOS, keep the canonical file protected with the `uappnd` filesystem
  flag. On platforms without that flag, the application-level append-only
  contract still applies.
- Never include secrets, tokens, credentials, PII or PHI, full private prompts,
  customer payloads, or raw session data. Redact them and describe their shape.
- For downstream intake, if an automatic helper is unavailable, append
  manually. Missing tooling is not a reason to skip a legitimate blocked
  finding.
- Triage the backlog periodically. Settle a finding by appending a new entry
  that references the original and records `fixed`, `superseded`, or
  `cannot-reproduce` with evidence. Never edit or delete the historical entry.

## Permanent Operator Journal

Every active Operator maintains one append-only journal rooted in the current
repository:

```text
<repo-root>/.vibecrafted/THE_JOURNAL.md
```

The repository-local `.vibecrafted/` directory is runtime state and remains
ignored by Git, `THE_JOURNAL.md` included (former name `JOURNAL.md` is
retired — do not recreate it): the journal is private to each machine
(Founder decision 2026-09-14) and is never committed. Do not introduce date-partitioned
canonical journals or a second journal system. Run-specific reports and
trackers may project or reference it, but they do not replace it. Record
material dispatches, awaits, stalls, recoveries, integrations, close-outs,
security guardrails, and every meaningful deviation from the active
Implementation Task Plan (ITP) or Task Definition (TD), including added,
skipped, reordered, or re-substrated cuts and why the final goal remains
coherent.

Journal actions and decisions, not negative activity. Do not record that an
agent did not edit a file, did not switch a branch, or did not create a commit.
Runtime metadata, Git, reports, and receipts already provide that provenance.
Worker closing rails and routine non-actions do not belong in the operator
journal.

---

# Why This Matters

Loctree changes agent work from:

> text rummaging

into:

> map-first engineering

The goal is not obedience.

The goal is:

- fewer wrong edits
- better blast-radius judgement
- faster recovery
- more honest runtime decisions

<!-- /loctree-advise -->

---

# Agent Behavior Standard

Binding summary; full text in `docs/agents/BEHAVIOR_STANDARD.md`.

- **Substrate.** One lane works in the shared Living Tree. Fleet work uses the
  substrate the User, launcher or wave contract selected: with `local-worktrees`
  each worker has its own branch and worktree under
  `${VIBECRAFTED_HOME:-$HOME/.vibecrafted}/worktrees` (never in the checkout or
  `/tmp`) and only the integrator lands changes; in a shared tree workers re-read
  and stage only owned files. The explicit current selection wins.
- **Structure before text.** Start with `vc-init`, then locate the target and
  read it, its callers, tests and docs. Make the smallest coherent change and
  verify it on the closest runtime path. If verification cannot run, say so.
- **One system.** Find the existing helper, parser, service, command or config
  path before adding one; a new path states why reuse was wrong.
- **Runtime truth.** Execution, configuration, packaging, CLI, API contracts and
  generated artifacts are proven on the real path; type checks are not readiness.
- **Existing work.** Never revert, delete or rewrite what you do not understand.
  Never recover state with a blind reset. Re-read after drift.
- **Handoff baseline.** Hand over branch and `HEAD`, `git status --short`, files
  changed, checks with results, known failures, scope and the next instruction.
  The receiver re-reads it and the live tree before editing.

## Founder Echo Packets

`!echo '<text>'` from the Founder is Founder input, not shell noise. For Codex it
is the realtime lane: it was sent now, even when it quotes earlier chat, while
other Codex channels can arrive late or replay after compaction. Do not assume
this for other runtimes until their harness is verified.

# Release And Install Doctrine

- **Never ship non-notarized** (Founder order 2026-08-26). Every macOS build
  handed to a person is notarized and stapled; `--no-notarize` is for pipeline
  debugging only. Headless notarization uses a Keychain profile
  (`NOTARY_PROFILE`, e.g. `vibecrafted-notary`); raw Apple-ID credentials are
  rejected without a TTY.
- **Own only your namespace.** Launchers only for `vc-*`, `vibecrafted*`,
  `vibecraft` and `telemetry`. Loct, aicx, prview and screenscribe come from their
  own channels (`scripts/install-foundations.sh`), never vendored or wrapped.
  Never overwrite another product's command; reclaim only by receipt path and
  digest, restore collision backups, leave no dependents dangling.
- **Host metadata is not payload.** `.DS_Store` is skipped by the carrier tar and
  inventory; every other rejection stays fail-closed.
- **Upgrades preserve the Founder.** An install never loses `[server]` config
  (`~/.config/vibecrafted/config.toml`), live frame sessions or running agents.
  Replacing the app bundle under a live workspace is Founder-gated.

# Repository-Specific Instructions

## Operator journal

Founder decision 2026-08-28: the decision log is `.vibecrafted/THE_JOURNAL.md`,
gitignored and never committed (the old `.vibecrafted/JOURNAL.md` is retired).
Read it at session start and before a course change a later agent
must inherit. Operators append material decisions; workers do not write here.

## Verification Expectations

- **Small edits:** `make check` (ruff, prettier, semgrep on changed files) plus
  the nearest pytest module, run with `env -u PYTHONPATH` (HAK-32).
- **Behavior changes:** a focused test that fails without the change, plus
  `make unified-product-contract-gate` when `vibecrafted_core/` or `scripts/`
  change. Rust: `cargo clippy --workspace --all-features -- -D warnings` and
  `cargo test`.
- **Release-impacting changes:** `scripts/build-portable-release.sh` from a clean
  commit and one `make dmg RELEASE_FLAGS=--snapshot-donors`, then
  `gh run list --workflow "Release source gate" --limit 1` on the tag (HAK-30).
- `tests/tui/*` and `vibecrafted-core/tests/*` run as separate pytest
  invocations (conftest collision). Use an isolated `VIBECRAFTED_HOME`: pytest
  can leak a workspace into `~/.vibecrafted/control_plane` (HAK-31). Compare
  timing-sensitive failures against a clean `HEAD` before attributing them.
- DMG signing, notarization, the release-gate probe and vibecrafted-io deploys
  are Founder buttons, never run by workers.

## Safety Boundaries

No global reformat, licensing-header change, telemetry, network call or external
service without explicit instruction. Check license, maintenance state and
necessity before adding a dependency.

## Pointers

- Scaffold editor (LAW): `/scaffold/editor` is a single-document studio, with
  one `.artifact-panel.is-active` at a time: `docs/agents/SCAFFOLD_EDITOR_IA.md`.
- Omni-observer and Slack gateway: `docs/runtime/OMNI_OBSERVER_SLACK_GATEWAY.md`.

## Handoff Format

Use these headings when they carry information: Summary · Files Changed ·
Verification Performed · Verification Not Performed · Risks Or Follow-Up.
`Verification Not Performed` is only for a required acceptance surface that is
still unverified and changes the risk or next move. Omit empty headings and
non-actions.

## Entry budget

This file stays at or under 12 000 bytes, like every `SKILL.md`; the
`tests/tui/test_agent_entry_budget.py` gate enforces both. Doctrine that does
not bind every turn goes to `docs/agents/`, not here; the Vibecrafted Manifesto
is `docs/agents/MANIFESTO.md`.
