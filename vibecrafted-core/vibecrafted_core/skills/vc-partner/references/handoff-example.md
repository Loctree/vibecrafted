# `vc-partner` — Hand-off & Return Command Example

### “Hand it off and come right back” example

“Hand it off and come right back” means delegate the prepared task immediately.
The synchronous action lasts only long enough to launch the worker, capture its
receipt and arm completion delivery. Then return attention to the conversation
while the worker executes; retain responsibility for receiving and closing out
the result. For an agreed Codex / `gpt-6-sol` task in an isolated worktree, run:

```bash
PROMPT="${VIBECRAFTED_HOME:-$HOME/.vibecrafted}/artifacts/<org>/<repo>/$(date +%Y_%m%d)/plans/<plan_file>.md"
vc-workflow codex \
  --model gpt-6-sol \
  --repo "$(pwd)" \
  --worktree true \
  --file "$PROMPT" \
  --json
```

Replace the placeholders with the actual saved brief path and preserve the
agreed provider, model and runtime. Assign `PROMPT` before the launch command:
an assignment on that command does not supply its own `$PROMPT` expansion.
`--file` loads the brief; `--prompt` takes inline text. Retain the returned run
receipt and arm completion delivery before returning to shared thinking.
