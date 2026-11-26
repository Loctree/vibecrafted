# vc-aicx — Output Structure & Transcript Extract Recovery

## The output structure:

```
[1-100/100 <score_range>] <org>/<repo> | <agent> | <date>
session(s): <session_id>
cwd: <cwd>
search result:
  > <result>
  > - <file_path>
  > [HH:MM:SS] assistant: <result>
  > [HH:MM:SS] user: <result>
source file(s):
$HOME/.aicx/store/<org>/<repo>/<date>/<type>/<agent>/<session_id>.md
```

## The extract tool use when you cannot read an agent's result directly:

- Output too large for Read tool (>10k tokens)
- Tool-results file is raw JSONL, not human-readable
- Subagent crashed but left a partial log
- Previous session context needed before starting work

1.  The Command

```bash
aicx extract --format {claude,codex,gemini,ollama} <INPUT_FILE> -o /tmp/aicx-extract-<basename>.md
```

`--format claude` parses Claude Code JSONL as well as Gemini json structure.
File extension does not matter — `.jsonl`, `.txt`, `.output` all
work the same.

**Output path**: Derive from input filename. Use the input file's basename (without extension) as the output name:
`/tmp/aicx-extract-<basename>.md`. Never ask the user for an output path.

## Where To Find Input Files

```
$HOME/.claude/projects/<project>/<session-id>/tool-results/<hash>.txt     # Agent result (most common)
$HOME/.claude/projects/<project>/<session-id>/subagents/agent-<id>.jsonl  # Subagent session
/private/tmp/claude-<uid>/<project>/tasks/<task-id>.output               # Background task
$HOME/.claude/projects/<project>/<uuid>.jsonl                             # Full session
```

## Useful Flags

| Flag                       | Effect                             |
| -------------------------- | ---------------------------------- |
| `--conversation`           | User/assistant only, no tool noise |
| `--max-message-chars 8000` | Truncate long messages             |
| `--user-only`              | Only user messages                 |

## Example Recovery Flow

```bash
# 1. Extract (output path derived automatically from input basename)
aicx extract --format claude \
  $HOME/.claude/projects/-Users-foo-myrepo/abc123/tool-results/xy9z.txt \
  -o /tmp/aicx-extract-xy9z.md

# 2. Read the result
Read /tmp/aicx-extract-xy9z.md
```
