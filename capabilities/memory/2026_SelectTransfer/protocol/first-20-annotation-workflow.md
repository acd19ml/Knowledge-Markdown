# First 20 Annotation Workflow

这份文件只服务于第一轮标注。

目标不是把 taxonomy 一次做完，而是先回答两个问题：

- 这套标签规则能不能稳定使用
- 后续的 `Relevant / Irrelevant` pairing 有没有可能做得住

因此，第一轮只做 **20 题** 就够。

建议分配：

- `HotpotQA`：10 题
- `2WikiMultiHopQA`：10 题

## 1. 先准备工作表

填写：

- [taxonomy.csv](./taxonomy.csv)

参考规则：

- [taxonomy_guideline.md](./taxonomy_guideline.md)

这一轮先填这几列：

- `task_id`
- `dataset`
- `question`
- `reasoning_label`
- `keep_drop`
- `note`

不要一开始就在 `note` 里写太长，只写最关键判断依据。

## 2. 抽题方式

不要手工挑“看起来有意思”的题。

第一轮建议：

- 从 `HotpotQA` 随机取 10 题
- 从 `2WikiMultiHopQA` 随机取 10 题

如果你已经有固定 split，也可以按顺序取前 10 题，但不要主观筛题。

第一轮的目的是测试 taxonomy 的可用性，不是证明某个假设。

## 3. 每题的实际标注步骤

对每道题，按固定顺序走，不要凭感觉直接拍标签。

### Step 1. 先读 question

只看题目，先形成一个初判：

- 它是在比较两个对象吗？
- 它是在判断时间顺序吗？
- 它必须通过中间实体串起来吗？
- 还是它最主要的难点在抗干扰？

这一步先不要急着下最终标签。

### Step 2. 想一遍“如果我来做，这题主要难在哪”

要问的不是题目表面长什么样，而是：

**如果不做哪一种 reasoning，这题就解不出来？**

### Step 3. 按顺序判断

严格按下面顺序判断：

1. `comparison`
2. `temporal`
3. `bridge`
4. `distractor-heavy`
5. 如果还不清楚，直接 `drop`

这个顺序不是理论真理，只是为了让第一轮标注更稳定。

### Step 4. 写 `note`

每题 `note` 最多一句话，类似：

- `comparison after retrieving two attributes`
- `temporal ordering is dominant`
- `bridge via intermediate entity`
- `drop: bridge and comparison equally strong`
- `drop: dominant pattern unclear`

`note` 的目的不是解释全部细节，而是让你未来回看时知道当初为什么这样标。

## 4. 第一轮想看到什么现象

20 题做完后，你主要看这些信号：

- 大多数题能不能自然落进某一类
- 某一类是不是几乎永远标不到
- 有没有很多题会在 `bridge` / `comparison` 之间摇摆
- `drop` 比例是不是太高

经验判断：

- 如果 20 题里有很多题都让你非常犹豫，这套 taxonomy 还不稳
- 如果 `drop` 只有少量，通常是健康的
- 如果 `distractor-heavy` 被你用成兜底标签，说明规则没收住

## 5. 第一轮做完后立刻回看

不要马上继续标更多题。

做完 20 题后，先做三件事。

### 回看 1. 统计分布

看一下：

- 每个标签各有多少题
- `drop` 有多少题
- 哪些题的 `note` 里出现了 `equally strong` 或 `unclear`

### 回看 2. 找最犹豫的 5 题

把最难判的 5 题拿出来，看它们共同卡在哪：

- `bridge vs comparison`
- `temporal vs bridge`
- taxonomy 规则不清
- 题目本身过于混合

### 回看 3. 隔一天重标 5 题

第二天从这 20 题里随机抽 5 题重新标一次。

如果你自己隔一天都经常改标签，说明规则还不够稳定，不要急着扩大样本。

## 6. 第一轮完成后的判断标准

可以进入下一步的信号：

- 大多数题都能比较自然归类
- `drop` 比例不高
- 你自己重标时大部分标签不变
- 歧义主要集中在少数边界 case，而不是全面混乱

不建议进入下一步的信号：

- 很多题都感觉“哪个都像”
- `distractor-heavy` 用得过多
- 你隔一天重标时经常推翻自己
- 两个 benchmark 的题型分布差异大到这套 taxonomy 很难共用

## 7. 第一轮结束后应输出什么

至少产出两样东西：

1. 填过的 [taxonomy.csv](./taxonomy.csv)
2. 一小段总结，写进 [notes.md](./notes.md)

总结只需要回答：

- 哪些标签最常见
- 哪些边界 case 最麻烦
- `drop` 比例大概多少
- taxonomy 需不需要改

## 8. 最重要的提醒

第一轮标注不要追求“正确率”。

当前没有 ground truth。你真正要验证的是：

**这套规则是否稳定、可重复、可继续扩大。**
