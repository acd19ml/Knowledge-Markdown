# Theory Lab

用于沉淀 `memory` 主题下的个人理论主张，以及每条主张对应的技术研究方向。

## Structure

- [theory_map.md](./theory_map.md) — 主入口，按主张浏览并跳转到对应技术文件
- [source/conversation_01.md](./source/conversation_01.md) — 原始对话来源
- [directions/](./directions/) — 每条主张对应一个技术方向文件

## Rules

- 总是从 `theory_map.md` 进入
- `theory_map.md` 保留主张和简短说明，不承载完整技术设计
- `directions/` 下每个文件只回应一条主张

## Research Direction Template

每个 `directions/*.md` 默认使用以下结构：

```md
# Research Direction

## 中文标题（必要时保留关键 technical term）

关联主张：
- [Theory Map](../theory_map.md)

### Goal

这条技术方向想解决什么问题。

### Problem Reframing

这条主张如果转成技术问题，真正要处理的核心矛盾是什么。

### Core Hypothesis

这条方向当前相对稳定的核心判断是什么。

### Requirements

无论未来采用什么方案，都必须满足哪些硬条件。

### Evaluation

评估重点是什么。
先写一句总括，再拆成 2 到 4 个关键判据。

### Open Questions

当前最关键、最值得继续追问的 2 到 4 个问题。
```

默认不写以下部分：

- `Solution Space`
- `Candidate Mechanism`

只有在某条主张已经进入具体方案比较阶段时，才额外加入这些部分。

区分原则：

- `Requirements` 是已经确认必须成立的条件
- `Open Questions` 是当前仍未回答、但会决定后续研究方向的问题
