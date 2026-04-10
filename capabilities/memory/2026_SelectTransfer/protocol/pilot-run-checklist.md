# Pilot Run Checklist

这份文件只回答一个问题：

**在正式开始第一批 pilot run 之前，要检查什么？**

目标不是追求“万无一失”，而是确保当前 setup 已经足够干净，值得进入第一轮实验。

## 1. 使用方式

在开始跑第一批条件之前，按下面顺序检查。

如果某一项明显不过关，不要急着进入 run 阶段，先回去修：

- taxonomy
- source sets
- pairing
- artifact 质量

## 2. Taxonomy 检查

### 检查项

- `taxonomy.csv` 已经有第一轮标注结果
- 大多数题都有清晰的 `reasoning_label`
- `drop` 比例没有高到说明规则失效
- 你自己重标的小样本没有大幅改标签

### 通过标准

- 至少有一批 `keep` 样本你自己觉得标签稳定
- 边界 case 集中在少数模式，而不是全面混乱

### 不通过信号

- 你隔一天重标经常推翻自己
- 很多题都只能靠主观感觉硬判
- `distractor-heavy` 被用成兜底标签

## 3. Source Set 检查

### 检查项

- [source_sets.csv](./source_sets.csv) 已经有第一批 source sets
- 每个 source set 只对应一个清晰 cluster
- 每个 source set 都能用一句话解释共享 pattern
- set 内部不是近似重复题堆在一起

### 通过标准

- 至少有 2 到 3 个你愿意直接拿去做 pilot 的干净 source sets
- 这些 set 看起来既共享 structure，又保留表面多样性

### 不通过信号

- 某个 set 只是 5 个几乎一样的题
- 你很难解释为什么这 5 题应该在一组
- 你预感 `cross_episode_consolidation` 只会生成空话

## 4. Pairing 检查

### 检查项

- [pairing_table.csv](./pairing_table.csv) 已经有第一批 pairs
- relevant pairs 的匹配理由清楚
- irrelevant pairs 的不匹配理由清楚
- 没有明显 entity overlap 或 answer leakage

### 通过标准

- relevant pairs 看起来理论上应该能帮助 target task
- irrelevant pairs 看起来不该自然帮助 target task
- 每条 pair 都能用一句 `pairing_note` 解释

### 不通过信号

- 你解释 irrelevant pair 时总会说“其实也可能有帮助”
- relevant / irrelevant 的区别主要来自 topic 差异，而不是 reasoning pattern 差异
- 你已经开始依赖事后解释 pair 是否合理

## 5. Artifact 检查

### 检查项

- 已为第一批 source sets 生成：
  - `episodic_trace`
  - `cross_episode_consolidation`
- 你已经人工读过这些 artifacts

### 通过标准

- `episodic_trace` 不是纯噪声堆积
- `cross_episode_consolidation` 不是空泛总结
- 两种 artifact 体现出不同 memory form

### 不通过信号

- `episodic_trace` 太乱，几乎无法直接用
- `consolidation` 看起来像泛化废话
- 两种 artifact 读起来几乎没有区别

## 6. 条件设计检查

### 第一批 pilot 建议条件

- `No Memory`
- `Episodic Trace`
- `Cross-Episode Consolidation`

只有当这三种条件已经能产生可解释现象时，再加入：

- `Cross-Episode Consolidation + Applicability Judgment`

### 通过标准

- 你已经明确第一轮不是跑完整矩阵，而是先验证 setup 是否 working

### 不通过信号

- 一开始就想把所有变体全跑完
- 在 setup 还不稳定时就引入太多条件

## 7. 指标检查

### 第一批 pilot 至少记录

- `EM`
- `F1`
- split (`relevant` / `irrelevant`)
- condition
- target task id
- source set id
- note

如果已经进入 judgment 条件，再额外记录：

- routing decision
- whether memory was attached

### 通过标准

- 你能明确说出每个指标服务于什么判断

### 不通过信号

- 记录了很多字段，但你自己也不知道后面怎么看
- 只看最终 EM/F1，完全不看 split 和 condition

## 8. 结果解释准备检查

在跑之前，你至少要写好一版“现象 -> 解释 -> 下一步”的对照表。

例如：

- relevant 涨、irrelevant 不掉 -> memory strategy 可能有 selective transfer value
- relevant 涨、irrelevant 也掉 -> memory 可能被乱用
- relevant 不涨、irrelevant 也不掉 -> setup 可能不敏感，先查 pairing / artifact
- 只有 judgment 稳 -> 后续更应研究 gating / applicability

### 通过标准

- 你已经提前想好不同结果分别意味着什么

### 不通过信号

- 打算等结果出来以后再现编解释

## 9. 第一批 pilot run 的最小规模

建议：

- `Relevant Split`：10 对
- `Irrelevant Split`：10 对

如果 setup 还不够稳，可以先缩成：

- 6 对 relevant
- 6 对 irrelevant

第一轮不要追求统计显著性，只追求：

- setup 能不能跑通
- 现象能不能解释
- negative transfer 能不能被观测到

## 10. Go / No-Go 标准

### 可以进入 pilot run

- taxonomy 基本稳定
- 至少有 2 到 3 个干净 source sets
- relevant / irrelevant pairing 已经能自圆其说
- artifacts 已人工检查通过
- 第一轮条件和指标已经收住

### 不建议进入 pilot run

- taxonomy 还在频繁改规则
- source sets 质量不稳
- pairing 很多都说不清
- artifact 看起来明显不可用

## 11. 最重要的提醒

第一批 pilot run 的目标不是“证明 hypothesis”，而是：

**确认这套 setup 能产出可解释的 selective-transfer 现象。**

如果这一点还做不到，就先不要急着扩大实验规模。
