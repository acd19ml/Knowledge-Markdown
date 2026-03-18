---
name: kb-maintenance
description: "Generate structured updates for a research knowledge base (comparison-matrix and gap-tracker) after reading a paper. Use this skill when the user has completed reading notes for a paper and wants to update their knowledge base, or when they say 更新知识库, update matrix, update gap tracker, sync notes to KB, 把笔记同步到矩阵, or similar. Also trigger when the user uploads or references a completed paper reading note (from the paper-reading-notes skill) and asks what should change in their cross-topic files. This skill reads a finished reading note and produces two update files - a comparison-matrix entry and gap-tracker updates, both in the researchers v2 format with evidence traceability."
---

# Knowledge Base Maintenance

## Purpose

After the researcher finishes reading a paper and completes their reading note (typically produced by the `paper-reading-notes` skill), this skill extracts the relevant information and generates structured updates for two cross-topic files:

1. **comparison-matrix**: A new or updated system entry with dimension values, evidence source tags, and experimental data
2. **gap-tracker**: New gap signals, new evidence for existing gaps, counter-evidence, or status changes

The researcher reviews these updates and manually merges them into their knowledge base. This skill never modifies the original files directly — it only produces update proposals.

## When This Skill Triggers

- User says "更新知识库" / "update KB" / "sync to matrix" after finishing a reading note
- User uploads a completed reading note and asks what should change in comparison-matrix or gap-tracker
- User asks "这篇论文对 Gap A-1 有什么新证据？"
- User asks to compare a newly-read paper against existing matrix entries

## Required Input

This skill needs TWO things:

1. **A completed reading note** — either uploaded as a file or already in the conversation. Must follow the paper-reading-notes template (has sections: Meta, Problem Setting, Core Method, Key Results, Limitations, Relation to My Research)

2. **The current state of comparison-matrix and gap-tracker** — either uploaded as files, pasted in conversation, or available in the uploads directory. If not provided, ask the user for them.

## Workflow

### Step 0: Load Format References

```
view /mnt/skills/kb-maintenance/references/matrix-format.md
view /mnt/skills/kb-maintenance/references/tracker-format.md
```

These define the exact output formats. Follow them precisely.

### Step 1: Parse the Reading Note

Extract these elements from the reading note:

**For comparison-matrix update:**
- System name, source domain, task type (from Meta)
- Method's memory mechanism: what type? how persistent? whose perspective? (from Core Method)
- Self-evolution capability: what kind? when does it happen? (from Core Method)
- Cross-task transfer ability (from Core Method + Key Results)
- Benchmark results with numbers (from Key Results table)
- Design choices and ablation status (from Design Choices table)

**For gap-tracker update:**
- Gap signals with original text evidence (from "Gap Signals" section)
- Limitations that connect to known Gaps (from "Limitations" section)
- Experimental results showing performance drops in specific conditions (from "Key Results")
- Citation tracking items that relate to existing Gaps (from "Citation Tracking")

### Step 2: Check Against Existing Knowledge Base

If the current comparison-matrix and gap-tracker are available:

**For comparison-matrix:**
- Does this system already have an entry? If yes, this is an UPDATE (mark changed fields as `[S→P]`). If no, this is a NEW ENTRY.
- Are there existing entries that this paper directly compares against? Note any corrections needed.

**For gap-tracker:**
- Does the paper provide new evidence for any existing Gap? (Check each A-class and B-class Gap)
- Does the paper partially or fully solve any existing Gap? (Counter-evidence)
- Does the paper reveal a new Gap not currently tracked?
- Should any Gap's evidence level change? (C→B if new single-source evidence, B→A if now multiple sources)

### Step 3: Generate Comparison-Matrix Update

Output a markdown block following the exact format in `references/matrix-format.md`.

Rules:
- Every dimension value MUST have an evidence source tag: `[P]` with (Author, Year, §Section, p.Page)
- If a dimension cannot be determined from the paper, write "未明确提及 `[P]`" — don't guess or infer from the survey
- Include ALL available benchmark results in the experimental data table
- If this is an update to an existing entry, clearly mark which fields changed and why

Language convention:
- Dimension values and evidence citations: English
- Qualifiers and analytical notes within cells: Chinese (e.g., "雏形——有操作记录但无归纳机制")
- "Last Updated" reason: Chinese

