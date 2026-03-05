# DEACTION — Detecting and correcting misaligned actions in CUAs

## Meta
- **Title**: When Actions Go Off-Task: Detecting and Correcting Misaligned Actions in Computer-Use Agents
- **Authors**: Yuting Ning et al. | The Ohio State University + Amazon AGI
- **Venue**: Preprint, 2026 | arXiv:2602.08995
- **Links**: [PDF](../source_todo/When-Actions-Go-Off-Task.pdf) | Project: https://osu-nlp-group.github.io/Misaligned-Action-Detection | Code: not listed in PDF
- **Citation count**: Check Semantic Scholar | **Read date**: 2026-03-06
- **Priority**: P1 | **Reading progress**: Pass 1

## One-line Summary
这篇论文首次系统定义 CUA 中的 misaligned action detection，构建含 2,264 条 action-level 标注的 MISACTBENCH，并提出可插拔 guardrail DEACTION，在离线检测上把 F1 提升 15%+，在线红队设置下把 attack success rate 降低 90% 以上，同时保持 benign utility（Abstract / Section 5, p.1-2, p.6-7）。

## Problem Setting
- **Core problem**: CUAs "frequently produce misaligned actions that deviate from the user's original intent" (Abstract, p.1)
- **Assumptions**: misalignment 可在 action 执行前根据当前指令、历史和观察判断；alignment 不等于最优，只要 action 能被解释为推进用户真实目标即可；misalignment 包括外部攻击与内部推理错误两大来源（Section 1-2, p.1-2）。
- **Insufficiency of existing approaches**: existing guardrails are "predominantly tied to predefined policies or known attack patterns," leaving many intent deviations uncovered (Introduction, p.1)

## Core Method
- **Method overview**: 论文先把问题定义从 safety policy violation 改写为 intent-centric action alignment。基于这个定义，作者把 misaligned actions 分成三类: Malicious Instruction Following、Harmful Unintended Behavior、Other Task-Irrelevant Behavior。随后构建 MISACTBENCH，混合收集真实攻击 benchmark 轨迹与 benign trajectory 上合成的 unintended subgoal 偏移，最终得到 2,264 条 human-annotated action-level labels。

  在此基础上，DEACTION 不是简单 block 动作，而是先检测、再给出 structured feedback，引导 agent 迭代修正。实现上它包含 fast check 与 systematic analysis 两级判断，并使用 narrative summaries 而不是直接喂长截图序列，以降低开销同时保留长期上下文。作者特别强调，这让 guardrail 可以即插即用地接入不同 CUA，而不要求读取 agent 内部 reasoning state。
- **Key Design Choices**:

| Design Decision | Author's Choice | Author's Rationale | Ablation Verified? |
|----------------|----------------|--------------------|--------------------|
| Problem framing | Intent-centric action alignment | 比 safety-policy framing 更广、更贴近真实误行为 | Yes |
| Benchmark granularity | Action-level human labels (MISACTBENCH) | 支持执行前检测，而非事后 trajectory 打分 | Yes |
| History representation | Narrative summaries | 比 raw screenshots 更省 token 且更适合长上下文判断 | Yes |
| Runtime correction | Detect + iterative structured feedback | 保持 task progress，而不是一刀切 blocking | Yes |

- **Core difference from prior work**: 过去方法多关注 prompt injection / policy violation；DEACTION 明确针对“ technically allowed but unjustified” 的 off-task actions，因此覆盖面更宽，也更接近用户真正关心的 agent reliability（Section 1-2, p.1-3）。

## Key Results

| Benchmark | This Method | Strongest Baseline | Δ | Notes |
|-----------|------------|-------------------|---|-------|
| MISACTBENCH F1 (GPT-5.1 Thinking) | 82.8 | TaskShield 66.9 | +15.9 pts | Table 3, p.6 |
| MISACTBENCH F1 (Claude Sonnet 4.5) | 80.4 | TaskShield 66.6 | +13.8 pts | Table 3, p.6 |
| MISACTBENCH F1 (Qwen3-VL-32B) | 70.7 | InferAct 61.6 | +9.1 pts | Table 3, p.6 |
| Detection precision (GPT-5.1 Thinking) | 89.9 | TaskShield 61.3 | +28.6 pts | Table 3, p.6 |
| Online adversarial evaluation | ASR reduced by >90% | no-defense / prior defenses | large reduction | Section 5.2, p.7 |

