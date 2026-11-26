# vc-review — Falsification Rules, Evidence Rubrics & Anti-Patterns

## Default Stance: Falsification

Default verdict for every spec-claim the diff makes is **UNVERIFIED**.
PR descriptions, commit messages, "fixes #123" markers, and prior agent
reports are _claims_, not evidence. `vc-review` converts those claims
to evidence by inspecting code + tests.

### Hard Non-Trust Rules

You MUST NOT trust PR description bullets, commit messages naming the
fix, `// done` / `# implemented` inline comments, prior `vc-followup`
or `vc-review` reports, frontmatter status on linked task files,
AICX / chronicle / memory slices, or "fixes #123" / "closes #456"
annotations — unless **independently confirmed in current code/tests**.

### Evidence Taxonomy

Every finding carries an explicit evidence grade:

| Grade  | Criteria                                                                         |
| ------ | -------------------------------------------------------------------------------- |
| STRONG | Code in diff + test asserting exact behavior + negative check (old path removed) |
| MEDIUM | Code in diff + weak/general test, or type-system-enforced                        |
| WEAK   | Code in diff only, no test, no negative check                                    |
| NONE   | No direct evidence — finding tagged `[VERIFY]`, severity capped at P3            |

A "ready to merge" recommendation is only valid if every P0/P1
candidate finding scored STRONG or MEDIUM. WEAK on a P0 candidate
means the review itself is UNVERIFIED on that axis.

### Stage-Aware Verdicts

Most PRs are mid-stage. A PR landing Stage 1 of 3 must NOT be marked
P1-blocking because Stage 2 is queued. Tag each finding explicitly:

- `[STAGE-OK-DEFERRED]` — gap is explicitly out of scope for this PR
- `[STAGE-PARTIAL]` — landed stage has a real gap inside its scope
- `[STAGE-DRIFT]` — PR mixes deferred and landed scope without saying so

Stage tags ride alongside P-level: `[P2][STAGE-OK-DEFERRED]` is a
hygiene note, not a merge blocker.

### P-Level Scale

| P-level | Definition                                           | Examples                                              |
| ------- | ---------------------------------------------------- | ----------------------------------------------------- |
| **P0**  | Blocker merge / security / data loss / failing gate  | Failing tsc, leaked credentials, missing artifacts    |
| **P1**  | High regression risk in core flow, breaking contract | Breaking API, large untested changes, critical cycles |
| **P2**  | Medium: edge cases, a11y, telemetry, partial tests   | Missing i18n keys, hardcoded URLs, no error handling  |
| **P3**  | Low risk / hygiene / minor drift                     | Empty doc titles, test setup duplication, naming      |

## Anti-Patterns

Tool usage:

- Using `--quick` as default for PR review (drops test/lint/security signal)
- Running `--deep` on every PR when `--with-tests --with-lint` suffices
- Reading `full.patch` entirely for large PRs (use `per-file-diffs/`)
- Ignoring `report.json` / `MERGE_GATE.json` (parse structured first)
- Not using `--update` after amend/force-push (duplicate artifact sets)

Analysis:

- Stopping at 5 findings when 25 are visible (findings-max = exhaustive)
- Findings without evidence grade (STRONG / MEDIUM / WEAK / NONE mandatory)
- Findings without negative check ("old path removed" must be verified)
- Mixing separate problems into one finding (one point = one problem)
- Skipping pattern scans (`.unwrap()` / `any` / PII checklist mandatory)
- Skipping the adversarial pass (Phase 2.5 is mandatory)
- Skipping self-attack on STRONG verdicts
- Modifying code during review (READ-ONLY — fixes belong in marbles)
- Trusting PR description / commits / `// done` without code verification
- Recommending "merge" while `model_confidence` ≠ `high`
- Treating mid-stage PRs as fully-staged (use `[STAGE-OK-DEFERRED]`)
