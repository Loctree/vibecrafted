---
name: vc-intents
version: 2.0.0
description: >
  Wydobądź kandydatów intencji ze źródeł dla jednego repozytorium w wybranym
  oknie, skonfrontuj każdego ze stanem kodu za pomocą dwóch niezależnych flot
  i przygotuj stabilny plan cięć dla vc-dispatch z uwzględnieniem zależności.
  Używaj przy prośbach „zbierz intencje”, „rozlicz intencje”, „co wynika ze
  źródeł”, „co obiecaliśmy i nie dowieźliśmy”, „co z planu siedzi w kodzie”,
  „co ustaliliśmy, że zbudujemy”, „co jeszcze jesteśmy winni”, „pokrycie
  intencji”, „plan kontra kod”, „najwyższa prawda”, „checklista z intencji”,
  albo gdy rozproszone wypowiedzi z transkryptów i sesji trzeba zamienić
  w kolejkę prac odporną na kompakcję i zmianę maszyny. Sięgaj po ten skill
  zamiast gołego `aicx search`, gdy trzeba oddzielić materiał źródłowy od
  klasyfikacji modeli i twierdzeń agentów o wykonaniu, a odpowiedź ma się
  skończyć planem, nie katalogiem.
loctree_value: "pytania strukturalne ustalają, czy obietnica ma ścieżkę runtime"
aicx_value: "indeksowane intencje i kontekst sesji; jedno z wielu źródeł"
dogfooding: "wymagane — połączenie korpusu, aicx, Loctree i dispatchu"
---

<!-- fleet-imperative: v3 -->

> **Wywołanie dla `vc-intents` (launcher `intents`)** — zobacz
> [Matrycę Delegacji](../DELEGATION_MATRIX.md).
>
> | Ścieżka           | Literał tego skilla                                                                                    |
> | ----------------- | ------------------------------------------------------------------------------------------------------ |
> | 1. Worker z ręki  | `vibecrafted intents <agent>` — jeden tor ekstrakcji albo konfrontacji, READ, zapisuje tylko swój JSON |
> | 2. Interaktywnie  | `/vc-intents` — samo polowanie, **w tej sesji**: sweep, tory, plany, merge, kolejka, render            |
> | 3. Agent-operator | wysyła formę workera przez `vc-dispatch` z planem napisanym przez `scripts/intents_cli.py plan`        |
>
> Kadencja pozostaje **read**: ten skill nigdy nie edytuje repo. Dostarczenie to
> osobny plan `implement`, który pisze dla floty.

<!-- /fleet-imperative -->

# vc-intents — od materiału źródłowego do planu cięć

Długo żyjący projekt gromadzi wypowiedzi szybciej niż kod. Materiał z marca może
przeczyć materiałowi z maja; agent proponuje inny kształt w czerwcu i twierdzi w
lipcu, że dowiózł. Odtwórz kontekst, zanim uznasz, co dotyczy tego repozytorium
i aktywnego zadania użytkownika.

Ten skill jest właścicielem całej ścieżki: **zebrać → rozdzielić głosy →
katalog z dosłownymi cytatami → konfrontacja dwiema flotami → reklasyfikacja
tego, co ukrywa „landed" → stabilna kolejka → plan dispatchu, który flota może
odpalić**. `vc-canary` znajduje kolizje prawdy i nigdy nie refaktoruje;
`vc-implement` tnie kod, ale nie odtwarza obietnicy; `vc-audit` falsyfikuje plan
wobec kodu. `vc-intents` odtwarza obietnicę, dowodzi, co z niej zostało, i
przekazuje resztę jako cięcia.

## Cel

`vc-intents` produkuje ledger, w którym każdy kandydat intencji z wybranego okna
ma jedną jawną dyspozycję, wynik zgodności między dwiema niezależnymi flotami i
warstwę korekt edytowalną przez człowieka — i jest gotowy, gdy
`intents_cli.py <workdir> --lang pl status` nazywa, co jest jeszcze otwarte, a
`plan --stage implement` zapisał dla tego plan dispatchu. Katalog nie zamyka
celu. Audyt nie zamyka celu. Plan cięć zamyka.

## Kanoniczna bramka orientacji

Przed każdym krokiem dotyczącym repo — sweep wobec repo, konfrontacja, plan —
uruchom albo skonsumuj procedurę `vc-init` dla przydzielonego repo.
`Loctree:loctree` jest domyślnym skillem percepcji strukturalnej w tym
przebiegu i musi wytworzyć albo odświeżyć Code-Derived Application Map
(`context`, `repo-view`, `focus`, `slice`, `impact`, `find`, `follow`). Tory
konfrontacji to dziedziczą: brief czyni loctree-mcp pierwszym ruchem, a
`landed` bez strukturalnej ścieżki za sobą nie jest werdyktem. Jeśli brak
świeżych dowodów `vc-init`, wykonaj najpierw init i traktuj polowanie jako
zablokowane, dopóki nie istnieje prawda repo. Sweep korpusu transkrypcji bez
podpiętego repo deklaruje w raporcie wyjątek no-repo.

## Zakres to okno, nie historia

Ogranicz polowanie przed sweepem: `--since/--until` albo temat. Pokrycie
raportujesz wobec tego okna. Cała historia to jedno z legalnych okien — nie
warunek zamknięcia. Czego okno nie zawiera, zapisujesz jako _poza zakresem_,
nigdy jako _absent_.

