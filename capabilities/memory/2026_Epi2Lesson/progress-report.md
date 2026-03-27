# 课题 6 进展报告（progress report）

## 摘要（Abstract）

本进展报告（progress report）既记录已完成的实证工作，也记录由此对项目提案（project proposal）的修订。原项目旨在通过 **Reflexion** 与 **ExpeL** 研究大语言模型智能体（LLM agents）中的无参数自我改进（parameter-free self-improvement），侧重反思正确性（reflection correctness）、跨任务迁移（cross-task transfer）与检索效用（retrieval utility）。试点实验（pilot experiments）已成功搭建两套系统可运行的本地流水线（pipelines），并产出初步产物，包括 10 个案例的 Reflexion 失败集与在 ALFWorld 上的 ExpeL 冒烟训练（smoke-train）。但这些试点也表明：原研究问题难以干净回答，因其依赖「真实失败原因（true failure cause）」「真实可迁移性（true transferability）」等潜变量与混杂（confounded）构念。据此，项目改述为边界更清晰的实证研究：从情节经验（episodic experience）到可复用教训（reusable lessons）的抽象（abstraction），如何影响大语言模型智能体的跨任务复用（cross-task reuse）。修订后的提案更贴近课程课题风格：固定基准（benchmark）、受控对比、可解释指标。本报告将项目呈现为方法论上有依据的收窄过程，而非失败的第一次尝试，并指向更清晰的终稿研究设计。

## 1. 项目背景（project context）

项目最初聚焦大语言模型智能体中的 **无参数自我改进（parameter-free self-improvement）**，使用两个代表性系统：

- **Reflexion**：失败后存储自然语言自我反思（self-reflections），在重试时复用
- **ExpeL**：存储轨迹（trajectories），提取可复用洞见（insights），并进行跨任务经验检索

初始动机是超越总体基准分数，追问机制层面问题：

- Reflexion 是否正确诊断任务失败原因？
- ExpeL 提取的洞见是否产生有用的跨任务迁移？
- 检索相似度（retrieval similarity）是否对应实际运行效用？

这是有力的起点，因它旨在比简单复现项目更批判地评估智能体记忆与自我改进。但后续试点表明，该表述不适合有边界的课程项目。

## 2. 原提案下已完成工作（completed work under the original proposal）

### 2.1 Reflexion 流水线（pipeline）

项目在独立 conda 环境中为 ALFWorld 搭建了可运行的本地 Reflexion 流水线。已完成两阶段：

- 无记忆冒烟运行（no-memory smoke run）
- 启用记忆、生成反思并记录的冒烟运行（memory-enabled smoke run）

无记忆冒烟使用 `num_trials = 1`、`num_envs = 2`、`model = gpt-4o`，得到：

- `SUCCESS: 0`
- `FAIL: 2`
- `TOTAL: 2`

启用记忆的运行确认端到端「重试+反思（retry-with-reflection）」可用，且生成的反思写入日志。

### 2.2 Reflexion 失败试点（failure pilot）

为超越轶事级样例，在 `8` 个 ALFWorld 环境上运行了更大规模的启用记忆试点；与此前 2 环境记忆运行合并，得到 **10 个失败的 Reflexion 案例**，且反思非空。

10 案例标注集（annotation set）的早期模式如下：

- 主要格式/交互协议失败（formatting / interaction protocol failure）：`10 / 10`
- 次要泛化或不可执行推理失败（generic or non-actionable reasoning failure）：`8 / 10`
- 反思中较清晰提到可能问题：`6 / 10`
- 仅部分提到：`4 / 10`
- 判为完全可执行（fully actionable）：`0 / 10`

这已是实质性试点结果：Reflexion 往往注意到接近失败模式的内容，但反思通常过于泛化，难以充当可执行修复策略（executable repair policy）。

### 2.3 ExpeL 流水线（pipeline）

ExpeL 也已进入可运行状态，但兼容性工作多于 Reflexion。项目已解决与 OpenAI 兼容 API 路由、ALFWorld 环境兼容、包版本不一致、`gpt-4o` 的 `tiktoken` 支持，以及「每次运行恰好 134 个任务」的硬编码假设等问题。

修复后，4 任务 ALFWorld 冒烟训练（smoke-train）顺利完成并产出标准 ExpeL 产物。观测结果为：

- `Success: 1`
- `Fail: 2`
- `Halted: 1`

现阶段 ExpeL 尚未为原迁移或检索分析提供足够证据，但已建立可用的训练阶段路径与可持久化检视的产物。

## 3. 为何修订原提案（why the original proposal was revised）

试点阶段最重要的产出不仅是工程进展，更是方法论澄清（methodological clarification）。

原提案依赖的问题包括：

- 反思是否「真正」正确，
- 经验是否「真正」可迁移，
- 检索到的记忆是否「真的」相关。

在当前设定下难以干净回答，因其依赖定义薄弱或潜藏的构念：

- 任务失败往往有多种合理解释，
- 交互式基准（interactive benchmarks）可能混合推理错误与接口、协议失败，
- 可迁移性与任务措辞、基准结构、检索设计纠缠，
- 相关性（relevance）可指语义相似、程序重叠或因果效用。

