---
name: vc-grill
version: 1.0.0
description: >
  Interactive design and intent interview protocol before code execution or planning.
  Walks down each branch of the decision tree one question at a time, resolving
  dependencies, stating explicit recommendations, and verifying ground truth in the
  codebase before asking. Trigger: "grill me", "vc-grill", "/grill-me", "zrób mi wywiad",
  "przemagluj mnie", "przemagluj plan", "interview me", "rozbij decyzje".
loctree_value: "code truth exploration before asking questions that the codebase already answers"
aicx_value: "historical decisions, past intents, and recorded preferences"
dogfooding: "recommended before complex architectural changes or ambiguous tasks"
---

# vc-grill — Interactive Intent & Design Interview

## Invocation

Invoke `/vc-grill` or ask the agent to use `vc-grill` in the current conversation.
Conduct the interview interactively with the Founder in this session. This skill
has no CLI launcher, shell alias, or headless worker form.

Use it when requested or when unresolved intent, design choices, or architectural
tradeoffs need a shared decision. It is not a mandatory interview stage for every
task. A known bug with a clear repair and acceptance criteria can proceed within
the existing authorization without an interview.

## Purpose

Reach a shared, unambiguous understanding of the task's architectural, functional,
and UX choices. Walk each relevant branch of the design tree, resolving decision
dependencies one at a time. Investigate facts yourself; ask the Founder to decide
intent and tradeoffs.

## Canonical Orientation Gate

For repository work, run or consume fresh `vc-init` evidence before the first
question. Use `Loctree:loctree` to inspect the Code-Derived Application Map:
`context`, `focus`, `slice`, `impact`, `find`, and `follow`. Use AICX to recover
prior decisions, intents, and preferences; verify historical claims against the
current code. Reuse fresh evidence and refresh the specific surface that drifted.

Read configuration, schemas, callers, and relevant commit history before asking
about existing behavior. Never ask the Founder where a file lives or how a
function currently works when the repository can answer it. For a task without
a repository, inspect the supplied material and identify the missing intent.

## Interview Rules

1. **Loctree & AICX first.** Resolve code truth before asking. Questions belong
   to business intent, design preferences, architectural tradeoffs, and unsettled
   edge behavior. Surface conflicts between recorded intent and current runtime
   evidence instead of silently selecting one.
2. **Exactly one question at a time.** Ask about one decision node and wait for
   the answer before entering a dependent branch. Never send a questionnaire or
   several questions in one tool call. A missing answer is not consent.
3. **Always recommend a choice.** Every question includes options and their
   costs, followed by an explicit agent recommendation and a concrete reason.
   Attribute your inference to yourself; only the Founder chooses for the Founder.
4. **Traverse dependencies.** Start with foundations and move toward detail.
   Track resolved nodes, open nodes, and their dependencies. Revisit a prior node
   when a later answer changes its assumptions; explain the dependency.
5. **Use the Founder's discovery language.** Polish is welcome. Settle the
   thesis and proof obligations before translating into delivery prose.

## Design Tree

Visit relevant unresolved branches in dependency order (skipping choices already settled by fresh evidence or Founder answers): **1. Scope & Boundaries** · **2. Architecture & Data Model** · **3. Runtime & Integration** · **4. Edge Cases & Failure Modes** · **5. Verification & DoU**. Ask the unresolved node that unlocks the most dependent choices. Full branch details: [references/protocol-and-contract.md](references/protocol-and-contract.md).

## Turn-by-Turn Protocol

Inspect available evidence first. On each turn: name the node and why it matters, list options with benefits and costs, state **My recommendation (agent)** with reason, ask one direct question and wait, then record the attributed answer. Single-question tools are fine, never batch questions or background the interview. Full turn protocol: [references/protocol-and-contract.md](references/protocol-and-contract.md).

## Stop Condition & Design Contract

Stop when relevant branches have no unresolved blocking dependencies or hidden implementation assumptions (if ended early, mark the contract partial and list open decisions without inventing answers). Return a concise **Design Contract** covering Goal & scope, Decisions (with attribution), Architecture & runtime, Acceptance & DoU, and Open items; completing the interview does not authorize edits or publication. Full contract template: [references/protocol-and-contract.md](references/protocol-and-contract.md).

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
