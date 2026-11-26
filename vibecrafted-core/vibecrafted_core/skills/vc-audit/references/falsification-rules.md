# vc-audit — Falsification Rules & Evidence Taxonomy

## Default Stance: Falsification

Default verdict for every requirement is **UNVERIFIED**. A requirement
earns PASS only with all four:

1. **Task evidence** — quoted acceptance criterion or non-goal
2. **Code evidence** — file path, function/type/test name, line range
3. **Test evidence** — test name + run output, or justified test-gap
4. **Negative check** — old/forbidden behavior not still present

### Hard Non-Trust Rules

You MUST NOT trust task frontmatter status, prior agent reports,
commit messages, AICX entries, memory slices, chronicle notes,
"completed" annotations, PR descriptions, inline `// done` comments,
or prior `vc-followup` / `vc-review` reports — unless **independently
confirmed in current code/tests**. Each of those is a _claim_, not
evidence. Audit converts claims into evidence by checking code.

### Evidence Taxonomy

| Grade  | Criteria                                        |
| ------ | ----------------------------------------------- |
| STRONG | Code + targeted test + negative check OK        |
| MEDIUM | Code + weak/general test + negative check OK    |
| WEAK   | Code only, no test or no negative check         |
| NONE   | No direct evidence — verdict must be UNVERIFIED |

**PASS requires STRONG or MEDIUM on all core requirements.**
