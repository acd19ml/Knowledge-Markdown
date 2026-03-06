# ExpeL — Cross-task experiential learning for LLM agents

## Meta
- **Title**: ExpeL: LLM Agents Are Experiential Learners
- **Authors**: Andrew Zhao et al. | Tsinghua University (BNRist)
- **Venue**: AAAI 2024 | arXiv:2308.10144v3 [cs.LG]
- **Links**: [PDF](./ExpeL.pdf) | [Code](https://github.com/LeapLabTHU/ExpeL) | [Project](https://andrewzh112.github.io/expel)
- **Citation count**: 未查询（建议补 Semantic Scholar） | **Read date**: 2026-03-05
- **Priority**: P1 | **Reading progress**: Pass 2

## One-line Summary
ExpeL 通过“跨任务经验池 + insight 抽取 + 相似任务检索”在不更新模型参数的前提下提升 LLM agent 决策表现；在 FEVER transfer 上把 SR 从 ReAct 的 63% 提升到 70%，并在 ALFWorld 的多轮评估中达到 64.2%（R3），显著高于 ReAct+Reflexion 的 54.4%。

## Problem Setting
- **Core problem**: 作者关注“如何在不做参数更新的情况下，让 LLM agent 真正从历史任务中学习”，并明确指出纯 prompt 方法受限于 context window，导致 “no recollections of what they have seen” (Section 1, p.2)。
- **Assumptions**:
  - 任务为交互式序列决策，agent 在每步观察后执行动作并追求目标（Section 3, p.2）。
  - 环境被设定为 deterministic（“We only deal with deterministic environments in this work.”, Section 3, p.2）。
  - 训练期允许 trial-and-error 收集成功/失败轨迹；测试期按单次尝试执行（Section 4, p.3-4）。
  - 主要实验场景是文本观测环境（HotpotQA / ALFWorld / WebShop / FEVER）（Section 5.1, p.7）。
- **Insufficiency of existing approaches**: 作者指出 finetuning “incurs high computational costs and needs access to the LLM’s parametric weights”，且可能损害泛化（Section 1, p.2）；而 few-shot prompt agent 因上下文窗口限制无法跨任务持续学习（Section 1, p.2）。

## Core Method
- **Method overview**:

ExpeL 把“学会做题”的过程拆成三个阶段：先在训练任务上反复尝试并记录轨迹（experience gathering），再把经验抽象成可复用 insight（insight extraction），最后在测试时用“insight + 相似成功轨迹”共同引导决策（task inference）（Figure 1, p.3; Section 4, p.3-5）。

经验收集阶段借用 Reflexion 的 retry 机制：同一训练任务最多尝试 Z 次，失败则追加 verbal reflection 再重试，成功/失败轨迹都进入经验池 B（Section 4.1, p.4）。这一步的关键不是只追求当前任务成功，而是故意收集“可对比”的 success/failure 对，供后续 insight 抽取使用。

经验利用阶段采用双通道：其一是从经验池检索 top-k 相似成功轨迹作为 in-context demos（FAISS + all-mpnet-base-v2 + task similarity 排序）；其二是让 LLM 对 success/failure 对或 success 集合做结构化操作（ADD/EDIT/UPVOTE/DOWNVOTE）迭代维护 insight 集合，并通过 importance 计数做保留/淘汰（Section 4.2, p.4）。最终在推理 prompt 中同时注入两类信息，形成“抽象规则 + 具体范例”的互补（Section 4.3, p.4-5）。

- **Key Design Choices**:

| Design Decision | Author's Choice | Author's Rationale | Ablation Verified? |
|----------------|----------------|--------------------|--------------------|
| 经验来源 | 用 Reflexion 进行多次重试来收集经验 | 同时提高成功样本数量并构造 success/failure 对 | Yes（Section 5.6 + Fig.6, p.9） |
| 学习通道 | 同时使用 insight 抽取与相似轨迹检索 | 抽象规则和具体示例在不同环境互补 | Yes（Section 5.2, p.7-8） |
| 检索排序 | 以 task similarity 排序 top-k 成功轨迹 | 减轻能力外推负担，优先可直接模仿经验 | Yes（Table 3 lower, p.10） |
| insight 更新机制 | ADD/EDIT/UPVOTE/DOWNVOTE + importance 计数 | 抑制噪声 insight，允许迭代修正 | Partial（机制描述充分，但无独立消融） |
| insight 输入材料 | success/failure 对 + L-success 集合 | 兼顾错误归因与成功共性抽取 | Partial（与 reflections 对比有实验） |
| insight 模型选择 | 默认 gpt-4-0613 生成 insight | 更少 hallucination、指令遵循更好 | Yes（Table 3 upper, p.10） |

- **Core difference from prior work**: 相比 Reflexion 的“单任务内反思重试”，ExpeL 主打“跨任务经验积累 + 跨任务 insight 复用”，并且测试时可以单次尝试而非依赖在线重试（Section 1, p.2; Section 4.5, p.6）。

## Key Results

| Benchmark | This Method | Strongest Baseline | Δ | Notes |
|-----------|------------|-------------------|---|-------|
| FEVER transfer (SR%) | ExpeLTransfer: 70.0 ± 0.7 | ReAct: 63.0 ± 0.4 | +7.0 abs | source=HotpotQA insights，目标域仍显著增益（Table 1, p.9） |
| ALFWorld + Reflexion rounds (R3) | ExpeL+Reflexion: 64.2% | ReAct+Reflexion: 54.4% | +9.8 abs | ExpeL 与 reattempt 机制可叠加（Table 2, p.9） |
| ALFWorld single-attempt proxy (R0) | ExpeL+Reflexion: 59.0% | ReAct+Reflexion: 40.3% | +18.7 abs | 论文强调 Highlight=one attempt（Table 2 caption, p.9） |
| HotpotQA insight ablation (SR%) | ExpeL (ours): 39.0 ± 1.7 | gpt-3.5 insight: 32.0 ± 0.4 | +7.0 abs | 说明更强 insight 生成器有效（Table 3 upper, p.10） |
| ALFWorld retrieval strategy (SR%) | ExpeL (task-sim retrieval): 59.0 ± 0.3 | Reasoning-similarity: 48.5 ± 2.1 | +10.5 abs | task similarity 排序优于替代策略（Table 3 lower, p.10） |
| WebShop reward score | ExpeL (ours): 0.701 | ReAct: 0.665 | +0.036 | 在 shop 场景 reward 更高（Table 5, p.36） |

- **Key ablation findings**:
  - 经验多样性关键：只靠初始 few-shot 抽 insight 基本无优势，必须依赖额外自主收集经验（Section 5.6 + Fig.6, p.9）。
  - insight 质量关键：LLM 自动学习的 insight 优于手工规则；将 reflections 直接并入 insight 抽取会掉点，作者解释为 hallucination 噪声（Table 3 upper, p.10）。
  - 检索策略关键：task similarity > reasoning similarity > random sample（Table 3 lower, p.10）。
- **Failure cases**:
  - WebShop 仍是短板，作者明确说其表现“approaching the lower side of Reflexion’s success rates”（Section 5.2, p.8）。
  - 论文行为分析虽展示了自纠错案例，但仍显示 ExpeL 对环境特定操作知识（如购物站点细节）依赖较强，跨环境稳定性仍需更多证据（Section 5.2-5.3, p.8）。

## Limitations
- **Author-stated limitations**:
  - 当前只验证文本观测任务，真实世界需要图像观测能力（Section 6, p.10）。
  - 主要基于 closed-source API LLM，部分场景不可用，需探索开源模型（Section 6, p.10）。
  - 长期学习下 insight 可能触发上下文窗口管理问题，需要额外检索机制（Section 6, p.10）。
  - prompt 方法缺少 RL 那样的理论保障，策略效率上限不清晰（Section 6, p.10）。
- **My observed limitations**:
> ⚠️ NEEDS YOUR INPUT: 初步判断 ExpeL 在“可解释、无需参数更新”上很实用，但对你若要做更强 self-evolving agent 仍有三处风险：  
> 1. 证据主要来自文本基准，尚不足以支撑移动端 GUI/视觉场景迁移；  
> 2. 经验池与 insight 更新规则较启发式，缺少稳定性理论与收敛分析；  
> 3. 成功率增益与 token/成本增加（Table 6）之间缺少系统性 cost-effectiveness 讨论。  
> 建议你确认这三点是否作为你方法章节里的“待突破瓶颈”。
- **Experimental design gaps**:
  - 主文对比对象以 Act/ReAct/Reflexion 为主，缺少与更广泛 memory/planning agent 的统一复现实验。
  - 缺少“经验池规模增长曲线”与“长周期退化”分析（lifelong 情况仅在 limitation 文字提及）。
  - transfer 只测 HotpotQA -> FEVER，一跳迁移仍偏窄。

## Relation to My Research

### Position in Survey
- **Corresponding survey section/category**:
> ⚠️ NEEDS YOUR INPUT: 建议放在 `Self_Evolve` 主线的 “Experience-to-Policy without Weight Update” 小节，作为连接 Reflexion（单任务反思）与 Skill/Memory 机制（跨任务积累）的桥接论文。
- **Role**: Positive example + Bridge paper（方法可复用，且暴露了跨模态迁移缺口）

### Gap Signals (extracted from this paper)
- Gap signal 1: “these agents have no recollections of what they have seen” (Section 1, p.2) → implies 仅靠短上下文 few-shot 难以支持持续学习。
- Gap signal 2: “self-reflection methods are stateless and cannot learn cross-task insights” (Appendix A.3, p.13) → implies 单任务 verbal feedback 不足以构建可迁移程序性记忆。
- Gap signal 3: “tasks with textual observation ... limiting in real-world scenarios” (Section 6, p.10) → implies 经验学习向视觉/GUI 迁移是明确开放问题。
- Gap signal 4: ALFWorld 检索消融中 random/非 task-sim 排序显著掉点（Table 3, p.10）→ implies “记忆检索策略”本身是性能瓶颈，而非仅仅“是否有记忆”。

> ⚠️ NEEDS YOUR INPUT: 你可以把 Gap 2 + Gap 4 合并成一个核心研究问题：如何让跨任务 memory 的“写入-检索-更新”具备更强鲁棒性与可解释性。

### Reusable Elements
- **Methodology**:
  - 三阶段闭环（gather -> extract -> infer）可直接迁移到你的 agent self-evolution pipeline。
  - insight 维护的“可编辑/可投票”机制适合做人类可干预 memory governance。
> ⚠️ NEEDS YOUR INPUT: 你可考虑把 ExpeL 的 `insight` 升级成“可执行 skill schema（触发条件 + 动作模板 + 失败回滚）”，更贴合 GUI 任务。
- **Experimental design**:
  - 强烈建议复用其 “single-attempt vs reattempt” 分离评估：可测真正的跨任务学习能力，而不是在线 retry 带来的即时补救收益。

### Connections to Other Papers in Knowledge Base
> ⚠️ NEEDS YOUR INPUT: 建议建立以下显式关联。  
> 1. `/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/2026_SkillRL.md`：都在探索经验到可复用行为单元的转化，但 ExpeL 偏 prompt-memory，SkillRL 偏强化学习范式。  
> 2. `/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/Reflexion.pdf`：ExpeL 将 Reflexion 从“单任务自改进”扩展到“跨任务累积学习”。  
> 3. `/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/2023_AppAgent.md`、`/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/2024_MobileAgentV2.md`、`/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/2026_MobileAgentV3_5.md`：ExpeL 的文本经验机制可作为 GUI 经验记忆模块的先导设计。

## Citation Tracking
- [ ] ExpeL (Zhao et al., 2024): 作为“无参数更新的跨任务经验学习”核心引用
- [ ] Reflexion (Shinn et al., 2023): 对照 ExpeL 的单任务重试基线
- [ ] ReAct (Yao et al., 2023): 作为 ExpeL 的基础决策框架
- [ ] ALFWorld / WebShop / HotpotQA / FEVER: 作为 benchmark 协议与评测背景引用

## Key Passages
> “these agents have no recollections of what they have seen” (Section 1, p.2)

> “ExpeL matches Reflexion’s performance (40% at R3 vs. 39%) for HotpotQA and even outperforms it for ALFWorld (54% at R3 vs. 59%)” (Section 5.2, p.8)

> “we investigated tasks with textual observation, which is limiting in real-world scenarios” (Section 6, p.10)
