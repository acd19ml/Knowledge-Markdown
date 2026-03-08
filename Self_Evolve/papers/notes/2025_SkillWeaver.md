# SkillWeaver — Autonomous website exploration to synthesize reusable API skills

## Meta
- **Title**: SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills
- **Authors**: Boyuan Zheng et al. | The Ohio State University, Carnegie Mellon University, University of Virginia, Purdue University, Cisco Research
- **Venue**: arXiv preprint, April 2025 | arXiv:2504.07097v1
- **Links**: [PDF](../source/SkillWeaver.pdf) | [Code](https://github.com/OSU-NLP-Group/SkillWeaver)
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-05
- **Priority**: P1 | **Reading progress**: Pass 2

## One-line Summary

SkillWeaver 通过“三阶段自探索（skill proposal → synthesis → honing）”把网页交互经验蒸馏为可复用 Playwright API，在 WebArena 与真实网站上分别带来 31.8% 和 39.8% 的相对成功率提升，并可把强模型探索到的技能迁移给弱模型（WebArena 上最高 54.3% 相对提升）。

## Problem Setting

- **Core problem**: "autonomous web agents still lack crucial self-improvement capabilities, struggling with procedural knowledge abstraction, skill refinement, and skill composition." (Abstract, p.1)
- **Assumptions**:
  - 智能体可执行网页原子动作并可调用 Python/Playwright API（Section 3.3, p.6）。
  - 可用 LLM reward model 判断任务是否完成（Section 2.2, p.4）。
  - 通过网站级预探索（每站点 160 iterations）可持续扩展 API 库（Section 3.4, p.6）。
- **Insufficiency of existing approaches**: "trajectory-based approaches ... struggle to explicitly abstract reusable procedural knowledge" 且 NL workflow "pose challenges for formal verification and precise composition into new workflows." (Section 1, p.2)

## Core Method

- **Method overview**:

SkillWeaver 的核心思想是把“探索轨迹”转成“可调用技能接口”。论文把技能统一表示成 Python function（Playwright automation API），并通过三阶段循环持续积累技能库（Section 2, p.3）：  
1) **Stage I: Skill Proposal**：基于截图、URL、a11y tree 和当前 skill library，提出新技能任务；任务类型覆盖 procedural / navigational / information-seeking，并显式追求“novel + reusable + short-horizon”（Section 2.1, p.3-4）。  
2) **Stage II: Skill Synthesis**：先 practice 生成轨迹，再用 reward model 判定成功，最后把成功轨迹合成为 API（带函数签名、docstring、usage log、前置状态说明）；并做静态分析修复常见代码错误（Section 2.2, p.4）。  
3) **Stage III: Skill Honing**：对合成 API 做单测；对有参数 API 让 LLM 生成测试参数，并结合执行反馈继续调试，提升鲁棒性（Section 2.3, p.5）。

推理时，agent 的动作空间从原子浏览动作扩展到“原子动作 + API 调用”。为控制大量 API 带来的噪声，作者加入 API selection 模块筛选相关且满足前置条件的 API（Section 3.3, p.6）。该机制使技能可作为可插拔外部记忆跨网站、跨 agent 复用（Section 4.2, p.7-8）。

- **Key Design Choices**:

| Design Decision | Author's Choice | Author's Rationale | Ablation Verified? |
|----------------|----------------|--------------------|--------------------|
| Skill representation | 用 Playwright Python API（函数）而非纯 NL workflow | 便于 formal verification、参数化调用与组合复用（Section 1, p.2; Section 2, p.3） | No |
| Exploration objective | 明确追求 short-horizon、reusable、novel skills | 提高后续 practice/synthesis 成功率，逐步形成可组合 skill 库（Section 2.1, p.3） | No |
| Three-stage loop | Proposal → Synthesis → Honing | 把发现、构建、验证解耦，降低单阶段错误传播（Section 2-2.3, p.3-5） | No |
| Reward-based synthesis | 仅把成功轨迹蒸馏为 API，并加静态代码检查 | 降低失败轨迹噪声，提高代码可执行性（Section 2.2, p.4） | No |
| Inference API selection | 从库中筛选相关 API，并过滤不满足 pre-condition 的 API | 避免 API 库增大后推理混乱，支持 compositional 调用（Section 3.3, p.6） | No |

