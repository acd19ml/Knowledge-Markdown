# Progress Report: Round 1e Relation-Chain Feasibility Check

Date: 2026-04-11

---

## 1. Executive Summary

Round 1e 的任务不是 rerun 现有模型条件，而是回答一个更前置、也更决定性的设计问题：

**在当前 `HotpotQA -> 2WikiMultiHopQA` setting 下，`HotpotQA` source side 是否真的能支持一个最小 `relation_chain_bridge` source set？**

这个问题来自 Round 1d。  
Round 1d 已经确认：

- `wiki_dev_2639` 是 `relation_chain_bridge`
- 当前 `hp_bridge_set_01` 只是 `attribute_bridge`

所以如果 `relation_chain_bridge` source pool 根本不存在，那正确做法就不是继续 rerun，而是承认：

- 当前 setting 不覆盖这个 subtype

Round 1e 的最终结论是：

1. **Batch 1 的 generic relation-term expansion 不够好，只得到 `1` 个稳定 keep。**
2. **Batch 2 的 high-precision template expansion 成功把 stable keep 提升到 `10`。**
3. **当前已经可以构造一个最小 draft `relation_chain_bridge` source set，并将 `wiki_dev_2639` / `wiki_dev_1379` reroute 到 subtype-matched source。**

因此，Round 1e 结束后，项目状态发生了实质变化：

- `relation_chain_bridge` 不再只是“可能存在的 subtype”
- 它已经变成一个可以被 source-side 支撑、并可进入后续 minimal rerun 的实验单元

---

## 2. What Changed Since Round 1d

相对于 [progress-report-round1d-bridge-subtype-repair.md](./progress-report-round1d-bridge-subtype-repair.md)，Round 1e 把问题从：

- “当前 source-target subtype 不匹配”

推进到了：

- “能不能补出 subtype-matched source support”

### 2.1 Batch 1: Generic Relation-Term Expansion

首先运行了第一批 relation-chain feasibility batch：

- [08_relation_chain_bridge_expansion.ipynb](../notebooks/08_relation_chain_bridge_expansion.ipynb)
- [batch_01_first_pass_screening.md](../results/08_relation_chain_bridge_expansion/batch_01_first_pass_screening.md)
- [batch_01_subtype_annotation_summary.md](../results/08_relation_chain_bridge_expansion/batch_01_subtype_annotation_summary.md)

这一批的特点是：

- 先从 `HotpotQA bridge` pool 中按 relation terms 预筛
- 再做 human screening
- 再做 subtype annotation

结果：

- filtered rows: `15`
- screened rows: `12`
- stable `relation_chain_bridge + keep`: `1`

结论：

- generic relation-term prefilter 的 recall 够用
- 但 precision 明显不足
- 不能直接据此构造 source set

### 2.2 Batch 2: High-Precision Template Expansion

随后运行了更高精度的第二批：

- [09_relation_chain_bridge_expansion_batch2.ipynb](../notebooks/09_relation_chain_bridge_expansion_batch2.ipynb)
- [batch_02_subtype_annotation_summary.md](../results/09_relation_chain_bridge_expansion_batch2/batch_02_subtype_annotation_summary.md)

这一批不再搜单个 kinship term，而是只保留：

- multi-relation wording
- nested relation structure

例如：

- `wife -> brother`
- `husband -> mother`
- `father -> son`
- `daughter -> wife -> king`

结果：

- screened rows: `17`
- stable `relation_chain_bridge + keep`: `10`

### 2.3 Source Set Construction and Pairing Reroute

由于 Batch 2 的命中率已经足够，我们没有再继续扩 Batch 3，而是直接进入：

- draft source set 选择
- working pairing reroute

相关文件：

- [relation_chain_source_set_selection.md](../results/09_relation_chain_bridge_expansion_batch2/relation_chain_source_set_selection.md)
- [relation_chain_pairing_update.md](../results/09_relation_chain_bridge_expansion_batch2/relation_chain_pairing_update.md)
- [source_sets.csv](../pilot/source_sets.csv)
- [pairing_table.csv](../pilot/pairing_table.csv)

---

## 3. Round 1e Results

### 3.1 Feasibility Comparison: Batch 1 vs Batch 2

| Batch | prefilter style | manually reviewed | stable `relation_chain_bridge + keep` | judgment |
|---|---|---|---|---|
| Batch 1 | generic relation-term | 12 | 1 | insufficient |
| Batch 2 | high-precision template | 17 | 10 | sufficient |

这个对比本身就是 Round 1e 最重要的结果。

它说明：

- 问题不是 `HotpotQA` 里根本没有 relation-chain source
- 问题是第一版搜索方式太粗，导致大量候选掉回：
  - `attribute_bridge`
  - 或 boundary cases

### 3.2 Combined Yield

把两批结果放在一起，当前 source-side 的 relation-chain pool 变成：

| Source | stable keep |
|---|---|
| Batch 1 | 1 |
| Batch 2 | 10 |
| Combined | 11 |

这已经明显高于项目当前的最小要求：

- `N = 5`

因此，Round 1e 成功把 source-side feasibility 从“高度可疑”推进到了“可以构造最小 source set”。

### 3.3 Draft Source Set Was Successfully Constructed

基于 Batch 2 keep pool，当前已构造出：

- `hp_relation_chain_bridge_set_01`

成员为：

- `hp_dev_7398`
- `hp_dev_2485`
- `hp_dev_1892`
- `hp_dev_5315`
- `hp_dev_7220`

