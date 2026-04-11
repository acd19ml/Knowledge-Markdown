# Selective Transfer in Memory-Augmented LLM Agents

> **Supporting materials**
> - **L1 Narrative:** [final-report-round1-section-v2.md](./final-report-round1-section-v2.md)
> - **L2 Evidence Map:** [round1-evidence-map.md](./round1-evidence-map.md)
> - **L3 Case Appendix:** [round1-case-appendix.md](./round1-case-appendix.md)
>
> Inline references use the format `[L2 §C3]` or `[L3 Exhibit A]`.

---

## Abstract

This project studies whether memory-augmented language-model agents exhibit **selective transfer** rather than indiscriminate memory reuse. Instead of asking whether memory improves average benchmark performance, we ask whether memory helps on structurally matched tasks while avoiding harm on mismatched tasks under a fixed experience budget. We operationalize this in a near-transfer setting from HotpotQA to 2WikiMultiHopQA using `Qwen/Qwen3.5-9B`, comparing three conditions — No Memory, Episodic Trace, and Cross-Episode Consolidation — across predefined Relevant and Irrelevant splits.

Round 1, the pilot phase, did not yield a simple benchmark-win story. A controlled sequence of single-variable repairs showed that early negative-transfer evidence was highly sensitive to prompt observability, case-role discipline, pairing granularity, and the executability of abstract memory. In the strongest diagnostic case, an apparent "relevant memory hurts" result was overturned after subtype-aware rerouting and operator-level repair — recovering both memory forms without changing the underlying model. The main contribution is methodological: selective transfer claims are only as reliable as the operational definition of relevance and the executability of the memory abstraction. Without fine-grained pairing, case-role discipline, and executable memory representations, the experiment risks measuring its own setup artifacts rather than the phenomenon of interest.

---

## 1. Introduction

### 1.1 Motivation

A central question in memory-augmented AI is not simply whether past experience can be stored, but when stored experience becomes **reusable knowledge** — something that selectively improves future performance rather than acting as inert context or a source of interference.

Existing memory-based methods for LLM agents — retrieval-augmented generation, episodic memory buffers, experience distillation — are typically evaluated by average benchmark performance. This evaluation practice conflates two very different outcomes: improvement because the retrieved experience was genuinely relevant, and improvement (or degradation) because more context was injected regardless of relevance. As a result, it is often unclear whether a memory method supports useful transfer or merely causes indiscriminate reuse.

### 1.2 Selective Transfer as the Research Frame

This project reframes memory evaluation around **selective transfer**:

> Under a fixed experience budget, does a memory mechanism help on structurally matched target tasks while avoiding harm on mismatched target tasks?

Under this framing, a memory strategy is useful only if it satisfies two constraints:

1. it helps, or at least does not harm, on structurally matched tasks
2. it avoids negative transfer on mismatched tasks

To operationalize this, we predefine two controlled splits for every target task:

- **Relevant Split** — source memory and target task share the same reasoning subtype.
- **Irrelevant Split** — source memory and target task belong to deliberately different reasoning subtypes.

If a memory strategy degrades performance on the Relevant Split, the question becomes whether this reflects a genuine memory failure or an artifact of the experimental infrastructure.

### 1.3 Scope

The long-term question behind this work — when does experience become reusable knowledge, and perhaps a lasting influence on later judgment — is too broad for a single course project. This project therefore cuts a narrower empirical slice: a near-transfer QA setting with a small model, a fixed experience budget, and a small number of controlled memory conditions.

The goal is not to produce a large-scale efficacy result. The goal is to build a measurement workflow that can separate genuine selective transfer from confounds introduced by coarse pairing, insensitive evaluation, or non-executable abstraction — and to identify which infrastructure components must be in place before any efficacy claim can be made.

### 1.4 Contribution

The contribution of Round 1 is threefold:

1. **An evaluation perspective.** The project evaluates Relevant and Irrelevant transfer separately rather than reporting only average gain.
2. **A reusable protocol.** Taxonomy, source-set construction, frozen pairing, role-aware case discipline, artifact review, and iterative single-variable diagnosis — a pipeline that makes each experimental decision traceable.
3. **A route-selection signal.** The results indicate whether future work should focus on memory *form* (how experience is represented), memory *use* (how experience is gated), or their coupling.

---

## 2. Method

### 2.1 Benchmark Setting

