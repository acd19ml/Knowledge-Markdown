# Memory Selective Transfer Under a Fixed Experience Budget

> **Supporting layers**
> - Main Round 1 narrative: [final-report-round1-section-v2.md](./final-report-round1-section-v2.md)
> - Claim-to-evidence traceability: [round1-evidence-map.md](./round1-evidence-map.md)
> - Key raw exhibits: [round1-case-appendix.md](./round1-case-appendix.md)

## Abstract

This project studies whether memory-augmented language-model agents exhibit **selective transfer** rather than indiscriminate memory reuse. Instead of asking whether memory improves average benchmark performance, we ask whether memory helps on structurally matched tasks while avoiding harm on mismatched tasks under a fixed source experience budget. We instantiate this question in a near-transfer setting from **HotpotQA** to **2WikiMultiHopQA** using `Qwen/Qwen3.5-9B`, comparing `No Memory`, `Episodic Trace`, and `Cross-Episode Consolidation`. Round 1 did not yield a simple benchmark-win story. Its main contribution is methodological: a sequence of controlled repairs showed that early negative-transfer evidence was highly sensitive to prompt observability, case-role discipline, pairing granularity, and the executability of abstract memory. In the strongest diagnostic case, an apparent “relevant memory hurts” result was overturned after subtype-aware rerouting and operator-level repair. The final outcome is not a claim that memory works broadly, but a claim that selective-transfer evaluation requires fine-grained pairing, role-aware analysis, and executable abstractions.

## 1. Introduction

The long-term question behind this project is not benchmark improvement by itself, but a broader memory question:

> when does past experience become reusable knowledge rather than a stored trace?

In current memory-augmented LLM work, evaluation often centers on average task performance or ablations over retrieval variants. That framing is too weak for the question we actually care about. A memory system can look useful in aggregate while still being applied indiscriminately, or it can appear harmful because the experiment operationalizes relevance too coarsely.

This project therefore focuses on **selective transfer**. Under this framing, a memory strategy is useful only if it satisfies two constraints:

1. it helps, or at least does not harm, on structurally matched tasks
2. it avoids negative transfer on mismatched tasks

This is a narrower empirical slice than a full theory of memory formation, but it is a defensible middle layer between broad theory and benchmark-only engineering. The project is designed as a route-selection experiment: if selective transfer depends mainly on how experience is represented, future work should prioritize `memory form`; if it depends mainly on how memory is gated or judged, future work should prioritize `memory use`.

## 2. Experimental Setting

We study a fixed near-transfer setting:

- **Source benchmark:** HotpotQA
- **Target benchmark:** 2WikiMultiHopQA
- **Model:** `Qwen/Qwen3.5-9B`
- **Source experience budget:** `N = 5` solved source episodes per source set

The experiment compares three memory conditions:

1. **No Memory**
2. **Episodic Trace**
3. **Cross-Episode Consolidation**

All important variables are held fixed within each controlled sub-round:

- benchmark split
- source-target pairing
- model
- prompt scaffold
- decoding strategy
- source experience count

This follows the project's experiment contract: each sub-round changes exactly one variable, and any interpretation must remain within the actual scope of the current setting.

## 3. Method

### 3.1 Pairing-Oriented Evaluation

The experiment is not built around benchmark-wide average gain. Instead, it uses predefined source-target pairings.

Each target task is assigned:

- a **Relevant** source set
- an **Irrelevant** source set

Both are frozen before the corresponding runs begin. Pairing is never retroactively redefined from the observed result. This matters because the central question is not whether memory exists, but whether its use is selective.

### 3.2 Reasoning Taxonomy and Granularity

Tasks are first organized into a small reasoning taxonomy. Early in the project, this included coarse labels such as:

- `bridge`
- `comparison`
- `temporal`
- `distractor-heavy`

Round 1 later showed that this taxonomy was not granular enough. In particular, `bridge` had to be split into:

- `attribute_bridge`
- `relation_chain_bridge`

This became one of the most important methodological findings of the project. A task can be “relevant” under a coarse cluster label while still being structurally mismatched at the subtype level.

### 3.3 Source Set Construction

Source memory is not drawn from an unconstrained retrieval pool. Instead, each source set:

- contains exactly `N = 5` solved source episodes
- is internally coherent by reasoning cluster
- is constructed before the target runs
- is manually reviewed before use in experiments

Three source sets are especially important in Round 1:

- `hp_comparison_set_01`
- `hp_bridge_set_01`
- `hp_relation_chain_bridge_set_01`

The third set was constructed only after the project discovered that some target tasks required a subtype-aware `relation_chain_bridge` source rather than a generic `bridge` source.

### 3.4 Memory Artifacts

The two memory-bearing conditions differ in representation:

- **Episodic Trace** stores compressed per-episode task traces
- **Cross-Episode Consolidation** stores an abstracted lesson synthesized across source episodes

A key methodological distinction emerged during Round 1: for abstract memory, topical relevance alone is insufficient. The consolidation artifact must preserve **operator structure** in an executable way.

### 3.5 Observability and Parsing

The original pilot produced mostly short, opaque answers. Round 1b repaired this by imposing a structured output scaffold:

- `## Reasoning`
- `## Final Answer`

This enabled:

- consistent parsing
- process-level inspection
- identification of explicit memory use and explicit memory rejection

Without this scaffold, the project would have remained a black-box score comparison.

## 4. Round 1 Results

Round 1 is best understood not as a single run, but as a controlled repair chain.

### 4.1 Stage I: Making the Experiment Observable

The initial pilot established the full pipeline, but its outputs were not sufficiently interpretable. Round 1b fixed the measurement layer by forcing structured reasoning output. This made process-level selectivity visible for the first time.

