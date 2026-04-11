# Method / Results / Discussion — Round 1

> **Traceability convention.** Every quantitative claim in this section can be traced through three layers:
> - **L1 Narrative:** [final-report-round1-section-v2.md](./final-report-round1-section-v2.md)
> - **L2 Evidence Map:** [round1-evidence-map.md](./round1-evidence-map.md)
> - **L3 Case Appendix:** [round1-case-appendix.md](./round1-case-appendix.md)
>
> Inline references use the format `[L2 §C3]` or `[L3 Exhibit A]` to point into the appropriate layer.

---

# 1. Method

## 1.1 Task Framing

This project does not evaluate memory by asking whether memory increases average benchmark performance. Instead, it studies **selective transfer**:

> Under a fixed experience budget, does a memory mechanism help on structurally matched target tasks while avoiding harm on mismatched target tasks?

To operationalize this, we define two controlled splits for every target task:

- **Relevant Split** — source memory and target task share the same reasoning subtype.
- **Irrelevant Split** — source memory and target task belong to deliberately different reasoning subtypes.

If a memory strategy supports selective transfer, it should improve (or at least not degrade) performance on the Relevant Split while avoiding negative transfer on the Irrelevant Split. If it degrades performance on the Relevant Split, the question becomes whether this reflects a genuine memory failure or an artifact of the experimental infrastructure.

The goal of the experiment is therefore methodological as well as empirical. We aim to distinguish genuine memory effects from artifacts introduced by coarse pairing, insensitive evaluation, or non-executable memory abstractions.

## 1.2 Benchmark Setting

| Component | Specification |
|---|---|
| Source benchmark | HotpotQA (dev set) |
| Target benchmark | 2WikiMultiHopQA (dev set) |
| Transfer type | Near-transfer (multi-hop QA → multi-hop QA, different dataset) |
| Model | Qwen/Qwen3.5-9B, local inference via `transformers` |
| Source experience budget | N = 5 solved source tasks per memory set |
| Decoding | Greedy; `MAX_NEW_TOKENS = 1600` |

The choice of a relatively small model (9B) was deliberate. The project is not optimizing for benchmark performance but for observable diagnostic behavior — a smaller model is more likely to reveal sensitivity to memory content.

## 1.3 Reasoning Taxonomy

We defined a small taxonomy of dominant reasoning patterns for multi-hop QA tasks:

| Label | Definition | Judgment cue |
|---|---|---|
| `bridge` | Answer requires chaining through an intermediate entity | "First find X, then through X find Y" |
| `comparison` | Answer requires retrieving attributes of two+ entities and comparing them | "Even with all facts, cannot answer without explicit comparison" |
| `temporal` | Answer depends on event ordering or time-interval reasoning | "Remove time info and the problem loses its main difficulty" |
| `distractor-heavy` | Main difficulty is filtering high-similarity irrelevant information | Last resort; only if none of the above dominate |

Each task receives exactly one dominant label. Tasks without a clear dominant pattern are dropped from the pairing pool. The taxonomy is frozen before any pairing or experiment begins [L2 §C2: role classification CSV].

During Round 1d, we discovered that `bridge` was too coarse. It was further split into:

- **`attribute_bridge`** — chain through an intermediate entity to retrieve a property (e.g., venue → opening date).
- **`relation_chain_bridge`** — chain through kinship or relational operators (e.g., wife → brother).

This refinement became one of Round 1's central findings (see Results §2.3).

## 1.4 Source Set Construction and Pairing Protocol

**Source sets.** From HotpotQA, we constructed source memory sets of N = 5 tasks each, all from the same reasoning cluster. Sets satisfy: entity-disjoint within set, low lexical overlap, no answer leakage into target tasks.

Two source sets were used in the initial pilot:

| Source Set ID | Reasoning Cluster | Bridge Subtype |
|---|---|---|
| `hp_comparison_set_01` | comparison | — |
| `hp_bridge_set_01` | bridge | attribute_bridge |

