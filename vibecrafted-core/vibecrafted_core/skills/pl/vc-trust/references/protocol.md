# vc-trust — Protokół falsyfikacji i skala oceny evidence

## Protokół

### 1. Zorientuj się i ogranicz strumień

Przejdź bramkę `vc-init`. Przeczytaj cały atlas Loctree i historię intencji
AICX. Uchwyć branch, HEAD, stan dirty i dokładny zakres commitów. Na Living Tree
nigdy nie przypisuj autorstwa brudnego pliku ani równoległego commita wyłącznie
na podstawie czasu.

Wylistuj nieosądzonych kandydatów:

```bash
python -m vibecrafted_core.trust enumerate <author> --since <sha-or-ISO-time>
```

### 2. Zamień prozę w falsyfikowalne claimy

Dla każdego commita wyciągnij każdy materialny claim z jego subjectu/body i ze
zmienionej powierzchni. Przepisz mgliste zdania na sprawdzenia w rodzaju:

- nazwany test albo bramka istnieje i pada, gdy zachowanie jest zepsute;
- ścieżka runtime'u dociera do zmienionego kodu;
- deklarowane zachowanie fail-closed nie ma obejścia ani silencera;
- docsy i powierzchnia launchera opisują zachowanie, które faktycznie jedzie;
- zakres diffu zgadza się z wiadomością i nie zawiera obcych, niezadeklarowanych
  plików.

Brak claimu w wiadomości nie ukrywa materialnej regresji w diffie.

### 3. Oceń evidence per claim

- `strong` — bezpośrednia reprodukcja w runtimie, test adwersarialny, dokładna
  inspekcja artefaktu albo niezależnie padająca-a-potem-przechodząca bramka.
- `medium` — skupiony test jednostkowy/integracyjny plus strukturalny dowód po
  stronie konsumentów.
- `weak` — statyczna proza, wywnioskowana intencja, evidence wyłącznie z
  happy path albo raport upstream, którego sędzia sam nie powtórzył.

`pass` wymaga, żeby każdy materialny claim miał wystarczające bezpośrednie
evidence. Słabe evidence może podpierać kontekst, ale samo z siebie nigdy nie
daje materialnego passa.

### 4. Falsyfikuj, nie odgrywaj ceremonii

Użyj Loctree `slice` dla zmienionych plików, `impact` dla zmian o dużym zasięgu,
literalnego find/body dla dokładnych claimów oraz `follow` dla istotnych
sygnałów dead/cycle/twin. Przeczytaj diff commita i jego rodziców. Uruchom
najbliższe testy i prawdziwą ścieżkę użytkownika. Sprawdź, czy sama komenda
weryfikująca w ogóle potrafi paść.

`vc-review` i `vc-audit` pozostają czymś innym:

- `vc-review` osądza jakość ograniczonego diffu/PR-a.
- `vc-audit` falsyfikuje ukończony plan albo wielozadaniową implementację.
- `vc-trust` osądza strumień commitów na żywym, wspólnym drzewie i zapisuje
  trwały werdykt per commit.

### 5. Zapisz dokładnie jeden jawny werdykt

Każdy `--claim` musi mieć jeden pasujący `--grade` i `--evidence`:

```bash
python -m vibecrafted_core.trust note <sha> pass \
  --claim "the blocking lane rejects insecure code" \
  --grade strong \
  --evidence "negative fixture failed before the fix and passed after it"
```

Osądzając commit(y) wyprodukowane przez run, dodaj `--run-id <id>`. Kanoniczny
settlement zapisuje wyłącznie to jawne `note`. Kod wyjścia, obecność raportu ani
zakończony await nigdy nie oznaczają trust passa.

Journal domyślnie leży w
`$VIBECRAFTED_HOME/trust/journal.jsonl` i używa
`vibecrafted.trust-journal.v1`. Nadpiszesz to przez
`VIBECRAFTED_TRUST_JOURNAL` albo `--journal`.

### 6. Czekaj na granicy runu

Podstawowy tryb cyklu życia nazywa się `await-primary`, nie `guard=await`:

```bash
python -m vibecrafted_core.trust await-primary <run-id> \
  --author <agent-author> \
  --since <baseline-sha>
```

Czeka synchronicznie przez kanoniczny control plane, a potem listuje nieosądzone
commity kandydujące. Nie auto-passuje, nie auto-notuje, nie odpytuje w tle i nie
działa jak stały monitor. Stałe monitorowanie jest wyłącznie wygodą w trybie
interactive i nie jest trwałym mechanizmem wybudzania.

### 7. Zbierz do kupy

```bash
python -m vibecrafted_core.trust triage [--run-id <id>]
```

Triage bierze najnowszy wpis append-only per repo+commit i raportuje kanoniczne
liczniki `f/x/n`. Nie przelicza settlementu z Gita ani z kodów wyjścia.
