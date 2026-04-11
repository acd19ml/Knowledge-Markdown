# Round 1 — Memory-Form Pilot: From False Negatives to Methodological Clarity

> **Supporting materials** — This narrative is Layer 1 of a three-layer report structure:
> - **L1 (this file):** Final narrative for the course report.
> - **L2:** [round1-evidence-map.md](./round1-evidence-map.md) — Maps every claim/non-claim to progress reports, result CSVs, raw outputs, and artifact versions.
> - **L3:** [round1-case-appendix.md](./round1-case-appendix.md) — Before/after raw evidence for key diagnostic cases (wiki_dev_2639, wiki_dev_8896, wiki_dev_7019).

## 1. Research Question

The goal of Round 1 was not to show that memory universally improves benchmark performance. Instead, it was to build and stress-test an evaluation workflow for **selective transfer**:

> Under a fixed experience budget (N = 5 source episodes), do different memory forms — No Memory, Episodic Trace, and Cross-Episode Consolidation — exhibit selective transfer behavior on structurally matched versus mismatched target tasks?

The benchmark setting is **HotpotQA → 2WikiMultiHopQA** near-transfer, using a local `Qwen/Qwen3.5-9B` model. Under this framing, the primary contribution of Round 1 is methodological: we aimed to determine whether apparent transfer effects were genuine memory effects or artifacts of coarse pairing, unstable prompting, and non-executable memory abstractions.

---

## 2. Experimental Path

Round 1 was not a single run-and-report cycle. It evolved through ten controlled sub-rounds, each changing exactly one variable while holding the rest fixed. These sub-rounds fall naturally into three phases.

### Phase A — Making the experiment observable (Rounds 1 → 1c)

The initial pilot established the basic pipeline — taxonomy, source-set construction, matched/mismatched pairing, artifact generation, and multi-condition runs — but early results were difficult to interpret. The model mostly answered in single lines without exposing reasoning traces, and several target cases were too insensitive for reliable diagnosis.

Round 1b repaired the measurement layer by introducing a structured `## Reasoning` + `## Final Answer` scaffold. All 36 runs parsed successfully, and for the first time explicit memory use and explicit memory rejection became observable in model outputs.

Round 1c then stopped treating the six smoke cases as a uniform mini-benchmark. Each case was reclassified into one of three roles — *process sanity*, *diagnostic*, or *audit/boundary* — and mixed-role aggregation was banned. This single discipline change eliminated several apparent paradoxes in the Round 1b summary table.

### Phase B — Repairing pairing granularity (Rounds 1d → 1g)

The bridge-subtype audit (Round 1d) revealed that the original `bridge` category was too coarse. Two of the smoke targets — `wiki_dev_2639` and `wiki_dev_1379` — were `relation_chain_bridge` tasks, but they had been paired to an `attribute_bridge` source set. What initially looked like "relevant memory can hurt" was better explained as a subtype mismatch.

Rounds 1e–1f confirmed that HotpotQA's source side could supply enough `relation_chain_bridge` episodes, constructed the new source set `hp_relation_chain_bridge_set_01`, and updated the routing table — all without running the model again.

Round 1g executed a minimal rerun (2 targets × 5 conditions = 10 runs). The result was decisive for `episodic_trace`: on the strongest diagnostic case (`wiki_dev_2639`), relevant episodic memory recovered from wrong to correct after subtype-aware rerouting. However, `cross_episode_consolidation` still failed, shifting the bottleneck from pairing to the memory-form layer.

### Phase C — Repairing operator-level abstraction (Rounds 1h → 1j)

Round 1h fixed formatting and branch-wording issues in the relation-chain consolidation artifact, but answer correctness did not return. The failure was narrowed to a specific cause: the consolidation heuristic left kinship operators like `sibling-in-law` as vague natural-language labels instead of executable checking rules.

Round 1i rewrote only the `sibling-in-law` operationalization — decomposing it into candidate paths (`spouse_of → sibling` vs. `sibling → spouse_of`) and explicitly prohibiting the `parent / grandparent / spouse-of-parent` defaults. This single change recovered the relevant consolidation answer on `wiki_dev_2639` from wrong to correct, while irrelevant consolidation remained wrong.

Round 1j performed no new model runs. It patched the repaired evidence back into the role-aware summary, formally withdrawing the earlier "relevant memory hurts" diagnosis.

### Sub-Round Summary Table

