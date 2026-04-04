# Appendix B2. Positive Case: United Action-Mode Redirection

> Purpose: provide a clean positive case where workflow changes the action mode from an incorrect `CLICK` to a correct `TYPE`.
>
> Primary sources:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/case_studies/positive_qwen_qwen3_5-397b-a17b_test_task_united_lm_wf.md`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/qwen/qwen3.5-397b-a17b/test_task/united/no_workflow/3.json`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/qwen/qwen3.5-397b-a17b/test_task/united/lm_wf/3.json`

## B2.1 Case metadata

| Field | Value |
|---|---|
| Website | `united` |
| Setting | `qwen/qwen3.5-397b-a17b`, `test_task`, `lm_wf` vs `no_workflow` |
| Task id | `3` |
| Raw step index | `3` |
| Case-study label | `5 / 27` |
| Task | `Find a basic economy flight + hotel for an award travel from las vegas to san francisco leaving and returning on any date on april for 1 traveler and one room` |

## B2.2 Claim supported

This case supports the step-level claim that, on a matched site, workflow guidance can redirect the model from an incorrect navigation-style click to the correct input-style typing action.

## B2.3 Target and predictions

| Condition | Prediction | Correct? |
|---|---|---|
| Target | `TYPE [10892] [las vegas]` | — |
| Baseline (`no_workflow`) | `CLICK [10978]` | No |
| Workflow (`lm_wf`) | `TYPE [10892] [las vegas]` | Yes |

## B2.4 Observation excerpt from raw JSON

```text
Observation: `<html> <div> <div radiogroup package-type> <label id=10978> <div> <input radio hotel + flight /> <svg img /> </div> Hotel + Flight </label> <label> Hotel + Flight + Car </label> <label> Flight + Car </label> </div> <div> <svg img /> <input id=10892 combobox text where to? /> </div> <div> <div> <svg id=11159 img /> <input id=11161 departing - returning /> </div> <button id=11164 button select traveler information> <div> <svg img /> 2 Adults, 1 Room </div> </button> </div> </div> </html>`
```

## B2.5 Workflow excerpt present in the prompt

```text
## enter_flight_locations
Given that you are on the United Airlines booking or search page, this workflow enters the departure and destination city/airport for your flight.
[combobox]  Enter your departing city, airport name, or airpor... -> TYPE: {origin-city}
[button]  {origin-option} -> CLICK
[combobox]  Enter your destination city, airport name, or airp... -> TYPE: {destination-city}
[button]  {destination-option} -> CLICK
```

## B2.6 Raw action outputs

### Baseline

```text
Action: `CLICK [10978]` ([label]  Hotel + Flight -> CLICK)
```

### Workflow condition

```text
Action: `TYPE [10892] [las vegas]` ([combobox]  Where to? -> TYPE: las vegas)
```

## B2.7 Minimal interpretation

This case supports the narrow claim that, on a matched site, a workflow can redirect the model from an incorrect navigation-style `CLICK` to the correct input-style `TYPE` action at a key form-filling step.

## B2.8 Limitation

This is evidence for step-level action-mode correction. It should not be used to claim that all positive cases are driven by the same mechanism.
