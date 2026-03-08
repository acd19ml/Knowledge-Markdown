# Stage 3 Workspace

> **Purpose**: 把 Stage 3 的方法论设计产物按职责集中管理，减少根目录噪音

## Layout

- `readiness/`
  - RQ proof、前驱筛选、进入原型实现前的就绪判断
- `design/`
  - 方法 brief、memory schema、实验协议、方法图
- `benchmark/`
  - 当前 Stage 3 使用的 benchmark split、task binding 与来源材料
- `formal/`
  - Stage 3 正式收口页：problem statement、method spec、nearest-work delta、evaluation plan

## Rule

- 新的 Stage 3 文档优先落在这个目录下，不再平铺到 `Cross_Topic/`
- benchmark 来源材料保留可追溯 artifact，但临时预览文件不要进入版本库

## Formal Package

- [problem-statement.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/formal/problem-statement.md)
- [method-spec.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/formal/method-spec.md)
- [nearest-work-delta.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/formal/nearest-work-delta.md)
- [evaluation-plan.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/formal/evaluation-plan.md)

Authority rule:

- `formal/` is the only package that should be cited as the Stage 3 final output.
- `readiness/`, `design/`, and `benchmark/` remain as supporting evidence, working detail, and audit artifacts.
