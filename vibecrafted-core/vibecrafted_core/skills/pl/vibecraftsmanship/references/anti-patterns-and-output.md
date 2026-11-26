# Vibecraftsmanship — Referencja antywzorców i stylu wyjścia

## Antywzorce

- **Dryf w locie** bez nazwania go: operator zauważa agenta w złej postawie, ale nie
  koryguje → zmarnowane cykle dispatchu
- **Szacowanie w konwencjonalnych osobodniach (ED)** bez świadomości empirycznej
  kompresji → błędne decyzje o zakresie
- **Rankowanie-gdy-prawdą-była-równa-intensywność**: agent narzuca
  primary/secondary/tertiary na równoległe opcje operatora
- **Odgrywanie poszukiwań**: dispatchowanie 3 agentów, gdy 1 to właściwa odpowiedź,
  albo 1, gdy 3 perspektywy wyłapałyby martwy punkt
- **Pomijanie sprawdzenia przetrwania**: ogłaszanie gotowości bez zielonej bramki +
  wylądowanego commita + kontaktu z rzeczywistością
- **Uruchamianie karty taktycznej bez decyzji o postawie**: wskakiwanie w vc-operator,
  gdy pracą był 1 slice (vc-ownership) albo wspólna decyzja (vc-partner)
- **Briefy dłuższe niż lądujące commity**: operator-agent pisze rozwlekłą ceremonię,
  ale workery dowożą więcej LOC, niż wyjaśniają briefy — odwróć proporcję
- **Zapominanie, że techniki są ortogonalne**: marbles/research/audit/review/polarize/prune
  to narzędzia dostępne w KAŻDEJ postawie, nie same wybory postawy

## Styl wyjścia

Domyślnie: powiedz, która oś jest aktualnie nośna dla następnego ruchu. Przykłady:

- „Decyzja gustu: wybiera operator. Opcje na stole: A, B, C z trade-offami."
- „Decyzja siły: poszukiwania niedostatecznie zbadane. Spawnowanie triple-research."
- „Decyzja rzeczywistości: commity wylądowały, ale bramki czerwone — przetrwania jeszcze nie ma."

Gdy wszystkie trzy są wyrównane, zadeklaruj to: „Triada wyrównana, można dispatchować.
Postawa: operator. Karta taktyczna: vc-operator. Go."