- **Core difference from prior work**: 相比“存轨迹用于 ICL/微调”或“NL workflow 记忆”，SkillWeaver 直接产出可执行 API 作为非参数化技能记忆，并通过自主探索持续扩容，不依赖人工标注 demonstrations（Section 1, p.2; Section 5, p.9）。

## Key Results

| Benchmark | This Method | Strongest Baseline | Δ | Notes |
|-----------|------------|-------------------|---|-------|
| WebArena AVG (GPT-4o agent) | 29.8 (+Skills) | 22.6 (same agent w/o skills) | +31.8% rel. (paper claim) | Table 1 shows large gains across all 5 domains (Section 4.1, p.6-7) |
| WebArena AVG (GPT-4o-mini agent) | 14.1 (+Skills) | 9.2 (same weak agent w/o skills) | up to +54.3% rel. (paper claim) | Domain gains range 40%-133% (Section 4.1/4.2, p.6-8) |
| Real-world websites AVG (Online-Mind2Web subset) | 56.2 (+Skills) | 40.2 (Baseline) | +39.8% rel. | 4 sites, 57 tasks, manual success check (Table 2, Section 3.2/4.1, p.5/7) |
| vs AutoEval (WebArena AVG) | SkillWeaver+Skills 29.8 | AutoEval 26.9 | +2.9 abs | 但 Shopping 域不占优（Section 4.1, p.6-7） |
| vs SteP (WebArena domain-wise) | SkillWeaver 在 CMS/Map 更好 | SteP 在 AVG 更高（33.0） | mixed | 体现自动合成 API 与人工 workflow 各有优势（Section 4.1, p.6-7） |

- **Key ablation findings**:
  - 论文没有给出严格的模块级消融（如去掉 Stage III、去掉 API selection、去掉 reward model）。
  - 现有证据主要是端到端对比 + 案例分析：出现 compositional API（Section 4.3, p.8; Appendix D.3），且跨 agent 迁移有效（Section 4.2, p.7-8）。
  - 人工 API 对比显示：低/中 API-support 网站（如 Reddit/Shopping）可接近或超过人工 API；高 API-support 网站（如 GitLab/Map）仍有差距（Section 4.2, p.8; Figure 3, p.8）。
- **Failure cases**:
  - **Fail to call API**：已生成 API 但执行期未调用（Appendix D.2.4, p.37-38）。
  - **Wrong parameter**：API 选对但参数错误导致失败（Appendix D.2.5, p.38-39）。
  - **Verification loophole**：仅以“不抛异常”判定 verified，可能误把坏 API 视为成功（Appendix D.2.1, p.34-35）。
  - **Lack realistic test data**：部分任务无法构造有效测试输入（Appendix D.2.2, p.36）。

## Limitations
- **Author-stated limitations**:
  - "LLMs like GPT-4o are still not robust enough at API calling" (Section 4.3, p.8)
  - "malfunctioning APIs could be marked as verified simply because they silenced all exceptions" (Appendix D.2.1, p.34)
  - 真实测试数据缺失会导致功能无法被正确验证（Appendix D.2.2, p.36）。
- **My observed limitations**:
  SkillWeaver 的价值在于把经验落成可执行 API 技能，但它也非常清楚地暴露了一个主线问题：有技能库，不等于会用技能库。当前收益更多来自“生成了工具”，而不是“建立了稳定的 skill selection / failure rewrite 机制”，因此它是 A-1 的正面部分解，而不是 A-4 的解。
- **Experimental design gaps**:
  - 未报告探索成本与收益曲线（如 iteration 数、token 成本、成功率增益之间关系）。
  - 无长期稳定性测试（网站 UI 变更后，旧 API 的失效率如何演化）。
  - 无跨 benchmark 泛化（例如未在更广泛 GUI/OS 任务上验证）。

