# AmbiBench — Benchmarking mobile GUI agents under ambiguous instructions

## Meta
- **Title**: AmbiBench: Benchmarking Mobile GUI Agents Beyond One-Shot Instructions in the Wild
- **Authors**: Jiazheng Sun et al. | Fudan University + Jilin University
- **Venue**: Preprint, 2026 | arXiv:2602.11750
- **Links**: [PDF](../source/AmbiBench.pdf) | Code: anonymous repository mentioned in PDF | Project: not listed in PDF
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-06
- **Priority**: P1 | **Reading progress**: Pass 2

## One-line Summary
AmbiBench 把 mobile GUI agent 评测从 one-shot instruction following 改成多轮 intent alignment，提出四级 instruction clarity taxonomy 与 MUSE 自动审计框架，并显示非交互式 agent 在 Ambiguous 任务上会系统性崩溃，而支持交互的 agent 能显著受益（Abstract, Section 5.2, p.1, p.16-17）。

## Problem Setting
- **Core problem**: "existing research and benchmarks predominantly operate under the idealized assumption that user-issued instructions are complete and unequivocal - a premise we term Instruction equals Intent." (Section 1, p.1)
- **Assumptions**: 用户真实意图常常不会在第一句里完整给出；评测需要允许 agent 通过交互补足缺失信息；移动端在线环境可通过 proxy sandbox、user simulator 与 judge agents 做统一审计（Section 1, Section 4, p.1, p.12-14）。
- **Insufficiency of existing approaches**: "This One-Shot Instruction model overlooks the phenomenon of cognitive misalignment prevalent in real-world human-computer interaction." (Section 1, p.1)

## Core Method
- **Method overview**: AmbiBench 的核心不是再造一个 agent，而是重写 benchmark 目标。作者把任务按 Cognitive Gap 理论拆成四个 clarity levels: Detailed、Standard、Incomplete、Ambiguous，并要求 agent 在执行过程中通过主动询问来收敛真实 intent。任务覆盖 25 个 app、240 个生态有效任务，强调 in-the-wild、跨应用、多轮交互，而不是 sandbox 中一次性给全指令。

  与此配套，作者提出 MUSE 作为自动化评测器。MUSE 不是只看最终成败，而是同时评 outcome、execution process、interaction quality 三个维度。它通过标准化 interaction interface 接入不同 agent，用 proxy sandbox 记录交互，再把 trajectory 序列化后交给多 agent 审计器计算 RCR、TSR、SHR、ARR、ETR、DCR、IGR 等指标。这使 AmbiBench 能回答的不再只是“做成了没”，而是“是否真的理解了用户 intent、是否靠 trial-and-error、是否有效提问”。
- **Key Design Choices**:

| Design Decision | Author's Choice | Author's Rationale | Ablation Verified? |
|----------------|----------------|--------------------|--------------------|
| Task taxonomy | 4 clarity levels from Detailed to Ambiguous | 显式建模 instruction 与 intent 的信息差 | Yes（RQ1） |
| Evaluation axes | Outcome + Execution + Interaction 三维联合评测 | 避免只用 success rate 误判 agent 能力 | Yes（RQ2/RQ3） |
| Judge framework | MUSE multi-agent auditing | 在动态线上环境中尽量自动化且细粒度评估 | Yes（5.5 Reliability） |
| Integration layer | Standardized interaction interface + proxy sandbox | 让不同 agent/framework 可被统一接入与分析 | No |

- **Core difference from prior work**: 以前的 mobile benchmarks 多把 instruction 视为完整 specification；AmbiBench 则把“澄清缺口并收敛 intent”提升为 benchmark 主任务，因此它评的是 alignment capability，而不只是 execution capability（Section 2-4, p.3-14）。

## Key Results

