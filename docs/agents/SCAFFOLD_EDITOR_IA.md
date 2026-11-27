> Moved verbatim from the repository `AGENTS.md` on 2026-11-27 so the agent entry file
> stays within its byte budget. `AGENTS.md` keeps a one-paragraph pointer.

## Scaffold editor IA (LAW — no 30m scroll)

The `/scaffold/editor` surface is a **single-document studio**, not a
stacked dump of every artifact. Reference shape:
`unicode-puzzles-portal` / GlyphPulse (`app-shell`: fixed chrome, one canvas).

Required layout for any scaffold review UI work:

| Region     | Role                                             |
| ---------- | ------------------------------------------------ |
| **Left**   | Artifact nav (tabs) — keep as the plan index     |
| **Center** | One active document only (topbar + canvas)       |
| **Right**  | Inspector: status, checkpoint, tools/endpoints   |
| **Bottom** | Stats bar (mode, chars/lines, checkpoint counts) |

Rules:

- **One `.artifact-panel.is-active` at a time.** Hash + left tabs switch;
  never render every panel in a scrollable column.
- **Edit/Save** is a pill on the same plane as `needs-checkpoint` /
  `checkpointed` (shared radius/border/padding) — not a ghost text link.
- Default view is **rich** markdown; Edit opens mono source; Save returns
  to rich (and posts if dirty).
- Briefs and ownership cuts that touch this surface **must** preserve the
  studio shell. "List every file full-height down the page" is a doctrine
  violation, same class as overlay replacement in Codescribe.

Implementation lives in `vibecrafted-server/web/src/scaffold/mod.rs`
(`review-shell`, `panel_nav_script`, `editor_ships_single_document_studio_shell`).

𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI
