# Compare parallel work before deploy

## Read-only worktree inventory and triage

```sh
vc-git worktrees
vc-git worktrees list /path/to/repository --target main
vc-git worktrees triage /path/to/repository --target main --json
```

With no action, `worktrees` lists the current repository. `list` and `triage`
expose the same read-only inventory, also available through
MCP `vc_worktrees(project=".", target=None)`. With no target they compare to
the invoking checkout's HEAD. An explicit target must name a local branch.
Rows include full source and target SHAs, ahead/behind counts, canonical
runtime/dispatch owners, baseline and report paths, tracked/untracked/ignored
payload, process observations, integration evidence and protection reasons.

Only genuine Git ancestry is reported as `exact_ancestor`. Replacement refs
and grafts cannot fabricate that evidence. Repository-local Git environment
overrides are refused instead of redirecting inspection. Cherry-picks and
squashes without exact ancestry remain `review_reception`; this is an invitation
to inspect their code, not proof that work is absent from the destination.

The conservative triage marks live or restarted runs as `working`, dirty or
hidden tracked work as `recoverable_work`, ignored payload as `ignored_payload`,
and missing or inconsistent ownership/identity as `unknown`. An exact ancestor
can be `integrated` with protection reasons, or `removable` when the observed
predicates have no blocker. `removable` is an inspection result, never permission
to remove the checkout. Primary/current/default/integrator/recovery checkouts,
active parent workspaces, durable reports/artifacts, ambiguous history and
observed open-file/process holders remain protected.

`list` and `triage` only inspect, and `removable` there is an inspection result
for agents, never permission to remove a checkout. Merge preparation, merge
execution and apply endpoints stay unavailable; the MCP surface is read-only.

## Clean up as the person at the terminal

Two separate commands do the housekeeping. Neither does the other's job.

```text
vc-git worktrees cleanup [PROJECT] [--dry-run] [--yes] [--with-ignored]
vc-git branches cleanup  [PROJECT] [--target REF] [--also-remote] [--dry-run] [--yes]
```

`worktrees cleanup` (alias `prune`) removes worktree directories and drops Git
registrations of directories that are already gone. Branches and commits always
stay. It sorts every worktree by what removal would cost: worktrees with
uncommitted files or a detached HEAD holding unmerged commits are kept; clean
worktrees are removed; clean worktrees that hold ignored local files beyond
build output are removed only with `--with-ignored`. Git's own refusal of an
unclean checkout remains a second guard, because `--force` is never passed.

`branches cleanup` removes branch names whose tip is an ancestor of the target
(default: the current HEAD), so no commit is lost. Trunks, `release/`,
`recovery/` and `archive/` branches, the target and every branch checked out in
a worktree are kept. `--also-remote` refreshes the remote and deletes the merged
branches there too. Squash-merged branches are listed as kept.

Both commands show the full listing, then ask. Without a terminal they remove
nothing unless `--yes` is given.

## Compare deliveries

Let independent workers finish their cuts, then review their delivered work
before deciding what to integrate and deploy:

```sh
vc-git /path/to/repository --compare DISPATCH_RUN_ID --cuts LEFT_CUT RIGHT_CUT
vc-git /path/to/repository --compare DISPATCH_RUN_ID --cuts LEFT_CUT RIGHT_CUT --json > comparison.json
```

Use the dispatch run ID and cut IDs from your dispatch plan and receipts. The
command reads the existing control-plane dispatch ledger under
`$VIBECRAFTED_HOME/control_plane/dispatches/DISPATCH_RUN_ID/receipts.json`.
Both selected cuts must be `settled` with `acceptance: verified`. Active,
queued, reported, failed, and stopped cuts are refused with exit code 2 before
either worker's changes are compared. A canonical provider runtime record, when
present, must also say `completed` with exit code 0.

The comparison uses each receipt's full baseline and delivered commit SHA. It
shows each worker's patch, shared files, report paths, and the difference between
the delivered trees. Later branch movement or uncommitted edits do not enter the
comparison. A changed receipt during comparison causes a refusal and retry.
The invoking repository must share the dispatch repository's Git storage.

Review both reports and patches, resolve disagreements, and choose the work to
integrate. Shared files are a review signal; they do not prove merge conflicts.
Different baselines remain visible, so a difference between tips may also contain
baseline differences. Retain the JSON output if the decision needs a durable
receipt. Repeat for additional pairs when a wave has more than two deliveries.

This command performs a review step. It does not merge, deploy, or grant release
approval, and does not intercept unrelated deployment tools. Integration and
deployment remain Founder decisions. The dispatch ledger attests worker delivery;
the comparison does not certify installed runtime or product acceptance.
