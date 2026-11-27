# `vc-followup` — Output Shape & Anti-Patterns

## Output Shape

Default output structure:

1. **Current state** — what exists now and what changed since the last implementation push
2. **What still feels off** — gaps, drift, fragility, unfinished surfaces
3. **Direction verdict** — is the work heading in the right direction or not
4. **Next move** — the highest-leverage continuation

If relevant, explicitly separate:

- code gap
- runtime gap
- architecture / integration gap
- (product-surface gap → tagged for `vc-dou`, not graded here)

## Anti-Patterns

Do not:

- collapse `vc-followup` into a synonym for `vc-review`
- force it to depend on a PR or commit range when the real question is directional
- return only findings without saying whether the current trajectory is healthy
- confuse "there are still gaps" with "the direction is wrong"
- drift into product-surface auditing (packaging, install, SEO, presence) —
  that is `vc-dou`'s frame; followup judges the work's direction, not its shippability