On the process-sanity case `wiki_dev_8896`, the model explicitly used relevant memory and explicitly rejected irrelevant memory while producing the same correct final answer in both cases. This did not show transfer efficacy, but it did show that the experiment could now observe memory interaction instead of inferring it from score changes alone.

Round 1c then prevented a second source of distortion: heterogeneous cases could no longer be pooled into a single smoke-benchmark average. Cases were reclassified into `process sanity`, `diagnostic`, and `boundary` roles, and mixed-role aggregate reporting was banned.

### 4.2 Stage II: Repairing Pairing Granularity

The most important early negative result came from `wiki_dev_2639`, a task asking:

> Who is the sibling-in-law of Harriet Pelham-Holles, Duchess Of Newcastle-Upon-Tyne?

The no-memory baseline answered correctly (`Henry Pelham`), but relevant memory initially degraded to refusal. At first glance, this looked like strong evidence that relevant memory could hurt.

Round 1d showed that this interpretation was too quick. The target was a `relation_chain_bridge` case, but its relevant source had been drawn from `hp_bridge_set_01`, which actually represented `attribute_bridge` episodes. In other words, the target was “relevant” only under an overly coarse label.

Rounds 1e–1f constructed a subtype-matched source set, `hp_relation_chain_bridge_set_01`, without changing the model or prompt. Round 1g then reran only the affected targets. On `wiki_dev_2639`:

- `No Memory` remained correct
- `Relevant Episodic Trace` changed from wrong to correct
- `Irrelevant Episodic Trace` remained wrong

This overturned the earlier interpretation. The episodic failure was not evidence that relevant memory was harmful; it was evidence that coarse pairing granularity can manufacture a false negative.

### 4.3 Stage III: Repairing Operator-Level Abstraction

Subtype-aware rerouting repaired episodic memory, but it did not automatically repair consolidation. The relevant consolidation run on `wiki_dev_2639` still failed.

Round 1h improved the relation-chain consolidation artifact's structure and wording, but correctness still did not return. This narrowed the remaining problem to a more specific source: the abstraction was still not executable enough.

Round 1i then repaired only the operator layer, focusing on the interpretation of `sibling-in-law`. The revised artifact explicitly decomposed the relation into candidate paths and prohibited irrelevant fallback branches.

This single change recovered the relevant consolidation answer on `wiki_dev_2639` from wrong to correct, while irrelevant consolidation remained wrong. The conclusion was therefore stronger than “better wording helps.” It showed that abstract memory must preserve executable operator structure if it is to support selective transfer on this kind of task.

### 4.4 The Key Diagnostic Case

`wiki_dev_2639` became the strongest diagnostic case in the project because it supported a full interpretation shift:

- the baseline was correct
- relevant memory initially degraded
- subtype-aware rerouting repaired episodic memory
- operator-aware repair repaired consolidation
- irrelevant memory remained wrong

This case is not enough to prove broad generalization. But it is enough to show that early “relevant memory hurts” evidence was not stable under protocol repair.

## 5. Discussion

The most important lesson of Round 1 is methodological rather than purely empirical.

At the start of the project, a plausible interpretation was:

> relevant memory can hurt an otherwise correct baseline

By the end of Round 1, that interpretation could no longer be defended in the key case. Once the experiment repaired:

- observability
- case-role discipline
- subtype-level pairing
- operator-level abstraction

the earlier negative interpretation was overturned.

This leads to two broader implications.

First, **relevance must be operationalized at the right granularity**. A coarse reasoning label is not enough if the actual target depends on a more specific subtype.

Second, **abstract memory must be executable, not merely relevant**. For consolidation-style memory, it is not enough to summarize what relation matters; the artifact must also encode how to operationalize that relation.

These conclusions do not establish broad memory efficacy. But they do provide a more defensible protocol for asking when memory is genuinely reusable and when the experiment is only measuring its own abstraction errors.

## 6. Claims and Non-Claims

Round 1 supports the following claims:

- process-level selectivity can be made observable
- mixed-role aggregate can be misleading
- coarse pairing granularity can create false negatives
- executable abstraction can be necessary for successful consolidation

Round 1 does **not** support the following stronger claims:

- strong average benchmark gain
- large-scale demonstration of selective transfer
- a universal ranking between episodic trace and consolidation
- broad generalization from a single repaired diagnostic case

These boundaries are not incidental. They are part of the project's experimental discipline.

## 7. Limitations

The current evidence remains limited in three important ways.

First, the strongest repaired evidence remains concentrated in a small number of diagnostic cases, especially `wiki_dev_2639`.

Second, all runs use `Qwen/Qwen3.5-9B`. The project does not test whether larger models would reduce the need for operator-level repair.

Third, even the repaired consolidation outcome remains imperfect at the reasoning-process level. The model arrives at the correct answer, but still shows visible hesitation and self-correction in the raw reasoning trace.

## 8. Future Work

The next sensible step is not another long chain of single-case repairs. The better continuation is:

- keep the repaired protocol fixed
- expand to a slightly broader but still clean diagnostic subset
- test whether the repaired `relation_chain` logic generalizes beyond one key case

In other words, the next round should ask:

> does the repaired workflow generalize beyond the strongest diagnostic case?

That is a cleaner question than returning to naive average-gain comparisons or adding uncontrolled new memory conditions.

## 9. Final Takeaway

Round 1 should be read as a **measurement and interpretation success**, not as a benchmark-win story.

Its main contribution is the following:

> apparent negative transfer can be produced by coarse pairing and non-executable abstraction, and a controlled repair chain can overturn that interpretation without changing the underlying model.

This does not prove that memory broadly works. It shows something more foundational for this project: **selective-transfer evaluation is only meaningful when pairing granularity, case-role discipline, and executable memory abstraction are all treated as first-class methodological variables.**
