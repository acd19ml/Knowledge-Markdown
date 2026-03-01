# Taxonomy of Memory in Foundation Agents

> Paper Section 3 (pages 8–20) | 218 papers surveyed

---

## Three Orthogonal Dimensions

The survey categorizes memory along **three independent axes**, each answering a different design question:

| Axis | Question | File |
|---|---|---|
| **Memory Substrate** | *Where / in what form* is memory stored? | [2.1_memory-substrates.md](2.1_memory-substrates.md) |
| **Cognitive Mechanism** | *What function* does memory serve in the pipeline? | [2.2_cognitive-mechanisms.md](2.2_cognitive-mechanisms.md) |
| **Memory Subject** | *Whose information* is memory designed to capture? | [2.3_memory-subjects.md](2.3_memory-subjects.md) |

---

## Full Taxonomy Map (Figure 4 in paper)

```
Foundation Agent Memory System
│
├── Memory Substrates (§3.1)
│   ├── External Memory (§3.1.1)
│   │   ├── Vector Index        — RAG-style, embedding similarity
│   │   ├── Text-Record         — Human-readable summaries + episodic logs
│   │   ├── Structural Store    — Relational tables, knowledge graphs, trees
│   │   └── Hierarchical Store  — Multi-module (episodic + semantic + procedural + ...)
│   └── Internal Memory (§3.1.2)
│       ├── Weights             — Parametric knowledge (continual learning, model editing)
│       ├── Latent-State        — Hidden activations, inference-time state
│       └── KV Cache            — Per-layer attention keys/values
│
├── Cognitive Mechanisms (§3.2)
│   ├── Short-Term
│   │   ├── Sensory Memory (§3.2.1)  — Perceptual buffer, temporal gating
│   │   └── Working Memory (§3.2.2)  — Active context, KV state management
│   └── Long-Term
│       ├── Episodic Memory (§3.2.3) — Episode recording, contextual retrieval
│       ├── Semantic Memory (§3.2.4) — Knowledge graphs, facts, schemas
│       └── Procedural Memory (§3.2.5)— Skills, workflows, action policies
│
└── Memory Subjects (§3.3)
    ├── User-Centric (§3.3.1)   — Dialogue, personalization, preference
    └── Agent-Centric (§3.3.2)  — Task trajectories, skills, domain knowledge
```

---

## Representative Works by Category

| Category | Key Systems |
|---|---|
| External Memory | S3, Memolet, MemTree, R3Mem, SeCom, Egolife |
| Internal Memory | vLLMPA, ChemDFM, MemoryLLM, MAC, WISE, Titans, LMLM |
| Sensory | UBSLLM, LightMem, M2PA, HMT, VIPeR |
| Working | RAP, FOT, ATFS, MemReasoner, ChunkKV, LM2, ACON |
| Episodic | Synapse, AgentCF, WarAgent, COMEDY, MemoryOS, Nemori |
| Semantic | ChatDB, FinMem, QuantAgent, Meminsight, CAM, MoM |
| Procedural | MetaGPT, G-Memory, MIRIX, Memp, ReasoningBank, BREW |
| User-Centric | RoleLLM, MAUMB, MemoCRS, RET-LLM, Zep, A-Mem, Echo |
| Agent-Centric | JARVIS-1, BoT, AWM, HippoRAG2, Cognee, Branch-and-Browse |

---

## Cross-Dimension Interactions

These three dimensions are **orthogonal but interact**:

- A **vector store** (substrate: external) can hold **episodic memories** (mechanism) for a **user** (subject)
- **Model weights** (substrate: internal) encode **semantic knowledge** (mechanism) used for **agent reasoning** (subject)
- **KV cache** (substrate: internal, latent) supports **working memory** (mechanism) during **single-agent task** execution

---

## Tradeoffs Across Substrates (§3.1.3)

| Substrate | Speed | Scalability | Updatability | Best For |
|---|---|---|---|---|
| Parametric (Weights) | Fast recall | Fixed size | Expensive retraining | Stable, general knowledge |
| Latent State (hidden/KV) | Very fast | Limited (linear w/ seq length) | Ephemeral | Within-session state |
| External (vector/text/graph) | Slower (retrieval latency) | Highly scalable | Easy edit/update | Long-term experience |

> **No single substrate dominates.** Effective systems adopt **hybrid architectures**: parametric for general knowledge, latent for fast short-term reasoning, external for scalable experience storage.