| Component | Specification |
|---|---|
| Source benchmark | HotpotQA (dev set) |
| Target benchmark | 2WikiMultiHopQA (dev set) |
| Transfer type | Near-transfer (multi-hop QA → multi-hop QA, different dataset) |
| Model | Qwen/Qwen3.5-9B, local inference via `transformers` |
| Source experience budget | N = 5 solved source tasks per memory set |
| Decoding | Greedy; `MAX_NEW_TOKENS = 1600` |

The choice of a 9B model was deliberate. The project is not optimizing for benchmark performance but for interpretable diagnostic behavior — a smaller model is more likely to reveal sensitivity to memory content.

### 2.2 Reasoning Taxonomy

We defined a small taxonomy of dominant reasoning patterns for multi-hop QA tasks:

| Label | Definition | Judgment cue |
|---|---|---|
| `bridge` | Answer requires chaining through an intermediate entity | "First find X, then through X find Y" |
| `comparison` | Answer requires retrieving attributes of two+ entities and comparing them | "Even with all facts, cannot answer without explicit comparison" |
| `temporal` | Answer depends on event ordering or time-interval reasoning | "Remove time info and the problem loses its main difficulty" |
| `distractor-heavy` | Main difficulty is filtering high-similarity irrelevant information | Last resort; only if none of the above dominate |

Each task receives exactly one dominant label. The taxonomy is frozen before any pairing or experiment begins [L2 §C2].

During Round 1d, we discovered that `bridge` was too coarse. It was further split into:

- **`attribute_bridge`** — chain through an intermediate entity to retrieve a property (e.g., venue → opening date).
- **`relation_chain_bridge`** — chain through kinship or relational operators (e.g., wife → brother).

This refinement became one of Round 1's central findings (see §3.3).

### 2.3 Source Sets and Pairing

Source memory is not treated as a generic retrieval pool. Instead, the project constructs explicit source sets of exactly N = 5 solved episodes from HotpotQA, each coherent by reasoning cluster. Sets satisfy: entity-disjoint within set, low lexical overlap, no answer leakage into target tasks.

| Source Set ID | Reasoning Cluster | Bridge Subtype |
|---|---|---|
| `hp_comparison_set_01` | comparison | — |
| `hp_bridge_set_01` | bridge | attribute_bridge |
| `hp_relation_chain_bridge_set_01` | bridge | relation_chain_bridge |

The third source set was constructed during the Round 1d–1f repair cycle after the subtype mismatch was discovered.

**Pairing rules.** Each target task is assigned a frozen Relevant and Irrelevant source set *before* any model runs. Pairing is never redefined from observed outcomes (experiment-contract §3). When pairing granularity was later found to be insufficient, the project preserved the old pairing and opened a new sub-round with corrected routing rather than editing completed runs [L2 §C3].

### 2.4 Memory Conditions

| Condition | Memory Content |
|---|---|
| **No Memory** | No `## Past Experience` block in prompt |
| **Episodic Trace** | Per-episode summaries of 5 solved source tasks: question, answer, key lookup path, reusable cue |
| **Cross-Episode Consolidation** | A single abstracted lesson synthesized across all 5 source episodes: shared structure, applicability criteria, operational heuristic, boundary/failure risks |

A fourth condition (Consolidation + Applicability Judgment) was defined in the proposal but intentionally deferred. Round 1 first focused on making the measurement workflow defensible before adding a gating mechanism.

Memory artifacts are generated from source sets and reviewed by hand before any experiment run (experiment-contract §4). Artifact files are versioned and archived [L2 §C3, §C4].

### 2.5 Prompt Scaffold and Observability

The initial pilot produced mostly single-line answers without visible reasoning. Round 1b introduced a structured scaffold:

```
## Context
{context_paragraphs}

## Question
{question}

## Past Experience                    ← only present in memory conditions
{memory_content}

## Instructions
- In ## Reasoning, write 3–6 short bullet points grounded in the provided context.
- If past experience is shown, either use it explicitly or state briefly why it is not useful here.
- In ## Final Answer, give only the final short answer phrase.

## Reasoning

## Final Answer
```

The answer extractor reads only from `## Final Answer`. This scaffold is fixed from Round 1b onward; subsequent sub-rounds do not modify it.

### 2.6 Metrics

**Outcome metrics:** Exact Match (EM) and token-level F1.

**Process metrics** (recorded per run, extracted from model output):

| Metric | Definition |
|---|---|
| `parse_success` | Whether the answer extractor succeeded |
| `reasoning_present` | Whether `## Reasoning` section exists |
| `final_answer_present` | Whether `## Final Answer` section exists |
| `memory_reference_type` | `explicit_use` / `explicit_reject` / `implicit_or_none` |

