# First Relation-Chain Bridge Expansion Batch

这份文件只回答一个问题：

**如果要验证 `HotpotQA` 是否能支持一个最小的 `relation_chain_bridge` source set，第一批应该怎么做？**

它是 [expand-relation-chain-bridge-source-pool.md](./expand-relation-chain-bridge-source-pool.md) 的执行版。  
这一批的目标不是“无论如何补出 5 个 `keep`”，而是尽快判断：

- 这个 subtype 在当前 source benchmark 里到底够不够多
- 值不值得继续第二批

---

## 1. 这一批要完成什么

第一批只做三件事：

1. 从当前 `HotpotQA` 同一 split 里预筛一批 relation-looking `bridge` candidates
2. 用 subtype 规则做人工标注
3. 判断：
   - 是否已经接近构造 `relation_chain_bridge` source set
   - 还是应直接判定当前 benchmark 不适合继续扩这一类

这一批不是要立刻产出新 source set，而是要产出：

- 一个清楚的 feasibility judgment

---

## 2. 这一批的固定前提

这一批开始前，不要改下面这些前提：

- `source benchmark = HotpotQA`
- `target benchmark = 2WikiMultiHopQA`
- `N = 5`
- 当前 `attribute_bridge` / `relation_chain_bridge` 定义不变
- 当前 `hp_bridge_set_01` 继续被视为 `attribute_bridge`
- 当前唯一明确需要 relation-chain coverage 的 target 是 `wiki_dev_2639`

如果你在这一步改了这些前提，那就不是“feasibility check”，而是在重写实验设计。

---

## 3. 推荐批量大小

第一批固定做：

- **15 个 raw candidates**

理由和之前的 `comparison` 扩池类似，但更保守：

- 太少：看不出 subtype 在 benchmark 里是否真实存在
- 太多：会把工作量拉回全量探索

这一批的成功标准不是“补齐 5 个”，而是：

- 你能明确判断这个 subtype 是：
  - 值得继续扩
  - 还是本来就太稀少

---

## 4. 数据来源

这一批候选题只从：

- 当前使用的 `HotpotQA` 同一 split

里取。

不要：

- 混 train / dev
- 借用 target benchmark
- 从别的 benchmark 偷题

因为当前要判断的是：

**在既定 setting 下，这个 subtype 是否可行。**

---

## 5. 候选题怎么找

### Step 1. 先限定在 `bridge` pool

因为 HotpotQA 原始 `type` 只有：

- `bridge`
- `comparison`

所以这一批必须先在：

- `raw type = bridge`

里找。

### Step 2. 再按 relation-term 预筛

优先搜索包含下面词的题面：

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

这一步只是预筛，不是最终标签。

### Step 3. 最小坏数据过滤

过滤掉：

- 缺题目
- 缺支撑信息
- 文本损坏

不要在这一层就做太多主观过滤。

---

## 6. 人工标注要求

这一批进入人工判断后，每题至少要补：

- `reasoning_label`
- `bridge_subtype`
- `keep_drop`
- `note`

推荐取值：

### `reasoning_label`

- 继续沿用现有大类：
  - `bridge`
  - `comparison`
  - `drop`

### `bridge_subtype`

- `relation_chain_bridge`
- `attribute_bridge`
- `mixed_bridge`
- `unclear`

### `keep_drop`

- `keep`
- `drop`

---

## 7. 第一批判断标准

### 应标成 `relation_chain_bridge`

只有在下面条件同时成立时，才标：

- 主导难点确实是沿关系链继续走
- 最关键的中间步骤不是取属性，而是找关系上的下一个人
- 你自己愿意把这题放进一个 relation-chain 5-shot source set

### 应 `drop`

如果出现下面任一情况，直接 `drop`：

- 表面出现亲属词，但核心仍是 attribute lookup
- relation chain 与 attribute lookup 同样主导，分不清哪个是核心
- 题型太混合
- 与已有候选几乎同模板

这一批宁可少要，也不要为了凑数把边界题塞进去。

---

## 8. 这一批完成后怎么判

第一批结束后，按下面三档做判断。

### 档位 A：继续

如果你已经拿到：

- `relation_chain_bridge keep >= 4`

而且这些题：

- 彼此不太像近重复
- 你自己愿意拿来构 set

那说明这个 subtype 在 `HotpotQA` 里是存在的，值得继续第二批，目标就是补到 `>= 5`。

### 档位 B：谨慎继续

如果只拿到：

- `relation_chain_bridge keep = 2 或 3`

但其中至少 2 题是高质量、很像这个 subtype 的核心样本，
可以继续第二批，但要非常克制，不要自动假设一定补得齐。

### 档位 C：停止并判定不可行

如果出现下面任一情况，建议直接停止：

- 真正高质量的 `relation_chain_bridge keep <= 1`
- 大多数候选都落回 `attribute_bridge`
- 勉强 `keep` 的题明显是边界题

这时更好的结论是：

- 当前 `HotpotQA` source benchmark 不足以支持稳定的 `relation_chain_bridge` source set

而不是继续无止境扩池。

---

## 9. 第一批数据写到哪里

推荐放到一个新目录：

- `results/08_relation_chain_bridge_expansion/`

至少保留：

- `candidate_batch_raw.csv`
- `candidate_batch_filtered.csv`
- `candidate_batch_for_subtype_annotation.csv`
- `candidate_batch_full.json`

如果你继续用主工作表，也可以把最终标注追加到：

- `pilot/taxonomy.csv`

但这一轮更重要的是：

- 保留一份 subtype-specific expansion 中间产物

---

## 10. 最短执行清单

如果你现在就要开做，直接照这 7 步：

1. 从当前 `HotpotQA` 同一 split 的 `bridge` pool 中筛 15 个 relation-looking raw candidates  
2. 做最小坏数据过滤  
3. 保存 raw / filtered candidate files  
4. 对 filtered candidates 逐题补：
   - `reasoning_label`
   - `bridge_subtype`
   - `keep_drop`
   - `note`
5. 统计真正的 `relation_chain_bridge keep` 数量  
6. 根据三档标准决定：
   - 继续第二批
   - 或停止并判定不可行  
7. 把判断写回 notes / report，而不是只留下表格

---

## 11. 一句话原则

**第一批 relation-chain 扩池的目标不是“凑够 5 个”，而是尽快判断这个 subtype 在当前 source benchmark 里是否值得继续追。**
