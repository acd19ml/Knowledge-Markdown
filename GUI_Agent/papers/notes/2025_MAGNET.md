# MAGNET — Dual-level memory (stationary + procedural) enables cross-app-version GUI agent adaptation

## Meta
- **Title**: MAGNET: Towards Adaptive GUI Agents with Memory-Driven Knowledge Evolution
- **Authors**: Libo Sun, Jiwen Zhang et al. | Fudan University & University of Southern California
- **Venue**: Preprint Jan 2026 | arXiv:2601.19992
- **Links**: [PDF](./MAGNET.pdf)
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-05
- **Priority**: P0 | **Reading progress**: Pass 2

## One-line Summary
Fudan/USC's MAGNET equips a planner–actor GUI agent with dual-level memory — stationary memory (visual UI patches → stable functional semantics) + procedural memory (abstract task workflows) — plus a dynamic evolution mechanism, achieving 42.62% on AndroidWorld vs. Agent-S 40.98% and AppAgent 34.43%, while also outperforming memory-free baselines on three offline benchmarks.

## Problem Setting
- **Core problem**: "frequent updates altering UI appearance and reorganizing workflows cause agents trained on historical data to fail" (Abstract, p.1). Two specific failure modes: (1) **appearance drift** — "UI elements are redesigned without altering their functions (e.g., the icon transition from Twitter to X)"; (2) **workflow drift** — "operation logic is reorganized across app versions (e.g., the task of 'changing the currency to USD')" (Introduction, p.1).
- **Assumptions**: Mobile GUI environment (Android); planner–actor multi-agent decomposition; memory can be initialized from offline datasets or self-exploration; backbone is a frozen MLLM (no fine-tuning); evaluation uses AndroidWorld (online) and AITZ / GUI-Odyssey / Amex (offline).
- **Insufficiency of existing approaches**: "existing specialized models are trained on fixed datasets that will be outdated as applications evolve, which limits them to generalize to evolving interface states" (Introduction, p.1). Memory-augmented systems "mainly focus on text-based workflow descriptions that lack multimodal knowledge, making them vulnerable to visual changes in UI elements" (Introduction, p.1). Specifically, AppAgent "stores UI elements and their functions using element identifiers from XML page structures" — identifier-based storage is fragile when page structure changes; Agent-S "emphasizes workflow-level memory but lacks grounded UI representations" (Section 3.2, p.6).

## Core Method

MAGNET is a memory-driven adaptive agent framework built on a planner–actor architecture. Its novelty lies in two complementary memory modules that exploit different forms of stability beneath surface-level app changes.

**Procedural Memory** (planner-side) addresses workflow drift by storing abstract, reusable task workflows distilled from completed trajectories. Each workflow entry consists of a task category name and a sequence of high-level steps with categorical placeholders (e.g., `[AppName]`, `[SearchQuery]`), enabling reuse across different contexts and interface versions. Construction involves three stages: (1) trajectory collection from human demos or curated datasets; (2) task clustering via cosine similarity on instruction embeddings (MiniCPM-Embedding) with maximal clique extraction; (3) workflow abstraction — a planner LLM synthesizes per-cluster common patterns into abstract workflows. At inference, incoming instructions retrieve the top-K most similar workflows, which are injected into the planner's context to guide task decomposition into subtasks.

**Stationary Memory** (actor-side) addresses appearance drift by storing pairs `<d_i, v_i>` where `d_i` is a natural-language functional description (e.g., "click the search icon to start searching") and `v_i` is the corresponding visual patch of the UI element. When the planner generates a subtask involving UI element localization, the subtask description queries stationary memory via cosine similarity to retrieve the top matching `<description, visual patch>` pairs. These visual patches are then concatenated into the actor's context as exemplars, enabling robust grounding despite visual redesigns of UI elements. For specialized grounding models with fixed input formats, retrieved patches are injected via template-matching to the current screenshot to produce a bounding box hint.

**Dynamic Memory Evolution** ensures memories stay current as apps update. A retention score `R_i = exp(-g_i / n_i)` (inspired by the Ebbinghaus forgetting curve) combines inactivity gap `g_i` and total retrieval count `n_i`, so frequently accessed entries decay more slowly. A two-stage retrieval uses semantic similarity for candidate selection followed by retention score + creation timestamp ranking to prioritize recent, well-validated knowledge. New workflows and UI element pairs extracted from successful task trajectories are automatically added; redundant entries are deduplicated via similarity checking.

