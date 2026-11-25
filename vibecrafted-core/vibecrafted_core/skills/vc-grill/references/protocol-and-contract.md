# vc-grill — Design Tree, Turn Protocol & Design Contract Reference

## Design Tree (Full Branch Guide)

Visit each relevant branch in this order, skipping decisions already settled by fresh evidence or an explicit Founder answer:

1. **Scope & Boundaries:** the user outcome, the smallest useful cut, and explicit exclusions.
2. **Architecture & Data Model:** state ownership, contracts, persistence, and existing shapes worth reusing.
3. **Runtime & Integration:** entry points, callers, execution substrate, integration ownership, and error propagation.
4. **Edge Cases & Failure Modes:** unavailable services, permissions, races, interrupted work, and recovery behavior.
5. **Verification & DoU:** observable acceptance, meaningful tests, and the product evidence needed to find, try, understand, trust, and ship the result.

Do not invent uncertainty to fill the tree. Ask the next unresolved decision whose answer unlocks the most dependent choices.

## Turn-by-Turn Protocol

Before the first question, inspect the available evidence and identify the main ambiguity. For each turn:

- Name the current node and give the brief context that makes the choice matter.
- Present the relevant options with a benefit and a cost for each.
- State **My recommendation (agent):** the chosen option and its reason.
- Ask one direct question selecting that decision, then wait.
- Record the answer with its attribution and update the remaining tree.

When available, a question tool can present this single decision. Otherwise ask in the chat. Tool availability does not justify batching questions or moving the interview into a background run.

## Stop Condition & Design Contract Template

Finish when the relevant branches have no unresolved blocking dependencies or hidden implementation assumptions. If the Founder ends the interview early, label the contract partial and expose unresolved decisions; do not invent answers.

Return a concise **Design Contract** in the conversation, ready to feed an implementation plan or `vc-dou`:

- **Goal & scope:** the desired outcome and explicit boundaries.
- **Decisions:** agreed choices, alternatives rejected, reasons, and attribution to Founder answers, source evidence, or agent proposals.
- **Architecture & runtime:** state and contract ownership, entry points, integration path, and failure/recovery behavior.
- **Acceptance & DoU:** concrete observable outcomes, verification steps, and required product evidence.
- **Open items:** any explicitly deferred questions, their impact, and owner; blocking questions keep the contract partial.

The interview produces a contract. Implementation follows the user's authorized scope; completing the interview does not itself authorize edits or publication.
