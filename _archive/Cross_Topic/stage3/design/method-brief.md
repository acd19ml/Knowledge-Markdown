# Stage 3 Method Brief

> **Status**: Supporting draft
> **Purpose**: 把 Stage 2 的 survey/gap 结论压缩成可执行的方法设计入口
> **Main Line**: `A-1 procedural memory for GUI` + `A-4 failure-driven write-back`
> **Primary Inputs**: [main-line.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/main-line.md), [taxonomy-draft.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/taxonomy-draft.md), [gap-tracker.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/gap-tracker.md), [interim-survey-draft.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/interim-survey-draft.md)
> **Readiness Artifacts**: [rq-proof-sheet.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/readiness/rq-proof-sheet.md), [precedent-synthesis.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/readiness/precedent-synthesis.md)
> **Formal Outputs**: [problem-statement.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/formal/problem-statement.md), [method-spec.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/formal/method-spec.md), [nearest-work-delta.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/formal/nearest-work-delta.md), [evaluation-plan.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/formal/evaluation-plan.md)
> **Note**: 本页保留设计推导细节；最终引用应优先使用 `formal/` 下对应页面。

---

## 1. One-Paragraph Decision

Stage 3 不再继续追问“GUI agent 是否需要 memory”。这个问题已经在 Stage 2 结束。当前方法问题正式收敛为：**如何把交互中获得、且超出基础模型先验的局部程序性经验，写成可检索、可施加、可被失败修订的 `experience-delta procedural memory`，并证明它在 repeated-task、same-app / same-site cross-task 和 near-domain app-family / site-family transfer 中带来稳定经验增益。**

因此，Stage 3 的目标不是再造一个泛化的 long-context agent，而是实现一套更窄、更可检验的 memory loop：

`post-task experience -> rule abstraction -> cross-task retrieval/application -> failure-driven write-back`

---

## 2. Final RQ

> **Final RQ**: LLM-based GUI agents 如何把交互中获得、且超出基础模型先验的 `experience-dependent procedural knowledge` 表示成可检索、可修订、可跨任务复用的 memory，并通过 `post-task -> cross-task` 的 failure-aware write-back，使其在重复任务、同 app / site 跨任务与近邻 app-family / site-family 场景中稳定带来经验增益？

### 2.1 Sub-RQ Mapping

- **Sub-RQ1**: 什么样的经验对象值得写入 memory，而不是留给 base model prior 或 raw trajectory？
- **Sub-RQ2**: 这些经验对象应如何表示，才能既保留 GUI grounding，又支持跨任务复用？
- **Sub-RQ3**: retrieval 和 application 应如何分离设计，避免 memory 退化成 prompt stuffing？
- **Sub-RQ4**: failure 应如何触发 memory 的 `edit / split / downweight / rewrite`，而不是只被当成一次运行时错误？

### 2.2 Five-Point RQ Check

当前 Final RQ 已经可以直接按 [KB-Expansion-Guide.md](/Users/mac/studyspace/Knowledge-Markdown/KB-Expansion-Guide.md) 的五项标准检验：

| Check | Current Evidence | Current Judgment |
|---|---|---|
| **Specific** | 研究对象已收紧到 `experience-dependent procedural knowledge`；场景已固定为 repeated-task、same-site cross-task、near-domain site-family transfer | Pass |
| **Answerable** | 已有明确对照组、memory unit、write-back 操作和 3 层 transfer protocol，见 [experiment-protocol.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/design/experiment-protocol.md) 与 [webarena-task-split.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena-task-split.md) | Pass |
| **Novel** | 与 `MobileGPT / MAGNET / ActionEngine / AWM / SkillWeaver` 的差异已收敛到 `GUI local rule + failure-aware rewrite`，而不是 app graph、workflow cache 或 API library | Pass, but must keep nearest-work delta explicit |
| **Feasible** | Stage 3 只锁定 WebArena pilot，不要求 execution-ready benchmark infra；24 个官方 task binding 已足够支撑方法设计 | Pass |
| **Impactful** | 若成立，结论推进的是“agent memory 应如何表示与修订”的领域认知，而不只是某个 benchmark 上的小工程优化 | Pass |

