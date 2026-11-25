# vc-scaffold — Artifacts, Hard-Gates & Serve/Doctor Reference

### 5.5 DRIVER.md (HARD-GATE — the Founder's hand-off driver)

Alongside the briefs, render **one `DRIVER.md`** co-located with `briefs/`. It is the single
self-sufficient artifact the Founder (or a cold fleet) drives the whole plan from **when the
in-thread loop dies**. NOT optional, NOT a re-skin of the atlas — it is the executable hand-off.
It MUST contain all six:

1. **Full absolute paths** — every plan artifact, brief, orient evidence, and input/fixture, as
   copy-pasteable absolute paths.
2. **Dependency graph WITH a `why` on every edge** — what-after-what AND why: why each cut precedes
   the next; why a pair is **SEQUENCE** (shared file domain → Living Tree conflict) vs **PARALLEL**
   (disjoint domains → safe concurrent); and where every **⛔ Founder-button STOP** sits
   (trunk merge, force-push, PR merge/close, tag/branch deletion, deploy, product decisions,
   or a wave-specific push/install fence). A graph without `why` is a diagram, not a driver.
3. **Ready handoff** — run `vibecrafted scaffold-doctor --plan <root> --repo <git-root>` first
   (REFUSE = no handoff), then exactly one plan-level validation block for the canonical
   `<plan-id>.dispatch.toml` (`vibecrafted dispatch … --doctor` + dry-run), followed by the `/vc-ship`
   A→Z handoff, or the explicit Founder-ordered bounded `vibecrafted dispatch <plan>` route.
   The selected supervisor owns start and resume; the DAG owns order and allowed parallelism. Do
   not turn DRIVER into a per-cut launcher list and do not teach manual `vibecrafted workflow ... --prompt`
   sequencing.
4. **The state alphabet + the `[ ]→[x]` rule, reproduced verbatim** (mirrors Measurement):
   `[ ]` todo · `[~]` running · `[?]` done-unverified · `[!]` blocked · `[x]` verifier-green.
   **Only a delivery-verifier flips `[~]→[x]`; an agent's claim NEVER reaches `[x]` on its own.**
   The rule lives IN the DRIVER on purpose — so that mid-dispatch nobody promotes a claim to done
   without re-running the verifier. That promotion-without-proof is the single failure mode that
   wrecks an operator run ("rozjedziemy się"). Encode it where the dispatcher's eyes are.
5. **Live status snapshot** + `dou-index = |[x]| / total`.
6. **Reception matrix (Odbiór) — R12, Founder 2026-09-15.** A section
   `## Odbiór (matryca wyników)` with one row per cut
   (`cut | commit | dowód (Operator) | Worker | Operator | Founder`) and the signature line
   **`Zatwierdzono przez: Worker [ ] Operator [ ] Founder [ ]`**. Every box starts `[ ]` — an
   untouched `[ ]` is a NON-DELIVERY indicator, not a formatting nit. Worker flips its own boxes
   as part of delivery (the supervisor refuses to verify a cut whose Acceptance boxes are still
   `[ ]`); the flip is a claim, never proof — verifiers still decide. Operator flips only after
   running the verifiers itself. **`Founder [x]` may only exist alongside
   `acceptance/founder.json` in the plan root; an agent never signs for the Founder** —
   scaffold-doctor R12 refuses a plan with a forged Founder signature or no matrix at all.

### 5.6 manifest.json (HARD-GATE — canonical artifact inventory)

Create one plan root at
`${VIBECRAFTED_HOME:-$HOME/.vibecrafted}/artifacts/<org>/<repo>/<YYYY_MMDD>/plans/<plan_id>/` and write
`manifest.json` there as mandatory output. Schema version `"1"` declares `plan_id`, `org`, `repo`,
`day`, and an ordered `artifacts` array. Every artifact entry declares a stable `id`, explicit
`role`, relative `path`, `editable`, and `required`; optional `dependencies` contain artifact IDs.
Supported roles are `driver`, `wave-atlas`, `dispatch`, `brief`, `design-doc`, `traceability`, `tracker`,
`falsification`, `report`, and `other`. Register every generated artifact before handoff. Filenames
never imply roles. Do not create an `operator/` mirror, compatibility copy, naming alias, or symlink.

### 5.7 YAML frontmatter on EVERY artifact (HARD-GATE — no bare markdown)

Every markdown artifact this skill produces — MISSION, ATLAS, DRIVER, tracker, falsification,
every brief, every design doc — opens with YAML frontmatter, no exceptions:

```yaml
---
plan_id: <plan_id>
run_id: <scaffold run id, when running under a lifecycle>
session_id: <agent session_id from `aicx sessions current` or raw `.jsonl` filename read>
role: driver | wave-atlas | brief | tracker | falsification | design-doc | mission | other
author: <artifact author>
agent: <executing agent/provider, if bound>
date: YYYY-MM-DD
project: <org>/<repo>
---
```

`author` records who created the artifact; it never selects its executor. For an
executable brief, `agent` binds the intended executing agent/provider, which may
differ from the author. It can be omitted when the launcher or typed dispatch
plan supplies the executor. When reusing a brief with `agent`, ensure that binding
matches the selected executor: a conflict is refused. Never infer an executor
from `author`.

