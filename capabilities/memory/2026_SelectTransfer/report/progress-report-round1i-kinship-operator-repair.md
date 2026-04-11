# Progress Report: Round 1i Kinship-Operator Repair

Date: 2026-04-11

---

## 1. Executive Summary

Round 1i 是在 `Round 1h` 基础上的**最小语义修复 round**。

这一轮不再改：

- model
- source pairing
- routing
- scoring / extraction
- `Round 1b` prompt scaffold

它只做一件事：

- 重写 `relation_chain` consolidation 中对 `sibling-in-law` 这类 kinship operator 的 executable interpretation

然后只在 `wiki_dev_2639` 上比较：

- `no_memory`
- `Round 1h revised relevant consolidation`
- `Round 1i operator-repaired relevant consolidation`
- `irrelevant consolidation`

Round 1i 的核心问题是：

**在 `Round 1h` 已经修复 formatting 之后，进一步修正 kinship operator 的解释，是否足以恢复 relevant consolidation 的正确性。**

最终结论是：

1. **operator-repaired relevant consolidation 恢复了正确答案。**
   - `Round 1h revised relevant consolidation = wrong`
   - `Round 1i operator-repaired relevant consolidation = correct`
2. **irrelevant consolidation 仍然保持错误。**
   - 也就是说，修复没有把所有 memory 都一起抬高，而是只修复了 relevant path
3. **当前 relation-chain consolidation line 已经从 “不可用” 转变为 “可修复且可用”。**
   - 但 reasoning 仍然带有部分 term-level hesitation
   - 因此更准确的表述是：outcome-level repair 成功，process-level purity 仍非完全理想

因此，Round 1i 给出的不是 “memory form 已完全解决”，而是：

**在 relation-chain diagnostic case 上，relevant consolidation failure 确实可以通过更精确的 operator-level abstraction 修复。**

---

## 2. What Changed Since Round 1h

相对于 [progress-report-round1h-consolidation-diagnosis.md](./progress-report-round1h-consolidation-diagnosis.md)，Round 1i 只改了一层：

- `kinship operator normalization`

### 2.1 The Repair Target Was Narrowed Further

本轮使用的 repair protocol：

- [../protocol/relation-chain-kinship-operator-repair.md](../protocol/relation-chain-kinship-operator-repair.md)

这次不再泛泛强调：

- spouse branch
- branch-sensitive heuristic

而是明确写死：

- `sibling-in-law`
  - first candidate: `spouse_of -> sibling`
  - second candidate: `sibling -> spouse_of`

并明确禁止：

- parent
- grandparent
- spouse-of-parent

被误当成默认 in-law path。

### 2.2 Scope Remained a Single Sensitive Target

这一轮仍然只保留：

- `wiki_dev_2639`

对应 prep 文件：

- [../results/12_round1i_prep/kinship_operator_failure_diagnosis.md](../results/12_round1i_prep/kinship_operator_failure_diagnosis.md)
- [../results/12_round1i_prep/relation_chain_operator_subset.csv](../results/12_round1i_prep/relation_chain_operator_subset.csv)

这是当前唯一最干净的 operator-level diagnostic case。

### 2.3 Round 1h Revised Artifact Was Kept as the Direct Control

这一轮没有把比较对象换成：

- original coarse artifact
- bigger rerun subset

而是直接对照：

- `Round 1h revised relevant consolidation`
- `Round 1i operator-repaired relevant consolidation`

运行 notebook：

- [../notebooks/13_round1i_kinship_operator_repair.ipynb](../notebooks/13_round1i_kinship_operator_repair.ipynb)

这保证了 Round 1i 真正只在比较：

- operator-repair 是否增加了有效信息

---

## 3. Round 1i Results

运行结果文件：

- [../results/12_round1i_run/round1i_operator_results.csv](../results/12_round1i_run/round1i_operator_results.csv)
- [../results/12_round1i_run/round1i_operator_results_detail.csv](../results/12_round1i_run/round1i_operator_results_detail.csv)
- [../results/12_round1i_run/raw_outputs/](../results/12_round1i_run/raw_outputs/)

### 3.1 Overall Execution Status

| metric | value |
|---|---|
| total runs | 4 |
| `failure_status = ok` | 4 |
| `reasoning_present = 1` | 4 |
| `final_answer_present = 1` | 4 |
| `parse_success = 1` | 4 |

Round 1i 没有 execution-level failure。  
因此这一轮可以直接做 behavior-level interpretation。

### 3.2 Run-Level Outcome Table

| condition | result |
|---|---|
| `no_memory` | correct |
| `Round 1h revised relevant consolidation` | wrong |
| `Round 1i operator-repaired relevant consolidation` | correct |
| `irrelevant consolidation` | wrong |

这张表已经足以说明：

**operator repair 在 relevant consolidation 上产生了真实 outcome change。**

### 3.3 Relevant Consolidation Was Recovered

相关文件：

