# CS6493 Project Topic

## Title

**Selective Transfer in Memory-Augmented LLM Agents**

Large language model (LLM) agents often use past experience as external memory to improve future task performance. However, existing memory-based methods are usually evaluated by average benchmark performance, which does not distinguish between two very different cases: when past experience is genuinely relevant to the current task, and when past experience is mismatched but still injected into the context. As a result, it is often unclear whether a memory method supports useful transfer or merely causes indiscriminate reuse.

This project studies **selective transfer** under a fixed experience budget. We focus on a controlled multi-hop QA setting, using **HotpotQA** as the source benchmark and **2WikiMultiHopQA** as the target benchmark. The key idea is to predefine two kinds of source-target pairs: **matched pairs**, where source experience and target task share the same reasoning pattern, and **mismatched pairs**, where they are deliberately constructed to be structurally different. This allows us to evaluate not only whether memory helps, but whether it helps only when it should.

The project focuses on two main components:

## 1. Memory Strategy Comparison under Matched / Mismatched Transfer

We will compare memory strategies under a fixed source experience budget (`N = 5` solved source tasks per memory set). The main conditions are:

- **No Memory**
- **Episodic Trace**
- **Cross-Episode Consolidation**
- **Cross-Episode Consolidation + Applicability Judgment**

To support this comparison, we will first define a small reasoning taxonomy for multi-hop QA tasks, including:

- `bridge`
- `comparison`
- `temporal`
- `distractor-heavy`

Using this taxonomy, we will construct:

- **Relevant Split**: source memory and target task belong to the same reasoning cluster
- **Irrelevant Split**: source memory and target task belong to different reasoning clusters

To reduce confounds, the source-target pairs will be filtered by:

- entity disjointness
- low lexical overlap
- no answer leakage

The goal is to compare whether different memory strategies improve performance on relevant tasks while avoiding negative transfer on irrelevant tasks.

## 2. Evaluation of Selective Transfer

The evaluation will focus on whether a memory strategy improves matched transfer without causing mismatched overuse.

Primary metrics:

- **Exact Match (EM)**
- **F1**

Transfer-specific metrics:

- **Relevant Gain**: improvement over `No Memory` on the Relevant Split
- **Irrelevant Delta**: change relative to `No Memory` on the Irrelevant Split
- **Negative Transfer Rate**: percentage of Irrelevant Split tasks where memory causes measurable degradation

Optional analysis:

- memory invocation rate
- rejection rate under applicability judgment
- token cost

## Why This Topic Is Narrower and More Defensible

Compared with our previous topic, this revised project is narrower in four ways:

- it uses a fixed benchmark setting rather than a broad critique of self-improvement methods
- it compares a small number of controlled memory conditions
- it relies on predefined matched / mismatched task pairs instead of post hoc interpretation
- it uses clear quantitative outputs rather than latent judgments such as whether a model “truly understood” its own failure

## Expected Value

This project is intended not only as a course project, but also as a route-selection experiment for future memory research:

- if results are mainly driven by **memory form**, future work should focus on consolidation and representation
- if results are mainly driven by **memory use**, future work should focus on applicability judgment and gating
- if both matter, future work should treat memory formation and memory use as a coupled problem

## Request

We would like to ask whether this revised topic fits the intended scope and standard of the CS6493 project.