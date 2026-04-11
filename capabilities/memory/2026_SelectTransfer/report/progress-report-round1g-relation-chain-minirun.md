# Progress Report: Round 1g Relation-Chain Minimal Rerun

Date: 2026-04-11

---

## 1. Executive Summary

Round 1g 是一个**最小 subtype-aware rerun**。

这一轮不再扩 benchmark，也不再改 `model / prompt scaffold / scoring`。它只做一件事：

- 把 `wiki_dev_2639` 和 `wiki_dev_1379` reroute 到新的 `relation_chain_bridge` source
- 然后比较：
  - `no_memory`
  - `relevant relation-chain memory`
  - `irrelevant attribute-bridge memory`

Round 1g 的核心问题是：

**此前 relation-chain targets 上观察到的 degradation，是否主要来自 subtype mismatch，而不是 memory 本身有害。**

最终结论是：

1. **`wiki_dev_2639` 上的 subtype repair 对 `episodic_trace` 有明确作用。**
   - `no_memory = correct`
   - `relevant episodic = correct`
   - `irrelevant episodic = wrong`
2. **`wiki_dev_2639` 上的 subtype repair 没有自动修复 `cross_episode_consolidation`。**
   - `relevant consolidation = wrong`
   - `irrelevant consolidation = wrong`
3. **`wiki_dev_1379` 在所有 5 个条件下都正确，属于 ceiling / low-sensitivity case。**

因此，Round 1g 给出的不是“relation-chain repair 完全成功”，而是更精确的判断：

**subtype mismatch 确实解释了此前一部分错误结论，但它主要修复的是 episodic case；relation-chain consolidation 仍然是一个未解决的 memory-form problem。**

---

## 2. What Changed Since Round 1f

相对于 [progress-report-round1e-relation-chain-feasibility.md](./progress-report-round1e-relation-chain-feasibility.md) 和 `Round 1f` 的 reroute prep，Round 1g 第一次真正把新的 relation-chain source set 用进了模型运行。

### 2.1 New Relation-Chain Artifacts Were Generated

在 rerun 之前，先为 `hp_relation_chain_bridge_set_01` 生成并检查了两类 artifact：

- [../artifacts/hp_relation_chain_bridge_set_01/episodic_trace.md](../artifacts/hp_relation_chain_bridge_set_01/episodic_trace.md)
- [../artifacts/hp_relation_chain_bridge_set_01/cross_episode_consolidation.md](../artifacts/hp_relation_chain_bridge_set_01/cross_episode_consolidation.md)

对应 manifest：

- [../artifacts/relation_chain_artifact_generation_manifest.csv](../artifacts/relation_chain_artifact_generation_manifest.csv)

artifact review 记录在：

- [../results/10_round1g_prep/relation_chain_artifact_review.md](../results/10_round1g_prep/relation_chain_artifact_review.md)

结论是：

- 两类 artifact 都已成功生成
- 两类 artifact 都足够 subtype-specific，可以进入最小 rerun

### 2.2 Round 1g Was Restricted to Two Targets

这一轮没有沿用 `Round 1b` 的 6-case smoke subset，而是进一步收缩到：

- `wiki_dev_2639`
- `wiki_dev_1379`

对应子集文件：

- [../results/10_round1g_prep/relation_chain_minirun_subset.csv](../results/10_round1g_prep/relation_chain_minirun_subset.csv)

这样做的原因是：

- `wiki_dev_2639` 是此前 subtype mismatch 最明显的 diagnostic case
- `wiki_dev_1379` 是另一条已经被 reroute 的 relation-chain companion case

### 2.3 Round 1b Scaffold Was Kept Fixed

Round 1g 明确继承了 `Round 1b` 的结构化 prompt scaffold：

- `## Reasoning`
- `## Final Answer`

使用 notebook：

- [../notebooks/11_round1g_relation_chain_minirun.ipynb](../notebooks/11_round1g_relation_chain_minirun.ipynb)

因此，这一轮允许变化的变量只有：

- relation-chain target 的 relevant / irrelevant source routing

而不包括：

- model
- prompt wording
- scoring rule
- answer extraction

---

## 3. Round 1g Results

运行结果文件：

- [../results/10_round1g_run/round1g_relation_chain_results.csv](../results/10_round1g_run/round1g_relation_chain_results.csv)
- [../results/10_round1g_run/round1g_relation_chain_results_detail.csv](../results/10_round1g_run/round1g_relation_chain_results_detail.csv)
- [../results/10_round1g_run/raw_outputs/](../results/10_round1g_run/raw_outputs)

