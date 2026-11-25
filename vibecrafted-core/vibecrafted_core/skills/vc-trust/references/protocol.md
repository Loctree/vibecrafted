# vc-trust — Falsification Protocol & Evidence Grading Rubric

## Protocol

### 1. Orient and bound the stream

Run the `vc-init` gate. Read the complete Loctree atlas and AICX intent history.
Capture branch, HEAD, dirty state, and the exact commit range. On a Living Tree,
never attribute a dirty file or concurrent commit from timing alone.

List unjudged candidates:

```bash
python -m vibecrafted_core.trust enumerate <author> --since <sha-or-ISO-time>
```

### 2. Turn prose into falsifiable claims

For each commit, extract every material claim from its subject/body and changed
surface. Rewrite vague prose into checks such as:

- named test or gate exists and fails when the behavior is broken;
- runtime path reaches the changed code;
- claimed fail-closed behavior has no bypass or silencer;
- docs and launcher surface describe the behavior that actually ships;
- diff scope matches the message and contains no unclaimed foreign files.

Absence of a claim in the message does not hide a material regression in the
diff.

### 3. Grade evidence per claim

- `strong` — direct runtime reproduction, adversarial test, exact artifact
  inspection, or an independently failing-then-passing gate.
- `medium` — focused unit/integration test plus structural consumer proof.
- `weak` — static prose, inferred intent, happy-path-only evidence, or an
  upstream report not re-run by the judge.

A `pass` requires every material claim to have sufficient direct evidence.
Weak evidence can support context, never a material pass by itself.

### 4. Falsify, do not replay ceremony

Use Loctree `slice` for changed files, `impact` for high-blast-radius changes,
literal find/body for exact claims, and `follow` for relevant dead/cycle/twin
signals. Read the commit diff and its parents. Run the nearest tests and the
real user path. Check that the verification command itself can fail.

`vc-review` and `vc-audit` remain different:

- `vc-review` judges bounded diff/PR quality.
- `vc-audit` falsifies a completed plan or multi-task implementation.
- `vc-trust` judges a commit stream on the live shared tree and records a
  durable per-commit verdict.

### 5. Record exactly one explicit verdict

Each `--claim` must have one matching `--grade` and `--evidence`:

```bash
python -m vibecrafted_core.trust note <sha> pass \
  --claim "the blocking lane rejects insecure code" \
  --grade strong \
  --evidence "negative fixture failed before the fix and passed after it"
```

When judging the commit(s) produced by a run, add `--run-id <id>`. Only this
explicit `note` writes the canonical settlement. Exit code, report presence,
or await completion never imply a trust pass.

The journal defaults to
`$VIBECRAFTED_HOME/trust/journal.jsonl` and uses
`vibecrafted.trust-journal.v1`. Override it with
`VIBECRAFTED_TRUST_JOURNAL` or `--journal`.

### 6. Await at the run boundary

The primary lifecycle mode is named `await-primary`, not `guard=await`:

```bash
python -m vibecrafted_core.trust await-primary <run-id> \
  --author <agent-author> \
  --since <baseline-sha>
```

It waits synchronously through the canonical control plane, then lists
unjudged candidate commits. It does not auto-pass, auto-note, poll in the
background, or act as a persistent monitor. Persistent monitoring is only an
interactive convenience and is not a durable wake mechanism.

### 7. Roll up

```bash
python -m vibecrafted_core.trust triage [--run-id <id>]
```

Triage uses the latest append-only record per repo+commit and reports canonical
`f/x/n` counts. It does not recompute settlement from Git or exit codes.
