# `vc-implement` — Execution Playbook (Steps 1–7)

## How You Work

### 1. Understand the task

If it is clear enough to act on, act. If it is genuinely ambiguous (two
plausible interpretations leading to different architectures), ask **ONE**
clarifying question. Not three. One.

If the task is vague enough to need architectural scoping (new product,
greenfield, "I have an idea"), use `vc-scaffold` first, then execute. Implement
consumes scaffold plans directly.

If the user said they are exhausted, bias toward action over more process — still
one question max when architecture truly forks.

### 2. Get your bearings

Bootstrap context quietly. No init report to the user. Use foundation tools
(loctree, aicx, prview, screenscribe):

- `repo-view` / `focus` / `slice` / `impact` — structure and risk
- `aicx extract` — if previous output is too large
- `prview` — if working on an existing PR
- `screenscribe` — if the task involves visual demo evidence
- Read existing code before writing new code
- Check git log for recent changes in the target area

30 seconds, not 5 minutes. Do not turn reconnaissance into a research project.

### 3. Plan internally

Decide your approach. Do not present a plan for approval. Think:

- Simplest architecture that works?
- Existing patterns this codebase uses?
- Integration points?
- What tests exist? What tests are needed?
- Blast radius if you get it wrong?

If blast radius is high and the approach is non-obvious, tell the user your plan
in 3 bullets and wait for a nod. Otherwise execute.

### 4. Implement

Use agents when parallel work buys real speed:

- Two independent modules → two agents
- Frontend + backend split → two agents
- One sequential feature → do it yourself, agents add overhead

Use `vc-agents` for real parallelization. Use `vc-delegate` for lightweight
in-session tasks. Do not spawn agents for a 50-line change.

While implementing:

- Follow existing patterns
- Write tests alongside, not after
- Do not refactor unrelated code
- Do not add features the user did not ask for
- Commit logical chunks, not one mega-diff
- In `decorate` rounds, preserve progress incrementally like marbles —
  numbered local commits (`decorate 1: ...`, `decorate 2: ...`) as verified
  seams harden.

### 5. Followup (mandatory)

When implementation feels complete, run a followup audit on yourself. Not
optional. This is where ship-stage delivery earns trust.

- Do quality gates pass? Run them.
- Does new code integrate cleanly with existing code?
- Untested paths?
- Regressions introduced?
- Would a reviewer flag anything obvious?

Produce a P0/P1/P2 finding list internally. You don't need to format a report —
you need to know the truth.

### 6. Marbles (mandatory when findings exist)

**NO EXCEPTION RULE:** if followup found ANY P0 or P1 issues, immediately invoke
`vc-marbles` to loop and fix them. Do not just report them.

If followup found only P2s: fix the obvious ones, document the rest.

The marbles loop under implement is tight:

```
while P0 > 0 or P1 > 0:
    fix top issue
    re-run affected gates
    re-assess findings
```

Do not announce iterations. Just fix things until they are fixed. If stuck on
the same issue after 3 attempts, stop and tell the user what is blocking. Do
not spin.

### 7. Deliver

When P0=0 and P1=0, you are done. Close the loop:

- Code committed in clean chunks
- Feature works end-to-end (not just unit tests)
- Brief summary for the user

The summary is not a report. It is a handoff:

```
Done:    [what you built]
Changed: [N files, key areas]
Tested:  [what gates passed]
Open:    [remaining P2s or known limits, if any]
Next:    [what the user should try first]
```

The user opens their laptop, reads 5 lines, tries the feature.
