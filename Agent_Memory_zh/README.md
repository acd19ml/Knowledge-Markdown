# Agent Memory — 知识库

> 原论文：**《重新思考基础智能体在下半场的记忆机制：一项综述》**
> 作者：Wei-Chieh Huang、Weizhi Zhang、Yueqing Liang 等（50+ 位作者，来自 UIC、UIUC、Stanford、Google、Salesforce、Meta 等机构）
> arXiv：[2502.06250](https://arxiv.org/abs/2506.02250) | GitHub：[AgentMemoryWorld/Awesome-Agent-Memory](https://github.com/AgentMemoryWorld/Awesome-Agent-Memory)
> 发表：2026 年 2 月 | 覆盖：218 篇论文（2023 Q1 – 2025 Q4）

---

## 为什么记忆现在如此重要

该领域正步入 AI 的 **"下半场"** —— 从追求基准分数转向现实世界的实用价值。现实世界中的智能体面临：
- **上下文爆炸**：长时域任务、多会话工作流、动态演化的环境
- **用户依赖性**：跨月/跨年的个性化适配，偏好随时间漂移
- **多智能体协调**：共享状态、路由、冲突消解

记忆是关键解决方案。218 篇论文在两年内发表，2025 年呈指数级增长。

---

## 知识库结构

```
Agent_Memory_zh/
├── README.md                        ← 当前文件（索引与概览）
│
├── 00_survey-overview.md            ← 论文元信息、摘要、分类体系图
├── 01_background.md                 ← 基础智能体、记忆概念、认知科学根源
│
├── 02_taxonomy/
│   ├── README.md                    ← 分类体系概览 + 交叉参考表
│   ├── 2.1_memory-substrates.md     ← 外部 vs 内部存储（记忆的物理载体）
│   ├── 2.2_cognitive-mechanisms.md  ← 感觉/工作/情节/语义/程序记忆
│   └── 2.3_memory-subjects.md       ← 以用户为中心 vs 以智能体为中心的记忆
│
├── 03_operations/
│   ├── single-agent-operations.md   ← 存储、检索、更新、压缩、遗忘
│   └── multi-agent-operations.md    ← 架构、路由、隔离与冲突
│
├── 04_learning-policy.md            ← 智能体如何学习记忆策略（提示/SFT/RL）
├── 05_scaling.md                    ← 规模挑战：上下文受限 vs 现实世界
├── 06_evaluation.md                 ← 评估指标 + 30+ 个标注基准
├── 07_applications.md               ← 11 个应用领域及代表性工作
└── 08_future-directions.md          ← 下一代记忆研究的 6 个开放挑战
```

---

## 快速导航

| 问题 | 前往 |
|---|---|
| 存在哪些类型的记忆存储？ | [2.1 记忆基底](02_taxonomy/2.1_memory-substrates.md) |
| 认知记忆类型如何映射到智能体？ | [2.2 认知机制](02_taxonomy/2.2_cognitive-mechanisms.md) |
| 记忆服务于用户还是智能体？ | [2.3 记忆主体](02_taxonomy/2.3_memory-subjects.md) |
| 单个智能体如何管理记忆？ | [3.1 单智能体操作](03_operations/single-agent-operations.md) |
| 多智能体系统如何共享记忆？ | [3.2 多智能体操作](03_operations/multi-agent-operations.md) |
| 智能体如何学习记忆策略？ | [4. 学习策略](04_learning-policy.md) |
| 哪些基准评估记忆能力？ | [6. 评估](06_evaluation.md) |
| 哪些领域使用了智能体记忆？ | [7. 应用](07_applications.md) |
| 有哪些开放的研究问题？ | [8. 未来方向](08_future-directions.md) |

---

## 三维分类体系（概览）

```
基础智能体记忆
        │
        ├── 记忆基底（WHERE / HOW 存储）
        │       ├── 外部：向量索引、文本记录、结构化存储、层次化存储
        │       └── 内部：权重、潜在状态、KV 缓存
        │
        ├── 认知机制（WHAT FUNCTION 功能定位）
        │       ├── 短期：感觉记忆、工作记忆
        │       └── 长期：情节记忆、语义记忆、程序记忆
        │
        └── 记忆主体（WHO 服务对象）
                ├── 以用户为中心：个性化、偏好、对话历史
                └── 以智能体为中心：任务轨迹、技能、领域知识
```

---

## 综述核心数据

- 分析了 **218 篇论文**（2023 Q1 – 2025 Q4）
- 2025 年 Q3–Q4 呈现**指数级增长**
- 外部记忆占主导地位（约 60% 的工作）
- 情节记忆和语义记忆是最常见的认知类型
- 评估差距：大多数基准测试短时域；现实世界需要长时域记忆指标

---

## 扩展路线图（待补充）

- [ ] 深入研究：具体系统（MemGPT、Generative Agents、Reflexion、Mem0）
- [ ] 深入研究：检索增强生成（RAG）及其向智能体记忆的演进
- [ ] 深入研究：记忆 + 持续学习
- [ ] 逐篇阅读笔记，链接自 `06_evaluation.md` 的基准表格
- [ ] 代码实现与实验
