---
name: vc-intents
version: 2.0.0
description: >
  Find candidate intents in source material for one repository inside a chosen window, settle
  every one of them against the live code with two independent fleets, and hand
  back a stable, dependency-ordered plan of cuts for vc-dispatch. Use whenever
  the team asks "collect intents", "reconcile intents", "what do the sources establish",
  "what did we promise but not deliver", "which planned work exists in code", "what did we
  agree to build", "what is still owed", "intent coverage", "planned vs code",
  "highest truth", "checklist from intents" — or when scattered decisions from
  transcripts and sessions must become an implementation queue that survives
  compactions and machines. Reach for this instead of a bare `aicx search`
  whenever source statements must be distinguished from model classifications and
  agent completion claims, and the answer must end in a plan, not a catalogue.
loctree_value: "structural questions decide whether a promise has a runtime shape"
aicx_value: "indexed intents, session context; one source among several"
dogfooding: "required — this skill is the join between corpus, aicx, Loctree and dispatch"
---

<!-- fleet-imperative: v3 -->

> **Invocation for `vc-intents` (launcher `intents`)** — see the
> [Delegation Matrix](../DELEGATION_MATRIX.md).
>
> | Path                    | Literal for this skill                                                                                |
> | ----------------------- | ----------------------------------------------------------------------------------------------------- |
> | 1. User-launched worker | `vibecrafted intents <agent>` — one lane of extraction or confrontation, READ, writes only its JSON   |
> | 2. Interactive          | `/vc-intents` — the hunt itself, **in this session**: sweep, lanes, plans, merge, queue, render       |
> | 3. Agent-operator       | dispatches the worker form through `vc-dispatch` with a plan written by `scripts/intents_cli.py plan` |
>
> Cadence stays **read**: this skill never edits the repo. Delivery is a
> separate `implement` plan it writes for the fleet.

<!-- /fleet-imperative -->

# vc-intents — from source evidence to a plan of cuts

A long-lived project accumulates statements faster than code. A source from March
may conflict with one from May; an agent may propose another shape in June and
claim it shipped in July. Reconstruct the context before deciding what applies
to this repository and the active user task.

This skill owns the whole path: **collect → separate voices → verbatim catalog →
confront with two fleets → reclassify what "landed" hides → stable queue → a
dispatch plan the fleet can run**. `vc-canary` finds truth collisions and never
refactors; `vc-implement` cuts code but does not reconstruct what was promised;
`vc-audit` falsifies a plan against code. `vc-intents` reconstructs the promise,
proves what is left of it, and hands the rest over as cuts.

## Goal

`vc-intents` produces a ledger in which every candidate intent from the chosen
window carries one explicit disposition, an agreement score between two
independent fleets, and a human-editable override layer — and it is done when
`intents_cli.py <workdir> status` names what is still open and
`plan --stage implement` has written a dispatch plan for it. A catalogue does
not close the goal. An audit does not close the goal. The plan of cuts does.

## Canonical Orientation Gate

Before any repo-specific step — sweep against a repo, confrontation, plan —
run or consume the `vc-init` procedure for the assigned repo. `Loctree:loctree`
is the default structural perception skill for that pass and must produce or
refresh the Code-Derived Application Map (`context`, `repo-view`, `focus`,
`slice`, `impact`, `find`, `follow`). Confrontation lanes inherit this: the
brief makes loctree-mcp the first move, and a `landed` without a structural
path behind it is not a verdict. If fresh `vc-init` evidence is absent, perform
the init pass first and treat the hunt as blocked until repo truth exists. A
sweep of a transcript corpus with no repo attached states the no-repo exception
in its report.

## Scope is a window, not a history

Bound the hunt before sweeping: `--since/--until`, or a theme. Coverage is
reported against that window. The whole history is one legal window among
others — not a precondition of closure. What the window does not contain is
recorded as _not in scope_, never as _absent_.

## The tool

