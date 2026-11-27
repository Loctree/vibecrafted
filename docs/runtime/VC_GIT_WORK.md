# vc-git: questions about work, not about commits

Git answers questions about a commit graph. `vc-git landed`, `vc-git gems` and
`vc-git save` answer the questions people ask about work:

| Question                      | Command                        |
| ----------------------------- | ------------------------------ |
| Did that work land?           | `vc-git landed ADDRESS`        |
| Where is work that did not?   | `vc-git gems [search QUERY]`   |
| Keep it safe, do not touch it | `vc-git save [ADDRESS] --to …` |

The overview (`vc-git`), the agent inventory (`vc-git worktrees list|triage`)
and the delivery comparison (`vc-git --compare … --cuts …`) are unchanged; see
[PARALLEL_WORK_COMPARISON.md](PARALLEL_WORK_COMPARISON.md).

## Work addresses

Every piece of work has one written form. Queries print addresses; measuring
and saving accept them. A single `-` reads addresses from stdin, one per line.

```text
feat-x  feat-x@1a2b3c4d5e          local branch, optionally pinned to a tip
origin/feat-x@1a2b3c4d5e           remote-tracking branch
1a2b3c4d5e6f                       any commit (also one only a reflog holds)
stash@{2}  stash@{2}@1a2b3c4d5e    stash entry; the pin survives renumbering
saved:NAME@1a2b3c4d5e              copy kept by vc-git save --to commit
wt:/path/to/checkout  wt:.         a checkout, including uncommitted files
patch:/path/to/file.patch          a unified diff on disk
run:RUN_ID                         a Vibecrafted run: its checkout, else its branch
pr:412                             a GitHub pull request head (read through gh)
```

Addresses printed by a query are pinned. If the branch moves before you act,
the pinned tip is used and the move is reported.

## One grammar

```text
vc-git <family> [action] [ADDRESS | QUERY …] [flags]
```

Scope flags mean the same thing everywhere: `--repo PATH`, `--target REF`
(what "landed" is measured against; default the remote's default branch),
`--base REF` (measure the work from here), `--remote`, `--since`, `--until`
(`2026-11-01` or `3d`), `--author`, `--agent`, `--path GLOB`, `--limit N`.

Output: sentences by default, `--json` (versioned schema
`vibecrafted.vc-git.<family>.v1`), `--addresses` (bare, for pipes), `--why`
(the evidence behind every answer, each claim labelled by its source: `git`,
`git-reflog`, `git-trailer`, `github`, `control-plane`, `harbor`).

Exit status: `0` yes/done, `1` no or partly, `2` usage or runtime error,
`3` cannot be established. A batch exits `1` if any answer is no, else `3` if
any cannot be established. "Cannot be established" is never folded into yes or
no — not in text, not in JSON, not in the exit status.

```bash
vc-git gems search "resume routing" --addresses \
  | vc-git landed - --target develop --addresses \
  | vc-git save - --to patch
```

## landed: how the answer is measured

From the cheapest strong evidence to the most detailed; the first rung that
settles the question answers it:

1. **Ancestry (revert-checked)** — the tip is in the target's history and its
   changed files were not reverted back to their pre-image in the target.
2. **Exact tree** — some target commit has exactly the tip's tree (a squash of
   an up-to-date branch).
3. **Patch identity** — every commit has an identical patch in the target
   (cherry-picks), or the whole change is one target commit (a squash).
4. **Per file**, against an index built from the target tree in a temporary
   file:
   - `identical` — the target holds exactly the content the work produces;
   - `present` — the target held exactly this content at some commit and has
     evolved it forward since (without reverting back to the pre-image), or the
     reverse patch applies while the forward patch does not;
   - `absent` — the forward patch applies, or the target has no such file
     (identical content at a different path is noted as evidence, never counted
     as landed);
   - `unknown` — both directions apply, or neither (the file diverged). A
     line-containment hint (`likely present/absent/mixed`) explains a diverged
     file but never settles it.

The work is measured from an explicit base, reported with every answer: the
`--base` you give, the commit a stash was made on, a run receipt's recorded
baseline, the boundary where no ref holds the history any more (for
reflog-only commits), the branch creation point recorded in its reflog, or the
integration line it most recently left (the target, the primary checkout's
branch, conventional trunk names).

Declared traces such as `(cherry picked from commit …)` are reported as
`git-trailer` evidence; measured content decides the answer.

## gems: where unlanded work hides

Searches local and remote branches, stash entries, checkouts with uncommitted
files or detached commits, and commits only a reflog holds. A gem is work
whose content is not in the target — a squash-merged branch is not a gem even
though Git calls it unmerged. Not listed separately, with the count reported:

- branches whose tip another branch or an integration line already carries;
- reflog-only commits that are earlier versions of rewritten commits (the same
  author and author date exist on a branch: amend, rebase);
- reflog-only merges whose parents all survive in refs (Git can redo them).

Ranking puts work that exists in only one copy first: reflog-only, then
uncommitted files and stash entries, then unpushed branches, then work with a
remote copy. A copy kept by `vc-git save` (a saved ref or a harbor patch with
the same patch identity) counts as a second copy.

## save: keep it without touching it

`--to patch` (default) writes a binary-safe patch with a SHA-256 manifest to
`$VIBECRAFTED_HOME/harbor/<repo>/<date>/` — it survives deleting the branch,
the checkout or the repository. `--to git-apply` adds a check that the patch
applies cleanly onto `--target` now. `--to commit` creates a create-only ref
under `refs/vc-git/saved/` (pushable, invisible to `git branch`). `--to stash`
stores a regular stash entry with staged, unstaged and untracked parts.

The source is never modified: a checkout is snapshotted through a temporary
index, so its files, its real index, HEAD and its branch stay as they were.
Ignored files and files marked assume-unchanged / skip-worktree are reported
as not included. Every save is appended to `harbor/<repo>/ledger.jsonl` and
`--why` prints how to remove the copy. `--dry-run` writes nothing.

## Read operations stay read-only

`landed` and `gems` write no refs, no objects and no index. Working-tree
comparisons use `git diff-index` because porcelain `git diff` refreshes and
rewrites the index on stat-only changes even with `GIT_OPTIONAL_LOCKS=0`; the
overview's `git status` probes run with optional locks off for the same
reason. Host settings that change parsed output (`diff.mnemonicPrefix`,
`diff.noprefix`, `color.ui`, `core.quotePath`, `log.showSignature`) are pinned
off for every call.

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
