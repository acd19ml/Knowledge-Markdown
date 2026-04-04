# Appendix B4. Negative Case: Sixflags Workflow-Content Mismatch

> Purpose: provide a clean negative case where a semantically mismatched workflow harms performance.
>
> Primary sources:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/case_studies/negative_gpt-4o_test_task_sixflags_offline_wf.md`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/gpt-4o/test_task/sixflags/no_workflow/2.json`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/gpt-4o/test_task/sixflags/offline_wf/2.json`

## B4.1 Case metadata

| Field | Value |
|---|---|
| Website | `sixflags` |
| Setting | `gpt-4o`, `test_task`, `offline_wf` vs `no_workflow` |
| Task id | `2` |
| Raw step index | `0` |
| Case-study label | `0 / 6` |
| Task | `Show the balance sheet and cash flow statement for the fiscal year 2021 of Six Flags.` |

## B4.2 Claim supported

This case supports the case-level claim that a semantically mismatched workflow can override an otherwise correct navigation decision and pull the model into the wrong task family.

## B4.3 Target and predictions

| Condition | Prediction | Correct? |
|---|---|---|
| Target | `CLICK [103]` | — |
| Baseline (`no_workflow`) | `CLICK [103]` | Yes |
| Workflow (`offline_wf`) | `CLICK [1042]` | No |

## B4.4 Observation excerpt from raw JSON

```text
Task: Apply for a job on the Six Flags White Water park
Trajectory:
Observation: `<html> <div> <div> <nav navigation> <a id=103> Jobs </a> </nav> <nav navigation> <a id=766> Jobs </a> </nav> </div> <div> <div select> <button id=1042> <div> Browse the Parks Below </div> </button> <button id=1045> Go! </button> </div> <form news letters form> <div> <label> First Name </label> <input id=2747 text andy /> </div> </form> </div> </div> </html>`
```

## B4.5 Workflow excerpt present in the prompt

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

## B4.6 Raw action outputs

### Baseline

```text
Action: `CLICK [103]`
```

### Workflow condition

```text
Action: `CLICK [1042]`
```

## B4.7 Minimal interpretation

This case supports the narrow claim that a semantically mismatched workflow can redirect the model toward an operation pattern that fits a different task family, thereby hurting step-level accuracy.

## B4.8 Limitation

This example is best used as evidence for workflow-content mismatch. It should not be overstated as proof that the model always follows workflow over local reasoning.
