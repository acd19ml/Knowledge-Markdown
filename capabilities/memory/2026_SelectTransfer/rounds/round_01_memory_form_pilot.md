# Experiment Round

## Round Name

`round_01_memory_form_pilot`

## Date

2026-04-10

## Objective

在第一批 clean pairs 上，初步观察不同 `memory form` 是否会带来可解释的 selective-transfer 现象。

这轮只回答一个问题：

**在不引入 `applicability judgment` 的前提下，`Episodic Trace` 与 `Cross-Episode Consolidation` 是否在 `Relevant Split` / `Irrelevant Split` 上表现出不同趋势？**

## Variable Being Changed

这轮唯一允许变化的核心变量：

- `memory form`

具体体现在：

- `No Memory`
- `Episodic Trace`
- `Cross-Episode Consolidation`

这轮不引入：

- `applicability judgment`
- 新 retrieval 机制
- 新 prompt 结构
- 新模型

## Fixed Conditions

这轮必须固定：

- benchmark setting：`HotpotQA -> 2WikiMultiHopQA`
- target task 集合
- source-target pairing
- model
- agent scaffold
- tools
- decoding params
- max steps
- source experience count：`N = 5`

## Conditions Compared

- `No Memory`
- `Episodic Trace`
- `Cross-Episode Consolidation`

比较目标：

- 看 memory form 是否在 matched / mismatched 条件下呈现不同效应
- 不比较 deployment policy

## Inputs Used

本轮使用第一批冻结后的归档版本：

- `pilot/archive/taxonomy_round1.csv`
- `pilot/archive/source_sets_round1.csv`
- `pilot/archive/pairing_table_round1.csv`
- `pilot/archive/notes_round1.md`
- `artifacts/` 中第一轮：
  - `episodic_trace`
  - `cross_episode_consolidation`

版本命名规则见：

- [protocol/versioning-convention.md](../protocol/versioning-convention.md)

如果这些输入中的任意一个还未冻结到 `archive/`，本轮不开始。

## Metrics

### Primary Metrics

- `EM`
- `F1`

### Secondary Metrics

- `relevant gain`
- `irrelevant delta`
- `negative transfer rate`

### Process Notes

额外记录：

- target task id
- source set id
- split
- condition
- token usage
- failure status
- case note

## What This Round Will Answer

这轮实验结束后，允许回答：

- 在当前 near-transfer setting 下，不同 `memory form` 是否已经能在第一批 clean pairs 上表现出可解释差异
- `Cross-Episode Consolidation` 是否比 `Episodic Trace` 更有可能在 `Relevant Split` 上提供稳定帮助
- 两种 memory form 是否会在 `Irrelevant Split` 上表现出不同程度的 negative transfer

## What This Round Will NOT Answer

这轮不回答：

- `applicability judgment` 是否有效
- deployment / gating 是否比 `memory form` 更重要
- 更广泛的 cross-domain generalization
- parameter internalization
- memory architecture 的最终优劣

## Pre-Run Checklist

开始前必须确认：

- [ ] taxonomy 已冻结
- [ ] pairing 已冻结
- [ ] source sets 已冻结
- [ ] artifacts 已人工检查
- [ ] 三个条件的 prompt scaffold 一致
- [ ] logging 字段已确认
- [ ] 结果解释表已提前写好

只要有一项未完成，不进入 run。

## Suggested Scale

第一轮只做小规模 pilot：

- `Relevant Split`：6 到 10 对
- `Irrelevant Split`：6 到 10 对

目标不是追求统计显著性，而是判断：

- setup 是否 working
- 现象是否可解释
- negative transfer 是否可被观测

## Success Signal

这轮如果成功，应至少看到以下之一：

- `Relevant Split` 上 memory 条件相对 `No Memory` 有清晰帮助趋势
- `Irrelevant Split` 上某种 memory form 更容易出现误用
- `Episodic Trace` 与 `Cross-Episode Consolidation` 在 case 级别已经表现出不同模式

## Failure Signal

这轮如果失败，不先下理论结论，先检查：

- taxonomy 是否不稳
- pairing 是否不干净
- artifact 是否质量过低
- 条件之间是否没有真正拉开

## Notes

这轮是整个项目的第一个真正实验轮次。

它的作用不是直接给出最终结论，而是验证：

- 当前 project framing 是否能落成可解释实验
- `memory form` 这个变量是否值得继续深入