A third source set was constructed during the Round 1d–1f repair cycle:

| Source Set ID | Reasoning Cluster | Bridge Subtype |
|---|---|---|
| `hp_relation_chain_bridge_set_01` | bridge | relation_chain_bridge |

**Pairing rules.** Each target task is bound to a fixed relevant source set and a fixed irrelevant source set *before* any model runs. Pairing is frozen and archived; it is never adjusted based on observed results (experiment-contract §3). When pairing granularity was found to be insufficient, the old pairing was preserved as-is and a new sub-round with corrected routing was opened [L2 §C3: round spec].

## 1.5 Memory Conditions

Three memory conditions are compared in Round 1:

| Condition | Memory Content |
|---|---|
| **No Memory** | No `## Past Experience` block in prompt |
| **Episodic Trace** | Per-episode summaries of 5 solved source tasks: question, answer, key lookup path, reusable cue |
| **Cross-Episode Consolidation** | A single abstracted lesson synthesized across all 5 source episodes: shared structure, applicability criteria, operational heuristic, boundary/failure risks |

A fourth condition (Consolidation + Applicability Judgment) was defined in the proposal but not included in Round 1, which focused on establishing the measurement workflow before adding a gating mechanism.

Memory artifacts are generated from source sets and reviewed by hand before any experiment run (experiment-contract §4). Artifact files are versioned and archived [L2 §C3, §C4: artifact links].

## 1.6 Evaluation Protocol

### 1.6.1 Prompt Scaffold and Observability

The initial pilot (Round 1) produced mostly single-line answers without visible reasoning. Round 1b introduced a structured scaffold to make the experiment observable:

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

### 1.6.2 Metrics

**Outcome metrics:**
- Exact Match (EM)
- Token-level F1

**Process metrics** (recorded per run, extracted from model output):
- `reasoning_present` — whether `## Reasoning` section exists
- `final_answer_present` — whether `## Final Answer` section exists
- `memory_reference_type` — `explicit_use` / `explicit_reject` / `implicit_or_none`
- `parse_success` — whether the answer extractor succeeded

**Reporting rule:** Relevant Split and Irrelevant Split are always reported separately. No mixed average is computed (experiment-contract §6).

### 1.6.3 Why Naive Aggregate Was Rejected

The initial smoke subset showed that a flat average over all target cases was misleading. Different cases served different methodological roles — some were useful only as **process sanity** checks, some were true **diagnostic** cases, and some were **audit / boundary** cases dominated by scoring or format effects.

After Round 1c, mixed-role aggregation was explicitly banned. Every case must be classified into its experimental role before entering any summary table.

### 1.6.4 Pairing Granularity as a First-Class Variable

The original `bridge` cluster was later found to be too coarse. The experiment had conflated `attribute_bridge` and `relation_chain_bridge`, meaning a coarse-grained "relevant" label could still be structurally mismatched at the subtype level. Round 1d–1g therefore redefined relevance at the subtype level and rerouted the most important diagnostic case to a subtype-matched source set.

### 1.6.5 Executable Abstraction Requirement

For `Cross-Episode Consolidation`, topical relevance alone was insufficient. The memory artifact also had to preserve the target task's **operator structure** in an executable form.

This distinction became crucial for relation-chain cases involving kinship operators such as `sibling-in-law`. A natural-language summary of the relation pattern was not enough; the memory artifact had to encode candidate operator branches explicitly enough for the model to execute them.

## 1.7 Controlled Repair Strategy

Round 1 was not a single run but a sequence of tightly controlled sub-rounds. Each sub-round changes exactly one variable while holding all others fixed:

- prompt scaffold
- case-role discipline
- pairing granularity
- source-side subtype feasibility
- routing
- consolidation formatting
- kinship-operator execution
- final patchback synthesis

