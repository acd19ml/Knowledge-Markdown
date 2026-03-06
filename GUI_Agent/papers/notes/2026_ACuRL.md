# ACuRL — Autonomous continual learning for environment adaptation

## Meta
- **Title**: Autonomous Continual Learning of Computer-Use Agents for Environment Adaptation
- **Authors**: Tianci Xue et al. | The Ohio State University + UC Berkeley
- **Venue**: Preprint, 2026 | arXiv:2602.10356
- **Links**: [PDF](../source_todo/Autonomous-Continual-Learning.pdf) | Code: github.com/OSU-NLP-Group/ACuRL | Project: not listed in PDF
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-06
- **Priority**: P1 | **Reading progress**: Pass 2

## One-line Summary
ACuRL 让 computer-use agent 在零人工数据条件下，通过 autonomous exploration + curriculum RL + CUAJudge 自动评估，在 6 个 GUI 环境中实现 4-22% 的持续学习收益，并保持无灾难性遗忘（Abstract, p.1）。

## Problem Setting
- **Core problem**: "real-world digital environments are diverse with millions of desktop and web applications" and "real-world digital environments are not static" (Abstract / Introduction, p.1)
- **Assumptions**: 目标环境本身可交互；可以从 web-crawled contexts 生成任务；自动 evaluator 能给出足够可靠的 reward；适配发生在特定 target environments 上而非完全开放世界（Section 1-3, p.1-5）。
- **Insufficiency of existing approaches**: "These challenges highlight continual learning in specific target environments as a central requirement for real-world applicability, which remains unexplored." (Introduction, p.1)

## Core Method
- **Method overview**: ACuRL 的思路是把环境适应看成持续 curriculum RL，而不是一次性 offline finetuning。系统先在目标环境中自主探索，收集 environment-grounded experiences；随后在每一轮训练后，让 curriculum generator 根据已有经验和上一轮反馈重新合成更贴合当前能力边界的新任务。这样训练数据不再来自人类示范，而来自 agent 与环境的闭环交互。

  为了让这个闭环可靠，作者引入 CUAJudge。它不是单一终局判分器，而是结合 state-difference analysis 与 evidence-grounded keypoint verification，对 computer-use trajectory 做更稳的 outcome judgement。作者还专门做了大规模环境编排优化，把 environment preloading、asynchronous evaluation 等工程机制加入 pipeline，让 RL 在真实 GUI 环境上仍能跑得动。
- **Key Design Choices**:

| Design Decision | Author's Choice | Author's Rationale | Ablation Verified? |
|----------------|----------------|--------------------|--------------------|
| Data source | Zero-human-data autonomous exploration | 避免昂贵人工标注，直接面向目标环境适应 | Yes |
| Task progression | Curriculum task generation from prior feedback | 让任务难度随 agent 能力动态上升 | Yes（Table 3, p.7） |
| Reward/evaluation | CUAJudge with state-difference + keypoint verification | GUI 任务需要比普通 Web judge 更环境落地的判定 | Yes（Table 4/5, p.8） |
| Infrastructure | Async environment preloading and evaluation | 解决真实 GUI RL 的吞吐瓶颈 | No |

- **Core difference from prior work**: 与只在静态 benchmark 上比较单次能力的 CUA 工作不同，ACuRL 直接研究“模型上线后如何针对具体环境继续学”，并把 continual learning 从语言模型内部问题，转成了 environment-grounded agent adaptation 问题（Section 1, p.1-2）。

## Key Results

| Benchmark | This Method | Strongest Baseline | Δ | Notes |
|-----------|------------|-------------------|---|-------|
| Intra-environment overall | 24.5 (Impress Iter2) | Base 18.7 | +5.8 pts | Best single-env continual learning overall (Table 1, p.6) |
| Impress target env | 40.7 | Base 31.1 | +9.6 pts | Iter3 in Impress environment (Table 1, p.6) |
| Thunderbird target env | 57.8 | Base 35.5 | +22.3 pts | Strongest per-env gain (Table 1, p.6) |
| Cross-environment overall | 24.7 | Base 18.7 | +6.0 pts | Impress→KAlgebra→Calc sequence (Table 2, p.7) |
| Automatic evaluation reliability | 93.7% agreement | Human judgment | N/A | CUAJudge overall agreement (Table 5, p.8) |

