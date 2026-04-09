# Final Report Writing Notes

> Purpose:
> This note turns the current analysis state into report-writing guidance.
> It is not a new analysis file. It tells the report what can be claimed, how strongly it can be claimed, and which appendix should support each claim.

---

## 1. Recommended Global Positioning

The final report should frame the project as:

> a **Mind2Web-centered, first-run reproduction and mechanism audit** of AWM

not as:

> a full-paper, all-benchmark, repeated-trial replication

This framing is already supported by:

- [scope-and-limitations.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/report/scope-and-limitations.md)
- [reproduction-status.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/reproduction-status.md)

---

## 2. What the Report Can Now Say Strongly

These claims are safe as main-text claims, provided that the attached appendix references are kept.

### 2.1 C1 mechanism

Safe wording:

> AWM's gains on Mind2Web are driven less by uniform all-step help than by a narrow set of beneficial interventions, especially stable TYPE-side value guidance and site-dependent CLICK grounding improvements.

Appendix support:

- [A1-step-level-breakdown.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A1-step-level-breakdown.md)
- [A2-paired-case-summary.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A2-paired-case-summary.md)

### 2.2 C2 online trade-off

Safe wording:

> The current Mind2Web evidence suggests an offline-vs-online trade-off rather than a simple dominance relation: offline workflows are broader and steadier on CLICK-side grounding, while online workflows are more test-proximate and stronger on local TYPE/value guidance, but also more vulnerable to trajectory-shaped errors under larger shift.

Appendix support:

- [A7-offline-vs-online-tradeoff.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A7-offline-vs-online-tradeoff.md)
- [A3-cross-site-diagnosis.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A3-cross-site-diagnosis.md)

### 2.3 Small-data efficiency

Safe wording:

> Under the current first-run evidence, online memory shows genuine very-small-budget gains on `kayak`, but this early-gain pattern does not generalize reliably to `tripadvisor` or `reddit`.

Appendix support:

- [A8-online-small-data-efficiency.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A8-online-small-data-efficiency.md)

### 2.4 LM vs Rule

Safe wording:

> LM-induced workflows are clearly more abstract and reusable than rule-induced workflows at the text level, but this abstractness does not automatically yield stronger site-wise performance.

Appendix support:

- [C1-lm-vs-rule-text-evidence.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/C1-lm-vs-rule-text-evidence.md)
- [A3-cross-site-diagnosis.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A3-cross-site-diagnosis.md)

### 2.5 Composition on Mind2Web

Safe wording:

> On Mind2Web, AWM shows signs of composition mainly as a flat library of reusable subflows rather than as explicit hierarchical workflow composition.

Appendix support:

- [C5-mind2web-compositionality-reading.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/C5-mind2web-compositionality-reading.md)

---

## 3. What the Report Must Keep Soft

These points are usable, but only with explicit qualifiers.

### 3.1 Alignment rate

Allowed:

> exploratory heuristic
> does not show a simple positive monotonic relation

Not allowed:

> strong quality metric
> causal score
> validated threshold

Support:

- [A6-alignment-rate-note.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A6-alignment-rate-note.md)

### 3.2 Workflow-first behavior

Allowed:

> case-level evidence suggests
> consistent with workflow-first behavior

Not allowed:

> the model generally obeys workflows over reasoning

Support:

- [B4-sixflags-negative-case.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/B4-sixflags-negative-case.md)
- [B6-tripadvisor-cross-site-negative.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/B6-tripadvisor-cross-site-negative.md)

### 3.3 Success predictor

Allowed:

> working hypothesis
> first-run post-hoc pattern

Not allowed:

> validated success law
> universal threshold rule

Support:

- [A1-step-level-breakdown.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A1-step-level-breakdown.md)
- [C4-site-feature-qualitative-coding.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/C4-site-feature-qualitative-coding.md)
- [C5-mind2web-compositionality-reading.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/C5-mind2web-compositionality-reading.md)

---

## 4. Recommended Narrative Arc for the Final Report

A strong report version should move in this order:

1. **Result audit**
   - C1-C5 reproduced / not reproduced summary
2. **Mechanism decomposition**
   - step-level and paired-case evidence
3. **Online trade-off**
   - offline vs online mechanism contrast
   - small-data efficiency as conditional rather than universal
4. **Representation and induction style**
   - LM vs Rule
   - code/text and NL/HTML
5. **Boundary conditions**
   - failure taxonomy
   - site-feature dependence
   - Mind2Web compositionality is flatter than the stronger paper narrative
6. **Scope and limitations**
   - Mind2Web-only
   - first-run
   - no `AWM_AS`
   - alignment heuristic is exploratory

---

## 5. Suggested “Contribution” Framing

The report should emphasize that its contribution is not just score checking.

A safe framing is:

> The study goes beyond numeric reproduction by turning the paper's verbal claims into step-level, paired-case, and prompt-level evidence, and by identifying where the original AWM narrative is supported, weakened, or needs to be rewritten conditionally under Mind2Web evidence.

This is stronger than saying only:

> we reproduced some tables

and safer than saying:

> we fully validated or falsified the whole paper

---

## 6. Minimal Appendix Set for the Final Report

If the final report must keep the appendix compact, the following set is sufficient:

- [A1-step-level-breakdown.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A1-step-level-breakdown.md)
- [A2-paired-case-summary.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A2-paired-case-summary.md)
- [A3-cross-site-diagnosis.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A3-cross-site-diagnosis.md)
- [A6-alignment-rate-note.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A6-alignment-rate-note.md)
- [A7-offline-vs-online-tradeoff.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A7-offline-vs-online-tradeoff.md)
- [A8-online-small-data-efficiency.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A8-online-small-data-efficiency.md)
- [B4-sixflags-negative-case.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/B4-sixflags-negative-case.md)
- [B6-tripadvisor-cross-site-negative.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/B6-tripadvisor-cross-site-negative.md)
- [C1-lm-vs-rule-text-evidence.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/C1-lm-vs-rule-text-evidence.md)
- [C5-mind2web-compositionality-reading.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/C5-mind2web-compositionality-reading.md)

---

## 7. One-Paragraph Writing Guidance

> The final report should present the project as a Mind2Web-centered first-run reproduction and mechanism audit of AWM. The strongest claims should come from step-level decomposition, paired-case distributions, target-site first-run result tracing, and workflow text comparisons. New analysis added in the current stage supports three further refinements: first, offline and online memory form a trade-off rather than a simple ranking; second, online memory can show very-small-budget gains on kayak but this pattern is not reproduced on the available target-site first runs; and third, Mind2Web workflow reuse is best understood as flat subflow reuse rather than strong hierarchical composition. At the same time, the report should keep explicit scope boundaries: no WebArena-wide claim, no `AWM_AS` coverage, first-run rather than repeated-trial judgments, and alignment rate treated as exploratory rather than decisive.
