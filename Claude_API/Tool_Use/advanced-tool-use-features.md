# Claude 高级工具调用功能（GA — 2026-02-18）

> 适用模型：Claude Opus 4.6 / Sonnet 4.6 / Sonnet 4.5 / Opus 4.5
> 可用平台：Claude API & Microsoft Foundry（**不支持** Bedrock / Vertex AI）

**参考来源**
- [Anthropic Engineering Blog — Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use)
- [官方文档 — Programmatic Tool Calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)
- [社区报告 — Claude Advanced Tool Use Patterns](https://github.com/shanraisshan/claude-code-best-practice/blob/main/reports/claude-advanced-tool-use.md)

---

## 概览

四项正式可用（GA）功能，用于优化多工具 workflow 的 token 消耗并降低 latency：

| 功能 | 解决的问题 | 效果 | 状态 |
|---|---|---|---|
| Programmatic Tool Calling (PTC) | 多轮交互污染 context | token 减少约 37% | GA |
| Tool Search Tool | 启动时加载过多工具定义 | 定义 token 减少约 85% | GA |
| Tool Use Examples | schema 无法表达使用模式 | 准确率 72% → 90% | GA |
| Dynamic Filtering（网页搜索/抓取） | 原始 HTML 撑爆 context | 输入 token 减少约 24% | GA |

---

## 1. Programmatic Tool Calling (PTC)

### 核心思路

**传统方式**：每次工具调用 = 1 次模型 inference。所有中间结果都进入 context window。

```
3 个工具 → 3 次 inference → 所有响应污染 context → token 成本高
```

**PTC**：Claude 编写一段 Python 脚本，在 sandbox 中编排所有工具调用。只有 `stdout`（最终摘要）进入 context window。

```
3 个工具 → 1 次 inference → 只有最终输出进入 context → token 成本降低约 37%
```

**真实场景举例**：检查 20 名员工的预算合规情况。
- 传统方式：20+ 次工具调用，2000+ 条费用记录进入 context。
- PTC：一个脚本执行 20 次查询，过滤结果，只返回 2–3 个超出预算的人。

### Benchmark 结果

| 指标 | 优化前 | 优化后 |
|---|---|---|
| token 用量 | 43,588 | 27,297（−37%） |
| BrowseComp（Sonnet 4.6） | 33.3% | 46.6% |
| BrowseComp（Opus 4.6） | 45.3% | 61.6% |
| DeepSearchQA F1（Sonnet 4.6） | 52.6% | 59.4% |
| DeepSearchQA F1（Opus 4.6） | 69.8% | 77.3% |

### 工作原理

1. Claude 编写 Python 代码，通过 `await tool_name(args)` 调用你的工具。
2. 代码在 sandbox container 中通过 code execution 工具运行。
3. API 暂停，返回一个 `tool_use` block —— 你提供工具结果。
4. 代码执行恢复；中间结果**不会**进入 Claude 的 context。
5. 只有最终的 `stdout` 返回给 Claude。

### 配置 — 关键字段

**工具定义** — 将工具标记为可 programmatic 调用：

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
- `["code_execution_20260120"]` — 只允许在 code execution 中调用
- `["direct", "code_execution_20260120"]` — 两者都允许（不推荐：需给 Claude 明确指引）

**Request 中还必须包含 code execution 工具：**

```json
{ "type": "code_execution_20260120", "name": "code_execution" }
```

**Response 中包含 `caller` 字段：**

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

**Container lifecycle：**
- 每个 session 创建一个新 container，除非传入 `container` ID 来复用。
- 空闲约 4.5 分钟后过期，注意监控 `expires_at`。
- 等待工具结果期间如果 container 过期，Claude 会自动重试。

### 高级模式

**Batch 处理（N 个条目 = 1 次 inference）：**
```python
regions = ["West", "East", "Central", "North", "South"]
results = {}
for region in regions:
    data = await query_database(f"SELECT * FROM sales WHERE region='{region}'")
    results[region] = sum(row["revenue"] for row in data)
top = max(results.items(), key=lambda x: x[1])
print(f"Top region: {top[0]} — ${top[1]:,}")
```

**Early termination：**
```python
for endpoint in ["us-east", "eu-west", "apac"]:
    if await check_health(endpoint) == "healthy":
        print(f"Healthy: {endpoint}")
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
print(f"{len(errors)} errors\n" + "\n".join(errors[-10:]))
```

### 限制

- 需要启用 code execution 工具。
- **不支持** Bedrock 或 Vertex AI。
- 与以下功能不兼容：MCP 工具、标准版网页搜索/抓取、`strict: true` structured output、强制 `tool_choice`。
- 不支持 `disable_parallel_tool_use: true`。
- 响应 programmatic tool call 时：message 必须**只**包含 `tool_result` block（不能有文本）。
- Container 有效期约 4.5 分钟。

### 适用场景

**推荐使用：** 需要聚合的大型数据集、3 个以上的依赖工具调用、在推理前需要过滤/排序、对大量条目并行操作。

**不推荐使用：** 单次工具调用且响应简单、极快的操作（container overhead 大于收益）。

---

## 2. Tool Search Tool

### 问题

加载 50 个 MCP 工具，每个约 1.5K token = 用户还没提问就消耗了 75K token。一个五服务器配置（58 个工具）消耗约 55K token；内部配置甚至达到 134K token。

### 解决方案

将不常用的工具标记为 `defer_loading: true`，Claude 通过正则或 BM25 search 按需发现它们 —— 系统自动提供一个 "Tool Search Tool"。

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
| token 减少 | 72K tokens | 8.7K tokens（−85%） |
| Opus 4 准确率 | 49% | 74% |
| Opus 4.5 准确率 | 79.5% | 88.1% |

### Claude Code 集成

自 v2.1.7 起默认开启 auto 模式。当 MCP 工具描述超过 context 的 10% 时自动 defer loading。可通过 `ENABLE_TOOL_SEARCH=auto:N` 配置。

### Best Practices

- 将最常用的 3–5 个工具始终保持加载（`defer_loading: false`）。
- 使用清晰、描述性强的工具名称，有助于 search discovery。

---

## 3. Tool Use Examples

### 问题

JSON Schema 定义了结构，但无法表达：
- 何时包含可选参数
- 有效的参数组合
- Format 约定
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

## 4. Dynamic Filtering（网页搜索/抓取）

### 问题

网页工具返回包含导航栏、广告和 boilerplate 的完整 HTML 页面 —— 浪费 token 并降低准确率。

### 解决方案

Claude 编写 filtering 代码，在结果进入 context 前提取相关内容。使用更新后的工具类型：

- `web_search_20260209`
- `web_fetch_20260209`

必须包含 request header：`anthropic-beta: code-execution-web-tools-2026-02-09`

### 效果

| 指标 | 优化前 | 优化后 |
|---|---|---|
| 输入 token | baseline | −24% |
| BrowseComp（Sonnet 4.6） | 33.3% | 46.6% |
| BrowseComp（Opus 4.6） | 45.3% | 61.6% |
| DeepSearchQA F1（Sonnet 4.6） | 52.6% | 59.4% |
| DeepSearchQA F1（Opus 4.6） | 69.8% | 77.3% |

---

## 实施策略

根据主要瓶颈选择对应功能：

| 瓶颈 | 解决方案 |
|---|---|
| 过多工具定义导致 context 膨胀 | Tool Search Tool（`defer_loading`） |
| 工具中间结果体量大 | Programmatic Tool Calling (PTC) |
| 网页搜索噪声 / 无关 HTML | Dynamic Filtering |
| 参数错误 / 工具调用质量差 | Tool Use Examples |

四项功能可叠加使用以获得复合收益（各自约束条件除外）。

---

## 模型兼容性

| 模型 | PTC Tool Version |
|---|---|
| Claude Opus 4.6（`claude-opus-4-6`） | `code_execution_20260120` |
| Claude Sonnet 4.6（`claude-sonnet-4-6`） | `code_execution_20260120` |
| Claude Sonnet 4.5（`claude-sonnet-4-5-20250929`） | `code_execution_20260120` |
| Claude Opus 4.5（`claude-opus-4-5-20251101`） | `code_execution_20260120` |

---

## 2026-02-28 更新 —— web_search 内置 PTC + LMArena 结果

> 来源：[Lance Martin — Claude Advanced Tool Use (Feb 28)](https://www.linkedin.com/posts/lance-martin-_advanced-tool-use-activity-7300910066866597888-...)

### web_search 内置 PTC（web_search_20260209）

`web_search_20260209` 工具已将 PTC 内置为默认行为：Claude 自动编写 filtering 代码在结果进入 context 前提取相关内容，**无需手动配置 `allowed_callers`**。

```python
# 只需传入更新版工具类型，PTC filtering 自动生效
tools = [
    {"type": "web_search_20260209", "name": "web_search"},
]
headers = {"anthropic-beta": "code-execution-web-tools-2026-02-09"}
```

原有限制中「与标准版网页搜索不兼容」的说法已过时：`web_search_20260209` 和 `web_fetch_20260209` **与 PTC 完全兼容**，是推荐的搭配方案。

### Composition Tax（工具组合税）

每次工具调用都附带一个隐性"税"：

| 组成部分 | 说明 |
|---|---|
| **Latency** | 一次工具调用 = 一次 round-trip 等待 |
| **Serialization** | 输入 / 输出的 JSON 序列化开销 |
| **Reasoning step** | Claude 每次调用前必须思考"是否调用、传什么参数" |

当工具调用链条变长时，这三部分开销累积显著。PTC 通过将多个调用打包进一个 Python 脚本，将 N 个 reasoning step 压缩为 1 个，降低 composition tax。

### LMArena Search Arena #1

Opus 4.6 + PTC（包含内置 `web_search_20260209`）在 LMArena Search Arena 榜单排名**第一**，超过所有竞争方案。

| 配置 | LMArena Search Arena |
|---|---|
| Opus 4.6 + PTC + web_search_20260209 | **#1** |
| 其他竞争方案 | 第二名及以下 |
