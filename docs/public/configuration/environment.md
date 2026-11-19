---
title: "Environment variables"
description: "Stable environment variables you can set, and the worker-injected variables you should read but never set yourself."
section: configuration
order: 20
---

# Environment variables

Vibecrafted reads a small set of stable environment variables. They split into three groups: variables you set to relocate or configure the install, variables that steer provenance discovery, and variables the runtime injects into worker sessions — informational, never set by hand.

## Install and location

| Variable                     | Default              | Effect                                                                                    |
| ---------------------------- | -------------------- | ----------------------------------------------------------------------------------------- |
| `VIBECRAFTED_HOME`           | `$HOME/.vibecrafted` | State root for artifacts, logs, backups, and control-plane state                          |
| `XDG_DATA_HOME`              | `$HOME/.local/share` | Parent of the installed runtime root (`…/vibecrafted/tools/`)                             |
| `XDG_CONFIG_HOME`            | `$HOME/.config`      | Parent of `vibecrafted/`, the one product config home                                     |
| `VIBECRAFTED_RUNTIME`        | `none`               | Runtime horse to stage at install time (`wezterm`, `vc-apprt`, `locterm`, `microsandbox`) |
| `HTTPS_PROXY` / `HTTP_PROXY` | unset                | Honored by the curl download path and by `uv` during install                              |

Set `VIBECRAFTED_HOME` **before** the first install if you want the state root somewhere else:

```bash
export VIBECRAFTED_HOME="$HOME/work/vibecrafted-state"
open https://github.com/vetcoders/vibecrafted/releases/latest
# Download and verify Vibecrafted_<version>-<YYYYMMDD>-<sha8>.dmg, then open it.
```

## Provenance discovery (receipt)

`vibecrafted receipt` never uses the process working directory to identify a tool's source checkout. When auto-discovery fails, point it explicitly:

| Variable                 | Points at                                           |
| ------------------------ | --------------------------------------------------- |
| `VIBECRAFTED_SOURCE`     | Source checkout of the vibecrafted framework        |
| `VC_FRAME_SOURCE`        | Source checkout of vc-frame                         |
| `LOCTREE_SOURCE`         | Source checkout of loctree                          |
| `AICX_SOURCE`            | Source checkout of aicx                             |
| `VIBECRAFTED_FLEET_ROOT` | One parent directory containing all fleet checkouts |

```bash
VIBECRAFTED_FLEET_ROOT="$HOME/projects" vibecrafted receipt --json
```

## Docker

| Variable                         | Default | Effect                                                                                                             |
| -------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------ |
| `VIBECRAFTED_DOCKER_SEED_SKILLS` | `1`     | Set to `0` to disable first-run skill seeding into `/workspace/.vibecrafted` when you mount your own runtime store |

## Precedent checks at launch

Set `VIBECRAFTED_PRECEDENS_HOOK` to the absolute path of the trusted fleet
`precedens-gate.py` to check the original task brief before a workflow starts.
This applies to workflow launches and dispatch-plan worker launches. For
`vibecrafted dispatch run` the enabled hook requires an explicit `--prompt-file`
to supply the brief. An unset hook leaves ordinary launches unchanged.

The hook reuses the caller's provider-session receipt. It accepts one
consistent identity from `CLAUDE_CODE_SESSION_ID`, `CODEX_THREAD_ID`, or
`CODEX_SESSION_ID`. Use `VIBECRAFTED_PRECEDENS_SESSION_ID` if the shell
filters those values or multiple provider identities are present.
A new launch without a caller identity
cannot borrow another session's receipt. Set these values in the operator's
launcher environment. Worker configuration does not choose the admission hook.

Refusals and invalid hook responses stop the launch before a worker starts.
This checks the supplied brief. Coverage of native provider tools and
the link between a continuation brief and its original case require separate
verification.

## Worker contract (injected — read-only)

When Vibecrafted launches a workflow run, it injects the run identity into the worker's environment. These are the contract surface a worker (or any tooling you hook into a run) can rely on. **Do not set them yourself** — the launcher owns them, and stale values are actively cleaned between runs.

| Variable                  | Injected value                                            | What a worker does with it                                      |
| ------------------------- | --------------------------------------------------------- | --------------------------------------------------------------- |
| `VIBECRAFTED_RUN_ID`      | The control-plane run id, e.g. `impl-<timestamp>-<id>`    | Identifies the run in status, settlements, and artifact naming  |
| `VIBECRAFTED_REPORT_PATH` | Absolute path under `~/.vibecrafted/artifacts/…/reports/` | The worker writes its final durable report to exactly this path |

A worker prompt receives the same instruction: _write your final report to the path in `VIBECRAFTED_REPORT_PATH`_. If a worker exits without writing it, the supervisor salvages a report from the transcript and marks it as salvaged.

Inspect the contract inside a running worker:

```bash
printf 'run:    %s\nreport: %s\n' "${VIBECRAFTED_RUN_ID:-unset}" "${VIBECRAFTED_REPORT_PATH:-unset}"
```

## Stability notes

- The variables in the first three tables are the stable, public surface.
- Additional `VIBECRAFTED_*` variables exist inside the runtime (session ambience, marbles loops, operator sessions). They are internal wiring, subject to change without notice — build nothing on them.
- Agent CLI credentials are read from each agent's own environment and config stores. Vibecrafted never stores secrets; skills read credentials from environment variables only.

## Next

- [Configuration](/docs/configuration/) — the directory surfaces these variables relocate.
- [Doctor](/docs/doctor/) — verifying the environment resolved correctly.