One shared CLI serves both variants. English is the default (`--lang en`).
Use `<workdir> --lang pl <command>` to select Polish briefs, prompts, reports
and review output. Source quotes always keep their original language.

```bash
CLI=~/.claude/skills/vc-intents/scripts/intents_cli.py   # or the store path
W=~/.vibecrafted/artifacts/<owner>/<repo>/intents         # one workdir per hunt
uv run "$CLI" "$W" <command> …
```

One working directory holds everything that must survive a compaction or a
second host: `sweep.json`, `shards/`, `intents.json`, `lanes/`, `LEDGER.json`,
`overrides.jsonl`, `queue.json`, `STABLE-QUEUE.md`, `LEDGER.md`,
`intents.html`. Agents read and judge; the script keeps the books, performs the
falsifications that need no judgment, and writes the plans that hand the
judging to a fleet.

## Procedure

Run the full 10-step hunt via `intents_cli.py`: 0. **Orientation** — `vc-init`, `aicx intents -p /<repo>`, and newest-intent vs newest-commit check.

1. **Sweep / Append** — `sweep --since/--until` (never re-sweep on new days; use `append` or `append --abort`).
2. **Extract** — throughput flash fleet (`references/extraction-brief.md`, `verify-quotes --strict`; `quote` must be verbatim).
3. **Separate voices** & **4. Chronology** — distinguish speaker/model/project; supersede only via `superseded_by`.
4. **Confront** — two independent fleets on two hosts (`references/confrontation-brief.md`, `references/loctree-questions.md`, `merge`).
5. **Reclassify** — `reclassify` applies `landed-contested` and `landed-by-doc` (`references/ledger-schema.md`).
6. **Human layer** — `render --html` + `decide` into `overrides.jsonl` (`references/review-surface.md`).
7. **Queue & Plan** — `queue --min-strength 4` then `plan --stage implement` (active user task/plan authorizes work).
8. **Closure** — `status` exits 0 only when zero open dispositions, zero unavailable/truncated sources, and all `landed` have `runtime_verified = yes`; on compaction re-entry read `LEDGER.md` + `status` + `queue` without re-sweeping.

Full commands, field baselines, append transaction recovery, and step rules: [references/procedure.md](references/procedure.md).

## Output contract

1. **Coverage** — window, sources with state (`read`/`empty`/`unavailable`/
   `truncated`), files and rows per source.
2. **Catalog** — candidates with quote containment checked, rejected quotes with reasons.
3. **Ledger** — per-host verdicts, agreement per pair, effective disposition,
   overrides (rule and human), `runtime_verified`.
4. **Queue** — stable open intents with the ordering rationale.
5. **Plan** — `intents-implement.<host>.dispatch.toml`, doctor-clean.
6. **Highest truth** — the one unresolved reality that should hurt a little.
   "43 % of what two fleets called landed is contested by source
   complaints" is a highest truth; "some items are partial" is not.

## Anti-patterns

Treating a ranked aicx hit as a read source · a paraphrase in `quote` · one
fleet's verdict as evidence · `landed` from `docs/*.md` · `superseded` without a
successor · re-running the sweep on re-entry · frontier models for mass reading
· the verifier `run` naming a lane literal (`release` inside `L6-build-release`
trips the dispatch hard-stop scan; the script spells paths through `{id}`) ·
pressing a hard-stop because the queue said so · reporting a green audit as
closure while the queue is non-empty.

## Related skills

`vc-init` before everything · `vc-canary` when two modules compete for the
truth an intent needs · `vc-dispatch` runs every plan this skill writes ·
`vc-implement` / `vc-ownership` are the cuts · `vc-trust` falsifies a worker's
completion claim afterwards · `vc-audit` for a written plan rather than a
corpus.

## Verify before the handoff

Walk around the truck — [Verification Rule](../VERIFICATION_RULE.md): the
ledger exists and `status` says OPEN with reasons you can name; the plan passed
`vibecrafted dispatch --doctor`; the HTML opens with the right host names and
working code links; every number in the report comes from a file in the
workdir, not from memory.

---

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
