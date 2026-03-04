# 从 Agent 的视角看世界 —— Claude Code 工具设计实录

> **来源**：Thariq Shihipar（Anthropic）—— "Seeing Like an Agent"（2026-02-28）
> **类型**：工程博客 / 设计反思
> **核心主题**：在真实 AI Agent（Claude Code）开发中，工具设计如何塑造模型认知；从失败案例中提炼的设计原则

---

## 一、核心论点

> **"Agent 所见即工具所塑"** —— 工具的形状决定了模型能感知什么、能推理什么。

Thariq 通过 Claude Code 团队的实际案例，说明"从 Agent 的视角设计工具"与"从人类工程师的视角设计 API"之间存在根本性差异。人类工程师倾向于设计灵活、通用的接口；但 Agent 需要的是**边界清晰、认知负荷低**的工具。

---

## 二、AskUserQuestion 工具：三次迭代的教训

### 背景

Claude Code 需要一个工具让模型在执行前向用户澄清意图。团队经历了三个版本才找到合适设计。

### v1：自由文本选项

```json
{
  "question": "Which style do you prefer?",
  "options": ["Option 1: Use tabs for indentation", "Option 2: Use spaces for indentation"]
}
```

**问题**：选项标签 = 完整说明。Claude 会把 option label 写得很长，用户选择时认知负荷高，且模型推理选项含义时容易绑定到表面文字。

### v2：拆分 label 和 description

```json
{
  "question": "Which style?",
  "options": [
    {"label": "Tabs", "description": "Use tabs for indentation throughout"},
    {"label": "Spaces", "description": "Use spaces (2 or 4) for indentation"}
  ]
}
```

**改进**：短 label 强制模型提炼核心概念，description 提供补充上下文。
**发现**：短 label 约束不只是 UI 设计，它迫使模型在构造选项时更清晰地思考选项的本质，而不是把所有细节塞进一行文字。

### v3：加入 markdown preview

```json
{
  "options": [
    {
      "label": "Tabs",
      "description": "...",
      "markdown": "```js\nif (condition) {\n\tdo_thing();\n}\n```"
    }
  ]
}
```

**效果**：对需要视觉对比的场景（代码风格、UI 布局、配置方案），preview 让用户无需想象就能做决策。

### 核心教训

> **工具约束 = 认知约束**。强制 label ≤ 12 字符不是 UI 限制，而是在迫使 Agent 清晰化自己的意图分类。限制越明确，模型思维越聚焦。

---

## 三、Tasks vs Todos：多 Agent 协作的基础设施演进

### Todos（早期版本）

- 简单列表，每项是字符串描述
- 单 Agent 内追踪进度的轻量工具
- 无法表达依赖关系，无法跨 Agent 共享

### Tasks（新版本）

| 字段 | 作用 |
|---|---|
| `subject` | 祈使句标题（"Run tests"） |
| `activeForm` | 进行时形式，显示在 spinner（"Running tests"） |
| `description` | 详细要求，足以让另一个 Agent 接手执行 |
| `blocks` / `blockedBy` | 显式依赖关系 |
| `owner` | 哪个 subagent 持有该任务 |
| `status` | pending / in_progress / completed / deleted |

### 设计动机

**多 Agent 协调需要任务具备三个属性**：
1. **可转移性**：description 足够详细，任意 Agent 都能接手
2. **依赖可见性**：blocks/blockedBy 让调度显式而非隐式
3. **状态持久性**：跨 subagent 边界的进度可追踪

Todos 满足了"单 Agent 进度追踪"，但在 Agent 编排场景下失败了 —— 一个 subagent 不知道另一个 subagent 在做什么，也不知道能否并行。

---

## 四、Grep over RAG：搜索策略的选择

### RAG 的隐性开销

对于结构化代码库，RAG（检索增强生成）引入了：
- **Chunking artifacts**：代码按 token 切块，语义边界被破坏
- **Retrieval failures**：向量相似性不等于代码语义相关性
- **Latency overhead**：embedding + 向量检索 + 重排序的额外延迟
- **Hallucinated coverage**：模型以为找到了相关代码，实际上漏掉了关键文件

### 直接 Grep 的优势

```
Grep("class AuthService") → 精确匹配，0 误差
RAG("authentication service") → 相关内容，但可能遗漏 AuthService 本身
```

