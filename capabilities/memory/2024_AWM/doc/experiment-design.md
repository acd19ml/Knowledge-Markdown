# AWM 复现实验设计（第一阶段）

> 本文档的目标不是提出新的批判性问题，而是**完整复现论文已经报告的核心实验结论**。
> 只有在这些结论被尽可能完整地验证之后，才进入第二阶段的批判性扩展。
> 具体命令、脚本入口、代码改动与运行顺序，统一放到 [experiment-protocol.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/experiment-protocol.md)。

---

## 1. 文档定位

当前阶段的任务是 **faithful reproduction**，不是批判性重设计。

这意味着本阶段优先回答的问题是：

1. 论文已经声称了哪些结论？
2. 每条结论对应哪组实验？
3. 这些实验在当前环境中能否复现出方向一致的结果？
4. 哪些结论被验证，哪些没有被验证？

因此，本文件不再以“我想挑战论文什么”为主线，而以“我要先把论文自己的结论逐条验证”为主线。

第二阶段才考虑：

- 原文未做但值得追问的问题
- 更强的机制分析
- 更严格的批判性假设检验

---

## 2. 第一阶段的总体目标

第一阶段的目标不是把论文所有细节全部重做一遍，而是尽可能完整地覆盖其**核心结论链条**：

- AWM 在 Mind2Web 上是否优于基线
- 这种提升主要体现在哪些指标上
- offline 与 online 在不同泛化场景下的表现关系是否一致
- LM-based workflow induction 是否优于较弱的规则归纳
- workflow 的表示形式与环境表示结论是否能复现
- workflow quality 的中间指标是否大体成立

如果这些结论都还没有被验证，就不应过早进入“提出新批判性问题”的阶段。

---

## 3. 复现成功的判据

本项目中的“复现成功”不应被定义为**绝对数值完全一致**，而应采用更稳健的判据。

### 3.1 最强判据：关键结论方向一致

例如：

- AWM 优于对应基线
- online 在更大 distribution gap 下相对更有优势
- LM induction 优于 rule induction
- NL description 优于 HTML

### 3.2 次强判据：相对排序一致

即使具体数值不同，只要方法间排序与论文大体一致，也可视为较强复现信号。

### 3.3 机制级判据：关键解释一致

如果不仅结果方向一致，而且伴随论文声称的关键现象也出现，则复现更有说服力。例如：

- 提升主要来自 `element accuracy`，而不是 `action F1`
- online 的优势随 train-test gap 增大而更明显
- rule induction 更容易保留完整、具体 trajectory 的偏差

### 3.4 失败判据

以下情况应视为未完成复现，而不是直接进入新问题分析：

- 主结果方向与论文相反
- 关键比较缺少对应 baseline
- 只跑了单个例子或极少样本，无法支撑结论
- 只看到总分，未检查论文强调的关键分解指标

---

## 4. 待复现的论文核心结论

本阶段以 `C1-C5` 为主线。

### C1：Mind2Web offline cross-task 主结果

要复现的论文结论：

- Offline AWM 在 Mind2Web `cross-task` 上优于基线
- 提升主要体现在 `element accuracy` 与 `step success rate`
- `action F1` 不一定同步提升，甚至可能略低

这对应论文第 3.2.1 节的主结果。

本结论的重要性最高，因为它是论文在 Mind2Web 上最核心的性能主张。

### C2：Online AWM 的泛化优势

要复现的论文结论：

- Online AWM 在 `cross-task`、`cross-website`、`cross-domain` 上都优于基线
- 随着 train-test distribution gap 增大，online 相对 offline 更有优势
- offline 在分布较匹配时仍可能更强

这对应论文第 3.2.2 节。

这部分不是单纯比较 online 和 offline 哪个“更好”，而是复现作者对二者适用边界的解释。

### C3：LM induction 优于 rule induction

要复现的论文结论：

- 在 Mind2Web 上，LM-based workflow induction 优于 rule-based induction
- 原因在于 LM 归纳出的 workflow 更抽象、更偏向可复用 sub-routines，而不是保留完整具体 trajectory

这对应论文第 4.1 节。

这部分很关键，因为它直接对应 AWM 的方法论核心，而不只是“加了 memory 有用”。

### C4：表示层消融的主要结论

要复现的论文结论：

- `code workflow` 与 `text workflow` 差异不大
- 使用 NL 描述环境状态通常优于加入 HTML

这对应论文第 4.2 与 4.3 节。

这部分优先级低于 C1-C3，但仍属于论文对“workflow 应该如何表示”的明确结论。

