# `vc-canary` — Tryb floty

## Tryb floty (duże repozytoria)

Jeden agent na oś (albo na scope karmiący osie), zmienne N z Phase I —
nigdy stała liczba. **Skalo-adaptacyjnie:** gdy jeden plan przytłacza
resztę, potnij go wzdłuż jego własnej podstruktury na uczciwe dla agenta
budżety, a to, co zostaje poza falą, zadeklaruj jako jawnie odroczoną falę
— odroczenie to zapisana decyzja, nie przemilczenie.

Substrat to mechanika, nie osąd: N=1 → Living Tree; N>1 → Fleet Worktrees
jako **formacja Mode B** Living Tree Rule — briefy per-scope są spisanym
planem dispatchu, bramki per-scope wcześniej zadeklarowanymi verifierami,
domeny scope'ów rozłączne, a sesja canary jednowątkowym integratorem.
**Worker sam tworzy swój worktree** od bazy integracji (launcher niczego
nie provisionuje) — przypięte SHA jako zamrożony widok, nie poczekalnia
zmian: radar jest wolny od mutacji, więc nie ma commitów scope'ów do
mergowania; integrator kopiuje pliki dowodowe per-oś
(`.loctree/canary/axes/*.json`, gitignored) z każdego worktree przed
sprzątaniem, a zwrócony JSON workera jest zabezpieczeniem. Nigdy nie
parkuj równoległej floty w jednym wspólnym
checkoucie (stałe polecenie operatora, 2026-08-20). Każdy scope dostaje
własny podkatalog scratchpadu, nazwany w briefie — płaskie wspólne nazwy
w tmp kolidują między równoległymi scope'ami.

Nie cytuj liczb bez przypiętego fingerprinta snapshotu: edycje floty
przesuwają linie i wyzwalają skany przyrostowe, więc liczby `loct follow`
dryfują w locie. Natywne subagenty dziedziczą **model rodzica** (agent
model parity); piny dotyczą tylko workerów zewnętrznych. Hybryda: N≤8
natywnie; N>8 zewnętrznie przez
[await-arming](../../vc-dispatch/references/await-arming.md). Szablon
briefu per-scope:
[references/canary-agent-brief.md](../../vc-canary/references/canary-agent-brief.md).
Pin agenta: user; inaczej ten launcher, który żyje w sesji, w kolejności
`claude` · `codex` · `grok` · `cursor`.
