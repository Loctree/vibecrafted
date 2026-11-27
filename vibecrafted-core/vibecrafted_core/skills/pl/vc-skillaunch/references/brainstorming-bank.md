# vc-skillaunch — Bank pytań i checklista brainstormingu (Faza 1)

## Faza 1: Brainstorming (OBOWIĄZKOWA)

Przeprowadź z użytkownikiem **iteracyjną rozmowę w obie strony**. NIE zadawaj wszystkich
pytań naraz. Wybierz 2-3 trafne pytania na rundę z banku poniżej, doprecyzuj swoje
rozumienie i dopytuj dalej.

### Runda 1: Zrozum workflow

Zacznij od podsumowania tego, co zaobserwowałeś w workflow, a potem zapytaj:

1.  „Oto moje rozumienie workflow: [podsumowanie]. Czy jest trafne? Co byś
    zmienił?"
2.  „Jakie są oczekiwane wejścia i wyjścia tego workflow?"
3.  „Jak często spodziewasz się uruchamiać ten workflow? Jest cykliczny czy jednorazowy?"

### Runda 2: Elastyczność i obsługa błędów

Dla każdego zidentyfikowanego kroku workflow ustal jego sztywność:

1.  „W [kroku X], jeśli główne podejście zawiedzie (np. API leży, brak wyników),
    czy agent powinien: (a) zapytać cię o wskazówki, (b) automatycznie spróbować
    alternatywnych podejść, czy (c) głośno zgłosić błąd?"
2.  „Czy są kroki, w których dokładna metoda ma znaczenie (np. trzeba użyć
    konkretnej bazy danych), w odróżnieniu od kroków, gdzie każde rozsądne podejście
    jest w porządku?"
3.  „Czy skill powinien obsługiwać przypadki brzegowe po cichu, czy wynosić je na wierzch
    do użytkownika?"

### Runda 3: Zależności i zasoby

Zanim zadasz te pytania, sprawdź, które z zainstalowanych skilli pokrywają się z
workflow. Jeśli istniejący skill z bundla science pokrywa jakiś krok, nowy skill
**MUSI** się do niego odwołać — nie proponuj wariantu samowystarczalnego.

1.  „Zauważyłem, że workflow korzysta z funkcjonalności pokrytej przez [istniejący skill X,
    skill Y]. Nowy skill będzie się do nich odwoływał, zamiast je reimplementować.
    Czy są jakieś inne narzędzia lub skille, które chcesz, żebym uwzględnił?"
2.  „Czy są jakieś limity zapytań API (rate limits), o których powinienem wiedzieć dla usług
    używanych w tym workflow, a które nie są już pokryte przez istniejący skill?"
3.  „Czy są konkretne pliki dostarczające ważnego kontekstu naukowego do
    stworzenia tego skilla? Na przykład: dokumentacja API, prace referencyjne,
    przykładowe zbiory danych lub notatki dziedzinowe. Jeśli tak, podaj je, a
    uwzględnię ich treść w materiałach referencyjnych skilla."

### Runda 4: Zakres, kształt i klasa matrycy

1.  „Nasz workflow obejmował [X, Y, Z]. Czy mam zdestylować je wszystkie do
    skilla, czy jest dodatkowa funkcjonalność, którą warto uwzględnić?
    I na odwrót — czy któreś z nich pominąć?"
2.  Ustal, czy skill potrzebuje jakiegokolwiek kodu. Jeśli jakiś krok wiąże się z wywołaniem
    API, przetwarzaniem danych, odczytem/zapisem plików lub obliczaniem wyników, skill
    **potrzebuje kodu** i powinieneś domyślnie wybrać wzorzec CLI. Sięgaj po skill
    czysto tekstowy (instruction-only) tylko wtedy, gdy każdy krok dotyczy wyłącznie
    rozumowania, koordynacji istniejących narzędzi lub trzymania się spisanego protokołu
    bez żadnej pracy programistycznej. Potwierdź swoją ocenę z użytkownikiem prostym
    językiem:
    - Jeśli kod jest potrzebny: „Część tych kroków wiąże się z [pobieraniem danych z
      API / przetwarzaniem plików / obliczaniem wyników], więc stworzę skrypt
      pomocniczy, który agent może uruchomić za ciebie. Skrypt będzie miał proste
      komendy w stylu `search`, `fetch`, `analyze` itd. — nie będziesz musiał
      pisać żadnego kodu samodzielnie. Brzmi dobrze?"
    - Jeśli kod nie jest potrzebny: „Ten workflow polega w całości na trzymaniu się zestawu
      kroków i używaniu istniejących narzędzi — żaden nowy kod nie jest potrzebny. Napiszę go
      jako zestaw jasnych instrukcji, których agent się trzyma. Brzmi
      dobrze?"
3.  Jeśli powstanie skrypt pomocniczy: „Myślę, że skrypt powinien mieć
    te komendy: [proponowane komendy prostym językiem, np. 'wyszukaj
    białka', 'pobierz wyniki', 'porównaj sekwencje']. Co byś dodał lub
    zmienił?"
    2b. **Klasa Matrycy Delegacji** — core launcher / meta / fundament; potwierdź literały (`vibecrafted <launcher> <agent>`). Nigdy uniwersalnego placeholdera `workflow`.
4.  „Jak skill ma się nazywać? Proponowana nazwa: `[sugestia]`."

### Runda 5: Testowanie (opcjonalna)

1.  „Czy możesz podać przykładowe zapytanie i oczekiwaną odpowiedź, których użyję do weryfikacji,
    że skill działa zgodnie z zamysłem? Na przykład: 'Jeśli zapytam [pytanie], skill
    powinien wyprodukować [odpowiedź].' To opcjonalne, ale pomaga mi zwalidować skilla
    w trakcie tworzenia."

### Kryteria ukończenia brainstormingu

Jesteś gotów przejść do Fazy 2, gdy potrafisz pewnie odpowiedzieć na WSZYSTKIE:

- [ ] Jaki jest cel i scope workflow?
- [ ] Jakie są wejścia i wyjścia?
- [ ] Które kroki są ścisłe, a które elastyczne?
- [ ] Do których istniejących skilli należy się odwołać?
- [ ] Jakie nowe skrypty (jeśli w ogóle) są potrzebne?
- [ ] Jakie limity zapytań (rate limits) obowiązują?
- [ ] Jak należy obsługiwać błędy?
- [ ] Czy workflow potrzebuje jakiegokolwiek kodu? (Jeśli tak → wzorzec CLI; jeśli nie →
      instruction-only)
- [ ] Klasa matrycy (core launcher / meta / fundament) i dokładne literały?
- [ ] Czy jest przykładowe zapytanie/odpowiedź do walidacji?
