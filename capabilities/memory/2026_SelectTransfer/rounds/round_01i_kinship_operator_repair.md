# Experiment Round

## Round Name

`round_01i_kinship_operator_repair`

## Date

2026-04-11

## Objective

在 `Round 1h` 已经表明：

- `relation_chain` consolidation 的 formatting 已经被修稳
- 但 `wiki_dev_2639` 上的 answer correctness 仍然失败

之后，这一轮只回答一个问题：

**当前 relevant `relation_chain` consolidation 是否主要败在对 kinship operator 的错误解释，而不是更高层的 source relevance 或 generic abstraction 问题。**

## Variable Being Changed

这轮唯一允许变化的变量：

- revised `relation_chain` consolidation 中对 kinship operator 的解释方式

具体来说，只允许调整：

- `sibling-in-law`
- `brother-in-law`
- `sister-in-law`

这类关系词在 memory heuristic 里的 operationalization。

## Fixed Conditions

这轮必须固定：

- model
- `Round 1b` structured prompt scaffold
- decoding params
- scoring / answer extraction
- target task
- source set
- routing
- irrelevant consolidation
- `episodic_trace`

## Inputs Used

本轮使用：

- [../report/progress-report-round1h-consolidation-diagnosis.md](../report/progress-report-round1h-consolidation-diagnosis.md)
- [../results/11_round1h_run/round1h_consolidation_results_detail.csv](../results/11_round1h_run/round1h_consolidation_results_detail.csv)
- [../results/11_round1h_run/raw_outputs/r1h_original_relevant_consolidation_wiki_dev_2639.md](../results/11_round1h_run/raw_outputs/r1h_original_relevant_consolidation_wiki_dev_2639.md)
- [../results/11_round1h_run/raw_outputs/r1h_revised_relevant_consolidation_wiki_dev_2639.md](../results/11_round1h_run/raw_outputs/r1h_revised_relevant_consolidation_wiki_dev_2639.md)
- [../artifacts/hp_relation_chain_bridge_set_01/cross_episode_consolidation.md](../artifacts/hp_relation_chain_bridge_set_01/cross_episode_consolidation.md)

## Target

这轮仍然只保留：

- `wiki_dev_2639`

原因：

- 它仍然是当前唯一同时满足：
  - subtype-matched episodic works
  - relevant consolidation fails
  - no-memory baseline is correct

## What This Round Will Answer

这轮允许回答：

- 当前 consolidation failure 是否主要来自：
  - `sibling-in-law` 解释不当
  - spouse branch / sibling branch 候选顺序错误
  - kinship term 没有被正确归一化成可执行检查项

## What This Round Will NOT Answer

这轮不回答：

- relation-chain memory 在更大 benchmark 上是否普遍有效
- 是否应换模型
- 是否需要新的 source set
- `episodic_trace` 与 `consolidation` 的一般优劣

## Success Signal

至少满足以下之一：

- operator-repaired relevant consolidation 给出正确答案
- reasoning 明确写出：
  - `sibling-in-law` first check = spouse's sibling
- 不再出现 parent / grandparent / spouse-of-parent 被误当成 in-law path 的现象

## Failure Signal

出现以下任一情况，则不继续沿这条 consolidation repair 线推进：

- operator repair 后仍然复现同样的 refusal answer
- reasoning 仍然没有把 kinship term 转成明确的候选关系
- relevant consolidation 与 irrelevant consolidation 继续不可区分

## Immediate Next Step

这轮之后，才决定是否：

1. 接受 `relation_chain episodic works but consolidation still not worth追`
2. 再做一次极小的 artifact-only rewrite
3. 暂停 `relation_chain consolidation` 这条线
