# vc-grill — Drzewo projektu, protokół tur i wzorzec Design Contract

## Drzewo projektu (pełny przewodnik gałęzi)

Odwiedź istotne gałęzie w tej kolejności, pomijając decyzje już rozstrzygnięte aktualnymi dowodami lub jawną odpowiedzią Foundera:

1. **Zakres i granice:** efekt dla użytkownika, najmniejszy użyteczny zakres zmiany oraz jawne wyłączenia.
2. **Architektura i model danych:** własność stanu, kontrakty, trwałość danych i istniejące rozwiązania warte ponownego użycia.
3. **Runtime i integracja:** punkty wejścia, wywołujący, środowisko wykonania, odpowiedzialność za integrację i propagacja błędów.
4. **Przypadki brzegowe i awarie:** niedostępne usługi, uprawnienia, wyścigi, przerwana praca i sposób odzyskiwania.
5. **Weryfikacja i DoU:** obserwowalna akceptacja, sensowne testy oraz dowody produktowe potrzebne, by rezultat dało się znaleźć, wypróbować, zrozumieć, obdarzyć zaufaniem i dostarczyć.

Nie wymyślaj niepewności, by wypełnić drzewo. Wybierz następny nierozstrzygnięty węzeł, którego odpowiedź odblokuje najwięcej zależnych decyzji.

## Protokół kolejnych tur

Przed pierwszym pytaniem zbadaj dostępne dowody i wskaż główną niejednoznaczność. W każdej turze:

- Nazwij bieżący węzeł i krótko wyjaśnij, dlaczego wybór ma znaczenie.
- Przedstaw istotne opcje, po jednej korzyści i jednym koszcie każdej.
- Zapisz **Moja rekomendacja (agent):** wybraną opcję i uzasadnienie.
- Zadaj jedno bezpośrednie pytanie o tę decyzję, a potem czekaj.
- Zapisz odpowiedź z jej źródłem i zaktualizuj pozostałe drzewo.

Jeśli jest dostępne narzędzie do pytań, może przedstawić tę jedną decyzję. W przeciwnym razie zapytaj na czacie. Dostępność narzędzi nie uzasadnia łączenia pytań ani przenoszenia wywiadu do zadania w tle.

## Warunek zakończenia i szablon Design Contract

Zakończ, gdy istotne gałęzie nie mają nierozstrzygniętych zależności blokujących ani ukrytych założeń implementacyjnych. Jeśli Founder zakończy wywiad wcześniej, oznacz kontrakt jako częściowy i ujawnij otwarte decyzje; nie wymyślaj odpowiedzi.

Zwróć w rozmowie zwięzły **Design Contract**, gotowy do wykorzystania w planie implementacji lub `vc-dou`:

- **Cel i zakres:** oczekiwany rezultat i jawne granice.
- **Decyzje:** uzgodnione wybory, odrzucone alternatywy, powody oraz wskazanie źródła: odpowiedź Foundera, dowód z kodu albo propozycja agenta.
- **Architektura i runtime:** własność stanu i kontraktów, punkty wejścia, ścieżka integracji oraz zachowanie przy awarii i odzyskiwaniu.
- **Akceptacja i DoU:** konkretne obserwowalne rezultaty, kroki weryfikacji i wymagane dowody produktowe.
- **Otwarte kwestie:** jawnie odroczone pytania, ich wpływ i właściciel; pytania blokujące utrzymują częściowy status kontraktu.

Wywiad daje kontrakt. Implementacja wynika z zakresu upoważnienia od użytkownika; samo zakończenie wywiadu nie uprawnia do edycji ani publikacji.
