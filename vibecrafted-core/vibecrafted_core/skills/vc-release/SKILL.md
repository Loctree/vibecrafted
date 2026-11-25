---
name: vc-release
version: 0.3.0
description: >
  Final outward ship skill. Turns "done in the repo" into "safe, visible, deployable,
  discoverable, and launchable in the world." Covers release mechanics, deployment
  topology, reverse-proxy defaults, Semgrep-gated security hygiene, domain and DNS
  wiring, SEO/indexability, verification challenges, onboarding truth, and post-release
  smoke checks. Trigger phrases: "release", "ship to market", "publish",
  "deploy to production", "vc-release", "go live", "launch", "wypuść wersję",
  "deploy", "release prep", "launch path", "launch checklist", "production checklist".
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Invocation for `vc-release` (launcher `release`)**
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
> | 1. User-launched worker | `vibecrafted release <agent>`                                                                                                            |
> | 2. Interactive          | `/vc-release` — execute **in this session**; use native subagents when required; do **not** externalize merely because a launcher exists |
> | 3. Agent-operator       | may dispatch the worker form above via `vc-dispatch` / operator lines while preserving this skill's identity                             |

> Freer native on some runs ≠ abandon external fleet. `vc-dispatch` and `vc-ship` keep their own identities.

<!-- /fleet-imperative -->

# vc-release — Ship It Without Lying

> "Done in the repo" is not "done in the world."

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
vibecrafted release codex --prompt 'Prepare v1.2.1 release'
vc-release claude --prompt 'Ship the web surface safely behind Caddy'
vibecrafted release gemini --file /path/to/release-checklist.md
```

Prefer `--file` for an existing plan, `--prompt` for inline intent.

Release is not ceremony. Release is an operational, security, visibility, and adoption contract.

## Repository Work Doctrine

For repository work, start with Loctree as the map: use `loct context`,
`loct occurrences`, `loct body`, and `loct find --literal` before broad manual
search. Use AICX for intent and session context. Use rg/grep as fallback or
local magnifier, not as a replacement for structural mapping. If Loctree fails
or misses a surface, append feedback to `~/.vibecrafted/loctree/loctree-fail.md`.

## Pipeline Position

```
scaffold → init → workflow → followup → marbles → dou → decorate → hydrate → [RELEASE]
```

Release runs after `vc-dou` verifies the product surface, `vc-decorate` ensures visual coherence, and `vc-hydrate` packages distribution/SEO/onboarding. Release makes hydrated artifacts real: tags, changelogs, registry/binary publication, deployment topology, proxy/TLS, domain/DNS/verification, indexability, security gates, post-release smoke.

## Public-surface floor

Release owns the ship gate. Run it before tagging and before calling the ship done:

```bash
vc-release --floor
vc-release --floor --require-release
```

`vc-release --floor` fails when a required channel, registry, or in-repo
surface disagrees with the version being cut. A GitHub Release that does not
exist yet is a warning at preflight, because this stage is what creates it:
pushing a tag and stopping is not a finished release. `--require-release`
fails until the Release object for that version exists. `scripts/publish-vibecrafted-release.sh`
runs the preflight and refuses to open a draft when the floor exits `1`.

Publish when the floor exits 0. `install_cta: no` means do not tell a stranger
to install; it does not by itself block the Release this stage creates. When
the only gap is the GitHub Release this publisher is about to create, the floor
warns and exits 0, and `install_cta` stays `no` until that Release exists.
`--acknowledge <surface-id>` records an accepted gap; it is the written risk
acceptance this skill already requires, and it stays in the report.
`scripts/publish-vibecrafted-release.sh --acknowledge <surface-id>` and
`make publish-release ACKNOWLEDGE="<surface-id>"` forward that id and reject
any other floor argument.
Contract: [`../vc-dou/references/public-surface-floor.md`](../vc-dou/references/public-surface-floor.md).

## Core Rule

**If the release canon below is not satisfied, release is a no-op.** Do not confuse "I can deploy it" with "it is safe, visible, and ready to meet strangers."

## The Release Canon — six planes

1. **Artifact truth** — versions, tags, changelog, published outputs
2. **Deployment truth** — topology, proxying, healthchecks, restart behavior
3. **Security truth** — Semgrep, exposed surfaces, headers, auth, secret handling
4. **Domain truth** — DNS, default host, TLS, redirects, verification challenges
5. **Visibility truth** — SEO, indexability, social cards, sitemap, robots, public metadata
6. **Onboarding truth** — install path, first run, docs, screenshots, quickstart, buyer path

If any plane is missing, call it out explicitly and block release unless the user knowingly accepts the risk.

## Artifact Canon, Deployment Topology & Proxy Defaults

Tag the exact commit, keep changelog and registry outputs aligned with boring descriptive artifact names, and pick the smallest honest stack (Caddy, Nginx, or Docker). Bind services to `127.0.0.1` by default, terminate TLS at an intentional reverse proxy preserving `Host`/forwarding/websocket headers, inject secrets at runtime, and require `/health` plus non-root containers.

Full canon, safe ladder, safety defaults, red flags, and reverse-proxy rules: [references/deployment-and-proxy.md](references/deployment-and-proxy.md).

## Semgrep Release Gate

Semgrep is part of the canon (not optional): run `make semgrep` against the full repo before release, classify findings by **dataflow boundary**, and block release on any unresolved blocking finding unless the user accepts the risk in writing in the report. If Semgrep is unavailable, state so explicitly, run `uvx semgrep`, and record that the gate was not satisfied.

Full dataflow-boundary remediation rules and minimum finding classes: [references/semgrep-gate.md](references/semgrep-gate.md).

## Release Report Contract

Every release report must include these mandatory sections and link back to
`references/release-report-template.md`:

- **Security gate** — `make semgrep` evidence, findings, and unresolved risk.
- **Exposed surface inventory** — public routes, services, ports, domains, and admin/debug surfaces.
- **Deployment mode decision** — selected topology, proxy/TLS posture, and rollback path.
- **Post-release install smoke** — cold-path install/run verification from the published artifact.

## Domain, Visibility, Onboarding & Post-Release Smoke

Public surfaces must verify DNS, canonical host redirects, TLS, `.well-known/*` / TXT ownership proofs, crawlable HTML/SSR SEO metadata, `robots.txt`/`sitemap.xml`, cold first-user onboarding, and cold-path smoke checks from the published artifact (never a local checkout or dev branch). Release also requires clear financial/legal readiness and avoiding common release anti-patterns.

Full checklists for Domain/DNS, SEO & visibility, onboarding truth, cold-path smoke verification, mandatory report breakdown, financial/legal reality, and anti-patterns: [references/visibility-smoke-and-antipatterns.md](references/visibility-smoke-and-antipatterns.md).

> Canonical template: [`references/release-report-template.md`](references/release-report-template.md).
> Full operator checklist: [`references/release-checklist.md`](references/release-checklist.md).
> Deployment reality deep-dive: [`references/deployment-reality.md`](references/deployment-reality.md).

## Final Principle

Ship only when it is safe enough, visible enough, installable enough, understandable enough, and the deployment story is boring enough to trust. If not, the honest result of `vc-release` is not "done" — it is "blocked, for these exact reasons."

---

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