| Benchmark | This Method | Strongest Baseline | Δ | Notes |
|-----------|------------|-------------------|---|-------|
| Benchmark scale | 240 tasks / 25 apps | Existing mobile benchmarks mostly single-level | N/A | AmbiBench adds multi-level ambiguity (Abstract, p.1) |
| Average TSR under AmbiBench | Fairy (#6): 40.4 | AutoGLM-9B: 35.4 | +5.0 pts | Table 2 average, p.15 |
| Ambiguous / incomplete setting | Fairy can reach 26.2 in Incomplete | Non-interactive agents collapse on Ambiguous | Qualitative reversal | Interaction changes ranking (p.16-17) |
| Reliability of evaluator | Jaccard 0.92 (`V_out`), 0.84 (`V_step`), 96% valid parameter fills | Human annotation | Strong alignment | Section 5.5, p.18 |
| Human annotation reliability | Fleiss' κ = 0.91 | N/A | N/A | Ground-truth itself is stable (Section 5.5, p.18) |

- **Key ablation findings**: 论文主打 benchmark diagnosis，而非模块消融。最关键的诊断结论是：当 clarity 从 Detailed 降到 Incomplete / Ambiguous，非交互式 agent 的 TSR 会断崖式下跌；同时 process metrics 揭示 AutoGLM 这类方法的高成功率部分来自 trial-and-error，而不是稳健规划（Section 5.2-5.3, p.16-17）。
- **Failure cases**: 非交互式 agent 在信息不足时要么硬猜、要么强行执行，导致 TSR 在 Ambiguous 场景跌到 0；部分交互式 agent 虽会提问，但 user simulator 和动态环境噪声仍可能带来不稳定评估（Section 5.2, 5.6, p.16, p.18）。

## Limitations
- **Author-stated limitations**: 作者在 Threats to Validity 中明确指出：任务规模相对长尾 app 生态仍有限；设备异构性可能影响泛化；在线环境存在 non-determinism；MUSE 可能忽略细粒度视觉与情感体验；clarity taxonomy 边界有主观性（Section 5.6, p.18）。
- **My observed limitations**: 
  AmbiBench 把“是否会澄清”从附加能力提升成了主评测维度，但它仍是 benchmark paper，而不是 memory / method paper。user simulator 只是近似真实用户，因此更准确地说，它测的是 clarification protocol competence，而不是长期 user modeling 或 cross-session memory。
- **Experimental design gaps**: 当前 strongest result 还是 benchmark-level diagnosis，不是统一 scaffold 下的 apples-to-apples interactive agent contest；另外，缺少更长 horizon、多 session、带 persistent user profile 的 mobile personalization 设置。

## ⭐ Relation to My Research

### Position in Survey
- **Corresponding survey section/category**:
  这篇应放进 GUI Agent survey 的 **Evaluation** 章节，尤其是从 single-turn execution 扩展到 interactive intent alignment evaluation 的小节。按当前主线，它主要服务于评测问题，而不是方法核心。
- **Role**: Background reference / Positive example

### Gap Signals (extracted from this paper)
- Gap signal 1: "Instruction equals Intent" (Section 1, p.1) → 现有 benchmark 默认 instruction 完整，这本身就是评测缺口。
- Gap signal 2: "Our stratified evaluation exposes a systemic failure of the non-interactive paradigm" (Section 5.2, p.16) → 说明 agent 是否支持 clarification，不应再被视为附加能力，而应是主评测维度。
- Gap signal 3: "Future work will prioritize the construction of high-fidelity local dynamic Apps" (Section 6, p.18) → 当前线上动态 app 虽有生态真实性，但 non-determinism 仍然是 benchmark 噪声源。

  对当前知识库来说，AmbiBench 的价值在于给 A-3 和 user-interaction 相关讨论提供 benchmark 入口，但它并不改变 A-1 / A-4 的主线判断，因为这里还没有长期个性化或跨会话经验累积机制。

### Reusable Elements
- **Methodology**: 四级 clarity taxonomy、Outcome/Execution/Interaction 三维指标、MUSE 标准化接入层都很可复用。
  最值得复用的是过程指标，而不是具体 task。ARR、DCR、IGR 能把 outcome、执行质量和交互合理性拆开，这对后续评测 memory 是否真的改善了 intent handling 很有用。
- **Experimental design**: 对同一 agent 同时报 outcome 和 process quality，是你的知识库里很值得保留的 benchmark 设计模板。

### Connections to Other Papers in Knowledge Base
  它可以与 [2023_AppAgent.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2023_AppAgent.md)、[2024_MobileAgentV2.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2024_MobileAgentV2.md) 和 [2025_MobileAgentV3.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2025_MobileAgentV3.md) 串联起来，作为这些执行型 agent 在 ambiguity / clarification 维度上的外部评测坐标。

## Citation Tracking
- [ ] Fairy: 代表性交互式 mobile agent，需要单读其 clarification 机制
- [ ] UI-TARS / AutoGLM: 作为 Agent-as-a-Model 参照
- [ ] AndroidWorld / MobileAgentBench: 用于 benchmark lineage 对照

## Key Passages
> "user-issued instructions are complete and unequivocal - a premise we term Instruction equals Intent." (Section 1, p.1)

> "Our stratified evaluation exposes a systemic failure of the non-interactive paradigm when confronting real-world ambiguity." (Section 5.2, p.16)

> "Future work will prioritize the construction of high-fidelity local dynamic Apps" (Section 6, p.18)
