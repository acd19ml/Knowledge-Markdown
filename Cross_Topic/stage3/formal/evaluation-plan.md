# Stage 3 Evaluation Plan

> **Status**: Final v1.0
> **Role**: Stage 3 的唯一正式评测入口页
> **Source Drafts**: [experiment-protocol.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/design/experiment-protocol.md), [rq-decision-matrix.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/readiness/rq-decision-matrix.md), [webarena-task-split.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena-task-split.md), [webarena-task-binding.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena-task-binding.md), [webarena-motif-audit.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena-motif-audit.md)

---

## 1. Benchmark Decision

### Formal Primary Benchmark

> `WebArena`

理由只有两条：

- 它足以回答当前 RQ，不要求先上 Android full-stack
- 它能以最小工程成本支撑 `L1/L2/L3` transfer 与 write-back 检验

### Deferred Benchmarks

- `Mind2Web / Online-Mind2Web`
- `AndroidEnv / AndroidWorld`

它们保留到下一阶段，不阻塞 Stage 3 收口。

---

## 2. Formal Pilot Set

Stage 3 formal pilot 固定为：

- `24` 个正式任务
- `4` 个 families
- 每个 family `L1 x2`, `L2 x2`, `L3 x2`

正式 split 以 [webarena-task-split.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena-task-split.md) 为准。

### Formal Note on TF-4

- `task 453` is part of the formal `L2` set
- `task 774` is `dev-only`

这条边界已经固定，不再回退。

---

## 3. Conditions

| Condition | Meaning | Role |
|---|---|---|
| `C0` | no memory | bare baseline |
| `C1` | raw retrieval | test whether any historical context is enough |
| `C2` | coarse workflow memory | test whether workflow cache is already sufficient |
| `C3` | EDPM success-only | test the rule representation itself |
| `C4` | EDPM failure-aware | test the write-back value |
| `C5` | EDPM + policy constraint | test retrieval/application separation |

### Minimum Stage 3 Build

Stage 3 只要求先实现：

- `C0`
- `C1`
- `C3`
- `C4`

`C2` 和 `C5` 可以稍后补，但 formal judgment 最终仍要回到这五组对照。

---

## 4. Transfer Split

| Level | What it tests | Formal interpretation |
|---|---|---|
| `L1` | repeated-task reuse | memory 是否能避免重复犯同类错误 |
| `L2` | same-site or same-app cross-task reuse | 学到的是不是 local transferable rule，而不是 literal replay |
| `L3` | near-domain site-family or app-family transfer | rule 是否超出单站点 cache |

判断优先级：

1. `L2` 是主战场
2. `L1` 是 sanity check
3. `L3` 是 guardrail，不要求一开始很强，但不能整体为负

在 WebArena formal pilot 中，conceptual 的 `app` 边界由 `site` 边界实例化。

---

## 5. Formal Success Rules

所有 go/no-go 判定都以 [rq-decision-matrix.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/readiness/rq-decision-matrix.md) 为准。

当前最小支持条件固定为：

- `H1`: `C3` 在 `L2` 上分别比 `C1` 与 `C2` 高 `>= 8` 个 success-rate 绝对点
- `H3`: `C4` 在 failure-first episodes 上比 `C3` 高 `>= 10` 个 failure-recovery 绝对点
- `Non-cache guardrail`: `L2` 相对 `C0` 仍保持 `>= 5` 个绝对点正增益，且 `L3` 总体不为负

更强支持条件：

- `H2`: `C5` 相对 `C4` 将 false-memory rate 降低 `>= 10` 个绝对点，且 success rate 不低于 `C4 - 2`

---

## 6. Logging Requirements

每个 episode 至少保存：

- full trajectory
- outcome
- failure type
- retrieved memory ids
- applied carrier type
- write-back operation
- pre-update rule snapshot
- post-update rule snapshot

没有这些日志，不允许宣称 “memory 有效”。

---

## 7. Current Audit Status

formal pilot 的 benchmark 侧结论如下：

- `TF-1` to `TF-4` pass the **minimal** audit for the formal pilot set
- `task 774` is retained only as `dev-only`
- `task 453` has completed a repo-grounded route-level sanity check; live browser walkthrough remains deferred
- generated config route expansion 仍未完成，但它已被明确列为下一阶段 TODO，不再和 formal pilot 绑定混淆

---

## 8. Immediate Execution Order

### Phase 0

- 保留 `task 453` live browser walkthrough 作为下一阶段 sanity upgrade
- 确认 `task 453 / 771 / 391 / 763` 的 motif-hit 细节

### Phase 1

- 实现 `C0 / C1 / C3 / C4`
- 先跑 `TF-2` 与 `TF-4`

选择这两个 family 的原因：

- `TF-2` 最接近 hidden prerequisite 与 failure-aware write-back
- `TF-4` 最接近 post-action re-grounding 与 state-change revision

### Phase 2

- 扩到 `TF-1` 与 `TF-3`
- 补 `C2`

### Phase 3

- 若 `H1/H3` 已初步成立，再补 `C5`

---

## 9. Failure Rules

出现以下任一情况，应停止扩写方法主张并回到 design review：

- 增益只出现在 `L1`
- `C4` 不优于 `C3`
- `C3` 不优于 `C2`
- formal pilot 中再次出现未解决 leakage 风险

---

## 10. One-Sentence Plan

> Stage 3 的正式评测目标不是先做大规模 benchmark，而是用 WebArena formal pilot 证明：EDPM 在 `L2` 上优于 raw retrieval 与 workflow memory，并且 failure-aware write-back 在 post-failure reuse 上带来净收益。
