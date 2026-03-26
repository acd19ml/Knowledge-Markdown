# Experiment Framework for the Revised Topic 6 Proposal

> Main proposal: [proposal.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2026_Epi2Lesson/proposal.md)  
> Critical rationale: [proposal-analysis.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2026_Epi2Lesson/proposal-analysis.md)  
> Progress narrative: [progress-report.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2026_Epi2Lesson/progress-report.md)

---

## 1. One-Sentence Project Definition

This project asks:

> **When the same source experience is stored as a concrete episode versus a reusable lesson, how does later cross-task reuse change?**

The project does **not** study:

- whether retrieval is optimal,
- whether prompt orchestration is optimal,
- whether the agent internally “understood” the failure correctly,
- or how to automatically generate the best possible lesson at scale.

It studies one controlled variable only:

- **experience abstraction**: `episode` vs `lesson`

---

## 2. Why This Is the Right Experimental Scope

The revised scope is chosen for three reasons.

### 2.1 It is narrower than the original proposal

The original proposal asked mechanism questions about:

- reflection correctness,
- transfer correctness,
- retrieval relevance.

Those questions became too hard to close cleanly because they depend on latent or weakly defined ground truth.

### 2.2 It is still open, but not too open

Existing work already shows:

- abstraction helps in some form,
- format alone is not the core issue,
- workflows, insights, and skills can sometimes transfer.

But existing work does **not** cleanly isolate:

> the behavioral difference between an **episodic memory** and a **lesson distilled from the same episode**.

This is therefore a reasonable course-project question:

- not fully solved in the selected setting,
- but clear enough to answer through controlled experiments.

### 2.3 It matches the official topic style

The official topics are built around:

- a bounded empirical question,
- explicit comparison conditions,
- concrete metrics,
- and interpretable tradeoffs.

This proposal now fits that template.

---

## 3. Core Experimental Objects

### 3.1 Episode memory

A context-rich description of a specific past event.

Characteristics:

- retains specific task instance details,
- retains concrete objects and local context,
- preserves the original event framing.

### 3.2 Lesson memory

A reusable abstraction distilled from the same source experience.

Characteristics:

- removes task-instance-specific details,
- keeps the condition-action lesson,
- aims for reuse beyond the original episode.

### 3.3 Benchmark role

The benchmark is **ALFWorld**, but only as a **controlled subset benchmark**.

Why:

- already available in the current infrastructure,
- low execution cost,
- easy success/failure interpretation,
- suitable for controlled memory injection.

But:

- some ALFWorld failures are dominated by interaction-format issues,
- so the benchmark must be filtered to task cases where reusable lessons are interpretable.

---

## 4. Experimental Matrix

The smallest useful experiment package is:

| Condition | Memory injected | Purpose |
|---|---|---|
| `C0` | No memory | baseline |
| `C1` | Episode memory | concrete experience reuse |
| `C2` | Lesson memory | abstracted experience reuse |

Target tasks are divided into:

| Target type | Meaning |
|---|---|
| `T1 Reusable` | source lesson should plausibly help |
| `T2 Near-miss` | superficially similar, but key constraint differs |
| `T3 Unrelated` | no plausible reuse relation |

This creates a minimal matrix:

- `C0/C1/C2 × T1/T2/T3`

That is already enough to answer the revised proposal.

---

## 5. Experiments

## Experiment 1. Episode vs Lesson

### Question

Does lesson memory help more than episode memory on later tasks?

### Design

For each selected source case:

1. collect one source experience,
2. construct an `episode` version,
3. construct a `lesson` version from the same case,
4. evaluate on target tasks under `C0`, `C1`, and `C2`.

### Metrics

- **Success Rate (SR)**
- **Transfer Gain** over `C0`
- **Prompt Length**

### Why this experiment matters

It isolates the project’s main variable directly.

### Critical reflection

- This is meaningful and not redundant.
- It is also the cleanest experiment in the proposal.
- If this experiment fails to show interpretable differences, the whole revised proposal weakens.

---

## Experiment 2. Information-Loss Analysis

### Question

When an episode is turned into a lesson, what information gets removed, and which removals hurt reuse most?

### Design

For each `episode -> lesson` conversion, annotate removed information categories such as:

- object-specific details,
- environment-specific constraints,
- preconditions,
- exception/failure cues,
- local action-order details.

Then examine which removed categories are associated with target-task failure.

### Outputs

- failure count by removed-information category,
- representative episode/lesson comparison table,
- compact qualitative discussion.

### Why this experiment matters

Without this step, the proposal becomes a simple winner-comparison.

### Critical reflection

- This is where the project gains depth.
- But it also introduces manual judgment.
- Therefore the sample must remain deliberately small.

---

## Experiment 3. Reuse vs Over-Generalization

### Question

Does lesson memory transfer better than episode memory, but also over-generalize more often?

### Design

Compare `C1` and `C2` across:

- `T1 Reusable`
- `T2 Near-miss`
- `T3 Unrelated`

### Metrics

- **Positive Transfer Gain**
- **Negative Transfer Count**
- **Net Utility**

### Why this experiment matters

It prevents the project from reducing to “abstraction is better.”

### Critical reflection

- This experiment is essential.
- Its validity depends on a stable definition of `Reusable / Near-miss / Unrelated`.
- These labels must be decided before observing results.

---

## 6. Evaluation Summary

The project should report:

| Category | Metrics |
|---|---|
| Main task outcome | `SR`, `Transfer Gain` |
| Compactness | `Prompt Length` |
| Failure tradeoff | `Negative Transfer Count`, `Net Utility` |
| Mechanism analysis | failure breakdown by removed-information type |

The project should **not** claim more than these metrics support.

In particular, it should not claim:

- “the agent truly understood the lesson,”
- “the lesson is objectively correct,”
- or “this solves cross-task memory in general.”

---

## 7. Risks

### Risk 1: ALFWorld subset is too noisy

If the chosen tasks are dominated by formatting or interface protocol failures, the experiment will measure interface brittleness instead of experience abstraction.

Mitigation:

- use a filtered subset,
- document why selected tasks support interpretable lesson construction.

### Risk 2: Lesson construction is too subjective

If episode and lesson versions are written inconsistently, results may reflect wording quality rather than abstraction level.

Mitigation:

- use a fixed construction template,
- keep lesson generation controlled,
- avoid turning this into a free-form prompting problem.

### Risk 3: The project becomes too ambitious again

If retrieval, triggering, progressive disclosure, or procedural-skill induction are added back in, the proposal will lose its clean variable.

Mitigation:

- keep retrieval fixed,
- keep injection style fixed,
- keep the focus on `episode -> lesson`.

---

## 8. Expected Contribution

The strongest plausible contribution for this course project is:

> a controlled empirical analysis of how a concrete experience changes in cross-task utility when abstracted into a reusable lesson.

That contribution is modest, but it is:

- clearly scoped,
- empirically testable,
- grounded in the repo’s memory theory,
- and not already fully answered in the selected setting.

---

## 9. Immediate Next Action

Before any new large-scale runs, the project should complete:

1. a **task-subset definition** for ALFWorld,
2. an **episode-to-lesson construction template**,
3. a small pilot under:
   - `No memory`
   - `Episode memory`
   - `Lesson memory`

If that pilot yields interpretable differences, the revised proposal is validated as experimentally viable.
