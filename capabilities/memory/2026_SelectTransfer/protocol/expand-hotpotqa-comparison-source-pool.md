# Expand HotpotQA Comparison Source Pool

这份文件只回答一个问题：

**当当前 sample 不足以构造 `comparison` source set 时，如何扩 `HotpotQA` 的 source-side candidate pool？**

这不是一般性的“再多抽点题”，而是一个带明确触发条件、明确停止条件、明确输出文件的定向扩池 workflow。

## 1. 什么时候需要执行这个 workflow

只有在出现下面这种情况时，才启动这份流程：

- 当前 `source benchmark = HotpotQA`
- 当前 `target benchmark = 2WikiMultiHopQA`
- 当前 `N = 5` 的 source set 约束不变
- 当前已经完成一轮 taxonomy 标注
- 但 `HotpotQA` 某个关键 cluster 的 `keep` 题数量不足 5

当前项目正好满足这个条件：

- `HotpotQA bridge` 足够先做一组 draft source set
- `HotpotQA comparison` 目前只有 2 题 `keep`
- 因此不能构造 `comparison` source set

这时不应该：

- 偷用 `2WikiMultiHopQA` 题来补 source
- 临时把 `N = 5` 改小
- 直接假装 `comparison` source set 不重要

正确做法是：

**定向扩 `HotpotQA` 的 `comparison` candidate pool。**

## 2. 这一步的目标

目标不是“重做整个 taxonomy”，而是用最小增量补足 source-side `comparison` coverage。

这一轮扩池只追求三件事：

- 找到足够多的新 `HotpotQA comparison` 候选题
- 用同一套 taxonomy 规则完成增量标注
- 最终构造至少 1 个可用的 `comparison` source set

更具体地说，当前已有：

- 2 个 `HotpotQA comparison keep`

最低目标是补到：

- 至少 5 个 `HotpotQA comparison keep`

更稳的目标是补到：

- 6 到 8 个 `HotpotQA comparison keep`

原因很简单：

- 只补到恰好 5 个，几乎没有替换空间
- 有 1 到 3 个 buffer，后面构 set 时才有选择余地

## 3. 这一轮不做什么

这一步明确 **不** 做下面这些事：

- 不重新定义 source-target setting
- 不改 `N = 5`
- 不改 taxonomy 标签体系
- 不重新抽整个 20-task rehearsal sample
- 不把 target-side 题挪成 source-side 题
- 不在这一轮加入新模型、新 prompt、新 memory condition

这一轮只回答一个问题：

**如何在不破坏当前设计前提的情况下，补足 `HotpotQA comparison` source pool。**

## 4. 数据来源

数据来源固定为：

- `HotpotQA` 的当前使用 split

优先建议：

- 和现有 rehearsal 使用同一 split
- 如果当前 rehearsal 来自 `HotpotQA dev`，这一轮也继续从 `HotpotQA dev` 扩

原因：

- 避免在 source expansion 时又引入 split confound
- 保持 source-side candidate pool 的来源一致

## 5. 扩池策略

这一步不要再用“完全随机 10 题”的思路。

原因是：

- 第一轮 random 20 的目标是 taxonomy sanity check
- 现在的目标已经变成 source-side cluster repair

所以这一轮应该采用：

**定向预筛 + 小批量增量标注**

### 核心原则

- 先用 benchmark 自带 metadata 或可见模式做 `comparison` 预筛
- 再进入人工 taxonomy 标注
- 最后只把通过统一规则的题纳入 source-side candidate pool

## 6. 推荐批量大小

不要一下扩太多。

当前推荐一批：

- 新增 12 到 15 个 `HotpotQA comparison` 候选题

为什么是这个量：

- 当前已有 2 个 `comparison keep`
- 理论上还缺 3 个
- 但考虑到边界题、drop、近重复、实体重合，必须留 buffer

经验上：

- 只补 3 到 5 个候选题，太冒险
- 一口气补 40 个，又会把工作量拉回全量标注

所以：

- 第一批 12 到 15 个最合适

## 7. 候选题怎么找

优先顺序如下。

### 方法 A：优先用 HotpotQA 原始 `type = comparison`

如果原始数据项里有 `type` 字段，优先从：

- `type = comparison`

里取候选题。

这不是直接拿来当最终标签，而只是做预筛。

原因：

- 这能显著提高命中率
- 同时不会替代你自己的 taxonomy

### 方法 B：如果没有 metadata，就按题面模式预筛

如果当前加载方式拿不到 `type`，就按题面优先找这类模式：

- `Which ... , A or B?`
- `Was A or B ... first / earlier / later / older / younger?`
- `What is the shared ... between A and B?`
- `Which of the two ...`

