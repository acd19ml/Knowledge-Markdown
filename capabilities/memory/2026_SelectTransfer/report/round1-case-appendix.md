# Round 1 — Case Appendix

This appendix provides before/after raw evidence for the key diagnostic cases referenced in [final-report-round1-section-v2.md](./final-report-round1-section-v2.md). Each exhibit includes the question, gold answer, condition, predicted answer, and the model's reasoning excerpt. The full raw outputs are linked for each entry.

For the claim-to-evidence mapping, see [round1-evidence-map.md](./round1-evidence-map.md).

---

## Exhibit A — `wiki_dev_2639` (Diagnostic Case)

**Task:** Who is the sibling-in-law of Harriet Pelham-Holles, Duchess Of Newcastle-Upon-Tyne?  
**Gold answer:** Henry Pelham  
**Task subtype:** relation_chain_bridge  
**Role:** artifact_sensitive_diagnosis (Round 1c classification)  
**Why this case matters:** It is the only case that simultaneously satisfies: (1) no-memory baseline is correct, (2) relevant memory initially degrades the answer, and (3) the degradation was subsequently repaired through subtype-aware routing and operator-level abstraction. It carries the strongest single-case evidence chain in Round 1.

<a id="exhibit-a-condition-1"></a>

### Condition 1: No Memory (Round 1b) — Correct

> **Pred:** Henry Pelham | **EM:** 1  
> **Source:** [r1b_no_memory_wiki_dev_2639_relevant.md](../results/05_round1b_run/raw_outputs/r1b_no_memory_wiki_dev_2639_relevant.md) (the no-memory baseline is identical across splits; this link points to the actual no-memory run)

The no-memory reasoning path on this task is straightforward: Harriet's husband is Thomas Pelham-Holles; his brother is Henry Pelham; therefore Henry Pelham is the sibling-in-law. The context paragraph for Thomas explicitly states "He held power with his brother, Prime Minister Henry Pelham."

<a id="exhibit-a-condition-2"></a>

### Condition 2: Relevant Episodic — Coarse Pairing (Round 1b) — Wrong

> **Pred:** Cannot be determined from the provided context. | **EM:** 0  
> **Source set:** `hp_bridge_set_01` (attribute_bridge — mismatched subtype)  
> **Artifact:** [artifacts/hp_bridge_set_01/episodic_trace.md](../artifacts/hp_bridge_set_01/episodic_trace.md)  
> **Raw output:** [r1b_episodic_trace_wiki_dev_2639_relevant.md](../results/05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_2639_relevant.md)  
> **`memory_reference_type`:** implicit_or_none

**Reasoning excerpt:**

> - As the daughter of the 2nd Earl of Godolphin, Harriet's siblings are the children of Francis Godolphin and Lady Henrietta Churchill.
> - The text mentions her grandfather [...] but not listing Harriet's specific siblings by name.
> - However, the question asks for a "sibling-in-law," which refers to the spouse of one's sibling. Since the text does not name Harriet's siblings or their spouses, the specific name of a sibling-in-law cannot be derived from the provided context.

**Diagnosis:** The attribute-bridge episodic trace (venue→attribute, event→property lookups) provided no kinship-chain traversal cue. The model interpreted "sibling-in-law" as "spouse of one's own sibling" and searched Harriet's blood family, missing the simpler husband→brother path entirely.

<a id="exhibit-a-condition-3"></a>

### Condition 3: Relevant Episodic — Subtype-Matched (Round 1g) — Correct

> **Pred:** Henry Pelham | **EM:** 1  
> **Source set:** `hp_relation_chain_bridge_set_01` (relation_chain_bridge — matched subtype)  
> **Artifact:** [artifacts/hp_relation_chain_bridge_set_01/episodic_trace.md](../artifacts/hp_relation_chain_bridge_set_01/episodic_trace.md)  
> **Raw output:** [r1g_episodic_trace_wiki_dev_2639_relevant.md](../results/10_round1g_run/raw_outputs/r1g_episodic_trace_wiki_dev_2639_relevant.md)  
> **`memory_reference_type`:** implicit_or_none

**Reasoning excerpt:**

