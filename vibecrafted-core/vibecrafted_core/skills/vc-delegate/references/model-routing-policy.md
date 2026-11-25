# vc-delegate — Native Subagent Model Routing & Economics Policy

## Native Delegation Policy

Pick each subagent's model by the **subtask's economics** (Founder rule,
2026-10-03 — supersedes the 2026-04-10 same-tier parity default): choose a
model with a justified margin above the capability and quality the cut
requires, then select the most economical option among the models that clear
that bar. This applies to the whole fleet, not just Codex.

In practice:

- **Mechanical fan-out** (rename sweeps, fixture writing, format probes,
  bounded file reads, boilerplate tests) → fast/cheap tier. Serializing this
  work on a frontier model is waste in both directions: slower delivery AND
  higher cost.
- **Load-bearing reasoning** (architecture, gnarly debugging, interpreting a
  Founder canon, high-blast-radius edits) → the parent's tier or stronger.
  Use a stronger model immediately when ambiguity, dependency depth, or the
  consequence of error warrants it; never force a cheap-first trial or defend
  a poor result because it cost less.
- Escalate after a demonstrated limitation, without automatically redoing
  every economical result on a stronger model.

Tie-breaker, not law: same-family models preserve cache locality and the
closest reasoning style to the parent — prefer them when two options clear
the capability bar equally. If you trade down for speed or availability,
recover quality in the parent orchestration pass.

Runtime availability notes:

- Claude: for extensive long-running tasks prefer `opus[1m]`; for lighter
  tasks `sonnet[1m]`.
- Gemini: if `gemini-3.1-pro-preview` is unavailable or unstable during peak
  demand, fall back to `auto-gemini-3`.
- A subagent role label alone does not prove the actual model or reasoning
  effort; when confirming routing, use available runtime metadata, without
  mandatory polling after every spawn.
