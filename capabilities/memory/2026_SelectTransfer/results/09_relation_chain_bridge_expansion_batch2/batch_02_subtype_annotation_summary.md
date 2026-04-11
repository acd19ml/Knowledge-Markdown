# Batch 02 Subtype Annotation Summary

Date: 2026-04-11

输入文件：

- [candidate_batch2_for_subtype_annotation.csv](./candidate_batch2_for_subtype_annotation.csv)
- [candidate_batch2_full.json](./candidate_batch2_full.json)
- [../08_relation_chain_bridge_expansion/batch_01_subtype_annotation_summary.md](../08_relation_chain_bridge_expansion/batch_01_subtype_annotation_summary.md)

## Outcome

- screened candidates annotated: `17`
- `relation_chain_bridge + keep`: `10`
- `attribute_bridge + drop`: `4`
- `unclear + drop`: `3`

## High-Quality Keep Candidates

Current Batch 2 produces the following stable `relation_chain_bridge` keeps:

- `hp_dev_1380`
- `hp_dev_7398`
- `hp_dev_1892`
- `hp_dev_2485`
- `hp_dev_4066`
- `hp_dev_4676`
- `hp_dev_5315`
- `hp_dev_6741`
- `hp_dev_6859`
- `hp_dev_7220`

## What Changed Relative to Batch 1

Batch 1 mainly failed because relation terms were too generic. Most candidates collapsed into:

- `attribute_bridge`
- or direct single-hop relation lookup

Batch 2 improves precision in the intended way:

- it surfaces many more cases where the key reasoning step is genuinely **relation-to-relation continuation**
- it sharply reduces cases that only use kinship terms as a gateway to ordinary attribute lookup

## Combined Feasibility Judgment

Batch 1 gave:

- `1` stable `relation_chain_bridge` keep

Batch 2 gives:

- `10` stable `relation_chain_bridge` keeps

Combined total:

- `11` stable keep candidates

This is now comfortably above the minimum `N = 5` threshold.

## Immediate Implication

The project no longer needs another expansion batch.

The correct next step is:

1. construct a minimal `relation_chain_bridge` source set
2. choose 5 non-near-duplicate keeps
3. reroute `wiki_dev_2639` to that new source set
4. only then decide whether a subtype-aware rerun is worth doing

## Recommended Next Step

Move from feasibility check to source-set construction.

Specifically:

- create `rc_bridge_set_01`
- prioritize diversity across:
  - spouse -> sibling
  - spouse -> parent
  - parent -> parent
  - son/daughter -> sibling
  - daughter/wife -> king/motto style historical chain

Do **not** run a third expansion batch.
