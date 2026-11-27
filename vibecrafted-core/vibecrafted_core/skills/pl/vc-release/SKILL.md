---
name: vc-release
version: 0.2.1
description: >
  Final outward ship skill. Turns "done in the repo" into "safe, visible, deployable,
  discoverable, and launchable in the world." Covers release mechanics, deployment
  topology, reverse-proxy defaults, Semgrep-gated security hygiene, domain and DNS
  wiring, SEO/indexability, verification challenges, onboarding truth, and post-release
  smoke checks. Trigger phrases: "release", "ship to market", "publish",
  "deploy to production", "vc-release", "go live", "launch", "wypuść wersję",
  "deploy", "release prep", "launch path", "launch checklist", "production checklist".
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Wywołanie dla `vc-release` (launcher `release`)**
>
> Ten sam _kształt_ trzech ścieżek floty, z **literałami tego** skilla — zobacz
> kanoniczną [Matrycę Delegacji](../DELEGATION_MATRIX.md):
>
> - [Wspólne trzy ścieżki](../DELEGATION_MATRIX.md#wspólne-trzy-ścieżki)
> - [Katalog launcherów](../DELEGATION_MATRIX.md#katalog-launcherów-core-runtime)
> - [Reguła per-launcher](../DELEGATION_MATRIX.md#reguła-per-launcher-delta-semantyczna)
> - [Native vs external](../DELEGATION_MATRIX.md#natywne-subagenty-vs-zewnętrzni-workerzy)
>
> | Ścieżka               | Literał tego skilla                                                                                                            |
> | --------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
> | 1. Worker użytkownika | `vibecrafted release <agent>`                                                                                                  |
> | 2. Interactive        | `/vc-release` — wykonaj **w tej sesji**; native subagenty gdy trzeba; **nie** zewnętrzniaj tylko dlatego, że launcher istnieje |
> | 3. Agent-operator     | może odpalić formę workera powyżej przez `vc-dispatch` / linie operatora, zachowując tożsamość tego skilla                     |

> Swobodniejszy native na niektórych biegach ≠ porzucenie floty external. `vc-dispatch` i `vc-ship` zachowują własne tożsamości.

<!-- /fleet-imperative -->

# vc-release — Dowieź bez ściemy

> „Zrobione w repo" to nie „zrobione w świecie".

## Wejście operatora

### Reguła Living Tree / Worktree

Ten workflow działa w bieżącym checkoucie i na bieżącej gałęzi operatora. Nie twórz worktree gita, nie przełączaj się na niego ani nie przenoś do niego wykonania, chyba że operator wprost poprosi o worktree w tym prompcie. Ogólne słowa w stylu „isolate", „parallel" czy „clean branch" to za mało. Jedyny usankcjonowany drugi tryb to dispatch Fleet Worktrees (pisany plan, zacommitowane wcześniej verifiery, rozłączne domeny plików, jednowątkowy integrator — patrz Reguła Living Tree, Tryb B); poza tą formacją zostań we wspólnym drzewie. Czytaj pliki ponownie przed edycją, dostosowuj się do równoległych zmian i zgłoś awarię podłoża (substrate failure), jeśli bieżące drzewo jest zbyt zatrute, by bezpiecznie kontynuować.

Zobacz [Reguła Living Tree](../LIVING_TREE_RULE.md).

## Checkpoint orientacji

Zanim ten workflow wykona analizę specyficzną dla repo, planowanie, implementację, review, release lub delegację, MUSI uruchomić lub skonsumować procedurę `vc-init` dla przypisanego repo. Jeśli brak świeżego evidence z `vc-init`, wykonaj najpierw przebieg init i traktuj pracę specyficzną dla workflow jako zablokowaną, dopóki nie ma aktualnej prawdy repo.

`Loctree:loctree` to domyślny skill do mapowania struktury repo dla tego przebiegu. Użyj Loctree przed grepem lub twierdzeniami z dokumentacji, aby wyprodukować lub odświeżyć Mapę Aplikacji Wyprowadzoną z Kodu (Code-Derived Application Map): repo-view, focus, slice, impact, find i follow w odpowiednim zakresie. Szukaj istniejących symboli i kontraktów, zanim utworzysz nowe; uruchom impact przed usunięciem lub dużym refaktorem; uruchom slice przed edycją.

Chodzi o znalezienie zaczepów: węzłów nośnych, twins (duplikaty), martwego kodu, dryfu, entrypointów runtime'u oraz pułapek o dużym zasięgu zmiany. Jeśli task jest jawnie poza repo lub bez kodu, zadeklaruj wyjątek no-repo w raporcie. W przeciwnym razie brak evidence z `vc-init`/Loctree to porażka procesu.

Wejdź przez `vibecrafted start` (lub `vc-start`). Następnie odpal przez command deck:

```bash
vibecrafted release codex --prompt 'Prepare v1.2.1 release'
vc-release claude --prompt 'Ship the web surface safely behind Caddy'
vibecrafted release gemini --file /path/to/release-checklist.md
```

Preferuj `--file` dla istniejącego planu, `--prompt` dla intencji inline.

Release to nie ceremonia. Release to operacyjny kontrakt bezpieczeństwa, widoczności i adopcji.

## Doktryna pracy z repozytorium

W pracy z repozytorium zacznij od Loctree jako mapy: użyj `loct context`,
`loct occurrences`, `loct body` i `loct find --literal` przed szerokim ręcznym
przeszukiwaniem. Używaj AICX do kontekstu intencji i sesji. Używaj rg/grep jako
fallbacku lub lokalnej lupy, nie jako zamiennika mapowania strukturalnego. Jeśli Loctree
zawiedzie lub przeoczy jakąś powierzchnię, dopisz feedback do `~/.vibecrafted/loctree/loctree-fail.md`.

## Pozycja w pipelinie

```
scaffold → init → workflow → followup → marbles → dou → decorate → hydrate → [RELEASE]
```

Release uruchamia się po tym, jak `vc-dou` zweryfikuje powierzchnię produktu, `vc-decorate` zapewni spójność wizualną, a `vc-hydrate` opakuje dystrybucję/SEO/onboarding. Release urealnia artefakty po hydrate: tagi, changelogi, publikację rejestru/binarek, topologię deploya, proxy/TLS, domenę/DNS/weryfikację, indeksowalność, bramki bezpieczeństwa, post-release smoke.

## Podłoga powierzchni publicznej

`vc-release --floor` jest bramką wydania. Sam tag bez obiektu GitHub Release nie kończy etapu; `--require-release` zostaje czerwone, dopóki Release nie istnieje.

Publikuj, gdy podłoga kończy się kodem 0. `install_cta: no` znaczy: nie mów obcemu, żeby instalował. Samo to nie blokuje Release, które ten etap dopiero tworzy. Gdy jedyną luką jest GitHub Release, które wydawca zaraz utworzy, podłoga ostrzega i kończy się kodem 0, a `install_cta` zostaje `no`, dopóki ten Release nie istnieje. `--acknowledge <surface-id>` zapisuje świadomie przyjętą lukę i zostaje w raporcie. `scripts/publish-vibecrafted-release.sh --acknowledge <surface-id>` oraz `make publish-release ACKNOWLEDGE="<surface-id>"` przekazują tylko identyfikator powierzchni i odrzucają każdą inną flagę podłogi.

Kontrakt: [`../../vc-dou/references/public-surface-floor.md`](../../vc-dou/references/public-surface-floor.md).

## Główna zasada

**Jeśli poniższy kanon release'u nie jest spełniony, release jest no-opem.** Nie myl „umiem to zdeployować" z „jest bezpieczne, widoczne i gotowe, by wyjść do obcych".

## Kanon release'u (Release Canon) — sześć płaszczyzn

1. **Prawda artefaktu** — wersje, tagi, changelog, opublikowane wyjścia
2. **Prawda deploya** — topologia, proxying, healthchecki, zachowanie przy restarcie
3. **Prawda bezpieczeństwa** — Semgrep, wyeksponowane powierzchnie, headery, auth, obsługa sekretów
4. **Prawda domeny** — DNS, domyślny host, TLS, redirecty, wyzwania weryfikacyjne
5. **Prawda widoczności** — SEO, indeksowalność, social cards, sitemap, robots, publiczne metadane
6. **Prawda onboardingu** — ścieżka instalacji, pierwsze uruchomienie, docs, screenshoty, quickstart, ścieżka kupującego

Jeśli brakuje którejkolwiek płaszczyzny, wskaż to jawnie i zablokuj release, chyba że użytkownik świadomie akceptuje ryzyko.

## Kanon artefaktu, topologia deploya i domyślne reguły proxy

Otaguj dokładny commit, utrzymuj zgodność changeloga i artefaktów rejestru z opisowymi nazwami plików oraz wybierz najmniejszy uczciwy stack (Caddy, Nginx lub Docker). Domyślnie binduj usługi do `127.0.0.1`, terminuj TLS na celowym reverse proxy zachowującym nagłówki `Host`/forwardujące/websocket, wstrzykuj sekrety w runtimie i wymagaj `/health` oraz kontenerów non-root.

Pełny kanon, bezpieczna drabina, domyślne ustawienia bezpieczeństwa, czerwone flagi i zasady reverse proxy: [references/deployment-and-proxy.md](references/deployment-and-proxy.md).

## Bramka release'u Semgrepa

Semgrep jest częścią kanonu (nieopcjonalny): przed release'em uruchom `make semgrep` na pełnym repo, klasyfikuj findingi wg **granicy przepływu danych** i zablokuj release przy każdym nierozwiązanym blokującym findingu, chyba że użytkownik zaakceptuje ryzyko na piśmie w raporcie. Gdy Semgrep jest niedostępny, uruchom `uvx semgrep` i zapisz niespełnienie bramki.

Pełne reguły naprawcze granic przepływu danych i minimalne klasy findingów: [references/semgrep-gate.md](references/semgrep-gate.md).

## Kontrakt raportu release'u

Każdy raport release'u musi zawierać te obowiązkowe sekcje i linkować z powrotem do
`references/release-report-template.md`:

- **Bramka bezpieczeństwa** — evidence z `make semgrep`, findingi i nierozwiązane ryzyko.
- **Inwentarz wyeksponowanej powierzchni** — publiczne route'y, usługi, porty, domeny oraz powierzchnie admin/debug.
- **Decyzja o trybie deploya** — wybrana topologia, postawa proxy/TLS oraz ścieżka rollbacku.
- **Smoke instalacji po release'ie** — weryfikacja instalacji/uruchomienia zimną ścieżką z opublikowanego artefaktu.

## Domena, widoczność, onboarding i smoke po release'ie

Publiczne powierzchnie muszą zweryfikować DNS, redirecty kanonicznego hosta, TLS, dowody własności `.well-known/*` / TXT, indeksowalne HTML/SSR SEO, `robots.txt`/`sitemap.xml`, onboarding pierwszego użytkownika na zimno oraz smoke test z opublikowanego artefaktu (nigdy z lokalnego checkoutu). Release wymaga też realiów finansowo-prawnych i unikania antywzorców.

Pełne checklisty domeny/DNS, SEO i widoczności, prawdy onboardingu, smoke weryfikacji na zimno, szczegółowego rozkładu raportu, realiów finansowo-prawnych i antywzorców: [references/visibility-smoke-and-antipatterns.md](references/visibility-smoke-and-antipatterns.md).

> Kanoniczny szablon: [`references/release-report-template.md`](references/release-report-template.md).
> Pełny checklist operatora: [`references/release-checklist.md`](references/release-checklist.md).
> Pogłębienie realiów deploya: [`references/deployment-reality.md`](references/deployment-reality.md).

## Zasada końcowa

Dowoź tylko wtedy, gdy jest wystarczająco bezpieczne, wystarczająco widoczne, wystarczająco instalowalne, wystarczająco zrozumiałe, a historia deploya jest wystarczająco nudna, by jej zaufać. Jeśli nie — uczciwym wynikiem `vc-release` nie jest „done", lecz „zablokowane, z tych dokładnie powodów".

---

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
