# Scaling: Memory, Contexts, and Environments

> Paper Section 6 (pages 30–33)

As LLMs and agents deploy in increasingly realistic settings, context grows rapidly along **three scaling axes**:
1. **Interaction horizon** — multi-session, multi-month workflows
2. **Environmental complexity** — heterogeneous data, tool states, structured artifacts
3. **System quantity** — multiple agents + human collaborators

---

## The Core Problem

Traditional evaluations use **context-limited, simple environments** — agents interact for short horizons with synthetic users. This yields:
- High benchmark scores (MMLU 90%+, MATH, SWE-bench partial)
- But agents **fail in real-world settings** requiring long-term adaptation, user personalization, or task-specific skill reuse

> "The utility gap: agents that achieve high scores on existing benchmarks frequently fail to exhibit long-term adaptation, user personalization, or task-specific skill reuse in open-ended, dynamic environments."

---

## 6.1 Context-Limited Simple Environments

Most current benchmarks live here — **controlled, episodic, reset-centric**:

| Benchmark Type | Examples | Memory Pressure |
|---|---|---|
| QA (frozen knowledge) | SQuAD, HotpotQA, KILT, MS MARCO, TriviaQA | Minimal — static retrieval, no cross-query state |
| Tool use / Web | ToolBench, WebShop, WorkArena | Low — fixed APIs, abstract away auth/failure/long-term state |
| Sequential/interactive | ScienceWorld, ALFWorld, TextWorld, Jericho | Moderate — episodic, but reset-centric |
| Code/SW engineering | APPS, SWE-bench, SWE-BenchPro, SWE-Lancer | Moderate — within-task state, but no cross-episode knowledge |

**What these miss**: Knowledge accumulation across episodes, long-horizon consistency, evolving preferences.

**Consequence**: Evaluation fails to assess the critical role of memory for robust real-world deployment.

---

## 6.2 Context-Exploded Real-World Environments

Real-world deployments expose agents to **multi-axis context explosion**.

### 6.2.1 Scaling with Interactions

#### User–Agent Long-Horizon Dialogue

Information from early rounds (user preferences, identity, constraints) may not immediately matter but becomes decisive later.

**Failure modes under finite context windows**:
- Early-context forgetting
- Progressive context drift as interaction length increases

**Key insight**: Interaction history functions less as static input and more as a **latent internal state that evolves over time**.

**Existing mitigations** (each with tradeoffs):
| Strategy | Approach | Limitation |
|---|---|---|
| Sliding context windows | Drop oldest context | Permanent loss of early information |
| Heuristic truncation | Keep recent N tokens | Discards potentially crucial early context |
| Summary-based memory | Compress → core summary | Compression can lose fine-grained detail |
| User profiles / persona memory | Explicit long-term structures | May not capture full interaction nuance |

#### Multi-Turn Tool Use Context Explosion

Beyond conversational history, tool-based agents must retain:
- Tool inputs and outputs
- Intermediate execution states (repeatedly referenced in subsequent steps)
- Planning traces + reflective reasoning (ReAct-style)

**Context size growth**: linear or even **exponential** with interaction length in ReAct-style agents.

**Challenge**: Naively removing/compressing tool traces breaks causal dependencies between reasoning and action steps.

---

### 6.2.2 Scaling with Environment Complexity

As environments grow complex, context must accommodate:
- Heterogeneous data modalities
- Asynchronous tool interactions
- Protocol/permission-constrained external state

**Naive flattening** of structured artifacts (API responses, files, databases, logs, configs) into token sequences is:
- Inefficient (excessive tokens)
- Structurally lossy (schema/provenance/temporal validity lost)

**Consequence**: Memory shifts from implicit prompt accumulation to **explicit, system-level component** responsible for structured context management.

#### Externalized Memory Interfaces

Externalized memory enables:
- Schema-aware retrieval
- Versioning
- Targeted edits
- Access control

Key protocols:
- **Model Context Protocol** (Anthropic, 2024) — defines query semantics, update policies, scope boundaries
- **Claude Agent Skills** (Anthropic, 2025) — skill-oriented abstractions for agent–environment state interaction

#### Persistence Requirements

User models, system configurations, and task artifacts represent **durable state** that must:
- Remain consistent across sessions
- Respect governance constraints (privacy, permissions, rollback)

Challenges: schema drift, concurrent updates, path-dependent evaluation.

---

### 6.2.3 Scaling with Environment Quantity

#### Memory as Interface Across Multiple Tool Environments

Real-world agents alternate between multiple heterogeneous environments:
- Physical household environment (perceptual feedback, long-horizon behavior)
- Digital web environment (browser-based information retrieval)
- OS/App environments (GUI interaction across apps)

Memory must:
- Preserve, differentiate, and reconcile environment-specific states
- Maintain structured, separated representations of environment state
- Support long-horizon reasoning without breaking context window

#### Multi-Human-Agent System Memory

As agent systems scale to multiple agents + human participants:
- Naïve context sharing fragments quickly under limited context windows
- Need: agent-aligned or semi-shared memory abstractions encoding relational histories, inter-agent dependencies

**Research directions in this space**:
- Role-specific memory templates preserving specialized perspectives while enabling shared substrate integration
- Hierarchical/role-aware dialogue schemes reducing noise in inter-agent exchanges
- Debate-based protocols with consensus/majority voting for collective decision-making
- Implicit graph-structured representations for organizing relational dependencies

---

## Implications for Memory System Design

| Scaling Axis | Memory Design Requirement |
|---|---|
| Long interaction horizons | Persistent user models; hierarchical summarization; temporal consistency |
| Complex environments | Externalized memory with schema-aware retrieval; versioning; access control |
| Multiple environments | Cross-environment state separation; memory-as-interface pattern |
| Multi-agent + human | Permission-aware routing; role-specific views; conflict resolution |

---

## The Memory Evolution

```
Simple benchmark agents       Real-world deployed agents
(context-limited)         →   (context-exploded)
        │                              │
Simple interaction log     Sophisticated context-management system
        │                              │
Short-term prompt          Long-term personalization
        │                              │
Single-environment         Cross-environment state management
        │                              │
Single agent               Multi-agent coordination + human collaboration
```

Memory transforms from a simple buffer into the **architectural backbone** that enables robust, long-horizon, user-dependent agent behavior.

---

## Connection to Research Challenges

→ [08_future-directions.md §3: Memory Infrastructure and Efficiency](08_future-directions.md#3-memory-infrastructure-and-efficiency) — how to scale memory without unbounded token cost
→ [08_future-directions.md §2: Multi-Human-Agent Memory Organization](08_future-directions.md#2-multi-human-agent-memory-organization) — coordination at scale
→ [06_evaluation.md](06_evaluation.md) — why current benchmarks fail to capture real-world memory demands
