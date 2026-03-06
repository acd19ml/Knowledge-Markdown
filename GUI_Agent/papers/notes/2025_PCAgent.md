# PC-Agent — Hierarchical Multi-Agent Framework for Complex PC Task Automation

## Meta

- **Title**: PC-Agent: A Hierarchical Multi-Agent Collaboration Framework for Complex Task Automation on PC
- **Authors**: Haowei Liu, Xi Zhang, Haiyang Xu et al. | CASIA (Chinese Academy of Sciences) / Alibaba Group
- **Venue**: Preprint, February 2025 | arXiv:2502.14282
- **Links**: [PDF](./PC-Agent.pdf) | [Code](https://github.com/X-PLUG/MobileAgent/tree/main/PC-Agent)
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-05
- **Priority**: P1 | **Reading progress**: Pass 2

## One-line Summary

CASIA 与阿里巴巴联合提出 PC-Agent，通过 Active Perception Module（OCR + A11y tree + 意图理解）与四层次多智能体架构（Manager→Progress→Decision+Reflection），在自建 PC-Eval 基准上以 56% 成功率超越前 SOTA（Agent-S 24%），绝对提升 32%。

## Problem Setting

- **Core problem**: "Compared to smartphones, the PC scenario not only features a more complex interactive environment, but also involves more intricate intra- and inter-app workflows." (Abstract, p.1) 具体表现为：(1) 更复杂的交互环境——PC GUI 包含密集多样的图标与控件，以及多变的文本排版，即使 Claude-3.5 在 GUI grounding 数据集上准确率仅 24.0%；(2) 更复杂的任务序列——PC 生产力场景涉及跨应用、长步骤（示例任务 28 步）的工作流，并存在子任务间依赖关系。
- **Assumptions**: 以 GPT-4o 为基础模型；PC Windows 环境（pyautogui + pywinauto API）；评估限定于生产力场景（Chrome、Word、Excel、Notepad、Clock、Calculator、Outlook、File Explorer）。
- **Insufficiency of existing approaches**: "However, these methods lack fine-grained perception and operation ability of on-screen text, which is crucial in productivity scenarios (e.g., Word document editing). Moreover, they generally overlook the complex dependencies between subtasks, thereby exhibiting limited abilities on realistic intra- and inter-app complex tasks." (Section 1, p.2) — 指 UFO、Agent-S 等已有方法。

## Core Method

PC-Agent 由三个核心设计组成。第一，**Active Perception Module (APM)**：针对 PC GUI 的两类元素分别处理——对于交互元素，调用 pywinautoo API 提取 A11y tree 获取边框坐标与功能描述，并以 SoM（Set-of-Mark）方式在截图上标注；对于文本内容，先由 MLLM 驱动的意图理解 Agent 确定目标文本的起止范围，再调用 OCR 工具精确定位，从而支持"划线下划线最后一段"等精细文本编辑操作。

第二，**三层次层级多智能体协作架构**：(1) Instruction 层——Manager Agent (MA) 将用户指令分解为参数化子任务列表，维护通信 hub 管理子任务间依赖与参数传递；(2) Subtask 层——Progress Agent (PA) 追踪并总结当前子任务进度，将 DA 的动作与 RA 的反馈整合为更新后的进度状态，独立于 instruction 级历史，避免长上下文干扰；(3) Action 层——Decision Agent (DA) 结合 APM 感知信息与 PA 进度状态逐步决策，以 Chain-of-Thought 方式先生成内心独白再输出动作。

第三，**Reflection-based Dynamic Decision-making**：与 DA 并行设置 Reflection Agent (RA)，观察 DA 执行动作前后的屏幕变化，判断为三种情形：截图变化不符预期（需重规划）、无有效响应（需调整操作位置）、执行正确（继续下一步）。RA 的反馈同时传递给 DA（即时纠正）和 PA（准确进度追踪），形成自底向上的错误反馈链路。

**Key Design Choices**:


| Design Decision   | Author's Choice                    | Author's Rationale                                 | Ablation Verified?                        |
| ----------------- | ---------------------------------- | -------------------------------------------------- | ----------------------------------------- |
| 文本感知方式            | 意图理解 Agent + OCR 工具（APM）           | A11y tree 无法获取文档内文本；单纯截图感知精度不足以支持精细文本操作            | Yes（Table 3：去除 APM 后 SSR -20%，SR -30%+）   |
| 任务分解粒度            | 三层（Instruction→Subtask→Action）     | 单一 Agent 对长步骤任务成功率从 41.8% 跌至 8%；层次分解降低每层决策复杂度      | Yes（Table 3：去除 MA 后 SR 降至 12%）            |
| 独立 Progress Agent | PA 独立于 MA 和 DA                     | 避免将整条 instruction 级历史传给 DA，减少长上下文干扰；实现更精确的子任务级进度追踪 | 定性分析（Section 2.3.2）                       |
| 反射 Agent          | RA 并行于 DA，逐步反馈                     | 即使 GPT-4o 在长操作序列中也会出错；单步错误会导致整条 instruction 失败     | Yes（Table 3：去除 RA 后 SSR -27.9%，SR -44.0%） |
| 子任务间通信            | MA 维护 Communication Hub，存储已执行子任务输出 | 子任务间存在复杂依赖（4 种类型），需要参数传递；Agent-S 直接写入字面量而非实际值      | Yes（Case Study Figure 4）                  |


- **Core difference from prior work**: UFO 仅做双 Agent 的应用切换，无细粒度文本感知；Agent-S 依赖在线搜索+本地记忆做经验增强规划，但缺乏子任务间参数依赖管理和精细文本操作能力。PC-Agent 首次将 APM（OCR + A11y tree 融合）与三层次反射架构结合，专门针对 PC 生产力场景的复杂跨应用工作流。

## Key Results


| Benchmark                     | This Method    | Strongest Baseline | Δ      | Notes                  |
| ----------------------------- | -------------- | ------------------ | ------ | ---------------------- |
| PC-Eval SR (Success Rate)     | 56.0%          | Agent-S: 24.0%     | +32.0% | 25 条真实复杂指令             |
| PC-Eval SSR (Subtask SR)      | 76.0%          | Agent-S: 55.7%     | +20.3% | 79 个子任务                |
| vs UFO on SR                  | 56.0% vs 12.0% | —                  | +44.0% | UFO 仅略优于单 Agent GPT-4o |
| GPT-4o single agent (PC-Eval) | 8.0% SR        | —                  | —      | 单 Agent 基线             |
| Qwen2.5-VL single agent       | 12.0% SR       | —                  | —      | 最强单 Agent 基线           |


**Ablation results (Table 3)**:


| 组合                    | SSR   | SR    |
| --------------------- | ----- | ----- |
| APM + MA + RA (full)  | 76.0% | 56.0% |
| APM + MA only         | 58.2% | 20.0% |
| APM + RA only (no MA) | 50.6% | 12.0% |
| MA + RA only (no APM) | 48.1% | 12.0% |


**Foundation model ablation (Table 4, with GPT-4o as best)**:

- GPT-4o: SSR 76.0%, SR 56.0%, Recovery Rate 64.0%, Manager SR 96.0%
- Claude-3.5: SSR 63.3%, SR 40.0%, Recovery Rate 48.0%
- Gemini-2.0: SSR 55.7%, SR 28.0%
- Qwen2.5-VL: SSR 32.9%, SR 12.0%（格式遵循能力不足导致回退）
- **Key ablation findings**:
  - RA 的贡献最大（去除后 SR 绝对下降 44%），说明反射对长步骤任务至关重要
  - MA 次之（去除后 SR 绝对下降 44%），子任务间参数传递依赖是 PC 场景独特挑战
  - APM 缺失导致精细文本操作（如 Word 文档编辑）完全失效
  - 基础模型能力是框架有效性的前提：Qwen2.5-VL 由于格式遵循能力弱，引入层次分解反而降低性能
- **Failure cases**: Gemini-2.0 和 Claude-3.5 在 Recovery Rate 上显著低于 GPT-4o（24% vs 64%），说明感知能力弱时反射机制也难以奏效；Qwen2.5-VL 无法遵循 MA 分解后的子任务格式。

## Limitations

- **Author-stated limitations**: "Currently, the best performing model remains the closed-source GPT-4o. However, there is still significant room for improving the efficiency of completing complex tasks by invoking closed-source models. And the privacy and security issues associated with closed-source models also deserve attention. Additionally, our focus in this work has primarily been on productivity scenarios. In future work, we will explore expanding into more scenarios such as social interaction and entertainment." (Limitations, p.8)
- **My observed limitations**:
  > ⚠️ NEEDS YOUR INPUT: (1) PA（Progress Agent）追踪子任务进度，本质上是**单次任务内的工作记忆**，任务结束后不保留；没有跨任务的历史经验存储，不具备 A-1（Procedural Memory）或 A-2（Episodic Memory）能力。(2) Agent-S 已尝试用本地记忆做"经验增强规划"，但本文反而放弃了这一路线，专注于感知和架构设计——这说明作者认为当前阶段感知和分解是瓶颈，记忆机制尚未成熟。(3) PC-Eval 仅有 25 条指令，规模小，且依赖人工评估，难以大规模自动化；未在 OSWorld 等通用基准上验证。(4) 完全依赖 GPT-4o 作为所有 Agent 的基础模型，部署成本高且有隐私风险。
- **Experimental design gaps**: 仅在自建 PC-Eval 上评估，未在 OSWorld、WindowsAgentArena 等标准基准上对比；未做 APM 内部消融（OCR vs A11y tree 各自的贡献）；未分析任务类型对成功率的影响（如纯应用内操作 vs 跨应用工作流）。

## ⭐ Relation to My Research

### Position in Survey

- **Corresponding survey section/category**:
  > ⚠️ NEEDS YOUR INPUT: 属于 GUI Agent Survey 中 **Section 3（Task Automation Pipeline）→ 3.2 Decision Making（多智能体）** 与 **3.1 Perception（APM）** 的交叉。Progress Agent 对 Cross_Topic/gap-tracker.md 中的 A-1/A-2 缺口有直接参照意义——PA 是“有限 session 内记忆”的具体实现，但与跨任务持久化记忆有本质差距，可作为 Gap Analysis 的“现有局部方案”引用。
- **Role**: Background reference（PC 场景多智能体基线）/ Contrastive baseline（与具备持久化记忆的未来方案对比）

### Gap Signals (extracted from this paper)

- Gap signal 1: "Agent-S … combines online search and local memory for experience-augmented planning." (Section 1, p.2; Related Work, p.8) → 作者指出 Agent-S 已尝试本地记忆，但效果有限（SR 仅 24%），暗示**当前记忆机制不足以支撑复杂 PC 任务**，需要更系统的记忆设计（A-1）。
- Gap signal 2: "the existence of inter-subtask dependencies requires the agent to consider the execution results of preceding subtasks when making decisions, further increasing the decision-making difficulty." (Section 1, p.1) → 子任务间依赖要求智能体在**跨步骤、跨应用**间传递上下文信息，当前 Communication Hub 是 session 内的手动传递，若能用持久化的过程性记忆自动管理此类依赖，将大幅降低人工设计成本（A-1 的应用场景）。
- Gap signal 3: "removing RA leads to a very significant performance decrease (i.e., 27.9% in SSR and 44.0% in SR). This is because during the execution of complex instructions, errors in perception and decision-making are inevitable." (Section 3.3, p.7) → 反射 Agent 可弥补感知与决策错误，但这是**即时纠错**而非**从过去错误中学习**；若 RA 的失败反馈能累积为跨任务的失败经验库，则对应 A-4（Offline Experience Evolution from failed trajectories）。

> ⚠️ NEEDS YOUR INPUT: PC-Agent 对研究的核心价值在于：它精确地描述了"PC 生产力场景下，记忆缺失导致的两类问题"——(1) 缺乏过程性知识（每次任务都要从零规划 Word 操作步骤），(2) 缺乏跨任务的失败经验积累（每次遇到同类错误都要 RA 即时重试而非从历史中预判）。这两点与 A-1 和 A-4 研究缺口高度对应，是很好的动机引用来源。

### Reusable Elements

- **Methodology**: APM 的"意图理解 Agent + OCR"双通道文本定位机制，可作为 GUI 记忆检索时的 observation 预处理模块（将截图中的文本准确抽取为记忆索引键）；Progress Agent 的进度追踪设计可扩展为"记忆检索触发器"——当当前进度与历史经验匹配时自动提取相关记忆。
  > ⚠️ NEEDS YOUR INPUT: (1) APM 的文本精准定位能力对构建 A-2（视觉片段性记忆）中的"记忆锚点"很有价值——历史截图中的关键文本可被 APM 风格的 OCR 抽取为结构化索引，支持跨任务检索。(2) Progress Agent 的"子任务级进度摘要"模式（对应 Agent_Memory 中的 Summary Memory）可扩展为持久化的"任务完成路径记录"，即 A-1 技能库条目的一种天然格式。
- **Experimental design**: PC-Eval 的 25 条跨应用指令设计值得参考——若研究 PC 场景记忆，可直接在此基准上扩展（加入"重复任务"测试集来测量记忆带来的提升）；Table 3 的消融设计（逐步去除各模块）是清晰的 ablation 模板。

### Connections to Other Papers in Knowledge Base

> ⚠️ NEEDS YOUR INPUT: (1) **与 Agent_Memory/ 的联系**：PA 对应 Agent_Memory/03_memory-types.md 中的 Working Memory（短期工作记忆）；Communication Hub 是 Semantic Memory 的 session 级简化版。本文 Limitations 提到 Agent-S 用 local memory 的尝试，可引用 Agent_Memory 中的相关分析来阐明"为何当前简单记忆不够用"。(2) **与 Cross_Topic/gap-tracker.md 的联系**：PC-Agent 是 A-1（Procedural Memory）缺口的直接动机来源——每次 Word 操作都从零规划，没有可复用的操作技能库。可在 gap-tracker.md 中将本文作为 A-1 的"佐证文献"补充。(3) **与同目录 Mobile-Agent-v3 的联系**：两者均来自阿里/CASIA，Mobile-Agent-v3 提供了更强的底层视觉基础模型（GUI-Owl），PC-Agent 提供了更精细的 PC 感知与分层决策架构。两篇可组合形成"感知+决策+记忆"完整 pipeline 的对比图。(4) **与 Self_Evolve/ 的联系**：PC-Agent 的 Reflection Agent 是单任务内的自我纠错，而 Self_Evolve 中的演化机制关注跨任务的持续学习，两者构成记忆研究的两个层次（within-task vs. across-task）。

## Citation Tracking

- Zhang et al., 2024 (UFO): PC 场景双 Agent 框架，直接对比基线，需阅读
- Agashe et al., 2024 (Agent-S): 使用 local memory 的经验增强规划，A-1 缺口的佐证
- Yang et al., 2023 (SoM): Set-of-Mark prompting，APM 的视觉标注方法来源
- Xie et al., 2024 (OSWorld): 标准 PC 基准，PC-Agent 未在此评估，是研究扩展方向
- Hurst et al., 2024 (GPT-4o): 本文唯一能驱动 PC-Agent 达到最优性能的基础模型

## Key Passages

> "Compared to smartphones, the PC scenario not only features a more complex interactive environment, but also involves more intricate intra- and inter-app workflows." (Abstract, p.1)

> "For instance, bold the last two paragraphs of this document. To address this, we propose utilizing active perception to obtain the content and position of the target text. … an MLLM-driven intention understanding agent to determine the start and end range of the target text, followed by using OCR tools to precisely locate the target text for subsequent detailed operations such as drag." (Section 2.2, p.3)

> "removing RA leads to a very significant performance decrease (i.e., 27.9% in SSR and 44.0% in SR). This is because during the execution of complex instructions, errors in perception and decision-making are inevitable. Removing RA causes the model to lack awareness and timely correction of errors, which predisposes it to getting stuck in meaningless repetition or incorrect steps." (Section 3.3, p.7)

> "Agent-S (Agashe et al., 2024) combines online search and local memory for experience-augmented planning. … However, these methods lack fine-grained perception and operation ability of on-screen text … Moreover, they generally overlook the complex dependencies between subtasks." (Section 1, p.2)

> "Currently, the best performing model remains the closed-source GPT-4o. However, there is still significant room for improving the efficiency of completing complex tasks by invoking closed-source models. And the privacy and security issues associated with closed-source models also deserve attention." (Limitations, p.8)
