# Stage 3 RQ Proof Sheet

> **Status**: Supporting draft
> **Purpose**: 证明当前 Final RQ 已通过五项检验，且已有明确实验验证路径
> **Primary Source**: [method-brief.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/design/method-brief.md)
> **Operational Decision Rules**: [rq-decision-matrix.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/readiness/rq-decision-matrix.md)
> **Formal Output**: [problem-statement.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/formal/problem-statement.md)
> **Note**: 本页是证据与推导页，不是最终引用版本。

---

## 1. Final RQ

> LLM-based GUI agents 如何把交互中获得、且超出基础模型先验的 `experience-dependent procedural knowledge` 表示成可检索、可修订、可跨任务复用的 memory，并通过 `post-task -> cross-task` 的 failure-aware write-back，使其在重复任务、同 app / site 跨任务与近邻 app-family / site-family 场景中稳定带来经验增益？

---

## 2. Five-Point Check

| Criterion | What the criterion asks | Current evidence | Judgment |
|---|---|---|---|
| **Specific** | 是否明确限定了对象、方法和评测场景 | 对象已限定为 `experience-dependent procedural knowledge`；方法收束到 `EDPM + failure-aware write-back`；评测限定为 `L1/L2/L3 transfer` | Pass |
| **Answerable** | 是否存在可以回答 RQ 的实验设计 | 已有 baseline package、memory unit、write-back ops、3 层 transfer protocol，见 [experiment-protocol.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/design/experiment-protocol.md) | Pass |
| **Novel** | 现有工作是否已直接回答 | 现有方法分别停在 app graph、workflow memory、API skill library 或 structural planning；尚未正面回答 `GUI local rule + failure-aware revision` | Pass |
| **Feasible** | 是否能在现有资源下验证 | 当前只需 WebArena pilot；24 个真实 task binding 已完成，见 [webarena-task-binding.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena-task-binding.md) | Pass |
| **Impactful** | 回答后是否能推进领域认知 | 若成立，推进的是 “agent memory 应存什么、如何修订、何时产生真实经验增益” | Pass |

---

## 3. Experimental Validation Path

具体的 `comparison -> metric -> falsification` 判定规则，已收成 [rq-decision-matrix.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/readiness/rq-decision-matrix.md)。本页只保留高层结构，不再用“明显优于”这类未操作化措辞单独充当证据。

### 3.1 Core Contrasts

- `no memory` vs `raw trajectory retrieval` vs `coarse workflow memory` vs `EDPM`
- `success-only memory` vs `failure-aware write-back`
- `context injection` vs `policy constraint / reranking`

### 3.2 Core Scenarios

- `L1 repeated task`
- `L2 same-site cross-task`
- `L3 near-domain site-family transfer`

### 3.3 Core Falsification Logic

- 如果增益只出现在 `L1`，说明方法更像 task cache，而不是 transferable rule
- 如果 `failure-aware` 不优于 `success-only`，说明 write-back 设计没有真正起作用
- 如果 `EDPM` 不优于 `coarse workflow memory`，说明记忆单位收缩没有带来方法收益

---

## 4. What Still Needs To Be True

以下事项仍需在后续阶段继续验证，但不阻塞当前 RQ 通过五项检验：

1. 最近邻工作差异表要持续保持清晰，避免 novelty 叙述滑回 “只是更细的 workflow memory”。
2. pilot 结果要至少在 `L2` 上出现稳定正增益，否则当前 RQ 的对象定义需要重审。
3. failure write-back 的实际决策规则还需要实现层验证，但这已经属于方法检验，不再属于 RQ 形式化问题。
