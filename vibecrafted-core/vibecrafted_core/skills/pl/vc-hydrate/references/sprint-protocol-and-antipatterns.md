# vc-hydrate — Protokół sprintu, pipeline, delegacja i antywzorce

## Protokół hydrate sprintu

1. **Wczytaj raport DoU.** Wyciągnij wszystkie findingi P0/P1. Posortuj wg wpływu (powierzchnia komercyjna > odkrywalność > zarządzanie repo).
2. **Triage do domen.** Zmapuj każdy finding do domeny (1-6). Niektóre findingi mapują się na wiele — wypisz wszystkie.
3. **Wygeneruj artefakty.** Per finding: brakujące pliki → utwórz je; brakująca meta → wygeneruj HTML; brakująca ścieżka instalacji → workflow CI; brakujący landing → napisz copy; brakująca reprezentacja → scaffold odpowiedni do typu produktu; brakujący listing marketplace → wygeneruj listing.
4. **Zweryfikuj przez DoU.** Uruchom ponownie na obszarach, których to dotyczy. Cel: redukcja Plague Score o ≥20 punktów.
5. **Przedstaw użytkownikowi.** Raport po hydrate z Plague Score'ami przed/po, tabelą artefaktów wygenerowanych według domen (status) oraz pozostałymi krokami ręcznymi (DNS, klucze API, przycisk submit w marketplace itd.).

## Integracja z pipeline'em

```
Phase 1 — Craft:     scaffold → init → workflow → followup
Phase 2 — Converge:  marbles ↻ (loop until P0=P1=P2=0)
Phase 3 — Ship:      dou → decorate → hydrate → release
```

Hydrate produkuje artefakty do dystrybucji i prezentacji. `vc-decorate` dopracowuje spójność wizualną przed hydrate. Po hydrate `vc-release` zajmuje się deployem i go-to-market launchem. Uruchom ponownie DoU po hydrate, aby zweryfikować, że luka się domknęła.

## Delegacja do subagentów

Przy dużych sprintach hydrate rozbij domeny między subagentów, używając `vc-agents`:

```
Agent 1: Repo Hydration (LICENSE, CONTRIBUTING, CI, CHANGELOG)
Agent 2: Distribution Hydration (release workflows, installers)
Agent 3: Discoverability Hydration (SEO, meta tags, pre-rendering)
Agent 4: Commercial Hydration (landing copy, marketplace listings)
```

Każdy agent dostaje: findingi DoU dla swojej domeny, szablony artefaktów z tego skilla, standardową preambułę Living Tree.

## Antywzorce

- Hydrate bez wcześniejszego audytu vc-dou (naprawianie tego, co zakładasz, nie tego, co zmierzone)
- Generowanie plików bez kontekstu repo (typ LICENSE musi pasować do intencji projektu)
- Pisanie copy marketingowego bez zrozumienia produktu (najpierw uruchom vc-init)
- Zakładanie, że produkty desktopowe / CLI / MCP / lokalne nie potrzebują warstwy reprezentacji
- Zakładanie, że hydrate robi się raz i temat znika. Hydrate powinien wracać cyklicznie, tak jak refactoring: po większych zmianach, przed release i po każdym DoU, które pokaże nowe luki.
- Hydrate wszystkiego naraz (priorytetyzuj: najpierw luki komercyjne P0)
- Zapominanie o ponownym uruchomieniu DoU po hydrate (zweryfikuj poprawkę)
