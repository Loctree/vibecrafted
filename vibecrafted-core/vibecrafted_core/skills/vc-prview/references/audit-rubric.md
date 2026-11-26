# vc-prview — Reading Order, Pattern Scans, Output Format & Anti-Patterns

## Reading Order (Obowiązkowy)

Read artifacts in this order. For each: what to extract.

### 1) `AI_INDEX.md` (if exists)

- Verify it points to real paths. Lying index → finding P3 [TOOLING].

### 2) `report.json` (default source of truth)

- `meta`: PR url, branch, base
- `gate`: allow_merge + policy_mode + reasons
- `checks[]`: status (PASS/WARN/FAIL/ERROR), log_path, command
- `diff.stats` + `diff.files[]`: scale, churn, hotspots, patch_path
- `quality`: breaking / coverage / sarif / heuristics

### 3) `00_summary/MERGE_GATE.json` + `SANITY.json`

- Cross-check with `report.json`. Inconsistency → finding P2 [TOOLING].
- Note: "All checks passed" with WARN/INLINE_FINDINGS present = misleading.

### 4) `00_summary/pr-metadata.txt` + `file-status.txt` + `commit-list.txt`

- Scope: how many files, what categories (A/M/D), commit progression
- Look for branch drift (infra files not in PR scope)

### 5) `30_context/INLINE_FINDINGS.sarif`

- Every SARIF result = ready-made finding. Transfer all to findings list.

### 6) `20_quality/*` (logs + results)

- PASS gates: extract warnings from logs (cargo warns, tsc non-errors)
- WARN/ERROR/FAIL gates: root cause + recommendation
- `checks-errors.log`: high-signal filtered errors
- `BREAKING_CHANGES.md`: assess real weight (P?)
- `coverage-delta.txt`: flag critical "NO_TEST_CHANGE" entries

### 7) `30_context/changed-tests.txt`

- Cross-reference with source changes — untested source files → finding

### 8) Diffs (selective, not exhaustive)

- `10_diff/per-file-diffs/00-INDEX.txt` → top churn files
- Per-file patches for hotspots
- `10_diff/per-commit-diffs/00-SUMMARY.md` → commits of highest impact
- Per-commit batches for line-level analysis

---

## Mandatory Pattern Scans

In per-file patches and/or `full.patch`, scan for these patterns:

### Rust

- `.unwrap()`, `.expect(` — unhandled panics
- `panic!`, `todo!` — incomplete code
- `unsafe` — review justification
- `dbg!`, `println!` — debug leftovers
- `#[allow(` — suppressed warnings

### TypeScript / JavaScript

- `any` — type escape
- `as unknown as` — double cast (type laundering)
- `@ts-ignore`, `@ts-expect-error` — type suppression
- `eslint-disable` — lint suppression
- `// TODO`, `// FIXME`, `// HACK` — deferred work
- Empty `catch {}` or `catch (e) {}` without log/rethrow
- Non-null assertion `!` on uncertain values
- `console.log`, `console.warn`, `console.error` — should use secureLogger (example-app)

### Security / PII

- Logging of tokens, emails, passwords, personal IDs
- New telemetry events without privacy review
- New endpoints / command handlers without auth checks
- Hardcoded URLs, API keys, secrets

### Data / Performance

- Query in loop (N+1)
- Missing batching for bulk operations
- Large payloads without pagination
- Unnecessary I/O in hot paths

Each "hit" in the diff = potential finding with evidence.

---

## Minimum Coverage Requirements

To prevent laconic reports:

- **All** entries in `INLINE_FINDINGS.sarif`
- **Top 10** files by churn (from `report.json` or `file-status.txt`) — read per-file patch
- **All** files in core risk categories (by path): auth, payments, database, session, security, encryption, middleware
- **All** critical "NO_TEST_CHANGE" entries from `coverage-delta.txt`
- **All** entries in `BREAKING_CHANGES.md` with assessed P-level
- **Per-commit progression** for PRs with >5 commits — identify phases, risky transitions

---

## Special Cases (Tooling)

### Cargo Geiger panic

`Matching variant not found` = tooling/misconfig (case-sensitive `--output-format`).
→ Finding **P1 [TOOLING]** if it blocks quality signal. Recommend: fix flag or pin/upgrade.

### Timeouts / "killed"

`killed (>timeout)` for tsc trace / eslint json:
→ Finding **P2 [TOOLING]** (missing quality signal). Recommend: increase timeout or disable with justification.

### Gate inconsistencies

`MERGE_GATE.json` says "All checks passed" but WARN/findings exist:
→ Finding **P2 [TOOLING]** with recommendation: "All blocking checks passed" vs "Non-blocking issues present".

### Branch drift

Files changed outside PR scope (CI, infra, unrelated config):
→ Finding **P1** if >10 files. Recommend: rebase on base branch.

---

## Output Format (Obowiązkowy)

Final output ALWAYS has these 2 mandatory sections (in this order):

### 1) Findings (P0/P1/P2/P3)

Each finding in this format:

```
- **[P?] <Title>** (optionally: [VERIFY] or [TOOLING])
  - **Evidence:** `<artifact-path>` + `<file:line>` + short fragment (1-2 lines)
  - **Comment:** 1 sentence on risk/impact
  - **Recommendation:** concrete "what to do" / "how to verify"
  - **Owner:** `author` / `reviewer` / `infra` (optional)
```

Number findings for cross-referencing: P1-01, P1-02, P2-01, etc.

### 2) Before-Merge TODO (Markdown Checkboxes)

```markdown
- [ ] **(P0)** ... (ref: P0-01)
- [ ] **(P1)** ... (ref: P1-01, P1-02)
- [ ] **(P2)** ... (ref: P2-01)
- [ ] **(P3)** ... (ref: P3-01)
```

Each TODO references finding IDs. Include verification commands in code fences where applicable.

### 3) Optional Sections (recommended)

Add when they provide value:

- **Executive Summary** (max 8 bullets): gate verdict, top 3 risks, test signal, top hotspots, scope delta
- **Architecture Context**: diagram or description of affected subsystem
- **Scope / What Changed**: based on `diff.stats` + top directories + top files
- **Commit Progression**: phases of work for multi-commit PRs
- **Test Coverage Matrix**: source file → test file → new tests count
- **Security & Privacy Check**: PII in logs, data flows, event filtering
- **QA Plan**: 5-15 manual + automated test recommendations
- **Evidence Index**: links to key artifacts used

---

## Anti-Patterns

### Tool usage

- Using `--quick` as the default for PR review in this skill (it drops test/lint/security signal)
- Running `--deep` on every PR when `--with-tests --with-lint` is enough (save `--deep` for merge gate / high-risk PRs)
- Reading `full.patch` entirely for large PRs (use `per-file-diffs/` for focused review)
- Ignoring `report.json` and `MERGE_GATE.json` (parse structured data first)
- Not using `--update` after amend/force-push (generates duplicate artifact sets)
- Running without `--no-fetch` on slow networks

### Analysis

- Stopping at 5 findings when 25 are visible (findings-max means exhaustive)
- Findings without evidence (every point needs artifact path + code fragment)
- Mixing separate problems into one finding (one point = one problem)
- Ignoring tooling issues (tool crash ≠ code issue, but still a finding)
- Skipping pattern scans (the `.unwrap()` / `any` / PII checklist is mandatory)
- Not cross-referencing coverage-delta with changed source files
