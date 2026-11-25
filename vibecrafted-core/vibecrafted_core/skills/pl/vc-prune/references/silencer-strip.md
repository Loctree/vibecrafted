# vc-prune — Fala 5: Silencer Strip i Antywzorce

## Fala 5 — Silencer Strip (Zdejmij i słuchaj)

### Inwentaryzacja

```bash
# Rust
rg -n '#\[allow\(' src-tauri/src
rg -n 'nosemgrep' .

# TypeScript / JavaScript
rg -n 'eslint-disable' src
rg -n '@ts-(ignore|nocheck|expect-error)' src
rg -n 'biome-ignore' src

# Python
rg -n '# noqa' .
rg -n '# type: ignore' .
rg -n '# pylint: disable' .
rg -n '@pytest\.mark\.skip' .

# Go
rg -n '//nolint' .
rg -n 'testing\.Short\(\) \|\| t\.Skip' .

# Test theater across languages
rg -n 'panic!\("Test requires|throw new Error\("requires' .
rg -n 'it\.skip|test\.skip|describe\.skip' .
```

Wychwyć **liczniki per kategoria**. To twoja linia bazowa „przed".

### Zdejmij je WSZYSTKIE w jednym przebiegu

Masowo usuń linie. Nie wstępnie kuratuj „oczywistych zatrzymanek" — to ten sam bias, który je tam wstawił, broniłby ich. Pozwól
zdecydować toolchainowi.

### Uruchom bramki

Cokolwiek repo już ma — nie wymyślaj nowych:

```bash
cargo clippy --all -- -D warnings && cargo test --all
pnpm lint:tsc && pnpm code:all && pnpm vitest run
ruff check . && mypy . && pytest          # Python
golangci-lint run && go test ./...        # Go
semgrep --config=auto .                   # if available
pre-commit run --all-files                # if installed
```

### Triażuj z rozwagą

| Finding                                  | Rozwiązanie                                                                                                                                                                                 |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Prawdziwy smell/code smell (zapaszek)    | **Napraw przyczynę źródłową.** Zrefaktoruj, napisz porządne typy, dodaj adapter, zdejmij locka przed await.                                                                                 |
| False positive                           | **Zrefaktoruj stylistycznie** tak, by warning nigdy nie odpalał. Bez ponownego dodawania.                                                                                                   |
| Faktyczne ograniczenie techniczne        | **Dodaj silencer z powrotem z komentarzem klasy incydentu**: DLACZEGO (powód techniczny), KIEDY (pod jakimi warunkami), GDZIE (konkretna ścieżka kodu). Nie „intentional", nie „by design". |
| **Zapomniana perełka (łagodna ścieżka)** | **Nie usuwaj. Zgłoś.** Warning `dead_code` na 200-liniowym module o przemyślanej strukturze to zaparkowana praca. Dodaj do **Raportu Zapomnianych Perełek**. Decyduje operator.             |
| Zdemaskowany teatr testów                | **Stop. To większe niż silencer.** Wzorzec panic-or-skip, który zawsze ewaluuje w jedną stronę, oznacza, że test nigdy nie był prawdziwy. Otwórz osobny plan na realne podpięcie.           |
| Ujawniony naprawdę martwy kod            | Silencer ukrywał `dead_code` na jednolinijkowym stubie lub pliku roboczym. Usuń — ale dopiero po szybkim sprawdzeniu pod kątem zapomnianej perełki.                                         |

Zasada: **silencer zarabia na swoje utrzymanie tylko z pisemnym powodem technicznym, który inny inżynier za pół roku
przyjąłby jako poważny.** Mgliste komentarze „intentional" nie są poważne. Tak samo: **usuwaj kod tylko wtedy, gdy jest
jednoznacznie śmieciem** — wszystko pomiędzy idzie do Raportu Zapomnianych Perełek.

### Raport Zapomnianych Perełek

Wynikiem Fali 5 **nie** jest mniejsze repo — to pisemny raport. Zapisz do
`$VIBECRAFTED_HOME/artifacts/<org>/<repo>/<YYYY_MMDD>/reports/<timestamp>_forgotten-gems.md`.

