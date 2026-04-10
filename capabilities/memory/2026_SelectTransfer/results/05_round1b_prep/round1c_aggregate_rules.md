# Round 1c Aggregate Rules

Date: 2026-04-11

这份文件定义 `Round 1c` 的 **case selection** 和 **aggregate reporting rules**。

对应子集：

- [round1c_role_aware_smoke_subset.csv](./round1c_role_aware_smoke_subset.csv)
- [round1c_role_aware_smoke_table.csv](./round1c_role_aware_smoke_table.csv)

---

## 1. 核心原则

从 `Round 1c` 开始，当前 6 个 smoke cases **不再被当作一个统一 benchmark**。

这意味着：

- 不再报告一个混合的 overall `EM / F1`
- 不再直接报告 6 个 case 混在一起的 `relevant vs irrelevant` 平均
- 不再把 boundary / ambiguity case 当作 memory effect evidence

相反，所有结果都必须按 `subset_bucket` 分开汇报。

---

## 2. Role-Aware Subset

当前 `Round 1c` 的 smoke subset 被固定为三类可解释角色，加上一类边界保留组。

### 2.1 Process Sanity

用途：

- 观察模型是否显式 `use / reject` memory
- 观察 `verbalized use` 是否等于 outcome dependence

包含：

- `wiki_dev_8896`
- `wiki_dev_10727`

允许汇报：

- `memory_reference_type`
- `explicit_use / explicit_reject`
- `reasoning_present / final_answer_present`
- `answer_changed_vs_baseline`

不允许汇报：

- “memory improved accuracy on process sanity set”

因为这两个 case 都是 ceiling / no-movement cases。

### 2.2 Artifact-Sensitive Diagnosis

用途：

- 观察 current artifact 是否把 baseline 拉坏
- 判断问题更像来自 pairing 过粗，还是 artifact wording 干扰

包含：

- `wiki_dev_2639`

允许汇报：

- `outcome_changed_vs_baseline`
- `degraded_vs_baseline`
- `memory_reference_type`
- 结合 raw output 的 refusal / derailment 描述

不允许汇报：

- “irrelevant memory better than relevant memory” 作为 general claim

因为这里只能支撑：

- 当前 relevant bridge artifact 在 relation-chain case 上可能不适配

### 2.3 Answer-Format Diagnosis

用途：

- 区分 reasoning improvement 和 output compression
- 观察 memory 是否改变答案粒度、答案类型或表述层级

包含：

- `wiki_dev_7019`

允许汇报：

- `answer_changed_vs_baseline`
- `improved_vs_baseline`
- answer granularity 变化说明

不允许汇报：

- “comparison memory transfers to bridge task”

因为当前更可信的解释是 answer-format correction。

### 2.4 Audit / Boundary Only

用途：

- 单独记录 benchmark ambiguity 和 scoring noise

包含：

- `wiki_dev_0092`
- `wiki_dev_6083`

允许汇报：

- `memory_reference_type`
- 作为 audit note 的 case-level 说明

不允许汇报：

- 进入任何 transfer aggregate
- 用于支持或反驳 memory efficacy

---

## 3. Allowed Aggregate Views

`Round 1c` 只允许以下三种 aggregate view：

1. **process summary**
   - 统计 process sanity cases 中：
     - `explicit_use`
     - `explicit_reject`
     - `memory_verbalized`
     - `outcome_changed_vs_baseline`

2. **diagnostic summary**
   - 统计 diagnostic cases 中：
     - `degraded_vs_baseline`
     - `improved_vs_baseline`
     - `answer_changed_vs_baseline`

3. **audit summary**
   - 单独列出 ambiguity / boundary cases
   - 说明它们为何被排除出 aggregate

---

## 4. Forbidden Aggregate Views

当前阶段禁止以下做法：

1. 对这 6 个 case 直接求一个统一 `EM / F1`
2. 对这 6 个 case 直接求统一的 `relevant vs irrelevant` 平均
3. 把 `wiki_dev_0092` 和 `wiki_dev_6083` 纳入任何 memory-effect aggregate
4. 把 `wiki_dev_7019` 的 improvement 直接写成 “transfer gain”
5. 把 `wiki_dev_2639` 的 degradation 直接写成 “relevant memory generally hurts”

---

## 5. Reporting Template

如果 `Round 1c` 要在报告里写成一段，推荐固定成三层：

1. `process sanity`
   - 这轮是否还能看到显式 `use / reject`

2. `diagnostic cases`
   - 当前 observed change 更像 artifact derailment，还是 answer-format correction

3. `audit exclusions`
   - 哪些 case 因 benchmark / scoring 问题被排除

这样写的好处是：

- 不会再把不相容的 case 混成一个平均数
- 每一类现象都有单独的解释语义

---

## 6. One-Line Rule

**从 Round 1c 开始，先按 role 解释，再决定能不能聚合；不能先聚合，再事后解释。**
