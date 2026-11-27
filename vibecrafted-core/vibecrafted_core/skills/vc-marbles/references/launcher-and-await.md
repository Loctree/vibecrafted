# vc-marbles — Launcher Examples & Await Discipline

Standard launcher:

```bash
# Single round (3 runs by default):
vibecrafted marbles codex --prompt 'Fix the 3 failing portable tests'
vc-marbles codex --prompt 'Harden the installer shell surface'

# Multiple rounds (convergence loop — runtime spawns fresh agent 3..n times)
vibecrafted marbles codex --count 5 --prompt 'Stabilize until P0=0'
vc-marbles claude --count 8 --prompt 'Refactor the 1500 LOC monoliths'

# From a plan file:
vibecrafted marbles codex --file ~/.vibecrafted/artifacts/vetcoders/vibecrafted/2026_0407/plans/marbles-plan.md
vc-marbles gemini --count 5 --file /path/to/plan.md

# Crawl back into the canonical store then read 'n' recently
# implemented plans then fill the all the gaps:
vibecrafted marbles codex --count 10 --depth n
vc-marbles claude --depth 12 --prompt 'Focus on "vc-followup assumptions from the last 12 plans'
```

After dispatch, arm `vibecrafted await <agent> --run-id <id>` immediately,
supervisor-side. Control-plane JSON, report files, transcripts, panes, and
scheduled wakeups are diagnostic only, not wake signals. Hedging await with
ad-hoc pollers/watchers is a Class 3 violation; fix `control_plane.await_run`,
do not normalize the hedge. See `docs/runtime/AGENT_OPS.md`.

3-signal liveness: await verdict, terminal run meta, worker pid dead, plus
promised report presence. Two agreeing signals are enough to act, three to
declare done; any disagreement means treat as live and re-arm await. Known skew:
rc=0-on-live and meta stuck `active`/`stalled` after real completion.

**Not the same as `vibecrafted implement codex <plan>`.** `implement`
is how code appears. `marbles` is what happens after code exists but
still needs to be made truthful and shippable. Each round wraps a
fresh agent in a convergence loop. `--count` controls outer loop
iterations.
