# Round 1 — Claim-to-Evidence Map

This file maps every claim and non-claim in [final-report-round1-section-v2.md](./final-report-round1-section-v2.md) to its supporting evidence chain: progress report, result CSV, raw output, and artifact version.

For key diagnostic cases, see [round1-case-appendix.md](./round1-case-appendix.md).

---

## Claims

### C1 — Process-level selectivity is real

| Layer | File | What it shows |
|---|---|---|
| Progress report | [progress-report-round1b-prompt-diagnosis.md](./progress-report-round1b-prompt-diagnosis.md) §3.2 | 36/36 parse success; 3/24 explicit use, 2/24 explicit reject |
| Result CSV | [results/05_round1b_run/round1b_smoke_results_detail.csv](../results/05_round1b_run/round1b_smoke_results_detail.csv) | Per-run `memory_reference_type` column |
| Raw output (explicit use) | [results/05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_8896_relevant.md](../results/05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_8896_relevant.md) | `memory_reference_type: explicit_use`, EM=1 |
| Raw output (explicit reject) | [results/05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_8896_irrelevant.md](../results/05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_8896_irrelevant.md) | `memory_reference_type: explicit_reject`, EM=1 |
| Case appendix | [round1-case-appendix.md § Exhibit B](./round1-case-appendix.md#exhibit-b--wiki_dev_8896-process-sanity) | Side-by-side reasoning excerpts |

### C2 — Mixed-role aggregate is misleading

| Layer | File | What it shows |
|---|---|---|
| Progress report | [progress-report-round1c-role-aware-smoke-repair.md](./progress-report-round1c-role-aware-smoke-repair.md) §3 | Aggregate overview, process/diagnostic/audit split |
| Role classification | [results/05_round1b_prep/round1b_case_role_reclassification.csv](../results/05_round1b_prep/round1b_case_role_reclassification.csv) | Per-case `case_role` and `aggregate_use` columns |
| Aggregate rules | [results/05_round1b_prep/round1c_aggregate_rules.md](../results/05_round1b_prep/round1c_aggregate_rules.md) | Defines which views are allowed / banned |
| Allowed overview CSV | [results/06_round1c_summary/round1c_allowed_aggregate_overview.csv](../results/06_round1c_summary/round1c_allowed_aggregate_overview.csv) | `process_sanity`: 0 outcome change; `diagnostic`: 7 outcome changes; `audit_boundary`: 0 outcome change |
| Process summary CSV | [results/06_round1c_summary/round1c_process_summary.csv](../results/06_round1c_summary/round1c_process_summary.csv) | wiki_dev_8896 and wiki_dev_10727 detail |
| Diagnostic summary CSV | [results/06_round1c_summary/round1c_diagnostic_summary.csv](../results/06_round1c_summary/round1c_diagnostic_summary.csv) | wiki_dev_7019 and wiki_dev_2639 detail |

### C3 — Pairing granularity is part of the result

| Layer | File | What it shows |
|---|---|---|
| Progress report (subtype audit) | [progress-report-round1d-bridge-subtype-repair.md](./progress-report-round1d-bridge-subtype-repair.md) | `bridge` split into `attribute_bridge` / `relation_chain_bridge` |
| Progress report (feasibility) | [progress-report-round1e-relation-chain-feasibility.md](./progress-report-round1e-relation-chain-feasibility.md) | Source-side feasibility confirmed |
| Progress report (rerun) | [progress-report-round1g-relation-chain-minirun.md](./progress-report-round1g-relation-chain-minirun.md) §3.3 | Episodic trace repaired on wiki_dev_2639 |
| Round spec | [rounds/round_01g_relation_chain_minirun.md](../rounds/round_01g_relation_chain_minirun.md) | Single-variable design: only source routing changed |
| Result CSV | [results/10_round1g_run/round1g_relation_chain_results_detail.csv](../results/10_round1g_run/round1g_relation_chain_results_detail.csv) | Per-run outcomes for 10 runs |
| Raw output (before: coarse pairing, wrong) | [results/05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_2639_relevant.md](../results/05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_2639_relevant.md) | source=`hp_bridge_set_01`, EM=0, pred=`Cannot be determined` |
| Raw output (after: subtype-matched, correct) | [results/10_round1g_run/raw_outputs/r1g_episodic_trace_wiki_dev_2639_relevant.md](../results/10_round1g_run/raw_outputs/r1g_episodic_trace_wiki_dev_2639_relevant.md) | source=`hp_relation_chain_bridge_set_01`, EM=1, pred=`Henry Pelham` |
| Artifact (coarse, irrelevant to target subtype) | [artifacts/hp_bridge_set_01/episodic_trace.md](../artifacts/hp_bridge_set_01/episodic_trace.md) | `attribute_bridge` episodes |
| Artifact (subtype-matched) | [artifacts/hp_relation_chain_bridge_set_01/episodic_trace.md](../artifacts/hp_relation_chain_bridge_set_01/episodic_trace.md) | `relation_chain_bridge` episodes |
| Artifact review | [results/10_round1g_prep/relation_chain_artifact_review.md](../results/10_round1g_prep/relation_chain_artifact_review.md) | Human review passed |
| Case appendix | [round1-case-appendix.md § Exhibit A](./round1-case-appendix.md#exhibit-a--wiki_dev_2639-diagnostic-case) | Full before/after reasoning |

### C4 — Abstract memory must be executable, not merely relevant

| Layer | File | What it shows |
|---|---|---|
| Progress report (formatting fix) | [progress-report-round1h-consolidation-diagnosis.md](./progress-report-round1h-consolidation-diagnosis.md) | Formatting repaired but correctness still fails; failure narrowed to kinship-operator interpretation |
| Progress report (operator repair) | [progress-report-round1i-kinship-operator-repair.md](./progress-report-round1i-kinship-operator-repair.md) §3.2 | Operator-repaired relevant consolidation: EM=1; Round 1h revised: EM=0 |
| Round spec (1h) | [rounds/round_01h_relation_chain_consolidation_diagnosis.md](../rounds/round_01h_relation_chain_consolidation_diagnosis.md) | Single variable: consolidation formatting |
| Round spec (1i) | [rounds/round_01i_kinship_operator_repair.md](../rounds/round_01i_kinship_operator_repair.md) | Single variable: kinship-operator executable interpretation |
| Repair protocol | [protocol/relation-chain-kinship-operator-repair.md](../protocol/relation-chain-kinship-operator-repair.md) | Exact operationalization of `sibling-in-law` |
| Result CSV | [results/12_round1i_run/round1i_operator_results_detail.csv](../results/12_round1i_run/round1i_operator_results_detail.csv) | 4 runs: no_memory=correct, 1h_revised=wrong, 1i_repaired=correct, irrelevant=wrong |
| Raw output (pre-repair, wrong) | [results/11_round1h_run/raw_outputs/r1h_revised_relevant_consolidation_wiki_dev_2639.md](../results/11_round1h_run/raw_outputs/r1h_revised_relevant_consolidation_wiki_dev_2639.md) | `memory_reference_type: implicit_or_none`, EM=0, pred=`Cannot be determined` |
| Raw output (repaired, correct) | [results/12_round1i_run/raw_outputs/r1i_operator_repaired_relevant_consolidation_wiki_dev_2639.md](../results/12_round1i_run/raw_outputs/r1i_operator_repaired_relevant_consolidation_wiki_dev_2639.md) | `memory_reference_type: explicit_use`, EM=1, pred=`Henry Pelham` |
| Raw output (irrelevant, still wrong) | [results/12_round1i_run/raw_outputs/r1i_irrelevant_consolidation_wiki_dev_2639.md](../results/12_round1i_run/raw_outputs/r1i_irrelevant_consolidation_wiki_dev_2639.md) | EM=0, pred=`Cannot be determined` |
| Artifact (pre-repair revised consolidation) | [results/11_round1h_run/revised_relation_chain_consolidation.md](../results/11_round1h_run/revised_relation_chain_consolidation.md) | Round 1h revised version before executable operator repair |
| Artifact (operator-repaired consolidation) | [results/12_round1i_run/operator_repaired_relation_chain_consolidation.md](../results/12_round1i_run/operator_repaired_relation_chain_consolidation.md) | Round 1i version with executable `sibling-in-law` operationalization |
| Case appendix (before) | [Condition 5](./round1-case-appendix.md#exhibit-a-condition-5) | Pre-repair wrong reasoning |
| Case appendix (after) | [Condition 6](./round1-case-appendix.md#exhibit-a-condition-6) | Operator-repaired correct reasoning |

### C5 — Seemingly negative transfer evidence can be fully overturned

| Layer | File | What it shows |
|---|---|---|
| Patchback summary | [results/13_round1j_summary/round1j_patchback_summary.md](../results/13_round1j_summary/round1j_patchback_summary.md) | Before/after interpretation of wiki_dev_2639 |
| Patchback data | [results/13_round1j_summary/round1j_wiki_dev_2639_patch_rows.csv](../results/13_round1j_summary/round1j_wiki_dev_2639_patch_rows.csv) | 4 patched rows with source_round, condition, EM |
| Progress report (synthesis) | [progress-report-round1-final-synthesis.md](./progress-report-round1-final-synthesis.md) §3.4–3.5 | Narrative of the full repair chain |
| Evidence chain spans | C3 evidence (episodic repair) + C4 evidence (consolidation repair) | Combined, they show both memory forms recovered on the same case |

---

## Non-Claims

### N1 — Cannot claim strong average benchmark gain

| Limiting evidence | File |
|---|---|
| Only 6 smoke cases in Round 1b | [results/05_round1b_prep/round1b_smoke_subset.csv](../results/05_round1b_prep/round1b_smoke_subset.csv) |
| All 6 excluded from transfer aggregate | [results/05_round1b_prep/round1b_case_role_reclassification.csv](../results/05_round1b_prep/round1b_case_role_reclassification.csv): every row has `aggregate_use = exclude_from_transfer_aggregate` |
| Round 1b aggregate EM for relevant episodic = 0.33 | [progress-report-round1b-prompt-diagnosis.md](./progress-report-round1b-prompt-diagnosis.md) §3.1 |

### N2 — Cannot claim consolidation universally better or worse than episodic

| Limiting evidence | File |
|---|---|
| On wiki_dev_2639: episodic repaired at Round 1g, consolidation required additional Round 1i operator repair | [results/10_round1g_run/round1g_relation_chain_results_detail.csv](../results/10_round1g_run/round1g_relation_chain_results_detail.csv) vs [results/12_round1i_run/round1i_operator_results_detail.csv](../results/12_round1i_run/round1i_operator_results_detail.csv) |
| Only 1 sensitive diagnostic case reached full repair | Only wiki_dev_2639 simultaneously satisfies: no_memory=correct, relevant_episodic=correct, relevant_consolidation=correct |

### N3 — Cannot claim selective transfer demonstrated at scale

| Limiting evidence | File |
|---|---|
| Round 1g rerun: 2 targets only | [results/10_round1g_prep/relation_chain_minirun_subset.csv](../results/10_round1g_prep/relation_chain_minirun_subset.csv) |
| wiki_dev_1379: ceiling case, all 5 conditions correct | [results/10_round1g_run/round1g_relation_chain_results_detail.csv](../results/10_round1g_run/round1g_relation_chain_results_detail.csv) |

### N4 — Cannot claim one repaired case proves broad generalization

| Limiting evidence | File |
|---|---|
| The entire C3→C4→C5 chain rests on wiki_dev_2639 | All raw outputs under `results/10_round1g_run/raw_outputs/` and `results/12_round1i_run/raw_outputs/` |
| No other case simultaneously had: baseline correct, relevant memory wrong, then repaired | [results/06_round1c_summary/round1c_diagnostic_summary.csv](../results/06_round1c_summary/round1c_diagnostic_summary.csv) |

### N5 — Cannot claim current model sufficient for production-grade memory use

| Limiting evidence | File |
|---|---|
| Even operator-repaired consolidation shows residual term-level hesitation in reasoning | [results/12_round1i_run/raw_outputs/r1i_operator_repaired_relevant_consolidation_wiki_dev_2639.md](../results/12_round1i_run/raw_outputs/r1i_operator_repaired_relevant_consolidation_wiki_dev_2639.md): reasoning contains extended self-correction loop before converging |
| Model: Qwen/Qwen3.5-9B, local inference | [progress-report-round1b-prompt-diagnosis.md](./progress-report-round1b-prompt-diagnosis.md) §2.3 |

---

## Failure Exhibit

Per experiment-contract §8, at least one failure case must be retained.

### F1 — Irrelevant consolidation remains wrong after all repairs (wiki_dev_2639)

| Layer | File | What it shows |
|---|---|---|
| Raw output (Round 1i, irrelevant consolidation) | [results/12_round1i_run/raw_outputs/r1i_irrelevant_consolidation_wiki_dev_2639.md](../results/12_round1i_run/raw_outputs/r1i_irrelevant_consolidation_wiki_dev_2639.md) | EM=0, pred=`Cannot be determined`, source=`hp_bridge_set_01` (attribute_bridge, mismatched) |
| Interpretation | Irrelevant `attribute_bridge` consolidation gives generic entity-chaining heuristics that do not help a kinship-chain task; the model defaults to conservative refusal |
| Case appendix | [Condition 7](./round1-case-appendix.md#exhibit-a-condition-7) | Full reasoning excerpt |
| Contract alignment | experiment-contract §8: failure case retained alongside success cases |

### F2 — wiki_dev_6083 remains a scoring-boundary case, never resolvable as transfer evidence

| Layer | File | What it shows |
|---|---|---|
| Role classification | [results/05_round1b_prep/round1b_case_role_reclassification.csv](../results/05_round1b_prep/round1b_case_role_reclassification.csv) | `case_role = scoring_boundary_case`, `aggregate_use = exclude_from_transfer_aggregate` |
| Explanation | All conditions output `Spain` while gold is `Spanish`; scoring boundary dominates any memory effect |
| Contract alignment | experiment-contract §12: negative result diagnosed as protocol issue, not theoretical defeat |
