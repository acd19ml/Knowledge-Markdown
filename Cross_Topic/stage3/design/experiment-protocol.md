# Stage 3 Experiment Protocol

> **Status**: Supporting draft
> **Role**: 把 Stage 3 主线方法写成可执行实验协议
> **Parent Brief**: [method-brief.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/design/method-brief.md)
> **Schema Spec**: [memory-unit-schema.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/design/memory-unit-schema.md)
> **Pilot Split**: [webarena-task-split.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena-task-split.md)
> **Formal Output**: [evaluation-plan.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/formal/evaluation-plan.md)
> **Note**: 本页保留实验协议细节；最终引用应优先使用正式评测页。

---

## 1. Experimental Goal

本协议不试图证明“memory 普遍有用”，而是专门验证三件事：

- `EDPM rule` 是否优于 raw retrieval 和 coarse workflow memory
- `failure-driven write-back` 是否优于 success-only accumulation
- 学到的内容是否超出 task cache，能够在 repeated-task、same-site cross-task 和 near-domain transfer 中带来经验增益

---

## 2. Benchmark Decision

### 2.1 Primary Benchmark

> **Primary**: `WebArena`

选择理由：

- 与 [2024_AWM.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2024_AWM.md) 和 [2025_SkillWeaver.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2025_SkillWeaver.md) 的 precedent 对齐
- 可控、可重复、便于插桩
- 适合构造 repeated exposure 与 post-task write-back
- same-site cross-task 和 site-family transfer 更容易明确定义

### 2.2 Secondary Benchmark

- `Online-Mind2Web / Mind2Web`
  用于检查从 sandboxed site 到更真实网页任务的迁移

### 2.3 Deferred Benchmark

- `AndroidEnv / AndroidWorld`
  当前不作为 Stage 3 blocker，只保留为 Stage 4 GUI-native 扩展

---

## 3. Evaluation Questions

### EQ1. Repeated Exposure

同一类任务第二次、第三次执行时，agent 是否因为 memory 而变好？

### EQ2. Same-Site Cross-Task Transfer

从任务 A 学到的局部 rule，是否能帮助同站点的相邻任务 B？

### EQ3. Near-Domain Transfer

从站点家族 A 学到的 rule，是否能部分迁移到结构相近的站点家族 B？

### EQ4. Write-Back Value

failure-driven write-back 是否优于 success-only accumulation？

---

## 4. Core Experimental Conditions

| Condition | Description | What it tests |
|---|---|---|
| `C0: No Memory` | 标准 agent，无外部记忆 | 基线能力 |
| `C1: Raw Retrieval` | 检索历史轨迹片段直接注入 | 任何经验上下文是否就足够 |
| `C2: Coarse Workflow Memory` | 存 workflow snippet 或 plan memo | workflow cache 是否已足够 |
| `C3: EDPM Success-Only` | 仅从成功轨迹抽规则 | rule 表示是否有效 |
| `C4: EDPM Failure-Aware` | 成功+失败都参与 write-back | failure write-back 的净贡献 |
| `C5: EDPM + Policy Constraint` | 在 C4 基础上增加 constraint/reranking | carrier 分离是否有效 |

最小主比较：

- `C3` vs `C1/C2`
- `C4` vs `C3`
- `C5` vs `C4`

---

## 5. Task Construction

### 5.1 Level 1: Repeated-Task Reuse

构造方式：

- 同一任务目标
- 不同随机种子或轻微页面扰动
- agent 可在多轮尝试间写回 memory

目标：

- 验证“第一次不会，第二次会”

### 5.2 Level 2: Same-Site Cross-Task Reuse

构造方式：

- 同一站点
- 不同任务
- 共享部分 interaction motif

示例：

- 同站点内多个 settings/location/navigation tasks
- 同站点内多个 form-completion / recovery tasks

目标：

- 验证 memory 不是 literal task replay

### 5.3 Level 3: Near-Domain Site-Family Transfer

构造方式：

- 不同站点
- 相同 site family 或 interaction archetype

示例：

- forum-like sites
- ecommerce-like sites
- settings-heavy SaaS sites

目标：

- 验证 memory 不是 site-specific cache

---

## 6. Split Policy

推荐把任务按 interaction pattern，而不是只按 benchmark 原始 domain 来切。

### 6.1 Development Split

- 用于调 schema、retrieval、write-back
- 不报告最终数字