| Sub-Round | Variable Changed | Core Finding |
|---|---|---|
| 1 | memory form | Low sensitivity; hard to interpret |
| 1b | prompt scaffold | 36/36 parseable; explicit memory use/reject observable |
| 1c | case-selection layer | Cases split into process / diagnostic / boundary roles; mixed aggregate banned |
| 1d | pairing granularity | `bridge` must split into `attribute_bridge` vs `relation_chain_bridge` |
| 1e–1f | source feasibility + routing | `relation_chain_bridge` source constructed; routing updated |
| 1g | source routing (rerun) | Episodic trace repaired on `wiki_dev_2639`; consolidation still fails |
| 1h | consolidation formatting | Formatting fixed; failure narrowed to kinship-operator interpretation |
| 1i | operator interpretation | Relevant consolidation recovers; irrelevant remains wrong |
| 1j | interpretation layer | Old "relevant memory hurts" diagnosis formally withdrawn |

---

## 3. Evidence Evolution on the Key Diagnostic Case

`wiki_dev_2639` is the single most informative case in Round 1. It is a **relation-chain bridge** task whose no-memory baseline answers correctly (`Henry Pelham`). The table below traces how each memory condition's outcome changed as the experimental infrastructure was repaired.

| Stage | No Memory | Episodic (rel.) | Episodic (irrel.) | Consolidation (rel.) | Consolidation (irrel.) |
|---|---|---|---|---|---|
| **1b** — coarse pairing | ✓ | ✗ refusal | ✗ refusal | ✗ refusal | ✓ |
| **1g** — subtype-aware reroute | ✓ | **✓ recovered** | ✗ refusal | ✗ still fails | ✗ |
| **1i** — operator-aware repair | ✓ | ✓ | ✗ refusal | **✓ recovered** | ✗ |

Three observations are worth highlighting:

1. **Relevant episodic trace was a false negative.** The Round 1b degradation disappeared entirely once the target was routed to a subtype-matched source. The earlier interpretation — "relevant memory harms an originally correct baseline" — was an artifact of coarse pairing, not a genuine negative transfer effect.

2. **Relevant consolidation required a deeper fix.** Subtype-aware routing alone was insufficient; the consolidation artifact also needed its relation operators encoded as executable checking rules. This is a qualitatively different layer of repair from pairing, suggesting that abstract memory has an additional precondition beyond source relevance.

3. **Irrelevant memory remained consistently harmful.** Across all repair stages, irrelevant memory continued to produce refusal or error. This confirms that the positive repairs are selective — they did not make the model generically more willing to guess.

---

## 4. Claims and Non-Claims

### What Round 1 Can Claim

