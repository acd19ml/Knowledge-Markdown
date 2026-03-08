# Mobile-Agent-v3 / GUI-Owl — Self-Evolving Foundation Model for GUI Automation

## Meta
- **Title**: Mobile-Agent-v3: Fundamental Agents for GUI Automation
- **Authors**: Jiabo Ye, Xi Zhang, Haiyang Xu et al. | Alibaba Tongyi Lab
- **Venue**: Preprint, September 2025 | arXiv:2508.15144
- **Links**: [PDF](../source/Mobile-Agent-v3.pdf) | [Code](https://github.com/X-PLUG/MobileAgent)
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-05
- **Priority**: P1 | **Reading progress**: Pass 2

## One-line Summary
Mobile-Agent-v3 以 GUI-Owl 为核心模型，通过 Self-Evolving GUI Trajectory Production 流水线和 TRPO 在线强化学习，在 AndroidWorld 达到 73.3、在 OSWorld-Verified 达到 37.7，成为当时的开源 SOTA。

## Problem Setting
- **Core problem**: "The existing methods can be broadly divided into two categories. The first category builds agent frameworks based on closed-source models … however, these approaches struggle to handle unfamiliar tasks and adapt to dynamic environments. The second category focuses mainly on end-to-end model performance … but such methods often fail to follow instructions faithfully and lack compatibility with diverse agent frameworks, significantly limiting their practical utility." (Section 1, p.2)
- **Assumptions**: 多平台 GUI 环境（Android、Ubuntu、macOS、Windows）；依赖 Qwen2.5-VL 作为基座；通过 SFT 冷启动后进行 RL 微调。
- **Insufficiency of existing approaches**: "The second category focuses mainly on end-to-end model performance (Qin et al., 2025; Wang et al., 2025a), but such methods often fail to follow instructions faithfully and lack compatibility with diverse agent frameworks." (Section 1, p.2)

## Core Method

GUI-Owl 以 Qwen2.5-VL 为基座，经三阶段训练：(1) **Pre-training Phase**：在大规模 UI 理解与交互轨迹数据上持续预训练，建立 GUI 元素识别与动作预测基础；(2) **Iterative Tuning Phase**：在真实桌面与手机环境中大规模部署，生成轨迹后清洗评分，转换为多样化推理数据集再离线训练；(3) **Reinforcement Learning Phase**：使用异步 RL 框架直接从真实环境交互中学习，强化成功行为并提升执行一致性。

核心训练数据由 **Self-Evolving GUI Trajectory Production** 流水线提供：GUI-Owl 在云虚拟环境中 roll-out 生成轨迹，经 Trajectory Correctness Judgment Module（Step-Level Critic + Trajectory-Level Critic 双通道共识机制）过滤，并为困难查询额外生成 Query-specific Guidance。这一流水线创造了自强化改进循环，持续减少人工标注需求。

在线强化学习阶段引入 **TRPO（Trajectory-aware Relative Policy Optimization）**：将整条轨迹的稀疏奖励 R(τ) 归一化为轨迹级优势估计 Aˆτ，再均匀分配给轨迹中所有步骤，缓解长 horizon GUI 任务的信用分配问题。同时维护成功轨迹 replay buffer，防止全为失败样本时训练信号消失。**Mobile-Agent-v3** 多智能体框架则在 GUI-Owl 基础上协调 Manager / Worker / Reflector / Notetaker 四类角色，并集成 RAG 模块提供外部知识。

**Key Design Choices**:
| Design Decision | Author's Choice | Author's Rationale | Ablation Verified? |
|----------------|----------------|--------------------|---------------------|
| 轨迹奖励分配 | TRPO: 轨迹级奖励均匀分配至所有步骤 | 绕开逐步奖励标注的不可行性；缓解稀疏奖励下的信用分配问题 | Yes（Figure 8：TRPO vs DAPO vs GRPO 对比） |
| 成功轨迹回放 | Replay buffer 注入历史成功轨迹 | 稀疏正样本条件下维持有效训练信号，避免全失败批次 | Yes（Online Filtering (DAPO) ablation，峰值仅 31.5%） |
| 数据来源 | Self-Evolving Pipeline（模型 roll-out + 自动评判） | 替代人工标注，实现可扩展数据生成 | 定性（Section 6） |
| 推理数据合成 | 离线 Hint-Guided Rejection Sampling + 多智能体蒸馏 + 在线迭代采样 | 提升推理模式多样性，避免单一风格偏差 | Yes（Figure 10） |
| 历史截图数量 | 默认保留最近 1-3 张图像，RL 阶段分析多张效果 | 节省 GPU 内存；更多历史图有助于理解 UI 变化对比 | Yes（Figure 9） |

- **Core difference from prior work**: GUI-Owl 将 Self-Evolving 数据飞轮与 TRPO 在线环境 RL 结合为统一框架，既能独立作端到端智能体，又能作为专门化模块嵌入多智能体系统（Mobile-Agent-v3），兼顾 scalability 与 versatility。相比 UI-TARS 等工作，显式引入轨迹级 RL 并解决了信用分配问题。

## Key Results
| Benchmark | This Method | Strongest Baseline | Δ | Notes |
|-----------|------------|-------------------|---|-------|
| AndroidWorld | Mobile-Agent-v3: 73.3 | UI-TARS-1.5: 64.2 | +9.1 | GUI-Owl-7B standalone: 66.4 |
| OSWorld-Verified | Mobile-Agent-v3: 37.7 | OpenCUA-32B: 34.8 | +2.9 | GUI-Owl-7B (RL-tuned): 34.9 |
| OSWorld-Verified (RL only) | GUI-Owl-7B TRPO: 34.9 | DAPO variant: ~31.5 | +3.4 | Starting from 27.1 checkpoint |
| ScreenSpot-Pro | GUI-Owl-7B: 54.9 | UI-TARS-72B: 38.1 (open-src) | +16.8 | 7B 超过 72B 模型 |
| MMBench-GUI-L2 (Overall) | GUI-Owl-7B: 80.49 | UI-TARS-72B-DPO: 74.25 | +6.24 | GUI-Owl-32B: 82.97 |
| Android Control | GUI-Owl-32B: 76.6 | UI-TARS-72B: 74.7 | +1.9 | 超过所有包括专有模型 |
| Mobile-Agent-E on AndroidWorld | GUI-Owl-32B: 62.1 | Seed-1.5-VL: 56.0 | +6.1 | 嵌入第三方框架测试 |
| Agent-S2 on OSWorld subset | GUI-Owl-32B: 48.4 | Seed-1.5-VL: 39.7 | +8.7 | 嵌入第三方框架测试 |

- **Key ablation findings**:
  - TRPO (Online Filtering + Experience Managing) > DAPO (Online Filtering only) > GRPO (Offline Filtering)：replay buffer 对稳定训练至关重要（Figure 8）
  - 历史图像数量增加 → 性能稳定提升；更长交互步数预算 → 性能提升（Figure 9）
  - 离线 Hint-Guided RS + 多智能体蒸馏 + general reasoning data 逐步累积改进 AndroidWorld 性能（Figure 10）
  - 在线迭代采样随模型能力提升而带来持续收益（Figure 10）
- **Failure cases**: 论文未明确列举失败案例；仅提及稀疏成功轨迹条件下训练不稳定（无 replay buffer 时峰值后下降）；推理历史过长超出模型上下文限制（32k for Qwen2.5-VL）

## Limitations
- **Author-stated limitations**: 论文未设置独立 Limitations 章节。结论仅提及 GUI-Owl 在 OSWorld-Verified 最大步数限制为 15 步（Section 5.2），以及 RL 实验仅在 OSWorld-Verified 验证。
- **My observed limitations**:
  Mobile-Agent-v3 的核心增益来自训练期自演化，而不是部署期记忆。Self-Evolving 流水线依赖 GUI-Owl 先滚出足够好的轨迹，因此存在明显冷启动约束；Notetaker Agent 只是在单任务内累积 notes，属于 working-memory / summary-memory，而不是 `post-task -> cross-task` 的持久 procedural memory；TRPO 仍依赖 OSWorld-Verified 这类可程序验证奖励，说明它更像“训练期经验利用”，而不是开放场景下的 runtime write-back。
- **Experimental design gaps**: Mobile-Agent-v3 框架未做模块消融（对比单纯 GUI-Owl 与加入 Manager/Reflector/Notetaker 各模块的贡献）；仅在 AndroidWorld + OSWorld-Verified 两个基准上做在线评估，未涵盖 Web 场景。

## ⭐ Relation to My Research

### Position in Survey
- **Corresponding survey section/category**:
  这篇应放在 GUI Agent survey 的 **Training / Self-Evolution** 主段，并在 **Memory & Knowledge** 中作为对照案例引用。按当前 `main-line`，它不是 A-1 / A-4 的解，而是证明“经验闭环可以在训练阶段成立”的强正例；Notetaker 只占到 A-2 的 session-level 边缘位置，不能当作跨任务 memory solution。
- **Role**: Positive example（自演化数据生成 + RL 对齐的完整工程案例）/ Contrastive baseline（其 Notetaker 记忆方案与 A-1/A-2 理想方案对比）

### Gap Signals (extracted from this paper)

- Gap signal 1: "a task planning pipeline that distills procedural knowledge from historical successful trajectories and large-scale pretrained LLMs to handle long-horizon, multi-application tasks" (Section 2.2.2, p.6) → 规划数据是离线蒸馏静态生成，**无跨任务的在线持久化技能库**，说明 A-1（Procedural Memory）缺口在此未被填补。

- Gap signal 2: "The Notetaker Agent … Triggered only on SUCCESS, it extracts and stores critical screen elements (e.g., codes, credentials) as notes N_t. The cumulative memory N_{t+1} supports both planning and execution in future steps." (Section 4, p.10) → Notetaker 仅在**当前任务内**累积笔记，任务结束后无持久化，不构成跨任务的片段性记忆（A-2），更无法在新任务中检索历史执行经验。

- Gap signal 3: "GUI automation tasks operate in online interactive environments, which renders manual annotation of trajectory data exceedingly tedious and costly, posing significant challenges for GUI trajectory data collection." (Section 6, p.17) → 数据稀缺性直接驱动自演化设计，同时暗示**离线失败轨迹未被充分利用**（失败轨迹只用于 RL 的负样本，不提炼为可重用经验），对应 A-4。

  本文最大的研究价值信号是：GUI agent 的经验闭环并非不可做，但当前实现被锁在训练阶段。也就是说，它能支撑 A-4 的问题动机，却不能充当 A-4 的现成解法；真正缺的仍是部署后把新失败 / 新成功写回成可复用 procedural rule 的机制，并让这些规则在后续任务中被稳定检索和修订。

### Reusable Elements
- **Methodology**: Trajectory Correctness Judgment Module（Step-Level Critic + Trajectory-Level Critic）可用于评估记忆片段的质量；TRPO 的轨迹级奖励归一化思路可用于设计记忆检索的奖励信号。
  最值得复用的不是整套 RL scaffold，而是两步：先用双通道 judgment 筛掉不可靠轨迹，再把成功经验蒸馏成 query-specific guidance。若沿 `main-line` 继续收缩，这一步应进一步抽象成带触发条件、局部策略和失败信号的 procedural rule，而不是保留为 session guidance。
- **Experimental design**: AndroidWorld + OSWorld-Verified 是当前主流 online 评估基准，应在我的研究中使用相同基准做对比；历史图像数量消融（Figure 9）为视觉记忆实验提供参考设计。

### Connections to Other Papers in Knowledge Base
  它与 `Self_Evolve` 里的 AWM / ExpeL / SkillRL / EvoCUA 形成清晰对照：这些工作在文本或训练框架里讨论经验演化，Mobile-Agent-v3 则给出 GUI 侧的训练期工程化版本。与 `Agent_Memory` 的关系也很直接，Notetaker 更接近 working / summary memory，而不是长期 episodic 或 procedural memory。与 [2025_PCAgent.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2025_PCAgent.md) 一起看时，两篇共同说明多智能体分工和任务内记忆已经能做，但跨任务 procedural reuse 仍然空缺。

## Citation Tracking
- [ ] Qin et al., 2025 (UI-TARS-1.5): 当前最强开源对比模型，需阅读了解其训练方法
- [ ] Wang et al., 2025a (OpenCUA): 另一 end-to-end 开源 GUI 模型，OSWorld 对比基准
- [ ] Agashe et al., 2025 (Agent-S2): 在 Agent-S2 框架中验证 GUI-Owl 适配性
- [ ] Xie et al., 2024 (OSWorld): 主要 online 评估基准，需了解任务分布
- [ ] Guo et al., 2025 (GRPO): TRPO 的基础算法，需了解 GRPO 与 TRPO 的区别

## Key Passages
> "a task planning pipeline that distills procedural knowledge from historical successful trajectories and large-scale pretrained LLMs to handle long-horizon, multi-application tasks" (Section 2.2.2, p.6)

> "The Notetaker Agent … Triggered only on SUCCESS, it extracts and stores critical screen elements (e.g., codes, credentials) as notes N_t. The cumulative memory N_{t+1} supports both planning and execution in future steps." (Section 4, p.10)

> "GUI automation tasks operate in online interactive environments, which renders manual annotation of trajectory data exceedingly tedious and costly, posing significant challenges for GUI trajectory data collection. To address these challenges, we develop a self-evolving GUI trajectory data production pipeline." (Section 6, p.17)

> "We employ a trajectory-aware relative policy optimization strategy (TRPO) … This approach circumvents the challenge of assigning per-step rewards, a task that is nearly impossible to perform accurately in complex GUI interactions. Instead, we evaluate the entire trajectory τ after its completion." (Section 3.1.2, p.9)

> "performance increases steadily as more historical images are provided. This is because the model's understanding of UI changes relies on contrasts between consecutive frames, and additional images also help the model promptly reflect on and correct persistent erroneous behaviors." (Section 5.2.1, p.15)
