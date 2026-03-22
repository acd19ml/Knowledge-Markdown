# AWM 深度复现研究路线图

> 本文档从更高层次定义整个 AWM 项目的研究路线。
> 它不替代 [experiment-design.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/experiment-design.md) 或 [experiment-protocol.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/experiment-protocol.md)，而是回答一个更大的问题：
> **为了在 final report 中产出“有深度的复现”，整个项目应该分几步推进，每一步要解决什么问题，最终怎样形成有说服力的论证。**

---

## 1. 项目总目标

这个项目的目标不是停留在“我把论文分数复现出来了”，也不是一开始就直接做反驳。

更高层的目标是完成一次**深度复现（deep reproduction）**：

- 先验证论文明确声称的结论是否成立
- 再解释这些结论为什么成立
- 最后系统寻找论文没有展开说明的边界、失败模式和不 work 的部分

换句话说，最终报告要回答的不只是：

> AWM 能不能 work？

而是进一步回答：

> AWM 为什么 work？
> 它到底靠什么 work？
> 它在哪些条件下不 work，或者没有论文写得那么稳？

这才是“有深度的复现”。

---

## 2. 总体研究策略

整个项目可以分为三个层次递进的问题。

### 层次一：论文声称是否成立

这是最基础的问题。

如果连论文已经写出来的主结果都没有被验证，那么后续所有机制分析和边界分析都会缺少支点。

这一层对应：

- faithful reproduction
- 对论文主表和核心消融的复现

### 层次二：论文结论为什么成立

当第一层基本站住后，下一步不是立即寻找反例，而是解释：

- AWM 的主要收益到底来自哪里
- 它改善了 agent 的哪个部分
- 它的 workflow abstraction 相比具体 exemplars 到底提供了什么额外价值
- offline / online 的差异究竟由什么机制驱动

这一层的目标是把“结果”推进成“机制解释”。

### 层次三：论文没有说清楚的部分是什么

只有在前两层完成后，第三层的问题才有意义：

- 哪些条件下 AWM 不 work
- 哪些情况下 workflow 会误导 agent
- 哪些论文中的解释其实只在局部成立
- 哪些边界条件、trade-off 或 failure mode 没有被作者展开

这一层不是为了“找茬”，而是为了把复现推进到比论文原文更完整的理解。

---

## 3. 项目的三阶段结构

为了让整个研究过程可执行，可以把项目明确分成三个阶段。

### 阶段一：结论复现

目标：

- 复现论文已经报告的核心结论

回答的问题：

- 论文表中的关键结果能否在当前环境中重现
- 方向、排序和关键现象是否一致

主要产物：

- C1-C5 的复现结果表
- 论文结论复现状态表

对应文档：

- [experiment-design.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/experiment-design.md)
- [experiment-protocol.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/experiment-protocol.md)

阶段完成标志：

- 大部分论文核心结论都已有明确的“复现成功 / 未成功”判断

### 阶段二：机制解释

目标：

- 解释 AWM 为什么 work

回答的问题：

- AWM 的提升主要来自 element grounding、action guidance，还是别的环节
- workflow abstraction 相对具体 trajectory memory 的价值是什么
- LM induction 相对 rule induction 的优势究竟体现在哪
- online / offline 的差异是否真的由 train-test distribution gap 驱动

主要产物：

- 机制分析表
- 指标分解图
- 典型案例分析
- failure taxonomy 初稿

这一阶段的关键词不是“新实验越多越好”，而是：

- 结果解释
- 机制归因
- 将论文中的 verbal claim 变成证据链

### 阶段三：边界与未说出的部分

目标：

- 找出论文没有展开写清楚的地方

回答的问题：

- AWM 在什么情形下失效
- workflow 在什么情形下会过度引导
- workflow quality 与 test-time gain 的关系是否稳定
- 哪些论文写出的优势只在特定条件下成立

主要产物：

- 边界条件表
- 负结果汇总
- “works / does not work / unclear” 三分结论

这一阶段的重点不是“推翻论文”，而是：

- 识别论文没有覆盖的局部不稳定性
- 识别作者没有展开讨论的 trade-off

---

## 4. 为什么必须按这个顺序推进

这个顺序不是形式主义，而是论证结构的需要。

### 4.1 如果没有阶段一，就没有可信的阶段二

如果主结果都还没站住，就很难说清：

- 到底是论文机制有问题
- 还是你根本没复现到同一个设置

### 4.2 如果没有阶段二，阶段三会流于“找异常点”

如果没有机制解释，看到某些失败案例时，你无法判断：

- 这是实现噪声
- 这是数据偶然性
- 还是 AWM 方法本身的结构性边界

