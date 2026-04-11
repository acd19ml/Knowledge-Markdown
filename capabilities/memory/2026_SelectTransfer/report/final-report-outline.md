# Final Report Outline

这份文件不是新的 `progress report`。

它的作用是把 `2026_SelectTransfer` 当前已经完成的材料，收束成**课程最终报告的装配计划**。在当前项目状态下，最重要的任务不再是继续开新实验，而是把已经完成的 `Round 1 -> 1j` 修复链条，组织成一个可 defend 的 final report。

## 1. 当前阶段判断

基于：

- [design/project-positioning.md](../design/project-positioning.md)
- [design/proposal.md](../design/proposal.md)
- [design/experiment-contract.md](../design/experiment-contract.md)
- [final-report-round1-section-v2.md](./final-report-round1-section-v2.md)

当前最合理的主线不是继续追加新的单-case repair round，而是：

1. 冻结 `Round 1` 的 canonical interpretation
2. 把 `Round 1` 写成最终报告成品
3. 只在时间非常充裕时，才考虑一个很小的 repaired validation round

一句话说：**现在应从 experiment mode 切到 final-report assembly mode。**

## 2. Final Report 目标

最终报告应该完成三件事：

1. 说明项目真正研究的问题不是 average gain，而是 `memory` 是否支持 `selective transfer`
2. 说明为什么 `Round 1` 的主要贡献是 methodological clarification，而不是简单的 benchmark improvement
3. 清楚区分：
   - 我们最终能 claim 什么
   - 我们不能 claim 什么

## 3. 推荐章节结构

### 3.1 Introduction

目标：

- 交代长期问题：`experience -> reusable knowledge / lasting influence`
- 说明课程项目为什么压成 `selective transfer`
- 指出当前 memory evaluation 的问题：只报 average gain，不拆 `Relevant / Irrelevant`

优先素材：

- [design/project-positioning.md](../design/project-positioning.md)
- [design/proposal.md](../design/proposal.md)

本节应回答：

- 为什么这个项目不是在做普通 benchmark comparison
- 为什么 `selective transfer` 是一个更合理的中层切片

### 3.2 Experimental Setting

目标：

- 写清 benchmark、source/target、memory conditions、固定模型、固定 budget
- 把实验对象收窄到 near-transfer setting

优先素材：

- [design/proposal.md](../design/proposal.md)
- [rounds/round_01_memory_form_pilot.md](../rounds/round_01_memory_form_pilot.md)
- [design/experiment-contract.md](../design/experiment-contract.md)

本节应回答：

- 我们测的到底是什么 setting
- 什么被固定，什么被当作变量

### 3.3 Evaluation Protocol

目标：

- 说明为什么不能直接做 naive aggregate
- 说明 taxonomy、source set、pairing、artifact review、case role discipline 的作用
- 交代 `bridge -> attribute_bridge / relation_chain_bridge` 的修复逻辑

优先素材：

- [progress-report-round1c-role-aware-smoke-repair.md](./progress-report-round1c-role-aware-smoke-repair.md)
- [progress-report-round1d-bridge-subtype-repair.md](./progress-report-round1d-bridge-subtype-repair.md)
- [progress-report-round1e-relation-chain-feasibility.md](./progress-report-round1e-relation-chain-feasibility.md)
- [results/13_round1j_summary/round1j_patchback_summary.md](../results/13_round1j_summary/round1j_patchback_summary.md)

本节应回答：

- 为什么 relevance 不是粗粒度标签就够
- 为什么 case role 必须先于 aggregate
- 为什么 consolidation 必须是 executable abstraction

### 3.4 Round 1 Results

目标：

- 不按流水账堆所有子轮次
- 按“问题暴露 -> 修复 -> 解释改变”的链条来写

推荐写法：

1. `Round 1 / 1b / 1c`
   - 让 process-level signal 可见
   - 停止混合 aggregate
2. `Round 1d / 1e / 1g`
   - pairing granularity repair
   - subtype-aware reroute 修复 episodic false negative
