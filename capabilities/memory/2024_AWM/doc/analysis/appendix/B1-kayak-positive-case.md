# Appendix B1. Positive Case: Kayak Date-Selection Correction

> Purpose: document a matched-site positive case where workflow memory is already present in the prompt and the workflow condition selects the correct late-stage date element.
>
> Experimental identity sources:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/gpt-4o/test_task/kayak/no_workflow/4.json`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/gpt-4o/test_task/kayak/offline_wf/4.json`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/case_studies/positive_gpt-4o_test_task_kayak_offline_wf.md`
>
> Prompt-level evidence source:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/gpt-4o/test_task/kayak/offline_wf/4.json`
>
> Source note:
> - The workflow excerpt quoted in this appendix is taken from the recorded prompt in `offline_wf/4.json`, not from a separate workflow file.

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

This case supports a narrow prompt-level claim: under the recorded `offline_wf` condition, workflow memory was already present in the prompt before raw step `6`, and the workflow condition selected the correct date element where the baseline selected a nearby wrong element.

This case does **not** by itself isolate workflow insertion as the only changed factor between control and treatment, so it should be read as mechanism-consistent evidence rather than strict causal identification.

## B1.3 What is verified here

This appendix verifies four limited facts:

1. the case belongs to the official `gpt-4o / test_task / kayak / offline_wf` comparison setting;
2. the `offline_wf` prompt already contains workflow memory at raw step `6`;
3. the baseline predicts the wrong date element, while the workflow condition predicts the correct one;
4. the corrected action is locally consistent with the date-selection routine visible in the injected workflow text.

## B1.4 Target and predictions

| Condition | Prediction | Correct? |
|---|---|---|
| Target | `CLICK [59393]` | — |
| Baseline (`no_workflow`) | `CLICK [63241]` | No |
| Workflow (`offline_wf`) | `CLICK [59393]` | Yes |

## B1.5 Observation excerpt from raw JSON

```text
Observation: `<html> <div menu> <div tab start date calendar input use> ... <div id=63241 button wednesday may 3, 2023> 3 </div> ... <div id=59393 button wednesday may 3, 2023> 3 </div> ... </div> </div> </html>`
```

## B1.6 Workflow excerpt present in the prompt

```text
## Workflow 2: Select Travel Dates
Given that you are on the search page for flights, cars, or hotels, this workflow selects the travel dates.
- [generic/button] Start date/End date -> CLICK
- [div/gridcell] {start-date} -> CLICK
- [div/gridcell] {end-date} -> CLICK
```

## B1.7 Raw action outputs

### Baseline

```text
Action: `CLICK [63241]` ([div] 3 -> CLICK)
```

### Workflow condition

```text
Action: `CLICK [59393]` ([button]  May 3, 2023 -> CLICK)
```

## B1.8 Strict interpretation

In this case, the control and treatment differ in late-stage date selection: the baseline clicks a nearby wrong calendar target, whereas the `offline_wf` condition clicks the correct date element. Because the treatment prompt already contains an explicit date-selection routine, the correction is locally consistent with workflow-guided date grounding on a matched site.

## B1.9 Limitation

This appendix supports step-level, prompt-level evidence for matched-site date-element correction. It should not be read as strict causal proof, and it should not be generalized into a claim that all `kayak` gains come from the same workflow fragment.
