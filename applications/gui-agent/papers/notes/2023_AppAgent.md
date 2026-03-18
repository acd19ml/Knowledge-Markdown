# AppAgent — Exploration-based knowledge document enables smartphone app operation without system access

## Meta
- **Title**: AppAgent: Multimodal Agents as Smartphone Users
- **Authors**: Chi Zhang et al. | Tencent
- **Venue**: Preprint Dec 2023; published CHI 2025 | arXiv:2312.11190
- **Links**: [PDF](../source/AppAgent.pdf) | [Project](https://appagent-official.github.io/)
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-05
- **Priority**: P0 | **Reading progress**: Pass 2

## One-line Summary
腾讯的 AppAgent 使用 GPT-4V 和“两阶段 exploration-then-deploy”框架，在不依赖系统 API 的前提下通过 GUI actions 操作手机 app；当知识文档来自 human demos 时，它在 10 个 app、50 个任务上达到 84.4% 的成功率。

## Problem Setting
- **Core problem**: "creating a multimodal agent capable of operating diverse smartphone apps presents significant challenges" — adapting models for embodied tasks requires extensive training data, and "collecting a large dataset of app demonstrations for training is a formidable task" (Introduction, p.2); further, "different apps have unique GUIs with varying icon meanings and operational logic, and it remains uncertain whether these adapted models can effectively generalize to unseen apps" (Introduction, p.2).
- **Assumptions**: Android OS environment; agent receives a real-time screenshot + XML file of interactive elements; backbone must support vision (GPT-4V); maximum 40 exploration steps and 10 deployment steps per task.
- **Insufficiency of existing approaches**: Existing intelligent phone assistants like Siri "operate through system back-end access and function calls" (Introduction, p.2), making them non-universal. Text-only LLM agents cannot handle visual GUIs. Models produce inaccurate XY coordinates for direct interaction — "LLM struggles with producing accurate xy coordinates" (Section 4.2, p.7).

## Core Method

AppAgent operates in two sequential phases. In the **Exploration Phase**, the agent learns app-specific UI element functions either through autonomous interaction or by watching human demonstrations. During autonomous exploration, the agent uses trial-and-error: it interacts with UI elements, observes before/after screenshots, and compiles findings into a per-app text document that records each element's function and the effect of actions upon it. The agent skips irrelevant pages (e.g., advertisement pages) using `Back()`, making exploration goal-oriented rather than exhaustive. When watching human demonstrations, the agent observes a human operating the app and records only the elements and actions the human used, producing a more accurate and efficient knowledge document.

In the **Deployment Phase**, the agent receives a task instruction and operates step-by-step. At each step it observes the current screenshot plus the dynamically generated knowledge document for the current UI page, reasons about its next action, executes it, and summarizes the interaction history into its next prompt — this summary serves as an in-context memory mechanism. The agent terminates when it invokes `Exit()` upon task completion.

The key enabler is the **simplified action space**: `tap(element)`, `long_press(element)`, `swipe(element, direction, dist)`, `text(str)`, `back()`, `exit()`. Elements are addressed by numeric identifiers overlaid on screenshots (derived from XML resource IDs or class+size+content combinations), eliminating the need for precise coordinate prediction.

**Key Design Choices**:
| Design Decision | Author's Choice | Author's Rationale | Ablation Verified? |
|----------------|----------------|--------------------|---------------------|
| Action space abstraction | Element-indexed actions (tap/swipe/text by element ID) instead of raw XY coordinates | "LLM struggles with producing accurate xy coordinates, while our simplified action space eliminates this challenging requirement" (p.7) | Yes — baseline with raw API: 2.2% SR vs. simplified: 48.9% SR |
| Knowledge document construction | Per-app text document updated through exploration | Eliminates need to fine-tune LLM or collect large training datasets per app; provides persistent external memory (p.2) | Yes — no doc: 48.9%, auto-explore doc: 73.3%, demo-watch doc: 84.4% |
| Exploration method | Watching human demos preferred over autonomous exploration | "watching human demonstrations proved to be highly effective … comparable to human-written documents" (p.7) | Yes — demo: 84.4% vs auto: 73.3% vs manual oracle: 95.6% |
| Backbone | GPT-4V | State-of-the-art vision-language capability for screenshot interpretation | No (only GPT-4V evaluated) |

- **Core difference from prior work**: Unlike prior GUI agents that rely on system API access or require fine-tuning on large annotated datasets, AppAgent (1) accesses no system back-end, (2) builds its own knowledge through lightweight exploration or demo-watching, and (3) uses a text knowledge document as an external long-term memory to bridge exploration and deployment phases.

## Key Results
| Benchmark | This Method | Strongest Baseline | Delta | Notes |
|-----------|------------|-------------------|-------|-------|
| 45 tasks, 9 apps (SR) | 84.4% (watching demos) | GPT-4 baseline, no doc: 48.9% | +35.5pp | Simplified action space used throughout |
| 45 tasks, 9 apps (SR) | 73.3% (auto exploration) | GPT-4 baseline: 48.9% | +24.4pp | |
| 45 tasks, 9 apps (SR) | 95.6% (manually crafted doc, oracle) | — | — | Upper-bound reference |
| Lightroom image editing (avg. rank) | 1.95 (demo-watch) vs 2.30 (GPT-4 baseline) | GPT-4 baseline: 2.30 | -0.35 rank | Lower rank = better; user study |

- **Key ablation findings**: (1) Simplified action space is critical — raw API drops SR from 48.9% to 2.2%. (2) Demo-watching doc quality is on par with manually crafted oracle docs (84.4% vs 95.6%), demonstrating exploration viability. (3) With a knowledge document, the agent uses more diverse tools during image editing tasks vs. the baseline.
- **Failure cases**: Not explicitly enumerated in the paper. Agent fails if the task cannot be completed within 10 steps. Complex multi-touch gestures and irregular gestures are not supported.

## Limitations
- **Author-stated limitations**: "We have adopted a simplified action space for smartphone operations, which means that advanced controls such as multi-touch and irregular gestures are not supported. This limitation may restrict the agent's applicability in some challenging scenarios." (Conclusion/Limitation, p.8)
- **My observed limitations**:
  1. **per-app 文档孤岛**：知识文档按 app 单独维护，迁移边界停留在单 app 内，无法支持主线所要求的 `post-task -> cross-task` procedural reuse。
  2. **表示粒度过粗**：文档记录的是“元素-动作-效果”描述，而不是带触发条件、约束和失败信号的 procedural rule，更接近 semantic doc 而非可改写的 procedural memory。
  3. **无失败写回机制**：部署阶段的失败不会回流为 memory edit / split / rewrite，因此不具备 A-4 所要求的 failure-driven write-back。
  4. **视觉鲁棒性不足**：纯文本知识文档无法稳定覆盖 UI 外观漂移和视觉定位问题，这也是后续 MAGNET 要引入视觉 patch memory 的直接动机。
- **Experimental design gaps**: Lightroom is excluded from the main SR evaluation because "assessing task completion in this application presented inherent ambiguities" (p.7) — this creates a gap where the most vision-demanding app is not quantitatively evaluated on success rate.

## ⭐ Relation to My Research

### Position in Survey
- **Corresponding survey section/category**:
  AppAgent 应放在 GUI Agent 综述的 **Memory-Augmented GUI Agents / Exploration-built Knowledge** 小节，作为外部知识文档路线的代表基线。按当前主线，它不是 procedural memory 的正例，而是 `pre-task exploration + app-bound semantic memory` 的典型系统，用来和后续的 MobileGPT / MAGNET 对照。
- **Role**: Positive example (pioneer of exploration-based knowledge document approach) + Contrastive baseline (lacks procedural/episodic memory)

### Gap Signals (extracted from this paper)
- Gap signal 1: "collecting a large dataset of app demonstrations for training is a formidable task. Moreover, different apps have unique GUIs with varying icon meanings and operational logic, and it remains uncertain whether these adapted models can effectively generalize to unseen apps." (Introduction, p.2) → 每次遇到新app都需要重新探索，缺乏跨app程序性知识迁移机制（对应Gap A-1）
- Gap signal 2: "We have adopted a simplified action space for smartphone operations, which means that advanced controls such as multi-touch and irregular gestures are not supported." (Conclusion/Limitation, p.8) → 现有知识文档和动作接口仍覆盖不了更复杂的 GUI 操作形态，说明 procedure abstraction 还受 action-space 上限约束。
- Gap signal 3: "This information is compiled into a document that records the effects of actions applied to different elements." (Section 3.3, p.5) → 记忆被压缩为元素-动作效果文档，而不是保留 richer visual episode；这为后续多模态 episodic memory 设计留下了空间。

AppAgent 对当前主线的价值在于提供一个清晰的“起点基线”：它证明 exploration → external knowledge → deployment 这条路线有效，但也同时暴露了主线要解决的三处核心缺口：`semantic doc ≠ procedural rule`、`app-bound reuse ≠ cross-task reusable memory`、`document lookup ≠ failure-driven write-back`。因此它是 A-1 与 A-4 的直接对比基线，而不是目标解法本身。

### Reusable Elements
- **Methodology**: The exploration → document → deploy pipeline is directly reusable as a baseline framework. The element-indexed action space design is standard and can be adopted as-is in new frameworks.
  可直接复用的部分主要有三项：(1) exploration → document → deploy 这一最小闭环可作为无训练 procedural-memory baseline；(2) goal-directed exploration 协议适合作为经验收集阶段的数据生成器；(3) 元素级动作效果记录可作为后续 procedural rule 抽象前的原始证据层，但需要再向上抽象成带 `context / constraint / failure signal` 的 memory unit。
- **Experimental design**: The 50-task / 10-app benchmark setup is widely adopted as a baseline evaluation protocol. The three-metric design (SR + Reward + Avg. Steps) is transferable.

### Connections to Other Papers in Knowledge Base
- 与 [2025_MAGNET.md](./2025_MAGNET.md) 构成直接前后继关系：MAGNET 的双层记忆就是对 AppAgent 文本文档路线的多模态化和 workflow 化升级。
- 与 Agent_Memory 的术语对齐时，AppAgent 更应归为 **Semantic Memory / app knowledge document**，而不是 Procedural Memory。
- 在 [comparison-matrix.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/comparison-matrix.md) 中，它是 `Semantic Doc (per-app)` 的代表；在 [gap-tracker.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/gap-tracker.md) 中，它是 A-1 与 A-4 的典型缺失案例。

## Citation Tracking
- [ ] AppAgentV2 (Li et al., 2024): extends AppAgent with flexible mobile interactions — should check if procedural memory gap is addressed
- [ ] MAGNET (Sun et al., 2025): directly extends AppAgent's memory design with dual-level memory for cross-app transferability
- [ ] Agent-S (Agashe et al., 2024): another memory-augmented agent using workflow-level memory, compared against in AndroidWorld

## Key Passages
> "Central to our agent's functionality is its innovative learning method. The agent learns to navigate and use new apps either through autonomous exploration or by observing human demonstrations. This process generates a knowledge base that the agent refers to for executing complex tasks across different applications." (Abstract, p.1)

> "documents generated through autonomous exploration and observing human demonstrations proved to be highly effective. Their results consistently outperformed the GPT-4 baseline and are comparable to the results of human-written documents, which highlights the efficacy of our design in enhancing the agent's performance across a diverse set of applications." (Section 4.2, p.7)

> "This information is incorporated into the next prompt, which provides the agent with a form of memory." (Section 3.3, p.5) — 注：这里的"memory"实际是in-context的interaction summary，是一种ephemeral working memory，并非持久化的长期记忆。
