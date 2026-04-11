# protocol/

Operational "how-to" documents. Reusable across rounds.

This directory now covers two layers of procedure:

- the original pilot-building workflow
- the later Round 1 repair-chain protocols (`bridge` subtype repair, relation-chain feasibility, consolidation/operator repair)

| File | Role |
|---|---|
| [pipeline.md](pipeline.md) | End-to-end pipeline: Phase 0 (setup) through Phase 8 (reproducibility) |
| [taxonomy_guideline.md](taxonomy_guideline.md) | Label definitions: bridge, comparison, temporal, distractor-heavy, drop |
| [csv-field-examples.md](csv-field-examples.md) | Field-by-field examples for all four CSV files |
| [experiment-round-template.md](experiment-round-template.md) | Template for writing per-round experiment specs |
| [first-20-task-sampling-strategy.md](first-20-task-sampling-strategy.md) | How to sample the first 20 tasks (simple random, minimal filtering) |
| [first-20-annotation-workflow.md](first-20-annotation-workflow.md) | How to annotate taxonomy labels on the first 20 tasks |
| [first-source-set-selection-workflow.md](first-source-set-selection-workflow.md) | How to select the first source sets from annotated tasks |
| [expand-hotpotqa-comparison-source-pool.md](expand-hotpotqa-comparison-source-pool.md) | How to expand the HotpotQA source-side pool when comparison coverage is insufficient |
| [first-hotpotqa-comparison-expansion-batch.md](first-hotpotqa-comparison-expansion-batch.md) | The concrete first batch checklist for expanding HotpotQA comparison candidates |
| [first-pairing-workflow.md](first-pairing-workflow.md) | How to construct relevant / irrelevant pairs |
| [pilot-run-checklist.md](pilot-run-checklist.md) | Go / no-go checklist before entering pilot runs |
| [cloud-artifact-generation-upload.md](cloud-artifact-generation-upload.md) | What to upload to a cloud machine before running artifact generation |
| [pilot-prompt-scaffold.md](pilot-prompt-scaffold.md) | Prompt templates for Round 1 pilot: base prompt, memory injection, logging, scoring |
| [pilot-prompt-scaffold-round1b.md](pilot-prompt-scaffold-round1b.md) | Structured reasoning scaffold for Round 1b prompt diagnosis |
| [round1b_pairing_artifact_audit.md](round1b_pairing_artifact_audit.md) | Case-by-case audit checklist for deciding whether Round 1b effects come from pairing, artifact wording, or more plausible memory interaction |
| [bridge-subtype-repair.md](bridge-subtype-repair.md) | How to split coarse `bridge` labels into subtype-aware pairing decisions before any new rerun |
| [expand-relation-chain-bridge-source-pool.md](expand-relation-chain-bridge-source-pool.md) | Feasibility-first workflow for deciding whether HotpotQA can support a minimal `relation_chain_bridge` source set |
| [first-relation-chain-bridge-expansion-batch.md](first-relation-chain-bridge-expansion-batch.md) | The concrete first batch checklist for testing whether relation-chain bridge candidates are abundant enough to justify a new source set |
| [high-precision-relation-chain-bridge-expansion-batch.md](high-precision-relation-chain-bridge-expansion-batch.md) | The final high-precision Batch 2 workflow for deciding whether `relation_chain_bridge` is realistically recoverable in the current HotpotQA source setting |
| [relation-chain-consolidation-repair.md](relation-chain-consolidation-repair.md) | How to isolate and repair the remaining `relation_chain` consolidation failure after subtype-aware reroute has already succeeded for `episodic_trace` |
| [relation-chain-kinship-operator-repair.md](relation-chain-kinship-operator-repair.md) | How to isolate whether the remaining `relation_chain` consolidation failure is specifically a kinship-operator interpretation problem |
| [versioning-convention.md](versioning-convention.md) | Naming and archiving rules for pilot data |

Recommended reading order:

1. `pipeline.md`
2. `taxonomy_guideline.md`
3. `pilot-prompt-scaffold.md` / `pilot-prompt-scaffold-round1b.md`
4. subtype-repair protocols only after Round 1b / 1c signals exist
