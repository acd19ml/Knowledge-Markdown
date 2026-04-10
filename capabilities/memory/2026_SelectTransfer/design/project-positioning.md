# 项目定位说明

这份文件面向自己和队友。

它不是正式 `proposal`，也不是实验细节文档。它只负责反复回答几件事：

- 我们真正关心的大问题是什么
- 当前课程项目在这个大问题里处于哪一层
- 为什么现在做的是 `selective transfer`，而不是别的方向
- 当前阶段的成功、失败分别意味着什么

关联文档：

- [theory_lab/README.md](../../theory_lab/README.md)
- [proposal.md](./proposal.md)
- [experiment-contract.md](./experiment-contract.md)
- [../protocol/](../protocol/) — operational how-to docs

## 1. 原始动机

我们长期关心的问题不是 benchmark 分数本身，而是：

`experience -> reusable knowledge / lasting influence`

更直白地说，我们真正想研究的是：

- 一段过去经验什么时候只是被存下来
- 什么时候会变成后续可复用的东西
- 什么时候进一步变成持续塑造系统判断和行为的东西

这也是当前项目和 `theory_lab` 的关系。`theory_lab` 里讨论的是更高层的长期问题，例如过去经验如何留下持续影响、如何成为当前倾向的一部分。`2026_SelectTransfer` 不是偏离这个问题，而是从中切出一个课程项目能实际回答的实验切片。

当前这个切片不是去直接回答“memory 到底是什么”或者“经验如何完全内化”，而是去问一个更可实验的问题：

**当前的 `memory` 是否体现为 `selective transfer`，而不是 `indiscriminate reuse`。**

也就是说，这个项目不是在研究“memory 平均有没有帮助”，而是在研究：

- 该帮的时候，它能不能帮
- 不该帮的时候，它会不会乱帮

只要这个切片能被做清楚，它就和长期的 memory research 是连着的，而不是偏题。

## 2. 三层定位

### 高层

- 我们研究的是：经验什么时候变成可复用的东西，而不只是过去发生过的记录。
- 更长期的问题是：经验如何转化为可迁移知识，甚至转化为持续影响后续判断的结构。
- 这一层对应的是 `theory_lab` 里的长期方向，而不是当前课程项目要一次性解决的内容。

### 中层

- 当前课程项目研究的是：`memory usefulness` 是否应该被重新定义成 `selective transfer`。
- 如果一个 memory 真的有价值，它不应该只在平均分上看起来有帮助，而应该在 `Relevant` 情况下带来收益，在 `Irrelevant` 情况下避免负迁移。
- 这一层的问题足够具体，能够被 benchmark、pairing 和 split-specific metrics 压成可操作的 empirical question。

### 低层

- 当前阶段并不是在跑 `final experiment`，也不是在证明一个大的 memory 理论。
- 当前阶段的任务是验证 measurement setup 是否 working。
- 更准确地说，我们现在是在造一把“可用的尺子”，这把尺子包括 taxonomy、source set、pairing、artifact review 和 split-specific evaluation。
- 如果这把尺子本身不稳，后面的分数和现象都没有解释价值。

## 3. 为什么做这个，不做别的

### 不继续做 Reflexion / ExpeL 的“机制正确性批判”

这个方向诱人的地方在于，它看起来离“机制理解”很近，也容易显得有批判性。但它当前不适合作为课程项目，因为问题太依赖潜变量，结果一出来很难分清到底是 model 能力、prompt、benchmark、annotation，还是机制本身在起作用。现在这版 `selective transfer` 更好，因为它把问题压到了固定 setting、固定 split、固定指标下的可测现象。

### 不只做简单的 `episodic vs consolidation` 平均分对比

这个方向诱人的地方在于，它最容易做、最像标准 benchmark comparison。但它当前不够好，因为 average gain 不能回答“memory 是否被正确复用”这个更关键的问题。现在这版更好，因为它明确要求把 `Relevant / Irrelevant` 拆开看，而不是用一个总平均掩盖问题。

### 不一开始就做更大的 memory theory

