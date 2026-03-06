# AppAgent — Exploration-based knowledge document enables smartphone app operation without system access

## Meta
- **Title**: AppAgent: Multimodal Agents as Smartphone Users
- **Authors**: Chi Zhang et al. | Tencent
- **Venue**: Preprint Dec 2023; published CHI 2025 | arXiv:2312.11190
- **Links**: [PDF](./AppAgent.pdf) | [Project](https://appagent-official.github.io/)
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-05
- **Priority**: P0 | **Reading progress**: Pass 2

## One-line Summary
Tencent's AppAgent uses GPT-4V with a two-phase exploration-then-deploy framework to operate smartphone apps via GUI actions (no system API access), achieving 84.4% task success rate on 50 tasks across 10 apps when using human-demo-based knowledge documents.

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
> ⚠️ NEEDS YOUR INPUT: 知识库是per-app的纯文本文档，存在以下问题：(1) 知识不能跨app迁移——每个新app都需要重新探索，无法复用已学到的UI模式；(2) 探索阶段生成的文档与任务强相关，不同任务可能需要不同的探索过程；(3) 没有对失败轨迹的学习机制，离线进化能力缺失；(4) 文本文档无法捕捉视觉外观信息，面对UI外观漂移时鲁棒性存疑。
- **Experimental design gaps**: Lightroom is excluded from the main SR evaluation because "assessing task completion in this application presented inherent ambiguities" (p.7) — this creates a gap where the most vision-demanding app is not quantitatively evaluated on success rate.

## ⭐ Relation to My Research

### Position in Survey
- **Corresponding survey section/category**:
> ⚠️ NEEDS YOUR INPUT: 对应survey中"训练无关/推理时记忆增强"方法类别（planner-actor框架下的知识库方法）。在GUI Agent综述的Memory部分，AppAgent是最具代表性的"外部知识文档"方法——通过exploration生成per-app文本文档作为语义记忆（Semantic Memory），但缺乏程序性记忆（Procedural Memory）和跨app知识迁移能力。建议放在 §Memory-Augmented GUI Agents 下，作为"基线/对比方法"。
- **Role**: Positive example (pioneer of exploration-based knowledge document approach) + Contrastive baseline (lacks procedural/episodic memory)

### Gap Signals (extracted from this paper)
- Gap signal 1: "collecting a large dataset of app demonstrations for training is a formidable task. Moreover, different apps have unique GUIs with varying icon meanings and operational logic, and it remains uncertain whether these adapted models can effectively generalize to unseen apps." (Introduction, p.2) → 每次遇到新app都需要重新探索，缺乏跨app程序性知识迁移机制（对应Gap A-1）
- Gap signal 2: "We have adopted a simplified action space for smartphone operations, which means that advanced controls such as multi-touch and irregular gestures are not supported." (Conclusion/Limitation, p.8) → 现有知识文档和动作接口仍覆盖不了更复杂的 GUI 操作形态，说明 procedure abstraction 还受 action-space 上限约束。
- Gap signal 3: "This information is compiled into a document that records the effects of actions applied to different elements." (Section 3.3, p.5) → 记忆被压缩为元素-动作效果文档，而不是保留 richer visual episode；这为后续多模态 episodic memory 设计留下了空间。

> ⚠️ NEEDS YOUR INPUT: AppAgent对研究的价值：它是Gap A-1（程序性记忆）和A-4（离线进化）最直接的对比基线。其知识文档设计思路（exploration → document → deploy）是本研究可以改进的出发点：(1) 将per-app文档升级为跨app可迁移的程序性技能库；(2) 引入离线进化机制，从历史轨迹（包括失败轨迹）中持续更新知识库；(3) 引入截图级别的多模态记忆以应对UI外观变化。

### Reusable Elements
- **Methodology**: The exploration → document → deploy pipeline is directly reusable as a baseline framework. The element-indexed action space design is standard and can be adopted as-is in new frameworks.
> ⚠️ NEEDS YOUR INPUT: 具体可复用之处：(1) 知识文档的数据结构（元素名、xpath、截图描述、动作效果）可作为程序性记忆条目设计的参考；(2) 探索阶段的goal-directed exploration策略（遇到无关页面就Back()）可作为memory construction的数据收集协议；(3) 将in-context的interaction history summary扩展为持久化的episodic memory是自然的研究方向。
- **Experimental design**: The 50-task / 10-app benchmark setup is widely adopted as a baseline evaluation protocol. The three-metric design (SR + Reward + Avg. Steps) is transferable.

### Connections to Other Papers in Knowledge Base
> ⚠️ NEEDS YOUR INPUT: (1) MAGNET (2025_MAGNET.md) 在AndroidWorld上直接与AppAgent对比，AppAgent得34.43% vs MAGNET 42.62%——MAGNET的双层记忆正是针对AppAgent文本文档不能应对视觉漂移的弱点设计的；(2) 与Agent_Memory/中的"Procedural Memory"定义对应——AppAgent的知识文档是语义记忆(Semantic Memory)而非程序性记忆，关键区别在于没有可跨任务重用的抽象工作流；(3) GUI_Agent/comparison-matrix.md中AppAgent已被收录，可更新其"Memory Type"字段为"Semantic Doc (per-app)"；(4) Cross_Topic/gap-tracker.md中A-1 Procedural Memory和A-4 Offline Evolution两个Gap的典型缺失案例就是AppAgent。

## Citation Tracking
- [ ] AppAgentV2 (Li et al., 2024): extends AppAgent with flexible mobile interactions — should check if procedural memory gap is addressed
- [ ] MAGNET (Sun et al., 2025): directly extends AppAgent's memory design with dual-level memory for cross-app transferability
- [ ] Agent-S (Agashe et al., 2024): another memory-augmented agent using workflow-level memory, compared against in AndroidWorld

## Key Passages
> "Central to our agent's functionality is its innovative learning method. The agent learns to navigate and use new apps either through autonomous exploration or by observing human demonstrations. This process generates a knowledge base that the agent refers to for executing complex tasks across different applications." (Abstract, p.1)

> "documents generated through autonomous exploration and observing human demonstrations proved to be highly effective. Their results consistently outperformed the GPT-4 baseline and are comparable to the results of human-written documents, which highlights the efficacy of our design in enhancing the agent's performance across a diverse set of applications." (Section 4.2, p.7)

> "This information is incorporated into the next prompt, which provides the agent with a form of memory." (Section 3.3, p.5) — 注：这里的"memory"实际是in-context的interaction summary，是一种ephemeral working memory，并非持久化的长期记忆。
