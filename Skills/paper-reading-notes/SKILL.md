---
name: paper-reading-notes
description: Generate or audit structured reading notes from academic paper PDFs for a literature review knowledge base. Use this skill whenever the user uploads a PDF of a research paper and wants reading notes, a paper summary following their template, or asks to "read this paper", "take notes on this paper", "精读这篇论文", "生成笔记", or similar requests involving academic paper analysis. Also trigger when the user mentions paper priority (P0/P1/P2), reading passes, asks whether an existing note truly meets Pass 2, wants to double check citations against the PDF, or wants knowledge base updates in the context of paper notes. This skill produces or audits a structured markdown note with extracted evidence, design choices, limitations, and gap signals — not a generic summary.
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
- User asks to audit an existing reading note, especially one already marked `Pass 2`
- User asks to double check citations / page numbers / quotes against the original PDF
- User wants to know whether a note can really support survey writing or KB updates without re-reading the paper

## Workflow

### Step 1: Identify Mode and Read the PDF / Existing Note

There are two valid entry modes:

- **Draft mode**: create a new reading note from a PDF
- **Audit mode**: review an existing note, especially a note already labeled `Pass 2`

In **Audit mode**, read the existing note first and treat the `Pass 2` label as untrusted until the audit confirms it.

First, read the PDF skill for file handling:
```
view /mnt/skills/public/pdf/SKILL.md
```

Then locate the original PDF. Prefer the repo copy under `papers/source/` when available. If the user uploaded a PDF for this turn, use that copy.

Extract the full text from the PDF. Use `pdfplumber` for text extraction as it preserves layout better:

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

If you are re-reading the PDF for quote verification or `Pass 2` audit, keep a **clean extracted text** file under the same topic's `papers/` tree so future quote checks do not require fresh extraction.

Preferred location:

```text
<topic>/papers/text/<pdf-stem>_clean.txt
```

Rules for the clean text file:

- Keep only the readable text needed for accurate quotation and page lookup
- Preserve page markers such as `--- Page N ---`
- Remove obvious extraction noise when safe to do so (duplicated blank lines, broken line wraps, repeated headers/footers if clearly identifiable)
- Do NOT save multiple noisy variants like `_layout`, `_raw`, `_debug` unless the user explicitly asks
- If `papers/text/` does not exist, create it

### Step 2: Read the Note Template, Audit Checklist, and Style Guide

```
view /mnt/skills/paper-reading-notes/references/note-template.md
view /mnt/skills/paper-reading-notes/references/quality-checklist.md
view /mnt/skills/paper-reading-notes/references/style-guide.md
```

The template defines the output structure. The checklist defines whether the note can remain `Pass 1`, be promoted to `Pass 2`, or be downgraded from an existing `Pass 2` label after audit. The style guide defines the note's positioning and language contract. Read all three before writing.

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

In **Audit mode**, do not rewrite everything blindly. First identify which claims are decision-critical for `Pass 2`:

- core problem / insufficiency quotes
- key design choices and ablation status
- author-stated limitations
- observed limitations
- gap signals
- connections to other papers / KB update readiness

Only reopen and patch the sections whose evidence chain is weak, missing, or suspicious.

### Step 4: Positioning and Language Convention

Treat the reading note as a **research intermediate artifact**, not as:

- final survey prose
- a generic summary
- a temporary TODO draft

Follow this language contract:

- **Template structure / headers / table headers**: English
- **Direct quotes / paper terminology / benchmark names / model names / metric names**: English
- **Analytical commentary / observations / research linkage**: Chinese

Default rule:

> **Chinese for analysis, English for evidence fidelity.**

Required style constraints:

- Do not write mixed Chinese-English slang sentences
- Do not switch terminology for the same concept within one note
- Do not write `Relation to My Research` like a generic survey paragraph
- Do not keep unresolved placeholders in notes that are meant to support KB sync

If uncertainty remains:

- write `原文未明确说明`
- or write `当前判断基于 Table X + Section Y 的间接证据`

instead of leaving vague placeholders or guesses.

Example of correct style:
```markdown
## Limitations
- **Author-stated limitations**: "Our method requires pre-defined action spaces and cannot handle novel UI elements" (Section 6, p.9)
- **My observed limitations**:
  1. 该方法只在 Android 平台验证，跨平台泛化仍未证明。
  2. 实验任务平均步骤数较短，因此对长序列任务的支持证据不足。
- **Experimental design gaps**: 缺少与更强 recent baseline 的统一重跑对比。
```

### Step 5: Run the Pass 2 Audit

After the draft note is filled, run the checklist in:

