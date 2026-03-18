# Agent KB — Cross-framework shared memory for planning guidance and feedback refinement

## Meta
- **Title**: AGENT KB: Leveraging Cross-Domain Experience for Agentic Problem Solving
- **Authors**: Xiangru Tang, Tianrui Qin, Tianhao Peng et al. | Yale, OPPO, UW-Madison, UNC, Stanford, ByteDance, Nanjing University, AllHands AI, DeepWisdom, Microsoft Research, Google DeepMind
- **Venue**: Preprint 2025 | arXiv:2507.06229
- **Links**: [PDF](../source/Agent KB.pdf) | [Code](https://github.com/OPPO-PersonalAI/Agent-KB)
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-08
- **Priority**: P1 | **Reading progress**: Pass 2

## One-line Summary

Agent KB 提出一个 plug-and-play shared memory layer，把多个异构 agent framework 的 trajectories 蒸馏成可复用 experience units，再在 planning time 与 feedback time 同时使用 hybrid retrieval 和 disagreement-gated refinement，在不重训 base agents 的前提下稳定提升 GAIA、GPQA、HLE 和 SWE-bench 表现。

## Problem Setting

- **Core problem**: Existing agent memory systems improve individual agents or single frameworks, but do not enable reusable knowledge transfer across heterogeneous agent architectures.
- **Assumptions**:
  - Different agent frameworks can export execution traces that can be abstracted into a common schema.
  - A shared memory layer can intervene without changing the base planner architecture.
  - Retrieved experience must be adapted, not copied blindly, because cross-framework context mismatch and interference are real.
- **Insufficiency of existing approaches**:
  - Current systems are siloed within one framework.
  - Cross-framework transfer faces three explicit challenges: representation heterogeneity, context mismatch, and knowledge interference.

## Core Method

**Method overview**:

Agent KB builds a shared experience repository over multiple agent frameworks such as smolagents, OWL, SWE-Agent, and OpenHands. It transforms execution logs into a structured experience unit:

`E = <pi, gamma, S, C>`

where `pi` is a task embedding, `gamma` captures goal constraints, `S` stores action-reasoning pairs, and `C` contains cross-framework metadata. The system then uses the same shared store in two stages of solving:

1. **Planning stage**: retrieve relevant experiences from task description to seed the initial plan.
2. **Feedback stage**: retrieve from execution feedback traces to refine the plan or fix mistakes after an initial attempt.

The retrieval pipeline is hybrid:

- lexical retrieval (BM25) for tool/domain compatibility
- semantic ranking via embeddings
- calibrated fusion of the two

Retrieved experiences are then adapted through a `Reason -> Retrieve -> Refine` loop. To avoid harmful transfer, Agent KB adds a **disagreement gate** that only accepts refinements sufficiently aligned with the current plan.

The knowledge base also self-evolves: similar candidate entries are compared by an LLM ranker, inferior ones are discarded, and low-utility items can be evicted via a learned utility score balancing recency, frequency, and transferability.

**Key Design Choices**:

| Design Decision | Author's Choice | Author's Rationale | Ablation Verified? |
|----------------|----------------|--------------------|--------------------|
| Memory scope | Cross-framework shared experience store | Break isolated agent silos | Yes |
| Experience unit | Structured abstraction over trajectories | Enables framework-agnostic transfer | Partial |
| Retrieval | Hybrid lexical + semantic | Exact tool/domain matches and broader semantic similarity are complementary | Yes |
| Solve loop | Planning-stage retrieval + feedback-stage retrieval | Supports both initial guidance and later correction | Yes |
| Safety filter | Disagreement gate on refinements | Mitigates knowledge interference | Yes |

- **Core difference from prior work**: Unlike single-agent memory systems such as A-MEM, Agent KB is explicitly designed for cross-framework transfer and treats memory as a reusable ecosystem layer, not an internal component of one agent.

## Key Results

| Benchmark | This Method | Strongest Baseline | Δ | Notes |
|-----------|------------|-------------------|---|-------|
| GAIA (smolagents, GPT-4.1, pass@3) | 73.9 | 55.2 baseline pass@1 | +18.7 pp | Main headline result |
| SWE-bench Lite (OpenHands, GPT-4.1, pass@1) | 28.3 | 24.3 | +4.0 pp | Also scales to later passes |
| HLE Bio/Chem (OpenHands, GPT-4.1, pass@3) | 14.1 | 9.5 | +4.6 pp | Beats Biomni baseline after retrieval |
| GPQA (OpenHands, GPT-4.1, pass@3) | 72.7 | 62.6 | +10.1 pp | Strong gain without retraining |

- **Key ablation findings**:
  - Removing the **Refine** stage causes the largest drop: average GAIA accuracy falls from `61.21` to `55.15`.
  - Removing either planning-stage or feedback-stage retrieval reduces performance to `59.39`, showing the two roles are complementary.
  - Hybrid retrieval consistently beats pure lexical or pure semantic retrieval.
  - Automatically generated experiences approach hand-curated ones: on GAIA average, `+AGENTKB` reaches `75.15` versus `76.97` for handcrafted experiences.
  - The disagreement gate is not cosmetic: the authors explicitly show best validation behavior around `beta ≈ 0.8`, which is one of the cleaner pieces of evidence in the paper that transfer needs interference control rather than naive memory injection.
- **Failure cases**:
  - Domain-specific knowledge transfers asymmetrically: reasoning knowledge partially transfers to SWE, but SWE knowledge does not generalize well back to reasoning tasks.
  - Harder tasks appear bottlenecked by abstraction quality, not just database size.

## Limitations

- **Author-stated limitations**:
  - The conclusion explicitly points to richer modalities and longer-horizon reasoning as future work.
  - The ethics statement notes risks around privacy, retrieval bias, and misuse in high-stakes settings.
- **My observed limitations**:
  1. **memory unit 已经是 transferable experience，但粒度仍然偏粗**。它比完整 trajectory 更进一步，但还没细到主线强调的 `experience-delta rule`。
  2. **write-back 逻辑是 KB-centric，而不是 environment-grounded**。Agent KB 可以新增、排序和淘汰 experiences，但不直接处理 GUI grounding 或 cross-app state alignment。
  3. **multi-pass 改善部分依赖重复 benchmark interaction**，因此一部分收益来自 held tasks 上的 iterative refinement，而不只是一次性可复用 consolidation。
  4. **cross-framework 论证很强，但仍主要停留在 text/tool 侧**。论文没有证明 visual GUI experiences 也能以同样保真度迁移。
- **Experimental design gaps**:
  - No GUI benchmark or multimodal computer-use setting.
  - The role of failed trajectories is present, but not isolated cleanly enough to show exactly how much value comes from failure-derived write-back.
  - The experience abstraction process depends on few-shot human seeds, so "fully automatic collective intelligence" is still not literal.
  - Pass-based evaluation is informative but also slightly entangles retrieval quality with repeated interaction effects on the same held benchmark instances.

## ⭐ Relation to My Research

### Position in Survey

- **Corresponding survey section/category**:
  Agent KB 应放在 Self_Evolve 线中，作为很强的 **cross-framework experience-transfer system**。按当前 main-line，它不是 GUI `A-1 + A-4` 的直接答案，但对收紧 `A-3` 很重要：它证明只要 memory 被适当抽象并加上 gate，experience sharing across agents 是可行的。

- **Role**: Strong peripheral positive example and cross-framework transfer reference

### Gap Signals (extracted from this paper)

- Gap signal 1: The paper solves **cross-framework transfer**, but not GUI-grounded memory reuse, so the main unresolved jump is from abstract transferable experience to grounded cross-app procedural knowledge.
- Gap signal 2: Agent KB confirms that **feedback-stage retrieval matters**, which supports the importance of post-attempt write-back rather than pre-task retrieval alone.
- Gap signal 3: The need for a disagreement gate shows that naive memory injection can easily hurt performance; therefore any future GUI write-back system also needs an interference-control mechanism.

在当前 main-line 下，Agent KB 不该被写成 “the answer”。它真正证明的是三件事：shared experience layer 确实有用；feedback-time refinement 很重要；外来知识必须经过严格过滤。但它仍然抽象了一层，也仍然太偏 text/tool，因此还不能算是已解决的 GUI procedural-memory system。

### Reusable Elements

- **Methodology**:
  - Shared `Reason -> Retrieve -> Refine` loops at both planning time and feedback time are directly reusable.
  - The disagreement gate is one of the cleanest mechanisms in the current literature for preventing harmful transfer.
  - Hybrid lexical + semantic retrieval is a practical pattern for memories that need both exact action/tool compatibility and broader analogical transfer.
  对当前工作来说，最值得直接复用的是 **feedback-stage retrieval** 和 **interference-control gate**。真正需要重设计的是 experience schema，因为 GUI transfer 需要比当前 cross-framework abstraction 更强的 grounding。

- **Experimental design**:
  - Multi-pass evaluation with `pass@1 / pass@2 / pass@3` is a clean way to separate first-pass retrieval gains from later refinement gains.
  - The comparison against handcrafted experiences is a strong template for evaluating whether automatically consolidated memories are actually competitive.
  - The gate and top-k ablations are also directly reusable if you later build a GUI memory layer: they provide a simple experimental recipe for checking whether transfer failure is due to bad retrieval or bad integration.

### Connections to Other Papers in Knowledge Base

- Relative to [2025_AMem.md](/Users/mac/studyspace/Knowledge-Markdown/Agent_Memory/papers/notes/2025_AMem.md), Agent KB is broader and explicitly cross-framework, but less focused on internal memory reorganization.
- Relative to [2024_AWM.md](./2024_AWM.md), it is less about workflow induction inside one agent and more about ecosystem-level knowledge sharing.
- Relative to [2025_MAGNET.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2025_MAGNET.md), it has stronger transfer and refinement machinery but weaker GUI grounding.
- Relative to [2024_OS-COPILOT.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2024_OS-COPILOT.md), it is more abstract and more portable across frameworks, but less explicit about concrete OS/GUI memory layout.

## Citation Tracking

- [ ] Agent KB (Tang et al., 2025): primary reference for cross-framework shared memory
- [ ] A-MEM (Xu et al., 2025): single-framework memory baseline compared on GAIA
- [ ] OpenHands / smolagents / OWL / SWE-Agent: integration targets
- [ ] GAIA / HLE / GPQA / SWE-bench Lite: evaluation benchmarks

## Key Passages

> "Current memory systems focus on individual agents or framework-specific demonstrations, failing to enable cross-architecture knowledge transfer." (Abstract, p.1)

> "planning seeds agents with cross-domain workflows, while feedback applies targeted diagnostic fixes." (Abstract, p.1)

> "future work aimed at richer modalities and longer-horizon reasoning." (Conclusion, p.10)
