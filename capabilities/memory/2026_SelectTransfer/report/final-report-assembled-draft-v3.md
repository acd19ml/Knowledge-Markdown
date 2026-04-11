# Selective Transfer in Memory-Augmented LLM Agents

> **Supporting materials**
> - **L1 Narrative:** [final-report-round1-section-v2.md](./final-report-round1-section-v2.md)
> - **L2 Evidence Map:** [round1-evidence-map.md](./round1-evidence-map.md)
> - **L3 Case Appendix:** [round1-case-appendix.md](./round1-case-appendix.md)

## Abstract

This project studies whether memory-augmented language-model agents exhibit **selective transfer** rather than indiscriminate memory reuse. Instead of asking whether memory improves average benchmark performance, we ask whether memory helps on structurally matched tasks while avoiding harm on mismatched tasks under a fixed experience budget. We instantiate this question in a near-transfer setting from **HotpotQA** to **2WikiMultiHopQA** using `Qwen/Qwen3.5-9B`, comparing three conditions: `No Memory`, `Episodic Trace`, and `Cross-Episode Consolidation`.

Round 1 did not yield a simple benchmark-win story. Its main contribution is methodological. A controlled sequence of single-variable repairs showed that early negative-transfer evidence was highly sensitive to prompt observability, case-role discipline, pairing granularity, and the executability of abstract memory. In the strongest diagnostic case, an apparent “relevant memory hurts” result was overturned after subtype-aware rerouting and operator-level repair. The final outcome is therefore not a claim that memory broadly works, but a claim that selective-transfer evaluation requires fine-grained pairing, role-aware analysis, and executable abstractions.

## 1. Introduction

### 1.1 Motivation

A central question in memory-augmented AI is not simply whether past experience can be stored, but when stored experience becomes **reusable knowledge** rather than inert context or a source of interference. Existing memory-based methods for LLM agents are often evaluated by average benchmark gain. That framing is too weak for the question we actually care about, because it does not distinguish useful reuse from indiscriminate reuse.

This project therefore reframes evaluation around **selective transfer**:

> Under a fixed experience budget, does a memory mechanism help on structurally matched target tasks while avoiding harm on mismatched target tasks?

Under this framing, a memory strategy is useful only if it satisfies two constraints:

1. it helps, or at least does not harm, on structurally matched tasks  
2. it avoids negative transfer on mismatched tasks

### 1.2 Scope of the Project

The long-term question behind this work is broader: when does experience become reusable knowledge, and perhaps a lasting influence on later judgment? That question is too broad for a single course project. This project therefore cuts a narrower empirical slice: a near-transfer QA setting with a small model, a fixed experience budget, and a small number of controlled memory conditions.

The goal is not to produce a large-scale efficacy result. The goal is to build a measurement workflow that can separate genuine selective transfer from confounds introduced by coarse pairing, insensitive evaluation, or non-executable abstraction.

### 1.3 Contribution

The contribution of Round 1 is threefold:

1. **An evaluation perspective.** The project evaluates `Relevant` and `Irrelevant` transfer separately rather than reporting only average gain.
2. **A protocol.** The project defines a traceable workflow including taxonomy, source-set construction, frozen pairing, case-role discipline, artifact review, and single-variable diagnosis.
3. **A route-selection signal.** The results indicate which later questions should focus on `memory form`, `memory use`, or their coupling.

## 2. Method

### 2.1 Experimental Setting

| Component | Specification |
|---|---|
| Source benchmark | HotpotQA (dev set) |
| Target benchmark | 2WikiMultiHopQA (dev set) |
| Transfer type | Near-transfer |
| Model | `Qwen/Qwen3.5-9B` |
| Source experience budget | `N = 5` solved source tasks per source set |
| Decoding | Greedy; fixed scaffold and max generation limit |

The choice of a 9B model was deliberate. The project is not optimizing for benchmark performance, but for interpretable diagnostic behavior.

### 2.2 Reasoning Taxonomy

The initial task taxonomy used a small number of dominant reasoning labels:

- `bridge`
- `comparison`
- `temporal`
- `distractor-heavy`

