# Progress Report: Round 1d Bridge Subtype Repair

Date: 2026-04-11

---

## 1. Executive Summary

Round 1d 没有新增模型运行，也没有修改 `model / prompt scaffold / artifact / decoding`。  
这一轮只修一层东西：

- `bridge` cluster 内部的 pairing granularity

Round 1c 之后，项目已经明确知道当前 6 个 smoke cases 不能再被当作统一 benchmark 使用；但还有一个更细的问题没有解决：

- 为什么 `wiki_dev_2639` 看起来像 “relevant bridge memory hurts”？

Round 1d 的核心结论是：

1. **当前 `hp_bridge_set_01` 并不是通用的 `bridge` source，而是一个稳定的 `attribute_bridge` source set。**
2. **当前 smoke subset 中的 `bridge` targets 并不属于同一个 subtype。**
3. **`wiki_dev_2639` 的最可信解释不再是 “relevant memory causes negative transfer”，而是 “当前 relevant source 在 subtype 层面并不真正 relevant”。**

因此，Round 1d 的价值不在于多得到一个平均分，而在于：

**把一个会误导结论的现象，重新识别为 pairing-design 问题。**

---

## 2. What Changed Since Round 1c

相对于 [progress-report-round1c-role-aware-smoke-repair.md](./progress-report-round1c-role-aware-smoke-repair.md)，Round 1d 没有继续修 aggregate 规则，而是把问题继续往 source-target matching 的结构层推进了一步。

### 2.1 Source-Side Subtype Audit

我们首先对当前 frozen `bridge` source set 做了 subtype 审计：

- [bridge_subtype_source_audit.csv](../results/07_round1d_prep/bridge_subtype_source_audit.csv)

审计对象：

- `hp_bridge_set_01` 的 5 条 source episodes

结果：

- 5 / 5 都稳定落在 `attribute_bridge`
- 没有一条能被合理判成 `relation_chain_bridge`

### 2.2 Target-Side Subtype Audit

随后，对当前 smoke subset 中仍然活跃的 `bridge` targets 做了 subtype 审计：

- [bridge_subtype_target_audit.csv](../results/07_round1d_prep/bridge_subtype_target_audit.csv)

结果：

- `wiki_dev_0092` → `attribute_bridge`
- `wiki_dev_7019` → `attribute_bridge`
- `wiki_dev_6083` → `attribute_bridge`
- `wiki_dev_2639` → `relation_chain_bridge`

### 2.3 Pairing Repair Note

最后，把 source/target 两边的 subtype judgment 收成了一个明确的 pairing repair note：

- [bridge_subtype_pairing_repair.md](../results/07_round1d_prep/bridge_subtype_pairing_repair.md)

这一步回答的不是：

- 哪个条件更强

而是：

- 当前哪些 `bridge` pairing 仍然合法
- 哪些其实已经不应继续被叫做 `relevant`

---

## 3. Round 1d Results

### 3.1 Source-Side Audit Result

| source_set_id | audited episodes | `attribute_bridge` | `relation_chain_bridge` | conclusion |
|---|---|---|---|---|
| `hp_bridge_set_01` | 5 | 5 | 0 | stable `attribute_bridge` source set |

这意味着当前 source set 的共享结构并不是笼统的 “bridge reasoning”，而是更具体的：

- 先定位中间实体
- 再从该实体上读取属性或关联事实

这与 Round 1 早期把它叫做 `bridge set` 的粗粒度命名相比，是一个更强、也更可解释的结论。

### 3.2 Target-Side Audit Result

| task_id | current role | subtype | pairing status after repair |
|---|---|---|---|
| `wiki_dev_0092` | `audit_case` | `attribute_bridge` | keep relevant |
| `wiki_dev_7019` | `diagnostic_case` | `attribute_bridge` | keep relevant |
| `wiki_dev_6083` | `boundary_case` | `attribute_bridge` | keep relevant |
| `wiki_dev_2639` | `diagnostic_case` | `relation_chain_bridge` | no longer truly relevant |

这张表的意义很关键：

