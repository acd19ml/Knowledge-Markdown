# Batch 01 Subtype Annotation Summary

Date: 2026-04-11

输入文件：

- [candidate_batch_for_subtype_annotation_screened.csv](./candidate_batch_for_subtype_annotation_screened.csv)
- [batch_01_first_pass_screening.md](./batch_01_first_pass_screening.md)
- [candidate_batch_full.json](./candidate_batch_full.json)

## Outcome

- screened candidates annotated: `12`
- `relation_chain_bridge + keep`: `1`
- `attribute_bridge + drop`: `7`
- `unclear + drop`: `4`

## Stable Keep Candidate

Only one row currently survives as a stable `relation_chain_bridge` source candidate:

- `hp_dev_0503`
  - `King William IV -> illegitimate daughter Elizabeth -> mother Dorothea Jordan -> birthday`

This is the only case in Batch 1 where the key intermediate step is genuinely **relation-to-relation continuation**, rather than:

- identify a relative
- then read an ordinary attribute from that person

## What Most Candidates Actually Are

Most screened rows still fall into one of two non-target patterns:

### 1. `attribute_bridge`

Examples:

- `hp_dev_0024`: child -> father -> award
- `hp_dev_0124`: daughter -> actress -> film
- `hp_dev_0256`: wife -> actress -> year
- `hp_dev_0832`: son -> footballer -> profession
- `hp_dev_0963`: wife -> actress -> birth year

These are still bridge questions, but they are not the subtype needed for `wiki_dev_2639`.

### 2. direct relation lookup / boundary cases

Examples:

- `hp_dev_0369`: second wife -> businessman
- `hp_dev_0686`: husband -> proper name
- `hp_dev_0789`: entertainer -> daughter
- `hp_dev_0907`: father of Childericus

These contain relation terms, but they do not expose a stable multi-step relation-chain pattern.

## Feasibility Judgment

Batch 1 does **not** provide enough evidence that `HotpotQA` can support a stable `N = 5` `relation_chain_bridge` source set.

Current yield:

- `1 / 12` screened rows survive as stable keep

This is too low to justify immediate source-set construction.

## Immediate Implication

At this point, the project should **not** create a `relation_chain_bridge` source set from Batch 1.

The correct interpretation is:

- `wiki_dev_2639` remains a valid `relation_chain_bridge` target
- but current source-side support for that subtype is still missing

## Recommended Next Step

Choose one of the following, and do not mix them:

1. **Conservative stop**
   - record that current `HotpotQA` evidence is insufficient
   - keep `wiki_dev_2639` only as subtype-mismatch evidence

2. **One more high-precision batch**
   - run a second expansion batch with stricter templates
   - prioritize explicit two-relation wording such as:
     - spouse's father
     - spouse's sibling
     - mother of X's daughter
     - father of Y's son

If a second batch is run, it should be explicitly treated as:

- a final feasibility check
- not an open-ended expansion loop
