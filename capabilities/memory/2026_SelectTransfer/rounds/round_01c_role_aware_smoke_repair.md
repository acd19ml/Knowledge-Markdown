# Experiment Round

## Round Name

`round_01c_role_aware_smoke_repair`

## Date

2026-04-11

## Objective

在保持 `model / prompt scaffold / source set / pairing / artifacts` 不再扩张的前提下，先修正 Round 1b 的解释层与 case 使用方式，回答：

1. 当前 6 个 smoke cases 应分别承担什么实验角色
2. 哪些 case 应从 transfer aggregate 中排除
3. 下一轮是否已经具备进入更大 rerun 的条件

这轮的目标不是再跑出一个新的平均分表，而是把 Round 1b 已经暴露出的：

- benchmark ambiguity
- scoring boundary
- artifact-sensitive derailment
- answer-format correction

从混合现象里拆开。

## Variable Being Changed

这轮唯一允许变化的核心变量：

- evaluation / case-selection layer

具体包括：

- case role reclassification
- boundary-case handling
- process metric refinement

这轮不允许同时再改：

- model
- prompt scaffold
- source sets
- pairing labels
- artifact contents

## Fixed Conditions

这轮必须固定：

- benchmark setting：`HotpotQA -> 2WikiMultiHopQA`
- model：`Qwen/Qwen3.5-9B`
- prompt scaffold：Round 1b 结构化版本
- source sets：Round 1 frozen archive
- pairing：Round 1 frozen archive
- artifacts：Round 1 frozen artifacts
- smoke cases：Round 1b 当前 6 条

## Conditions Compared

条件本身不变，仍然是：

- `No Memory`
- `Episodic Trace`
- `Cross-Episode Consolidation`

但这轮不再把所有 case 混在一起汇总，而是按 role 分开解释。

## Inputs Used

本轮使用：

- [results/05_round1b_run/round1b_smoke_results.csv](../results/05_round1b_run/round1b_smoke_results.csv)
- [results/05_round1b_run/round1b_smoke_results_detail.csv](../results/05_round1b_run/round1b_smoke_results_detail.csv)
- [results/05_round1b_run/raw_outputs/](../results/05_round1b_run/raw_outputs)
- [results/05_round1b_prep/round1b_pairing_artifact_audit.md](../results/05_round1b_prep/round1b_pairing_artifact_audit.md)
- [results/05_round1b_prep/round1b_case_role_reclassification.csv](../results/05_round1b_prep/round1b_case_role_reclassification.csv)
- [results/05_round1b_prep/round1b_case_role_reclassification.md](../results/05_round1b_prep/round1b_case_role_reclassification.md)
- [results/05_round1b_prep/round1c_role_aware_smoke_table.csv](../results/05_round1b_prep/round1c_role_aware_smoke_table.csv)
- [results/05_round1b_prep/round1c_role_aware_smoke_summary.md](../results/05_round1b_prep/round1c_role_aware_smoke_summary.md)
- [results/05_round1b_prep/round1c_role_aware_smoke_subset.csv](../results/05_round1b_prep/round1c_role_aware_smoke_subset.csv)
- [results/05_round1b_prep/round1c_aggregate_rules.md](../results/05_round1b_prep/round1c_aggregate_rules.md)
- [results/05_round1b_prep/round1_target_audit.md](../results/05_round1b_prep/round1_target_audit.md)

## Metrics

### Outcome Metrics

- `EM`
- `F1`

### Process Metrics

- `reasoning_present`
- `final_answer_present`
- `memory_reference_type`

### New Interpretation Axes

- `case_role`
- `aggregate_eligible`
- `answer_granularity_change`
- `artifact_sensitive_derailment`
- `boundary_case`

## What This Round Will Answer

这轮允许回答：

- 当前 6 个 smoke cases 中，哪些还能作为 process sanity check 保留
- 哪些 case 应降级为 audit / boundary 用途
- 哪些现象更可能来自 artifact wording，而不是 transfer 本身
- 下一轮是否需要重建 smoke subset，而不是直接 full rerun

## What This Round Will NOT Answer

这轮不回答：

- 哪种 memory form 最终更好
- 当前 setup 已经支持强 selective-transfer claim
- 更换更大模型是否会直接解决问题

## Pre-Run Checklist

开始前必须确认：

- [ ] Round 1b results 已冻结
- [ ] pairing / artifact audit 已完成
- [ ] case role reclassification 已完成
- [ ] `wiki_dev_0092` 与 `wiki_dev_6083` 已明确降级为 boundary / audit 用途
- [ ] 不再把当前 6 case 当作统一 aggregate smoke benchmark

## Suggested Scale

优先做 analysis / relabel，不先做 full rerun。

如果确实需要 rerun，也只允许：

- 针对 role-aware subset 的最小 rerun
- 或为了验证新 process metric 的极小补跑

## Success Signal

只有同时满足以下条件，才建议进入更大的 rerun：

- 每个 smoke case 都有稳定角色
- boundary / ambiguity cases 已从 transfer aggregate 中剥离
- 至少保留 1 到 2 个 process sanity cases
- 至少保留 1 个 artifact-sensitive diagnostic case
- 下一轮 smoke subset 的构成不再依赖临时解释

## Failure Signal

如果出现以下任一情况，就不应进入 full rerun：

- case role 仍然高度不稳定
- 大多数 signal 仍由 scoring / benchmark boundary 主导
- 没有任何 case 可以作为相对干净的 transfer evidence
- 当前 smoke subset 需要整体重建

## Notes

这轮本质上是：

**把 Round 1b 从“结果观察”推进到“下一轮可执行筛选规则”。**

如果它做不好，继续 full rerun 只会把当前混杂现象放大。
