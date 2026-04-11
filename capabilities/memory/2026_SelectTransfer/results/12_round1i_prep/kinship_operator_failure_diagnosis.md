# Round 1i Prep: Kinship Operator Failure Diagnosis

Date: 2026-04-11

## Question

After `Round 1h`, what is the narrowest remaining failure on `wiki_dev_2639`?

## Inputs Reviewed

- [../11_round1h_run/round1h_consolidation_results_detail.csv](../11_round1h_run/round1h_consolidation_results_detail.csv)
- [../11_round1h_run/raw_outputs/r1h_no_memory_wiki_dev_2639.md](../11_round1h_run/raw_outputs/r1h_no_memory_wiki_dev_2639.md)
- [../11_round1h_run/raw_outputs/r1h_original_relevant_consolidation_wiki_dev_2639.md](../11_round1h_run/raw_outputs/r1h_original_relevant_consolidation_wiki_dev_2639.md)
- [../11_round1h_run/raw_outputs/r1h_revised_relevant_consolidation_wiki_dev_2639.md](../11_round1h_run/raw_outputs/r1h_revised_relevant_consolidation_wiki_dev_2639.md)
- [../../artifacts/hp_relation_chain_bridge_set_01/cross_episode_consolidation.md](../../artifacts/hp_relation_chain_bridge_set_01/cross_episode_consolidation.md)
- [../11_round1h_run/revised_relation_chain_consolidation.md](../11_round1h_run/revised_relation_chain_consolidation.md)

## Observed Pattern

### 1. Baseline already knows the correct executable path

`no_memory` correctly answers:

- `Harriet -> spouse Thomas Pelham-Holles -> brother Henry Pelham`

So the benchmark context itself is sufficient.

### 2. Original relevant consolidation failed at both formatting and reasoning

`original relevant consolidation` showed:

- explicit memory use
- over-long reasoning
- no stable `## Final Answer`
- drift toward "no siblings are mentioned"

### 3. Revised relevant consolidation fixed formatting but still failed semantically

`revised relevant consolidation` showed:

- stable `## Final Answer`
- shorter reasoning
- but still answered:
  - `Cannot be determined from the provided context.`

This means the current repair improved output control, but not relation interpretation.

## Failure Hypothesis

The narrowest remaining hypothesis is:

**the consolidation still does not correctly normalize the kinship operator in the question.**

More concretely:

- it does not explicitly map `sibling-in-law` to:
  - spouse's sibling
  - sibling's spouse
- it does not prioritize those branches before refusal
- it therefore falls back to a vague family-tree reading

## Why This Matters

If this diagnosis is correct, the next repair should not touch:

- model
- source set
- routing
- scoring

It should touch only:

- the executable interpretation of kinship operators inside the relevant consolidation artifact

## Decision

Proceed to `Round 1i` as a minimal `kinship operator repair` round.

Do **not** full rerun.