> Zobacz [references/case-studies.md](case-studies.md), gdzie znajdziesz pełny szablon Raportu Zapomnianych Perełek, szablon
> raportu teatru testów oraz konkretne realne/hipotetyczne studia przypadków (example-app 0.67.3 silencer-strip, odpowiednik
> billing-service w sample-portal, katalog zaskakujących findingów).

Teatr testów to dług, nie perełka. Zawsze dostaje plan followupu zapisany do `<timestamp>_test-theater.md`. Nigdy przywrócenia
silencera.

### Kryteria akceptacji dla fali

- Pozostała liczba silencerów to **mały ułamek** inwentaryzacji (cel ≤25%, często ≤10%).
- Każdy pozostały silencer niesie komentarz klasy incydentu.
- Każda bramka przechodzi na zielono bez `--no-verify`, `cargo clippy --allow-dirty`, `pnpm lint --fix --quiet` ani żadnego innego triku „
  zazielenić to przez ukrycie".

### Zaskakujące findingi są nagrodą

Wypatruj: testów, które zawsze się skipują / zawsze panikują, allow `dead_code` na funkcjach, których jedyny caller usunięto trzy
release'y temu, `@ts-ignore` na typach poprawnych od roku, `eslint-disable jsx-a11y/...` na prawdziwych naruszeniach a11y,
`nosemgrep: react-dangerouslysetinnerhtml` na HTML-u, który **nie** jest sanityzowany, `# type: ignore[arg-type]` na funkcji,
której sygnaturę naprawiono dwa refactory temu. Każdy z nich to prawdziwy bug albo prawdziwe kłamstwo, które silencer ukrywał.

## Antywzorce

- Usuwanie dziesięciu martwych symboli, podczas gdy cały porzucony podsystem wciąż stoi.
- Ufanie raportom „unused" bez sprawdzenia dynamicznego ładowania przez router frameworka.
- Zachowywanie chaotycznego pliku na 2000 linii, bo „może się przyda" — od tego jest historia Gita.
- Czyszczenie kodu z pozostawieniem nieaktualnych zależności w lockfile'u.
- Selektywne zdejmowanie silencerów. Cały sens Fali 5 to ominięcie tego biasu.
- Masowe przywracanie silencerów, bo było „za dużo warningów". To znów zakopywanie komunikatu.
- Dodawanie nowych silencerów, by wyciszyć świeżo odkryte warningi. Napraw warning albo zrefaktoruj go.
- Traktowanie `panic!("Test requires X")` jak prawdziwej bramki albo `it.skip` / `@pytest.mark.skipif` jak nieszkodliwych. Testy, które
  zawsze się skipują, nie istnieją; kosztują uwagę recenzenta.
- Automatyczne usuwanie kodu, który ukrywał allow `dead_code`, bez wcześniejszego sprawdzenia pod kątem zapomnianej perełki.
- Traktowanie Fali 5 jako konfrontacyjnej. Dawni inżynierowie dodawali silencery z prawdopodobnych powodów. Fala 5 to ponowne czytanie, nie
  wyrok.

## Zasada prune

Nie żądaj od repo, by wyjaśniło każdą bliznę. Żądaj, by uzasadniło każdą przetrwałą powierzchnię.

Jeśli powierzchnia nie działa na produkcji, nie buduje release'u ani nie testuje integralności — ruchem **nie** jest automatycznie
usunięcie. Ruchem jest **zdecydować z intencją**: revive, archive albo delete. Skill istnieje po to, by wydobywać decyzje na powierzchnię, a nie podejmować
je na autopilocie.

**Toolchain to nie wróg do wyciszenia. To świadek do przesłuchania.** Zdejmij wyciszenie. Uruchom bramki.
Słuchaj. Potem zdecyduj — przypadek po przypadku, z pisemnym powodem — co naprawdę zasługuje na milczenie, co potrzebuje prawdziwej
naprawy, a co było zapomnianą perełką ukrytą za silencerem przez cały ten czas.

Repo, które przeszło przez `vc-prune`, niekoniecznie jest mniejsze. Jest **czytelne**. Każda przetrwała powierzchnia, każdy
przetrwały silencer, każdy przetrwały test ma pisemny powód, by tam być. To jest wygrana.