**Reporting rule:** Relevant Split and Irrelevant Split are always reported separately. No mixed average is computed (experiment-contract §6).

### 2.7 Methodological Commitments

Three protocol-level commitments emerged during Round 1 and became central to the method:

1. **Case-role discipline.** Cases must be classified as `process sanity`, `diagnostic`, or `boundary` before any summary table is trusted. Mixed-role aggregation is banned.
2. **Subtype-aware pairing.** A coarse label such as `bridge` is not enough if the target depends on a more specific subtype. Relevance must be defined at the subtype level.
3. **Executable abstraction.** For consolidation-style memory, topical relevance is insufficient unless the artifact preserves operator structure in an executable form.

These are not implementation details. They are part of the experimental method itself.

> The protocol is part of the result, not merely a preprocessing detail.

### 2.8 Iterative Diagnosis Protocol

Round 1 follows a strict single-variable iterative protocol. Each sub-round changes exactly one variable while holding all others fixed. If a sub-round reveals a confound, the confound is repaired in a new sub-round rather than retroactively adjusting already-completed runs. This makes the causal chain traceable: any observed change in behavior can be attributed to the single variable that was modified [L1 §2].

### 2.9 Scale and Scope

Round 1 is a pilot. It operates on 6 smoke cases (Round 1b: 36 runs) and 2 rerouted relation-chain targets (Round 1g: 10 runs; Round 1i: 4 runs). The goal is not statistical power but diagnostic clarity: determining whether the setup can produce interpretable selective-transfer signals, and identifying which infrastructure components need repair before scaling.

---

## 3. Results

Round 1 is best interpreted as a **repair chain**, not as a single benchmark comparison. The results below trace how each controlled repair changed the interpretation of early evidence.

### 3.1 Stage I: Making the Experiment Observable

Round 1b's structured scaffold made memory behavior visible for the first time:

| Process Metric | Round 1b Value |
|---|---|
| Total runs | 36 (6 targets × 3 conditions × 2 splits) |
| `parse_success` | 36 / 36 |
| `reasoning_present` | 36 / 36 |
| `final_answer_present` | 36 / 36 |
| `memory_reference_type = explicit_use` | 3 / 24 memory runs |
| `memory_reference_type = explicit_reject` | 2 / 24 memory runs |

This was especially clear on the process-sanity case `wiki_dev_8896`, where the model explicitly used relevant episodic memory and explicitly rejected irrelevant episodic memory — while the outcome (EM = 1) remained unchanged in both conditions [L3 Exhibit B]. This did not yet establish transfer efficacy, but it established that **process-level selectivity was observable**.

Round 1c then showed that the six smoke cases could not be pooled into a single mini-benchmark. Once cases were reassigned into three experimental roles, mixed-role averages lost their interpretive value:

| Role | Cases | Outcome Changed | Improved | Degraded |
|---|---|---|---|---|
| Process sanity | wiki_dev_8896, wiki_dev_10727 | 0 | 0 | 0 |
| Diagnostic | wiki_dev_2639, wiki_dev_7019 | 7 | 2 | 5 |
| Audit / Boundary | wiki_dev_0092, wiki_dev_6083 | 0 | 0 | 0 |

If all 6 cases were averaged into a single EM, the 7 outcome changes in the diagnostic bucket would be diluted by 12 unchanged runs from the other two. More critically, `wiki_dev_7019`'s apparent improvement (answer-format compression toward gold) would be pooled with `wiki_dev_2639`'s apparent degradation (artifact-induced derailment), producing a near-zero average that masks both phenomena [L3 Exhibit C].

*Evidence: [L2 §C1] → result CSV, raw outputs for wiki_dev_8896. [L2 §C2] → role classification CSV, aggregate overview CSV.*

### 3.2 Stage II: Repairing Pairing Granularity

The most important early negative result came from `wiki_dev_2639`. The Round 1b aggregate for relevant memory appeared unfavorable:

| Split | Condition | EM |
|---|---|---|
| relevant | no_memory | 0.50 |
| relevant | episodic_trace | 0.33 |
| relevant | cross_episode_consolidation | 0.33 |

The no-memory baseline on `wiki_dev_2639` answered correctly (`Henry Pelham`), but both relevant memory conditions produced refusal (`Cannot be determined from the provided context`). At first glance, this looked like strong evidence that relevant memory could hurt.

