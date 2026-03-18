# Stage 3 Problem Statement

> **Status**: Final v1.0
> **Role**: Stage 3 的唯一正式问题陈述页
> **Source Drafts**: [method-brief.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/design/method-brief.md), [rq-proof-sheet.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/readiness/rq-proof-sheet.md), [rq-decision-matrix.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/readiness/rq-decision-matrix.md)

---

## 1. Final Research Question

> **RQ**: LLM-based GUI agents 如何把交互中获得、且超出基础模型先验的 `experience-dependent procedural knowledge` 表示成可检索、可修订、可跨任务复用的 memory，并通过 `post-task -> cross-task` 的 failure-aware write-back，使其在 repeated-task、same-site or same-app cross-task 与 near-domain site-family or app-family transfer 中稳定带来经验增益？

这不是一个泛化的 “memory 是否有用” 问题，而是一个更窄的设计问题：

- memory **应存什么**
- memory **如何影响下一次决策**
- failure **如何进入 memory revision**
- 增益 **如何被证明不是 task replay**

---

## 2. Scope of the Question

### In Scope

- `experience-dependent procedural knowledge`
- post-task consolidation，而不是无限在线自修复
- repeated-task、same-site or same-app cross-task、near-domain site-family or app-family transfer 三层复用
- retrieval、application、write-back 三个可分离模块

### Out of Scope

- generic GUI prior 是否存在
- 单纯的 long-context prompt engineering
- 训练期参数更新路线
- user profile / persona memory
- full episodic archive 作为主 memory object

---

## 3. Why This RQ Is Worth Pursuing

当前最近邻工作已经分别证明了以下几点：

- GUI memory 可以提升 warm-start reuse
- workflow abstraction 比 raw trajectory retrieval 更强
- executable skills 需要 selection / governance
- memory 不一定只能 append

但仍没有工作正面回答下面这个更窄的问题：

> 在 GUI 场景中，什么样的局部经验单元既足够 grounded，又足够可迁移；并且当它失败时，系统应如何修订它，而不是只是继续堆成功案例？

这就是当前 Stage 3 要锁定的空白。

---

## 4. Main Claims To Be Tested

### Claim A. Memory Unit Claim

真正值得存的对象不是 raw trajectory、whole workflow 或 API library，而是更小的 `experience-delta procedural rule`。

### Claim B. Application Claim

把 retrieval 和 application 分开设计，比“检索后直接塞进上下文”更稳。

### Claim C. Write-Back Claim

failure-aware write-back 比 success-only accumulation 更接近真正的经验演化。

### Claim D. Non-Cache Claim

如果方法成立，增益不应只出现在 `L1 repeated task`，而应至少扩展到 `L2 same-site or same-app cross-task`。

---

## 5. Operational Testability

这份 RQ 不以模糊措辞判定，而以 [rq-decision-matrix.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/readiness/rq-decision-matrix.md) 的硬规则判定。

最关键的 go/no-go 约束是：

- `H1`: `C3` 在 `L2` 上必须分别优于 `C1` 和 `C2`
- `H3`: `C4` 在 failure-first episodes 上必须优于 `C3`
- `Non-cache guardrail`: `L2` 必须保持正增益，`L3` 总体不能为负

在 WebArena formal pilot 中，上述 `same-app / app-family` 边界由 `same-site / site-family` 具体实例化。

若只在 `L1` 有提升，则本 RQ 只得到 `Borderline` 甚至 `Fail`，因为那更像 task cache，而不是可迁移经验。

---

## 6. Hypotheses

| ID | Hypothesis | What would support it | What would weaken it |
|---|---|---|---|
| `H1` | `EDPM rule` 优于 raw retrieval 与 coarse workflow memory | `C3 > C1/C2` on `L2` | `C3` 只在 `L1` 有优势，或 `C3 <= C2` |
| `H2` | retrieval/application separation 降低误用 | `C5` 降低 false-memory rate，且不损失成功率 | `C5` 只是更复杂，但没有净收益 |
| `H3` | failure-aware write-back 带来 post-failure gain | `C4 > C3` on recovery metrics | failure 进入写回后仍无净收益 |

---

## 7. Stage 3 Exit Judgment

只要下面四件事同时成立，Stage 3 就算完成：

1. Final RQ 已固定，不再切换问题对象。
2. 主 memory object 已固定，不再在 workflow / API skill / note memory 之间摇摆。
3. 最近邻差异已固定，能明确说明“为什么不是它们”。
4. 实验判定规则已固定，后续方法实现只能在这套规则下接受或被否。

---

## 8. One-Sentence Version

> 本课题要回答的不是 “GUI agent 需不需要 memory”，而是 “GUI agent 应该把什么样的局部经验写成可修订 procedural memory，并在 failure-aware write-back 下证明它带来的增益不是任务缓存，而是可迁移经验”。
