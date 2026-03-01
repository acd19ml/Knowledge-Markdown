# Model-Centric Self-Evolution — Overview

> Paper Section III (pages 5–9)

---

## Section Overview

Model-Centric Self-Evolution focuses on improving agent capabilities **within the model itself** — either at inference time (without weight updates) or via training (with weight updates). The environment plays a passive, static role; the agent drives improvement through internal computation.

```
Model-Centric Self-Evolution
├── A. Inference-Based [→ 2.1_inference-based.md]
│   ├── Parallel Sampling (width)
│   ├── Sequential Self-Correction (depth)
│   └── Structured Reasoning (search)
└── B. Training-Based [→ 2.2_training-based.md]
    ├── Synthesis-Driven Offline (Table I)
    └── Exploration-Driven Online (RL)
```

---

## Paradigm Comparison

| Sub-paradigm | Weight Update? | Environment Needed? | Signal Source | Ceiling |
|---|---|---|---|---|
| Inference-Based | No | Minimal | Self-generated | Context window + base model capacity |
| Training-Based (Offline) | Yes | Static | Synthesized data | Base model initial capacity |
| Training-Based (Online) | Yes | Required | Environment feedback | Environment complexity |

---

## Key Limitation: Model Collapse Risk

> "Synthesis-Driven Offline Evolution serves as an efficient bootstrapper by consolidating internal priors; however, it remains fundamentally bounded by the base model's initial capacity, risking model collapse where internal feedback loops amplify hallucinations without introducing new information entropy."

**Model Collapse**: When iterative self-training on model-generated data progressively:
- Narrows output distribution
- Loses long-tail information
- Reduces linguistic and strategic diversity
- Amplifies systematic errors

**Prevention**: External environmental feedback (→ Environment-Centric and Co-Evolution paradigms)
