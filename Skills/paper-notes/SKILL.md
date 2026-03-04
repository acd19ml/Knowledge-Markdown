---
name: paper-notes
description: >
  Complete academic paper processing workflow for the Knowledge-Markdown
  knowledge base at /Users/mac/studyspace/Knowledge-Markdown/. Use this skill
  whenever the user provides a PDF path for a research paper and wants
  structured notes, or says things like "处理这篇论文", "给这篇论文做笔记",
  "把这篇paper加进知识库", "读一下这个PDF", "分析这篇论文", "帮我记录这篇文献",
  or simply drops a .pdf file path in the conversation. The skill handles the
  full pipeline: PDF extraction → structured analysis (three-pass reading) →
  Chinese markdown notes with English technical terms and links → automatic
  updates to comparison-matrix.md and gap-tracker.md → quality checklist
  verification. Always invoke this skill for any academic paper note-taking
  task in the Knowledge-Markdown project, even if the user only asks a simple
  question like "把这篇论文的笔记加进去".
---

# Paper Notes — Complete Workflow

Knowledge base root: `/Users/mac/studyspace/Knowledge-Markdown/`

Work through the steps below in order. Don't skip steps.

---

## Step 1: Extract PDF

Use pdfplumber (already installed) to extract full text:

```python
import pdfplumber
with pdfplumber.open("<pdf_path>") as pdf:
    text = "\n".join(page.extract_text() or "" for page in pdf.pages)
print(text[:3000])   # sanity check first 3k chars
```

If the PDF is large (>50 pages), also extract page-by-page to enable targeted re-reads during analysis.

---

## Step 2: Determine Target Directory

Infer the right topic directory from the paper content:

| Topic | Directory |
|-------|-----------|
| GUI agents, web agents, computer-use agents, UI automation | `GUI_Agent/papers/` |
| Memory mechanisms (episodic, semantic, working, procedural) | `Agent_Memory/papers/` |
| Self-evolving, self-improving, continual learning agents | `Self_Evolve/papers/` |
| Industry talks, podcasts, practitioner perspectives | `Industry_Insights/` |
| New topic | Create `<TopicName>/papers/` and inform the user |

If the paper spans multiple topics (e.g., GUI Agent + Memory), pick the primary topic and note the cross-topic connection in the note.

If genuinely uncertain, ask the user.

---

## Step 3: Analyze the Paper (Three-Pass Reading)

Think through the paper in three passes. You have the full text, so do this mentally — don't output intermediate pass summaries unless the user asks.

**Pass 1 (scan):** Title → Abstract → last two paragraphs of Introduction → Conclusion.
Extract: paper identity, one-sentence contribution, priority (P0/P1/P2), reading status.

**Pass 2 (structure):** Full text, skip proofs and implementation details.
Extract: core method, key results with numbers, limitations, relation to the user's research on GUI agents.

**Pass 3 (depth, as needed):** Experimental setup, ablation studies, appendix.
Extract: methodology details, reusable experimental designs, gap signals.

---

## Step 4: Generate the Paper Note

Read `references/note-template.md` for the exact template.

**Language rules** (strictly follow):
- **Chinese** — all analysis text, summaries, observations, section content
- **English** — paper titles, author names, benchmark/dataset names, arXiv IDs, URLs, model names, technical terms (write as `情节记忆 (Episodic Memory)` on first use)

**File naming:** `YYYY_ShortName.md` where ShortName is the paper's common abbreviation or first meaningful word (e.g., `2024_CogAgent.md`, `2025_WebVoyager.md`).

The **"⭐ 与我的研究的关系"** section is the most important. Explicitly connect to files already in the knowledge base:
- For memory mechanisms → relate to `Agent_Memory/` notes
- For self-improvement → relate to `Self_Evolve/` notes
- Identify whether this paper is a baseline, a competing approach, or an enabling technique for the user's survey work.

---

## Step 5: Quality Check

Before saving, verify every item in `references/quality-checklist.md`. Fix any that fail — don't just note them.

---

## Step 6: Save the Note

Save to `<KB_ROOT>/<topic_dir>/<YYYY_ShortName>.md`.

If `<topic_dir>` doesn't exist yet, create it and also create a `README.md` stub with a one-line topic description.

---

## Step 7: Update comparison-matrix.md

File: `<KB_ROOT>/<topic_dir>/comparison-matrix.md`

Read `references/analysis-tools.md` for the exact format.

- If the file doesn't exist, create it with the full header and dimension definitions before adding the row.
- Add one row for the new paper. Use `?` for any field not determinable from the paper.
- After adding the row, re-read all existing rows and update the **"从矩阵中观察到的模式"** section if any new pattern emerges.

---

## Step 8: Update gap-tracker.md

File: `<KB_ROOT>/<topic_dir>/gap-tracker.md`

Read `references/analysis-tools.md` for the exact format.

- If the file doesn't exist, create it with the full template.
- For each gap signal found in Step 4 (Section "Research Gap 信号"):
  - If the gap already exists in gap-tracker.md → add this paper as additional evidence and upgrade the strength rating if warranted (弱→中→强 as 1→2→3+ papers)
  - If it's a new gap → add a new entry with this paper as the sole evidence (strength: 弱)
- Reconsider the **"Gap 优先级排序"** if the new evidence changes the rankings.

---

## Step 9: Report to User

Provide a concise summary:

```
✓ 笔记已保存: <path>
✓ comparison-matrix.md: <N> → <N+1> 行，[新模式 or 无新模式]
✓ gap-tracker.md: <X> 个已有 gap，新增 <Y> 个
✓ 质量检查: 全部通过 / [指出哪条需要用户补充]

建议追踪阅读（来自"关键引用追踪"）:
- [论文名]: [原因]
- ...
```
