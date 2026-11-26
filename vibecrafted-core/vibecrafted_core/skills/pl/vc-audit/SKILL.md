---
name: vc-audit
version: 1.0.0
description: >
  READ-ONLY falsification of a completed plan or multi-task
  implementation. Builds a per-task requirements matrix, then proves
  or refuses each claim against code + tests evidence. Default verdict
  is UNVERIFIED — PASS is earned, never assumed. Runs whenever a
  written plan claims completion, regardless of upstream — workflow,
  implement, marbles, human work, or a mix. Trigger phrases: "audit",
  "vc-audit", "task-by-task audit", "verify implementation plan",
  "spec falsification", "post-marbles audit", "did this plan actually
  land", "weryfikuj implementację", "audyt planu", "co naprawdę
  wylądowało", "falsyfikacja completion".
default: vc-audit
aliases:
  - vc-verify
compatibility:
  tools:
    - Skill
    - TaskCreate
    - TaskUpdate
    - Bash
    - Read
    - Write
requires:
  - vc-init
  - loctree
loctree_value: "primary repo map for structural/literal repository work"
aicx_value: "intent, session, and decision-context retrieval"
dogfooding: "required for repo-impacting work"
---

<!-- fleet-imperative: v3 -->

> **Wywołanie dla `vc-audit` (launcher `audit`)**
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
> | 1. Worker użytkownika | `vibecrafted audit <agent>`                                                                                                  |
> | 2. Interactive        | `/vc-audit` — wykonaj **w tej sesji**; native subagenty gdy trzeba; **nie** zewnętrzniaj tylko dlatego, że launcher istnieje |
> | 3. Agent-operator     | może odpalić formę workera powyżej przez `vc-dispatch` / linie operatora, zachowując tożsamość tego skilla                   |

> Swobodniejszy native na niektórych biegach ≠ porzucenie floty external. `vc-dispatch` i `vc-ship` zachowują własne tożsamości.

<!-- /fleet-imperative -->

# vc-audit — READ-ONLY falsyfikator plan-vs-kod

> Karta falsyfikacji. Tam, gdzie `vc-review` mówi **„findings-max na
> diffie"**, a `vc-marbles` mówi **„tynkować każdą rysę na zapas"**,
> ten mówi **„domyślnie UNVERIFIED — PASS się zarabia, nigdy nie
> zakłada, a auditor nigdy nie dotyka kodu"**.

---

## Wejście operatora

### Reguła Living Tree / Worktree

Działa w bieżącym checkoucie i na bieżącej gałęzi operatora. Nie twórz
worktree gita, nie przełączaj się na niego ani nie przenoś do niego
wykonania, chyba że operator wprost o to poprosi. Ogólne słowa w stylu
„isolate", „parallel" czy „clean branch" to za mało. Jedyny usankcjonowany drugi tryb to dispatch Fleet Worktrees (pisany plan, zacommitowane wcześniej verifiery, rozłączne domeny plików, jednowątkowy integrator — patrz Reguła Living Tree, Tryb B); poza tą formacją zostań we wspólnym drzewie. Czytaj pliki
ponownie przed oceną stanu finalnego, dostosowuj się do równoległych
zmian i zgłoś awarię podłoża (substrate failure), jeśli drzewo jest zbyt
zatrute, by bezpiecznie kontynuować.

Zobacz [Reguła Living Tree](../LIVING_TREE_RULE.md).

### Checkpoint orientacji

Zanim ten workflow wykona jakikolwiek audit, MUSI skonsumować świeże
dowody z `vc-init` dla przypisanego repo. Jeśli ich brak, najpierw
uruchom `vc-init`; traktuj audit jako zablokowany, dopóki nie ma
aktualnej prawdy repo.

`Loctree:loctree` to domyślna warstwa percepcji strukturalnej. Używaj
Loctree przed grepem / dokumentacją / twierdzeniami „pamiętam, że...",
aby zmaterializować Mapę Aplikacji Wyprowadzoną z Kodu (Code-Derived
Application Map) (repo-view, focus, slice, impact, find, follow).
Decyzje audytowe omijające Loctree w kwestiach, które Loctree obsługuje
(grafy importerów, zasięg zmiany, martwy kod, lokalizacje symboli), to
błędy procesu.

Standardowy launcher:

