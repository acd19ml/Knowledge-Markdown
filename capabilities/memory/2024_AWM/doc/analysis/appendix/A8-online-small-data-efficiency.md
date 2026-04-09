# Appendix A8. Online Workflow Efficiency Under Very Small Data Budgets

## Purpose

This appendix is retained as an exploratory prefix-level rereading of logged online results. It should not be used as a primary final-report appendix for a cross-site mechanism claim.

The paper's online-memory narrative implies that a small number of trajectories may already be enough to make the induced workflow useful.

This appendix checks that implication without adding any new experiment. It asks:

- when `induce_steps=1`, does `online_wf` show measurable gains after only a few induced examples?
- is that early-gain pattern stable across source and target settings?

## Source Materials

- [online_small_data_curve_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/online_small_data_curve_output.txt)
- [online_small_data_curve.py](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/scripts/online_small_data_curve.py)
- [step_breakdown_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/step_breakdown_output.txt)
- [paired_case_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/paired_case_output.txt)

## A8.1 Method

For each online setting, define:

- `budget = i`
- where `i` is the number of prior examples already used for workflow induction when evaluating sample `i`

Under `induce_steps=1`:

- `budget=0` means the very first sample, still without induced workflow
- `budget=1` means one prior example has already been folded into the workflow
- `budget=2` means two prior examples have already been folded in

For each site, we compare:

- `online_wf`
- against the matching `no_workflow`

and compute cumulative prefix deltas for:

- `Elem Acc`
- `Action F1`
- `Step SR`

## A8.2 Main Result

### Prefix-level `Step SR` deltas

| site | earliest positive prefix | best prefix | final prefix |
|---|---|---|---|
| kayak | `budget=1`, `+5.00pp` | `budget=5`, `+5.63pp` | `+5.63pp` |
| tripadvisor | none | best observed still negative (`budget=1`, `-3.57pp`) | `-11.74pp` |
| reddit | `budget=10`, `+2.02pp` | `budget=10`, `+2.02pp` | `-2.16pp` |

This is the most concise descriptive answer to the small-data question:

- **yes on the source site (`kayak`)**
- **no on the harder target-site first run (`tripadvisor`)**
- **only weakly and temporarily on `reddit`**

So the current evidence does not support a benchmark-wide claim that online memory becomes useful after only a very small budget. It supports a narrower descriptive claim: **very-small-budget gains appear on `kayak`, but the same pattern is not reproduced on the two available target-site first runs.**

## A8.3 Site-by-Site Reading

### `kayak`

From [online_small_data_curve_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/online_small_data_curve_output.txt):

- after only **one** induced example, cumulative `Step SR` is already `+5.00pp`
- the gain remains positive throughout the available prefix
- the final prefix reaches `+5.63pp`

This is real early gain, not just a late-stage effect.

Combined with [A7-offline-vs-online-tradeoff.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A7-offline-vs-online-tradeoff.md), a cautious reading is:

- `online_wf` quickly learns a locally useful routine
- on `kayak`, that routine is close enough to the test distribution to help early

### `tripadvisor`

- the first induced example already yields cumulative `Step SR = -3.57pp`
- no positive prefix appears at any small budget
- the full prefix ends at `-11.74pp`

This is the opposite of a small-data efficiency story.

One exploratory explanation is not simply "too little data", but **wrong early pattern acquisition**:

- a few early induced trajectories are enough to create a workflow
- but that workflow is already semantically mismatched to the target navigation structure
- so small data does not produce early benefit; it produces early bias

### `reddit`

- there is no early gain at budgets `1, 2, 3, 5`
- the first positive cumulative `Step SR` appears only at `budget=10`
- that gain is small (`+2.02pp`) and disappears by the final prefix

So `reddit` is not a clean "small-data works" case either.

The more cautious interpretation is:

- online induction may need more than a handful of examples before any net benefit appears
- even then, the benefit may be unstable

## A8.4 Mechanism Interpretation

This pattern is consistent with a broader exploratory reading developed elsewhere in the project:

- on `kayak`, `online_wf` can acquire a useful local routine quickly
- on the two target-site first runs here, the same small-budget pattern is not stable

So the small-data question should be answered conditionally and descriptively:

> Online workflow induction can show early gains under very small budgets on `kayak`, but the current first-run evidence does not show the same pattern on `tripadvisor` or `reddit`.

## A8.5 Safe Claim

This appendix supports the following conservative wording:

> Under the current Mind2Web first-run evidence, online memory shows genuine early gains on `kayak` after only one induced example, but this very-small-budget benefit does not generalize reliably to larger distribution shifts such as `tripadvisor` and `reddit`.

## A8.6 Boundary Note

- This is still a first-run analysis.
- The prefix curve is reconstructed from logged online results, not from repeated random seeds.
- The comparison is strongest as a descriptive small-budget pattern, not as a formal learning-curve estimate.
