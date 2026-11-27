# vc-audit — Output Contract, Anti-Patterns & Acceptance Criteria

## Output Contract

`vc-audit` produces exactly three files in the report directory:

1. **`audit_report.md`** — executive verdict first, per-task table,
   self-attack pass, model check
2. **`audit_requirements_matrix.jsonl`** — one JSON record per
   requirement: verdict, evidence grade, code locations, test
   evidence, negative check result
3. **`audit_trace.log`** — compact per-phase trace (`BEGIN`,
   `READ_CONTEXT_PACK`, `READ_TASK`, `EXTRACT_REQUIREMENTS`,
   `INSPECT_CODE`, `VERIFY_TESTS`, `NEGATIVE_CHECK`, `DEPENDENCY_CHECK`,
   `STAGE_CHECK`, `CLASSIFY`, `SELF_ATTACK`, `WRITE_REPORT`, `END`)

Executive verdict MUST include task counts per verdict, P0/P1/P2/P3
counts, top 5 risks, next five actions, and `model_confidence: high |
medium | low`.

Operator dispatch template lives in [`DISPATCH.md`](DISPATCH.md).

## Anti-Patterns

Do not in audit mode:

- fix code during audit ("just a small refactor while I'm here")
- mark PASS based on commit messages, frontmatter, or prior reports
- collapse all tasks into a general summary
- skip the negative check ("new code is there, that's enough")
- skip the adversarial pass or self-attack
- treat Stage 1 landed as full-plan PASS
- treat Stage 2 deferred as full-plan FAIL
- produce only the report without a matrix + trace
- trust AICX / chronicle / memory slices as repo truth
- bypass Loctree on importer-graph / blast-radius / dead-code questions
- protect your first verdict during self-attack instead of downgrading

## Acceptance Criteria

The audit run is **done** when:

- [ ] Every task / plan file has `task_read_status: FULL_READ`
- [ ] Every requirement has evidence grade + verdict
- [ ] Every requirement has positive + negative check results
- [ ] Self-attack executed on every PASS / PASS_WITH_GAPS
- [ ] Model check emitted with confidence rating
- [ ] All three output files written
- [ ] `git diff` empty for non-report paths (no code touched)
- [ ] Executive verdict references concrete next move