```bash
vibecrafted start
vc-audit claude --prompt 'Audit the 22-task plan in plans/2026Q2-loctree/'
vc-audit codex  --prompt 'Verify post-marbles surface against acceptance criteria'
vc-audit gemini --file /path/to/plan-and-target.md
```

---

## Doktryna pracy z repozytorium

W pracy z repozytorium zacznij od Loctree jako mapy: użyj `loct context`,
`loct occurrences`, `loct body` i `loct find --literal` przed szerokim ręcznym
przeszukiwaniem. Używaj AICX do kontekstu intencji i sesji. Używaj rg/grep jako
fallbacku lub lokalnej lupy, nie jako zamiennika mapowania strukturalnego. Jeśli Loctree
zawiedzie lub przeoczy jakąś powierzchnię, dopisz feedback do `~/.vibecrafted/loctree/loctree-fail.md`.

## Cel

Użyj tego skilla, gdy napisany plan, spec lub multi-task brief **deklaruje
ukończenie**. Implementacja mogła powstać z `vc-workflow`,
`vc-implement`, `vc-marbles`, z pracy człowieka lub z dowolnej kombinacji —
audit odmawia przyjmowania deklaracji ukończenia za dobrą monetę,
niezależnie od upstreamu. Odbudowuje wymagania planu atomowo, a potem
zmusza każde z nich do obrony za pomocą evidence z kodu + testów. Cokolwiek
nie potrafi się obronić, pozostaje `UNVERIFIED`.

Ten skill **nigdy nie modyfikuje kodu**. Edytowanie, refactoring,
„naprawianie przy okazji audytu" i commitowanie podczas auditu są
zabronione. Wynikiem jest matryca verdictów, raport i trace — nic więcej.

---

## Kiedy używać

Użyj `vc-audit`, gdy:

- napisany plan / spec / multi-task brief deklaruje ukończenie
- operator przekazuje katalog plików z taskami plus checkout
- `vc-marbles` skończyło rundę, a baza kodu deklaruje, że spełnia
  brief; audit sprawdza, co faktycznie wylądowało
- para PR + napisany spec wymaga falsyfikacji spec-vs-kod (nie tylko
  higieny diffa — to `vc-review`)

**Nie** używaj tego skilla, gdy:

- celem jest goły PR bez napisanego specu — to `vc-review`
- celem jest „to repo, czy kierunek jest zdrowy?" — to
  `vc-followup`
- operator chce, żeby luki zostały naprawione w trakcie passa — to
  `vc-marbles` (audit nigdy nie dotyka kodu)
- pytanie brzmi „która prawda wygrywa?" — to `vc-polarize`

---

## Pozycja w pipelinie

`vc-audit` siedzi w **slocie falsyfikacji plan-vs-kod**. Typowe
ścieżki upstream zasilające go:

```
[workflow] ┐
[implement]├──► [AUDIT: READ-ONLY] ──► next decision
[marbles]  │
[mixed]    ┘
```

Downstream zależy od verdictu:

- PASS / PASS_WITH_GAPS → `vc-polarize`, `vc-dou` lub `vc-release`
- PARTIAL / UNVERIFIED → operator decyduje: kolejna runda `vc-marbles`,
  powrót do `vc-implement` po luki albo cięcie scope'u przez `vc-polarize`
- FAIL → operator eskaluje: przepisanie specu albo przebudowa od `vc-scaffold`

Audit **nigdy** nie jest krokiem terminalnym. Wynik zawsze zasila kolejną
decyzję operatora.

---

## Postawa domyślna: falsyfikacja

Domyślny verdict dla każdego wymagania to **UNVERIFIED**; PASS wymaga dowodów z taska, kodu, testów i negative checku o sile `STRONG` lub `MEDIUM` na wszystkich kluczowych wymaganiach. Nie ufaj frontmatterowi, commit messages, AICX ani wcześniejszym raportom bez weryfikacji w kodzie. Pełne reguły nie-ufania i taksonomia dowodów w [references/falsification-rules.md](references/falsification-rules.md).

---

## Model działania

Audit przebiega w **ośmiu fazach**. Sekwencyjnych, nieopcjonalnych.
Pełny szczegół faz w [`PHASES.md`](PHASES.md).

