# notebooks/

Colab notebooks for each experiment phase. Run on Google Colab (GPU for agent runs, CPU for data prep).

| Notebook | Phase | GPU needed? |
|---|---|---|
| [01_sampling.ipynb](01_sampling.ipynb) | Sample first 20 tasks from HotpotQA + 2WikiMultiHopQA | No (CPU) |
| [02_hotpotqa_comparison_expansion.ipynb](02_hotpotqa_comparison_expansion.ipynb) | Expand the first HotpotQA comparison candidate batch for source-set construction | No (CPU) |
| [03_delayed_reannotation_review.ipynb](03_delayed_reannotation_review.ipynb) | Export delayed re-annotation subset, compare second-pass labels, and detect affected source sets / pairs | No (CPU) |
| [04_artifact_generation.ipynb](04_artifact_generation.ipynb) | Generate `episodic_trace` and `cross_episode_consolidation` from frozen Round 1 source sets with local Hugging Face inference | Yes (GPU recommended for actual generation; prompt preview can run on CPU) |
| [05_pilot_run.ipynb](05_pilot_run.ipynb) | Round 1 pilot: compare `no_memory` / `episodic_trace` / `cross_episode_consolidation` on 10 targets × 2 splits | Yes (GPU for local inference; or API mode) |
| [06_round1b_prompt_diagnosis.ipynb](06_round1b_prompt_diagnosis.ipynb) | Round 1b smoke subset: structured `## Reasoning` + `## Final Answer` prompt diagnosis on 6 targets × 3 conditions × 2 splits | Yes (GPU for actual generation; dry run works on CPU) |

Default model recommendation for [04_artifact_generation.ipynb](04_artifact_generation.ipynb):

- Primary: `Qwen/Qwen3.5-9B`
- Fallback on tighter VRAM: `Qwen/Qwen3.5-4B`
