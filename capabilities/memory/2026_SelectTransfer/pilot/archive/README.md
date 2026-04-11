# pilot/archive/

Frozen snapshots after each completed round. Never edit files here directly.

## Current Round 1 Snapshot

| File | Content |
|---|---|
| taxonomy_round1.csv | Frozen working taxonomy after comparison expansion and delayed re-annotation review |
| source_sets_round1.csv | Frozen Round 1 source sets |
| pairing_table_round1.csv | Frozen Round 1 pairing table |
| notes_round1.md | Frozen pilot notes snapshot used for Round 1 inputs |

## Rule

- `pilot/` 根目录继续作为 working area
- `pilot/archive/` 只保存已经通过 freeze review 的版本
- 如果下一轮修改了 taxonomy / source sets / pairing，请新建下一轮快照，不要回写当前文件

注意：

- 这个 archive 代表的是 Round 1 的 frozen inputs
- 后续 `relation_chain` subtype repair、reroute 与 artifact updates 不会回写到这里
- 那些后续变化应从 [../source_sets.csv](../source_sets.csv)、[../pairing_table.csv](../pairing_table.csv) 以及 `results/` / `report/` 读取
