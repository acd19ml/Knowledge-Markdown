# OS-Copilot / FRIDAY — Generalist computer agent with self-improvement through tool accumulation and OS-level memory

## Meta
- **Title**: OS-Copilot: Towards Generalist Computer Agents with Self-Improvement
- **Authors**: Zhiyong Wu, Chengcheng Han, Zichen Ding, Zhenmin Weng, Zhoumianze Liu, Shunyu Yao, Tao Yu, Lingpeng Kong | Shanghai AI Laboratory, East China Normal University, Princeton University, The University of Hong Kong
- **Venue**: ICLR 2024 | arXiv:2402.07456
- **Links**: [PDF](../source/OS-COPILOT.pdf) | [Project](https://os-copilot.github.io/)
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-08
- **Priority**: P1 | **Reading progress**: Pass 2

## One-line Summary

OS-Copilot 提出统一的 OS-level agent framework，并将其实现为自我改进的 computer agent FRIDAY；该系统结合 planner、working memory、declarative memory、procedural memory、execution feedback 与 self-directed learning，为未见应用持续积累可复用 tools。

## Problem Setting

- **Core problem**: Most computer-use agents remain narrow and application-specific, while OS-level assistants must generalize across browsers, terminals, files, multimedia, and arbitrary third-party applications.
- **Assumptions**:
  - A unified OS interaction interface is available, including Python, bash, API calls, and mouse/keyboard control.
  - The agent can inspect execution feedback and use it for self-correction.
  - Tool construction and tool reuse are viable ways to scale to unfamiliar applications.
- **Insufficiency of existing approaches**:
  - Previous agents focus on isolated software domains.
  - Building custom tools and prompts for each application by hand is not scalable.
  - Existing general-purpose agents lack explicit self-directed learning for unfamiliar applications.

## Core Method

**Method overview**:

OS-Copilot defines a four-part architecture:

1. **Planner**: decomposes a user request into subtasks, optionally as a DAG.
2. **Configurator**: maintains the working memory and retrieves relevant tools, OS knowledge, and user information for each subtask.
3. **Actor**: executes actions and performs self-criticism based on execution outcomes.
4. **Universal runtime interface**: supports Python, bash, APIs, and mouse/keyboard interactions across the OS.

FRIDAY is the concrete self-improving agent built on top of this framework. Its memory design is explicitly inspired by human memory systems:

- **Declarative memory**: user profile plus semantic knowledge from past trajectories, the internet, users, and OS state.
- **Procedural memory**: a tool repository storing executable skills.
- **Working memory**: the central short-term hub that retrieves from and updates long-term memory, passes task-relevant information to the actor, and absorbs execution feedback for revision.

The self-improvement mechanism has two layers:

- **Self-refinement**: after an execution attempt, the critic can suggest correcting an action, tool, or subtask structure; high-quality tools are scored and preserved in procedural memory.
- **Self-directed learning**: for unfamiliar applications, the configurator proposes a curriculum of tasks, FRIDAY solves them, and accumulates application-specific tools as reusable skills.

**Key Design Choices**:

| Design Decision | Author's Choice | Author's Rationale | Ablation Verified? |
|----------------|----------------|--------------------|--------------------|
| Agent scope | OS-level, not single-app | Targets generalist computer assistance | Indirectly |
| Memory decomposition | Working + declarative + procedural memory | Mirrors human memory organization and separates concerns | No |
| Skill representation | Executable tools in repository | Reusable tools are the practical skill carrier | Partial |
| Self-improvement path | Critic-guided self-correction + self-directed learning curriculum | Lets the agent improve without hand-authoring all tools | Yes |
| Runtime interface | Python, bash, API, mouse/keyboard | Covers heterogeneous OS interaction modes | Indirectly |

- **Core difference from prior work**: OS-Copilot is not just a GUI grounding system or a browser agent. Its main novelty is the combination of OS-level action interfaces, explicit memory decomposition, and a self-improvement loop that stores newly learned tools as procedural memory.
  A detail worth keeping for later comparison is that the configurator is the real memory locus of the system: working memory gathers tools, user information, OS state, and actor feedback before the actor acts. That makes FRIDAY a useful systems reference even if its memory objects are still too coarse for the current main line.

## Key Results

| Benchmark | This Method | Strongest Baseline | Δ | Notes |
|-----------|------------|-------------------|---|-------|
| GAIA Level 1 success rate | 40.86% | Previous best 30.3% | +10.56 abs | About 35% relative improvement |
| GAIA Level 3 success rate | 6.12% | Prior systems effectively 0 | Positive | Hardest split remains difficult |
| SheetCopilot-20 / spreadsheet control | 60% after self-directed learning | SheetCopilot GPT-4 55% | +5 abs | FRIDAY starts at 0% before learning |
| Excel / PowerPoint case studies | Qualitative success after self-learning | No-learning variant fails | Positive | Demonstrates unseen-app adaptation |

- **Key ablation findings**:
  - FRIDAY without self-directed learning fails on the spreadsheet benchmark, while the learned variant reaches 60% success.
  - The paper's strongest evidence is not just baseline comparison; it is the before/after contrast showing that accumulated tools enable previously impossible application control.
  - The paper also makes a useful methodological point: self-improvement here is not parameter update but skill accumulation in procedural memory. That distinction matters because it aligns more with external-memory evolution than with continual model training.
- **Failure cases**:
  - Performance on harder GAIA levels remains low.
  - The system still depends heavily on prompt engineering and on whether the base model can generate or revise useful tools.

## Limitations

- **Author-stated limitations**:
  1. The system still relies heavily on prompt engineering.
  2. Better performance may require fine-tuning or reinforcement learning, but collecting the right data is difficult.
  3. Multimodal interaction remains underdeveloped.
  4. Evaluating subtask completion in OS environments is hard due to lack of exact ground truth and difficulty comparing states.
- **My observed limitations**:
  1. **procedural memory 是 tool-centric，不是 rule-centric**。FRIDAY 存的是可执行 tools，这很强，但还不是当前 main-line 需要的紧凑跨任务 procedural rules。
  2. **write-back 路径明显 success-biased**。高分 tools 会被保留，但论文没有展示强的 failure-aware consolidation 机制去在失败后改写 memory。
  3. **memory 架构显式、粒度仍粗**。working / declarative / procedural memory 的命名很清楚，但具体内容与更新策略没有像后续 memory papers 那样被细致研究。
  4. **框架范围大于 GUI**。这有助于 generality，但也意味着 GUI-specific memory 问题只被部分隔离出来。
- **Experimental design gaps**:
  - No careful ablation over memory contents or write-back policy.
  - Limited controlled evidence for long-horizon memory reuse across many application families.
  - Heavy reliance on case studies for unseen-application learning.
  - The paper does not isolate whether gains come primarily from better planning, better runtime interfaces, or the actual memory/self-learning loop; for your survey, this means FRIDAY is more valuable as a capability precursor than as a clean causal memory study.

## ⭐ Relation to My Research

### Position in Survey

- **Corresponding survey section/category**:
  OS-Copilot / FRIDAY 应放在 GUI_Agent 线中，作为早期且重要的 **system-side precursor to self-improving computer agents**。按当前 main-line，它最重要的价值是支撑 `A-3`：OS / GUI 层的 system-level self-improvement 是可行的，但这仍不等于细粒度的 post-task procedural write-back。

- **Role**: Bridge paper and historical precursor for GUI self-improvement

### Gap Signals (extracted from this paper)

- Gap signal 1: FRIDAY stores and reuses **tools**, but not compact cross-task procedural deltas, so the representation is still too coarse for the `A-1` target.
- Gap signal 2: The self-improvement loop emphasizes successful tool accumulation more than failure-aware memory revision, so `A-4` remains only partially addressed.
- Gap signal 3: The paper explicitly points out the difficulty of OS-level evaluation, which means stronger memory claims need richer diagnostics than final task success alone.

这篇论文的重要性在于，它证明这条路不是空想：computer agent 确实可以通过积累可复用 procedural artifacts 来持续改进。但它还没有给出当前主线真正想要的 memory object。FRIDAY 的 procedural memory 本质上是 tool repository，不是 experience-delta rule store；它的 revision 机制也还不是 principled 的 failure-driven write-back loop。

### Reusable Elements

- **Methodology**:
  - The tripartite decomposition of declarative, procedural, and working memory is directly reusable as survey scaffolding.
  - The idea that execution feedback flows back into working memory and then can update long-term memory is a useful precursor to later write-back designs.
  - Self-directed learning as curriculum generation for unfamiliar apps is an important systems blueprint.
  对当前主线，最值得复用的是 **system slotting**：什么应放进 working memory，什么应进入 long-term knowledge，以及 feedback 应该从哪里注入。反而不该直接照搬的是 “tool-as-skill” 这一假设，因为主线想要的 procedural unit 比完整 tool 更细。

- **Experimental design**:
  - The before/after self-directed-learning evaluation on unseen applications is a good template for demonstrating real adaptation.
  - Its limitation as an evaluation template is equally important: future GUI memory work should avoid relying only on before/after case studies and should report repeated-task or cross-task diagnostics more directly.

### Connections to Other Papers in Knowledge Base

- Relative to [2023_AppAgent.md](./2023_AppAgent.md), FRIDAY is broader and more system-oriented.
- Relative to [2024_MobileGPT.md](./2024_MobileGPT.md), it has a clearer self-improvement story but weaker GUI-specific grounding.
- Relative to [2025_MAGNET.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2025_MAGNET.md), it is earlier and conceptually coarser: MAGNET has more explicit memory modules for appearance and workflow drift.
- Relative to [2024_AWM.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2024_AWM.md), FRIDAY stores tools whereas AWM stores abstracted workflows; the latter is closer to your current procedural-memory target.

## Citation Tracking

- [ ] OS-Copilot / FRIDAY (Wu et al., 2024): system-level self-improving computer agent reference
- [ ] GAIA (Mialon et al., 2023): general assistant benchmark
- [ ] SheetCopilot (Li et al., 2023): spreadsheet-control baseline
- [ ] AppAgent / MobileGPT / MAGNET: later GUI-memory systems for comparison

## Key Passages

> "FRIDAY is a self-improving embodied agent for automating general computer tasks." (Abstract, p.1)

> "the working memory module is responsible for retrieving information from and updating the long-term memory." (Section 2.2.3, p.4)

> "showcasing strong generalization to unseen applications via accumulated skills from previous tasks." (Abstract, p.1)