Each task received exactly one dominant label before pairing. During Round 1, the project discovered that `bridge` was too coarse and had to be refined into:

- `attribute_bridge`
- `relation_chain_bridge`

This refinement later became one of the key methodological findings.

### 2.3 Source Sets and Pairing

Source memory is not treated as a generic retrieval pool. Instead, the project constructs explicit source sets of exactly `N = 5` solved episodes. Each set is internally coherent by reasoning cluster and reviewed before use.

The main source sets used in Round 1 are:

| Source Set ID | Reasoning Cluster | Bridge Subtype |
|---|---|---|
| `hp_comparison_set_01` | comparison | — |
| `hp_bridge_set_01` | bridge | attribute_bridge |
| `hp_relation_chain_bridge_set_01` | bridge | relation_chain_bridge |

Each target task is assigned a frozen `Relevant` and `Irrelevant` source set **before** runs begin. Pairing is never redefined from observed outcomes. When pairing granularity was later found to be insufficient, the project preserved the old pairing and opened a new sub-round with corrected routing rather than editing completed runs.

### 2.4 Memory Conditions

Round 1 compares three conditions:

| Condition | Memory Content |
|---|---|
| `No Memory` | No past-experience block |
| `Episodic Trace` | Per-episode compressed solved trajectories |
| `Cross-Episode Consolidation` | A single abstraction synthesized from all five episodes |

A fourth condition involving applicability judgment was defined in the broader proposal but intentionally deferred. Round 1 first focused on making the measurement workflow defensible.

### 2.5 Prompt Scaffold and Metrics

The early pilot often produced opaque one-line answers. Round 1b repaired this by imposing a structured scaffold with:

- `## Reasoning`
- `## Final Answer`

This made the following process-level metrics available:

- `parse_success`
- `reasoning_present`
- `final_answer_present`
- `memory_reference_type`

Outcome metrics remained:

- Exact Match (EM)
- token-level F1

Relevant and Irrelevant results are always reported separately. Mixed aggregate reporting is forbidden.

### 2.6 Methodological Commitments

Three protocol-level commitments became central to the method:

1. **Case-role discipline.** Cases must be classified as `process sanity`, `diagnostic`, or `boundary` before any summary table is trusted.
2. **Subtype-aware pairing.** A coarse label such as `bridge` is not enough if the target depends on a more specific subtype.
3. **Executable abstraction.** For consolidation-style memory, topical relevance is insufficient unless the artifact preserves operator structure in an executable form.

These are not implementation details. They are part of the experimental method itself.

## 3. Results

Round 1 is best interpreted as a **repair chain**, not as a single benchmark comparison.

### 3.1 Stage I: Making the Experiment Observable

Round 1b's structured scaffold made memory behavior visible for the first time. All smoke runs became parseable, and the model began to show explicit memory use and explicit memory rejection in the reasoning trace.

This was especially clear on `wiki_dev_8896`, where the model explicitly used relevant episodic memory and explicitly rejected irrelevant episodic memory while keeping the same correct answer in both cases. This did not yet establish transfer efficacy, but it established that process-level selectivity was observable.

Round 1c then showed that the six smoke cases could not be pooled into a single mini-benchmark. Once cases were reassigned into `process sanity`, `diagnostic`, and `boundary` roles, mixed-role averages lost their interpretive value.

### 3.2 Stage II: Repairing Pairing Granularity

The most important early negative result came from `wiki_dev_2639`, where the no-memory baseline answered correctly (`Henry Pelham`) but relevant memory degraded to refusal. At first glance, this looked like strong evidence that relevant memory could hurt.

Round 1d showed that this interpretation was too quick. `wiki_dev_2639` is a `relation_chain_bridge` task, but its relevant source had originally been drawn from `hp_bridge_set_01`, which actually represented `attribute_bridge` episodes. The target was therefore only “relevant” under an overly coarse label.

After subtype-aware source expansion and rerouting, Round 1g reran the affected relation-chain targets. On `wiki_dev_2639`:

- `No Memory` remained correct
- `Relevant Episodic Trace` changed from wrong to correct
- `Irrelevant Episodic Trace` remained wrong

