# Evaluation: Metrics and Benchmarks

> Paper Section 7 (pages 33–39)

> "Evaluating foundation agent memory is fundamentally about measuring whether stored information and experience are accurate, useful, reliable, and efficiently accessible under long-horizon interactions."

---

## 7.1 Metrics

Three categories of metrics used in memory evaluation:

### Accuracy-Based Metrics

For tasks with clear objective outcomes:

| Metric | Use Case | Notes |
|---|---|---|
| **Accuracy / Memory Accuracy** | Long-history QA, factual recall | Direct alignment with ground truth |
| **F1** | When responses have variance | Partial overlap at token level |
| **Recall@K** | Explicit memory module evaluation | Did the system retrieve at least one relevant item in top-K? |
| **MAP** (Mean Average Precision) | Ranked retrieval quality | Considers both relevance and ranking |
| **NDCG@K** | Ranked retrieval quality | Discounted gain — rewards relevant items appearing earlier |
| **Success Rate (SR)** | Interactive agents | Did the agent finish the task end-to-end? |
| **Goal Completion (GC)** | Interactive agents | Environment-defined success |
| **Pass@K** | Code / tool-use settings | At least one of top-K attempts solves the task |
| **Resolved Rate (RR)** | SW engineering (SWE-bench) | Issue resolution rate |
| **Memory Integrity** | Memory-centric benchmarks | Do extracted memories cover required memory points? |
| **False Memory Rate** | Memory hallucination | How often does the system introduce fabricated or incorrect memories? |

### Similarity-Based Metrics

For dialogue generation and summarization where exact correctness doesn't apply:

| Metric | What It Measures | Limitation |
|---|---|---|
| **BLEU** | Lexical overlap with reference | Can underestimate valid paraphrases |
| **ROUGE / ROUGE-L** | Lexical overlap | Can overestimate fluent but ungrounded responses |
| **Distinct-n** | Lexical diversity | Discourages repetitive generation |
| **BERTScore** | Embedding-based semantic similarity | Better for paraphrases than BLEU/ROUGE |
| **FactScore** | Atomic factual claim agreement | Good for summarization as compression mechanism |
| **Perplexity** | Likelihood-based generation quality | Indirect; doesn't verify historical grounding |

### LLM-as-a-Judge Metrics

For open-ended outputs where reference answers are insufficient:
- Score response correctness or preference adherence using LLM evaluator
- Examples: LongMemEval, PrefEval, MemoryBench, ConvoMem
- **Advantage**: Expands coverage to realistic assistant behavior
- **Risk**: Sensitive to evaluator model choice and rubric design

---

## Core Memory Abilities Being Evaluated

Six core memory abilities tracked across benchmarks (Table 3 in paper):

| Ability | Abbreviation | Description |
|---|---|---|
| **Memory Extraction** | ME | Correctly extract facts from interaction history |
| **Memory Retrieval** | MR | Find relevant memories at query time |
| **Memory Update** | MU | Correctly update memory when information changes |
| **Abstention Behavior** | AB | Know when to abstain under missing evidence |
| **Compression** | CS | Efficiently compress memory |
| **Forgetting / Retention** | FR | Selectively forget while preserving important items |

**Evaluation gaps**:
- CS and FR are **comparatively under-evaluated** in current benchmark designs
- AB is inconsistently required — few benchmarks reward abstention under missing evidence
- Most benchmarks reduce evaluation to ME and MR

---

## 7.2 User-Centric Benchmarks

Evaluate memory from the **user's perspective** — personalization, dialogue consistency, preference following.

| Benchmark | Focus | Metrics | Notes |
|---|---|---|---|
| **DuLeMon** (Xu et al., 2022b) | Long-term dialogue memory | Accuracy, Similarity | User consistency over sessions |
| **MemoryBank** (Zhong et al., 2024) | Explicit memory records + operations | Memory accuracy, operation-level search | Searchable memory evaluation |
| **PerLTQA** (Du et al., 2024) | Personal long-term memory QA | Accuracy, F1, Recall@K | Multi-type user memory QA |
| **LoCoMo** (Maharana et al., 2024) | Long-form conversation memory | Accuracy, F1, BERTScore | Multi-session, multi-type questions |
| **DialSim** (Kim et al., 2024a) | Dialog-based memory simulation | Accuracy | Simulated long-term dialogue |
| **LongMemEval** (Wu et al., 2025b) | Long-term memory evaluation | Accuracy, Recall@K, LLM-judge | Explicit question-type categorization by memory ability |
| **HaluMem** (Chen et al., 2025a) | Memory hallucination detection | Memory Accuracy, Integrity, False Memory Rate | Only benchmark explicitly tracking false memory rate |
| **PersonaMem** (Jiang et al., 2025a) | Persona-based memory | Accuracy, F1 | Persona consistency across sessions |
| **MemoryBench** (Ai et al., 2025) | Memory capacity + efficiency | Similarity, LLM-judge | Capacity/cost trade-offs |
| **MemoryAgentBench** (Hu et al., 2025c) | Comprehensive agent memory | Accuracy, Similarity, LLM-judge | Combines multiple memory abilities |
| **PrefEval** (Zhao et al., 2025c) | Preference following in memory | LLM-judge | User preference adherence |
| **Mem-Gallery** (Bei et al., 2026) | Memory gallery evaluation | Accuracy | Cross-type memory assessment |
| **LOCCO** (Jia et al., 2025b) | Memory retention evaluation | Memory Retention Score (MRS) | Explicit retention measurement |
| **MemBench** (Tan et al., 2025a) | Memory capacity + efficiency | Capacity, Efficiency | Cost/performance tradeoffs |
| **ConvoMem** (Pakhomov et al., 2025) | Conversational memory | LLM-judge | Long-form conversation evaluation |
| **MADial-Bench** (He et al., 2025a) | Multi-aspect dialogue | Similarity | Diversity in evaluation |

