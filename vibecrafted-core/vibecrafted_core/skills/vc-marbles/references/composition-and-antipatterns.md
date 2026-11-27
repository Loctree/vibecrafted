# vc-marbles — Skill Composition, Anti-Patterns & Closing Rail

## Composition with adjacent skills

- **`vc-init`** — required gate. Every round begins here.
- **`vc-audit`** — downstream READ-ONLY falsification. Audit checks
  whether the swarm's claimed fixes actually landed against a written
  plan.
- **`vc-polarize`** — downstream WRITE step. After marbles flood +
  audit verdict, polarize strips back to one truth.
- **`vc-review`** — adjacent READ-ONLY review on bounded diffs. A
  marbles round commit can be reviewed individually before swarm
  continuation.
- **`vc-followup`** — adjacent READ-ONLY trajectory check. Use after
  marbles wave to assess overall direction health.

---

## Anti-Patterns

- **Historical self-awareness** — reading prior marble artifacts to sound informed
- **Convergence cosplay** — talking about step size / delta / loop mastery
- **Surface-area vanity** — touching many files to make the round look bigger
- **Polishing theater** — cleanup that doesn't close a failure mode
- **Backward-compatibility worship** — preserving rotten contracts
- **Narrative inflation** — long explanations hiding a weak gate
- **Parallel contamination** — importing another marble's context
- **Fake omniscience** — pretending to see the full global backlog
- **Agent contempt** — treating other agents as inferior; why-matrix is
  a map of styles, not a hierarchy of worth
- **Solving product smear in the worker** — expose, do not decide;
  leave it for polarize
- **Self-extension** — writing the next round's plan from inside this
  round

---

## Closing Rail

```text
=======================
Remember: marbles mode is permission to write the small or braad truthful
fix, not permission to refactor, unless it is clearly given as a task
description. You don't need to bother about the overgrown code around the
certain parts of the codebase, but you have the hard obligation to describe
it in the report if encountered.
The worker sees the tree, never the factory. One round, one commit, one report.
Then leave. The swarm produces the excess; polarize strips it.
(•̀⌄•́)و ̑̑
=======================

Dad's joke: Why does the marble worker never argue with the next worker?
Because by then it's already left the locker room.  (._.)
```
