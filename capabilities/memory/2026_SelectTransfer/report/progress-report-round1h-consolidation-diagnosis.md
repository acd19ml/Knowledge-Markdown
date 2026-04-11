# Progress Report: Round 1h Relation-Chain Consolidation Diagnosis

Date: 2026-04-11

---

## 1. Executive Summary

Round 1h 是一个**单 target、单变量**的 diagnosis round。

这一轮不再改：

- source pairing
- model
- `Round 1b` prompt scaffold
- scoring / extraction

它只做一件事：

- 重写 `hp_relation_chain_bridge_set_01` 的 `cross_episode_consolidation`
- 然后只在 `wiki_dev_2639` 上比较：
  - `no_memory`
  - `original relevant consolidation`
  - `revised relevant consolidation`
  - `irrelevant consolidation`

Round 1h 的核心问题是：

**在 `Round 1g` 已经证明 subtype-matched `episodic_trace` 可用之后，为什么 matched `relation_chain` consolidation 仍然失败。**

最终结论是：

1. **revised consolidation 修复了 output-format instability。**
   - `original relevant consolidation` 没有稳定产出 `## Final Answer`
   - `revised relevant consolidation` 已恢复稳定结构化输出
2. **但 revised consolidation 没有修复 answer correctness。**
   - `revised relevant consolidation` 仍然给出 `Cannot be determined from the provided context.`
3. **当前剩余失败不再主要是 subtype mismatch，也不再主要是 formatting failure。**
   - 它更像是一个更窄的 `kinship operator interpretation` 问题：
   - consolidation 把 `sibling-in-law` 这种关系词解释错了
   - 并因此把 reasoning 推向错误的 family-branch reading

因此，Round 1h 给出的不是 “relation-chain consolidation 完全无效”，而是更精确的判断：

**当前 consolidation 失败已经收缩到一个更具体的语义层错误：它没有正确 operationalize 题目中的 kinship operator。**

---

## 2. What Changed Since Round 1g

相对于 [progress-report-round1g-relation-chain-minirun.md](./progress-report-round1g-relation-chain-minirun.md)，Round 1h 只改了 `relevant relation_chain consolidation` 的 wording。

### 2.1 Scope Was Reduced to a Single Sensitive Target

这一轮只保留：

- `wiki_dev_2639`

对应子集：

- [../results/11_round1h_prep/relation_chain_consolidation_subset.csv](../results/11_round1h_prep/relation_chain_consolidation_subset.csv)

原因是：

- `wiki_dev_2639` 是当前唯一同时满足以下条件的 case：
  - `no_memory` 正确
  - `relevant episodic` 正确
  - `relevant consolidation` 失败

它是当前最干净的 `consolidation-only failure` case。

### 2.2 The Repair Target Was Restricted to the Consolidation Artifact

本轮使用的 repair protocol：

- [../protocol/relation-chain-consolidation-repair.md](../protocol/relation-chain-consolidation-repair.md)

主要改动方向是：

- 减少过强的 boundary wording
- 强化 spouse-branch sensitivity
- 恢复稳定的 `## Final Answer`

这轮没有改：

- `episodic_trace`
- irrelevant artifact
- routing
- scoring

### 2.3 Round 1b Structured Scaffold Remained Fixed

Round 1h 继承了 `Round 1b` 的结构化输出约束：

- `## Reasoning`
- `## Final Answer`

运行 notebook：

- [../notebooks/12_round1h_consolidation_diagnosis.ipynb](../notebooks/12_round1h_consolidation_diagnosis.ipynb)

因此，这一轮允许变化的变量只有：

- relevant `relation_chain` consolidation artifact

---

## 3. Round 1h Results

运行结果文件：

- [../results/11_round1h_run/round1h_consolidation_results.csv](../results/11_round1h_run/round1h_consolidation_results.csv)
- [../results/11_round1h_run/round1h_consolidation_results_detail.csv](../results/11_round1h_run/round1h_consolidation_results_detail.csv)
- [../results/11_round1h_run/raw_outputs/](../results/11_round1h_run/raw_outputs/)

### 3.1 Overall Execution Status

| metric | value |
|---|---|
| total runs | 4 |
| `failure_status = ok` | 4 |
| `reasoning_present = 1` | 4 |
| `parse_success = 1` | 4 |

这一轮没有 execution-level failure。  
所以 Round 1h 的结论可以直接解释为 behavior-level outcome，而不是运行故障。

### 3.2 Run-Level Outcome Table

| condition | result | note |
|---|---|---|
| `no_memory` | correct | baseline remains strong |
| `original relevant consolidation` | wrong | formatting unstable, no clean `## Final Answer` |
| `revised relevant consolidation` | wrong | formatting repaired, answer still wrong |
| `irrelevant consolidation` | wrong | still falls back to conservative refusal |

### 3.3 The Revised Consolidation Improved Format, Not Accuracy

这是本轮最重要的直接发现。

相关文件：

- original relevant output: [r1h_original_relevant_consolidation_wiki_dev_2639.md](../results/11_round1h_run/raw_outputs/r1h_original_relevant_consolidation_wiki_dev_2639.md)
- revised relevant output: [r1h_revised_relevant_consolidation_wiki_dev_2639.md](../results/11_round1h_run/raw_outputs/r1h_revised_relevant_consolidation_wiki_dev_2639.md)

`original relevant consolidation` 的失败形态是：

