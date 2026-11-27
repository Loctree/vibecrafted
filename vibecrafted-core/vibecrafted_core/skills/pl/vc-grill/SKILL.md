---
name: vc-grill
version: 1.0.0
description: >
  Interactive design and intent interview protocol before code execution or planning.
  Walks down each branch of the decision tree one question at a time, resolving
  dependencies, stating explicit recommendations, and verifying ground truth in the
  codebase before asking. Trigger: "grill me", "vc-grill", "/grill-me", "zrób mi wywiad",
  "przemagluj mnie", "przemagluj plan", "interview me", "rozbij decyzje".
loctree_value: "code truth exploration before asking questions that the codebase already answers"
aicx_value: "historical decisions, past intents, and recorded preferences"
dogfooding: "recommended before complex architectural changes or ambiguous tasks"
---

# vc-grill — Interaktywny wywiad o intencji i projekcie

## Wywołanie

Wywołaj `/vc-grill` lub poproś agenta o użycie `vc-grill` w bieżącej rozmowie.
Prowadź wywiad interaktywnie z Founderem w tej sesji. Ten skill
nie ma launchera CLI, aliasu powłoki ani trybu workera headless.

Używaj go na prośbę lub gdy nieustalona intencja, wybory projektowe albo kompromisy
architektoniczne wymagają wspólnej decyzji. To nie jest obowiązkowy etap każdego
zadania. Znany błąd z jasną naprawą i kryteriami akceptacji można naprawić w ramach
istniejącego upoważnienia bez wywiadu.

## Cel

Osiągnij wspólne, jednoznaczne zrozumienie wyborów architektonicznych,
funkcjonalnych i UX zadania. Przejdź przez każdą istotną gałąź drzewa projektu,
rozwiązując zależności między decyzjami pojedynczo. Fakty zbadaj samodzielnie;
Foundera pytaj o intencje i kompromisy.

## Canonical Orientation Gate

Przy pracy w repozytorium wykonaj `vc-init` lub wykorzystaj jego aktualne dowody
przed pierwszym pytaniem. Użyj `Loctree:loctree`, by zbadać
Code-Derived Application Map: `context`, `focus`, `slice`, `impact`, `find`
i `follow`. Przez AICX odzyskaj wcześniejsze decyzje, intencje i preferencje;
twierdzenia historyczne zweryfikuj w aktualnym kodzie. Wykorzystuj świeże dowody
i odświeżaj konkretną powierzchnię, która uległa zmianie.

Przeczytaj konfigurację, schematy, miejsca wywołań i istotną historię commitów,
zanim zapytasz o obecne zachowanie. Nigdy nie pytaj Foundera, gdzie leży plik
lub jak obecnie działa funkcja, jeżeli repozytorium daje odpowiedź. Przy zadaniu
bez repozytorium zbadaj dostarczone materiały i wskaż brakującą intencję.

## Zasady wywiadu

1. **Najpierw Loctree & AICX.** Ustal prawdę w kodzie przed pytaniem. Pytania
   dotyczą intencji biznesowej, preferencji projektowych, kompromisów
   architektonicznych i nieustalonych zachowań brzegowych. Ujawniaj konflikt
   między zapisaną intencją a dowodami z runtime'u zamiast wybierać po cichu.
2. **Dokładnie jedno pytanie na raz.** Pytaj o jeden węzeł decyzyjny i czekaj
   na odpowiedź przed wejściem w zależną gałąź. Nie wysyłaj kwestionariusza ani
   kilku pytań w jednym wywołaniu narzędzia. Brak odpowiedzi nie oznacza zgody.
3. **Zawsze z rekomendacją.** Każde pytanie zawiera opcje i ich koszty,
   a następnie jawną rekomendację agenta z konkretnym uzasadnieniem.
   Podpisuj własne wnioski; wyłącznie Founder podejmuje decyzje Foundera.
4. **Przechodź po zależnościach.** Zacznij od fundamentów, potem przejdź do
   szczegółów. Śledź rozstrzygnięte i otwarte węzły oraz ich zależności. Wróć
   do wcześniejszego węzła, gdy późniejsza odpowiedź zmieni jego założenia;
   wyjaśnij tę zależność.
5. **Używaj języka odkrywania Foundera.** Polski jest mile widziany. Ustal
   tezę i wymagane dowody przed tłumaczeniem na język materiałów wdrożeniowych.

## Drzewo projektu

Odwiedź nierozstrzygnięte gałęzie w kolejności zależności (pomijając decyzje rozstrzygnięte dowodami lub odpowiedzią Foundera): **1. Zakres i granice** · **2. Architektura i model danych** · **3. Runtime i integracja** · **4. Przypadki brzegowe i awarie** · **5. Weryfikacja i DoU**. Wybieraj węzeł odblokowujący najwięcej zależnych decyzji. Pełny opis gałęzi: [references/protocol-and-contract.md](references/protocol-and-contract.md).

## Protokół kolejnych tur

Przed pierwszym pytaniem zbadaj dowody. W każdej turze nazwij węzeł i wagę wyboru, przedstaw opcje (korzyść i koszt), podaj **Moja rekomendacja (agent)** z uzasadnieniem, zadaj jedno bezpośrednie pytanie i czekaj, potem zapisz odpowiedź ze źródłem. Nigdy nie łącz pytań ani nie przenoś wywiadu w tło. Pełny protokół: [references/protocol-and-contract.md](references/protocol-and-contract.md).

## Warunek zakończenia i Design Contract

Zakończ, gdy brak nierozstrzygniętych zależności blokujących lub ukrytych założeń (przy wcześniejszym końcu oznacz kontrakt jako częściowy i wskaż otwarte kwestie bez zmyślania odpowiedzi). Zwróć zwięzły **Design Contract** (Cel i zakres · Decyzje ze źródłem · Architektura i runtime · Akceptacja i DoU · Otwarte kwestie); zakończenie wywiadu nie uprawnia jeszcze do edycji ani publikacji. Szablon: [references/protocol-and-contract.md](references/protocol-and-contract.md).

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
