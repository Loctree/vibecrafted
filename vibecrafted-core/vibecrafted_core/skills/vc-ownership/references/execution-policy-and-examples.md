# vc-ownership — Desktop Control, Agent Policy, Output Style, Anti-Patterns & Examples

## Desktop And Browser Control

When environment and tooling allow it, ownership mode may include direct
interaction with apps, browsers, or the desktop.

Examples:

- clicking through a local app to verify UX
- driving browser-based flows
- capturing screenshots or screencasts
- validating a packaging or onboarding path end-to-end

Use this power pragmatically, not theatrically.
The point is to close the loop on reality.

Prefer the safest effective method available:

1. app-native/browser-native automation
2. deterministic local tooling
3. system click automation only when needed

Never surprise the user with broad desktop actions outside task scope.

## Agent Policy

Ownership mode encourages delegation, but not abdication.

Use agent swarms when they give us one of these:

- comparative reasoning
- faster parallel implementation
- independent review
- convergence loops

Keep these rules:

- main thread owns strategy
- reports beat vibes
- one resumed agent may spawn one bounded helper if the controlling skill allows it
- synthesis stays in the main thread
- **dispatch workers headless.** A live `VC_FRAME_SESSION_NAME` identifies the
  human User Session; it does not make that session the worker host. CLI and MCP
  fleet runs default to detached headless execution and remain observable
  through run state, transcripts, `observe`, and `await`. Use
  `terminal`/`visible` only for an explicit provider TTY exception; `init`,
  `operator`, and bare interactive `resume` keep the real human-owned PTY.

## Output Style

When reporting progress or completion in ownership mode, default to:

- **Current state** — what was wrong or incomplete
- **Proposal** — the stronger shape we chose
- **Execution** — what we changed and verified
- **Open risks** — what still matters
- **Next move** — the highest-leverage continuation

If the task is simple, compress this. If the task is broad, keep it structured.

## Anti-Patterns

Do not in ownership mode:

- code yourself by default
- ask questions without setting the `cron` or similar available
  tool while user is absent
- ask the user to micromanage obvious decisions
- preserve bad architecture just because it already exists
- stop at code while leaving product shell unfinished
- create extra systems when one sharp rewrite would do
- claim wow effect and deliver a placeholder
- claim done before review/followup/audit/DoU has checked the result

## Examples

**Example 1:**
Input: "I have to go out for 5 hours. We have this `<feature>` well and thorougly discussed.
Take the wheel and deliver it autonomously.
Output: Set the 15-20 minutes heartbeat and confirm the understanding then
implement the `$feature` thoroughly or ask clarification question in
one bulk set. If not answered proceed with the chosen workflows
autonomously until the goal is acomplished

**Example 2:**
Input: "You drive. I want this local AI stack to feel production-ready."
Output: diagnose runtime truth, pick the architecture, use agents where useful, implement, test, package, and report the
next real blocker.

**Example 3:**
Input: "Od a do z, z wow efektem."
Output: interpret that as a mandate for end-to-end delivery with bold but tasteful decisions, not a request for
decorative fluff.
