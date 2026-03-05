# Persona2Web — Benchmarking personalized web agents with user history

## Meta
- **Title**: Persona2Web: Benchmarking Personalized Web Agents for Contextual Reasoning with User History
- **Authors**: Serin Kim et al. | Yonsei University
- **Venue**: ICML 2026 | arXiv:2602.17003
- **Links**: [PDF](../source_todo/Persona2Web.pdf) | Code: placeholder mentioned in PDF | Project: not listed in PDF
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-06
- **Priority**: P1 | **Reading progress**: Pass 1

## One-line Summary
Persona2Web 提出首个 real open web 上的 personalized web agent benchmark，通过 clarify-to-personalize 查询、用户历史和 reasoning-aware rubric 评估个性化能力，并揭示现有 agent 在没有用户历史时对模糊查询的成功率会直接掉到 0%（Abstract / Section 5.3, p.1, p.7）。

## Problem Setting
- **Core problem**: "current agents lack personalization capabilities" and practical web agents must infer user preferences from history rather than fully specified instructions (Abstract, p.1)
- **Assumptions**: 用户历史可被构造成长期、隐式偏好线索；个性化 query 会故意省略关键约束；评测需要看 reasoning trace 才能区分 personalization failure 与 navigation failure（Section 1, 3-4, p.1-6）。
- **Insufficiency of existing approaches**: "task completion alone cannot capture personalization capability" (Introduction, p.2 / Section 5.3, p.7)

## Core Method
- **Method overview**: Persona2Web 的设计目标不是测“网页会不会点”，而是测 agent 能否利用 user history 补全用户未明说的偏好。为此，作者围绕 clarify-to-personalize 原则构造 benchmark：用户历史中埋有长期偏好线索；query 刻意保留歧义；agent 必须在执行时读取并使用历史，而不是靠 query 里显式给出的 slot 填值。

  评测上，作者没有停留在 outcome-based success，而是提出 reasoning-aware evaluation framework，对 preference、website、intent 三个维度用 rubric 打分。与 action-wise / outcome-based 自动评估相比，这种方法利用了 history retrieval 与 reasoning trace，因此更能定位 personalization 是“没找到相关历史”，还是“找到了但没用对”。实验则把 AgentOccam 与 Browser-Use 两种基础架构加上 personalization module，在 no-history / on-demand / pre-execution 三种 history access schemes 下统一比较。
- **Key Design Choices**:

| Design Decision | Author's Choice | Author's Rationale | Ablation Verified? |
|----------------|----------------|--------------------|--------------------|
| Query design | Clarify-to-personalize ambiguous queries | 强迫 agent 从 history 推断缺失偏好 | Yes |
| Context source | Long-span user history | 让偏好以隐式行为模式而非显式槽位出现 | Yes |
| Evaluation | Reasoning-aware rubric | 区分 personalization vs navigation failure | Yes（Table 4, p.6-7） |
| Access schemes | No-history / On-demand / Pre-execution | 比较何时访问历史更有效 | Yes（Table 3, p.6） |

- **Core difference from prior work**: 现有 web benchmarks 大多测显式任务执行，Persona2Web 则把 personalization 设成一级目标，并且把评估粒度从 outcome 推进到 reasoning-level diagnosis（Section 1-2, p.1-3）。

## Key Results

| Benchmark | This Method | Strongest Baseline | Δ | Notes |
|-----------|------------|-------------------|---|-------|
| No-history scheme SR | 0% across all models | N/A | N/A | Confirms user history is necessary (Section 5.3, p.7) |
| Browser-Use + GPT-4.1 (On-demand) | SR 0.13, `P_avg` 0.767 | Same scheme AgentOccam + GPT-4.1: SR 0.06, `P_avg` 0.658 | +0.07 SR / +0.109 `P_avg` | Table 3, p.6 |
| Browser-Use + o3 (On-demand) | SR 0.13 | AgentOccam + o3: 0.07 | +0.06 | Table 3, p.6 |
| Reasoning-aware eval (Preference) | Pearson 0.7200, Accuracy 0.8800 | Action-wise: 0.3993 / 0.5600 | substantial | Table 4, p.6 |
| Reasoning-aware eval (Intent) | Pearson 0.7386, Accuracy 0.7400 | Outcome-based: 0.5909 / 0.7000 | better aligned | Table 4, p.6 |

