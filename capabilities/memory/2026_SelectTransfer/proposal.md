### Title: 固定经验预算下的 memory selective transfer

---

### 1. 问题定义

当一个 LLM agent 在多轮任务中携带过去经验时，核心问题不应该只是“memory 平均有没有帮助”，而应该是它是否能 **selectively** 地起作用：

- 当过去经验在结构上与当前任务相关时，memory 应该带来帮助
- 当过去经验在结构上与当前任务不相关时，memory 不应被滥用，也不应引入 negative transfer

现有不少 memory work 更常比较 retrieval 变体，或者比较 memory vs. no memory 的 benchmark 平均结果。但这会遗漏一个更精确的问题：

**一种 memory strategy 能否支持 selective transfer，而不是 indiscriminate reuse？**

这个 proposal 在 fixed experience budget 下研究这个问题，目标是拆开两个可能的瓶颈：

- `memory form`：过去经验被表示成什么形式
- `memory use`：系统如何判断过去经验是否应被用于当前任务

### 2. 研究问题

在 fixed source experience budget 下，哪种 memory strategy 最能支持 multi-hop QA 中的 **selective transfer**？

更具体地说：

**当 source experience 与当前任务相关时，这种 strategy 是否能提升表现；当 source experience 被刻意设置为不匹配时，这种 strategy 是否能避免 negative transfer？**

### 3. 为什么这个问题重要

这个问题的价值在于，它会直接影响后续研究方向。

- 如果结果主要由 `memory form` 驱动，后续更应研究 consolidation 质量与 representation
- 如果结果主要由 `memory use` 驱动，后续更应研究 applicability judgment、gating 与 deployment policy
- 如果两者都重要，后续应把 memory formation 和 memory use 当作耦合问题来研究，而不是分开看

也就是说，这不只是一个小的 empirical question，而是一个会影响未来研究主轴的 route-selection question。

### 4. Benchmark 与受控 setting

**Source benchmark:** HotpotQA  
**Target benchmark:** 2WikiMultiHopQA

之所以选择这个 setting，是因为它足够收敛：

- 两个 benchmark 都要求 multi-hop QA
- 二者共享一定 reasoning structure，但数据分布不同
- 这种 transfer 既有意义，又足够受控，便于做可 defend 的 pairing

所有条件保持一致：

- backbone model
- ReAct-style agent scaffold
- tool interface
- decoding parameters
- maximum step limit
- source experience count

### 5. 任务 taxonomy 与 pairing protocol

这个实验不会只看 benchmark average，而是建立在 **预定义的 source-target pairs** 上。

首先，我们把 source 和 target tasks 归入一个小型 reasoning taxonomy：

- `bridge`
- `comparison`
- `temporal`
- `distractor-heavy`

只有 dominant reasoning pattern 足够清楚的题，才会进入 pairing pool。

然后构造两个 evaluation splits：

**Relevant Split**

- source set 和 target task 属于同一 reasoning cluster
- `entity-disjoint`
- lexical overlap 低于阈值
- 不存在 answer leakage

**Irrelevant Split**

- source set 和 target task 属于不同 reasoning clusters
- `entity-disjoint`
- lexical overlap 低于阈值
- 不存在 answer leakage

这个 pairing protocol 必须在 memory experiments 之前固定下来，避免事后根据结果解释“为什么这次帮上了”或“为什么这次没帮上”。

### 6. Source experience 构造

对 HotpotQA 中每个 reasoning cluster，构造 source memory sets。

每个 source set：

- 固定包含 `N = 5` 个 solved episodes
- 只来自同一个 reasoning cluster
- 内部 `entity-disjoint`
- 在所有实验条件下保持 source set 大小一致

这样可以保证差异主要来自经验如何被表示与使用，而不是来自系统看过多少经验。

### 7. 实验条件

主实验只保留 4 个核心条件：

- `No Memory`
- `Episodic Trace`
- `Cross-Episode Consolidation`
- `Cross-Episode Consolidation + Applicability Judgment`

定义如下：

- `Episodic Trace`：从同一 source set 生成压缩后的 solved trajectories
- `Cross-Episode Consolidation`：从同一 source set 联合归纳出一条 consolidated principle
- `Cross-Episode Consolidation + Applicability Judgment`：使用相同的 consolidated memory，但系统必须先判断该 memory 是否与当前任务相关，再决定是否使用

主实验暂时不加入 single-episode abstraction 或 sham control。这些可以作为后续扩展，而不是一开始就放进主问题。

### 8. 评估指标

主任务指标：

- Exact Match (`EM`)
- F1

直接服务于 transfer 问题的指标：

- `relevant gain`
  - 相对 `No Memory`，在 Relevant Split 上的提升
- `irrelevant delta`
  - 相对 `No Memory`，在 Irrelevant Split 上的变化
- `negative transfer rate`
  - 在 Irrelevant Split 上，因为引入 memory 而出现可测量退化的任务比例

可选分析指标：

- memory invocation rate
- rejection rate under applicability judgment
- token cost

核心评估思想是：

**好的 memory strategy 不只是提升 matched transfer，还要避免 mismatched overuse。**

### 9. 假设

**H1:** 在 Relevant Split 上，两种 memory 条件都应优于 `No Memory`，但 `Cross-Episode Consolidation` 应比 `Episodic Trace` 更稳定。

**H2:** 在 Irrelevant Split 上，`Episodic Trace` 和未加控制的 `Cross-Episode Consolidation` 更容易出现 negative transfer，而 `Cross-Episode Consolidation + Applicability Judgment` 应更稳。

**H3:** `Cross-Episode Consolidation + Applicability Judgment` 应在 relevant tasks 的正向迁移和 irrelevant tasks 的稳健性之间取得最好平衡。

### 10. 预期贡献

这项工作预期提供两类贡献：

- 一套可 defend 的 pairing protocol，用于评估 matched / mismatched transfer 下的 memory
- 一个 empirical comparison，回答不同 memory strategies 是否支持 selective transfer，而不是 indiscriminate reuse

### 11. 局限性

- 当前 reasoning taxonomy 仍然较粗，可能无法覆盖更深层的 task structure
- 即使有过滤规则，pairing 质量仍然可能引入噪声
- 这里研究的是 near-transfer，而不是更广义的 open-world generalization
- 本研究中的 memory 仍是 external text-based memory，不涉及 parameter internalization

---
