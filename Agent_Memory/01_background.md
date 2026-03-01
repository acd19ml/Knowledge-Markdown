# Background: Foundation Agents & Memory

> Paper Section 2 (pages 5–8)

---

## 2.1 Large Language Models and Foundation Agents

### What is a Foundation Agent?

> "A foundation agent is an autonomous or semi-autonomous system that uses foundation models, such as LLMs, as its core decision modules, augmented with mechanisms for state estimation, action execution, and memory management."

Key distinction from chatbots:
- Chatbots: static, one-shot question → answer
- Foundation agents: **full loop** — perceive → reason → act → observe → update memory → repeat

### Core Capabilities

| Capability | Description | Representative Works |
|---|---|---|
| **Planning** | Task decomposition, decision making | ReAct (Yao et al., 2023), Huang et al. (2024b) |
| **Tool Use** | External functions, APIs, models | Toolformer (Schick et al., 2023), ToolLLM |
| **Multimodal Perception** | Vision-language models | Liu et al. (2023a), Bai et al. (2025) |
| **Memory** | Short-term context + long-term horizons | MemGPT, Generative Agents |

### Emerging Real-World Applications

- Workflow automation (Xiong et al., 2025c)
- Tutoring (Wang et al., 2025l)
- Web/GUI interaction (He et al., 2024a)
- Embodied control in physical/simulated environments (Fan et al., 2022; Yang et al., 2025c)
- Scientific assistance (Ren et al., 2025; Zheng et al., 2025d)
- Deep Research, Manus — multi-step + tool-augmented

### Remaining Challenges

1. **Long-horizon reliability** — preventing compounding errors, behavioral loops
2. **Evaluation** — moving beyond static QA to dynamic, interactive, long-horizon feedback
3. **Alignment & safety** — controllability as autonomy and tool access expand

---

## 2.2 Memory

### Definition

> "Memory generally refers to a system's ability to retain, organize, and exploit information over time. In the context of LLM-based foundation agents, memory is used to explain how agents go beyond single-turn contexts to support long-term interaction, behavioral consistency, and experience accumulation."

### Cognitive Science Roots

The paper draws from **human cognitive psychology**:

| Cognitive Type | Function | Biological Analog |
|---|---|---|
| **Sensory memory** | Brief buffer of raw perceptual inputs | Sperling (1960) — iconic memory |
| **Working memory** | Temporary holding + active manipulation under capacity constraints | Baddeley (2020) |
| **Episodic memory** | Specific experiences in time and context | Tulving (1972, 1985) |
| **Semantic memory** | Abstract facts and conceptual knowledge | Tulving (1972) |
| **Procedural memory** | Skills, habits, action policies (implicit) | Cohen & Squire (1980); Squire (1992) |

**Key biological mechanism**: Synaptic plasticity (Hebb, 2005; Bliss & Lømo, 1973), circuit-level changes → memory traces/engrams (Tonegawa et al., 2015)

### Agent Memory vs. Biological Memory

Biological memory: persistent, experience-driven neural change (synaptic plasticity, consolidation)

Agent memory: the more relevant insight is **how memory is designed, realized, and used** to:
- Support different functions
- Enable different representations
- Serve different targets (users vs. agents)

### The Utility Gap

**Problem**: context windows are limited, environments evolve over time.

**Current failure modes under long horizons**:
- Early-context forgetting
- Progressive context drift
- Inability to personalize over time
- Short-horizon pattern matching ≠ long-horizon memory

**Solution**: External memory stores + summarization + reflection + consolidation
→ Compress experience into reusable knowledge

### Memory Architecture Evolution

| Era | Memory Style | Characteristic |
|---|---|---|
| Early (2023) | Static, predefined, simple | Fixed prompts, single memory block |
| Mid (2024) | Structured external memory | RAG, vector stores, graph memory |
| Now (2025) | Self-adaptive, self-evolving, flexible | Intelligently store/load/summarize/forget/refine |

---

## Why Memory Is Uniquely Important Now

Two primary empirical dimensions of agent adaptation:

1. **User-facing personalization** — adapting to individual users over months
   - Interaction contexts expand far beyond prompt-based mechanisms
   - Multi-session data grows exponentially

2. **Task-oriented specialization** — vertical domains (coding, web search)
   - Accumulated context from project work expands beyond single context windows
   - Static memory insufficient; needs self-evolving units

---

## Connection to Later Sections

| Concept introduced here | Where it's expanded |
|---|---|
| Sensory / Working / Episodic / Semantic / Procedural | [2.2 Cognitive Mechanisms](02_taxonomy/2.2_cognitive-mechanisms.md) |
| External vs. Internal memory substrates | [2.1 Memory Substrates](02_taxonomy/2.1_memory-substrates.md) |
| User-centric vs. Agent-centric | [2.3 Memory Subjects](02_taxonomy/2.3_memory-subjects.md) |
| Context explosion challenge | [5. Scaling](05_scaling.md) |
| Memory management operations | [3. Operations](03_operations/) |
