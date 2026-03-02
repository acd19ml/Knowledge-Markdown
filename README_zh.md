# Knowledge-Markdown

个人知识库 —— AI 工程笔记、API 参考与实践指南。

> English index: [README.md](README.md)

## 双语维护约定

所有笔记同时维护中英两个版本。

| 文件 | 语言 |
|------|------|
| `<name>.md` | 英文（主版本） |
| `<name>_zh.md` 或 `<name>_zh/` | 中文 |

中英文件放在同一目录或对应 `_zh` 目录下，便于对照编辑与同步更新。本索引只链接中文文件 —— 英文索引见 [README.md](README.md)。

## 目录结构

```
Knowledge-Markdown/
├── README.md                    # 英文总目录
├── README_zh.md                 # 中文总目录（本文件）
│
├── Agent_Skills/                # 为 Claude Code 构建自定义 Skill
│   ├── The-Complete-Guide-to-Building-Skill-for-Claude.md       # 英文
│   └── The-Complete-Guide-to-Building-Skill-for-Claude_zh.md    # 中文
│
├── Agent_Memory/                # 基础智能体记忆 —— 英文（论文 + 结构化笔记）
│   └── （详见英文 README.md）
│
├── Agent_Memory_zh/             # 基础智能体记忆 —— 中文翻译
│   ├── README.md
│   ├── 00_survey-overview.md
│   ├── 01_background.md
│   ├── 02_taxonomy/
│   │   ├── README.md
│   │   ├── 2.1_memory-substrates.md
│   │   ├── 2.2_cognitive-mechanisms.md
│   │   └── 2.3_memory-subjects.md
│   ├── 03_operations/
│   │   ├── single-agent-operations.md
│   │   └── multi-agent-operations.md
│   ├── 04_learning-policy.md
│   ├── 05_scaling.md
│   ├── 06_evaluation.md
│   ├── 07_applications.md
│   └── 08_future-directions.md
│
├── Self_Evolve/                 # 自演化智能体 —— 英文（论文 + 结构化笔记）
│   └── （详见英文 README.md）
│
├── Self_Evolve_zh/              # 自演化智能体 —— 中文翻译
│   ├── README.md
│   ├── 00_survey-overview.md
│   ├── 01_background.md
│   ├── 02_model-centric/
│   │   ├── README.md
│   │   ├── 2.1_inference-based.md
│   │   └── 2.2_training-based.md
│   ├── 03_env-centric/
│   │   ├── README.md
│   │   ├── 3.1_static-knowledge.md
│   │   ├── 3.2_dynamic-experience.md
│   │   ├── 3.3_modular-arch.md
│   │   └── 3.4_agentic-topology.md
│   ├── 04_co-evolution.md
│   ├── 05_applications.md
│   ├── 06_challenges.md
│   └── 07_benchmarks.md
│
├── Industry_Insights/           # 从业者视角：播客、演讲、行业分析
│   ├── 2025-12_CUA-Slow-Thinking-Podcast.md     # 英文
│   └── 2025-12_CUA-Slow-Thinking-Podcast_zh.md  # 中文
│
└── Claude_API/                  # Claude API 功能与最佳实践
    └── Tool_Use/
        ├── advanced-tool-use-features.md       # 英文
        └── advanced-tool-use-features_zh.md    # 中文
```

## 快速索引

### Agent Skills

| 主题 | 文件 | 标签 |
|------|------|------|
| 为 Claude 构建 Skill 完全指南 | [Agent_Skills/The-Complete-Guide-to-Building-Skill-for-Claude_zh.md](Agent_Skills/The-Complete-Guide-to-Building-Skill-for-Claude_zh.md) | skills, slash-commands, claude-code |

### Claude API

| 主题 | 文件 | 标签 |
|------|------|------|
| 高级工具调用功能（PTC、工具搜索、示例、动态过滤） | [Claude_API/Tool_Use/advanced-tool-use-features_zh.md](Claude_API/Tool_Use/advanced-tool-use-features_zh.md) | api, tool-use, tokens, performance |

### 基础智能体记忆（中文）

