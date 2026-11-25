# `vc-dou` — Sekwencja audytu (Fazy 1–5)

## Sekwencja audytu

### Faza 1 — Zarządzanie repo

Wymagane pliki: `LICENSE`, `README.md` (install/usage/contributing), `CONTRIBUTING.md`,
`CHANGELOG.md`, `.github/workflows/`, `.github/ISSUE_TEMPLATE/`, `SECURITY.md`.

```bash
for f in LICENSE README.md CONTRIBUTING.md CHANGELOG.md SECURITY.md; do
  [ -f "$ROOT/$f" ] && echo "[PASS] $f" || echo "[FAIL] $f MISSING"
done
[ -d "$ROOT/.github/workflows" ] && echo "[PASS] CI" || echo "[FAIL] No CI"
```

Strukturalny check Loctree przez `repo-view(project)`: martwe eksporty (0 dla
release'u), cykle (0 lub udokumentowane), health score.

### Faza 2 — Ścieżka instalacji

Test „czy obcy potrafi tego użyć".

- **CLI:** opublikowane do rejestru, badge wersji się zgadza, `cargo install`/`npm i -g`/`pip install` działa,
  binarka uruchamia się bez dev toolchainu, `--help` i `--version` działają.
- **Desktop:** dostępne DMG/MSI/AppImage, formuła Homebrew lub odpowiednik, signed/notarized (macOS).
- **Web:** URL dostępny, ładuje się <3s, responsywność mobilna, łagodny fallback no-JS.

### Faza 3 — Obecność i odkrywalność

Dla każdego publicznego URL-a:

```
1. WebFetch(url, "title, meta description, h1, content summary, CTAs, pricing.
   Report if page appears empty or JS-only.")
2. SSR check: curl -s <url> | grep -c '<h1\|<p\|<main' (< 3 → invisible to crawlers)
3. Security headers: curl -sI <url> | grep -i 'strict-transport\|x-frame\|content-security'
4. OG/Twitter: curl -s <url> | grep -i 'og:\|twitter:card'
```

Podstawy SEO: opisowy title (nie „React App"), meta description, H1, treść no-JS,
robots.txt, sitemap.xml, brak duplicate content między domenami.

Obecność w wyszukiwarce:

```
brave-search("<product>")            # appears in top 20?
brave-search("<product> <category>") # category ranking
brave-search("site:<domain>")        # indexed page count
```

**Brak publicznej aplikacji webowej?** Zamiast tego uruchom Representation Surface Audit:
landing/showcase/one-pager · 30-sekundowy explainer · screenshoty/diagramy/dema ·
widoczna ścieżka instalacji · narracja niewymagająca dostępu do repo · zrozumiałe dla
obcego bez founderów. Wszystkie „nie" → `[MISSING]` Presence.

**Przy `[MISSING]` Presence — wygeneruj `./presence/`** (nie tylko oznacz i jedź dalej):

- `index.html` — nazwa, one-liner, co robi, komenda instalacji, 3-5 features,
  linki (GitHub, docs, registry).
- `styles.css` — ciemny motyw, monospace chrome UI, czysta typografia, paleta ze scaffoldu lub neutralna.
- `app.js` — przycisk copy, smooth scroll, observer fade-up. Nic więcej.

Zasady: minimalnie, ale nie ubogo · brak frameworków · deployowalne na GitHub Pages · meta tagi
(OG/Twitter), favicon, robots.txt, sitemap.xml · brak animacji poza fade-up,
brak particles, brak glow. DoU tworzy je, gdy nic nie istnieje; decorate poleruje;
hydrate pakuje.

### Faza 4 — Powierzchnia komercyjna

```
Discovery → Landing → Understanding → Trial → Adoption → Payment
```

Zweryfikuj każdy etap. Brakujące etapy = dziury w lejku. Dla produktów nie-webowych
„Landing" oznacza landing page, showcase, explainer w dokumentacji lub jawną warstwę
reprezentacji. Brak takiej warstwy = lejek zepsuty na Landing/Understanding, nawet jeśli
produkt działa.

### Faza 5 — Gotowość do marketplace

**Claude Skills Marketplace:** frontmatter SKILL.md (name, version, description) ·
trigger phrases (EN+PL) · `references/` · brak hardkodowanych ścieżek · łagodny
fallback opcjonalnych zależności · przetestowany clean-install.

**GitHub / crates.io / npm:** kompletne metadane pakietu (description, keywords,
homepage, repo) · kategorie/tagi · screenshoty lub demo GIF w README ·
kompatybilna licencja.
