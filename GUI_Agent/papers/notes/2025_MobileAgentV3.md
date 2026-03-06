# Mobile-Agent-v3 / GUI-Owl — Self-Evolving Foundation Model for GUI Automation

## Meta
- **Title**: Mobile-Agent-v3: Fundamental Agents for GUI Automation
- **Authors**: Jiabo Ye, Xi Zhang, Haiyang Xu et al. | Alibaba Tongyi Lab
- **Venue**: Preprint, September 2025 | arXiv:2508.15144
- **Links**: [PDF](./Mobile-Agent-v3.pdf) | [Code](https://github.com/X-PLUG/MobileAgent)
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-05
- **Priority**: P1 | **Reading progress**: Pass 2

## One-line Summary
Alibaba Tongyi Lab 提出 GUI-Owl（7B/32B 基础模型）与 Mobile-Agent-v3 框架，通过 Self-Evolving GUI Trajectory Production 流水线 + TRPO 在线强化学习，在 AndroidWorld 达到 73.3、OSWorld-Verified 达到 37.7，成为开源模型 SOTA。

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
> ⚠️ NEEDS YOUR INPUT: (1) Self-Evolving 流水线依赖 GUI-Owl 自身能力滚出轨迹，模型初期能力弱时难以生成高质量正样本，存在自举冷启动问题。(2) 虽然 Notetaker Agent 维护了跨步骤的工作记忆，但属于 within-task 的短期上下文记录，**没有跨任务的持久化过程性记忆**（技能库/操作手册），每次任务重新从零规划，对应 A-1 缺口。(3) TRPO 在线 RL 仍依赖 OSWorld-Verified 的可程序验证奖励信号，难以推广到任意开放场景。
- **Experimental design gaps**: Mobile-Agent-v3 框架未做模块消融（对比单纯 GUI-Owl 与加入 Manager/Reflector/Notetaker 各模块的贡献）；仅在 AndroidWorld + OSWorld-Verified 两个基准上做在线评估，未涵盖 Web 场景。

## ⭐ Relation to My Research

### Position in Survey
- **Corresponding survey section/category**:
> ⚠️ NEEDS YOUR INPUT: 属于 GUI Agent Survey 中 **Section 3（Task Automation Pipeline）→ 3.4 Memory & Knowledge** 与 **Section 5（Self-Evolving / Training）** 的交叉节点。GUI-Owl 的 Self-Evolving Trajectory Production 框架直接对应 Cross_Topic/gap-tracker.md 中 A-4（Offline Experience Evolution）的初步实例；Mobile-Agent-v3 的 Notetaker Agent 是 A-2（Episodic Memory）的轻量实现。
- **Role**: Positive example（自演化数据生成 + RL 对齐的完整工程案例）/ Contrastive baseline（其 Notetaker 记忆方案与 A-1/A-2 理想方案对比）

### Gap Signals (extracted from this paper)

- Gap signal 1: "a task planning pipeline that distills procedural knowledge from historical successful trajectories and large-scale pretrained LLMs to handle long-horizon, multi-application tasks" (Section 2.2.2, p.6) → 规划数据是离线蒸馏静态生成，**无跨任务的在线持久化技能库**，说明 A-1（Procedural Memory）缺口在此未被填补。

- Gap signal 2: "The Notetaker Agent … Triggered only on SUCCESS, it extracts and stores critical screen elements (e.g., codes, credentials) as notes N_t. The cumulative memory N_{t+1} supports both planning and execution in future steps." (Section 4, p.10) → Notetaker 仅在**当前任务内**累积笔记，任务结束后无持久化，不构成跨任务的片段性记忆（A-2），更无法在新任务中检索历史执行经验。

- Gap signal 3: "GUI automation tasks operate in online interactive environments, which renders manual annotation of trajectory data exceedingly tedious and costly, posing significant challenges for GUI trajectory data collection." (Section 6, p.17) → 数据稀缺性直接驱动自演化设计，同时暗示**离线失败轨迹未被充分利用**（失败轨迹只用于 RL 的负样本，不提炼为可重用经验），对应 A-4。

> ⚠️ NEEDS YOUR INPUT: 本文最大的研究价值信号在于：Self-Evolving 流水线证明了"模型可以从自身执行经验中持续学习"的可行性，但这种学习被限定在训练阶段（offline/online RL），**推理部署后的新任务经验无法反哺模型**。这正是 A-4（Offline Experience Evolution at inference time）和 A-1（runtime skill reuse）的研究切入点。

### Reusable Elements
- **Methodology**: Trajectory Correctness Judgment Module（Step-Level Critic + Trajectory-Level Critic）可用于评估记忆片段的质量；TRPO 的轨迹级奖励归一化思路可用于设计记忆检索的奖励信号。
> ⚠️ NEEDS YOUR INPUT: (1) Trajectory Correctness Judgment 的双通道评判机制可直接移植为"记忆条目质量评估"模块——在构建 GUI 过程性记忆库时，用类似机制筛选值得存储的成功轨迹。(2) Self-Evolving 流水线的 Query-specific Guidance Generation 模块（将成功轨迹蒸馏为步骤级指导）是构建 A-1 技能库的自然起点，可扩展为"跨任务可检索的操作手册"。
- **Experimental design**: AndroidWorld + OSWorld-Verified 是当前主流 online 评估基准，应在我的研究中使用相同基准做对比；历史图像数量消融（Figure 9）为视觉记忆实验提供参考设计。

### Connections to Other Papers in Knowledge Base
> ⚠️ NEEDS YOUR INPUT: (1) **与 Self_Evolve/ 的联系**：GUI-Owl 的 Iterative Online Rejection Sampling 与 Self_Evolve/04_self-evolution-mechanisms.md 中的“经验驱动演化”高度对应，但 GUI-Owl 仍局限于训练阶段演化，未达到 Self_Evolve 文献中部署后持续演化的目标。(2) **与 Agent_Memory/ 的联系**：Notetaker Agent 对应 Agent_Memory 中的 Working Memory / Episodic Memory 概念，但缺乏长期存储与跨任务检索能力。(3) **与 Cross_Topic/gap-tracker.md 的联系**：可作为 A-2（Episodic Memory 缺口）的“当前最好实践但仍不足”的典型案例写入。(4) **与同目录 PC-Agent 的联系**：PC-Agent 同为层级多智能体框架，但专注 PC 场景感知与任务分解，两者互补——GUI-Owl 提供更强的底层感知模型，PC-Agent 提供更精细的多层代理协作设计。

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
