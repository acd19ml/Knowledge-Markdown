# Claim-to-Source Evidence Index

> **Status**: Final v1.0
> **Role**: 把 Interim 和 Stage 3 的核心论断显式挂回 paper notes
> **Parent Docs**: [interim-survey-draft.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/interim-survey-draft.md), [interim-summary.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/interim-summary.md)

---

## 1. Usage Rule

本页不替代 survey 正文，也不替代单篇 paper note。

它的作用只有一个：

> 当你说 “这个 gap / 这个 method choice / 这个 nearest-work judgment 有原文支撑” 时，快速指出证据来自哪几篇笔记、笔记中的哪类证据块、以及它在 Stage 3 决策中被用来支持什么。

---

## 2. Core Claims

| Claim ID | Core claim | Source note(s) | Note evidence block(s) | Used for |
|---|---|---|---|---|
| `C1` | GUI agent 的下一瓶颈不是 generic memory，而是 interaction-derived procedural knowledge | [2024_MobileGPT.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2024_MobileGPT.md), [2025_MAGNET.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2025_MAGNET.md), [2026_ActionEngine.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2026_ActionEngine.md) | `Core Method`, `Limitations`, `Gap Signals`, `Reusable Elements` | survey introduction; final problem framing |
| `C2` | app-bound memory / workflow memory / structural memory 都是部分解，不是最终对象 | [2024_MobileGPT.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2024_MobileGPT.md), [2025_MAGNET.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2025_MAGNET.md), [2026_ActionEngine.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2026_ActionEngine.md), [2025_SkillWeaver.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2025_SkillWeaver.md) | `Key Design Choices`, `Limitations`, `Relation to My Research` | `A-1` gap; nearest-work delta |
| `C3` | 经验应被抽象，而不该只做 raw trajectory replay | [2024_AWM.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2024_AWM.md), [2025_MAGNET.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2025_MAGNET.md) | `Core Method`, `Key Design Choices`, `Key Results` | memory unit choice; `H1` |
| `C4` | workflow 粒度仍偏粗，GUI 场景需要更小的 local rule unit | [2024_AWM.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2024_AWM.md), [2025_MAGNET.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2025_MAGNET.md), [2024_MobileGPT.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2024_MobileGPT.md) | `Limitations`, `Gap Signals`, `My observed limitations` | EDPM object definition |
| `C5` | retrieval 和 application 应拆开，不应只做 prompt stuffing | [2025_SkillWeaver.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2025_SkillWeaver.md), [2025_MAGNET.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2025_MAGNET.md) | `Core Method`, `Failure cases`, `Gap Signals`, `Reusable Elements` | `H2`; application carrier design |
| `C6` | failure 不是 runtime incident，而应进入 memory revision | [2024_AWM.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2024_AWM.md), [2025_SkillWeaver.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2025_SkillWeaver.md), [2025_AMem.md](/Users/mac/studyspace/Knowledge-Markdown/Agent_Memory/papers/notes/2025_AMem.md), [2026_SkillRL.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2026_SkillRL.md) | `Gap Signals`, `Limitations`, `Reusable Elements`, `Key Passages` | `A-4` gap; write-back policy |
| `C7` | memory 不一定只能 append，新证据可以修订旧 memory | [2025_AMem.md](/Users/mac/studyspace/Knowledge-Markdown/Agent_Memory/papers/notes/2025_AMem.md), [2024_ExpeL.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2024_ExpeL.md) | `Core Method`, `Gap Signals`, `Reusable Elements` | defend revisability; justify `edit / split / downweight / rewrite` |
| `C8` | training-time evolution 不能替代 deployment-time external memory revision | [2026_EvoCUA.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2026_EvoCUA.md), [2026_MobileAgentV3_5.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2026_MobileAgentV3_5.md) | `Core Method`, `Relation to My Research`, `Gap Signals` | alternative-explanation exclusion |
| `C9` | 当前最可信的实验边界是 repeated-task / same-site or same-app cross-task / near-domain site-family or app-family transfer | [2024_AWM.md](/Users/mac/studyspace/Knowledge-Markdown/Self_Evolve/papers/notes/2024_AWM.md), [2024_MobileGPT.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2024_MobileGPT.md), [2025_MAGNET.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2025_MAGNET.md) | `Experimental design`, `Key Results`, `Gap Signals` | evaluation plan; non-cache guardrail |
| `C10` | user-centric memory 已被确认有价值，但仍不应挤占当前主线 | [2024_OS-COPILOT.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2024_OS-COPILOT.md), [2026_Persona2Web.md](/Users/mac/studyspace/Knowledge-Markdown/GUI_Agent/papers/notes/2026_Persona2Web.md) | `Problem Setting`, `Key Results`, `Relation to My Research` | keep `A-3` as extension line |

---

## 3. Claim Bundles for Stage 3 Decisions

### Final RQ Bundle

用于支持最终 RQ 的最小证据组合：

- `C1`
- `C3`
- `C6`
- `C9`

这些共同支撑：

- 为什么问题对象是 procedural knowledge
- 为什么 memory 必须可修订
- 为什么评测必须跨 `L1/L2/L3`

### Method Object Bundle

用于支持 EDPM object 的最小证据组合：

- `C2`
- `C3`
- `C4`
- `C5`

这些共同支撑：

- 为什么不是 raw trajectory
- 为什么不是 workflow cache
- 为什么不是 API skill library
- 为什么 application 不能等同 retrieval

### Novelty Defense Bundle

用于支持 nearest-work delta 的最小证据组合：

- `C2`
- `C6`
- `C8`

这些共同支撑：

- 为什么不是 MobileGPT / MAGNET / ActionEngine 的延伸线
- 为什么不是 training-time evolution 的换皮

---

## 4. How To Cite This in Interim

若在 Interim 口头汇报或书面总结中需要快速回指，可用下面模板：

```text
Claim: GUI agents still lack revisable cross-task procedural memory.
Evidence: MobileGPT / MAGNET / ActionEngine notes + AWM precedent note.
Decision use: supports A-1 and the EDPM memory-unit choice.
```

---

## 5. Current Gaps in the Evidence Index

这份索引已经足够支撑 Interim，但仍有两个后续可补项：

1. 给每条 claim 补 note 内更精确的 section anchors 或 quote anchors。
2. 把 `C10` 的 user-memory supporting notes再做一次统一格式检查，确保和 Stage 2 survey 的 B-level 语言一致。
