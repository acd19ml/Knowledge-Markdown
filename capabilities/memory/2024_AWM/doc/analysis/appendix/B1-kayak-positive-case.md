# Appendix B1. Positive Case: Kayak Date-Selection Correction

> Purpose: provide a clean positive case where the workflow corrects a late-stage click on a matched site.
>
> Primary sources:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/gpt-4o/test_task/kayak/no_workflow/4.json`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/gpt-4o/test_task/kayak/offline_wf/4.json`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/case_studies/positive_gpt-4o_test_task_kayak_offline_wf.md`

## B1.1 Case metadata

| Field | Value |
|---|---|
| Website | `kayak` |
| Setting | `gpt-4o`, `test_task`, `offline_wf` vs `no_workflow` |
| Task id | `4` |
| Raw step index | `6` |
| Case-study step label | `8 / 14` |
| Task | `check cheap flights from NYC to London on 23rd of April for students over 18 years.` |

> Note: the case-study file uses a different step numbering convention (`step=8/14`), while the raw JSON pair index corresponds to raw step index `6`.  
> This appendix uses the raw JSON indexing to avoid ambiguity.

## B1.2 Claim supported

This case supports the step-level claim that, on a matched site, workflow guidance can improve late-stage date-element grounding by steering the model toward the correct calendar target.

## B1.3 Target and predictions

| Condition | Prediction | Correct? |
|---|---|---|
| Target | `CLICK [59393]` | — |
| Baseline (`no_workflow`) | `CLICK [63241]` | No |
| Workflow (`offline_wf`) | `CLICK [59393]` | Yes |

## B1.4 Observation excerpt from raw JSON

```text
Observation: `<html> <div menu> <div tab start date calendar input use> ... <div id=63241 button wednesday may 3, 2023> 3 </div> ... <div id=59393 button wednesday may 3, 2023> 3 </div> ... </div> </div> </html>`
```

## B1.5 Workflow excerpt present in the prompt

```text
## Workflow 2: Select Travel Dates
Given that you are on the search page for flights, cars, or hotels, this workflow selects the travel dates.
- [generic/button] Start date/End date -> CLICK
- [div/gridcell] {start-date} -> CLICK
- [div/gridcell] {end-date} -> CLICK
```

## B1.6 Raw action outputs

### Baseline

```text
Action: `CLICK [63241]` ([div] 3 -> CLICK)
```

### Workflow condition

```text
Action: `CLICK [59393]` ([button]  May 3, 2023 -> CLICK)
```

## B1.7 Minimal interpretation

This case supports the narrow claim that, on a matched site, a workflow can help the model choose the correct late-stage date element rather than a nearby distractor with similar surface text.

## B1.8 Limitation

This appendix supports step-level element grounding improvement on a matched site. It should not be read as evidence that all `kayak` gains come from the same workflow fragment.