**Key Design Choices**:
| Design Decision | Author's Choice | Author's Rationale | Ablation Verified? |
|----------------|----------------|--------------------|---------------------|
| Dual-level memory decomposition | Stationary (UI-level) + Procedural (workflow-level) | "decoupling memory representations from page-specific identifiers while jointly modeling UI-level and workflow-level knowledge" (p.6); each addresses a distinct form of drift | Yes — Table 3: combined > either alone |
| Stationary memory representation | Visual patch + functional description (multimodal) | Text-only descriptions are "vulnerable to visual changes in UI elements" (p.1); visual patches provide appearance-invariant grounding | Yes — stationary memory contributes +0.26%–+0.88% Grd. improvement |
| Memory ranking | Retention score R_i = exp(-g_i/n_i) + creation timestamp | Inspired by Ebbinghaus forgetting curve; balances usage frequency (reliability) and recency (currency) | Indirectly — Table 5: memory evolution shows improving SR over 3 iterations |
| Procedural memory construction | Clustering-then-abstracting pipeline | Groups similar tasks before distillation to ensure workflows are general enough to cover task variants | Yes — procedural memory contributes +2.66% SR on AMEX (larger than stationary) |
| UI-40K dataset | 41,009 multimodal entries from AITZ + GUI-Odyssey + Amex | Provides pre-built stationary memory initialization; also usable for GUI grounding and offline RL | Indirectly validated via offline benchmark results |

- **Core difference from prior work**: AppAgent stores per-app text documents indexed by XML element identifiers (fragile to UI updates); Agent-S stores workflow-level text memory without grounded visual UI representations. MAGNET is the first to combine (1) multimodal visual-functional pairs for appearance-robust grounding and (2) abstract procedural workflows for workflow-drift adaptation, under a unified dynamic evolution mechanism.

## Key Results
| Benchmark | This Method | Strongest Baseline | Delta | Notes |
|-----------|------------|-------------------|-------|-------|
| AndroidWorld (online SR) | 42.62% (MAGNET, Qwen2.5-VL-32B) | Agent-S: 40.98% | +1.64pp | Memory-augmented agent category |
| AndroidWorld (online SR) | 42.62% | AppAgent: 34.43% | +8.19pp | |
| AITZ (offline SR) | 43.50% (Qwen) / 52.77% (Gemini-2.5-Pro) | Agent-S: 42.98% (Qwen) | +0.52pp / — | Agentic framework category; specialized models reach up to 66.64% |
| GUI-Odyssey (offline SR) | 50.16% (Qwen) / 49.74% (Gemini) | Agent-S: 49.21% (Qwen) | +0.95pp | |
| Amex (offline SR) | 62.84% (Qwen) / 62.23% (Gemini) | Agent-S: 58.29% (Qwen) | +4.55pp | |
| Cross-architecture avg. | +2.3% SR, +2.7% Grd. over no-memory baseline | — | — | Averaged over 5 planner–actor configs, Table 4 |

- **Key ablation findings**: (1) Both memory modules provide consistent individual gains; combined use achieves the best performance (Table 3). (2) Procedural memory contributes larger SR improvements (+2.66% on AMEX), while stationary memory contributes more to grounding accuracy (+0.26%–+0.88% Grd.) — they are complementary. (3) Heterogeneous planner–actor pairings (e.g., QwenVL planner + OS-Atlas actor) benefit the most (+4.2% SR), suggesting memory compensates for planning/execution module mismatches. (4) Continual adaptation (Table 5): starting from Amex-initialized memory, SR rises from 31.14% → 37.70% → 39.34% → 40.98% over 3 AndroidWorld iterations; Amex-derived memory share drops to 26% (procedural) and 18% (stationary), confirming online knowledge replacement.
- **Failure cases**: "The framework requires successful trajectories for memory construction, making it less effective in completely novel domains where initial exploration fails." (Limitations, p.9). "The clustering-based workflow extraction may struggle with highly diverse task structures that do not form clear patterns." (Limitations, p.9).