- `bridge` cluster 并没有在 subtype 层面保持一致
- 只有前三条 target 真正和当前 source set 同 subtype
- `wiki_dev_2639` 则是明确的 subtype mismatch

### 3.3 Repaired Pairing Decision

Round 1d 最重要的 pairing 决策可以压成一句话：

**从现在开始，`bridge == bridge` 不再自动等于 `relevant`。**

具体来说：

- `wiki_dev_0092` / `wiki_dev_7019` / `wiki_dev_6083`
  - 仍可保留为 subtype-matched bridge cases
- `wiki_dev_2639`
  - 不能再继续使用 `hp_bridge_set_01` 作为 relevant source
  - 如果后续还想保留这条 case，必须新建 `relation_chain_bridge` source set

---

## 4. Deep Analysis

### 4.1 Finding 1: Round 1b 的 “relevant derailment” 其实混入了 subtype mismatch

Round 1b 中最刺眼的现象之一是：

- `wiki_dev_2639` 在 `no_memory` 下正确
- 在相关 memory 条件下被拉坏

如果只看粗标签，这会很容易被写成：

- relevant memory hurts

但 Round 1d 说明这个解释并不成立。

更可信的结构解释是：

- target 需要的是 `person -> spouse -> sibling`
- source 提供的是 `entity -> attribute`

也就是说，Round 1b 观察到的不是一个干净的 memory efficacy failure，而是：

- **subtype-mismatched source 被误当成 relevant**

这会直接改变后续报告中对 `wiki_dev_2639` 的用法。

### 4.2 Finding 2: 不是所有 bridge task 都该进入同一个 pairing bucket

Round 1d 的另一个重要发现是：

- `wiki_dev_0092`
- `wiki_dev_7019`
- `wiki_dev_6083`

虽然都属于 `bridge`，但它们与 `hp_bridge_set_01` 的匹配方式和 `wiki_dev_2639` 完全不同。

前者更像：

- `film -> director -> birthplace`
- `song -> performer -> award`
- `film -> director -> nationality`

也就是标准的 `attribute_bridge`。

这说明：

- 当前的 `bridge` 大类并不是没用
- 但它只能作为第一层 taxonomy
- 一旦进入 source-target pairing，就必须进一步细分 subtype

### 4.3 Finding 3: Round 1d 是一次解释修复，而不是结果修复

Round 1d 没有让任何分数变高，也没有新生成任何模型输出。  
但它依然是必要的一轮，原因在于：

- 它把一个容易被误解的 observed effect 重新归位
- 它阻止你继续把 subtype mismatch 写成 memory effect

这类轮次在学生项目里往往容易被忽略，因为它“不产出新数字”。  
但对你这个项目来说，它反而非常关键，因为你的初衷从来不是只要一个平均 gain，而是要知道：

- memory 什么时候真在起作用
- 什么时候只是 measurement / pairing 错了

Round 1d 正是在做这件事。

---

## 5. Diagnostic Conclusion

Round 1d 的最终结论可以压成三句：

1. **当前 `hp_bridge_set_01` 只能代表 `attribute_bridge`，不能继续代表所有 `bridge` source memory。**
2. **`wiki_dev_2639` 不应再被用作 “relevant memory hurts” 的证据，而应改写为 subtype-mismatch evidence。**
3. **如果还想测试 `wiki_dev_2639` 这类 target，下一步必须先补 `relation_chain_bridge` source-side support，而不是直接 rerun。**

因此，Round 1d 的最重要产出不是新结果，而是：

**一个更可信的 relevant 定义。**

---

## 6. Next Step

基于 Round 1d，下一步最合理的顺序是：

1. **对 `relation_chain_bridge` 做 source-side feasibility check**
   - 不再使用 generic `bridge` source set 硬配
   - 先判断 `HotpotQA` 是否真的有足够多的 relation-chain source candidates

2. **如果 feasibility 不成立，就停止这条线**
   - `wiki_dev_2639` 只保留为 subtype-mismatch evidence

3. **如果 feasibility 成立，再构造新的 subtype-matched source set**
   - 然后才考虑最小 rerun

一句话总结：

**Round 1d 把下一步从“继续跑”改成了“先修 source-side coverage”。**
