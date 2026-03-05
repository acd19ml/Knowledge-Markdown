# MobileGPT — Human-like hierarchical app memory enables reusable sub-task learning for mobile automation

## Meta
- **Title**: MobileGPT: Augmenting LLM with Human-like App Memory for Mobile Task Automation
- **Authors**: Sunjae Lee et al. | KAIST (with Simon Fraser University)
- **Venue**: ACM MobiCom 2024 (The 30th Annual International Conference on Mobile Computing and Networking, November 18–22, 2024, Washington D.C.) | arXiv:2312.10190 (per DOI: 10.1145/3636534.3690682)
- **Links**: [PDF](./MobileGPT.pdf) | [Code](https://mobile-gpt.github.io/)
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-05
- **Priority**: P0 | **Reading progress**: Pass 2

## One-line Summary
Lee et al. (KAIST) propose MobileGPT, which emulates human app learning via an Explore-Select-Derive-Recall pipeline backed by a three-level hierarchical app memory (task / sub-task / action), achieving 82.7% task learning accuracy and 98.75% recall accuracy on 185 tasks across 18 apps, with 62.5% latency and 68.8% cost reductions versus a GPT-4-powered baseline.

## Problem Setting
- **Core problem**: "The inherent non-deterministic and unpredictable nature of LLMs can undermine the reliability and consistency of task automation. This is critical in mobile environments as many mobile tasks nowadays involve sensitive and private information. Second, LLMs are costly, both in terms of budget and time." (Section 1, Page 1). Existing LLM-based automators treat every task execution as independent, discarding learned procedures and incurring full LLM inference costs on repetition.
- **Assumptions**: Mobile tasks are recurrent and share sub-tasks across different user instructions. The system has offline exploration access to app screens before task execution. LLM services (GPT-3.5 and GPT-4) are available via API. Screen layout is accessible via Android Accessibility Service (text-based HTML representation). Vision-based screens (Flutter, WebApps, image-dominated) are not covered by the current implementation.
- **Insufficiency of existing approaches**: "We observed that tasks that would take just over 30 seconds for a human could take more than two minutes for an LLM, and cost over a dollar each time they are performed." (Section 1, Page 1). Prior approaches (AutoDroid, AppAgent) store task procedures at the task level, causing redundant learning of shared sub-tasks; they also cannot adapt learned actions to new parameters or screen changes.

## Core Method

MobileGPT emulates the human cognitive process of learning a new mobile app by decomposing it into four phases: **Explore, Select, Derive, and Recall**. During the offline **Explore** phase (conducted before task execution), MobileGPT uses a random explorer and user trace monitor to visit app screens and asks the LLM to enumerate available sub-tasks for each screen in a structured function-call format: `{name, description, params, UI_index}`. This builds a per-app transition graph of known sub-tasks without requiring any user task to be issued.

At task execution time, the **Select** phase prompts the LLM with the user instruction, the current screen's HTML representation (derived from Android Accessibility Service, pruned to interactive elements, reducing token count by an average of 84.6%), and the list of known sub-tasks for that screen. The LLM picks the most relevant sub-task and fills in its parameters. If a required parameter is missing from the instruction, MobileGPT asks the user (interactive slot-filling). If the chosen sub-task already exists in memory, it is executed directly, bypassing the Derive phase.

The **Derive** phase incrementally executes low-level primitive actions (click, input, scroll, long-click) to complete the selected sub-task. Actions are stored in a generalized format: screen generalization replaces screen-specific UI indices with stable UI attributes (id, text, description), and parameter generalization replaces literal values with parameter names (e.g., `click(id:"contact", text:"[contact_name]")`). This two-step generalization ensures that stored actions remain reusable under parameter changes and screen content variations.

The three-level **hierarchical memory** (task → sub-task → action) is organized as an app-level transition graph where nodes represent app pages (grouped by shared sub-task lists, not visual appearance) and edges represent sub-task execution sequences. Critically, sub-task knowledge is shared across tasks: once MobileGPT learns how to "search for a contact" in Telegram for the task "Send a message to Bob," this sub-task is reused when executing "Send a message to Alice" or "Open chat with Alex." During the **Recall** phase, if the instruction matches a known task, MobileGPT replays the sub-task sequence, bypassing all three learning phases and only performing slot-filling and in-context action adaptation for contextual differences. A dual-strategy failure handling mechanism combines rule-based self-feedback generation and human-in-the-loop (HITL) task repair.

**Key Design Choices**:
| Design Decision | Author's Choice | Author's Rationale | Ablation Verified? |
|----------------|----------------|--------------------|---------------------|
| Memory granularity | Three-level hierarchy (task / sub-task / action) | Sub-task sharing minimizes redundant learning across tasks that share common operations | Yes (Table 2: sub-task phase accuracy shows 96–99% per phase) |
| Sub-task representation | Function-call format with typed parameters | Enables precise parameterization; handles implicit/incomplete instructions at sub-task boundary | Yes (ablation baseline uses Derive-only; MobileGPT outperforms even on cold-start) |
| Screen representation | Simplified HTML from Android Accessibility Service | LLMs comprehend GUIs better in HTML syntax; prunes non-interactive elements, 84.6% token reduction | Implicitly (AutoDroid's list-based representation loses hierarchical info and performs worse) |
| Screen classification | Sub-task-based (functionality) rather than appearance | Screens with different appearances but same sub-tasks should share memory; appearance-based fails this | Yes (269 screens: 3 false positives, 0 false negatives vs. 38/14 for text-based, 57/28 for vision-based SotA) |
| Offline exploration | Random explorer + user trace monitor pre-task | Proactively caches sub-tasks, eliminates Explore overhead for known screens during live tasks | Yes ($10.78 one-time cost for 89.65% page coverage; warm-start 87–90% latency reduction) |
| Action recall | Attribute-based adaptation + LLM few-shot fallback | Rule-based is fast and reliable; LLM fallback handles edge cases where attributes are ambiguous | Yes (53/327 actions needed LLM in-context adaptation; 100% adaptation accuracy) |

- **Core difference from prior work**: Unlike AutoDroid and AppAgent which treat each task independently and re-run full LLM inference every time, MobileGPT's hierarchical memory enables sub-task-level reuse across tasks. The key novelty is app-level memory organized as a transition graph (not a task-level lookup table), allowing sub-tasks to be shared across any tasks within the same app. This is structurally analogous to how humans build app familiarity, not just task-specific scripts.

## Key Results

| Benchmark | This Method | Strongest Baseline | Δ | Notes |
|-----------|------------|-------------------|---|-------|
| Overall task success rate (cold-start) | 82.7% | AutoDroid: 74.7% | +8.0 pp | 185 tasks, 18 apps |
| Overall task success rate (warm-start) | 82.16% | AutoDroid: 74.7% | +7.5 pp | Near-identical to cold-start |
| Task recall accuracy (warm-start) | 98.75% | — | — | MobileGPT own dataset, 80 tasks |
| Latency reduction (warm-start vs. baseline) | 62.5% reduction | — | — | Baseline = Derive-only structure with same prompts |
| Cost reduction (warm-start vs. baseline) | 68.8% reduction | — | — | GPT-4-turbo + GPT-3.5 pricing |
| AutoDroid dataset | 86.8% (cold) / 85.7% (warm) | AutoDroid: 83.5% | +3.3 pp cold | 7 apps, 91 tasks |
| AppAgent dataset | 50.0% (cold+warm) | AppAgent: 27.3% | +22.7 pp | 3 complex apps |
| Screen classification (false positives) | 3 / 269 | Text-based SotA: 38 | 12.7x fewer | Sub-task-based classification |

- **Key ablation findings**: MobileGPT's cold-start already outperforms the Derive-only baseline due to task decomposition and sub-task sharing. During warm-start, near-perfect accuracy (98.75%) is achieved because HITL-corrected cold-start executions are stored in memory, preventing LLM non-determinism from causing repeated errors. Memory hit rate (Table 3) ranges from 6.7% (Gmail, few overlapping sub-tasks) to 98.6% (Telegram, heavy contact search reuse). Step accuracy across Explore (96.4%), Select (96.2%), Derive (99.1%), slot-filling (99.5%), in-context adaptation (100%) confirms each phase is individually reliable. (Table 2, Page 11)
- **Failure cases**: Gmail has the lowest memory hit rate (6.7%) because its tasks have few overlapping sub-tasks. Warm-start had one additional failure compared to cold-start due to an error in memory recall (UberEats). The attribute-based adaptation fails when target UI lacks key attributes, multiple UIs share attributes, or app updates change UI structure — falling back to LLM in-context adaptation, which introduces non-determinism.

## Limitations
- **Author-stated limitations**: (1) Current implementation does not support apps without text-based screen layouts (Flutter, WebApps, image-dominated screens such as maps/camera) — VLM extension is discussed as future work. (Section 9, Page 14). (2) Cross-app task execution (e.g., "Check bank account, and if it has over $10, order me a pizza") is not currently supported but identified as a future extension via a global cross-app task dataset. (Section 9, Page 14). (3) App memory is stored locally per device; crowd-sourcing or sharing app memory across users is proposed as future work that could eliminate individual cold-start learning. (Section 9, Page 14).
- **My observed limitations**:
> ⚠️ NEEDS YOUR INPUT: 1) 系统依赖离线 Explore 阶段预建 sub-task 图，每个新 app 都需要一次性探索成本（约 10-15 分钟 + $10.78），在 app 快速更新（UI 变更）场景下维护成本高。2) 记忆是 app 级别的（per-app transition graph），每个 app 独立存储，无法跨 app 泛化子任务（如「搜索联系人」在 Telegram 和 Gmail 中分别存储，不共享）——这是 A-1 gap 中「跨 app 技能复用」的缺口。3) 失败轨迹最终通过 HITL 修复后才存入记忆，没有自动从失败经验中学习的机制（A-4 gap）。4) 评测基准（185 任务）由作者自建，数据集规模偏小，缺乏与标准 GUI Agent 基准的对比。
- **Experimental design gaps**: Dataset is self-constructed (MobileGPT dataset: 80 tasks / 8 apps) with only partial coverage of AutoDroid and AppAgent datasets; no AndroidWorld, AITW full-set, or AitZ evaluation. HITL task repair is disabled in comparative study but enabled in ablation, creating inconsistency. Evaluation on a single device (Google Pixel 6) limits generalizability.

