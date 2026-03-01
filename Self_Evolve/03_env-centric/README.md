# Environment-Centric Self-Evolution — Overview

> Paper Section IV (pages 9–12)

---

## Section Overview

Environment-Centric Self-Evolution treats the **external environment** as the primary driver of agent improvement. Rather than optimizing purely internal processes, agents improve by structuring how they interact with, retrieve from, and adapt to their operational context.

```
Environment-Centric Self-Evolution
├── A. Static Knowledge Evolution   [→ 3.1_static-knowledge.md]
│   └── Environment = knowledge base (RAG, Deep Research)
│
├── B. Dynamic Experience Evolution [→ 3.2_dynamic-experience.md]
│   └── Environment = experience repository (offline/online/lifelong)
│
├── C. Modular Architecture Evol.   [→ 3.3_modular-arch.md]
│   └── Environment = optimizable interface (memory, tools, protocols)
│
└── D. Agentic Topology Evolution   [→ 3.4_agentic-topology.md]
    └── Environment = multi-agent collective (team design)
```

---

## Key Distinction from Model-Centric

| Aspect | Model-Centric | Environment-Centric |
|---|---|---|
| What evolves | Internal model parameters/reasoning | How agent interacts with external world |
| Signal source | Self-generated | Environment-provided |
| Ceiling | Base model capacity | Environment complexity |
| Risk | Model collapse | Environment lock-in |

---

## Four Sub-Paradigms at a Glance

| Sub-paradigm | Environment Role | Key Systems |
|---|---|---|
| Static Knowledge | Information repository bridging knowledge gaps | Self-RAG, FLARE, MindSearch, WebThinker |
| Dynamic Experience | Gymnasium for refining strategies via trajectories | AWM, SkillWeaver, VOYAGER, FLEX |
| Modular Architecture | Optimizable structural components | MemGPT, A-MEM, ReAct, CREATOR, Alita |
| Agentic Topology | Multi-agent collective to optimize | GPTSwarm, AFLOW, ADAS, AutoAgents |

---

## The Static-to-Dynamic Progression

> "Relying solely on one-way extraction from a fixed environment eventually bounds agent improvement by the environment's inherent complexity. The agent-environment relationship must shift from passive extraction to reciprocal interaction."

```
Static Knowledge          Dynamic Experience         Co-Evolution
(what IS in the world)  → (how TO DO in the world) → (environment ADAPTS with agent)
     RAG                        RL/Trajectories           Adaptive Curriculum
```

This progression motivates the **Model-Environment Co-Evolution** paradigm (→ [04_co-evolution.md](../04_co-evolution.md)).
