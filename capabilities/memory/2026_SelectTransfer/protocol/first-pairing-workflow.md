# First Pairing Workflow

这份文件只回答一个问题：

**第一批 `relevant / irrelevant pairs` 怎么构造？**

目标不是一次做出完整 pairing table，而是先构造出一小批足够干净、足够可解释的 pairs，用来支撑第一轮 pilot。

## 1. pairing 在这个项目里的作用

这个项目的重点不是单纯比较 memory 有没有帮助，而是比较：

- 当 source experience 与当前任务结构相关时，memory 是否能带来正向迁移
- 当 source experience 与当前任务结构不相关时，memory 是否会被误用并造成 negative transfer

因此，pairing 的作用是：

- 为 `Relevant Split` 构造“理论上应该有帮助”的 source-target pairs
- 为 `Irrelevant Split` 构造“理论上不该自然帮上忙”的 source-target pairs

如果 pairing 本身不干净，后面的结果就很难解释。

## 2. 第一轮 pairing 的规模

第一轮不要贪多。

建议：

- `Relevant Split`：先做 10 对
- `Irrelevant Split`：先做 10 对

总计：

- 20 个 target task pairing

如果第一轮 taxonomy 和 source sets 还不够稳，也可以先从：

- 6 个 relevant pairs
- 6 个 irrelevant pairs

开始。

## 3. 进入 pairing 候选池的前提

只有以下内容可以进入 pairing：

### target task

- 在 [taxonomy.csv](./taxonomy.csv) 中被标为 `keep`
- `reasoning_label` 清楚
- 不是高歧义边界 case

### source set

- 已写入 [source_sets.csv](./source_sets.csv)
- cluster 清楚
- 内部 pattern 足够稳定
- 你自己愿意拿它去生成 `episodic_trace` 和 `consolidation`

如果 target task 或 source set 本身不干净，先不要进入 pairing。

## 4. Relevant pair 的构造规则

一条 `relevant pair` 至少满足：

- target task 与 source set 属于同一个 `reasoning_label`
- `entity-disjoint`
- lexical overlap 尽量低
- 没有明显 answer leakage

### 怎样理解 “relevant”

不是说：

- source set 和 target task 看起来像

而是说：

- source set 中的经验在 reasoning structure 上，理论上对 target task 有帮助

如果你只能说“它们表面比较像”，那不够。

### Relevant pair 的一句话定义

每条 relevant pair 最好都能写一句话说明为什么它合理，例如：

- `same bridge pattern via intermediate entity lookup`
- `same comparison structure with different entities`
- `same temporal ordering pattern under different surface form`

如果写不出这句话，这条 pair 通常还不够稳。

## 5. Irrelevant pair 的构造规则

一条 `irrelevant pair` 至少满足：

- target task 与 source set 属于不同 `reasoning_label`
- `entity-disjoint`
- lexical overlap 尽量低
- 没有明显 answer leakage

### 怎样理解 “irrelevant”

不是说：

- 它们完全随机、毫无关系

而是说：

- source set 中的经验不应该在 reasoning structure 上自然帮助这个 target task

换句话说，`irrelevant` 的定义是：

**不具备结构性迁移理由。**

### Irrelevant pair 的一句话定义

每条 irrelevant pair 最好也能写一句说明，例如：

- `comparison source set paired with bridge target`
- `temporal source set does not match distractor-heavy target`

如果你解释时开始说“也许还是能帮一点”，那说明这条 pair 可能不够干净。

## 6. 实际构造流程

### Step 1. 先选 target tasks

先从 `taxonomy.csv` 里挑出第一轮最干净的 target tasks：

- `keep`
- label 清楚
- 不是边界 case

优先选你自己最有把握的题，不要一开始就拿最模糊的 target tasks 做 pairing。

### Step 2. 给每个 target task 找一个 relevant source set

按 cluster 匹配：

- `bridge` target -> 先找 `bridge` source set
- `comparison` target -> 先找 `comparison` source set
- `temporal` target -> 先找 `temporal` source set

然后检查：

- entities 是否重叠
- lexical overlap 是否太高
- 是否存在潜在泄漏

### Step 3. 再给同一个 target task 找一个 irrelevant source set

按不同 cluster 选择：

- `bridge` target -> 优先试 `comparison` 或 `temporal` source set
- `comparison` target -> 优先试 `bridge` 或 `temporal` source set
- `temporal` target -> 优先试 `bridge` 或 `comparison` source set

然后继续检查：

- entities 是否重叠
- lexical overlap 是否太高
- 是否真的不具备自然迁移理由

### Step 4. 写 pairing note

每条 pair 都要写一句 `pairing_note`，说明为什么它是 relevant 或 irrelevant。

推荐写法：

- `relevant: same comparison pattern, different entities`
- `irrelevant: temporal source mismatched with bridge target`
- `irrelevant: same topic words but different reasoning structure`

`pairing_note` 的目的不是写长篇解释，而是给未来回看和答辩时留下明确证据。

## 7. 第一轮 pairing 后的检查

每批 pair 做完后，至少检查 3 件事。

### 检查 1. Relevant pair 是否真的“该有帮助”

问自己：

- 如果 memory 真有用，这条 pair 理论上应该提供帮助吗？

如果答案是“说不清”，那它可能不够好。

### 检查 2. Irrelevant pair 是否真的“不该自然帮上忙”

问自己：

- 这条 source set 如果帮上忙，是因为 memory 真学到了更高层的可迁移知识，还是因为 pair 其实并不够不匹配？

如果你怀疑后一种解释，这条 irrelevant pair 还不够干净。

### 检查 3. 两个 split 是否在结构上区分明确

Relevant / Irrelevant 的区别应该主要来自：

- reasoning pattern 是否匹配

而不是来自：

- topic 完全不同
- 问题长度差异太大
- 数据质量显著不同

如果 split 的区别混入太多别的因素，解释会变弱。

## 8. 第一轮 pairing 应输出什么

更新 [pairing_table.csv](./pairing_table.csv)。

至少填写：

- `target_task_id`
- `target_cluster`
- `relevant_source_set_id`
- `irrelevant_source_set_id`
- `entity_overlap_score`
- `lexical_overlap_score`
- `leakage_check_label`
- `pairing_note`

同时在 [notes.md](./notes.md) 里补一段总结：

- 哪些 cluster 之间最容易构造 clean relevant pairs
- 哪些 cluster 之间最容易构造 clean irrelevant pairs
- 哪些 pair 经常处在“看起来不够干净”的中间状态

## 9. 第一轮 pairing 的成功标准

第一轮 pairing 成功，不是数量很多，而是：

- 至少有一批你自己愿意拿去做 pilot 的 clean pairs
- relevant pairs 看起来确实“理论上应该有帮助”
- irrelevant pairs 看起来确实“不该自然帮上忙”
- 你可以用一句话解释每条 pair 的合理性

## 10. 最重要的提醒

pairing 的目标不是追求“绝对正确”，而是：

**先构造出一小批可 defend、可解释、可用于 pilot 的 source-target pairs。**

只要这一步做稳，你后面才有可能解释：

- 是 memory strategy 本身在起作用
- 还是 source-target 关系本来就不干净
