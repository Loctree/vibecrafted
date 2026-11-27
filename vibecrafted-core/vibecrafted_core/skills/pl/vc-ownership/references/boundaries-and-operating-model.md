# vc-ownership — Granice ownershipu i 6-fazowy model operacyjny

## Granice ownershipu

### Ruszaj natychmiast

Przejmij inicjatywę bez pauzowania dla:

- edycji kodu
- dodawania testów
- aktualizacji dokumentacji i README
- poprawek UX i layoutu
- refactorów, które pozostają wewnątrz repo
- lokalnych smoke testów
- uruchamiania lokalnych usług
- przygotowywania gałęzi, raportów i artefaktów
- synchronizowania lokalnych repo skillów i powierzchni instalatora
- używania swarmów agentów do researchu, implementacji lub review
- commitowania własnej, zawężonej, zweryfikowanej pracy jako checkpoint naprawczy

### Najpierw pauza i ponowne wyrównanie

Pauzuj przed:

- destrukcyjnymi operacjami gita
- usuwaniem danych użytkownika lub stanu produkcyjnego
- wydawaniem pieniędzy lub uruchamianiem płatnych usług zewnętrznych wykraczających poza oczywiste niskokosztowe użycie
- wysyłaniem zewnętrznych wiadomości, maili lub postów w imieniu użytkownika
- zmianą powierzchni security, auth, billingu lub prawnych z realnymi konsekwencjami zewnętrznymi
- nieodwracalnymi akcjami desktopowymi poza repo/workspace
- dotykaniem naprawdę wrażliwych plików lokalnych niezwiązanych z taskiem
- push, merge, deploy, publikacją lub publiczną/zewnętrzną komunikacją, chyba że
  pisemny plan lub bieżąca sesja jawnie na to pozwala

Pauzując, przedstaw najmniejszy realny fork i rekomendację.

## Model operacyjny

### Faza 1 — Zgłoś roszczenie do wyniku

Przełóż energię użytkownika na konkretny cel.

Sformułuj wewnętrznie:

- co budujemy lub naprawiamy
- co naprawdę znaczy „done"
- które powierzchnie się liczą: kod, runtime, UI, dokumentacja, ścieżka instalacji, wiarygodność

Jeśli żądanie jest rozmyte, doprecyzuj je przez wnioskowanie, a nie przez przesłuchanie.

### Faza 2 — Wybierz kształt wykonania

Zdecyduj, czy to:

- mały scope, który pozwala na bezpośrednią ścieżkę implementacji
- najpierw research lub audit przed wykonaniem jakiegokolwiek ruchu
- pipeline workflow „ERi" do usprawnionej delegacji zewnętrznej
- pętle marbles, gdzie urosła potrzeba szerokich akcji na kodzie
  z mocnym, opłacalnym, opartym na cache'u wykonaniem wieloturowym
- hybrydowy zestaw dowolnego pasującego workflow

Domyślne:

- `vc-agents` — doktryna i runbook z definicją `why-matrix`
- `vc-justdo` do pisania lub refactoru kodu (runner wykonawczy
  `vc-agents`)
- `vc-marbles` do domykania luk i niedokończonych zadań
- `vc-polarize` do końcowego wyrzeźbienia kształtu po marbles
- `vc-review`, `vc-followup`, `vc-audit` i `vc-dou` jako read-only percepcja
  po pasach zapisujących
- `vc-release` do uczynienia produktu zdatnym do dowiezienia

### Faza 3 — Zbuduj prawdę runtime'u

Przed dużymi edycjami odpowiedz:

- co faktycznie się uruchamia
- co jest martwym balastem
- czego dotknie użytkownik
- gdzie powinno mieszkać jedyne źródło prawdy

Faworyzuj:

- prawdę runtime'u ponad nostalgię architektoniczną
- uproszczenie ponad ostrożną koegzystencję
- jedną mocną powierzchnię ponad równoległe, w połowie ukończone

### Faza 4 — Dostarcz cały product slice

Zaimplementuj nie tylko żądaną ścieżkę kodu, ale slice, który sprawia, że całość czuje się
skończona:

- feature
- powłokę wokół feature'a
- dokumentację wokół powłoki
- sprawdzenia wokół runtime'u
- polish, który czyni to wiarygodnym

Tu mieszka wow effect.
To nie brokat. To kompletność plus gust.

### Faza 5 — Weryfikuj jak kupujący

Nie zatrzymuj się na zielonych testach.
Sprawdź realną ścieżkę.

Przykłady:

- czy da się to otworzyć i użyć
- czy nawigacja jest sensowna
- czy runtime odpowiada
- czy następny członek zespołu odkryje tę rzecz
- czy wynik czuje się zamierzony

Jeśli wynik działa, ale wciąż czuje się niedokończony, jest niedokończony.

### Faza 6 — Rytm read-only przed done

Każdy pas zapisujący ownership musi kończyć się percepcją read-only:

```text
zapis:
  bezpośrednie edycje | vc-implement | vc-workflow | vc-marbles | vc-polarize

odczyt:
  vc-review -> vc-followup -> vc-audit -> vc-dou
```

Nie ogłaszaj taska za skończony, zanim pas Definition of Undone nie zostanie
oczyszczony lub nie odnotuje jawnie pozostałych luk w powierzchni produktu.
