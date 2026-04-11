# Progress Report: Round 1 Final Synthesis

Date: 2026-04-11

---

## 1. Executive Summary

Round 1 不应再被概括成：

- `memory` 平均上有没有帮助

也不应再被概括成：

- `wiki_dev_2639` 证明了 relevant memory can hurt

在经过 `Round 1 -> 1b -> 1c -> 1d -> 1e -> 1g -> 1h -> 1i -> 1j` 之后，更准确的 Round 1 结论是：

1. **当前项目已经成功建立了一套可解释的 `selective transfer` measurement workflow。**
   - prompt scaffold、raw outputs、role-aware case analysis、subtype-aware pairing repair 都已经落地
2. **粗粒度 aggregate 会制造错误结论。**
   - 尤其是当 pairing granularity 不够细、case role 不加区分时，`relevant / irrelevant` 平均会掩盖真正的问题来源
3. **`wiki_dev_2639` 这类 relation-chain case 证明的不是 “relevant memory harms”，而是 “coarse pairing + incomplete operator abstraction can create false negative transfer evidence”。**
4. **在最敏感的 repaired diagnostic case 上，relevant memory 最终可被恢复。**
   - `episodic_trace` 通过 subtype-aware reroute 恢复
   - `cross_episode_consolidation` 通过 operator-aware repair 恢复

因此，Round 1 最终支持的不是一个简单的 efficacy claim，而是一个更有方法论价值的判断：

**对 memory selective transfer 的判断，高度依赖 pairing granularity、case-role discipline，以及 abstract memory 是否把 relation operators 编码成可执行规则。**

---

## 2. What Round 1 Initially Looked Like

在最初的 Round 1 pilot 中，项目看起来像是一个相当不理想的结果：

- sensitivity 严重不足
- 很多 case 没有 movement
- `wiki_dev_2639` 等 case 还会让人直觉上觉得：
  - relevant memory seems harmful

如果停在那个阶段，最容易写出的结论会是：

- memory 没什么稳定收益
- relevant / irrelevant distinction 不明显
- consolidation 甚至可能更容易出错

但后续几轮说明，这种早期读法并不稳。

---

## 3. How The Interpretation Changed Across Rounds

### 3.1 Round 1b: The project first became observable

Round 1b 修复了最早期的 measurement problem：

- 从单行直答转成稳定的
  - `## Reasoning`
  - `## Final Answer`

对应：

- [progress-report-round1b-prompt-diagnosis.md](./progress-report-round1b-prompt-diagnosis.md)

这一步的意义不是分数更高，而是：

- 你第一次真的能看到模型有没有引用 memory
- 能看到 explicit use / explicit reject
- 能做 process-level diagnosis

### 3.2 Round 1c: The project stopped treating all smoke cases as one benchmark

Round 1c 的贡献是 role-aware interpretation：

- `process sanity`
- `diagnostic`
- `audit / boundary`

对应：

- [progress-report-round1c-role-aware-smoke-repair.md](./progress-report-round1c-role-aware-smoke-repair.md)

这一步之后，项目不再允许：

- 对 6 个 smoke cases 混着报一个平均 `EM/F1`

这是整个项目方法论上最关键的收束之一。

### 3.3 Round 1d / 1e: The project discovered that `bridge` was too coarse

Round 1d 先说明：

- `bridge` 至少应该拆成：
  - `attribute_bridge`
  - `relation_chain_bridge`

Round 1e 再说明：

- `HotpotQA` 的 source side 其实可以支持一个最小 `relation_chain_bridge` source set

对应：

- [progress-report-round1d-bridge-subtype-repair.md](./progress-report-round1d-bridge-subtype-repair.md)
- [progress-report-round1e-relation-chain-feasibility.md](./progress-report-round1e-relation-chain-feasibility.md)

这两轮一起改变了一个关键认识：

- 有些看起来像 “memory harmful” 的 case，实际上只是 relevant pairing 粒度太粗

### 3.4 Round 1g / 1h / 1i: The project repaired the strongest false negative

这一段是 Round 1 最重要的 evidence chain。

#### Round 1g

- subtype-aware reroute 修复了 `wiki_dev_2639` 上的 relevant `episodic_trace`
- 但 `consolidation` 仍然失败