### 2.3 Experimental Validation Path

当前 RQ 的实验回答路径已经足够明确，不需要继续扩 benchmark 基础设施才能成立：

1. **对象对照**：`no memory` vs `raw trajectory retrieval` vs `coarse workflow memory` vs `EDPM`
2. **写回对照**：`success-only` vs `failure-aware write-back`
3. **施加对照**：`context injection` vs `policy constraint / reranking`
4. **场景对照**：`L1 repeated task` vs `L2 same-site cross-task` vs `L3 near-domain transfer`
5. **结果判断**：如果优势只出现在 L1，而 L2/L3 不稳定，则说明学到的是 task cache，而不是 transferable rule

正式的 go/no-go 规则见 [rq-decision-matrix.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/readiness/rq-decision-matrix.md)。Stage 3 后续不再接受“看起来更好”式结论，必须按该表逐项判断 `Support / Borderline / Fail`。

---

## 3. Core Hypotheses

### H1. Memory Unit Hypothesis

将 GUI 经验表示为带 `trigger / procedure / constraint / failure signal / revision cue / scope` 的 procedural rule，会优于：

- `raw trajectory retrieval`
- `coarse workflow memory`
- `success-only memory`

因为它更接近真正可迁移的经验差分知识，而不是 task cache。

### H2. Retrieval-Application Separation Hypothesis

把 `retrieval` 和 `application` 分开设计，会比单纯的 `similarity retrieval + context injection` 更稳定。至少在同等 retrieval 质量下，带有显式 policy constraint 或 tool-level invocation 的 carrier，应该优于纯 prompt 注入。

### H3. Failure Write-Back Hypothesis

failure-aware write-back 会显著优于 success-only accumulation，尤其在：

- 界面轻微变化
- 隐含前置条件
- 相似任务但非完全重复的场景

因为它能让 memory 从“成功案例仓库”变成“可修订的经验层”。

---

## 4. Proposed Method Object

### 4.1 Target Object

方法对象不是 generic skill、不是 semantic app note、也不是完整 workflow replay，而是：

> **Experience-Delta Procedural Memory (EDPM)**

它只记录那些通过交互才显露出来、且对后续决策有判别价值的局部策略。

### 4.2 Memory Unit Schema

每条记忆至少包含：

- **Intent / Task Slice**: 当前局部目标是什么
- **Trigger Context**: 触发这条经验的界面状态、视觉线索或任务条件
- **Procedure**: 推荐操作策略
- **Constraint / Preconditions**: 策略成立的前提条件
- **Failure Signal**: 哪些现象说明这条规则可能失效
- **Revision Cue**: 失败后应该如何修改
- **Scope**: repeated task / same app-site / app-family-site-family
- **Evidence Link**: 这条规则来自哪些成功/失败片段

### 4.3 Non-Goals

当前阶段不把以下对象当作主 memory unit：

- generic GUI prior
- whole-task workflow cache
- unconstrained natural-language advice
- user profile memory
- full episodic archive

这些对象可以作为辅助层，但不应抢占主方法对象。

---

## 5. Method Sketch

### 5.1 Module 1: Experience Candidate Mining

从执行轨迹里筛出真正值得写入的经验片段，而不是把所有步骤都存下来。

优先保留：

- 首次不稳定但后来成功的局部片段
- 对任务成败有决定性影响的分叉步骤
- 失败后暴露隐藏前提的片段
- 在多个任务中反复出现的局部策略模式

过滤掉：

- base model 稳定会做的 GUI 常识
- 纯机械重复步骤
- 无法定位失败原因的噪声片段

### 5.2 Module 2: Procedural Rule Abstraction

把候选片段抽象成局部 procedural rule，而不是整段 workflow。

当前推荐借鉴：

- [2024_AWM.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2024_AWM.md)
  取其 `trajectory -> reusable workflow abstraction`
