# Gap Tracker v2 — Format Reference

## Gap Entry Format

```markdown
### [Gap ID]: [Short Title]

**Status**: `待验证` / `精读确认` / `需修正` / `已推翻`

**Statement**: (One sentence — precisely describe what is missing)

**Evidence Level**: A / B / C

**Primary Evidence**:
| # | Paper | Location | Evidence Content | Evidence Type |
|---|-------|----------|-----------------|---------------|
| 1 | Author (Year) | §X, p.Y | "direct quote" or data description | Direct statement / Experimental gap / Indirect implication |

> **Evidence Analysis**: [Why these pieces of evidence together support the Gap claim]

**Counter-evidence Check** (Has any paper partially solved this Gap?):
| Paper | What it did | What it didn't do (why Gap still holds) |
|-------|------------|----------------------------------------|
| ... | ... | ... |

> **Counter-evidence Conclusion**: [Is there a closest existing work? Why doesn't it fully address the Gap?]

**Cross-domain Intersection**:
- [Domain A] → [Domain B]: [specific technique/concept + citation]
- Why no one has done this: [explanation]

**Potential Approach**: [brief description]

**Feasibility Assessment**:
- Technical feasibility: High / Medium / Low (reason)
- Required resources: [datasets + frameworks]
- Relation to RQ: Corresponds to Sub-RQ ___

**Priority**: P0 / P1 / P2

**Update Log**:
| Date | Event | Change |
|------|-------|--------|
| YYYY-MM-DD | [what triggered the update] | [what changed] |
```

## Evidence Level Definitions (from methodology §6.1)

| Level | Definition | Operational Standard | Survey Phrasing |
|-------|-----------|---------------------|-----------------|
| **A (Strong)** | Multiple independent direct evidence | ≥ 2 papers explicitly state this Gap, OR ≥ 3 papers' experimental data indirectly prove it | "As [A] and [B] explicitly acknowledge..." |
| **B (Medium)** | Single source or indirect evidence | 1 paper mentions it explicitly, OR systematic absence observed in comparison matrix | "While [A] hints at..., no work has directly..." |
| **C (Weak)** | Reasonable inference only | Based on logic only, no original text support | Should NOT appear in survey — needs upgrade first |

## Status Definitions

| Status | Meaning | Next Step |
|--------|---------|-----------|
| `待验证` | Only Survey inference, not confirmed by original paper | Need to read related papers |
| `精读确认` | ≥ 2 original paper evidence, counter-evidence check done | Can be written into survey |
| `需修正` | Reading revealed original statement was inaccurate | Revise statement + re-collect evidence |
| `已推翻` | Reading found a paper that effectively solves this Gap | Record reason, remove from priority list |

## Rules

1. All Gap claims entering the Interim Survey must be level B or above
2. All Gap claims entering a top-venue paper Motivation must be level A
3. Every A-class Gap MUST have a completed counter-evidence check
4. C-level Gaps should either be upgraded (find evidence) or marked as `待验证`
5. The "Excluded Papers" section at the bottom tracks papers considered but not included, with exclusion reasons

## Excluded Papers Section

```markdown
## Excluded Papers
| Paper | Exclusion Reason | Date |
|-------|-----------------|------|
| ... | ... | YYYY-MM-DD |
```

## Update Triggers

The gap-tracker should be updated when:
- A new paper is read that provides evidence for/against an existing Gap
- A new Gap signal is discovered in a paper's limitations or experimental results
- A paper is found that partially or fully addresses an existing Gap
- The comparison matrix reveals a new systematic absence