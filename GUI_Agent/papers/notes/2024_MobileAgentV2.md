# Mobile-Agent-v2 — Multi-agent collaboration solves long-context navigation in mobile device operation

## Meta
- **Title**: Mobile-Agent-v2: Mobile Device Operation Assistant with Effective Navigation via Multi-Agent Collaboration
- **Authors**: Junyang Wang et al. | Beijing Jiaotong University / Alibaba Group
- **Venue**: Preprint, June 2024 | arXiv:2406.01014
- **Links**: [PDF](./Mobile-Agent-v2.pdf) | [Code](https://github.com/X-PLUG/MobileAgent)
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-05
- **Priority**: P0 | **Reading progress**: Pass 2

## One-line Summary
Wang et al. propose a three-agent (Planning + Decision + Reflection) architecture with a Memory Unit for task-relevant focus content, achieving >30% SR improvement over single-agent Mobile-Agent v1 on dynamic mobile device operation benchmarks covering HarmonyOS and Android.

## Problem Setting
- **Core problem**: "The two major navigation challenges in mobile device operation tasks — task progress navigation and focus content navigation — are difficult to effectively solve under the single-agent architecture of existing work. This is due to the overly long token sequences and the interleaved text-image data format, which limit performance." (Abstract, Page 1)
- **Assumptions**: Agent operates on real mobile devices (HarmonyOS / Android via ADB); screen perception relies on an external Visual Perception Module (VPM) rather than end-to-end MLLM; no task-specific training — relies on prompting GPT-4 / GPT-4V.
- **Insufficiency of existing approaches**: "As the task progresses, the lengthy history of interleaved image and text history operations and screens as input can significantly reduce the effectiveness of navigation in a single-agent architecture." (Section 1, Page 2). Mobile-Agent v1 (Wang et al., 2024) uses a pure single-agent GPT-4V pipeline that degrades on long sequences and multi-app tasks.

## Core Method

Mobile-Agent-v2 decomposes mobile operation into three specialized agent roles that run in a pipeline each iteration. First, the **Planning Agent** (text-only GPT-4) reads the user instruction, the previous operation, and the previous task progress, then emits an updated pure-text task progress summary `TP_t = PA(Ins, O_{t-1}, TP_{t-1}, FC_{t-1})`. By converting the interleaved image-text history into a compact text summary, context length is dramatically reduced for the downstream decision step.

The **Decision Agent** (GPT-4V) receives the current task progress, the current screen's visual perception results (from the VPM: OCR + icon detection + icon description), the focus content from the Memory Unit, and any reflection feedback from the previous step. It generates the next operation `O_t = DA(Ins, TP_{t-1}, FC_{t-1}, R_{t-1}, S_t, P_t)` and simultaneously determines whether the current screen contains task-relevant focus content; if so, it updates the Memory Unit: `FC_t = DA(Ins, FC_{t-1}, S_t, P_t)`. The operation space is constrained to six primitives: OpenApp, Tap, Swipe, Type, Home, Stop.

The **Reflection Agent** (GPT-4V) observes the screen states before and after each operation to classify the outcome as correct, erroneous (navigated to wrong page — triggers rollback), or ineffective (no screen change). Erroneous and ineffective operations are excluded from the operation history to prevent the Decision Agent from repeating them. The Memory Unit acts as a short-term working memory that persists task-relevant focus content (e.g., weather data queried in one app that needs to be referenced when composing a message in another app) across steps without relying on full screenshot history.

**Key Design Choices**:
| Design Decision | Author's Choice | Author's Rationale | Ablation Verified? |
|----------------|----------------|--------------------|---------------------|
| History compression | Planning Agent converts interleaved image-text history → pure-text task progress | Reduces context length; easier for Decision Agent to navigate progress | Yes (Table 4: removing Planning Agent causes largest SR drop) |
| Focus content persistence | Separate Memory Unit updated by Decision Agent | Task-relevant content from earlier screens (other apps) is lost if only task progress text is used | Yes (Table 4: removing Memory Unit hurts multi-app tasks most) |
| Error correction | Reflection Agent classifies each operation; erroneous ops trigger rollback | MLLMs produce hallucinations even at GPT-4V level; errors compound in long sequences | Yes (Table 4: removing Reflection Agent degrades performance) |
| Operation space restriction | Six fixed primitives | Reduces decision complexity; avoids unconstrained output | No explicit ablation |
| Planning Agent model | Text-only GPT-4 (not MLLM) | Planning does not require screen perception; cheaper and faster | No |

- **Core difference from prior work**: Unlike Mobile-Agent v1 (single GPT-4V agent with full image-text history in context), Mobile-Agent-v2 uses role specialization: one agent compresses history, one agent acts, one agent verifies. The Memory Unit explicitly separates "focus content" (semantic working memory) from the operation history, which is a novel architectural choice for mobile GUI agents.

## Key Results

| Benchmark | This Method | Strongest Baseline | Δ | Notes |
|-----------|------------|-------------------|---|-------|
| Non-English (HarmonyOS) — Basic SR | 17/20 (85%) | Mobile-Agent: 7/20 (35%) | +50 pp | System + External apps |
| Non-English (HarmonyOS) — Advanced SR | 11/20 (55%) | Mobile-Agent: 4/20 (20%) | +35 pp | System + External apps |
| English (Android) — Basic SR | 18/20 (90%) | Mobile-Agent: 16/20 (80%) | +10 pp | System + External apps |
| English (Android) — Advanced SR | 13/20 (65%) | Mobile-Agent: 7/20 (35%) | +30 pp | System + External apps |
| Multi-app — Basic SR | 2/2 (100%) | Mobile-Agent: 3/4 (75%) | +25 pp | Largest gain for multi-app |
| Multi-app — Advanced SR | 2/2 (100%) | Mobile-Agent: 1/4 (25%) | +75 pp | Strongest signal for Memory Unit value |
| Average improvement (English scenario) | — | — | +27% SR | Paper-stated aggregate |

- **Key ablation findings**: Removing the Planning Agent produces the largest performance drop among the three components, confirming that long-context navigation is the dominant bottleneck for single-agent systems. The Memory Unit provides the most critical benefit in multi-app tasks where focus content must span app boundaries. (Table 4, Page 9)
- **Failure cases**: Even with knowledge injection, Decision Accuracy does not reach 100%, showing that erroneous decisions are unavoidable; reflection partially mitigates but does not eliminate them. In advanced single-app tasks, success rate is still only 55%–65%, indicating that complex task understanding remains an open problem. Errors in single-agent architecture "predominantly occur in the later stages of the tasks" (Section 4.3.3, Page 9), a pattern eliminated by the multi-agent design.

## Limitations
- **Author-stated limitations**: The paper notes that "manually injected operation knowledge can mitigate the limitations of an agent's operation capability" (Section 4.3, Page 8) — implying the system still requires human-authored hints for the hardest tasks. The knowledge injection results also highlight that automated knowledge generation is a future direction: "automating the generation of high-quality operation knowledge can further improve the performance of Mobile-Agent-v2" (Page 8).
- **My observed limitations**:
> ⚠️ NEEDS YOUR INPUT: 1) Memory Unit 是纯文本短期记忆，随任务结束清空，没有跨任务持久化能力——每个新任务都从零开始，无法积累过去任务的操作经验（即缺少 A-1 所定义的程序性记忆/技能库）。2) 论文的评测集是作者自设的 88 条指令（非公开基准），可复现性有限。3) Planning Agent 压缩历史的质量完全依赖 GPT-4 的摘要能力，若压缩失真则误差传播给 Decision Agent，此风险未做量化分析。4) 系统不支持离线学习或轨迹回放，失败经验被直接丢弃（对应 A-4 gap）。
- **Experimental design gaps**: Benchmark is author-designed with only 88 instructions across 10 apps per OS; no comparison against AppAgent or AutoDroid (only Mobile-Agent v1 as baseline). Evaluation is dynamic (live device) which reduces reproducibility. No latency/cost breakdown is reported.

