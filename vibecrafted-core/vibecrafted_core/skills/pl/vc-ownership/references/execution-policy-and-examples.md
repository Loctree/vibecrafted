# vc-ownership — Sterowanie desktopem, polityka agentów, styl wyjścia, antywzorce i przykłady

## Sterowanie desktopem i przeglądarką

Gdy środowisko i narzędzia na to pozwalają, tryb ownership może obejmować bezpośrednią
interakcję z aplikacjami, przeglądarkami lub desktopem.

Przykłady:

- przeklikiwanie lokalnej aplikacji, by zweryfikować UX
- prowadzenie flowów opartych na przeglądarce
- przechwytywanie screenshotów lub screencastów
- walidacja ścieżki pakowania lub onboardingu end-to-end

Używaj tej mocy pragmatycznie, nie teatralnie.
Chodzi o domknięcie pętli z rzeczywistością.

Preferuj najbezpieczniejszą skuteczną dostępną metodę:

1. automatyzację app-native/browser-native
2. deterministyczne lokalne narzędzia
3. systemową automatyzację klikania tylko wtedy, gdy potrzebna

Nigdy nie zaskakuj użytkownika szerokimi akcjami desktopowymi poza scope'em taska.

## Polityka agentów

Tryb ownership zachęca do delegacji, ale nie do abdykacji.

Używaj swarmów agentów, gdy dają nam jedno z tych:

- rozumowanie porównawcze
- szybszą równoległą implementację
- niezależny review
- pętle zbieżności

Trzymaj się tych reguł:

- główny wątek jest właścicielem strategii
- raporty biją vibe'y
- jeden wznowiony agent może zespawnować jednego bounded helpera, jeśli kontrolujący skill na to pozwala
- synteza zostaje w głównym wątku

## Styl wyjścia

Raportując postęp lub ukończenie w trybie ownership, domyślnie stosuj:

- **Stan obecny** — co było złe lub niekompletne
- **Propozycja** — mocniejszy kształt, który wybraliśmy
- **Wykonanie** — co zmieniliśmy i zweryfikowaliśmy
- **Otwarte ryzyka** — co wciąż ma znaczenie
- **Następny ruch** — kontynuacja o najwyższej dźwigni

Jeśli task jest prosty, skompresuj to. Jeśli task jest szeroki, trzymaj strukturę.

## Antywzorce

Nie rób w trybie ownership tego:

- kodowania samodzielnie domyślnie
- zadawania pytań bez ustawienia `cron` lub podobnego dostępnego
  narzędzia, gdy użytkownik jest nieobecny
- proszenia użytkownika o mikrozarządzanie oczywistymi decyzjami
- zachowywania złej architektury tylko dlatego, że już istnieje
- zatrzymywania się na kodzie przy pozostawionej niedokończonej powłoce produktu
- tworzenia dodatkowych systemów, gdy wystarczyłby jeden ostry rewrite
- ogłaszania wow effectu i dostarczania placeholdera
- ogłaszania done, zanim review/followup/audit/DoU sprawdzi wynik

## Przykłady

**Przykład 1:**
Wejście: „Muszę wyjść na 5 godzin. Ten `<feature>` mamy dobrze i dokładnie omówiony.
Przejmij ster i dowieź go autonomicznie.
Wyjście: Ustaw 15-20-minutowy heartbeat i potwierdź zrozumienie, a potem
zaimplementuj `$feature` dokładnie albo zadaj pytania doprecyzowujące w
jednym zbiorczym zestawie. Jeśli nie ma odpowiedzi, kontynuuj wybranymi workflowami
autonomicznie, aż cel zostanie osiągnięty.

**Przykład 2:**
Wejście: „You drive. Chcę, żeby ten lokalny stack AI czuł się production-ready."
Wyjście: zdiagnozuj prawdę runtime'u, wybierz architekturę, użyj agentów tam, gdzie przydatne, zaimplementuj, przetestuj, spakuj i zaraportuj
następny realny blocker.

**Przykład 3:**
Wejście: „Od a do z, z wow efektem."
Wyjście: zinterpretuj to jako mandat do dostarczenia end-to-end ze śmiałymi, ale gustownymi decyzjami, a nie żądanie
dekoracyjnej waty.
