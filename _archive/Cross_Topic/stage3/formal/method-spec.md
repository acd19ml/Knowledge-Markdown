# Stage 3 Method Spec

> **Status**: Final v1.0
> **Role**: Stage 3 的唯一正式方法规格页
> **Source Drafts**: [method-brief.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/design/method-brief.md), [memory-unit-schema.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/design/memory-unit-schema.md), [method-figure.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/design/method-figure.md)

---

## 1. Method Name

> **Experience-Delta Procedural Memory (EDPM)**

EDPM 的目标不是存整段任务，也不是存一般性 GUI 建议，而是把交互中暴露出的、对后续决策真正有判别价值的局部经验压成可检索、可修订的 procedural rule。

---

## 2. Core Object

### Formal Object

每条 EDPM unit 至少包含：

- `intent_slice`
- `trigger_context`
- `procedure`
- `constraints`
- `failure_signals`
- `scope`
- `evidence_refs`
- `revision_policy`

### Unit Boundary

EDPM unit 必须满足：

- 比原子动作更高
- 比 whole-task workflow 更低
- 能被单独命中
- 能被单独修订

合格例子：

- “在 settings/profile 架构下，如果一级导航缺目标入口，优先检查 overflow / secondary menu”
- “表单提交无报错但页面状态不变时，先检查隐藏 prerequisite，而不是重复点击 submit”

---

## 3. Module Specification

### Module 1. Experience Candidate Mining

输入：完整轨迹与 outcome。

保留：

- 首次不稳定但后来成功的局部片段
- 暴露隐藏前提的失败片段
- 决定 outcome 的局部分叉步骤
- 跨任务重复出现的 interaction motif

过滤：

- base model 已稳定掌握的 GUI 常识
- 纯机械重复步骤
- 无法归因的噪声片段

### Module 2. Procedural Rule Abstraction

把候选片段压成局部 rule，而不是整段 workflow。

抽象原则：

- 保留 trigger 与 failure cue
- 只抽象到局部可迁移粒度
- 必须可追溯回 evidence

### Module 3. Retrieval and Application

`retrieval` 与 `application` 分离：

- retrieval 负责找对 rule
- application 负责让 rule 真正改变决策

最小实现分两级：

- `v0`: context injection
- `v1`: policy constraint / reranking

### Module 4. Failure-Driven Write-Back

write-back 默认在 episode 结束后触发。

允许的最小操作：

- `edit`
- `downweight`
- `split`
- `rewrite`

Stage 3 v0 只要求先实现：

- `edit`
- `downweight`

---

## 4. Data and Store Policy

### Store States

- `candidate`
- `active`
- `superseded`
- `deprecated`

### Minimal Promotion Rules

- `candidate -> active`
  - 至少 `2` 条支持 evidence，或 `1 success + 1 failure contrast`
- `active -> superseded`
  - 被 `split` 或 `rewrite` 替代
- `active -> deprecated`
  - 连续失败且无法通过 `edit` 修复

### Retrieval Rule

采用两阶段命中：

1. `semantic_summary + intent_slice` 做粗检索
2. `constraints / scope / page_type_key` 做后过滤

---

## 5. Non-Goals

当前方法明确不把以下对象当作主方法对象：

- raw trajectory archive
- whole-task workflow cache
- executable API skill library
- semantic note memory
- user profile / persona memory

这些可以作为辅助层或对照组，但不应占据主 object。

---

## 6. What Is Actually New Here

EDPM 的方法主张不是单点创新，而是三个设计选择的组合：

1. **对象收缩**：从 workflow / skill / note 收缩到 local procedural rule
2. **模块分离**：把 retrieval 和 application 分开
3. **failure-aware revision**：让 failure 直接决定 memory 更新，而不是只累计 success cases

如果这三点里任一点没有被实验支持，就必须收缩方法主张。

---

## 7. Stage 3 v0 Build Boundary

### Must Build

- EDPM unit schema
- candidate/active/superseded store
- `C0 / C1 / C3 / C4` 四个条件
- post-task write-back
- retrieval/application logging

### Nice To Have But Not Required For Entry

- `C5` policy carrier
- automatic `split / rewrite`
- Android-native extension
- larger benchmark coverage beyond WebArena pilot

---

## 8. One-Sentence Method Claim

> EDPM 不是 workflow cache、API skill library 或 semantic note memory，而是一层以局部 procedural rule 为核心、以 retrieval/application separation 为执行接口、以 failure-aware write-back 为修订机制的 GUI experience layer。
