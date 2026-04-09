# Appendix A7. Offline vs Online Workflow Trade-off on Mind2Web

## Purpose

This appendix is retained as an exploratory rereading of existing Mind2Web outputs. It should not be used as a primary final-report appendix for cross-site mechanism claims.

The goal here is not to introduce a new experiment. It is to re-read existing C1 and C2 outputs from a mechanism perspective and ask:

- what kinds of step-level gains does `offline_wf` produce on `kayak`?
- what kinds of step-level gains does `online_wf` produce on the same site?
- what first-run result pattern appears on the farther targets `tripadvisor` and `reddit`?

## Source Materials

- [step_breakdown_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/step_breakdown_output.txt)
- [paired_case_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/paired_case_output.txt)
- [offline_online_tradeoff_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/offline_online_tradeoff_output.txt)
- [kayak_offline_wf.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/kayak_offline_wf.txt)
- [kayak_online_wf.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/kayak_online_wf.txt)
- [negative_qwen_qwen3_5-397b-a17b_test_website_tripadvisor_online_wf.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/case_studies/negative_qwen_qwen3_5-397b-a17b_test_website_tripadvisor_online_wf.md)
- [negative_qwen_qwen3_5-397b-a17b_test_domain_reddit_online_wf.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/case_studies/negative_qwen_qwen3_5-397b-a17b_test_domain_reddit_online_wf.md)

## A7.1 Same-Site Comparison on `kayak`

### Aggregate outcome

From `step_breakdown_output.txt`:

| condition | Elem Acc | Act F1 | Step SR |
|---|---:|---:|---:|
| no_workflow | 52.1% | 60.9% | 47.9% |
| offline_wf | 58.3% | 63.2% | 54.2% |
| online_wf | 56.2% | 65.4% | 54.2% |

Observation:

- both `offline_wf` and `online_wf` improve `Step SR` by `+6.3pp` over baseline on `kayak`
- `offline_wf` has slightly higher `Elem Acc`
- `online_wf` has slightly higher `Act F1`

This already suggests that the two conditions are not helping in exactly the same way.

### Action-type decomposition

From `step_breakdown_output.txt`:

| delta vs no_workflow | CLICK dStepSR | TYPE dActF1 | TYPE dStepSR |
|---|---:|---:|---:|
| offline_wf | +10.7% | +1.4% | +0.0% |
| online_wf | +7.1% | +19.2% | +16.7% |

Reading:

- `offline_wf` contributes more on `CLICK` grounding
- `online_wf` contributes much more on `TYPE` formatting/value guidance

This is the clearest quantitative sign of a trade-off rather than a simple dominance relation.

### Direct paired comparison: `online_wf` vs `offline_wf`

From [offline_online_tradeoff_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/offline_online_tradeoff_output.txt):

| category | count | pct |
|---|---:|---:|
| positive | 1 | 2.1% |
| negative | 1 | 2.1% |
| ineffective | 21 | 43.8% |
| redundant | 25 | 52.1% |

By action type:

| type | pos | neg | total |
|---|---:|---:|---:|
| CLICK | 0 | 1 | 28 |
| TYPE | 1 | 0 | 6 |

The only positive case for `online_wf` over `offline_wf` is a TYPE-format correction:

- task: `Find a cheapest SUV in Brooklyn for 1 day`
- target: `TYPE [35686] [PENN STATION]`
- offline-side prediction: `Penn Station`
- online-side prediction: `PENN STATION`

The only negative case for `online_wf` against `offline_wf` is a CLICK choice on the same task:

- target: `CLICK [59393]`
- offline-side prediction: `CLICK [59393]`
- online-side prediction: `CLICK [63241]`

So the direct pair is internally consistent with the aggregate decomposition above:

- `online_wf` helps on local value formatting
- `offline_wf` is slightly steadier on result-page clicking

## A7.2 Workflow-Text Difference

The workflow texts show a structural contrast.

### `kayak_offline_wf`

[kayak_offline_wf.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/kayak_offline_wf.txt) contains broader reusable search primitives:

- enter location for car or hotel search
- select travel dates
- select one-way flight
- search vacation packages
- search flights
- select flight filters
- select hotel filters
- view and select deals

These are relatively general travel-site routines. They are not tied to one exact successful task sequence.

### `kayak_online_wf`

[kayak_online_wf.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/kayak_online_wf.txt) is narrower and more trajectory-shaped:

- `search_for_cars_kayak`
- `select_location_kayak`
- `select_dates_for_rental_kayak`
- `search_flights_kayak`
- `browse_car_type_kayak`

Compared with the offline library, the online library is:

- more site-specific
- more task-family-specific
- more tightly coupled to the successful test-time routines that generated it

This supports the interpretation that `online_wf` is closer to the current test distribution, but also less robust as a general reusable library.

## A7.3 First-Run Target-Site Underperformance for `online_wf`

The same logged setting that helps on `kayak` does not carry over as a positive first-run result on the two target sites available here.

### Tripadvisor

From `paired_case_output.txt`:

- `positive = 4`
- `negative = 18`
- `net = -14`

From [negative_qwen_qwen3_5-397b-a17b_test_website_tripadvisor_online_wf.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/case_studies/negative_qwen_qwen3_5-397b-a17b_test_website_tripadvisor_online_wf.md):

- multiple step-0 failures convert a required `CLICK` into an early `TYPE`
- example tasks that should begin by entering a category or opening navigation are pushed into location search instead
- example wrong values include `Eiffel Tower Paris`, `Jaipur`, `San Francisco`, and `Egypt`

This is consistent with a recorded prompt-level mismatch pattern, but not by itself a controlled causal proof.

### Reddit

From `paired_case_output.txt`:

- `positive = 2`
- `negative = 5`
- `net = -3`

From [negative_qwen_qwen3_5-397b-a17b_test_domain_reddit_online_wf.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/case_studies/negative_qwen_qwen3_5-397b-a17b_test_domain_reddit_online_wf.md):

- the failures are mostly `CLICK` substitutions
- the induced workflow assumes a small menu of Reddit-specific routines such as search, join, sort, and time filter
- these routines are not broadly transferable once the target task diverges from the learned community/search template

This is weaker than the Tripadvisor case and should be read only as same-direction exploratory evidence.

## A7.4 Exploratory Reading

The existing evidence supports only a cautious exploratory reading.

### Offline workflow

- derived from training data rather than from the model's own recent test-time trajectories
- broader and more reusable at the text level
- steadier on `CLICK` grounding and later-stage navigation on `kayak`
- potentially vulnerable when the learned library is semantically misaligned with the evaluated task/site

### Online workflow

- induced from same-run trajectories in the current implementation, so it is closer to the immediate test distribution
- stronger at local TYPE/value guidance on `kayak`
- narrower and more routine-shaped
- more likely to encode local biases or wrong subroutines that later appear in prompt-level mismatch cases

## A7.5 Safe Claim

This appendix supports the following conservative claim:

> On the current first-run Mind2Web logs, `offline_wf` and `online_wf` appear to differ in where their gains show up on `kayak`: `offline_wf` looks steadier on CLICK-side grounding, while `online_wf` looks stronger on local TYPE/value guidance. The additional target-site results are exploratory context only and should not be promoted to a standalone causal mechanism claim.

## A7.6 Boundary Note

This is still first-run evidence, not a repeated-estimate claim.

In particular:

- the direct `offline_wf` vs `online_wf` comparison here is only on `kayak`
- the target-site underperformance evidence comes from only `tripadvisor` and `reddit`
- the mechanism reading remains weaker than controlled causal identification and should be treated as exploratory
