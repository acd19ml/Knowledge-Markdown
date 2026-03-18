# Stage 3 Memory Unit Schema

> **Status**: Draft v0.1
> **Role**: 把 `experience-delta procedural memory` 从概念对象压成可实现的数据结构
> **Parent Brief**: [method-brief.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/design/method-brief.md)

---

## 1. Design Goal

当前 memory unit 不是用来存整段 workflow，也不是用来存模糊经验提示，而是用来存一条**局部、可检索、可修订、可判定何时失效的 procedural rule**。

它必须同时满足四个条件：

- **GUI-grounded**: 不能脱离页面状态、视觉线索或结构线索
- **cross-task reusable**: 不能只是某一次任务的完整回放
- **failure-aware**: 必须显式表示失效信号
- **rewrite-friendly**: 必须支持 `edit / split / downweight / rewrite`

---

## 2. Unit Definition

> **EDPM unit** = 一条从 post-task 经验中抽象出来的局部 procedural rule，它描述“在什么条件下，面对什么局部目标，优先采用什么策略；什么现象说明这条策略失效；失败后应如何修改这条记忆”。

推荐把 unit 粒度控制在：

- 比原子动作更高
- 比 whole-task workflow 更低
- 能独立被 retrieval 命中
- 能被单独改写而不污染整个 memory store

合适的例子：

- “在 profile/settings 型页面中，如果顶部一级导航找不到目标项，优先检查 overflow / secondary menu”
- “表单提交失败且按钮未灰化时，优先检查隐藏 prerequisite field，而不是重复点击 submit”

不合适的例子：

- “先点 A，再点 B，再点 C，最后提交”
- “设置页面通常很复杂”

---

## 3. Canonical Schema

| Field | Type | Required | Purpose |
|---|---|---:|---|
| `memory_id` | string | Yes | 唯一标识 |
| `status` | enum | Yes | `candidate / active / deprecated / superseded` |
| `intent_slice` | string | Yes | 这条规则服务的局部目标 |
| `trigger_context` | object | Yes | 触发条件 |
| `procedure` | list[string] | Yes | 推荐策略 |
| `constraints` | list[string] | Yes | 成立前提 |
| `expected_effect` | string | Yes | 预期会带来什么局部结果 |
| `failure_signals` | list[string] | Yes | 什么现象说明规则可能失效 |
| `scope` | object | Yes | 适用边界 |
| `evidence_refs` | list[object] | Yes | 来自哪些成功/失败片段 |
| `retrieval_keys` | object | Yes | 检索用摘要和结构键 |
| `confidence` | float | Yes | 当前可信度 |
| `support_count` | int | Yes | 支持该规则的正例数 |
| `failure_count` | int | Yes | 触发失败的反例数 |
| `revision_policy` | object | Yes | 失败后优先采用哪种更新操作 |
| `revision_history` | list[object] | Yes | 历史改写记录 |
| `created_at` | string | Yes | 首次生成时间 |
| `updated_at` | string | Yes | 最近更新时间 |

---

## 4. Field Semantics

### 4.1 `intent_slice`

只描述局部任务意图，不描述整个任务。

推荐形式：

- `find hidden settings entry`
- `recover from silent form submission failure`
- `re-ground after modal closes and focus resets`

### 4.2 `trigger_context`

`trigger_context` 至少包含四层线索：

- **task cue**: 用户当前局部意图
- **page cue**: 当前页面类型、结构模式、站点/app 名称
- **visual cue**: 视觉线索，如 overflow icon、disabled field、toast disappearance
- **state cue**: 任务状态或前一步操作结果

推荐子字段：

| Subfield | Type | Purpose |
|---|---|---|
| `platform_family` | string | web / android / desktop |
| `app_or_site` | string | 具体 app/site 名 |
| `page_type` | string | settings / search / checkout / form |
| `ui_cues` | list[string] | 可见结构或控件提示 |
| `state_cues` | list[string] | 执行前后状态提示 |
| `task_cues` | list[string] | 语义触发条件 |

### 4.3 `procedure`

必须是**局部策略**，不是动作日志。推荐 2-5 步。

例如：

1. 检查顶部显式导航是否存在目标入口
2. 若无，则优先查看 overflow / kebab / profile submenu
3. 进入二级菜单后重新 grounding，而不是沿用旧目标框

### 4.4 `constraints`

显式记录这条规则何时才成立。

例如：

- 页面属于 settings/profile/info architecture
- 当前任务目标不是 free-form search，而是 feature location
- 页面尚未进入 modal-only state

### 4.5 `failure_signals`

这是当前 schema 的关键字段，不能省略。

例如：

- overflow 展开后仍无相关入口
- repeated click on submit yields identical page state
- focus reset caused target element grounding mismatch

### 4.6 `scope`

推荐最小结构：

| Subfield | Example |
|---|---|
| `reuse_level` | `repeated_task / same_site_cross_task / near_domain_family` |
| `site_family` | `ecommerce`, `forum`, `settings-heavy SaaS` |
| `exclusions` | 不适用于 wizard-style forms |

