# Experiment Round

## Round Name

`round_01j_patchback_synthesis`

## Date

2026-04-11

## Objective

在 `Round 1i` 已经表明：

- `wiki_dev_2639` 的 relevant `relation_chain` consolidation 可以被 operator repair 修复

之后，这一轮不再做新的 model run。  
它只回答一个问题：

**如何把 `Round 1g` 与 `Round 1i` 的 repaired evidence 补回 `Round 1c` 的 role-aware interpretation，使最终 Round 1 synthesis 不再建立在已经过时的 `wiki_dev_2639` 诊断之上。**

## Variable Being Changed

这轮唯一允许变化的变量：

- result interpretation layer

具体来说，只允许更新：

- `wiki_dev_2639` 在 role-aware summary 中的 case interpretation

## Fixed Conditions

这轮必须固定：

- all run-level outputs
- model
- prompt scaffold
- scoring
- source sets
- routing decisions already used in `Round 1g` / `Round 1i`

## Inputs Used

本轮使用：

- [../results/05_round1b_prep/round1c_role_aware_smoke_table.csv](../results/05_round1b_prep/round1c_role_aware_smoke_table.csv)
- [../results/10_round1g_run/round1g_relation_chain_results_detail.csv](../results/10_round1g_run/round1g_relation_chain_results_detail.csv)
- [../results/12_round1i_run/round1i_operator_results_detail.csv](../results/12_round1i_run/round1i_operator_results_detail.csv)
- [../report/progress-report-round1i-kinship-operator-repair.md](../report/progress-report-round1i-kinship-operator-repair.md)

## What This Round Will Answer

这轮允许回答：

- `wiki_dev_2639` 在最终 Round 1 synthesis 中应该如何被重新分类
- 哪些旧结论需要撤回
- 哪些更高层结论因此变得更强

## What This Round Will NOT Answer

这轮不回答：

- any new memory efficacy claim
- any larger benchmark generalization claim
- whether to change model or prompt again

## Success Signal

至少满足以下之一：

- `wiki_dev_2639` 的 patched interpretation 被明确改写
- Round 1 synthesis 不再依赖 “relevant memory hurts” 这一旧说法
- 最终 summary 能把 coarse pairing / operator abstraction 作为核心 methodological lesson

## Failure Signal

如果 patchback 后仍然无法清楚说明：

- 为什么旧诊断应被撤回
- 为什么 repaired evidence 更可信

那说明 current reporting layer still mixes pre-repair and post-repair evidence.

## Immediate Next Step

这轮之后，优先做：

1. Round 1 final synthesis
2. final project report structuring

而不是继续单-case repair
