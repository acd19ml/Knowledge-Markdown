# Stage 3 Precedent Synthesis

> **Status**: Supporting draft
> **Purpose**: 从已精读文章列表中筛选真正影响 Stage 3 design-choice 判断的前驱集合，而不是只围绕 AWM 与 SkillWeaver 下结论
> **Primary Inputs**: [2024_MobileGPT.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2024_MobileGPT.md), [2025_MAGNET.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2025_MAGNET.md), [2024_AWM.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2024_AWM.md), [2025_SkillWeaver.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2025_SkillWeaver.md), [2026_ActionEngine.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2026_ActionEngine.md), [2026_EvoCUA.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2026_EvoCUA.md), [2026_MobileAgentV3_5.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2026_MobileAgentV3_5.md)
> **Formal Output**: [nearest-work-delta.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/formal/nearest-work-delta.md)
> **Note**: 本页是筛选与论证页，不是最终引用版本。

---

## 1. Screening Principle

当前目的不是证明 “AWM + SkillWeaver 足够重要”，而是回答更严格的问题：

> 从已完成 Pass 2 的精读文章中，哪些论文**真的会改变** Stage 3 对 `memory unit / application carrier / write-back / governance / alternative route` 的判断？

筛选标准不是论文名气，也不是是否“相关”，而是是否满足以下任一条件：

1. 它直接给出当前方法的候选 design choice。
2. 它构成当前方法最强的邻近替代路线，必须正面对照。
3. 它提供反证，说明某类 design choice 其实不该继承。

---

## 2. Screened Precedent Set

### Tier A: Must-Use Precedents

这些论文会直接改变当前方法如何定义自身，不看就不能稳定下结论。

| Paper | Why it survives screening | What it controls |
|---|---|---|
| [2024_MobileGPT.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2024_MobileGPT.md) | GUI 侧最早、最强的 app-bound hierarchical procedural memory | `memory unit` 的 GUI 本地化边界 |
| [2025_MAGNET.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2025_MAGNET.md) | 当前 GUI memory 路线最强 partial solution | `workflow memory + success-driven evolution` 的上限 |
| [2024_AWM.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2024_AWM.md) | 抽象 workflow 与 online update 的强 precedent，且有较完整 ablation | `experience -> abstraction -> reuse` 是否成立 |
| [2025_SkillWeaver.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2025_SkillWeaver.md) | 把 `selection / verification / governance` 问题显式化 | `governance` 是否必须单列 |
| [2026_ActionEngine.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2026_ActionEngine.md) | 提供 structural memory / programmatic planning 的强替代路线 | 证明当前方法不是 structural prior |

### Tier B: Must-Check Alternative Routes

这些论文不直接给出你的 memory design，但会决定“为什么不走训练期演化或 native route”。

| Paper | Why it survives screening | What it controls |
|---|---|---|
| [2026_EvoCUA.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2026_EvoCUA.md) | 训练期 self-evolution 的强工程路线 | `training-time evolution vs deployment-time memory` |
| [2026_MobileAgentV3_5.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2026_MobileAgentV3_5.md) | native multi-platform GUI model 的能力上限 | `stronger backbone 是否能替代 external memory` |

### Tier C: Useful but Non-Blocking for This Stage

这些论文对主线有价值，但不会实质改变当前 Stage 3 的 design-choice 结论，因此不应抢占前驱 synthesis 的中心位置。

| Paper | Why it is not co-primary now |
|---|---|
| Reflexion / ExpeL | failure-learning 思想重要，但离 GUI-grounded procedural memory 还有桥接距离 |
| AgentKB / SkillRL | 证明 transferable experience 可能成立，但不直接回答 GUI-grounded local rule |
| MemGPT / Generative Agents | 对 A-2 episodic memory 更关键，不是当前 A-1/A-4 主线的最直接 precedent |

---

## 3. Why Not “Just AWM + SkillWeaver”

原来的判断过于简化，因为它默认：

- AWM 负责 abstraction loop
- SkillWeaver 负责 governance

但这会漏掉三类关键约束：

1. **漏掉 GUI 侧已有最强前驱**
   [2024_MobileGPT.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2024_MobileGPT.md) 已经说明 hierarchical procedural memory 在 GUI 中并非空白；如果不把它拉进来，就会高估 AWM 的直接可移植性。
2. **漏掉当前最强 partial solution**
   [2025_MAGNET.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2025_MAGNET.md) 已经把 GUI procedural memory + dynamic evolution 做到系统级；如果不把它放进中心，就无法准确界定当前 novelty 还剩多少。
3. **漏掉最强替代路线**
   [2026_ActionEngine.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2026_ActionEngine.md)、[2026_EvoCUA.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2026_EvoCUA.md)、[2026_MobileAgentV3_5.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2026_MobileAgentV3_5.md) 分别代表 structural memory、training-time evolution、native model scaling。如果不放进判断，当前方法的边界会显得不牢。

因此，AWM 与 SkillWeaver 仍然重要，但它们只能是 **screened set 里的两篇核心论文**，不能再被写成“唯一 blueprint”。

---

## 4. Design-Choice Validation Matrix

