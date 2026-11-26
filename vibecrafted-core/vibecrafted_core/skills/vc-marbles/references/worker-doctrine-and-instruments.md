# vc-marbles — Worker Doctrine & Instruments vs Gates

## Worker Doctrine (Blind on Purpose)

A worker is intentionally **blind to prior marble history**, working
against the **current workspace state** only. Context weight kills
quality — an agent working 90 minutes makes worse decisions in minute
91 than a fresh agent in minute 1, defending sunk cost instead of
seeing the tree. Every round gets a fresh mind. Not a workaround —
the design.

The **reception layer** (operator / orchestrator)
holds the open-finding ledger, candidate comparison across parallel
rounds, and the decision to converge or fire another wave. See
[`RECEPTION.md`](RECEPTION.md). Do not load reception into worker
context.

---

## Instruments vs Gates

**Instruments** (loctree, semgrep, aicx-steer) go at the **beginning**
— they direct where to look (prosecution: accusing the tree with
evidence).

**Tests** (pytest, cargo test, build) go at the **end** — they verify
the fix (the gate).

Tests-first collapses field of vision to "what fails" instead of
"what is fragile". Red tests scream loudest, but the real structural
weakness is often silent.
