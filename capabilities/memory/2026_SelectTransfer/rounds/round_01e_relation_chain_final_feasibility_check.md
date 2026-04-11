# Experiment Round

## Round Name

`round_01e_relation_chain_final_feasibility_check`

## Date

2026-04-11

## Objective

在保持 `model / prompt / artifacts / target benchmark / subtype definition` 不变的前提下，只对 `relation_chain_bridge` source-side feasibility 再做最后一次高精度检查，回答：

1. `HotpotQA` 是否能提供至少 5 个稳定的 `relation_chain_bridge` source candidates
2. 如果不能，是否应正式停止这条扩池线
3. `wiki_dev_2639` 之后是否只能保留为 subtype-mismatch evidence

## Variable Being Changed

这轮唯一允许变化的核心变量：

- candidate prefilter precision

具体来说，只允许把：

- Batch 1 的泛 relation-term prefilter

收紧成：

- explicit multi-relation / relation-chain template prefilter

## Fixed Conditions

这轮必须固定：

- `source benchmark = HotpotQA`
- `target benchmark = 2WikiMultiHopQA`
- `CURRENT_SPLIT = validation`
- `N = 5`
- 当前 `attribute_bridge / relation_chain_bridge` 定义
- 当前 `hp_bridge_set_01 = attribute_bridge`
- 当前 `wiki_dev_2639 = relation_chain_bridge`

## Conditions Compared

这轮不做模型条件对比。

只比较两种 source-side feasibility state：

- `Batch 1 generic relation-term expansion`
- `Batch 2 high-precision relation-chain expansion`

## Inputs Used

本轮使用：

- [../results/08_relation_chain_bridge_expansion/batch_01_subtype_annotation_summary.md](../results/08_relation_chain_bridge_expansion/batch_01_subtype_annotation_summary.md)
- [../results/08_relation_chain_bridge_expansion/candidate_batch_for_subtype_annotation_screened.csv](../results/08_relation_chain_bridge_expansion/candidate_batch_for_subtype_annotation_screened.csv)
- [../protocol/expand-relation-chain-bridge-source-pool.md](../protocol/expand-relation-chain-bridge-source-pool.md)
- [../protocol/high-precision-relation-chain-bridge-expansion-batch.md](../protocol/high-precision-relation-chain-bridge-expansion-batch.md)

## Metrics

### Primary Feasibility Outputs

- raw candidates found
- filtered candidates retained
- manually reviewed candidates
- stable `relation_chain_bridge + keep`

### Secondary Quality Outputs

- false-positive pressure
- `attribute_bridge` contamination rate
- `unclear` rate

## What This Round Will Answer

这轮允许回答：

- 更高精度模板是否能显著提高 `relation_chain_bridge` 候选命中率
- 当前 source benchmark 是否值得再补一批
- 当前项目是否还能合法地追 `relation_chain_bridge` source set

## What This Round Will NOT Answer

这轮不回答：

- memory form 的优劣
- prompt 是否继续改
- 是否更换模型
- `wiki_dev_2639` 在 rerun 中最终会如何表现

## Pre-Run Checklist

开始前必须确认：

- [ ] Batch 1 screening 已完成
- [ ] Batch 1 subtype annotation 已完成
- [ ] Batch 1 只保留了 `1` 个稳定 `relation_chain_bridge`
- [ ] 当前这轮被视为 final feasibility check，而不是开放式扩池

## Suggested Scale

建议：

- raw candidates: `12-20`
- 只用更高精度的 relation-chain 模板
- 优先保证 precision，而不是 recall

## Success Signal

只有满足下面任一条件，才建议继续 source-set construction：

- 新 batch 中新增 `>= 4` 个高质量 `relation_chain_bridge keep`
- 或 Batch 1 + Batch 2 合计 `>= 5`，且样本不明显近重复

## Failure Signal

如果出现下面任一情况，应停止这条线：

- 新 batch 仍然只有 `<= 2` 个高质量 keep
- 大多数候选继续落回 `attribute_bridge`
- 真正保留下来的题明显近重复或边界过强

## Notes

这轮是：

**最后一次 relation-chain feasibility check。**

如果这一步仍然不够，就不该继续通过扩池去“拯救” `wiki_dev_2639`，而应正式承认当前 setting 不覆盖这个 subtype。
