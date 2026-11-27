# vc-marbles — Przykłady launchera

Standardowy launcher:

```bash
# Single round (3 runs by default):
vibecrafted marbles codex --prompt 'Fix the 3 failing portable tests'
vc-marbles codex --prompt 'Harden the installer shell surface'

# Multiple rounds (convergence loop — runtime spawns fresh agent 3..n times)
vibecrafted marbles codex --count 5 --prompt 'Stabilize until P0=0'
vc-marbles claude --count 8 --prompt 'Refactor the 1500 LOC monoliths'

# From a plan file:
vibecrafted marbles codex --file ~/.vibecrafted/artifacts/vetcoders/vibecrafted/2026_0407/plans/marbles-plan.md
vc-marbles gemini --count 5 --file /path/to/plan.md

# Crawl back into the canonical store then read 'n' recently
# implemented plans then fill the all the gaps:
vibecrafted marbles codex --count 10 --depth n
vc-marbles claude --depth 12 --prompt 'Focus on "vc-followup assumptions from the last 12 plans'
```

**To nie to samo co `vibecrafted implement codex <plan>`.** `implement`
to sposób, w jaki kod powstaje. `marbles` to to, co dzieje się po tym, jak kod
już istnieje, ale wciąż trzeba uczynić go prawdziwym i gotowym do dowiezienia.
Każda runda owija świeżego agenta w gorącą pętlę zbieżności. `--count` steruje
liczbą iteracji pętli zewnętrznej.
