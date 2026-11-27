# vc-guard — Gate Inventory & Fairness / f-x-n Completeness

## Gate inventory (named, not reimplemented)

| Gate                       | Phase    | Mode                                          |
| -------------------------- | -------- | --------------------------------------------- |
| `commit-msg`               | commit   | hard — format + trailers + ban vendor footers |
| `prepare-commit-msg`       | commit   | helper — fill trailers                        |
| `pre-commit`               | commit   | hard — ruff/prettier/semgrep family           |
| `pre-push`                 | push     | hard — push-time gates                        |
| `loctree-first`            | agent    | policy — map before rummage                   |
| `classifier-hard-stops`    | dispatch | policy — AUTONOMY buttons                     |
| `commit-msg-diff-advisory` | commit   | advisory seed — claim vs staged pack          |
| `trust-block-dispatch`     | dispatch | hard — this skill's proof path                |

Coverage gaps (honest): fleet-wide hook seeding, elevating diff-gate to hard,
PATH/install drift, per-branch line policy beyond HEAD default.

## Relation to agent fairness and f/x/n completeness

- **Living Tree** allows parallel commits; fairness claims must still hold.
- **commit-msg** makes the message machine-legal.
- **vc-trust** falsifies whether the legal message is true (fairness +
  completeness + runtime claims) and writes settlement.
- **vc-guard** stops the fleet from continuing on a line trust has blocked.