## ⭐ Relation to My Research

### Position in Survey
- **Corresponding survey section/category**: GUI_Agent survey — Section on Multi-Agent Architectures for Mobile GUI Agents; also relevant to Memory & State Management subsection.
> ⚠️ NEEDS YOUR INPUT: 建议放在 GUI Agent 综述的「多智能体协作」分支下，作为任务级工作记忆（working memory）的典型正例。与 AppAgent（单智能体探索）形成对比。在 Cross_Topic/comparison-matrix.md 与 Cross_Topic/gap-tracker.md 中可作为 working memory 的代表案例引用。

### Gap Signals (extracted from this paper)
- Gap signal 1: "automating the generation of high-quality operation knowledge can further improve the performance of Mobile-Agent-v2" (Section 4.3, Page 8) → 作者明确承认缺乏自动化知识生成（即 A-1 技能库自动构建），这是直接支持 A-1 gap 的作者自我陈述。
- Gap signal 2: "we design a memory unit to store the focus content related to the current task from history screens" (Section 3.2, p.4-5) → 作者明确把 Memory Unit 定义为 current-task scoped working memory，而不是跨任务可复用的 procedure memory。
- Gap signal 3: Failed operations are discarded from history (Page 6): "Neither erroneous nor ineffective operations are recorded in the operation history to prevent the agent from following these operations." → 失败轨迹被主动丢弃，无法用于离线学习（A-4 gap 的直接证据）。

