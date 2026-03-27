## 课题 6：从情节经验到可复用教训（From Episodic Experience to Reusable Lessons）

> 本文档不重复 [proposal.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2026_Epi2Lesson/proposal.md) 的全文，目的在于检验：修订后的提案在方法论上是否成立、对课题 6 是否仍足够开放、又是否足够有边界以成为可辩护的课程项目。

---

## 1. 变更内容（what changed）

此前项目表述侧重 **对 Reflexion 与 ExpeL 的压力测试（stress-testing）**，问题包括：

- Reflexion 是否正确诊断失败原因，
- ExpeL 检索到的经验是否「真正相关」，
- 反思式或经验式记忆是否如原论文所述那样起作用。

这些问题有趣，但方法论上不稳定，依赖：

- 主观失败归因（failure attribution），
- 潜藏推理正确性（latent reasoning correctness），
- 模型能力、提示设计、检索质量与环境协议之间的混杂（confounds），
- 「诊断正确性（diagnostic correctness）」「真实相关性（true relevance）」等概念薄弱或缺失的真值（ground truth）。

修订提案远离此类潜藏主张，转而研究更可操纵的问题：

> **从情节经验（episodic experience）到可复用教训（reusable lessons）的抽象，如何影响大语言模型智能体（LLM agents）的跨任务复用（cross-task reuse）？**

这一变更并非表面措辞：项目从 **解释内部认知（interpreting internal cognition）** 转向 **测量被操纵的记忆表征（memory representation）的行为效应（behavioral effect）**。

---

## 2. 新方向为何更好（why this new direction is better）

### 2.1 使用可操纵变量（controllable variable）

关键操纵对象现为 **同一条源经验以不同抽象层次表达**：

- 情节记忆（episodic memory），
- 教训记忆（lesson memory）。

这比追问模型解释是否「真的对」干净得多。

### 2.2 与仓库内记忆理论基础对齐

仓库内记忆综述已指出 **情节记忆（episodic memory）**、**语义记忆（semantic memory）**、**程序记忆（procedural memory）** 之间的过渡：

- **情节记忆（episodic memory）**：具体过去经验，
- **语义记忆（semantic memory）**：抽象稳定知识，
- **程序记忆（procedural memory）**：可复用例程与策略。

参见：

- [2.2_cognitive-mechanisms.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/survey/02_taxonomy/2.2_cognitive-mechanisms.md)
- [3.2_dynamic-experience.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/survey/03_env-centric/3.2_dynamic-experience.md)

修订提案研究该记忆阶梯中的一步：

> **情节经验 → 语义化教训（episodic experience -> semantic lesson）**

使项目在理论上扎根而不致过大。

### 2.3 契合官方课程课题风格

五个官方课题并非要求学生解决完全开放的未解前沿问题，而是要求：

- 有边界的实证问题（bounded empirical question），
- 受控对比（controlled comparisons），
- 明确指标（metrics），
- 可解释分析（interpretable analysis），
- 在直接复现之外有限但有意义的扩展。

修订提案遵循该模式：不声称解决终身记忆（lifelong memory），而追问可通过清晰实验矩阵（experimental matrix）检验的更窄问题。

---

## 3. 批判性反思：是否仍过宽？（critical reflection: is this still too broad?）

是——若范围不明确，很容易再次变宽。

### 3.1 风险：「语义抽象（semantic abstraction）」沦为空洞口号

若项目只说：

> 「我研究语义抽象层次。」

则变量仍欠具体化。抽象可去除多种信息：

- 对象身份（object identity），
- 环境特定约束，
- 失败线索（failure cues），
- 前置条件（preconditions），
- 动作顺序细节（action-order details）。

修订提案因此避免泛用的「低/中/高抽象」用语，只使用两个单位：

- **Episode（情节）**，
- **Lesson（教训）**。

这是刻意的，使问题可解释。

### 3.2 风险：项目变成检索研究（retrieval research）

你已指出：

- 记忆是否被触发主要是检索（retrieval）问题，
- 渐进披露（progressive disclosure）主要是上下文工程（context-engineering）问题。

若这些成为中心，主变量不再是抽象。因此项目将检索与注入方式视为 **受控背景选择（controlled background choices）**，而非主要贡献。

### 3.3 风险：项目变成提示工程（prompt engineering）

若教训构造非正式或随意，任何增益可能仅反映文笔而非有原则的抽象步骤。

因此提案须明确：

- 教训构造将 **基于模板或人工受控（template-based or manually controlled）**，
- 项目研究抽象的 **效应（effect）**，
- **不**试图解决自动抽象生成（automatic abstraction generation）。

该限制是必要约束，而非弱点。

---

## 4. 该问题是否已被解决？（is this problem already solved?）

