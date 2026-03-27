# 修订后课题 6 提案的实验框架（experiment framework）

> 主提案：[proposal.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2026_Epi2Lesson/proposal.md)  
> 关键论证：[proposal-analysis.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2026_Epi2Lesson/proposal-analysis.md)  
> 进展叙述：[progress-report.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2026_Epi2Lesson/progress-report.md)

---

## 1. 一句话项目定义（one-sentence project definition）

本项目追问：

> **当同一条源经验（source experience）分别以具体情节（concrete episode）与可复用教训（reusable lesson）两种形式存储时，后续的跨任务复用（cross-task reuse）会如何变化？**

本项目**不**研究：

- 检索（retrieval）是否最优，
- 提示编排（prompt orchestration）是否最优，
- 智能体是否在内部「正确」理解了失败，
- 或如何大规模自动生成最优教训（lesson）。

只操纵一个受控变量：

- **经验抽象（experience abstraction）**：`episode`（情节记忆）对比 `lesson`（教训记忆）

---

## 2. 为何这是合适的实验范围（experimental scope）

修订后的范围基于三点理由。

### 2.1 比原提案更窄

原提案追问的机制问题包括：

- 反思正确性（reflection correctness），
- 迁移正确性（transfer correctness），
- 检索相关性（retrieval relevance）。

这些问题难以干净收尾，因其依赖潜变量或定义不清的真值（ground truth）。

### 2.2 仍有开放性，但不过度开放

已有工作已表明：

- 抽象（abstraction）在某种形式上有帮助，
- 单靠格式（format）往往不是核心，
- 工作流（workflows）、洞见（insights）与技能（skills）有时可以迁移。

但已有工作**未能**干净隔离：

> **情节记忆（episodic memory）** 与同一条情节**蒸馏（distill）**出的 **lesson（教训记忆）** 之间的行为差异。

因此这是合理的课程项目问题：

- 在所选设定下尚未完全解决，
- 但可通过受控实验（controlled experiments）给出清晰答案。

### 2.3 符合官方课题风格

官方课题通常围绕：

- 有边界的实证问题（bounded empirical question），
- 明确的对比条件（comparison conditions），
- 具体指标（metrics），
- 可解释的权衡（interpretable tradeoffs）。

本提案现已贴合该模板。

---

## 3. 核心实验对象（core experimental objects）

### 3.1 情节记忆（episode memory）

对某一具体过去事件的、富含上下文的描述。

特点：

- 保留具体任务实例（task instance）细节，
- 保留具体对象与局部情境，
- 保留原始事件框架。

### 3.2 教训记忆（lesson memory）

从同一条源经验中蒸馏出的、可复用的抽象。

特点：

- 去除任务实例特有细节，
- 保留条件—行动式教训（condition-action lesson），
- 旨在超越原情节（episode）而复用。

### 3.3 基准（benchmark）角色

基准为 **ALFWorld**，但仅作为**受控子集基准（controlled subset benchmark）**。

原因：

- 当前基础设施中已可用，
- 执行成本较低，
- 成败易于解释，
- 适合受控记忆注入（memory injection）。

但：

- 部分 ALFWorld 失败由交互格式（interaction-format）问题主导，
- 因此必须过滤任务，使可复用教训在语义上可解释。

---

## 4. 实验矩阵（experimental matrix）

最小可用实验包为：

| 条件（Condition） | 注入的记忆（Memory injected） | 目的（Purpose） |
|---|---|---|
| `C0` | 无记忆（No memory） | 基线（baseline） |
| `C1` | 情节记忆（Episode memory） | 具体经验复用 |
| `C2` | 教训记忆（Lesson memory） | 抽象经验复用 |

目标任务（target tasks）分为：

| 目标类型（Target type） | 含义（Meaning） |
|---|---|
| `T1 Reusable`（可复用） | 源教训理应能带来帮助 |
| `T2 Near-miss`（近失） | 表面相似但关键约束不同 |
| `T3 Unrelated`（无关） | 无合理复用关系 |

由此得到最小矩阵：

- `C0/C1/C2 × T1/T2/T3`

已足以回答修订后的提案。

---

## 5. 实验（experiments）

## 实验一：情节（episode）对比教训（lesson）

### 问题（Question）

在后续任务上，教训记忆（lesson memory）是否比情节记忆（episode memory）更有帮助？

### 设计（Design）

对每个选定的源案例（source case）：

1. 收集一条源经验（source experience），
2. 构造 `episode`（情节）版本，
3. 从同一案例构造 `lesson`（教训）版本，
4. 在 `C0`、`C1`、`C2` 下对目标任务（target tasks）评估。