## ⭐ Relation to My Research

### Position in Survey
- **Corresponding survey section/category**: GUI_Agent survey — Memory & Knowledge Reuse subsection; most directly relevant to A-1 (procedural memory / skill library) gap.
> ⚠️ NEEDS YOUR INPUT: 这篇论文是目前 GUI Agent 领域最接近 A-1 gap（程序性记忆）的现有工作。建议在 Cross_Topic/gap-tracker.md 的 A-1 gap 条目下将其列为「已有工作」的最强基线，同时指出其局限（per-app 存储、依赖人工修复、无跨 app 泛化）作为 gap 仍然存在的论据。在 GUI_Agent/ 的 survey notes 中，应在「Memory」章节重点介绍。

### Gap Signals (extracted from this paper)
- Gap signal 1: "MobileGPT currently stores memory on a local basis, meaning each device has its own version of app memory." (Section 9, Page 14) → 记忆无法跨用户/跨设备共享，作者明确承认这是限制，指向 A-1 中「共享/可扩展技能库」的需求。
- Gap signal 2: "Cross App Task execution... MobileGPT can be extended to maintain a global dataset of known tasks across apps." (Section 9, Page 14) → 跨 app 任务无法处理，作者将其列为 future work，这是 A-1 gap 中「跨 app 程序性记忆」的直接证据。
- Gap signal 3: The HITL task repair mechanism means that learning from failures requires human intervention — no automatic failure-driven learning. Failed trajectories, unless repaired by humans, are not leveraged. This is a direct structural gap matching A-4 (offline evolution from failed trajectories).
- Gap signal 4: The offline Explore phase is a one-time preparation step, not a continuous learning process. App updates requiring memory refresh are not addressed, pointing to the lack of online/offline experience evolution (A-4).