因此，放大原计划很可能产生更多标注与产物，但中心主张仍弱。问题不在于工程不足，而在于原研究问题对清晰实证答案而言尚不够干净。

这一点很重要，因官方课程课题并非宽泛的可解释性问题，而是有边界的实证研究，要求：

- 固定基准或系统设定，
- 少量受控变量（controlled variables），
- 可解释指标。

原提案过于接近「智能体内部是否正确」——这是有趣的研究问题，但不最契合课程形式。

## 4. 修订后的提案（revised proposal）

修订后的项目题为：

> **从情节经验到可复用教训：评估大语言模型智能体跨任务复用中的经验抽象（From Episodic Experience to Reusable Lessons: Evaluating Experience Abstraction for Cross-Task Reuse in LLM Agents）**

中心问题是：

> **从情节经验到可复用教训的抽象，如何影响大语言模型智能体的跨任务复用？**

该方向更窄、更可辩护，因用受控变量替代潜藏的正确性：

- 所存储经验的抽象层次（abstraction level）

修订项目也与仓库中已有记忆框架对齐：

- **情节记忆（episodic memory）**：具体过去经验，
- **语义记忆（semantic memory）**：抽象稳定知识，
- **程序记忆（procedural memory）**：可复用例程与技能。

项目仅关注第一步过渡：

> `episodic experience -> reusable lesson`（情节经验 → 可复用教训）

这比此前对 Reflexion 与 ExpeL 的机制层批判更精确、边界更清晰。

## 5. 新提案为何更好（why the new proposal is better）

修订提案在四个方面更优。

### 5.1 使用可操纵变量（controllable variable）

项目不再评判模型内部诊断是否正确，而是比较两种显式记忆形式：

- **情节记忆（episode memory）**：对过去任务事件的具体、富含上下文的描述，
- **教训记忆（lesson memory）**：从同一经验中蒸馏出的可复用抽象。

### 5.2 提出有边界但仍开放的问题（bounded open question）

AWM、ExpeL、SkillWeaver 等工作表明抽象重要，但在所选设定下并未干净隔离：

> 对同一条源经验，存为具体情节与存为抽象教训，有何不同？

这不是普适未解难题，但在所选设定下也未被完全回答，适合课程项目。

### 5.3 契合课程课题风格

官方课题通常要求学生在固定基准下比较方法、配置或策略，调查有边界的实证问题。修订提案现遵循同一结构：

- 固定基准，
- 受控对比，
- 少量变量，
- 可解释指标。

### 5.4 使终稿有更清晰的研究叙事（research story）

项目可叙述为：

> 初始假设 → 试点证据 → 提案再评估 → 更尖锐的实证问题

这比堆积机制向标注却缺乏强终局主张的报告清晰得多。

## 6. 修订后的实验计划（revised experimental plan）

基准仍为 **ALFWorld**，但不是完整榜单复现，而是作为**受控子集基准（controlled subset benchmark）**，使可复用教训可解释。

修订计划围绕三项实验。

### 6.1 实验一：情节对比教训（Episode vs Lesson）

比较：

- `No memory`（无记忆），
- `Episode memory`（情节记忆），
- `Lesson memory`（教训记忆）。

主要指标：

- 成功率（success rate），
- 相对无记忆基线的迁移增益（transfer gain），
- 提示长度（prompt length）。

### 6.2 实验二：信息损失分析（information-loss analysis）

对每条源经验，识别情节抽象为教训时去除了哪些信息，例如：

- 对象特定细节，
- 环境特定约束，
- 前置条件（preconditions），
- 失败特定线索（failure-specific cues）。

再分析哪类被去除信息最常与复用失败对应。

### 6.3 实验三：复用对比过度泛化（reuse vs over-generalization）

在三类目标上测试情节记忆与教训记忆：

- `Reusable`（可复用），
- `Near-miss`（近失），
- `Unrelated`（无关）。

主要指标：

- 正迁移（positive transfer），
- 负迁移（negative transfer），
- 净效用（net utility）。

## 7. 范围与下一步（scope and next steps）

项目**刻意不**将检索设计、分阶段上下文注入（staged context injection）、完整工作流归纳或可执行技能合成作为研究主对象。这些主题有意义，但会过快扩大范围。

近期下一步：

1. 定义可复用教训可解释的受控 ALFWorld 子集，
2. 设计将源经验转为情节记忆与教训记忆的稳定模板，
3. 在 `No memory`、`Episode memory`、`Lesson memory` 间进行首次修订版对比实验。

## 8. 结论（conclusion）

项目当前阶段已同时产出真实实证产物与更成熟的研究方向。Reflexion 与 ExpeL 现可在本地运行；试点证据不仅证明可行，更说明原提案对清晰课程贡献而言方法论上过于不稳。

修订提案因此不是背离原想法，而是更好的表述：不问智能体是否内心正确理解自身失败，而问边界更清晰、可检验的问题：

> **从情节经验到可复用教训的抽象，如何影响大语言模型智能体的跨任务复用？**

这为终稿同时满足技术可执行与实证可辩护提供了更强路径。