### 3.1 Overall Execution Status

| metric | value |
|---|---|
| total runs | 10 |
| `failure_status = ok` | 10 |
| `reasoning_present = 1` | 10 |
| `parse_success = 1` | 10 |

这一轮没有出现 execution-level failure。  
因此，Round 1g 的结果可以直接做行为和 outcome 层分析。

### 3.2 Run-Level Outcome Table

| target | condition | result |
|---|---|---|
| `wiki_dev_2639` | `no_memory` | correct |
| `wiki_dev_2639` | `episodic_trace + relevant` | correct |
| `wiki_dev_2639` | `episodic_trace + irrelevant` | wrong |
| `wiki_dev_2639` | `cross_episode_consolidation + relevant` | wrong |
| `wiki_dev_2639` | `cross_episode_consolidation + irrelevant` | wrong |
| `wiki_dev_1379` | all 5 conditions | correct |

这张表已经基本浓缩了 Round 1g 的主要信息。

### 3.3 `wiki_dev_2639`: Episodic Repair Worked

这是本轮最有信息量的一条 case。

对于 `wiki_dev_2639`：

- `no_memory` 给出正确答案 `Henry Pelham`
- `relevant episodic` 仍然给出正确答案 `Henry Pelham`
- `irrelevant episodic` 退化成 `Cannot be determined from the provided context.`

相关 raw outputs：

- [r1g_no_memory_wiki_dev_2639.md](../results/10_round1g_run/raw_outputs/r1g_no_memory_wiki_dev_2639.md)
- [r1g_episodic_trace_wiki_dev_2639_relevant.md](../results/10_round1g_run/raw_outputs/r1g_episodic_trace_wiki_dev_2639_relevant.md)
- [r1g_episodic_trace_wiki_dev_2639_irrelevant.md](../results/10_round1g_run/raw_outputs/r1g_episodic_trace_wiki_dev_2639_irrelevant.md)

这说明一件很关键的事：

**relation-chain subtype repair 至少在 episodic form 上是有效的。**

它没有把 baseline 进一步推高，但它阻止了 memory 被 subtype-mismatched `attribute_bridge` artifact 带偏。

### 3.4 `wiki_dev_2639`: Consolidation Repair Did Not Work

对于同一 target，`cross_episode_consolidation` 没有表现出和 `episodic_trace` 同样的修复效果：

- `relevant consolidation`：错误
- `irrelevant consolidation`：错误

而且两种错误的形态并不完全一样。

相关 raw outputs：

- [r1g_cross_episode_consolidation_wiki_dev_2639_relevant.md](../results/10_round1g_run/raw_outputs/r1g_cross_episode_consolidation_wiki_dev_2639_relevant.md)
- [r1g_cross_episode_consolidation_wiki_dev_2639_irrelevant.md](../results/10_round1g_run/raw_outputs/r1g_cross_episode_consolidation_wiki_dev_2639_irrelevant.md)

`relevant consolidation` 的问题更值得注意：

- 它显式提到了 `Past Experience`
- 但输出没有形成稳定的 `## Final Answer` 结构
- 最终被 extractor 退化地抓到了 reasoning 里的句子：`There is no mention of siblings.`

这说明：

**当前 relation-chain consolidation 不是“完全没被用”，而是“被用了，但用坏了”。**

### 3.5 `wiki_dev_1379`: Ceiling Case Remained Insensitive

`wiki_dev_1379` 在所有 5 个条件下都正确：

- `no_memory`
- `relevant episodic`
- `irrelevant episodic`
- `relevant consolidation`
- `irrelevant consolidation`

相关 raw outputs：

- [r1g_no_memory_wiki_dev_1379.md](../results/10_round1g_run/raw_outputs/r1g_no_memory_wiki_dev_1379.md)
- [r1g_episodic_trace_wiki_dev_1379_relevant.md](../results/10_round1g_run/raw_outputs/r1g_episodic_trace_wiki_dev_1379_relevant.md)
- [r1g_cross_episode_consolidation_wiki_dev_1379_relevant.md](../results/10_round1g_run/raw_outputs/r1g_cross_episode_consolidation_wiki_dev_1379_relevant.md)

所以这条 case 的作用更接近：

- sanity check

而不是：

- sensitivity case

它证明 reroute 并没有引入额外破坏，但它也不能单独支持 stronger transfer claim。

---

## 4. Deep Analysis

