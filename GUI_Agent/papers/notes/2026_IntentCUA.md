# IntentCUA — Intent-level skill abstraction for long-horizon desktop automation

## Meta
- **Title**: IntentCUA: Learning Intent-level Representations for Skill Abstraction and Multi-Agent Planning in Computer-Use Agents
- **Authors**: Seoyoung Lee et al. | Sookmyung Women's University
- **Venue**: AAMAS 2026 | arXiv:2602.17049
- **Links**: [PDF](../source_todo/IntentCUA.pdf) | Code: not listed in PDF | Project: not listed in PDF
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-06
- **Priority**: P1 | **Reading progress**: Pass 1

## One-line Summary
IntentCUA 将 raw interaction traces 提炼成 multi-view intent representations、skill hints 与 shared plan memory，用多 agent 协同规划稳定长序列 desktop 任务，在 286 个任务上达到 74.8% success、0.91 SER，显著优于 UI-TARS-1.5 与 UFO2（Abstract / Table 2, p.1, p.8）。

## Problem Setting
- **Core problem**: long-horizon desktop automation suffers from "(i) plans spanning multiple substeps often drift from the original intent and redundantly re-solve already completed routines, (ii) local perception errors accumulate and lead to cascading retries" (Introduction, p.1)
- **Assumptions**: 可以获得用户 traces 做离线 intent labeling；计划可分解成 ENV / ACT / KEY / DES 等多视图；plan memory 只缓存 user-approved global plans；桌面任务通常跨窗口、跨应用、10-20 步以上（Section 1-3, p.1-5）。
- **Insufficiency of existing approaches**: "intent drift and redundant re-planning remain common in long-horizon workflows" (Section 2.1, p.3)

## Core Method
- **Method overview**: IntentCUA 的核心是把低层 GUI actions 上升到 intent level。作者先把 raw traces 转成多视图表示，再在共享嵌入空间里聚成 intent groups (IG) 和 subgroups (SG)。随后把 SG 对应的 action patterns 抽象成带参数槽位的 skill hints，连同用户批准过的 global plans 一起存进 plan memory。这样做的关键收益是: runtime planning 不再从零开始逐步搜索，而是先检索 intent prototype，再用 skill / cached plan 做 plan completion。

  在线阶段由 Planner、Plan-Optimizer、Critic 协同工作。Planner 先把自然语言任务分解成结构化 intent units，再基于 shared memory 复用已有 global plan 或补齐缺失动作；Plan-Optimizer 负责把 plan grounding 成具体 GUI 操作；Critic 则做后验校验与局部恢复。相比直接把整个长轨迹塞进 prompt，IntentCUA 让“什么要做”与“怎么点”两种表示分开管理，重点解决 long-horizon desktop agent 的 intent coherence。
- **Key Design Choices**:

| Design Decision | Author's Choice | Author's Rationale | Ablation Verified? |
|----------------|----------------|--------------------|--------------------|
| Representation level | Multi-view intent abstraction | 从原子 action 提升到可复用 skill / subgroup 层级 | Yes |
| Memory content | Shared plan memory + subgroup skill hints | 减少重复 re-planning，并支持 partial plan augmentation | Yes |
| Planning architecture | Planner / Plan-Optimizer / Critic multi-agent loop | 将全局规划、局部 grounding、校验恢复解耦 | Yes |
| Plan reuse rule | Cache-first reuse with template-based gap filling | 优先复用历史 plan，而非从头生成 | No |

- **Core difference from prior work**: UI-TARS 更偏 RL-based visual action policy，UFO2 更偏 trajectory-centric demonstration reuse；IntentCUA 则强调“intent abstraction + memory-grounded coordination”，把核心瓶颈从 perception 推向 plan coherence（Section 1-2, p.1-3）。

## Key Results

| Benchmark | This Method | Strongest Baseline | Δ | Notes |
|-----------|------------|-------------------|---|-------|
| Overall success (286 tasks) | 74.8% | UFO2 51.2% | +23.6 pts | Table 2, p.8 |
| Overall success (286 tasks) | 74.8% | UI-TARS-1.5 38.8% | +36.0 pts | Table 2, p.8 |
| WebVoyager subset | 71.6% | UFO2 69.0% | +2.6 pts | Table 2, p.8 |
| ScreenAgent subset | 77.1% | UI-TARS 42.9% | +34.2 pts | Table 2, p.8 |
| Step Efficiency Ratio | 0.91 | UI-TARS 0.85 / UFO2 0.82 | +0.06 / +0.09 | Section 6.1, p.8 |
| Avg. latency | 1.46 min | UFO2 6.63 / UI-TARS 9.82 | much lower | Section 6.1, p.8 |

