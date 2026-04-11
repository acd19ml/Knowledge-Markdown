# Experiment Round

## Round Name

`round_01g_relation_chain_minirun`

## Date

2026-04-11

## Objective

在 `relation_chain_bridge` source set 已经构造完成、artifact review 已通过之后，执行一个最小 subtype-aware rerun。

这轮只回答一个问题：

**之前在 relation-chain targets 上观察到的 degradation，是否主要来自 subtype mismatch，而不是 memory 本身有害。**

## Variable Being Changed

这轮唯一允许变化的变量：

- relevant / irrelevant source routing for relation-chain targets

具体来说：

- relevant source: `hp_relation_chain_bridge_set_01`
- irrelevant source: `hp_bridge_set_01`

## Fixed Conditions

这轮必须固定：

- model
- `Round 1b` prompt scaffold
- decoding params
- answer extraction rule
- scoring rule
- target tasks outside the rerouted relation-chain subset
- memory forms compared:
  - `no_memory`
  - `episodic_trace`
  - `cross_episode_consolidation`

## Inputs Used

本轮使用：

- [../results/10_round1g_prep/relation_chain_artifact_review.md](../results/10_round1g_prep/relation_chain_artifact_review.md)
- [../results/10_round1g_prep/relation_chain_minirun_subset.csv](../results/10_round1g_prep/relation_chain_minirun_subset.csv)
- [../results/09_relation_chain_bridge_expansion_batch2/relation_chain_pairing_update.md](../results/09_relation_chain_bridge_expansion_batch2/relation_chain_pairing_update.md)
- [../pilot/pairing_table.csv](../pilot/pairing_table.csv)
- [../artifacts/hp_relation_chain_bridge_set_01/episodic_trace.md](../artifacts/hp_relation_chain_bridge_set_01/episodic_trace.md)
- [../artifacts/hp_relation_chain_bridge_set_01/cross_episode_consolidation.md](../artifacts/hp_relation_chain_bridge_set_01/cross_episode_consolidation.md)
- [../artifacts/hp_bridge_set_01/episodic_trace.md](../artifacts/hp_bridge_set_01/episodic_trace.md)
- [../artifacts/hp_bridge_set_01/cross_episode_consolidation.md](../artifacts/hp_bridge_set_01/cross_episode_consolidation.md)

## Planned Runs

每个 target 只跑 5 条：

1. `no_memory`
2. `episodic_trace + relevant`
3. `episodic_trace + irrelevant`
4. `cross_episode_consolidation + relevant`
5. `cross_episode_consolidation + irrelevant`

当前最小 rerun target:

- `wiki_dev_2639`
- `wiki_dev_1379`

总 run 数：

- `2 targets x 5 conditions = 10`

## Outputs

这轮应产出：

- `results/10_round1g_run/round1g_relation_chain_results.csv`
- `results/10_round1g_run/round1g_relation_chain_results_detail.csv`
- `results/10_round1g_run/raw_outputs/`

## What This Round Will Answer

这轮允许回答：

- subtype-matched relation-chain source 是否比 subtype-mismatched `attribute_bridge` source 更稳
- `wiki_dev_2639` 的历史 degradation 是否会被修正
- `wiki_dev_1379` 是否显示类似方向的变化

## What This Round Will NOT Answer

这轮不回答：

- relation-chain source 在更大 benchmark 上是否普遍有效
- 是否应该继续修改 prompt
- `Applicability Judgment` 是否必要
- relation-chain memory 一定优于其他 memory forms

## Success Signal

至少满足下列之一：

- 在至少一个 rerouted target 上，`relevant` memory 相对 `irrelevant` memory 更接近或优于 `no_memory`
- reasoning 中出现对 relation-chain memory 的显式使用，而不是被 `attribute_bridge` memory 带偏

## Failure Signal

出现以下任一情况，则不进入 full rerun：

- rerouted target 仍然主要被 `attribute_bridge` irrelevant memory 带偏，但 relevant memory 没有改善
- new artifacts 虽然被显式引用，但输出行为没有任何变化
- 两个 target 都显示 subtype repair 不足以解释之前的问题

## Immediate Next Step

运行：

- [../notebooks/11_round1g_relation_chain_minirun.ipynb](../notebooks/11_round1g_relation_chain_minirun.ipynb)

然后只分析这 10 条 rerun，不做 full rerun。