> - Thomas Pelham-Holles is described as having held power with his brother, Henry Pelham, who served as Prime Minister.
> - Therefore, Henry Pelham is the brother of Harriet's husband, making him her sibling-in-law.
> - The provided context does not mention any siblings of Harriet herself, so the query must refer to her husband's siblings.

**Diagnosis:** With relation-chain episodes in the memory (kinship traversals like "wife→brother", "daughter→mother"), the model correctly resolved "sibling-in-law" through the husband→brother path. The subtype-matched episodic trace did not need to be explicitly referenced — its structural priming was sufficient to redirect the reasoning chain.

**What changed between Condition 2 and 3:** Only the source set routing. Model, prompt, scoring, and target are identical. The shift from `attribute_bridge` → `relation_chain_bridge` source is the sole independent variable.

<a id="exhibit-a-condition-4"></a>

### Condition 4: Irrelevant Episodic (Round 1g) — Wrong

> **Pred:** Cannot be determined from the provided context. | **EM:** 0  
> **Source set:** `hp_bridge_set_01` (attribute_bridge — mismatched, now serving as irrelevant)  
> **Raw output:** [r1g_episodic_trace_wiki_dev_2639_irrelevant.md](../results/10_round1g_run/raw_outputs/r1g_episodic_trace_wiki_dev_2639_irrelevant.md)

Reasoning follows the same Godolphin-sibling dead end as Condition 2. Confirms the irrelevant source continues to misdirect, while the relevant source recovers.

<a id="exhibit-a-condition-5"></a>

### Condition 5: Relevant Consolidation — Revised but Pre-Operator-Repair (Round 1h) — Wrong

> **Pred:** Cannot be determined from the provided context. | **EM:** 0  
> **Source set:** `hp_relation_chain_bridge_set_01`  
> **Artifact:** [revised_relation_chain_consolidation.md](../results/11_round1h_run/revised_relation_chain_consolidation.md) (Round 1h revised version before operator repair)  
> **Raw output:** [r1h_revised_relevant_consolidation_wiki_dev_2639.md](../results/11_round1h_run/raw_outputs/r1h_revised_relevant_consolidation_wiki_dev_2639.md)  
> **`memory_reference_type`:** implicit_or_none

**Reasoning excerpt:**

> - Harriet Pelham-Holles was the wife of Thomas Pelham-Holles.
> - Thomas Pelham-Holles held power with his brother Henry Pelham.
> - However, "sibling-in-law" usually refers to the spouse of one's sibling or the sibling of one's spouse, and the context does not explicitly state the exact relationship from Harriet to Henry.
> - Therefore, the answer cannot be determined from the provided context.

**Diagnosis:** By Round 1h, the consolidation artifact had already been cleaned up structurally, but the operator remained non-executable. The model recognized the spouse branch and the candidate `Henry Pelham`, yet still refused because `sibling-in-law` was treated as a vague label rather than an explicit decision rule.

<a id="exhibit-a-condition-6"></a>

### Condition 6: Relevant Consolidation — Operator-Repaired (Round 1i) — Correct

> **Pred:** Henry Pelham | **EM:** 1  
> **Source set:** `hp_relation_chain_bridge_set_01`  
> **Artifact:** [operator_repaired_relation_chain_consolidation.md](../results/12_round1i_run/operator_repaired_relation_chain_consolidation.md) (Round 1i version with executable `sibling-in-law` operationalization)  
> **Raw output:** [r1i_operator_repaired_relevant_consolidation_wiki_dev_2639.md](../results/12_round1i_run/raw_outputs/r1i_operator_repaired_relevant_consolidation_wiki_dev_2639.md)  
> **`memory_reference_type`:** explicit_use

**Reasoning excerpt (abridged from the extended self-correction chain):**

> - **Identify the starting entity and spouse**: Harriet Pelham-Holles [...] was the wife of Thomas Pelham-Holles, 1st Duke of Newcastle.
> - **Determine the sibling relation**: Thomas Pelham-Holles served under his brother, Henry Pelham.
> - **Apply the sibling-in-law definition**: [...] If the question strictly means "spouse of a sibling", the answer is not in the text. If it means "any sibling-in-law relationship partner", Henry is the only candidate.
> - **Self-Correction**: Actually, looking at similar QA patterns, if the text says "A is married to B, and B has a brother C", the answer to "Who is A's sibling-in-law?" is often C.

