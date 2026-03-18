# MAGNET — Dual-level memory (stationary + procedural) enables cross-app-version GUI agent adaptation

## Meta
- **Title**: MAGNET: Towards Adaptive GUI Agents with Memory-Driven Knowledge Evolution
- **Authors**: Libo Sun, Jiwen Zhang et al. | Fudan University & University of Southern California
- **Venue**: Preprint Jan 2026 | arXiv:2601.19992
- **Links**: [PDF](../source/MAGNET.pdf)
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-05
- **Priority**: P0 | **Reading progress**: Pass 2

## One-line Summary
复旦大学与 USC 的 MAGNET 为 planner-actor GUI agent 引入双层记忆，即 stationary memory（visual UI patches -> stable functional semantics）与 procedural memory（abstract task workflows），并配合 dynamic evolution 机制；它在 AndroidWorld 上达到 42.62%，高于 Agent-S 的 40.98% 与 AppAgent 的 34.43%，同时在三个离线 benchmark 上也优于无记忆基线。

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
  1. **workflow 抽象仍偏 coarse**：procedural memory 由聚类后归纳出的 workflow 构成，适合 similarity-based reuse，但距离主线要求的 fine-grained experience-delta rule 还有一步。
  2. **成功轨迹依赖仍强**：stationary 与 procedural 两层 memory 都建立在成功样本上，冷启动和新域失败场景下缺乏自举能力。
  3. **迁移证据仍偏单一路径**：continual adaptation 主要验证 Amex → AndroidWorld 的持续替换，尚不足以证明更广的 app-family 泛化。
  4. **memory 增益不是万能补丁**：在 AITZ / GUI-Odyssey 上的优势有限，说明 memory 设计虽有效，但仍受 backbone、benchmark 分布和任务粒度约束。
- **Experimental design gaps**: Offline benchmarks use step-level success rate, not end-to-end task completion rate — performance on harder long-horizon tasks may not be well-captured. The online AndroidWorld evaluation uses only Qwen2.5-VL-32B as the backbone, leaving open the question of whether stronger backbones further amplify MAGNET's gains in the online setting.

## ⭐ Relation to My Research

### Position in Survey
- **Corresponding survey section/category**:
  MAGNET 是当前主线里最重要的 **partial solution / strongest baseline**。它已经弱占位了 `post-task / Skills / 相似性检索 × 上下文注入` 这格，因此写综述时应作为 GUI procedural memory 的当前最佳实践来讨论；但必须同时明确，它仍未解决 failure-driven write-back，也还没有把 workflow memory 提升为更细粒度、可稳定改写的 experience-delta rule。
- **Role**: Positive example (current SOTA for memory-augmented GUI agents) + Gap signal provider (shows what remains unsolved)

### Gap Signals (extracted from this paper)
- Gap signal 1: "The framework requires successful trajectories for memory construction, making it less effective in completely novel domains where initial exploration fails." (Limitations, p.9) → 无法从失败轨迹构建记忆，离线进化能力受限（直接对应Gap A-4：No offline experience evolution for GUI agents）
- Gap signal 2: "memory-augmented systems … mainly focus on text-based workflow descriptions that lack multimodal knowledge, making them vulnerable to visual changes in UI elements" (Introduction, p.1) → 即使MAGNET引入了视觉patch，仍是检索式的点对点匹配，缺乏结构化的多模态情景记忆流（对应Gap A-2）
- Gap signal 3: "the clustering-based workflow extraction may struggle with highly diverse task structures that do not form clear patterns." (Limitations, p.9) → procedural memory 目前仍依赖 task clustering 质量，说明其跨任务迁移粒度和技能抽象稳定性还不够强。

MAGNET 对主线的价值有三层：(1) 它证明 GUI procedural memory 在 system level 上已经可行，不再只是理论空白；(2) 它提供了 memory construction、ranking、injection 的完整工程参考；(3) 它又恰好把主线剩余问题暴露得很清楚，即 success-only evolution 仍不足以支持 A-4 所要求的 failure-aware memory rewriting。因此它是最强 baseline，但不是终点。

### Reusable Elements
- **Methodology**: (1) The `<functional_description, visual_patch>` pair representation for stationary memory is directly reusable as multimodal memory unit design; (2) The Ebbinghaus-inspired retention score `R_i = exp(-g_i/n_i)` is a clean, principled memory prioritization formula adaptable to other dynamic memory systems; (3) The planner–actor separation with memory injected at different levels is a good architectural template.
  以当前主线看，最合理的复用方式不是照搬 MAGNET，而是做三处改造：(1) 保留双层分工思路，但把 procedural memory 从 coarse workflow 推进一步到 finer-grained experience-delta rule；(2) 把 retention 机制扩展为 success / failure aware，使其支持 memory rewrite 而不仅是 success-only accumulation；(3) 视需要使用 UI-40K 或其构建流程作为冷启动资源，而不是把数据集本身当成方法核心。
- **Experimental design**: (1) AndroidWorld online evaluation protocol (self-exploration → memory initialization → evaluation) is a standard reproducible setup; (2) The ID/TS/AS/DS subset design for GUI-Odyssey and Amex is a rigorous distribution-shift evaluation framework worth replicating; (3) Continual adaptation experiment (Table 5: iterative deployment + memory update) is a good template for evaluating offline/online memory evolution.

### Connections to Other Papers in Knowledge Base
- 与 [2023_AppAgent.md](./2023_AppAgent.md) 构成直接升级关系：MAGNET 把 text doc 路线推进到 multimodal grounding + workflow memory。
- 与 Agent_Memory 的术语对齐时，stationary memory 对应 semantic memory，procedural memory 对应 workflow-level procedural memory，但系统仍缺少真正的 episodic replay layer。
- 与 Self_Evolve 的关系在于：它已经做到了受限的 offline evolution，但仍停留在 success-only accumulation，而不是 failure-aware rewriting。
- 在 [gap-tracker.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/gap-tracker.md) 中，它应继续作为 A-1 的 `Current Best Partial Solution`；同时它也是 A-4 未被解决的最强反证材料。

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
