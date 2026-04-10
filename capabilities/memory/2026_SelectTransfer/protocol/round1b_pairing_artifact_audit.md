# Round 1b Pairing / Artifact Audit

这份文件不是新的实验 proposal，也不是新的 round spec。  
它只服务于一个非常具体的目标：

**在 Round 1b 已经确认 prompt scaffold 可用之后，回头检查当前 observed effects 到底更像是来自 `pairing`、`artifact wording`，还是更接近我们真正想测的 `selective transfer`。**

它回答的问题不是：

- 哪个条件最终更好
- memory 是否已经被证明有效

而是：

- 当前 6 个 smoke cases 上，`relevant / irrelevant` 的区分到底有没有站住
- `episodic_trace` 与 `cross_episode_consolidation` 是否真的提供了不同性质的 memory
- 某些 improvement / degradation 是否其实更像 prompt wording 或 answer formatting effect

---

## 1. 为什么现在要做这一层

Round 1b 的结果已经说明两件事：

- 新 scaffold 成功 elicited 了 `## Reasoning` 与 `## Final Answer`
- process-level 的 `memory use / reject` 现在可以被观察

但当前 aggregate 仍然有几个反直觉现象：

- `relevant` memory 有时把 baseline 拉坏
- `irrelevant` consolidation 有时反而更好
- 某些 case 的 improvement 更像答案压缩，而不是策略迁移

如果在这个阶段直接把问题归因到：

- measurement 不够稳
- 或 memory 在当前模型上无效

都太早。中间还缺一层：

**先确认 pairing 和 artifact 本身是不是已经在当前 case 上制造了额外偏差。**

---

## 2. 这轮 audit 要审什么

只审 3 类对象：

1. `pairing`
   - relevant / irrelevant 在当前 case 上是否真的成立

2. `artifact content`
   - `episodic_trace` 与 `cross_episode_consolidation` 是否在当前 case 上提供了不同类型的信息
   - 这些信息是 task-structural，还是更像 domain-general advice

3. `observed interaction`
   - 当前 prediction 的变化，更像：
     - strategy reuse
     - answer-format correction
     - generic prompt interference
     - reasoning derailment

---

## 3. 当前优先审的 6 个 smoke cases

### A. `wiki_dev_8896`

角色：
- clean comparison case
- process-level selectivity 已经出现

为什么重要：
- 它是当前最接近“该用时用，不该用时拒绝”的 case
- 如果连这个 case 都站不住，Round 1b 的 process-level argument 会明显变弱

要重点检查：
- relevant episodic trace 为什么被 explicit use
- irrelevant episodic trace 为什么被 explicit reject
- 这种 distinction 是真的来自 cluster mismatch，还是只是 wording 太容易拒绝

### B. `wiki_dev_2639`

角色：
- baseline 正确，但 relevant memory 拉坏
- irrelevant consolidation 又回到正确答案

为什么重要：
- 它是当前最强的 “memory-induced degradation” 证据
- 也是最能暴露 pairing / artifact 是否有问题的 case

要重点检查：
- relevant pairing 是否真的对该 task 更相关
- relevant artifact 是否过度强调某种不适用的 bridge pattern
- irrelevant consolidation 是否其实提供了更短、更干净的 reasoning cue

### C. `wiki_dev_7019`

角色：
- answer-format sensitive case
- irrelevant consolidation 带来唯一可见 improvement

为什么重要：
- 这个 case 容易被误读成 “irrelevant memory 更好”
- 但它也可能只是让答案更短、更贴近 gold phrase

要重点检查：
- prediction improvement 是不是主要来自 output compression
- consolidation wording 是否给了更强的“只输出核心 award 名”暗示
- 这个 case 能不能被算作 strategy-level transfer evidence

### D. `wiki_dev_0092`

角色：
- audit / ambiguity case

为什么重要：
- 它不应用来证明 transfer
- 但它能帮助判断模型是沿 strongest evidence 走，还是被 memory 带偏

要重点检查：
- memory 是否改变了解题路径
- 如果 prediction 不变，模型对 memory 的 use/reject 文字是否可信

### E. `wiki_dev_6083`

角色：
- scoring boundary case

为什么重要：
- 它不适合判断 memory 本身是否有效
- 但它会污染 aggregate interpretation

要重点检查：
- 这个 case 在后续 aggregate 里是否应该单独标注
- answer normalization 是否需要最小修正

