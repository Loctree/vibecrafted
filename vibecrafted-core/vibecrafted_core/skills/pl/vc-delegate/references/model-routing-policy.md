# vc-delegate — Polityka doboru modeli i ekonomii subagentów

## Polityka natywnej delegacji

Dobieraj model każdego subagenta według ekonomii podzadania (reguła Foundera,
2026-10-03, zastępująca domyślną zgodność tieru z 2026-04-10). Wybierz model
z uzasadnionym marginesem ponad wymagane możliwości i jakość, a potem najbardziej
ekonomiczną opcję spełniającą próg. Reguła dotyczy całej floty, nie tylko Codexa.

- Mechaniczny fan-out (rename, fixture'y, format probes, ograniczone odczyty,
  boilerplate testów): szybki/tani tier. Szeregowa praca na frontier kosztuje
  jednocześnie więcej czasu i pieniędzy.
- Rozumowanie nośne (architektura, trudny debugging, interpretacja kanonu Foundera,
  duży blast radius): tier rodzica lub mocniejszy. Od razu sięgnij po mocniejszy
  model, gdy uzasadnia to niejednoznaczność, głębokość zależności lub skutki błędu.
  Nie wymuszaj próby cheap-first ani nie broń słabego wyniku niższą ceną.
- Eskaluj po wykazanym ograniczeniu, bez automatycznego powtarzania każdego
  ekonomicznego wyniku na mocniejszym modelu.

Ta sama rodzina jest tie-breakerem, nie prawem: zachowuje cache i najbliższy
styl rozumowania. Preferuj ją przy równych możliwościach. Przy zejściu w dół
dla szybkości/dostępności odzyskaj jakość w orkiestracji rodzica.

Dostępność runtime'ów:

- Claude: dla rozległych, długich zadań preferuj opus[1m], dla lżejszych sonnet[1m].
- Gemini: gdy gemini-3.1-pro-preview jest niedostępny lub niestabilny w szczycie,
  użyj auto-gemini-3.
- Etykieta roli subagenta nie dowodzi modelu ani reasoning effort. Potwierdzając
  routing, korzystaj z dostępnych metadanych runtime'u; nie wymagaj pollingu
  po każdym spawnie.
