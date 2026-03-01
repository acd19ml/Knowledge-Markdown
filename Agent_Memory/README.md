# Agent Memory — Knowledge Base

> Based on: **"Rethinking Memory Mechanisms of Foundation Agents in the Second Half: A Survey"**
> Authors: Wei-Chieh Huang, Weizhi Zhang, Yueqing Liang et al. (50+ authors across UIC, UIUC, Stanford, Google, Salesforce, Meta, etc.)
> arXiv: [2502.06250](https://arxiv.org/abs/2506.02250) | GitHub: [AgentMemoryWorld/Awesome-Agent-Memory](https://github.com/AgentMemoryWorld/Awesome-Agent-Memory)
> Published: Feb 2026 | Covers: 218 papers (2023 Q1 – 2025 Q4)

---

## Why Memory Matters Now

The field is entering the **"second half"** of AI — shifting from benchmark scores to real-world utility. Real-world agents face:
- **Context explosion**: long-horizon tasks, multi-session workflows, evolving environments
- **User-dependence**: personalization over months/years, preference drift
- **Multi-agent coordination**: shared state, routing, conflict resolution

Memory is the critical solution. 218 papers in 2 years, with exponential growth in 2025.

---

## Knowledge Base Structure

```
Agent_Memory/
├── README.md                        ← You are here (index & overview)
│
├── 00_survey-overview.md            ← Paper metadata, abstract, taxonomy diagram
├── 01_background.md                 ← Foundation agents, memory concepts, cognitive science roots
│
├── 02_taxonomy/
│   ├── README.md                    ← Taxonomy overview + cross-reference table
│   ├── 2.1_memory-substrates.md     ← External vs Internal storage (where memory lives)
│   ├── 2.2_cognitive-mechanisms.md  ← Sensory / Working / Episodic / Semantic / Procedural
│   └── 2.3_memory-subjects.md       ← User-centric vs Agent-centric memory
│
├── 03_operations/
│   ├── single-agent-operations.md   ← Store, Retrieve, Update, Compress, Forget
│   └── multi-agent-operations.md    ← Architecture, Routing, Isolation & Conflicts
│
├── 04_learning-policy.md            ← How agents learn memory policies (Prompting / SFT / RL)
├── 05_scaling.md                    ← Scaling challenges: context-limited vs real-world
├── 06_evaluation.md                 ← Metrics + 30+ benchmarks with annotations
├── 07_applications.md               ← 11 application domains with representative works
└── 08_future-directions.md          ← 6 open challenges for next-gen memory research
```

---

## Quick Navigation

| Question | Go To |
|---|---|
| What types of memory storage exist? | [2.1 Memory Substrates](02_taxonomy/2.1_memory-substrates.md) |
| How do cognitive memory types map to agents? | [2.2 Cognitive Mechanisms](02_taxonomy/2.2_cognitive-mechanisms.md) |
| Who does memory serve — user or agent? | [2.3 Memory Subjects](02_taxonomy/2.3_memory-subjects.md) |
| How does a single agent manage memory? | [3.1 Single-Agent Operations](03_operations/single-agent-operations.md) |
| How do multi-agent systems share memory? | [3.2 Multi-Agent Operations](03_operations/multi-agent-operations.md) |
| How do agents learn memory policies? | [4. Learning Policy](04_learning-policy.md) |
| What benchmarks evaluate memory? | [6. Evaluation](06_evaluation.md) |
| Which domains use agent memory? | [7. Applications](07_applications.md) |
| What are the open research problems? | [8. Future Directions](08_future-directions.md) |

---

## Three-Dimensional Taxonomy (at a glance)

```
Foundation Agent Memory
        │
        ├── Memory Substrate (WHERE / HOW stored)
        │       ├── External: Vector Index, Text-Record, Structural Store, Hierarchical Store
        │       └── Internal: Weights, Latent-State, KV Cache
        │
        ├── Cognitive Mechanism (WHAT FUNCTION it serves)
        │       ├── Short-term: Sensory Memory, Working Memory
        │       └── Long-term:  Episodic Memory, Semantic Memory, Procedural Memory
        │
        └── Memory Subject (WHO it serves)
                ├── User-Centric: personalization, preference, dialogue history
                └── Agent-Centric: task trajectories, skills, domain knowledge
```

---

## Key Stats from the Survey

- **218 papers** analyzed (2023 Q1 – 2025 Q4)
- **Exponential growth** in 2025 Q3–Q4
- External memory dominates (~60% of works)
- Episodic and semantic memory most common cognitive types
- Evaluation gap: most benchmarks test short-horizon; real-world needs long-horizon memory metrics

---

## Extension Roadmap (for future notes)

- [ ] Deep-dive: Specific systems (MemGPT, Generative Agents, Reflexion, Mem0)
- [ ] Deep-dive: Retrieval-Augmented Generation (RAG) and its evolution into agent memory
- [ ] Deep-dive: Memory + Continual Learning
- [ ] Paper-by-paper reading notes linked from benchmark table in `06_evaluation.md`
- [ ] Code implementations and experiments
