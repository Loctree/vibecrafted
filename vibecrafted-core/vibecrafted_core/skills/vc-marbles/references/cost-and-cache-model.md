# vc-marbles — Cost Awareness: Cold Start, Hot Loop

## Cost Awareness: Cold Start, Hot Loop

`vc-marbles` looks expensive only when every agent run is counted as a
fresh event. That is the wrong accounting model.

The expensive part is the cold start: reading the repo, reconstructing
intent, finding the real failure surface, and learning where the system
lies. Once that context is hot, repeated marble runs over the same
bounded surface are not waste. They are compression.

Marbles exploits cache heat.

A good marble loop keeps the substrate stable:

- same repository
- same task surface
- same failing gates
- same architectural intent
- same or comparable prompt
- short time distance between runs

This makes each new worker pay less for archaeology and spend more of
its budget on deltas: missed cracks, false fixes, brittle assumptions,
and disagreements between agents.

The goal is not cheap runs. The goal is denser runs.

One isolated agent call gives you one interpretation. A hot marble loop
gives you convergence pressure. When several workers keep pressing the
same surface, the remaining disagreements become signal: either the code
is still lying, or the product truth is smeared.

That is where `vc-polarize` takes over.

Cost rule:

- one cold run discovers the shape
- repeated hot runs expose convergence
- stale loops create noise
- scattered loops destroy cache heat
- `vc-polarize` decides what survives

Do not scatter marble runs across unrelated initiatives. Do not keep
rewriting the target surface unless the operator intentionally resets
the experiment. Marbles works because the swarm keeps pressing against
the same cracks until the false repairs, overfilled gaps, and real
structural decisions become visible.

In short: marbles spend warmed context to buy completeness. Cache heat
makes that completeness cheaper, denser, and comparable across workers.

The excess is deliberate. Marbles fills too much so `vc-polarize` can
cut back to one truth with evidence, not taste.