Why this is a hard-gate, not decoration: the settlement contract's rule 6 ("no bare markdown —
artifact without run_id lands as needs-attention"), retrieval (search/index engines rank and
scope by these fields), and provenance (an artifact found loose on disk must identify its plan
and author without archaeology). A plan package with bare-markdown members fails scaffold review
the same way a missing brief does. A prior field report recorded this on 2026-07-23 after receiving a
package with frontmatter on some members and none on others — mixed is worse than missing,
because it teaches readers to stop checking.

### 5.8 `<plan-id>.dispatch.toml` (HARD-GATE — supervisor-readable execution contract)

Every scaffold, including a one-cut scaffold, ends with a `<plan-id>.dispatch.toml` using schema
`vibecrafted.dispatch.v1`. It encodes the complete cut set, named phases, `depends_on` edges,
explicit allowed concurrency, agent/workflow identity and model pins, per-cut brief paths, commit policy, and
delivery-verifiers. Register it in `manifest.json` with role `dispatch`. The cut IDs and brief paths
MUST cover every executable cut in the atlas exactly once; no second scheduling truth is allowed.
Prove the artifact before handoff with:

```bash
vibecrafted dispatch <absolute-plan-root>/<plan-id>.dispatch.toml --doctor
vibecrafted dispatch <absolute-plan-root>/<plan-id>.dispatch.toml --dry-run --json
```

After validation, hand that exact artifact to `/vc-ship` for the normal A→Z lifecycle.
For an explicit Founder-ordered bounded dispatch, DRIVER may instead name
`vibecrafted dispatch <plan.dispatch.toml>` and its resume command. This is a supported
shaped-wave route, not a second scheduler. Preserve Founder model pins verbatim, headless
workers by default, and armed supervisor-side `vibecrafted await <agent> --run-id <id>`.
Workers finish foreground gates, report and commit in the current turn; they cannot be
woken by background completions. Worker acceptance boxes never sign for Operator/Founder.

Do not require the Founder to hand-write TOML or paste one `vibecrafted workflow <agent> --prompt ...`
command per task. Manual per-cut launch instructions do not belong in **Running This Plan** or the
normal DRIVER path. Besides the supported bounded plan-level route, an emergency recovery note may use a per-cut launch
only after naming the `/vc-ship`/supervisor failure and the reason the normal route is unavailable;
it must record return-control evidence and may not become a parallel execution system.

### Compile-embargo plans

If a plan defers compile/test gates while shaping architecture, apply the phase-aware recovery
contract in `references/compile-embargo.md`. Once the Founder authorizes an embargo phase,
`--no-verify` is fully authorized for each local worker checkpoint in that phase. It bypasses the
bundled Git hook entrypoint as a whole, so workers report what ran and what was skipped; it is not
a security or compile/test delivery claim. Workers do not push; a push using `--no-verify` is an
exclusive Founder button. The designated integrator may make
a local structural admission after exact commit/scope, Semgrep, and secret/security review, so later
waves can build on the joined architecture while compile, lint, type-check, and tests remain
deferred. Only named closure plus full language-appropriate gates creates verified delivery.

### 6. Serve & review (editable artifacts via vibecrafted-server)

The plan + briefs are **editable artifacts**, not a wall of inline questions. The flow is:
research → present findings + effort estimate → propose the first cut/wave shape → render the
briefs → **serve them for Founder review through `vibecrafted-server`** (the natural home of this
phase's tooling: it reads the typed control-plane contract and renders the wave atlas + briefs as a
**multi-tab, editable** HTML surface — one tab per artifact (atlas · each brief · each design doc),
edited in place). The Founder steers by editing the rendered plan in the browser, not by answering
twenty questions mid-scaffold. Refine WITH the Founder on the served artifacts.

**Transplant the surface — do not reinvent it.** Proven sources to lift from: `../pensieve`
(multi-tab editable workspace dashboard), `../unicode-puzzles-portal` (portal generators), and
`/brainstorming`'s visual-companion (proven HTML mockup/diagram generators). The server-review tab
must be multi-tab + editable from day one, not a static dump.

**scaffold-doctor (the gate, machine-checked):** run the product verb before any
scaffold→implement handoff — do not treat the validator as an external server-only tool:

```bash
vibecrafted scaffold-doctor --plan <root> --repo <git-root>
```

REFUSE (exit 1) means no handoff. The verb locates the generation (or locally built)
`scaffold-doctor` binary and loads the same typed `manifest.json` the server uses. It refuses
until: the manifest identity matches its canonical plan root; all declared required artifacts
exist; IDs and paths are unique; dependencies resolve; editable paths are non-symlinked and remain
inside the plan root; briefs on disk are declared; and the atlas has a wave atlas + dependency
graph; every cut has a `briefs/<wave>-<slot>_<slug>.md` with all 12 sections; acceptance bullets are
atomic + verifier-backed; a design doc exists for every cut flagged `needs_design`; **a `DRIVER.md`
exists and carries all six (full paths · why-annotated graph · ready commands · the `[ ]→[x]` rule
verbatim · status snapshot · the R12 reception matrix with an unforged Founder box)**. The gate is
**machine-checked, not agent-promised** — it is the
same artifact-as-truth gate the async runtime uses between every read-write cadence handoff.
