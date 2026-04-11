# Expand Relation-Chain Bridge Source Pool

这份文件回答的不是一般性的“再扩一批 source”，而是一个更具体的问题：

**如果 `wiki_dev_2639` 这类 `relation_chain_bridge` target 想继续保留在实验里，如何判断当前 `HotpotQA` source-side 是否能支持一个最小可用的 `relation_chain_bridge` source set。**

这一步的重点不是立刻补题，而是先做 **feasibility-first expansion**。

也就是说：

- 如果 `HotpotQA` 里确实有足够多的 `relation_chain_bridge` 候选题，就定向扩池
- 如果没有，就不要硬撑，而应把 `wiki_dev_2639` 从后续 transfer evidence 中移出

关联文档：

- [bridge-subtype-repair.md](./bridge-subtype-repair.md)
- [../rounds/round_01d_bridge_subtype_repair.md](../rounds/round_01d_bridge_subtype_repair.md)
- [../results/07_round1d_prep/bridge_subtype_pairing_repair.md](../results/07_round1d_prep/bridge_subtype_pairing_repair.md)

---

## 1. 为什么需要这一步

`Round 1d` 的关键发现已经很明确：

- `hp_bridge_set_01` 是 `attribute_bridge`
- `wiki_dev_2639` 是 `relation_chain_bridge`

所以当前的 relevant pairing 在 subtype 层面并不成立。

这意味着现在有且只有两个合法方向：

1. **构建一个最小的 `relation_chain_bridge` source set**
2. **承认当前 source benchmark 不覆盖这个 subtype，并把相关 target 从 transfer evidence 中移出**

不合法的方向是：

- 继续把 `hp_bridge_set_01` 当作 `wiki_dev_2639` 的 relevant source
- 或者在没有 subtype 覆盖的情况下，继续用这条 case 支持 “relevant memory hurts”

---

## 2. 什么时候才启动这份流程

只有同时满足以下条件，才启动：

- 当前项目仍然固定 `source benchmark = HotpotQA`
- 当前项目仍然希望保留至少 1 个 `relation_chain_bridge` target
- 当前 `attribute_bridge` source set 已确认不能覆盖该 target
- 当前不准备改模型 / prompt / artifact，而是优先修 pairing

当前项目满足这些条件，因此可以进入这一步。

---

## 3. 这一步真正的目标

这一步不是“无论如何都要补出一套新 source”。

真正目标是回答下面这个问题：

**在不破坏当前实验 setting 的前提下，`HotpotQA` 是否能提供至少 5 个稳定的 `relation_chain_bridge` source episodes？**

因此成功有两种形式：

### 成功 A：可行

- 找到足够多的候选题
- 经过人工标注后，至少有 `5` 个 `keep`
- 它们之间不是近重复
- 可以构成一个最小 `relation_chain_bridge` source set

### 成功 B：不可行但结论清楚

- 经过定向筛选后，发现 `HotpotQA` 中这一 subtype 太稀少或太不稳定
- 无法构成 `N = 5` 的可用 source set

这也是成功，因为它提供了一个重要的实验设计结论：

- 当前 setting 不应继续把 `relation_chain_bridge` 当作 source-supported subtype

---

## 4. 这一轮不做什么

这一步明确 **不** 做下面这些事：

- 不改 `source benchmark`
- 不改 `target benchmark`
- 不临时把 `N = 5` 改小
- 不拿 `2WikiMultiHopQA` 反向当 source
- 不把 `relation_chain_bridge` 和 `attribute_bridge` 混成一个新大类
- 不在这一轮引入新模型或新 prompt

也就是说，这一步是：

**在既定 setting 下做 feasibility check，不是重新设计整个项目。**

---

## 5. 推荐 subtype 定义

当前建议仅保留一个很窄的 `relation_chain_bridge` 定义：

### `relation_chain_bridge`

只有当题目满足下面条件时，才标成这一类：

