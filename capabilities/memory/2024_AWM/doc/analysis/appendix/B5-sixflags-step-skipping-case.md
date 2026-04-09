# Appendix B5. Negative Case: Sixflags Template-Induced Step Skipping

> Purpose: document a negative case where workflow memory is already present in the prompt and the workflow condition takes a premature `Book Now` click instead of the correct date-selection step.
>
> Experimental identity sources:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/case_studies/negative_gpt-4o_test_task_sixflags_offline_wf.md`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/gpt-4o/test_task/sixflags/no_workflow/1.json`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/gpt-4o/test_task/sixflags/offline_wf/1.json`
>
> Prompt-level evidence source:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/gpt-4o/test_task/sixflags/offline_wf/1.json`
>
> Source note:
> - The workflow excerpt quoted in this appendix is taken from the recorded prompt in `offline_wf/1.json`, and the audited raw step corresponds to the Great Escape lodging task visible in both paired result files.

## B5.1 Case metadata

| Field | Value |
|---|---|
| Website | `sixflags` |
| Setting | `gpt-4o`, `test_task`, `offline_wf` vs `no_workflow` |
| Task id | `1` |
| Raw step index | `5` |
| Case-study label | `Case 2: task=1, step=5/14` |
| Current step task | `Find a place to stay near Great Escape New Park from April 21 to April 24 for 2 adults and 1 kid, and book the cheapest themed room.` |

## B5.2 Claim supported

This case supports a narrow prompt-level claim: under the recorded `offline_wf` condition, workflow memory was already present in the prompt before raw step `5`, and the workflow condition produced a premature purchase-oriented `CLICK` where the baseline took the correct date-selection action.

This case does **not** isolate workflow insertion as the only changed factor between treatment and control, so it should be read as mechanism-consistent evidence rather than strict causal identification.

## B5.3 What is verified here

This appendix verifies four limited facts:

1. the case belongs to the official `gpt-4o / test_task / sixflags / offline_wf` comparison setting;
2. the audited raw step is part of the Great Escape lodging task recorded in both paired result files;
3. the `offline_wf` prompt already contains workflow memory at raw step `5`;
4. the workflow condition clicks `Book Now` too early, while the baseline correctly clicks the arrival-date input, and this premature click is locally consistent with the purchase-oriented routine visible in the injected workflow text.

## B5.4 Target and predictions

| Condition | Prediction | Correct? |
|---|---|---|
| Target | `CLICK [46822]` | — |
| Baseline (`no_workflow`) | `CLICK [46822]` | Yes |
| Workflow (`offline_wf`) | `CLICK [47084]` | No |

## B5.5 Observation excerpt from raw JSON

```text
Observation: `<html> <div> <a id=47084 book now> Book Now </a> <div> <div> <label> Check in date </label> <input id=46822 text startdate select arrival date /> </div> <div> <label> Check out date </label> <input id=47302 text enddate select departure date /> </div> <input hotelid 6491 /> <button id=47310 submit> Check Rates </button> </div> ... </html>`
```

## B5.6 Workflow excerpt present in the prompt

```text
## buy_group_tickets
Given that you are on a selected Six Flags park's page, this workflow buys group tickets by entering necessary group information.
[link]  Groups -> CLICK
[button]  Buy Now -> CLICK
[button]  {date} -> CLICK
[button]  Buy Now -> CLICK
[input]   -> TYPE: {group-name}
...
```

## B5.7 Raw action outputs

### Baseline

```text
Action: `CLICK [46822]` (select Check in date -> CLICK)
```

### Workflow condition

```text
Action: `CLICK [47084]` ([link]  Book Now -> CLICK)
```

## B5.8 Strict interpretation

In this case, the control and treatment differ in local step ordering: the baseline first opens the arrival-date field, whereas the `offline_wf` condition clicks `Book Now` before the required date-selection step. Because the treatment prompt already contains a compressed purchase-oriented routine with repeated `Buy Now` actions, the error is locally consistent with template-induced step skipping.

## B5.9 Limitation

This appendix supports prompt-level, mechanism-consistent evidence for template-induced step skipping in this specific case. It should not be generalized into a universal rule, and it should not be used as strict causal proof without a more controlled comparison.
