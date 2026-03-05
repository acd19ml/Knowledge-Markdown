# GUI Agent — 知识库索引

**领域**：LLM-based GUI Agent（图形用户界面智能体）

---

## 目录结构

```
GUI_Agent/
├── README.md                           # 本文件
├── 00_survey-overview.md               # 综述概览：论文信息、分类框架、结构图
├── 01_background.md                    # 背景知识：LLM、MLLM、Agent 概念
├── 02_capabilities/                    # Section 3：GUI Agent 核心能力
│   ├── README.md                       # 能力层次总览 + 代表系统对比
│   ├── 2.1_gui-comprehension.md        # GUI 环境理解（Text/Vision/Hybrid）
│   ├── 2.2_device-control.md           # 设备控制（Code-based vs UI-based）
│   ├── 2.3_user-interaction.md         # 用户交互（单轮 vs 任务导向对话）
│   └── 2.4_advanced-capabilities.md    # 个性化服务 + 多智能体协同
├── 03_task-automation-pipeline.md      # Section 4：两阶段流程（探索→利用）
├── 04_evaluation.md                    # Section 5：数据集 + 评估指标
└── 05_challenges.md                    # Section 6：挑战与机遇
```

> 跨综述矩阵与全局 Gap 追踪位于 [../Cross_Topic/comparison-matrix.md](../Cross_Topic/comparison-matrix.md) 和 [../Cross_Topic/gap-tracker.md](../Cross_Topic/gap-tracker.md)。

---

## 核心综述

| 文件 | 内容摘要 |
|------|---------|
| [00_survey-overview.md](00_survey-overview.md) | GA Survey 全貌：分类框架、四大贡献、与知识库的关联 |
| [01_background.md](01_background.md) | LLM 架构类型、MLLM 设计原理、LLM-based Agent 三大能力 |
| [02_capabilities/](02_capabilities/) | GUI 理解三范式、两种设备控制、用户交互形式、个性化与多 Agent |
| [03_task-automation-pipeline.md](03_task-automation-pipeline.md) | 探索→利用两阶段流程，AppAgent/MobileGPT/AutoDroid/MMAC-Copilot |
| [04_evaluation.md](04_evaluation.md) | 24个数据集概览（Table 2）、Success Rate/SSR/Element Similarity 等指标 |
| [05_challenges.md](05_challenges.md) | 计算成本、幻觉/安全/可行性、AIOS 连接 |

---

## 与知识库其他主题的关联

| 本主题 | 关联主题 | 交叉点 |
|--------|---------|--------|
| GUI Agent 个性化服务 | [Agent_Memory/](../Agent_Memory/) | 用户中心记忆（User-Centric Memory）是实现个性化的技术基础 |
| 探索→利用两阶段流程 | [Self_Evolve/](../Self_Evolve/) | 探索阶段是自我进化的数据收集阶段；Reflection 机制共享 |
| 跨任务经验积累（Gap） | Agent_Memory + Self_Evolve | GUI Agent 目前几乎没有跨任务记忆——最大的研究机会 |
| 幻觉与自我反思 | [Self_Evolve/02_model-centric/](../Self_Evolve/02_model-centric/) | Self-Reflection 机制直接对应 GUI Agent 的幻觉治理 |
