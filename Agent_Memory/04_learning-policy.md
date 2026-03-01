# Memory Learning Policy

> Paper Section 5 (pages 26–30)

How agents **learn to manage memory** — what to store, when to store it, how to represent it, when to retrieve or discard it — rather than relying on fixed, hand-crafted heuristics.

> "Learning policy refers to how an agent learns to manage memory: what to store, when to store it, how to represent it, when to retrieve or discard it, and where to store or retrieve — rather than relying on fixed, hand-crafted heuristics. Such policies are typically optimized from data or feedback (e.g., supervised signals, reinforcement learning, or self-improvement)."

---

## Three Paradigms

| Paradigm | Learning Signal | Key Advantage | Key Limitation |
|---|---|---|---|
| **Prompting** | Natural language instructions (no gradient updates) | No expensive fine-tuning; highly interpretable | No explicit credit assignment; limited long-term optimization |
| **Fine-tuning (SFT)** | Supervised labels / curated data | Stable, reusable memory behaviors embedded in weights | Fixed after training; no adaptation to new rewards |
| **Reinforcement Learning** | Task outcome rewards / interaction feedback | Explicit credit assignment; downstream task outcomes shape memory decisions | Sample efficiency; reward design complexity |

---

## 5.1 Prompt-Based Memory Learning

Parameterizes memory policy as **natural language prompts**. The agent executes these prompts to determine when to access, modify, or prune memory.

**Advantages**: No fine-tuning required; highly interpretable.

### 5.1.1 Static Prompt-Based Control

Fixed, human-designed rules that remain **invariant during execution**. Memory decisions are specified at design time.

Three design targets:

#### A. Static Memory OS and Organization
Treat memory as a structured container with enforced hierarchical partitioning, indexing, summarization, or schema-based representations.

| System | Approach |
|---|---|
| SCM (Wang et al., 2023a) | Structured context management |
| MemGPT (Packer et al., 2023) | OS-style paging between main and external context |
| LiCoMemory (Huang et al., 2025e) | Hierarchical long-context memory |
| MemoChat (Lu et al., 2023) | Structured memo writing via instruction tuning |
| A-Mem (Xu et al., 2025e) | Dynamic structured memory organization |
| D-SMART (Lei et al., 2025) | Structured memory for long dialogues |
| MemWeaver | Multi-component memory weaving |
| Zep (Rasmussen et al., 2025) | Production memory infrastructure |

#### B. Static Memory Control in Single-Agent Settings
Access and retention constrained by **persona identities or domain-specific priors** encoded in prompts.

| System | Domain |
|---|---|
| RoleLLM (Wang et al., 2024e) | Role-playing with persona-consistent memory |
| ChatHaruhi (Li et al., 2023a) | Character simulation |
| WarAgent (Hua et al., 2023) | Multi-agent simulation with role-based memory |
| MemoTime (Tan et al., 2025b) | Temporal memory for long-term agents |
| FinMem (Yu et al., 2025e) | Financial domain memory |
| TradingGPT (Li et al., 2023b) | Trading-specific memory management |
| MemoCRS (Xi et al., 2024) | Conversational recommendation |

#### C. Static Memory Assignment in Multi-Agent Settings
Memory distributed across agents through predefined roles, modular decomposition, structured communication protocols.

| System | Approach |
|---|---|
| MIRIX (Wang & Chen, 2025) | Hierarchical memory manager |
| LEGOMem (Han et al., 2025) | Modular memory with orchestrator |
| G-Memory (Zhang et al., 2025c) | Graph-based multi-agent memory |
| GameGPT (Chen et al., 2023) | Multi-agent game development memory |
| ChatDev (Qian et al., 2024a) | Role-based development workflow |

---

### 5.1.2 Dynamic Prompt-Based Control

Memory policies **adapted at test time** based on experience and feedback — without updating model parameters.

Key research questions:

#### A. Memory Usage Policy Correction via Reflection
Can memory policies be corrected through reflection on past outcomes?
- Agent analyzes failures/successes → converts insights into revised memory instructions → guides future behavior
- Systems: **Reflexion** (Shinn et al., 2023), ReasoningBank (Ouyang et al., 2025), WebCoach, QuantAgent

#### B. Dynamic Optimization of Memory Representations
Can memory representations themselves be dynamically optimized for efficiency under limited context budgets?
- Compression, denoising, structural reorganization as adaptive, prompt-driven processes
- Systems: ACON, ACE, SeCom, Nemori, CAM, EvoMem, ViLoMem

#### C. Distilling Accumulated Experience into Reusable Procedural Knowledge
Can dynamic prompting distill experiences into reasoning templates, execution scripts, or tool-usage strategies?
- Systems: BoT (Yang et al., 2024b), Memp (Fang et al., 2025b), ToolMem (Xiao et al., 2025)

**Limitation**: Language-mediated; lacks explicit credit assignment → limited capacity for long-term policy optimization vs. fine-tuning/RL.

---

## 5.2 Fine-Tuning: Parameterized Memory Policies

**SFT internalizes memory policies into model parameters**, enabling more stable and reusable memory behaviors.

> "SFT-based approaches investigate how memory policies are internalized, stabilized, and executed efficiently once embedded into model weights."

### 5.2.1 Policy Internalization into Parameters

Memory control as a **parametric policy** — not context manipulation.

