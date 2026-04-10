# First Source Set Selection Workflow

这份文件只回答一个问题：

**第一轮 20 题标完后，怎么挑第一批 source sets？**

目标不是一次挑出“最终版本”的 source sets，而是先构造出一批足够干净、足够可用的初始集合，支撑后续的 pilot pairing。

## 1. 先明确 source set 的作用

在这个项目里，source set 不是简单的“5 道题打包在一起”。

它承担两个作用：

- 为 `Episodic Trace` 提供 source experience
- 为 `Cross-Episode Consolidation` 提供可联合抽象的材料

所以一个好的 source set 必须同时满足：

- 内部确实共享某种 reasoning pattern
- 但又不是几道几乎重复的题

如果只满足前者，它容易变成模板重复。
如果只满足后者，它又很难支撑 consolidation。

## 2. 第一轮 source set 的规模

第一轮不要贪多。

建议目标：

- 每个可用 cluster 先挑 **1 个 source set**
- 每个 source set 固定 **5 题**

也就是说，如果第一轮 taxonomy 后只有 3 个 cluster 比较稳定，那就先只做 3 个 source sets。

不要为了“凑齐四类”硬塞质量差的题。

## 3. 进入 source set 候选池的前提

只有满足以下条件的题，才进入 source set 候选池：

- 在 [taxonomy.csv](./taxonomy.csv) 中被标为 `keep`
- `reasoning_label` 清晰，不是边界 case
- `note` 中没有明显写出“equally strong” 或 “unclear”

第一轮 source set 构造时，**不要**优先使用你自己都很犹豫的题。

原则：

- 宁可少做几个 source sets，也不要把不稳定样本放进去

## 4. 每个 source set 的挑选标准

对每个 cluster，按下面标准挑 5 题。

### 标准 1：同一 dominant reasoning pattern

5 题必须都属于同一个 `reasoning_label`。

这一点不能妥协。
否则你后面做 consolidation 时，根本不知道是在总结一个 pattern，还是把几种不同 pattern 混成一句空话。

### 标准 2：表面形式不能过于重复

虽然它们共享同一种 reasoning pattern，但不应该只是同题改写。

要尽量避免：

- 同样的实体结构
- 同样的问句模板
- 同样的表面目标关系

否则生成的 consolidation 很可能只是模板化总结，没有可迁移价值。

### 标准 3：尽量 `entity-disjoint`

第一轮就要尽量控制：

- 5 题之间的核心实体不要高度重叠

这样做有两个好处：

- 避免 source set 本身泄漏过多表面线索
- 逼 consolidation 更偏向 reasoning structure，而不是实体记忆

### 标准 4：难度不要极端失衡

如果 5 题里有 1 题特别复杂、4 题特别简单，consolidation 容易被复杂题或简单题单独带偏。

第一轮不需要严格量化难度，但你至少要避免：

- 一半以上题明显复杂得多
- 或者其中一题完全不像同一层次的任务

### 标准 5：先可解释，再追求规模

第一轮 source set 的核心标准不是“覆盖尽可能多数据”，而是：

- 你自己能解释为什么这 5 题应该被放进同一组

如果你说不清这组的共享 pattern 是什么，这组就不该进 pilot。

## 5. 实际挑选流程

### Step 1. 按 cluster 分组

先把 `taxonomy.csv` 里所有 `keep` 的题按 `reasoning_label` 分开。

得到类似：

- `bridge` candidates
- `comparison` candidates
- `temporal` candidates
- `distractor-heavy` candidates

### Step 2. 先筛掉边界题

把这些题里 `note` 明显显示犹豫的先拿掉。

比如：

- `drop: bridge and comparison equally strong`
- `dominant pattern unclear`
- `bridge but temporal also strong`

第一轮宁可先不用。

### Step 3. 选“最干净的 5 题”

对每个 cluster，优先选：

- pattern 清楚
- 表面形式有差异
- 实体不重合
- 你自己看了会觉得“这 5 题放在一起是合理的”

不要从“最有趣的题”开始选，而是从“最稳定的题”开始选。

### Step 4. 为每个 source set 写一句定义

选完一组后，你必须能写一句非常短的定义：

- `bridge via intermediate entity lookup`
- `comparison after retrieving two attributes`
- `temporal ordering across linked events`

如果写不出来，说明这组还不够干净。

## 6. 第一轮 source set 完成后的检查

每个 source set 选完后，做 3 个检查。

### 检查 1：共享 pattern 是否清楚

问自己：

- 这 5 题真正共享的是什么？

如果答案只能是：

- “它们感觉差不多”

那不够。

### 检查 2：是否太像

问自己：

- 如果我把其中 5 题缩写出来，看上去是不是像 5 个近似改写版本？

如果是，说明这组过于单一。

### 检查 3：能不能支撑后续 artifact

问自己：

- 这组能不能生成一个像样的 `episodic_trace`？
- 这组能不能生成一个不空泛的 `cross_episode_consolidation`？

如果你预感 consolidation 只会写出一句废话，这组也不该进入第一轮 pilot。

## 7. 第一轮应该产出什么

第一轮做完后，至少要更新 [source_sets.csv](./source_sets.csv)。

每行至少填：

- `source_set_id`
- `cluster`
- `member_task_ids`
- `entity_disjoint`
- `lexical_overlap_note`
- `note`

`note` 推荐写法：

- `clean bridge set, diverse surface forms`
- `comparison set, one borderline item`
- `temporal set, low overlap`

另外，在 [notes.md](./notes.md) 里补一小段总结：

- 哪些 cluster 足够稳定，可以先做 pilot
- 哪些 cluster 当前还太混乱，不应急着进入 source set

## 8. 第一轮 source set 的成功标准

第一轮 source set 挑选成功，不是指“挑得很多”，而是：

- 至少得到 2 到 3 个你自己敢拿去做 pilot 的干净 source sets
- 每个 set 的共享 pattern 都能被一句话说清
- 你不担心它们只是表面模板重复
- 你觉得它们足以生成有差异的 `episodic_trace` 和 `consolidation`

## 9. 最重要的提醒

第一轮 source set 不是为了“全面覆盖数据”，而是为了：

**先构造出少量、干净、可解释的 source memory units。**

只要这一步做稳，后面的 pairing、artifact 生成和 pilot run 才有意义。
