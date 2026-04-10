# CSV Field Examples

这份文件提供四个 CSV 的字段填写示例：

- [taxonomy.csv](./taxonomy.csv)
- [source_sets.csv](./source_sets.csv)
- [pairing_table.csv](./pairing_table.csv)
- [../results/pilot_results.csv](../results/pilot_results.csv)

这些示例只用于说明字段含义，不建议直接粘贴进正式数据文件。

## 1. `taxonomy.csv`

表头：

```csv
task_id,dataset,question,reasoning_label,keep_drop,note
```

示例：

```csv
hp_dev_001,HotpotQA,"Which university did the author of The Hobbit attend?",bridge,keep,"bridge via intermediate entity lookup"
wiki_dev_014,2WikiMultiHopQA,"Which film was released earlier, X or Y?",comparison,keep,"comparison after retrieving two release dates"
hp_dev_022,HotpotQA,"What happened first, A or B?",temporal,keep,"temporal ordering is dominant"
wiki_dev_031,2WikiMultiHopQA,"Question mixes bridge and comparison equally",,drop,"drop: bridge and comparison equally strong"
```

字段说明：

- `task_id`
  - benchmark 原始样本 id
- `dataset`
  - `HotpotQA` 或 `2WikiMultiHopQA`
- `question`
  - 题目文本，允许简写，但要能识别
- `reasoning_label`
  - `bridge` / `comparison` / `temporal` / `distractor-heavy`
  - 如果 `drop`，可以留空
- `keep_drop`
  - `keep` 或 `drop`
- `note`
  - 最短一句解释为什么这样标

## 2. `source_sets.csv`

表头：

```csv
source_set_id,cluster,member_task_ids,entity_disjoint,lexical_overlap_note,note
```

示例：

```csv
bridge_set_01,bridge,"hp_dev_001|hp_dev_007|hp_dev_019|hp_dev_024|hp_dev_030",yes,"low overlap, different entities","clean bridge set, diverse surface forms"
comparison_set_01,comparison,"hp_dev_005|hp_dev_011|hp_dev_018|hp_dev_021|hp_dev_026",mostly,"one pair has mild lexical overlap","comparison set, still acceptable for pilot"
```

字段说明：

- `source_set_id`
  - source set 的唯一 id
- `cluster`
  - 该 set 对应的 reasoning cluster
- `member_task_ids`
  - 组内 5 道题的 id，建议用 `|` 分隔
- `entity_disjoint`
  - `yes` / `mostly` / `no`
- `lexical_overlap_note`
  - 简短写明 lexical overlap 情况
- `note`
  - 一句总结这组 source set 的质量

## 3. `pairing_table.csv`

表头：

```csv
target_task_id,target_cluster,relevant_source_set_id,irrelevant_source_set_id,entity_overlap_score,lexical_overlap_score,leakage_check_label,pairing_note
```

示例：

```csv
wiki_dev_014,comparison,comparison_set_01,bridge_set_01,0.00,0.12,safe,"relevant: same comparison pattern; irrelevant: bridge source mismatched"
wiki_dev_022,bridge,bridge_set_01,temporal_set_01,0.00,0.08,safe,"relevant: bridge via intermediate entity; irrelevant: temporal source should not naturally help"
```

字段说明：

- `target_task_id`
  - target task 的 id
- `target_cluster`
  - target task 的 reasoning label
- `relevant_source_set_id`
  - 该 target 对应的 matched source set
- `irrelevant_source_set_id`
  - 该 target 对应的 deliberately mismatched source set
- `entity_overlap_score`
  - 一个简单数值，先用 0 到 1 即可
- `lexical_overlap_score`
  - 一个简单数值，先用 0 到 1 即可
- `leakage_check_label`
  - 推荐先用：`safe` / `review` / `unsafe`
- `pairing_note`
  - 一句话说明 relevant / irrelevant 为什么合理

## 4. `pilot_results.csv`

表头：

```csv
run_id,target_task_id,split,condition,source_set_id,routing_decision,memory_attached,em,f1,token_usage,failure_status,note
```

示例：

```csv
run_001,wiki_dev_014,relevant,Episodic Trace,comparison_set_01,na,yes,1,1.0,2840,none,"memory helped on matched comparison case"
run_002,wiki_dev_014,irrelevant,Episodic Trace,bridge_set_01,na,yes,0,0.0,2795,wrong_answer,"possible negative transfer from mismatched bridge memory"
run_003,wiki_dev_022,irrelevant,Cross-Episode Consolidation + Applicability Judgment,temporal_set_01,reject,no,1,1.0,3012,none,"judge rejected mismatched memory"
```

字段说明：

- `run_id`
  - 每次 run 的唯一 id
- `target_task_id`
  - 当前 target task
- `split`
  - `relevant` / `irrelevant`
- `condition`
  - 当前实验条件名称
- `source_set_id`
  - 使用的 source set
- `routing_decision`
  - 对非 judgment 条件可填 `na`
- `memory_attached`
  - `yes` / `no`
- `em`
  - `0` 或 `1`
- `f1`
  - 小数
- `token_usage`
  - 总 token 消耗
- `failure_status`
  - 例如 `none` / `wrong_answer` / `format_error` / `halted`
- `note`
  - 一句记录这个 case 的关键信号

## 当前建议

- CSV 本体保持干净，不直接写说明
- 示例统一放在这份文档里
- 如果后续字段调整，优先先改这里，再改正式 CSV schema
