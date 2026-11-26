# Vibecraftsmanship — Autonomous Self-Pacing Reference

## Operational default — autonomous self-pacing (Claude Code native)

**HARD RULE (Power axis enforcement, second canonical surface):** When the
agent enters autonomous behavior — operator absent, deferred decisions,
recurring monitoring, multi-turn execution without manual re-prompts —
the default mechanism is the Claude Code native **`/loop`** skill
(equivalent: `ScheduleWakeup` with `<<autonomous-loop-dynamic>>` sentinel
for dynamic-pacing mode). NOT silent waiting. NOT polling in tight Bash
sleeps. NOT "I'll just answer next turn whenever the operator returns."

**Reason:** `/loop` is the canonical Claude Code power feature for
autonomous self-pacing — it bridges the gap between "operator drives every
turn" and "agent fires and forgets". Without entering `/loop`, the agent
falls back to single-turn passivity: operator must re-prompt to continue
work, even when next steps are obvious. `/loop` makes the agent's
autonomous tail observable and bounded (heartbeat interval, fallback
schedule, explicit stop condition).

**When to enter `/loop`:**

- Operator declared "bez odbioru" / "decide autonomously" / "I'm leaving"
- Awaiting external work (CI, dispatched fleet, long-running build)
- Multi-wave dispatch where waves complete asynchronously
- Substrate operation with known wait window (rebase, install, sync)
- Recurring observation (PR babysitting, deploy monitoring)

**When NOT to enter `/loop`:**

- Single-turn answer with no follow-up
- Operator actively engaged in conversation
- Work explicitly scoped to "do this one thing and stop"

**Composition with external dispatch:**

- External dispatch (`vibecrafted <launcher> <agent>`) produces async work
  that needs `await`. Enter `/loop` to keep heartbeat alive between
  `task-notification` events from the harness.
- `/loop` + `vibecrafted` = canonical autonomous-operator pattern. One
  declares "I'm staying engaged"; the other declares "I'm using
  observable external surface". Both together = vibecraftsmanship power
  axis fully realized.

**Detection signal (STOP and enter loop):** if you catch yourself ending
a turn with "operator's next move" or "waiting for response" while there
is already-authorized queued work that fits the current scope and stop
conditions, that is missed `/loop` entry. Re-think: schedule a self-paced
check, declare what you'll do on each tick, stop when the stop condition is met.
