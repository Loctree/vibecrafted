# vc-hydrate — Domeny hydrate (1–6)

## Domeny hydrate

### Domena 1 — Hydrate repo

Domknij luki w zarządzaniu repo wykryte przez DoU. Wygeneruj treść adekwatną do kontekstu:

- **LICENSE** — wykryj intencję projektu (komercyjny / open-source / dual), wybierz MIT/Apache-2.0/proprietary
- **CONTRIBUTING.md** — wyciągnij z README, jeśli istnieje; pokryj setup, standardy kodowania, proces PR, link do code-of-conduct
- **CHANGELOG.md** — sparsuj git log pod kątem niewydanych zmian; format Keep-a-Changelog; nagłówki wersji zgodne z opublikowanymi wersjami
- **SECURITY.md** — standardowy szablon responsible disclosure; preferowane GitHub Security Advisories
- **Workflow CI** — sterowane wykrywaniem języka (Rust: cargo check/clippy/test/fmt; Node: lint/test/build; Python: ruff/pytest); zawsze dołącz audyt zależności + sprawdzenie licencji

**Sync wersji:** `grep -rn "version" Cargo.toml package.json pyproject.toml`, a następnie porównaj z opublikowanymi wersjami (`cargo search`, `npm view`) oraz badge'ami/referencjami na stronie. Niezgodność → finding P1.

### Domena 2 — Hydrate dystrybucji

Spraw, by produkt dało się zainstalować bez dev toolchaina:

- **Narzędzia CLI (Rust):** `cargo install <name>` działa; GitHub Releases z prekompilowanymi binarkami (linux-x86_64, macos-arm64, macos-x86_64); skrypt instalacyjny `curl -sSfL <url> | sh`; formuła Homebrew (tap lub core); wygenerowane i dołączone shell completions. Wygeneruj workflow release'u GitHub Actions: cele cross-compile, assety GitHub Release, auto-aktualizacja formuły Homebrew.
- **Aplikacje desktopowe (macOS):** bundle `.app` z poprawnym Info.plist; DMG z obrazem tła i symlinkiem do Applications; code signing z Developer ID; notaryzacja przez notarytool; formuła cask Homebrew; Sparkle (lub odpowiednik) do auto-aktualizacji. Użyj szablonu `create-dmg` (`--volname`, `--background dmg-background.png`, `--window-size 600 400`, `--icon-size 100`, `--app-drop-link 400 200`).
- **Aplikacje webowe:** Dockerfile, docker-compose.yml do lokalnego podglądu, dokumentacja env-var (`.env.example`), endpoint health check (`/health` lub `/api/health`), obsługa graceful shutdown.

### Domena 3 — Hydrate odkrywalności

Napraw SEO i obecność w sieci:

**SSR / pre-rendering dla stron SPA.** Problem: strony renderowane w JS są niewidoczne dla crawlerów. Rozwiązania w kolejności preferencji:

1. Statyczny pre-rendering na etapie buildu (najlepsze dla landing page'y)
2. SSR z hydration (dla treści dynamicznej)
3. Hybryda: statyczny landing + SPA dla aplikacji
4. Minimum: fallback `<noscript>` z kluczową treścią

Dla Leptos (WASM): włącz tryb SSR lub wygeneruj statyczny HTML; pre-renderuj krytyczne trasy na etapie buildu; zapewnij, że `<title>`, `<meta>`, `<h1>` istnieją w początkowym HTML.

**Szablon meta tagów** na każdą publiczną stronę: `<title>{Product} — {Tagline} | {Company}</title>`, meta description (≤155 znaków), meta keywords (5-8 trafnych), zestaw Open Graph (`og:title`, `og:description`, `og:image`, `og:type=website`), zestaw Twitter card (`twitter:card=summary_large_image`, `twitter:title`, `twitter:description`).

**Nagłówki bezpieczeństwa (konfiguracja serwera):** `Strict-Transport-Security: max-age=63072000; includeSubDomains`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Content-Security-Policy: default-src 'self'`.

**robots.txt + sitemap.xml** — wygeneruj z rzeczywistej struktury URL; zapewnij brak zduplikowanej treści między domenami; zgłoś do Google Search Console (krok ręczny — oflaguj dla użytkownika).

### Domena 4 — Hydrate powierzchni komercyjnej

Zbuduj ścieżkę od obcego do klienta.

**Struktura landing page:**

1. Sekcja hero: tagline + 1-zdaniowy value prop + główne CTA
2. Problem: pain point słowami użytkownika
3. Rozwiązanie: jak produkt go rozwiązuje (maks. 3 punkty)
4. Social proof: statystyki, opinie, case studies
5. Jak to działa: 3-krokowy flow wizualny
6. Cennik: jasne tiery lub „contact us"
7. Powtórka CTA: to samo główne CTA

Wygeneruj jako: Markdown (statyczne generatory stron), HTML (bezpośrednie użycie), dokument copy (handoff do projektanta).

**Scaffold powierzchni reprezentacji (obowiązkowy, gdy brakuje).** Jeśli produkt nie jest aplikacją webową, Hydrate i tak tworzy scaffold powierzchni prezentacji:

- **Aplikacje desktopowe** — landing/showcase, zrzuty ekranu / product shoty, „jak to działa", ścieżka instalacji (DMG/MSI/AppImage/cask Homebrew), sygnały zaufania (bezpieczeństwo, local-first, offline, prywatność)
- **Narzędzia CLI** — landing lub one-pager w stylu docs, przykłady komend, komenda instalacji, przykładowe wyjście, dla-kogo-to-jest
- **Serwery MCP / narzędzia infra** — strona objaśniająca, diagram architektury, przykłady workflow, ścieżka instalacji i podłączenia, realne przypadki użycia
- **Produkty wewnętrzne/hybrydowe** — showcase skierowany do founderów, podsumowanie możliwości, zrzuty ekranu / diagramy / mockupy, objaśnienie runtime vs warstwa prezentacji

Hydrate nigdy nie powinno zakładać, że „nie potrzeba strony" oznacza „nie potrzeba reprezentacji".

**Listingi marketplace:**

Dla Claude Code Skills Marketplace:

```markdown
# {Skill Name}

{One-line description}

## What it does

{2-3 sentences explaining the value}

## When to use

{Bullet list of trigger scenarios}

## How it works

{Brief technical explanation}

## Requirements

- {Required tools/dependencies}
- {Optional enhancements}

## Part of

{Suite name} — {suite description}
```

Dla crates.io / npm / PyPI: description (<250 znaków, bogaty w słowa kluczowe), keywords (5 trafnych terminów), categories (zgodne z rejestrem), homepage (URL landinga), repository (URL GitHuba), documentation (URL docs), readme (ścieżka).

### Domena 5 — Hydrate onboardingu

Stwórz pierwsze 5 minut użytkownika:

- **Narzędzia CLI:** komenda instalacji (jedna linia, do skopiowania) → pierwsza komenda (natychmiastowa wartość) → „co się właśnie stało" → kolejne kroki (2-3 progresywne komendy) → gdzie szukać pomocy
- **Aplikacje webowe:** rejestracja (<3 pola) → kreator onboardingu (<5 kroków) → dane przykładowe lub tryb demo → quick win w ciągu 60s → link do docs
- **Skille/wtyczki:** komenda instalacji → fraza triggerująca do przetestowania → oczekiwane wyjście → opcje personalizacji

### Domena 6 — Hydrate warstwy reprezentacji

Dla produktów, które są realne, używalne i wartościowe, ale obecnie niewidoczne z zewnątrz. Zbuduj minimalną, zamierzoną powierzchnię widoczną z zewnątrz, niezbędną, by produkt był czytelny dla obcych.

Możliwe artefakty: landing page `docs/index.html`, jednostronicowy statyczny showcase, one-pager produktu (Markdown/HTML), feature explainer, paczka zrzutów ekranu / diagramów, obrazek social preview, zwięzłe copy pozycjonujące, warstwa CTA („install"/„try"/„request access"/„contact").

Zalecana struktura: nazwa produktu + 1-liniowy value prop → czym jest → dla kogo jest → po co istnieje → jak działa → jak wypróbować/zainstalować/uzyskać dostęp → dowód wizualny (zrzuty ekranu, diagramy, przykłady).

**To nie jest opcjonalny ornament. To publiczna powierzchnia produktu.**
