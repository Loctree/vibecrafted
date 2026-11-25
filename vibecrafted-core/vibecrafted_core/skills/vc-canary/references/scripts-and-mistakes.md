# `vc-canary` — Utility Scripts, Dependencies & Common Mistakes

## Utility scripts

```bash
CLI="uv run --python 3.12 …/vc-canary/scripts/canary_cli.py"

$CLI snapshot-path --root .
$CLI repo-view --root .
$CLI atlas --root . --refresh
$CLI coverage --root .
```

All writes go under `./.loctree/` (atlas + canary). Status on stdout; data
in files.

## Dependencies

| Skill / tool                | Why                                  |
| --------------------------- | ------------------------------------ |
| `loct` / loctree            | snapshot, organs, prism, occurrences |
| `vc-loctree`                | structural doctrine                  |
| `vc-dispatch` await-arming  | fleet wake, not log files            |
| `vc-delegate` / `vc-agents` | hybrid native vs external            |

## Common mistakes

- Treating every multi-authority as a defect (an `INTENTIONAL_VARIANT`
  with a proven boundary is a healthy answer)
- Proposing refactors or thrones inside the canary run
- Claiming absence from semantic search without literal coverage
- Producing a report on a stale snapshot or ignoring dirty/worktree state
- Overwriting the journal instead of appending
- Using `loct-context-full.json` as the file inventory
- Fixed agent count instead of axes from Phase I
- Counting definitions instead of references (a definition census once hid
  141 call sites)
- Reconstructing or interpolating missing historical checkpoints instead
  of recording `MISSING`
- Dispatching the retired docstring-WRITE cataloger brief — canary mutates
  no code (contract retired 2026-08-24)