> ⚠️ NEEDS YOUR INPUT: 这篇论文的 gap signal 价值极高。Memory Unit 明确只解决了「当前任务内」的焦点内容保留问题，完全没有触及跨任务技能积累。知识注入实验（Section 4.3）间接证明：若有结构化操作知识库，性能可进一步显著提升——这正是 A-1 要构建的东西。此论文可以作为「现有工作已有 working memory，但缺少 procedural/skill memory」这一论断的强有力引用。

### Reusable Elements
- **Methodology**: The three-agent decomposition pattern (progress tracker + decision maker + verifier) is directly transferable. For a memory-augmented GUI agent, the Planning Agent role could be extended to also query a persistent skill library instead of only summarizing recent history.
> ⚠️ NEEDS YOUR INPUT: Planning Agent 的「历史压缩→纯文本任务进度」机制可复用于技能库检索的触发点设计：每次规划时不仅生成任务进度，还查询历史相似任务的操作程序。Reflection Agent 的三分类（correct/erroneous/ineffective）可直接用作离线经验标注的标签体系，为 A-4 离线进化提供训练信号。
- **Experimental design**: Dynamic evaluation on real devices (HarmonyOS + Android, ADB) with four metrics (SR/CR/DA/RA) is a solid evaluation framework. Multi-app task design is particularly useful for benchmarking cross-app memory retrieval.

### Connections to Other Papers in Knowledge Base
> ⚠️ NEEDS YOUR INPUT: 1) 与 Agent_Memory/（LLM Agent Memory Survey）的关联：Memory Unit 对应 Cognitive Types 中的 working memory（短期、任务内）；与 A-1 gap 中缺失的 procedural memory 形成互补。2) 与 Self_Evolve/ 的关联：反思智能体（Reflection Agent）是一种在线自我评估机制，但没有将反思结果持久化用于未来任务，是 Self-Evolve 框架中「经验积累」环节的缺失。3) 与 MobileGPT（本批次另一篇）的关联：MobileGPT 解决了跨任务子任务复用问题（A-1 方向），而 Mobile-Agent-v2 解决了单任务内长上下文导航问题——两者互补，一起形成对 A-1+A-4 gap 的完整论证。

## Citation Tracking
- [ ] Mobile-Agent (Wang et al., 2024, arXiv:2401.16158): 直接前作，single-agent baseline
- [ ] AppAgent (Zhang et al., 2023, arXiv:2312.11190): 对比工作，XML-based localization
- [ ] AutoGen (Wu et al., 2024): multi-agent 框架，作为 related work 被引

## Key Passages
> "The two major navigation challenges in mobile device operation tasks — task progress navigation and focus content navigation — are difficult to effectively solve under the single-agent architecture of existing work. This is due to the overly long token sequences and the interleaved text-image data format, which limit performance." (Abstract, Page 1)

> "The memory unit serves as a short-term memory module that is updated as the task progresses. The memory unit is crucial for scenarios involving multiple apps." (Section 3.2, Page 4)

> "The planning agent's inputs consist of four parts: user instruction Ins, the focus content FC_t in memory unit, the previous operation O_{t-1}, and the previous task progress TP_{t-1}." (Section 3.3, Page 5)

> "Neither erroneous nor ineffective operations are recorded in the operation history to prevent the agent from following these operations." (Section 3.5, Page 6)

> "automating the generation of high-quality operation knowledge can further improve the performance of Mobile-Agent-v2" (Section 4.3, Page 8)

> "From the results of multiple apps, it can be seen that Mobile-Agent-v2 achieves improvements of 37.5% and 44.2% in SR and CR, respectively, compared to Mobile-Agent." (Section 4.3.1, Page 8)
