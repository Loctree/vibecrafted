# vc-release — Kanon artefaktu, topologia deploya i domyślne reguły proxy

## Kanon artefaktu

**Git/wersjonowanie:** otaguj dokładny commit (`git tag -a v1.2.3 -m "Release 1.2.3"`), push (`git push origin v1.2.3`), obowiązkowy changelog, opublikowana wersja zgadza się z referencjami w repo/badge'ach/docs/stronie.

**Opublikowane wyjścia:** npm (`npm publish` po bumpie wersji), crates.io (`cargo publish`), PyPI (wheel + sdist), GitHub Release (dołącz dokładne artefakty z nudnymi, opisowymi nazwami plików), Docker (otaguj dokładną wersję, opcjonalnie `latest` — nigdy nie dowoź samego `latest` jako tożsamości).

**Nazewnictwo artefaktów:** `myapp-v1.2.3-linux-x86_64.tar.gz` (dobrze) vs `release.zip` (źle).

## Topologia deploya

Wybierz jedną świadomie:

- **Caddy** — solo/mały zespół, kilka prostych upstreamów, automatyczny HTTPS. Domyślne dla webowych MVP, proxy landing+app.
- **Nginx** — już go obsługujesz pewnie, zaawansowane potrzeby reverse-proxy, wiele upstreamów. Dla ustalonych stacków ops, większych posiadłości web/API.
- **Docker** — odtwarzalność, heterogeniczne środowiska, przenośny preview/staging/prod.

**Bezpieczna drabina:** najprostszy realny launch → static hosting lub Caddy. App + worker + db → Docker + reverse proxy. Dojrzała infra → Nginx lub standard platformy. Wybierz najmniejszy uczciwy stack, nie to, co brzmi imponująco.

## Domyślne ustawienia bezpieczeństwa deploya

- Domyślnie binduj usługi aplikacji do `127.0.0.1`; udokumentuj każdy wyjątek `0.0.0.0`
- Terminuj TLS na celowym proxy/ingressie; preferuj reverse proxy nad surowym wystawieniem portu
- Wewnętrzna sieć Dockera zamiast portów publikowanych na hoście dla usług prywatnych
- Wstrzykiwanie env w runtimie, nigdy sekrety wpieczone w obrazy
- Wymagaj endpointu `/health`, graceful shutdown, kontenerów non-root, `.dockerignore` bez sekretów

**Czerwone flagi:** panel admin/debug zbindowany publicznie; publiczna usługa na `:3000`/`:5173`/`:8000` bez proxy/TLS; `CORS *` na uwierzytelnionych API; wyeksponowane stacktrace'y lub bannery frameworka; pliki `.env` lub backupy dostępne z weba.

## Reverse proxy i ekspozycja

Minimalne oczekiwania wobec reverse-proxy:

- nagłówki `Host` i forwardujące zachowane celowo
- wsparcie websocket upgrade, jeśli aplikacja tego potrzebuje
- rozsądne ustawienia timeoutu i rozmiaru body
- redirect `www`/apex zgodnie z decyzją kanoniczną
- redirect 80 -> 443, gdy zamierzony jest publiczny HTTPS

Ekspozycja na publiczny Internet to decyzja, nie domyślny tryb.