- **Key ablation findings**: history access 方式会显著影响结果。总体上，启用 history 后 SR 才能从 0 提升到 6-13% 的区间；Browser-Use 在 personalization score 上通常比 AgentOccam 更强，作者将其归因于 richer DOM representation 更利于使用历史（Section 5.3, p.6-7）。
- **Failure cases**: 作者明确指出两类 failure: history retrieval failure 与 history utilization failure。也就是说，即便检索了历史，agent 也常常不知道在什么步骤使用它，例如检索到 location 但没有在真正搜索前设置它（Section 5.3 / error analysis, p.7-8）。

## Limitations
- **Author-stated limitations**: 论文在 Impact Statement 中承认，真实 personalized agents 需要访问真实用户数据，会带来 consent 与 data protection 问题；同时 open web 本身也可能暴露 agent 于有害内容（Impact Statement, p.9）。
- **My observed limitations**: 
> ⚠️ NEEDS YOUR INPUT: (1) 当前 benchmark 强在“个性化需求识别”，但实际 task success 仍很低，说明 personalization 还没有被真正做成可用能力。(2) 用户历史是合成的，虽然避免隐私问题，但和真实用户噪声、矛盾偏好、演化偏好之间仍有差距。(3) benchmark 主要强调 ambiguous query resolution，对长期跨 session memory 更新还没有展开。
- **Experimental design gaps**: 没有测试 user profile 会持续变化时的适应；也没有纳入显式用户澄清对话，只评 history-based disambiguation。

## ⭐ Relation to My Research

### Position in Survey
- **Corresponding survey section/category**:
> ⚠️ NEEDS YOUR INPUT: 最适合放在 **Personalization / User Modeling / Evaluation** 小节，尤其适合作为“user history as memory”方向的 benchmark 入口。
- **Role**: Background reference / Positive example

### Gap Signals (extracted from this paper)
- Gap signal 1: "all agents fail completely on ambiguous queries, achieving a 0% success rate" (Section 5.3, p.7) → 没有历史就无法做 personalization。
- Gap signal 2: 即使有 history access，top proprietary models 的 SR 也仅 6-13%（Table 3, p.6-7）→ user history 可用性并不等于 history utilization competence。
- Gap signal 3: reasoning-aware evaluation 明显优于 action-wise / outcome-based（Table 4, p.6）→ personalization 评估若不看 reasoning，会严重低估失败原因复杂度。

> ⚠️ NEEDS YOUR INPUT: 如果你后续想把 GUI agents 和 user memory 联系起来，这篇是很强的 benchmark 证据，但它还停留在“读取已有历史”，没有讨论 agent 如何持续维护和更新 personalization memory。

### Reusable Elements
- **Methodology**: clarify-to-personalize query design、reasoning-aware personalization rubrics、history access scheme 对照。
> ⚠️ NEEDS YOUR INPUT: 这篇最值得复用的是评估设计，不一定是任务本身。尤其是“个性化失败 vs 导航失败”的拆分，对 survey 写作很有用。
- **Experimental design**: 同时报 `P_web`、`P_pref`、intent satisfaction、SR，是个性化 agent 评测里很完整的一组指标。

### Connections to Other Papers in Knowledge Base
> ⚠️ NEEDS YOUR INPUT: 可与 [2026_AmbiBench](./2026_AmbiBench.md) 对比“ambiguity + clarification”在 mobile 与 web 上的不同表现；与 [2026_M2](./2026_M2.md) 对比 history/memory 的用途，一个是 personalization，一个是长程 navigation。

## Citation Tracking
- [ ] Browser-Use / AgentOccam: 作为 personalization scaffolds 的基础架构
- [ ] WebArena / WebVoyager / PersonalWAB: benchmark lineage 对照
- [ ] PrefEval / MemEval: 评估 user preference 与 memory 的相关工作

## Key Passages
> "the first benchmark for evaluating personalized web agents on the real open web" (Abstract, p.1)

> "all agents fail completely on ambiguous queries, achieving a 0% success rate" (Section 5.3, p.7)

> "reasoning is essential for accurately evaluating personalization" (Section 5.3 / Table 4 discussion, p.6-7)
