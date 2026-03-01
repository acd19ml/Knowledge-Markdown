# Survey Overview

> Section: Introduction (pages 1–4)

---

## Paper Metadata

| Field | Value |
|---|---|
| Title | A Systematic Survey of Self-Evolving Agents: From Model-Centric to Environment-Driven Co-Evolution |
| Focus | Self-evolving LLM-based agents |
| Length | 26 pages |
| Key Tables | Table I (Training-Based Methods), Table II (Dynamic Experience), Table III (Applications), Table IV (Benchmarks), Table V (OSS Libraries) |

---

## The Supervision Bottleneck

The core motivation for self-evolving agents:

> "Post-training still relies heavily on human oversight: SFT limits models to imitation, while RL depends on sparse and human-defined rewards that can be fragile or exploitable."

**Current limitations**:
- SFT: Bounded by quality and quantity of human demonstrations — models learn to imitate, not to generalize
- RLHF: Reward models reflect human biases, are expensive to scale, and can be exploited through reward hacking

**Self-evolution answer**: Agents that generate their own training signals through interaction, discovering policies beyond the initial training distribution.

---

## Core Definition

> "Self-Evolving Agents: systems that autonomously improve their capabilities through continual interaction, self-assessment, and experience accumulation — without requiring perpetual human supervision."

Three fundamental pathways for evolution:
1. **Within the model** — optimizing internal representations and policies (Model-Centric)
2. **Through environmental interaction** — leveraging external feedback (Environment-Centric)
3. **Via joint co-evolution** — model and environment developing together (Co-Evolution)

---

## Three-Paradigm Taxonomy

```
           SELF-EVOLVING AGENTS
                    │
    ┌───────────────┼───────────────────┐
    │               │                   │
Model-Centric   Env-Centric      Co-Evolution
(Internal)      (External)       (Joint)
    │               │                   │
Inference +    Static +          Multi-Agent +
Training       Dynamic +         Environment
               Modular +         Training
               Topology
```

### Why three paradigms?

| Paradigm | Strength | Limitation |
|---|---|---|
| Model-Centric | Fast, no env setup needed | Bounded by initial capacity; risks model collapse |
| Environment-Centric | External signal prevents self-reinforcing bias | Static envs cause saturation |
| Co-Evolution | Open-ended growth; no ceiling | Requires sophisticated env engineering |

---

## Paper Structure Map

| Section | Content | Pages |
|---|---|---|
| I. Introduction | Motivation, overview | 1–4 |
| II. Preliminaries | Agent def, MDP, problem setup | 4–5 |
| III. Model-Centric | Inference-Based + Training-Based | 5–9 |
| IV. Environment-Centric | Static + Dynamic + Modular + Topology | 9–12 |
| V. Co-Evolution | Multi-Agent Policy + Environment Training | 10–11 |
| VI. Applications | Science, SWE, Open-World | 11–12 |
| VII. Discussion | Tensions, Challenges, Future | 12–13 |
| VIII. Benchmarks | Intrinsic + Agentic (Table IV) | 13–16 |
| IX. Open Source Libraries | Table V (13 key libraries) | 17–18 |
| X. Conclusion | Summary | 19 |
| References | 353 cited works | 19–26 |

---

## Figure 6: Advantages of Co-Evolution

The paper's central diagram comparing all three paradigms:

| Problem | Model-Centric | Env-Centric | Co-Evolution |
|---|---|---|---|
| Verification | Lacks external verification | Gets env feedback | Gets grounded feedback |
| Data ceiling | Self-bounded | Fixed env complexity | Adaptive difficulty |
| Training disconnect | Error accumulation in iteration | Static env limitation | Targeted feedback on demand |
| Scalability | Non-scalable (single-task) | Limited | Scalable multi-task |

---

## Key Metrics and Results Referenced

- **VOYAGER**: 15.3× faster task progression in Minecraft vs baselines
- **GITM**: +47.5% success on Diamond-level Minecraft tasks
- **GNoME**: 2.2 million new stable crystal structures discovered
- **A-Lab**: 71% synthesis success rate over 17-day continuous run
- **AlphaProof**: IMO 2024 silver-level mathematical reasoning
- **CRESt**: 9.3× cost-performance gain in catalysis discovery

---

## Related Surveys

| Survey | Focus | Relationship |
|---|---|---|
| Foundation Agent Memory (this repo: [Agent_Memory/](../Agent_Memory/)) | Memory mechanisms in LLM agents | Complementary: memory is a key substrate for self-evolution |
| LLM Post-Training Survey | SFT, RL, alignment methods | Foundations for Training-Based evolution (Section III-B) |
| Survey of LLMs | General LLM capabilities | Background context |
| Scientific Discovery Survey | AI for science | Application domain (Section VI-A) |
