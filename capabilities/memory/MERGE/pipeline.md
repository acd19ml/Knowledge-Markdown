Phase 0. Global Setup

统一：
	•	model
	•	prompt scaffold
	•	tools
	•	decoding params
	•	max steps
	•	random seed
	•	API wrapper
	•	checkpoint path
	•	concurrency limit

⸻

Phase 1. Reasoning Pattern Taxonomy

先定义推理类型：
	•	Bridge
	•	Comparison
	•	Temporal
	•	Distractor-heavy

给 source/target tasks 打标签。

⸻

Phase 2. Source Experience Construction

在每个 reasoning cluster 内构建 source memory sets。
每组包含 5 个 solved episodes。

新增约束：

Pairing eligibility filters

source set 若要用于某个 target task，必须满足：
	•	same reasoning cluster
	•	entity-disjoint
	•	lexical-overlap below threshold
	•	optional contamination judge = safe

⸻

Phase 3. Memory Construction

从同一 source set 构建：
	•	A episodic trace
	•	B single-episode abstraction
	•	C cross-episode consolidation
	•	D uses same C memory but with applicability-gated deployment
	•	D-sham placebo control
	•	baseline no memory

⸻

Phase 4. Safe Oracle-Cluster Injection

对每个 target task：
	1.	找到 reasoning-matched source sets
	2.	过滤掉 entity-overlap / lexical-overlap pairings
	3.	选一个安全 memory set 作为固定注入源

这一步不再是简单 oracle injection，
而是：

safe oracle-cluster injection

⸻

Phase 5. Hard-Gated Two-Node Execution

A/B/C

直接挂载对应 memory，进入 standard ReAct executor

D

先跑 Node 1：

Node 1: Applicability Judge
输出：
	•	decision: use / partial / reject
	•	why relevant
	•	failure conditions
	•	if partial: relevant fragment only

然后进入 Node 2：

Node 2: Executor with hard routing
	•	reject → no memory attached
	•	partial → only selected fragment attached
	•	use → full memory attached

D-sham

输出一段与 relevance 无关的泛化反思，但不进行 hard gating

⸻

Phase 6. Robust Logging

每个 run 完成后立即 append 到 .jsonl：
	•	task id
	•	condition
	•	memory set id
	•	cluster
	•	routing decision
	•	loaded memory fragment
	•	trajectory
	•	final answer
	•	metrics
	•	failure status

⸻

Phase 7. Evaluation

主任务指标
	•	EM
	•	F1
	•	success rate

主行为指标
	•	LLM-judged first-action shift
	•	LLM-judged strategic shift
	•	harmful vs helpful shift

辅助行为指标
	•	first-action exact change
	•	action-type sequence distance
	•	query overlap ratio

memory-specific 指标
	•	error repetition rate
	•	applicability judgment accuracy
	•	acceptance / rejection / partial-use rate

⸻

Phase 8. Runtime Infrastructure

必须实现：
	•	exponential backoff
	•	retry with jitter
	•	append-only jsonl checkpoint
	•	resume-from-checkpoint
	•	bounded concurrency
	•	error logging per run

⸻

六、我建议你再补一个很重要的实验日志字段

为了后面做 contamination 审计，建议每条 run 额外记录：
	•	source entities
	•	target entities
	•	entity overlap score
	•	lexical overlap score
	•	contamination-judge label

这样如果老师或 reviewer 质疑，你可以直接展示：

我们不是口头说 entity-disjoint，而是对每个配对都做了程序化记录与审计。

这个会很加分。