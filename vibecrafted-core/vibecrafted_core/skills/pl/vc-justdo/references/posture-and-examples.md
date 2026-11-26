# vc-justdo — Taksonomia, tryby launchera i granice własności

## Taksonomia

```yaml
vc-justdo:
  kind: standalone_posture_skill
  pipeline: none # NON-pipeline — nie faza cadence VC-ship (tą jest vc-implement)
  posture: vc-ownership
  task_type: defined_by_prompt # implement | review | audit | research | fix | anything
  scope: interactive_or_headless_session
  questions: none # interactive: eksploracja zamiast interrogacji
```

Wywołanie skilla ≠ wywołanie runtime. `$vc-justdo` w czacie = agent przyjmuje
postawę Just Do. `vibecrafted justdo <agent>` / `vc-justdo <agent>` = osobny run
runtime ze skill id `justdo`.

## Dwa tryby i przykłady launchera

**1. Non-interactive (launcher `justdo`):** typ zadania jest w prompcie; zero pytań; wykonaj.

```bash
vc-justdo claude --prompt 'zrób review moich ostatnich 5 komitów pod kątem X'
vc-justdo codex  --file  <broad-implementation-plan>.md
vibecrafted justdo gemini --prompt 'Audit the install path only'
```

**2. Interactive (`/vc-justdo`):** po wywołaniu brak dalszych pytań; przy cienkim
kontekście proaktywnie eksploruj zamiast pytać.

## Granice `vc-ownership`

Z [`../../../vc-ownership/SKILL.md`](../../../vc-ownership/SKILL.md):

- **Ruszaj natychmiast (odwracalne):** edycje, testy, dokumentacja, zawężone refaktory, lokalny smoke, recovery-commity.
- **Pauza i uzgodnienie (nieodwracalne):** destrukcyjny git, merge do trunka, deploy/publish, koszty, sekrety/auth, produkcyjne dane.

## Miejsce w matrycy i dowód

- `vc-justdo` stoi **obok** pipeline'u VC-ship (non-pipeline, ADR-0001). Etap WRITE w ship to `vc-implement`.
- Zdjęcie ceremonii nie zdejmuje weryfikacji: kończysz `[x]` walk-around / DoU, nie `[~]` na słowo. Zobacz [Verification Rule](../../../VERIFICATION_RULE.md).