## Narzędzie

Jedna wspólna implementacja CLI obsługuje obie wersje. Polski wariant zawsze
wybieraj przez `<workdir> --lang pl <komenda>`: dotyczy to briefów, promptów,
raportów i widoków. Domyślne `--lang en` daje angielski wynik. Cytaty źródłowe
zachowują oryginalny język; nie są tłumaczone.

```bash
CLI=~/.claude/skills/vc-intents/scripts/intents_cli.py   # albo ścieżka w store
W=~/.vibecrafted/artifacts/<owner>/<repo>/intents         # jeden workdir na polowanie
uv run "$CLI" "$W" --lang pl <komenda> …
```

Jeden katalog roboczy trzyma wszystko, co musi przeżyć kompakcję albo drugi
host: `sweep.json`, `shards/`, `intents.json`, `lanes/`, `LEDGER.json`,
`overrides.jsonl`, `queue.json`, `STABLE-QUEUE.md`, `LEDGER.md`,
`intents.html`. Agenci czytają i orzekają; skrypt prowadzi księgi, robi
falsyfikacje, które nie wymagają osądu, i pisze plany oddające osąd flocie.

## Procedura

Wykonaj pełne 10-krokowe polowanie przez `intents_cli.py`: 0. **Orientacja** — `vc-init`, `aicx intents -p /<repo>` i kontrola negatywna najnowszego commitu vs intencji.

1. **Sweep / Append** — `sweep --since/--until` (w kolejne dni użyj `append` lub `append --abort`, nigdy ponownego `sweep`).
2. **Ekstrakcja** — szybka flota flash (`references/extraction-brief.md`, `verify-quotes --strict`; `quote` musi być dosłownym podciągiem).
3. **Rozdziel głosy** i **4. Chronologia** — oddziel autorów/projekty/cytaty modeli; unieważniaj tylko przez `superseded_by`.
4. **Konfrontacja** — dwie niezależne floty na dwóch hostach (`references/confrontation-brief.md`, `references/loctree-questions.md`, `merge`).
5. **Reklasyfikacja** — `reclassify` nakłada `landed-contested` i `landed-by-doc` (`references/ledger-schema.md`).
6. **Warstwa człowieka** — `render --html` + `decide` do `overrides.jsonl` (`references/review-surface.md`).
7. **Kolejka i plan** — `queue --min-strength 4`, potem `plan --stage implement` (autoryzację daje aktywne zadanie lub plan).
8. **Zamknięcie** — `status` zwraca 0 tylko przy zerze otwartych dyspozycji, braku źródeł `unavailable`/`truncated` i `runtime_verified = yes` dla każdego `landed`; po kompakcji czytaj `LEDGER.md` + `status` + `queue` bez powtarzania sweepu.

Pełne komendy, wyniki z pola, odzyskiwanie `append` i zasady kroków: [references/procedure.md](references/procedure.md).

## Kontrakt wyjścia

1. **Pokrycie** — okno, źródła ze stanem (`read`/`empty`/`unavailable`/
   `truncated`), pliki i wiersze per źródło.
2. **Katalog** — kandydaci z leksykalnie sprawdzonymi cytatami, odrzucone cytaty z powodami.
3. **Ledger** — werdykty per host, zgodność per para, dyspozycja efektywna,
   korekty (reguła i człowiek), `runtime_verified`.
4. **Kolejka** — stabilne otwarte intencje z uzasadnieniem porządku.
5. **Plan** — `intents-implement.<host>.dispatch.toml`, czysty po doktorze.
6. **Najwyższa prawda** — jedna nierozwiązana rzeczywistość, która powinna
   trochę zaboleć. „43 % tego, co dwie floty nazwały landed, kwestionują
   skargi w źródłach" to najwyższa prawda; „część pozycji jest partial" nie.

## Antywzorce

Traktowanie rankingowego trafienia aicx jak przeczytanego źródła · parafraza w
`quote` · werdykt jednej floty jako dowód · `landed` z `docs/*.md` ·
`superseded` bez następcy · powtarzanie sweepu po powrocie · modele z czołówki
do masowego czytania · verifier `run` z literałem toru (`release` w
`L6-build-release` wyzwala hard-stop parsera dispatchu; skrypt pisze ścieżki
przez `{id}`) · naciskanie hard-stopu, bo kolejka tak kazała · raportowanie
zielonego audytu jako zamknięcia, gdy kolejka jest niepusta.

## Skille pokrewne

`vc-init` przed wszystkim · `vc-canary`, gdy dwa moduły konkurują o prawdę,
której intencja potrzebuje · `vc-dispatch` odpala każdy plan, który ten skill
pisze · `vc-implement` / `vc-ownership` to cięcia · `vc-trust` falsyfikuje
potem claim ukończenia workera · `vc-audit` dla spisanego planu zamiast korpusu.

## Zweryfikuj przed przekazaniem

Obejdź ciężarówkę — [Reguła Weryfikacji](../VERIFICATION_RULE.md): ledger
istnieje i `status` mówi OPEN z powodami, które umiesz nazwać; plan przeszedł
`vibecrafted dispatch --doctor`; HTML otwiera się z właściwymi nazwami hostów i
działającymi linkami do kodu; każda liczba w raporcie pochodzi z pliku w
workdirze, nie z pamięci.

---

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
