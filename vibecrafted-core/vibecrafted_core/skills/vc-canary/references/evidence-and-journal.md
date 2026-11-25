# `vc-canary` — Evidence Schema, Run Verdict & Journal Contract

## Evidence schema (per finding)

Axis · competitors (`file:line`, LOC) · symbols at war · pair verdict ·
legend mark · classification · proof (loct outputs cited by organ) ·
absence-falsification receipt (the literal coverage line). A finding
missing any element is a candidate, not a finding.

## Run verdict & honest exit

Every run returns exactly one verdict:

| Verdict                      | Condition                                                                                                                                            |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AXES_CLOSED_CANDIDATE`      | zero `UNRESOLVED` rows; every retained executable edge resolves to one authority; zero bypasses; complete untruncated evidence under one fingerprint |
| `AXES_OPEN`                  | anything less — say so plainly                                                                                                                       |
| `INSTRUMENT_INCOMPLETE`      | Loctree could not cover the required questions (fail-log appended)                                                                                   |
| `LAUNCHER_CONTRACT_CONFLICT` | inherited instructions demanded mutation or commits — stop, keep N=1, report                                                                         |

Missing historical checkpoints stay `MISSING` — never reconstructed or
interpolated. The report ends with the honest state line
`BUILD/LINT/TEST/RUNTIME=NOT_ASSESSED`: canary is a mutation-free radar
and green gates are outside its jurisdiction.

## Journal contract

Append-only `./.loctree/canary/JOURNAL.md` in the target repo. Each run
appends: HEAD SHA, Phase 0 receipts, axes examined, findings with evidence,
prism scores. Runs never overwrite history — the journal shows what the
radar saw _at that SHA_, even when a later run knows better.
