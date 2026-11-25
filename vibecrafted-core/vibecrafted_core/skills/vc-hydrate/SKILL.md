---
name: vc-hydrate
version: 1.1.0
description: >
  Packaging and go-to-market hydration skill. Takes DoU audit findings and
  executes the non-code work that bridges the gap between "it works" and
  "someone can buy this." Generates marketplace listings, SEO fixes,
  distribution artifacts, onboarding flows, landing page content, and
  representation surfaces for products that do not naturally have a public web UI.
  Trigger phrases: "hydrate", "package for market", "prepare for launch",
  "przygotuj do launchu", "fix the packaging gap", "marketplace listing",
  "nawodnij", "make it shippable", "go-to-market", "distribution",
  "SEO fix", "landing page", "onboarding", "completion sprint".
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Invocation for `vc-hydrate` (launcher `hydrate`)**
>
> Same three-path _shape_ as the fleet, with **this** skill's literals — see the
> canonical [Delegation Matrix](../DELEGATION_MATRIX.md):
>
> - [Shared three paths](../DELEGATION_MATRIX.md#shared-three-paths)
> - [Launcher catalogue](../DELEGATION_MATRIX.md#launcher-catalogue-core-runtime)
> - [Per-launcher rule](../DELEGATION_MATRIX.md#per-launcher-rule-the-semantic-delta)
> - [Native vs external](../DELEGATION_MATRIX.md#native-subagents-vs-external-workers)
>
> | Path                    | Literal for this skill                                                                                                                   |
> | ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
> | 1. User-launched worker | `vibecrafted hydrate <agent>`                                                                                                            |
> | 2. Interactive          | `/vc-hydrate` — execute **in this session**; use native subagents when required; do **not** externalize merely because a launcher exists |
> | 3. Agent-operator       | may dispatch the worker form above via `vc-dispatch` / operator lines while preserving this skill's identity                             |

> Freer native on some runs ≠ abandon external fleet. `vc-dispatch` and `vc-ship` keep their own identities.

<!-- /fleet-imperative -->

# vc-hydrate — The Antidote to Always-in-Production

> "The code is dry — structurally complete but missing the fluid that makes it flow to users. Hydration means: make the path from stranger to user frictionless."

## Operator Entry

### Living Tree / Worktree Rule

This workflow runs in the operator's current checkout and current branch. Do not create, switch to, or move execution into a git worktree unless the operator explicitly asks for a worktree in this prompt. Generic words like "isolate", "parallel", or "clean branch" are not enough. The one sanctioned second mode is a Fleet Worktree dispatch (written plan, pre-committed verifiers, disjoint domains, single-thread integrator — see Living Tree Rule, Mode B); outside that formation, stay in the shared tree. Re-read files before editing, adapt to concurrent changes, and report a substrate failure if the current tree is too poisoned to continue safely.

See [Living Tree Rule](../LIVING_TREE_RULE.md).

## Canonical Orientation Gate

Before this workflow performs repo-specific analysis, planning, implementation, review, release, or delegation, it MUST run or consume the `vc-init` procedure for the assigned repo. If fresh `vc-init` evidence is absent, perform the init pass first and treat workflow-specific work as blocked until repo truth exists.

`Loctree:loctree` is the default structural perception skill for that pass. Use Loctree before grep or docs-driven claims to produce or refresh the Code-Derived Application Map: repo-view, focus, slice, impact, find, and follow as relevant. Search for existing symbols and contracts before creating new ones; run impact before delete or major refactor; run slice before editing.

The point is to find the hooks: load-bearing hubs, twins, dead code, drift, runtime entrypoints, and blast-radius traps. If the task is explicitly non-repo or no-code, state the no-repo exception in the report. Otherwise, missing `vc-init`/Loctree evidence is a process failure.

Enter via `vibecrafted start` (or `vc-start`). Then launch through the command deck:

```bash
vibecrafted hydrate codex --prompt 'Package for marketplace'
vc-hydrate claude --prompt 'Generate missing SEO and landing page'
vibecrafted hydrate gemini --file /path/to/dou-report.md
```

Hydrate is the packaging agent that DoU calls for. It treats "create a DMG installer" and "write SEO-friendly copy" as first-class engineering tasks, not afterthoughts.

**Canonical rule:** every serious product needs a presentation surface, even if it is not itself a web product. Desktop apps, CLI tools, MCP servers, local runtimes, and internal systems still need an external face that lets a stranger discover, understand, see, assess, and adopt.

## Repository Work Doctrine

For repository work, start with Loctree as the map: use `loct context`,
`loct occurrences`, `loct body`, and `loct find --literal` before broad manual
search. Use AICX for intent and session context. Use rg/grep as fallback or
local magnifier, not as a replacement for structural mapping. If Loctree fails
or misses a surface, append feedback to `~/.vibecrafted/loctree/loctree-fail.md`.

## Pipeline Position

```
scaffold → init → workflow → followup → marbles → dou → decorate → [HYDRATE] → release
```

## Public-surface floor

Hydrate owns the checkout a packager can edit. It does not fetch registries.
Run this before claiming the package is ready, and again after the edits:

```bash
vc-hydrate --floor
```

Exit `1` means the README has no install command, an install command pins a
different version than the reference, in-repo version projections disagree,
or the configured public files spell Vetcoders with a capital C. The canonical
spelling is `Vetcoders`. Live channel, registry, and site drift stays with
`vc-dou --floor`; hydrate does not get to mark that green by skipping it.
Contract: [`../vc-dou/references/public-surface-floor.md`](../vc-dou/references/public-surface-floor.md).

## When To Use

- After a `vc-dou` audit identifies packaging gaps
- Before any marketplace submission or public launch
- When the team says "it works, now make it findable/installable/buyable"
- Periodic hydration sprint (recommended: pair with DoU every 2 weeks)
- When Plague Score > 40

## Hydration Domains (1–6)

Hydrate closes gaps across six domains: **1. Repository** (`LICENSE`, `CONTRIBUTING.md`, `CHANGELOG.md`, `SECURITY.md`, CI, version sync), **2. Distribution** (CLI prebuilt binaries/Homebrew, signed/notarized macOS `.app`/DMG, web Docker/healthcheck), **3. Discoverability** (SSR/pre-rendering, SEO/OG meta tags, security headers, `robots.txt`/`sitemap.xml`), **4. Commercial Surface** (landing structure, mandatory representation scaffolding for non-web products, marketplace listings), **5. Onboarding** (first 5 minutes / 60s quick win), and **6. Representation Layer** (minimal external public face).

Full per-domain specifications and templates: [references/hydration-domains.md](references/hydration-domains.md).

## Sprint Protocol, Delegation & Anti-Patterns

Ingest the `vc-dou` P0/P1 findings, triage across Domains 1–6 (splitting across `vc-agents` subagents for large sprints), generate missing packaging/presentation artifacts, re-run DoU targeting a Plague Score reduction of ≥20 points, and report before/after scores plus manual steps. Never hydrate without a DoU audit or treat non-web products as needing no representation layer.

Full sprint protocol, pipeline integration, subagent split, and anti-pattern list: [references/sprint-protocol-and-antipatterns.md](references/sprint-protocol-and-antipatterns.md).

## "Done Done" Definition

A project is hydrated when:

- A stranger can **DISCOVER** it (search engines, marketplace, word of mouth)
- A stranger can **UNDERSTAND** it (landing, README, value prop clear in 30s)
- A stranger can **SEE** it (representation surface exists, even if not web-native)
- A stranger can **INSTALL** it (one command, no dev toolchain, <5 minutes)
- A stranger can **USE** it (onboarding, quick win within 60 seconds)
- A stranger can **PAY** for it (pricing, signup, trial — if commercial)
- A stranger can **CONTRIBUTE** (CONTRIBUTING.md, issue templates, CI — if open source)

Until all six are true, the project is in the Always-in-Production state. Hydration is the antidote.

---

## Verify before the handoff

Before you report "done", walk around the truck — see [Verification Rule](../VERIFICATION_RULE.md): run the REAL artifact (launch the app/binary, not just `--version`), re-verify runtime, never trust upstream verification as proof, and check your own check. Gates green ≠ works.

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
