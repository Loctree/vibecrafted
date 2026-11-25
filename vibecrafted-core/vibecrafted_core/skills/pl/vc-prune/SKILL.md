---
name: vc-prune
version: 3.3.3
description: >
  Repository curation, not clear-cutting. Map what truly participates in runtime 
  truth versus what is silently parked — then decide revive, archive, or delete. 
  Includes the silencer strip: rip every `#[allow(...)]`, `// nosemgrep`, 
  `eslint-disable`, `@ts-ignore`, `# noqa`, `# type: ignore`, panic-vs-skip pattern, 
  and any other annotation that mutes a quality gate. Run the gates. Listen.
  Triage with care — `#[allow(dead_code)]` (and equivalents) is often the most 
  valuable smell in a repo: parked work the team forgot about. Surface those as 
  forgotten gems for the operator to decide.
  This skill is a gem hunter, not a clear-cutter.
  Trigger phrases: "prune", "strip dead code", "wyczyść mądrze", "strip the silencers",
  "zdejmij wszystkie ignore", "zobacz co realne", "forgotten gems",
  "co tam zapomnieliśmy".
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Wywołanie dla `vc-prune` (launcher `prune`)**
>
> Ten sam _kształt_ trzech ścieżek floty, z **literałami tego** skilla — zobacz
> kanoniczną [Matrycę Delegacji](../DELEGATION_MATRIX.md):
>
> - [Wspólne trzy ścieżki](../DELEGATION_MATRIX.md#wspólne-trzy-ścieżki)
> - [Katalog launcherów](../DELEGATION_MATRIX.md#katalog-launcherów-core-runtime)
> - [Reguła per-launcher](../DELEGATION_MATRIX.md#reguła-per-launcher-delta-semantyczna)
> - [Native vs external](../DELEGATION_MATRIX.md#natywne-subagenty-vs-zewnętrzni-workerzy)
>
> | Ścieżka               | Literał tego skilla                                                                                                          |
> | --------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
> | 1. Worker użytkownika | `vibecrafted prune <agent>`                                                                                                  |
> | 2. Interactive        | `/vc-prune` — wykonaj **w tej sesji**; native subagenty gdy trzeba; **nie** zewnętrzniaj tylko dlatego, że launcher istnieje |
> | 3. Agent-operator     | może odpalić formę workera powyżej przez `vc-dispatch` / linie operatora, zachowując tożsamość tego skilla                   |

> Swobodniejszy native na niektórych biegach ≠ porzucenie floty external. `vc-dispatch` i `vc-ship` zachowują własne tożsamości.

<!-- /fleet-imperative -->

# vc-prune — Kuratorstwo, nie wycinka

> Nie pal domu. Zdejmij wszystko aż do nośnych ścian i zdaj raport z tego, co znalazłeś za tapetą.

## Wejście operatora

### Reguła Living Tree / Worktree

Ten workflow działa w bieżącym checkoucie i na bieżącej gałęzi operatora. Nie twórz worktree gita, nie przełączaj się na niego ani nie przenoś do niego
wykonania, chyba że operator wprost poprosi o worktree w tym prompcie. Ogólne słowa w stylu „isolate", „
parallel" czy „clean branch" to za mało. Jedyny usankcjonowany drugi tryb to dispatch Fleet Worktrees (pisany plan, zacommitowane wcześniej verifiery, rozłączne domeny plików, jednowątkowy integrator — patrz Reguła Living Tree, Tryb B); poza tą formacją zostań we wspólnym drzewie. Czytaj pliki ponownie przed edycją, dostosowuj się do równoległych zmian i zgłoś
awarię podłoża (substrate failure), jeśli bieżące drzewo jest zbyt zatrute, by bezpiecznie kontynuować.

Zobacz [Reguła Living Tree](../LIVING_TREE_RULE.md).

## Checkpoint orientacji

Zanim ten workflow wykona analizę specyficzną dla repo, planowanie, implementację, przegląd, release lub delegowanie, MUSI
uruchomić lub skonsumować procedurę `vc-init` dla przypisanego repo. Jeśli brakuje świeżych dowodów z `vc-init`, najpierw wykonaj
przebieg init i traktuj pracę specyficzną dla workflow jako zablokowaną, dopóki nie ma aktualnej prawdy repo.

`Loctree:loctree` to domyślny skill do mapowania struktury repo dla tego przebiegu. Używaj Loctree przed grepem lub twierdzeniami
opartymi na dokumentacji, aby wygenerować lub odświeżyć Mapę Aplikacji Wyprowadzoną z Kodu (Code-Derived Application Map):
repo-view, focus, slice, impact, find i follow w odpowiednim zakresie. Szukaj istniejących symboli i kontraktów, zanim utworzysz
nowe; uruchom impact przed usunięciem lub dużym refactorem; uruchom slice przed edycją.

Chodzi o znalezienie zaczepów: węzłów nośnych, twins (duplikaty), martwego kodu, dryfu, entrypointów runtime'u oraz pułapek o dużym zasięgu zmiany.
Jeśli zadanie jawnie nie dotyczy repo lub nie dotyczy kodu, odnotuj w raporcie wyjątek „bez repo". W przeciwnym razie brak dowodów z `vc-init`
/Loctree to błąd procesu.

Uruchom przez command deck (pełny kontrakt wejścia operatora znajdziesz w `vc-init`):

```bash
vibecrafted prune <agent> --file /path/to/prune-plan.md
vc-prune codex --prompt 'Strip silencers and listen'
```

Vibe-codowane repo zwykle zbiera dwie warstwy gruzu: **martwą powierzchnię** (porzucone eksperymenty z auth, zdublowane
handlery Stripe'a, martwe funkcje serverless) oraz **wyciszoną powierzchnię** (warningi zamknięte w pośpiechu, testy, które zawsze się skipują,
paniki, które zawsze odpalają). `vc-prune` oddziela obie warstwy od prawdy runtime'u — i jedną od drugiej.

## Doktryna pracy z repozytorium

W pracy z repozytorium zacznij od Loctree jako mapy: użyj `loct context`,
`loct occurrences`, `loct body` i `loct find --literal` przed szerokim ręcznym
przeszukiwaniem. Używaj AICX do kontekstu intencji i sesji. Używaj rg/grep jako
fallbacku lub lokalnej lupy, nie jako zamiennika mapowania strukturalnego. Jeśli Loctree
zawiedzie lub przeoczy jakąś powierzchnię, dopisz feedback do `~/.vibecrafted/loctree/loctree-fail.md`.

## Aksjomaty

1. **Agresywny prune, z wiarą w archiwum VCS.** Martwy kod to nie zły kod — to cmentarz wartościowych pomysłów. Jego miejsce jest
   w historii Gita, nie w runtimie. Tnij bez sentymentów — ale dopiero po aksjomacie 4.
2. **Idź naprzód zamiast trzymać się wstecznej kompatybilności.** Zgniłe abstrakcje blokujące stabilizację tnie się czysto. Graf
   zależności jest częścią prawdy runtime'u.
3. **Kod wie. Zdejmij wyciszenie i słuchaj.** Każdy silencer to odroczona rozmowa. Większość dodano w pośpiechu. Jedyny uczciwy test tego,
   które wciąż zarabiają na swoje utrzymanie, to wyrwać je wszystkie i pozwolić mówić toolchainowi.
4. **`#[allow(dead_code)]` (i kuzyni) to często najwartościowszy sygnał w repo.** Zwykle oznacza zaparkowaną pracę — w 90%
   gotowy flow logowania, pipeline eksportu dla utraconego (churned) klienta, debugowy wizualizer, o którym nikt nie wspomniał nowym osobom w zespole.
   To **zapomniane perełki**, nie śmieci. Wydobądź je na powierzchnię; nigdy nie usuwaj automatycznie.

## Główny kontrakt

- Przy nietrywialnym prune zewnętrzny dispatch przez `vc-agents` to domyślny pierwszy ruch.
- Zakładaj, że 30% vibe-codowanego repo to martwe rusztowanie.
- Sklasyfikuj każdego kandydata: `KEEP-RUNTIME`, `KEEP-BUILD`, `MOVE-ARCHIVE`, `DELETE-NOW`, `VERIFY-FIRST` lub
  `FORGOTTEN-GEM`.
- Wolej wycinać całe martwe pionowe wycinki (slice'y) niż przycinać symboliczne liście.
- Dociskaj kontrakty po każdej fali: manifesty, dokumentacja, CI, bounds pakietów.
- Uruchamiaj bramki po każdej fali. Wymagaj jednego prawdziwego dowodu smoke albo build.

## Doktryna delegacji

| Potrzeba                                                | Najlepszy model |
| ------------------------------------------------------- | --------------- |
| Archeologia, ukryta osiągalność, łowienie perełek       | Claude          |
| Dokładne usunięcia, dociskanie manifestów, robota mech. | Codex           |
| Radykalne upraszczanie, wycinanie całych podsystemów    | Gemini          |

## Workflow

### Faza 1 — Zdefiniuj stożek runtime'u

Wychwyć: prawdziwe entrypointy, obowiązkowe flow użytkownika, ścieżkę build/release. Nie zaczynaj od „nieużywanych eksportów" — zacznij od „
czy to obsługuje żywy ruch?"

### Faza 2 — Zmapuj przez `loct`

```bash
loct auto && loct manifests && loct hotspots && loct dead
loct routes      # web/API
loct commands    # desktop/Tauri
loct events
```

### Faza 3 — Prune falami (od najbezpieczniejszej → do najryzykowniejszej)

- **Fala 1 — spaliny AI i rusztowanie prototypu.** `v1_backup.ts`, `old_auth_handler.js`, `stripe_test_claude.ts`, martwe
  foldery sesji `.claude/` `.codex/`, nieaktualne zrzuty ekranu.
- **Fala 2 — całe martwe pionowe wycinki (slice'y).** Frontendy bez konsumentów, alternatywne strony logowania nigdy niezamontowane, handlery
  webhooków zastąpione przez SaaS. Przetnij pasmo, pozwól Gitowi je zarchiwizować.
- **Fala 3 — nieosiągalna powierzchnia produktu.** Niezamontowane route'y, zdublowane silniki (Prisma + surowy SQL robiące to samo),
  martwe feature flagi zachowane po launchu.
- **Fala 4 — dociskanie kontraktów.** Zależności w `package.json`, features w `Cargo.toml`, extras w `pyproject.toml`, nieaktualne sekrety
  w `.env.example`, workflowy CI.
- **Fala 5 — Silencer Strip (zdejmowanie wyciszeń).** Osobna fala, bo nie chodzi o usuwanie martwego kodu — chodzi o odciszanie
  toolchaina, żeby żywy kod mógł przemówić. Patrz niżej.

### Faza 4 — Zweryfikuj rzeczywistość

Zielone statyczne bramki są konieczne, ale niewystarczające. Dodaj jedną prawdziwą ścieżkę dowodu: zbootuj aplikację, uruchom CLI, uderz w główny
route.

---

## Fala 5 — Silencer Strip (Zdejmij i słuchaj)

Zrób inwentaryzację wszystkich silencerów per język (`#[allow(`, `nosemgrep`, `eslint-disable`, `@ts-*`, `# noqa`, `# type: ignore`, `//nolint`, skip/panic teatr testów), zdejmij je wszystkie w jednym przebiegu bez wstępnej kurateli i uruchom wszystkie bramki repo. Triażuj wyniki na: naprawę przyczyny źródłowej, refaktor stylistyczny, komentarz klasy incydentu (DLACZEGO/KIEDY/GDZIE), **Raport Zapomnianych Perełek** (`dead_code` na prawdziwej zaparkowanej pracy — nigdy auto-delete) albo plan `<timestamp>_test-theater.md`. Cel: ≤25% (często ≤10%) pozostałych silencerów przy zielonych bramkach bez trików ukrywania.

Pełne komendy `rg`, bramki, tabela triażu, ścieżka raportu i lista zaskakujących findingów: [references/silencer-strip.md](references/silencer-strip.md) (oraz [references/case-studies.md](references/case-studies.md)).

## Antywzorce

Nie przycinaj liści, gdy stoi cały porzucony podsystem; nie ufaj „unused" bez sprawdzenia routera; nie zdejmuj silencerów selektywnie w Fali 5 ani nie przywracaj ich masowo; nie traktuj testów zawsze skipujących/panikujących jak bramek i nie usuwaj automatycznie `dead_code` bez sprawdzenia perełki. Pełny katalog: [references/silencer-strip.md#antywzorce](references/silencer-strip.md#antywzorce).

## Zasada prune

Żądaj od repo uzasadnienia każdej przetrwałej powierzchni, nie każdej blizny: powierzchnie poza produkcją, buildem release'u lub testami integralności wymagają jawnej decyzji **revive, archive albo delete**, tak by każdy przetrwały element miał pisemny powód. Pełna zasada: [references/silencer-strip.md#zasada-prune](references/silencer-strip.md#zasada-prune).

---

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
