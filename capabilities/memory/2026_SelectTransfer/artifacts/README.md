# artifacts/

Generated memory artifacts for each source set.

## Expected Structure

```
artifacts/
├── bridge_set_01/
│   ├── episodic_trace.md
│   └── cross_episode_consolidation.md
├── comparison_set_01/
│   ├── episodic_trace.md
│   └── cross_episode_consolidation.md
└── ...
```

## Rules

- One subdirectory per `source_set_id`
- Each must contain both artifact types before entering pilot runs
- All artifacts must pass manual quality review (see [../protocol/pilot-run-checklist.md](../protocol/pilot-run-checklist.md) Section 5)
- Artifacts that leak answers, are empty filler, or are indistinguishable from each other must be rejected
