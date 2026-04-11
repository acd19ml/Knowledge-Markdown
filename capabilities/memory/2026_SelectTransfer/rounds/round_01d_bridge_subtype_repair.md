# Experiment Round

## Round Name

`round_01d_bridge_subtype_repair`

## Date

2026-04-11

## Objective

在保持 `model / prompt scaffold / source sets / artifacts` 不变的前提下，只修正当前 `bridge` pairing 的粒度问题，回答：

1. 当前 `bridge` cluster 是否过粗
2. 哪些 `bridge` target 实际上属于不同 subtype
3. 哪些现有 `relevant` pairing 需要降级、改配或移出 smoke subset

这轮的目标不是再跑出新的 aggregate，而是把：

- `entity -> attribute` bridge
- `relation-chain / kinship` bridge

从同一个粗标签里拆开，避免继续把 subtype mismatch 误读成 memory effect。

## Variable Being Changed

这轮唯一允许变化的核心变量：

- pairing granularity

具体包括：

- `bridge` subtype definition
- source-set subtype assignment
- target-task subtype assignment
- `relevant / irrelevant` 的 subtype-level 复核

这轮不允许同时再改：

- model
- prompt scaffold
- artifact wording
- decoding params
- aggregate rules

## Fixed Conditions

这轮必须固定：

- benchmark setting：`HotpotQA -> 2WikiMultiHopQA`
- model：`Qwen/Qwen3.5-9B`
- prompt scaffold：Round 1b 结构化版本
- artifacts：Round 1 frozen artifacts
- source sets：Round 1 frozen source sets
- smoke subset roles：Round 1c 已定义版本

## Conditions Compared

这轮不新增实验条件。

仍然沿用：

- `No Memory`
- `Episodic Trace`
- `Cross-Episode Consolidation`

但当前轮次的主任务不是比较它们，而是决定：

- 哪些 case 在 subtype repair 后还值得 rerun

## Inputs Used

本轮使用：

- [results/05_round1b_prep/round1b_pairing_artifact_audit.md](../results/05_round1b_prep/round1b_pairing_artifact_audit.md)
- [results/05_round1b_prep/round1b_case_role_reclassification.csv](../results/05_round1b_prep/round1b_case_role_reclassification.csv)
- [results/05_round1b_prep/round1c_role_aware_smoke_subset.csv](../results/05_round1b_prep/round1c_role_aware_smoke_subset.csv)
- [pilot/archive/source_sets_round1.csv](../pilot/archive/source_sets_round1.csv)
- [pilot/archive/pairing_table_round1.csv](../pilot/archive/pairing_table_round1.csv)
- [artifacts/hp_bridge_set_01/episodic_trace.md](../artifacts/hp_bridge_set_01/episodic_trace.md)
- [artifacts/hp_bridge_set_01/cross_episode_consolidation.md](../artifacts/hp_bridge_set_01/cross_episode_consolidation.md)
- [protocol/bridge-subtype-repair.md](../protocol/bridge-subtype-repair.md)

## Metrics

### Primary Repair Outputs

- `bridge_subtype`
- `source_set_subtype`
- `target_subtype`
- `subtype_match`
- `pairing_action`

### Secondary Diagnostic Outputs

- `rerun_priority`
- `keep_in_smoke_subset`
- `needs_source_rebuild`

## What This Round Will Answer

这轮允许回答：

- `wiki_dev_2639` 这类 case 是否因为 subtype mismatch 才表现为 relevant derailment
- 当前 `hp_bridge_set_01` 更接近哪一类 bridge pattern
- 哪些 bridge tasks 还可以继续保留为 subtype-aware relevant cases
- 下一轮应该做最小 rerun、source rebuild，还是直接放弃某些 bridge case

## What This Round Will NOT Answer

这轮不回答：

- memory form 的最终优劣
- prompt scaffold 是否还要继续修改
- 是否应直接更换更大模型
- applicability judgment 是否该加入主实验

## Pre-Run Checklist

开始前必须确认：

- [ ] Round 1b pairing / artifact audit 已完成
- [ ] Round 1c case role reclassification 已完成
- [ ] `wiki_dev_2639` 已被明确识别为 bridge-sensitive derailment case
- [ ] 当前修复只针对 `bridge` subtype，不扩到 `comparison`
- [ ] 本轮不会新增真实模型 rerun，除非 subtype repair 完成后另开新轮

## Suggested Scale

优先做 subtype audit，不先跑新实验。

建议最小范围：

- 审 `hp_bridge_set_01` 的 5 个 source episodes
- 审当前 smoke subset 里所有 `bridge` tasks
- 只在需要时生成一个 subtype-aware repaired pairing draft

## Success Signal

只有同时满足以下条件，才建议进入下一轮最小 rerun：

- `bridge` 至少能稳定拆成 2 个 subtype
- `hp_bridge_set_01` 的 subtype 能被明确命名
- `wiki_dev_2639` 这类 case 的 subtype mismatch 有清晰解释
- 能明确列出哪些 bridge cases 应继续保留、哪些应降级或移出

## Failure Signal

如果出现以下任一情况，就不应继续做 bridge rerun：

- `bridge` subtype 仍然高度主观且不稳定
- 大多数 bridge source / target 都混合了多个 subtype
- subtype repair 无法明显改善 pairing 可解释性
- 当前 `bridge` source set 本身需要完全重建

## Notes

这轮本质上是：

**把 Round 1c 的“case role repair”继续推进到 `bridge pairing repair`。**

如果这一步不做，后面任何 bridge-related rerun 都仍然会把 subtype mismatch 和 memory effect 混在一起。
