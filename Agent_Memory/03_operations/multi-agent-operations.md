# Multi-Agent Memory Operations

> Paper Section 4.2 (pages 23–26)

In multi-agent systems, memory operations extend beyond single-agent management to handle **cross-agent read/write coordination**, routing, isolation, and conflict resolution.

> "What matters more in multi-agent settings is cross-agent read and write rules: which memory is appropriate for agents with different roles, and how to remove redundancy, resolve conflicts, and keep memory consistent."

---

## Three Key Problems in Multi-Agent Memory

1. **Architecture**: Where does memory live? Who can read/write it?
2. **Routing**: How is appropriate memory selected and injected for each agent/role?
3. **Isolation & Conflicts**: How do we prevent inconsistency when multiple agents update shared state?

---

## 4.2.1 Memory Architecture

Defines **where memory resides** and **what permissions** agents have to read/write.

### Architecture Types

#### Private-Only

Each agent has its own independent memory. Read/write rights apply only within that agent's memory.

```
Agent A          Agent B          Agent C
[Private Memory] [Private Memory] [Private Memory]
      ↕                ↕                ↕
   (task A)         (task B)         (task C)
```

**Properties**:
- Strong isolation → easier to verify behavior
- Same memories often recreated in multiple private spaces → resource waste
- Collaboration only through explicit information exchange (selected viewpoints, not full memory dump)

**Representative**:
- RecAgent: one agent per user, private memory prevents history mixing → privacy
- TradingGPT: each trading agent maintains private memory for consistent risk preference
- MetaAgents: each role has isolated past thoughts/decisions → role stability

---

#### Shared-Workspace

All agents read from and write to a **common memory pool**.

```
           Shared Memory Pool
          ┌─────────────────┐
          │ Results, State  │
          │ Intermediate    │
          │ Artifacts       │
          └─────────────────┘
         ↗    ↗    ↗    ↗
  Agent A  B   C   D  (all read/write)
```

**Properties**:
- Reduces peer-to-peer messaging overhead
- Shared pool can quickly become noisy → needs filtering mechanisms
- Coordination required to avoid conflicts on simultaneous updates

**Representative**:
- MetaGPT (Hong et al., 2023): role agents filter the shared pool using role profiles — each agent pulls only relevant memory
- InteRecAgent: Candidate Bus — tools repeatedly read/write filtered candidates → progressively narrowed to avoid prompt overflow
- MAICC: shared experience pool + online replay buffer → agents query with sub-trajectory, retrieve top-k similar

---

#### Hybrid

Both private + shared layers. A policy decides whether new information → private or shared. Build permission-limited memory views.

```
       Private Layer        Shared Layer
       ┌──────────┐        ┌──────────────┐
Agent A│ private  │←──────→│ shared       │
       └──────────┘  write │ knowledge    │
       ┌──────────┐  policy│              │
Agent B│ private  │←──────→│              │
       └──────────┘        └──────────────┘
```

**Properties**:
- Balance memory reuse and sensitive information isolation
- Write policy: "is this generally useful or user-specific?" → route accordingly
- Read policy: access graph defines permission-limited view per agent

**Representative**:
- Collaborative Memory (Rezazadeh et al., 2025a): write policy + read policy with access graph
- MirrorMind (Zeng et al., 2025): each AuthorAgent has private memory (research interests) + public shared disciplinary knowledge → AI Scientist structure

---

#### Orchestrated

Introduces an **explicit controller** that coordinates agents and mediates memory access in a hierarchical workflow.

```
         ┌─────────────────┐
         │   Orchestrator  │  ← Decomposes tasks, assigns subtasks,
         │   (Controller)  │    decides memory routing
         └─────────────────┘
              ↙   ↓   ↘
         Agent A  B   C  (worker agents)
         [role-specific memory views]
```

**Properties**:
- Centralized coordination → well-suited for multi-stage workflows
- Potential bottleneck; single point of failure
- Orthogonal to storage layout — can combine with private/shared/hybrid

**Representative**:
- ChatDev (Qian et al., 2024a): ChatChain (design→coding→testing), stage outputs as structured handoffs
- MIRIX (Wang & Chen, 2025): MetaMemoryManager routes updates/retrievals to specialized MemoryManagers
- MGA: Planner as controller, lower-level agents submit to shared workspace, planner selects what to inject

---

## 4.2.2 Memory Routing

Given an architecture, routing defines **which past memories are retrieved and how they are injected** into each agent's context for a given task.

### Three Routing Approaches

#### Orchestrator-Based Routing

**Central orchestrator makes all routing decisions.**

```
Orchestrator maintains global task state
    ↓ decomposes task
    ↓ assigns subtasks to role agents
    ↓ distributes required memory
    ↓ decides execution order
    ↓ updates dynamically as state changes
```

**Properties**: Centralized global workflow; risk of orchestrator becoming bottleneck/single point of failure.

