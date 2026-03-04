# Knowledge-Markdown

个人知识库 —— AI 工程笔记、API 参考与实践指南。

> **语言约定**：所有笔记以中文为主，technical terms 保留英文原词。
> `Claude_Skills/` 为工具目录，保持英文原样。

---

## 目录结构

```
Knowledge-Markdown/
├── README.md                    # 本文件 —— 总索引
│
├── Agent_Skills/                # 为 Claude Code 构建自定义 skill
│   └── The-Complete-Guide-to-Building-Skill-for-Claude.md
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
│   └── 08_future-directions.md
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
│   └── 07_benchmarks.md
│
├── GUI_Agent/                   # GUI Agent（论文综述 + 结构化笔记）
│   ├── 00_survey-overview.md
│   ├── comparison-matrix.md
│   ├── 02_capabilities/
│   │   ├── 2.1_gui-comprehension.md
│   │   ├── 2.2_device-control.md
│   │   ├── 2.3_user-interaction.md
│   │   └── 2.4_advanced-capabilities.md
│   └── 04_evaluation.md
│
├── Cross_Topic/                 # 跨综述交叉分析（核心研究工具）
│   ├── master-comparison-matrix.md  # 唯一核心矩阵：GUI Agent × Memory × Self-Evolve
│   ├── gap-tracker.md               # 全局 Gap 分层（A/B/C 类）
│   ├── gui-agent-x-memory.md        # GUI Agent × Agent Memory 交叉分析
│   ├── gui-agent-x-self-evolving.md # GUI Agent × Self-Evolving 交叉分析
│   └── taxonomy-draft.md            # 综述分类框架草稿
│
├── Industry_Insights/           # 从业者视角：podcast、演讲、行业分析
│   └── 2025-12_CUA-Slow-Thinking-Podcast.md
│
├── Claude_API/                  # Claude API 功能与 best practices
│   └── Tool_Use/
│       └── advanced-tool-use-features.md
│
└── Claude_Skills/               # ~/.claude/skills 备份（保持英文原样）
    ├── paper-notes/
    ├── pdf/
    └── skill-creator/
```

---

## 快速索引

### Agent Skills

| 主题 | 文件 | 标签 |
|---|---|---|
| 为 Claude 构建 skill 完全指南 | [Agent_Skills/The-Complete-Guide-to-Building-Skill-for-Claude.md](Agent_Skills/The-Complete-Guide-to-Building-Skill-for-Claude.md) | skills, slash-commands, claude-code |

### Claude API

| 主题 | 文件 | 标签 |
|---|---|---|
| 高级工具调用（PTC、Tool Search、Examples、Dynamic Filtering）；web_search 内置 PTC + LMArena #1 | [Claude_API/Tool_Use/advanced-tool-use-features.md](Claude_API/Tool_Use/advanced-tool-use-features.md) | api, tool-use, token, performance, lmarena |

### Agent Memory

| 主题 | 文件 | 标签 |
|---|---|---|
| 综述概览与导航索引 | [Agent_Memory/README.md](Agent_Memory/README.md) | agent-memory, survey, LLM |
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
| 能力对比矩阵 | [GUI_Agent/comparison-matrix.md](GUI_Agent/comparison-matrix.md) | comparison, capabilities |
| GUI comprehension | [GUI_Agent/02_capabilities/2.1_gui-comprehension.md](GUI_Agent/02_capabilities/2.1_gui-comprehension.md) | perception, screenshot |
| Device control | [GUI_Agent/02_capabilities/2.2_device-control.md](GUI_Agent/02_capabilities/2.2_device-control.md) | mouse, keyboard, API |
| User interaction | [GUI_Agent/02_capabilities/2.3_user-interaction.md](GUI_Agent/02_capabilities/2.3_user-interaction.md) | clarification, feedback |
| Advanced capabilities | [GUI_Agent/02_capabilities/2.4_advanced-capabilities.md](GUI_Agent/02_capabilities/2.4_advanced-capabilities.md) | planning, memory, tools |
| Evaluation | [GUI_Agent/04_evaluation.md](GUI_Agent/04_evaluation.md) | benchmarks, OSWorld |

### Cross Topic（核心研究工具）

| 主题 | 文件 | 标签 |
|------|------|------|
| Master 对比矩阵（GUI × Memory × Self-Evolve）| [Cross_Topic/master-comparison-matrix.md](Cross_Topic/master-comparison-matrix.md) | cross-domain, memory, self-evolving |
| 全局 Gap 分层（A/B/C 类，7个 Gap）| [Cross_Topic/gap-tracker.md](Cross_Topic/gap-tracker.md) | gap, research-direction, priority |
| GUI Agent × Agent Memory 交叉分析 | [Cross_Topic/gui-agent-x-memory.md](Cross_Topic/gui-agent-x-memory.md) | episodic, procedural, user-centric |
| GUI Agent × Self-Evolving 交叉分析 | [Cross_Topic/gui-agent-x-self-evolving.md](Cross_Topic/gui-agent-x-self-evolving.md) | AWM, offline-evolution, skills |
| 综述分类框架草稿 | [Cross_Topic/taxonomy-draft.md](Cross_Topic/taxonomy-draft.md) | taxonomy, survey-outline |

### Industry Insights

| 主题 | 文件 | 标签 |
|---|---|---|
| CUA 慢思考实录 —— Ungrounded 播客第 1 期 | [Industry_Insights/2025-12_CUA-Slow-Thinking-Podcast.md](Industry_Insights/2025-12_CUA-Slow-Thinking-Podcast.md) | CUA, GUI-agent, benchmark, business-model, GenUI |
| 从 Agent 视角看世界 —— Claude Code 工具设计实录 | [Industry_Insights/2026-02_Claude-Code-Agent-Design.md](Industry_Insights/2026-02_Claude-Code-Agent-Design.md) | claude-code, tool-design, progressive-disclosure, grep-vs-rag |
