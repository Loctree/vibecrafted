---
name: vc-scaffold
version: 0.2.0
description: >
  Founder-first main brainstorm + planwriting — the armored lighthouse (pancerna
  latarnia) that carries a single cut, multiple cuts, or a whole project into the
  autonomous VC-ship pipeline. The WRITE entry of the read/write cadence: produces a
  measurable, self-sufficient plan a fleet executes with the Founder absent mid-flight.
  This skill should be used when the user asks to "scaffold", "plan this", "architect
  this", "break this down", "I have an idea", "design the system", "vc-scaffold",
  "zaplanuj to", "rozrysuj architekturę", "mam pomysł".
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Wywołanie dla `vc-scaffold` (launcher `scaffold`)**
>
> Ten sam _kształt_ trzech ścieżek floty, z **literałami tego** skilla — zobacz
> kanoniczną [Matrycę Delegacji](../DELEGATION_MATRIX.md):
>
> - [Wspólne trzy ścieżki](../DELEGATION_MATRIX.md#shared-three-paths)
> - [Katalog launcherów](../DELEGATION_MATRIX.md#launcher-catalogue-core-runtime)
> - [Reguła per-launcher](../DELEGATION_MATRIX.md#per-launcher-rule-the-semantic-delta)
> - [Native vs external](../DELEGATION_MATRIX.md#native-subagents-vs-external-workers)
>
> | Ścieżka               | Literał tego skilla                                                                                                             |
> | --------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
> | 1. Worker użytkownika | `vibecrafted scaffold <agent>`                                                                                                  |
> | 2. Interactive        | `/vc-scaffold` — wykonaj **w tej sesji**; native subagenty gdy trzeba; **nie** zewnętrzniaj tylko dlatego, że launcher istnieje |
> | 3. Agent-operator     | może odpalić formę workera powyżej przez `vc-dispatch` / linie operatora, zachowując tożsamość tego skilla                      |

> Swobodniejszy native na niektórych biegach ≠ porzucenie floty external. `vc-dispatch` i `vc-ship` zachowują własne tożsamości.

<!-- /fleet-imperative -->

# vc-scaffold: Founder-First Planning — Pancerna Latarnia

## What this is

Scaffold to główna powierzchnia **brainstormu + planwritingu**: bierze mglisty pomysł i produkuje
zawężony, **mierzalny** plan budowy. Skaluje się przez jedną bramkę: **pojedyncze cięcie**, **wiele
cięć** albo **cały projekt**. To **wejście WRITE w cadence read/write VC-ship** —
plan, który emituje, musi być **samowystarczalny i falsyfikowalny**, bo w autonomicznym dostarczaniu
Founder jest nieobecny w locie i widzi tylko artefakty pośrednie. Planuj tak, jakby nikt nie miał
odpowiedzieć na pytanie po dispatchu. Front-loaduj każdą decyzję tutaj. Zobacz `references/cadence.md`.

Latarnia orientuje, zanim flota wypłynie; pancerz to weryfikacja, którą niesie każde cięcie.

## Operator Entry

Aktualne `AGENTS.md` i `docs/public/dispatch/dispatch-schema.md` mają pierwszeństwo przed historycznymi poradami przy rozbieżnościach substratu, ownership, journali lub zgód. Szanuj wybrany runtime (`local-native`, `local-worktrees`, VM); typowany dispatch daje nie-integratorom worktree `cut/<cut-id>` utworzony przez supervisora (workerzy dziedziczą, nie tworzą drugiego brancha/worktree ani nie integrują). Start przez `vibecrafted start` + `vibecrafted scaffold <agent> --prompt|--file`. Pełne reguły i przykłady: [references/phases-and-operator.md](references/phases-and-operator.md).

## Canonical Orientation Gate (HARD-BLOCK — safety-critical)

Przed jakąkolwiek analizą lub planowaniem specyficznym dla repo uruchom lub skonsumuj `vc-init` dla przypisanego repo.
**To nie jest krok poprawkowy — to bezpiecznik bezpieczeństwa (safety bezpiecznik).** W autonomicznym VC-ship agent, który
komponuje z pamięci, wstrzykuje cichy dryf, którego Founder nie wyłapie na żywo. Dlatego: **żadnego planu,
dopóki nie istnieje prawda o repo/runtime.** Brakujące evidence z `vc-init`/Loctree to porażka procesu, nie
ostrzeżenie.

`Loctree:loctree` to domyślna percepcja strukturalna. Użyj jej przed grepem lub twierdzeniami opartymi na dokumentacji,
aby wyprodukować lub odświeżyć **Mapę Aplikacji Wyprowadzoną z Kodu (Code-Derived Application Map)**:
`repo-view`, `focus`, `slice` (przed edycją), `impact` (przed usunięciem), `find` / `find --literal`
(przed utworzeniem), `follow` (dead/cycles/twins/hotspots). Znajdź nośne węzły, twins (duplikaty), martwy kod,
dryf, entrypointy runtime'u, pułapki o dużym zasięgu zmiany. Jeśli task jest jawnie non-repo/greenfield,
zadeklaruj **wyjątek no-repo** w raporcie i nazwij użyte zamiast tego źródło orientacji.

## Repository Work Doctrine

W pracy z repozytorium zacznij od Loctree jako mapy: użyj `loct context`,
`loct occurrences`, `loct body` i `loct find --literal` przed szerokim ręcznym
przeszukiwaniem. Używaj AICX do kontekstu intencji i sesji. Używaj rg/grep jako
fallbacku lub lokalnej lupy, nie jako zamiennika mapowania strukturalnego. Jeśli Loctree
zawiedzie lub przeoczy jakąś powierzchnię, dopisz feedback do `~/.vibecrafted/loctree/loctree-fail.md`.

## Founder Interview Gate (HARD-BLOCK)

Przed Shape zapisz we frontmatterze i Orient jeden dowód: (1) istniejące źródło wywiadu (journal, sesja/ekstrakt AICX lub brief foundera z ścieżką/session ID + odzyskanymi decyzjami) albo (2) odpowiedzi foundera z bieżącej rozmowy. W przeciwnym razie najpierw zapytaj o brakujące decyzje produktowe — bez samowyłączeń. Pełna bramka: [references/phases-and-operator.md](references/phases-and-operator.md).

## Pipeline Position

`[SCAFFOLD] → init → implement → review → workflow → followup → marbles → audit → polarize → dou → hydrate → release`
Scaffold to wejście WRITE (`references/cadence.md`). Jasne, ograniczone zadania startują od `vc-init`; `vc-ship` jest normalną klamrą lifecycle, a ograniczony dispatch przez `vc-dispatch` zarządzony przez Foundera jest wspierany, gdy DRIVER zachowuje wszystkie bramki artefaktów/manifestu/briefów. Szczegóły: [references/phases-and-operator.md](references/phases-and-operator.md).

## The Six Phases

Uruchamiaj po kolei; każda faza karmi następną. Szczegóły faz i egzekwowania: [references/phases-and-operator.md](references/phases-and-operator.md) oraz [references/artifacts-and-gates.md](references/artifacts-and-gates.md):

1. **Orient:** przejdź bramkę orientacji, zmapuj węzły/twins/cykle przez Loctree, uchwyć ograniczenia tech/zespołu/czasu/scope'u.
2. **Falsify:** spróbuj złamać założenie fundujące przed kształtowaniem; każde „to działa” musi przetrwać realną sondę.
3. **Shape:** wybierz 3–5 granic architektonicznych, bezwzględny scope in/out, tożsamość produktu i kształt wyjścia ([references/output-shapes.md](references/output-shapes.md)).
4. **Defend:** rozbij na cięcia 30–120 min z `Vector`, 4-członową deltą, `state` i niefałszowalnym `delivery-verifier` ([references/measure-core.md](references/measure-core.md)).
5. **Brief every cut (HARD-GATE):** wyprodukuj master plan ([references/plan-template.md](references/plan-template.md)) ORAZ wyrenderuj każdy `briefs/<wave>-<slot>_<slug>.md` z 12 sekcjami (`references/output-shapes.md`). Brak briefu = brak cięcia; zakazane wymówki o „małym cięciu”.
   - **5.5 `DRIVER.md` (HARD-GATE):** samowystarczalne przekazanie Foundera z (1) pełnymi ścieżkami absolutnymi, (2) grafem zależności z `why` + `⛔ Founder-button STOP`, (3) `scaffold-doctor` + jedną walidacją `<plan-id>.dispatch.toml` + drogą `/vc-ship` (lub ograniczonym `vibecrafted dispatch`), (4) regułą `[ ]→[x]` verbatim, (5) snapshotem statusu + `dou-index`, (6) matrycą R12 `## Odbiór (matryca wyników)` (wszystko `[ ]`; `Founder [x]` tylko z `acceptance/founder.json`).
   - **5.6 `manifest.json` (HARD-GATE):** obowiązkowy inwentarz schema `"1"` pod `${VIBECRAFTED_HOME:-$HOME/.vibecrafted}/artifacts/<org>/<repo>/<YYYY_MMDD>/plans/<plan_id>/`; zarejestruj każdy artefakt; bez lustra `operator/` ani aliasów.
   - **5.7 Frontmatter YAML (HARD-GATE):** każdy artefakt markdown zaczyna się frontmatterem YAML (`plan_id`, `run_id`, `session_id`, `role`, `author`, opcjonalny `agent`, `date`, `project`). Nigdy nie wyprowadzaj wykonawcy z `author`.
   - **5.8 `<plan-id>.dispatch.toml` (HARD-GATE):** kontrakt `vibecrafted.dispatch.v1` pokrywający każde cięcie dokładnie raz; udowodnij przez `--doctor` i `--dry-run --json`; zachowaj piny modeli i headless workerów.
   - **Compile-embargo plans:** stosuj [references/compile-embargo.md](references/compile-embargo.md); `--no-verify` dotyczy wyłącznie lokalnych checkpointów workera (nigdy push), z admission strukturalnym integratora i późniejszym domknięciem pełnych bramek.
6. **Serve & review:** zaserwuj wielozakładkowe edytowalne artefakty przez `vibecrafted-server`, potem przejdź `vibecrafted scaffold-doctor --plan <root> --repo <git-root>` (REFUSE = brak handoffu).

## Measurement (the armor)

Każda jednostka planu jest adresowalna przez twierdzenie/wynik. **Tylko verifier przerzuca `[~]→[x]`; twierdzenie nigdy
samo nie dochodzi do `[x]`** — ten inwariant czyni plan mierzalnym zamiast optymistycznym.
`dou-index = |[x]| / total`; `delta = {[ ],[~],[?],[!]}`; trigger/stop czyta kolumnę `state`
(`[!]`/`[?]` → STOP → recovery-vector; pełna fala `[x]` → TRIGGER następną). **STOP to nigdy nie kapitulacja —
to wyzwala recovery-vector** (fallback/failover/handsoff). Pełen alfabet + markery:
`references/measure-core.md`.

## Critical Rules, Emil Closing & Prompt Verification

- **Twarde bramki:** research-first (`vc-init` + Loctree), wywiad/AICX foundera, brief na każde cięcie, `DRIVER.md`, `manifest.json`, `.dispatch.toml` (`vibecrafted.dispatch.v1`), `scaffold-doctor` i zamknięcie R12 trzema podpisami (`Founder [x]` tylko z `acceptance/founder.json`).
- **Higiena zapisu:** trwałe artefakty NIGDY nie trafiają do `/tmp` ani do checkoutu produktu — wyłącznie do `~/.vibecrafted/artifacts/<org>/<repo>/<DATE>/plans/<plan_id>/`. Jedynym journalem Operatora jest ignored `.vibecrafted/THE_JOURNAL.md`.
- **Zamknięcie Emila i weryfikacja:** każdy master plan, DRIVER i brief kończy unikalna linia motywacyjna, konkretne CTA i suchar z kaomoji ([klamra Emila](../vc-operator/DISPATCH.md#closing-rail--the-emil-default-block)). Przenoś [Verification Rule](../VERIFICATION_RULE.md) do promptów; zmiany skillów regenerują `SKILL_PROVENANCE.json` (`make skills-check UPDATE=1`).

Pełne reguły, zamknięcie Emila, powiązania, antywzorce i weryfikacja promptu: [references/rules-and-closing.md](references/rules-and-closing.md).

## Additional Resources

- **`references/measure-core.md`** · **`references/cadence.md`** · **`references/output-shapes.md`** · **`references/plan-template.md`** · **`references/compile-embargo.md`**
- **`references/phases-and-operator.md`** · **`references/artifacts-and-gates.md`** · **`references/rules-and-closing.md`**

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