> ⚠️ NEEDS YOUR INPUT: MobileGPT 的 gap signal 价值在于：它已经实现了「子任务级别的程序性记忆」，但被限制在 per-app、per-device 范围内，且依赖 HITL 修复失败。这意味着研究空间是：(a) 将 sub-task 记忆从 app 级提升为 cross-app、cross-domain 的通用技能库（A-1 核心方向）；(b) 将 HITL 修复替换为自动的失败轨迹学习（A-4 方向）。此论文是迄今为止最相关的 related work，应在 proposal 中详细讨论其局限。

### Reusable Elements
- **Methodology**: The function-call format for sub-task representation is directly reusable for encoding skills in a procedural memory library. The transition graph structure can inspire a cross-app skill graph design. The attribute-based action generalization mechanism is a concrete technique for making stored actions context-independent.
> ⚠️ NEEDS YOUR INPUT: 具体复用建议：1) Sub-task 的 function-call 格式（name, desc, params, UI_index）可直接作为技能库的存储格式，无需重新设计。2) Sub-task-based screen classification（用子任务列表表征页面，而非视觉外观）可用于跨 app 技能检索：在新 app 中找到具有相同子任务集的页面，直接复用已学技能。3) 失败轨迹的 HITL 修复 pipeline 可以作为半自动标注框架，用于训练离线经验学习模型（A-4 方向的数据收集方法）。
- **Experimental design**: The cold-start / warm-start evaluation paradigm is essential for benchmarking any memory-augmented GUI agent. Memory hit rate per app is a useful metric for quantifying memory utilization. The 185-task, 18-app dataset (combining AutoDroid + AppAgent + MobileGPT datasets) provides a reasonable starting evaluation scope.

