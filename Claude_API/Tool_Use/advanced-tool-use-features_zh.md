# Claude 高级工具调用功能（GA — 2026-02-18）

> 适用模型：Claude Opus 4.6 / Sonnet 4.6 / Sonnet 4.5 / Opus 4.5
> 可用平台：Claude API & Microsoft Foundry（**不支持** Bedrock / Vertex AI）

**参考来源**
- [Anthropic 工程博客 — Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use)
- [官方文档 — Programmatic Tool Calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)
- [社区报告 — Claude Advanced Tool Use Patterns](https://github.com/shanraisshan/claude-code-best-practice/blob/main/reports/claude-advanced-tool-use.md)

---

## 概览

四项正式可用（GA）功能，用于优化多工具工作流中的 Token 消耗并降低延迟：

| 功能 | 解决的问题 | 效果 | 状态 |
|---|---|---|---|
| 程序化工具调用（PTC） | 多轮交互污染上下文 | Token 减少约 37% | GA |
| 工具搜索工具 | 启动时加载过多工具定义 | 定义 Token 减少约 85% | GA |
| 工具使用示例 | Schema 无法表达使用模式 | 准确率 72% → 90% | GA |
| 动态过滤（网页搜索/抓取） | 原始 HTML 撑爆上下文 | 输入 Token 减少约 24% | GA |

---

## 1. 程序化工具调用（PTC）

### 核心思路

**传统方式**：每次工具调用 = 1 次模型推理。所有中间结果都进入上下文窗口。

```
3 个工具 → 3 次推理 → 所有响应污染上下文 → Token 成本高
```

**PTC**：Claude 编写一段 Python 脚本，在沙盒中编排所有工具调用。只有 `stdout`（最终摘要）进入上下文窗口。

```
3 个工具 → 1 次推理 → 只有最终输出进入上下文 → Token 成本降低约 37%
```

**真实场景举例**：检查 20 名员工的预算合规情况。
- 传统方式：20+ 次工具调用，2000+ 条费用记录进入上下文。
- PTC：一个脚本执行 20 次查询，过滤结果，只返回 2–3 个超出预算的人。

### 基准测试结果

| 指标 | 优化前 | 优化后 |
|---|---|---|
| Token 用量 | 43,588 | 27,297（−37%） |
| BrowseComp（Sonnet 4.6） | 33.3% | 46.6% |
| BrowseComp（Opus 4.6） | 45.3% | 61.6% |
| DeepSearchQA F1（Sonnet 4.6） | 52.6% | 59.4% |
| DeepSearchQA F1（Opus 4.6） | 69.8% | 77.3% |

### 工作原理

1. Claude 编写 Python 代码，通过 `await tool_name(args)` 调用你的工具。
2. 代码在沙盒容器中通过代码执行工具运行。
3. API 暂停，返回一个 `tool_use` 块 —— 你提供工具结果。
4. 代码执行恢复；中间结果**不会**进入 Claude 的上下文。
5. 只有最终的 `stdout` 返回给 Claude。

### 配置 — 关键字段

**工具定义** — 将工具标记为可程序化调用：

```json
{
  "name": "query_database",
  "description": "执行 SQL，以 JSON 对象列表形式返回行数据。",
  "input_schema": { ... },
  "allowed_callers": ["code_execution_20260120"]
}
```

`allowed_callers` 可选值：
- `["direct"]` — 只允许 Claude 直接调用（默认）
- `["code_execution_20260120"]` — 只允许在代码执行中调用
- `["direct", "code_execution_20260120"]` — 两者都允许（不推荐：需给 Claude 明确指引）

**请求中还必须包含代码执行工具：**

```json
{ "type": "code_execution_20260120", "name": "code_execution" }
```

**响应中包含 `caller` 字段：**

```json
{
  "type": "tool_use",
  "name": "query_database",
  "caller": {
    "type": "code_execution_20260120",
    "tool_id": "srvtoolu_abc123"
  }
}
```

**容器生命周期：**
- 每个会话创建一个新容器，除非传入 `container` ID 来复用。
- 空闲约 4.5 分钟后过期，注意监控 `expires_at`。
- 等待你的工具结果期间如果容器过期，Claude 会自动重试。

### 高级模式

**批量处理（N 个条目 = 1 次推理）：**
```python
regions = ["West", "East", "Central", "North", "South"]
results = {}
for region in regions:
    data = await query_database(f"SELECT * FROM sales WHERE region='{region}'")
    results[region] = sum(row["revenue"] for row in data)
top = max(results.items(), key=lambda x: x[1])
print(f"最佳区域：{top[0]} — ${top[1]:,}")
```

**提前终止：**
```python
for endpoint in ["us-east", "eu-west", "apac"]:
    if await check_health(endpoint) == "healthy":
        print(f"健康端点：{endpoint}")
        break
```

**条件工具选择：**
```python
info = await get_file_info(path)
content = await read_full_file(path) if info["size"] < 10000 else await read_file_summary(path)
print(content)
```

**数据过滤：**
```python
logs = await fetch_logs(server_id)
errors = [l for l in logs if "ERROR" in l]
print(f"{len(errors)} 条错误\n" + "\n".join(errors[-10:]))
```

### 限制

- 需要启用代码执行工具。
- **不支持** Bedrock 或 Vertex AI。
- 与以下功能不兼容：MCP 工具、标准版网页搜索/抓取、`strict: true` 结构化输出、强制 `tool_choice`。
- 不支持 `disable_parallel_tool_use: true`。
- 响应程序化工具调用时：消息必须**只**包含 `tool_result` 块（不能有文本）。
- 容器有效期约 4.5 分钟。

### 适用场景

**推荐使用：** 需要聚合的大型数据集、3 个以上的依赖工具调用、在推理前需要过滤/排序、对大量条目并行操作。

**不推荐使用：** 单次工具调用且响应简单、极快的操作（容器开销大于收益）。

---

## 2. 工具搜索工具

### 问题

加载 50 个 MCP 工具，每个约 1.5K Token = 用户还没提问就消耗了 75K Token。一个五服务器配置（58 个工具）消耗约 55K Token；内部配置甚至达到 134K Token。

### 解决方案

将不常用的工具标记为 `defer_loading: true`，Claude 通过正则或 BM25 搜索按需发现它们 —— 系统自动提供一个"工具搜索工具"。

### 配置

```json
{
  "toolsets": [
    {
      "default_config": { "defer_loading": true },
      "tools": [
        { "name": "essential_tool", "defer_loading": false },
        { "name": "rare_tool" }
      ]
    }
  ]
}
```

### 效果

| 指标 | 优化前 | 优化后 |
|---|---|---|
| Token 减少 | 72K tokens | 8.7K tokens（−85%） |
| Opus 4 准确率 | 49% | 74% |
| Opus 4.5 准确率 | 79.5% | 88.1% |

### Claude Code 集成

自 v2.1.7 起默认开启自动模式。当 MCP 工具描述超过上下文的 10% 时自动延迟加载。可通过 `ENABLE_TOOL_SEARCH=auto:N` 配置。

### 最佳实践

- 将最常用的 3–5 个工具始终保持加载（`defer_loading: false`）。
- 使用清晰、描述性强的工具名称，有助于搜索发现。

---

## 3. 工具使用示例

### 问题

JSON Schema 定义了结构，但无法表达：
- 何时包含可选参数
- 有效的参数组合
- 格式约定
- 嵌套结构的用法

### 解决方案

在工具定义中添加 `input_examples` 数组，提供具体使用样例：

```json
{
  "name": "query_database",
  "description": "执行 SQL 查询...",
  "input_schema": { ... },
  "input_examples": [
    { "sql": "SELECT * FROM sales WHERE region='West' AND year=2025" },
    { "sql": "SELECT customer_id, SUM(revenue) FROM orders GROUP BY customer_id LIMIT 10" }
  ]
}
```

### 效果

工具参数准确率：**72% → 90%**（复杂参数处理场景）。

---

## 4. 动态过滤（网页搜索/抓取）

### 问题

网页工具返回包含导航栏、广告和样板内容的完整 HTML 页面 —— 浪费 Token 并降低准确率。

### 解决方案

Claude 编写过滤代码，在结果进入上下文前提取相关内容。使用更新后的工具类型：

- `web_search_20260209`
- `web_fetch_20260209`

必须包含请求头：`anthropic-beta: code-execution-web-tools-2026-02-09`

### 效果

| 指标 | 优化前 | 优化后 |
|---|---|---|
| 输入 Token | 基准 | −24% |
| BrowseComp（Sonnet 4.6） | 33.3% | 46.6% |
| BrowseComp（Opus 4.6） | 45.3% | 61.6% |
| DeepSearchQA F1（Sonnet 4.6） | 52.6% | 59.4% |
| DeepSearchQA F1（Opus 4.6） | 69.8% | 77.3% |

---

## 实施策略指南

根据你的主要瓶颈选择对应功能：

| 瓶颈 | 解决方案 |
|---|---|
| 过多工具定义导致上下文膨胀 | 工具搜索工具（`defer_loading`） |
| 工具中间结果体量大 | 程序化工具调用（PTC） |
| 网页搜索噪声 / 无关 HTML | 动态过滤 |
| 参数错误 / 工具调用质量差 | 工具使用示例 |

可叠加使用多个功能以获得复合收益 —— 四项功能相互兼容（各自的约束条件除外）。

---

## 模型兼容性

| 模型 | PTC 工具版本 |
|---|---|
| Claude Opus 4.6（`claude-opus-4-6`） | `code_execution_20260120` |
| Claude Sonnet 4.6（`claude-sonnet-4-6`） | `code_execution_20260120` |
| Claude Sonnet 4.5（`claude-sonnet-4-5-20250929`） | `code_execution_20260120` |
| Claude Opus 4.5（`claude-opus-4-5-20251101`） | `code_execution_20260120` |