Round 1d showed that this interpretation was too quick. `wiki_dev_2639` is a **relation-chain bridge** task — it requires traversing `wife → husband → brother` to answer "Who is the sibling-in-law of Harriet Pelham-Holles?" But the relevant source set (`hp_bridge_set_01`) contained **attribute-bridge** episodes (venue → opening date, event → designation). The "relevant" label was structurally misleading: the source and target shared the coarse `bridge` cluster but belonged to different subtypes.

After subtype-aware source expansion and rerouting, Round 1g reran only the affected targets, changing only the source routing while holding all other variables fixed:

| Condition | Source Set | EM | Pred |
|---|---|---|---|
| no_memory | — | 1 | Henry Pelham |
| episodic_trace + relevant | hp_relation_chain_bridge_set_01 | **1** | Henry Pelham |
| episodic_trace + irrelevant | hp_bridge_set_01 | 0 | Cannot be determined |
| consolidation + relevant | hp_relation_chain_bridge_set_01 | 0 | *(still fails)* |
| consolidation + irrelevant | hp_bridge_set_01 | 0 | Cannot be determined |

The subtype-aware reroute repaired relevant episodic trace from wrong to correct. The irrelevant condition remained wrong, confirming the repair was selective. The earlier episodic failure was not evidence that relevant memory was intrinsically harmful — it was a **false negative created by coarse pairing granularity** [L3 Exhibit A, Conditions 2→3].

However, Cross-Episode Consolidation still failed on the same target. This shifted the bottleneck from pairing to the memory-form layer.

*Evidence: [L2 §C3] → Round 1b raw output (before), Round 1g raw output (after), artifact comparison.*

### 3.3 Stage III: Repairing Operator-Level Abstraction

Subtype-aware rerouting repaired episodic memory, but relevant consolidation still failed on `wiki_dev_2639`. The remaining problem was no longer subtype mismatch — it was operator interpretation.

Two further sub-rounds isolated the cause:

- **Round 1h** fixed formatting and branch-wording issues in the consolidation artifact. Output structure stabilized, but the answer remained wrong (`Cannot be determined`). The failure was narrowed to **kinship-operator interpretation**: the heuristic left `sibling-in-law` as a vague natural-language label.

- **Round 1i** rewrote only the operator-level guidance — decomposing `sibling-in-law` into two explicit candidate paths (`spouse_of → sibling` and `sibling → spouse_of`) and prohibiting default parent/grandparent substitutions:

| Condition | EM | Pred | Memory Ref |
|---|---|---|---|
| no_memory | 1 | Henry Pelham | — |
| Round 1h revised relevant consolidation | 0 | Cannot be determined | implicit_or_none |
| **Round 1i operator-repaired relevant consolidation** | **1** | **Henry Pelham** | **explicit_use** |
| irrelevant consolidation | 0 | Cannot be determined | implicit_or_none |

The operator repair recovered relevant consolidation from wrong to correct. The irrelevant consolidation remained wrong. Same model, same target, same scaffold, same scoring — only the operator-level abstraction changed [L3 Exhibit A, Conditions 5→6].

This result is stronger than a generic "prompt refinement helps" claim. It shows that relevant abstract memory can still fail if its abstraction is not executable enough for the target operator structure.

**Process-level observation.** The repaired consolidation reasoning contains ~20 lines of self-correction before converging on the correct answer. The repaired episodic trace answers in 4 clean bullets. Consolidation carries higher process-level cost even when the outcome is correct [L3 Exhibit A, Condition 6].

*Evidence: [L2 §C4] → Round 1h raw output (pre-repair), Round 1i raw output (post-repair), repair protocol, artifact versions.*

### 3.4 The Full Repair Chain

`wiki_dev_2639` is the single most informative case in Round 1. It supports a full before/after interpretation shift: the no-memory baseline is correct, relevant memory initially degrades, subtype-aware rerouting repairs episodic trace, operator-aware repair repairs consolidation, and irrelevant memory remains wrong throughout.

| Stage | No Mem. | Epis. (rel.) | Epis. (irrel.) | Consol. (rel.) | Consol. (irrel.) |
|---|---|---|---|---|---|
| 1b — coarse pairing | ✓ | ✗ | ✗ | ✗ | ✓ |
| 1g — subtype reroute | ✓ | **✓** | ✗ | ✗ | ✗ |
| 1i — operator repair | ✓ | ✓ | ✗ | **✓** | ✗ |

Three properties are visible:

1. **Relevant memory was recoverable on both memory forms** — once the correct infrastructure was in place.
2. **Irrelevant memory remained consistently harmful** — confirming the repairs were selective, not generic.
3. **Episodic and consolidation required different layers of repair** — subtype-aware routing sufficed for episodic; consolidation additionally required executable operator guidance.

This single case does not prove broad generalization. But it is enough to show that early "relevant memory hurts" evidence was not stable under protocol repair.

*Evidence: [L2 §C5] → patchback summary, patchback CSV. [L3 Exhibit A] → full 7-condition table with reasoning excerpts.*

### 3.5 Retained Failure Cases

Per experiment-contract §8, we retain failure cases alongside successes.

**F1: Irrelevant consolidation on `wiki_dev_2639`.** After all repairs, irrelevant consolidation still produces `Cannot be determined`. The attribute-bridge consolidation provides generic entity-chaining heuristics with no kinship-chain guidance. The model falls into the Godolphin-sibling dead end — searching Harriet's blood family instead of traversing `husband → brother` [L3 Exhibit A, Condition 7].

**F2: `wiki_dev_6083` (scoring boundary).** All conditions produce `Spain` while the gold answer is `Spanish`. The scoring boundary dominates any possible memory effect. This case was excluded from all transfer analyses [L2 §F2].

---

## 4. Discussion

At the start of Round 1, one plausible interpretation of the data was:

> relevant memory can hurt an otherwise correct baseline.

By the end of Round 1, that interpretation could no longer be defended on the strongest diagnostic case. Once the experiment repaired observability, case-role discipline, subtype-level pairing, and operator-level abstraction, the earlier negative interpretation was overturned. The most important outcome is therefore methodological rather than purely empirical.

### 4.1 What Round 1 Established

Round 1 built and validated a diagnostic workflow for evaluating memory selective transfer. The workflow comprises:

1. A structured prompt scaffold that makes memory use/reject visible in model reasoning.
2. A role-aware case analysis that prevents misleading mixed aggregates.
3. A subtype-aware pairing protocol that operates at the reasoning-pattern subtype level, not the coarse cluster level.
4. An iterative single-variable diagnosis protocol that makes each repair step causally traceable.

These four components are infrastructure — they are prerequisites for any subsequent efficacy study, not efficacy results themselves.

### 4.2 Claims

Building on this infrastructure, Round 1 supports five empirical claims:

**C1: Process-level selectivity is real.** The structured scaffold reveals explicit memory use and explicit memory rejection in model reasoning, even when the final answer does not change (§3.1, [L3 Exhibit B]).

**C2: Mixed-role aggregate is misleading.** Pooling process-sanity, diagnostic, and boundary cases into a single average obscures qualitatively different phenomena (§3.2, [L3 Exhibit C]).

**C3: Pairing granularity is part of the result.** Coarse `bridge` pairing created false negative-transfer evidence on the strongest diagnostic case. Subtype-aware rerouting repaired the relevant episodic trace (§3.3, [L3 Exhibit A, Conditions 2→3]).

**C4: Abstract memory must be executable, not merely relevant.** Even with correct subtype matching, consolidation failed until relation operators were encoded as executable checking rules (§3.4, [L3 Exhibit A, Conditions 5→6]).

**C5: Seemingly negative transfer evidence can be fully overturned.** The same case that initially appeared to show "relevant memory hurts" was recovered on both memory forms after pairing repair and operator-level abstraction (§3.5).

### 4.3 Non-Claims

Round 1 does **not** justify the following:

**N1: Strong average benchmark gain from memory.** Round 1 operated on ≤ 6 smoke cases; no large-scale aggregate was computed or intended.

**N2: Universal superiority of either memory form.** Episodic trace was repaired by subtype routing alone; consolidation required additional operator-level repair. One diagnostic case cannot establish a general ranking.

**N3: Selective transfer demonstrated at scale.** The project established the measurement workflow, not a broad empirical result.

**N4: Broad generalization from one repaired case.** `wiki_dev_2639` is a proof of concept for the diagnosis-and-repair methodology, not statistical evidence.

**N5: Sufficiency of the current model.** The 9B model shows residual process-level hesitation even in the repaired consolidation output [L3 Exhibit A, Condition 6].

These boundaries are deliberate. They are part of the project's experimental discipline.

### 4.4 Theoretical Implication

Beyond methodology, Round 1 carries a substantive implication for how memory selective transfer should be conceptualized.

The project started from a broader question: *when does experience become reusable knowledge rather than a stored trace?* Round 1 does not answer that large question directly. But it supports one narrower and useful theoretical claim: **relevance alone is not enough.**

