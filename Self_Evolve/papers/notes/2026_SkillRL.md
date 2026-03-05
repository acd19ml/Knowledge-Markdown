# SkillRL — Recursive skill-augmented RL enabling agent self-evolution through distilled experience

## Meta
- **Title**: SKILLRL: Evolving Agents via Recursive Skill-Augmented Reinforcement Learning
- **Authors**: Peng Xia, Jianwen Chen, Hanyang Wang et al. | UNC-Chapel Hill, Univ. of Chicago, UCSD, NEC Labs America, UC Berkeley, UC Santa Cruz
- **Venue**: Preprint, February 10, 2026 | arXiv:2602.08234 (位置待确认，请自行核查)
- **Links**: [PDF](./skillRL.pdf) | [Code](https://github.com/aiming-lab/SkillRL)
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-05
- **Priority**: P1 | **Reading progress**: Pass 1

## One-line Summary

SKILLRL 提出将 LLM agent 的轨迹（成功 + 失败）自动蒸馏为分层 SKILLBANK，并在 RL 训练中递归演化 skill library，在 ALFWorld 上达到 89.9% 成功率（vs. GRPO 基线 77.6%，+12.3%），在 WebShop 上达到 72.7%（vs. SimpleMem+GRPO 46.9%，+25.8%），同时将 context token 用量减少约 10.3%。

## Problem Setting

- **Core problem**: "LLM agents operate in isolation, unable to learn from past successes or failures, which significantly hinders their evolution." (Section 1, p.1)
- **Assumptions**:
  - 任务有明确的二值成功信号（binary reward r(τ) ∈ {0,1}）。
  - 环境支持多轮 rollout（需要持续采样轨迹做蒸馏和演化）。
  - 有高能力的 teacher model（本文用 OpenAI o3）可做技能蒸馏。
- **Insufficiency of existing approaches**: "These raw trajectories are often lengthy and contain significant redundancy and noise, making it difficult for the model to extract critical information." (Section 1, p.1) 以及 "these methods merely mimic past solutions and they fail to distill core principles or adapt the agent's internal policy to leverage memory for guided decision-making." (Section 1, p.2)

## Core Method

**Method overview**:

SKILLRL 分三个阶段。第一阶段是**经验蒸馏**：用基础模型在目标环境中采集轨迹，同时保留成功轨迹（提取策略模式 s⁺）和失败轨迹（合成"反事实失败教训" s⁻），由 teacher model (o3) 完成蒸馏，将冗长轨迹压缩为紧凑的 skill 条目（实现 10–20× token 压缩）。

第二阶段是**分层 SKILLBANK 构建**：将蒸馏出的技能分为两层——General Skills（跨任务通用策略，如系统性探索、状态验证）和 Task-Specific Skills（特定任务类别的精细化策略）。推理时，通用技能始终加入上下文，特定技能通过语义相似度检索（Top-K，K=6），大幅降低 context 膨胀。

第三阶段是**Cold-Start SFT + 递归演化 RL**：RL 训练前先做 SFT，让基础模型学会"如何使用 skill"，再以 GRPO 优化 skill-augmented policy。每个 validation epoch 后，对失败任务类别（成功率 < δ=0.4）采集失败轨迹，由 teacher model 分析并生成新 skill 或更新现有 skill，实现 skill library 与 policy 的协同演化（"virtuous cycle"）。

**Key Design Choices**:

| Design Decision | Author's Choice | Author's Rationale | Ablation Verified? |
|----------------|----------------|--------------------|--------------------|
| Skill 分层结构（General + Task-Specific） | 两层分层 | 通用技能提供跨任务基础；任务特定技能提供细粒度指导 | Yes — w/o hierarchical structure: -13.1% ALFWorld |
| 失败轨迹处理 | 蒸馏为反事实教训（而非直接存储） | 直接存储导致 noise 过重；蒸馏后提取核心错误原因 | Yes — w/o Skill Library (raw traj): -25% ALFWorld |
| Cold-Start SFT | RL 前先 SFT 学 skill 使用方式 | 直接给 base model skill 效果有限；需要显式演示 | Yes — w/o Cold-Start SFT: -24.7% ALFWorld |
| 递归 skill 演化 | 每 validation epoch 对失败类别生成/更新 skill | 静态 library 无法覆盖 policy 探索到的新场景 | Yes — w/o Dynamic Evolution: -5.5% ALFWorld |
| Teacher Model | OpenAI o3 | 需要高能力模型做蒸馏和 SFT 数据生成 | **No** — 未对比更弱的 teacher model |
| 检索参数（K=6, δ=0.4） | K=6 task-specific skills; δ=0.4 演化触发阈值 | 经验调参 | **No** — 无超参数敏感性分析 |
| Base optimizer | GRPO | 主流 group-based RL，无需 critic | No（GRPO 作为基线对比，非架构选择消融） |

- **Core difference from prior work**: 与 EvolveR、MemRL 等 memory-augmented RL 的核心区别在于"抽象层级"——现有方法存储原始轨迹或压缩轨迹，但 SKILLRL 提取的是可泛化的**行为原则**（skills），并且将 skill library 视为与 policy 协同演化的**动态组件**，而非静态知识库。

## Key Results

| Benchmark | This Method | Strongest Baseline | Δ | Notes |
|-----------|------------|-------------------|---|-------|
| ALFWorld (Overall) | 89.9% | GRPO: 77.6% | +12.3% | 同一 base optimizer，差距纯来自 skill augmentation |
| ALFWorld Pick2 | 87.5% | GRPO: 64.7% | +22.8% | 最难子任务之一 |
| ALFWorld Cool | 95.5% | GRPO: 72.5% | +23.0% | 最难子任务之一 |
| WebShop (Succ.) | 72.7% | SimpleMem+GRPO: 46.9% | +25.8% | 最强 memory-aug RL 基线 |
| WebShop (Score) | 85.2% | SimpleMem+GRPO: 67.8% | +17.4% | |
| Search QA (Avg.) | 47.1% | EvolveR: 43.1% | +4.0% | 训练仅用 NQ + HotpotQA |
| Bamboogle (OOD) | 73.8% | EvolveR: 54.4% | +19.4% | 强 OOD 泛化 |
| vs GPT-4o (ALFWorld) | 89.9% | GPT-4o: 48.0% | +41.9% | 7B 开源 vs 闭源大模型 |
| vs Gemini-2.5-Pro (ALF) | 89.9% | Gemini-2.5-Pro: 60.3% | +29.6% | |

- **Key ablation findings**:
  - **贡献最大的组件**：Cold-Start SFT（-24.7%）和 Skill Library vs Raw Trajectories（-25%）几乎同等重要——说明"技能抽象质量"和"模型使用技能的能力初始化"缺一不可。
  - **贡献较小的组件**：递归演化（仅 +5.5%）——这意味着初始 skill library 质量决定了大部分性能；演化机制是锦上添花而非核心。
  - **未消融的组件**：teacher model（o3）的能力对蒸馏质量的影响；K 值和 δ 阈值的敏感性；skill 数量上限。

- **Failure cases**: 论文未专门展示失败案例。Figure 6 只展示成功案例的推理过程。失败模式仅通过 ablation 间接体现（如无 cold-start 时多步任务中 skill 被忽略）。

## Limitations

- **Author-stated limitations**: 论文**无专门的 Limitations 章节**，Conclusion 也未提及局限。唯一接近的表述是："applying [RL] to agentic skills remains challenging due to sparse rewards and long horizons" (Section 5, p.8)，但这是对领域问题的描述，而非对本文方法的限制说明。

- **My observed limitations**:
> ⚠️ NEEDS YOUR INPUT: 初步观察如下，请结合你的 RQ 验证：
> 1. **Teacher model 依赖**：蒸馏和 SFT 数据生成全部依赖 OpenAI o3（前沿闭源模型），计算成本高昂且不可在 air-gapped 环境运行。论文完全未消融 teacher 能力对结果的影响——这是一个潜在的可再现性问题。
> 2. **环境范围局限**：仅在 ALFWorld（文本环境）、WebShop（结构化 web）和静态 QA 任务上测试，均有预定义动作空间。未测试开放域 GUI 任务（如真实浏览器或移动 UI），技能蒸馏在视觉观察下是否仍有效存疑。
> 3. **二值奖励假设**：框架依赖 r(τ) ∈ {0,1} 的二值任务成功信号；对奖励稀疏或需要中间反馈的任务（如长步骤导航）适用性未验证。
> 4. **演化效益边际递减**：Dynamic Evolution 仅贡献 +5.5%（ALFWorld）和 +2.4%（WebShop），而初始 skill library 贡献了 ~25%。这说明"如何获得高质量初始技能"比"如何演化"更关键——文章的核心叙事（recursive evolution）与数据并不完全吻合。

- **Experimental design gaps**:
  - 所有 ALFWorld 基线结果中，部分（标 ∗）为从 Feng et al., 2025 复现，而非在相同环境下统一实验，存在实验设置不一致的风险。
  - Search-augmented QA 实验中，SKILLRL 仅在 NQ + HotpotQA 上训练，其他 5 个数据集均为 OOD——与 EvolveR 的训练集是否完全一致？文中未明确说明。
  - 未报告 RL 训练的计算成本（GPU-hours），难以评估实际 sample efficiency。

## ⭐ Relation to My Research

### Position in Survey

- **Corresponding survey section/category**:
> ⚠️ NEEDS YOUR INPUT: 初步建议——该论文同时涉及：
> 1. **Self-Evolving Agents**（主要归属）：属于 "Experience-driven Skill Discovery + RL co-evolution" 模式，与 Self_Evolve 综述中"经验驱动自演化"分类高度对应。
> 2. **Procedural Memory**（Agent_Memory 视角）：SKILLBANK 本质上是一个 procedural memory 系统——存储的是"如何做"而非"做了什么"。这是 Cross_Topic/ 中 A-1 Gap（Procedural Memory 与 Self-Evolution 结合）的一个具体实例。
> 请确认：这篇文章在你的 Self_Evolve 综述中应放在哪个子节？是否也需要在 Agent_Memory 综述中交叉引用？

- **Role**: Positive example（展示 procedural memory 驱动 RL 演化的可行路径）+ Contrastive baseline（与纯 memory-based 方法的对比基准）

### Gap Signals (extracted from this paper)

- Gap signal 1: "applying RL to agentic skills remains challenging due to sparse rewards and long horizons" (Section 5, p.8) → 隐含：SKILLRL 在 dense reward 环境（ALFWorld 有明确动作空间）生效，但在真实 GUI 任务（奖励更稀疏、动作空间更大）下能否有效蒸馏 skill 未被验证。
- Gap signal 2: Ablation Table 3 shows Dynamic Evolution contributes only +5.5% on ALFWorld — 隐含：递归演化的收益依赖于初始 SKILLBANK 质量，而初始质量取决于 teacher model 能力（o3）。若 teacher 更弱，skill 质量下降，演化可能无法弥补——**skill 初始化质量 vs 演化能力的权衡**是未解问题。
- Gap signal 3: Paper has no Limitations section, and teacher model (o3) is never ablated → 隐含：**teacher-free 或 self-distillation 路径**（agent 自己蒸馏技能）是明确未探索的方向；"we leave X to future work" 形式的表述完全缺失，但这个 gap 从实验设计可推断。

> ⚠️ NEEDS YOUR INPUT: 评估以上 Gap 信号的价值：
> - Gap 1（视觉/GUI 场景）对你的 GUI Agent 方向是否直接相关？证据等级 B（实验覆盖局限，但推断合理）。
> - Gap 2（初始化 vs 演化权衡）对 Self_Evolve 综述是否构成论点？证据等级 A（有 ablation 数据支撑）。
> - Gap 3（teacher-free skill 蒸馏）是否与你当前的 A-1 Gap 研究方向重叠？

### Reusable Elements

- **Methodology**:
  - **失败轨迹蒸馏为反事实教训**的方法（Eq. 3, Section 3.1）——将失败分析结构化为 (failure point, flawed reasoning, what should have been done, general principle) 四元组，这个格式可直接迁移到 GUI Agent 场景的 error recovery 技能构建。
  - **两层 Skill 组织结构**（General + Task-Specific）——可以参考用于设计 GUI Agent 的 skill library：通用技能（如屏幕分区策略、状态验证）+ 应用特定技能（如购物流程、表单填写）。
> ⚠️ NEEDS YOUR INPUT: 如何在你的方法中迁移？具体来说——失败轨迹四元组格式是否适合 GUI Agent 的 action trace 分析？两层结构是否能对应 GUI Agent 的 app-type 分类？

- **Experimental design**:
  - ALFWorld 的子任务分解（Pick/Look/Clean/Heat/Cool/Pick2）是评估 task-specific skill 泛化性的良好模板——可参考用于 GUI 任务的 difficulty stratification。
  - 用**技能库规模增长曲线**（Figure 3，skill count vs training steps）来可视化演化动态是一个可借用的分析视角。

### Connections to Other Papers in Knowledge Base

> ⚠️ NEEDS YOUR INPUT: 请基于你已有的 Self_Evolve/ 和 Cross_Topic/ 文件确认以下初步关联：
> - 与 **EvolveR**（文中作为 baseline）的关系：竞争 — EvolveR 也做经验驱动 RL，但用原始轨迹存储，SKILLRL 的 skill 抽象是核心改进。若知识库中有 EvolveR 笔记，可作为直接对比。
> - 与 **MemRL / Mem0+GRPO**（文中 baselines）的关系：竞争 — 均为 memory-augmented RL，但不做 skill 抽象；SkillRL 的 cold-start SFT 是它们没有的关键设计。
> - 与 **Cross_Topic/gui-agent-x-self-evolving.md** 中的 A-1 Gap（Procedural Memory + Self-Evolution）：正面例证 — SKILLRL 是 procedural skill + RL co-evolution 的一个完整实现，可作为 A-1 Gap 研究的 prior work 参考。

## Citation Tracking

- [ ] ExpeL (Zhao et al., 2024): SKILLRL 引用为 prompt-based memory 基线，理解 experience-based learning 的前期工作
- [ ] EvolveR (Wu et al., 2025): 最接近的 memory-augmented RL 竞争方法，需精读理解差异
- [ ] MemRL (Zhang et al., 2026): 另一个 memory-aug RL 基线，policy frozen 只更新 memory bank
- [ ] SimpleMem (Liu et al., 2026): 高效 lifelong memory，+GRPO 后仍弱于 SKILLRL 27%
- [ ] Search-R1 (Jin et al., 2025): Search-augmented QA 的 RL 基线，了解 RL for retrieval-augmented reasoning
- [ ] Anthropic Agent Skills (2024): SKILLRL 直接引用 Claude 的 skill 概念作为设计灵感（Section 3.2, p.3）

## Key Passages

> "Effective experience transfer requires abstraction. Human experts do not memorize every action in every situation; instead, they develop skills, compact and reusable strategies that capture the essence of how to accomplish specific subtasks." (Section 1, p.2)

> "Simply providing skills to an unchanged model yields limited benefit. We therefore perform a cold-start supervised fine-tuning stage." (Section 3.3, p.4) — 说明 skill 的价值依赖于 model 具备使用 skill 的能力，而非 skill 本身。

> "Skill distillation achieves 10–20× token compression compared to raw trajectories while enhancing rather than degrading the utility of the original experience." (Section 3.2, p.4)
