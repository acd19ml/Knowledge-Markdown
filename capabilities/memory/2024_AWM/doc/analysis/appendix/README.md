# Appendix Evidence Index

This directory stores appendix-ready evidence blocks for the AWM reproduction report.

## Aggregated evidence

- [A1-step-level-breakdown.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A1-step-level-breakdown.md)
- [A2-paired-case-summary.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A2-paired-case-summary.md)
- [A3-cross-site-diagnosis.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A3-cross-site-diagnosis.md)
- [A4-c4-result-table.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A4-c4-result-table.md)
- [A5-c5-quality-table.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A5-c5-quality-table.md)
- [A6-alignment-rate-note.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A6-alignment-rate-note.md)
- [A7-offline-vs-online-tradeoff.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A7-offline-vs-online-tradeoff.md)
- [A8-online-small-data-efficiency.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A8-online-small-data-efficiency.md)

## Case evidence

- [B1-kayak-positive-case.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/B1-kayak-positive-case.md)
- [B2-united-positive-case.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/B2-united-positive-case.md)
- [B4-sixflags-negative-case.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/B4-sixflags-negative-case.md)
- [B5-sixflags-step-skipping-case.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/B5-sixflags-step-skipping-case.md)
- [B6-tripadvisor-cross-site-negative.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/B6-tripadvisor-cross-site-negative.md)

## Workflow text evidence

- [C1-lm-vs-rule-text-evidence.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/C1-lm-vs-rule-text-evidence.md)
- [C2-concrete-value-counting-rule.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/C2-concrete-value-counting-rule.md)
- [C3-workflow-counting-and-site-features.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/C3-workflow-counting-and-site-features.md)
- [C4-site-feature-qualitative-coding.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/C4-site-feature-qualitative-coding.md)
- [C5-mind2web-compositionality-reading.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/C5-mind2web-compositionality-reading.md)

## Current status

- Created as source-traceable support for final-report正文 claims.
- These files are evidence-only and intentionally avoid stronger claims than the current runbooks support.
- `A3` is now best read as an exploratory first-run target-site result note rather than a standalone mechanism appendix.
- `A7` and `A8` are retained as exploratory follow-up analyses, not minimal core evidence for the final report.
- Historical candidate selection notes live in [appendix-evidence-candidates.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix-evidence-candidates.md), but that file is now deprecated as an active source of truth.
- For正文 claim-to-appendix linkage, use [mechanism-appendix-mapping.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/mechanism-appendix-mapping.md).

## Case template

All `B*` case appendices now use a source-traceable case structure. The common core is:

1. a `Source` block separating experimental identity and prompt-level evidence
2. `Case metadata`
3. `Claim supported`
4. `What is verified here`
5. `Target and predictions`
6. `Observation excerpt from raw JSON`
7. `Workflow excerpt present in the prompt` or equivalent prompt-level evidence
8. `Raw action outputs`
9. `Strict interpretation`
10. `Limitation`

This template is meant to keep case-level evidence comparable across positive and negative examples while making source identity and causal limits explicit by default.
