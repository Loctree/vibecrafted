# vc-scaffold — Wejście operatora, pozycja w pipeline i fazy 1–5

## Operator Entry

Aktualne `AGENTS.md` i `docs/public/dispatch/dispatch-schema.md` mają pierwszeństwo
przed historycznymi poradami, gdy rozchodzą się substrat, ownership, journale lub
semantyka zgód.

### Living Tree / Worktree Rule

Używaj runtime'u wybranego przez Foundera, plan lub launcher: Living Tree /
`local-native`, Fleet Worktrees / `local-worktrees`, Fleet VM local lub Fleet VM
cloud. Pojedyncza interaktywna linia domyślnie używa bieżącego Living Tree, gdy
nie wybrano innego substratu. Ogólne słowa „isolate” czy „parallel” nie upoważniają
do przeniesienia pracy. Typowany dispatch przydziela każdemu nie-integratorowi
worktree utworzony przez supervisora na `cut/<cut-id>` z rozwiązanego baseline'u;
workerzy go dziedziczą, nigdy nie tworzą drugiej gałęzi/worktree ani nie integrują
siebie. Zapisz parent/effective roots, baseline i terminal SHA, artefakty oraz
integration disposition. Czytaj ponownie przed edycją, stage'uj tylko własne
ścieżki/hunki, zachowaj cudzą pracę i zgłoś nierozwiązywalny overlap.

Zobacz [Living Tree Rule](../../LIVING_TREE_RULE.md).

### Dispatch

Wejdź w sesję frameworka, a potem odpalaj przez command deck (nie surowe `skills/.../*.sh`):

```bash
vibecrafted start            # or: vc-start
vibecrafted scaffold claude --prompt 'Design the payment system'
vc-scaffold agy --prompt 'Plan migration from NextAuth to custom auth'
vibecrafted scaffold codex --file /path/to/idea-brief.md
```

Preferuj `--file` dla istniejącego planu/artefaktu i `--prompt` dla intencji inline.

---

## Pipeline Position

```
[SCAFFOLD] → init → implement → review → workflow → followup → marbles → audit → polarize → dou → hydrate → release
^^^^^^^^^^   WRITE entry of the read/write cadence (WRITE produces an artifact, READ falsifies it)
```

Scaffold to wejście WRITE. Jeśli task jest już jasny i bounded, pomiń scaffold i zacznij od
`vc-init`. Pełen cadence oraz klasyfikacja WRITE/READ żyją w `references/cadence.md`.

`vc-ship` pozostaje normalną klamrą lifecycle. **Ograniczony dispatch zarządzony
przez Foundera** dla już ukształtowanej naprawy jest wspieraną ścieżką przez
`vc-dispatch`; nie wymaga wszystkich etapów lifecycle ani wcześniejszej awarii.
Zachowaj aktualną orientację, pełne briefy, piny modeli, doctor/dry-run,
zadeklarowane verifiery i prawdziwe receipty. Gdy ograniczony dispatch konsumuje
pakiet scaffolda, wszystkie wymagania artefaktów/manifestu/DRIVER-a/briefów nadal
obowiązują; wybrana droga wykonania musi być jawna w DRIVER.

---

## Sześć faz (1–5 szczegółowo)

### 1. Orient (research-first)

Przejdź Checkpoint orientacji. Zmapuj istniejący krajobraz: `repo-view` dla rozmiaru/zdrowia,
`focus` na podejrzanych modułach, `slice` na krytycznych plikach, `tree` dla hotspotów, `follow` dla dead/cycles.
Uchwyć **przestrzeń ograniczeń** — tech (stack/wersje/infra), zespół (kto buduje, w jakich językach),
biznes (budżet czasu, deadline), scope (MVP vs pełna wizja). Ograniczenia kształtują wszystko.

### 2. Falsify (adversarial premise check)

Zanim zwiążesz się z kształtem, spróbuj **złamać** założenie fundujące. Spytaj „skąd bym wiedział, że to
kłamstwo?". Lekcja z 0-bajtów-przechodzi-exit-0: każde „to działa" musi przetrwać realną sondę, nigdy
samego zielonego ptaszka. Wyciągnij na wierzch tryby porażki, przed którymi plan musi się bronić.