| Research Direction | Approach | Representative |
|---|---|---|
| Internalize memory content | Distill short-term context into long-term parametric representations | MemoryLLM (Wang et al., 2024m), SELF-PARAM (Wang et al., 2025o) |
| Internalize memory access/retrieval behaviors | Learn parameterized interfaces mediating interaction with external memory | Memory3 (Yang et al., 2024a), MLP Memory (Wei et al., 2025c) |
| Hierarchical parameterized memory policy | Scalable invocation of large memory; decouple long-tail knowledge from core reasoning | PHM (Pouransari et al., 2025) |

### 5.2.2 Parameterized Policy Stabilization and Boundary Control

Supervision used to **regularize memory updates and enforce boundary constraints** — preventing error accumulation, concept drift, persona inconsistency.

| Direction | Mechanism | Representative |
|---|---|---|
| Reflection before committing | Train models to reflect/self-analyze → store high-level, noise-resistant representations | TIM (Liu et al., 2023b), LearntoMemorize, COMEDY |
| Error/staleness repair | Learn when to revise or override existing knowledge | WISE (Wang et al., 2024f), SuperIntelliAgent, CRMWeaver |
| Defensive boundary control | Restrict which experiences can be retained/reused (role/identity consistency) | Character-LLM (Shao et al., 2023) |

### 5.2.3 Parameterized Policy Efficiency and Retrieval Refinement

SFT to refine **how memory policies execute at inference time** — particularly for memory reading and retrieval.

| Direction | What's Learned | Representative |
|---|---|---|
| Precise retrieval cues | Generate targeted queries for memory access | MemoRAG (Qian et al., 2025b) |
| Multi-hop / progressive retrieval | Refine queries across reasoning steps | MemReasoner (Ko et al., 2024) |
| Compression-aware retrieval | Internalize/reversibly refine compressed memory representations | MemoryDecoder (Cao et al., 2025b), SUPO |

**Limitation**: Resulting policies are fixed after training; no credit assignment over extended decision horizons.

---

## 5.3 Reinforcement Learning for Memory Policies

RL enables memory policies to be optimized through **interaction and reward feedback** — downstream task outcomes influence earlier memory decisions.

> "Unlike prompt-based or supervised approaches, RL allows downstream task outcomes to influence earlier memory-related decisions, making memory construction itself a learnable policy."

Three temporal scopes, from shortest to longest:

### 5.3.1 Step-Level Memory Decisions

RL applied to individual **step-level memory operations** (short-horizon scope).

**Formulation**: Memory management as a sequence of step-level decisions, each selected by a learning policy and optimized based on immediate/short-horizon task reward.

| System | Approach |
|---|---|
| **Memory-R1** (Yan et al., 2025b) | Atomic memory operations (ADD/UPDATE/DELETE/NOOP) learned via task-level rewards |
| **MemAct** (Zhang et al., 2025n) | Finer-grained editing (trimming, summarization) integrated into unified agent policy space |
| **MemAgent** (Yu et al., 2025b) | Learn which info to write into fixed-size memory buffer for extremely long contexts |
| **RMM** (Tan et al., 2025c) | Similar to MemAgent; interaction-driven feedback on memory writes |
| **Mem-α** (Wang et al., 2025p) | Frame memory construction as sequential decision-making: populate/update structured multi-component memories (core/semantic/episodic) |

**Limitation**: Does not explicitly model long-term effects of memory state construction.

---

### 5.3.2 Trajectory-Level Memory Representation

RL for **cumulative influence of memory over long trajectories**.

> "The value of memory decisions often emerges only through their cumulative influence on future reasoning and action selection."

**Key insight**: Trajectory-level memory as part of the agent's **Markov state** — quality assessed through downstream decision performance.

| Research Question | Direction | Representative |
|---|---|---|
| How to abstract long histories? | Summarization/folding/compression as policy decisions evaluated via future outcomes | SUPO, Sun et al. (2025b), DeepAgent |
| How should memory evolve over time? | Iteratively updated compact state; propagate advantages across contexts | MemSearcher (Yuan et al., 2025a) |
| What is decision-sufficient representation? | Trajectory memory as learned state whose utility is defined by long-term decision quality | Chen et al. (2025c), Wu et al. (2025d) |

---

### 5.3.3 Cross-Episode and Multi-Agent Memory

RL at the **broadest scope** — memory accumulates experience across repeated episodes or multiple agents.

> "At this scope, reinforcement learning is essential, as only long-term and cross-episode reward signals can determine which memories should persist, adapt, or be revised."

**Key insight**: Distill higher-level decision-relevant knowledge (reusable strategies, self-correction rules, abstracted behavioral patterns) whose utility emerges only through repeated RL signals.

| System | Approach |
|---|---|
| MCTR (Li et al., 2025h) | Experience encoded as transferable decision knowledge via interaction |
| TGM (Xia et al., 2025) | Graph-based experience abstraction |
| Retroformer (Yao et al., 2024) | Reflective retrieval policies |
| Memento (Zhou et al., 2025a) | Context-dependent RL-guided retrieval and application |
| MemGen (Zhang et al., 2025d) | Latent/non-textual memory representations |
| MAICC (Jiang et al., 2025d) | Shared/decentralized memory policies in multi-agent RL |
| SRMT (Sagirova et al., 2025) | Decentralized multi-agent memory via RL |

---

## Choosing the Right Paradigm

| Situation | Recommended Paradigm |
|---|---|
| Fast prototyping, interpretability matters | Static prompting |
| Need adaptation but no labeled data | Dynamic prompting (reflection, self-improvement) |
| Stable deployment, consistent behavior needed | Fine-tuning (SFT) |
| Long-horizon tasks, complex credit assignment | RL |
| Single-turn or short-context tasks | Prompting sufficient |
| Multi-session, evolving user preferences | SFT or RL |
| Memory must be explicitly optimized for task outcomes | RL |
