# `vc-dou` — Output Format, Anti-Patterns & Plague Diagnostic

## Output Format

```markdown
# Definition of Undone: <project/ecosystem>

Date: <YYYY-MM-DD>
Auditor: <agent>

## Executive Summary

<2-3 sentences: gap between code and market>

## Undone Matrix

| Project | Repo | Web | Commercial | Critical Gap |
| ------- | ---- | --- | ---------- | ------------ |

## Findings by Severity

### P0 — Ship Blockers

### P1 — Credibility Gaps

### P2 — Polish

## The Funnel Test

Discovery → Landing → Understanding → Trial → Adoption → Payment
<for each product, mark where the funnel breaks>

## Hydration Priorities

<ordered fix list with effort estimates>

## Plague Score

0 = fully shipped and discoverable | 100 = brilliant, commercially invisible
```

## Anti-Patterns

- Running DoU only on code (it's a PRODUCT surface audit)
- Treating `[OK]` repo health as proof of readiness
- Auditing without crawling URLs
- Assuming non-web products need no representation surface
- Skipping the install path test
- Reporting without severity ranking
- Not re-running after hydration

## The Plague Diagnostic

Plague pattern:

1. Tests pass `[PASS]`
2. Architecture sound `[PASS]`
3. README exists `[PASS]`
4. Nobody can find it from Google `[FAIL]`
5. Nobody can install without a toolchain `[FAIL]`
6. Nobody can pay for it `[FAIL]`

Items 4-6 are the Definition of Undone.
