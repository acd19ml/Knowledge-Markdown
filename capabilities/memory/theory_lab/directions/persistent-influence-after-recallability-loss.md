# Research Direction

## 可回忆性消失后的持续影响（causal residue）

关联主张：
- [Theory Map](../theory_map.md)

### Goal

研究一段经验在失去显式 `recallability` 之后，如何仍然持续影响后续行为与判断。

### Problem Reframing

目标不是“记住一切”，而是让经验在失去 `recallability` 之后，仍保留对后续判断和行为的持续影响。

### Core Hypothesis

一段经验可能留下两种不同层面的后效：

- 对当前行为持续起作用的 `disposition`
- 在事后被调用时，对其来源进行重建的 `retrospective explanation`

前者可以稳定存在，后者则可能缺失、模糊，或者出现错误归因。

### Requirements

- 当前决策不应依赖对原始 `episode` 的显式 `retrieval`
- 过去经验造成的影响应作为当前倾向的一部分持续存在
- 这种影响必须跨越单次 `context` 持续存在
- 系统可以在事后尝试重建来源，但这种重建不是决策前提
- 事后因果解释可以是不确定的、可错的、可修正的
- 后续经验必须能够强化、削弱或改写已有影响

### Evaluation

评估重点不应只是系统能否找回源头经验，而应同时看两件事：

- 过去经验是否仍在持续影响当前决策
- 系统对这种影响来源的解释是否是不确定、脆弱、可错的

一个更接近这条理论的系统，应该允许“影响仍然存在，但来源解释并不稳定”。

关键判据包括：

- `decision independence`
  - 当前决策不依赖显式调用原始 `episode`

- `behavioral persistence`
  - 经验造成的倾向能够跨越多个后续情境持续存在

- `explanatory fragility`
  - 系统在事后解释来源时可以表现出模糊、不确定、甚至错误归因，而不影响当前倾向本身存在

- `revisability`
  - 后续经验能够强化、削弱或修正已有影响，而不是让早期经验永久固化

### Open Questions

- 什么样的经验值得被视为会留下长期影响的经验
- 如何区分“当前倾向仍在起作用”和“系统仍在隐式调用旧记录”
- 后续经验应如何强化、削弱或改写已有影响，而不是把它简单覆盖
