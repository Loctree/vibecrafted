# vc-release — Szczegóły bramki release'u Semgrepa

## Bramka release'u Semgrepa

Semgrep jest częścią kanonu. Nieopcjonalny. Raport release'u musi nieść evidence.

Komenda kanoniczna: `make semgrep` (podpięta tak samo jak lokalne hooki pre-commit/pre-push: `semgrep scan --config auto --error --quiet --exclude-rule html.security.audit.missing-integrity.missing-integrity .`). Hooki mieszkają w `scripts/hooks/`, aktywowane przez `make init-hooks`.

Przed release'em: uruchom `make semgrep` na pełnym repo, zapisz findingi (rule id, severity, plik, zakres linii), klasyfikuj wg **granicy przepływu danych (dataflow boundary)** (nie wg lokalizacji pliku):

- tainted-path / sinki LFI → napraw przy zwalidowanym obiekcie root
- regexy podatne na ReDoS → ograniczone parsowanie lub bezpieczny kształt
- niebezpieczne merge'owanie headerów/obiektów → jawna allowlista + niemutowalna granica wejścia
- konstrukcja command/shell → sparametryzowane wywołanie, nigdy konkatenacja stringów przez niezaufany szew (untrusted seam)

Zablokuj release przy każdym nierozwiązanym blokującym findingu, chyba że użytkownik jawnie akceptuje ryzyko na piśmie wewnątrz raportu.

Minimalne klasy: obejścia auth/authz, niebezpieczna obsługa sekretów, shell/command injection, SSRF, path traversal/LFI, niebezpieczne serwowanie plików, słaba walidacja wejścia na groźnych sinkach, niebezpieczna deserializacja/eval-podobne, regexy ReDoS, niebezpieczne merge'owanie headerów/obiektów, pozostawione włączone endpointy debug/dev frameworka.

Jeśli Semgrep niedostępny, powiedz to jawnie, uruchom `uvx semgrep` (udokumentowany fallback) i zapisz w raporcie, że bramka nie została spełniona. Cisza jest nieakceptowalna.