**Diagnosis:** The operator-repaired consolidation provided an executable `sibling-in-law` decomposition (`spouse_of → sibling` as first candidate). The model's reasoning shows extended self-debate about the exact definition, but ultimately converges correctly. This is the "outcome-level repair success, process-level purity incomplete" pattern noted in the main report.

**Note on process impurity:** The reasoning chain contains ~20 lines of self-correction before settling on "Henry Pelham." This hedging does not exist in the episodic condition (Condition 3), where the model answers in 4 bullets. This difference is consistent with the main report's observation that consolidation carries higher process-level cost even when the outcome is correct.

<a id="exhibit-a-condition-7"></a>

### Condition 7: Irrelevant Consolidation (Round 1i) — Wrong (Failure Exhibit)

> **Pred:** Cannot be determined from the provided context. | **EM:** 0  
> **Source set:** `hp_bridge_set_01` (attribute_bridge — mismatched)  
> **Artifact:** [artifacts/hp_bridge_set_01/cross_episode_consolidation.md](../artifacts/hp_bridge_set_01/cross_episode_consolidation.md)  
> **Raw output:** [r1i_irrelevant_consolidation_wiki_dev_2639.md](../results/12_round1i_run/raw_outputs/r1i_irrelevant_consolidation_wiki_dev_2639.md)  
> **`memory_reference_type`:** implicit_or_none

**Reasoning excerpt:**

> - As the daughter of the 2nd Earl of Godolphin, Harriet's siblings are the children of Francis Godolphin and Lady Henrietta Churchill.
> - The question asks for a "sibling-in-law," which refers to the spouse of one's sibling. Since the specific names of Harriet's siblings are not provided in the text, their spouses (the sibling-in-laws) cannot be identified from the given context.

**Diagnosis:** The attribute-bridge consolidation (entity→attribute heuristics) provides no kinship-chain guidance. The model falls into the same Godolphin-sibling dead end. This confirms that the Round 1i repair was selective: it only recovered the relevant path, not a generic improvement.

**Why this matters for experiment-contract §8:** This condition is the failure exhibit. Even after all repairs, irrelevant memory on this case remains wrong. The repair did not make the model generically better — it made the *relevant* path usable.

### Exhibit A Summary Table

| # | Condition | Round | Source Set | EM | Pred | Ref Type |
|---|---|---|---|---|---|---|
| 1 | no_memory | 1b | — | 1 | Henry Pelham | — |
| 2 | episodic_trace + relevant | 1b | hp_bridge_set_01 | 0 | Cannot be determined | implicit_or_none |
| 3 | episodic_trace + relevant | 1g | hp_relation_chain_bridge_set_01 | 1 | Henry Pelham | implicit_or_none |
| 4 | episodic_trace + irrelevant | 1g | hp_bridge_set_01 | 0 | Cannot be determined | implicit_or_none |
| 5 | consolidation + relevant (revised, pre-operator repair) | 1h | hp_relation_chain_bridge_set_01 | 0 | Cannot be determined | implicit_or_none |
| 6 | consolidation + relevant (operator repaired) | 1i | hp_relation_chain_bridge_set_01 | 1 | Henry Pelham | explicit_use |
| 7 | consolidation + irrelevant | 1i | hp_bridge_set_01 | 0 | Cannot be determined | implicit_or_none |

---

## Exhibit B — `wiki_dev_8896` (Process Sanity)

**Task:** comparison-type question (details in raw output)  
**Gold answer:** Jean-Baptiste Le Prince  
**Task subtype:** comparison  
**Role:** process_selectivity_sanity_check (Round 1c classification)  
**Why this case matters:** It is the cleanest demonstration that the structured scaffold (Round 1b) makes memory use/reject observable at the process level, even when the outcome does not change.

### Condition 1: Relevant Episodic — Explicit Use

> **Pred:** Jean-Baptiste Le Prince | **EM:** 1  
> **Source set:** `hp_comparison_set_01` (matched)  
> **Raw output:** [r1b_episodic_trace_wiki_dev_8896_relevant.md](../results/05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_8896_relevant.md)  
> **`memory_reference_type`:** explicit_use