This design is central to the method. The project is not claiming that memory "worked" after arbitrary iterative tuning. It is claiming that each suspected confound was isolated, repaired, and traced forward to its effect on interpretation. If a sub-round reveals a confound (e.g., coarse pairing), the confound is repaired in a new sub-round rather than retroactively adjusting already-completed runs. This makes the causal chain traceable: any observed change in behavior can be attributed to the single variable that was modified.

The full sub-round sequence is documented in [L1 §2: Experimental Path] and [L1 Sub-Round Summary Table].

## 1.8 Scale and Scope

Round 1 is a pilot. It operates on 6 smoke cases (Round 1b: 36 runs) and 2 rerouted relation-chain targets (Round 1g: 10 runs; Round 1i: 4 runs). The goal is not statistical power but diagnostic clarity: determining whether the setup can produce interpretable selective-transfer signals, and identifying which infrastructure components need repair before scaling.

## 1.9 What the Method Establishes

The methodological contribution of Round 1 is the following protocol claim:

- selective-transfer evaluation requires pre-frozen pairing
- case roles must be assigned before aggregation
- relevance must be defined at the right structural granularity
- consolidation artifacts must preserve executable operator structure

Without these constraints, the experiment risks measuring its own setup artifacts rather than the phenomenon of interest.

---

# 2. Results

## 2.1 Stage I: Making the Experiment Observable

The initial pilot produced mostly single-line answers with no visible reasoning. Round 1b's structured scaffold resolved this completely:

| Process Metric | Round 1b Value |
|---|---|
| Total runs | 36 (6 targets × 3 conditions × 2 splits) |
| `parse_success` | 36 / 36 |
| `reasoning_present` | 36 / 36 |
| `final_answer_present` | 36 / 36 |
| `memory_reference_type = explicit_use` | 3 / 24 memory runs |
| `memory_reference_type = explicit_reject` | 2 / 24 memory runs |

For the first time, memory interaction became visible in model outputs. On the process-sanity case `wiki_dev_8896`, the model explicitly used relevant episodic memory and explicitly rejected irrelevant episodic memory — while the outcome (EM = 1) remained unchanged in both conditions [L3 Exhibit B]. This demonstrates that the scaffold enables **process-level selectivity observation** even when the outcome is insensitive.

Round 1c then showed that the six smoke cases could not be treated as a single mini-benchmark. Once cases were reassigned into `process sanity`, `diagnostic`, and `boundary` roles, the mixed aggregate lost its authority as a summary statistic:

| Role | Cases | Outcome Changed | Improved | Degraded |
|---|---|---|---|---|
| Process sanity | wiki_dev_8896, wiki_dev_10727 | 0 | 0 | 0 |
| Diagnostic | wiki_dev_2639, wiki_dev_7019 | 7 | 2 | 5 |
| Audit / Boundary | wiki_dev_0092, wiki_dev_6083 | 0 | 0 | 0 |

If all 6 cases were averaged into a single EM, the 7 outcome changes in the diagnostic bucket would be diluted by 12 unchanged runs from the other two buckets. More critically, `wiki_dev_7019`'s apparent improvement (answer-format compression toward gold) would be pooled with `wiki_dev_2639`'s apparent degradation (artifact-induced derailment), producing a near-zero average that masks both phenomena [L3 Exhibit C].

*Evidence: [L2 §C1] → result CSV, raw outputs for wiki_dev_8896. [L2 §C2] → role classification CSV, aggregate overview CSV.*

## 2.2 Stage II: Repairing Pairing Granularity

The Round 1b aggregate for relevant memory appeared unfavorable:

| Split | Condition | EM |
|---|---|---|
| relevant | no_memory | 0.50 |
| relevant | episodic_trace | 0.33 |
| relevant | cross_episode_consolidation | 0.33 |

The most visible degradation was on `wiki_dev_2639`: the no-memory baseline answered correctly (`Henry Pelham`), but both relevant memory conditions produced refusal (`Cannot be determined from the provided context`).

