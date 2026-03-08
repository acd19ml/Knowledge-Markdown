# Stage 3 Nearest-Work Delta

> **Status**: Final v1.0
> **Role**: Stage 3 的唯一正式最近邻差异页
> **Source Drafts**: [precedent-synthesis.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/readiness/precedent-synthesis.md), [method-brief.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/design/method-brief.md)

---

## 1. Positioning Rule

当前方法不允许再用 “AWM + SkillWeaver 的 GUI 版” 这种宽泛说法自我定位。

正式定位必须同时回答三类问题：

1. 最近的正向 precedent 是谁
2. 最强的替代解释是谁
3. 当前方法到底在哪个 design axis 上发生了收缩或偏转

---

## 2. Co-Primary Precedents

| Work | It already established | What it still does not answer | EDPM delta |
|---|---|---|---|
| `MobileGPT` | GUI 场景中的 per-app hierarchical memory 与 warm-start reuse | 没有 cross-app/site transfer；failure repair 依赖 HITL | EDPM 把对象从 per-app memory graph 收缩成 post-task local rule，并把 write-back 自动化 |
| `MAGNET` | GUI procedural memory + dynamic evolution；是当前最强 GUI memory partial solution | 主要依赖成功轨迹；memory unit 仍偏 workflow-level | EDPM 从 success-driven workflow memory 进一步推进到 failure-aware local rule revision |
| `AWM` | `experience -> abstraction -> reuse` 闭环；online update mindset；三层 transfer 评测 | 仍是文本/web + workflow 粒度，不是 GUI-grounded local rule | EDPM 继承 abstraction loop，但继续收缩 unit 粒度 |
| `SkillWeaver` | skill selection、precondition filtering、verification / honing 问题显式化 | 主对象是 per-website API skill；关键 design choices 缺少模块级 ablation | EDPM 借 governance 视角，不把 API skill 当主 object |

---

## 3. Contrastive Precedent

| Work | Why it matters | Why EDPM is not this route |
|---|---|---|
| `ActionEngine` | 它证明强 web agent memory 也可以走 structural state-machine + program synthesis 路线 | EDPM 关注的是 post-task revisable procedural rule，不是 site topology / graph program memory |

---

## 4. Alternative Explanations That Must Be Excluded

| Alternative route | Strong claim from that route | Why it is not enough for the current RQ |
|---|---|---|
| `EvoCUA` | 更强 training-time self-evolution 可以吸收 failure 并持续提升 | 这回答的是训练期策略更新，不是 deployment-time external memory revision |
| `MobileAgent-v3.5` | 更强 backbone + RL + in-context memory management 可以显著抬高 GUI 基线 | 这不能替代独立的 post-task write-back loop，也不能说明外部 procedural memory 没有独立价值 |

---

## 5. Write-Back Precedent, But Not Direct Method Blueprint

| Work | Useful part | Why it is not a direct methodological precedent |
|---|---|---|
| `A-MEM` | 证明 memory 不一定只能 append；新证据可以修订旧 memory | 它修订的是 semantic notes 与 links，不是 GUI-grounded procedural rule |

因此 `A-MEM` 应被写成：

- **write-back precedent**
- 不是 **direct methodological precedent**

---

## 6. Design-Axis Delta

| Design axis | Closest old answer | EDPM answer |
|---|---|---|
| `Memory Unit` | app graph / workflow / API skill / semantic note | local procedural rule |
| `Application Carrier` | retrieval + prompt stuffing 或直接 API 调用 | retrieval 与 application 分离，先 `v0` 再 `v1` |
| `Write-Back Logic` | success accumulation 或 training-time update | post-task failure-aware revision |
| `Governance` | implicit 或 API-library centric | rule store with selection, evidence trace, and revision policy |
| `Transfer Claim` | warm-start reuse 或 workflow reuse | non-cache transfer across `L1/L2/L3` |

---

## 7. Formal Novelty Defense

### EDPM is not MobileGPT

- 因为它不是 per-app memory graph
- 因为它不依赖 HITL 作为主要修复机制
- 因为它要求 `L2/L3` transfer，而不只证明 warm-start

### EDPM is not MAGNET

- 因为它不把成功驱动 accumulation 当成终点
- 因为它把 failure-aware revision 放到方法中心
- 因为它把 unit 从 workflow-level 继续收缩

### EDPM is not AWM

- 因为它不是文本 web workflow
- 因为它不是把 abstraction 终止在 reusable workflow
- 因为它要在 GUI-grounded local rule 上做 write-back

### EDPM is not SkillWeaver

- 因为它不把 API function 当主 memory unit
- 因为它关注的是 rule revision，而不仅是 skill construction / calling

### EDPM is not ActionEngine

- 因为它不把 state graph / program synthesis 当主 memory representation

---

## 8. One-Sentence Delta

> EDPM 回答的不是 “怎样做更大的 workflow cache、API skill library、graph memory 或训练期自演化”，而是 “怎样把 GUI 交互中的局部经验差分知识写成可修订 procedural rule，并证明它在 deployment-time 产生非缓存式 transfer gain”。
