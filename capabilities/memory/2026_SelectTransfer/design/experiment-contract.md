# Experiment Contract

这份文件定义 `2026_SelectTransfer` 项目中必须严格遵守的实验约定。

目的不是写一般性的“好习惯”，而是防止后续出现以下情况：

- 跑完实验才发现变量不止一个
- 结果无法追溯回具体 case
- 解释和结论超过实验实际 scope
- protocol 在过程中不断漂移，导致结果无法比较

配套模板：

- [experiment-round-template.md](./experiment-round-template.md)

## 核心原则

- 严谨
- 可追溯
- 可解释
- 可重复
- 单变量

## 1. 单变量原则

每一轮正式比较，只允许改变一个核心变量。

例如：

- 只改 `memory form`
- 或只改 `applicability judgment`

不能在同一轮对比里同时改：

- prompt
- memory artifact
- model
- retrieval
- decoding

只要多个关键变量一起变，结果就不再可解释。

## 2. 固定 setting 原则

同一轮实验中，以下内容必须固定：

- benchmark split
- source-target pairing
- model
- agent scaffold
- tools
- decoding params
- max steps
- source experience count

如果其中任意一项改变，这就不是同一轮受控比较。

## 3. Pairing 先于实验

`Relevant / Irrelevant` pairing 必须在实验开始前定义并落盘保存。

禁止以下做法：

- 先看结果，再说某些 pair 不合理
- 根据跑出来的效果回头调整 split

pairing protocol 必须先冻结，再运行条件。

## 4. Artifact 先检查后运行

任何 memory artifact 在进入正式 run 之前，都必须先人工检查。

至少确认：

- 不是空话
- 不是乱码
- 不泄漏答案
- 不只是表面重复

如果 artifact 本身不合格，则该轮实验无解释价值。

## 5. 先 pilot，后 full run

任何新条件、新指标、新 protocol，必须先经过小规模 pilot。

禁止：

- 第一次实现就直接跑全量 benchmark
- 没看 case 就直接汇总总分

pilot 的目标不是证明 hypothesis，而是确认 setup 能产出可解释现象。

## 6. 分 split 报告，禁止只看总平均

`Relevant Split` 和 `Irrelevant Split` 必须分别报告。

禁止只给：

- overall average

因为本项目研究的不是“memory 平均有没有帮助”，而是“memory 是否支持 selective transfer”。

## 7. 结果先描述现象，再解释原因

写结果时，先写：

- 观察到了什么现象

再写：

- 这些现象可能意味着什么

禁止把解释直接写成事实。

例如，不应直接写：

- `applicability judgment` 有效

而应写：

- 在当前 setup 下，judgment 条件在 `Irrelevant Split` 上出现了更少的 negative transfer

## 8. 成功 case 与失败 case 同样重要

每一轮至少保留：

- 1 到 2 个成功 case
- 1 到 2 个失败或 negative transfer case

禁止只挑“好看”的例子。

失败 case 往往比成功 case 更能暴露 setup 的真实问题。

## 9. 日志必须可追溯

每次 run 至少能追溯到：

- target task
- split
- condition
- source set
- artifact
- routing decision
- final output
- metrics

要求是：

**任何一个表格里的数字，都应该能追溯回原始 case。**

## 10. 不事后改定义

一旦某轮实验开始，以下定义不得在中途随意修改：

- taxonomy label 规则
- pairing 规则
- metrics 公式
- success / failure 判定方式

如果必须修改，必须：

- 停止当前轮次
- 开新版本
- 明确记录版本变化

## 11. 结论必须与 scope 匹配

实验得到的结论只能覆盖当前实际 scope。

例如，如果当前只测：

- `HotpotQA -> 2WikiMultiHopQA`
- near-transfer
- external text memory

那么结论不能扩写成：

- 某方法在所有 memory research 中都更优

最多只能写成：

- 在当前 near-transfer setting 下，观察到某种更稳定的 selective transfer 现象

## 12. 负结果先做 protocol diagnosis，再做理论解释

如果实验没效果，不能立刻下结论说：

- hypothesis 错了

必须先排查：

- pairing 是否不稳
- artifact 是否太差
- 条件是否没有真正拉开
- benchmark 是否不敏感

也就是说：

**负结果优先诊断 protocol，再解释理论。**

## 13. 每轮实验前先写“本轮回答什么，不回答什么”

每一轮实验开始前，必须先写清楚：

- 本轮只回答什么
- 本轮明确不回答什么

例如：

- 本轮只回答：`Cross-Episode Consolidation` 是否比 `Episodic Trace` 更支持 relevant split 上的稳定迁移
- 本轮不回答：更广泛的 generalization、parameter internalization、memory architecture 的终极优劣

这样做的目的是防止实验范围在写结果时无意扩大。

## 一句话约束

后续所有实验都必须满足：

**变量先收住，定义先冻结，artifact 先检查，split 分开报告，结论不越界。**
