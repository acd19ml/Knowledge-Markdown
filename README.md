# Knowledge-Markdown — 终身学习知识库

**目标：** 从 foundations 到 applications 构建完整的 AI Agent 知识体系
**方法：** 阅读原文 + 源码 → 代码实践 → 实验复盘 → Critical Reflection
**原则：** 可扩展性优先，位置即关系，不维护交叉链接

> **语言约定**：中文为主，technical terms 保留英文。
> **论文约定**：`papers/notes/` 精读笔记，`papers/source/` 原文 PDF，`papers/text/` 提取文本。

---

## 知识体系

```
┌──────────────────────────────────────────────────────┐
│              applications/                            │
│   gui-agent/                                         │
│   （综合使用所有 capabilities 的具体系统）               │
├──────────────────────────────────────────────────────┤
│              capabilities/           能力层           │
│   memory          self-improvement     grounding     │
│   planning         alignment                         │
│   （Agent 需要的跨学科能力，从多个 core 学科汲取）       │
├──────────────────────────────────────────────────────┤
│              core/                   核心领域层        │
│   nlp-llm          reinforcement-learning            │
│   generative-models                                  │
│   （独立学科的理论体系）                                │
├──────────────────────────────────────────────────────┤
│              foundations/            基础层           │
│   python       ml       deep-learning                │
│   （工具与数学语言）                                    │
└──────────────────────────────────────────────────────┘
```

---

## 仓库结构

```
Knowledge-Markdown/
├── README.md                                   ← 你在这里
├── _meta/                                      进度看板、面试题库
├── _tools/                                     工具参考（Claude API、Skills）
├── _archive/                                   interim 阶段归档（只读）
│
├── foundations/                                 基础层
│   ├── python/
│   ├── ml/
│   └── deep-learning/
│
├── core/                                        核心领域层
│   ├── nlp-llm/
│   │   └── context-management/                 专题：上下文管理与记忆系统
│   ├── reinforcement-learning/
│   └── generative-models/
│
├── capabilities/                                能力层
│   ├── memory/                                 Agent 如何记住
│   │   ├── survey/                             Agent Memory Survey 笔记
│   │   └── papers/                             MemGPT, Generative Agents, AWM 等
│   ├── self-improvement/                       Agent 如何变强
│   │   ├── survey/                             Self-Evolving Agents Survey 笔记
│   │   └── papers/                             Reflexion, ExpeL, SkillWeaver 等
│   └── grounding/                              Agent 如何感知世界（CS6487）
│
└── applications/                                应用层
    └── gui-agent/                              北极星
        ├── survey/                             GUI Agent Survey 笔记
        └── papers/                             AppAgent, MobileAgent, MAGNET 等
```

---

## 每个目录的约定

```
{topic}/
├── README.md           概念索引 + 子目录导航（持续更新）
├── survey/             survey 来源的结构化笔记（标记来源，待通过原文深化）
├── papers/             单篇论文精读 + 源码复现
│   ├── notes/          精读笔记 .md
│   ├── source/         原文 PDF
│   └── text/           提取文本
├── tutorial.ipynb      代码实践（持续更新）
└── {subtopic}/         子主题（递归同样结构）
```

---

## 课程对应

| 课程 | 定位 | 目录位置 |
|------|------|---------|
| CS5489 | ML/DL 全局底座 | `foundations/` |
| CS5491 | FunSearch + LLM CoT | `core/nlp-llm/` |
| CS6493 | NLP → LLM → Agent | `core/nlp-llm/` + `capabilities/self-improvement/` |
| SDS6007 | RL 完整体系 | `core/reinforcement-learning/` |
| CS5494 | 生成模型全家族 | `core/generative-models/` |
| CS6487 | MLLM Visual Grounding | `capabilities/grounding/` |
