# Appendix B6. Negative Case: Tripadvisor Online-Workflow Mismatch

> Purpose: document a case-level mismatch under the `test_website / tripadvisor / online_wf` setting, and verify that workflow memory was already present in the prompt when the wrong first action was produced.
>
> Experimental identity sources:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/runbook/c2-runbook.md`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/case_studies/negative_qwen_qwen3_5-397b-a17b_test_website_tripadvisor_online_wf.md`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/qwen/qwen3.5-397b-a17b/test_website/tripadvisor/no_workflow/2.json`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/qwen/qwen3.5-397b-a17b/test_website/tripadvisor/online_wf/2.json`
>
> Execution-mechanism sources:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/pipeline.py`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/online_induction.py`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/memory.py`
>
> Prompt-level evidence source:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/qwen/qwen3.5-397b-a17b/test_website/tripadvisor/online_wf/2.json`
>
> Optional prefix provenance sources:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/qwen/qwen3.5-397b-a17b/test_website/tripadvisor/online_wf/0.json`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/qwen/qwen3.5-397b-a17b/test_website/tripadvisor/online_wf/1.json`
>
> Source note:
> - The workflow text relevant to this case is taken from the prompt recorded in `online_wf/2.json`, not from the final workflow file currently stored on disk, because online induction rewrites the workflow file across prefixes.

## B6.1 Case metadata

| Field | Value |
|---|---|
| Website | `tripadvisor` |
| Setting | `qwen/qwen3.5-397b-a17b`, `test_website`, `online_wf` vs `no_workflow` |
| Task id | `2` |
| Raw step index | `0` |
| Case-study label | `0 / 13` |
| Task | `Find a vacation rental with 2 bedrooms and 2 bathrooms for the 15 to 20 June period, in Kanha National Park, India, and book the cheapest one.` |

## B6.2 Claim supported

This case supports a narrow prompt-level claim: under the recorded `online_wf` condition, workflow memory was already present in the prompt before the first action of task `2`, and the treatment condition produced an incorrect early `TYPE` where the baseline produced the correct `CLICK`.

This case does **not** by itself establish that the injected workflow text was the sole causal driver of the error, because the prompt is not controlled to differ only by workflow insertion.

## B6.3 What is verified here

The appendix verifies four limited facts:

1. the case belongs to the official `C2 / test_website / tripadvisor / online_wf` run setting;
2. the `online_wf` prompt already contains workflow memory at task `2`, step `0`;
3. the baseline predicts the correct first-step `CLICK`, while the `online_wf` condition predicts an incorrect `TYPE`;
4. the wrong `TYPE` is locally consistent with the search-first routine visible in the injected workflow message.

## B6.4 Target and predictions

| Condition | Prediction | Correct? |
|---|---|---|
| Target | `CLICK [631]` | — |
| Baseline (`no_workflow`) | `CLICK [631]` | Yes |
| Workflow (`online_wf`) | `TYPE [808] [Kanha National Park, India]` | No |

## B6.5 Observation excerpt from raw JSON

```text
Task: Find a vacation rental with 2 bedrooms and 2 bathrooms for the 15 to 20 June period, in Kanha National Park, India, and book the cheapest one.
Trajectory:
Observation: `<html> <div> <form search> ... <a id=631> <span> Vacation Rentals </span> </a> ... <input id=808 searchbox search q where to? /> ... </html>`
```

## B6.6 Workflow message actually present in the prompt

```text
## Summary Workflows:
## search_destination
Given that you are on the TripAdvisor search page, this workflow searches for and selects a specific destination or attraction.
[input]  Search where to? -> TYPE: {destination}
[option]  {destination_suggestion} -> CLICK
```

## B6.7 Raw action outputs

### Baseline

```text
Action: `CLICK [631]` ([link]  Vacation Rentals -> CLICK)
```

### Workflow condition

```text
Action: `TYPE [808] [Kanha National Park, India]`
```

## B6.8 Strict interpretation

The baseline and treatment differ in first-step behavior: the baseline takes the correct category-entry `CLICK`, whereas the `online_wf` condition takes an incorrect early `TYPE` into the search box. Because the treatment prompt already contains a search-first workflow routine, the error is consistent with workflow-conditioned entry-point mismatch.

However, this appendix should be read as prompt-level, mechanism-consistent evidence rather than strict causal identification.

## B6.9 Limitation

This case does not prove workflow provenance beyond the current prefix-level online setting, does not show that the workflow was induced only from successful prior trajectories, and does not isolate workflow insertion as the only changed prompt factor. It is therefore best used together with aggregated C2 diagnostics, not as a standalone causal proof.