### C5：Workflow quality analysis

要复现的论文结论：

- 归纳出的 workflow 数量相对精简
- workflow 在测试中有较高 utility rate
- workflow 间功能重叠较低
- 在 Mind2Web cross-task 上，coverage 不必很高，但这不自动意味着 workflow 失败

这对应附录 A.3。

这部分的意义是补足中间证据，使复现不只停留在最终分数上。

---

## 5. 每条结论需要的证据

### 5.1 C1 需要的证据

至少需要以下结果：

| 证据 | 目的 |
|------|------|
| AWM offline 与基线的总体指标对比 | 验证主结果方向 |
| `element accuracy / action F1 / step SR / SR` 分解 | 验证提升主要来自哪里 |
| 至少一个稳定网站或设置下的完整结果 | 避免只靠零散案例下结论 |

对于 C1，最关键的问题不是“有没有提升”，而是“提升结构是否与论文一致”。

### 5.2 C2 需要的证据

至少需要以下结果：

| 证据 | 目的 |
|------|------|
| `cross-task / cross-website / cross-domain` 三档结果 | 复现泛化主张 |
| offline 与 online 的并排结果 | 复现两者关系 |
| distribution gap 增大时的趋势观察 | 检查作者解释是否成立 |

对于 C2，重点不是单一数字，而是三档泛化场景中的相对趋势。

### 5.3 C3 需要的证据

至少需要以下结果：

| 证据 | 目的 |
|------|------|
| LM induction 与 rule induction 的结果对比 | 复现方法比较 |
| workflow 示例或人工审计样例 | 支撑“更抽象、更可复用”的解释 |
| 指标分解，尤其是 element accuracy | 检查论文给出的原因是否出现 |

### 5.4 C4 需要的证据

至少需要以下结果：

| 证据 | 目的 |
|------|------|
| code vs text workflow 对比 | 复现“差异不大” |
| NL vs HTML vs NL+HTML 对比 | 复现环境表示结论 |

对于 C4，不必过度解释机制，重点是先确认论文报告的趋势是否成立。

### 5.5 C5 需要的证据

至少需要以下结果：

| 证据 | 目的 |
|------|------|
| `#workflows` | 检查 workflow 库是否紧凑 |
| `coverage` | 检查 workflow 对测试轨迹的覆盖 |
| `function overlap` | 检查冗余程度 |
| `utility rate` | 检查测试时 workflow 是否真的被用到 |

对于 C5，重点是用中间指标补全“为什么结果会这样”。

---

## 6. 实验优先级

本阶段不应平均用力，而应按论文主张的重要性排序。

### 第一优先级

- C1：Mind2Web offline cross-task 主结果

这是整篇论文在 Mind2Web 上最核心的结果。如果 C1 尚未站住，后面很多扩展都失去基础。

### 第二优先级

- C2：online 泛化结果
- C3：LM vs rule induction

这两部分共同回答“AWM 为什么有效、在什么条件下有效”。

### 第三优先级

- C4：表示层消融
- C5：workflow quality analysis

它们重要，但属于在主结果之后补强解释的部分。

---

## 7. 本阶段暂不进入的内容

以下内容明确留到第二阶段，不作为当前 `experiment-design` 的主线：

- 提出论文未做过的全新假设
- 设计原文没有对应主张的新对照组
- 围绕个别异常案例提前展开大规模机制批判
- 把“workflow 是否真的被用了”设为主问题并重写整套实验

这些问题并非不重要，而是它们应建立在“原文核心结论已被较完整复现”的前提上。

---

## 8. 第一阶段结束的标志

只有当下面条件大体满足时，才应进入第二阶段：

1. C1-C5 中的大多数核心实验已经有结果
2. 对每条结论，都能回答“是否复现成功”
3. 对未复现的部分，已能明确是实现问题、样本问题、设置差异，还是论文结论本身不稳
4. 已形成一份“论文结论复现状态表”

到那时，第二阶段的问题才会自然浮现，例如：

- 哪条论文解释最不稳
- 哪类结论只在特定设置下成立
- 哪些机制在论文中被声称但尚未真正证明

---

## 9. 与执行文档的边界

为了避免本文件重新膨胀成操作手册，以下内容不放在这里：

- 代码架构与脚本入口说明
- 命令行示例
- 运行顺序
- 输出目录规范
- 需要修改哪些脚本

这些都放在 [experiment-protocol.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/experiment-protocol.md)。

本文件是“这一阶段要复现哪些论文结论”；
[experiment-protocol.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/experiment-protocol.md) 是“如何把这些复现实验跑出来”。