## Limitations
- **Author-stated limitations**: "The framework requires successful trajectories for memory construction, making it less effective in completely novel domains where initial exploration fails. Additionally, the clustering-based workflow extraction may struggle with highly diverse task structures that do not form clear patterns. Future work could explore zero-shot memory initialization and more flexible workflow representations." (Limitations, p.9)
- **My observed limitations**:
> ⚠️ NEEDS YOUR INPUT: (1) 程序性记忆的抽象工作流是通过聚类后让LLM归纳生成的，质量依赖聚类准确性和LLM的归纳能力，对稀有任务类型效果可能下降；(2) 静态记忆（stationary memory）的视觉patch + 文本描述对的构建需要成功的轨迹数据，冷启动时仍需大量人工演示或已有数据集；(3) 记忆进化实验（Table 5）是从Amex预热再在AndroidWorld上迭代，现实中跨平台迁移的有效性还需进一步验证；(4) 与专精模型（如Atlas-Pro-7B 66.64%）相比，MAGNET在in-distribution设置下仍有明显差距，记忆增强的收益在offline benchmark上相对有限（尤其是AITZ和GUI-Odyssey上的提升小于1%）。
- **Experimental design gaps**: Offline benchmarks use step-level success rate, not end-to-end task completion rate — performance on harder long-horizon tasks may not be well-captured. The online AndroidWorld evaluation uses only Qwen2.5-VL-32B as the backbone, leaving open the question of whether stronger backbones further amplify MAGNET's gains in the online setting.

## ⭐ Relation to My Research

### Position in Survey
- **Corresponding survey section/category**:
> ⚠️ NEEDS YOUR INPUT: MAGNET直接对应研究的核心关注点：(1) 程序性记忆（Procedural Memory）在GUI Agent中的实例化——对应Gap A-1的一个重要解决方案，可作为正面示例；(2) 离线经验进化（Offline Evolution）——其"dynamic memory evolution"机制涉及从历史成功轨迹中更新记忆库，部分回应了Gap A-4，但仍局限于成功轨迹，对失败轨迹的利用不足；(3) 多模态情景记忆——stationary memory存储视觉patch，部分回应Gap A-2。在GUI Agent survey的记忆章节中，MAGNET应作为"当前最佳实践"的正面示例，同时也展示了仍存在的Gap：记忆初始化仍需成功轨迹，无法从失败中离线学习。
- **Role**: Positive example (current SOTA for memory-augmented GUI agents) + Gap signal provider (shows what remains unsolved)

### Gap Signals (extracted from this paper)
- Gap signal 1: "The framework requires successful trajectories for memory construction, making it less effective in completely novel domains where initial exploration fails." (Limitations, p.9) → 无法从失败轨迹构建记忆，离线进化能力受限（直接对应Gap A-4：No offline experience evolution for GUI agents）
- Gap signal 2: "memory-augmented systems … mainly focus on text-based workflow descriptions that lack multimodal knowledge, making them vulnerable to visual changes in UI elements" (Introduction, p.1) → 即使MAGNET引入了视觉patch，仍是检索式的点对点匹配，缺乏结构化的多模态情景记忆流（对应Gap A-2）
- Gap signal 3: Procedural memory stores abstract workflows per task category; there is no mechanism to generalize across semantically related but categorically different tasks → 程序性记忆的迁移粒度较粗，依赖任务分类聚类，对细粒度技能（如"在任意app中搜索"这种原子操作）的跨场景复用支持不足（对应Gap A-1的深层问题）

> ⚠️ NEEDS YOUR INPUT: MAGNET对研究的核心价值：(1) 它是最接近"解决Gap A-1+A-4"的现有工作，可直接作为研究的强baseline——如果本研究在AndroidWorld或相同offline benchmarks上超过MAGNET，即为显著的positive result；(2) MAGNET的stationary memory构建流水线（triplet collection → region annotation → function description）是memory construction的工程参考，可以参考其UI-40K数据集的构建方式；(3) MAGNET的局限（只从成功轨迹学习）是本研究"从失败中学习/离线进化"这一研究方向的直接motivation支撑。

