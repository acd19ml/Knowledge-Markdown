# Bridge Subtype Repair

这份文件定义 `Round 1d` 中如何修正当前过粗的 `bridge` pairing。

目的不是重写整个 taxonomy，而是只回答一个更小的问题：

**当前被统一标成 `bridge` 的 source / target，是否实际上包含了不同 subtype，导致 relevant pairing 在 subtype 层面并不成立。**

关联文档：

- [../rounds/round_01d_bridge_subtype_repair.md](../rounds/round_01d_bridge_subtype_repair.md)
- [../results/05_round1b_prep/round1b_pairing_artifact_audit.md](../results/05_round1b_prep/round1b_pairing_artifact_audit.md)
- [../results/05_round1b_prep/round1c_role_aware_smoke_subset.csv](../results/05_round1b_prep/round1c_role_aware_smoke_subset.csv)

---

## 1. Why This Repair Exists

`Round 1b` 和 `Round 1c` 暴露出一个具体问题：

- `wiki_dev_2639` 在 label 层面属于 `bridge`
- relevant source `hp_bridge_set_01` 也属于 `bridge`
- 但实际效果却更像 relevant artifact 把 baseline 拉坏

这说明单纯的 cluster-level `bridge == bridge` 已经不够了。

当前最合理的假设是：

- `bridge` 至少混入了两种不同结构

### subtype A: `attribute_bridge`

典型形式：

- `song -> singer -> birth year`
- `film -> actor -> TV work`
- `venue -> park -> opening date`

特点：

- 先定位中间实体
- 再从该实体上取一个属性

### subtype B: `relation_chain_bridge`

典型形式：

- `person -> spouse -> sibling`
- `person -> spouse -> father`

特点：

- 关键不只是取属性
- 而是沿关系链继续推理

---

## 2. What Must Be Audited

`Round 1d` 至少审三类对象：

1. `hp_bridge_set_01` 的 5 个 source episodes
2. 当前 smoke subset 中所有 `bridge` target
3. 如果需要，`pairing_table_round1.csv` 中其余 `bridge` target

目标不是全面扩展，而是先判断：

- 当前 source set 更偏哪种 subtype
- 当前 target 与它是否真的同 subtype

---

## 3. Required Output Fields

对每个被审对象，至少补这几个字段：

- `bridge_subtype`
- `subtype_note`
- `subtype_confidence`

对每个 pair，至少补这几个字段：

- `source_subtype`
- `target_subtype`
- `subtype_match`
- `pairing_action`

推荐取值：

### `bridge_subtype`

- `attribute_bridge`
- `relation_chain_bridge`
- `mixed_bridge`
- `unclear`

### `subtype_match`

- `yes`
- `partial`
- `no`

### `pairing_action`

- `keep_as_relevant`
- `downgrade_to_mismatched`
- `remove_from_smoke_subset`
- `needs_new_source_set`

---

## 4. Decision Rule

### Keep As Relevant

只有当以下条件同时成立，当前 pair 才应继续被视为 `relevant`：

- source 和 target 同属一个稳定 subtype
- 当前 artifact wording 与 target 的求解路径大致一致
- `Round 1b` observed effect 不显示明显 derailment

### Downgrade To Mismatched

如果 cluster label 一致，但 subtype 明显不同，则应降级：

- `bridge -> bridge`
- 但实际上 `attribute_bridge -> relation_chain_bridge`

这类 pair 不能再被写成 relevant evidence。

### Remove From Smoke Subset

如果某个 case 同时满足：

- subtype 不清楚
- benchmark 本身又有 ambiguity / scoring 问题

则更合理的做法不是保留，而是直接从下一轮 smoke subset 移出。

### Needs New Source Set

如果关键 target 属于 `relation_chain_bridge`，但当前 source set 几乎全是 `attribute_bridge`，则应明确记录：

- 当前问题不是 prompt、不是模型
- 而是 source set 本身没有覆盖这个 subtype

---

## 5. Minimum Concrete Task

最小可执行任务是：

1. 给 `hp_bridge_set_01` 的 5 条 source episode 打 subtype
2. 给 `wiki_dev_2639`、`wiki_dev_0092`、`wiki_dev_6083`、`wiki_dev_7019` 这些 bridge target 打 subtype
3. 只针对这些 bridge cases 生成一个 repaired pairing note

如果这三步做完，仍然看不出 subtype 是否稳定，再考虑：

- 是否需要重建 bridge source set

在这之前，不要急着 rerun。

---

## 6. One-Line Rule

**从 Round 1d 开始，`bridge` 不再因为同属一个粗 cluster 就自动算作 `relevant`。**
