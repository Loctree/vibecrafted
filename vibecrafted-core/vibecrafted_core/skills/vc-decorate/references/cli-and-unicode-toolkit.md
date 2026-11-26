# vc-decorate — CLI Surface & Unicode Toolkit Reference

## CLI Is Also an Interface

A terminal is not a dumping ground. CLI output is a UI. It deserves the same
coherence, rhythm, and intentionality as a web page. Nasty, raw, unformatted
terminal output is not "developer-friendly" — it is offensive to the operator.

Decorate applies to CLI surfaces too. If the product has a terminal interface, that interface is part of the product
surface. Decorate it. The obvious areas include:

- installer output (alignment, colors, progress signals)
- main runtime (branded, compact, informative)
- post-execution (spinners, progress bars, per step summaries)
- help/--help outputs (structured sections, colors, columns)
- doctor/health checks (clear pass/fail summaries, readable minimal logs)
- error messages (machine/human-readable separation)

If `screenscribe` is available, vc-decorate can consume a narrated UI
screencast to detect drift, awkward transitions, and coherence breaks across a
real flow — useful when static screenshots are too thin.

### Unicode Toolkit for CLI

𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. ships a Unicode database (2601 chars, 13 categories) and a
`unicode-puzzles-mcp` server. Use them for CLI decoration instead of guessing
code points or hardcoding ANSI escape sequences.

**Pipeline: plain text → unicode transform → decorate_text**

1. Write the plain text content first
2. Transform labels/titles via `rewrite_using_unicode` (choose style)
3. Wrap final layout with `decorate_text` for box art (if needed)

Never hand-pick code points by memory. Use the MCP — it returns verified,
consistent characters from the same Unicode block.

**Available styles** (`rewrite_using_unicode`):

| Style          | Look     | Best for                        |
| -------------- | -------- | ------------------------------- |
| `squared`      | 🄵🅁🄰🄼🄴    | Branding stamps, footer badges  |
| `vaporwave`    | Ｖｉｂｅ | Spaced-out headers              |
| `monospace`    | 𝚟𝚒𝚋𝚎     | CLI subheaders, version strings |
| `smallCaps`    | Vɪʙᴇ     | Inline emphasis                 |
| `fraktur`      | 𝔙𝔦𝔟𝔢     | Decorative section titles       |
| `doubleStruck` | 𝕍𝕚𝕓𝕖     | Mathematical / formal labels    |
| `bubble`       | Ⓥⓘⓑⓔ     | Status badges, tags             |

**CLI decoration elements** (Unicode DB):

| Need       | Characters          | Source                   |
| ---------- | ------------------- | ------------------------ |
| Box frames | `╭─╮│╰─╯`           | Box Drawing              |
| Separators | `·` `─` `━` `┄`     | Box Drawing, Punctuation |
| Checkmarks | `✓` `✗` `⚠`         | Dingbats                 |
| Bullets    | `▸` `▪` `◆` `›`     | Geometric Shapes         |
| Progress   | `⣿⣶⣤⣀` `█▓▒░`       | Braille, Block Elements  |
| Sparklines | `⣀⣤⣶⣿` (8px/cell)   | Braille (256 combos)     |
| Arrows     | `→` `←` `↑` `↓` `⟶` | Arrows                   |
| Status     | `⚒` `⚡` `⚙` `⟳`    | Misc Symbols             |
| Brands     | `🄵·🅁·🄰·🄼·🄴·🅆·🄾·🅁·🄺` | Enclosed Alphanumerics   |

**Braille sparklines** deserve attention. A single Braille char encodes 8 dots
in a 2×4 grid (256 combos) — 40 chars = 320-point convergence curve in the
terminal, no graphics library. Use for: token usage over time · P0/P1/P2
findings across marbles loops · agent activity timelines · any trend data.

**Rules:**

- Zero ANSI escape codes for text styling — pure unicode renders everywhere.
- ANSI colors (`\033[32m` etc.) acceptable for status coloring only.
- Never mix Unicode blocks within one label (squared F next to negative squared R
  looks like a bug, not a choice — unless deliberately a signature mark like
  `🅵·🅁·🄰·🄼·🄴·🅆·🄾·🅁·🄺`).
- Test rendering on at least two terminals (macOS Terminal + Linux default).
- Use `search_unicode` to find a specific symbol — don't guess.
