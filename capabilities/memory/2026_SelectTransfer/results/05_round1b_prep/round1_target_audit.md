# Round 1 Target Audit

Date: 2026-04-11

这份文件的目的不是重写 Round 1 结果，而是为 `Round 1b` 做最小必要的 target / scoring 审计。

核心原则：

- 先审计 measurement，再做下一轮 prompt 诊断
- 不把 benchmark 噪声和 prompt 问题混在一起
- `Round 1b` 先跑一个 `smoke subset`，不是立刻 full rerun

## 审计结论

### 1. 需要从下一轮 aggregate 指标中临时剔除的 case

#### `wiki_dev_0092`

- 当前 gold: `Paris`
- 当前 no-memory 预测: `Alexandria, Egypt`
- 问题：context 中明确写了 `Alex Joffé was born ... in Alexandria, Egypt`，而不是 `Paris`
- 结论：这不是一个干净的 metric case

处理建议：

- `Round 1b` 中保留该 case 作为 **qualitative diagnostic case**
- 不纳入默认 aggregate EM / F1
- 直到单独完成 benchmark/gold 审核前，不把它当成正式 quantitative evidence

### 2. 需要双版本评分的 case

#### `wiki_dev_6083`

- 当前 gold: `Spanish`
- 当前所有条件预测: `Spain`
- 问题：这是 `country / demonym` 表述边界，不是明显的 reasoning failure

处理建议：

- `Round 1b` 保留 strict score
- 同时增加一个 `audit-adjusted note`，明确该 case 在语义上接近正确
- 先不要直接改 official score function；先在 analysis 层显式报告

### 3. 适合用来做 Round 1b smoke test 的 case

以下 6 个 case 足以覆盖当前最重要的诊断模式：

#### `wiki_dev_8896`

- 类型：movement case
- 用途：检查 `CoT / structured reasoning` 是否会让 memory influence 变得可解释

#### `wiki_dev_0092`

- 类型：output-type degradation + gold ambiguity
- 用途：检查 memory 是否仍然把回答从地点带偏到人名
- 说明：只做 qualitative，不进 aggregate

#### `wiki_dev_2639`

- 类型：divergent error path
- 用途：检查 irrelevant memory 是否仍会改变错误关系链

#### `wiki_dev_6083`

- 类型：scoring boundary case
- 用途：检查结构化输出是否能减少表述层级错误

#### `wiki_dev_7019`

- 类型：stable floor / wrong reasoning level
- 用途：检查加入 reasoning scaffold 后，模型是否会从 “奖项名” 与 “节庆名” 中做出更明确区分

#### `wiki_dev_10727`

- 类型：clean ceiling control
- 用途：检查新 prompt 不会破坏原本 already-correct case

## 暂不优先进入 smoke subset 的 case

### `wiki_dev_0123`

- 也是 ceiling case，但和 `wiki_dev_10727` 相比信息增益更低

### `wiki_dev_10378`

- clean ceiling，可留作 full rerun 时再纳入

### `wiki_dev_12298`

- 是有效 floor case，但与 `wiki_dev_7019` 相比，当前更难区分是 reasoning 不足还是稳定错误 pattern
- 可以作为 smoke subset 备选，不是第一优先

### `wiki_dev_1379`

- 稳定错误，但目前信息增益低于 `wiki_dev_2639`

## Round 1b 的最小目标

`Round 1b` 不直接追求 selective transfer 的最终结论。

这一轮先回答三个更小的问题：

1. 新 prompt 是否能稳定诱发显式 reasoning，而不再是单行直答
2. memory 是否会在 reasoning text 中被显式引用、显式拒绝、或显式忽略
3. 新 scaffold 是否至少让部分 floor / movement case 变得更可解释

## Gate

只有在 smoke subset 上同时满足以下条件，才进入 full rerun：

- 至少大多数 run 不再是单行答案
- `## Final Answer` 可稳定解析
- 至少 2 个 case 出现可解释的 memory interaction

如果这三条不满足，先停在 prompt / parser diagnosis，不进入更大规模运行。
