# Final Report Scope and Limitations Note

> Purpose:
> This note hardens the reporting boundary of the AWM reproduction project.
> It is written in a report-ready style so that the final report can reuse it directly or in condensed form.

---

## 1. Scope Boundary

This reproduction should be described as a **Mind2Web-centered first-run reproduction**, not as a full end-to-end replication of every benchmark and every experimental branch in the AWM paper.

More precisely:

- the executed main experiments are all on **Mind2Web**
- the evidence base covers `C1-C5` under the current Mind2Web implementation
- the current mechanism analysis is therefore a **Mind2Web mechanism analysis**, not a benchmark-agnostic statement about AWM in general

### Safe report wording

> Unless otherwise noted, all conclusions in this report are derived from Mind2Web experiments and should be interpreted as Mind2Web-specific evidence rather than benchmark-independent claims about AWM.

### Why this matters

The original paper also reports results on **WebArena**, and some of its more ambitious narratives, especially around workflow composition and broader environment transfer, are not fully testable from the current Mind2Web-only evidence base.

So the correct stance is:

- **not**: "the paper is reproduced in full"
- **but**: "the core Mind2Web claims and their mechanism-level implications have been deeply audited"

---

## 2. First-Run Boundary

All main result judgments in the current project are based on **first-run evidence**, not on repeated trials with variance estimates.

This applies to:

- `C1` site-wise reproduced / not reproduced judgments
- `C2` cross-site online generalization judgments
- `C3` LM-vs-rule comparisons
- `C4` representation ablations
- `C5` workflow-quality statistics

### Safe report wording

> All reproduced / not reproduced judgments in this report should be read as first-run judgments under the current implementation and prompt setup, not as repeated-estimate conclusions with variance bounds.

### Why this matters

This does **not** make the conclusions unusable. It means the report should avoid over-claiming:

- `not reproduced` should not be written as "definitively false"
- `reproduced` should not be written as "robustly established across reruns"

Instead, the correct style is:

- `supported by first-run evidence`
- `not reproduced in the current first-run setting`
- `directionally supported`
- `mixed under current evidence`

---

## 3. Coverage Boundary: `AWM_AS` Not Covered

The current project does **not** reproduce the paper's action-space extension experiment (`AWM_AS`, paper §5 / Table 9).

### Current status

- no direct implementation-level reproduction of `AWM_AS`
- no parallel comparison between standard AWM and extended-action AWM
- no independent verification of the paper's "18.5% call rate" style efficiency claim in that branch

### Interpretation

This should be treated as a **coverage limitation**, not as a hidden omission.

The reason it is acceptable is that the present project prioritized:

- the core Mind2Web result lines
- the main mechanism questions behind C1-C5
- the paper's central claims about workflow usefulness, induction style, representation, and workflow quality

### Safe report wording

> We did not reproduce the paper's `AWM_AS` action-space extension branch. This is a scope limitation of the current study rather than a contradictory finding; the present report focuses on the core Mind2Web result lines and their mechanism-level interpretation.

---

## 4. Metric Boundary: Alignment Rate Is Exploratory

The `alignment rate` analysis should be reported as an **exploratory heuristic**, not as a strong metric.

### What it is

The current implementation uses:

- keyword overlap between workflow pattern descriptions
- and observation / target-step context

This is useful for a directional check, but it is not a strong semantic matching metric.

### What it does support

It can support a modest claim such as:

> workflow-target alignment does not show a simple positive monotonic relation with success under the current Mind2Web first-run evidence.

### What it does not support

It should **not** be used to claim:

- a precise causal law
- a stable threshold for success
- a benchmark-independent quality metric

### Safe report wording

> The alignment-rate analysis is exploratory. It is based on a keyword-overlap heuristic rather than a stronger semantic matching method, and should therefore be interpreted as suggestive evidence rather than as a decisive metric.

---

## 5. Recommended Reporting Stance

If the report wants to remain rigorous under scrutiny, the safest global stance is:

1. The study provides a **deep Mind2Web reproduction and mechanism audit** of AWM.
2. The study does **not** claim full-paper, all-benchmark, repeated-trial reproduction.
3. Strongest conclusions should be attached to:
   - step-level decomposition
   - paired-case distributions
   - cross-site failure diagnosis
   - workflow text comparisons
4. More interpretive claims should be explicitly labeled as:
   - `first-run`
   - `exploratory`
   - `working hypothesis`
   - `case-level evidence`

---

## 6. One-Paragraph Report Version

> This report should be read as a Mind2Web-centered first-run reproduction and mechanism audit of AWM. It covers the paper's main Mind2Web result lines (`C1-C5`) and analyzes why they hold, fail, or become conditional under the current implementation. The scope does not include the paper's WebArena branch or the `AWM_AS` action-space extension experiment, so the resulting conclusions are not full-paper claims. In addition, all reproduced / not reproduced judgments are first-run judgments rather than repeated-trial estimates, and the alignment-rate analysis is reported only as an exploratory heuristic rather than a strong metric. These boundaries are intentional and should be treated as part of the study's reporting discipline rather than as hidden omissions.

---

## 7. Reviewer-Facing Short Version

> Scope note: this is a Mind2Web-only, first-run reproduction of the core AWM result lines and their mechanism-level implications. We do not claim full-benchmark coverage, we do not include `AWM_AS`, and we treat alignment rate as exploratory rather than definitive.