---

## 7.2.2 Agent-Centric Benchmarks

Evaluate foundation models as **semi-autonomous agents** executing multi-step actions in an environment.

**Key principle**: Correctness defined by environment state — not user preference. Same task, same success signal across different users.

### Benchmark Annotation Tags

| Tag | Meaning |
|---|---|
| TEMP | Temporal/sequence reasoning over event order and time dependencies |
| STATE | Tracking and updating environment/task state across multi-step interaction |
| GROUND | Grounding natural-language instructions into concrete environment targets/actions |
| PLAN | Planning and re-planning multi-step actions toward a goal |
| TOOL | Selecting and correctly invoking tools/APIs |
| MHOP | Multi-hop reasoning composing multiple evidence pieces |
| DIAL | Goal-directed dialogue management (clarification, consistency across turns) |
| ACT | Executing correct environment actions (click/type/select) |
| TTL | Test-time learning: improve later performance by accumulating experience without parameter updates |

### Key Agent-Centric Benchmarks

| Benchmark | #Data | Environment | Core Abilities | Evaluation |
|---|---|---|---|---|
| **HotpotQA** | 113K | TEXT | MHOP, STATE | Accuracy, F1 |
| **2WikiMultiHopQA** | 193K | TEXT | MHOP, STATE | Accuracy, F1 |
| **MuSiQue** | 25K | TEXT | MHOP, STATE | F1 |
| **HLE** | 2.5K | TEXT | MHOP, STATE | Accuracy, RMSE |
| **BrowseComp** | 1,266 | WEB | PLAN, TOOL, MHOP, STATE | Accuracy, PR |
| **Mind2Web** | 2.35K | WEB (GUI) | GROUND, PLAN, STATE | Accuracy, F1, SR |
| **WebArena** | 812 | WEB (GUI, SIM) | GROUND, PLAN, STATE | SR |
| **WebShop** | 12.1K | WEB (GUI, MIX) | GROUND, PLAN, STATE | TaskScore, SR |
| **GAIA** | 466 | WEB | TOOL, MHOP, PLAN, STATE | Accuracy, SR |
| **OSWorld** | 369 | OS (GUI, MM) | GROUND, PLAN, STATE | SR |
| **AppWorld** | 750 | APP (API, MT) | TOOL, CODEGEN, PLAN, STATE | SR |
| **τ-Bench** | 165 | APP (API, MT) | TOOL, PLAN, STATE, DIAL | Pass^1, Pass^k |
| **HumanEval** | 164 | CODE | CODEGEN, DEBUG | Pass@1 |
| **SWE-Bench** | 2.3K | CODE | PATCH, DEBUG, STATE | RR |
| **ALFRED** | 25.7K | ROBOT (ACT, MM) | GROUND, PLAN, STATE | SR, GC |
| **ALFWorld** | 3.8K | ROBOT (ACT, MT) | PLAN, STATE, GROUND | SR |
| **MineDojo** | 3.1K | GAME (ACT, MM) | PLAN, STATE, GROUND | SR |
| **EgoSchema** | 5,031 | VIDEO | TEMP | Accuracy |
| **MT-Mind2Web** | 720 | WEB (GUI, MT) | GROUND, PLAN, STATE, DIAL | Accuracy, F1, SR |
| **Evo-Memory** | ~3,700 | TEXT | TTL, PLAN, STATE | Accuracy, SR |
| **LifelongAgentBench** | 1,396 | APP/OS | TTL, TOOL, PLAN, STATE | SR |
| **OdysseyBench** | 602 | APP (GUI, MT) | PLAN, TOOL, STATE, TEMP | PR |

---

## Evaluation Gaps and Future Needs

### Current Gaps

1. **Most benchmarks reduce evaluation to final answer accuracy** — doesn't attribute success/failure to memory mechanism
2. **CS (Compression) and FR (Forgetting/Retention)** are rarely explicitly evaluated
3. **AB (Abstention Behavior)** inconsistently required — hallucination-safe memory behavior undervalued
4. **Benchmark time horizons** are too short — few test cross-session or multi-month interactions

### What Next-Generation Benchmarks Need

Two critical additional dimensions for memory-centric analysis:

1. **Dependency distance**: How far apart is the required information from its later use? (within-turn, cross-turn, cross-session)
2. **Memory correctness under interaction**: Do stored items remain faithful, non-contradictory, and policy-consistent as the environment evolves?

**Recommended memory-sensitive measurements**:
- Retrieval faithfulness and coverage for required facts/tool outputs
- Error modes in state tracking (drift, omission, contradiction)
- Persistence under interruptions (resume after long gaps)
- Efficiency trade-offs (memory size, update frequency, retrieval cost)

→ See [08_future-directions.md §6: Real-World Benchmarking](08_future-directions.md#6-real-world-benchmarking-and-evaluations) for detailed research agenda.