| # | Claim | Evidence | Trace |
|---|---|---|---|
| C1 | **Process-level selectivity is real.** Structured scaffolding makes memory use/reject observable; the project is no longer a black-box score comparison. | 1b: 36/36 parseable; explicit use and explicit reject both observed. | [map §C1](./round1-evidence-map.md#c1--process-level-selectivity-is-real) / [Exhibit B](./round1-case-appendix.md#exhibit-b--wiki_dev_8896-process-sanity) |
| C2 | **Mixed-role aggregate is misleading.** Treating heterogeneous cases as a uniform benchmark produces contradictory summaries. | 1c: role-aware reclassification eliminated apparent paradoxes. | [map §C2](./round1-evidence-map.md#c2--mixed-role-aggregate-is-misleading) / [Exhibit C](./round1-case-appendix.md#exhibit-c--wiki_dev_7019-answer-format-diagnosis) |
| C3 | **Pairing granularity is part of the result, not a secondary detail.** Coarse `bridge` pairing created false negative-transfer evidence. | 1d→1g: episodic trace on `wiki_dev_2639` goes from wrong → correct after subtype-aware rerouting. | [map §C3](./round1-evidence-map.md#c3--pairing-granularity-is-part-of-the-result) / [Exhibit A](./round1-case-appendix.md#exhibit-a--wiki_dev_2639-diagnostic-case) |
| C4 | **Abstract memory must be executable, not merely relevant.** Source relevance alone is insufficient; relation operators must be encoded as executable checking rules. | 1h→1i: only changing `sibling-in-law` operationalization recovers consolidation from wrong to correct. | [map §C4](./round1-evidence-map.md#c4--abstract-memory-must-be-executable-not-merely-relevant) / [Exhibit A](./round1-case-appendix.md#exhibit-a--wiki_dev_2639-diagnostic-case) |
| C5 | **Seemingly negative transfer evidence can be fully overturned** by repairing pairing granularity and operator-level abstraction. | Full chain: 1b "relevant hurts" → 1j "relevant recovers on both memory forms." | [map §C5](./round1-evidence-map.md#c5--seemingly-negative-transfer-evidence-can-be-fully-overturned) |

### What Round 1 Cannot Claim

| # | Non-Claim | Reason | Trace |
|---|---|---|---|
| N1 | Memory provides strong average benchmark gain. | ≤ 6 smoke cases; no large-scale aggregate was computed or intended. | [map §N1](./round1-evidence-map.md#n1--cannot-claim-strong-average-benchmark-gain) |
| N2 | Consolidation is universally better (or worse) than episodic trace. | Only one sensitive diagnostic case reached full repair. | [map §N2](./round1-evidence-map.md#n2--cannot-claim-consolidation-universally-better-or-worse-than-episodic) |
| N3 | Selective transfer has been fully demonstrated at scale. | The project established the measurement workflow, not a broad empirical result. | [map §N3](./round1-evidence-map.md#n3--cannot-claim-selective-transfer-demonstrated-at-scale) |
| N4 | One repaired case proves broad generalization. | `wiki_dev_2639` is a single-case proof of concept for the diagnosis-and-repair methodology. | [map §N4](./round1-evidence-map.md#n4--cannot-claim-one-repaired-case-proves-broad-generalization) |
| N5 | The current model is sufficient for production-grade memory use. | Process-level hesitation remains even in the repaired consolidation output. | [map §N5](./round1-evidence-map.md#n5--cannot-claim-current-model-sufficient-for-production-grade-memory-use) |

---

## 5. Theoretical Implication

Beyond methodology, Round 1 carries a substantive implication for how memory selective transfer should be conceptualized.

The standard framing asks: *is the source experience relevant to the target?* Round 1 suggests this question is necessary but insufficient. A more complete framing requires two additional conditions:

1. **Relevance must be operationalized at the right granularity.** A coarse-grained `bridge` label is not the same as a subtype-specific `relation_chain_bridge` match. If the granularity is wrong, even genuinely relevant experience will appear harmful.

2. **Abstract memory must preserve operator structure.** For consolidation-style memory, it is not enough to summarize *what* relation holds between entities; the memory must encode *how* to verify that relation — i.e., the operator must be executable. Without this, the model defaults to conservative refusal even when the memory is topically relevant.

Together, these conditions suggest that the boundary between useful and harmful memory is not determined by relevance at a coarse label level alone. It also depends on whether the memory representation preserves the operator structure required by the target task.

---

## 6. Limitations

Round 1 remains limited in three respects:

1. **Scale.** The strongest repaired evidence comes from a single diagnostic case (`wiki_dev_2639`) rather than a large evaluation set. The remaining cases either served as process-sanity checks or were too easy (ceiling) to provide sensitivity.

2. **Model capacity.** All runs used `Qwen/Qwen3.5-9B`. It is possible that a larger model would resolve some of the operator-level failures without explicit repair, but this was not tested.

3. **Outcome vs. process purity.** Even in the repaired consolidation run, the model's reasoning showed residual hesitation around kinship terminology before converging on the correct answer. The repair is outcome-level complete but process-level imperfect.

These limitations do not undermine the methodological findings — they define where the next round of work should begin.

---

## 7. Final Takeaway

> Round 1 shows that evaluating memory selective transfer is **highly sensitive to how relevance is operationalized**. Coarse pairing granularity and non-executable operator abstractions can manufacture false negative-transfer evidence — making it appear that relevant memory harms performance when the real problem lies in the measurement infrastructure. Through a controlled chain of sub-round repairs (prompt scaffold → role-aware case discipline → subtype-aware routing → operator-level abstraction), the project recovered the relevant memory path on its strongest diagnostic case for both episodic trace and cross-episode consolidation. The result is not a claim that memory "works" in general, but a methodological demonstration that **selective transfer claims require fine-grained pairing, case-role discipline, and executable memory abstractions** — without which, the experiment measures its own artifacts rather than the phenomenon of interest.

---

## 8. Methodological Lessons for Future Rounds

1. **Never aggregate before assigning case roles.** Every case must have a declared experimental role (process sanity / diagnostic / boundary) before entering any summary table.
2. **Treat pairing granularity as a first-class variable.** A "relevant" label is only meaningful at the subtype level, not at a coarse cluster level.
3. **Require executable abstractions in consolidation artifacts.** Relation operators must be decomposed into candidate-checking steps, not left as natural-language labels.
4. **Keep sub-round scope minimal.** Each sub-round should change exactly one variable — this discipline is what made the causal chain traceable.
