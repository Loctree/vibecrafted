# `vc-dou` — Audit Sequence (Phases 1–5)

## Audit Sequence

### Phase 1 — Repo Governance

Required files: `LICENSE`, `README.md` (install/usage/contributing), `CONTRIBUTING.md`,
`CHANGELOG.md`, `.github/workflows/`, `.github/ISSUE_TEMPLATE/`, `SECURITY.md`.

```bash
for f in LICENSE README.md CONTRIBUTING.md CHANGELOG.md SECURITY.md; do
  [ -f "$ROOT/$f" ] && echo "[PASS] $f" || echo "[FAIL] $f MISSING"
done
[ -d "$ROOT/.github/workflows" ] && echo "[PASS] CI" || echo "[FAIL] No CI"
```

Loctree structural check via `repo-view(project)`: dead exports (0 for release),
cycles (0 or documented), health score.

### Phase 2 — Install Path

The "can a stranger use this" test starts with `vc-dou --floor` (see
[the public-surface floor](references/public-surface-floor.md)). The checks
below are the rest of the path, not a substitute for that probe.

- **CLI:** published to registry, version badge matches, `cargo install`/`npm i -g`/`pip install` works,
  binary runs without dev toolchain, `--help` and `--version` work.
- **Desktop:** DMG/MSI/AppImage available, Homebrew formula or equivalent, signed/notarized (macOS).
- **Web:** URL accessible, loads <3s, mobile responsive, graceful no-JS fallback.

### Phase 3 — Presence and Discoverability

For each public URL:

```
1. WebFetch(url, "title, meta description, h1, content summary, CTAs, pricing.
   Report if page appears empty or JS-only.")
2. SSR check: curl -s <url> | grep -c '<h1\|<p\|<main' (< 3 → invisible to crawlers)
3. Security headers: curl -sI <url> | grep -i 'strict-transport\|x-frame\|content-security'
4. OG/Twitter: curl -s <url> | grep -i 'og:\|twitter:card'
```

SEO basics: descriptive title (not "React App"), meta description, H1, no-JS
content, robots.txt, sitemap.xml, no duplicate content across domains.

Search presence:

```
brave-search("<product>")            # appears in top 20?
brave-search("<product> <category>") # category ranking
brave-search("site:<domain>")        # indexed page count
```

**No public web app?** Run a Representation Surface Audit instead:
landing/showcase/one-pager · 30-second explainer · screenshots/diagrams/demos ·
visible install path · narrative not requiring repo access · stranger-comprehensible
without founders. All "no" → `[MISSING]` Presence.

**On `[MISSING]` Presence — generate `./presence/`** (do not just mark and move on):

- `index.html` — name, one-liner, what it does, install command, 3-5 features,
  links (GitHub, docs, registry).
- `styles.css` — dark theme, monospace chrome, clean typography, palette from scaffold or neutral.
- `app.js` — copy button, smooth scroll, fade-up observer. Nothing more.

Rules: minimal but not poor · no frameworks · GitHub Pages deployable · meta tags
(OG/Twitter), favicon, robots.txt, sitemap.xml · no animations beyond fade-up,
no particles, no glow. DoU creates these when nothing exists; decorate polishes;
hydrate packages.

### Phase 4 — Commercial Surface

```
Discovery → Landing → Understanding → Trial → Adoption → Payment
```

Verify each stage. Missing stages = funnel holes. For non-web products, "Landing"
means a landing page, showcase, docs explainer, or explicit representation layer.
No such layer = funnel broken at Landing/Understanding even if the product works.

### Phase 5 — Marketplace Readiness

**Claude Skills Marketplace:** SKILL.md frontmatter (name, version, description) ·
trigger phrases (EN+PL) · `references/` · no hardcoded paths · graceful
optional-dep fallback · clean-install tested.

**GitHub / crates.io / npm:** package metadata complete (description, keywords,
homepage, repo) · categories/tags · screenshots or demo GIF in README ·
license compatible.
