# vc-scaffold — Artefakty, twarde bramki i serve/doctor

### 5.5 DRIVER.md (HARD-GATE — the Founder's hand-off driver)

Obok briefów wyrenderuj **jeden `DRIVER.md`** współlokowany z `briefs/`. To jeden
samowystarczalny artefakt, z którego Founder (albo zimna flota) prowadzi cały plan, **gdy
pętla w wątku umiera**. NIE opcjonalny, NIE re-skin atlasu — to wykonywalne przekazanie.
MUSI zawierać wszystkie sześć:

1. **Pełne ścieżki absolutne** — każdy artefakt planu, brief, evidence z orient oraz input/fixture, jako
   gotowe-do-wklejenia ścieżki absolutne.
2. **Graf zależności Z `why` na każdej krawędzi** — co-po-czym ORAZ dlaczego:
   dlaczego każde cięcie poprzedza następne; dlaczego para jest **SEQUENCE**
   (wspólna domena plików → konflikt Living Tree) zamiast **PARALLEL** (rozłączne
   domeny → bezpieczna współbieżność); i gdzie siedzi każdy **⛔ Founder-button STOP**
   (trunk merge, force-push, PR merge/close, kasowanie tagów/gałęzi, deploy, decyzje
   produktowe lub specyficzna dla fali granica push/install). Graf bez `why` to
   diagram, nie driver.
3. **Gotowe przekazanie** — najpierw `vibecrafted scaffold-doctor --plan <root> --repo <git-root>`
   (REFUSE = brak handoffu), potem dokładnie jeden blok walidacji poziomu planu
   kanonicznego `<plan-id>.dispatch.toml` (`vibecrafted dispatch … --doctor` +
   dry-run), następnie przekazanie A→Z do `/vc-ship` albo jawna ograniczona droga
   `vibecrafted dispatch <plan>` zarządzona przez Foundera. Wybrany supervisor
   posiada start i resume; DAG kolejność i dozwoloną równoległość. Nie zamieniaj
   DRIVER-a w listę launcherów per cięcie i nie ucz ręcznego sekwencjonowania
   `vibecrafted workflow ... --prompt`.

