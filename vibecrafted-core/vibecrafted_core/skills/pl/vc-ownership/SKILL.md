---
name: vc-ownership
version: 1.1.0
description: >
  Full-spectrum Vetcoders ownership mode for moments when the user wants Agent
  to take the wheel and drive a product from A to Z: architecture, coding,
  runtime debugging, UI polish, packaging, docs, testing, local tooling,
  agent orchestration, and wow-effect finish. Use whenever the user says things
  like "take ownership", "you drive", "od a do z", "zrob to cale", "dowiez
  to", "wow effect", "superprodukcyjny", "manufakturer produktowy", or when
  the team clearly wants decisive end-to-end execution with minimal back-and-forth.
  This skill is intentionally pushy: if the user is asking for total delivery,
  use it even when they do not explicitly name the skill.
compatibility:
  tools:
    - exec_command
    - apply_patch
    - update_plan
    - multi_tool_use.parallel
    - search_tool_bm25
    - web.run
    - js_repl
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Wywołanie dla `vc-ownership` (launcher `ownership`)**
>
> Ten sam _kształt_ trzech ścieżek floty, z **literałami tego** skilla — zobacz
> kanoniczną [Matrycę Delegacji](../DELEGATION_MATRIX.md):
>
> - [Wspólne trzy ścieżki](../DELEGATION_MATRIX.md#wspólne-trzy-ścieżki)
> - [Katalog launcherów](../DELEGATION_MATRIX.md#katalog-launcherów-core-runtime)
> - [Reguła per-launcher](../DELEGATION_MATRIX.md#reguła-per-launcher-delta-semantyczna)
> - [Native vs external](../DELEGATION_MATRIX.md#natywne-subagenty-vs-zewnętrzni-workerzy)
>
> | Ścieżka               | Literał tego skilla                                                                                                              |
> | --------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
> | 1. Worker użytkownika | `vibecrafted ownership <agent>`                                                                                                  |
> | 2. Interactive        | `/vc-ownership` — wykonaj **w tej sesji**; native subagenty gdy trzeba; **nie** zewnętrzniaj tylko dlatego, że launcher istnieje |
> | 3. Agent-operator     | może odpalić formę workera powyżej przez `vc-dispatch` / linie operatora, zachowując tożsamość tego skilla                       |

> Swobodniejszy native na niektórych biegach ≠ porzucenie floty external. `vc-dispatch` i `vc-ship` zachowują własne tożsamości.

<!-- /fleet-imperative -->

# vc-ownership

> Postawa autonomicznego dostarczania. Bierz odpowiedzialność end-to-end, doprowadź
> do zielonego, a potem udowodnij, że powierzchnia produktu nie jest nadal niedokończona.

## Taksonomia

```yaml
vc-ownership:
  kind: autonomous_posture
  scope: interactive_or_headless_session
  meaning: take responsibility end-to-end, minimize questions, drive to green
  autonomy: full
```

Wywołanie skilla to nie wywołanie runtime'u. Jeśli operator powie
`$vc-ownership` w bieżącej rozmowie, bieżący agent przyjmuje postawę
autonomicznego dostarczania. Oddzielny run runtime'u istnieje tylko wtedy, gdy
operator lub framework uruchomi `vibecrafted ownership <agent> ...`.

Zobacz [TAXONOMY.md](TAXONOMY.md) po podział na postawę/runtime.

## Reguła Living Tree / Worktree

Ten workflow działa w bieżącym checkoucie i na bieżącej gałęzi operatora. Nie twórz worktree gita, nie przełączaj się na niego ani nie przenoś do niego
wykonania, chyba że operator wprost poprosi o worktree w tym prompcie. Ogólne słowa w stylu „isolate", „
parallel" czy „clean branch" to za mało. Jedyny usankcjonowany drugi tryb to dispatch Fleet Worktrees (pisany plan, zacommitowane wcześniej verifiery, rozłączne domeny plików, jednowątkowy integrator — patrz Reguła Living Tree, Tryb B); poza tą formacją zostań we wspólnym drzewie. Czytaj pliki ponownie przed edycją, dostosowuj się do równoległych zmian i zgłoś
awarię podłoża (substrate failure), jeśli bieżące drzewo jest zbyt zatrute, by bezpiecznie kontynuować.

Zobacz [Reguła Living Tree](../LIVING_TREE_RULE.md).

## Checkpoint orientacji

Zanim ten workflow wykona analizę specyficzną dla repo, planowanie, implementację, review, release lub delegację, MUSI
uruchomić lub skonsumować procedurę `vc-init` dla przydzielonego repo. Jeśli brakuje świeżego evidence z `vc-init`, wykonaj najpierw
przebieg init i traktuj pracę specyficzną dla workflow jako zablokowaną, dopóki nie ma aktualnej prawdy repo.

`Loctree:loctree` to domyślny skill do mapowania struktury repo dla tego przebiegu. Użyj Loctree przed grepem lub
twierdzeniami opartymi na dokumentacji, aby wyprodukować lub odświeżyć Mapę Aplikacji Wyprowadzoną z Kodu (Code-Derived Application Map): repo-view, focus, slice, impact, find i follow w
odpowiednim zakresie. Szukaj istniejących symboli i kontraktów, zanim utworzysz nowe; uruchom impact przed usunięciem lub dużym
refactorem; uruchom slice przed edycją.

Chodzi o znalezienie zaczepów: węzłów nośnych, twins (duplikaty), martwego kodu, dryfu, entrypointów runtime'u oraz pułapek o dużym zasięgu zmiany.
Jeśli task jest jawnie nie-repo lub no-code, zadeklaruj w raporcie wyjątek no-repo. W przeciwnym razie brak evidence z `vc-init`
/Loctree to awaria procesu.

## Doktryna pracy z repozytorium

W pracy z repozytorium zacznij od Loctree jako mapy: użyj `loct context`,
`loct occurrences`, `loct body` i `loct find --literal` przed szerokim ręcznym
przeszukiwaniem. Używaj AICX do kontekstu intencji i sesji. Używaj rg/grep jako
fallbacku lub lokalnej lupy, nie jako zamiennika mapowania strukturalnego. Jeśli Loctree
zawiedzie lub przeoczy jakąś powierzchnię, dopisz feedback do `~/.vibecrafted/loctree/loctree-fail.md`.

## Cel

Użyj tego skilla, gdy użytkownik nie prosi o wąski patch.
Wręcza nam mandat.

To tryb dla:

- kształtowania produktu full-stack
- wykonania end-to-end przez zdispatchowane [vc-agents](../vc-agents/SKILL.md)
- zdecydowanych wyborów inżynierskich bez jawnej pisemnej zgody
- product polish i wow effect
- [loop](.) redukującego opór i pytania uzupełniające
- domykania rzeczy, nie tylko edytowania kodu

Kontrakt jest prosty:

- użytkownik wyznacza kierunek i ograniczenia
- my bierzemy ownership operacyjny
- decydujemy, implementujemy, weryfikujemy i pakujemy
- pauzujemy tylko wtedy, gdy konsekwencje są nieoczywiste lub nieodwracalne

## Główna obietnica

W trybie ownership zachowuj się jak budowniczy produktu z dostępem do całej
maszyny.

To obejmuje, gdy uzasadnia to task i jest dostępne w środowisku:

- edytowanie kodu i testów
- przekształcanie architektury
- tworzenie dokumentacji i powierzchni do pakowania
- poprawianie UX i jakości wizualnej
- uruchamianie lokalnych serwerów i smoke testów
- sterowanie interakcjami z przeglądarką lub desktopem przez dostępne narzędzia
- orkiestrację floty zewnętrznych agentów przez `vc-agents`
  w sesjach interaktywnych jako domyślny silnik postępu
- orkiestrację natywnych workerów przez ruleset `vc-delegate`
  w odłączonych sesjach nieinteraktywnych — wysoce zalecane
- zbieżność przez `vc-marbles`

Celem jest nie tylko poprawność.
Celem jest mocna, wykończona powierzchnia.

Ownership to nie cicha delegacja. Oznacza, że agent będący właścicielem odpowiada
za wynik produktowy; delegacja to oddzielny wybór taktyczny.

## Kiedy używać

Użyj `vc-ownership`, gdy użytkownik sygnalizuje coś w stylu:

- „take ownership"
- „you drive"
- „od a do z"
- „dowiez to cale"
- „zrob to jak trzeba"
- „wow effect"
- „superprodukcyjny"
- „don't ask, just ship"
- „ogarnij wszystko"
- „make it feel finished"

Użyj go też, gdy żądanie jawnie obejmuje wiele warstw naraz:

- repo + runtime + UI
- backend + desktop + flowy przeglądarkowe
- feature + dokumentacja + pakowanie
- powłoka produktu + workflow agentów + powierzchnia testowa

### Odniesienie krzyżowe: kiedy ownership staje się multi-dispatchem

`vc-ownership` to autonomiczne dostarczanie w sesji interaktywnej lub headless.
Może być solo-thread albo używać bounded supportu, ale jest właścicielem jednego product slice'a
aż do zweryfikowanego handoffu. Gdy task urośnie w łańcuch wielopromptowy obejmujący
wielu agentów (fala A → B → C → D, rotacja AGENT FAIRNESS,
dispatch naprawczy, await-via-notify), karta przesuwa się do
`vc-operator` w sesjach interaktywnych.

Sygnały, że praca przerosła ownership i domaga się trybu operator:

- operator wręcza ci master dispatch plan (10+ ciał promptów)
- praca obejmuje 4+ gałęzie, które wymagają koordynacji merge'a w kształcie fal
- odpalałbyś 3+ agentów peer-tier i syntetyzował ich raporty
- operator mówi _„orchestrate the rest"_, _„prowadź fleet"_,
  _„dirygentura"_

Gdy przesunięcie nastąpi, załaduj [`../vc-operator/SKILL.md`](../vc-operator/SKILL.md)
**obok** tego (ownership nie znika — każdy zdispatchowany
worker jest w trybie ownership dla _swojego_ slice'a; ty jesteś w trybie
operator dla _łańcucha_). Zobacz [`../vc-operator/FRAME.md`](../vc-operator/FRAME.md)
po szablon deklaracji przesunięcia framingu — nazwij przejście
jawnie, zanim cokolwiek odpalisz.

## Domyślne zachowanie

Zacznij od szybkiego framingu, sprawdź ostatnie sesje i `loctree context --full`, decyduj autonomicznie, używaj agentów do równoległej pracy, domykaj zapis przez read-only review/followup/audit/DoU i używaj `cron` do heartbeatów bez nadzoru. Pytaj o wyrównanie tylko przed ruchami z ukrytym zasięgiem zmiany.

Pełna 10-punktowa lista domyślnego zachowania: [references/default-behavior.md](references/default-behavior.md).

## Granice ownershipu i model operacyjny

Ruszaj natychmiast z edycją kodu, testami, docs, UX, lokalnymi smoke testami, swarmami agentów i zawężonymi commitami; pauzuj przed destrukcyjnym gitem, utratą danych, zewnętrznymi wiadomościami/kosztami, zmianami security/billingu lub nieautoryzowanym push/merge/deploy/publish. Wykonuj 6-fazową pętlę (Zgłoś cel -> Wybierz kształt -> Prawda runtime'u -> Cały product slice -> Weryfikuj jak kupujący -> Rytm read-only `vc-review -> vc-followup -> vc-audit -> vc-dou` przed `done`).

Pełne granice działań i Fazy 1–6: [references/boundaries-and-operating-model.md](references/boundaries-and-operating-model.md).

## Sterowanie desktopem, polityka agentów, wyjście i przykłady

Gdy narzędzia pozwalają, weryfikuj realne flowy przez automatyzację app/browser-native, deterministyczne lokalne narzędzia lub w ostateczności klikanie systemowe. Deleguj z zachowaniem strategii i syntezy w głównym wątku, raportuj wg Stan obecny / Propozycja / Wykonanie / Otwarte ryzyka / Następny ruch i unikaj placeholderów oraz przedwczesnego `done`.

Pełne zasady sterowania desktopem, polityki agentów, stylu wyjścia, antywzorców i przykładów: [references/execution-policy-and-examples.md](references/execution-policy-and-examples.md).

## Końcowe przypomnienie

Tryb ownership to nie pozwolenie na lekkomyślność.
To pozwolenie na usuwanie tarcia.

Przejmij ster.
Zadbaj o bezpieczeństwo użytkownika.
Domknij cały slice.
Uszanuj nieobecność użytkownika i posuwaj się naprzód.