The model explicitly references the episodic memory in its reasoning and arrives at the correct answer.

### Condition 2: Irrelevant Episodic — Explicit Reject

> **Pred:** Jean-Baptiste Le Prince | **EM:** 1  
> **Source set:** `hp_bridge_set_01` (mismatched)  
> **Raw output:** [r1b_episodic_trace_wiki_dev_8896_irrelevant.md](../results/05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_8896_irrelevant.md)  
> **`memory_reference_type`:** explicit_reject

The model explicitly states the provided memory is not useful for this task, then answers correctly without it.

### Exhibit B Interpretation

- **Outcome:** No change (correct in both conditions).
- **Process:** Explicit use vs. explicit reject is clearly distinguishable in the reasoning text.
- **Claim supported:** C1 (process-level selectivity is real). The model does not blindly apply or ignore memory — it discriminates based on relevance, even though the final answer happens to be the same.
- **Limitation:** Because the outcome does not change, this case cannot support any transfer efficacy claim. It supports only the observability claim.

### Exhibit B Summary Table

| # | Condition | Source Set | EM | Memory Ref Type |
|---|---|---|---|---|
| 1 | episodic_trace + relevant | hp_comparison_set_01 | 1 | explicit_use |
| 2 | episodic_trace + irrelevant | hp_bridge_set_01 | 1 | explicit_reject |

---

## Exhibit C — `wiki_dev_7019` (Answer-Format Diagnosis)

**Task:** bridge-type question  
**Role:** answer_format_sensitive_case (Round 1c classification)  
**Why this case is included:** It showed outcome change in Round 1b, but the improvement was diagnosed as answer-format compression rather than genuine strategy transfer. It illustrates why mixed aggregate is misleading (C2).

### Round 1c Diagnostic Summary

From [round1c_diagnostic_summary.csv](../results/06_round1c_summary/round1c_diagnostic_summary.csv):

| metric | value |
|---|---|
| total_runs | 6 |
| outcome_changed_runs | 4 |
| improved_runs | 2 |
| degraded_runs | 2 |
| answer_changed_runs | 4 |

### Interpretation

- 4 out of 6 runs showed answer changes, but the improvement pattern is better explained by output compression toward the gold format rather than genuine strategy reuse from memory.
- If this case were included in a flat aggregate alongside `wiki_dev_2639`, the "2 improved / 2 degraded" would cancel out and mask both the real derailment on `wiki_dev_2639` and the format-correction artifact on `wiki_dev_7019`.
- This is the primary evidence behind C2 (mixed-role aggregate is misleading).

### Raw Outputs

The most relevant raw files for this case are:

- [r1b_no_memory_wiki_dev_7019_relevant.md](../results/05_round1b_run/raw_outputs/r1b_no_memory_wiki_dev_7019_relevant.md)
- [r1b_episodic_trace_wiki_dev_7019_relevant.md](../results/05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_7019_relevant.md)
- [r1b_episodic_trace_wiki_dev_7019_irrelevant.md](../results/05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_7019_irrelevant.md)
- [r1b_cross_episode_consolidation_wiki_dev_7019_relevant.md](../results/05_round1b_run/raw_outputs/r1b_cross_episode_consolidation_wiki_dev_7019_relevant.md)
- [r1b_cross_episode_consolidation_wiki_dev_7019_irrelevant.md](../results/05_round1b_run/raw_outputs/r1b_cross_episode_consolidation_wiki_dev_7019_irrelevant.md)

---

## Cross-Exhibit Reading Guide

| Question | Where to look |
|---|---|
| Was the repair selective, not generic? | Exhibit A: Compare Condition 3 (relevant recovered) vs Condition 4 (irrelevant still wrong) |
| Did the repair only affect the relevant path? | Exhibit A: Compare Condition 5 (relevant consolidation recovered) vs Condition 6 (irrelevant consolidation still wrong) |
| Is process-level selectivity observable? | Exhibit B: explicit_use vs explicit_reject on same task |
| Why can't we just average all cases? | Exhibit C: answer-format improvement ≠ strategy transfer |
| What does a failure look like after all repairs? | Exhibit A, Condition 7: irrelevant consolidation reasoning follows Godolphin dead end |
