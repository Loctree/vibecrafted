# vc-release — Semgrep Release Gate Details

## Semgrep Release Gate

Semgrep is part of the canon. Not optional. Release report must carry the evidence.

Canonical command: `make semgrep` (wired same as local pre-commit/pre-push hooks: `semgrep scan --config auto --error --quiet --exclude-rule html.security.audit.missing-integrity.missing-integrity .`). Hooks live in `scripts/hooks/`, activated through `make init-hooks`.

Before release: run `make semgrep` against full repo, record findings (rule id, severity, file, line range), classify by **dataflow boundary** (not file location):

- tainted-path / LFI sinks → fix at validated root object
- ReDoS-prone regex → bounded parsing or safe shape
- header/object merge unsafety → explicit allowlist + immutable input boundary
- command/shell construction → parameterized invocation, never string concatenation across an untrusted seam

Block release on any unresolved blocking finding unless user explicitly accepts risk in writing inside the report.

Minimum classes: auth/authz bypasses, insecure secret handling, shell/command injection, SSRF, path traversal/LFI, unsafe file serving, weak input validation on dangerous sinks, insecure deserialization/eval-like, ReDoS regexes, unsafe header/object merge, framework debug/dev endpoints left enabled.

If Semgrep unavailable, say so explicitly, run `uvx semgrep` (documented fallback), and record in the report that the gate was not satisfied. Silence is not acceptable.
