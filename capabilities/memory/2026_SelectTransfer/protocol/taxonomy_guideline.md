# Taxonomy Guideline

用于填写 [taxonomy.csv](./taxonomy.csv)。

目标不是做一个完美的 reasoning taxonomy，而是建立一套足够稳定、可 defend、能支持 `Relevant / Irrelevant` pairing 的标注规则。

## CSV 字段说明

- `task_id`
  - 原 benchmark 中的样本 id
- `dataset`
  - 例如 `HotpotQA` / `2WikiMultiHopQA`
- `question`
  - 原题目文本，可保留简写版
- `reasoning_label`
  - 只允许填写一个主标签
- `keep_drop`
  - 只允许填写 `keep` 或 `drop`
- `note`
  - 记录边界 case、歧义来源、或为什么 drop

## 标注目标

每道题只标一个 **dominant reasoning pattern**。

这里要回答的不是：

- 这道题表面长什么样
- 这道题包含了多少种推理

而是：

- 如果要正确解这道题，哪一种 reasoning pattern 是主导性的

如果主导模式不清楚，这道题就不应该进入 pairing pool，应直接 `drop`。

## 标签定义

### 1. `bridge`

定义：

- 需要通过一个中间实体或中间事实，把两个信息点串起来，才能得到答案

典型特征：

- 问题本身往往看不到最终答案对应的实体
- 必须先找到一个中间节点，再继续往下查
- 核心难点是“连接”而不是“比较”

判断提示：

- 如果你解题时的关键步骤是“先找到 X，再通过 X 找到 Y”，优先考虑 `bridge`

### 2. `comparison`

定义：

- 需要先找到两个或多个候选对象的属性，再进行比较，最后得出答案

典型特征：

- 问题里常出现比较关系，如更早、更大、更多、同/不同
- 核心难点是把多个对象放在同一判断框架下比较

判断提示：

- 如果即使找到了所有事实，不做显式比较也无法回答，优先考虑 `comparison`

### 3. `temporal`

定义：

- 回答依赖事件时间顺序、时间关系或阶段先后

典型特征：

- 需要判断 before / after / during / first / later 等关系
- 核心难点是时间轴上的排序或定位

判断提示：

- 如果去掉时间信息，这题就失去主要难点，优先考虑 `temporal`

### 4. `distractor-heavy`

定义：

- 题目核心难点在于检索过程会遇到大量高相似度但无关的信息，需要强过滤

典型特征：

- 表面上像普通 multi-hop，但真正困难在于多个候选页面、实体或线索高度相似
- 核心难点不是桥接、比较或时间推理本身，而是抗干扰

判断提示：

- 如果这题最主要的失败风险是被相似但无关的信息带偏，且其他三类都不明显占主导，才标 `distractor-heavy`

## 标注顺序

为了减少随意性，按下面顺序判断：

1. 先问：是否明显是 `comparison`
2. 再问：是否明显是 `temporal`
3. 再问：是否明显是 `bridge`
4. 如果前三者都不主导，但抗干扰最强，再标 `distractor-heavy`
5. 如果仍然无法稳定判断，直接 `drop`

这个顺序不是理论真理，只是为了让标注更稳定。

## `keep` / `drop` 规则

标 `keep` 的条件：

- dominant reasoning pattern 清楚
- 题目文本足够完整，能支持后续 pairing
- 不是明显的多标签混合 case

标 `drop` 的条件：

- 两种以上 reasoning pattern 同样主导，难以区分主次
- 题目依赖的数据异常、文本不完整，或无法稳定判断
- 你自己在阅读后仍然无法解释“为什么它属于这个标签而不是另一个”

原则：

- 宁可 `drop` 一些边界题，也不要把不稳定的题硬塞进 taxonomy

## 边界 case 处理

### `bridge` vs `comparison`

如果题目既要先找到中间实体，又要比较两个对象：

- 如果真正难点在于“找到连接路径”，标 `bridge`
- 如果真正难点在于“拿到两个对象后做比较”，标 `comparison`

### `bridge` vs `temporal`

如果时间只是桥接中的一个属性，不是主导推理轴，标 `bridge`

如果必须围绕时间顺序组织整个推理过程，标 `temporal`

### `distractor-heavy` 与其他三类

`distractor-heavy` 不是兜底垃圾桶。

只有在以下条件同时满足时才用：

- 其他三类都不明显主导
- 题目真正主要的难点是抗干扰

否则优先标前三类之一。

## `note` 栏怎么写

`note` 不需要长，只要能留下关键判断依据。

推荐写法：

- `bridge via intermediate entity`
- `comparison after retrieving two attributes`
- `temporal ordering is dominant`
- `drop: bridge and comparison equally strong`
- `drop: dominant pattern unclear`

目的不是解释所有细节，而是让未来回看时知道当初为什么这样标。

## 标注一致性建议

第一轮先不要追求量，先做小样本一致性检查。

建议流程：

1. 先标 20 题
2. 隔一天重新看其中 5 到 10 题
3. 看自己是否会改标签
4. 如果频繁改标签，先修规则，再继续扩大样本

如果你后面有第二个人参与标注，也先对同一小批题做双人标注，再看分歧主要出在哪类边界 case。

## 当前原则

这套 taxonomy 的目标不是解释所有 multi-hop QA。

它只需要满足三点：

- 能稳定标注
- 能支持 pairing
- 能让 `Relevant / Irrelevant` 的定义更可 defend