未完全解决，但部分已在间接意义上被讨论。

### 4.1 AWM 已回答的内容

AWM 已研究工作流表征（workflow representation）的多个问题：

- 语言模型诱导的抽象（LM-induced abstraction）对比基于规则的复用（rule-based reuse），
- 代码工作流（code workflow）对比文本工作流（text workflow），
- 自然语言环境描述（NL environment description）对比 HTML 增强描述（HTML-enhanced description）。

这些结果已暗示：

- 抽象重要，
- 表面格式（surface format）较次要，
- 更多具体细节并不总有益。

修订提案因此 **不应** 再问：

- 工作流应为代码还是文本，
- 更多 HTML 细节是否改善记忆，
- 子程序抽象是否根本有帮助。

这些问题已有相当探索。

### 4.2 仍开放的部分

AWM、ExpeL、SkillWeaver 均在 **跨系统比较不同记忆对象**，但未能干净隔离：

> **情节（episode）** 与同一条情节**蒸馏出的教训（lesson distilled from the same episode）** 之间的行为差异。

这是本提案利用的缺口（gap）。

### 4.3 该缺口为何仍有意义

这不是「无人讨论过抽象」式的新颖性主张，而是更窄、更强的主张：

> 已有工作尚未提供 **同源情节记忆对比教训级记忆（same-source episodic vs lesson-level memory）** 的受控比较，以及二者之间的信息损失权衡（information-loss tradeoff）。

这对课程项目已足够。

---

## 5. 实验逻辑（experimental logic）

修订提案应作为受控实证研究评估，而非宽泛架构项目。

### 实验一：情节对比教训（Episode vs Lesson）

比较：

- 无记忆（no memory），
- 情节记忆（episode memory），
- 教训记忆（lesson memory）。

回答抽象是否改变复用表现。

### 实验二：信息损失分析（information-loss analysis）

追踪情节转为教训时丢弃的信息，再分析哪类被去除信息与后续失败相关。

这是项目超越基准表（benchmark table）的部分。

### 实验三：正复用对比过度泛化（positive reuse vs over-generalization）

在以下目标上评估情节记忆与教训记忆：

- 可复用目标（reusable targets），
- 近失目标（near-miss targets），
- 无关目标（unrelated targets）。

防止项目退化为「抽象越多越好」的简化论断。

---

## 6. ALFWorld 是否是合理基准？（is ALFWorld a reasonable benchmark?）

是，但须明确注意事项。

### ALFWorld 的吸引力

- 当前仓库中已可用，
- 纯文本、成本可承受，
- 支持受控记忆注入，
- 成败易于观察。

### ALFWorld 的风险

仓库内试点已表明部分失败由以下主导：

- 格式不匹配（formatting mismatch），
- 交互协议问题（interaction protocol issues），
- 重复无效命令行为（repetitive invalid command behavior）。

故 ALFWorld 很容易测到接口脆弱性（interface brittleness）而非可复用经验。

### 设计结论

ALFWorld 仅应作为 **受控子集基准（controlled subset benchmark）**：

- 选择可复用教训可解释的任务族，
- 排除纯格式崩溃主导的案例，
- 使基准服务于问题而非反过来定义问题。

这与课程课题风格一致：不必评估一切，较小受控子集若更贴合问题即可。

---

## 7. 预期贡献（expected contribution）

若执行得当，项目可在以下层面贡献：

> 具体经验（concrete experience）被抽象为可复用教训（reusable lesson）时，其效用（utility）如何变化的受控实证分析。

更具体可澄清：

- 教训级抽象是否较情节级记忆改善复用，
- 哪些信息不应被抽象掉，
- 抽象何时开始过度泛化（over-generalize）。

比一般智能体记忆理论窄，但对课题 6 足够强，因具备：

- 理论根基，
- 可实证检验，
- 范围清晰，
- 已有文献尚未完全回答。

---

## 8. 本提案不是什么（what this proposal is not）

为避免重蹈早期表述的问题，修订提案应明确 **不是**：

- 关于智能体是否内心「理解」自身失败的项目，
- 伪装成记忆论文的检索论文（retrieval-paper disguised as a memory paper），
- 关于分阶段上下文释放的提示工程研究，
- 完整技能归纳或终身学习系统，
- 主张情节到语义抽象普遍最优。

明确非目标（non-goals）时，项目反而更强。

---

## 9. 一句话判断（one-sentence judgment）

> 修订提案较原提案可辩护得多，因用受控的记忆表征问题替代潜藏正确性主张；但其可行前提仍是 **紧扣 `episode -> lesson`（情节→教训）抽象步骤**，不扩张到检索（retrieval）、编排（orchestration）或完整程序性技能学习（procedural-skill learning）。
