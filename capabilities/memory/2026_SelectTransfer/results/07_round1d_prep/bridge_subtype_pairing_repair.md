# Round 1d Bridge Subtype Pairing Repair

Date: 2026-04-11

输入文件：

- [bridge_subtype_source_audit.csv](./bridge_subtype_source_audit.csv)
- [bridge_subtype_target_audit.csv](./bridge_subtype_target_audit.csv)
- [pairing_table_round1.csv](../../pilot/archive/pairing_table_round1.csv)
- [round1b_pairing_artifact_audit.md](../05_round1b_prep/round1b_pairing_artifact_audit.md)

---

## 1. Source Set Judgment

`hp_bridge_set_01` 的 5 个 source episodes 当前可以稳定判成：

- `attribute_bridge`

也就是说，这个 source set 的主要能力不是一般性的 “bridge reasoning”，而是更具体的：

- 先定位中间实体
- 再从该实体上提取属性或关联事实

它并不覆盖：

- `relation_chain_bridge`

因此，从 `Round 1d` 开始，不应再把 `hp_bridge_set_01` 当作所有 `bridge` target 的天然 relevant source。

---

## 2. Target-Level Judgment

### `wiki_dev_0092`

- subtype: `attribute_bridge`
- pairing action: `keep_as_relevant`

理由：

- `film -> director -> birthplace` 与当前 source set 的 entity-to-attribute pattern 是匹配的
- 这条 case 的主要问题不是 subtype mismatch，而是 benchmark ambiguity

结论：

- relevant pairing 可以保留
- 但仍然只作 `audit_case`

### `wiki_dev_7019`

- subtype: `attribute_bridge`
- pairing action: `keep_as_relevant`

理由：

- `song -> performer -> award` 与当前 source set pattern 基本匹配
- 当前异常更像 answer granularity / output-layer 问题，而不是 subtype mismatch

结论：

- relevant pairing 可以保留
- 但继续只作 `answer_format_diagnosis`

### `wiki_dev_6083`

- subtype: `attribute_bridge`
- pairing action: `keep_as_relevant`

理由：

- `film -> director -> nationality` 与当前 source set pattern 匹配
- 当前问题主要是 `Spain` vs `Spanish` scoring boundary

结论：

- relevant pairing 可以保留
- 但继续只作 `boundary_case`

### `wiki_dev_2639`

- subtype: `relation_chain_bridge`
- pairing action: `needs_new_source_set`

理由：

- target 需要的是 `person -> spouse -> sibling` 这类 relation-chain reasoning
- 当前 `hp_bridge_set_01` 几乎全是 `attribute_bridge`
- 因此这条 case 的 relevant derailment 更合理的解释不是 “relevant memory hurts”，而是：
  - **当前 relevant source 在 subtype 层面并不真正 relevant**

结论：

- 应从当前 `attribute_bridge`-based relevant pairing 中移出
- 不应再用它支持任何 “relevant memory hurts” 的一般结论
- 如果后续还想测试这条 case，需要新建 `relation_chain_bridge` source set

---

## 3. Repaired Pairing Decision

当前 smoke subset 中的 4 个 `bridge` targets，修复后的 pairing 结论如下：

| task_id | subtype | current relevant source | repaired decision | next action |
|---|---|---|---|---|
| `wiki_dev_0092` | `attribute_bridge` | `hp_bridge_set_01` | keep relevant | 保留为 `audit_case` |
| `wiki_dev_7019` | `attribute_bridge` | `hp_bridge_set_01` | keep relevant | 保留为 `answer_format_diagnosis` |
| `wiki_dev_6083` | `attribute_bridge` | `hp_bridge_set_01` | keep relevant | 保留为 `boundary_case` |
| `wiki_dev_2639` | `relation_chain_bridge` | `hp_bridge_set_01` | no longer truly relevant | 需要新建 `relation_chain_bridge` source set |

---

## 4. Immediate Implication

`Round 1d` 当前最重要的结论只有一句：

**当前 `hp_bridge_set_01` 只能代表 `attribute_bridge`，不能继续代表所有 `bridge` target。**

这意味着下一步如果继续：

- 不要直接 rerun 全部 bridge cases
- 先决定是否值得专门构建一个 `relation_chain_bridge` source set

在这之前，`wiki_dev_2639` 更适合作为：

- subtype mismatch evidence

而不是：

- relevant-memory-negative-transfer evidence