### 4.3 深度复现不是“先批判”，而是“先理解，再定位边界”

导师要的不是简单复述论文，也不是轻率质疑。

导师要的是：

- 你知道它为什么值得发表
- 你知道它真正 work 的部分是什么
- 你也知道它没有说出的局限在哪里

---

## 5. 每个阶段的核心研究问题

为了让整条路线更清楚，可以把每一阶段压缩成一个核心问题。

### 阶段一核心问题

> 论文已经声称的结论，在我的环境里是否成立？

### 阶段二核心问题

> 如果这些结论成立，它们到底是靠什么成立的？

### 阶段三核心问题

> 在论文没有展开说明的地方，AWM 的边界和失败模式是什么？

这三层问题合起来，才构成 final report 所需的完整深度。

---

## 6. Final Report 应有的论证结构

从 final report 反推，项目应该积累三类证据。

### 第一类：确认性证据

用来说明：

- 论文主结论并非只存在于原文表格里
- 在当前复现环境中，核心趋势依然成立

这部分对应阶段一。

### 第二类：解释性证据

用来说明：

- AWM 的有效性来自哪些具体机制
- 哪些指标变化支撑了论文的叙述
- 哪些 workflow 特性与性能提升相关

这部分对应阶段二。

### 第三类：边界性证据

用来说明：

- AWM 并非无条件有效
- 论文未写出的不 work 情况是什么
- 有哪些 trade-off、局限与风险

这部分对应阶段三。

如果这三类证据都齐了，final report 才会真正有层次：

- 不是只报结果
- 不是只做口头分析
- 不是只列几个失败例子

而是形成“结果成立 -> 机制解释 -> 边界辨认”的完整闭环。

---

## 7. 当前文档体系在整个项目中的位置

当前建议把文档分成三层。

### 7.1 路线层

负责回答：

- 整个项目为什么这样推进
- 先做什么，后做什么
- 每一阶段的目标是什么

对应文档：

- [research-roadmap.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/research-roadmap.md)

### 7.2 设计层

负责回答：

- 当前阶段要复现或验证哪些结论
- 成功判据是什么

对应文档：

- [experiment-design.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/experiment-design.md)

### 7.3 执行层

负责回答：

- 这些实验具体怎么跑
- 需要保存哪些产物
- 结果怎么组织

对应文档：

- [experiment-protocol.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/experiment-protocol.md)

这样的层次结构有一个好处：

- 路线层不被命令污染
- 设计层不被高层叙事拖散
- 执行层不承担研究定位

---

## 8. 从现在开始的实际推进计划

结合当前进度，后续建议按下面方式推进。

### 8.1 先完成阶段一

优先完成：

- C1：Mind2Web offline cross-task 主结果
- C2：online 泛化结果
- C3：LM vs rule induction

原因：

- 这三项最能决定论文主张是否站得住

### 8.2 在阶段一后半程同步为阶段二留证据

即使当前不正式进入机制分析，也应在跑实验时提前保存：

- 逐样本结果
- workflow 文本
- induction 输入
- 中间指标

否则第二阶段会被迫返工。

### 8.3 阶段一结束后再启动阶段二文档

建议在阶段一结束后再新建单独文档，例如：

- `mechanism-analysis.md`

专门记录：

- 为什么 AWM work
- 哪些证据支持这些解释

### 8.4 阶段二完成后再启动阶段三文档

建议届时再新建：

- `boundary-analysis.md`

专门记录：

- 哪些地方不 work
- 哪些现象论文没有说
- 哪些结论只局部成立

---

## 9. 这份路线图对 final report 的直接意义

如果你最终按这条路线推进，那么 final report 将不只是“复现论文”。

它将具备三层价值：

### 9.1 第一层价值：确认论文不是偶然结果

你能说明：

- 论文主要结论在你的环境里仍能成立

### 9.2 第二层价值：解释论文为什么成立

你能说明：

- AWM 的有效性背后有哪些真正起作用的因素

### 9.3 第三层价值：补上论文没有写出的部分

你能说明：

- AWM 不 work 的边界是什么
- 哪些 trick 是关键
- 哪些隐藏前提没有在论文中被充分展开

这正是导师所要求的“有深度的复现”。

---

## 10. 当前结论

对当前项目而言，最重要的判断是：

> 现在还不应该直接跳去做大规模批判性问题设计，
> 但也不应该把目标仅仅定义为“复现论文表格”。

更准确的定位是：

> 先完成论文结论复现，
> 再进入机制解释，
> 最后系统梳理论文没有说清楚的边界条件。

这三步连起来，才是整个 AWM 项目的完整研究计划。