- **Key ablation findings**: narrative summary history 表达优于 actions-only 和 actions+observations，既更准也更便宜；两阶段 fast check + systematic analysis 在 11.3s/step 时达到 79.9 F1，优于只追求极低 latency 的 fast check-only（Table 4 / Figure 4, p.6-7）。
- **Failure cases**: 作者在 Error Analysis 中指出三类残留 failure: disguised malicious instructions 绕过 fast check、LLM 对 coordinate-based actions grounding 不足、以及高层 intent reasoning 本身犯错（Section 5.1, p.7）。

## Limitations
- **Author-stated limitations**: "these failure modes highlight promising directions for future work, such as more robust injection detection, fine-grained action understanding, and accurate intent-level reasoning." (Section 5.1, p.7)
- **My observed limitations**: 
> ⚠️ NEEDS YOUR INPUT: (1) DEACTION 的前提是仍有足够强的外部模型来做 alignment judgment，这在成本与 latency 上不会免费。(2) 它主要是 runtime guardrail，而不是从 misalignment 中持续学习的机制；失败经验没有被进一步沉淀成 memory/skill。(3) action alignment 仍由语言模型判断，遇到非常细粒度 GUI state 差异时可能会不稳。
- **Experimental design gaps**: 还没有看到 guardrail 与 agent 内部 planner 更深耦合后的效果；也缺少对 benign-but-suboptimal exploratory actions 的更细颗粒分类。

## ⭐ Relation to My Research

### Position in Survey
- **Corresponding survey section/category**:
> ⚠️ NEEDS YOUR INPUT: 适合放在 GUI Agent survey 的 **Reliability / Safety / Guardrails** 小节，但注意它的 framing 比传统 safety paper 更偏“intent preservation”。
- **Role**: Positive example / Contrastive baseline

### Gap Signals (extracted from this paper)
- Gap signal 1: "not all problematic behaviors can be anticipated and enumerated as policy violations" (Introduction, p.1) → GUI agent reliability 不能只靠 policy blacklist。
- Gap signal 2: MISACTBENCH 需要人工 action-level 标注才得以建立（Section 3, p.3-5）→ 高质量 misalignment 数据仍稀缺。
- Gap signal 3: future work points to injection detection, action understanding, intent reasoning (Section 5.1, p.7) → 当前 guardrail 仍远未覆盖复杂开放世界偏移。

> ⚠️ NEEDS YOUR INPUT: 如果你的知识库主线会碰到 memory / self-correction，这篇可作为“runtime guardrail”参照物，然后进一步问: guardrail 检出的 misalignment 能不能转化成可复用经验？

### Reusable Elements
- **Methodology**: intent-centric alignment definition、narrative-summary history representation、detect-and-correct loop 都值得借鉴。
> ⚠️ NEEDS YOUR INPUT: 我认为最值得复用的是 action alignment 的定义，而不是具体 prompt。它能作为后续 memory filtering 或 trajectory quality control 的判断标准。
- **Experimental design**: 同时报 offline F1 / precision / recall 与 online ASR / UA / benign SR，非常完整。

### Connections to Other Papers in Knowledge Base
> ⚠️ NEEDS YOUR INPUT: 可与 [2026_ActionEngine](./2026_ActionEngine.md) 对比 runtime reliability，一个偏 deterministic planning，一个偏 guardrail；也可与 [2026_ACuRL](./2026_ACuRL.md) 对比“检测错误”与“从错误中持续学习”的区别。

## Citation Tracking
- [ ] TaskShield / InferAct: action alignment baseline
- [ ] RedTeamCUA / RiOSWorld / OSWorld: online adversarial evaluation setup
- [ ] PromptArmor / DSP: 防注入基线

## Key Passages
> "misaligned actions that deviate from the user's original intent" (Abstract, p.1)

> "DEACTION outperforms baselines by over 15% absolute in F1 score" (Abstract / Section 2, p.1-2)

> "future work, such as more robust injection detection, fine-grained action understanding, and accurate intent-level reasoning" (Section 5.1, p.7)
