# Interim Survey Skeleton — GUI Agent × Memory × Self-Evolving

> **Stage**: Stage 2 draft skeleton
> **Status**: v0.1
> **Built from**: [KB-Expansion-Guide.md](../KB-Expansion-Guide.md) | [main-line.md](main-line.md) | [taxonomy-draft.md](taxonomy-draft.md) | [gap-tracker.md](gap-tracker.md) | [comparison-matrix.md](comparison-matrix.md)
> **Writing principle**: 先把可辩护的 claim 骨架写稳，再逐节补正文与原文引文。

---

## 0. Working Title Candidates

1. **From App-Bound Hints to Reusable Experience: A Survey of Procedural Memory for LLM-based GUI Agents**
2. **Beyond Workflow Caching: Memory, Write-Back, and Experience Reuse in LLM-based GUI Agents**
3. **Experience-Dependent Procedural Knowledge in GUI Agents: A Taxonomy and Research Agenda**

> **当前推荐标题**：第三个。它最贴近当前主线，且允许 Interim Survey 同时覆盖 taxonomy、gap 和 methodology agenda。

---

## 1. Abstract Skeleton

### 1.1 Opening

LLM-based GUI agents have made rapid progress in perception, planning, and action execution, yet their improvement remains dominated by stronger backbones, larger training corpora, or app-specific workflow hints. A more fundamental question is whether GUI agents can accumulate and reuse **experience-dependent procedural knowledge** acquired through interaction.

### 1.2 Problem Statement

This survey argues that the missing capability is not generic GUI skill, but a form of memory that can capture localized procedural rules, constraints, and repair signals that only emerge after task execution, and then reuse them across repeated tasks, same-app transfer, and near-domain app-family transfer.

### 1.3 What This Survey Does

This survey makes three contributions:

1. It formalizes the problem through a taxonomy over **What is learned**, **When experience is written back**, and **How experience is matched and applied**.
2. It shows that current GUI systems only weakly occupy the `post-task / Skills / similarity retrieval × context injection` region, while `rule generalization`, `cross-task reuse`, and `failure-driven memory rewrite` remain largely open.
3. It synthesizes a research agenda centered on **procedural memory** and **failure-aware write-back**, with episodic memory and user-centric personalization treated as supporting or extension lines.

### 1.4 Closing Sentence

The resulting view positions Interim Survey not as a broad inventory of memory mechanisms, but as a focused bridge from current GUI-agent practice to a more reusable and revisable experience layer.

---

## 2. Introduction

### 2.1 Why This Problem Matters

**Core claim**: GUI agents still struggle in dynamic, long-horizon, and interface-specific tasks because much of the needed knowledge is not available as model prior and must be acquired from interaction.

**Paragraph targets**:

- 先交代 GUI 是现实任务自动化的关键接口。
- 再指出单靠更强 backbone 或更长 context 不能替代经验积累。
- 最后收束到“真正缺的不是 generic skill，而是 experience-dependent procedural knowledge”。

**Evidence anchors**:

- GUI survey / AppAgent / MobileGPT / MobileAgentV3.5
- `gap-tracker.md` 中 A-1、A-4 的 primary evidence

### 2.2 Scope and Boundary

**This survey is about**:

- LLM-based GUI agents
- externalized or operationalized experience reuse
- post-task to cross-task knowledge accumulation

**This survey is not mainly about**:

- 纯训练阶段自进化
- generic prompt engineering
- 单次任务内短期压缩 alone
- 非 GUI 的纯文本 agent unless used as transferable precedent

**Boundary sentence to reuse**:

> We distinguish reusable experience-dependent procedural knowledge from generic GUI priors already likely encoded in the base model.

### 2.3 Research Question

直接放当前主线 RQ 的精简版：

> **RQ**: How can LLM-based GUI agents represent interaction-derived, experience-dependent procedural knowledge as retrievable, revisable, and cross-task reusable memory, and improve it through failure-aware write-back from post-task experience?

### 2.4 Contributions of This Survey

1. 提出一个可操作的 taxonomy，而不是把 memory / self-improvement / GUI skill 混成一类。
2. 用 occupancy + counter-evidence 检验定位真正有价值的空白格子。
3. 把 A-1 与 A-4 收束为主线，把 A-2 与 A-3 明确降为支撑线与扩展线。
4. 为后续 methodology section 提供 design-choice-ready 的问题定义。