## ⭐ Relation to My Research

### Position in Survey
- **Corresponding survey section/category**:
  这篇应归入 `Self_Evolve` 主线中的 **Non-parametric Skill Self-Improvement**。如果单列 “procedural memory as executable tools”，它应是代表文献之一，但要明确它解决的是 skill construction，而不是 complete skill governance。
- **Role**: Positive example（可执行技能库）+ Contrastive baseline（显示“会生成技能”与“会用技能”之间仍有鸿沟）

### Gap Signals (extracted from this paper)
<!-- Only record gaps with textual evidence from the paper -->
- Gap signal 1: "LLMs like GPT-4o are still not robust enough at API calling" (Section 4.3, p.8) → implies 技能执行策略仍是瓶颈，需更强 tool-selection / parameter-planning。
- Gap signal 2: "malfunctioning APIs could be marked as verified simply because they silenced all exceptions" (Appendix D.2.1, p.34) → implies 当前验证信号可被“静默失败”欺骗，鲁棒评估机制不足。
- Gap signal 3: "the agent does not call available APIs even when they are generated during exploration" (Appendix D.2.4, p.37) → implies 探索期与执行期存在策略断层（exploration-to-execution gap）。
- Gap signal 4: real-world 表中 Car 站点最终提升为 0%（11.1 → 11.1），且作者说明到达最终状态后仍在最后步骤失败（Section 4.1, p.7）→ implies 复杂长链任务仍受限于终局推理与视觉理解能力。

  对当前主线，最关键的 gap 不是 API 会不会生成，而是 skill 会不会被正确调用、验证、淘汰和重写。因此 exploration-to-execution gap 与 verifier 质量问题最值得保留，它们分别对应 A-1 的调用层和 A-4 的写回层。

### Reusable Elements
- **Methodology**: 三阶段闭环（proposal/synthesis/honing）+ 可执行 API 表示 + pre-condition 过滤式 skill selection。
  真正可迁移的是 skill CI 思路，而不是某个具体 API 生成器。Stage III 的单测与调试可以扩展成版本化、回归测试和退化检测一体化的 skill governance 层。
- **Experimental design**: “同一 agent 架构，仅替换是否接入技能库”的对照方式，以及“强模型探索 -> 弱模型复用”的迁移评估框架值得复用。

### Connections to Other Papers in Knowledge Base
  它与 [2026_SkillRL.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2026_SkillRL.md) 形成 non-parametric API memory vs RL skill co-evolution 的对照；与 [2024_AWM.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2024_AWM.md) 则是 NL workflow vs executable API 的对照。再与 [2026_EvoCUA.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2026_EvoCUA.md) 并置，就能形成参数化与非参数化自演化的清晰分野。

## Citation Tracking
- [ ] SkillWeaver (Zheng et al., 2025): non-parametric API skill self-improvement 主参考
- [ ] Agent Workflow Memory (Wang et al., 2024): workflow memory 对照基线
- [ ] ICAL (Sarch et al., 2024): abstract routine 相关工作
- [ ] AutoEval (Pan et al., 2024): LLM reward guided inference baseline
- [ ] SteP (Sodhi et al., 2024): human-crafted workflow baseline
- [ ] Online-Mind2Web (Xue et al., 2025): 真实网站评测基准来源

## Key Passages
> "autonomous web agents still lack crucial self-improvement capabilities, struggling with procedural knowledge abstraction, skill refinement, and skill composition." (Abstract, p.1)

> "trajectory-based approaches ... struggle to explicitly abstract reusable procedural knowledge" and NL routines "pose challenges for formal verification and precise composition into new workflows." (Section 1, p.2)

> "LLMs like GPT-4o are still not robust enough at API calling ... We identify two primary categories of failures: (1) failure to identify the appropriate API and (2) generating wrong parameters." (Section 4.3, p.8)
