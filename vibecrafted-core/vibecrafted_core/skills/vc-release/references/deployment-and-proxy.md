# vc-release — Artifact Canon, Deployment Topology & Proxy Defaults

## Artifact Canon

**Git/versioning:** tag exact commit (`git tag -a v1.2.3 -m "Release 1.2.3"`), push (`git push origin v1.2.3`), mandatory changelog, published version matches repo/badges/docs/website refs.

**Published outputs:** npm (`npm publish` after version bump), crates.io (`cargo publish`), PyPI (wheel + sdist), GitHub Release (attach exact artifacts with boring descriptive filenames), Docker (tag exact version, optionally `latest` — never ship `latest` alone as identity).

**Artifact naming:** `myapp-v1.2.3-linux-x86_64.tar.gz` (good) vs `release.zip` (bad).

## Deployment Topology

Pick one intentionally:

- **Caddy** — solo/small team, few simple upstreams, automatic HTTPS. Default for MVP web apps, landing+app proxy.
- **Nginx** — already operating it confidently, advanced reverse-proxy needs, many upstreams. For established ops stacks, larger web/API estates.
- **Docker** — reproducibility, heterogeneous environments, portable preview/staging/prod.

**Safe ladder:** simplest real launch → static hosting or Caddy. App + worker + db → Docker + reverse proxy. Mature infra → Nginx or platform standard. Choose the smallest honest stack, not what sounds impressive.

## Deployment Safety Defaults

- Bind app services to `127.0.0.1` by default; document every `0.0.0.0` exception
- Terminate TLS at a deliberate proxy/ingress; prefer reverse proxy over raw port exposure
- Internal Docker network over host-published ports for private services
- Environment injection at runtime, never secrets baked into images
- Require `/health` endpoint, graceful shutdown, non-root containers, `.dockerignore` with no secrets

**Red flags:** admin/debug panel bound publicly; public service on `:3000`/`:5173`/`:8000` without proxy/TLS; `CORS *` on authenticated APIs; stacktraces or framework banners exposed; `.env` or backup files web-accessible.

## Reverse Proxy and Exposure

Minimum reverse-proxy expectations:

- `Host` and forwarding headers preserved intentionally
- websocket upgrade support if the app needs it
- sane timeout and body-size settings
- redirect `www`/apex according to canonical decision
- 80 -> 443 redirect when public HTTPS is intended

Public internet exposure is a decision, not a default.
