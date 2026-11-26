# vc-release — Domain, SEO, Onboarding, Smoke Verification & Anti-Patterns

## Domain, DNS, Verification

If the product has any public surface, verify: domain registered and intended, DNS to correct target, canonical host (
`www` vs apex), redirects match canonical, TLS resolves cleanly, staging vs prod domains not confused. Also: no stale
preview domains advertised as primary, no mismatched favicon/title/og:image leaking old identity, no broken
`/.well-known/*` paths.

Ownership proofs (when public products need them): Search Console, Bing Webmaster, domain TXT/challenge files, Apple/Google ecosystem `.well-known/` endpoints, any challenge-response proofs required by infra/platforms. If domain ownership proof is required and the challenge path is missing, release is not done.

## SEO and Visibility Canon

Visibility is a hard checklist, not nice-to-have.

- **Page-level**: descriptive `<title>`, meta description, one real `<h1>`, crawlable content in initial HTML or
  truthful fallback, canonical URL, Open Graph + Twitter card tags, correct status code, `noindex` only when
  intentional.
- **Site-level**: `robots.txt`, `sitemap.xml`, canonical host strategy, consistent internal linking, no broken
  docs/marketing links, favicon + social preview assets.
- **Indexability checks**: `curl` page and verify meaningful content without JS; route not blocked by `robots.txt`; meta
  robots not `noindex` unless intentional; canonical points to intended public URL.
- **Domain visibility checks**: docs/landing/CTA all resolve; install instructions point to real public artifacts; social share preview not broken.

If a stranger cannot discover, understand, and try the product quickly, release is incomplete.

## Onboarding Truth

Verify the first-user path: install from published artifacts (not the repo), follow the public quickstart cold, screenshots and demos match reality, app or CLI starts without dev-only assumptions, errors are human-readable.

## Post-Release Smoke Verification

Verify from a **cold path**. The dev machine is not a witness.

Install from the **published artifact** (npm/cargo/PyPI/GitHub Release/Docker registry — never local checkout, never
side-loaded tarball, never dev branch). Then verify: public URL resolves, TLS valid + matches canonical host, health
endpoint passes, core action works end to end, docs and CTA links resolve, published version matches running version,
onboarding screenshots/demos match cold-installer output.

Report must name exact artifact source (registry URL, tag, digest, download URL). "It worked on my repo" does not satisfy this gate.

### Release Report Mandatory Breakdown & Sign-Off

**Mandatory sections:**

1. **Security gate** — command run (`make semgrep` or equivalent), exit status and finding count, per-finding classification (rule id, severity, file, line range, dataflow boundary), resolution per finding (fixed in commit X / accepted with reason / deferred with tracking issue), explicit statement when gate was not actually satisfied.
2. **Exposed surface inventory** — listening ports and bind addresses (default `127.0.0.1`, document every `0.0.0.0`), reverse proxy in front (Caddy/Nginx/cloud LB/none) and where TLS terminates, authentication boundaries per surface, response headers added/stripped at the edge (HSTS, CSP, frame options, CORS allowlist), secret materialization path.
3. **Deployment mode decision** — chosen topology with justification, why it is the smallest honest fit, rollback story (how to revert without manual heroics).
4. **Post-release install smoke** — artifact source (registry URL, tag, digest, download URL — never `file://` from working tree), command sequence executed from clean environment, first-run output evidence (exit code, version banner, health check), any drift between documented quickstart and observed behavior.

**Sign-off** only when all four sections are populated and each has objective evidence attached. A green Semgrep gate without exposed-surface inventory is not a sign-off. A topology decision without a smoke run is not a sign-off. Truth is cumulative.

## Financial / Legal Reality

Hosting and bandwidth costs understood, registry/CDN limits known, LICENSE correct, SECURITY.md exists, privacy policy/terms exist if user data is involved. Do not market proprietary as open source. Do not collect data without saying so.

## Anti-Patterns

- Publishing without `vc-dou`
- Skipping hydration and assuming users will figure it out
- No Semgrep or equivalent security gate
- Exposing services on `0.0.0.0` without deliberate proxy/TLS design
- Broken canonical domain or redirect logic
- Forgetting verification challenge files / TXT records
- Shipping a JS-only empty shell that crawlers cannot understand
- Tagging without a changelog
- Tagging without a GitHub Release (`vc-release --floor --require-release` stays red)
- Calling the ship done while `vc-release --floor` exits `1`
- Deploying without post-release smoke checks
- Treating release as one-time ceremony instead of repeatable discipline