这个 5-shot set 的设计目标不是最容易做，而是尽量覆盖不同 family：

- spouse -> sibling
- spouse -> parent
- parent -> parent
- son -> sibling
- daughter -> wife -> king/motto

这比单纯取前 5 个 keep 更合理，因为它更接近一个真正可复用的 source memory unit。

### 3.4 Pairing Was Updated for Relation-Chain Targets

Round 1e 之后，working pairing 已不再把所有 `bridge` target 都继续接到 `hp_bridge_set_01`。

目前至少有两条 target 已被 reroute：

- `wiki_dev_2639`
- `wiki_dev_1379`

更新方式是：

- relevant source → `hp_relation_chain_bridge_set_01`
- irrelevant source → `hp_bridge_set_01`

这意味着后续 rerun 将第一次真正比较：

- subtype-matched relation-chain source
- subtype-mismatched attribute-bridge source

而不再只是：

- coarse-cluster relevant vs cross-cluster irrelevant

---

## 4. Deep Analysis

### 4.1 Finding 1: Batch 1 失败不是 benchmark 不行，而是搜索模板不够精确

Round 1e 最开始其实并不乐观。  
Batch 1 的结果只有：

- `1 / 12` stable keep

如果在这一步直接停下，很容易写出：

- `HotpotQA` 不支持 `relation_chain_bridge`

但 Batch 2 证明这不是完整事实。

更准确的解释是：

- relation-chain source 确实存在
- 只是 generic relation-term prefilter 会把大量：
  - `child -> parent -> attribute`
  - `wife -> actress -> year`
  - `daughter -> film`

这类 `attribute_bridge` 也抓进来

所以 Batch 1 的低 yield 更像：

- prefilter failure

而不是：

- source benchmark failure

### 4.2 Finding 2: High-Precision Template Search Resolves the Source-Side Feasibility Question

Batch 2 最重要的价值，不只是 `10` 个 keep 这个数字，而是它证明了：

- 通过更高精度的 template family，
- 项目可以把 source-side candidate search 从 generic kinship word match
- 收紧到真正的 relation-to-relation continuation

这意味着当前项目在 method 层面也往前走了一步：

- pairing granularity 的修复，不只是 target-side subtype relabeling
- 它也需要 source-side retrieval/generation pool 的模板化收缩

这件事和你最初的研究问题是对齐的，因为它说明：

- “什么算 structurally relevant” 不能只看 cluster 名字
- 还必须看 source pool 是怎么被构出来的

### 4.3 Finding 3: Round 1e 把 `wiki_dev_2639` 从孤立异常变成了可继续实验的目标

在 Round 1d 结束时，`wiki_dev_2639` 的状态还是：

- subtype mismatch evidence

也就是说，它虽然解释清楚了，但还不能被“救回来”进入下一轮 matched rerun。

Round 1e 改变了这一点。

现在：

- source-side support 已经存在
- draft source set 已经存在
- working pairing 也已经 reroute 完成

所以 `wiki_dev_2639` 不再只是一个“说明以前 pairing 错了”的 case，  
而是第一次变成：

- 一个可以被 subtype-aware rerun 真正重新测试的 target

这对整个项目很重要，因为它意味着：

- Round 1d 的识别结论不是死胡同
- 它是可以接出下一轮实验动作的

### 4.4 Round 1e 仍然不是 rerun 成功，而是 rerun 前提成功

这一点必须说清楚。

Round 1e 还没有回答：

- 新 source set 的 episodic / consolidation artifact 哪种更好
- subtype-aware rerun 后 `wiki_dev_2639` 会不会恢复
- relevant relation-chain source 会不会稳定优于 mismatched attribute source

Round 1e 回答的是更前一层的问题：

**这种 rerun 现在终于变得合法了。**

这和前几轮的逻辑是一致的：

- Round 1b 修的是 prompt measurement
- Round 1c 修的是 aggregate interpretation
- Round 1d 修的是 pairing granularity
- Round 1e 修的是 source-side subtype coverage

也就是说，它是一次非常典型的：

- protocol repair / feasibility success

而不是 efficacy result。

---

## 5. Diagnostic Conclusion

Round 1e 的最终结论可以压成三句：

1. **`HotpotQA` 并非不支持 `relation_chain_bridge`，而是需要高精度 template search 才能把这类 source candidates 稳定找出来。**
2. **当前项目已经拥有一个可用的 `relation_chain_bridge` draft source set，不需要第三批扩池。**
3. **`wiki_dev_2639` 与 `wiki_dev_1379` 现在已经可以进入真正的 subtype-aware rerun 准备阶段。**

因此，Round 1e 的最大成果不是新分数，而是：

**把 source-side coverage 这个阻塞条件真正解除。**

---

## 6. Next Step

基于 Round 1e，下一步最合理的顺序是：

1. **为 `hp_relation_chain_bridge_set_01` 生成两类 artifact**
   - `episodic_trace`
   - `cross_episode_consolidation`

2. **完成 relation-chain source 的人工 artifact review**
   - 确认不是空泛 advice
   - 确认两类 form 有实质差异

3. **只对 rerouted relation-chain targets 做最小 rerun**
   - 重点看：
     - `wiki_dev_2639`
     - `wiki_dev_1379`

4. **禁止再开 Batch 3**
   - 当前问题已经从 source feasibility 转成 artifact + rerun efficacy
   - 再扩池只会把问题重新拉回探索态

一句话总结：

**Round 1e 结束后，项目已经从“能不能支持 relation-chain”进入“怎么用 relation-chain source 真正重跑关键 case”。**
