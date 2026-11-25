# vc-hydrate — Sprint Protocol, Pipeline Integration, Delegation & Anti-Patterns

## Hydration Sprint Protocol

1. **Ingest DoU report.** Extract all P0/P1 findings. Sort by impact (commercial surface > discoverability > repo governance).
2. **Triage into domains.** Map each finding to a domain (1-6). Some findings map to multiple — list all.
3. **Generate artifacts.** Per finding: missing files → create them; missing meta → generate HTML; missing install path → CI workflow; missing landing → write copy; missing representation → scaffold appropriate to product type; missing marketplace listing → generate listing.
4. **Verify via DoU.** Re-run on affected areas. Target: Plague Score reduction ≥20 points.
5. **Present to user.** Hydration Report with before/after Plague Scores, table of artifacts generated per domain (status), and remaining manual steps (DNS, API keys, marketplace submit button, etc.).

## Pipeline Integration

```
Phase 1 — Craft:     scaffold → init → workflow → followup
Phase 2 — Converge:  marbles ↻ (loop until P0=P1=P2=0)
Phase 3 — Ship:      dou → decorate → hydrate → release
```

Hydrate produces packaging artifacts. `vc-decorate` polishes visual coherence before hydration. After hydration, `vc-release` handles deployment and go-to-market launch. Re-run DoU after hydration to verify the gap closed.

## Subagent Delegation

For large hydration sprints, split domains across subagents using `vc-agents`:

```
Agent 1: Repo Hydration (LICENSE, CONTRIBUTING, CI, CHANGELOG)
Agent 2: Distribution Hydration (release workflows, installers)
Agent 3: Discoverability Hydration (SEO, meta tags, pre-rendering)
Agent 4: Commercial Hydration (landing copy, marketplace listings)
```

Each agent receives: DoU findings for its domain, template artifacts from this skill, standard living-tree preamble.

## Anti-Patterns

- Hydrating without a DoU audit first (fixing what you assume, not what's measured)
- Generating files without repo context (LICENSE type must match project intent)
- Writing marketing copy without understanding the product (run vc-init first)
- Assuming desktop / CLI / MCP / local products do not need a representation layer
- Treating hydration as one-off (it's a recurring sprint, like refactoring)
- Hydrating everything at once (prioritize: P0 commercial gaps first)
- Forgetting to re-run DoU after hydration (verify the fix)