**原则**：当搜索目标是**精确标识符**（类名、函数名、变量名、文件路径）时，grep/glob 优先于 RAG。RAG 适合模糊语义查询（"所有和支付相关的逻辑在哪里"）。

### 在 Claude Code 中的体现

Claude Code 的工具集提供了专用的 `Grep` 和 `Glob` 工具，而不仅仅是通用搜索。这不是简单的"封装 grep 命令"，而是在 Agent 层面做出的**认知决策**：不同类型的搜索问题需要不同的工具，而不是一个万能搜索接口。

---

## 五、Progressive Disclosure：分层上下文加载

### 问题

Agent 上下文窗口有限，但需要访问的信息量可能很大。传统解法是"把所有信息都塞进 system prompt" —— 这同时带来了 token 浪费和信号噪声。

### Progressive Disclosure 模式

```
metadata（name + description）
    ↓ 始终在 context，~100 words
SKILL.md body
    ↓ 触发时加载，< 500 lines
references/（引用文件）
    ↓ 按需加载，无限量
scripts/（可执行脚本）
    ↓ 执行时使用，无需全文加载
```

**关键设计**：顶层文件包含明确指针（"当遇到 X 情况时，读取 references/X.md"），而不是把所有可能用到的内容都预加载。Agent 在需要的时候才去加载更深层的信息。

### 原则

> 信息深度 = 触发深度。给 Agent 的信息应该和 Agent 当前任务的复杂度匹配，而不是一次性倾倒所有可能相关的内容。

---

## 六、Claude Code Guide Subagent

Claude Code 引入了一个专用 subagent：`claude-code-guide`。

**职责**：回答关于 Claude Code 本身的问题（功能、hooks、slash commands、MCP servers、设置、IDE 集成、键盘快捷键）以及 Claude API 使用问题。

**设计意图**：将产品知识作为独立的可检索资产，而不是让每个 Agent 都重新学习。这是 **Semantic Memory**（Agent_Memory 框架中的抽象知识存储）在工具设计中的具体应用。

**触发条件**：用户以 "Can Claude..."、"Does Claude..."、"How do I..." 提问时主动调用。

---

## 七、关键设计原则总结

| 原则 | 体现 | 反面教训 |
|---|---|---|
| **约束即认知** | AskUserQuestion 的 label 字数限制 | 无约束 = 模型输出不可控 |
| **为转移性设计** | Tasks 的 description 字段 | Todos 无法跨 Agent |
| **工具匹配查询类型** | Grep/Glob vs 语义搜索 | 万能搜索接口误导模型选择 |
| **信息按需加载** | Progressive Disclosure | 预加载所有信息 = 信号噪声 |
| **知识实体化** | Claude Code Guide subagent | 每次都从头推理产品知识 |

---

## 八、与知识库现有内容的关联

| 主题 | 关联文件 |
|---|---|
| Agent Memory（Semantic/Procedural/Episodic） | [../Agent_Memory/02_taxonomy/2.2_cognitive-mechanisms.md](../Agent_Memory/02_taxonomy/2.2_cognitive-mechanisms.md) |
| Self-Evolving Agents 中的工具增强 | [../Self_Evolve/03_env-centric/3.1_static-knowledge.md](../Self_Evolve/03_env-centric/3.1_static-knowledge.md) |
| Claude Code skill 构建指南 | [../Agent_Skills/The-Complete-Guide-to-Building-Skill-for-Claude.md](../Agent_Skills/The-Complete-Guide-to-Building-Skill-for-Claude.md) |
| GUI Agent 的工具设计对比 | [../GUI_Agent/02_capabilities/2.4_advanced-capabilities.md](../GUI_Agent/02_capabilities/2.4_advanced-capabilities.md) |
| PTC 与工具调用优化 | [../Claude_API/Tool_Use/advanced-tool-use-features.md](../Claude_API/Tool_Use/advanced-tool-use-features.md) |

---

## 个人研究笔记

- [ ] AskUserQuestion 的三次迭代是否揭示了一个更通用的原则：**工具 schema 应该反映认知过程，而不只是数据结构**？
- [ ] Progressive Disclosure 与 Self-Evolving Agents 中的"工具增强"（Tool Use Evolution）是否有结构性对应关系？
- [ ] Grep over RAG 的选择在 GUI Agent 场景中如何应用？GUI Agent 的"信息检索"是截图嵌入检索还是 UI 元素精确匹配？
