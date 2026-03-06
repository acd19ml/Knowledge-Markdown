# Knowledge-Markdown

个人知识库 —— AI 工程笔记、API 参考与实践指南。

> **语言约定**：所有笔记以中文为主，technical terms 保留英文原词。
> `Skills/` 为工具目录，保持英文原样。
> **论文材料约定**：各主题下统一使用 `papers/notes/` 存放精读笔记，`papers/source/` 存放原文 PDF。

---

## 目录结构

```
Knowledge-Markdown/
├── README.md                    # 本文件 —— 总索引
├── KB-Expansion-Guide.md        # 知识库扩展工作流指南（论文筛选 → 笔记 → 归档）
│
├── Agent_Memory/                # Foundation Agent Memory（论文综述 + 结构化笔记）
│   ├── README.md
│   ├── 00_survey-overview.md
│   ├── 01_background.md
│   ├── 02_taxonomy/
│   │   ├── 2.1_memory-substrates.md      # External vs Internal storage
│   │   ├── 2.2_cognitive-mechanisms.md   # Sensory/Working/Episodic/Semantic/Procedural
│   │   └── 2.3_memory-subjects.md        # User-centric vs Agent-centric
│   ├── 03_operations/
│   │   ├── single-agent-operations.md
│   │   └── multi-agent-operations.md
│   ├── 04_learning-policy.md
│   ├── 05_scaling.md
│   ├── 06_evaluation.md
│   ├── 07_applications.md
│   ├── 08_future-directions.md
│   └── papers/
│       ├── notes/               # 精读笔记
│       └── source/              # 原文 PDF
│
├── Self_Evolve/                 # Self-Evolving Agents（论文综述 + 结构化笔记）
│   ├── README.md
│   ├── 00_survey-overview.md
│   ├── 01_background.md
│   ├── 02_model-centric/
│   │   ├── 2.1_inference-based.md
│   │   └── 2.2_training-based.md
│   ├── 03_env-centric/
│   │   ├── 3.1_static-knowledge.md
│   │   ├── 3.2_dynamic-experience.md
│   │   ├── 3.3_modular-arch.md
│   │   └── 3.4_agentic-topology.md
│   ├── 04_co-evolution.md
│   ├── 05_applications.md
│   ├── 06_challenges.md
│   ├── 07_benchmarks.md
│   └── papers/
│       ├── notes/
│       └── source/
│
├── GUI_Agent/                   # GUI Agent（论文综述 + 结构化笔记）
│   ├── README.md
│   ├── 00_survey-overview.md
│   ├── 01_background.md
│   ├── 02_capabilities/
│   │   ├── 2.1_gui-comprehension.md
│   │   ├── 2.2_device-control.md
│   │   ├── 2.3_user-interaction.md
│   │   └── 2.4_advanced-capabilities.md
│   ├── 03_task-automation-pipeline.md
│   ├── 04_evaluation.md
│   ├── 05_challenges.md
│   └── papers/
│       ├── notes/
│       └── source/
│
├── Cross_Topic/                 # 跨综述交叉分析（核心研究工具）
│   ├── comparison-matrix.md         # 核心矩阵：GUI Agent × Memory × Self-Evolve
│   ├── gap-tracker.md               # 全局 Gap 分层（A/B/C 类）
│   ├── main-line.md                 # 当前主线问题定义
│   ├── taxonomy-draft.md            # 综述分类框架草稿
│   └── inprogress/                  # 批量同步时的中间更新草稿
│
├── Industry_Insights/           # 从业者视角：podcast、演讲、行业分析
│   ├── 2025-12_CUA-Slow-Thinking-Podcast.md
│   └── 2026-02_Claude-Code-Agent-Design.md
│
├── Claude_API/                  # Claude API 功能与 best practices
│   └── Tool_Use/
│       └── advanced-tool-use-features.md
│
└── Skills/                      # ~/.claude/skills 备份（保持英文原样）
    ├── The-Complete-Guide-to-Building-Skill-for-Claude.md
    ├── kb-maintenance/
    ├── paper-reading-notes/
    ├── pdf/
    └── skill-creator/
```

---

## 当前工作流

