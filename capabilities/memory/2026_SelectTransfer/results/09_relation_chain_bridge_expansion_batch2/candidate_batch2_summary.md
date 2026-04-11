# Relation-Chain Bridge Expansion Batch 2 Summary

- split: `validation`
- raw candidates: `17`
- filtered candidates: `17`

## Relation-Term Distribution

- `mother`: 7
- `daughter`: 6
- `brother`: 5
- `father`: 5
- `son`: 4
- `wife`: 3
- `husband`: 3
- `sister`: 2

## Template Distribution

- `sibling_family_chain`: 7
- `spouse_family_chain`: 6
- `parent_child_chain`: 5
- `possessive_relation_chain`: 4
- `nested_of_chain`: 1

## Subtype Annotation Outcome

- screened rows annotated: `17`
- stable `relation_chain_bridge` keep: `10`

See:

- [batch_02_subtype_annotation_summary.md](./batch_02_subtype_annotation_summary.md)

## Next Step

不要继续扩 Batch 3。

当前更合理的下一步是：

1. 从这批 keep 中挑 5 个非近重复题
2. 构造最小 `relation_chain_bridge` source set
3. 再决定是否做 subtype-aware rerun

已选出的第一版 draft source set 见：

- [relation_chain_source_set_selection.md](./relation_chain_source_set_selection.md)