### F. `wiki_dev_10727`

角色：
- clean ceiling comparison case

为什么重要：
- 它可以作为“memory 不该破坏 baseline”的 sanity check

要重点检查：
- memory 是否只是被忽略
- 即使 explicit use 出现，是否只是 verbalization，而不是真正影响决策

---

## 4. 每个 case 要回答的固定问题

审每个 case 时，都按同一组问题回答，不要临时换标准。

### 4.1 Pairing Audit Questions

1. 当前 `relevant` source set 与 target task，在 reasoning structure 上真的更接近吗？
2. 当前 `irrelevant` source set 是否只是 topic 不同，还是在 reasoning structure 上也确实不匹配？
3. 如果 `irrelevant` 看起来也能自然帮上忙，那问题更像是：
   - pairing 定义太弱
   - 还是该 target 本来就对更泛化的 strategy 开放

### 4.2 Artifact Audit Questions

1. `episodic_trace` 提供的是 episode-level pattern，还是已经在偷渡更高层原则？
2. `cross_episode_consolidation` 提供的是 cluster-specific heuristic，还是其实过于通用？
3. relevant / irrelevant 两个 artifact 在当前 target 上，哪一个更像：
   - task-structural help
   - generic answer-style instruction
   - cognitive overload

### 4.3 Interaction Audit Questions

1. memory 是否改变了 reasoning path？
2. memory 是否改变了 answer type？
3. memory 是否只是让答案变短 / 变像 gold，而没有改变推理本身？
4. 当前 observed change 更应归因于：
   - strategy reuse
   - answer-format correction
   - prompt interference
   - ambiguity in benchmark

---

## 5. 审计时优先读哪些文件

每个 case 最少读这几类材料：

1. `Round 1b` raw outputs
   - `results/05_round1b_run/raw_outputs/r1b_*.md`

2. 当前 frozen pairing
   - [pairing_table_round1.csv](../pilot/archive/pairing_table_round1.csv)

3. 当前 frozen source sets
   - [source_sets_round1.csv](../pilot/archive/source_sets_round1.csv)

4. 两类 artifacts
   - [artifacts/hp_bridge_set_01/episodic_trace.md](../artifacts/hp_bridge_set_01/episodic_trace.md)
   - [artifacts/hp_bridge_set_01/cross_episode_consolidation.md](../artifacts/hp_bridge_set_01/cross_episode_consolidation.md)
   - [artifacts/hp_comparison_set_01/episodic_trace.md](../artifacts/hp_comparison_set_01/episodic_trace.md)
   - [artifacts/hp_comparison_set_01/cross_episode_consolidation.md](../artifacts/hp_comparison_set_01/cross_episode_consolidation.md)

5. 如果 case 本身有 audit 问题，再补读：
   - [round1_target_audit.md](../results/05_round1b_prep/round1_target_audit.md)

---

## 6. 输出形式

这轮 audit 不需要新 notebook，也不需要新 benchmark run。  
建议直接输出一个 markdown 文件，按 case 写短结论。

推荐文件名：

- `results/05_round1b_prep/round1b_pairing_artifact_audit.md`

每个 case 固定写这 5 行：

1. `Observed effect`
2. `Pairing judgment`
3. `Artifact judgment`
4. `Most likely explanation`
5. `Implication for next round`

---

## 7. 判定标准

### 可以支持进入下一步 full rerun 的信号

- 至少大多数关键 case 上，`relevant / irrelevant` 的判断能被解释清楚
- 至少大多数关键 case 上，artifact 差异看起来确实是 structural 而不是 stylistic
- 改善与退化大致能被稳定地归到少数几类机制上，而不是每个 case 都讲不通

### 暂时不应进入 full rerun 的信号

- `relevant / irrelevant` 在多个关键 case 上都站不住
- `cross_episode_consolidation` 看起来太通用，几乎像 generic reasoning advice
- observed gain / loss 主要来自 answer wording，而不是 reasoning strategy
- 每个 case 都需要完全不同的事后解释，无法形成可复用 pattern

---

## 8. 一句话目标

这轮 audit 的目的不是证明某个 memory form 赢了，而是回答：

**当前 Round 1b 里看到的 improvement / degradation，到底有多少已经足以被解释为 memory effect，又有多少其实还是 pairing 或 artifact 自身造成的。**