1. 精读论文后，将结构化笔记写入对应主题的 `papers/notes/`。
2. 原文 PDF 统一放在对应主题的 `papers/source/`。
3. 需要跨主题沉淀时，更新 [Cross_Topic/comparison-matrix.md](Cross_Topic/comparison-matrix.md) 与 [Cross_Topic/gap-tracker.md](Cross_Topic/gap-tracker.md)。
4. 批量同步时，可先在 `Cross_Topic/inprogress/` 生成 proposal，再合并到正式文件。

---

## 快速索引

### Skills

| 主题 | 文件 | 标签 |
|---|---|---|
| 为 Claude 构建 skill 完全指南 | [Skills/The-Complete-Guide-to-Building-Skill-for-Claude.md](Skills/The-Complete-Guide-to-Building-Skill-for-Claude.md) | skills, slash-commands, claude-code |
| 论文精读笔记生成 | [Skills/paper-reading-notes/SKILL.md](Skills/paper-reading-notes/SKILL.md) | paper-notes, literature-review, evidence |
| 知识库同步（matrix / tracker） | [Skills/kb-maintenance/SKILL.md](Skills/kb-maintenance/SKILL.md) | kb-sync, matrix, gap-tracker |

### Claude API

| 主题 | 文件 | 标签 |
|---|---|---|
| 高级工具调用（PTC、Tool Search、Examples、Dynamic Filtering）；web_search 内置 PTC；LMArena #1 | [Claude_API/Tool_Use/advanced-tool-use-features.md](Claude_API/Tool_Use/advanced-tool-use-features.md) | api, tool-use, token, performance, lmarena |

### Agent Memory

| 主题 | 文件 | 标签 |
|---|---|---|
| 综述概览与导航索引 | [Agent_Memory/README.md](Agent_Memory/README.md) | agent-memory, survey, LLM |
| 精读论文笔记目录 | [Agent_Memory/papers/notes/](Agent_Memory/papers/notes/) | papers, reading-notes |
| Memory substrates（External/Internal） | [Agent_Memory/02_taxonomy/2.1_memory-substrates.md](Agent_Memory/02_taxonomy/2.1_memory-substrates.md) | RAG, KV-cache, vector-store |
| Cognitive mechanisms（5 种类型） | [Agent_Memory/02_taxonomy/2.2_cognitive-mechanisms.md](Agent_Memory/02_taxonomy/2.2_cognitive-mechanisms.md) | episodic, semantic, working, procedural |
| Memory subjects（user-centric / agent-centric） | [Agent_Memory/02_taxonomy/2.3_memory-subjects.md](Agent_Memory/02_taxonomy/2.3_memory-subjects.md) | personalization |
| Memory operations（single & multi-agent） | [Agent_Memory/03_operations/](Agent_Memory/03_operations/) | operations, routing |
| Learning policy（prompting / SFT / RL） | [Agent_Memory/04_learning-policy.md](Agent_Memory/04_learning-policy.md) | fine-tuning, RL |
| Scaling 挑战 | [Agent_Memory/05_scaling.md](Agent_Memory/05_scaling.md) | scaling, context |
| Evaluation benchmarks（30+） | [Agent_Memory/06_evaluation.md](Agent_Memory/06_evaluation.md) | benchmarks, metrics |
| Applications（11 个领域） | [Agent_Memory/07_applications.md](Agent_Memory/07_applications.md) | healthcare, robotics, science |
| Future directions（6 大挑战） | [Agent_Memory/08_future-directions.md](Agent_Memory/08_future-directions.md) | research, open-problems |

### Self-Evolving Agents

| 主题 | 文件 | 标签 |
|---|---|---|
| 综述概览与导航索引 | [Self_Evolve/README.md](Self_Evolve/README.md) | self-evolution, survey, LLM |
| 精读论文笔记目录 | [Self_Evolve/papers/notes/](Self_Evolve/papers/notes/) | papers, workflows, self-evolve |
| Inference-based evolution（test-time scaling） | [Self_Evolve/02_model-centric/2.1_inference-based.md](Self_Evolve/02_model-centric/2.1_inference-based.md) | CoT, tree-search, self-correction |
| Training-based evolution（SFT / RL） | [Self_Evolve/02_model-centric/2.2_training-based.md](Self_Evolve/02_model-centric/2.2_training-based.md) | self-instruct, STaR, GRPO |
| Environment-centric evolution | [Self_Evolve/03_env-centric/](Self_Evolve/03_env-centric/) | RAG, experience, MAS-topology |
| Model-environment co-evolution | [Self_Evolve/04_co-evolution.md](Self_Evolve/04_co-evolution.md) | co-evolution, MARL |
| Applications（Science、SWE、open-world） | [Self_Evolve/05_applications.md](Self_Evolve/05_applications.md) | science, software-engineering |
| 挑战与未来前沿 | [Self_Evolve/06_challenges.md](Self_Evolve/06_challenges.md) | model-collapse, future-work |
| Benchmarks（40+） | [Self_Evolve/07_benchmarks.md](Self_Evolve/07_benchmarks.md) | SWE-bench, WebArena |