| 主题 | 文件 | 标签 |
|------|------|------|
| 综述概览与导航索引 | [Agent_Memory_zh/README.md](Agent_Memory_zh/README.md) | agent-memory, survey, LLM, research |
| 记忆基底（外部/内部） | [Agent_Memory_zh/02_taxonomy/2.1_memory-substrates.md](Agent_Memory_zh/02_taxonomy/2.1_memory-substrates.md) | memory, RAG, KV-cache, vector-store |
| 认知机制（5 种类型） | [Agent_Memory_zh/02_taxonomy/2.2_cognitive-mechanisms.md](Agent_Memory_zh/02_taxonomy/2.2_cognitive-mechanisms.md) | episodic, semantic, working, procedural |
| 记忆主体（以用户/智能体为中心） | [Agent_Memory_zh/02_taxonomy/2.3_memory-subjects.md](Agent_Memory_zh/02_taxonomy/2.3_memory-subjects.md) | user-memory, agent-memory, personalization |
| 记忆操作（单/多智能体） | [Agent_Memory_zh/03_operations/](Agent_Memory_zh/03_operations/) | operations, multi-agent, routing |
| 记忆学习策略（提示/SFT/RL） | [Agent_Memory_zh/04_learning-policy.md](Agent_Memory_zh/04_learning-policy.md) | learning, RL, fine-tuning, prompting |
| 规模化挑战 | [Agent_Memory_zh/05_scaling.md](Agent_Memory_zh/05_scaling.md) | scaling, context, multi-agent |
| 评估基准（30+ 条目） | [Agent_Memory_zh/06_evaluation.md](Agent_Memory_zh/06_evaluation.md) | benchmarks, evaluation, metrics |
| 应用场景（11 个领域） | [Agent_Memory_zh/07_applications.md](Agent_Memory_zh/07_applications.md) | healthcare, robotics, finance, science |
| 未来研究方向（6 大挑战） | [Agent_Memory_zh/08_future-directions.md](Agent_Memory_zh/08_future-directions.md) | research, future, open-problems |

### 行业洞察

| 主题 | 文件 | 标签 |
|------|------|------|
| CUA 慢思考实录 —— Ungrounded 播客第 1 期 | [Industry_Insights/2025-12_CUA-Slow-Thinking-Podcast_zh.md](Industry_Insights/2025-12_CUA-Slow-Thinking-Podcast_zh.md) | CUA, GUI-agent, benchmark, business-model, GenUI, continual-learning, startup |

### 自演化智能体（中文）

| 主题 | 文件 | 标签 |
|------|------|------|
| 综述概览与导航索引 | [Self_Evolve_zh/README.md](Self_Evolve_zh/README.md) | self-evolution, survey, LLM, agents |
| 基于推理的演化（测试时扩展） | [Self_Evolve_zh/02_model-centric/2.1_inference-based.md](Self_Evolve_zh/02_model-centric/2.1_inference-based.md) | inference, CoT, tree-search, self-correction |
| 基于训练的演化（SFT/RL） | [Self_Evolve_zh/02_model-centric/2.2_training-based.md](Self_Evolve_zh/02_model-centric/2.2_training-based.md) | self-instruct, STaR, GRPO, WebRL |
| 以环境为中心的演化 | [Self_Evolve_zh/03_env-centric/](Self_Evolve_zh/03_env-centric/) | RAG, experience, memory-arch, MAS-topology |
| 模型-环境协同进化 | [Self_Evolve_zh/04_co-evolution.md](Self_Evolve_zh/04_co-evolution.md) | co-evolution, adaptive-curriculum, MARL |
| 应用场景（科学、软件工程、开放世界） | [Self_Evolve_zh/05_applications.md](Self_Evolve_zh/05_applications.md) | science, software-engineering, gaming |
| 挑战与未来前沿 | [Self_Evolve_zh/06_challenges.md](Self_Evolve_zh/06_challenges.md) | challenges, model-collapse, future-work |
| 评估基准（40+ 条目） | [Self_Evolve_zh/07_benchmarks.md](Self_Evolve_zh/07_benchmarks.md) | benchmarks, evaluation, SWE-bench, WebArena |