```
view /mnt/skills/paper-reading-notes/references/quality-checklist.md
```

Apply these rules strictly:

- New notes start as `Pass 1` unless the audit proves otherwise.
- Existing notes labeled `Pass 2` must also pass the same audit again; do not trust the old label by default.
- Do NOT mark a note as `Pass 2` just because every section in the template is non-empty.
- Upgrade to `Pass 2` only if every `Hard Gate` passes and the note is strong enough to support `comparison-matrix` / `gap-tracker` updates without reopening the PDF.
- If any `Hard Gate` fails, keep or change the note to `Pass 1` and record the blocking items for the user.
- If a claim depends on inference rather than direct evidence, keep the note at `Pass 1` unless the inference is clearly labeled and the supporting quote/data is still present.

When auditing an existing `Pass 2` note, use a skeptical standard:

- If a direct quote cannot be verified quickly from the note alone, re-check the PDF
- If page numbers or section references look uncertain, re-check the PDF
- If a gap signal is strong enough to influence `comparison-matrix` / `gap-tracker`, re-check the PDF unless the note already contains exact supporting quote/data
- If the note cannot support a survey paragraph without reopening the PDF, it is not truly `Pass 2`

Typical blockers for `Pass 2`:

- missing section/page references in core evidence fields
- gap signals that are mostly inference, not quote/data-backed
- limitations that only restate the authors' own wording
- research linkage too vague to place into the survey or KB
- direct quotes that cannot be confidently traced back to the original PDF

Necessary conclusion for a true `Pass 2` note:

- the paper can be written into a survey paragraph directly from the note
- `comparison-matrix` and `gap-tracker` can be updated from the note without reopening the PDF
- core claims are fully supportable from the paper's original wording or result tables

### Step 6: Output

Save the completed note to: `/mnt/user-data/outputs/<short-name>-notes.md`

Where `<short-name>` is a lowercase-hyphenated version of the paper's short name or system name (e.g., `appagent-notes.md`, `awm-notes.md`).

After saving, use `present_files` to share with the user.

### Step 7: Post-output Reminder

After presenting the file, remind the user:

```
笔记已生成。

- 如果这是 `Pass 1` 草稿：请重点检查 `My observed limitations`、`Relation to My Research` 和 `Gap Signals` 是否需要进一步收口。
- 如果这是 `Pass 2` 笔记：它应已可直接支持 KB 同步，不应再残留未收口占位。
```

Also report the audit result in plain language:

- If promoted: `Pass 2 audit: passed` + 2-3 reasons it passed
- If not promoted: `Pass 2 audit: not yet` + the blocking checklist items
- If re-auditing an old `Pass 2` note that fails: `Pass 2 audit: failed on re-check` + whether the note was downgraded to `Pass 1`
- If the PDF was reopened: report that the original was re-checked and include the saved clean text path

## Quality Criteria

Minimum quality checks before delivery:
- [ ] One-line summary contains: subject + method + benchmark + number
- [ ] Problem setting has direct quotes with Section + page references
- [ ] Design Choices table is filled; ablation verification column is marked
- [ ] Limitations include at least one observation NOT stated by the authors
- [ ] Gap signals have original text evidence (Section + page), not just inference
- [ ] Key Passages section has 1-3 critical quotes with exact locations
- [ ] Language follows the rule: Chinese analysis + English evidence anchors
- [ ] Research-facing sections are aligned with the current main line / gap tracker rather than generic commentary

For `Pass 2` decisions, use the full audit in `references/quality-checklist.md` rather than only this short list.

## Important Notes

- Do NOT hallucinate page numbers or section references. If you cannot locate the exact position, write "位置待确认" instead of guessing.
- Do NOT copy the abstract as the method overview. Rewrite in your own words.
- Do NOT leave the Design Choices table empty — even a 2-row table is better than none. If the paper doesn't clearly describe design choices, note what you can infer and mark them as "从实验设置推断".
- If table extraction from the PDF is poor (garbled text), note this and suggest the user manually fill in the Key Results table.
- The priority of this skill is **evidence extraction accuracy**. A shorter note with correct page references beats a longer note with vague attributions.
- `Pass 2` is a readiness judgment, not a formatting judgment. A complete-looking note can still be only `Pass 1`.
- For `Pass 2` re-audits, prefer false-negative over false-positive. If evidence feels shaky, re-open the PDF and verify.
- In finalized notes, prefer fully written analytical judgments over `⚠️ NEEDS YOUR INPUT`. Placeholders are acceptable only for genuine unresolved researcher decisions, not as the default output style.
