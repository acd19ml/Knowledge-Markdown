# Experiment Round Template

每开始一轮新实验前，先复制这份模板，生成一个新的 round 说明文件。

目的不是写长文，而是强制回答：

- 这轮只改什么变量
- 这轮固定什么
- 这轮回答什么，不回答什么

如果这些问题写不清楚，就不要开始跑。

---

## Round Name

例如：

- `round_01_memory_form_comparison`
- `round_02_add_applicability_judgment`

## Date

填写开始日期。

## Objective

这轮实验只想回答什么问题？

要求：

- 只写一个核心问题
- 不要把多个问题混在一起

## Variable Being Changed

这轮唯一允许变化的核心变量是什么？

例如：

- `memory form`
- `applicability judgment`

如果这里写了两个以上变量，说明这轮设计不合格。

## Fixed Conditions

这轮必须固定不变的内容：

- benchmark split
- source-target pairing
- model
- agent scaffold
- tools
- decoding params
- max steps
- source experience count

如果有任何项会变，必须明确写出来，并说明为什么这不破坏本轮比较。

## Conditions Compared

列出本轮对比的所有条件。

例如：

- `No Memory`
- `Episodic Trace`
- `Cross-Episode Consolidation`

要求：

- 条件数量尽量少
- 每个条件都必须服务于同一个核心问题

## Inputs Used

说明这轮使用的输入资源：

- taxonomy version
- source set version
- pairing table version
- artifact version

这里的目标是保证可追溯。

## Metrics

这轮主要看哪些指标？

至少写：

- primary metrics
- secondary metrics

并说明：

- 哪个指标对应什么判断

## What This Round Will Answer

明确写出：

- 这轮实验跑完后，允许得出的结论是什么

例如：

- 在当前 near-transfer setting 下，`Cross-Episode Consolidation` 是否比 `Episodic Trace` 在 `Relevant Split` 上更稳定

## What This Round Will NOT Answer

明确写出：

- 这轮实验不回答什么

例如：

- 不回答更广泛的 generalization
- 不回答 parameter internalization
- 不回答 memory architecture 的最终优劣

这一栏必须写，不允许留空。

## Pre-Run Checklist

开始之前确认：

- taxonomy 已冻结
- pairing 已冻结
- artifacts 已人工检查
- metrics 已定义
- logging 字段已确认
- result interpretation table 已准备

如果其中任一项未完成，不进入 run。

## Notes

写本轮实验开始前的补充说明。