对应：

- [progress-report-round1g-relation-chain-minirun.md](./progress-report-round1g-relation-chain-minirun.md)

#### Round 1h

- 修复 `relation_chain consolidation` 的 formatting 和 branch wording
- 结果是 formatting 修好了，但 correctness 还没回来
- failure 被进一步收缩成 `kinship operator interpretation`

对应：

- [progress-report-round1h-consolidation-diagnosis.md](./progress-report-round1h-consolidation-diagnosis.md)

#### Round 1i

- 只修 `sibling-in-law` 这类 operator 的 executable interpretation
- relevant `consolidation` 在 `wiki_dev_2639` 上恢复正确

对应：

- [progress-report-round1i-kinship-operator-repair.md](./progress-report-round1i-kinship-operator-repair.md)

这一链条最终说明：

**同一个 case 上，早期看起来像 “relevant memory harms” 的现象，其实可以被更细的 pairing 与 operator-level repair 完整改写。**

### 3.5 Round 1j: The interpretation layer was patched back

Round 1j 没有再做新运行，而是把 repaired evidence 补回 role-aware summary：

- [../results/13_round1j_summary/round1j_patchback_summary.md](../results/13_round1j_summary/round1j_patchback_summary.md)

这一步的意义是：

- 最终报告不会再引用一个已经被后续轮次推翻的旧诊断

---

## 4. What Round 1 Can Now Defend

经过全部修复后，Round 1 现在可以 defend 的内容主要有 4 点。

### 4.1 Process-level selectivity is real

你已经看到：

- explicit use
- explicit reject
- reasoning format stabilization

这意味着：

- 这个项目不再停留在“只看最终分数”的黑箱比较

### 4.2 Mixed aggregate can be misleading

如果不区分：

- process sanity
- diagnostic
- boundary

也不区分：

- coarse pairing
- repaired pairing

那 aggregate 很容易得出错误结论。

### 4.3 Pairing granularity is not a secondary detail

Round 1 最强的方法论发现之一是：

**pairing granularity 本身就是结果的一部分。**

如果 `bridge` 只作为一个粗 cluster 使用，就可能把：

- subtype mismatch

误写成：

- memory harmful

### 4.4 Abstract memory must be executable, not just relevant

Round 1i 最重要的启示是：

- 相关经验并不自动等于可用经验
- 对 `consolidation` 来说，relevance 还不够
- 它必须把 relation operator 编码成可执行规则

否则：

- memory 仍然会把模型推向保守拒答或错误 branch

---

## 5. What Round 1 Should Not Claim

即使到现在，Round 1 仍然**不应该** claim：

- memory has strong average benchmark gain
- consolidation is universally better than episodic trace
- selective transfer has already been fully demonstrated on a large benchmark
- one repaired case is enough to prove broad generalization

这些结论都超出了当前 Round 1 的 scope。

更稳妥的说法应该是：

- Round 1 has established a usable diagnosis workflow
- and shown that seemingly negative transfer evidence can be overturned after repairing pairing granularity and operator-level abstraction

---

## 6. Final Round 1 Takeaway

如果要把整个 Round 1 压成一句最重要的话，我建议写成：

**Round 1 shows that evaluating memory selective transfer is highly sensitive to how relevance is operationalized: coarse pairing and non-executable abstractions can create false negative transfer evidence, while subtype-aware routing and operator-aware repair can recover the relevant memory path on the strongest diagnostic case.**

这比写：

- “memory works”
- “memory does not work”

都更准确，也更符合你最初的项目定位。

---

## 7. Next Step

现在最合理的下一步不再是继续围绕单个 case 开新的微调 round。  
更合理的是：

1. 用 [../results/13_round1j_summary/round1j_patchback_summary.md](../results/13_round1j_summary/round1j_patchback_summary.md) 更新最终 Round 1 叙述
2. 把本文件作为 Round 1 的高层 synthesis，直接服务于课程最终报告
3. 如果还有后续实验时间，再决定是否进入：
   - 更大范围的 repaired evaluation
   - 或更聚焦的 final report writing

一句话说：

**Round 1 现在应该收束到 synthesis 和 final reporting，而不是继续在同一个 diagnostic case 上做更多 prompt polishing。**
