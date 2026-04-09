# Appendix Rigor Audit

> Purpose:
> - audit the current appendix set against the stricter evidence standard established during the `B6` review
> - separate source-closed evidence from exploratory or over-strong readings
> - identify which appendix files are safe for final-report use, which must stay exploratory, and which still need repair

## 1. Audit standard

The audit uses three related standards, depending on appendix type.

### 1.1 Case appendices (`B*`)

For case appendices, the strict standard is:

1. experiment identity must be closed;
2. treatment content must be traceable to the actual prompt or recorded condition;
3. timing/execution mechanism must be understood when relevant;
4. local mechanism correspondence must be visible;
5. conclusion strength must not exceed the evidence;
6. if control and treatment are not single-variable controlled, the appendix may support only prompt-level or mechanism-consistent evidence, not strict causal attribution.

### 1.2 Aggregated appendices (`A*`)

For aggregated appendices, the strict standard is:

1. the source output must be explicit and primary;
2. the appendix must state exactly what claims the table/output can support;
3. boundary notes must block causal or semantic over-reading when the metric is only descriptive or heuristic;
4. if the appendix is first-run only, that limitation must be explicit.

### 1.3 Text / definition appendices (`C*`)

For text and definition appendices, the strict standard is:

1. the counting rule / coding rule must be explicit;
2. the raw textual sources must be listed;
3. the appendix must distinguish structural/textual support from performance support;
4. qualitative readings must not be rewritten as hard quantitative laws.

## 2. Executive summary

### 2.1 Safe for direct use with current wording

- `A1`
- `A2`
- `A4`
- `A5`
- `A6` as exploratory only
- `B1`
- `B2`
- `B4`
- `B5`
- `B6`
- `C1`
- `C2`
- `C3`
- `C4` as qualitative only
- `C5` as qualitative only

### 2.2 Safe only as exploratory / first-run tracing

- `A3`
- `A7`
- `A8`

### 2.3 Needs repair before strong reuse

- none in the current appendix set

## 3. File-by-file audit

### A1. Step-Level Breakdown

- Verdict: `PASS`
- Strongest safe use:
  - support direction-of-effect claims about `TYPE` vs `CLICK`
  - support later-step concentration/degradation patterns as first-run tendencies
- Cannot support:
  - strict causal claims about why a delta occurs
- Why it passes:
  - primary source explicit
  - verified claims section explicit
  - boundary notes already present

### A2. Paired-Case Summary

- Verdict: `PASS`
- Strongest safe use:
  - support behavioral-footprint claims
  - support `negative = 0` vs `negative > positive` distribution facts
- Cannot support:
  - equal importance of all changed steps
  - causal importance of a given changed step without case-level evidence
- Why it passes:
  - corrected denominator explicit
  - source explicit
  - boundary notes explicit

### A3. First-Run Target-Site Result Note

- Verdict: `EXPLORATORY / FIRST-RUN ONLY`
- Strongest safe use:
  - record that `tripadvisor` and `reddit` first-run target-site results underperform baseline
  - note that `tripadvisor` shows weaker baseline candidate quality
  - note that negative steps are dominated by `CLICK`
- Cannot support:
  - workflow provenance
  - full causal decomposition
  - a standalone cross-site mechanism claim
- Why it is limited:
  - the underlying script output remains diagnostic, not causal
  - the file is now correctly bounded, but should stay in that role only

### A4. C4 Result Table

- Verdict: `PASS`
- Strongest safe use:
  - first-run result claims for `NL vs HTML`
  - first-run result claim for `code vs text` on `kayak`
- Cannot support:
  - broader representational laws beyond audited first runs
- Why it passes:
  - runbook is the primary source
  - first-run boundary is explicit

### A5. C5 Quality Table

- Verdict: `PASS`
- Strongest safe use:
  - compactness / low overlap under current approximation
  - prompt-level proxy wording for coverage / utility
- Cannot support:
  - strict behavioral adherence
- Why it passes:
  - proxy limitation is already explicit

### A6. Alignment-Rate Note

- Verdict: `PASS AS EXPLORATORY ONLY`
- Strongest safe use:
  - support the weaker claim that surface alignment does not reliably predict performance
- Cannot support:
  - semantic match
  - causal explanation
- Why it passes:
  - metric identity and limitation are explicit

### A7. Offline vs Online Trade-Off

- Verdict: `EXPLORATORY ONLY`
- Strongest safe use:
  - exploratory reading of where `offline_wf` and `online_wf` gains show up on `kayak`
- Cannot support:
  - a report-level causal trade-off law
  - a target-site mechanism proof
- Why it is limited:
  - same-site direct comparison is only on `kayak`
  - target-site part is interpretive context, not controlled evidence

### A8. Online Small-Data Efficiency

- Verdict: `EXPLORATORY ONLY`
- Strongest safe use:
  - descriptive prefix-level pattern: early gains on `kayak`, not reproduced on the two target-site first runs
- Cannot support:
  - benchmark-wide small-data efficiency
  - a causal explanation for early bias