---

## 3. Background and Problem Formulation

### 3.1 Three Source Threads

本节先用 3 个小节交代三个来源，但不要写成三篇综述摘要：

#### 3.1.1 GUI Agents

要点：

- GUI understanding, planning, acting 是当前系统的主体能力
- 已有系统多依赖 app-specific docs、workflow hints、hierarchical action traces
- 代表系统：AppAgent, MobileGPT, MobileAgent-v2, MAGNET, ActionEngine, IntentCUA

#### 3.1.2 Agent Memory

要点：

- memory 不是单一概念，应区分 procedural / episodic / semantic / user-centric
- 文本域已证明外部 memory、retrieval、reflection、virtual context management 的技术可行性
- 代表系统：Generative Agents, MemGPT, A-MEM

#### 3.1.3 Self-Evolving Agents

要点：

- failure-driven experience extraction、workflow induction、memory evolution 已在文本/Web 环境有成熟 precedent
- 这些工作说明“从经验中学习”可行，但尚未完成 GUI grounded adaptation
- 代表系统：AWM, ExpeL, SkillRL, AgentKB

### 3.2 Key Definitions

本节建议给出 4 个操作化定义：

1. **Experience-dependent procedural knowledge**
2. **Memory unit**
3. **Write-back**
4. **Cross-task reuse**

建议定义句：

> A memory unit is not a raw action trace, but a structured procedural rule with trigger, procedure, constraint, failure signal, revision cue, and scope.

### 3.3 Common Confusions to Eliminate

**Confusion 1**: workflow cache != procedural memory  
**Confusion 2**: context compression != cross-session episodic memory  
**Confusion 3**: stronger training pipeline != deployment-stage write-back  
**Confusion 4**: user profile concept != validated user-centric memory mechanism

---

## 4. Taxonomy

### 4.1 Dimension I: What Is Learned

沿用 [taxonomy-draft.md](taxonomy-draft.md)：

- Skills
- World
- Episodes
- User

**写法要求**：

- 每类都给“为什么值得存”
- 每类都给“与 base-model prior 的边界”
- 每类都给一个 GUI 例子

### 4.2 Dimension II: When Is Experience Written Back

- pre-task
- in-task
- post-task
- cross-task

**本综述的立场**：

> The main bottleneck is not whether learning happens at all, but whether `post-task` experience can be consolidated into `cross-task` reusable memory.

### 4.3 Dimension III: How Is Experience Reused

#### 4.3.1 Match Operator

- exact match
- similarity retrieval
- rule generalization

#### 4.3.2 Application Carrier

- context injection
- external tool call
- policy constraint
- memory rewrite

**必须明确写的一句**：

> We separate matching from application because prior taxonomies often conflate how experience is found with how it is enforced.

### 4.4 ME/CE Result

这一小节直接吸收 `taxonomy-draft.md` 的正式结论：

- `What` 与 `When` 在 memory-unit level 上可用
- 旧版 `How` 混层，不应再使用
- `Match Operator × Application Carrier` 是后续 gap 分析的正式描述语言

### 4.5 Occupancy Summary

本节结尾直接收束到三个结论：

1. `post-task / Skills / similarity retrieval × context injection` 已有弱占位
2. `post-task / Skills / rule generalization` 仍稀缺
3. `cross-task / Skills` 与 `memory rewrite` 仍是主线空白

---

## 5. Related Work Through the Taxonomy

> **写作顺序建议**：先完成这一节，因为它最接近 Stage 1 已有证据。

### 5.1 Pre-Task Exploration and App-Bound Knowledge

**Representative systems**:

- AppAgent
- MobileGPT
- AutoDroid

**Section claim**:

> Early GUI memory mostly serves environment familiarization and app-specific task decomposition, rather than reusable procedural abstraction.

### 5.2 In-Task Reflection, Compression, and Local Repair

**Representative systems**:

- MobileAgent-v2
- MobileAgentV3.5
- M2

**Section claim**:

> Many recent systems improve execution through in-task reflection or context compression, but these mechanisms rarely survive beyond the current run as revisable long-term memory.

### 5.3 Post-Task Workflow Memory as the Current Best GUI-Side Partial Solution

