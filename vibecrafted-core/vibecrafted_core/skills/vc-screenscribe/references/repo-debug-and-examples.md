# vc-screenscribe — Repo / Debug Path & Examples

## Repo / Debug Path

Canonical upstream repo:

- [vetcoders/Screenscribe](https://github.com/vetcoders/Screenscribe)

When repo work is needed, prefer the current Screenscribe checkout if the user
already opened one. Do not assume a fixed local path. If no checkout is open,
refer to the default repo above and only mention a local path once it is
actually known.

Drop into the repo only when:

- the CLI is missing or broken
- provider/config/runtime debugging is needed
- the user wants work on Screenscribe itself

Then prefer:

```bash
cd /path/to/Screenscribe
uv run python -m screenscribe review /absolute/path/to/video.mov
```

### Review

Single video:

```bash
cd /path/to/Screenscribe
uv run python -m screenscribe review /absolute/path/to/video.mov
```

Batch:

```bash
cd /path/to/Screenscribe
uv run python -m screenscribe review /path/video1.mov /path/video2.mov -o /absolute/output/dir
```

Useful flags:

- `--keywords-only`
- `--estimate`
- `--dry-run`
- `--no-vision`
- `--resume`
- `--lang en`
- `-o /path/output`

### Preprocess

```bash
cd /path/to/Screenscribe
uv run python -m screenscribe preprocess /absolute/path/to/video.mov
```

Useful flags:

- `--no-audio`
- `--force`
- `--lang en`
- `-o /path/output`

### Transcribe

```bash
cd /path/to/Screenscribe
uv run python -m screenscribe transcribe /absolute/path/to/video.mov -o /absolute/path/to/transcript.txt
```

### Interactive Analyze Server

Preferred:

```bash
cd /path/to/Screenscribe
make analyze VIDEO=/absolute/path/to/video.mov PORT=8766
```

### Safe Triage Commands

Only use these if the normal `screenscribe review ...` or `screenscribe preprocess ...` path failed:

```bash
screenscribe review --help
screenscribe preprocess --help
screenscribe version
ffmpeg -version
test -f ~/.config/screenscribe/config.env && echo CONFIG_OK || echo CONFIG_MISSING
```

## Examples

**Example 1**
Input: "Przeleć mi ten review.mov i wypluj JSON + markdown z bugami."
Action: run `screenscribe review /absolute/path/to/review.mov`, return output dir and key findings.

**Example 2**
Input: "Mam video, ale chcę tylko transcript, timestampy i pack dla agenta."
Action: run `screenscribe preprocess /absolute/path/to/video.mov`, return bundle dir and artifact list.

**Example 3**
Input: "W repo https://github.com/vetcoders/Screenscribe coś popsuliśmy w HTML Pro."
Action: treat this as repo work, use repo-native commands and quality gates, not a plain review run.
