# 课题 6 — 从情节经验到可复用教训（From Episodic Experience to Reusable Lessons）

## 评估大语言模型智能体跨任务复用中的经验抽象（Evaluating Experience Abstraction for Cross-Task Reuse in LLM Agents）

### 背景（background）

大语言模型智能体（large language model agents, LLM agents）在多步推理与交互式决策任务上表现可期，但许多智能体在 **跨任务复用经验（reusing experience across tasks）** 上仍弱。现有系统常将经验存为三大类之一：

- **情节轨迹（episodic traces）**：具体过去轨迹或失败，
- **语义教训（semantic lessons）**：抽象的自然语言洞见，
- **程序性例程（procedural routines）**：工作流或可执行技能。

近期工作表明这些形式在部分设定下有用。例如 **Reflexion** 在失败后存储言语反思（verbal reflections），**ExpeL** 从过去轨迹提取可复用洞见，**AWM** 从成功经验归纳工作流（workflows）。但这些工作并未干净回答更基础的问题：

> **具体情节（concrete episode）何时成为可复用教训（reusable lesson）？**

本项目聚焦该抽象步骤。不研究智能体内部诊断是否「真正正确」，而研究更可操纵、可度量的问题：**同一条源经验（same source experience）的抽象层次（abstraction level）如何改变后续跨任务复用（cross-task reuse）。**

---

### 原提案为何修订（why the original proposal was revised）

原提案依赖的假设包括：

- Reflexion 是否正确诊断失败的真实原因，
- ExpeL 检索到的经验是否「真正相关」，
- 自我反思是否因果地导致后续恢复。

这些问题有趣，但难以操作化（operationalize）。它们依赖潜藏真值、主观失败归因，以及模型能力、环境协议、检索质量与提示设计之间的混杂。结果往往是难以定量辩护的解释。

修订提案因此从 **潜藏推理正确性（latent reasoning correctness）** 转向 **行为上可检验的经验抽象（behaviorally testable experience abstraction）**：

- 源经验固定，
- 检索流水线（retrieval pipeline）固定，
- 提示位置固定，
- 主操纵变量为 **所存储经验的抽象层次（abstraction level of the stored experience）**。

该表述更接近课程课题风格：定义有边界的实证对比，含明确条件、基准与指标。

---

### 中心研究问题（central research question）

> **从情节经验（episodic experience）到可复用教训（reusable lessons）的抽象，如何影响大语言模型智能体（LLM agents）的跨任务复用（cross-task reuse）？**

更具体地，项目追问：具体过去经验保留为 **情节（episode）** 与抽象为 **教训（lesson）** 何者更有用，以及该抽象过程中损失了哪些信息。

---

## 核心概念（core concepts）

本项目使用两种经验单位（experience units）。

### 1. 情节记忆（episodic memory）

对过去经验的具体、富含上下文的描述：

- 具体任务实例（task instance），
- 具体对象或实体，
- 具体失败或成功事件，
- 局部执行细节。

示例形式：

> 「在厨房任务中，智能体在先前步骤已成功的情况下，将冷却后的番茄放入微波炉时失败。」

### 2. 教训记忆（lesson memory）

从同一条经验中蒸馏出的、带条件的可复用抽象：

- 保留可执行的教训（actionable lesson），
- 去除任务实例特有细节，
- 旨在支持后续任务中的复用。

示例形式：

> 「当任务要求将物体放入目标容器时，在执行最终放置步骤之前，先确认目标处于可放置的有效状态。」

提案有意止于 `episode -> lesson`（情节→教训）这一过渡。**不**试图解决从完整程序技能或可执行工具 API 中推导的更大问题。

---

## 研究问题（research questions）

### RQ1. 复用效应（reuse effect）

当同一条源经验存为 **情节（episode）** 与存为 **教训（lesson）** 时，后续跨任务表现如何变化？

### RQ2. 信息损失（information loss）

情节抽象为教训时，哪类丢失信息最常导致复用失败？

### RQ3. 过度泛化（over-generalization）

教训是否比情节迁移更广，但在表面相似任务上产生更高 **错误泛化（false generalization）** 风险？

---

## 实验设计（experimental design）

### 基准选择（benchmark choice）

主基准为 **ALFWorld**，采用 **受控子集设定（controlled subset setting）**，而非完整规模复现。

理由：

- 纯文本、相对轻量，
- 支持对任务指令与结果进行受控操纵，
- 记忆注入后可直接观察成败，
- 当前项目基础设施中已可用。

但项目不把 ALFWorld 当作所有经验复用形式的完美代理。已知局限是部分 ALFWorld 失败来自交互协议（interaction protocol）问题而非有意义的语义教训。因此实验聚焦 **过滤后的任务子集（filtered subset of tasks）**，使可复用教训可解释且不被格式伪影（formatting artifacts）主导。

---

### 实验一：情节对比教训（Episode vs Lesson）

对每个选定的源案例：

1. 收集一条源成功/失败情节（source success/failure episode），
2. 构造 **情节记忆（episodic memory）** 版本，
3. 从同一案例构造 **教训记忆（lesson memory）** 版本，
4. 在三种条件下评估目标任务：
   - `No memory`（无记忆），
   - `Episode memory`（情节记忆），
   - `Lesson memory`（教训记忆）。