### Reusable Elements
- **Methodology**: (1) The `<functional_description, visual_patch>` pair representation for stationary memory is directly reusable as multimodal memory unit design; (2) The Ebbinghaus-inspired retention score `R_i = exp(-g_i/n_i)` is a clean, principled memory prioritization formula adaptable to other dynamic memory systems; (3) The planner–actor separation with memory injected at different levels is a good architectural template.
> ⚠️ NEEDS YOUR INPUT: 具体复用建议：(1) 保留双层记忆的架构划分（UI-level stationary + workflow-level procedural），但扩展stationary memory以支持跨app的功能语义聚合而不只是per-entry检索；(2) 将retention score机制扩展为同时考虑"成功/失败"标签，使记忆能从失败轨迹中降权低质知识；(3) UI-40K数据集可作为初始化记忆库的现成资源，节省冷启动成本。
- **Experimental design**: (1) AndroidWorld online evaluation protocol (self-exploration → memory initialization → evaluation) is a standard reproducible setup; (2) The ID/TS/AS/DS subset design for GUI-Odyssey and Amex is a rigorous distribution-shift evaluation framework worth replicating; (3) Continual adaptation experiment (Table 5: iterative deployment + memory update) is a good template for evaluating offline/online memory evolution.

### Connections to Other Papers in Knowledge Base
> ⚠️ NEEDS YOUR INPUT: (1) AppAgent (2023_AppAgent.md)：MAGNET在AndroidWorld上直接与AppAgent对比（42.62% vs 34.43%），MAGNET的双层记忆正是对AppAgent文本文档的multimodal升级和程序性升级。两篇笔记应相互交叉引用。(2) Agent_Memory/中的记忆类型分类：MAGNET的stationary memory对应"Semantic Memory"（元素功能语义），procedural memory对应"Procedural Memory"（任务工作流），但两者都缺乏"Episodic Memory"（情景历史回放）。(3) Self_Evolve/中的"自进化"框架：MAGNET的dynamic memory evolution是一种受限的自进化——只从成功轨迹进化，且是规则驱动而非模型驱动；与Self_Evolve/中更激进的进化方法（如基于反馈信号的策略更新）有显著差距，这正是研究的切入点。(4) Cross_Topic/gap-tracker.md：MAGNET是Gap A-1（Procedural Memory）的最新正面示例，应更新Gap A-1的"Current Best"字段；同时它也证实了Gap A-4（Offline Evolution）仍未被解决（其Limitation一节明确承认）。(5) GUI_Agent/comparison-matrix.md：应将MAGNET添加至comparison matrix，Memory Type字段填"Stationary(visual) + Procedural(abstract workflow)"。

## Citation Tracking
- [ ] AppAgent (Zhang et al., 2025/CHI): primary baseline — MAGNET improves +8.19pp SR on AndroidWorld over AppAgent
- [ ] Agent-S (Agashe et al., 2024, arXiv:2410.08164): memory-augmented agent with workflow memory but no visual grounding — MAGNET improves +1.64pp SR
- [ ] COAT (Zhang et al., 2024a / AITZ paper): memory-free baseline framework using chain-of-action-thought
- [ ] UI-40K dataset: MAGNET constructs and releases this 41,009-entry multimodal memory dataset — may be directly usable for future work
- [ ] Ebbinghaus (1885): inspiration for retention score formula — worth citing if adopting similar memory decay mechanism

## Key Passages
> "Building on this insight, we introduce MAGNET, a memory-driven adaptive agent framework with dual-level memory: stationary memory linking diverse visual features to stable functional semantics for robust action grounding and procedural memory capturing stable task intents across varying workflows." (Abstract, p.1)

> "Despite surface changes, functional semantics and task intents remain fundamentally stable." (Abstract, p.1) — 这是整篇论文的核心假设，是双层记忆设计的理论基础。

> "AppAgent stores UI elements and their functions using element identifiers from XML page structures, while Agent-S emphasizes workflow-level memory but lacks grounded UI representations. In contrast, MAGNET integrates stationary memory with multimodal grounding of UI elements and procedural memory with reusable workflows, enabling the agent to reason jointly over interface structure and action-level experience." (Section 3.2, p.6)

> "The framework requires successful trajectories for memory construction, making it less effective in completely novel domains where initial exploration fails." (Limitations, p.9) — 直接指出了Gap A-4（无法利用失败轨迹进行离线进化）。