**Representative**:
- LEGOMem: orchestrator generates next subtask → selects agent → updates state from summary; memory injected by orchestrator
- GameGPT: manager defines pipeline, each stage writes key outputs to shared workspace P_t
- Westhäußer et al. (2025): MCP-based orchestrator selects memory sources to call; Self-Validator requests more retrieval if needed

---

#### Agent-Initiated Routing

**Each agent decides locally what memory to retrieve, based on role and task.**

```
Shared memory pool
    ↓ (published by agents)
Each agent applies constraint mechanisms
    ↓ (filters based on role/task)
Agent-specific memory view constructed
```

**Properties**: More flexible; depends on good filtering design; can miss important information if filtering is poor.

**Representative**:
- SRMT: personal memory vector + cross-attention over shared memory sequence; each agent decides how much to read
- S3 (Gao et al., 2023): platform-wide message stream → scored by forgetting/relevance/source credibility factors → small subset retained per agent
- Talker-Reasoner (Christakopoulou et al., 2024): Talker reads from shared store written by Reasoner; Talker decides when to read or wait for update

---

#### Memory-Driven Routing

**Retrieval from the memory store itself determines routing.**

```
Current task as query
    ↓
Memory store: retrieve → score → rerank → select
    ↓ (optionally expand via graph links)
Inject relevant memory subset into agent context
```

**Properties**: Retrieval quality drives routing quality; graph expansion can enrich results.

**Representative**:
- G-Memory (Zhang et al., 2025c): multi-agent histories as hierarchical graph → retrieve relevant nodes → expand via neighborhood → compress into core subgraph → trim to role-specific views
- CRMWeaver (Lai et al., 2025): route at guideline level — retrieve most relevant workflow guideline from past successes; write back new guideline when no match
- Spark (Tablan et al., 2025): each coding problem as query → retrieval agent analyzes intent → selects relevant documentation + experience traces

---

## 4.2.3 Memory Isolation and Conflicts

When multiple agents write to shared memory, **consistency conflicts** arise:
- Different agents may write contradictory facts
- Outdated information may not be removed
- Parallel writes may overwrite each other's updates

### Approach 1: Write Control for Memory Isolation

**Enforce isolation at write/update stage.**

**Mechanism**: Compare newly extracted facts against existing memory state → selective update via controlled evaluation.

**Memory-R1 (Yan et al., 2025b)** — memory manager agent is the **only** agent allowed to mutate memory, using four atomic editing actions:

| Action | When Used |
|---|---|
| **ADD** | New entry, not already covered |
| **UPDATE** | New info refines/corrects existing; keep version with more information |
| **DELETE** | New evidence clearly contradicts or makes obsolete |
| **NOOP** | Info already covered or not important for long-term memory |

**WebCoach**: memory store updated only **after episode completion** → partial trajectories never written → no mid-episode conflicts

---

### Approach 2: Feedback Loop for Memory Consistency

**Treat conflicts as an iterative optimization problem.**

```
Multi-agent system
    ├── Constraint Memory: hard requirements that persist across iterations
    │      (new iterations must satisfy these constraints)
    └── Feedback Memory: failures from earlier rounds
           (used to improve subsequent iterations)
```

**EvoMem (Fan et al., 2025b)**:
- Verifier compares candidate solutions against stored constraint memory
- Outputs a score
- System accepts solution only when score = 100 (all constraints satisfied)

---

## Comparison: Single vs. Multi-Agent Memory Operations

| Operation | Single-Agent | Multi-Agent Extensions |
|---|---|---|
| Storage | Write to own memory | Write to private/shared memory; routing decision required |
| Retrieval | Query own memory | Query own + shared; permission-limited views |
| Update | Revise own entries | Must coordinate with other agents; write control or feedback loops |
| Compression | Compress own context | Compress shared pool; avoid losing cross-agent knowledge |
| Forgetting | Remove from own memory | Shared memory pruning requires consensus or orchestrator decision |

---

## Representative Multi-Agent Systems

| System | Architecture | Routing | Conflict Handling |
|---|---|---|---|
| MetaGPT | Shared workspace | Agent-initiated (role profile filter) | Role-based filtering |
| ChatDev | Orchestrated | Orchestrator-based | Stage handoffs |
| MIRIX | Orchestrated + hierarchical | Orchestrator (MetaMemoryManager) | Specialized managers |
| Collaborative Memory | Hybrid | Write/read policy | Access graph (permission-limited) |
| G-Memory | Shared (graph) | Memory-driven | Graph structure maintains consistency |
| Memory-R1 | Orchestrated | Agent memory manager | Atomic CRUD actions |
| SRMT | Private + shared | Agent-initiated (cross-attention) | Personal memory vector isolation |
| MAICC | Shared (experience pool) | Memory-driven (trajectory similarity) | Separate online/offline buffers |
