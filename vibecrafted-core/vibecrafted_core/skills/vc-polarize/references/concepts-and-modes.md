# vc-polarize — Core Vocabulary & Modes Reference

## Core Vocabulary

### Code Smear

A runtime or product concept whose truth is spread across many files,
layers, docs, tests, artifacts, public surfaces, and operator memory.
Smear is not automatically bad — it becomes dangerous when the spread
creates **competing** truths.

### Prism Score

Diagnostic score for how much a concept refracts across `loct
context --task` framings. High prism score means:

- one local slice will mislead future agents
- the concept deserves a corpus entry
- a polarization pass may be needed before release

It does **not** mean: bad code, CI failure, shame KPI, file-count
penalty.

### Polarization

The opposite motion from smear. Pick one axis / facet and make
runtime, tests, docs, artifacts, and public surfaces agree.

## Modes

### Concept Mode

Use when an architectural / runtime concept is smeared. Examples:
marbles lifecycle, release surface, installer public contract,
research swarm synthesis, auth boundary, memory/search context.

Output: one concept contract and proof path.

### Product Mode

Use when a product / public surface is smeared. Examples: too many
audiences, split CTA, landing page disagreeing with install path,
docs overpromising runtime, release brief lacking one shippable thesis.

Output: one product thesis and DoU / release handoff.