1. **Context Receipt** — pack Loctree, dirty_worktree, hotspoty, zastrzeżenia autorytetu
2. **Task Ingestion Receipt** — full-read każdego taska; wyemituj tabelę `Tasks Loaded`
3. **Atomic Requirements Extraction** — testowalne elementy do `audit_requirements_matrix.jsonl`
4. **Positive + Negative Code Verification** — loctree-first, oba checki
5. **Adversarial Pass** — aktywnie udowodnij, że implementacja jest niekompletna (5 sub-checków)
6. **Stage-Aware Verdict** — scope wylądowany vs odroczony
7. **Per-Task Verdict Table** — jeden wiersz na task, bez zwijania w narrację
8. **Self-Attack Pass + Model Check** — atakuj verdicty PASS; wyemituj `model_confidence`

Verdicty: `PASS`, `PASS_WITH_GAPS`, `PARTIAL`, `FAIL`, `UNVERIFIED`,
`STAGE_PASS`, `STAGE_PASS_WITH_GAPS`, `STAGE_PARTIAL`,
`FULL_PLAN_INCOMPLETE_BY_DESIGN`.

Severity: P0 (sprzeczne z taskiem / psuje zależnych / narusza non-goal),
P1 (brak kluczowego kryterium), P2 (luka testowa/raportowa/procesowa), P3 (kosmetyka).

---

## Kontrakt wyjścia

`vc-audit` zapisuje trzy pliki (`audit_report.md`, `audit_requirements_matrix.jsonl`, `audit_trace.log`) z liczbami verdictów, P0–P3, top 5 ryzyk, kolejnymi 5 akcjami i `model_confidence`. Pełna lista faz trace'u i odwołanie do `DISPATCH.md` w [references/output-and-acceptance.md](references/output-and-acceptance.md).

---

## Kompozycja ze skillami sąsiednimi

`vc-audit` komponuje się z — nie zastępuje — tych:

- **`vc-init`** — wymagana bramka. Bez świeżych dowodów z init audit
  jest ślepy.
- **`vc-review`** — siostrzana rola READ-ONLY na scope diffa per
  implementacja. Używaj review do „czy ten PR wyglądał czysto?", auditu
  do „czy napisany spec faktycznie wylądował w kodzie?".
- **`vc-followup`** — siostrzana rola READ-ONLY na scope trajektorii.
  Używaj followupa do „czy kierunek jest zdrowy?", auditu do „czy spec
  został dowieziony?".
- **`vc-marbles`** — typowy upstream. Marbles tynkuje rysy na zapas;
  audit sprawdza, co przetrwało.
- **`vc-polarize`** — typowy downstream. Polarize konsumuje verdict
  auditu, by zdecydować, która prawda wygrywa.

---

## Antywzorce

Nie edytuj kodu w trakcie auditu, nie ufaj twierdzeniom bez sprawdzenia kodu i testów, nie pomijaj negative checku ani self-attacku, nie zwijaj tasków w narrację i nie omijaj Loctree przy pytaniach strukturalnych. Pełna lista antywzorców w [references/output-and-acceptance.md](references/output-and-acceptance.md).

---

## Kryteria akceptacji

Audit jest gotowy, gdy wszystkie pliki tasków mają `FULL_READ`, każde wymaganie ma positive/negative check + stopień evidence, wykonano self-attack i `model_confidence`, istnieją wszystkie trzy pliki wyjściowe, a `git diff` poza raportem jest pusty. Pełna checklista w [references/output-and-acceptance.md](references/output-and-acceptance.md).

---

## Wezwanie do działania

Przeczytaj [`PHASES.md`](PHASES.md) przed pierwszym auditem — niesie
szczegół per-faza oraz loctree-first wzorce negative-check. Przeczytaj
[`DISPATCH.md`](DISPATCH.md) przed napisaniem pierwszego ciała
operator-dispatch — niesie kanoniczny kształt promptu auditu dla 22 tasków.
Potem ustaw każde twierdzenie domyślnie na UNVERIFIED i zarabiaj każdy PASS.

---

## Klamra końcowa

```text
=======================
Pamiętaj: tryb auditu to pozwolenie, by odmówić twierdzeniu, nie
pozwolenie, by je naprawić. Czytasz spec, czytasz kod, oceniasz
evidence, zatrzymujesz się. Kolejny ruch należy do operatora.
(•̀ᴗ•́)و
=======================

Suchar: Dlaczego auditor nigdy nie mówi PASS od razu? Bo UNVERIFIED to
jedyny nastrój, który dobrze się starzeje.  (._.)
```

---

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
