# vc-guard — Inwentarz bramek i relacja do fairness / f-x-n

## Inwentarz bramek (nazwane, nie reimplementowane)

| Bramka                     | Faza     | Tryb                                               |
| -------------------------- | -------- | -------------------------------------------------- |
| `commit-msg`               | commit   | twarda — format + trailery + zakaz vendor footerów |
| `prepare-commit-msg`       | commit   | pomocnicza — wypełnia trailery                     |
| `pre-commit`               | commit   | twarda — rodzina ruff/prettier/semgrep             |
| `pre-push`                 | push     | twarda — bramki przy pushu                         |
| `loctree-first`            | agent    | polityka — mapa przed grzebaniem                   |
| `classifier-hard-stops`    | dispatch | polityka — guziki z AUTONOMY                       |
| `commit-msg-diff-advisory` | commit   | zalążek doradczy — claim vs paczka staged          |
| `trust-block-dispatch`     | dispatch | twarda — ścieżka dowodowa tego skilla              |

Luki pokrycia (uczciwie): rozsiewanie hooków na całą flotę, podniesienie bramki
diffowej do twardej, dryf PATH/instalacji, polityka per-branch wykraczająca poza
domyślny HEAD.

## Relacja do agent fairness i kompletności f/x/n

- **Living Tree** dopuszcza równoległe commity; twierdzenia o fairness i tak
  muszą się bronić.
- **commit-msg** czyni wiadomość legalną maszynowo.
- **vc-trust** falsyfikuje, czy legalna wiadomość jest prawdziwa (fairness +
  kompletność + twierdzenia o runtimie) i pisze settlement.
- **vc-guard** powstrzymuje flotę przed kontynuowaniem na linii, którą trust
  zablokował.
