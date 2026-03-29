# Pilot Notes

## 目标

先用一个小规模 pilot 验证这套 setup 是否真的能产生可解释的 selective-transfer 现象，再决定是否进入 full experiment。

## Current Checklist

- 先把 task taxonomy 稳定下来
- 构造固定 `N = 5` 的 source sets
- 按固定规则构造 relevant / irrelevant pairs
- 在大规模运行前先检查 memory artifact 质量
- 先确认 mismatched pairs 上确实能观察到 negative transfer

## Phase 1: Taxonomy

建议规模：

- HotpotQA: 40 tasks
- 2WikiMultiHopQA: 40 tasks

Reasoning labels:

- `bridge`
- `comparison`
- `temporal`
- `distractor-heavy`

规则：

- 每题只分配一个 dominant label
- 没有清晰 dominant label 的题先 drop
- 边界 case 记录在 notes 里

## Phase 2: Source Sets

建议规模：

- 每个 cluster 至少 2 个 source sets
- 每个 source set 固定使用 `N = 5` 个 solved episodes

检查点：

- same reasoning cluster
- entity-disjoint within the set
- no near-duplicate questions

## Phase 3: Pairing

对每个 target task，定义：

- one relevant source set
- one irrelevant source set

Relevant:

- same cluster
- entity-disjoint
- low lexical overlap
- no answer leakage

Irrelevant:

- different cluster
- entity-disjoint
- low lexical overlap
- no answer leakage

## Phase 4: Artifacts

对每个 source set，生成：

- `episodic_trace`
- `cross_episode_consolidation`

人工检查：

- `trace` 是否可用，而不是纯噪声
- `consolidation` 是否足够具体，而不是套话
- 两种 artifact 是否真的体现出不同 memory form

## Phase 5: Small Runs

第一轮先做：

- 10 relevant pairs
- 10 irrelevant pairs

Run:

- `No Memory`
- `Episodic Trace`
- `Cross-Episode Consolidation`

只有当基础 setup 已经能产生可解释现象时，再加入 `Cross-Episode Consolidation + Applicability Judgment`。

## Pilot Success Criteria

- relevant / irrelevant pairs 看起来是可 defend 的
- artifacts 可读，而且不是 trivial summary
- mismatched pairs 上能观察到 negative transfer
- judgment behavior 在 relevant / irrelevant tasks 上存在差异