**Representative systems**:

- MAGNET
- ActionEngine
- IntentCUA

**Section claim**:

> GUI agents have begun to externalize workflow-level experience, but current memory is still largely app- or site-bound, success-dominated, and weak in rule abstraction.

### 5.4 Transferable Precedents from Memory and Self-Evolving Agents

**Representative systems**:

- Generative Agents
- MemGPT
- AWM
- ExpeL
- SkillRL
- A-MEM
- AgentKB

**Section claim**:

> The strongest building blocks for GUI experience reuse currently come from adjacent fields rather than from GUI-native systems.

### 5.5 User-Centric Personalization as a Peripheral but Confirmed Line

**Representative systems**:

- Friday / OS-Copilot
- Persona2Web

**Section claim**:

> Personalization is no longer a speculative direction, but current GUI systems still lack a validated user-centric memory loop.

---

## 6. Gap Analysis

### 6.1 Main Gap A-1: Procedural Memory for GUI

**One-sentence statement**:

> Current GUI agents still lack a reusable procedural memory that can transform post-task experience into cross-task applicable rules.

**What to cover**:

- 现有 partial solutions 到了哪里
- 为什么它们还不等于主线要求的 procedural memory
- 为什么 AWM / SkillWeaver 等是可迁移 precedent

**Must cite from**:

- `gap-tracker.md` A-1
- MAGNET / MobileGPT / ActionEngine / IntentCUA notes

### 6.2 Main Gap A-4: Failure-Driven Write-Back

**One-sentence statement**:

> Current GUI agents may accumulate successful traces or benefit from stronger training flywheels, yet they still lack a deployment-stage mechanism that rewrites memory based on failure.

**What to cover**:

- success-only accumulation 的上限
- training-stage self-evolution 与 deployment-stage write-back 的差异
- AWM / ExpeL / SkillRL / A-MEM 为何重要但仍未完成 GUI 迁移

**Must cite from**:

- `gap-tracker.md` A-4
- MobileAgent-v2 / MAGNET / MobileAgentV3.5 / EvoCUA notes

### 6.3 Supporting Gap A-2: Episodic Memory for GUI

**Positioning sentence**:

> Episodic memory is best treated as supporting infrastructure for retrieval and evaluation, rather than the central object of the current main line.

### 6.4 Extension Gap A-3: User-Centric Memory

**Positioning sentence**:

> User-centric memory is a high-value extension line, but it currently sits outside the most feasible and best-evidenced main contribution path.

### 6.5 Why These Gaps Matter More Than Other Blanks

本小节只做一件事：解释为什么不是所有空白格子都值得做。

可直接复用的判断框架：

- 技术上可行
- 已有相邻领域 precedent
- 与 current RQ 直接对齐
- 能在有限 benchmark 上验证

---

## 7. Methodology Agenda for Stage 3

> **注意**：这节不是正式提出完整方法，而是把 survey 自然收束到“哪些 design choices 已经被文献和 gap 推出来了”。

### 7.1 What Should Be Stored

主张：

- 不存 raw trace
- 不存 generic GUI prior
- 存带条件、失败信号、可修订 scope 的 procedural rule

### 7.2 How Memory Should Be Retrieved and Applied

主张：

- 至少要比较 `raw retrieval` vs `coarse workflow memory` vs `fine-grained delta procedural memory`
- application carrier 不能只停留在 context injection

### 7.3 Why Failure Must Trigger Memory Revision

主张：

- 没有 write-back 的 memory 最终只会变成 success case cache
- rewrite / split / downweight / edit 是方法选择，不是实现细节

### 7.4 Minimum Evaluation Package

直接沿用 [main-line.md](main-line.md)：

- no memory
- raw trajectory retrieval
- success-only memory
- failure-aware memory update
- coarse workflow memory
- fine-grained delta procedural memory

并在 3 个迁移边界上验证：

- repeated task
- same-app transfer
- near-domain app-family transfer

---

## 8. Discussion

### 8.1 What Would Count as Real Memory Gain

讨论 3 个审稿人会问的问题：

- 增益是否超出 base-model prior
- 是否只是 cache 命中
- 是否能在失败后被修正

### 8.2 Limits of the Current Survey

需要主动承认：

