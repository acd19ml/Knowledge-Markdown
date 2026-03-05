# Comparison Matrix v2 — Format Reference

## Evidence Source Tags

- `[S]` = Inferred from Survey (Stage 0, not verified against original paper)
- `[P]` = Confirmed from original paper (Stage 1, with Section + page number)
- `[S→P]` = Originally from Survey, now updated/confirmed by reading the original paper

## Per-System Entry Format

```markdown
### [System Name]

| Dimension | Value | Evidence Source |
|-----------|-------|-----------------|
| **Source** | [Domain: GUI_Agent / Self_Evolve / Agent_Memory] | — |
| **Task Type** | [Mobile / Web / Desktop / General] | — |
| **Memory Cognitive Type** | [None / Working / Episodic / Semantic / Procedural + qualifier] | `[S]` or `[P]` + citation |
| **Memory Persistence** | [In-task / Cross-task (app-level) / Cross-session / Permanent] | `[S]` or `[P]` + citation |
| **Memory Subject** | [Agent-centric / User-centric / None] | `[S]` or `[P]` + citation |
| **Self-Evolution Type** | [None / Inference-time / Offline Experience / Online Experience / Lifelong] | `[S]` or `[P]` + citation |
| **Evolution Timing** | [In-task (real-time) / Post-task (offline) / Cross-task continuous / Pre-task exploration] | `[S]` or `[P]` + citation |
| **Cross-task Transfer** | [None / Task-level / App-level / Cross-app] | `[S]` or `[P]` + citation |

**Representative Experimental Data**:
| Benchmark | Metric | This System | Strongest Baseline | Δ | Source |
|-----------|--------|-------------|-------------------|---|--------|
| ... | ... | ... | ... | ... | Table X, p.Y |

**Reading Notes**: `[path]` or "Not yet read"
**Last Updated**: YYYY-MM-DD | Reason for update
```

## Dimension Definitions

| Dimension | Source | Valid Values |
|-----------|--------|-------------|
| Memory Cognitive Type | Agent_Memory Survey §3.2 | Sensory / Working / Episodic / Semantic / Procedural (can add qualifiers like "雏形") |
| Memory Persistence | Agent_Memory Survey §2.1 | In-task / Cross-task / Cross-session / Permanent |
| Memory Subject | Agent_Memory Survey §3.3 | Agent-centric / User-centric / None |
| Self-Evolution Type | Self_Evolve Survey §III–IV | None / Inference-time correction / Offline experience / Online experience / Lifelong learning |
| Evolution Timing | Self_Evolve Survey §III–IV | In-task (single-step correction) / Post-task (offline) / Cross-task continuous / Pre-task exploration |
| Cross-task Transfer | Cross-analysis | None / Task-level / App-level / Cross-app |

## Rules

1. Every dimension value in a `[P]`-tagged cell MUST have a paper citation: (Author, Year, §Section, p.Page)
2. If a dimension cannot be determined from the paper, write "未明确提及" with `[P]` tag — this is still valuable information
3. The experimental data table can be left empty if the paper's benchmarks are not comparable to others in the matrix; note why
4. When updating from `[S]` to `[P]`, record what changed (if anything) in "Last Updated"