The standard framing asks: *is the source experience relevant to the target?* Round 1 suggests this question is necessary but insufficient. Two additional conditions must hold:

1. **Relevance must be operationalized at the right granularity.** A coarse `bridge` label is not the same as a subtype-specific `relation_chain_bridge` match. If the granularity is wrong, even genuinely relevant experience produces harmful behavior — not because the memory is bad, but because the relevance label is misleading.

2. **Abstract memory must preserve operator structure.** For consolidation-style memory, it is not enough to summarize *what* relation holds between entities; the memory must encode *how* to verify that relation. Decomposing `sibling-in-law` into explicit candidate paths (`spouse_of → sibling` vs. `sibling → spouse_of`) was the difference between failure and success — same model, same target, same context.

Together, these conditions suggest that the boundary between useful and harmful memory is not determined by topic-level relevance alone. It also depends on whether the memory representation preserves the **operator structure** required by the target task.

---

## 5. Limitations

**Scale.** The strongest repaired evidence comes from a single diagnostic case (`wiki_dev_2639`). The remaining cases served as process-sanity checks or were too easy (ceiling) to provide sensitivity. Any generalization beyond this case is tentative.

**Model capacity.** All runs used Qwen/Qwen3.5-9B. A larger model might resolve some operator-level failures without explicit repair, collapsing the episodic–consolidation distinction observed here. This was not tested.

**Outcome vs. process purity.** The operator-repaired consolidation produces the correct answer, but its reasoning chain contains extended self-correction (~20 lines of hedging before convergence). The repair is outcome-level complete but process-level imperfect. Whether process-level purity matters for downstream reliability remains an open question.

**Applicability Judgment not tested.** The fourth planned condition (Consolidation + Applicability Judgment) was deferred. It is possible that a gating mechanism would have surfaced selective-transfer signals more directly without requiring the pairing and operator repairs that dominated Round 1.

---

## 6. Future Work

Round 1 identifies three natural next steps, ordered by priority:

1. **Repaired evaluation at moderate scale.** Apply the corrected pairing and operator-aware artifacts to a larger target set (20–40 cases) to test whether the patterns observed on `wiki_dev_2639` generalize across relation-chain bridge tasks.

2. **Applicability Judgment condition.** Introduce the gating mechanism and compare whether it can achieve selective transfer without requiring the fine-grained pairing that Round 1 found necessary.

3. **Model scaling.** Repeat the key diagnostic comparisons with a larger model (e.g., 32B–70B) to determine whether the episodic–consolidation gap and the operator-level sensitivity persist at higher capacity.

The next round should ask a much cleaner question than reopening average-gain comparisons:

> Does the repaired workflow generalize beyond the strongest diagnostic case?

---

## 7. Conclusion

Round 1 should be read as a **measurement and interpretation success**, not as a benchmark-win story. Its central contribution is this:

> Apparent negative transfer can be produced by coarse pairing and non-executable abstraction, and a controlled repair chain can overturn that interpretation without changing the underlying model.

This does not prove that memory broadly works. It shows something more foundational: **selective-transfer evaluation is only meaningful when pairing granularity, case-role discipline, and executable memory abstraction are treated as first-class methodological variables.** Without these, the experiment measures its own artifacts rather than the phenomenon of interest.

The project's value lies in showing that apparent negative transfer may be an artifact of experimental granularity, that abstract memory fails when it is not executable enough, and that careful single-variable repair can reverse an incorrect conclusion without changing the model itself. This provides a more defensible protocol for asking when memory is genuinely reusable — and when it is merely present.

---

## References

### Internal Supporting Materials

| Layer | File | Role |
|---|---|---|
| L1 | [final-report-round1-section-v2.md](./final-report-round1-section-v2.md) | Main Round 1 narrative with sub-round summary table |
| L2 | [round1-evidence-map.md](./round1-evidence-map.md) | Claim-to-evidence traceability: progress report → CSV → raw output → artifact |
| L3 | [round1-case-appendix.md](./round1-case-appendix.md) | Before/after raw evidence for key diagnostic cases |

### Experimental Infrastructure

| Document | Role |
|---|---|
| [experiment-contract.md](../design/experiment-contract.md) | 13 rules governing single-variable protocol, frozen pairing, traceability |
| [protocol/pipeline.md](../protocol/pipeline.md) | 8-phase experimental pipeline |
| [protocol/taxonomy_guideline.md](../protocol/taxonomy_guideline.md) | Reasoning taxonomy definitions and annotation rules |
