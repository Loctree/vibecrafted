# vc-skillaunch — Phase 1 Brainstorming Question Bank & Checklist

## Phase 1: Brainstorming (MANDATORY)

Have an **iterative back-and-forth conversation** with the user. Do NOT ask all
questions at once. Pick 2-3 relevant questions per round from the bank below,
refine your understanding, and ask follow-ups.

### Round 1: Understand the Workflow

Start by summarizing what you observed from the workflow, then ask:

1.  "Here's my understanding of the workflow: [summary]. Is this accurate? What
    would you change?"
2.  "What are the expected inputs and outputs for this workflow?"
3.  "How often do you expect to run this workflow? Is it recurring or one-off?"

### Round 2: Flexibility and Error Handling

For each step identified in the workflow, determine its rigidity:

1.  "For [step X], if the primary approach fails (e.g., API down, no results),
    should the agent: (a) ask you for guidance, (b) try alternative approaches
    automatically, or (c) fail loudly with an error?"
2.  "Are there any steps where the exact method matters (e.g., must use a
    specific database), vs. steps where any reasonable approach is fine?"
3.  "Should the skill handle edge cases silently or surface them to the user?"

### Round 3: Dependencies and Resources

Before asking these questions, check which of your installed skills overlap with
the workflow. If an existing skill from the science bundle covers a step, the
new skill **MUST** reference it — do not offer a self-contained option.

1.  "I noticed the workflow uses functionality covered by [existing skill X,
    skill Y]. The new skill will reference these rather than reimplementing
    them. Are there any other tools or skills you'd like me to incorporate?"
2.  "Are there any API rate limits I should be aware of for services used in
    this workflow that aren't already covered by an existing skill?"
3.  "Are there specific files that provide important scientific context for
    creating this skill? For example: API documentation, reference papers,
    example datasets, or domain-specific notes. If so, please share them and I
    will incorporate their content into the skill's reference materials."

### Round 4: Scope, Shape, and Matrix Class

1.  "Our workflow covered [X, Y, Z]. Should I distill all of these into the
    skill, or is there additional functionality that's important to include?
    Conversely, should any of these be left out?"
2.  **Delegation Matrix class** — decide before naming the launcher:
    - **Core launcher** — will ship as `vibecrafted <name> <agent>` / `/vc-<name>`
    - **Meta** — init / ship / dispatch / operator-style surface
    - **Foundation** — no worker CLI; loaded inside other skills
      Confirm the class and the exact literals with the user. Never invent
      `vibecrafted <workflow> <agent>` as a universal placeholder. Read
      [`DELEGATION_MATRIX.md`](../../DELEGATION_MATRIX.md).
3.  Determine whether the skill needs any code. If any step involves calling an
    API, processing data, reading/writing files, or computing results, the skill
    **needs code** and you should default to the CLI pattern. Only use a
    text-only instruction skill when every step is purely about reasoning,
    coordinating existing tools, or following a written protocol with no
    programmatic work at all. Confirm your assessment with the user in plain
    language:
    - If code is needed: "Some of these steps involve [fetching data from an
      API / processing files / computing results], so I'll create a helper
      script that the agent can run for you. The script will have simple
      commands like `search`, `fetch`, `analyze`, etc. — you won't need to
      write any code yourself. Does that sound right?"
    - If no code is needed: "This workflow is entirely about following a set
      of steps and using existing tools — no new code is needed. I'll write it
      as a set of clear instructions the agent follows. Does that sound
      right?"
4.  If a helper script will be created: "I'm thinking the script should have
    these commands: [proposed commands in plain English, e.g. 'search for
    proteins', 'fetch results', 'compare sequences']. What would you add or
    change?"
5.  "What should the skill be called? Proposed name: `[suggestion]`."
    If core launcher: proposed CLI `vibecrafted <launcher> <agent>` must match.

### Round 5: Testing (Optional)

1.  "Can you provide a sample query and expected answer that I can use to verify
    the skill works as intended? For example: 'If I ask [question], the skill
    should produce [answer].' This is optional but helps me validate the skill
    during development."

### Brainstorming Completion Criteria

You are ready to move to Phase 2 when you can confidently answer ALL of:

- [ ] What is the workflow's purpose and scope?
- [ ] What are the inputs and outputs?
- [ ] Which steps are strict vs. flexible?
- [ ] Which existing skills should be referenced?
- [ ] What new scripts (if any) are needed?
- [ ] What rate limits apply?
- [ ] How should errors be handled?
- [ ] Does the workflow need any code? (If yes → CLI pattern; if no →
      instruction-only)
- [ ] Matrix class (core launcher / meta / foundation) and exact literals?
- [ ] Is there a sample query/answer for validation?
