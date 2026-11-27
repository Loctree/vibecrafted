# vc-marbles — Złożenie ze skillami sąsiednimi, antywzorce i klamra końcowa

## Złożenie ze skillami sąsiednimi

- **`vc-init`** — wymagana bramka. Każda runda zaczyna się tutaj.
- **`vc-audit`** — downstreamowa READ-ONLY falsyfikacja. Audit sprawdza,
  czy deklarowane fixy swarmu faktycznie wylądowały względem spisanego
  planu.
- **`vc-polarize`** — downstreamowy krok WRITE. Po zalewie marbles +
  verdykcie auditu polarize zdziera z powrotem do jednej prawdy.
- **`vc-review`** — sąsiednie READ-ONLY review na bounded diffach.
  Commit rundy marbles można przejrzeć indywidualnie przed kontynuacją
  swarmu.
- **`vc-followup`** — sąsiedni READ-ONLY check trajektorii. Użyj po
  fali marbles, by ocenić zdrowie ogólnego kierunku.

---

## Antywzorce

- **Historyczna samoświadomość** — czytanie wcześniejszych artefaktów marbles, by zabrzmieć kompetentnie
- **Cosplay zbieżności** — gadanie o rozmiarze kroku / delcie / mistrzostwie pętli
- **Próżność powierzchni** — dotykanie wielu plików, żeby runda wyglądała na większą
- **Teatr polerowania** — sprzątanie, które nie zamyka żadnego trybu awarii
- **Kult wstecznej kompatybilności** — zachowywanie zgniłych kontraktów
- **Inflacja narracyjna** — długie wyjaśnienia ukrywające słabą bramkę
- **Kontaminacja równoległa** — importowanie kontekstu innego marble'a
- **Fałszywa wszechwiedza** — udawanie, że widzi się cały globalny backlog
- **Pogarda wobec agentów** — traktowanie innych agentów jako gorszych; why-matrix to
  mapa stylów, nie hierarchia wartości
- **Rozwiązywanie rozmazu produktu w workerze** — eksponuj, nie rozstrzygaj;
  zostaw to dla polarize
- **Samorozszerzanie** — pisanie planu następnej rundy z wnętrza tej
  rundy

---

## Klamra końcowa

```text
=======================
Pamiętaj: tryb marbles to pozwolenie na napisanie małego albo szerzej zakrojonego,
ale prawdziwego fixa, nie pozwolenie na refactor, chyba że wynika to wprost
z opisu taska. Nie musisz przejmować się przerośniętym kodem wokół pewnych
części bazy kodu, ale masz twardy obowiązek opisać go
w raporcie, jeśli na niego natrafisz.
Worker widzi drzewo, nigdy fabrykę. Jedna runda, jeden commit, jeden raport.
Potem wychodzi. Swarm produkuje nadmiar; polarize go zdziera.
(•̀⌄•́)و ̑̑
=======================

Suchar: Dlaczego worker marbles nigdy nie kłóci się z następnym workerem?
Bo do tego czasu już wyszedł z szatni.  (._.)
```