- [2025_SkillWeaver.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2025_SkillWeaver.md)
  取其 `executable skill representation + precondition-aware selection`

当前明确不直接照搬：

- AWM 的全文本 workflow 表示
- SkillWeaver 的 website-specific API skill 形式

因为当前目标是 GUI-grounded local rule，不是 web API 库。

### 5.3 Module 3: Retrieval and Application

`Match Operator` 与 `Application Carrier` 分离实现。

推荐最小实现：

- **Match Operator**: similarity retrieval over rule candidates
- **Application Carrier**:
  - v0: context injection
  - v1: policy constraint / reranking

这样可以先验证“rule 表示是否有效”，再验证“carrier 是否进一步增强稳定性”。

### 5.4 Module 4: Failure-Driven Write-Back

失败后不只是再试一次，而是对已有 rule 做结构化更新。

最小操作集：

- **edit**: 原规则大体正确，但条件或描述不完整
- **split**: 一个 rule 混合了两个不同情境
- **downweight**: rule 仍可用，但适用范围被高估
- **rewrite**: 原规则已不再成立，需要替换为新规则

---

## 6. Nearest-Work Delta

当前最近邻工作不应只理解为 “AWM + SkillWeaver”，而应按 [precedent-synthesis.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/readiness/precedent-synthesis.md) 的 screened set 来看：哪些论文定义了候选 design choice，哪些论文构成替代解释，哪些论文只是背景支撑。

### 6.1 Co-Primary Precedents

| Nearest Work | 它已经做到什么 | 它没做到什么 | 当前方法的核心差异 |
|---|---|---|---|
| MobileGPT | per-app hierarchical memory；sub-task / action reuse；warm-start procedural recall | 无 cross-app/site reuse；failure repair 依赖 HITL | 从 `per-app memory graph` 转向 `post-task rule abstraction + cross-task reusable rule` |
| MAGNET | GUI procedural memory + dynamic evolution；双层 memory；当前最强 partial solution | evolution 仍主要依赖成功轨迹；procedural unit 仍偏 workflow-level | 从 `success-driven workflow memory` 推进到 `failure-aware experience-delta rule` |
| AWM | 从成功/失败经验抽象 reusable workflow；online update；transfer-oriented evaluation | 文本/web setting；whole-workflow 粒度；不是 GUI-grounded local rule | 借其 `experience -> abstraction -> reuse` 闭环，但收缩 memory unit 粒度 |
| SkillWeaver | skill selection / precondition filtering / verification / honing 问题显式化 | per-website API skill；关键 design choices 缺乏严格模块级 ablation | 借其 governance 视角，而不继承 API skill 作为主 memory unit |

### 6.2 Contrastive Precedent

| Nearest Work | 它已经做到什么 | 它没做到什么 | 当前方法的核心差异 |
|---|---|---|---|
| ActionEngine | structural state-machine memory；programmatic planning；强效率收益 | 记忆对象是 topology/template，不是 post-task experience rule | 当前方法关注可修订 procedural memory，而非 site graph / program synthesis 主线 |

### 6.3 Alternative Routes That Must Be Excluded

| Alternative Route | 它已经做到什么 | 为什么仍不是当前方法的答案 | 当前方法需要说清什么 |
|---|---|---|---|
| EvoCUA | training-time self-evolution；failure-aware training recipe；大规模可验证经验闭环 | 主战场在训练期策略更新，不是 deployment-time external memory revision | 为什么 inference-time memory 不是训练路线的弱替代 |
| Mobile-Agent-v3.5 | native multi-platform GUI model；强 backbone + RL + in-context memory management | 更强 native model 仍未替代 external procedural memory；部署后无独立 write-back loop | 为什么“更大模型 + 更强训练”不足以回答当前 RQ |

### 6.4 One-Sentence Claim

> 当前方法不是再做一个更大的 workflow cache、API skill library、structural graph memory 或 training-time evolution recipe，而是把 GUI 交互中的局部经验差分知识写成可修订 procedural rule，并把 failure 直接接入 deployment-time write-back loop。

---