- **Key ablation findings**: 去掉 iterative training 后，Impress 环境在 Iter3 从 40.7 掉到 32.6；去掉 curriculum learning 后，Iter3 只有 36.4，说明“持续训练 + 难度自适应任务生成”两者缺一不可（Table 3, p.7）。
- **Failure cases**: 作者没有给出单独 failure gallery，但从 ablation 可见，固定任务池会导致 overfitting，随机任务生成则削弱学习效率；这意味着 continual learning 的关键失败模式不是“学不会”，而是“任务供给机制失配”（Section 4.5, p.7）。

## Limitations
- **Author-stated limitations**: 论文没有独立 limitations 章节，但结论与实验设置已暗示边界: 目前仅在 6 个代表性环境中验证，并且适配依赖目标环境可被反复访问和训练（Section 4-6, p.6-10）。
- **My observed limitations**: 
> ⚠️ NEEDS YOUR INPUT: (1) ACuRL 虽然实现了 continual learning，但仍是一个显式训练阶段过程，不是部署期即插即用的 runtime memory adaptation。(2) 任务生成与自动评估都强依赖外部高能力模型（如 GPT-5 / GPT-5-mini），真实部署成本和可迁移性还要单独评估。(3) 环境覆盖仍偏 office / productivity，尚未证明在更开放的真实 consumer web / desktop software 上同样成立。
- **Experimental design gaps**: 未直接与 inference-time memory / retrieval methods 做比较；也没有分析若目标环境本身变化非常剧烈，过去经验是否会误导 curriculum。

## ⭐ Relation to My Research

### Position in Survey
- **Corresponding survey section/category**:
> ⚠️ NEEDS YOUR INPUT: 这篇最适合放在 GUI Agent survey 的 **Training / Adaptation / Self-Evolution** 小节，也可以作为“online continual adaptation”与“inference-time memory reuse”之间的重要分界线。
- **Role**: Positive example / Background reference

### Gap Signals (extracted from this paper)
- Gap signal 1: "continual learning in specific target environments ... remains unexplored" (Introduction, p.1) → 说明环境适应本身在 GUI agent 里仍是空白地带。
- Gap signal 2: ACuRL 的适应闭环由 autonomous exploration、curriculum generation、RL 更新和 CUAJudge 组成（Sections 3-4, p.3-8）→ 这是训练期 continual learning 方案，而不是 deployment-time retrieval / memory reuse；两类持续改进机制仍应区分。
- Gap signal 3: sparse updates around only 20% parameters and about 80% unchanged (Abstract / Figure 2 discussion, p.1, p.8) → 暗示也许存在更轻量的 parameter-efficient or memory-based adaptation 路径。

> ⚠️ NEEDS YOUR INPUT: 如果你的 RQ 聚焦“agent 如何持续吸收经验”，ACuRL 可以作为训练期自演化的强基线，而你的工作可进一步问: 能不能把这套能力搬到 inference-time、无显式 RL 的设置里。

### Reusable Elements
- **Methodology**: CUAJudge 非常值得复用，尤其是 state-difference + evidence-grounded verification 的组合；curriculum generator 也适合作为 self-evolving pipeline 的 task source。
> ⚠️ NEEDS YOUR INPUT: 我会优先复用 CUAJudge，而不是整套 RL 框架。前者能直接迁移到“经验筛选 / 记忆质量评估”，后者工程代价较高。
- **Experimental design**: 同时报 intra-environment、cross-environment、agreement with human judgments、update sparsity，是很完整的 continual learning 评测模板。

### Connections to Other Papers in Knowledge Base
> ⚠️ NEEDS YOUR INPUT: 可与 [2025_MobileAgentV3](../notes/2025_MobileAgentV3.md) 对比训练期自演化；与 [2026_GUI-Genesis](./2026_GUI-Genesis.md) 对比“构造训练环境”路线；与 memory-oriented papers 如 [2026_M2](./2026_M2.md) 对比训练期 adaptation vs inference-time augmentation。

## Citation Tracking
- [ ] CUAJudge / WebJudge lineage: 需要追 evaluator 设计来源
- [ ] UI-TARS-1.5: 作为 base agent 必须回看其能力边界
- [ ] ScienceBoard / OfficeWorld / OSWorld: 需要补 benchmark 生态差异

## Key Passages
> "real-world digital environments are not static" (Abstract, p.1)

> "our method effectively enables both intra-environment and cross-environment continual learning, yielding 4-22% performance gains" (Abstract, p.1)

> "CUAJudge consistently exhibit[s] high agreement with human judgments (93.7%)" (Section 4.6, p.8)
