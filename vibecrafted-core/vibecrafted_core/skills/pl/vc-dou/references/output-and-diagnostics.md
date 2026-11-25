# `vc-dou` — Format wyjścia, antywzorce i diagnostyka plagi

## Format wyjścia

```markdown
# Definition of Undone: <project/ecosystem>

Date: <YYYY-MM-DD>
Auditor: <agent>

## Executive Summary

<2-3 sentences: gap between code and market>

## Undone Matrix

| Project | Repo | Web | Commercial | Critical Gap |
| ------- | ---- | --- | ---------- | ------------ |

## Findings by Severity

### P0 — Ship Blockers

### P1 — Credibility Gaps

### P2 — Polish

## The Funnel Test

Discovery → Landing → Understanding → Trial → Adoption → Payment
<for each product, mark where the funnel breaks>

## Hydration Priorities

<ordered fix list with effort estimates>

## Plague Score

0 = fully shipped and discoverable | 100 = brilliant, commercially invisible
```

## Antywzorce

- Uruchamianie DoU tylko na kodzie (to audyt powierzchni PRODUKTU)
- Traktowanie `[OK]` repo health jako dowodu gotowości
- Audytowanie bez crawlowania URL-i
- Zakładanie, że produkty nie-webowe nie potrzebują powierzchni reprezentacji
- Pomijanie testu ścieżki instalacji
- Raportowanie bez rankingu po severity
- Nieuruchamianie ponownie po hydracji

## Diagnostyka plagi (The Plague Diagnostic)

Wzorzec plagi:

1. Testy przechodzą `[PASS]`
2. Architektura solidna `[PASS]`
3. README istnieje `[PASS]`
4. Nikt nie znajdzie tego z Google `[FAIL]`
5. Nikt nie zainstaluje bez toolchainu `[FAIL]`
6. Nikt nie może za to zapłacić `[FAIL]`

Punkty 4-6 to Definition of Undone.
