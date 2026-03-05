---
name: paper-reading-notes
description: Generate structured reading notes from academic paper PDFs for a literature review knowledge base. Use this skill whenever the user uploads a PDF of a research paper and wants reading notes, a paper summary following their template, or asks to "read this paper", "take notes on this paper", "精读这篇论文", "生成笔记", or similar requests involving academic paper analysis. Also trigger when the user mentions paper priority (P0/P1/P2), reading passes, or knowledge base updates in the context of uploaded PDFs. This skill produces a structured markdown note with extracted evidence, design choices, limitations, and gap signals — not a generic summary.
---

# Paper Reading Notes Generator

## Purpose

Transform an uploaded academic paper PDF into a structured reading note that follows a specific research methodology template. The note serves as an entry in the researcher's knowledge base for writing a survey and eventually a top-venue paper.

The key insight: this is NOT a generic paper summary. It's an **evidence extraction** task. Every section of the output must trace back to specific locations in the paper (Section + page number). The researcher will use these notes to build argumentation chains (Claim → Evidence → Reasoning) for their survey.

## When This Skill Triggers

- User uploads a PDF and asks for reading notes, paper analysis, or 精读笔记
- User mentions "add this to my knowledge base" with a PDF
- User asks to analyze a paper following their template
- User uploads a paper and asks about its methods, gaps, or relation to their research

## Workflow

### Step 1: Read the PDF

First, read the PDF skill for file handling:
```
view /mnt/skills/public/pdf/SKILL.md
```

Then extract the full text from the uploaded PDF. Use `pdfplumber` for text extraction as it preserves layout better:

```python
import pdfplumber

with pdfplumber.open("/mnt/user-data/uploads/<filename>.pdf") as pdf:
    full_text = ""
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            full_text += f"\n--- Page {i+1} ---\n{text}"
```

Also extract tables separately — they contain key experimental results:

```python
    all_tables = []
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            all_tables.append({"page": i+1, "table_index": j, "data": table})
```

### Step 2: Read the Note Template

```
view /mnt/skills/paper-reading-notes/references/note-template.md
```

This template defines the exact output structure. Follow it precisely.

### Step 3: Fill the Template

Work through the template section by section. Here are the extraction strategies for each:

#### Meta Information
- **Title, Authors, Venue**: Extract from the first page header/footer area. If venue isn't clear from the PDF, note "Venue not identified in PDF — check manually."
- **arXiv ID**: Look for patterns like `arXiv:XXXX.XXXXX` in headers or footers.
- **Citation count**: Write "Check Semantic Scholar" — don't guess.
- **Read date**: Use today's date.
- **Priority & Reading progress**: Default to `P1` and `Pass 1`. The user will adjust.

#### One-line Summary
Format: `[System/Method name] [does what] on [which benchmarks], achieving [key metric improvement over baseline].`
Extract from Abstract + Conclusion. Be specific with numbers.

#### Problem Setting
This is critical — find the **exact quotes** where the authors state:
1. The problem they solve (usually Introduction paragraphs 1-3)
2. Why existing approaches are insufficient (usually Introduction paragraphs 3-5 or Related Work)
3. Their assumptions (often implicit — check the experimental setup)

Always include Section references and page numbers: `(Section 1, p.2)`

#### Core Method
- Write the overview in your own words, explaining the architecture/pipeline
- For the **Design Choices table**: identify every major architectural decision. Check if each one has a corresponding ablation experiment. This is crucial — unablated design choices are potential gaps.

#### Key Results
- Extract from the main results table(s). Identify the strongest baseline for each benchmark.
- Calculate Δ (delta) if not provided: `this_method - strongest_baseline`
- For ablation findings: identify which component removal causes the largest drop

#### Limitations
- **Author-stated**: Search for "limitation" section (usually near the end) and "future work"
- **Observed**: Look for:
  - Benchmarks that seem too easy or too narrow
  - Baselines that are missing (recent strong systems not compared)
  - Assumptions that might not hold in practice
  - Scalability concerns not addressed

#### Gap Signals
Search the paper for:
- Phrases like "we leave X to future work", "beyond the scope", "does not address"
- Experimental results where performance drops significantly in specific conditions
- Comparisons where certain categories of methods are absent

Each gap signal MUST have a direct quote or data point with location.

### Step 4: Language Convention

Follow this mixed-language convention:
- **Template structure / headers / table headers**: English (matches the template)
- **Extracted quotes and technical terms**: English (preserve original)
- **Analytical commentary and observations**: Chinese (方便研究者思考)
- **`⚠️ NEEDS YOUR INPUT` sections**: Chinese (这些是给研究者的提示)

Example of correct style:
```markdown
## Limitations
- **Author-stated limitations**: "Our method requires pre-defined action spaces and cannot handle novel UI elements" (Section 6, p.9)
- **My observed limitations**: 
> ⚠️ NEEDS YOUR INPUT: 初步观察——作者仅在 Android 平台测试，未验证跨平台泛化能力。此外，实验中的任务复杂度较低（平均步骤数 < 5），无法说明方法在长序列任务上的表现。请确认这些观察是否与你的 RQ 相关。
```

### Step 5: Output

Save the completed note to: `/mnt/user-data/outputs/<short-name>-notes.md`

Where `<short-name>` is a lowercase-hyphenated version of the paper's short name or system name (e.g., `appagent-notes.md`, `awm-notes.md`).

After saving, use `present_files` to share with the user.

### Step 6: Post-output Reminder

After presenting the file, remind the user:

```
笔记已生成。以下部分标记了 ⚠️ NEEDS YOUR INPUT，需要你补充：
1. Priority 和 Reading progress 确认
2. "My observed limitations" 的验证和补充
3. Survey 中的定位（章节/分类）
4. Gap 信号的价值判断和证据等级
5. 可借鉴元素的迁移思路
6. 与知识库其他论文的关联

完成后，这篇笔记就可以并入你的知识库了。
```

## Quality Criteria

A good note satisfies these checks:
- [ ] One-line summary contains: subject + method + benchmark + number
- [ ] Problem setting has direct quotes with Section + page references
- [ ] Design Choices table is filled; ablation verification column is marked
- [ ] Limitations include at least one observation NOT stated by the authors
- [ ] Gap signals have original text evidence (Section + page), not just inference
- [ ] All `⚠️ NEEDS YOUR INPUT` blocks contain a preliminary AI suggestion (not left blank)
- [ ] Key Passages section has 1-3 critical quotes with exact locations

## Important Notes

- Do NOT hallucinate page numbers or section references. If you cannot locate the exact position, write "位置待确认" instead of guessing.
- Do NOT copy the abstract as the method overview. Rewrite in your own words.
- Do NOT leave the Design Choices table empty — even a 2-row table is better than none. If the paper doesn't clearly describe design choices, note what you can infer and mark them as "从实验设置推断".
- If table extraction from the PDF is poor (garbled text), note this and suggest the user manually fill in the Key Results table.
- The priority of this skill is **evidence extraction accuracy**. A shorter note with correct page references beats a longer note with vague attributions.