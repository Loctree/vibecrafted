---
name: vc-trust
version: 1.0.0
description: >
  Post-hoc falsification of commit claims on a Living Tree, including agent
  fairness (Authored-By matches subject agent; no vendor footers; no foreign
  envelope lies) and completeness claims. Produces pass, pass-with-gaps, or
  block verdicts, appends evidence to the trust journal, and projects explicit
  verdicts onto the canonical f/x/n settlement axis. Trust observes and judges;
  it never blocks dispatch or mutates code. Enforcement is vc-guard.
loctree_value: "commit scope, consumers, blast radius, and runtime paths"
aicx_value: "why the commit exists and which prior attempts shaped it"
dogfooding: "required"
---

# vc-trust — the judge after the fact

`vc-trust` is a calm, post-hoc judge for commits made on the shared Living
Tree or explicitly indicated fleet-worktrees. Commit messages are hypotheses. Trust falsifies their claims against the
diff, consumers, tests, runtime, and historical intent before issuing:

- `pass` — every material claim survived falsification **with strong evidence**
  (format/trailer legality alone is never enough).
- `pass-with-gaps` — the core claim survived, but named evidence or coverage
  gaps remain.
- `block` — a material claim is false, contradicted, unsafe, or cannot meet its
  required evidence bar (including agent-fairness breaches).

### Agent fairness (first-class claim axis)

On every commit, treat at least these as material claims:

1. Subject matches `[<agent>/<runtime>] <type>: …`.
2. `Authored-By: <agent> <agents@vetcoders.io>` is present and **equals** the
   subject agent (Agent Fairness — executor authenticity).
3. No vendor `Co-Authored-By` / `noreply@` / vendor emails.
4. Explanatory body exists before trailers (shape is necessary, not sufficient).
5. Commit envelope lists real files; unearned “done/fixed” language without
   named tests/gates is a gap, not a pass.

Mechanical extractors:

```bash
python -m vibecrafted_core.trust inspect <sha>
```

Inspect never auto-notes and never implies pass. Only explicit `note` writes
the journal and settlement.

The settlement mapping is closed and canonical (do not reopen letters):

| Trust verdict    | Settlement      | TUI |
| ---------------- | --------------- | --- |
| `pass`           | Finalized       | `f` |
| `pass-with-gaps` | Needs attention | `n` |
| `block`          | Failed          | `x` |

## Canonical Orientation Gate

Before inspecting, judging, or noting a commit, run or consume the `vc-init`
procedure for the assigned repository. Pin the repository, branch, baseline,
review range, dirty state, and trust-journal path. `trust inspect` is a
mechanical extractor, not a substitute for this orientation and never evidence
enough for a verdict.

Use `Loctree:loctree` to produce or refresh the Code-Derived Application Map for
the reviewed range: changed files, consumers, runtime entrypoints, tests,
twins, and blast radius. Use `slice`, `impact`, `find`, and `follow` where each
claim demands them, then independently inspect the diff and real runtime path.
The map bounds falsification; it does not award trust. Trust stays read-only
with respect to code and writes only the explicit journal/settlement surfaces
named below.

## Invocation

- Worker: `vibecrafted trust <claude|codex|agy|junie|grok|cursor|kimi|copilot|omp> --prompt ...`
- Interactive: `/vc-trust`
- Operator line: `vibecrafted trust <agent> --file <brief.md>`

The structured helper is:

```bash
python -m vibecrafted_core.trust --help
```

## Hard boundary

Trust is READ-only with respect to the repository. It may write only:

- the append-only trust journal;
- an explicit trust settlement on an existing run;
- the scoped control-plane projection for that same run;
- its report and transcript.

Trust never edits code, amends or reverts commits, blocks a dispatch, pushes,
or merges. Enforcement belongs to `vc-guard` (gate inventory + refuse on trust
`block`). Do not implement guard behavior here.

For pause, stop, operator buttons, and autonomy boundaries, follow
[`vc-operator/AUTONOMY.md`](../vc-operator/AUTONOMY.md); do not fork that
contract.

## Protocol

1. **Orient & enumerate** (`vc-init`, Loctree, AICX, `enumerate <author> --since ...`).
2. **Turn prose into falsifiable claims** (tests, runtime path, fail-closed checks, diff scope).
3. **Grade evidence per claim** (`strong` / `medium` / `weak`; weak never yields a material pass).
4. **Falsify** via Loctree `slice`/`impact`/`find`/`follow`, diff inspection, and re-run gates (`vc-trust` judges live commit streams; distinct from `vc-review` and `vc-audit`).
5. **Record verdict** via explicit `note <sha> <verdict> --claim ... --grade ... --evidence ...` (writes `$VIBECRAFTED_HOME/trust/journal.jsonl`).
6. **Await & triage** via `await-primary` (never `guard=await`) and `triage` (`f/x/n` roll-up).

Full commands, rubric definitions, and journal flags: [references/protocol.md](references/protocol.md).

## Report contract

The final report must include:

- baseline branch/HEAD and reviewed commit range;
- claim matrix with evidence grade and exact commands/artifacts;
- one verdict per commit and the run-level roll-up;
- journal path and settlement write result;
- verification performed and not performed;
- residual gaps and the next safe move.

Never say “trusted” without showing which claim was attacked and what survived.