### 4.1 Finding 1: Round 1d / 1e 的 subtype repair 不是空转，它确实修复了 episodic-level mismatch

在 Round 1d 之前，`wiki_dev_2639` 更容易被解释成：

- relevant memory hurts

但 Round 1g 说明，这个解释至少对 `episodic_trace` 不成立。

更准确的解释是：

- 旧 relevant source 其实只是 coarse `bridge` match
- 一旦 relevant source 改成真正的 `relation_chain_bridge`
- episodic memory 至少不再把原本正确的 baseline 带偏

也就是说：

**此前的一部分 degradation 确实来自 pairing granularity 不够。**

### 4.2 Finding 2: Subtype repair 对 `consolidation` 不够，说明当前问题已经从 pairing 层转移到了 memory-form 层

Round 1g 最重要的诊断价值在这里。

如果 reroute 之后：

- `episodic` repaired
- `consolidation` still failed

那更合理的解释就不再是：

- pairing 还是错的

而是：

- 当前 `relation_chain` consolidation artifact 还不够稳
- 或者 consolidation prompt 把 memory 抽象到了一个会误导该类目标的层级

这和你的长期问题是对齐的。  
它意味着：

**source relevance 并不自动保证 abstract memory form 可用。**

### 4.3 Finding 3: `wiki_dev_1379` confirms non-destructive reroute, but not positive transfer

`wiki_dev_1379` 这一条不是没价值，而是价值有限。

它说明：

- 关系链 reroute 至少没有把本来稳定的 easy case 搞坏

但它不能说明：

- relevant relation-chain memory 稳定优于 irrelevant memory

因为这条 case 本身太容易了，baseline 就已经是 ceiling。

所以在后续 aggregate 里，它不应被拿来和 `wiki_dev_2639` 同权解释。

### 4.4 Round 1g Changed the Bottleneck Again

Round 1c 之前，主要瓶颈在：

- measurement / case-role confusion

Round 1d / 1e 期间，主要瓶颈在：

- subtype-aware pairing 是否存在

现在 Round 1g 之后，最主要的瓶颈已经变成：

- **relation-chain consolidation 是否是一个可用的 memory form**

这意味着项目的当前阶段已经进一步收缩：

- 不需要再继续怀疑 relation-chain subtype 是否存在
- 也不需要再继续怀疑 reroute 是否有必要
- 现在最该怀疑的是：
  - 当前 consolidation prompt
  - consolidation artifact 粒度
  - consolidation 的 boundary / applicability 描述是否反而让模型过度保守

---

## 5. Diagnostic Conclusion

Round 1g 的结论可以压成四句：

1. **relation-chain subtype repair 是必要的，而且对 `episodic_trace` 已经显示出明确价值。**
2. **此前 `wiki_dev_2639` 的一部分 degradation 确实是 subtype mismatch artifact，不应再被解释成 “relevant memory generally hurts”。**
3. **但 relation-chain `cross_episode_consolidation` 仍未被修复，当前 failure 已经从 pairing 问题转成 memory-form 问题。**
4. **`wiki_dev_1379` 只证明 reroute 非破坏性，不足以支持 stronger transfer claim。**

因此，Round 1g 的最准确定位是：

**一次成功的 subtype-aware rerun diagnosis。**

它没有证明 relation-chain memory 已经整体有效，但它成功把“pairing 问题”和“consolidation 问题”分开了。

---

## 6. Next Step

基于 Round 1g，下一步最合理的动作不是 full rerun，而是：

### 6.1 Open a consolidation-only diagnosis round

只针对：

- `wiki_dev_2639`

只改：

- `relation_chain` consolidation artifact / consolidation prompt

保持不变：

- model
- `Round 1b` scaffold
- scoring
- pairing
- `episodic_trace`

换句话说，下一轮应当回答：

**为什么 subtype-matched `episodic_trace` 已经修复，而 subtype-matched `cross_episode_consolidation` 仍然失败？**

### 6.2 Do Not Full Rerun Yet

现在还不该：

- 把全部 smoke cases 再跑一遍
- 把新的 relation-chain source 直接推广到更大 benchmark
- 同时改 prompt 和 consolidation wording

因为当前最重要的问题已经很具体：

- 不是 “relation-chain source 有没有用”
- 而是 “relation-chain consolidation 为什么会把可修复 case 重新推坏”

一句话说：

**Round 1g 之后，项目的下一步应从 subtype-repair 转入 consolidation-specific diagnosis，而不是立刻扩大 rerun 规模。**
