# Notes × Frontend Consistency Rules

本文件定义最直观、可执行的规则，确保笔记内容与前端可视化一致。

## 核心原则

1. **Markdown 是唯一真源**：前端仅渲染，不反向编辑。
2. **规则可自动检查**：任何一致性问题都能通过 `npm run check:notes` 被发现。
3. **可视化块有结构约束**：必须能被机器解析，否则构建失败。

---

## 规则 A：链接必须有效

- 任何 Markdown 链接都必须指向存在的文件。
- 构建时会检查相对路径和 `.md` 缺省补全。
- 断链会被写入 `web/public/data/consistency-report.md`。

**修复方式**：更新路径或删除无效链接。

---

## 规则 B：可视化块必须使用 `viz-matrix`

当需要替代 ASCII 图时，使用以下结构：

```
```viz-matrix
id: knowledge-reuse-pattern
title: 知识复用方式 × 任务阶段
xAxis: [精确, 相似, 泛化, 注入]
rows:
  - key: pre_task
    label: 任务前探索
    lanes: [Skills, World]
cells:
  - row: pre_task/Skills
    col: 精确
    status: existing
    label: AppAgent
    link: ../GUI_Agent/comparison-matrix.md
```
```

**必须字段**：`id`、`xAxis`、`rows`、`cells`  
**合法状态**：`existing`、`gap`、`neutral`

**规则检查**：
- `row` 必须存在于 `rows` 定义中
- `col` 必须存在于 `xAxis` 中
- 解析失败将导致 `check:notes` 失败

---

## 规则 C：新增笔记的最小要求

- 必须有 `# 标题`
- 必须用标准 Markdown 链接关联相关文件
- 如有矩阵/图示，优先使用 `viz-matrix`

---

## 运行方式

在 `web/` 目录下执行：

- `npm run build:index` 生成前端数据
- `npm run check:notes` 校验一致性并输出报告

报告路径：`web/public/data/consistency-report.md`