- **Key ablation findings**: 摘要已明确指出，multi-view intent abstraction 与 shared plan memory 共同提升 execution stability，而 cooperative multi-agent loop 对 long-horizon tasks 的收益最大；这意味着增益不是来自单一检索，而是“表示 + memory + 协作规划”的组合（Abstract, p.1）。
- **Failure cases**: 作者给出一个明确 failure case：unexpected pop-up 遮挡关键元素时，script-based grounding 会失败并引发错误重试，说明该方法对 transient interface changes 仍脆弱（Section 6, p.8）。

## Limitations
- **Author-stated limitations**: "This highlights a limitation of script-based GUI grounding under transient interface changes." (Section 6, p.8)
- **My observed limitations**: 
> ⚠️ NEEDS YOUR INPUT: (1) IntentCUA 需要离线 traces 和人工批准的 global plans，前置成本不低。(2) plan memory 更像受控 plan cache，而不是开放式长期经验库；其 memory 仍偏 task-template reuse，不是面向持续自演化的开放记忆。(3) 当前评测主要是 desktop workflow，尚未展示在更强动态 web / mobile 环境中的适配性。
- **Experimental design gaps**: 论文没有把 memory 命中率、plan reuse 频率、cache miss 时的退化程度单独拆出来；也缺少对不同 trace quality 的敏感性分析。

## ⭐ Relation to My Research

### Position in Survey
- **Corresponding survey section/category**:
> ⚠️ NEEDS YOUR INPUT: 这篇适合放进 **Planning / Skill Abstraction / Memory** 交叉区域，尤其是“从 atomic GUI actions 向 reusable skill units 抽象”的代表工作。
- **Role**: Positive example

### Gap Signals (extracted from this paper)
- Gap signal 1: "plans ... drift from the original intent and redundantly re-solve already completed routines" (Introduction, p.1) → current desktop agents 的核心问题不是只会不会点，而是是否保持 intent-level coherence。
- Gap signal 2: memory 只存 user-approved global plans + subgroup skills（Figure 1 / Section 3, p.2-5）→ 长期经验仍然受限于预先整理过的结构，不支持真正开放世界持续积累。
- Gap signal 3: pop-up failure case (Section 6, p.8) → 高层 intent abstraction 并不能替代底层 grounding robustness。

> ⚠️ NEEDS YOUR INPUT: 这篇适合在你的知识库里被标成“skill abstraction 路线代表作”，但它还没有回答如何从失败轨迹中持续生成新 skill。

### Reusable Elements
- **Methodology**: multi-view intent embedding、intent group / subgroup clustering、parameterized skill hints、cache-first global planning 都很值得迁移。
> ⚠️ NEEDS YOUR INPUT: 如果你之后要做 GUI procedural memory，我建议优先借它的“sub-intent -> parameterized skill schema”这一步，而不是整个多 agent scaffold。
- **Experimental design**: success + SER + latency 三联指标对长 horizon task 很有效，比只看 SR 更有解释力。

### Connections to Other Papers in Knowledge Base
> ⚠️ NEEDS YOUR INPUT: 可与 [2026_ActionEngine](./2026_ActionEngine.md) 对比 symbolic structural memory；与 [2026_M2](./2026_M2.md) 对比 summary/retrieval memory；与 [2025_MobileAgentV3](../notes/2025_MobileAgentV3.md) 对比多 agent 分工但不同 memory 粒度。

## Citation Tracking
- [ ] UI-TARS-1.5: RL-based baseline
- [ ] UFO2: trajectory-centric baseline
- [ ] OS-ATLAS / process-mining lines: 作为 trace abstraction 前驱

## Key Passages
> "plans spanning multiple substeps often drift from the original intent and redundantly re-solve already completed routines" (Introduction, p.1)

> "IntentCUA achieves a 74.83% task success rate with a Step Efficiency Ratio (SER) of 0.91" (Abstract, p.1)

> "This highlights a limitation of script-based GUI grounding under transient interface changes." (Section 6, p.8)
