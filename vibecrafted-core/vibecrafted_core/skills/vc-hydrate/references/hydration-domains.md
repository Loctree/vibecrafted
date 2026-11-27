# vc-hydrate — Hydration Domains (1–6)

## Hydration Domains

### Domain 1 — Repository Hydration

Fix repo governance gaps from DoU. Generate contextually appropriate content:

- **LICENSE** — detect project intent (commercial / open-source / dual), pick MIT/Apache-2.0/proprietary
- **CONTRIBUTING.md** — extract from README if present; cover setup, coding standards, PR process, code-of-conduct link
- **CHANGELOG.md** — parse git log for unreleased changes; Keep-a-Changelog format; version headers match published versions
- **SECURITY.md** — standard responsible disclosure template; GitHub Security Advisories preferred
- **CI workflows** — language-detection driven (Rust: cargo check/clippy/test/fmt; Node: lint/test/build; Python: ruff/pytest); always include dependency audit + license check

**Version sync:** `vc-hydrate --floor` checks the checkout. The live comparison (`cargo search`, `npm view`, the site, the channel) is `vc-dou --floor`, and it must be redone after hydrate. A mismatch is a P1 finding; do not close hydrate on the grep alone.

### Domain 2 — Distribution Hydration

Make the product installable without a dev toolchain:

- **CLI Tools (Rust):** `cargo install <name>` works; GitHub Releases with prebuilt binaries (linux-x86_64, macos-arm64, macos-x86_64); install script `curl -sSfL <url> | sh`; Homebrew formula (tap or core); shell completions generated and included. Generate GitHub Actions release workflow: cross-compile targets, GitHub Release assets, auto-update Homebrew formula.
- **Desktop Apps (macOS):** `.app` bundle with proper Info.plist; DMG with background image and Applications symlink; code signing with Developer ID; notarization via notarytool; Homebrew cask formula; Sparkle (or equivalent) for auto-updates. Use `create-dmg` template (`--volname`, `--background dmg-background.png`, `--window-size 600 400`, `--icon-size 100`, `--app-drop-link 400 200`).
- **Web Apps:** Dockerfile, docker-compose.yml for local preview, env-var docs (`.env.example`), health check endpoint (`/health` or `/api/health`), graceful shutdown handling.

### Domain 3 — Discoverability Hydration

Fix SEO and web presence:

**SSR / pre-rendering for SPA sites.** Problem: JS-rendered sites are invisible to crawlers. Solutions in order of preference:

1. Static pre-rendering at build time (best for landing pages)
2. SSR with hydration (for dynamic content)
3. Hybrid: static landing + SPA for app
4. Minimum: `<noscript>` fallback with key content

For Leptos (WASM): enable SSR mode or generate static HTML; pre-render critical routes at build time; ensure `<title>`, `<meta>`, `<h1>` exist in initial HTML.

**Meta tags template** per public page: `<title>{Product} — {Tagline} | {Company}</title>`, meta description (≤155 chars), meta keywords (5-8 relevant), Open Graph set (`og:title`, `og:description`, `og:image`, `og:type=website`), Twitter card set (`twitter:card=summary_large_image`, `twitter:title`, `twitter:description`).

**Security headers (server config):** `Strict-Transport-Security: max-age=63072000; includeSubDomains`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Content-Security-Policy: default-src 'self'`.

**robots.txt + sitemap.xml** — generate from actual URL structure; ensure no duplicate content across domains; submit to Google Search Console (manual step — flag for user).

### Domain 4 — Commercial Surface Hydration

Build the stranger-to-customer path.

**Landing page structure:**

1. Hero: tagline + 1-sentence value prop + primary CTA
2. Problem: pain point in user's words
3. Solution: how product solves it (3 bullets max)
4. Social proof: stats, testimonials, case studies
5. How it works: 3-step visual flow
6. Pricing: clear tiers or "contact us"
7. CTA repeat: same primary CTA

Generate as: Markdown (static site generators), HTML (direct use), copy doc (designer handoff).

**Representation surface scaffolding (mandatory when missing).** If the product is not a web app, Hydrate still scaffolds a presentation surface:

- **Desktop apps** — landing/showcase, screenshots/product shots, "how it works", install path (DMG/MSI/AppImage/Homebrew cask), trust signals (security, local-first, offline, privacy)
- **CLI tools** — landing or docs-style one-pager, command examples, install command, sample output, who-it's-for
- **MCP servers / infra tools** — explainer page, architecture diagram, workflow examples, install + connection path, real-world use cases
- **Internal/hybrid products** — founder-facing showcase, capability summary, screenshots/diagrams/mocks, runtime-vs-presentation explanation

Hydrate should never assume "no website needed" means "no representation needed."

**Marketplace listings:**

For Claude Code Skills Marketplace:

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

For crates.io / npm / PyPI: description (<250 chars, keyword-rich), keywords (5 relevant terms), categories (matching registry), homepage (landing URL), repository (GitHub URL), documentation (docs URL), readme (path).

### Domain 5 — Onboarding Hydration

Create the "first 5 minutes" experience:

- **CLI tools:** install command (one line, copy-pasteable) → first command (immediate value) → "what just happened" → next steps (2-3 progressive commands) → where to get help
- **Web apps:** signup (<3 fields) → onboarding wizard (<5 steps) → sample data or demo mode → quick win within 60s → docs link
- **Skills/plugins:** install command → trigger phrase to test → expected output → customization options

### Domain 6 — Representation Layer Hydration

For products that are real, usable, and valuable but currently invisible from the outside. Build the minimum intentional external-facing surface required for the product to be legible to strangers.

Possible artifacts: `docs/index.html` landing page, one-page static showcase, product one-pager (Markdown/HTML), feature explainer, screenshots/diagram pack, social preview image, concise positioning copy, CTA layer ("install"/"try"/"request access"/"contact").

Recommended structure: product name + 1-line value prop → what it is → who it's for → why it exists → how it works → how to try/install/access → visual proof (screenshots, diagrams, examples).

**This is not optional garnish. It is the product's public face.**
