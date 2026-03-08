# Mobile-Agent-v3.5 / GUI-Owl-1.5 — Multi-platform native GUI agent with hybrid data flywheel and multi-platform RL

## Meta
- **Title**: Mobile-Agent-v3.5: Multi-platform Fundamental GUI Agents
- **Authors**: Haiyang Xu et al. | Tongyi Lab, Alibaba Group
- **Venue**: Preprint, February 2026 | arXiv:2602.16851
- **Links**: [PDF](../source/Mobile-Agent-v3.5.pdf) | [Code](https://github.com/X-PLUG/MobileAgent)
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-05
- **Priority**: P0 | **Reading progress**: Pass 2

## One-line Summary
Xu et al.（Alibaba Tongyi）用 hybrid data flywheel 与 MRPO reinforcement learning 训练 GUI-Owl-1.5（2B–235B），在 desktop / mobile / browser 三类平台上取得当前开源 SOTA：OSWorld 56.5%、AndroidWorld 71.6%、WebArena 48.4%、ScreenSpotPro 80.3%。

## Problem Setting
- **Core problem**: "The development of robust and practically usable GUI agents still faces several challenges. (1) The efficiency of real-world data collection: Collecting large-scale trajectories is costly to hamper the scalability of GUI datasets ... (2) The adaptation to multiple platforms ... (3) The comprehensive agentic capabilities: The General GUI Agent should be capable of completing tasks efficiently, not limited to GUI-only operations. It should also support tool/Model Context Protocol (MCP) invocation, short-term and long-term memory, multi-agent adaptation, and human–agent interaction." (Section 1, p.2)
- **Assumptions**: End-to-end learning from native agent models (rather than agentic frameworks on top of closed-source LLMs); multi-turn interactive decision-making; unified policy across mobile/desktop/browser.
- **Insufficiency of existing approaches**: "native agent models based on end-to-end learning have demonstrated great potential, rather than only building agent frameworks on top of closed-source models" (Section 1, p.2) — but they lack multi-platform unification, scalable trajectory generation pipelines, and robust RL training across heterogeneous device families.

## Core Method

**GUI-Owl-1.5** is built on Qwen3-VL and trained through a three-stage pipeline (pre-training → SFT → RL), offering instruct and thinking variants at 2B, 4B, 8B, 32B, and 235B-A22B parameters. The paper describes the system under the Mobile-Agent-v3.5 umbrella name but the resulting model family is called GUI-Owl-1.5.

**Hybird Data Flywheel** combines two complementary data tracks. For grounding, the pipeline generates hard grounding data through challenging app GUI synthesis (using MLLMs to render diverse professional-grade screenshots) and multi-window high-resolution composition, then extends coverage through trajectory-based grounding extraction, tutorial knowledge mining from software documentation/forums, and infeasible query generation. For trajectories, the framework builds a DAG-based task synthesis workflow: annotators encode application workflows as directed acyclic graphs; an automated agent then rolls out trajectories on real devices with checkpoint-based verification and truncation-repair to produce clean partially-correct supervision; human demonstrations fill gaps for unsolvable tasks; and a suite of web-rendering virtual environments (built via Vibe Coding) handles high-frequency primitive actions (scroll, drag, CAPTCHA-style scenarios) that real-world exploration cannot reliably cover.

**Unified Enhancement of Agent Capabilities** operates in three layers beyond raw trajectory data. First, GUI Knowledge Injection crawls software documentation, forums, and Q&A platforms to produce large-scale QA/VQA knowledge data, supplemented by world-modeling supervision (predicting screen state transitions from action-conditioned descriptions). Second, a Unified CoT Synthesis pipeline augments every trajectory step with screen observation, memory extraction, progress reflection, and tool invocation reasoning using a VLM, teaching the model to simultaneously record key on-screen facts and self-correct from execution failures. Third, Multi-Agent Collaboration data is collected via the Mobile-Agent-v3.5 framework (Manager/Worker/Reflector/Notetaker roles) to train the model to operate as both a standalone end-to-end agent and as role-specialized components inside multi-agent pipelines.

**MRPO (Multi-platform Reinforcement Policy Optimization)** addresses four RL challenges specific to multi-platform GUI training: (i) a single device-conditioned policy `π_θ(a|o,d)` unifies learning across `d ∈ {mobile, desktop, web}`; (ii) an online rollout buffer oversample-then-subsample mechanism (oversample `kn` trajectories, guarantee mixed-outcome groups) prevents collapsed GRPO groups without introducing off-policy bias; (iii) token-ID transport from inference to training eliminates log-probability inconsistencies caused by tokenization mismatches; (iv) alternating (interleaved) per-platform optimization trains on one device family at a time cyclically, preventing gradient interference between platforms. (Section 2.4.3, p.10-11)

**Context Management** uses a sliding window with hierarchical compression: the most recent N dialogue turns are retained in full multimodal fidelity, while earlier turns are condensed into a concatenated text summary of action conclusions, balancing immediate decision richness with long-horizon awareness. (Section 2.1, p.3-4)

**Key Design Choices**:
| Design Decision | Author's Choice | Author's Rationale | Ablation Verified? |
|----------------|----------------|--------------------|---------------------|
| Trajectory source | Hybrid: real device + virtual web-rendering environments | Real-world exploration fails on CAPTCHA/anti-bot; virtual envs give exact subtask-level feedback and scalable generation | Yes — removing virtual envs drops PC-Eval 75.4→42.0%, Mobile-Eval 86.7→50.0% (Table 11) |
| CoT augmentation | Unified CoT synthesis at every step (observation + memory + reflection + progress) | Enables long-horizon planning and in-context information retention across steps | Yes — removing CoT drops OSWorld 52.9→47.4%, AndroidWorld 71.6→65.0% (Table 10) |
| RL training strategy | Alternating (interleaved) per-platform vs. mixed-platform | Mixed-platform causes cross-device gradient conflicts; interleaved isolates adaptation per device | Yes — Figure 8(b) shows mixed-platform causes oscillation |
| RL task selection | Unstable-set-only training (tasks with mixed rollout outcomes) | Collapsing groups are uninformative; unstable tasks drive faster convergence and higher accuracy | Yes — Figure 8(a) shows faster convergence with unstable-set training |
| Model sizes | 2B/4B/8B/32B/235B instruct + thinking variants | Edge instruct models for real-time low-latency; cloud thinking models for complex planning; enables edge-cloud collaboration | Implicitly validated by benchmark scaling |

- **Core difference from prior work**: Unlike prior work that adapts general VLMs via agentic frameworks (Mobile-Agent-v2, AppAgent), GUI-Owl-1.5 is a natively trained model covering all platforms simultaneously with a single policy; it adds memory management and MCP tool invocation as first-class training objectives, not post-hoc add-ons.

## Key Results
| Benchmark | This Method | Strongest Baseline | Δ | Notes |
|-----------|------------|-------------------|---|-------|
| OSWorld-Verified | 56.5 (32B-Instruct) | UI-TARS-2: 53.1 | +3.4 | Best open-source; even 2B-Instruct (43.5) beats UI-TARS-72B-DPO (27.1) |
| AndroidWorld | 71.6 (8B-Thinking) | UI-TARS-2: 73.3 | −1.7 | On par with SOTA; 32B-Instruct also 69.8 |
| WebArena | 48.4 (32B-Thinking) | AgentSymbiotic-8B: 43.2 | +5.2 | Best open-source browser agent |
| VisualWebArena | 46.6 (32B-Thinking) | WALT+GPT-5: 52.9 | −6.3 | Best open-source; competitive with proprietary |
| OSWorld-MCP | 47.6 (32B-Instruct) | Claude-4-Sonnet: 43.3 | +4.3 | Outperforms leading proprietary on tool-use task |
| MobileWorld | 46.8 (32B-Instruct) | MAI-UI-235B-A22B: 41.7 | +5.1 | Best open-source on tool+GUI joint tasks |
| ScreenSpotPro | 80.3 (32B-Instruct+crop) | Gemini-3-Pro: 72.7 | +7.6 | 72.9 even without crop tool, beating Gemini-3-Pro |
| GUI-KnowledgeBench | 75.45 (32B-Instruct) | o3: 73.30 | +2.15 | Best overall including proprietary models |
| MemGUI-Bench (Easy) | 27.1 (32B native model) | Qwen3-VL-8B-Instruct: 18.8 | +8.3 | Best native model; workflow agents reach 41.7 |
| WindowsAgentArena | 44.76 (32B-Instruct) | UI-TARS-2: 50.1 | −5.3 | Best open-source multi-platform model |

- **Key ablation findings**:
  - Virtual environment trajectory production is critical: removing it collapses PC-Eval from 75.4% to 42.0% and Mobile-Eval from 86.7% to 50.0% (Table 11, p.17)
  - Unified CoT synthesis is essential for long-horizon tasks: removing it drops OSWorld by 5.5pp and AndroidWorld by 6.6pp (Table 10, p.17)
  - Interleaved (alternating) RL training outperforms mixed-platform training; unstable-task-focused RL converges faster than full-dataset training (Figure 8, p.18)
- **Failure cases**: On MemGUI-Bench easy tasks, native agent models (best: 27.1) still trail workflow-based agents (best: 41.7), indicating that even with explicit memory training, structured external orchestration provides complementary benefits for memory-intensive tasks.

## Limitations
- **Author-stated limitations**: Not explicitly enumerated as a dedicated limitations section, but the results section shows that on MemGUI-Bench "workflow agents reach 41.7" while the best native GUI-Owl-1.5-32B reaches 27.1 (Section 3.2.2, p.17), indicating that memory-intensive long-horizon tasks are still not fully solved by the native model alone. Table 2 / Table 9 also leave some large-model evaluations incomplete, so the end-to-end ceiling of the 235B family is not comprehensively established.
- **My observed limitations**:
  1. **native model 仍缺外部 procedural memory**：MemGUI-Bench 上 27.1 vs 41.7 的差距说明，单靠训练把“记忆管理”蒸馏进模型，还不足以替代显式 workflow / memory orchestration。
  2. **上下文压缩不等于 episodic retrieval**：sliding window + summary 只能缓解单 session 内的信息拥塞，不能覆盖跨任务 episode 检索或 cross-task reusable rule。
  3. **经验闭环停在预部署阶段**：Hybrid Data Flywheel 与 MRPO 都服务于训练期能力构建，部署后没有 memory write-back 通道。
  4. **训练基础设施成本高**：MRPO 依赖可 rollout 的真实或虚拟环境，对缺少沙箱的新平台并不轻量。
- **Experimental design gaps**: MemGUI-Bench evaluation is limited to "Easy" tasks only, leaving medium/hard task performance unreported. GUI-Owl-1.5-32B-Thinking is not benchmarked on WebArena/VisualWebArena (Table 2 shows "—" entries). The 235B variant lacks comprehensive end-to-end evaluation.

## ⭐ Relation to My Research

### Position in Survey
- **Corresponding survey section/category**:
  本文在综述中的最佳位置是 **Native Agent Models / Multi-platform Training** 主段落，并在 Memory 小节中作为“能力上限证据”引用。按当前主线，它不是 A-1/A-4 的正解，而是最强 native route 的 `insufficient positive case`：说明更强 backbone、更长训练配方和 RL 虽然重要，但仍不能自动替代 external procedural memory 与 failure-driven write-back。
- **Role**: Positive example (state-of-the-art baseline for GUI automation); also serves as a Contrastive baseline for memory and experience evolution gaps (A-1, A-4).

### Gap Signals (extracted from this paper)

- Gap signal 1: "short-term and long-term memory" listed as a key capability requirement but implemented only via sliding-window context compression + CoT annotation — no persistent cross-session or cross-app memory store. (Section 1, p.2; Section 2.1, p.3-4) → **A-2 gap**: multimodal episodic memory (screenshot-based memory stream retrieval) is entirely absent.

- Gap signal 2: "Among native agent models, GUI-Owl-1.5-32B achieves 27.1, substantially outperforming all prior baselines ... Even our 8B variant (22.9) surpasses all existing native baselines, confirming that our training recipe effectively instills long-horizon memory capabilities without relying on external workflow orchestration." (Section 3.2.2, p.17) — yet workflow agents hit 41.7, a 14pp gap. → **A-1 gap**: no procedural skill/knowledge base that accumulates reusable task templates across sessions and apps.

- Gap signal 3: The Hybrid Data Flywheel is defined through pre-deployment DAG synthesis, checkpoint verification, truncation-repair, and curated trajectory production (Sections 2.2-2.3, p.4-9) → 论文没有描述部署后从真实用户轨迹持续写回模型/记忆库的机制，因此 post-deployment experience evolution 仍是空白。

- Gap signal 4: "we design a unified chain-of-thought (CoT) synthesis pipeline that augments all trajectory data with step-wise observation, reflection, memory management, and tool invocation reasoning" (Section 1 / Abstract, p.1) — memory management here means extracting key info within a single trajectory, not retrieving from a historical episodic store. → Reinforces A-2: the distinction between in-context memory and external episodic memory is architecturally unaddressed.

以当前主线判断，本文对三个 gap 的价值并不对称：A-1 与 A-4 是核心，A-2 是配套支撑。具体来说，MemGUI-Bench 的 14pp 差距直接强化了 A-1 的研究必要性；Hybrid Data Flywheel 则说明“更强训练 pipeline”并没有消除 A-4 所要求的部署后经验写回需求；A-2 在本文中的主要价值是提供 memory benchmark 与 negative evidence，而不是提供主方法对象。

### Reusable Elements
- **Methodology**:
  - The **DAG-based trajectory synthesis** (directed acyclic graph over atomic subtasks with checkpoint predicates) is directly reusable as a structured memory encoding format: each DAG path can be stored as a procedural memory episode with verified subtask completion states.
  - The **CoT synthesis pipeline** (observation → memory extraction → reflection → progress update) defines a step-level memory annotation schema that could be adapted to build an episodic memory stream (A-2).
  - The **Notetaker role** in the multi-agent framework (`N_{t+1} = u_C(N_t, S_{t+1})` if success) is a lightweight persistent note mechanism that could be extended into a retrieval-augmented procedural memory bank.
  对主线最有价值的复用不是整套 training recipe，而是三项局部资产：(1) DAG/checkpoint 表达可作为程序性经验的结构化容器；(2) CoT synthesis schema 可作为 step-level evidence extraction 格式；(3) MemGUI-Bench 可直接作为 A-1/A-2 的评测基准。相比之下，MRPO 本身更像工程能力建设，不是当前主线的核心方法组件。

- **Experimental design**:
  - **MemGUI-Bench** (Liu et al., 2026) evaluates recall of interaction history over long horizons and is a directly transferable benchmark for A-1/A-2 research.
  - **GUI-KnowledgeBench** covers GUI knowledge breadth (widget function, action parameter prediction, task planning) — useful for evaluating procedural knowledge retrieval.
  - The ablation design (Table 10: ±CoT synthesis; Table 11: ±virtual environments) provides a clean template for ablating memory module contributions.

### Connections to Other Papers in Knowledge Base
- 与 [GUI_Agent/00_survey-overview.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/00_survey-overview.md) 的关系是：它代表当前 native multi-platform 路线的能力上限。
- 与 [gap-tracker.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/gap-tracker.md) 的关系是：MemGUI-Bench 直接强化 A-1，context compression 的实现方式强化 A-2 的 negative evidence，而训练期 flywheel 则反证 A-4 仍未被解决。
- 与 Agent_Memory 的术语对齐时，Notetaker 和 hierarchical compression 更接近 working memory / in-task summary memory，而非真正的 episodic store。
- 与 Self_Evolve 的关系是：它展示了训练期经验闭环的强工程版本，但并未跨过部署后 memory evolution 这条线。

## Citation Tracking
- [ ] Liu et al. (2026), "MemGUI-Bench: Benchmarking memory of mobile GUI agents in dynamic environments" — arXiv:2602.06075: 直接评测GUI agent记忆能力，与A-1/A-2研究高度相关
- [ ] Ye et al. (2025), "Mobile-Agent-v3: Fundamental agents for GUI automation" — arXiv:2508.15144: GUI-Owl-1.5的前身，提供基线架构对比
- [ ] Xue et al. (2026), "EvoCUA: Evolving computer use agents via learning from scalable synthetic experience" — arXiv:2601.15876: 同期工作，关注经验进化，与A-4直接相关
- [ ] Shi et al. (2025), "GUIKnowledgeBench: Revealing the knowledge gap behind VLM failure in GUI tasks" — arXiv:2510.26098: 评测GUI知识（含程序性知识），A-1研究参考

## Key Passages

> "short-term and long-term memory, multi-agent adaptation, and human–agent interaction" (Section 1, p.2) — 明确将记忆作为通用GUI Agent的必备能力，但全文技术方案中仅实现了短期in-context记忆。

> "we design a unified chain-of-thought (CoT) synthesis pipeline that augments all trajectory data with step-wise observation, reflection, memory management, and tool invocation reasoning, enabling superior long-horizon planning and in-context information retention." (Abstract, p.1) — "in-context information retention"是关键限定词，说明记忆仍限于单次轨迹上下文内。

> "Among native agent models, GUI-Owl-1.5-32B achieves 27.1, substantially outperforming all prior baselines including Qwen3-VL-8B-Instruct (18.8) and UI-TARS-1.5-7B (8.3). Even our 8B variant (22.9) surpasses all existing native baselines, confirming that our training recipe effectively instills long-horizon memory capabilities without relying on external workflow orchestration." (Section 3.2.2, p.17) — 原生模型与workflow型agent（41.7）的14pp差距是研究机会。

> "Upon successful progress, the Notetaker extracts and stores salient transient information for future steps: N_{t+1} = u_C(N_t, S_{t+1}) if j_t = SUCCESS" (Section 2.3.3, p.9) — Notetaker是本文最接近"持久记忆"的机制，但仅限单session，无跨任务检索。

> "The CoT synthesis pipeline designed above enables the model to: (i) reflect on the execution outcome of the previous action and analyze the overall task progress accordingly, thereby achieving superior long-horizon decision-making capability; and (ii) simultaneously record key on-screen information (e.g., prices, weather conditions) that may be required in subsequent steps during the operational process, thereby achieving enhanced memory capability." (Section 2.3.2, p.8-9) — 两种能力（反思+记录）都局限于当前轨迹上下文。
