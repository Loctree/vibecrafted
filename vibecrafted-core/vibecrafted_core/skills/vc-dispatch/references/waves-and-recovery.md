# vc-dispatch — Fast Wave, Refire, Cadence, Pulse & Failure Patterns

## Fast wave (blitz) — Founder-ordered bounded dispatch

When the Founder points at N verified findings and orders a wave ("dispatchuj
falę na te pakiety", "blitzkrieg, nie partyzantka"), the dispatcher IS the
brief author. Do not route through vc-scaffold, do not build a DRIVER, do not
ask clarifying rounds — the findings-with-evidence are the plan.

Shape (field-proven, loctree-suite findings-wave-2, 2026-08-22):

1. **Pre-flight stays**: fresh baseline SHA (fetch — HEAD moves between your
   diagnosis and the order), disjoint file domains per cut, shared-file
   regions declared explicitly in the briefs, sibling pending branches listed
   as do-not-touch.
2. **Lean brief per cut**, written by the dispatcher in minutes, not hours:
   frontmatter + mission + verbatim evidence (repro commands, line anchors) +
   files + acceptance (≥2 non-trivial tests) + gates + out-of-scope +
   substrate block + commit/trailer rules + report path + idempotency clause.
   Checklist of field-learned mines: `references/fast-wave-brief.md`.
3. **Founder pins ride verbatim**: agents and models named by the Founder
   (`gpt-5.6-sol | grok-4.6 | claude-opus-5`) go straight into the launcher
   `--model` flags and the tracker table. No silent substitution.
4. **Launch all cuts in parallel**, arm supervisor-side awaits immediately,
   write the lean tracker (cut | worker@model | run_id | branch | state).
5. **Dispatcher integrates**: single-thread, after settle, by diffs — the
   fast wave changes brief authorship, never the SPRAWDZENIE/FLIP rigor.

A fast wave is still a line: tracker, ledger evidence, declared verifiers and
integration receipts remain required. Complete the bounded acceptance without
claiming completion of a whole lifecycle.

## Refire = mini-marbles

Re-running the SAME prompt (vc-frame: `<ENTER> re-run` on the spawn pane, or
re-launching `--file` with the same path) is the cheapest convergence
primitive — hot substrate, the worker pays less for archaeology and spends
budget on deltas (vc-marbles: "Marbles exploits cache heat").

- **Precondition**: briefs must be IDEMPOTENT — written so a re-run on a tree
  where the work already landed verifies and stops ("nothing to do"), never
  duplicates.
- **Use refire when**: the task may be too huge for one worker round; the
  report says a sub-item was not done; you want marbles-style convergence
  pressure on a fragile surface.
- Prefer launcher dispatch over inline work precisely BECAUSE refire makes
  partial progress cumulative.

## Read/Write cadence

- Reads (pulse, artifacts, loct) are cheap and continuous; writes happen at
  loop boundaries: tracker/journal after each transition, prompt files before
  dispatch, own commits immediately (one unit = one commit, hook-formed,
  real session_id trailer).
- During waves: no incidental duplicate lint/test runs by the dispatcher, NO drive-by fixes in
  worker scope. Declared verifiers and integrator admission settle delivery;
  invoke formal audit when the Founder requests it.
- Dispatcher's own hands touch the repo only for: line bookkeeping, bounded bookkeeping repairs
  the Founder assigns directly (then: own commit obligatory), and recovery
  evidence gathering.

## Pulse & stall (hard rule, both postures)

Heartbeat is FRAMEWORK-FIRST — the loop/cron mechanics are already automated
in vibecrafted; do not hand-roll timers when these exist:

- `vibecrafted loop spanko --run-id <id> --agent <a> --verify '<cmd>'
--tracker <tracker.md> --cut-id <cut> --then '<next dispatch>'` — the
  command-rank dispatcher await loop: SPANKO → SPRAWDZENIE → FLIP → BATON;
- `vibecrafted loop start|next|status|complete` — line state machine with
  `--max-iterations` and `--completion-promise`;
- `vibecrafted cron line --root <repo> --every-minutes 10 --then-cmd
'vibecrafted loop next'` — real-crontab heartbeat that captures Loctree +
  AICX context per tick;
- `vibecrafted cron tick --after-idle-minutes 10 --then-cmd <cmd>` — resume
  an approved next command after an idle window.

Drive the await with the dedicated command (OUR vc-loop / cron) as the
STANDARD even from an interactive session — a dispatched run HAS the CLI. The
harness `/loop` is a true last-resort, only when the vibecrafted CLI is
genuinely unavailable.

On each tick, judge liveness by three independent signals per
`references/pulse-and-stall.md`: control-plane status, agent session-file
mtime+size, `git status` deltas. **≥10 min of silence on all three → kill the
launcher tree, check for orphans (an orphan often DELIVERS), then
recovery-dispatch with the evidence written into the BATON update** —
possibly a different agent. Never blind-restart; never kill on one signal
(a signal matching a known failure ≠ that failure).

## In-flight corrections

Founder overturns a delivered cut's policy mid-line → write a correction
brief (suffix `b`, e.g. C2→C2b), queue it respecting file overlaps, carry the
Founder's decision verbatim-spirit in the BATON. The mechanics of the old
cut stay; only the policy is corrected. Post-line findings (smoke bugs,
feature wishes) go to a backtracker file with code-truth anchors, become
backlog cuts on the Founder's button.

## Failure patterns (do not repeat)

- Prompt in argv; placeholders left unrendered. Gate on the **known
  placeholder tokens** (`grep -E '\{(repo|id|agent|workflow|resolved_workflow|reports_dir|tracker|baton)\}'`
  over the dry-run prompts, expect empty) — a naive `grep -c '{'` gate
  false-positives on rendered `{baton}` JSON, which legitimately carries
  braces (see `references/toml-plan-preflight.md`).
- Killing a supervisor racing its own loop — check `ps` children and
  `git log` after; the orphan often delivers.
- Founder heredoc typed into chat instead of shell — verify the file exists
  before referencing it.
- Re-running worker gates "to be sure" — claim vs proof is settled by SHA +
  hooks + audit layer, not by your duplicate build.
- Treating a teammate's hands in "your" file as a hazard — on the Living
  Tree a landed commit is the line's, not yours; divergence across rounds is
  signal for vc-polarize, not damage.
