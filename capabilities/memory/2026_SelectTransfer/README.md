# 2026_SelectTransfer

这个项目研究的不是 “memory 平均有没有帮助”，而是：

**在固定经验预算下，memory 是否支持 `selective transfer`，而不是 `indiscriminate reuse`。**

如果过去经验与当前任务结构相关，memory 应该带来帮助；如果过去经验被刻意设置为不匹配，memory 不应被滥用，也不应引入明显的 `negative transfer`。

## 目录结构

```text
2026_SelectTransfer/
├── design/        # Why / What：项目定位、proposal、实验约定
├── report/        # Progress report、supporting layers、final report drafts
├── protocol/      # How：taxonomy、workflow、checklist、模板
├── rounds/        # Per-round experiment specs
├── pilot/         # 当前工作表：taxonomy / source set / pairing / notes
│   └── archive/   # 每轮冻结后的快照
├── results/       # 结果与阶段性产物
│   ├── 01_sampling/
│   └── 02_hotpotqa_comparison_expansion/
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
- [protocol/pilot-prompt-scaffold.md](./protocol/pilot-prompt-scaffold.md)

### `report/`

这一层现在不再只是 `progress report` 素材，而是已经扩展成完整的报告装配区：

- `progress report` 轮次分析
- `L1 / L2 / L3` supporting layers
- final report section drafts
- assembled full-report drafts

入口：

- [report/README.md](./report/README.md)
- [report/final-report-round1-section-v2.md](./report/final-report-round1-section-v2.md)
- [report/round1-evidence-map.md](./report/round1-evidence-map.md)
- [report/round1-case-appendix.md](./report/round1-case-appendix.md)
- [report/final-report-assembled-draft-v4.md](./report/final-report-assembled-draft-v4.md)

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

阶段性输出和实验结果。这里已经覆盖了从前期 sampling 到 `Round 1j patchback synthesis` 的整条结果链。

入口：

- [results/README.md](./results/README.md)
- [results/04_pilot_run/](./results/04_pilot_run)
- [results/05_round1b_run/](./results/05_round1b_run)
- [results/10_round1g_run/](./results/10_round1g_run)
- [results/11_round1h_run/](./results/11_round1h_run)
- [results/12_round1i_run/](./results/12_round1i_run)
- [results/13_round1j_summary/](./results/13_round1j_summary)

### `notebooks/`

Notebook 入口与运行说明。

- [notebooks/README.md](./notebooks/README.md)
- [notebooks/01_sampling.ipynb](./notebooks/01_sampling.ipynb)
- [notebooks/02_hotpotqa_comparison_expansion.ipynb](./notebooks/02_hotpotqa_comparison_expansion.ipynb)
- [notebooks/03_delayed_reannotation_review.ipynb](./notebooks/03_delayed_reannotation_review.ipynb)
- [notebooks/04_artifact_generation.ipynb](./notebooks/04_artifact_generation.ipynb)
- [notebooks/05_pilot_run.ipynb](./notebooks/05_pilot_run.ipynb)
- [notebooks/06_round1b_prompt_diagnosis.ipynb](./notebooks/06_round1b_prompt_diagnosis.ipynb)
- [notebooks/07_round1c_allowed_aggregate_summary.ipynb](./notebooks/07_round1c_allowed_aggregate_summary.ipynb)
- [notebooks/08_relation_chain_bridge_expansion.ipynb](./notebooks/08_relation_chain_bridge_expansion.ipynb)
- [notebooks/09_relation_chain_bridge_expansion_batch2.ipynb](./notebooks/09_relation_chain_bridge_expansion_batch2.ipynb)
- [notebooks/10_relation_chain_artifact_generation.ipynb](./notebooks/10_relation_chain_artifact_generation.ipynb)
- [notebooks/11_round1g_relation_chain_minirun.ipynb](./notebooks/11_round1g_relation_chain_minirun.ipynb)
- [notebooks/12_round1h_consolidation_diagnosis.ipynb](./notebooks/12_round1h_consolidation_diagnosis.ipynb)
- [notebooks/13_round1i_kinship_operator_repair.ipynb](./notebooks/13_round1i_kinship_operator_repair.ipynb)
- [notebooks/14_round1j_patchback_summary.ipynb](./notebooks/14_round1j_patchback_summary.ipynb)

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

- 设计层已经稳定：
  - `project-positioning`
  - `proposal`
  - `experiment-contract`
- Round 1 frozen inputs 已完成并归档到 [pilot/archive/](./pilot/archive/)
- `Round 1b` prompt diagnosis 已完成：
  - 结构化 `## Reasoning` / `## Final Answer` 输出已跑通
  - raw outputs 与 process-level signals 已可观察