Round 1d diagnosed the cause. `wiki_dev_2639` is a **relation-chain bridge** task — it requires traversing `wife → husband → brother` to answer "Who is the sibling-in-law of Harriet Pelham-Holles?" But the relevant source set (`hp_bridge_set_01`) contained **attribute-bridge** episodes (venue → opening date, event → designation). The "relevant" label was structurally misleading: the source and target shared the coarse `bridge` cluster but belonged to different subtypes.

Round 1g tested this diagnosis by rerouting `wiki_dev_2639` to a newly constructed `relation_chain_bridge` source set, changing only the source routing while holding all other variables fixed:

| Condition | Source Set | EM | Pred |
|---|---|---|---|
| no_memory | — | 1 | Henry Pelham |
| episodic_trace + relevant | hp_relation_chain_bridge_set_01 | **1** | Henry Pelham |
| episodic_trace + irrelevant | hp_bridge_set_01 | 0 | Cannot be determined |
| consolidation + relevant | hp_relation_chain_bridge_set_01 | 0 | *(format failure)* |
| consolidation + irrelevant | hp_bridge_set_01 | 0 | Cannot be determined |

The subtype-aware reroute repaired relevant episodic trace from wrong to correct. The irrelevant condition remained wrong, confirming the repair was selective. The earlier "relevant memory hurts" interpretation was a **false negative created by coarse pairing granularity** [L3 Exhibit A, Conditions 2→3].

At this point, however, `Cross-Episode Consolidation` still failed on the same target. This shifted the bottleneck from pairing to the memory-form layer.

*Evidence: [L2 §C3] → Round 1b raw output (before), Round 1g raw output (after), artifact comparison.*

## 2.3 Stage III: Repairing Operator-Level Abstraction

Subtype-aware rerouting did not automatically repair consolidation. Round 1g's relevant consolidation on `wiki_dev_2639` still failed, despite using the correctly matched source set. The failure mode shifted: the model now explicitly referenced the memory but could not resolve the kinship operator `sibling-in-law`.

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

**Process-level observation.** The repaired consolidation reasoning contains ~20 lines of self-correction before converging on the correct answer. By contrast, the repaired episodic trace answers in 4 clean bullets. This suggests that consolidation carries higher process-level cost even when the outcome is correct [L3 Exhibit A, Condition 6 note on process impurity].

*Evidence: [L2 §C4] → Round 1h raw output (pre-repair), Round 1i raw output (post-repair), repair protocol, artifact versions.*

## 2.4 The Key Diagnostic Case

`wiki_dev_2639` is the single most informative case in the project. It is valuable because it simultaneously satisfies all conditions for a full before/after interpretation shift:

- the no-memory baseline is correct
- relevant memory initially degrades
- subtype-aware rerouting repairs episodic memory
- operator-aware repair repairs consolidation
- irrelevant memory remains wrong throughout

Combining §2.2 and §2.3, the evidence evolution on this case is:

| Stage | No Mem. | Epis. (rel.) | Epis. (irrel.) | Consol. (rel.) | Consol. (irrel.) |
|---|---|---|---|---|---|
| 1b — coarse pairing | ✓ | ✗ | ✗ | ✗ | ✓ |
| 1g — subtype reroute | ✓ | **✓** | ✗ | ✗ | ✗ |
| 1i — operator repair | ✓ | ✓ | ✗ | **✓** | ✗ |

Three properties are visible:

1. **Relevant memory was recoverable on both memory forms** — once the correct infrastructure was in place.
2. **Irrelevant memory remained consistently harmful** — confirming the repairs were selective, not generic.
3. **Episodic and consolidation required different layers of repair** — subtype-aware routing sufficed for episodic; consolidation additionally required executable operator guidance.

The detailed reasoning traces for all seven conditions on this case are documented in [L3 Exhibit A].

*Evidence: [L2 §C5] → patchback summary, patchback CSV.*

## 2.5 Retained Failure Cases

Per experiment-contract §8, we retain failure cases alongside successes.

