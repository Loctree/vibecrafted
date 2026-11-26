# vc-research — Launch Config, 6-Step Plan Template & Anti-Patterns

## Launcher Invocations & Runtime Config

Enter the framework session via `vibecrafted start` (or `vc-start`). Then launch through the command deck — never raw `skills/.../*.sh` paths:

```bash
vibecrafted research --prompt 'Compare auth libraries for Tauri desktop'
vc-research --prompt 'State of the art for MCP streaming transports'
vibecrafted research --file /path/to/research-plan.md
vc-research codex agy --prompt 'Override lanes for this run'
```

Research defaults to detached headless lanes both inside and outside vc-frame. Prefer `--file` for an existing plan and `--prompt` for inline intent. Use an explicit terminal runtime only for a TTY-required compatibility lane.

Runtime lane defaults are read at launch time from `${VIBECRAFTED_HOME:-$HOME/.vibecrafted}/config/research.yaml`. Missing file means built-in defaults: `claude`, `codex`, `agy`, with no model pins and last-survivor synthesis. The packaged commented example lives at `runtime/vc-research/research.yaml.example`; copy it into the runtime config dir to edit operator policy without touching the repo or reinstalling.

---

## Step 2 — Research Plan Template

Create one plan file. Every agent receives this plan:

```markdown
---
run_id: <generated-unique-id>
agent: <claude|codex|agy|cursor>
skill: vc-research
project: <repo-name>
status: in-progress
---

# Research Plan: <title>

## Problem

<co-defined problem statement>

## Questions

1. <specific, answerable question>
2. ...

## Mandatory tools

- loctree MCP (repo-view, slice, find, impact) — for codebase questions
- Brave Search or WebSearch — for external ground truth

## Encouraged tools (agent's choice)

- Context7 (resolve-library-id → query-docs) — for library docs
- WebFetch — for URLs found via search
- Codebase grep — for internal patterns (only after loctree mapping)

## Report format

Each question answered with: **Sources**, **Finding**, **Confidence** (high/medium/low), **Evidence**.
Conclude with **Synthesis**: recommended approach, alternatives, open questions, implementation notes.

## Constraints

- Append current year to search queries for freshness
- Prefer primary sources (official docs, RFCs, source code) over blog posts
- If two sources disagree, note the disagreement explicitly
- Do not hallucinate API signatures — verify them
```

`vc-research` records the effective plan under `$VIBECRAFTED_HOME/artifacts/<org>/<repo>/<YYYY_MMDD>/research/<run_id>/plans/<ts>_<slug>_research-plan.md`. Plans can be split for separable domains, but each agent gets ALL plans — they are independent researchers, not specialists.

---

## Step 3 — Spawn the Research Swarm (Forms & YAML Schema)

```bash
PLAN="$VIBECRAFTED_HOME/artifacts/<org>/<repo>/<YYYY_MMDD>/plans/<ts>_<slug>_research-plan.md"
vc-research --file "$PLAN"
```

Repo-owned spawn scripts remain the internal engine. Do not document raw `bash skills/...spawn.sh` paths as the operator entrypoint.

The launcher keeps one common `run_id` and starts the configured headless lanes against the same plan. Defaults are claude + codex + agy. vc-frame may project the run; the explicit terminal compatibility lane uses one shared `research.kdl` tab. Divergence between reports reveals blind spots.

Supported invocation forms:

```bash
# Canonical agentless form: full configured swarm.
vibecrafted research --prompt "State of the art for MCP streaming"
vibecrafted research --file "$PLAN"

# Backward-compatible core form: full configured swarm, claude synthesizes.
vibecrafted research claude --file "$PLAN"

# Shell override form: exactly these lanes for this run; codex synthesizes.
vc-research codex agy --prompt "Compare two toolchains"

# Explicit synthesizer override.
vc-research claude codex agy --synthesizer claude --file "$PLAN"
```

Runtime YAML schema:

