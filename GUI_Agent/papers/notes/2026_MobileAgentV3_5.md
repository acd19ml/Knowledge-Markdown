# Mobile-Agent-v3.5 / GUI-Owl-1.5 — Multi-platform native GUI agent with hybrid data flywheel and multi-platform RL

## Meta
- **Title**: Mobile-Agent-v3.5: Multi-platform Fundamental GUI Agents
- **Authors**: Haiyang Xu et al. | Tongyi Lab, Alibaba Group
- **Venue**: Preprint, February 2026 | arXiv:2602.16851
- **Links**: [PDF](./Mobile-Agent-v3.5.pdf) | [Code](https://github.com/X-PLUG/MobileAgent)
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-05
- **Priority**: P0 | **Reading progress**: Pass 2

## One-line Summary
Xu et al. (Alibaba Tongyi) train GUI-Owl-1.5 (2B–235B) on a hybrid data flywheel + MRPO reinforcement learning, achieving SOTA open-source results on OSWorld (56.5%), AndroidWorld (71.6%), WebArena (48.4%), and ScreenSpotPro (80.3%) across desktop/mobile/browser platforms.

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
> ⚠️ NEEDS YOUR INPUT:
> 1. **记忆机制的天花板**：MemGUI-Bench上原生模型（27.1）与Workflow型智能体（41.7）之间仍存在14pp差距，说明通过CoT合成注入的"记忆管理"能力尚未真正实现持久化、跨任务的程序性记忆（A-1类空白）。
> 2. **被动记忆 vs 主动检索**：本文的记忆机制是sliding window + 行动结论拼接，属于上下文压缩式短期记忆，不涉及外部记忆库检索或跨session的episode回放（A-2类空白未覆盖）。
> 3. **离线经验进化缺失**：数据飞轮是生成时的离线pipeline，但模型部署后并不支持从实际运行轨迹中自动学习更新（A-4类空白）。
> 4. **RL依赖环境沙箱**：MRPO需要真实或虚拟环境rollout，对没有沙箱环境的新平台适配成本高。
- **Experimental design gaps**: MemGUI-Bench evaluation is limited to "Easy" tasks only, leaving medium/hard task performance unreported. GUI-Owl-1.5-32B-Thinking is not benchmarked on WebArena/VisualWebArena (Table 2 shows "—" entries). The 235B variant lacks comprehensive end-to-end evaluation.

## ⭐ Relation to My Research

### Position in Survey
- **Corresponding survey section/category**:
> ⚠️ NEEDS YOUR INPUT:
> 对应GUI Agent综述中的以下位置：
> - **Section: Native Agent Models（原生智能体模型）**：GUI-Owl-1.5是端到端训练的原生模型，区别于基于通用VLM的框架型agent。
> - **Section: Multi-platform Generalization（多平台泛化）**：MRPO是目前少数同时处理mobile/desktop/web训练冲突的RL方案。
> - **Section: Memory and Knowledge（记忆与知识）**：通过CoT合成注入记忆管理能力，并在GUI-KnowledgeBench和MemGUI-Bench上设有专项评测。
> - **在Cross_Topic/gap-tracker.md中**：本文可作为A-1（程序性记忆）和A-4（离线经验进化）空白的"不充分正例"——有尝试但未真正解决。
- **Role**: Positive example (state-of-the-art baseline for GUI automation); also serves as a Contrastive baseline for memory and experience evolution gaps (A-1, A-4).

### Gap Signals (extracted from this paper)

- Gap signal 1: "short-term and long-term memory" listed as a key capability requirement but implemented only via sliding-window context compression + CoT annotation — no persistent cross-session or cross-app memory store. (Section 1, p.2; Section 2.1, p.3-4) → **A-2 gap**: multimodal episodic memory (screenshot-based memory stream retrieval) is entirely absent.

- Gap signal 2: "Among native agent models, GUI-Owl-1.5-32B achieves 27.1, substantially outperforming all prior baselines ... Even our 8B variant (22.9) surpasses all existing native baselines, confirming that our training recipe effectively instills long-horizon memory capabilities without relying on external workflow orchestration." (Section 3.2.2, p.17) — yet workflow agents hit 41.7, a 14pp gap. → **A-1 gap**: no procedural skill/knowledge base that accumulates reusable task templates across sessions and apps.

- Gap signal 3: The Hybrid Data Flywheel is defined through pre-deployment DAG synthesis, checkpoint verification, truncation-repair, and curated trajectory production (Sections 2.2-2.3, p.4-9) → 论文没有描述部署后从真实用户轨迹持续写回模型/记忆库的机制，因此 post-deployment experience evolution 仍是空白。

- Gap signal 4: "we design a unified chain-of-thought (CoT) synthesis pipeline that augments all trajectory data with step-wise observation, reflection, memory management, and tool invocation reasoning" (Section 1 / Abstract, p.1) — memory management here means extracting key info within a single trajectory, not retrieving from a historical episodic store. → Reinforces A-2: the distinction between in-context memory and external episodic memory is architecturally unaddressed.

> ⚠️ NEEDS YOUR INPUT:
> **空白价值评估**：
> - **A-1（程序性记忆）**：本文GUI-KnowledgeBench（75.5）表明GUI知识QA已可处理，但跨任务的可重用技能库（如"如何打开Outlook附件"这类操作记忆）仍未被建模。若能在GUI-Owl-1.5级别的原生模型上增加procedural memory模块，MemGUI-Bench的差距（14pp）有可能大幅缩小。研究价值：高。
> - **A-2（多模态情节记忆）**：截图流式记忆检索在本文中完全缺失，但MemGUI-Bench存在恰好是此类任务（recall interaction history over long horizons）。可将其作为评测目标。
> - **A-4（离线经验进化）**：数据飞轮的思路（DAG + checkpoint验证 + repair）提供了经验进化pipeline的良好工程参考，但需要扩展到部署后的持续学习阶段。

### Reusable Elements
- **Methodology**:
  - The **DAG-based trajectory synthesis** (directed acyclic graph over atomic subtasks with checkpoint predicates) is directly reusable as a structured memory encoding format: each DAG path can be stored as a procedural memory episode with verified subtask completion states.
  - The **CoT synthesis pipeline** (observation → memory extraction → reflection → progress update) defines a step-level memory annotation schema that could be adapted to build an episodic memory stream (A-2).
  - The **Notetaker role** in the multi-agent framework (`N_{t+1} = u_C(N_t, S_{t+1})` if success) is a lightweight persistent note mechanism that could be extended into a retrieval-augmented procedural memory bank.

> ⚠️ NEEDS YOUR INPUT:
> **如何复用到你的研究中**：
> 1. **DAG结构作为程序性记忆骨架**：将GUI-Owl-1.5中的DAG任务图扩展为跨应用的"skill graph"，其中每个节点是可重用的操作单元，边代表前置条件，即可构建A-1所需的程序性记忆库。
> 2. **CoT合成schema作为情节记忆的标注格式**：将step-level的observation+memory字段直接映射到multi-modal episodic memory的存储格式，支持基于截图向量的语义检索（A-2）。
> 3. **Notetaker持久化机制**：Notetaker对成功步骤的选择性更新逻辑（只在SUCCESS时更新）是一个简洁的episodic consolidation机制，可作为A-4离线经验筛选策略的参考。
> 4. **MemGUI-Bench**：本文将其作为memory能力评测，是A-1/A-2研究的理想评测基准。

- **Experimental design**:
  - **MemGUI-Bench** (Liu et al., 2026) evaluates recall of interaction history over long horizons and is a directly transferable benchmark for A-1/A-2 research.
  - **GUI-KnowledgeBench** covers GUI knowledge breadth (widget function, action parameter prediction, task planning) — useful for evaluating procedural knowledge retrieval.
  - The ablation design (Table 10: ±CoT synthesis; Table 11: ±virtual environments) provides a clean template for ablating memory module contributions.

### Connections to Other Papers in Knowledge Base

> ⚠️ NEEDS YOUR INPUT:
> **与知识库其他文献的联系**：
> 1. **GUI_Agent/00_survey-overview.md**：本文是综述中native agent models类别的最新代表，可作为多平台能力建设的基准参照。
> 2. **Cross_Topic/gap-tracker.md（A-1/A-2 空白）**：本文的 MemGUI-Bench 结果（native model 27.1 vs workflow 41.7）直接佐证了 A-1“缺乏可重用程序性记忆”的空白；CoT 记忆提取方案也印证了 A-2（仅 in-context，无 episodic 检索）的不足。
> 3. **Cross_Topic/gap-tracker.md（A-4 空白）**：Hybrid Data Flywheel 的 checkpoint-repair 机制与 Self_Evolve 综述中“经验过滤与整理”主题高度重叠，但仅限预部署阶段，没有部署后在线进化，印证 A-4 空白的真实性。
> 4. **Agent_Memory/**：本文的Notetaker角色和hierarchical context compression对应Agent Memory综述中的"Working Memory"和"Episodic Memory"分类，但未引用该体系，说明GUI Agent研究与Agent Memory研究存在领域隔离，这本身是值得探索的融合机会。
> 5. **Self_Evolve/**：MRPO的unstable-task-focused训练策略与Self-Evolving agents中"从失败经验学习"的主题有共鸣，但MRPO限于训练期，不是部署后进化。

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
