---
name: vc-skillaunch
description: >
  This skill should be used when the user asks to "make this a skill",
  "create a skill from what we just did", "package this workflow",
  "distill this session into a skill", "turn this into a vc- skill",
  or "przepuść przez matrycę" for skill packaging. Distills a completed
  interaction or pattern into a reusable agent skill under the Delegation
  Matrix. Do not use for greenfield skills with no completed workflow
  (use the scaffolder + CONTRIBUTING-SKILLS instead).
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Invocation for `vc-skillaunch` (foundation skill)**
>
> Not a core `vibecrafted skillaunch <agent>` worker. Load interactively and
> execute in-session. Package other skills under the
> [Delegation Matrix](../DELEGATION_MATRIX.md) — per-launcher literals, no
> workflow paste, freer native when packaging needs depth, external fleet
> unchanged. See [Foundation skills](../DELEGATION_MATRIX.md#foundation-no-core-vibecrafted-name-agent-worker-of-their-own).

<!-- /fleet-imperative -->

# Workflow-to-Skill Distiller

Turns a completed workflow into a reusable agent skill. Specifically, this skill
extracts patterns from an interaction or workflow that **already happened** and
packages them.

## Canonical Orientation Gate

If the workflow being distilled depends on a repository, run or consume the
`vc-init` procedure before writing the skill contract. `Loctree:loctree` is the
default structural perception skill for that pass and must produce or refresh
the Code-Derived Application Map.

If fresh `vc-init` evidence is absent, perform the init pass first and treat
repo-dependent skill writing as blocked until repo truth exists.

If the workflow is not repo-specific, state the no-repo exception and distill
the interaction evidence directly.

> [!CAUTION] **You MUST complete Phase 1 (Brainstorming) before writing any code
> or SKILL.md content.** Skipping brainstorming produces skills that are either
> too rigid or too vague. The brainstorming conversation is the most important
> part of this process.

## Repository Work Doctrine

For repository work, start with Loctree as the map: use `loct context`,
`loct occurrences`, `loct body`, and `loct find --literal` before broad manual
search. Use AICX for intent and session context. Use rg/grep as fallback or
local magnifier, not as a replacement for structural mapping. If Loctree fails
or misses a surface, append feedback to `~/.vibecrafted/loctree/loctree-fail.md`.

## Phase 1: Brainstorming (MANDATORY)

Run an iterative back-and-forth conversation (2–3 questions per round, never all at once) covering five rounds: (1) Workflow inputs/outputs/cadence, (2) Step rigidity and error handling, (3) Existing skill dependencies, rate limits, and context files, (4) Scope, Delegation Matrix class (`core` / `meta` / `foundation` with exact literals), code-vs-instruction-only decision, and naming, (5) Optional validation sample query/answer. Proceed to Phase 2 only after all 10 completion criteria are answered.

Full question bank and completion checklist: [references/brainstorming-bank.md](references/brainstorming-bank.md).

## Phase 2: Skill Design

Produce a **design document** (as an artifact / implementation plan) and present
it to the user for approval. The document must include:

1.  **Skill name and description** (following YAML frontmatter rules: name ≤64
    chars, lowercase + hyphens; description ≤1024 chars; third-person triggers).
2.  **Matrix class + invocation table** (worker / interactive / operator) with
    concrete literals for **this** skill only.
3.  **Directory structure** showing all planned files (prefer progressive
    disclosure: lean SKILL.md, detail in `references/`).
4.  **Existing skills referenced** with rationale for each.
5.  **New scripts** (if any) with proposed subcommands and arguments.
6.  **Rate limiting strategy** for any APIs not covered by existing skills.
7.  **Error handling strategy** per step.

**Wait for explicit user approval before proceeding to Phase 3.**

## Phase 3: Implementation

### Guiding Principles

General guidelines for skill implementation:

- Use `uv run`, never `python` or `python3`.
- Prefer stdlib libraries that come with a default Python 3 installation
  (`urllib` preferred); Avoid libraries that require extra installation if
  possible.
- Rate limits must be documented and respected in code. Prefer
  **file-lock–based rate limiting** so that concurrent sub-agents sharing the
  same machine collectively respect the limit. See other skills in the Science
  Skills bundle for the canonical cross-process–safe implementation.
- Skill output must be <500 lines or redirected to a file. Long output files
  should be processed programmatically to extract relevant fields.
- Hyphens are recommended for the skill name and YAML `name:` field.

### Rule 1: Reuse Existing Skills

When the workflow uses functionality covered by an existing installed skill, the
new SKILL.md **MUST** reference it by name rather than reimplementing. Include a
**Dependencies** section in the SKILL.md listing required skills with a brief
rationale for each.

### Rule 2: Rate Limiting for New APIs

For any API interaction **not** covered by an existing skill, the generated CLI
script **MUST** implement rate limiting. Before writing any rate-limiting code,
**look up the API's official rate-limit guidelines**: check any documentation
the user provided during brainstorming, then search the API's public
documentation online. If no documented rate limit can be found, **default to 1
request per second**. The rate limiting pattern is built directly into the CLI
template at `references/cli_script_template.py` — see the `RateLimitError` class
and the `_request` method of the API client.

Key requirements:

- Use `time.monotonic()` for timing (not `time.time()`).
- Calculate delay from documented rate limits.
- Implement retry with exponential backoff for transient errors (5xx).
- Raise a dedicated `RateLimitError` when HTTP 429 is received.
- Log retry attempts to stderr so the agent can observe progress.
- Include the URL and rate-limit value in error messages.
- On non-retriable HTTP errors (e.g. 400, 403, 404), read and include the
  response body in the error message — not just the status code. API response
  bodies contain actionable details (e.g., "Invalid parameter") that enable
  the agent to self-correct.

### Rule 3: CLI Script Pattern (Default When Code Is Needed)

**This is the default choice.** If **any** step in the workflow involves API
calls, data processing, file I/O, computation, or any other programmatic work,
produce a multi-command CLI script using `argparse` with subcommands. Follow the
template in `references/cli_script_template.py`.

Key requirements:

- Each major workflow step becomes a subcommand.
- All subcommands accept `--output` for writing results to a file.
- Use `json.dump` with `indent=2` for JSON output.
- Print a success message with the output file path.
- Exit with code 1 on errors.
- Make arguments like `--limit` **required** (no silent defaults). This forces
  the agent to specify the value explicitly, preventing it from assuming it
  retrieved "all" results when it was silently capped.

### Rule 4: Default to File Output

All scripts and workflows **MUST** write output to files, not stdout. Stdout
should only contain short status messages (e.g., "Success! Data written to:
results.json"). This is critical because:

- API responses can be very large and will truncate in terminal output.
- File output is token-efficient — the agent reads only the fields it needs
  using `jp` or Python one-liners.
- Large stdout output wastes context window space.

### Rule 5: Instruction-Only Pattern (Only When No Code Is Needed)

Use this pattern **only** when the workflow requires **zero** programmatic work
— i.e., every step is purely about orchestration, reasoning, multi-skill
coordination, or following a written protocol. If any step needs code (API
calls, data processing, file I/O, etc.), use the CLI pattern from Rule 3
instead. Produce a SKILL.md with a structured workflow section:

```markdown
## Workflow

### 1. Step Name

- Description of what to do
- Which skill to use and how

### 2. Next Step

...
```

### Rule 6: SKILL.md Structure

Every generated SKILL.md must follow this structure (imperative body language;
third-person `description` with concrete triggers):

```markdown
---
name: { skill-name }
description: >-
  This skill should be used when the user asks to "…", "…". {outcome}.
version: 0.1.0
---

<!-- fleet-imperative: v3 -->

> **Invocation for `vc-{name}` (launcher `{name}`)** — table of three paths
> with **this** skill's literals. Link [DELEGATION_MATRIX.md](../DELEGATION_MATRIX.md).
> Foundation skills: state "no worker CLI" explicitly.

<!-- /fleet-imperative -->

# {Skill Title}

## Overview

{Brief description of what the skill does.}

## Dependencies

{List of required skills, if any.}

## Quick Start

{Minimal example using the real launcher literals.}

## Utility Scripts (if CLI-based)

{Document each subcommand with examples.}

## Workflow (if instruction-only)

{Numbered steps with clear instructions.}

## Rate Limiting (if applicable)

{Document rate limits and how they are enforced.}

## Common Mistakes

{List 2-3 common pitfalls — include "workflow paste" if relevant.}

## Verify before the handoff

{Link VERIFICATION_RULE.md when the skill can claim done.}
```

### Rule 7: Progressive Disclosure

- Keep SKILL.md lean (~1.5–3k words). Move long procedures to `references/`.
- Do **not** copy the full Delegation Matrix into the skill body.
- Do **not** paste ERi / `vc-workflow` rails onto non-workflow skills.
- Prefer `tools/vc-skill-new.sh` for greenfield scaffolding; this skill distills
  completed interactions.

## Phase 4: Validation

After implementation is complete:

1.  **Matrix check** — invocation rail matches class; no generic
    `vibecrafted <workflow>` blur; literals match skill name.
2.  **Skill-development check** — third-person triggers, imperative body,
    progressive disclosure, examples present.
3.  **Test the skill manually** by invoking the agent with a natural-language
    prompt that should trigger the new skill.
4.  **If a sample query/answer was provided** during brainstorming, run it
    through the skill and verify the output matches expectations.
5.  **`make test-skills`** when packaging into the vibecrafted skills tree.
