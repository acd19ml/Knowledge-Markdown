# notebooks/

Colab notebooks for each experiment phase. Earlier notebooks build the evaluation setup; later notebooks implement the Round 1 repair chain and final synthesis. Run on Google Colab or another notebook GPU environment (GPU for generation runs, CPU for data prep / analysis).

| Notebook | Phase | GPU needed? |
|---|---|---|
| [01_sampling.ipynb](01_sampling.ipynb) | Sample first 20 tasks from HotpotQA + 2WikiMultiHopQA | No (CPU) |
| [02_hotpotqa_comparison_expansion.ipynb](02_hotpotqa_comparison_expansion.ipynb) | Expand the first HotpotQA comparison candidate batch for source-set construction | No (CPU) |
| [03_delayed_reannotation_review.ipynb](03_delayed_reannotation_review.ipynb) | Export delayed re-annotation subset, compare second-pass labels, and detect affected source sets / pairs | No (CPU) |
| [04_artifact_generation.ipynb](04_artifact_generation.ipynb) | Generate `episodic_trace` and `cross_episode_consolidation` from frozen Round 1 source sets with local Hugging Face inference | Yes (GPU recommended for actual generation; prompt preview can run on CPU) |
| [05_pilot_run.ipynb](05_pilot_run.ipynb) | Round 1 pilot: compare `no_memory` / `episodic_trace` / `cross_episode_consolidation` on 10 targets × 2 splits | Yes (GPU for local inference; or API mode) |
| [06_round1b_prompt_diagnosis.ipynb](06_round1b_prompt_diagnosis.ipynb) | Round 1b smoke subset: structured `## Reasoning` + `## Final Answer` prompt diagnosis on 6 targets × 3 conditions × 2 splits | Yes (GPU for actual generation; dry run works on CPU) |
| [07_round1c_allowed_aggregate_summary.ipynb](07_round1c_allowed_aggregate_summary.ipynb) | Round 1c analysis-only notebook: read frozen Round 1b results plus role-aware rules and generate only the allowed aggregate summaries | No (CPU) |
| [08_relation_chain_bridge_expansion.ipynb](08_relation_chain_bridge_expansion.ipynb) | Round 1d feasibility notebook: scan HotpotQA bridge pool for relation-looking candidates and export the first subtype-annotation batch | No (CPU) |
| [09_relation_chain_bridge_expansion_batch2.ipynb](09_relation_chain_bridge_expansion_batch2.ipynb) | Round 1e final feasibility notebook: use stricter multi-relation templates to test whether HotpotQA can still yield enough `relation_chain_bridge` source candidates | No (CPU) |
| [10_relation_chain_artifact_generation.ipynb](10_relation_chain_artifact_generation.ipynb) | Generate `episodic_trace` and `cross_episode_consolidation` only for `hp_relation_chain_bridge_set_01` using working source-set and Batch 2 annotation files | Yes (GPU recommended for actual generation; prompt preview can run on CPU) |
| [11_round1g_relation_chain_minirun.ipynb](11_round1g_relation_chain_minirun.ipynb) | Round 1g minimal rerun: keep the Round 1b scaffold fixed and rerun only the two rerouted relation-chain targets under subtype-aware routing | Yes (GPU for actual generation; dry run works on CPU) |
| [12_round1h_consolidation_diagnosis.ipynb](12_round1h_consolidation_diagnosis.ipynb) | Round 1h single-target diagnosis: generate a revised relation-chain consolidation and compare it against original relevant / irrelevant consolidation on `wiki_dev_2639` only | Yes (GPU for actual generation; dry run works on CPU) |
| [13_round1i_kinship_operator_repair.ipynb](13_round1i_kinship_operator_repair.ipynb) | Round 1i single-target operator repair: generate an operator-repaired relation-chain consolidation and compare it against the Round 1h revised version on `wiki_dev_2639` only | Yes (GPU for actual generation; dry run works on CPU) |
| [14_round1j_patchback_summary.ipynb](14_round1j_patchback_summary.ipynb) | Round 1j analysis-only notebook: patch the repaired `wiki_dev_2639` relation-chain evidence back into the role-aware interpretation layer and write a synthesis-ready summary | No (CPU) |

Default model recommendation for [04_artifact_generation.ipynb](04_artifact_generation.ipynb):

- Primary: `Qwen/Qwen3.5-9B`
- Fallback on tighter VRAM: `Qwen/Qwen3.5-4B`

Terminal state:

- `01`–`06`: early pipeline + Round 1b diagnosis
- `07`: analysis-only Round 1c summary
- `08`–`10`: relation-chain subtype recovery setup
- `11`–`13`: minimal reruns and operator repair
- `14`: patchback / synthesis only
