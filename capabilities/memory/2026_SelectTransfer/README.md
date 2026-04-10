# 2026_SelectTransfer

这个项目研究的不是 “memory 平均有没有帮助”，而是：

**在固定经验预算下，memory 是否支持 `selective transfer`，而不是 `indiscriminate reuse`。**

如果过去经验与当前任务结构相关，memory 应该带来帮助；如果过去经验被刻意设置为不匹配，memory 不应被滥用，也不应引入明显的 `negative transfer`。

## 目录结构

```text
2026_SelectTransfer/
├── design/        # Why / What：项目定位、proposal、实验约定
├── report/        # Progress report 素材与可直接使用的段落草稿
├── protocol/      # How：taxonomy、workflow、checklist、模板
├── rounds/        # Per-round experiment specs
├── pilot/         # 当前工作表：taxonomy / source set / pairing / notes
│   └── archive/   # 每轮冻结后的快照
├── results/       # 结果与阶段性产物
│   └── 01_sampling/
├── notebooks/     # Colab / notebook 入口
└── artifacts/     # 生成的 memory artifacts
```

## 各目录分别负责什么

### `design/`

稳定的设计文档，回答“为什么做这个项目、项目边界是什么、当前约束是什么”。

- [design/README.md](./design/README.md)
- [design/project-positioning.md](./design/project-positioning.md)
- [design/proposal.md](./design/proposal.md)
- [design/proposal-summary.md](./design/proposal-summary.md)
- [design/experiment-contract.md](./design/experiment-contract.md)

### `protocol/`

可复用的操作说明，回答“这一套实验应该怎么做”，而不是“已经做了什么”。

- [protocol/README.md](./protocol/README.md)
- [protocol/pipeline.md](./protocol/pipeline.md)
- [protocol/taxonomy_guideline.md](./protocol/taxonomy_guideline.md)
- [protocol/first-20-annotation-workflow.md](./protocol/first-20-annotation-workflow.md)
- [protocol/first-source-set-selection-workflow.md](./protocol/first-source-set-selection-workflow.md)
- [protocol/first-pairing-workflow.md](./protocol/first-pairing-workflow.md)
- [protocol/pilot-run-checklist.md](./protocol/pilot-run-checklist.md)

### `report/`

面向课程 `progress report` 的写作素材，不重复实验细节，而是把当前问题、发现和决策整理成可直接粘贴的段落。

- [report/README.md](./report/README.md)
- [report/progress-report-draft.md](./report/progress-report-draft.md)

### `rounds/`

每一轮实验的受控说明，回答：

- 这一轮只改什么变量
- 固定了什么
- 这一轮回答什么，不回答什么

入口：

- [rounds/README.md](./rounds/README.md)
- [rounds/round_01_memory_form_pilot.md](./rounds/round_01_memory_form_pilot.md)

### `pilot/`

当前工作区。这里放的是正在填写的工作表和实验日志，而不是稳定的设计文档。

- [pilot/README.md](./pilot/README.md)
- [pilot/taxonomy.csv](./pilot/taxonomy.csv)
- [pilot/source_sets.csv](./pilot/source_sets.csv)
- [pilot/pairing_table.csv](./pilot/pairing_table.csv)
- [pilot/notes.md](./pilot/notes.md)
- [pilot/archive/README.md](./pilot/archive/README.md)

### `results/`

阶段性输出和实验结果。当前已经有 sampling 阶段的中间产物。

- [results/README.md](./results/README.md)
- [results/01_sampling/taxonomy_round1_raw.csv](./results/01_sampling/taxonomy_round1_raw.csv)
- [results/01_sampling/sampled_20_full.json](./results/01_sampling/sampled_20_full.json)
- [results/pilot_results.csv](./results/pilot_results.csv)

### `notebooks/`

Notebook 入口与运行说明。

- [notebooks/README.md](./notebooks/README.md)
- [notebooks/01_sampling.ipynb](./notebooks/01_sampling.ipynb)

### `artifacts/`

后续生成的 `episodic trace`、`cross-episode consolidation` 等 memory artifacts。

- [artifacts/README.md](./artifacts/README.md)

## 推荐阅读顺序

如果是第一次进入这个项目，建议按这个顺序读：

1. [design/project-positioning.md](./design/project-positioning.md)
2. [design/proposal.md](./design/proposal.md)
3. [design/experiment-contract.md](./design/experiment-contract.md)
4. [protocol/README.md](./protocol/README.md)
5. [pilot/README.md](./pilot/README.md)
6. [rounds/round_01_memory_form_pilot.md](./rounds/round_01_memory_form_pilot.md)

## 当前实际进度

基于当前目录内容，项目状态是：

- 设计层已经基本稳定：`project-positioning`、`proposal`、`experiment-contract` 都已落盘
- `sampling` 阶段已经有产物：`results/01_sampling/` 下已有 notebook、完整抽样 JSON 和 raw CSV
- [pilot/taxonomy.csv](./pilot/taxonomy.csv) 已完成 20 个 sampled tasks 的首轮标注，当前分布为 `bridge = 14`、`comparison = 6`
- [pilot/source_sets.csv](./pilot/source_sets.csv) 已写入一个 draft `HotpotQA bridge` source set
- [pilot/pairing_table.csv](./pilot/pairing_table.csv) 还是空表
- [results/pilot_results.csv](./results/pilot_results.csv) 仍未开始写入 run 结果

也就是说，当前不缺框架，缺的是：

- delayed re-annotation 后的稳定 taxonomy
- 至少一个更完整的 source-side candidate pool，尤其是 `comparison` coverage
- 第一轮可 defend 的 relevant / irrelevant pairs

## 当前最重要的下一步

不要继续扩文档层级，也不要继续把问题做大。当前最重要的是按顺序完成：

1. 完成 5 个边界 case 的 delayed re-annotation
2. 扩 `HotpotQA` source-side candidate pool，补足 `comparison` cluster
3. 在此基础上继续完善 [pilot/source_sets.csv](./pilot/source_sets.csv) 与 [pilot/pairing_table.csv](./pilot/pairing_table.csv)
4. 只有在 pair 和 artifact 都过检后，才进入 `pilot run`

## 一句话约束

这个项目的核心不是“尽快跑分”，而是：

**先造一把可用的尺子，再用它去测 `selective transfer`。**
