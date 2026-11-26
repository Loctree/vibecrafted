---
name: vc-guard
version: 1.0.0
description: >
  In-flight enforcer sibling of vc-trust. Inventories existing gates
  (commit-msg, pre-commit, pre-push, loctree-first, classifier hard-stops,
  commit-msg-diff advisory, trust-block dispatch refuse) and ships one
  fail-closed proof path: refuse workflow continuation when the trust journal
  records block for HEAD. Guard never invents settlement letters or re-judges
  claims. Trigger: "guard", "vc-guard", "gate inventory", "refuse on trust block".
loctree_value: "blast radius of gate surfaces and dispatch choke points"
aicx_value: "why gates exist and which race modes they cover"
dogfooding: "required"
---

# vc-guard — egzekutor bramek (nie sędzia)

`vc-guard` to **strażnik**, brat `vc-trust`. Trust obserwuje i osądza po fakcie
na Living Tree. Guard **egzekwuje przy bramce**.

| Rola               | Skill             | Kiedy         | Zmienia kod? | Blokuje dispatch?            | Pisze settlement?              |
| ------------------ | ----------------- | ------------- | ------------ | ---------------------------- | ------------------------------ |
| Sędzia             | `vc-trust`        | po fakcie     | nigdy        | nigdy                        | tak (tylko przez jawne `note`) |
| Egzekutor          | `vc-guard`        | w locie       | nigdy        | **tak** (przy trust `block`) | **nigdy**                      |
| Kształt wiadomości | `commit-msg` hook | przy commicie | nigdy        | tylko commit                 | nigdy                          |

**Nie** mieszaj tych ról. Guard nie powtarza falsyfikacji. Trust nie odmawia
startu.

## Kanoniczna bramka strukturalna

Zanim worker skilla `vc-guard` zinwentaryzuje bramki albo zaraportuje decyzję
egzekucyjną, uruchom lub skonsumuj procedurę `vc-init` dla przypisanego
repozytorium. Ustal branch, HEAD, stan dirty, właściciela runtime'u i ścieżkę
trust journala. Samo `guard check` to wąska decyzja na podstawie journala; nie
zastępuje orientacji w repozytorium.

Używaj `Loctree:loctree` jako domyślnej warstwy strukturalnej, żeby wyprodukować
lub odświeżyć Code-Derived Application Map faktycznej linii egzekucji:
entrypointy hooków, wywołujący `enforce_continuation`, czytelnicy journala,
wąskie gardła dispatchu i możliwe obejścia. Użyj `slice`, `find` i `follow`, żeby
udowodnić te ścieżki, oraz `impact`, zanim orzekniesz o pokryciu bramek. Guard
pozostaje niemutujący: ta mapa wspiera prawdziwą inwentaryzację i evidence pod
odmowę, nigdy objazd w stronę implementacji.

## Wywołanie

```bash
vibecrafted guard <agent> --prompt 'Audit gate inventory and remedium paths'
python -m vibecrafted_core.guard inventory
python -m vibecrafted_core.guard check            # HEAD
python -m vibecrafted_core.guard check --sha <sha>
```

`launch_workflow` woła `enforce_continuation`, chyba że `VIBECRAFTED_GUARD=0`.
Autoryzowana naprawa/admission idzie przez flagi publicznego launchera
`--remediate-trust-block --remediation-task repair|admission --remediation-reason TEXT`.
Nadpisanie ląduje na receipcie i nigdy nie przepisuje journala trust.
`python -m vibecrafted_core.guard check` zostaje BLOCK.

## Doktryna (twarda)

1. **Fail-closed** — gdy dla docelowego commita zapisano trust `block`,
   kontynuacja jest odmówiona. Brak journala ⇒ brak blokady ⇒ przepuść (sędzią
   jest trust; brak osądu nie jest blokadą).
2. **Remedium obowiązkowe** — każda odmowa wypisuje czytelną dla człowieka
   ścieżkę naprawy (który journal, które claimy, jak ponownie zbadać i ponownie
   zanotować).
3. **Bezpieczne bez interakcji** — żadnych promptów na TTY; wyłącznie kody
   wyjścia.
4. **Zakaz wymyślania settlementu** — litery f/x/n pisze wyłącznie
   `vc-trust note` przez istniejące API settlementu
   (`pass→f`, `pass-with-gaps→n`, `block→x`). Guard tylko czyta werdykty z
   journala.
5. **Zakaz forkowania AUTONOMY.md** — operator buttons (push/merge/deploy)
   zostają w charterze autonomii; guard ich nie redefiniuje.
6. **Agent fairness** — commit-msg egzekwuje **kształt** Authored-By; trust
   falsyfikuje **prawdę** o fairness; guard może odmówić, gdy trust zablokował
   linię za naruszenie fairness albo kompletności.

## Inwentarz bramek i relacja do fairness / f-x-n

`vc-guard` inwentaryzuje osiem istniejących bramek w fazach commit, push, agent i dispatch (`commit-msg`, `prepare-commit-msg`, `pre-commit`, `pre-push`, `loctree-first`, `classifier-hard-stops`, `commit-msg-diff-advisory`, `trust-block-dispatch`) bez ich reimplementowania oraz zatrzymuje dispatch na liniach zablokowanych przez `vc-trust` za naruszenie fairness lub kompletności.

Pełna tabela inwentarza bramek, uczciwe luki pokrycia oraz relacja `Living Tree` / `commit-msg` / `vc-trust` / `vc-guard`: [references/gate-inventory.md](references/gate-inventory.md).

## Twarda granica

Guard może pisać wyłącznie:

- własny raport/transcript, gdy działa jako worker skilla;
- tekst remedium na stderr przy odmowie.

Guard nigdy nie edytuje kodu, nie amenduje ani nie rewertuje, nie pushuje, nie
merguje i nie przepisuje trust journali. Nigdy nie awansuje brakującej notatki
trustu na pass.

## Kontrakt raportu

- snapshot inwentarza + luki pokrycia;
- decyzja egzekucyjna dla HEAD (przepuszczone/odmówione) ze ścieżką journala;
- jawne przypomnienie, że litery settlementu pochodzą wyłącznie z notatek
  trustu;
- luki resztkowe.

_𝚅𝚒𝚋𝚎𝚌𝚛𝚊𝚏𝚝𝚎𝚍. with AI Agents by Vetcoders (c)2024-2026 LibraxisAI_
