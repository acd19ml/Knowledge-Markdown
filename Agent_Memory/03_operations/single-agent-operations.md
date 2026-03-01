# Single-Agent Memory Operations

> Paper Section 4.1 (pages 20–23)

Five core operations that govern how a single agent **actively constructs, updates, controls, and utilizes memory** throughout long-horizon interaction and task execution.

> "Rather than treating memory as a static repository, modern agents manipulate memory through a sequence of operations: indexing, retrieval, updating, compression, summarization, forgetting, and pruning."

---

## Operations Overview

```
[New Experience / Observation]
           ↓
    ┌─────────────┐
    │  1. STORAGE │  ← Write-time: embed, index, organize
    │   & INDEX   │
    └─────────────┘
           ↓
    ┌─────────────┐
    │ 2. LOADING  │  ← Query-time: filter, rank, retrieve
    │ & RETRIEVAL │
    └─────────────┘
           ↓
    ┌─────────────┐
    │ 3. UPDATE   │  ← Revise existing entries, merge, rewrite
    │  & REFRESH  │
    └─────────────┘
           ↓
    ┌──────────────┐
    │ 4. COMPRESS  │  ← Convert fine-grained → compact abstractions
    │ & SUMMARIZE  │
    └──────────────┘
           ↓
    ┌──────────────┐
    │ 5. FORGETTING│  ← Remove obsolete; prioritize high-utility
    │  & RETENTION │
    └──────────────┘
```

---

## 4.1.1 Storage and Index

**Purpose**: Organize information at write time for efficient and reliable later retrieval.

### What Happens

Memory entries are indexed with:
- **Semantic embeddings** (for similarity search)
- **Auxiliary metadata**: timestamps, task identifiers, entities, tool usage

### Storage Format Choices

| Format | Retrieval Method | Best For |
|---|---|---|
| **Vector index** | Approximate nearest-neighbor (ANN) | Semantic similarity; scalable episodic/semantic memory |
| **Structured store** | Relational queries, graph traversal, tree navigation | Relational data; multi-level abstraction; schema-aware access |
| **Text-record** | Keyword matching, lightweight string-based | Transparency; human-readable; controllable |
| **Parametric (implicit)** | Model-internal recall (no explicit retrieval) | Stable background knowledge |
| **KV cache** | Attention mechanism | Within-session working memory |

### Key Principle

> "As memory scales across longer horizons, the choice of storage format and indexing strategy directly affects retrieval precision, computational overhead, and downstream reasoning reliability."

---

## 4.1.2 Loading and Retrieval

**Purpose**: Efficiently find task-relevant memories during ongoing reasoning, while limiting influence of irrelevant/outdated information.

### Two-Stage Process

**Stage 1 — Loading (pre-selection)**:
- Filter by metadata: recency, task scope, memory type
- Lightweight, rule-based

**Stage 2 — Retrieval (semantic ranking)**:
- Similarity-based over vectorized representations
- Further ranked/refined by semantic similarity, heuristic constraints, or budget-aware selection
- Injected into model's prompt or working context

### Retrieval Quality Matters

> "Retrieving excessive memory can introduce noise and context overload, while overly restrictive retrieval may prevent access to critical historical information."

**Goal**: Balance **relevance**, **diversity**, and **context budget** to support coherent long-horizon behavior.

### Research Directions

- Dense retrieval (DPR, RAG-style)
- Sparse retrieval (BM25)
- Hybrid retrieval
- Iterative/progressive retrieval (multi-hop reasoning)
- Budget-aware selection (context window constraints)
- Compression-aware retrieval (retrieve from compressed representations)

---

## 4.1.3 Update and Refresh

**Purpose**: Revise existing memory in response to new observations, feedback, or reflection — allowing memory to **evolve** rather than merely accumulate.

### Update Triggers

- After task completion
- On receiving evaluation signals
- On detecting inconsistencies with stored information
- After agent reflection

### Update Types

| Type | What Changes |
|---|---|
| **Rewrite** | Overwrite semantic summaries with more accurate version |
| **Merge** | Combine overlapping episodic records |
| **Importance adjustment** | Reweight stored information (recency, frequency, impact) |

### Refresh Operations

Adjust **prominence and accessibility** without altering core content:
- Re-rank salient entries
- Regenerate condensed summaries
- Reinforce frequently accessed memories

