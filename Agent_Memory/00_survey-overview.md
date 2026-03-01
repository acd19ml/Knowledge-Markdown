# Survey Overview

## Paper Info

| Field | Detail |
|---|---|
| **Title** | Rethinking Memory Mechanisms of Foundation Agents in the Second Half: A Survey |
| **arXiv** | 2502.06250 (Feb 10, 2026) |
| **GitHub** | [AgentMemoryWorld/Awesome-Agent-Memory](https://github.com/AgentMemoryWorld/Awesome-Agent-Memory) |
| **Scope** | 218 papers, 2023 Q1 – 2025 Q4 |
| **Core Institutions** | UIC, UIUC, Stanford, UCLA, Google, Salesforce, Meta, Roblox, Cisco |
| **Key Authors** | Weizhi Zhang (project organizer), Philip S. Yu & Kai Shu (supervisors) |

---

## Abstract (condensed)

AI is entering the **"second half"** — shifting from benchmark scores to real-world utility. The central challenge: agents operating in **long-horizon, dynamic, and user-dependent environments** face **context explosion** and must continuously accumulate, manage, and selectively reuse large volumes of information.

Memory, with hundreds of papers released in 2025 alone, emerges as the critical solution.

This survey provides a **unified view of foundation agent memory** along three dimensions:
1. **Memory substrate** — internal vs. external
2. **Cognitive mechanism** — episodic, semantic, sensory, working, procedural
3. **Memory subject** — agent-centric vs. user-centric

---

## The "Second Half" Framing

### First Half (2017–2023)
- Focus: architecture innovation, benchmark scores, scaling
- Recipe: massive pre-training + post-training alignment
- Result: LLMs/agents hit 90%+ on MMLU, MATH, etc.

### Second Half (2024–now)
- Focus: **real-world utility**, long-horizon reliability, user personalization
- Challenge: context windows explode; static memory insufficient
- Critical capability: **accumulate, retain, selectively reuse** across extended interactions

> "In the first half, progress was driven by training methods, scaling, and model architectures. In the second half, the focus shifts from improving training recipes to solving the critical utility problem in reality."

---

## Core Thesis

Real-world agents operate in environments where context grows along **three scaling axes**:
1. **Interaction horizon** — multi-session, multi-month tasks
2. **Environmental complexity** — heterogeneous data, tool states, structured artifacts
3. **System quantity** — multiple agents + human collaborators

Memory architecture must evolve from:
- Static, predefined, simple → Self-adaptive, self-evolving, flexible
- Intelligently store, load, summarize, forget, and refine

---

## Three-Dimensional Taxonomy

```
                    Foundation Agent Memory System
                              │
     ┌────────────────────────┼────────────────────────┐
     │                        │                        │
Memory Substrate       Cognitive Mechanism        Memory Subject
(WHERE/HOW stored)     (WHAT FUNCTION)            (WHO it serves)
     │                        │                        │
External    Internal    Short-term  Long-term    User    Agent
  ↓ ↓ ↓       ↓ ↓ ↓      ↓    ↓    ↓  ↓  ↓    Centric  Centric
Vector   Weights    Sensory Working  Epi Sem Pro
Text     Latent
Struct   KV Cache
Hierch
```

→ See [02_taxonomy/README.md](02_taxonomy/README.md) for full detail.

---

## Paper Structure Map

| Section | Title | Pages | Notes File |
|---|---|---|---|
| 1 | Introduction | 3–5 | This file |
| 2 | Background | 5–8 | [01_background.md](01_background.md) |
| 3 | Taxonomy | 8–20 | [02_taxonomy/](02_taxonomy/) |
| 4 | Memory Operation Mechanism | 20–26 | [03_operations/](03_operations/) |
| 5 | Memory Learning Policy | 26–30 | [04_learning-policy.md](04_learning-policy.md) |
| 6 | Scaling | 30–33 | [05_scaling.md](05_scaling.md) |
| 7 | Evaluation | 33–39 | [06_evaluation.md](06_evaluation.md) |
| 8 | Applications | 39–44 | [07_applications.md](07_applications.md) |
| 9 | Future Directions | 44–48 | [08_future-directions.md](08_future-directions.md) |
| 10 | Conclusions | 48 | (summarized below) |

---

## Conclusions (Section 10)

Memory is becoming the **key component** for foundation agents in long-horizon, context-exploded, user-dependent environments. The survey:
- Unifies design along 3 dimensions (substrate, mechanism, subject)
- Analyzes operation under single/multi-agent topologies
- Shows the growing role of prompting/SFT/RL-based learning policies
- Summarizes metrics and benchmarks
- Lists **6 key future challenges** for reliable, scalable, self-evolving, trustworthy memory

---

## Publication Trends

- Research volume: **exponential acceleration** through 2025
- 2025 Q4 saw a dramatic peak
- Distribution across three dimensions:
  - **Substrate**: External memory dominates
  - **Cognitive**: Episodic and semantic most common
  - **Subject**: Both user-centric and agent-centric growing rapidly

---

## Related Surveys (context)

| Survey | Focus | Gaps addressed by this paper |
|---|---|---|
| Zhang et al. (2025o) | Memory management strategies | No substrate or subject distinction |
| Du et al. (2025) | Task applications | No substrate or subject distinction |
| Wu et al. (2025g) | Neuroscience-inspired | Doesn't model memory subject |
| Liang et al. (2025) | Memory lifecycle | Doesn't model memory subject |
| Hu et al. (2025d) | Forms/functions/temporal | Focuses on agent-centric only, misses user-centric |