这个方向诱人的地方在于，它最接近我们真正想关心的长期问题。但它当前不适合作为课程项目，因为 scope 过大、变量过多、很难在一个小实验里得到可 defend 的结论。现在这版更好，因为它是一个中间层问题：足够接近长期动机，但又能被压成一个受控实验。

## 4. 当前项目真正的产出

这个项目的产出不应只理解为“最后哪一组分数更高”，而至少包括三类东西。

### 一个更好的评估视角

不是只问 average gain，而是明确区分：

- `Relevant / Irrelevant`
- positive transfer / negative transfer

如果这个视角能站住，它本身就是对 memory evaluation 的推进。

### 一个更好的 protocol

也就是一套相对可 defend 的实验协议：

- taxonomy
- source set
- pairing
- split-specific metrics

这套 protocol 的价值在于，它把“memory 是否真的支持 selective transfer”这个问题，从泛泛而谈变成了可重复检查的实验流程。

### 一个路线判断

这个项目真正想给未来研究提供的是路线信号，而不是万能结论。结果出来以后，我们更希望回答的是：

- 后续更该往 `memory form` 走
- 更该往 `memory use` 走
- 还是两者耦合才是关键

所以即使结果不算强，只要 protocol 能工作、现象可解释，这个项目仍然有价值。它的目标不是证明一个万能结论，而是帮助确定下一步研究主轴。

## 5. 失败意味着什么

这里必须提前写清楚，避免后面把所有负结果都情绪化地理解成“项目没意义”。

### `protocol failure`

这类失败指的是实验尺子本身没有造稳，例如：

- taxonomy 不稳
- pairing 不干净
- artifact 太差

如果是这类失败，说明当前 protocol 还不能支撑后续解释。这里的问题首先不在理论，而在实验装置。

### `measurement failure`

这类失败指的是 protocol 看起来基本成立，但 setup 没有把 `selective transfer` 这个现象有效暴露出来。例如：

- `Relevant / Irrelevant` 区分度不够
- metric 太钝
- split 没有真正拉开

如果是这类失败，说明当前 measurement design 不够敏感，不代表问题本身不重要。

### `theoretical failure`

这类失败指的是 protocol 和 measurement 都比较稳，但 memory 仍然没有表现出预期差异。只有到了这一步，才有资格认真讨论：

- 当前关于 `selective transfer` 的工作假设是否不成立
- 或者 memory form / memory use 的作用并不像原先设想的那样

必须明确：

- 负结果先查 `protocol`
- 再查 `measurement`
- 最后才谈 `theory`

“没有效果” 不自动等于 “问题不重要”，也不自动等于 “长期方向错了”。

## 6. 现在所处位置

当前项目已经完成了一次重要压缩：`proposal` 已经从大而散的问题，收到了 `selective transfer` 这个更可测的中层问题上。与此同时，`experiment-contract`、`round` 文档和 `pilot workflow` 也都已经搭好。

所以现在的状态不是“完全没有方向”，而是：

- 不缺框架
- 不缺约束
- 不缺文档
- 缺第一轮真实材料

当前最缺的不是新想法，而是第一轮真实标注，以及由真实标注支撑起来的第一轮稳定 source-target pool。

因此下一步最重要的动作不是继续扩思路，也不是继续增加元文档，而是完成下面四件事：

- benchmark pool 全量列出
- taxonomy 初版标注
- source set 初版构造
- pairing 初版构造

这也是当前阶段最重要的提醒：

- 现在不要再把问题做大
- 不要急着讨论更远的 memory theory
- 不要过早加入更多条件
- 不要在没有真实标注和真实 pair 的情况下讨论 full experiment

如果读完这份文件后，自己或队友仍然答不出下面这些问题，就说明当前定位还没有真正稳定下来：

- 这个项目和长期 memory research 的关系是什么
- 这个项目现在具体在测什么，不在测什么
- 为什么现在不做更大、更直接、更花哨的问题
- 如果实验失败，第一反应应该检查什么
- 当前下一步最重要的动作是什么
