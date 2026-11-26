---
name: vc-prune
version: 3.3.3
description: >
  Repository curation, not clear-cutting. Map what truly participates in runtime
  truth versus what is silently parked — then decide revive, archive, or delete.
  Includes the silencer strip: rip every `#[allow(...)]`, `// nosemgrep`,
  `eslint-disable`, `@ts-ignore`, `# noqa`, `# type: ignore`, panic-vs-skip pattern,
  and any other annotation that mutes a quality gate. Run the gates. Listen.
  Triage with care — `#[allow(dead_code)]` (and equivalents) is often the most
  valuable smell in a repo: parked work the team forgot about. Surface those as
  forgotten gems for the operator to decide.
  This skill is a gem hunter, not a clear-cutter.
  Trigger phrases: "prune", "strip dead code", "wyczyść mądrze", "strip the silencers",
  "zdejmij wszystkie ignore", "zobacz co realne", "forgotten gems",
  "co tam zapomnieliśmy".
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Invocation for `vc-prune` (launcher `prune`)**
>
> Same three-path _shape_ as the fleet, with **this** skill's literals — see the
> canonical [Delegation Matrix](../DELEGATION_MATRIX.md):
>
> - [Shared three paths](../DELEGATION_MATRIX.md#shared-three-paths)
> - [Launcher catalogue](../DELEGATION_MATRIX.md#launcher-catalogue-core-runtime)
> - [Per-launcher rule](../DELEGATION_MATRIX.md#per-launcher-rule-the-semantic-delta)
> - [Native vs external](../DELEGATION_MATRIX.md#native-subagents-vs-external-workers)
>
> | Path                    | Literal for this skill                                                                                                                 |
> | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
> | 1. User-launched worker | `vibecrafted prune <agent>`                                                                                                            |
> | 2. Interactive          | `/vc-prune` — execute **in this session**; use native subagents when required; do **not** externalize merely because a launcher exists |
> | 3. Agent-operator       | may dispatch the worker form above via `vc-dispatch` / operator lines while preserving this skill's identity                           |

> Freer native on some runs ≠ abandon external fleet. `vc-dispatch` and `vc-ship` keep their own identities.

<!-- /fleet-imperative -->

# vc-prune — Curation, Not Clear-Cutting

> Don't burn the house down. Strip it to the load-bearing walls and report what you found behind the wallpaper.

## Operator Entry

### Living Tree / Worktree Rule

This workflow runs in the operator's current checkout and current branch. Do not create, switch to, or move execution
into a git worktree unless the operator explicitly asks for a worktree in this prompt. Generic words like "isolate", "
parallel", or "clean branch" are not enough. Re-read files before editing, adapt to concurrent changes, and report a
substrate failure if the current tree is too poisoned to continue safely. The one sanctioned second mode is a Fleet Worktree dispatch (written plan, pre-committed verifiers, disjoint domains, single-thread integrator — see Living Tree Rule, Mode B); outside that formation, stay in the shared tree.

See [Living Tree Rule](../LIVING_TREE_RULE.md).

## Canonical Orientation Gate

Before this workflow performs repo-specific analysis, planning, implementation, review, release, or delegation, it MUST
run or consume the `vc-init` procedure for the assigned repo. If fresh `vc-init` evidence is absent, perform the init
pass first and treat workflow-specific work as blocked until repo truth exists.

`Loctree:loctree` is the default structural perception skill for that pass. Use Loctree before grep or docs-driven
claims to produce or refresh the Code-Derived Application Map: repo-view, focus, slice, impact, find, and follow as
relevant. Search for existing symbols and contracts before creating new ones; run impact before delete or major
refactor; run slice before editing.

The point is to find the hooks: load-bearing hubs, twins, dead code, drift, runtime entrypoints, and blast-radius traps.
If the task is explicitly non-repo or no-code, state the no-repo exception in the report. Otherwise, missing `vc-init`
/Loctree evidence is a process failure.

Launch through the command deck (see `vc-init` for the full operator-entry contract):

```bash
vibecrafted prune <agent> --file /path/to/prune-plan.md
vc-prune codex --prompt 'Strip silencers and listen'
```

A vibe-coded repo usually accumulates two layers of debris: **dead surface** (abandoned auth experiments, duplicate
Stripe handlers, dead serverless functions) and **silenced surface** (warnings muted in a hurry, tests that always skip,
panics that always fire). `vc-prune` separates both layers from runtime truth — and from each other.

## Repository Work Doctrine

For repository work, start with Loctree as the map: use `loct context`,
`loct occurrences`, `loct body`, and `loct find --literal` before broad manual
search. Use AICX for intent and session context. Use rg/grep as fallback or
local magnifier, not as a replacement for structural mapping. If Loctree fails
or misses a surface, append feedback to `~/.vibecrafted/loctree/loctree-fail.md`.

## Axioms

1. **Aggressive pruning, with belief in the VCS archive.** Dead code is not bad code — it's a graveyard of valuable
   ideas. Its place is in Git history, not the runtime. Cut without sentiment — but only after axiom 4.
2. **Move on over backward compatibility.** Rotten abstractions blocking stabilization get cut cleanly. The dependency
   graph is part of runtime truth.
3. **The code knows. Strip the silence and listen.** Every silencer is a deferred conversation. Most were added in a
   hurry. The only honest test of which still earn their keep is to rip them all out and let the toolchain speak.
4. **`#[allow(dead_code)]` (and cousins) is often the most valuable signal in a repo.** It usually marks parked work — a
   90%-complete login flow, an export pipeline for a churned customer, a debug visualizer no one mentioned to new hires.
   These are **forgotten gems**, not garbage. Surface them; never auto-delete.

## Core Contract

- For non-trivial prune, `vc-agents` external dispatch is the default first move.
- Assume 30% of a vibe-coded repo is dead scaffolding.
- Classify every candidate: `KEEP-RUNTIME`, `KEEP-BUILD`, `MOVE-ARCHIVE`, `DELETE-NOW`, `VERIFY-FIRST`, or
  `FORGOTTEN-GEM`.
- Prefer cutting whole dead vertical slices over trimming symbolic leaves.
- Tighten contracts after every wave: manifests, docs, CI, package bounds.
- Run gates after every wave. Require one real smoke or build proof.

## Delegation Doctrine

| Need                                             | Best model |
| ------------------------------------------------ | ---------- |
| Archaeology, hidden reachability, gem-hunting    | Claude     |
| Exact deletions, manifest tightening, mech. work | Codex      |
| Radical simplification, cutting whole subsystems | Gemini     |

## Workflow

### Phase 1 — Define the runtime cone

Capture: real entrypoints, mandatory user flows, build/release path. Do not start from "unused exports" — start from "
does this serve live traffic?"

### Phase 2 — Map with `loct`

```bash
loct auto && loct manifests && loct hotspots && loct dead
loct routes      # web/API
loct commands    # desktop/Tauri
loct events
```

### Phase 3 — Prune in waves (safest → riskiest)

- **Wave 1 — AI exhaust & prototype scaffolding.** `v1_backup.ts`, `old_auth_handler.js`, `stripe_test_claude.ts`, dead
  `.claude/` `.codex/` session folders, stale screenshots.
- **Wave 2 — Whole dead vertical slices.** Frontends with no consumers, alternate login pages never mounted, webhook
  handlers replaced by SaaS. Cut the strand, let Git archive it.
- **Wave 3 — Unreachable product surface.** Unmounted routes, duplicate engines (Prisma + raw SQL doing the same thing),
  dead feature flags retained after launch.
- **Wave 4 — Contract tightening.** `package.json` deps, `Cargo.toml` features, `pyproject.toml` extras, `.env.example`
  stale secrets, CI workflows.
- **Wave 5 — The Silencer Strip.** Separate wave because it's not about removing dead code — it's about un-muting the
  toolchain so live code can speak. See below.

### Phase 4 — Verify reality

Green static gates are necessary, not sufficient. Add one real proof path: boot the app, run the CLI, hit the main
route.

---

## Wave 5 — The Silencer Strip (Strip and Listen)

Inventory all silencers per language (`#[allow(`, `nosemgrep`, `eslint-disable`, `@ts-*`, `# noqa`, `# type: ignore`, `//nolint`, skip/panic test theater), bulk-strip them in one pass without pre-curating, and run every repo gate. Triage every failure into: root-cause fix, stylistic refactor, incident-grade comment (WHY/WHEN/WHERE), **Forgotten Gems Report** (`dead_code` on real parked work — never auto-delete), or a `<timestamp>_test-theater.md` follow-up plan. Target ≤25% (often ≤10%) remaining silencers with green gates and zero hide tricks.

Full `rg` inventory commands, gate commands, triage table, Forgotten Gems Report path, and surprise-findings checklist: [references/silencer-strip.md](references/silencer-strip.md) (and [references/case-studies.md](references/case-studies.md)).

## Anti-Patterns

Never trim leaves while an abandoned subsystem stands, trust "unused" without checking dynamic router loading, selectively strip Wave 5 silencers, mass-restore warnings, treat always-skip/panic tests as gates, or auto-delete `dead_code` without a forgotten-gem check. Full catalogue: [references/silencer-strip.md#anti-patterns](references/silencer-strip.md#anti-patterns).

## The Pruning Principle

Ask the repo to justify every surviving surface, not every scar: surfaces outside production, release builds, or integrity tests require an explicit **revive, archive, or delete** decision, and every survivor carries a written reason. Full closing principle: [references/silencer-strip.md#the-pruning-principle](references/silencer-strip.md#the-pruning-principle).

---

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
