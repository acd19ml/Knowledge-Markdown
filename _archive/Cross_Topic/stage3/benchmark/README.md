# Stage 3 Benchmark Workspace

> **Purpose**: 集中管理 Stage 3 方法设计当前使用的 benchmark 原文、task 定义、split 设计与任务绑定表

## Suggested Layout

- `webarena-task-split.md`
- `webarena/`
- `mind2web/`
- `android/`

## Current Status

- `webarena-task-split.md`: Stage 3 pilot split 已锁定到 24 个官方 task
- `webarena/`: 已具备 benchmark 论文、官方 `test.raw.json`、正式 binding 表与 paper-grounded extraction

## Rule

- 允许把 Stage 3 的最小 grounding 写到真实 `task_id / site / intent / intent_template_id`
- 在 generated config URL、browser walkthrough、leakage audit 完成前，不要把 `page path` 写成已核实事实
