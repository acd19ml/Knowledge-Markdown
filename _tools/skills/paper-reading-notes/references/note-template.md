# Paper Reading Note Template

Use this exact structure for every paper note. The note is a research intermediate artifact for KB sync, survey writing, and method design. Default style is: **Chinese for analysis, English for evidence fidelity**. Only use `> ⚠️ NEEDS YOUR INPUT:` for genuine unresolved researcher decisions; do not leave it as the default output style for finalized notes.

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
[AI fills with finalized analytical judgment when evidence is sufficient; use `⚠️ NEEDS YOUR INPUT` only if a real researcher decision is still required]
- **Experimental design gaps**: [Benchmark coverage? Baseline omissions? Metric bias?]

## ⭐ Relation to My Research

### Position in Survey
- **Corresponding survey section/category**:
[AI fills with a concrete survey / taxonomy placement aligned with the current main line; use `⚠️ NEEDS YOUR INPUT` only if the placement is genuinely ambiguous]
- **Role**: Positive example / Contrastive baseline / Background reference

### Gap Signals (extracted from this paper)
<!-- Only record gaps with textual evidence from the paper -->
- Gap signal 1: "[Quote]" (Section X, p.Y) → implies ___
- Gap signal 2: Experimental results show ___ scenario performance drops ___%, implying ___

[AI should give a concrete preliminary value judgment and evidence level. Use `⚠️ NEEDS YOUR INPUT` only if this judgment would materially change the research direction.]

### Reusable Elements
- **Methodology**: [Which module? How could it be reused or adapted?]
[AI should write a concrete migration judgment when possible; reserve `⚠️ NEEDS YOUR INPUT` for truly unresolved design decisions]
- **Experimental design**: [Which benchmark config / ablation design is transferable?]

### Connections to Other Papers in Knowledge Base
[AI should state the relation type explicitly: 前驱 / 互补 / 竞争 / 扩展 / counter-evidence / blueprint / partial solution]

## Citation Tracking
- [ ] [Paper name]: Tracking reason (supports Gap X / validates Method Y / understanding Tech Z)

## Key Passages
<!-- Only 1-3 sentences critical to your argumentation, with Section and page number -->
> "..." (Section X, p.Y)
```
