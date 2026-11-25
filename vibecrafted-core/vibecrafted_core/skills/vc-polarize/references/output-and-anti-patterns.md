# vc-polarize — Output Contract, Composition & Anti-Patterns

## Output Contract

Recommended artifacts:

```
$VIBECRAFTED_HOME/artifacts/<org>/<repo>/<YYYY_MMDD>/polarize/
  thesis.md
  concept-contract.md
  surface-map.json
  decision-ledger.md
  dou-handoff.md
  release-brief.md
```

If runtime has no dedicated `polarize/` artifact directory yet, write
only the normal injected report and include these sections inside it.

### Report sections (mandatory order)

1. **Polarized Thesis** — one sentence, no hedge words
2. **Mode** — `concept` or `product`
3. **Prism Evidence** — task framings, context pack paths, score axes
4. **Primary Boundary / Audience** — what wins now
5. **Rejected Alternatives** — what loses now, and why
6. **Runtime Proof** — concrete repo / runtime evidence
7. **Surface Alignment** — current claim/path → problem → chosen replacement
8. **Edits Made** — if implementation was in scope
9. **Gates Run** — commands, exit status, what they prove
10. **DoU Handoff** — what DoU should audit next
11. **Release Handoff** — what release can honestly ship and what remains blocked

## Composition with adjacent skills

- **`vc-init`** — required gate. Polarize without init evidence is blind.
- **`vc-marbles`** — required upstream. Without marbles' excess to
  strip, polarize has nothing to cut.
- **`vc-audit`** — adjacent READ-ONLY falsifier. Audit's verdict
  matrix can be a direct input to polarize when the question is
  "which UNVERIFIED claims to accept and which to reject?".
- **`vc-dou`** — downstream READ-ONLY shipping readiness check.
  Polarize emits DoU handoff section.
- **`vc-release`** — downstream WRITE for shipping. Polarize emits
  release brief.

## Anti-Patterns

- "Everyone can use it" framing (split audience never polarizes)
- One more wrapper instead of one contract
- Changing copy without runtime proof
- Scoring file count instead of authority drift
- Treating prism score as a CI failure / shame KPI
- Treating old context packs as live code truth
- Hiding a product choice behind technical cleanup
- Averaging two viable axes instead of choosing one
- Running polarize on `abort` / `memo` band (must dispatch only on
  `pass` / `doctrine`)
- Continuing into DoU / hydrate / decorate / release without operator ask
- Loading stale prism packs as authoritative
