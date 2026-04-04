# Reproduction Status: AWM 复现总状态表

> 本文档用于汇总 AWM 各阶段复现状态。
> 它面向研究推进，而不是运行细节；具体命令和过程分别见各阶段 runbook。

---

## 1. 总览

| stage | claim | status | current judgment | reference |
|------|------|------|------|------|
| `C1` | offline AWM 在 `cross-task` 上优于 baseline | 首轮已完成 | mixed; stability insufficient | [c1-runbook.md](../runbook/c1-runbook.md) |
| `C2` | online AWM 在更大 distribution gap 下更稳、更优 | 首轮已完成 | mixed; overall direction not reproduced | [c2-summary.md](../runbook/c2-summary.md) |
| `C3` | LM induction vs rule induction | 首轮已完成 | mixed; explanatory signal supported, one site reproduced | [c3-runbook.md](../runbook/c3-runbook.md) |
| `C4` | workflow 表示层/构成消融 | 首轮已完成 | code/text reproduced on first run; NL/HTML not reproduced after three-site first run | [c4-runbook.md](../runbook/c4-runbook.md) |
| `C5` | workflow quality 与性能关系 | 首轮已完成 | reproduced under current approximation; utility proxy remains loose | [c5-runbook.md](../runbook/c5-runbook.md) |

---

## 2. 当前结论

截至目前，C1-C5 全部完成首轮复现：

- `C1`：证据混合，暂不记为整体 `reproduced`（7 站点中 2 个 reproduced, 2 个 not reproduced, 3 个 unclear）
- `C2`：整体方向偏向 `not reproduced`（仅 test_task/kayak 成功，cross-site 均退化）
- `C3`：LM vs Rule 的解释性结论成立（文本层面 4/4 指标支持），但性能优势为 mixed
- `C4`：code vs text“差异不大”在 `kayak` 首轮成立；NL vs HTML 三站点首轮整体 `not reproduced`
- `C5`：在当前近似统计口径下，workflow 库精简、低冗余、高 utility proxy 均得到支持；但 utility proxy 仍比“真实遵循率”宽松

**阶段一总结**：

```text
C1-C5 已全部完成首轮复现。五条核心主张中，得到最强支持的是 C3 的解释性结论（LM workflow 更抽象），以及 C4 的 code/text 差异不大、C5 在当前近似统计口径下所呈现的 workflow 库紧凑与低冗余。得到最弱支持的是 C2 的 cross-site 泛化主张（方向相反）和 C4 的 NL vs HTML 主张（三站点首轮整体不支持）。C1 的核心性能主张稳定性不足。整体而言，AWM 的方法论设计有其合理性（LM 归纳确实更抽象），但性能收益不稳定且高度站点相关，论文呈现的“普适有效”图景在当前复现中未能成立。
```

---

## 3. 层次二三分析状态

阶段二三的机制分析已基于 C1-C5 日志完成，详见 [mechanism-analysis.md](mechanism-analysis.md)。

核心发现：
1. AWM 的收益主要来自 TYPE 步骤的值模板效应，CLICK 步骤高度站点相关
2. reproduced 站点 negative=0（workflow 无害），not reproduced 站点 negative >> positive（workflow 有害）
3. cross-site 退化主因是 workflow 内容不适配（假说 A），辅以 HTML 结构差异（假说 B）
4. 论文未讨论的 7 个关键边界条件已识别

---

## 4. 当前建议

1. C1-C5 首轮结果全部冻结
2. 层次二三的分析已可支撑 final report 的”机制解释”和”边界识别”章节
3. 下一步：进入 final report 撰写

---

## 5. Reporting Boundary

为降低 final report 中的过度声称风险，当前项目采用以下统一边界：

- 本项目的主证据范围限于 **Mind2Web**
- 当前所有 `reproduced / not reproduced` 判断均为 **first-run judgments**
- 论文 `AWM_AS` action-space extension 分支 **未覆盖**
- `alignment rate` 只按 **exploratory heuristic** 使用，不作为强证据

建议 final report 直接复用：
- [scope-and-limitations.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/report/scope-and-limitations.md)
