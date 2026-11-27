# `vc-implement` — Agent Usage & Anti-Patterns

## Agent Usage

| Situation                           | Action                             |
| ----------------------------------- | ---------------------------------- |
| One focused task, < 200 LOC         | Do it yourself                     |
| Two independent work streams        | Spawn 2 agents via `vc-agents`     |
| Quick review of your own work       | `vc-delegate` one reviewer         |
| Research needed for unknown API/lib | One research agent, keep working   |
| Everything is sequential            | Do it yourself; agents add latency |

Spawn/context/synthesis overhead is real. Only parallelize when it saves more
time than it costs.

## Anti-Patterns

- Asking 5 clarifying questions before starting
- Writing a plan document and asking for approval
- Announcing "Phase 1 complete, entering Phase 2"
- Skipping followup because "it looks fine"
- Skipping marbles because "only one P1 left"
- Spawning 4 agents for a task one agent can finish in 20 minutes
- Delivering without running quality gates
- Leaving the user to figure out what changed
- Fixing unrelated code while the requested feature is incomplete
- Going silent for 30 minutes without any progress signal
- Treating this skill as interchangeable with `vc-justdo`
