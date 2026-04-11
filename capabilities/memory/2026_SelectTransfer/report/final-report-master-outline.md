# Final Report — Master Outline

这份文件是最终课程报告的**总装配清单**。

它不重复写实验内容，而是回答三个问题：

1. 最终报告应该按什么章节顺序组织
2. 每一节优先使用哪些现有文件
3. 哪些内容应进入正文，哪些内容应留在 supporting layers

## 1. 推荐成品结构

建议把最终报告收成下面 8 节：

1. `Abstract`
2. `Introduction`
3. `Experimental Setting`
4. `Evaluation Protocol`
5. `Round 1 Results`
6. `Discussion`
7. `Limitations`
8. `Future Work`

如果老师要求篇幅更短，可以把：

- `Experimental Setting` + `Evaluation Protocol` 合并成 `Method`
- `Discussion` + `Limitations` + `Future Work` 合并成 `Discussion`

## 2. 章节到文件的映射

### 2.1 Abstract

目标：

- 一段话说明问题、方法、核心结果、范围边界

优先来源：

- [final-report-round1-section-v2.md](./final-report-round1-section-v2.md)
- [final-report-results-section.md](./final-report-results-section.md)
- [final-report-discussion-section.md](./final-report-discussion-section.md)

摘要里应保留：

- 研究的是 `selective transfer`
- 主要贡献是 methodological clarification
- 关键诊断 case 经 repair 后 overturn 了早期 false negative

摘要里不要写：

- 太多 round 编号
- 所有 repair 细节
- 任何超出 scope 的 general claim

### 2.2 Introduction

目标：

- 从长期问题切到课程项目的中层问题

优先来源：

- [design/project-positioning.md](../design/project-positioning.md)
- [design/proposal.md](../design/proposal.md)

建议保留：

- `experience -> reusable knowledge / lasting influence`
- 为什么不看 average gain，而看 `selective transfer`
- 为什么课程项目需要把问题压成 near-transfer empirical slice

### 2.3 Experimental Setting

目标：

- 用最短篇幅交代实验 setting

优先来源：

- [final-report-method-section.md](./final-report-method-section.md)
- [design/proposal.md](../design/proposal.md)

建议保留：

- `HotpotQA -> 2WikiMultiHopQA`
- `Qwen/Qwen3.5-9B`
- `N = 5`
- 三种 memory condition

### 2.4 Evaluation Protocol

目标：

- 说明为什么这个实验的核心不只是跑分，而是 protocol design

优先来源：

- [final-report-method-section.md](./final-report-method-section.md)
- [round1-evidence-map.md](./round1-evidence-map.md)
- [round1-case-appendix.md](./round1-case-appendix.md)

建议保留：

- case-role discipline
- subtype-aware pairing
- executable abstraction
- structured `Reasoning / Final Answer` scaffold

这一节最好明确一句：

> The protocol is part of the result, not merely a preprocessing detail.

### 2.5 Round 1 Results

目标：

- 这是正文最核心的一节
- 用 repair chain 组织结果，而不是按时间流水账平铺

优先来源：

- [final-report-round1-section-v2.md](./final-report-round1-section-v2.md)
- [final-report-results-section.md](./final-report-results-section.md)
- [round1-case-appendix.md](./round1-case-appendix.md)

推荐子结构：

1. `Making the experiment observable`
2. `Repairing pairing granularity`
3. `Repairing operator-level abstraction`
4. `Key diagnostic case: wiki_dev_2639`
5. `Claims and non-claims`

这一节建议把 [round1-case-appendix.md](./round1-case-appendix.md) 当 supporting appendix 来引用，而不是把所有 raw excerpts 全部搬进正文。

### 2.6 Discussion

目标：

- 把结果升到理论解释层，但不越界

优先来源：

- [final-report-discussion-section.md](./final-report-discussion-section.md)
- [final-report-round1-section-v2.md](./final-report-round1-section-v2.md)

建议保留：

- relevance 必须在对的 granularity 上 operationalize
- consolidation 必须保留 executable operator structure
- apparent negative transfer can be a protocol artifact

### 2.7 Limitations

目标：

- 主动约束结论范围

优先来源：

- [final-report-round1-section-v2.md](./final-report-round1-section-v2.md)
- [final-report-discussion-section.md](./final-report-discussion-section.md)

建议保留：

- repaired evidence 仍然集中在少数 diagnostic cases
- `wiki_dev_2639` 是最强但仍是单 case
- `Qwen/Qwen3.5-9B` 限制
- outcome-level repair != full process purity

### 2.8 Future Work

目标：

- 只保留最自然的下一步

优先来源：

- [final-report-discussion-section.md](./final-report-discussion-section.md)
- [final-report-outline.md](./final-report-outline.md)

建议保留：

- 用 repaired protocol 做一个更 clean 的 validation subset
- 扩 relation-chain diagnostics
- 不要写 full rerun / model escalation 作为默认下一步

## 3. 正文 vs Supporting Layers

### 正文应放什么

- 研究问题
- setting
- protocol principles
- repair chain 的高层结果
- claim / non-claim
- limitations

### L2 应放什么

- [round1-evidence-map.md](./round1-evidence-map.md)
- 每个 claim/non-claim 的证据链

### L3 应放什么

- [round1-case-appendix.md](./round1-case-appendix.md)
- 关键 case 的 raw evidence

也就是说：

- **正文负责论证**
- **L2 负责 traceability**
- **L3 负责 raw evidence**

## 4. 最推荐的装配顺序

不要从 `Introduction` 开始写整篇。

建议按这个顺序装配：

1. 先定 [final-report-round1-section-v2.md](./final-report-round1-section-v2.md) 作为正文主叙述
2. 再把 [final-report-method-section.md](./final-report-method-section.md) 吸收到 `Method`
3. 再把 [final-report-results-section.md](./final-report-results-section.md) 吸收到 `Results`
4. 再把 [final-report-discussion-section.md](./final-report-discussion-section.md) 吸收到 `Discussion / Limitations / Future Work`
5. 最后回头压缩 `Introduction` 和 `Abstract`

这样做的原因是：

- 你现在最稳定的是结果解释
- 不是开场 framing

## 5. 建议的最小提交版本

如果时间有限，最终课程报告至少应包含：

- `Introduction`
- `Method`
- `Results`
- `Discussion`

并把这三层材料作为 supporting references：

- [final-report-round1-section-v2.md](./final-report-round1-section-v2.md)
- [round1-evidence-map.md](./round1-evidence-map.md)
- [round1-case-appendix.md](./round1-case-appendix.md)

## 6. 当前下一步

现在最自然的动作不是再扩实验，而是：

1. 用这份 master outline 作为最终报告章节骨架
2. 把已有 `method / results / discussion` 三份成品合并到课程报告主文档
3. 只在需要 supporting evidence 时，引用 L2 / L3

一句话说：

**现在已经具备 final report assembly 所需的材料，接下来应从“写更多局部文件”切到“组装最终提交稿”。**
