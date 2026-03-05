# Paper Reading Note Template

Use this exact structure for every paper note. Sections marked with `[AI]` should be filled by Claude from the PDF content. Sections marked with `[HUMAN]` require the researcher's judgment — generate a preliminary suggestion but wrap it in a `> ⚠️ NEEDS YOUR INPUT:` blockquote so it's visually distinct and easy to find.

---

```markdown
# [Short Name] — [One-line core contribution]

## Meta
- **Title**: [Full English title]
- **Authors**: [First author et al.] | [Institution]
- **Venue**: [Conference/Journal, Year] | arXiv:[ID]
- **Links**: [PDF] | [Code] | [Project]
- **Citation count**: [As of reading date] | **Read date**: YYYY-MM-DD
- **Priority**: P0 / P1 / P2 | **Reading progress**: Pass 1 / Pass 2 / Pass 3

## One-line Summary
<!-- Format: WHO did WHAT on WHICH benchmark, improving by HOW MUCH -->
[AI fills this]

## Problem Setting
- **Core problem**: [Precise quote of author's formulation, with Section & page number]
- **Assumptions**: [Input conditions, scenario constraints the method relies on]
- **Insufficiency of existing approaches**: [Quote from paper, with page number]

## Core Method
- **Method overview**: [2-3 paragraphs in your own words, NOT copied from abstract]
- **Key Design Choices**:

| Design Decision | Author's Choice | Author's Rationale | Ablation Verified? |
|----------------|----------------|--------------------|--------------------|
| [AI extracts] | ... | ... | Yes / No |

- **Core difference from prior work**: [What makes this method distinct]

## Key Results

| Benchmark | This Method | Strongest Baseline | Δ | Notes |
|-----------|------------|-------------------|---|-------|
| [AI fills from experiment tables] | ... | ... | ... | ... |

- **Key ablation findings**: [Which component contributes most? Which was NOT ablated?]
- **Failure cases**: [What failure modes did authors show?]

## Limitations
- **Author-stated limitations**: [Quote + page number]
- **My observed limitations**: 
> ⚠️ NEEDS YOUR INPUT: [AI provides preliminary observations, but you should verify and add your own]
- **Experimental design gaps**: [Benchmark coverage? Baseline omissions? Metric bias?]

## ⭐ Relation to My Research

### Position in Survey
- **Corresponding survey section/category**:
> ⚠️ NEEDS YOUR INPUT: [AI suggests based on paper content, you confirm]
- **Role**: Positive example / Contrastive baseline / Background reference

### Gap Signals (extracted from this paper)
<!-- Only record gaps with textual evidence from the paper -->
- Gap signal 1: "[Quote]" (Section X, p.Y) → implies ___
- Gap signal 2: Experimental results show ___ scenario performance drops ___%, implying ___

> ⚠️ NEEDS YOUR INPUT: 评估以上 Gap 信号的价值——是否与你的 RQ 直接相关？证据等级是 A/B/C？

### Reusable Elements
- **Methodology**: [Which module? How could it be reused or adapted?]
> ⚠️ NEEDS YOUR INPUT: 具体如何迁移到你的方法中？
- **Experimental design**: [Which benchmark config / ablation design is transferable?]

### Connections to Other Papers in Knowledge Base
> ⚠️ NEEDS YOUR INPUT: 与 [Paper X] 的关系（互补/竞争/扩展/前驱）+ 具体描述

## Citation Tracking
- [ ] [Paper name]: Tracking reason (supports Gap X / validates Method Y / understanding Tech Z)

## Key Passages
<!-- Only 1-3 sentences critical to your argumentation, with Section and page number -->
> "..." (Section X, p.Y)
```