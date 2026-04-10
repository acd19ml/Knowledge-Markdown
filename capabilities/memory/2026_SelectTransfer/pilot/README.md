# pilot/

这里是 `pilot` 阶段的当前工作区。

这一层只放两类东西：

- 正在填写的工作表
- 实验日志

所有 “how-to” 文档都在 [../protocol/](../protocol/)，不要混放到这里。

## 当前文件

| File | Role | Current State |
|---|---|---|
| [taxonomy.csv](taxonomy.csv) | task-level taxonomy 标注表 | 首轮标注已完成，待做 delayed re-annotation |
| [source_sets.csv](source_sets.csv) | source set 构造表 | 已有 1 个 draft `HotpotQA bridge` source set |
| [pairing_table.csv](pairing_table.csv) | relevant / irrelevant pairing 表 | 只有表头，尚未开始 |
| [notes.md](notes.md) | 实验日志：观察、判断、go/no-go | Active |
| [archive/](archive/) | 已冻结的轮次快照 | 不可回写 |

## 推荐使用顺序

1. 先完成 [taxonomy.csv](taxonomy.csv) 的 delayed re-annotation 检查
2. 再扩 source-side candidate pool，并继续完善 [source_sets.csv](source_sets.csv)
3. 再按 [../protocol/first-pairing-workflow.md](../protocol/first-pairing-workflow.md) 填写 [pairing_table.csv](pairing_table.csv)
4. 回到 [notes.md](notes.md) 记录观察、边界 case 和 go/no-go 判断
5. 每完成一轮，就把冻结版本放进 [archive/](archive/)

## `notes.md` 和 CSV 的分工

- CSV 记录：做了什么
- `notes.md` 记录：为什么这么做、遇到了什么问题、下一步怎么判断

如果后面出现 “这个标签当时为什么这么定”“这个 pair 为什么保留” 之类的问题，优先回看 [notes.md](notes.md)。

## 规则

- `notes.md` 是决策原因的单一来源
- 当前 working CSV 可以修改，但进入 [archive/](archive/) 后不得再改
- 如果某轮中途改了 taxonomy、pairing 或指标定义，必须开新版本，不得假装还是同一轮
- 所有实验约束以 [../design/experiment-contract.md](../design/experiment-contract.md) 为准
