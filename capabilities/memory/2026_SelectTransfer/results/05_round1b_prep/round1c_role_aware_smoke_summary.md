# Round 1c Role-Aware Smoke Summary

Date: 2026-04-11

这份摘要把 `Round 1b` 的 run-level 结果按 `case role` 重新组织，用于支持 `Round 1c` 的 case-selection repair。

对应表格：

- [round1c_role_aware_smoke_table.csv](./round1c_role_aware_smoke_table.csv)
- [round1b_case_role_reclassification.csv](./round1b_case_role_reclassification.csv)

## Summary Table

| case_role | runs | memory runs | verbalized | explicit use | explicit reject | outcome changed | improved | degraded |
|---|---|---|---|---|---|---|---|---|
| process_selectivity_sanity_check | 6 | 4 | 2 | 1 | 1 | 0 | 0 | 0 |
| clean_ceiling_process_case | 6 | 4 | 1 | 1 | 0 | 0 | 0 | 0 |
| artifact_sensitive_failure_case | 6 | 4 | 0 | 0 | 0 | 3 | 0 | 3 |
| answer_format_sensitive_case | 6 | 4 | 0 | 0 | 0 | 4 | 2 | 2 |
| ambiguity_audit_case | 6 | 4 | 2 | 1 | 1 | 0 | 0 | 0 |
| scoring_boundary_case | 6 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |

## Readout

- `process_selectivity_sanity_check` 只有 1 个 task，但已经提供了当前最干净的 `explicit_use / explicit_reject` 证据。
- `clean_ceiling_process_case` 说明 verbalized memory use 可以出现而不改变结果，因此后续 process metric 必须区分“提到 memory”和“memory 真正改变 outcome”。
- `artifact_sensitive_failure_case` 当前最关键，因为它显示 relevant artifact 可以把正确 baseline 拉坏。
- `answer_format_sensitive_case` 提醒当前某些 improvement 更接近 output compression，而不是 strategy transfer。
- `ambiguity_audit_case` 与 `scoring_boundary_case` 都不应继续进入 transfer aggregate。

## Direct Implication

下一轮不应再直接对这 6 个 case 求混合平均，而应按 role 分开使用：

- process sanity
  - `wiki_dev_8896`, `wiki_dev_10727`
- artifact-sensitive diagnosis
  - `wiki_dev_2639`
- answer-format diagnosis
  - `wiki_dev_7019`
- audit / boundary only
  - `wiki_dev_0092`, `wiki_dev_6083`