## 7. Benchmark Lock-In

### 7.1 Recommended Primary Benchmark

> **Primary**: `WebArena`

原因：

- 与 `AWM / SkillWeaver / ActionEngine / EvoCUA` 的 web precedent 和 alternative routes 对齐最好
- 能以最低工程成本承接 `MobileGPT / MAGNET` 在 GUI memory 侧提出的 design questions
- site-level instrumentation 更容易做 repeated exposure 与 write-back 分析
- same-site cross-task 与 near-domain site-family transfer 更容易构造
- 工程难度明显低于直接从 Android full-stack 起步

### 7.2 Recommended Secondary Evaluation

- **Secondary A**: `Online-Mind2Web / Mind2Web`
  用于验证从静态网站到更真实网页任务的迁移
- **Secondary B**: AndroidEnv / AndroidWorld
  不作为 Stage 3 必须项，作为后续 GUI-native 扩展验证

### 7.3 Transfer Boundaries to Test

- **Level 1**: repeated-task reuse
- **Level 2**: same-site cross-task reuse
- **Level 3**: near-domain site-family transfer

开放跨站点泛化不作为 Stage 3 入口门槛。

---

## 8. Minimum Experimental Package

### 8.1 Baselines

- `no memory`
- `raw trajectory retrieval`
- `success-only memory`
- `failure-aware memory update`
- `coarse workflow memory`
- `fine-grained delta procedural memory`

### 8.2 Core Metrics

- task success rate
- repeated-exposure improvement
- same-site cross-task transfer gain
- near-domain transfer gain
- failure-after-write-back recovery rate
- memory precision
  - 检索到的 rule 是否真的适用
- memory revision quality
  - 更新后是否减少误用

### 8.3 Minimal Ablations

- 去掉 `failure write-back`
- 去掉 `constraint / failure signal`
- `rule` 换成 `workflow snippet`
- `policy constraint` 换成纯 `context injection`

---

## 9. Direct Methodological Precedent Synthesis

这部分的目标不是“证明我读过 AWM 和 SkillWeaver”，而是明确：**当前方法具体借什么，不借什么，为什么。**

### 9.1 AWM: What To Reuse

[2024_AWM.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2024_AWM.md) 对当前方法最有约束力的 design choices 有三条：

| AWM design choice | Why it matters | What to reuse in EDPM | What not to copy directly |
|---|---|---|---|
| 把轨迹抽象成可复用 workflow，而不是直接检索原始样例 | 证明“经验抽象”比“样例回放”更有价值 | 保留 `experience -> abstraction -> reuse` 这条主链 | 不直接存 whole-workflow |
| online setting 中 success/failure 都会影响后续记忆 | 证明测试时持续演化值得做 | 保留 write-back 视角，把 failure 纳入 memory revision | 不照搬其 offline/online 混合策略 |
| cross-template / cross-website / cross-domain 三层评测 | 证明 memory 不是只在重复任务上有效 | 保留三层 transfer 评测框架 | 不继续沿用文本 web workflow 作为主对象 |

对当前方法的直接启发是：**必须做抽象，但抽象单位要继续收缩**。AWM 的 workflow 已经证明了“比原始轨迹更好”，但它也暴露了 workflow 过粗时会在动态界面和 memory compatibility 上出问题。因此 EDPM 不再把整段任务当单位，而是把 unit 收缩到 `trigger + local procedure + constraint + failure cue`。

### 9.2 SkillWeaver: What To Reuse

[2025_SkillWeaver.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2025_SkillWeaver.md) 对当前方法最关键的约束不是 API 生成本身，而是 skill governance：

| SkillWeaver design choice | Why it matters | What to reuse in EDPM | What not to copy directly |
|---|---|---|---|
| skill synthesis 不等于 skill 可用，必须有 selection / honing | 说明 memory 库需要治理层 | 保留 precondition-aware selection 与 post-hoc debugging 思路 | 不把 memory unit 直接写成 Playwright API |
| exploration 与 execution 之间存在断层 | 说明“会生成”不代表“会调用” | 保留 application carrier 与 policy layer 的单独设计 | 不把 API 调用成功率当成唯一主问题 |
| verifier 可能被静默失败欺骗 | 说明 write-back 不能只基于表面 success flag | 保留 failure signal / revision cue / downweight 机制 | 不沿用只看 exception-free 的验证标准 |