- Why it is limited:
  - reconstructed prefix curves
  - first-run only

### B1. Kayak Positive Case

- Verdict: `PASS UNDER STRICT CASE STANDARD`
- Strongest safe use:
  - case-level evidence that a workflow can help late-stage date-element selection on a matched site
- Cannot support:
  - strict causal identification
  - a general claim that all `kayak` gains come from the same mechanism
- Why it passes:
  - experiment identity sources explicit
  - prompt-level evidence source explicit
  - source note clarifies that the excerpt is taken from the recorded prompt
  - causal limitation is now explicit

### B2. United Positive Case

- Verdict: `PASS UNDER STRICT CASE STANDARD`
- Strongest safe use:
  - case-level evidence that workflow can redirect action mode from wrong `CLICK` to correct `TYPE`
- Cannot support:
  - strict causal identification
  - universal claims about positive cases
- Why it passes:
  - experiment identity sources explicit
  - prompt-level evidence source explicit
  - source note clarifies that the excerpt is taken from the recorded prompt
  - causal limitation is now explicit

### B4. Sixflags Negative Case

- Verdict: `PASS UNDER STRICT CASE STANDARD`
- Strongest safe use:
  - case-level evidence that workflow-content mismatch can redirect the model into the wrong task family
- Cannot support:
  - strict causal identification
  - a universal claim that all `sixflags` failures come from the same mismatch
- Why it passes:
  - the current-step task identity is now aligned to the raw JSON prompt rather than the stale case-study index label
  - experiment identity sources explicit
  - prompt-level evidence source explicit
  - causal limitation is now explicit

### B5. Sixflags Step-Skipping Case

- Verdict: `PASS UNDER STRICT CASE STANDARD`
- Strongest safe use:
  - case-level evidence that a compressed purchase-oriented template can pull the model to a later action too early
- Cannot support:
  - universal step-skipping claims
  - strict causal proof
- Why it passes:
  - experiment identity sources explicit
  - current-step task identity is now aligned to the paired raw JSON files
  - prompt-level evidence source explicit
  - causal limitation is now explicit

### B6. Tripadvisor Online-Workflow Mismatch

- Verdict: `PASS UNDER STRICT CASE STANDARD`
- Strongest safe use:
  - prompt-level mismatch case
  - verifies workflow memory was present before the wrong first action
  - supports mechanism-consistent, not strictly causal, interpretation
- Cannot support:
  - transferred workflow provenance
  - success-only induction
  - strict causal attribution
- Why it passes:
  - experiment identity sources explicit
  - execution-mechanism sources explicit
  - prompt-level evidence source explicit
  - source note explicit
  - causal limitation explicit

### C1. LM vs Rule Text Evidence

- Verdict: `PASS`
- Strongest safe use:
  - text-structural abstraction claim
- Cannot support:
  - direct performance superiority claim on its own
- Why it passes:
  - textual nature of evidence is explicit
  - boundary note already blocks performance overreach

### C2. Concrete-Value Counting Rule

- Verdict: `PASS`
- Strongest safe use:
  - definitional repair for “concrete values”
- Cannot support:
  - any performance claim
- Why it passes:
  - counting rule explicit
  - examples explicit
  - safe wording explicit

### C3. Workflow Counting and Site-Feature Definitions

- Verdict: `PASS`
- Strongest safe use:
  - definitional repair for workflow counts / average steps
- Cannot support:
  - performance interpretation on its own
- Why it passes:
  - dual counting conventions explicit
  - recommended usage explicit

### C4. Site-Feature Qualitative Coding

- Verdict: `PASS AS QUALITATIVE ONLY`
- Strongest safe use:
  - structured qualitative comparison of site/task/workflow relations
- Cannot support:
  - hard quantitative law
- Why it passes:
  - boundary already states qualitative coding memo

### C5. Mind2Web Compositionality Reading

- Verdict: `PASS AS QUALITATIVE ONLY`
- Strongest safe use:
  - flat subflow reuse reading
- Cannot support:
  - strong hierarchical composition claim
- Why it passes:
  - conceptual distinctions are explicit
  - bottom-line reading already bounded

## 4. Priority fixes

### P0

- Repair `B4` source identity mismatch before using it as a flagship negative case.

### P1

- Upgrade `B1`, `B2`, and `B5` to the stricter `B6` structure if they will be cited as prompt-level case evidence in the final report.

### P2

- Keep `A3`, `A7`, and `A8` out of any wording that sounds like an independently established mechanism theorem.

## 5. Safe final-report set under the stricter standard

If the final report wants the safest appendix chain under the current rigor standard, the best subset is:

- `A1`
- `A2`
- `A4`
- `A5`
- `A6` as exploratory only
- `B6`
- `C1`
- `C2`
- `C3`
- `C4` as qualitative only
- `C5` as qualitative only

If positive/negative prompt-level cases beyond `B6` are needed, `B1`, `B2`, and `B5` should first be upgraded to the same source-discipline template.
