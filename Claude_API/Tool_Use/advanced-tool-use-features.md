# Claude Advanced Tool Use Features (GA — 2026-02-18)

> Applies to: Claude Opus 4.6 / Sonnet 4.6 / Sonnet 4.5 / Opus 4.5
> Available via: Claude API & Microsoft Foundry (NOT Bedrock / Vertex AI)

**Sources**
- [Anthropic Engineering Blog — Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use)
- [Official Docs — Programmatic Tool Calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)
- [Community Report — Claude Advanced Tool Use Patterns](https://github.com/shanraisshan/claude-code-best-practice/blob/main/reports/claude-advanced-tool-use.md)

---

## Overview

Four GA features that optimize token consumption and reduce latency for multi-tool workflows:

| Feature | Problem Solved | Impact | Status |
|---|---|---|---|
| Programmatic Tool Calling (PTC) | Multi-round-trip context pollution | ~37% fewer tokens | GA |
| Tool Search Tool | Too many tool definitions loaded upfront | ~85% fewer token on definitions | GA |
| Tool Use Examples | Schema can't express usage patterns | 72% → 90% accuracy | GA |
| Dynamic Filtering (Web Search/Fetch) | Raw HTML bloats context | ~24% fewer input tokens | GA |

---

## 1. Programmatic Tool Calling (PTC)

### Core Idea

**Traditional:** Each tool call = 1 model inference pass. All intermediate results enter the context window.

```
3 tools → 3 inference passes → all responses pollute context → HIGH token cost
```

**PTC:** Claude writes a Python script that orchestrates all tools inside a sandbox. Only `stdout` (the final summary) enters the context window.

```
3 tools → 1 inference pass → only final output enters context → ~37% LOWER token cost
```

**Real-world example:** Budget compliance across 20 employees.
- Traditional: 20+ tool calls, 2,000+ expense items enter context.
- PTC: One script runs 20 lookups, filters results, returns only the 2–3 people who exceeded budget.

### Benchmark Results

| Benchmark | Before | After |
|---|---|---|
| Token usage | 43,588 | 27,297 (−37%) |
| BrowseComp (Sonnet 4.6) | 33.3% | 46.6% |
| BrowseComp (Opus 4.6) | 45.3% | 61.6% |
| DeepSearchQA F1 (Sonnet 4.6) | 52.6% | 59.4% |
| DeepSearchQA F1 (Opus 4.6) | 69.8% | 77.3% |

### How It Works

1. Claude writes Python code calling your tool as `await tool_name(args)`.
2. Code runs in a sandboxed container via the code execution tool.
3. API pauses, returns a `tool_use` block — you provide the result.
4. Code execution resumes; intermediate results **never** enter Claude's context.
5. Only the final `stdout` is returned to Claude.

### Setup — Key Fields

**Tool definition** — mark a tool as programmatically callable:

```json
{
  "name": "query_database",
  "description": "Execute SQL. Returns list of rows as JSON objects.",
  "input_schema": { ... },
  "allowed_callers": ["code_execution_20260120"]
}
```

`allowed_callers` values:
- `["direct"]` — only Claude calls it directly (default)
- `["code_execution_20260120"]` — only callable from within code execution
- `["direct", "code_execution_20260120"]` — both (avoid: give Claude clear guidance)

**Request must also include the code execution tool:**

```json
{ "type": "code_execution_20260120", "name": "code_execution" }
```

**Response includes a `caller` field:**

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

**Container lifecycle:**
- New container per session unless you pass a `container` ID to reuse.
- Expires after ~4.5 minutes of inactivity. Monitor `expires_at`.
- If container expires while waiting for your tool result, Claude retries.

### Advanced Patterns

**Batch processing (N items = 1 inference pass):**
```python
regions = ["West", "East", "Central", "North", "South"]
results = {}
for region in regions:
    data = await query_database(f"SELECT * FROM sales WHERE region='{region}'")
    results[region] = sum(row["revenue"] for row in data)
top = max(results.items(), key=lambda x: x[1])
print(f"Top region: {top[0]} — ${top[1]:,}")
```

**Early termination:**
```python
for endpoint in ["us-east", "eu-west", "apac"]:
    if await check_health(endpoint) == "healthy":
        print(f"Healthy: {endpoint}")
        break
```

**Conditional tool selection:**
```python
info = await get_file_info(path)
content = await read_full_file(path) if info["size"] < 10000 else await read_file_summary(path)
print(content)
```

**Data filtering:**
```python
logs = await fetch_logs(server_id)
errors = [l for l in logs if "ERROR" in l]
print(f"{len(errors)} errors\n" + "\n".join(errors[-10:]))
```

### Constraints

- Requires code execution tool to be enabled.
- NOT available on Bedrock or Vertex AI.
- Incompatible with: MCP tools, web search/fetch (standard), `strict: true` structured outputs, forced `tool_choice`.
- `disable_parallel_tool_use: true` not supported.
- When responding to programmatic tool calls: message must contain **only** `tool_result` blocks (no text).
- Container lifetime ~4.5 minutes.

### When to Use

**Good:** Large datasets needing aggregation, 3+ dependent tool calls, filtering/sorting before reasoning, parallel operations across many items.
**Skip:** Single tool call with simple response, very fast operations where container overhead outweighs benefit.

---

## 2. Tool Search Tool

### Problem

Loading 50 MCP tools at ~1.5K tokens each = 75K tokens consumed before the user asks anything. A five-server setup with 58 tools used ~55K tokens; internal setups reached 134K tokens.

### Solution

Mark infrequently-used tools with `defer_loading: true`. Claude discovers them on-demand via regex or BM25 search — a "Tool Search Tool" provided automatically.

### Configuration

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

### Results

| Setup | Before | After |
|---|---|---|
| Token reduction | 72K tokens | 8.7K tokens (−85%) |
| Opus 4 accuracy | 49% | 74% |
| Opus 4.5 accuracy | 79.5% | 88.1% |

### Claude Code Integration

Auto-mode enabled by default since v2.1.7. Defers MCP tools when their descriptions exceed 10% of context. Configure with: `ENABLE_TOOL_SEARCH=auto:N`.

### Best Practices

- Keep 3–5 most-used tools always loaded (`defer_loading: false`).
- Use clear, descriptive tool names for better search discovery.

---

## 3. Tool Use Examples

### Problem

JSON Schema defines structure but cannot express:
- When to include optional parameters
- Valid parameter combinations
- Format conventions
- Nested structure usage

### Solution

Add `input_examples` arrays to tool definitions with concrete usage samples:

```json
{
  "name": "query_database",
  "description": "Execute SQL query...",
  "input_schema": { ... },
  "input_examples": [
    { "sql": "SELECT * FROM sales WHERE region='West' AND year=2025" },
    { "sql": "SELECT customer_id, SUM(revenue) FROM orders GROUP BY customer_id LIMIT 10" }
  ]
}
```

### Results

Tool parameter accuracy: **72% → 90%** on complex parameter handling.

---

## 4. Dynamic Filtering for Web Search / Fetch

### Problem

Web tools return full HTML pages with navigation, ads, and boilerplate — wasting tokens and reducing accuracy.

### Solution

Claude writes filtering code that extracts relevant content before results enter context. Uses updated tool types:

- `web_search_20260209`
- `web_fetch_20260209`

Required header: `anthropic-beta: code-execution-web-tools-2026-02-09`

### Results

| Metric | Before | After |
|---|---|---|
| Input tokens | baseline | −24% |
| BrowseComp (Sonnet 4.6) | 33.3% | 46.6% |
| BrowseComp (Opus 4.6) | 45.3% | 61.6% |
| DeepSearchQA F1 (Sonnet 4.6) | 52.6% | 59.4% |
| DeepSearchQA F1 (Opus 4.6) | 69.8% | 77.3% |

---

## Strategic Implementation Guide

Choose features based on your biggest bottleneck:

| Bottleneck | Solution |
|---|---|
| Context bloat from too many tool definitions | Tool Search Tool (`defer_loading`) |
| Large intermediate tool results | Programmatic Tool Calling |
| Web search noise / irrelevant HTML | Dynamic Filtering |
| Wrong parameters / bad tool invocations | Tool Use Examples |

Stack features for compounding gains — all four are compatible with each other (where individual constraints allow).

---

## Model Compatibility

| Model | PTC Tool Version |
|---|---|
| Claude Opus 4.6 (`claude-opus-4-6`) | `code_execution_20260120` |
| Claude Sonnet 4.6 (`claude-sonnet-4-6`) | `code_execution_20260120` |
| Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`) | `code_execution_20260120` |
| Claude Opus 4.5 (`claude-opus-4-5-20251101`) | `code_execution_20260120` |