- [r1i_round1h_revised_relevant_consolidation_wiki_dev_2639.md](../results/12_round1i_run/raw_outputs/r1i_round1h_revised_relevant_consolidation_wiki_dev_2639.md)
- [r1i_operator_repaired_relevant_consolidation_wiki_dev_2639.md](../results/12_round1i_run/raw_outputs/r1i_operator_repaired_relevant_consolidation_wiki_dev_2639.md)

`Round 1h revised relevant consolidation` 的失败表现是：

- 维持结构化输出
- 但仍然回答：
  - `Cannot be determined from the provided context.`

而 `Round 1i operator-repaired relevant consolidation` 则恢复成：

- `Henry Pelham`

并且：

- `memory_reference_type = explicit_use`

这说明 relevant consolidation 不只是“碰巧答对”，而是至少在文本层面显式参考了 injected memory。

### 3.4 Irrelevant Consolidation Remained Wrong

相关文件：

- [r1i_irrelevant_consolidation_wiki_dev_2639.md](../results/12_round1i_run/raw_outputs/r1i_irrelevant_consolidation_wiki_dev_2639.md)

`irrelevant consolidation` 仍然保持：

- `Cannot be determined from the provided context.`

这很重要，因为它说明 Round 1i 的修复不是一个 generic “让模型更愿意猜”的效应。  
它更像是：

- relevant relation-chain memory 在 operator 层面被修正后，才变得真正可用

### 3.5 The Reasoning Is Correct Enough for Outcome, But Not Fully Clean

Round 1i 最值得保留的保守判断在这里。

虽然 `operator-repaired relevant consolidation` 已经答对，但它的 reasoning 仍然表现出：

- 对 `sibling-in-law` 与 `brother-in-law` 的术语边界有过一轮自我犹豫
- 最终是通过 “dataset likely intends Henry Pelham” 这种修正回到正确答案

也就是说：

- outcome-level repair: **成功**
- process-level semantic cleanliness: **部分成功**

这不影响它作为有效 repair signal，但意味着：

**Round 1i 更强地支持 “可修复性”，而不是 “process 已经完全纯净”。**

---

## 4. Deep Analysis

### 4.1 Finding 1: Round 1i changes the interpretation of `wiki_dev_2639`

在 `Round 1c` 之前，`wiki_dev_2639` 更像：

- a derailment case
- relevant bridge memory hurts an originally correct baseline

但经过 `Round 1d → 1e → 1g → 1h → 1i` 之后，这个解释已经不成立了。

更准确的解释应该是：

- coarse pairing granularity gave a false negative
- subtype-aware reroute repaired episodic memory
- operator-aware repair repaired consolidation

所以：

**`wiki_dev_2639` 不再是 “relevant memory hurts” 的证据，而是 “diagnostic false negative can be repaired when pairing granularity and operator abstraction are made precise” 的证据。**

### 4.2 Finding 2: The remaining difficulty is no longer whether consolidation can work

Round 1h 之前，还可以怀疑：

- relation-chain consolidation 这条线是不是 fundamentally not useful

Round 1i 之后，这个怀疑已经明显变弱。

因为现在已经看到：

- same model
- same target
- same scaffold
- same scoring

只改 operator-level guidance，就能把 relevant consolidation 从 wrong 拉回 correct。

所以当前更合理的判断是：

**consolidation 不是不能 work，而是需要更精确的 executable abstraction。**

### 4.3 Finding 3: The project should now shift from micro-diagnosis to synthesis

Round 1i 之后，再继续围绕 `wiki_dev_2639` 做更细的 micro-repair，边际收益已经明显下降。

因为你已经得到足够强的链式证据：

1. coarse `bridge` pairing can create false negative transfer evidence  
2. subtype-aware reroute can repair episodic behavior  
3. operator-aware repair can repair consolidation behavior

这已经足以支撑一个更高层的 Round 1 synthesis：

- selective transfer claims are highly sensitive to pairing granularity
- memory-form conclusions are highly sensitive to how abstract memory operationalizes relation operators

---

## 5. Diagnostic Conclusion

Round 1i 的核心结论可以压成三句：

1. **operator-repaired relevant consolidation successfully recovered `wiki_dev_2639`.**
2. **therefore, the previous consolidation failure was not evidence that relation-chain consolidation is inherently useless.**
3. **the stronger conclusion is that abstract memory must encode relation operators at an executable level, or it will create false negative transfer evidence.**

也就是说，Round 1i 之后，relation-chain 这条线已经从：

- unresolved failure

转成：

- repaired diagnostic branch

这对整个项目的意义很大，因为它把一个原本看起来像 “memory harmful” 的 case，重新解释成了：

- measurement / representation issue
- not an immediate theoretical defeat

---

## 6. Next Step

下一步不该再开一个新的 GPU-heavy repair round。  
更合理的是：

- 做一次 `Round 1j patchback / synthesis`

目标是：

- 把 `wiki_dev_2639` 的 repaired evidence 补回 role-aware summary
- 更新 Round 1 的高层结论
- 明确这个 case 在最终报告里不应再被写成 derailment evidence

如果后面还继续实验，优先级也应低于：

- Round 1 synthesis
- final project framing

而不是继续在同一个 kinship operator 上做更细的 prompt polishing
