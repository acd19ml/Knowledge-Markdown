# Relation-Chain Bridge Expansion Batch 1 Summary

- split: `validation`
- raw candidates: `15`
- filtered candidates: `15`

## Relation-Term Distribution

- `father`: 5
- `daughter`: 4
- `wife`: 3
- `son`: 2
- `mother`: 1
- `husband`: 1

## Screening Outcome

- `likely_relation_chain`: `10`
- `needs_manual_read`: `2`
- `obvious_false_positive`: `3`

See:

- [batch_01_first_pass_screening.md](./batch_01_first_pass_screening.md)
- [batch_01_first_pass_screening.csv](./batch_01_first_pass_screening.csv)

## Subtype Annotation Outcome

- screened rows annotated: `12`
- stable `relation_chain_bridge` keep: `1`

See:

- [batch_01_subtype_annotation_summary.md](./batch_01_subtype_annotation_summary.md)

## Next Step

Batch 1 目前不足以直接构造 `relation_chain_bridge` source set。

下一步只剩两种合法选择：

1. 停止扩池，并正式记录当前 `HotpotQA` 对该 subtype 支撑不足
2. 再做 **一批更高精度** 的 `relation_chain` 扩池，作为最后一次 feasibility check
