# Relation-Chain Consolidation Failure Diagnosis

Date: 2026-04-11

## Target

- `wiki_dev_2639`

## Compared Outputs

- [../10_round1g_run/raw_outputs/r1g_no_memory_wiki_dev_2639.md](../10_round1g_run/raw_outputs/r1g_no_memory_wiki_dev_2639.md)
- [../10_round1g_run/raw_outputs/r1g_episodic_trace_wiki_dev_2639_relevant.md](../10_round1g_run/raw_outputs/r1g_episodic_trace_wiki_dev_2639_relevant.md)
- [../10_round1g_run/raw_outputs/r1g_cross_episode_consolidation_wiki_dev_2639_relevant.md](../10_round1g_run/raw_outputs/r1g_cross_episode_consolidation_wiki_dev_2639_relevant.md)
- [../10_round1g_run/raw_outputs/r1g_cross_episode_consolidation_wiki_dev_2639_irrelevant.md](../10_round1g_run/raw_outputs/r1g_cross_episode_consolidation_wiki_dev_2639_irrelevant.md)
- [../../artifacts/hp_relation_chain_bridge_set_01/cross_episode_consolidation.md](../../artifacts/hp_relation_chain_bridge_set_01/cross_episode_consolidation.md)

## Observed Pattern

### Baseline

- `no_memory` is correct.
- The model takes the spouse branch:
  - Harriet -> husband Thomas Pelham-Holles -> brother Henry Pelham

### Relevant Episodic

- `relevant episodic_trace` is also correct.
- The reasoning remains tied to a local kinship continuation:
  - subject -> spouse -> sibling of spouse

### Relevant Consolidation

- `relevant cross_episode_consolidation` is wrong.
- The output does not contain a valid `## Final Answer` section.
- The reasoning drifts into a meta-analysis of what “sibling-in-law” means and whether Harriet’s own siblings are mentioned.
- The model explicitly references the memory, but the memory appears to push it toward over-general kinship verification rather than the correct spouse-branch continuation.

### Irrelevant Consolidation

- `irrelevant cross_episode_consolidation` is also wrong.
- It stays structurally cleaner than the relevant consolidation, but still concludes that the answer cannot be determined.

## Most Likely Failure Mode

This does **not** look like a simple retrieval failure.

The more plausible failure is:

- the current relation-chain consolidation is too abstract
- its boundary / applicability language encourages over-verification
- the model shifts from:
  - “follow the spouse branch to the named sibling”
  to:
  - “verify whether the queried person’s own siblings are explicitly listed”

That is, the consolidation appears to bias the model toward the wrong branch of the kinship graph.

## Repair Hypothesis

The next repair should not rewrite the whole experiment.

It should only test whether a **more operational, branch-sensitive consolidation** can preserve the correct reasoning path on `wiki_dev_2639`.

Specifically, the revised consolidation should:

- foreground spouse-branch continuation when the query asks for in-law relations
- explicitly warn against collapsing “sibling-in-law” into “spouse of Harriet’s sibling”
- keep boundary statements shorter and less dominant
- preserve structured output stability

## Decision

Round 1h should isolate a single variable:

- revised `relation_chain` consolidation prompt / artifact

and evaluate it only on:

- `wiki_dev_2639`

before any broader rerun.