### GUI Agent

| 主题 | 文件 | 标签 |
|---|---|---|
| 综述概览 | [GUI_Agent/00_survey-overview.md](GUI_Agent/00_survey-overview.md) | GUI-agent, survey, CUA |
| 精读论文笔记目录 | [GUI_Agent/papers/notes/](GUI_Agent/papers/notes/) | papers, GUI-agent, reading-notes |
| 背景：LLM / MLLM / Agent 基础 | [GUI_Agent/01_background.md](GUI_Agent/01_background.md) | MLLM, CogAgent, LLaVA |
| GUI comprehension | [GUI_Agent/02_capabilities/2.1_gui-comprehension.md](GUI_Agent/02_capabilities/2.1_gui-comprehension.md) | perception, screenshot |
| Device control | [GUI_Agent/02_capabilities/2.2_device-control.md](GUI_Agent/02_capabilities/2.2_device-control.md) | mouse, keyboard, API |
| User interaction | [GUI_Agent/02_capabilities/2.3_user-interaction.md](GUI_Agent/02_capabilities/2.3_user-interaction.md) | clarification, feedback |
| Advanced capabilities（个性化 + 多 Agent 协同） | [GUI_Agent/02_capabilities/2.4_advanced-capabilities.md](GUI_Agent/02_capabilities/2.4_advanced-capabilities.md) | planning, memory, tools |
| Task automation pipeline（探索 → 利用）| [GUI_Agent/03_task-automation-pipeline.md](GUI_Agent/03_task-automation-pipeline.md) | exploration, exploitation |
| Evaluation（24 个数据集）| [GUI_Agent/04_evaluation.md](GUI_Agent/04_evaluation.md) | benchmarks, OSWorld |
| 挑战与未来方向 | [GUI_Agent/05_challenges.md](GUI_Agent/05_challenges.md) | cost, safety, AIOS |

### Cross Topic（核心研究工具）

| 主题 | 文件 | 标签 |
|------|------|------|
| 对比矩阵（GUI × Memory × Self-Evolve）| [Cross_Topic/comparison-matrix.md](Cross_Topic/comparison-matrix.md) | cross-domain, memory, self-evolving |
| 全局 Gap 分层（A/B/C 类，7 个 Gap）| [Cross_Topic/gap-tracker.md](Cross_Topic/gap-tracker.md) | gap, research-direction, priority |
| 主线问题定义 | [Cross_Topic/main-line.md](Cross_Topic/main-line.md) | main-line, rq, method-design |
| 综述分类框架草稿 | [Cross_Topic/taxonomy-draft.md](Cross_Topic/taxonomy-draft.md) | taxonomy, survey-outline |
| 批量同步中间稿 | [Cross_Topic/inprogress/](Cross_Topic/inprogress/) | sync, proposal, batch-update |

### Industry Insights

| 主题 | 文件 | 标签 |
|---|---|---|
| CUA 慢思考实录 —— Ungrounded 播客第 1 期 | [Industry_Insights/2025-12_CUA-Slow-Thinking-Podcast.md](Industry_Insights/2025-12_CUA-Slow-Thinking-Podcast.md) | CUA, GUI-agent, benchmark, business-model, GenUI |
| 从 Agent 视角看世界 —— Claude Code 工具设计实录 | [Industry_Insights/2026-02_Claude-Code-Agent-Design.md](Industry_Insights/2026-02_Claude-Code-Agent-Design.md) | claude-code, tool-design, progressive-disclosure, grep-vs-rag |
