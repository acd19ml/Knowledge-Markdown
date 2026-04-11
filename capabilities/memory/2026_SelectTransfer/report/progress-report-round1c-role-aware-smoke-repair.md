# Progress Report: Round 1c Role-Aware Smoke Repair

Date: 2026-04-11

---

## 1. Executive Summary

Round 1c 没有新增模型运行，也没有改变 `model / prompt scaffold / source set / pairing / artifacts`。  
这一轮只修改一层东西：

- `evaluation / case-selection layer`

也就是说，Round 1c 的任务不是再跑一次 `Round 1b`，而是把 `Round 1b` 已经得到的 36 条结果，重新整理成一个**允许解释、允许汇报、且不再自相矛盾**的结果结构。

这一轮的核心结论有三条：

1. **当前 6 个 smoke cases 不能再被视为一个统一的小 benchmark。**
2. **从现在开始，不允许再对这 6 个 case 直接报告统一 `EM / F1` 或统一 `relevant vs irrelevant` 平均。**
3. **更合理的做法是把它们拆成三类可解释角色：**
   - `process sanity`
   - `diagnostic`
   - `audit / boundary`

因此，Round 1c 的本质不是“又做了一轮分析”，而是：

**把 Round 1b 从“有现象但难以汇总”推进到“下一轮可按规则解释和汇报”。**

---

## 2. What Changed Since Round 1b

相对于 [progress-report-round1b-prompt-diagnosis.md](./progress-report-round1b-prompt-diagnosis.md)，Round 1c 不再追求新的 prompt-level 证据，而是把已有证据转成三层固定产物。

### 2.1 Pairing / Artifact Audit Was Finalized

我们先完成了 6 个 smoke cases 的逐条审计：

- [round1b_pairing_artifact_audit.md](../results/05_round1b_prep/round1b_pairing_artifact_audit.md)

这一步回答的不是：

- 哪个条件平均更高

而是：

- 当前 observed effect 更像来自什么
  - clean process-level selectivity
  - artifact-induced derailment
  - answer-format correction
  - benchmark ambiguity
  - scoring boundary

### 2.2 Case Role Reclassification Was Introduced

在 audit 基础上，我们把 6 个 smoke cases 重分类为固定角色：

- [round1b_case_role_reclassification.csv](../results/05_round1b_prep/round1b_case_role_reclassification.csv)
- [round1b_case_role_reclassification.md](../results/05_round1b_prep/round1b_case_role_reclassification.md)

这一步的关键作用是：

- 不再把每个 case 都默认当作同一种 transfer evidence
- 明确哪些 case 还能保留、但保留时是作为什么角色

### 2.3 Allowed Aggregate Views Were Frozen

Round 1c 进一步把“哪些 aggregate 允许、哪些 aggregate 禁止”也固定下来了：

- [round1c_aggregate_rules.md](../results/05_round1b_prep/round1c_aggregate_rules.md)
- [round1c_role_aware_smoke_subset.csv](../results/05_round1b_prep/round1c_role_aware_smoke_subset.csv)

这意味着从这一轮开始：

- 允许的汇报方式只有：
  - `process summary`
  - `diagnostic summary`
  - `audit summary`
- 不再允许：
  - 直接对 6 个 case 求一个统一 `EM / F1`
  - 直接对 6 个 case 求统一 `relevant vs irrelevant` 平均

### 2.4 Allowed Aggregate Summary Was Generated

最后，我们把这些规则真正落到了自动汇总层：

- [round1c_role_aware_smoke_table.csv](../results/05_round1b_prep/round1c_role_aware_smoke_table.csv)
- [round1c_allowed_aggregate_summary.md](../results/06_round1c_summary/round1c_allowed_aggregate_summary.md)
- [round1c_process_summary.csv](../results/06_round1c_summary/round1c_process_summary.csv)
- [round1c_diagnostic_summary.csv](../results/06_round1c_summary/round1c_diagnostic_summary.csv)
- [round1c_audit_summary.csv](../results/06_round1c_summary/round1c_audit_summary.csv)

对应 notebook：

- [07_round1c_allowed_aggregate_summary.ipynb](../notebooks/07_round1c_allowed_aggregate_summary.ipynb)

所以 Round 1c 的新增不是新模型输出，而是：

**新的解释层与新的汇总层。**

---

## 3. Round 1c Results

### 3.1 Allowed Aggregate Overview

| subset_bucket | task_count | run_count | memory_runs | memory_verbalized_runs | explicit_use_runs | explicit_reject_runs | outcome_changed_runs | improved_runs | degraded_runs |
|---|---|---|---|---|---|---|---|---|---|
| process_sanity | 2 | 12 | 8 | 3 | 2 | 1 | 0 | 0 | 0 |
| diagnostic | 2 | 12 | 8 | 0 | 0 | 0 | 7 | 2 | 5 |
| audit_boundary | 2 | 12 | 8 | 2 | 1 | 1 | 0 | 0 | 0 |

这个表的含义很重要：

- `process_sanity` 已经能提供 `explicit_use / explicit_reject`
- `diagnostic` 才是当前 outcome change 真正发生的地方
- `audit_boundary` 虽然也有 memory verbalization，但不应再进入 transfer aggregate

也就是说，当前 36 条 run 的差异来源不是单一的。  
它们已经分化成：

- process signal
- diagnostic signal
- boundary noise