**F1: Irrelevant consolidation on `wiki_dev_2639`.** After all repairs, irrelevant consolidation still produces `Cannot be determined`. The attribute-bridge consolidation provides generic entity-chaining heuristics with no kinship-chain guidance. The model falls into the Godolphin-sibling dead end — searching Harriet's blood family instead of traversing `husband → brother` [L3 Exhibit A, Condition 7].

**F2: `wiki_dev_6083` (scoring boundary).** All conditions produce `Spain` while the gold answer is `Spanish`. The scoring boundary dominates any possible memory effect. This case was excluded from all transfer analyses and retained only as an audit case [L2 §F2].

## 2.6 What Round 1 Actually Shows

The most important outcome of Round 1 is not "memory improves performance." The real result is a methodological correction:

> Evidence that initially looked like relevant negative transfer was not stable under protocol repair.

Once the experiment repaired observability, case-role discipline, subtype-level pairing, and operator-level abstraction, the strongest early negative example no longer supported the original negative interpretation. This means the project's main contribution is not a broad efficacy claim. It is a demonstration that **selective-transfer evaluation is highly sensitive to how relevance and abstraction are operationalized**.

---

# 3. Discussion

## 3.1 What Round 1 Established

Round 1's primary contribution is **methodological**: it built and validated a diagnostic workflow for evaluating memory selective transfer. The workflow comprises:

1. A structured prompt scaffold that makes memory use/reject visible in model reasoning.
2. A role-aware case analysis that prevents misleading mixed aggregates.
3. A subtype-aware pairing protocol that operates at the reasoning-pattern subtype level, not the coarse cluster level.
4. An iterative single-variable diagnosis protocol that makes each repair step causally traceable.

These four components are infrastructure — they are prerequisites for any subsequent efficacy study, not efficacy results themselves.

## 3.2 Claims

Building on this infrastructure, Round 1 supports five empirical claims. Each is stated with its evidence chain; full traceability is provided in [L2].

**C1: Process-level selectivity is real.** The structured scaffold reveals explicit memory use and explicit memory rejection in model reasoning, even when the final answer does not change (§2.1, [L3 Exhibit B]).

**C2: Mixed-role aggregate is misleading.** Pooling process-sanity, diagnostic, and boundary cases into a single average obscures qualitatively different phenomena (§2.1, [L3 Exhibit C]).

**C3: Pairing granularity is part of the result.** Coarse `bridge` pairing created false negative-transfer evidence on the strongest diagnostic case. Subtype-aware rerouting repaired the relevant episodic trace (§2.2, [L3 Exhibit A, Conditions 2→3]).

**C4: Abstract memory must be executable, not merely relevant.** Even with correct subtype matching, consolidation failed until relation operators were encoded as executable checking rules (§2.3, [L3 Exhibit A, Conditions 5→6]).

**C5: Seemingly negative transfer evidence can be fully overturned.** The same case that initially appeared to show "relevant memory hurts" was recovered on both memory forms after pairing repair and operator-level abstraction (§2.4).

## 3.3 Non-Claims

Round 1 does **not** justify the following:

**N1: Strong average benchmark gain from memory.** Round 1 operated on ≤ 6 smoke cases; no large-scale aggregate was computed or intended.

**N2: Universal superiority of either memory form.** Episodic trace was repaired by subtype routing alone; consolidation required additional operator-level repair. One diagnostic case cannot establish a general ranking.

**N3: Selective transfer demonstrated at scale.** The project established the measurement workflow, not a broad empirical result.

**N4: Broad generalization from one repaired case.** `wiki_dev_2639` is a proof of concept for the diagnosis-and-repair methodology, not statistical evidence.

**N5: Sufficiency of the current model.** The 9B model shows residual process-level hesitation even in the repaired consolidation output [L3 Exhibit A, Condition 6].

## 3.4 Why This Matters Theoretically

Beyond methodology, Round 1 carries a substantive implication for how memory selective transfer should be conceptualized.