4. **Alfabet stanów + reguła `[ ]→[x]`, odtworzone verbatim** (lustro Pomiaru):
   `[ ]` todo · `[~]` running · `[?]` done-unverified · `[!]` blocked · `[x]` verifier-green.
   **Tylko delivery-verifier przerzuca `[~]→[x]`; twierdzenie agenta NIGDY samo nie dochodzi do `[x]`.**
   Reguła żyje W DRIVER-ze celowo — po to, żeby w trakcie dispatchu nikt nie promował twierdzenia do done
   bez ponownego uruchomienia verifiera. Ta promocja-bez-dowodu to jedyny tryb porażki, który
   wykłada przebieg operatora („rozjedziemy się"). Zakoduj to tam, gdzie są oczy dispatchera.
5. **Snapshot statusu na żywo** + `dou-index = |[x]| / total`.
6. **Matryca odbioru (Odbiór) — R12, Founder 2026-09-15.** Sekcja
   `## Odbiór (matryca wyników)` z jednym wierszem na cięcie
   (`cut | commit | dowód (Operator) | Worker | Operator | Founder`) i linią podpisów
   **`Zatwierdzono przez: Worker [ ] Operator [ ] Founder [ ]`**. Każde pole startuje jako `[ ]` —
   nietknięte `[ ]` to wskaźnik NIEDOWIEZIENIA, nie usterka formatowania. Worker przerzuca własne
   pola w ramach dostawy (supervisor odmawia weryfikacji cięcia z nieprzerzuconymi polami
   Acceptance); przerzucenie to twierdzenie, nigdy dowód — decydują verifiery. Operator przerzuca
   dopiero po własnym uruchomieniu verifierów. **`Founder [x]` może istnieć wyłącznie obok
   `acceptance/founder.json` w root planu; agent nigdy nie podpisuje za Foundera** —
   scaffold-doctor R12 odrzuca plan ze sfałszowanym podpisem Foundera albo bez matrycy.

### 5.6 manifest.json (HARD-GATE — canonical artifact inventory)

Utwórz jeden root planu pod
`${VIBECRAFTED_HOME:-$HOME/.vibecrafted}/artifacts/<org>/<repo>/<YYYY_MMDD>/plans/<plan_id>/` i zapisz w nim obowiązkowy
`manifest.json`. Schema version `"1"` deklaruje `plan_id`, `org`, `repo`, `day` i uporządkowaną
tablicę `artifacts`. Każdy wpis artefaktu deklaruje stabilne `id`, jawną `role`, względną `path`,
`editable` i `required`; opcjonalne `dependencies` zawierają ID artefaktów. Obsługiwane role:
`driver`, `wave-atlas`, `dispatch`, `brief`, `design-doc`, `traceability`, `tracker`, `falsification`, `report`,
`other`. Zarejestruj każdy wygenerowany artefakt przed przekazaniem. Nazwy plików nigdy nie wyznaczają
roli. Nie twórz lustra `operator/`, kopii kompatybilności, aliasu nazwy ani symlinka.

### 5.7 YAML frontmatter on EVERY artifact (HARD-GATE — no bare markdown)

Każdy markdownowy artefakt produkowany przez ten skill — MISSION, ATLAS, DRIVER, tracker,
falsyfikacja, każdy brief i każdy design doc — zaczyna się frontmatterem YAML, bez wyjątków:

```yaml
---
plan_id: <plan_id>
run_id: <scaffold run id, when running under a lifecycle>
session_id: <agent session_id from `aicx sessions current` or raw `.jsonl` filename read>
role: driver | wave-atlas | brief | tracker | falsification | design-doc | mission | other
author: <autor artefaktu>
agent: <agent/provider wykonawczy, jeśli przypisany>
date: YYYY-MM-DD
project: <org>/<repo>
---
```

`author` zapisuje autora artefaktu; nigdy nie wybiera wykonawcy. W wykonywalnym
briefie `agent` przypisuje docelowego agenta/providera wykonawczego, który może
być inny niż autor. Pole można pominąć, gdy wykonawcę określa launcher lub
typowany plan dispatch. Przy ponownym użyciu briefu z `agent` upewnij się, że
przypisanie odpowiada wybranemu wykonawcy: konflikt jest odrzucany. Nigdy nie
wyprowadzaj wykonawcy z `author`.

To hard-gate, nie dekoracja: reguła 6 kontraktu settlementu („bez gołego
markdownu — artefakt bez run_id trafia do needs-attention”), retrieval (wyszukiwarki
rankingują i ograniczają zakres przez te pola) oraz proweniencja (luźny artefakt
na dysku musi identyfikować plan i autora bez archeologii). Pakiet planu z gołym
markdownem nie przechodzi review tak samo jak brakujący brief. Raport z pola
odnotował to 2026-07-23 po otrzymaniu pakietu z frontmatterem tylko na części
plików — mieszanka jest gorsza od braku, bo uczy czytelników przestać sprawdzać.

### 5.8 `<plan-id>.dispatch.toml` (HARD-GATE — supervisor-readable execution contract)

Każdy scaffold, także jednocięciowy, kończy się `<plan-id>.dispatch.toml` ze schematem
`vibecrafted.dispatch.v1`. Koduje pełny zbiór cięć, nazwane fazy, krawędzie `depends_on`, jawnie
dozwoloną równoległość, tożsamość agenta i workflow oraz piny modeli, ścieżki briefów per cięcie, politykę commitów
oraz delivery-verifiery. Zarejestruj go w `manifest.json` z rolą `dispatch`. ID cięć i ścieżki
briefów MUSZĄ pokrywać każde wykonywalne cięcie atlasu dokładnie raz; drugi scheduler jest zakazany.
Udowodnij artefakt przed przekazaniem:

```bash
vibecrafted dispatch <absolute-plan-root>/<plan-id>.dispatch.toml --doctor
vibecrafted dispatch <absolute-plan-root>/<plan-id>.dispatch.toml --dry-run --json
```

Po walidacji przekaż dokładnie ten artefakt do `/vc-ship` dla normalnego lifecycle
A→Z. Przy jawnym ograniczonym dispatchu zarządzonym przez Foundera DRIVER może
zamiast tego wskazać `vibecrafted dispatch <plan.dispatch.toml>` i komendę resume.
To wspierana ścieżka ukształtowanej fali, nie drugi scheduler. Zachowaj piny modeli
Foundera dosłownie, domyślnie headless workerów i uzbrojony supervisor-side
`vibecrafted await <agent> --run-id <id>`. Workerzy kończą bramki na pierwszym
planie, raport i commit w bieżącej turze; zakończenia w tle nie mogą ich wybudzić.
Pola acceptance workera nigdy nie podpisują za Operatora/Foundera.

Nie wymagaj, aby Founder ręcznie pisał TOML albo wklejał komendę
`vibecrafted workflow <agent> --prompt ...` na każde zadanie. Ręczne launchery
per cięcie nie należą do **Running This Plan** ani normalnej drogi DRIVER-a.
Poza wspieraną ograniczoną ścieżką poziomu planu notatka awaryjna może użyć launchu
per cięcie dopiero po nazwaniu awarii `/vc-ship`/supervisora i powodu niedostępności
normalnej drogi; musi zapisać evidence powrotu kontroli i nie może tworzyć
równoległego systemu wykonania.

### Compile-embargo plans

Jeśli plan odracza bramki compile/test podczas kształtowania architektury, stosuj fazowo-świadomy
kontrakt recovery z `references/compile-embargo.md`. Gdy Founder autoryzuje fazę embarga,
`--no-verify` jest w pełni autoryzowany dla każdego lokalnego checkpointu workera w tej fazie.
Obejmuje całe wejście bundlowanych hooków Gita, więc worker raportuje, co uruchomiono, a co
pominięto; nie jest to claim dostarczenia zweryfikowanego przez bezpieczeństwo ani compile/test.
Worker nie pushuje; push z `--no-verify` jest wyłącznym przyciskiem Foundera. Wyłącznie wyznaczony
integrator może zrobić lokalny structural admission po
weryfikacji dokładnego commita/zakresu, Semgrep oraz przeglądzie sekretów/bezpieczeństwa, aby kolejne
fale budowały na złączonej architekturze, podczas gdy compile, lint, type-check i testy pozostają
odroczone. Dopiero nazwana closure oraz pełne, odpowiednie dla języka bramki tworzą verified delivery.

### 6. Serve & review (editable artifacts via vibecrafted-server)

Plan + briefy to **edytowalne artefakty**, nie ściana pytań inline. Flow jest taki:
research → przedstaw findings + estymatę wysiłku → zaproponuj pierwszy kształt cięcia/fali → wyrenderuj
briefy → **zaserwuj je do przeglądu Foundera przez `vibecrafted-server`** (naturalny dom tooling-u tej
fazy: czyta typowany kontrakt control-plane i renderuje wave atlas + briefy jako
**wielozakładkową, edytowalną** powierzchnię HTML — jedna zakładka na artefakt (atlas · każdy brief · każdy design doc),
edytowane w miejscu). Founder steruje przez edycję wyrenderowanego planu w przeglądarce, nie przez odpowiadanie na
dwadzieścia pytań w trakcie scaffoldu. Dopracowujesz Z Founderem na zaserwowanych artefaktach.

**Przeszczep powierzchnię — nie wymyślaj jej od nowa.** Sprawdzone źródła do zerżnięcia: `../pensieve`
(wielozakładkowy edytowalny dashboard workspace), `../unicode-puzzles-portal` (generatory portali) oraz
visual-companion z `/brainstorming` (sprawdzone generatory mockupów/diagramów HTML). Zakładka server-review
musi być wielozakładkowa + edytowalna od pierwszego dnia, nie statyczny zrzut.

**scaffold-doctor (bramka, sprawdzana maszynowo):** uruchom verba produktu przed każdym
przekazaniem scaffold→implement — nie opisuj walidatora jako zewnętrznego narzędzia serwera:

```bash
vibecrafted scaffold-doctor --plan <root> --repo <git-root>
```

REFUSE (exit 1) = brak handoffu. Verb odnajduje binarkę `scaffold-doctor` (generacja albo lokalny
build) i ładuje ten sam typowany `manifest.json` co server. Odmawia, dopóki: tożsamość manifestu nie
zgadza się z kanonicznym rootem planu; wszystkie wymagane artefakty nie istnieją; ID i ścieżki nie
są unikalne; zależności się nie rozwiązują; edytowalne ścieżki są symlinkami lub wychodzą poza root;
briefy na dysku nie są zadeklarowane; oraz master-dispatch nie ma wave atlasu + grafu zależności;
każde cięcie nie ma `briefs/<wave>-<slot>_<slug>.md` z wszystkimi 12 sekcjami; bullety acceptance nie
są atomowe + poparte verifierem; nie istnieje design doc dla każdego cięcia oznaczonego
`needs_design`; **nie istnieje `DRIVER.md` niosący wszystkie sześć (pełne ścieżki · graf z adnotacją
why · gotowe komendy · reguła `[ ]→[x]` verbatim · snapshot statusu · matryca odbioru R12 z
niesfałszowanym polem Foundera)**. Bramka jest **sprawdzana
maszynowo, nie obiecywana przez agenta** — to ta sama bramka artefakt-jako-prawda, której async
runtime używa między każdym przekazaniem cadence read-write.
