# High-Precision Relation-Chain Bridge Expansion Batch

这份文件定义 `Batch 2` 应该如何做。

它的定位不是“继续泛泛再搜一批带亲属词的题”，而是：

**用更高 precision 的 relation-chain 模板，做最后一次 feasibility check。**

关联文档：

- [expand-relation-chain-bridge-source-pool.md](./expand-relation-chain-bridge-source-pool.md)
- [../rounds/round_01e_relation_chain_final_feasibility_check.md](../rounds/round_01e_relation_chain_final_feasibility_check.md)
- [../results/08_relation_chain_bridge_expansion/batch_01_subtype_annotation_summary.md](../results/08_relation_chain_bridge_expansion/batch_01_subtype_annotation_summary.md)

---

## 1. Why Batch 2 Exists

Batch 1 的结论已经很清楚：

- screened rows: `12`
- stable `relation_chain_bridge + keep`: `1`

这说明：

- 泛 relation-term prefilter 的 recall 够用
- 但 precision 仍然太低
- 大部分候选最终还是掉回 `attribute_bridge`

所以 Batch 2 不应再重复 Batch 1 的搜索方式，而应直接提高模板精度。

---

## 2. Core Rule

从 Batch 2 开始，候选题不能只满足：

- 出现 1 个 relation term

而必须尽量满足下面之一：

### Rule A: explicit multi-relation wording

题面同时出现两个不同 relation terms，例如：

- `mother` + `daughter`
- `wife` + `father`
- `husband` + `sister`
- `father` + `son`

### Rule B: nested relation structure

题面出现明显的关系嵌套，例如：

- `mother of the daughter of ...`
- `father of ...'s son`
- `wife of the brother of ...`
- `husband of the daughter of ...`

如果一题只有单一 relation term，再怎么像 kinship 题，也不应优先进入 Batch 2。

---

## 3. Recommended Template Families

Batch 2 推荐只保留高精度模板。

### Family 1: parent-child chain

- `mother ... daughter`
- `mother ... son`
- `father ... daughter`
- `father ... son`
- `daughter ... mother`
- `daughter ... father`
- `son ... mother`
- `son ... father`

### Family 2: spouse + family chain

- `wife ... father`
- `wife ... mother`
- `wife ... sibling`
- `husband ... father`
- `husband ... mother`
- `husband ... sibling`
- `spouse ... father`
- `spouse ... mother`

### Family 3: sibling + family chain

- `brother ... wife`
- `sister ... husband`
- `sibling ... father`
- `sibling ... mother`

### Family 4: possessive nested chain

- `X's wife`
- `X's husband`
- `X's daughter`
- `X's son`

只有当 possessive 结构和第二个 relation term共同出现时，才应高优先保留。

---

## 4. What To Exclude Early

Batch 2 应主动排除这些高频噪声：

- honorific / metaphorical `father of ...`
- title matches such as `Father Ted`
- title matches such as `Son of ...`
- single-hop spouse lookup
- single-hop parent lookup

也就是说：

- `wife -> businessman`
- `father -> profession`
- `daughter -> film`

这类题即使是合法 `bridge`，也不再进入 Batch 2 的高优先候选。

---

## 5. Batch Size

推荐：

- raw candidates: `12-20`

Batch 2 的目标不是搜很多，而是让每一条都更像真的 relation-chain 候选。

---

## 6. Annotation Rule

Batch 2 的人工标注仍然使用：

- `reasoning_label`
- `bridge_subtype`
- `keep_drop`
- `note`

但判断时更严格：

- 只有明确体现 relation-to-relation continuation，才记为 `relation_chain_bridge`
- 单一 relation -> attribute 的题，直接标 `attribute_bridge + drop`
- 边界题直接 `unclear + drop`

---

## 7. Decision Rule After Batch 2

### Continue to source-set construction

只有在下面条件满足时才继续：

- Batch 2 新增 `>= 4` 个高质量 keep
- 或 Batch 1 + Batch 2 合计 `>= 5`
- 且这 5 个题不明显近重复

### Stop and close this line

如果 Batch 2 后仍然无法达到上面条件，就应正式记录：

- 当前 `HotpotQA` source benchmark 不足以支持稳定的 `relation_chain_bridge` source set

此时：

- 不再继续扩池
- `wiki_dev_2639` 只保留为 subtype-mismatch evidence

---

## 8. Output Location

推荐输出到：

- `results/09_relation_chain_bridge_expansion_batch2/`

至少保留：

- `candidate_batch2_raw.csv`
- `candidate_batch2_filtered.csv`
- `candidate_batch2_for_subtype_annotation.csv`
- `candidate_batch2_full.json`
- `candidate_batch2_summary.md`

如果需要继续补：

- `batch_02_subtype_annotation_summary.md`

---

## 9. One-Line Rule

**Batch 2 要优先提高 precision，而不是继续扩大 generic relation-term recall。**