### Key Pattern

Reflective/self-evaluative processes can **autonomously trigger** both updating and refresh:
- Reflexion (Shinn et al., 2023): explicit self-reflection → memory update
- Ouyang et al. (2025): reasoning bank updated with verified conclusions

> "Together, these mechanisms allow memory representations to evolve dynamically, supporting adaptation in non-stationary environments while mitigating the accumulation of obsolete or misleading information."

---

## 4.1.4 Compression and Summarization

**Purpose**: Regulate memory growth while preserving information essential for future reasoning.

### The Problem

Episodic records grow without bound → redundancy, inefficiency, context overflow

### Compression Strategies

| Strategy | Description | Timing |
|---|---|---|
| **Periodic summarization** | Consolidate interaction histories into compact semantic/hierarchical memory | After task or after N turns |
| **Hierarchical consolidation** | Multi-level / tree-structured representations | Enables scalable retrieval at different abstraction levels |
| **Dynamic Cheatsheet** | Compact, task-adaptive summary continuously updated | Real-time during task execution |
| **Abstractive compression** | Convert fine-grained to high-level (lossy but compact) | On storage |

### Key Tradeoff

> "An inherent trade-off between abstraction fidelity and long-term recall: aggressive summarization improves context utilization and scalability but can permanently lose fine-grained details needed later."

### Representative Works

- MemoryOS (Kang et al., 2025a): hierarchical memory OS-style management
- SeCom (Pan et al., 2025): segment-level context compression
- ACON (Kang et al., 2025c): compression-aware context management
- SUPO (Lu et al., 2025b): progressive summarization under context budget

---

## 4.1.5 Forgetting and Retention

**Purpose**: As task objectives change and environments become non-stationary, manage the trade-off between retaining important information and purging obsolete/low-utility information.

### Forgetting

**Goal**: Reduce influence of obsolete or low-utility information.

**Implementations**:
- **Recency-based decay**: Older items get lower weight/priority (mimics Ebbinghaus forgetting curve)
- **Importance threshold**: Remove entries below relevance score
- **Learned forgetting strategies**: Optimize memory removal under resource/efficiency constraints

### Retention

**Goal**: Preserve high-utility knowledge even under memory growth pressure.

**Mechanisms**:
- Adaptive retention priorities based on task context and feedback signals
- Long-term performance objectives guide which memories to keep
- Dynamic adjustment under non-stationary environments

### Key Insight

> "Indiscriminate memory accumulation is increasingly misaligned with effective long-term reasoning. Memory relevance evolves over time as task objectives change."

### Research Challenge

Learning **when to forget** is harder than learning what to store — requires understanding future information needs.

→ See [Learning Policy: RL for Memory Policies](../04_learning-policy.md#53-reinforcement-learning-for-memory-policies) — RL can be used to learn optimal forgetting policies.

---

## Design Principles for Single-Agent Memory

1. **Context budget awareness**: Every operation must account for finite context windows
2. **Selectivity over completeness**: Not all information deserves the same retention priority
3. **Temporal coherence**: Updates/refreshes should maintain logical consistency across the timeline
4. **Retrieval-storage co-design**: How you store determines what you can retrieve later
5. **Adaptive management**: Static rules fail in dynamic environments; learned policies outperform heuristics

---

## Representative Single-Agent Systems

| System | Key Operations | Domain |
|---|---|---|
| MemGPT (Packer et al., 2023) | OS-style context management: move between main/external context | General dialogue |
| Generative Agents (Park et al., 2023) | Memory stream + reflection + retrieval by recency/importance/relevance | Social simulation |
| Reflexion (Shinn et al., 2023) | Episodic storage + reflective update | Task agents |
| MemoryBank (Zhong et al., 2024) | Explicit memory records + operation-level search | Personalized dialogue |
| A-Mem (Xu et al., 2025e) | Dynamic memory with structured organization and update | User-facing assistant |
| Mem0 (Chhikara et al., 2025) | Production-grade memory layer with selective retention | Commercial assistant |
| D-SMART (Lei et al., 2025) | Structured memory management for long dialogues | Dialogue |
| MemAgent (Yu et al., 2025b) | RL-based joint memory management for long contexts | Information search |
