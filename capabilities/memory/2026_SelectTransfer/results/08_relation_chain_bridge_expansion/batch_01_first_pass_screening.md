# Batch 01 First-Pass Screening

## Purpose

This screening step is inserted before manual subtype annotation to avoid spending annotation effort on obvious false positives created by relation-term prefiltering.

## Outcome

- total filtered candidates reviewed: `15`
- `likely_relation_chain`: `10`
- `needs_manual_read`: `2`
- `obvious_false_positive`: `3`

## Obvious False Positives

- `hp_dev_0028`
  - `"father of modern American shipbuilding"` is an honorific title, not kinship.
- `hp_dev_0198`
  - `"Son of al Qaeda"` is a title match, not a family-relation bridge.
- `hp_dev_0919`
  - `"Father Ted"` is a title match, not a family-relation bridge.

## Manual-Read Boundary Cases

- `hp_dev_0369`
  - likely spouse-based, but may be too close to a direct lookup rather than a stable relation-chain bridge.
- `hp_dev_0907`
  - likely kinship-based, but historical genealogy structure should be checked before subtype assignment.

## Recommendation

Do **not** annotate the raw 15-row batch directly.

Instead:

1. Drop the 3 obvious false positives.
2. Move the remaining 12 rows into a screened annotation subset.
3. Perform subtype annotation only on the screened subset.
4. After annotation, check whether at least 5 stable `relation_chain_bridge` source candidates remain.

## Interpretation

The repaired prefilter is now good enough to continue, but it is still not clean enough to skip a human first-pass screening layer. The current batch should be treated as:

- a **usable feasibility batch**
- not yet a final annotation-ready pool without screening
