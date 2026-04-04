# Appendix B6. Negative Case: Tripadvisor Cross-Site Workflow Mismatch

> Purpose: provide a clean cross-site negative case where a transferred workflow changes a correct `CLICK` into an incorrect `TYPE`.
>
> Primary sources:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/case_studies/negative_qwen_qwen3_5-397b-a17b_test_website_tripadvisor_online_wf.md`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/qwen/qwen3.5-397b-a17b/test_website/tripadvisor/no_workflow/2.json`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/results/qwen/qwen3.5-397b-a17b/test_website/tripadvisor/online_wf/2.json`

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

This case supports the case-level claim that a transferred online workflow can inject the wrong operation pattern on a new site, replacing a correct navigation click with an inappropriate search-typing routine.

## B6.3 Target and predictions

| Condition | Prediction | Correct? |
|---|---|---|
| Target | `CLICK [631]` | — |
| Baseline (`no_workflow`) | `CLICK [631]` | Yes |
| Workflow (`online_wf`) | `TYPE [808] [Kanha National Park, India]` | No |

## B6.4 Observation excerpt from raw JSON

```text
Task: Find a vacation rental with 2 bedrooms and 2 bathrooms for the 15 to 20 June period, in Kanha National Park, India, and book the cheapest one.
Trajectory:
Observation: `<html> <div> <form search> ... <a id=631> <span> Vacation Rentals </span> </a> ... <input id=808 searchbox search q where to? /> ... </html>`
```

## B6.5 Workflow excerpt present in the prompt

```text
## search_destination
Given that you are on the TripAdvisor search page, this workflow searches for and selects a specific destination or attraction.
[input]  Search where to? -> TYPE: {destination}
[option]  {destination_suggestion} -> CLICK
```

## B6.6 Raw action outputs

### Baseline

```text
Action: `CLICK [631]` ([link]  Vacation Rentals -> CLICK)
```

### Workflow condition

```text
Action: `TYPE [808] [Kanha National Park, India]`
```

## B6.7 Minimal interpretation

This case supports the narrow claim that a transferred workflow can inject an inappropriate operation pattern on a new site: instead of taking the correct navigation click, the model is pulled into a destination-typing routine.

## B6.8 Limitation

This case is best used together with aggregated C2 diagnostics. On its own, it is evidence of cross-site workflow mismatch, not a complete explanation of all tripadvisor failures.
