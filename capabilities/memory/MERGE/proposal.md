### Title: From Stored Experience to Reusable Knowledge: Memory Consolidation, Reconstruction, and Transfer in LLM Agents

---

### 1. Problem Definition

When an LLM agent completes multiple tasks sequentially, it may carry forward memories of past experience to support future decisions. Existing memory systems differ in what they retain: raw trajectories, summaries, or distilled rules. However, most current work treats memory as a static object to be stored and retrieved, rather than asking a more fundamental question:

**Under what conditions does remembered experience become reusable knowledge rather than inert textual residue?**

This proposal argues that the key issue is not simply the abstraction level of memory, but the form of consolidation through which memory is produced and later reused. Furthermore, memory may not help merely because it is retrieved, but because it can be critically evaluated for relevance in light of the current task.

The central empirical question is: **Under a fixed exposure to past experiences, how do different forms of memory consolidation (episodic storage, single-episode abstraction, cross-episode consolidation, and consolidation with meta-evaluation) affect in-domain and cross-domain transfer in LLM agents?**

### 2. Why This Question Matters

**Beyond "More is Better":** The broader goal of agent memory is to allow past experience to inform new situations flexibly. A memory can fail if it remains too tied to a single episode, becomes so abstract that it turns into vague advice, or is applied mechanically without checking whether it still fits the current context.

**Gap in Existing Work:** Prior work often compares different retrieval mechanisms or "memory vs. no memory". It rarely isolates whether the abstraction is derived from a single episode or multiple episodes, and whether the agent can evaluate the applicability of a memory before using it. Current literature does not clearly answer whether high-level memory helps because it captures general structure, or merely because it is shorter and safer to insert into context.

### 3. Experimental Design

**Fixed Setting:** We use a single ReAct-style QA agent with the same backbone LLM, prompting scaffold, and retrieval mechanism across all conditions.

**Key Control (Fixed Source Experience Count):** Instead of merely fixing token limits, all memory conditions are strictly derived from the same number of past solved tasks ($N=5$). This ensures differences arise from *how* experience is processed, not *how much* experience was seen.

**Condition A: Episodic Trace:** The agent stores compressed trajectories from the $N$ tasks, including intermediate reasoning steps and tool uses.
**Condition B: Single-Episode Abstraction:** The agent generates exactly $N$ distinct task-level rules, each derived independently from one of the $N$ trajectories.
**Condition C: Cross-Episode Consolidation:** The agent induces a consolidated principle jointly from all $N$ tasks, forming a single, multi-supported generalization.
**Condition D: Cross-Episode Consolidation + Meta-Evaluation:** The agent retrieves the memory from Condition C, but must explicitly output a brief assessment of *why* it is relevant and *under what conditions it might fail* before executing its first action.
**Baselines:** No Memory (Zero-shot) to establish base capability.

### 4. Benchmarks and Setting

**Source Domain:** HotpotQA. Selected for its requirement of multi-hop reasoning, explicit intermediate state tracking, and integration of multiple evidence sources.

**Target Conditions:**
* **In-domain transfer:** Train memory on one subset of HotpotQA, evaluate on a held-out split.
* **Cross-domain transfer:** Train memory on HotpotQA, evaluate on 2WikiMultiHopQA (and optionally MuSiQue). These tasks share multi-hop requirements but differ in data distribution, creating a controlled near-transfer scenario.

### 5. Evaluation Metrics

**Main Task Metrics:** Exact Match (EM), F1 Score, and Task Success Rate.

**Actionability Score:** To distinguish genuine cognitive transfer from superficial linguistic changes, we quantify the divergence in the agent's tool calls (e.g., search queries) compared to the No Memory baseline. Let $A_{base}$ be the set of tool queries in the baseline, and $A_{mem}$ be the set in the memory condition. The score is calculated using Jaccard distance:

$$Score_{actionability} = 1 - \frac{|A_{base} \cap A_{mem}|}{|A_{base} \cup A_{mem}|}$$

A high score indicates the memory caused concrete behavioral shifts, rather than just adding generic reasoning text.

**Memory-specific Metrics:** Error Repetition Rate (does it repeat known mistakes) and Applicability Judgment Accuracy (for Condition D).

### 6. Hypotheses

**H1:** In in-domain transfer, Episodic Trace and Cross-Episode Consolidation will outperform Single-Episode Abstraction, as one-shot abstractions are brittle and under-supported.
**H2:** In cross-domain transfer, Cross-Episode Consolidation will outperform Episodic Trace, as multi-task abstraction strips away source-specific surface details.
**H3:** Single-Episode Abstraction will consistently underperform Cross-Episode Consolidation, demonstrating that abstraction is only useful when grounded across repeated experiences.
**H4:** Cross-Episode Consolidation + Meta-Evaluation will achieve the highest cross-domain performance and Actionability Score, proving that successful transfer requires judging applicability, not just recall.

### 7. Critical Analysis and Limitations

**LLM-generated abstraction quality remains a confound:** Even consolidated memories are LLM-generated. Weak performance may stem from generation quality rather than flawed consolidation.
**Cross-domain is near transfer:** The shift from HotpotQA to 2WikiMultiHopQA is a distribution shift, not a full modality jump. Conclusions apply to controlled transfer.
**No true parameter internalization:** Memories remain external textual artifacts evaluated in-context, not stable skills inscribed into model weights.

---