### 3.2 Process Summary

| task_id | target_cluster | total_runs | memory_verbalized_runs | explicit_use_runs | explicit_reject_runs | outcome_changed_runs |
|---|---|---|---|---|---|---|
| `wiki_dev_8896` | comparison | 6 | 2 | 1 | 1 | 0 |
| `wiki_dev_10727` | comparison | 6 | 1 | 1 | 0 | 0 |

这两条 case 共同说明：

1. prompt repair 的确成功了  
   - 模型已经能在部分 memory runs 中显式说明自己是否使用 memory

2. verbalized memory use 不等于 outcome dependence  
   - 即使 `wiki_dev_10727` 出现了 irrelevant episodic 的 `explicit_use`
   - 最终答案仍完全不变

因此，Round 1c 对 process 层最重要的推进是：

**以后必须把“提到了 memory”和“memory 真正改变了结果”分开记。**

### 3.3 Diagnostic Summary

| task_id | subset_bucket | total_runs | outcome_changed_runs | improved_runs | degraded_runs | answer_changed_runs |
|---|---|---|---|---|---|---|
| `wiki_dev_7019` | answer_format_diagnosis | 6 | 4 | 2 | 2 | 4 |
| `wiki_dev_2639` | artifact_sensitive_diagnosis | 6 | 3 | 0 | 3 | 3 |

这两条 case 说明，当前真正有信息量的现象不是“平均 gain”，而是：

- `wiki_dev_2639`
  - relevant bridge artifact 会把正确 baseline 拉坏
  - 更像 `artifact-induced derailment`

- `wiki_dev_7019`
  - 某些 improvement 更像 output compression
  - 更接近 answer-format correction，而不是 clear strategy transfer

这直接改变了对 `Round 1b` 的理解方式：

- 不是 “memory generally helps / hurts”
- 而是 “不同 case 暴露的是不同 failure mode”

### 3.4 Audit / Boundary Summary

| task_id | total_runs | memory_verbalized_runs | report_as |
|---|---|---|---|
| `wiki_dev_0092` | 6 | 2 | audit_case |
| `wiki_dev_6083` | 6 | 0 | boundary_case |

这两条 case 现在已经被明确降级：

- `wiki_dev_0092`
  - benchmark ambiguity case
  - 只用来观察 `use / reject / ignore`

- `wiki_dev_6083`
  - scoring boundary case
  - `Spain` vs `Spanish` 不再被误判为 memory failure

因此，Round 1c 最重要的纪律性进展之一是：

**把这些 case 明确排除出 transfer evidence。**

---

## 4. Why This Matters

Round 1c 之所以必要，是因为如果不先做这一层修复，后面继续跑更多 case 只会放大当前的解释混乱。

如果仍然沿用 Round 1b 之前的方式，直接报告：

- 6 个 smoke cases 的整体 `EM / F1`
- 整体 `relevant vs irrelevant` 平均

那么会把以下完全不同的现象混在一起：

- clean process-level selectivity
- relevant artifact 把 baseline 拉坏
- answer-format correction
- benchmark ambiguity
- scoring normalization gap

而这些现象显然不应该被一个平均数强行压扁。

所以 Round 1c 的真正价值不是“多得出一个结论”，而是：

**把什么可以聚合、什么不能聚合这件事先定死。**

这一步对后续研究的价值也更高，因为它直接回答了：

- 现在的 measurement setup 哪些部分已经可以信
- 哪些部分还只能做 diagnostic，不该上升成 stronger claim

---

## 5. Diagnostic Conclusion

Round 1c 的最终结论可以压成三句：

1. **Round 1b 已经足以支持 process-level analysis，但还不足以支持混合的 outcome-level aggregate。**
2. **当前 smoke subset 应被视为一个 role-aware diagnostic bundle，而不是一个统一的小 benchmark。**
3. **下一轮如果继续，必须先按 role 选择 case，再决定是否 rerun，而不是继续对原 6 case 直接求平均。**

因此，Round 1c 的更准确定位是：

**一次解释层与汇总层的修复。**

它不证明 memory 已经有效，但它让后续实验不再用错误的方式解释已有结果。

---

## 6. Next Step

基于 Round 1c，下一步最合理的顺序是：

1. **固定新的 smoke subset 使用方式**
   - `wiki_dev_8896`、`wiki_dev_10727`：只作 `process sanity`
   - `wiki_dev_2639`：只作 `artifact-sensitive diagnosis`
   - `wiki_dev_7019`：只作 `answer-format diagnosis`
   - `wiki_dev_0092`、`wiki_dev_6083`：只作 `audit / boundary`

2. **补 process metric，而不是先补更多 case**
   - 例如：
     - whether memory was merely mentioned
     - whether memory materially changed answer type
     - whether answer was compressed toward gold

3. **对 `bridge` cluster 做更细的 subtype 检查**
   - 当前 `wiki_dev_2639` 已经说明：
     - label-level `bridge` matching 不够
     - relation-chain bridge 与一般 attribute-bridge 不能直接合并

4. **只有在 case role、process metric、boundary handling 都稳定后，再考虑更大的 rerun**

一句话总结：

**Round 1c 已经把“哪些结果可以报、哪些结果不能报”这件事收住了；下一步应该基于这个更干净的解释框架继续，而不是再把不相容的 case 混成一个平均数。**
