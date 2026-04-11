# rounds/

Per-round experiment specs. Each file defines: what this round tests, what it does NOT test,
which variable changes, what is fixed, pre-run checklist, and success/failure signals.

| File | Variable | Status |
|---|---|---|
| [round_01_memory_form_pilot.md](round_01_memory_form_pilot.md) | memory form (No Memory / Episodic / Consolidation) | Completed |
| [round_01b_prompt_diagnosis.md](round_01b_prompt_diagnosis.md) | prompt scaffold only | Completed |
| [round_01c_role_aware_smoke_repair.md](round_01c_role_aware_smoke_repair.md) | evaluation / case-selection layer only | Completed |
| [round_01d_bridge_subtype_repair.md](round_01d_bridge_subtype_repair.md) | pairing granularity inside `bridge` only | Completed |
| [round_01e_relation_chain_final_feasibility_check.md](round_01e_relation_chain_final_feasibility_check.md) | source-side relation-chain feasibility only | Completed |
| [round_01f_relation_chain_reroute_prep.md](round_01f_relation_chain_reroute_prep.md) | reroute only the relation-chain targets to the new subtype-matched source set | Completed |
| [round_01g_relation_chain_minirun.md](round_01g_relation_chain_minirun.md) | minimal subtype-aware rerun for the rerouted relation-chain targets only | Completed |
| [round_01h_relation_chain_consolidation_diagnosis.md](round_01h_relation_chain_consolidation_diagnosis.md) | isolate the remaining consolidation failure on the sensitive relation-chain target only | Completed |
| [round_01i_kinship_operator_repair.md](round_01i_kinship_operator_repair.md) | isolate whether the last remaining relation-chain consolidation failure comes from incorrect kinship-operator interpretation | Completed |
| [round_01j_patchback_synthesis.md](round_01j_patchback_synthesis.md) | patch the repaired relation-chain evidence back into the role-aware summary layer before final Round 1 synthesis | Completed |

Current status:

- Round 1 is closed as an experimental chain
- no new active `Round 1k` is planned
- the project has moved from repair rounds to final-report assembly