主要指标：

- **成功率（Success Rate, SR）**
- 相对无记忆基线的 **迁移增益（Transfer Gain）**
- **提示长度（Prompt Length）** 作为紧凑性代理（compactness proxy）

为何重要：

- 直接隔离主变量：从情节到教训的抽象。
- 已有工作比较轨迹、洞见、工作流或技能，但**未干净比较同一条源经验的两种抽象层次**。

关键反思：

- 该实验有意义。
- AWM、ExpeL、SkillWeaver 并未完全解决该问题。
- 但若其他变量不固定，任何效应都可能来自检索或提示差异而非抽象本身，说服力会下降。

---

### 实验二：信息损失分析（information-loss analysis）

对每个源案例，相对原始情节标注教训版本中被去除的信息。候选 **信息损失类别（information-loss categories）** 包括：

- 对象特定细节（object-specific details），
- 环境特定约束（environment-specific constraints），
- 前置条件（preconditions），
- 异常或失败线索（exception or failure cues），
- 局部动作顺序细节（local action-order details）。

对目标任务失败，分析哪类缺失信息最可能解释失败。

主要产出：

- 按缺失信息类型的失败计数，
- 情节记忆与教训记忆按类别的对照，
- 代表性案例的简明定性表。

为何重要：

- 超越「谁更好」，追问 **抽象为何失败**。

关键反思：

- 这是项目中最偏分析的部分。
- 引入人工判断，规模须小且受控。
- 仍符合允许分类分析与针对性人工评估的课程课题风格。

---

### 实验三：复用对比过度泛化（reuse vs over-generalization）

目标任务分为三组：

- **Reusable（可复用）**：源教训理应能带来帮助，
- **Near-miss（近失）**：表面相似但关键约束已变，
- **Unrelated（无关）**：无合理复用关系。

再在这些组上比较情节记忆与教训记忆。

主要指标：

- **正迁移增益（Positive Transfer Gain）**
- **负迁移次数（Negative Transfer Count）**
- **净效用（Net Utility）** = 正迁移收益减去有害案例

为何重要：

- 防止项目退化为「抽象总是更好」的简化论断。

关键反思：

- 该实验重要但敏感。
- 最难的是一致定义 `Reusable / Near-miss / Unrelated`。
- 为可辩护，这些类别须在跑实验**前**定义，而非观察结果后定义。

---

## 范围控制（scope control）

为使项目可完成，以下明确 **超出范围（out of scope）**：

- 设计新检索算法（retrieval algorithm），
- 将渐进披露（progressive disclosure）或分阶段上下文注入（staged context injection）作为主问题研究，
- 大规模从原始轨迹自动生成最优教训，
- 完整程序性技能归纳或可执行 API 合成（executable API synthesis），
- 证明智能体内部解释是否「真正正确」。

这些是有价值的扩展，但纳入会模糊主变量并重现原提案的方法论问题。

---

## 预期贡献（expected contribution）

本项目旨在为智能体记忆中的一步具体但研究不足的过渡提供 **受控实证分析（controlled empirical analysis）**：

> 从 **具体情节经验（concrete episodic experience）** 到 **可复用语义教训（reusable semantic lesson）** 的转变。

若成功，将澄清：

- 教训级抽象是否改善跨任务复用，
- 哪些信息不应被抽象掉，
- 抽象何时开始过度泛化（over-generalize）。

这比泛泛声称无参数自我改进（parameter-free self-improvement）是否「普遍有效」更紧、更可辩护。

---

## 局限性（limitations）

- 基准受控且简化；结论未必直接迁移到更丰富 GUI 或真实环境。
- 教训构造可能涉及人工或模板化抽象，故项目研究抽象的 **效应** 而非完全自动化抽象。
- 项目仅涉及 `episodic -> lesson`（情节→教训）步骤，不涉及后续 `lesson -> procedural skill`（教训→程序性技能）过渡。

对课程项目可接受，因目标不是解决完整终身记忆问题，而是在其中隔离一个清晰、可度量的开放问题。

---

## 参考文献（references）

1. Shinn N, Cassano F, Labash A, et al. Reflexion: Language agents with verbal reinforcement learning. *Advances in Neural Information Processing Systems*, 2023, 36.
2. Zhao A, Huang D, Xu Q, et al. ExpeL: LLM agents are experiential learners. *Proceedings of the AAAI Conference on Artificial Intelligence*, 2024, 38(17): 19632–19642.
3. Wang Z Z, Mao J, Fried D, et al. Agent workflow memory. *arXiv preprint*, 2024.
4. Zheng B, Fatemi M Y, Jin X, et al. SkillWeaver: Web agents can self-improve by discovering and honing skills. *arXiv preprint*, 2025.
5. Park J S, O’Brien J C, Cai C J, et al. Generative agents: Interactive simulacra of human behavior. *Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology*, 2023.
6. Shridhar M, Yuan X, Côté M A, et al. ALFWorld: Aligning text and embodied environments for interactive learning. *International Conference on Learning Representations*, 2021.