### 指标（Metrics）

- **成功率（Success Rate, SR）**
- 相对 `C0` 的 **迁移增益（Transfer Gain）**
- **提示长度（Prompt Length）**

### 为何重要（Why this experiment matters）

直接隔离本项目的主变量。

### 关键反思（Critical reflection）

- 有意义且不冗余。
- 也是提案中最干净的一组实验。
- 若该实验无法呈现可解释差异，整个修订提案会整体变弱。

---

## 实验二：信息损失分析（information-loss analysis）

### 问题（Question）

当情节（episode）变为教训（lesson）时，哪些信息被去除，哪些去除最损害复用？

### 设计（Design）

对每次 `episode -> lesson` 转换，标注被去除的信息类别，例如：

- 对象特定细节（object-specific details），
- 环境特定约束（environment-specific constraints），
- 前置条件（preconditions），
- 异常/失败线索（exception/failure cues），
- 局部动作顺序细节（local action-order details）。

再检验哪些去除类别与目标任务失败相关。

### 产出（Outputs）

- 按「被去除信息」类别统计的失败次数（failure count），
- 代表性的情节/教训对照表，
- 简短的定性讨论。

### 为何重要

没有这一步，提案会退化为简单的「谁赢」对比。

### 关键反思

- 这是项目获得深度的部分。
- 也会引入人工判断（manual judgment）。
- 因此样本必须刻意保持较小。

---

## 实验三：复用（reuse）对比过度泛化（over-generalization）

### 问题（Question）

教训记忆是否比情节记忆迁移更好，但也更常过度泛化？

### 设计（Design）

在以下类型上比较 `C1` 与 `C2`：

- `T1 Reusable`（可复用），
- `T2 Near-miss`（近失），
- `T3 Unrelated`（无关）。

### 指标（Metrics）

- **正迁移增益（Positive Transfer Gain）**
- **负迁移次数（Negative Transfer Count）**
- **净效用（Net Utility）**

### 为何重要

避免项目退化为「抽象总是更好」。

### 关键反思

- 该实验必不可少。
- 其有效性依赖 `Reusable / Near-miss / Unrelated` 的稳定定义。
- 这些标签必须在观察结果**之前**确定。

---

## 6. 评估汇总（evaluation summary）

项目应报告：

| 类别（Category） | 指标（Metrics） |
|---|---|
| 主任务结果 | `SR`，`Transfer Gain` |
| 紧凑性 | `Prompt Length` |
| 失败权衡 | `Negative Transfer Count`，`Net Utility` |
| 机制分析 | 按被去除信息类型的失败分解 |

项目**不应**声称超出上述指标所能支持的内容。

尤其不应声称：

- 「智能体真正理解了教训」，
- 「教训在客观上正确」，
- 或「本工作一般性地解决了跨任务记忆」。

---

## 7. 风险（risks）

### 风险一：ALFWorld 子集噪声过大

若所选任务主要由格式或接口协议（interface protocol）失败主导，实验测到的是接口脆弱性（interface brittleness），而非经验抽象。

缓解：

- 使用过滤后的子集，
- 文档说明所选任务为何支持可解释的教训构造。

### 风险二：教训构造过于主观

若情节版与教训版写法不一致，结果可能反映措辞质量而非抽象层次。

缓解：

- 使用固定构造模板（construction template），
- 控制教训生成方式，
- 避免变成自由形式的提示工程（prompting）问题。

### 风险三：项目再次野心过大

若把检索（retrieval）、触发（triggering）、渐进披露（progressive disclosure）或程序性技能归纳（procedural-skill induction）重新纳入主问题，提案会失去干净变量。

缓解：

- 检索固定，
- 注入方式固定，
- 聚焦 `episode -> lesson`。

---

## 8. 预期贡献（expected contribution）

本课程项目最站得住脚的贡献是：

> 在受控实证下，分析具体经验（concrete experience）被抽象为可复用教训（reusable lesson）时，其跨任务效用（cross-task utility）如何变化。

该贡献在规模上适度，但：

- 范围清晰，
- 可实证检验，
- 与仓库内记忆理论一致，
- 在所选设定下尚未被完全回答。

---

## 9. 近期下一步（immediate next action）

在任何大规模跑数之前，应先完成：

1. 针对 ALFWorld 的 **任务子集定义（task-subset definition）**，
2. **情节到教训的构造模板（episode-to-lesson construction template）**，
3. 小规模试点（pilot），覆盖：
   - 无记忆（No memory），
   - 情节记忆（Episode memory），
   - 教训记忆（Lesson memory）。

若试点呈现可解释差异，则修订提案在实验上可行。