The project started from a broader long-term question: *when does experience become reusable knowledge rather than a stored trace?* Round 1 does not answer that large question directly. But it supports one narrower and useful theoretical implication: **relevance alone is not enough.**

The standard framing asks: *is the source experience relevant to the target?* Round 1 suggests this question is necessary but insufficient. Two additional conditions must hold:

1. **Relevance must be operationalized at the right granularity.** A coarse `bridge` label is not the same as a subtype-specific `relation_chain_bridge` match. If the granularity is wrong, even genuinely relevant experience produces harmful behavior — not because the memory is bad, but because the relevance label is misleading.

2. **Abstract memory must preserve operator structure.** For consolidation-style memory, it is not enough to summarize *what* relation holds between entities; the memory must encode *how* to verify that relation. In our case, decomposing `sibling-in-law` into explicit candidate paths (`spouse_of → sibling` vs. `sibling → spouse_of`) was the difference between failure and success — using the same model, same target, same context.

Together, these conditions suggest that the boundary between useful and harmful memory is not determined by topic-level relevance alone. It also depends on whether the memory representation preserves the **operator structure** required by the target task. This connects to the broader question motivating this project: when does past experience become reusable knowledge, rather than inert record or misleading bias?

## 3.5 Limitations

**Scale.** The strongest repaired evidence comes from a single diagnostic case (`wiki_dev_2639`). The remaining cases served as process-sanity checks or were too easy (ceiling) to provide sensitivity. Any generalization beyond this case is tentative.

**Model capacity.** All runs used Qwen/Qwen3.5-9B. A larger model might resolve some operator-level failures without explicit repair, collapsing the episodic–consolidation distinction observed here. This was not tested.

**Outcome vs. process purity.** The operator-repaired consolidation produces the correct answer, but its reasoning chain contains extended self-correction. The repair is outcome-level complete but process-level imperfect. Whether process-level purity matters for downstream reliability remains an open question.

**Applicability Judgment not tested.** The fourth planned condition (Consolidation + Applicability Judgment) was deferred. It is possible that a gating mechanism would have surfaced selective-transfer signals more directly without requiring the pairing and operator repairs that dominated Round 1.

## 3.6 Future Work

Round 1 identifies three natural next steps, ordered by priority:

1. **Repaired evaluation at moderate scale.** Apply the corrected pairing and operator-aware artifacts to a larger target set (20–40 cases) to test whether the patterns observed on `wiki_dev_2639` generalize across relation-chain bridge tasks.

2. **Applicability Judgment condition.** Introduce the gating mechanism and compare whether it can achieve selective transfer without requiring the fine-grained pairing that Round 1 found necessary.

3. **Model scaling.** Repeat the key diagnostic comparisons with a larger model (e.g., 32B–70B) to determine whether the episodic–consolidation gap and the operator-level sensitivity persist at higher capacity.

The next round should ask a much cleaner question than reopening average-gain comparisons:

> Does the repaired workflow transfer beyond one key diagnostic case?

## 3.7 Conclusion

Round 1 should be read as a **measurement and interpretation success**, not as a benchmark-win story. It shows that evaluating memory selective transfer is **highly sensitive to how relevance is operationalized**. Coarse pairing granularity and non-executable operator abstractions can manufacture false negative-transfer evidence — making it appear that relevant memory harms performance when the real problem lies in the measurement infrastructure.

Through a controlled chain of single-variable repairs, the project recovered the relevant memory path on its strongest diagnostic case for both episodic trace and cross-episode consolidation. The result is not a claim that memory "works" in general, but a methodological demonstration that **selective transfer claims require fine-grained pairing, case-role discipline, and executable memory abstractions** — without which, the experiment measures its own artifacts rather than the phenomenon of interest.

Its value lies in showing that apparent negative transfer may be an artifact of experimental granularity, that abstract memory fails when it is not executable enough, and that careful repair can reverse an incorrect conclusion without changing the model itself. This makes the project useful even without large-scale gains: it provides a more defensible protocol for asking when memory is genuinely reusable and when it is merely present.
