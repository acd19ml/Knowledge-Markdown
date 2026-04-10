# Experiment Round

## Round Name

`round_01b_prompt_diagnosis`

## Date

2026-04-11

## Objective

在保持 `model / source set / pairing / artifacts` 不变的前提下，只修改 prompt scaffold，检查：

1. 模型是否开始输出可解析的显式 reasoning
2. memory interaction 是否从隐式扰动变成可观察行为

这轮不是为了直接给出新的 selective-transfer 结论，而是为了判断：

**Round 1 的主要 bottleneck 到底是不是 prompt / measurement。**

## Variable Being Changed

这轮唯一允许变化的核心变量：

- prompt scaffold

具体变化：

- 从 `## Answer` 单段式输出
- 改为 `## Reasoning` + `## Final Answer` 的结构化输出

## Fixed Conditions

这轮必须固定：

- benchmark setting：`HotpotQA -> 2WikiMultiHopQA`
- source sets：Round 1 frozen archive
- pairing：Round 1 frozen archive
- model：`Qwen/Qwen3.5-9B`
- artifacts：Round 1 frozen artifacts
- decoding params
- source experience count：`N = 5`

## Conditions Compared

仍然保留 Round 1 的三个条件：

- `No Memory`
- `Episodic Trace`
- `Cross-Episode Consolidation`

但这里的主问题不是比较哪种 memory form 更好，而是看：

- 新 scaffold 是否让 memory 的使用方式变得可观察

## Inputs Used

本轮使用：

- [pilot/archive/taxonomy_round1.csv](../pilot/archive/taxonomy_round1.csv)
- [pilot/archive/source_sets_round1.csv](../pilot/archive/source_sets_round1.csv)
- [pilot/archive/pairing_table_round1.csv](../pilot/archive/pairing_table_round1.csv)
- [artifacts/hp_bridge_set_01/episodic_trace.md](../artifacts/hp_bridge_set_01/episodic_trace.md)
- [artifacts/hp_bridge_set_01/cross_episode_consolidation.md](../artifacts/hp_bridge_set_01/cross_episode_consolidation.md)
- [artifacts/hp_comparison_set_01/episodic_trace.md](../artifacts/hp_comparison_set_01/episodic_trace.md)
- [artifacts/hp_comparison_set_01/cross_episode_consolidation.md](../artifacts/hp_comparison_set_01/cross_episode_consolidation.md)
- [results/05_round1b_prep/round1_target_audit.csv](../results/05_round1b_prep/round1_target_audit.csv)
- [protocol/pilot-prompt-scaffold-round1b.md](../protocol/pilot-prompt-scaffold-round1b.md)

## Metrics

### Primary Metrics

- `EM`
- `F1`

### Process Metrics

- `reasoning_present`
- `final_answer_present`
- `memory_reference_type`
- `parse_success`

## What This Round Will Answer

这轮允许回答：

- prompt scaffold 是否是 Round 1 的主要 bottleneck
- 模型是否开始显式使用或显式拒绝 memory
- 是否值得在相同模型下继续 full rerun

## What This Round Will NOT Answer

这轮不回答：

- 最终的 selective transfer 结论
- 更强模型是否一定更好
- `applicability judgment` 是否有效

## Pre-Run Checklist

开始前必须确认：

- [ ] target audit 已完成
- [ ] smoke subset 已冻结
- [ ] 新 answer extractor 已实现
- [ ] `reasoning_present / final_answer_present / memory_reference_type` logging 字段已定义
- [ ] 新 scaffold 与旧 scaffold 的差异只在结构化 reasoning 上

## Suggested Scale

先只做 `smoke subset`：

- 6 个 target task
- 3 个条件
- 2 个 split

总共 36 runs

## Success Signal

只有同时满足以下条件，才建议 full rerun：

- 大多数 run 不再是单行直答
- `## Final Answer` 可稳定解析
- 至少 2 个 case 出现可解释的 memory interaction

## Failure Signal

如果以下任一情况出现，就停止 full rerun：

- 仍然大量单行直答
- reasoning 是空话，不引用 context / memory
- parse failure 太高

## Notes

这轮是一个严格的 protocol diagnosis round。

如果它失败，下一步优先考虑：

- 换模型
- 而不是继续在同一 scaffold 上做更多 full runs