对当前方法的直接启发是：**memory library 要有选择和修订机制**。SkillWeaver 已经证明可执行技能库有价值，但它也明确说明“available APIs may still not be called”且 verifier 可能误判，所以当前主线更应把重点放在 `retrieval/application separation + failure-driven rewrite`，而不是重新做一遍 API synthesis。

### 9.3 Joint Reading Conclusion

把 AWM 和 SkillWeaver 放在一起，当前方法真正成立的前提就清楚了：

1. **必须抽象经验**，否则只会退化成 raw trajectory retrieval。
2. **抽象单位不能过粗**，否则会退化成 workflow cache。
3. **记忆库必须可治理**，否则会生成但不会用、会用但不会修。
4. **failure 必须进入 write-back**，否则 memory 只会 append，不会 evolution。

因此，EDPM 不是 AWM 的 GUI 版，也不是 SkillWeaver 的 API-less 版。它更准确的定位是：

> 取 AWM 的经验抽象闭环，取 SkillWeaver 的 selection/governance 约束，再把记忆对象收缩成 GUI-grounded local procedural rule，并把 failure-aware revision 放到方法中心。

### 9.4 Must Beat Conceptually

- [2025_MAGNET.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2025_MAGNET.md)
  必须证明自己不是换皮 workflow memory
- [2024_MobileGPT.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2024_MobileGPT.md)
  必须证明自己不被局限在 per-app memory graph
- [2026_ActionEngine.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2026_ActionEngine.md)
  必须说明自己解决的不是 structural planning
- [2025_AMem.md](/Users/mac/studyspace/Knowledge-Markdown/Agent_Memory/papers/notes/2025_AMem.md)
  必须保留 “memory evolution 不是 append-only” 这条原则

---

## 10. Main Risks

- **Risk 1**: 学到的只是 task cache，不是 transferable rule
- **Risk 2**: failure diagnosis 噪声太大，write-back 反而污染 memory
- **Risk 3**: retrieval 有提升，但 application carrier 太弱，无法显著影响决策
- **Risk 4**: benchmark 改造成本过高，导致 Stage 3 卡在数据基础设施

### Mitigations

- 先做 local rule 而非 whole-workflow abstraction
- 先在 WebArena 锁定 repeated-task 与 same-site transfer
- 先用 `edit / downweight`，后做 `split / rewrite`
- 先做 offline write-back，再考虑 online continuous update

---

## 11. Stage 3 Exit Deliverables

完成以下四项，即可认为 Stage 3 结束、进入原型实现：

- 一页正式 problem statement
  - [problem-statement.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/formal/problem-statement.md)
- 一页 method diagram / module spec
  - [method-spec.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/formal/method-spec.md)
- 一页 benchmark and evaluation plan
  - [evaluation-plan.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/formal/evaluation-plan.md)
- 一页 nearest-work delta and novelty defense
  - [nearest-work-delta.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/formal/nearest-work-delta.md)

---

## 12. Immediate Next Steps

1. 把 Section 2.2 和 2.3 收成一页 `RQ proof sheet`，作为 Stage 3 就绪判断的正式证据页。
2. 把 Section 9 收成单独的 `precedent synthesis note`，用于回答 “从已精读文章列表里，哪些前驱真正影响当前 design-choice 判断，为什么不是别的路线”。
3. 只保留能服务于上述两项的 benchmark 细节；execution-ready 配置延后。
4. 在这两项闭合后，再进入 write-back policy 与原型实现。

### Companion Specs

- [memory-unit-schema.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/design/memory-unit-schema.md)
- [experiment-protocol.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/design/experiment-protocol.md)
- [method-figure.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/design/method-figure.md)
- [webarena-task-split.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena-task-split.md)
