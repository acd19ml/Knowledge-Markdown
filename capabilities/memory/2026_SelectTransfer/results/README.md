# results/

Experiment run results and prep artifacts. This directory now spans the full Round 1 chain:

- early sampling / pool construction
- pilot and Round 1b runs
- Round 1c analysis-only summaries
- subtype repair and relation-chain feasibility
- Round 1g / 1h / 1i reruns
- Round 1j patchback synthesis

| File | Content |
|---|---|
| [pilot_results.csv](pilot_results.csv) | Per-run results: task, split, condition, EM, F1, routing decision, notes |

Round-specific preparation artifacts also live under subdirectories such as:

- [05_round1b_prep/round1_target_audit.md](./05_round1b_prep/round1_target_audit.md)
- [05_round1b_prep/round1_target_audit.csv](./05_round1b_prep/round1_target_audit.csv)
- [05_round1b_prep/round1b_smoke_subset.csv](./05_round1b_prep/round1b_smoke_subset.csv)
- [05_round1b_prep/round1b_case_role_reclassification.md](./05_round1b_prep/round1b_case_role_reclassification.md)
- [05_round1b_prep/round1c_aggregate_rules.md](./05_round1b_prep/round1c_aggregate_rules.md)

Round 1b run outputs live under:

- `05_round1b_run/`
- expected files:
  - `round1b_smoke_results.csv`
  - `round1b_smoke_results_detail.csv`
  - `raw_outputs/`

Round 1c analysis outputs live under:

- [06_round1c_summary/round1c_allowed_aggregate_summary.md](./06_round1c_summary/round1c_allowed_aggregate_summary.md)
- [06_round1c_summary/round1c_process_summary.csv](./06_round1c_summary/round1c_process_summary.csv)
- [06_round1c_summary/round1c_diagnostic_summary.csv](./06_round1c_summary/round1c_diagnostic_summary.csv)
- [06_round1c_summary/round1c_audit_summary.csv](./06_round1c_summary/round1c_audit_summary.csv)

Round 1d subtype repair prep lives under:

- [07_round1d_prep/bridge_subtype_source_audit.csv](./07_round1d_prep/bridge_subtype_source_audit.csv)
- [07_round1d_prep/bridge_subtype_target_audit.csv](./07_round1d_prep/bridge_subtype_target_audit.csv)
- [07_round1d_prep/bridge_subtype_pairing_repair.md](./07_round1d_prep/bridge_subtype_pairing_repair.md)

Relation-chain bridge expansion artifacts should be written under:

- `08_relation_chain_bridge_expansion/`
- expected files:
  - `candidate_batch_raw.csv`
  - `candidate_batch_filtered.csv`
  - `candidate_batch_for_subtype_annotation.csv`
  - `candidate_batch_for_subtype_annotation_screened.csv`
  - `candidate_batch_full.json`
  - `candidate_batch_summary.md`
  - `batch_01_prefilter_diagnosis.md`
  - `batch_01_first_pass_screening.md`
  - `batch_01_first_pass_screening.csv`
  - `batch_01_subtype_annotation_summary.md`

Batch 2 high-precision relation-chain feasibility artifacts should be written under:

- `09_relation_chain_bridge_expansion_batch2/`
- expected files:
  - `candidate_batch2_raw.csv`
  - `candidate_batch2_filtered.csv`
  - `candidate_batch2_for_subtype_annotation.csv`
  - `candidate_batch2_full.json`
  - `candidate_batch2_summary.md`
  - `batch_02_subtype_annotation_summary.md`
  - `relation_chain_source_set_selection.md`
  - `relation_chain_pairing_update.md`

Round 1g relation-chain minimal rerun prep and outputs live under:

- `10_round1g_prep/`
- expected files:
  - `relation_chain_artifact_review.md`
  - `relation_chain_minirun_subset.csv`
- `10_round1g_run/`
- expected files:
  - `round1g_relation_chain_results.csv`
  - `round1g_relation_chain_results_detail.csv`
  - `raw_outputs/`

Round 1h consolidation-diagnosis prep lives under:

- `11_round1h_prep/`
- expected files:
  - `relation_chain_consolidation_subset.csv`
  - `relation_chain_consolidation_failure_diagnosis.md`
- `11_round1h_run/`
- expected files:
  - `revised_relation_chain_consolidation_prompt.md`
  - `revised_relation_chain_consolidation.md`
  - `round1h_consolidation_results.csv`
  - `round1h_consolidation_results_detail.csv`
  - `raw_outputs/`

Round 1i kinship-operator repair prep lives under:

- `12_round1i_prep/`
- expected files:
  - `kinship_operator_failure_diagnosis.md`
  - `relation_chain_operator_subset.csv`

Round 1i kinship-operator repair outputs should be written under:

- `12_round1i_run/`
- expected files:
  - `operator_repaired_relation_chain_consolidation_prompt.md`
  - `operator_repaired_relation_chain_consolidation.md`
  - `round1i_operator_results.csv`
  - `round1i_operator_results_detail.csv`
  - `raw_outputs/`

Round 1j patchback / synthesis artifacts live under:

- `13_round1j_prep/`
- expected files:
  - `round1j_patchback_plan.md`
- `13_round1j_summary/`
- expected files:
  - `round1j_wiki_dev_2639_patch_rows.csv`
  - `round1j_patchback_summary.md`

Current interpretation:

- `04_pilot_run/` = original Round 1 pilot
- `05_round1b_run/` = observability / prompt diagnosis
- `10_round1g_run/` = subtype-aware episodic rerun
- `11_round1h_run/` = consolidation wording / formatting diagnosis
- `12_round1i_run/` = kinship-operator repair
- `13_round1j_summary/` = final patchback layer used to update the Round 1 narrative

See [protocol/csv-field-examples.md](../protocol/csv-field-examples.md) for field definitions.
