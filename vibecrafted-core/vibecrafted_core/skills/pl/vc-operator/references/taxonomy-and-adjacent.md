# vc-operator — Taksonomia, Powierzchnie wspierające i Skille pokrewne

## Taksonomia

```yaml
vc-operator:
  kind: orchestration_posture
  scope: interactive_session
  meaning: dispatch, await, synthesize, recover, close waves
  autonomy: orchestration
```

`vc-operator` to nie skill implementacyjny. To postawa dyrygenta dla zaplanowanego
łańcucha pracy.

- `vc-partner` zachowuje i współsteruje pierwotnym kształtem przed pracą strategiczną
  lub w jej trakcie.
- `vc-ownership` prowadzi jeden slice produktowy end-to-end.
- `vc-operator` prowadzi flotę przez plan i zatrzymuje się przy operator button.
- `vc-init` otwiera sesję prawdą repo/runtime'u/intencji; nie jest postawą.

Wywołanie skilla to nie wywołanie runtime'u. Jeśli operator powie `$vc-operator`
wewnątrz bieżącej rozmowy, bieżący agent przyjmuje tę postawę orkiestracji. Osobny
przebieg runtime'u istnieje tylko wtedy, gdy operator lub framework uruchomi
`vibecrafted operator <agent> ...`.

Zobacz [CONTRACT.md](../CONTRACT.md) po wiążący podział postawa/runtime.

## Powierzchnie wspierające (Obowiązkowy punkt wejścia)

Najpierw przeczytaj [RUNNER.md](../RUNNER.md).

`SKILL.md` definiuje postawę. `RUNNER.md` to deterministyczny runbook. Pozostałe
dokumenty to powierzchnie wspierające:

- [FLOW.md](../FLOW.md) - pętla orkiestracji i artefakty.
- [TAXONOMY.md](../TAXONOMY.md) - taksonomia postawy operatora vs runtime'u.
- [FRAME.md](../FRAME.md) - granice ról Worker / Owner / Operator.
- [GUIDE.md](../GUIDE.md) - struktura wave atlas.
- [DISPATCH.md](../DISPATCH.md) oraz [DISPATCH_TEMPLATE.md](../DISPATCH_TEMPLATE.md) -
  kontrakt briefu workera.
- [AWAIT.md](../AWAIT.md) - dyscyplina await/odzyskiwania.
- [AUTONOMY.md](../AUTONOMY.md) - granice autonomii i operator button.
- [JOURNAL.md](../JOURNAL.md) - dziennik operatora tylko do dopisywania.
- [RUNTIME.md](../RUNTIME.md) - kontrakt uruchamiania runtime'u i artefaktów.
- [WHY_MATRIX_TABLE.md](../WHY_MATRIX_TABLE.md) - routing agentów.

## Skille pokrewne

- `vc-init` - wymagany checkpoint orientacji.
- `vc-scaffold` - autorstwo lub przekształcanie planu przed dispatchem.
- `vc-ownership` - każdy worker może działać z ownership wewnątrz swojego slice'a;
  operator jest właścicielem łańcucha.
- `vc-partner` - wspólna strategia, zanim plan stanie się dispatchowalny.
- `vc-marbles` - zbieżność, gdy slice zawodzi na dryfie prawdy.
- `vc-audit` / `vc-review` / `vc-followup` - powierzchnie weryfikacji po falach.
- `vc-release` - dowiezienie na zewnątrz, gdy akcje release'u są dozwolone przez
  plan/sesję lub gdy operator button został naciśnięty.