- 目标答案依赖一个明确的关系链
- 关键中间步骤不是“找属性”，而是“沿关系继续走”
- 例如：
  - spouse -> sibling
  - spouse -> father
  - parent -> sibling
  - child -> spouse

如果一题看起来有两个实体，但最终只是：

- 找到一个中间人
- 再读取该人的出生地 / 国籍 / 年份

那仍应视为：

- `attribute_bridge`

不要为了凑数，把边界题都往 `relation_chain_bridge` 里塞。

---

## 6. 推荐搜索策略

这一步不能靠完全随机抽样。

应该采用：

**relation-term prefilter + manual subtype annotation**

### 6.1 题面预筛关键词

优先搜索这类词：

- `father-in-law`
- `mother-in-law`
- `brother-in-law`
- `sister-in-law`
- `spouse`
- `husband`
- `wife`
- `father`
- `mother`
- `sibling`
- `son`
- `daughter`

注意：

- 这只是预筛
- 不是只要出现这些词就算 `relation_chain_bridge`

### 6.2 为什么不用原始 `type`

HotpotQA 的原始 `type` 只有：

- `bridge`
- `comparison`

它没法再细分到 subtype，所以这里只能：

- 先按 `bridge` pool 预筛
- 再靠你自己的 subtype annotation 做真正判断

---

## 7. 推荐批量大小

第一批不要太大，先做：

- **12 到 20 个 raw candidates**

这个范围的理由是：

- 关系链题在 `HotpotQA` 中未必很多
- 命中率可能显著低于之前 `comparison` 扩池
- 但也不值得一开始就扫很大一批

第一批的成功标准不是“直接凑够 5 个”，而是：

- 能看出这个 subtype 在 source benchmark 中到底稀不稀

---

## 8. 标注与过滤规则

### 必填字段

追加到工作表时，每题至少补：

- `reasoning_label`
- `bridge_subtype`
- `keep_drop`
- `note`

### `keep` 的最低标准

只有当下面条件同时成立，才值得 `keep`：

- 主导难点真的是 relation-chain reasoning
- 不是单纯 attribute lookup
- 和现有候选相比不是近重复模板
- 你自己愿意把它放进一个 5-shot relation-chain source set

### 应该 `drop` 的情况

- 题面出现亲属词，但实际只是在查某人的出生地 / 国籍
- 关系链存在，但最终主导难点仍是 attribute lookup
- 关系链太混合，无法清楚判断主 subtype
- 和已有候选几乎同模板

---

## 9. 停止条件

这一步必须有明确停止条件。

### 继续扩池

如果第一批之后：

- 已有 `relation_chain_bridge keep < 5`
- 但你看到这个 subtype 在 `HotpotQA` 中明显存在，只是第一批不够

那可以继续第二批。

### 停止并判定不可行

如果第一批之后出现以下任一情况，就应停止，而不是继续硬扩：

- 真正的 `relation_chain_bridge keep` 极少
- 多数候选都是边界题
- 就算凑到 5 个，也明显近重复或质量不稳

这时应直接记录结论：

- **在当前 `HotpotQA` source benchmark 下，`relation_chain_bridge` source pool 不足以支持一个稳定 `N = 5` source set。**

---

## 10. 如果不可行，下一步怎么做

如果最终判定不可行，下一步不是继续硬跑，而是：

1. 把 `wiki_dev_2639` 从任何 transfer aggregate 中永久移出
2. 在报告里明确说明：
   - 当前 source benchmark 不覆盖该 subtype
   - 因此不能用它评价当前 memory strategy 的 matched transfer
3. 保留它作为：
   - subtype mismatch evidence
   - pairing design limitation evidence

也就是说：

**“补不出来” 也是结果，不是失败。**

---

## 11. One-Line Rule

**只有在 `HotpotQA` 里真的能找到稳定的 `relation_chain_bridge` source pool 时，`wiki_dev_2639` 才值得继续做 rerun；否则它应被当作 subtype-mismatch evidence，而不是 memory-effect evidence。**
