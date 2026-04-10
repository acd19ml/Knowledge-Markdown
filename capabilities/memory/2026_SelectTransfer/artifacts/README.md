# artifacts/

Generated memory artifacts for each source set.

## Expected Structure

```
artifacts/
├── round1_artifact_generation_manifest.csv
├── hp_bridge_set_01/
│   ├── prompt_episodic_trace.md
│   ├── prompt_cross_episode_consolidation.md
│   ├── episodic_trace.md
│   └── cross_episode_consolidation.md
├── hp_comparison_set_01/
│   ├── prompt_episodic_trace.md
│   ├── prompt_cross_episode_consolidation.md
│   ├── episodic_trace.md
│   └── cross_episode_consolidation.md
└── ...
```

## Rules

- One subdirectory per `source_set_id`
- Prompt preview files may be generated before actual artifacts
- `round1_artifact_generation_manifest.csv` records whether each artifact is still `prompt_only` or already `generated`
- Each must contain both artifact types before entering pilot runs
- All artifacts must pass manual quality review (see [../protocol/pilot-run-checklist.md](../protocol/pilot-run-checklist.md) Section 5)
- Artifacts that leak answers, are empty filler, or are indistinguishable from each other must be rejected

## Current Workflow

1. Run [../notebooks/04_artifact_generation.ipynb](../notebooks/04_artifact_generation.ipynb)
2. Check prompt previews first
3. In Colab or another GPU environment, use local Hugging Face inference to generate:
   - `episodic_trace.md`
   - `cross_episode_consolidation.md`
4. Review the two artifact types manually before any pilot run

Current default backend:

- `huggingface_transformers`
- Primary model: `Qwen/Qwen3.5-9B`
- Fallback model: `Qwen/Qwen3.5-4B`
