# Versioning Convention

这份文件定义 `pilot/` 阶段的版本命名规则。

目的：

- 让每一轮输出都能被 `round_xx` 文档明确引用
- 避免出现“第一轮到底用的是哪个 taxonomy / pairing”这种模糊情况

## 基本原则

- 当前工作版本保留在根目录
- 每完成一轮稳定版本，就复制到 [../pilot/archive/](../pilot/archive/) 中
- `round_xx` 文档只引用 `archive/` 中的稳定版本，不引用正在编辑的根目录文件

## 命名格式

推荐格式：

- `taxonomy_round1.csv`
- `source_sets_round1.csv`
- `pairing_table_round1.csv`
- `notes_round1.md`

如果需要更细，可以继续加后缀：

- `taxonomy_round1_v2.csv`
- `pairing_table_round1_clean.csv`

但第一轮建议先保持简单，不要一开始就引入过多版本层级。

## Round 01 约定

当第一轮 20 题标注和第一批 source sets / pairs 完成后，归档到：

- `pilot/archive/taxonomy_round1.csv`
- `pilot/archive/source_sets_round1.csv`
- `pilot/archive/pairing_table_round1.csv`
- `pilot/archive/notes_round1.md`

`round_01_memory_form_pilot.md` 应只引用这些归档版本。

## 当前规则

- 根目录文件：正在编辑
- `archive/` 文件：可用于实验的冻结版本

如果某一轮还没冻结，就不要写进正式 `round_xx` 文档。