- `Round 1c` 已完成 role-aware reinterpretation：
  - 当前 6 个 smoke cases 不再被当作统一 benchmark 求平均
- `Round 1d` 已确认：
  - `bridge` 需要拆成 subtype
  - `wiki_dev_2639` / `wiki_dev_1379` 是 `relation_chain_bridge`
  - `hp_bridge_set_01` 实际更接近 `attribute_bridge`
- `Round 1e` 已完成 source-side feasibility：
  - `Batch 2` 找到了足够多的 `relation_chain_bridge` candidates
  - 已构造 `hp_relation_chain_bridge_set_01`
- `Round 1f` 已完成 reroute prep：
  - [pilot/pairing_table.csv](./pilot/pairing_table.csv) 已将 `wiki_dev_2639` / `wiki_dev_1379` reroute 到新的 subtype-matched source
- `Round 1g` 已完成：
  - subtype-aware reroute 在 `wiki_dev_2639` 上修复了 relevant `episodic_trace`
  - `wiki_dev_1379` 被确认为 ceiling / sanity case
- `Round 1h` 已完成：
  - relation-chain consolidation 的 formatting / branch wording 修复已验证
  - failure 被进一步收缩成 `kinship operator interpretation`
- `Round 1i` 已完成：
  - operator-aware repair 使 `wiki_dev_2639` 上的 relevant consolidation 从 wrong 恢复为 correct
- `Round 1j` 已完成：
  - `wiki_dev_2639` 的 repaired evidence 已 patch back 到 synthesis 层
  - 它不再应被写成 “relevant memory hurts” 的证据
- final-report assembly 已进入收稿阶段：
  - L1 narrative: [report/final-report-round1-section-v2.md](./report/final-report-round1-section-v2.md)
  - L2 evidence map: [report/round1-evidence-map.md](./report/round1-evidence-map.md)
  - L3 case appendix: [report/round1-case-appendix.md](./report/round1-case-appendix.md)
  - current assembled draft: [report/final-report-assembled-draft-v4.md](./report/final-report-assembled-draft-v4.md)

## 当前最重要的下一步

不要再继续围绕 `wiki_dev_2639` 做新的微调 rerun。当前最重要的是：

1. 以 [report/final-report-assembled-draft-v4.md](./report/final-report-assembled-draft-v4.md) 作为当前 canonical draft
2. 用 [results/13_round1j_summary/round1j_patchback_summary.md](./results/13_round1j_summary/round1j_patchback_summary.md) 约束 `wiki_dev_2639` 的最终解释
3. 在最终课程报告里明确：
   - coarse pairing granularity 会制造 false negative transfer evidence
   - abstract memory 只有在 relation operator 被编码成 executable rule 时才真正可用
4. 只在课程要求更强 empirical support 时，才考虑一个很小的 repaired validation subset

当前 `artifact generation` 默认不再依赖 `OPENAI_API_KEY`，而是使用本地 Hugging Face 推理：

- 主推荐模型：`Qwen/Qwen3.5-9B`
- 显存更稳的回退：`Qwen/Qwen3.5-4B`

## 一句话约束

这个项目的核心不是“尽快跑分”，而是：

**先造一把可用的尺子，再用它去测 `selective transfer`。**
