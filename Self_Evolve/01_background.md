# Background & Preliminaries

> Paper Section II (pages 4–5)

---

## Agent Definition

A **Foundation Agent** is defined as:

> An LLM-based system that perceives observations, reasons over them, and selects actions to achieve goals — operating within an environment through a perceive-reason-act loop.

### Core Agent Components

| Component | Description |
|---|---|
| **Model** | LLM backbone that generates reasoning and actions |
| **Observation (o)** | Current state perceived from the environment |
| **Action (a)** | Output produced by the model (text, tool call, code, etc.) |
| **Environment (E)** | The world the agent interacts with: text, code, web, tools, physics |
| **Reward / Feedback** | Signal from environment evaluating action quality |
| **Memory** | Accumulated experience enabling long-horizon behavior |

---

## Formal MDP Framework

Agent-environment interaction is modeled as a **Markov Decision Process (MDP)**:

```
(S, A, T, R, γ)
```

| Symbol | Meaning |
|---|---|
| S | State space (all possible observations) |
| A | Action space (all possible agent outputs) |
| T | Transition function: T(s' | s, a) — how actions change state |
| R | Reward function: R(s, a, s') — quality signal |
| γ | Discount factor for future rewards |

### Interaction Loop

```
s_t → Agent (LLM) → a_t → Environment → s_{t+1}, r_t
         ↑                                      │
         └──────────── Memory / History ────────┘
```

The agent's goal: learn a policy π(a|s) that maximizes expected cumulative reward.

---

## The Supervision Bottleneck (Problem Framing)

Current LLM training pipelines:

```
Human Demonstrations → SFT → RLHF → Deployed Model
        ↑                    ↑
  Manual labels        Human preferences
  (expensive,          (fragile, exploitable,
   bounded)             limited scale)
```

**Two fundamental limitations**:

1. **SFT bounds**: Models can only be as good as the human demonstrations they imitate. Novel strategies beyond training distribution are inaccessible.

2. **RL reward fragility**: Human-defined reward functions:
   - May be hacked (agent finds loopholes)
   - Sparse in complex environments (long-horizon tasks)
   - Cannot scale to all task types automatically

---

## Self-Evolution: The Solution

Self-evolving agents break the supervision bottleneck by generating their own improvement signals:

```
Agent ──→ Action ──→ Environment
  ↑                       │
  └── Self-generated  ←───┘
      training signal
      (no human needed)
```

**Sources of self-generated signal**:
- **Internal**: Self-critique, consistency checking, confidence estimation
- **Environmental**: Code execution feedback, search results, test results, peer evaluation
- **Social**: Multi-agent discussion, competitive self-play

---

## Environment Types

The paper categorizes environments agents interact with:

| Type | Examples | Signal Type |
|---|---|---|
| **Code Execution** | Python REPL, terminals, compilers | Binary (pass/fail) or traceback |
| **Mathematical** | Lean provers, symbolic solvers | Verified/unverified |
| **Web/Search** | Search engines, browsers | Retrieved documents |
| **Physical/Robotic** | Simulators, robotic labs | Sensor feedback |
| **Social/Game** | Minecraft, multi-agent debates | Score, emergent behavior |
| **Scientific** | Chemistry/physics simulators, DFT | Experimental measurements |

---

## Key Distinction: Training vs Inference Self-Evolution

The survey distinguishes two timescales of evolution:

| Scale | When | Mechanism | Examples |
|---|---|---|---|
| **Inference-time** | During deployment, per-query | Sampling, self-critique, tree search | CoT, Reflexion, ToT |
| **Training-time** | Offline, model weight updates | SFT on self-generated data, RL | STaR, GRPO, WebRL |

This becomes the basis for the **Model-Centric** taxonomy split (Section III).

---

## Cross-Reference: Agent Memory

Self-evolution is deeply intertwined with agent memory (see [Agent_Memory/](../Agent_Memory/)):

| Memory Type | Role in Self-Evolution |
|---|---|
| **Episodic** | Stores past trajectories for offline learning (experience replay) |
| **Procedural** | Accumulated skills enable more efficient exploration |
| **Semantic** | Knowledge graphs from environment interaction |
| **Working** | Context window — determines what's available during inference evolution |

> Self-evolution can be understood as memory-driven learning: agents retain experiences and use them to improve future behavior.
