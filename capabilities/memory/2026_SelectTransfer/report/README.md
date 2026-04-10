# report/

这一层用于整理可直接写入课程 `progress report` 的文字素材。

它和其他目录的分工是：

- `design/` 回答：项目为什么这样定义
- `protocol/` 回答：实验应该怎么做
- `pilot/` 回答：当前具体做到了哪里
- `report/` 回答：这些过程如何被写成对外可读、可提交的进展叙述

## 当前文件

- [progress-report-draft.md](./progress-report-draft.md)
  - 可直接用于 `progress report` 的段落草稿（写于 taxonomy + source-set feasibility 阶段，尚未包含 pilot 结果）
- [progress-report-round1-pilot.md](./progress-report-round1-pilot.md)
  - Round 1 pilot 完整结果分析：60 runs 的 case-level 诊断、sensitivity deficit 根因分析、下一步方向建议
  - 重点写：
    - 问题如何收缩
    - protocol 如何建立
    - 当前真实发现是什么
    - 这些发现如何改变设计决策
    - 下一步是什么
- [progress-report-round1b-prompt-diagnosis.md](./progress-report-round1b-prompt-diagnosis.md)
  - Round 1b prompt diagnosis 结果分析：6 个 smoke targets 上的 structured reasoning 输出、memory use/reject 证据、以及为什么当前还不能直接下 selective transfer 结论
  - 重点写：
    - prompt scaffold 是否修复了 Round 1 的单行直答问题
    - process-level evidence 是否出现
    - 哪些 case 出现了 memory-induced degradation / recovery
    - 为什么下一步应先收紧 scoring、process analysis 与 case role reclassification
- [../results/05_round1b_prep/round1c_role_aware_smoke_summary.md](../results/05_round1b_prep/round1c_role_aware_smoke_summary.md)
  - Round 1c 前置摘要：把 Round 1b 的 run-level 结果按 `case role` 重组，明确哪些 case 只能做 process sanity、哪些是 artifact / format / boundary case
  - 重点写：
    - 哪些 runs 已经不该进入 transfer aggregate
    - 哪些 case 仍可保留作 process-level signal
    - 为什么下一轮应先修 case selection，而不是继续求混合平均
- [../results/05_round1b_prep/round1c_aggregate_rules.md](../results/05_round1b_prep/round1c_aggregate_rules.md)
  - Round 1c 的聚合规则：明确哪些平均数以后禁止再报，哪些 case 只能作为 process / diagnostic / boundary 使用

## 使用方式

- 不要把整份文件原样无脑粘贴
- 先根据老师要求的篇幅，选用其中的段落
- 如果 report 需要更短版本，优先保留：
  - `摘要段落`
  - `问题收缩`
  - `当前发现`
  - `设计决策`
  - `下一步`

## 原则

- 只写已经发生、且能被文件或数据支持的内容
- 不把焦虑、犹豫、元讨论本身写成进展
- 把“问题发现 -> 证据 -> 决策 -> 下一步”写清楚