### 3. Shape (scale-adaptive)

Zdecyduj o architekturze przez **granice i decyzje** (3-5 tych, które się liczą, nie tysiąc szczegółów), ustaw
**scope** (in / out / explicitly out — bądź bezwzględny) i zdefiniuj **tożsamość produktu** (metafora
materiałowa, role kolorów, typografia, ton, dark/light) — tożsamość to decyzja architektoniczna, która
karmi później DoU i Decorate. Potem wybierz **kształt wyjścia wg skali**: brief pojedynczego cięcia · wave-atlas+tracker · pipeline read/write projektu. Zobacz `references/output-shapes.md`.

### 4. Defend (gates first-class)

Rozbij pracę na cięcia rozmiaru agenta (30-120 min). **Każde cięcie niesie measure-core**: `Vector`
(stabilize/implement/recon/e2e), czteroczłonową deltę (`intent | baseline | claim | delivery`), marker
`state` `[ ] [~] [?] [!] [x]` oraz **delivery-verifier** — niefałszowalny test, który przerzuca
`[~]→[x]`. Cięcie bez verifiera dowozi się jako `[?]`, nigdy `[x]`. Zobacz `references/measure-core.md`.

### 5. Brief every cut (HARD-GATE — this is the delivery mechanism)

Wyprodukuj plan z `references/plan-template.md` (master-dispatch: wave atlas + graf
zależności + kolumna `state`). **Potem — bez negocjacji — wyrenderuj brief dla KAŻDEGO
cięcia.** Cięcie bez wyrenderowanego, poprawnego briefu nie istnieje z punktu widzenia
planu. Ta zasada zamienia plan z wydmuszki w coś, co flota może wykonać.

Dla każdego cięcia napisz `briefs/<wave>-<slot>_<slug>.md` z 12-sekcyjnego szablonu dispatchu
(`references/output-shapes.md`): mission · context · files · acceptance · gates · out-of-scope ·
etykieta Living Tree (verbatim) · Loctree-first · podpowiedź recovery · branch+commit · ścieżka raportu.

**Egzekwowanie (przeniesione z `/brainstorming`, flow, który prowadzi agenta za rękę):**

- **Checklist→TODOs:** utwórz jeden element TodoWrite na każdy brief cięcia; domykaj je po kolei. Scaffold
  nie jest „gotowy", dopóki jakikolwiek todo briefu cięcia jest otwarty.
- **Hard-gate:** NIE przekazuj do `vc-operator`, nie dispatchuj ani nie ogłaszaj scaffoldu za ukończony, dopóki
  KAŻDE cięcie w wave atlasie nie ma pasującego briefu z wszystkimi 12 sekcjami obecnymi.
- **Loop do zielonego:** brakujący lub źle sformułowany brief → wróć i wyrenderuj go. Jeden stan terminalny:
  wszystkie briefy wyrenderowane ORAZ bramka scaffold-doctor przechodzi.
- **Wyprzedzanie antywzorca (ZAKAZANE racjonalizacje):** „to cięcie jest za małe, żeby potrzebowało
  briefu", „jesteśmy 1:1, więc briefy zbędne", „tabela master-dispatch wystarczy". Plan bez
  briefów per cięcie to wydmuszka, nie plan. Bez wyjątków, niezależnie od postrzeganej prostoty.

---

## Founder Interview Gate (HARD-BLOCK)

Scaffold jest founder-first, więc nie może wymyślać intencji foundera. Przed Shape zapisz we
frontmatterze planu i sekcji Orient jeden z dwóch rodzajów dowodu:

1. konkretne istniejące źródło wywiadu (journal operatora, sesja/ekstrakt AICX albo brief foundera),
   wraz ze ścieżką/session ID i decyzjami naprawdę z niego odzyskanymi; albo
2. odpowiedzi foundera zebrane w bieżącej rozmowie.

Jeśli nie istnieje żaden z nich, zadaj founderowi brakujące pytania produktowe przed napisaniem
planu architektury. „Wywiad nie był potrzebny", „task był jasny" i „niezapytanie nie zaszkodziło"
to zakazane samowyłączenia. Ta bramka jest intake'em discovery; nie legalizuje dwudziestu pytań
w środku scaffoldu, gdy decyzje są już uchwycone.