### Step 4: Generate Gap-Tracker Updates

This section may contain multiple types of updates. Organize them clearly:

#### 4a. New Evidence for Existing Gaps

For each existing Gap that receives new evidence from this paper:

```markdown
## 🔄 Update to [Gap ID]: [Gap Title]

**New evidence from [Paper Name]**:
| # | Location | Evidence Content | Evidence Type |
|---|----------|-----------------|---------------|
| N+1 | §X, p.Y | "quote" or data description | type |

**Impact on evidence level**: [stays at X / upgrades from X to Y]
**Impact on status**: [no change / should change to ___]

**Suggested addition to Update Log**:
| Date | Event | Change |
|------|-------|--------|
| YYYY-MM-DD | [Paper] 精读 | 新增原文证据 #N+1; 证据等级 [变化描述] |
```

#### 4b. Counter-evidence for Existing Gaps

If this paper partially or fully addresses an existing Gap:

```markdown
## ⚠️ Counter-evidence for [Gap ID]: [Gap Title]

**This paper does**: [what it solves]
**This paper does NOT do**: [why the Gap still holds, or why it should be marked 已推翻]

**Suggested addition to Counter-evidence Check table**:
| Paper | What it did | What it didn't do |
|-------|------------|-------------------|
| [This paper] | ... | ... |
```

#### 4c. New Gap Signals

If the paper reveals a Gap not currently tracked:

```markdown
## 🆕 New Gap Signal: [Proposed Title]

**Statement**: [one sentence]
**Provisional evidence level**: B / C
**Evidence**:
| # | Paper | Location | Evidence Content | Evidence Type |
|---|-------|----------|-----------------|---------------|
| 1 | [This paper] | §X, p.Y | "..." | ... |

**Potential classification**: A / B / C class
**Reasoning**: [why this might be a valuable Gap]

> ⚠️ NEEDS YOUR INPUT: 这是初步识别的 Gap 信号，需要你判断：(1) 是否与你的 RQ 相关？(2) 是否值得追踪？(3) 应归入哪一类？
```

### Step 5: Output

Generate TWO files:

1. `/mnt/user-data/outputs/[short-name]-matrix-update.md` — the comparison-matrix entry
2. `/mnt/user-data/outputs/[short-name]-tracker-update.md` — all gap-tracker updates

Where `[short-name]` matches the reading note's short name (e.g., `appagent`, `awm`).

Use `present_files` to share both files with the user.

### Step 6: Post-output Summary

After presenting files, give the user a concise summary:

```
知识库更新建议已生成：

📊 Comparison Matrix:
- [NEW ENTRY / UPDATE]: [系统名] — [简述关键维度值]
- 实验数据: [几个 benchmark 已填入]

📋 Gap Tracker:
- 🔄 现有 Gap 更新: [列出受影响的 Gap ID 和变化]
- ⚠️ 反证发现: [如有]
- 🆕 新 Gap 信号: [如有]

标记了 ⚠️ NEEDS YOUR INPUT 的部分需要你确认后再合并。
```

## Quality Criteria

- [ ] Every `[P]` tagged cell has a complete citation (Author, Year, §Section, p.Page)
- [ ] No dimension value is guessed — if not in the paper, marked as "未明确提及"
- [ ] Experimental data table has actual numbers from the paper, not approximations
- [ ] Gap evidence uses direct quotes or specific data points, not paraphrases
- [ ] Counter-evidence check is attempted for every A-class Gap that the paper might relate to
- [ ] New Gap signals include evidence level assessment and relevance question for the researcher
- [ ] All `⚠️ NEEDS YOUR INPUT` blocks contain a preliminary AI suggestion

## Important Notes

- This skill produces UPDATE PROPOSALS, not final content. The researcher always makes the final merge decision.
- Do NOT fabricate page numbers or section references. If the reading note doesn't include precise locations, flag this: "精读笔记中未标注具体位置，建议回查原文确认"
- When in doubt about a Gap connection, include it as a `⚠️ NEEDS YOUR INPUT` item rather than omitting it. False negatives (missing a connection) are worse than false positives (suggesting a connection the researcher rejects).
- If the reading note is incomplete (missing sections or `⚠️ NEEDS YOUR INPUT` items not yet filled), still generate what you can, but note which updates are provisional: "以下更新基于未经确认的初步分析，待研究者补充后可能需要修正"