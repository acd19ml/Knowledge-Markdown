# Appendix B4. Negative Case: Sixflags Workflow-Content Mismatch

> Purpose: provide a clean negative case where a semantically mismatched workflow harms performance.
>
> Experimental identity sources:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/case_studies/negative_gpt-4o_test_task_sixflags_offline_wf.md`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/gpt-4o/test_task/sixflags/no_workflow/2.json`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/gpt-4o/test_task/sixflags/offline_wf/2.json`
>
> Prompt-level evidence source:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/gpt-4o/test_task/sixflags/offline_wf/2.json`
>
> Source note:
> - The case-study file indexes this as `task=2, step=0/6`, but the actual current step recorded in the raw JSON prompt is already under a new task: `Apply for a job on the Six Flags White Water park`.
> - This appendix follows the raw JSON prompt for the current-step task identity, while keeping the file-level `task id = 2` for traceability.

## B4.1 Case metadata

| Field | Value |
|---|---|
| Website | `sixflags` |
| Setting | `gpt-4o`, `test_task`, `offline_wf` vs `no_workflow` |
| Result-file task id | `2` |
| Raw step index | `0` |
| Case-study label | `0 / 6` |
| Current step task | `Apply for a job on the Six Flags White Water park` |

## B4.2 Claim supported

This case supports a narrow prompt-level claim: under the recorded `offline_wf` condition, workflow memory was already present in the prompt before raw step `0`, and the workflow condition produced the wrong park-selection click where the baseline produced the correct `Jobs` click.

This case does **not** isolate workflow insertion as the only changed factor between treatment and control, so it should be read as mechanism-consistent evidence rather than strict causal identification.

## B4.3 What is verified here

This appendix verifies four limited facts:

1. the case belongs to the audited `gpt-4o / test_task / sixflags / offline_wf` setting;
2. the current step in the raw JSON prompt is a jobs-related task, not the earlier balance-sheet task that appears in the file-level case-study index;
3. the baseline predicts the correct `Jobs` navigation click, while the workflow condition predicts the wrong `Browse the Parks Below` click;
4. the wrong click is locally consistent with the park-selection workflows present in the prompt.

## B4.4 Target and predictions

| Condition | Prediction | Correct? |
|---|---|---|
| Target | `CLICK [103]` | — |
| Baseline (`no_workflow`) | `CLICK [103]` | Yes |
| Workflow (`offline_wf`) | `CLICK [1042]` | No |

## B4.5 Observation excerpt from raw JSON

```text
Task: Apply for a job on the Six Flags White Water park
Trajectory:
Observation: `<html> <div> <div> <nav navigation> <a id=103> Jobs </a> </nav> <nav navigation> <a id=766> Jobs </a> </nav> </div> <div> <div select> <button id=1042> <div> Browse the Parks Below </div> </button> <button id=1045> Go! </button> </div> <form news letters form> <div> <label> First Name </label> <input id=2747 text andy /> </div> </form> </div> </div> </html>`
```

## B4.6 Workflow excerpt present in the prompt

```text
## select_park
Given that you are on the Six Flags website, this workflow selects a specific park from a list of options.
[button]  Browse the Parks Below -> CLICK
[span]  {park-name} -> CLICK
[button]  Go! -> CLICK

## select_event_options
Given that you are on a selected Six Flags park's page, this workflow navigates to see all events available at that park.
[link]  Events  -> CLICK
[link]  See all events  -> CLICK
```

## B4.7 Raw action outputs

### Baseline

```text
Action: `CLICK [103]`
```

### Workflow condition

```text
Action: `CLICK [1042]`
```

## B4.8 Strict interpretation

In this case, the control and treatment differ in first-step task routing: the baseline clicks the correct `Jobs` link, whereas the `offline_wf` condition clicks `Browse the Parks Below`. Because the treatment prompt already contains park-selection routines that fit a different task family, the wrong click is locally consistent with workflow-content mismatch.

## B4.9 Limitation

This appendix supports prompt-level, mechanism-consistent evidence for workflow-content mismatch in this specific case. It should not be overstated as proof that the model always follows workflow over local reasoning, and it does not isolate workflow insertion as the only changed prompt factor.