- reasoning 过长
- 强烈受 `Past Experience` 牵引
- 最终没有形成稳定 `## Final Answer`
- extractor 只能退化地抓到 reasoning 里的一句文本

而 `revised relevant consolidation` 的结果是：

- 保持了结构化输出
- `## Final Answer` 恢复
- 但最终答案仍然是：
  - `Cannot be determined from the provided context.`

这说明：

**本轮 repair 确实修复了 formatting layer，但没有修复 reasoning correctness layer。**

### 3.4 The Remaining Error Is Narrower Than Before

`revised relevant consolidation` 的 reasoning 不再像 `Round 1g` 那样完全失控，但它仍然犯了一个更具体的错误：

- 它把题目中的 kinship relation 理解成了错误的 family branch
- 它没有稳定地把 `sibling-in-law` operationalize 成 “spouse's sibling / sibling's spouse” 这一类可执行分支
- 结果仍然退化为：
  - “context does not explicitly name the needed sibling”

而 `no_memory` baseline 恰恰能直接从：

- Harriet -> husband Thomas Pelham-Holles
- Thomas Pelham-Holles -> brother Henry Pelham

走到正确答案。

这说明当前 consolidation 并不是缺少信息，而是：

**在 abstract memory guidance 介入后，模型更容易把 kinship operator 解释错。**

### 3.5 Irrelevant Consolidation Still Serves as the Refusal Baseline

相关文件：

- [r1h_irrelevant_consolidation_wiki_dev_2639.md](../results/11_round1h_run/raw_outputs/r1h_irrelevant_consolidation_wiki_dev_2639.md)

`irrelevant consolidation` 的错误仍然是典型的 conservative refusal：

- 认为文本没有明确给出 Harriet 自己 siblings 的 spouse
- 最终回答 `Cannot be determined from the provided context.`

这条的作用现在更明确了：

- 它不是 subtle transfer case
- 它只是一个 refusal-style lower bound

而 `revised relevant consolidation` 与它仍然收敛到同一错误答案，说明：

**relevant consolidation 目前还没能摆脱这种过度保守的 reading strategy。**

---

## 4. Deep Analysis

### 4.1 Finding 1: Round 1h confirmed that the main remaining problem is no longer pairing

在 `Round 1d` 和 `Round 1g` 之后，`wiki_dev_2639` 的 subtype mismatch 已经被基本排除：

- relevant `episodic_trace` 可用
- irrelevant `episodic_trace` 明显更差

所以 Round 1h 的失败不应再解释成：

- source set 还是不匹配

更合理的解释是：

- 当前 `consolidation` 这种 memory form 把 relation-chain pattern 抽象到了一个不够可执行的层级

### 4.2 Finding 2: The revised consolidation solved stability but not operator interpretation

这轮修复至少完成了两个正面效果：

- 恢复 `## Final Answer`
- 压缩 reasoning，减少原先的 meta-discussion

但它没有完成最关键的一步：

- 正确解释 `sibling-in-law`

也就是说，当前问题已经不在：

- “是不是 abstraction 太 broad”

而更像：

- “abstraction 还没有把题目中的 relation operator 变成正确的 executable rule”

### 4.3 Finding 3: The failure is now narrow enough to justify one more repair round

这是 Round 1h 最有价值的地方。

在这轮之前，remaining failure 还可能被解释成：

- consolidation 太长
- output format 不稳
- branch-sensitive heuristic 还不够明确

但这轮之后，这些解释都被大幅压缩了。  
现在最剩下的核心失败模式是：

- **kinship operator normalization failure**

例如：

- 没有优先把 `sibling-in-law` 映射到可检查的候选关系：
  - spouse's sibling
  - sibling's spouse
- 没有优先使用 context 中已经出现的 explicit spouse branch
- 反而转向更抽象、更保守的 family-tree refusal

这使得下一轮可以继续遵守单变量原则：

- 不用再换模型
- 不用再换 source set
- 不用再改 scoring
- 只修 consolidation 对 kinship operator 的解释方式

---

## 5. Diagnostic Conclusion

Round 1h 的核心结论可以概括成三句：

1. **relation-chain consolidation repair 已经修复了 output stability，但没有修复 correctness。**
2. **当前失败不再主要来自 subtype mismatch，而主要来自 kinship operator interpretation。**
3. **因此，下一步不该 full rerun，而应开一个更窄的 round，只修 `sibling-in-law` 这类关系词的 executable interpretation。**

换句话说，Round 1h 之后，这条线没有被否掉。  
它只是被进一步收紧成一个更具体的 memory-form diagnosis：

**`consolidation` 在 relation-chain tasks 上的问题，不是“有没有相关经验”，而是“抽象后的经验是否把关系词解释成了正确的操作”。**

---

## 6. Next Step

下一步应该开一个新的最小 repair round：

- `Round 1i: kinship operator repair`

这一轮只做：

- 为 `relation_chain` consolidation 增加明确的 kinship operator normalization
- 明确写出：
  - `sibling-in-law` 首先检查 `spouse's sibling`
  - 其次检查 `sibling's spouse`
  - 不要把 parent / grandparent / spouse-of-parent 错当成 in-law answer path

这一轮不该做：

- full rerun
- 模型切换
- prompt scaffold 再改一轮
- benchmark 扩展

只有当这个更窄的 repair 仍然失败时，才有理由考虑：

- 暂停 `relation_chain consolidation` 这条线
- 或把它重新定义成不适合当前课程项目继续推进的分支
