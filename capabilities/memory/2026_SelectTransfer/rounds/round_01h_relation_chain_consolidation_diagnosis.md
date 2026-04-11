# Experiment Round

## Round Name

`round_01h_relation_chain_consolidation_diagnosis`

## Date

2026-04-11

## Objective

在 `Round 1g` 已经表明：

- `relation_chain` subtype repair 对 `episodic_trace` 有效
- 但对 `cross_episode_consolidation` 仍然无效

之后，这一轮只回答一个问题：

**为什么 subtype-matched `relation_chain` consolidation 仍然会在敏感 target 上失败。**

## Variable Being Changed

这轮唯一允许变化的变量：

- `relation_chain` consolidation artifact / consolidation prompt

也就是说，只允许调整：

- `hp_relation_chain_bridge_set_01` 的 consolidation wording
- 或 consolidation generation prompt

## Fixed Conditions

这轮必须固定：

- model
- `Round 1b` structured prompt scaffold
- decoding params
- scoring / answer extraction rule
- target task
- pairing routing
- `episodic_trace` artifact
- `attribute_bridge` artifacts

## Inputs Used

本轮使用：

- [../report/progress-report-round1g-relation-chain-minirun.md](../report/progress-report-round1g-relation-chain-minirun.md)
- [../results/10_round1g_run/round1g_relation_chain_results_detail.csv](../results/10_round1g_run/round1g_relation_chain_results_detail.csv)
- [../results/10_round1g_run/raw_outputs/r1g_cross_episode_consolidation_wiki_dev_2639_relevant.md](../results/10_round1g_run/raw_outputs/r1g_cross_episode_consolidation_wiki_dev_2639_relevant.md)
- [../results/10_round1g_run/raw_outputs/r1g_cross_episode_consolidation_wiki_dev_2639_irrelevant.md](../results/10_round1g_run/raw_outputs/r1g_cross_episode_consolidation_wiki_dev_2639_irrelevant.md)
- [../artifacts/hp_relation_chain_bridge_set_01/cross_episode_consolidation.md](../artifacts/hp_relation_chain_bridge_set_01/cross_episode_consolidation.md)
- [../results/11_round1h_prep/relation_chain_consolidation_subset.csv](../results/11_round1h_prep/relation_chain_consolidation_subset.csv)

## Target

这轮只保留一个 target：

- `wiki_dev_2639`

原因：

- 它是当前唯一对 subtype repair 有明显敏感性的 relation-chain case
- `wiki_dev_1379` 在 `Round 1g` 中是 ceiling case，不适合继续承担 consolidation diagnosis

## What This Round Will Answer

这轮允许回答：

- 当前 consolidation failure 更像：
  - abstraction too broad
  - boundary / applicability wording too conservative
  - output-format instability
  - wrong bridge selection heuristic

## What This Round Will NOT Answer

这轮不回答：

- relation-chain memory 在更大 benchmark 上是否普遍有效
- 是否应切换模型
- 是否需要引入 `Applicability Judgment`
- `episodic_trace` 是否已经最优

## Success Signal

至少满足以下之一：

- revised relevant consolidation 不再把 `wiki_dev_2639` 推向错误答案
- revised relevant consolidation 至少恢复到 `no_memory` 水平
- reasoning 中对 relation-chain consolidation 的引用变得更具体，且不再出现明显的 relation-direction confusion

## Failure Signal

出现以下任一情况，则不进入更大 rerun：

- consolidation wording 调整后仍然复现相同失败模式
- relevant consolidation 与 irrelevant consolidation 仍然都失败，且错误没有区分度
- consolidation 仍频繁破坏结构化输出

## Immediate Next Step

这轮之后，才决定是否：

1. 保留 `relation_chain` episodic line 继续推进
2. 单独重写 consolidation prompt
3. 暂停 relation-chain consolidation 这条线
