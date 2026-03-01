# Self-Evolving Agents — Knowledge Base

> Survey: "A Systematic Survey of Self-Evolving Agents: From Model-Centric to Environment-Driven Co-Evolution"
> PDF: `A_Survey_of_Self_Evolving_Agents.pdf` (26 pages)

---

## Core Thesis

> "Self-Evolving Agents" represents a paradigm shift from static model training to systems that **continuously improve through autonomous interaction** — generating their own training signals, refining strategies, and co-evolving with their environment without perpetual human supervision.

The supervision bottleneck in current AI: SFT limits models to imitation; RL depends on sparse, human-defined rewards. Self-evolution transcends this through **active agency**.

---

## Three-Paradigm Taxonomy

```
Self-Evolving Agents
├── III. Model-Centric Self-Evolution        [pages 5–9]
│   ├── A. Inference-Based (test-time scaling)
│   └── B. Training-Based (data synthesis + RL)
│
├── IV. Environment-Centric Self-Evolution   [pages 9–12]
│   ├── A. Static Knowledge Evolution (RAG, Deep Research)
│   ├── B. Dynamic Experience Evolution (offline/online/lifelong)
│   ├── C. Modular Architecture Evolution (memory, tools, protocols)
│   └── D. Agentic Topology Evolution (MAS design)
│
└── V. Model-Environment Co-Evolution        [pages 10–11]
    ├── A. Multi-Agent Policy Co-Evolution
    └── B. Environment Training (curriculum + scalable envs)
```

**Core tension**: Model-Centric risks model collapse without external verification; Environment-Centric risks stagnation in static environments. Co-Evolution represents the synthesis.

---

## Directory Structure

```
Self_Evolve/
├── README.md                  # This file — navigation hub
├── 00_survey-overview.md      # Paper metadata, key stats, related surveys
├── 01_background.md           # Preliminaries: agent definition, MDP, problem framing
│
├── 02_model-centric/          # Section III: Model-Centric Self-Evolution
│   ├── README.md              # Section overview + comparison table
│   ├── 2.1_inference-based.md # Parallel sampling, self-correction, structured reasoning
│   └── 2.2_training-based.md  # Synthesis-driven offline, exploration-driven online
│
├── 03_env-centric/            # Section IV: Environment-Centric Self-Evolution
│   ├── README.md              # Section overview
│   ├── 3.1_static-knowledge.md  # Agentic RAG, Deep Research
│   ├── 3.2_dynamic-experience.md # Offline/Online/Lifelong experience evolution
│   ├── 3.3_modular-arch.md    # Interaction protocols, memory arch, tool-augmented
│   └── 3.4_agentic-topology.md  # Offline search, runtime adaptation, structural state
│
├── 04_co-evolution.md         # Section V: Model-Environment Co-Evolution
├── 05_applications.md         # Section VI: Scientific Discovery, SWE, Open-World
├── 06_challenges.md           # Section VII: Discussion, Challenges, Future Work
└── 07_benchmarks.md           # Section VIII+IX: Evaluation benchmarks + OSS libraries
```

---

## Quick Navigation

| Topic | File |
|---|---|
| Paper overview & stats | [00_survey-overview.md](00_survey-overview.md) |
| Agent & MDP fundamentals | [01_background.md](01_background.md) |
| Inference-time evolution (test-time scaling) | [02_model-centric/2.1_inference-based.md](02_model-centric/2.1_inference-based.md) |
| Training-based evolution (SFT/RL) | [02_model-centric/2.2_training-based.md](02_model-centric/2.2_training-based.md) |
| Static knowledge evolution (RAG/Deep Research) | [03_env-centric/3.1_static-knowledge.md](03_env-centric/3.1_static-knowledge.md) |
| Dynamic experience evolution | [03_env-centric/3.2_dynamic-experience.md](03_env-centric/3.2_dynamic-experience.md) |
| Memory & tool architecture evolution | [03_env-centric/3.3_modular-arch.md](03_env-centric/3.3_modular-arch.md) |
| Multi-agent topology evolution | [03_env-centric/3.4_agentic-topology.md](03_env-centric/3.4_agentic-topology.md) |
| Model-Environment Co-Evolution | [04_co-evolution.md](04_co-evolution.md) |
| Applications (Science, SWE, Games) | [05_applications.md](05_applications.md) |
| Challenges & Future Frontiers | [06_challenges.md](06_challenges.md) |
| Evaluation benchmarks | [07_benchmarks.md](07_benchmarks.md) |

---

## Key Systems at a Glance

| System | Paradigm | Domain | Mechanism |
|---|---|---|---|
| DeepSeek-R1 | Model-Centric / Training | Math/Reasoning | GRPO + RL |
| Reflexion | Model-Centric / Inference | General | Verbal self-feedback |
| Self-RAG | Env-Centric / Static | Knowledge | Selective retrieval + critique |
| VOYAGER | Env-Centric / Tool-Aug | Gaming | Executable skill library |
| GPTSwarm | Env-Centric / Topology | MAS | Gradient-based graph optimization |
| SWE-agent | Co-Evolution | Software Eng | ACI + error feedback |
| The AI Scientist | Co-Evolution | Science | Auto peer-review loop |
| Generative Agents | Co-Evolution | Social Sim | Observe-Reflect-Plan |
| AlphaProof | Co-Evolution | Math | Lean verifier loop |

---

## Research Extension Notes

- [ ] How does RL reward shaping differ across the three paradigms?
- [ ] What role does the verifier play — and what happens without one?
- [ ] How do offline vs online evolution trade off compute, data, and safety?
- [ ] What's the connection between Self-Evolving Agents and Agent Memory (cross-reference [Agent_Memory/](../Agent_Memory/))?
- [ ] Explore Model Collapse: why does self-training sometimes degrade performance?
