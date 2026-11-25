# vc-release — Domena, SEO, onboarding, smoke weryfikacja i antywzorce

## Domena, DNS, weryfikacja

Jeśli produkt ma jakąkolwiek publiczną powierzchnię, zweryfikuj: domena zarejestrowana i zamierzona, DNS na właściwy target, kanoniczny host (
`www` vs apex), redirecty zgadzają się z kanonem, TLS rozwiązuje się czysto, domeny staging vs prod nie pomieszane. Także: żadnych nieaktualnych domen preview reklamowanych jako główne, żadnego niepasującego favicona/title/og:image wyciekającego starą tożsamość, żadnych zepsutych ścieżek
`/.well-known/*`.

Dowody własności (gdy publiczne produkty ich potrzebują): Search Console, Bing Webmaster, pliki TXT/challenge domeny, endpointy `.well-known/` ekosystemu Apple/Google, wszelkie proofy challenge-response wymagane przez infrę/platformy. Jeśli dowód własności domeny jest wymagany, a ścieżka challenge jest nieobecna, release nie jest skończony.

## Kanon SEO i widoczności

Widoczność to twardy checklist, nie nice-to-have.

- **Poziom strony**: opisowy `<title>`, meta description, jeden prawdziwy `<h1>`, crawlable content w początkowym HTML lub
  prawdziwy fallback, kanoniczny URL, tagi Open Graph + Twitter card, poprawny status code, `noindex` tylko gdy
  zamierzony.
- **Poziom strony (site)**: `robots.txt`, `sitemap.xml`, strategia kanonicznego hosta, spójne linkowanie wewnętrzne, żadnych zepsutych
  linków docs/marketing, favicon + assety social preview.
- **Sprawdzenia indeksowalności**: `curl` strony i weryfikacja sensownej treści bez JS; route nieblokowany przez `robots.txt`; meta
  robots nie `noindex`, chyba że zamierzone; canonical wskazuje na zamierzony publiczny URL.
- **Sprawdzenia widoczności domeny**: docs/landing/CTA wszystkie się rozwiązują; instrukcje instalacji wskazują na realne publiczne artefakty; podgląd social share nie jest zepsuty.

Jeśli obcy nie potrafi szybko odkryć, zrozumieć i wypróbować produktu, release jest niekompletny.

## Prawda onboardingu

Zweryfikuj ścieżkę pierwszego użytkownika: instalacja z opublikowanych artefaktów (nie z repo), przejście publicznego quickstartu na zimno, screenshoty i dema zgodne z rzeczywistością, app lub CLI startuje bez założeń dev-only, błędy są czytelne dla człowieka.

## Smoke weryfikacja po release'ie

Weryfikuj z **zimnej ścieżki**. Maszyna deweloperska nie jest świadkiem.

Zainstaluj z **opublikowanego artefaktu** (npm/cargo/PyPI/GitHub Release/registry Dockera — nigdy lokalny checkout, nigdy
side-loadowany tarball, nigdy gałąź dev). Następnie zweryfikuj: publiczny URL się rozwiązuje, TLS ważny + zgodny z kanonicznym hostem, endpoint health
przechodzi, kluczowa akcja działa end to end, linki docs i CTA się rozwiązują, opublikowana wersja zgadza się z uruchomioną wersją,
screenshoty/dema onboardingu zgodne z wyjściem instalatora na zimno.

Raport musi nazwać dokładne źródło artefaktu (URL rejestru, tag, digest, URL pobierania). „Działało na moim repo" nie spełnia tej bramki.

Każdy przebieg `vc-release` musi wyprodukować raport z faktycznym evidence. Nie można uczciwie powiedzieć „done" bez czterech obowiązkowych sekcji poniżej. Jeśli którejś brakuje, release jest **zablokowany**, dopóki nie zostanie wypełniona lub użytkownik nie zaakceptuje luki na piśmie.

### Szczegółowy rozkład raportu i sign-off

**Obowiązkowe sekcje:**

1. **Bramka bezpieczeństwa** — uruchomiona komenda (`make semgrep` lub odpowiednik), status wyjścia i liczba findingów, klasyfikacja per finding (rule id, severity, plik, zakres linii, granica przepływu danych), rozwiązanie per finding (naprawione w commicie X / zaakceptowane z powodem / odroczone z issue trackującym), jawne stwierdzenie, gdy bramka faktycznie nie została spełniona.
2. **Inwentarz wyeksponowanej powierzchni** — nasłuchujące porty i adresy bind (domyślnie `127.0.0.1`, udokumentuj każdy `0.0.0.0`), reverse proxy z przodu (Caddy/Nginx/cloud LB/brak) i gdzie terminuje się TLS, granice uwierzytelniania per powierzchnia, nagłówki odpowiedzi dodawane/zdejmowane na brzegu (HSTS, CSP, frame options, allowlista CORS), ścieżka materializacji sekretów.
3. **Decyzja o trybie deploya** — wybrana topologia z uzasadnieniem, dlaczego to najmniejsze uczciwe dopasowanie, historia rollbacku (jak cofnąć bez ręcznych bohaterstw).
4. **Smoke instalacji po release'ie** — źródło artefaktu (URL rejestru, tag, digest, URL pobierania — nigdy `file://` z drzewa roboczego), sekwencja komend wykonana z czystego środowiska, evidence z pierwszego uruchomienia (exit code, banner wersji, health check), wszelki dryf między udokumentowanym quickstartem a zaobserwowanym zachowaniem.

**Sign-off/zatwierdzenie** tylko gdy wszystkie cztery sekcje są wypełnione i każda ma dołączone obiektywne evidence. Zielona bramka Semgrepa bez inwentarza wyeksponowanej powierzchni to nie sign-off. Decyzja o topologii bez przebiegu smoke to nie sign-off. Prawda jest kumulatywna.

## Realia finansowe / prawne

Koszty hostingu i transferu zrozumiane, limity rejestru/CDN znane, LICENSE poprawny, SECURITY.md istnieje, polityka prywatności/regulamin istnieją, jeśli w grę wchodzą dane użytkownika. Nie marketinguj własnościowego jako open source. Nie zbieraj danych bez powiedzenia o tym.

## Antywzorce

- Publikowanie bez `vc-dou`
- Pomijanie hydracji i zakładanie, że użytkownicy sami sobie poradzą
- Brak Semgrepa lub równoważnej bramki bezpieczeństwa
- Wystawianie usług na `0.0.0.0` bez celowego projektu proxy/TLS
- Zepsuta logika kanonicznej domeny lub redirectów
- Zapominanie o plikach wyzwań weryfikacyjnych / rekordach TXT
- Dowiezienie pustej skorupy tylko z JS, której crawlery nie rozumieją
- Tagowanie bez changeloga
- Deployowanie bez sprawdzeń smoke po release'ie
- Traktowanie release'u jako jednorazowej ceremonii zamiast powtarzalnej dyscypliny
