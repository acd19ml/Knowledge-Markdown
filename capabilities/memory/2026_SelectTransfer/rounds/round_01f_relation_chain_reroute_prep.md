# Experiment Round

## Round Name

`round_01f_relation_chain_reroute_prep`

## Date

2026-04-11

## Objective

在 `relation_chain_bridge` source set 已经可行之后，准备一个最小 subtype-aware rerun 所需的 source-side and pairing-side inputs。

这轮只回答：

1. 哪些 target 应被 reroute 到新的 `hp_relation_chain_bridge_set_01`
2. 哪些 target 继续留在 `hp_bridge_set_01`
3. 下一轮真正 rerun 前还缺哪些 artifact

## Variable Being Changed

这轮唯一允许变化的变量：

- source-set routing for relation-chain targets

也就是：

- new subtype-matched relevant source
- new subtype-mismatched irrelevant source

## Fixed Conditions

这轮必须固定：

- model
- prompt scaffold
- decoding params
- target benchmark
- target subset roles
- `attribute_bridge` pairing for non-relation-chain targets

## Inputs Used

本轮使用：

- [../results/09_relation_chain_bridge_expansion_batch2/batch_02_subtype_annotation_summary.md](../results/09_relation_chain_bridge_expansion_batch2/batch_02_subtype_annotation_summary.md)
- [../results/09_relation_chain_bridge_expansion_batch2/relation_chain_source_set_selection.md](../results/09_relation_chain_bridge_expansion_batch2/relation_chain_source_set_selection.md)
- [../results/09_relation_chain_bridge_expansion_batch2/relation_chain_pairing_update.md](../results/09_relation_chain_bridge_expansion_batch2/relation_chain_pairing_update.md)
- [../pilot/source_sets.csv](../pilot/source_sets.csv)
- [../pilot/pairing_table.csv](../pilot/pairing_table.csv)

## Outputs

这轮应产出：

- 新的 relation-chain source set 已写入 working `source_sets.csv`
- working `pairing_table.csv` 已 reroute relation-chain targets
- 一份明确说明：下一轮 rerun 前需要先生成哪些 artifact

## What This Round Will Answer

这轮允许回答：

- `wiki_dev_2639` 和 `wiki_dev_1379` 是否应 reroute 到新的 source set
- 当前 rerun 是否只需要改少数 targets，而不是全表重跑

## What This Round Will NOT Answer

这轮不回答：

- rerun 之后结果是否一定改善
- `relation_chain_bridge` source artifact 哪种 form 更好
- 是否该继续改 prompt

## Immediate Next Step

完成本轮后，下一步应是：

1. use [../notebooks/04_artifact_generation.ipynb](../notebooks/04_artifact_generation.ipynb) 为 `hp_relation_chain_bridge_set_01` 生成 `episodic_trace` 和 `cross_episode_consolidation`
2. 另开一轮最小 rerun，只跑被 reroute 的 relation-chain targets
