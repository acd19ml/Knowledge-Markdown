# Appendix B2. Positive Case: United Action-Mode Redirection

> Purpose: document a matched-site positive case where workflow memory is already present in the prompt and the workflow condition switches the first relevant action from an incorrect `CLICK` to the correct `TYPE`.
>
> Experimental identity sources:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/case_studies/positive_qwen_qwen3_5-397b-a17b_test_task_united_lm_wf.md`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/qwen/qwen3.5-397b-a17b/test_task/united/no_workflow/3.json`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/qwen/qwen3.5-397b-a17b/test_task/united/lm_wf/3.json`
>
> Prompt-level evidence source:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/qwen/qwen3.5-397b-a17b/test_task/united/lm_wf/3.json`
>
> Source note:
> - The workflow excerpt quoted in this appendix is taken from the recorded prompt in `lm_wf/3.json`, not from a separate workflow file.

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

This case supports a narrow prompt-level claim: under the recorded `lm_wf` condition, workflow memory was already present in the prompt before raw step `3`, and the workflow condition produced the correct `TYPE` where the baseline produced an incorrect `CLICK`.

This case does **not** by itself establish workflow insertion as the sole causal difference between the two conditions, so it should be read as mechanism-consistent evidence rather than strict causal identification.

## B2.3 What is verified here

This appendix verifies four limited facts:

1. the case belongs to the official `qwen/qwen3.5-397b-a17b / test_task / united / lm_wf` comparison setting;
2. the `lm_wf` prompt already contains workflow memory at raw step `3`;
3. the baseline predicts an incorrect `CLICK`, while the workflow condition predicts the correct `TYPE`;
4. the corrected `TYPE` is locally consistent with the location-entry routine visible in the injected workflow text.

## B2.4 Target and predictions

| Condition | Prediction | Correct? |
|---|---|---|
| Target | `TYPE [10892] [las vegas]` | — |
| Baseline (`no_workflow`) | `CLICK [10978]` | No |
| Workflow (`lm_wf`) | `TYPE [10892] [las vegas]` | Yes |

## B2.5 Observation excerpt from raw JSON

```text
Observation: `<html> <div> <div radiogroup package-type> <label id=10978> <div> <input radio hotel + flight /> <svg img /> </div> Hotel + Flight </label> <label> Hotel + Flight + Car </label> <label> Flight + Car </label> </div> <div> <svg img /> <input id=10892 combobox text where to? /> </div> <div> <div> <svg id=11159 img /> <input id=11161 departing - returning /> </div> <button id=11164 button select traveler information> <div> <svg img /> 2 Adults, 1 Room </div> </button> </div> </div> </html>`
```

## B2.6 Workflow excerpt present in the prompt

```text
## enter_flight_locations
Given that you are on the United Airlines booking or search page, this workflow enters the departure and destination city/airport for your flight.
[combobox]  Enter your departing city, airport name, or airpor... -> TYPE: {origin-city}
[button]  {origin-option} -> CLICK
[combobox]  Enter your destination city, airport name, or airp... -> TYPE: {destination-city}
[button]  {destination-option} -> CLICK
```

## B2.7 Raw action outputs

### Baseline

```text
Action: `CLICK [10978]` ([label]  Hotel + Flight -> CLICK)
```

### Workflow condition

```text
Action: `TYPE [10892] [las vegas]` ([combobox]  Where to? -> TYPE: las vegas)
```

## B2.8 Strict interpretation

In this case, the control and treatment differ in action mode at a key form-filling step: the baseline takes an incorrect package-option `CLICK`, whereas the `lm_wf` condition types into the correct destination combobox. Because the treatment prompt already contains an explicit location-entry routine, the correction is locally consistent with workflow-guided action-mode redirection on a matched site.

## B2.9 Limitation

This appendix supports step-level, prompt-level evidence for matched-site action-mode correction. It should not be used as strict causal proof, and it should not be generalized into a claim that all positive cases are driven by the same mechanism.