```yaml
lanes:
  - agent: claude
    model: claude-opus-4-6
    enabled: true
  - agent: codex
    model: gpt-5.5
    enabled: true
  - agent: agy
    # Unsupported model flags are reported honestly in receipts.
    model: gemini-pro
    enabled: true
lane_count: 3
synthesizer:
  agent: claude
  model: claude-sonnet-4-6
```

Precedence is: built-in defaults < legacy TOML fallback < runtime YAML < env/positional override < per-run `--model` flags. Unsupported model flags are not silently dropped; the receipt records `model_override_supported: false`, `model_override_skipped: true`, and `model_override_skip_reason: unsupported_agent_model_flag`.

Immediately after spawn, the operator gets a launch card with shared `run_id`, run directory, reports directory, summary path, and the exact await command. **The launch card is the default surface.** `observe --last` is a drilldown tool, not the primary source of truth.

---

## Step 4 — Collect Reports

Reports land in:

```
$VIBECRAFTED_HOME/artifacts/<org>/<repo>/<YYYY_MMDD>/research/<run_id>/reports/{claude,codex,agy}.md
```

Launch card lives at `research/<run_id>/summary.md`. Metadata, transcripts, raw streams, prompts, launchers, vc-frame layout stay inside `research/<run_id>/logs/` and `research/<run_id>/tmp/`.

Wait for all three through the dedicated runtime helper:

```bash
vc-research-await --run-id <run_id>
vc-research-await --last     # newest swarm
```

For transcript-level inspection while the swarm is running:

```bash
vibecrafted observe claude --last
vibecrafted observe codex --last
vibecrafted observe agy --last
```

Do not treat manual `observe --last` calls as sufficient observability. Workflow state goes through launch metadata, the await helper, and durable report paths by default.

---

## Step 5 — Synthesize (Layered Slicing & Rules)

**Before citing a single line of any source report, you MUST have read each report in full via layered slicing.** Non-negotiable.

Most reports run 30-100KB. Tools cap output at ~25KB and dump the rest to a file with a "see path: ..." warning. Skipping that file because it's "long" or working only from the warning text is the failure mode this skill exists to prevent. A synthesis built from truncation warnings is a hallucination wearing the costume of expertise.

Per source report:

1. Read in full via offset/limit slicing in spans of ~1500-2000 lines (or ~80,000 chars).
2. Record coverage in synthesis section "0. Coverage statement" — lines/bytes per source report.
3. If a report is too large for the available budget, **HALT** and report the boundary. Do NOT cite line ranges you have not actually read.

**Synthesis = operator's expert opinion built ON the three reports, NOT a copy.** Two sections: **A. Convergent (deduplicated)** and **B. Signals (single-agent findings — potentially key insights)**. Voting/majority rules explicitly rejected.

- **A. Convergent** — findings where two or three reports overlap, reduced to one statement. Cite agreeing reports with file:line. If one didn't address the question, note explicitly (silence ≠ disagreement).
- **B. Signals** — findings surfaced by only one agent. NOT lower-priority. Often the actual direction the work needed. Per signal: what (file:line) + why others missed it + operator verdict (amplify / flag / acknowledge & reject) + reasoning.

---

## Anti-Patterns

- Passing `claude|codex|agy` to `vc-research` (defeats the purpose — the launcher is the swarm)
- Giving each agent different questions (they must answer the SAME questions for triangulation)
- Running `vc-research` three times for claude/codex/agy; one invocation already launches the swarm
- Skipping synthesis and concatenating reports (the value is in the delta)
- Researching things you can verify by reading one file (use loctree slice)
- Writing the research plan without the user (Step 1 is collaborative)
- Trusting blog posts over official documentation
- Letting agents research without loctree context (they ask wrong questions)
- Jumping to raw `*_spawn.sh` invocations when `*-research` exists in the real shell helper surface
- Patchwork meta-artifact synthesis (verbatim concat of 3 reports)
- Compressed-view synthesis (operator paraphrase only, no file:line refs)