---

## 5. Retrieval Representation

同一条 memory unit 应同时支持：

- **dense retrieval**
- **structured filtering**

因此 `retrieval_keys` 推荐拆成两层：

| Key | Purpose |
|---|---|
| `semantic_summary` | 用于 embedding 检索 |
| `intent_key` | 局部目标过滤 |
| `page_type_key` | 页面类型过滤 |
| `platform_key` | 平台过滤 |
| `failure_mode_key` | 失败类型过滤 |

### Retrieval Rule

推荐先走两阶段：

1. 用 `intent_slice + trigger_context.semantic_summary` 做粗检索
2. 用 `constraints / scope / page_type_key` 做后过滤

这可以降低“检索到相似但不适用规则”的误用率。

---

## 6. Write-Back Operations

### 6.1 `edit`

适用情形：

- 规则总体正确
- 只是触发条件、约束或 procedure 描述不完整

典型例子：

- 给规则补一条 prerequisite field 条件

### 6.2 `split`

适用情形：

- 一条规则被用于两个外观相似但机制不同的页面

典型例子：

- “settings page hidden entry” 实际混合了 profile menu 和 kebab menu 两种情况

### 6.3 `downweight`

适用情形：

- 规则偶尔仍有效
- 但适用范围被高估

典型例子：

- 某条 overflow heuristic 只在部分站点家族有效

### 6.4 `rewrite`

适用情形：

- 原策略结构性失效
- 失败不是边界条件，而是主 procedure 已错

典型例子：

- 目标入口从 navigation path 迁移成 search-first interaction

---

## 7. Minimal JSON-Like Template

```json
{
  "memory_id": "edpm_00017",
  "status": "active",
  "intent_slice": "find hidden settings entry",
  "trigger_context": {
    "platform_family": "web",
    "app_or_site": "reddit",
    "page_type": "settings",
    "ui_cues": ["top-level navigation lacks target option", "overflow menu visible"],
    "state_cues": ["user already entered settings area"],
    "task_cues": ["need to locate account or preference option"]
  },
  "procedure": [
    "Check visible navigation first",
    "If target option is absent, inspect overflow or profile submenu",
    "After expansion, re-ground candidate options before clicking"
  ],
  "constraints": [
    "page belongs to settings-like information architecture",
    "task is feature location rather than free-form search"
  ],
  "expected_effect": "recover hidden navigation path without blind page wandering",
  "failure_signals": [
    "expanded secondary menu still lacks target option",
    "same navigation branch repeats with no new candidates"
  ],
  "scope": {
    "reuse_level": "same_site_cross_task",
    "site_family": "settings-heavy community sites",
    "exclusions": ["wizard-style flows", "search-first dashboards"]
  },
  "evidence_refs": [
    {"trajectory_id": "traj_223", "step_span": "9-14", "outcome": "success"},
    {"trajectory_id": "traj_241", "step_span": "7-10", "outcome": "failure"}
  ],
  "retrieval_keys": {
    "semantic_summary": "When a settings-like page hides a target option, check overflow or profile submenu before random navigation.",
    "intent_key": "hidden_settings_entry",
    "page_type_key": "settings",
    "platform_key": "web",
    "failure_mode_key": "missing_visible_option"
  },
  "confidence": 0.72,
  "support_count": 3,
  "failure_count": 1,
  "revision_policy": {
    "default_action": "edit",
    "escalate_to_split_if": "same rule fails under two distinct menu structures"
  },
  "revision_history": [],
  "created_at": "2026-03-08",
  "updated_at": "2026-03-08"
}
```

---

## 8. Store-Level Rules

memory store 至少要满足：

- 同一条 rule 可追溯到原始 evidence
- 同一 failure 不会无限追加重复 rule
- 被 `rewrite` 或 `split` 的旧条目不会直接删除，而是变 `superseded`
- retrieval 默认只命中 `active`

推荐的 store policy：

- `candidate -> active`
  条件：至少 2 条支持 evidence 或 1 成功 + 1 有效 failure contrast
- `active -> deprecated`
  条件：连续失败且无法通过 edit 修复
- `active -> superseded`
  条件：被 split 或 rewrite 替代

---

## 9. Concrete Acceptance Tests

一条 EDPM unit 要进入实验系统，至少应通过以下检查：

- **Specificity**: 是否描述了局部意图，而不是整个任务
- **Grounding**: 是否包含页面/视觉/状态线索
- **Actionability**: 是否给出可执行 procedure
- **Falsifiability**: 是否定义 failure signal
- **Rewriteability**: 是否能明确选择 `edit / split / downweight / rewrite`

任一项不通过，不应入库。

---

## 10. Immediate Build Order

1. 先实现 `candidate / active / superseded` 三态 store。
2. 先支持 `edit` 和 `downweight`，不急着做 `split / rewrite` 自动化。
3. 先做 web/site schema，后扩到 Android。
4. 先用 20-50 条高质量 unit 验证 retrieval/application，再扩 store 规模。
