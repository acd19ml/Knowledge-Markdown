# 自演化智能体 — 知识库

> 综述：《自演化智能体系统综述：从以模型为中心到环境驱动的协同进化》
> PDF：`A_Survey_of_Self_Evolving_Agents.pdf`（26 页）

---

## 核心论点

> "自演化智能体"代表了从静态模型训练到**通过自主交互持续改进**系统的范式转变 —— 自主生成训练信号、精炼策略，并在无需持续人工监督的情况下与环境共同进化。

当前 AI 的监督瓶颈：SFT 将模型限制于模仿；RL 依赖稀疏的、由人类定义的奖励。自演化通过**主动智能体行为**突破了这一瓶颈。

---

## 三范式分类体系

```
自演化智能体
├── III. 以模型为中心的自演化        [第 5–9 页]
│   ├── A. 基于推理（测试时扩展）
│   └── B. 基于训练（数据合成 + RL）
│
├── IV. 以环境为中心的自演化         [第 9–12 页]
│   ├── A. 静态知识演化（RAG、深度研究）
│   ├── B. 动态经验演化（离线/在线/终身）
│   ├── C. 模块化架构演化（记忆、工具、协议）
│   └── D. 智能体拓扑演化（MAS 设计）
│
└── V. 模型-环境协同进化             [第 10–11 页]
    ├── A. 多智能体策略协同进化
    └── B. 环境训练（课程 + 可扩展环境）
```

**核心张力**：以模型为中心若缺乏外部验证有模型崩溃风险；以环境为中心在静态环境中有停滞风险。协同进化是二者的综合。

---

## 目录结构

```
Self_Evolve/
├── README.md                  # 本文件 —— 导航中心
├── 00_survey-overview.md      # 论文元信息、关键数据、相关综述
├── 01_background.md           # 预备知识：智能体定义、MDP、问题框架
│
├── 02_model-centric/          # 第 III 节：以模型为中心的自演化
│   ├── README.md              # 章节概览 + 对比表
│   ├── 2.1_inference-based.md # 并行采样、自我修正、结构化推理
│   └── 2.2_training-based.md  # 合成驱动的离线演化、探索驱动的在线演化
│
├── 03_env-centric/            # 第 IV 节：以环境为中心的自演化
│   ├── README.md              # 章节概览
│   ├── 3.1_static-knowledge.md  # 智能体 RAG、深度研究
│   ├── 3.2_dynamic-experience.md # 离线/在线/终身经验演化
│   ├── 3.3_modular-arch.md    # 交互协议、记忆架构、工具增强
│   └── 3.4_agentic-topology.md  # 离线搜索、运行时适应、结构状态
│
├── 04_co-evolution.md         # 第 V 节：模型-环境协同进化
├── 05_applications.md         # 第 VI 节：科学发现、软件工程、开放世界
├── 06_challenges.md           # 第 VII 节：讨论、挑战、未来工作
└── 07_benchmarks.md           # 第 VIII+IX 节：评估基准 + 开源库
```

---

## 快速导航

| 主题 | 文件 |
|---|---|
| 论文概览与关键数据 | [00_survey-overview.md](00_survey-overview.md) |
| 智能体与 MDP 基础 | [01_background.md](01_background.md) |
| 推理时演化（测试时扩展） | [02_model-centric/2.1_inference-based.md](02_model-centric/2.1_inference-based.md) |
| 基于训练的演化（SFT/RL） | [02_model-centric/2.2_training-based.md](02_model-centric/2.2_training-based.md) |
| 静态知识演化（RAG/深度研究） | [03_env-centric/3.1_static-knowledge.md](03_env-centric/3.1_static-knowledge.md) |
| 动态经验演化 | [03_env-centric/3.2_dynamic-experience.md](03_env-centric/3.2_dynamic-experience.md) |
| 记忆与工具架构演化 | [03_env-centric/3.3_modular-arch.md](03_env-centric/3.3_modular-arch.md) |
| 多智能体拓扑演化 | [03_env-centric/3.4_agentic-topology.md](03_env-centric/3.4_agentic-topology.md) |
| 模型-环境协同进化 | [04_co-evolution.md](04_co-evolution.md) |
| 应用（科学、软件工程、游戏） | [05_applications.md](05_applications.md) |
| 挑战与未来前沿 | [06_challenges.md](06_challenges.md) |
| 评估基准 | [07_benchmarks.md](07_benchmarks.md) |

---

## 关键系统一览

| 系统 | 范式 | 领域 | 机制 |
|---|---|---|---|
| DeepSeek-R1 | 以模型为中心 / 训练 | 数学/推理 | GRPO + RL |
| Reflexion | 以模型为中心 / 推理 | 通用 | 言语自我反馈 |
| Self-RAG | 以环境为中心 / 静态 | 知识 | 选择性检索 + 批评 |
| VOYAGER | 以环境为中心 / 工具增强 | 游戏 | 可执行技能库 |
| GPTSwarm | 以环境为中心 / 拓扑 | MAS | 基于梯度的图优化 |
| SWE-agent | 协同进化 | 软件工程 | ACI + 错误反馈 |
| The AI Scientist | 协同进化 | 科学 | 自动同行评审循环 |
| Generative Agents | 协同进化 | 社会仿真 | 观察-反思-规划 |
| AlphaProof | 协同进化 | 数学 | Lean 验证器循环 |

---

## 研究延伸笔记

- [ ] RL 奖励塑造在三种范式中有何不同？
- [ ] 验证器扮演什么角色 —— 没有验证器会发生什么？
- [ ] 离线 vs 在线演化在计算、数据和安全方面的权衡？
- [ ] 自演化智能体与智能体记忆的关联（交叉参考 [Agent_Memory/](../Agent_Memory/)）？
- [ ] 探索模型崩溃：为什么自我训练有时会降低性能？
