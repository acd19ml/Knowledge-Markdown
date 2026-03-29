Phase 0. 全局设置

所有实验统一固定：

- model
- agent scaffold
- tools
- decoding params
- max steps
- random seed policy
- API wrapper
- checkpoint format
- concurrency limit

---

Phase 1. 任务 taxonomy

先定义一个小型 reasoning taxonomy：

- `bridge`
- `comparison`
- `temporal`
- `distractor-heavy`

对 source 和 target tasks 都进行标注。

规则：

- 每题只分配一个 dominant reasoning label
- 没有清晰 dominant pattern 的题先丢弃
- taxonomy 在 pairing 之前冻结，不允许边跑实验边改

---

Phase 2. Source experience sets

从 HotpotQA 构造 source memory sets。

每个 source set：

- 固定大小 `N = 5`
- 全部来自同一 reasoning cluster
- set 内部 `entity-disjoint`
- 在可能的情况下保持较低 lexical overlap

目标：

- 每个 set 能代表一种 reasoning pattern
- 但不能退化成几乎重复的题目集合

---

Phase 3. Pairing protocol

在任何 memory experiment 之前，先构造 source-target pairs。

`Relevant Split`

- same reasoning cluster
- `entity-disjoint`
- lexical overlap 低于阈值
- no answer leakage

`Irrelevant Split`

- different reasoning cluster
- `entity-disjoint`
- lexical overlap 低于阈值
- no answer leakage

关键要求：

- pairing rules 必须先固定
- 每个 target task 在 protocol 下绑定固定 source set
- 不能在看到结果后再手工挑“更好看”的 examples

---

Phase 4. Memory 条件

主实验只保留 4 个核心条件：

- `No Memory`
- `Episodic Trace`
- `Cross-Episode Consolidation`
- `Cross-Episode Consolidation + Applicability Judgment`

构造方式：

- `Episodic Trace`
  - 从 paired source set 生成压缩后的 solved trajectories
- `Cross-Episode Consolidation`
  - 从 paired source set 生成一条联合归纳的 lesson
- `Cross-Episode Consolidation + Applicability Judgment`
  - 使用同一条 consolidated lesson，但系统必须先判断 relevance 再决定是否使用

在主实验结果稳定之前，不额外加入更多分支。

---

Phase 5. 执行协议

对于 `No Memory`、`Episodic Trace`、`Cross-Episode Consolidation`：

- 挂载对应 memory artifact
- 使用同一个 standard executor

对于 `Cross-Episode Consolidation + Applicability Judgment`：

Node 1: Applicability Judge

输出：

- decision: `use` / `reject`
- 简短 relevance explanation
- 简短 failure-condition note

Node 2: Executor

- `use` -> 挂载 memory
- `reject` -> 不挂载 memory

Judge 的目标不是更频繁地使用 memory，而是支持 selective use。

---

Phase 6. 日志记录

每次 run 记录：

- task id
- split (`relevant` / `irrelevant`)
- condition
- source set id
- source cluster
- target cluster
- routing decision
- whether memory was attached
- final answer
- EM
- F1
- token usage
- failure status

同时记录 contamination audit 字段：

- source entities
- target entities
- entity overlap score
- lexical overlap score
- leakage check label

---

Phase 7. 评估

主指标：

- `EM`
- `F1`

transfer-sensitive 指标：

- `relevant gain`
- `irrelevant delta`
- `negative transfer rate`

可选分析：

- memory invocation rate
- rejection rate
- token cost

主报告规则：

- `Relevant Split` 和 `Irrelevant Split` 必须分开报告
- 不能直接压成一个 benchmark average

---

Phase 8. 基础设施与可复现性

必须具备：

- append-only run logs
- checkpoint and resume
- retry with backoff
- bounded concurrency
- per-run error logging
- 固定 pairing table 落盘保存

最终产出：

- taxonomy file
- pairing table
- run logs
- 按 split 和 condition 聚合后的 metrics
