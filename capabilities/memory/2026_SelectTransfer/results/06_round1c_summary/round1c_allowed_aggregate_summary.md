# Round 1c Allowed Aggregate Summary

Date: 2026-04-11

这份摘要只按 `allowed aggregate views` 组织 `Round 1b` 结果，不再对 6 个 smoke cases 直接求混合平均。

输入文件：

- [round1c_role_aware_smoke_table.csv](../05_round1b_prep/round1c_role_aware_smoke_table.csv)
- [round1c_role_aware_smoke_subset.csv](../05_round1b_prep/round1c_role_aware_smoke_subset.csv)
- [round1c_aggregate_rules.md](../05_round1b_prep/round1c_aggregate_rules.md)

## 1. Allowed Aggregate Overview


| subset_bucket  | task_count | run_count | memory_runs | memory_verbalized_runs | explicit_use_runs | explicit_reject_runs | outcome_changed_runs | improved_runs | degraded_runs |
| -------------- | ---------- | --------- | ----------- | ---------------------- | ----------------- | -------------------- | -------------------- | ------------- | ------------- |
| process_sanity | 2          | 12        | 8           | 3                      | 2                 | 1                    | 0                    | 0             | 0             |
| diagnostic     | 2          | 12        | 8           | 0                      | 0                 | 0                    | 7                    | 2             | 5             |
| audit_boundary | 2          | 12        | 8           | 2                      | 1                 | 1                    | 0                    | 0             | 0             |


## 2. Process Summary


| task_id        | target_cluster | subset_priority | total_runs | memory_runs | memory_verbalized_runs | explicit_use_runs | explicit_reject_runs | outcome_changed_runs | notes                                                                                  |
| -------------- | -------------- | --------------- | ---------- | ----------- | ---------------------- | ----------------- | -------------------- | -------------------- | -------------------------------------------------------------------------------------- |
| wiki_dev_8896  | comparison     | primary         | 6          | 4           | 2                      | 1                 | 1                    | 0                    | primary sanity check for explicit use vs explicit reject without outcome movement      |
| wiki_dev_10727 | comparison     | secondary       | 6          | 4           | 1                      | 1                 | 0                    | 0                    | ceiling sanity case; useful for separating verbalized use from real outcome dependence |


## 3. Diagnostic Summary


| task_id       | subset_bucket                | total_runs | outcome_changed_runs | improved_runs | degraded_runs | answer_changed_runs | notes                                                                              |
| ------------- | ---------------------------- | ---------- | -------------------- | ------------- | ------------- | ------------------- | ---------------------------------------------------------------------------------- |
| wiki_dev_7019 | answer_format_diagnosis      | 6          | 4                    | 2             | 2             | 4                   | key answer-granularity case; improvement likely comes from output compression      |
| wiki_dev_2639 | artifact_sensitive_diagnosis | 6          | 3                    | 0             | 3             | 3                   | key derailment case; relevant bridge artifact harms an originally correct baseline |


## 4. Audit / Boundary Summary


| task_id       | total_runs | memory_verbalized_runs | report_as     | notes                                                                    |
| ------------- | ---------- | ---------------------- | ------------- | ------------------------------------------------------------------------ |
| wiki_dev_0092 | 6          | 2                      | audit_case    | benchmark ambiguity case; retain only for use/reject/ignore observation  |
| wiki_dev_6083 | 6          | 0                      | boundary_case | country vs demonym scoring boundary; retain only for normalization audit |


## 5. Reporting Rule

- 只允许分别报告 `process summary`、`diagnostic summary`、`audit summary`。
- 不允许再对这 6 个 case 直接报告统一 `EM / F1` 或统一 `relevant vs irrelevant` 平均。
- `wiki_dev_0092` 与 `wiki_dev_6083` 只作 boundary / audit 说明，不进入 transfer evidence。