### 6.2 Main Evaluation Split

- repeated-task set
- same-site cross-task set
- near-domain transfer set

### 6.3 Holdout Principle

同一条具体 workflow 不应同时出现在 memory construction 和 final test 中，避免把 workflow cache 误报为 rule transfer。

---

## 7. Episode Protocol

每次任务执行按以下顺序：

1. 初始化 agent 与当前 memory store
2. 执行任务并记录完整轨迹
3. 判断任务 outcome 与关键 failure point
4. 触发 post-task abstraction
5. 对 store 执行 `add / edit / downweight / split / rewrite`
6. 在下一轮或下一任务中允许 retrieval/application

关键约束：

- 不允许在单轮中无限自修复，避免把 runtime trial-and-error 和 post-task write-back 混淆
- write-back 默认发生在 episode 结束后

---

## 8. Metrics

### 8.1 Outcome Metrics

- success rate
- normalized step count
- task completion latency

### 8.2 Learning Metrics

- repeated-exposure gain
- cross-task transfer gain
- near-domain transfer gain

### 8.3 Memory Metrics

- retrieval precision
  - 被取出的 rule 中有多少真正适用
- retrieval coverage
  - 需要经验的任务中，有多少命中过正确 rule
- write-back utility
  - 更新后的 rule 是否带来后续成功率提升
- rule survival quality
  - 有多少 rule 在多轮后仍保持有效
- false-memory rate
  - 被错误触发或误导决策的 rule 比例

### 8.4 Failure Metrics

- failure recovery rate after write-back
- repeated failure suppression
  - 同类错误在后续任务中是否减少
- revision success rate
  - `edit / downweight / split / rewrite` 后是否真的改善

---

## 9. Required Ablations

### A1. Representation Ablation

- `EDPM rule` vs `workflow snippet` vs `raw trajectory`

### A2. Failure Signal Ablation

- 有 `failure_signals`
- 无 `failure_signals`

### A3. Write-Back Ablation

- success-only
- failure-aware

### A4. Carrier Ablation

- context injection only
- policy constraint / reranking

---

## 10. Success Criteria

Stage 3 pilot 的正式判定以 [rq-decision-matrix.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/readiness/rq-decision-matrix.md) 为准。最小支持条件压缩为：

- `H1`: `C3` 在 `L2` 上分别比 `C1` 和 `C2` 高 `>= 8` 个 success-rate 绝对点
- `H3`: `C4` 在 failure-first episodes 上比 `C3` 高 `>= 10` 个 failure-recovery 绝对点
- `RQ non-cache guardrail`: `L2` 相对 `C0` 仍保持 `>= 5` 个绝对点正增益，且 `L3` 总体不为负

更强支持版本：

- `H2`: `C5` 相对 `C4` 将 false-memory rate 降低 `>= 10` 个绝对点，且 success rate 不低于 `C4 - 2`
- `L3` 至少 `2/4` 个 families 保持非负 transfer gain

### Failure Conditions

若出现以下任一情况，需要收缩主张：

- 只在 repeated-task 有增益
- `C4` 不优于 `C3`
- `EDPM rule` 不优于 workflow memory
- 任何仍带未解决 leakage 风险的 family 被直接拿去做 transfer claim

这意味着当前实现更像 task cache 或 success-case store，而非可修订 procedural memory。

---

## 11. Logging Requirements

每次实验至少保存：

- full trajectory
- task outcome
- failure type
- retrieved memory ids
- applied carrier type
- write-back operation
- pre-update vs post-update rule snapshot

没有这些日志，后面无法解释“为什么 memory 有用或无用”。

---

## 12. Minimal Execution Plan

### Phase 0

- 手工标注 20-30 个高价值 interaction motifs
- 验证 schema 是否够用

### Phase 1

- 在 WebArena 上跑 `C0-C4`
- 只做 repeated-task + same-site cross-task

### Phase 2

- 引入 `C5`
- 扩到 near-domain site-family transfer

### Phase 3

- 用 Mind2Web / Online-Mind2Web 做外部迁移检查

---

## 13. Immediate Next Steps

1. 选 2 个 WebArena site family，写出 repeated-task 与 same-site transfer 任务池。
2. 为每个任务定义“需要经验差分知识”的关键 interaction motif。
3. 先实现 `C0 / C1 / C3 / C4` 四个条件。
4. 先测 repeated-task learning curve，再扩 cross-task transfer。
