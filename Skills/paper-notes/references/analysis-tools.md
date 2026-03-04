# Analysis Tools: Comparison Matrix & Gap Tracker

These two files are maintained per topic directory. They grow as more papers are added.

---

## Comparison Matrix (comparison-matrix.md)

### File structure

```markdown
# [Topic Name] 方法对比矩阵

## 维度定义
<!-- 说明各列含义，根据领域调整 -->
- **输入模态**: 截图 / 文本 / HTML DOM / 多模态
- **记忆机制**: 无 / 短期 / 情节 (Episodic) / 语义 (Semantic) / 程序性 (Procedural)
- **自我进化能力**: 无 / 微调 (Fine-tuning) / 提示优化 / 经验反思 (Reflection) / 混合
- **任务类型**: Web / Desktop / Mobile / 通用
- **核心基准**: 论文使用的主要 benchmark 名称

## 论文对比

| 论文 | 年份 | 输入模态 | 记忆机制 | 自我进化能力 | 任务类型 | 核心基准 | 最佳结果 | 主要局限 |
|------|------|---------|---------|------------|---------|---------|---------|---------|
| [ShortName] | YYYY | ... | ... | ... | ... | BenchmarkName | XX% | ... |

## 从矩阵中观察到的模式
<!-- 更新每次新增论文后 -->
- 观察 1:
- 观察 2:
- 观察 3:

## 由此产生的 Research Gap 候选
<!-- 从模式中提炼，详细内容记录在 gap-tracker.md -->
- Gap A:
- Gap B:
```

### Rules for updating

- One row per paper. Columns that can't be determined from the paper: use `?`
- Keep `主要局限` to one concise phrase — the single most important limitation
- After every new row, re-read all rows holistically and revise the "模式" section
- If adding a new dimension column, backfill `?` for existing rows

---

## Gap Tracker (gap-tracker.md)

### File structure

```markdown
# Research Gap 追踪

## Gap 候选列表

### Gap [N]: [简短描述，10字以内]
- **证据强度**: 强 (3+ papers) / 中 (2 papers) / 弱 (1 paper or inference)
- **支撑证据**:
  - [[论文 A](link)] 指出: "..." (Section X)
  - [[论文 B](link)] 的实验表明: ...
  - 对比矩阵显示: N 篇论文中仅 M 篇涉及此问题
- **潜在研究方向**:
- **可行性评估**: 高 / 中 / 低
- **所需资源**:

---

## Gap 优先级排序
<!-- 综合证据强度 × 可行性 × 研究价值 排序 -->
1. **Gap [N]** — 理由: [1-2句，说明为什么排第一]
2. **Gap [M]** — 理由: ...
3. ...
```

### Rules for updating

**Adding a new gap:**
- Check if a semantically equivalent gap already exists (same problem, different wording) — if so, merge and add evidence
- Assign strength 弱 for a single paper; upgrade to 中 when a second paper confirms it; 强 when 3+ papers converge
- Be specific in 支撑证据 — quote the actual limitation or observation from the paper

**Upgrading existing gaps:**
- When a new paper provides additional evidence for an existing gap, add it to 支撑证据 and upgrade strength if threshold is met
- Update 优先级排序 whenever strength ratings change

**Pruning:**
- If a subsequent paper appears to have solved a gap, mark it with `~~strikethrough~~` and add a note: `[已有解决方案: 论文名]`