This overturned the early interpretation. The episodic failure was not evidence that relevant memory was intrinsically harmful; it was evidence that coarse pairing granularity can manufacture a false negative.

### 3.3 Stage III: Repairing Operator-Level Abstraction

Subtype-aware rerouting repaired episodic memory, but relevant consolidation still failed on `wiki_dev_2639`. Round 1h improved the structure and wording of the relation-chain consolidation artifact, but the answer remained wrong. The remaining problem was no longer subtype mismatch. It was operator interpretation.

Round 1i therefore changed only the executable interpretation of `sibling-in-law`. The repaired artifact decomposed the operator into explicit candidate paths and blocked irrelevant default branches. This single change recovered the relevant consolidation answer from wrong to correct, while irrelevant consolidation remained wrong.

This result is stronger than a generic “prompt refinement helps” claim. It shows that relevant abstract memory can still fail if its abstraction is not executable enough for the target operator structure.

### 3.4 The Key Diagnostic Case

`wiki_dev_2639` is the most informative case in Round 1 because it supports a full before/after interpretation shift:

- the no-memory baseline is correct
- relevant memory initially degrades
- subtype-aware rerouting repairs episodic trace
- operator-aware repair repairs consolidation
- irrelevant memory remains wrong

This single case does not prove broad generalization. But it is enough to show that early “relevant memory hurts” evidence was not stable under protocol repair.

## 4. Discussion

The most important outcome of Round 1 is methodological rather than purely empirical.

At the start of the project, one plausible interpretation was:

> relevant memory can hurt an otherwise correct baseline

By the end of Round 1, that interpretation could no longer be defended in the strongest diagnostic case. Once the experiment repaired:

- observability
- case-role discipline
- subtype-level pairing
- operator-level abstraction

the earlier negative interpretation was overturned.

This leads to two broader implications.

First, **relevance must be operationalized at the correct granularity**. A coarse cluster label is not enough if the target depends on a more specific subtype.

Second, **abstract memory must be executable, not merely relevant**. For consolidation-style memory, it is not enough to summarize what relation matters. The artifact must also preserve how that relation should be checked.

These conclusions do not establish broad memory efficacy. They establish a stronger evaluation standard for future work.

## 5. Claims and Non-Claims

Round 1 supports the following claims:

- process-level selectivity can be made observable
- mixed-role aggregate can be misleading
- coarse pairing granularity can create false negatives
- executable abstraction can be necessary for successful consolidation

Round 1 does **not** support the following stronger claims:

- strong average benchmark gain
- large-scale demonstration of selective transfer
- universal ranking between episodic trace and consolidation
- broad generalization from a single repaired diagnostic case

These boundaries are deliberate. They are part of the project's experimental discipline.

## 6. Limitations

The current evidence remains limited in three important ways.

First, the strongest repaired evidence is concentrated in a small number of diagnostic cases, especially `wiki_dev_2639`.

Second, all runs use `Qwen/Qwen3.5-9B`. The project does not test whether larger models would reduce the need for operator-level repair.

Third, even the repaired consolidation result remains imperfect at the process level. The model reaches the correct answer, but still shows visible hesitation and self-correction in its reasoning trace.

## 7. Future Work

The next sensible step is not another long chain of single-case repairs. The better continuation is:

- keep the repaired protocol fixed
- expand to a slightly broader but still clean diagnostic subset
- test whether the repaired `relation_chain` logic generalizes beyond one key case

The next round should therefore ask:

> does the repaired workflow generalize beyond the strongest diagnostic case?

That is a cleaner next question than reopening naive average-gain comparisons or adding uncontrolled new memory conditions.

## 8. Final Takeaway

Round 1 should be read as a **measurement and interpretation success**, not as a benchmark-win story.

Its central contribution is this:

> apparent negative transfer can be produced by coarse pairing and non-executable abstraction, and a controlled repair chain can overturn that interpretation without changing the underlying model.

This does not prove that memory broadly works. It shows something more foundational for this project: **selective-transfer evaluation is only meaningful when pairing granularity, case-role discipline, and executable memory abstraction are treated as first-class methodological variables.**
