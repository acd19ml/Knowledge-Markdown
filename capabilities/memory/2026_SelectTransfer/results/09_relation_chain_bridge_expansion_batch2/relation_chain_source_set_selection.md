# Relation-Chain Source Set Selection

Date: 2026-04-11

基于 [batch_02_subtype_annotation_summary.md](./batch_02_subtype_annotation_summary.md) 的结果，当前已可以从 Batch 2 的 `relation_chain_bridge + keep` 候选中构造一个最小 draft source set。

## Selected Draft Set

`hp_relation_chain_bridge_set_01`

成员：

- `hp_dev_7398`
- `hp_dev_2485`
- `hp_dev_1892`
- `hp_dev_5315`
- `hp_dev_7220`

## Why These 5

选择标准不是“最容易做”，而是尽量覆盖不同的 relation-chain family，同时避免明显近重复。

### `hp_dev_7398`

- pattern: `wife -> brother`
- value: clean spouse-to-sibling chain with person answer

### `hp_dev_2485`

- pattern: `husband -> mother`
- value: clean spouse-to-parent chain

### `hp_dev_1892`

- pattern: `father -> mother`
- value: parent-to-parent chain rather than spouse-based chain

### `hp_dev_5315`

- pattern: `son -> younger sister`
- value: child-to-sibling chain, different from the three genealogy-like historical cases

### `hp_dev_7220`

- pattern: `daughter -> wife -> king -> motto`
- value: longer historical chain with a non-person final answer

## Why Not The Other Keep Candidates

以下题保留为 reserve，不先进第一版 set：

- `hp_dev_1380`
  - also `wife -> brother`, too close to `hp_dev_7398`
- `hp_dev_4066`
  - good chain, but phrasing is less transparent than the selected set
- `hp_dev_4676`
  - close to identity-resolution style; good reserve candidate
- `hp_dev_6741`
  - useful modern celebrity case, but more narrative and less canonical than the selected five
- `hp_dev_6859`
  - interesting literary chain, but wording is more indirect and may add unnecessary instability in the first draft set

## Current Judgment

This is now sufficient for a draft `relation_chain_bridge` source set.

The project no longer needs:

- a third expansion batch
- more generic relation-term search

## Immediate Next Step

Use this draft set to:

1. generate `episodic_trace`
2. generate `cross_episode_consolidation`
3. reroute `wiki_dev_2639` to subtype-matched source memory
4. then decide whether a minimal subtype-aware rerun is worth doing