注意：

- 这仍然只是预筛
- 最终仍要按你自己的 taxonomy 标注

## 8. 候选题过滤规则

候选题进入增量标注前，只做最小必要过滤。

保留：

- 清楚是 multi-hop QA 的 comparison-looking 题
- 题目文本完整
- 能访问支撑信息

过滤掉：

- 文本异常或损坏
- 事实上不是 comparison，而只是表面像比较
- 和当前已有 `HotpotQA comparison keep` 几乎同模板、同实体结构的近重复题

这里要注意：

- 不要因为“这题看起来难”就过滤
- 不要因为“这题不是最典型”就过滤
- 但要避免把 5 个几乎同模板的题全塞进来

## 9. 增量标注怎么做

这一步仍然使用现有：

- [taxonomy_guideline.md](./taxonomy_guideline.md)

不要另起一套 comparison 专用规则。

### 标注要求

每个新增候选题仍然要填：

- `reasoning_label`
- `keep_drop`
- `note`

### 标注判断重点

重点不是“它是不是看起来像 comparison”，而是：

- 如果拿到全部事实后，是否必须做显式比较才能回答？

如果答案是 yes，优先标：

- `comparison`

如果它需要先桥接、但真正主导难点仍是最终比较，也仍然可以标：

- `comparison`

如果你自己仍然觉得：

- `bridge` 和 `comparison` 同样主导

那就：

- `drop`

宁可少要一点，也不要把边界题硬塞进 source pool。

## 10. 新数据写到哪里

这一步不要新开第二份 taxonomy 主表。

推荐做法：

### 主工作表

继续使用：

- [pilot/taxonomy.csv](../pilot/taxonomy.csv)

把新增的 `HotpotQA comparison` 候选题追加进去。

### 配套记录

同时在：

- [pilot/notes.md](../pilot/notes.md)

记录这是一轮 `source pool expansion`，并明确写：

- 扩了多少题
- 预筛依据是什么
- 最后新增了多少 `comparison keep`

### 原始中间产物

如果这一轮用了 notebook 或脚本筛选，原始输出建议放到：

- `results/02_hotpotqa_comparison_expansion/`

例如：

- `candidate_batch_raw.csv`
- `candidate_batch_full.json`
- `02_hotpotqa_comparison_expansion.ipynb`

这样 working table 和 raw output 分开，不会混。

## 11. 什么时候停止

不要无限扩。

这一轮可以停止的条件是：

### 停止条件 A：已经足够构造 set

当你达到下面任一条件时，可以停止：

- `HotpotQA comparison keep >= 5`，且这 5 题足够干净
- 更稳的是：`HotpotQA comparison keep >= 6`，能留一点替换空间

### 停止条件 B：连续扩池但收益太低

如果你已经做了两小批扩池，例如：

- 第一批 12 到 15 题
- 第二批再补 8 到 10 题

但 `comparison keep` 仍然很难稳定增加，那不要继续机械扩。

这时要停下来检查：

- taxonomy 对 comparison 是否过严
- 当前 split 的 comparison 本来就稀疏
- `N = 5` 是否对课程项目来说过于刚性

## 12. 这一轮完成后的最小产出

这一轮做完后，最少应该更新四样东西：

### 1. `pilot/taxonomy.csv`

新增 comparison 候选题及其标注结果。

### 2. `pilot/source_sets.csv`

如果条件满足，新增：

- `hp_comparison_set_01`

### 3. `pilot/notes.md`

补一条 expansion log，说明：

- 为什么扩
- 扩了多少
- 新增多少 `comparison keep`
- 最终是否足够构 set

### 4. `results/02_hotpotqa_comparison_expansion/`

保存这一轮的 raw outputs，而不是只留最终表。

## 13. 一个可执行的最小版本

如果你现在就要开始做，最小版本直接按这个顺序：

1. 从当前 `HotpotQA` 使用 split 中预筛 15 个 `comparison` 候选题
2. 做最小过滤，去掉异常项和明显近重复
3. 把这 15 题追加进 [pilot/taxonomy.csv](../pilot/taxonomy.csv)
4. 按现有 taxonomy 规则逐题标注
5. 看 `HotpotQA comparison keep` 是否能补到至少 5
6. 如果可以，构造 `hp_comparison_set_01`
7. 如果还不够，再决定是否做第二小批扩池

## 14. 最重要的提醒

这一轮扩池的意义不是“把数据做大”，而是：

**在不破坏当前实验设计的前提下，补齐 source-side comparison coverage。**

如果这一步做稳，后面的 pairing 和 pilot 才不会因为 source-side cluster 缺失而天然失衡。