| Design axis | Closest positive precedent | Strongest counter-pressure | Current judgment |
|---|---|---|---|
| `Memory Unit` | MobileGPT, AWM, MAGNET | ActionEngine, SkillWeaver | 不该是 raw trajectory、whole-workflow、API skill 或 graph state；应收敛到 GUI-grounded local procedural rule |
| `Application Carrier` | AWM, SkillWeaver | MobileGPT, ActionEngine | 不能只有 retrieval + prompt stuffing；至少要把 retrieval 与 application 分离 |
| `Write-Back Logic` | AWM, MAGNET | EvoCUA, MobileAgent-v3.5 | success-only accumulation 已被部分验证，但不足；failure-aware revision 仍是核心未解 |
| `Governance` | SkillWeaver | MAGNET, MobileGPT | append-only memory 不够，至少需要 selection / verification / revision 视角 |
| `Alternative explanation` | EvoCUA, MobileAgent-v3.5 | — | 必须显式说明为什么不是“更强训练 / 更大 backbone 就够了” |

---

## 5. Paper-by-Paper Judgment

### 5.1 MobileGPT

保留为 co-primary precedent。

原因：

- 它已经证明 `task / sub-task / action` hierarchy 能在 GUI 中形成稳定 warm-start reuse。
- 它直接约束当前方法不能把 novelty 写成“GUI 里还没人做 procedural memory”。
- 它同时告诉你边界仍停在 `per-app / per-device`，并且 failure learning 依赖 HITL。

结论：

> MobileGPT 不是当前方法的终点，但它是 `GUI-grounded procedural memory` 的最重要起点之一。

### 5.2 MAGNET

保留为 co-primary precedent。

原因：

- 它是 GUI 侧目前最强的 memory partial solution。
- 它已经做到了 `procedural memory + dynamic evolution`，因此会直接压缩当前 novelty 空间。
- 它的 author-stated limitation 恰好说明：当前 evolution 仍依赖成功轨迹，failure-aware rewrite 仍未解决。

结论：

> MAGNET 应作为“当前最强 GUI memory baseline”，而不是外围 related work。

### 5.3 AWM

保留为 co-primary precedent，但定位要收紧。

原因：

- 它对 `abstraction over raw trajectory`、`online update mindset`、`transfer-oriented evaluation` 的支持最强。
- 但它仍是文本 web、whole-workflow 粒度，不应被误写成 GUI local rule 的现成答案。

结论：

> AWM 提供的是 abstraction loop precedent，不是最终 memory unit blueprint。

### 5.4 SkillWeaver

保留为 co-primary precedent，但只在 governance 轴上成立。

原因：

- 它清楚提出了 `selection / verification / exploration-to-execution gap`。
- 但其关键 design choices 缺乏严格模块级 ablation，不能被直接视为“已验证的最佳做法”。
- 它的 API skill representation 与当前目标对象不同。

结论：

> SkillWeaver 更像治理问题提出者，而不是可直接继承的主 blueprint。

### 5.5 ActionEngine

保留为重要 contrastive precedent。

原因：

- 它说明强 GUI memory 也可以走 `state-machine graph + program synthesis` 路线。
- 如果不把它纳入，当前方法就很难说清“为什么自己不是 structural memory”。

结论：

> ActionEngine 不是当前方法要继承的主线，但它是必须显式排除的最强替代解释之一。

### 5.6 EvoCUA / Mobile-Agent-v3.5

保留为 alternative-route precedents。

原因：

- 二者都把“更强训练、更大 backbone、更大经验循环”推到了高位。
- 它们告诉你：如果当前方法不能证明 inference-time external memory 的独立价值，就会被解释成“只要继续训练就好”。

结论：

> 这两篇不是 memory design precedent，而是 novelty defense 必须处理的竞争路线。

---

## 6. Revised Conclusion

更稳的结论不是：

> AWM + SkillWeaver 是当前方法的两个 blueprint。

而是：

> 从已精读文章列表筛选后，当前方法的前驱集合至少应包含 MobileGPT、MAGNET、AWM、SkillWeaver、ActionEngine，并用 EvoCUA / Mobile-Agent-v3.5 作为替代路线压力测试。只有在这个 screened set 下，Stage 3 才能稳妥地判断：当前方法既不是 app-bound memory、不是 coarse workflow cache、不是 API skill library、不是 structural graph memory，也不是 training-time evolution 的翻版，而是在回答更窄的 `GUI-grounded, failure-aware, deployment-time procedural rule revision`。

---

## 7. Completion Judgment

针对 [KB-Expansion-Guide.md](/Users/mac/studyspace/Knowledge-Markdown/KB-Expansion-Guide.md) 里的这一项：

> 已精读目标方法论的直接前驱论文（如 AWM + SkillWeaver），能描述其设计选择

当前判断应升级为：

- **精读状态**：已满足，且不止 AWM 与 SkillWeaver，而是已有一组足以支撑 Stage 3 的 screened precedent set
- **设计选择描述**：部分满足，已经能描述关键 design axes，但还需要把 `why not these alternatives` 压成更正式的 nearest-work delta prose
- **下一步最值当**：把本文件的 screened set 收回 [method-brief.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/design/method-brief.md) 的 `Nearest-Work Delta`，避免后续又滑回“只讲两篇论文”的表述
