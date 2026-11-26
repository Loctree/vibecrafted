# vc-prune — Wave 5: The Silencer Strip & Anti-Patterns

## Wave 5 — The Silencer Strip (Strip and Listen)

### Inventory

```bash
# Rust
rg -n '#\[allow\(' src-tauri/src
rg -n 'nosemgrep' .

# TypeScript / JavaScript
rg -n 'eslint-disable' src
rg -n '@ts-(ignore|nocheck|expect-error)' src
rg -n 'biome-ignore' src

# Python
rg -n '# noqa' .
rg -n '# type: ignore' .
rg -n '# pylint: disable' .
rg -n '@pytest\.mark\.skip' .

# Go
rg -n '//nolint' .
rg -n 'testing\.Short\(\) \|\| t\.Skip' .

# Test theater across languages
rg -n 'panic!\("Test requires|throw new Error\("requires' .
rg -n 'it\.skip|test\.skip|describe\.skip' .
```

Capture **counts per category**. That's your before-baseline.

### Strip ALL of them in one pass

Bulk-delete the lines. Do not pre-curate "obvious keepers" — the bias that put them there is the same bias that would
protect them. Let the toolchain decide.

### Run gates

Whatever the repo already has — do not invent new ones:

```bash
cargo clippy --all -- -D warnings && cargo test --all
pnpm lint:tsc && pnpm code:all && pnpm vitest run
ruff check . && mypy . && pytest          # Python
golangci-lint run && go test ./...        # Go
semgrep --config=auto .                   # if available
pre-commit run --all-files                # if installed
```

### Triage with care

| Finding                         | Resolution                                                                                                                                                             |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Authentic code smell            | **Fix root cause.** Refactor, write proper types, add adapter, drop lock before await.                                                                                 |
| False positive                  | **Refactor stylistically** so the warning never fires. No re-add.                                                                                                      |
| Genuine technical constraint    | **Re-add silencer with incident-grade comment**: WHY (technical reason), WHEN (under what conditions), WHERE (specific code path). Not "intentional", not "by design". |
| **Forgotten gem (gentle path)** | **Do not delete. Report.** A `dead_code` warning on a 200-line module with thoughtful structure is parked work. Add to **Forgotten Gems Report**. Operator decides.    |
| Test theater unmasked           | **Stop. Bigger than the silencer.** A panic-or-skip pattern that always evaluates one way means the test was never real. Open a separate plan for real wiring.         |
| Truly dead code revealed        | The silencer was hiding `dead_code` on a one-liner stub or scratch file. Delete — but only after a fast forgotten-gem check.                                           |

The rule: **a silencer earns its keep only with a written technical reason that another engineer six months from now
would accept as serious.** Vague "intentional" comments are not serious. Equally: **delete code only when it is
unambiguously trash** — anything in between goes to the Forgotten Gems Report.

### Forgotten Gems Report

Output of Wave 5 is **not** a smaller repo — it's a written report. Save to
`$VIBECRAFTED_HOME/artifacts/<org>/<repo>/<YYYY_MMDD>/reports/<timestamp>_forgotten-gems.md`.

> See [references/case-studies.md](case-studies.md) for the full Forgotten Gems Report template, the
> test-theater report template, and concrete real/hypothetical case studies (example-app 0.67.3 silencer-strip, sample-portal
> billing-service equivalent, surprise-findings catalog).

Test theater is debt, not gem. It always gets a follow-up plan saved to `<timestamp>_test-theater.md`. Never a silencer
reinstatement.

### Acceptance for the wave

- Remaining silencer count is a **small fraction** of the inventory (target ≤25%, often ≤10%).
- Every remaining silencer carries an incident-grade comment.
- Every gate runs green without `--no-verify`, `cargo clippy --allow-dirty`, `pnpm lint --fix --quiet`, or any other "
  make it green by hiding it" trick.

### Surprise findings are the prize

Watch for: tests that always skip / always panic, `dead_code` allow on functions whose only caller was deleted three
releases ago, `@ts-ignore` on types correct for a year, `eslint-disable jsx-a11y/...` on real a11y violations,
`nosemgrep: react-dangerouslysetinnerhtml` on HTML that is **not** sanitized, `# type: ignore[arg-type]` on a function
whose signature was fixed two refactors ago. Each is a real bug or a real lie the silencer was hiding.

## Anti-Patterns

- Deleting ten dead symbols while a whole abandoned subsystem still stands.
- Trusting "unused" reports without checking dynamic loading via framework router.
- Preserving a chaotic 2000-line file because "we might need it" — that's what Git history is for.
- Cleaning code but leaving stale dependencies in the lockfile.
- Stripping silencers selectively. The whole point of Wave 5 is to bypass that bias.
- Mass-restoring silencers because there were "too many warnings". That's burying the message again.
- Adding new silencers to silence newly-uncovered warnings. Fix the warning or refactor it away.
- Treating `panic!("Test requires X")` as a real gate, or `it.skip` / `@pytest.mark.skipif` as harmless. Tests that
  always skip do not exist; they cost reviewer attention.
- Auto-deleting code that a `dead_code` allow was hiding without a forgotten-gem check first.
- Treating Wave 5 as adversarial. Past engineers added silencers for plausible reasons. Wave 5 is the reread, not a
  verdict.

## The Pruning Principle

Do not ask the repo to explain every scar. Ask it to justify every surviving surface.

If a surface does not run in production, build the release, or test integrity — the move is **not** automatically
delete. The move is **decide with intent**: revive, archive, or delete. The skill exists to surface decisions, not make
them on autopilot.

**The toolchain is not an enemy to be muted. It is a witness to be interrogated.** Strip the silence. Run the gates.
Listen. Then decide — case by case, with a written reason — what genuinely deserves to stay quiet, what needs a real
fix, and what was a forgotten gem hiding behind the silencer all along.

A repo that has been through `vc-prune` is not necessarily smaller. It is **legible**. Every surviving surface, every
surviving silencer, every surviving test has a written reason to be there. That is the win.
