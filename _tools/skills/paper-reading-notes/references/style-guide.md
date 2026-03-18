# Reading Notes Style Guide

## Positioning

Reading notes are not:

- final survey prose
- generic summaries
- temporary TODO drafts

They are a **research intermediate artifact** serving three downstream uses:

1. KB synchronization
2. survey writing
3. method design

Definition:

> Reading note = Chinese analytical skeleton + English evidence anchors + main-line-aware judgment.

## Language Rule

Default rule:

> **Chinese for analysis, English for evidence fidelity.**

Use Chinese for:

- problem explanation
- method interpretation
- limitations analysis
- relation to the researcher's main line
- connections to other papers

Keep English for:

- title / venue / authors
- benchmark / metric / model / method names
- direct quotes
- section names and exact paper terminology where precision matters

## Do Not

- write mixed Chinese-English slang sentences
- switch terminology for the same concept within one note
- write reading notes like final survey prose
- leave TODO / TBD / unresolved placeholders in finalized notes
- keep `⚠️ NEEDS YOUR INPUT` in notes that are supposed to be ready for KB sync

## Preferred Terminology

- `Procedural Memory（程序性记忆）` -> later use `程序性记忆`
- `Episodic Memory（情节记忆）` -> later use `情节记忆`
- `Semantic Memory（语义记忆）` -> later use `语义记忆`
- `Working Memory（工作记忆）` -> later use `工作记忆`
- `experience-dependent procedural knowledge` -> `经验依赖的程序性知识`
- `experience-delta procedural rule` -> `经验差分程序规则`
- `failure-aware write-back` -> `失败感知写回`

## Section-Level Rule

- `One-line Summary`: one Chinese sentence with benchmark + number
- `Problem Setting`: paper-faithful, minimal interpretation
- `Core Method`: explain design choices, not abstract copy-paste
- `Key Results`: result + comparison + implication
- `Limitations`: separate author-stated vs observed vs experimental-design gaps
- `Relation to My Research`: fully aligned with main line / gap tracker / taxonomy
- `Connections to Other Papers`: every link must specify relation type
- `Key Passages`: only high-value English quotes

## Final Readiness Rule

A note is ready for KB synchronization only if:

- terminology is stable
- language follows the Chinese-analysis / English-evidence split
- no unresolved placeholders remain
- research-facing sections are consistent with the current main line
- core results and quotes are traceable without reopening the PDF