### Connections to Other Papers in Knowledge Base
> ⚠️ NEEDS YOUR INPUT: 1) 与 Agent_Memory/（记忆综述）：MobileGPT 的三层记忆（task/sub-task/action）对应认知记忆分类中的程序性记忆（procedural memory）+ 工作记忆的结合体。在 agent memory 综述中被归为 external memory / parametric memory 的哪一类？值得对照。2) 与 Self_Evolve/（自进化综述）：MobileGPT 的「Recall → HITL修复 → 存回记忆」流程是一种 human-in-the-loop 的轻量进化机制，但不满足 Self_Evolve 综述中定义的「自主」进化条件（需要自动化）。3) 与 Mobile-Agent-v2（本批次）：互补关系——Mobile-Agent-v2 解决单任务内的工作记忆（working memory），MobileGPT 解决跨任务的程序性记忆（procedural memory）。两者结合构成一个更完整的记忆架构。4) 与 Cross_Topic/gap-tracker.md 的 A-1 gap：MobileGPT 是 A-1 的最强 related work，应在 gap tracker 的 A-1 条目中更新「已有工作」字段。

## Citation Tracking
- [ ] AutoDroid (Wen et al., 2023): 直接对比基线，LLM + Android UI text representation
- [ ] AppAgent (Zhang et al., 2023): 直接对比基线，vision-language mobile automation
- [ ] (Li et al., [22] in paper): A-mash, multi-app UI mashup — related work on multi-app interaction
- [ ] AITW (Rawles et al., 2022, [53] in paper): 标准 GUI Agent 数据集，MobileGPT 未评测，应补充对比

## Key Passages
> "MobileGPT emulates the cognitive process of humans interacting with a mobile app — explore, select, derive, and recall. This approach allows for a more precise and efficient learning of a task's procedure by breaking it down into smaller, modular sub-tasks that can be re-used, re-arranged, and adapted for various objectives." (Abstract, Page 1)

> "MobileGPT employs a three-level hierarchical memory structure: tasks, sub-tasks, and actions. This hierarchy enables MobileGPT to access memory at the sub-task level, facilitating the sharing of past execution experience across different tasks." (Section 1, Page 2)

> "MobileGPT organizes its memory in the form of a transition graph that encapsulates the following key information: i) available sub-tasks of each app screen (Explore), ii) sequence of sub-tasks involved in each task (Select), and iii) how to perform each sub-task (Derive). Note that these graphs exist per app, not per task, meaning that tasks within the same app all share the same graph." (Section 4.1, Page 6)

> "MobileGPT currently stores memory on a local basis, meaning each device has its own version of app memory. To enhance this, the memory can be shared or crowd-sourced to create a large-scale app memory." (Section 9, Page 14)

> "MobileGPT achieves a task completion rate of 82.7% when executing a new task, outperforming these systems by 8% and 15.3% respectively. Furthermore, MobileGPT achieves a near-perfect (98.75%) success rate in adapting learned tasks to a new instruction with different task parameters." (Section 1, Page 2)

> "MobileGPT suggests that MobileGPT achieves a 62.5% reduction in task completion time and a 68.8% decrease in LLM query costs when recalling learned tasks." (Section 1, Page 2)
