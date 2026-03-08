# Mobile-Agent-v2 — Multi-agent collaboration solves long-context navigation in mobile device operation

## Meta
- **Title**: Mobile-Agent-v2: Mobile Device Operation Assistant with Effective Navigation via Multi-Agent Collaboration
- **Authors**: Junyang Wang et al. | Beijing Jiaotong University / Alibaba Group
- **Venue**: Preprint, June 2024 | arXiv:2406.01014
- **Links**: [PDF](../source/Mobile-Agent-v2.pdf) | [Code](https://github.com/X-PLUG/MobileAgent)
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-05
- **Priority**: P0 | **Reading progress**: Pass 2

## One-line Summary
Wang et al. 提出由 Planning、Decision 与 Reflection 组成的三智能体架构，并加入用于存储 task-relevant focus content 的 Memory Unit；该设计在 HarmonyOS 与 Android 的动态移动设备操作任务上，相比单智能体 Mobile-Agent v1 带来超过 30% 的成功率提升。

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
  1. **仅覆盖任务内 working memory**：Memory Unit 明确服务于当前任务，任务结束即失效，无法形成主线所需的 cross-task reusable procedural memory。
  2. **摘要链条脆弱**：Planning Agent 的文本压缩是下游决策的唯一历史接口，但论文没有量化摘要失真如何影响后续 action quality。
  3. **失败经验被主动舍弃**：Reflection Agent 虽能发现错误，却不把错误转化为可持久化经验，这是 A-4 的直接缺口。
  4. **评测外部效度有限**：88 条作者自建指令足以证明架构有效，但不足以说明这种 working-memory 设计在标准长期记忆 benchmark 上的稳定性。
- **Experimental design gaps**: Benchmark is author-designed with only 88 instructions across 10 apps per OS; no comparison against AppAgent or AutoDroid (only Mobile-Agent v1 as baseline). Evaluation is dynamic (live device) which reduces reproducibility. No latency/cost breakdown is reported.

## ⭐ Relation to My Research

### Position in Survey
- **Corresponding survey section/category**: GUI_Agent survey — Section on Multi-Agent Architectures for Mobile GUI Agents; also relevant to Memory & State Management subsection.
  Mobile-Agent-v2 应放在 GUI Agent 综述的 **Multi-Agent Architecture + Working Memory** 交叉位置。按当前主线，它不是 A-1 的正解，而是“现有系统已经能做 in-task memory compression / reflection，却仍没有 `post-task -> cross-task` procedural write-back”的代表性对照组。

### Gap Signals (extracted from this paper)
- Gap signal 1: "automating the generation of high-quality operation knowledge can further improve the performance of Mobile-Agent-v2" (Section 4.3, Page 8) → 作者明确承认缺乏自动化知识生成（即 A-1 技能库自动构建），这是直接支持 A-1 gap 的作者自我陈述。
- Gap signal 2: "we design a memory unit to store the focus content related to the current task from history screens" (Section 3.2, p.4-5) → 作者明确把 Memory Unit 定义为 current-task scoped working memory，而不是跨任务可复用的 procedure memory。
- Gap signal 3: Failed operations are discarded from history (Page 6): "Neither erroneous nor ineffective operations are recorded in the operation history to prevent the agent from following these operations." → 失败轨迹被主动丢弃，无法用于离线学习（A-4 gap 的直接证据）。

这篇论文的 gap signal 价值很高，因为它把边界画得很清楚：系统已经证明 **working memory + reflection** 能提升长程导航，但这类提升仍停留在单任务内；一旦任务结束，经验不再存在。知识注入实验又反过来说明，若系统拥有可复用的结构化操作知识，性能还会继续提升。因此它是“已有 in-task memory，但缺少 cross-task procedural memory”的强证据。

### Reusable Elements
- **Methodology**: 三智能体分解模式（progress tracker + decision maker + verifier）可以直接迁移。若扩展成 memory-augmented GUI agent，Planning Agent 不应只总结最近历史，还应承担 persistent skill library 的检索入口。
  最值得复用的不是 Memory Unit 本身，而是两个接口：(1) Planning Agent 产出的 `task progress` 可作为 procedural memory 检索触发器；(2) Reflection Agent 的 `correct / erroneous / ineffective` 三分类可直接作为 failure-aware write-back 的标签体系，用来决定 memory 是保留、降权还是改写。
- **Experimental design**: Dynamic evaluation on real devices (HarmonyOS + Android, ADB) with four metrics (SR/CR/DA/RA) is a solid evaluation framework. Multi-app task design is particularly useful for benchmarking cross-app memory retrieval.

### Connections to Other Papers in Knowledge Base
- 与 Agent_Memory 的对齐很直接：Memory Unit 是 **working memory**，不是 long-term procedural memory。
- 与 Self_Evolve 的关系在于：Reflection Agent 已经具备在线错误识别能力，但没有任何跨任务沉淀，恰好停在“自我评估”而非“经验积累”之前。
- 与 [2024_MobileGPT.md](./2024_MobileGPT.md) 形成互补：前者解决 in-task navigation，后者提供 app 内 procedural reuse；两者合起来反而更能凸显当前系统仍缺失 `failure-driven cross-task write-back`。

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