3. `Round 1h / 1i / 1j`
   - operator-level executable abstraction repair
   - consolidation false negative 被撤回

优先素材：

- [final-report-round1-section-v2.md](./final-report-round1-section-v2.md)
- [progress-report-round1-final-synthesis.md](./progress-report-round1-final-synthesis.md)
- [progress-report-round1i-kinship-operator-repair.md](./progress-report-round1i-kinship-operator-repair.md)

本节应回答：

- `wiki_dev_2639` 为什么是关键 case
- 为什么早期 “relevant memory hurts” 结论必须撤回
- 最终真正支持的结论是什么

### 3.5 Claims and Non-Claims

目标：

- 显式限制结论范围
- 防止 final report 又退回过度宣称

优先素材：

- [final-report-round1-section-v2.md](./final-report-round1-section-v2.md)
- [design/experiment-contract.md](../design/experiment-contract.md)

本节应至少包含：

- 能 claim：
  - process-level selectivity 可观察
  - coarse pairing 会制造 false negatives
  - executable abstraction 是 consolidation 的必要条件之一
- 不能 claim：
  - strong average benchmark gain
  - large-scale selective transfer 已被充分证明
  - consolidation universally better or worse

### 3.6 Limitations

目标：

- 承认 scale 和 sensitivity 的边界
- 把限制写成 scope，而不是写成项目失败

优先素材：

- [final-report-round1-section-v2.md](./final-report-round1-section-v2.md)
- [progress-report-round1-final-synthesis.md](./progress-report-round1-final-synthesis.md)

本节应至少写：

- repaired evidence 仍然高度依赖少数 diagnostic cases
- 当前模型固定为 `Qwen/Qwen3.5-9B`
- outcome-level repair 成功，不等于 process-level purity 完全恢复

### 3.7 Future Work

目标：

- 只写和当前结论自然衔接的下一步
- 不把未来工作写成新的愿望清单

推荐方向：

1. 用 repaired protocol 做一个更小但更 clean 的 validation subset
2. 扩 relation-chain diagnostics，而不是扩一堆新 memory conditions
3. 比较 `memory form` 与 `memory use` 的下一层问题

本节应避免：

- 直接宣称下一步要 full benchmark rerun
- 直接切到更大模型 / 更复杂 agent

## 4. 写作顺序

最终报告建议按下面顺序写，而不是从 Introduction 开始：

1. 先定 [final-report-round1-section-v2.md](./final-report-round1-section-v2.md) 的最终版
2. 再写 `Claims / Non-Claims`
3. 再写 `Evaluation Protocol`
4. 再写 `Limitations`
5. 最后回头写 `Introduction`

原因很简单：

- 你现在最稳定的是结果解释，不是开场叙述
- 先把 claim 边界写清楚，前面的 framing 才不会飘

## 5. 当前最该产出的文件

如果只做最必要的 final report assembly，优先补这三份：

1. `final-report-method-section.md`
2. `final-report-results-section.md`
3. `final-report-discussion-section.md`

其中：

- `method` 负责 setting + protocol
- `results` 负责 Round 1 repair chain
- `discussion` 负责 implication + limitations + future work

## 6. 现在不该做什么

- 不继续开新的 `Round 1k`
- 不再做更多单-case operator patch
- 不先换模型再回头重跑一堆
- 不把多个 progress 文档原样拼成 final report

## 7. 最短行动计划

当前建议的执行顺序：

1. 以 [final-report-round1-section-v2.md](./final-report-round1-section-v2.md) 为 Round 1 主体
2. 基于本大纲拆出 `method / results / discussion`
3. 用 [results/13_round1j_summary/round1j_patchback_summary.md](../results/13_round1j_summary/round1j_patchback_summary.md) 作为 `wiki_dev_2639` 修正解释的最终依据
4. 完成课程最终报告的 Round 1 部分后，再决定是否需要一个很小的 repaired validation round