- A-3 证据仍只有 B 级
- 若干外围系统尚未完整纳入
- 当前主线刻意不以 fully open cross-app generalization 为前提

### 8.3 Outlook

用 1 段话收束：

- Interim Survey 输出的是 `taxonomy + evidence-backed gaps + methodology agenda`
- Stage 3 再把它压成可检验方法

---

## 9. Conclusion Skeleton

可直接续写的 closing paragraph：

> This survey argues that the next bottleneck for LLM-based GUI agents is not simply stronger perception, larger models, or longer context, but a missing experience layer: reusable, revisable procedural knowledge acquired through interaction. By organizing the field through `What / When / How`, we show that current systems have only weakly occupied the post-task memory region, while cross-task procedural reuse and failure-driven write-back remain underdeveloped. This framing narrows the research agenda from broad memory rhetoric to a more testable target: experience-dependent procedural memory for GUI agents.

---

## 10. Section-Level Evidence Map

> **规则**：凡是准备写进正文的 claim，证据强度至少达到 B；A-1 / A-4 主张优先使用 A 级。


| Section          | Claim                                                                            | Evidence Source                              | Current Strength | Status             |
| ---------------- | -------------------------------------------------------------------------------- | -------------------------------------------- | ---------------- | ------------------ |
| Introduction     | GUI agents still need interaction-derived knowledge beyond base-model priors     | AppAgent / MobileGPT / MobileAgentV3.5 / A-1 | A                | Ready              |
| Introduction     | The real bottleneck is reusable procedural experience rather than generic memory | `main-line.md` + A-1 + taxonomy occupancy    | A                | Ready              |
| Taxonomy         | `How` must be split into match vs application                                    | `taxonomy-draft.md` §2                       | A                | Ready              |
| Related Work 5.1 | Early GUI memory is mainly app-bound exploration support                         | AppAgent / MobileGPT / comparison matrix     | A-B              | Ready              |
| Related Work 5.2 | In-task reflection rarely becomes revisable long-term memory                     | MobileAgent-v2 / MobileAgentV3.5 / M2        | A-B              | Ready              |
| Related Work 5.3 | Current best GUI-side memory remains workflow-level and weak in rule abstraction | MAGNET / ActionEngine / IntentCUA / A-1      | A                | Ready              |
| Related Work 5.4 | Adjacent fields provide the strongest precedents for reusable experience         | AWM / ExpeL / MemGPT / A-MEM / AgentKB       | A                | Ready              |
| Gap 6.1          | GUI agents lack cross-task reusable procedural memory                            | A-1                                          | A                | Ready              |
| Gap 6.2          | GUI agents lack failure-driven write-back at deployment time                     | A-4                                          | A                | Ready              |
| Gap 6.3          | Episodic memory is supporting infrastructure, not current core object            | A-2 + `main-line.md`                         | A                | Ready              |
| Gap 6.4          | User-centric memory is confirmed but still peripheral                            | A-3                                          | B                | Ready with caution |
| Methodology      | Memory unit should be a revisable procedural rule, not a raw trace               | `main-line.md` + A-1 + A-4                   | A-B              | Ready              |
| Evaluation       | Success-only memory is insufficient; failure-aware update must be tested         | `main-line.md` + A-4                         | A                | Ready              |


---

## 11. Writing Queue

### Priority 1: Can be written now

1. Section 5 `Related Work Through the Taxonomy`
2. Section 6 `Gap Analysis`
3. Section 4 `Taxonomy`

### Priority 2: Write after related-work text stabilizes

1. Section 2 `Introduction`
2. Section 7 `Methodology Agenda`
3. Section 8 `Discussion`

### Priority 3: Final pass

1. Abstract
2. Conclusion
3. Reference normalization

---

## 12. Fill-In Checklist

- 每个 section 开头先写 topic sentence，不要先堆 citation
- 每个核心 claim 都能回指到 `gap-tracker.md` 或 `comparison-matrix.md`
- A-1 / A-4 段落都包含 counter-evidence check
- 至少一处明确解释“为什么不是 generic model prior”
- 至少一处明确解释“为什么不是 workflow cache”
- Methodology 节避免写成完整 proposal，只写 design agenda
- A-3 相关表述保持 B-level 语气，不写成已解决问题

