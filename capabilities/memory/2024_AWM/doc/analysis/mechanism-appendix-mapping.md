# `mechanism-analysis.md` -> Appendix Evidence Mapping

> 目的：
> - 为 [mechanism-analysis.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/mechanism-analysis.md) 中的关键主张建立稳定的 appendix 挂靠关系。
> - 区分哪些结论可以作为 `HARD` 结论进入 final report，哪些只能保留为 `SOFT` / `exploratory` / `working hypothesis`。
> - 本文件不改正文，只提供引用底图。

## 1. 使用规则

- `HARD`：有脚本输出、runbook 主结果、或已回源确认的 case 直接支持。
- `SOFT`：由多个 case 或多处统计共同支持，但不存在单一直接观测变量。
- `exploratory`：有脚本或统计来源，但指标定义较弱、未充分验证。
- `qualitative`：主要来自 workflow 文本或案例阅读，应避免写成普适定律。

## 2. Section-by-Section Mapping

| 正文位置 | 关键主张 | 推荐 appendix | 证据强度 | 当前状态 | 写作约束 |
|---|---|---|---|---|---|
| `§1.3.3 (1)` | `TYPE` 步骤收益最稳定 | `A1` | HARD | 可直接引用 | 保持“最稳定”而非“总是最高收益” |
| `§1.3.3 (2)` | `CLICK` 步骤决定 reproduced / not reproduced 分野 | `A1` | HARD | 可直接引用 | 需保留“高度依赖站点匹配度”限定 |
| `§1.3.3 (3)` | kayak 后半段收益显著更大 | `A1` | HARD | 可直接引用 | 明确是 `kayak especially`，不要泛化到全部 reproduced 站点 |
| `§1.3.3 (4)` | budget 后半段退化更严重 | `A1` | HARD | 可直接引用 | 明确是 budget 强支持、sixflags 仅弱支持 |
| `§2.3.4 (1)` | reproduced 站点 `negative = 0` | `A2` | HARD | 可直接引用 | 限定在当前已审计 C1 设置 |
| `§2.3.4 (2)` | not reproduced 站点 `negative >> positive` | `A2` | HARD | 可直接引用 | 可直接写成 paired-case 事实 |
| `§2.3.4 (3)` | workflow 实际影响面有限 | `A2` | HARD | 可直接引用 | 建议写“影响面有限”，不要写“收益天花板很低” |
| `§2.3.4 (4)` | workflow 只在少量步骤上改变行为 | `A2` | HARD | 可直接引用 | 不要把范围值写死到单一 split |
| `§3.3.2 tripadvisor` | tripadvisor 为 A+B 混合退化 | `A3`, `B6` | HARD | 可直接引用 | 可同时挂汇总表和一个负例 |
| `§3.3.2 reddit` | reddit 主要是 workflow-content mismatch | `A3` | HARD | 可直接引用 | 保留“主要”而不是“唯一” |
| `§3.3.3` | distribution gap 增大时 online AWM 可能产生负迁移 | `A3` | HARD | 可直接引用 | 限定为“当前首轮 cross-site 结果” |
| `§3` 补充段 / final report trade-off note | `offline_wf` 更稳但受 train-test gap 拖累；`online_wf` 更贴近 test distribution，但更易固化 trajectory-shaped errors | `A7` | SOFT + source-driven | 可保留 | 只能写 trade-off / mechanism contrast，不能写成跨设置的严格优劣定律 |
| final report small-data note | online memory 在 very small budget 下的早期收益是否出现 | `A8` | SOFT + source-driven | 可保留 | 只能写 source-style early gain，不可扩成 benchmark-wide efficiency claim |
| `§4.3.1-4.3.3` | LM workflow 文本上更抽象、更短、更少、更少具体值 | `C1`, `C2`, `C3` | HARD | 可直接引用 | 文本层结论可写强；不要自动推出性能优势 |
| `§4.3.4` | 抽象性不自动等于性能优势 | `C1`, `A3` | HARD + SOFT | 可直接引用 | 对 `newegg` 只能写 `mixed/unclear` |
| `§5.2.1` | `code_wf` 与 `text_wf` 差异不大（kayak） | `A4` | HARD | 可直接引用 | 限定为 `kayak first run` |
| `§5.2.2-5.2.3` | `NL vs HTML` 三站点首轮整体 `not reproduced` | `A4` | HARD | 可直接引用 | 这是 C4 主结论之一 |
| `§6.2.1` | workflow 库规模较紧凑 | `A5`, `C3` | HARD | 可直接引用 | 计数口径以 runbook/C3 counting rule 为准 |
| `§6.2.2` | function overlap 很低 | `A5` | HARD | 可直接引用 | 数值口径固定为 `0-3.33%` |
| `§6.2.3` | utility/coverage 高，但属于 prompt-level proxy | `A5` | HARD | 可直接引用 | 必须保留 `proxy` 限定 |
| `§7.2` | paired total = `475`，且 failure taxonomy 可追溯 | `A2` | HARD | 可直接引用 | 当前已修正；不要再写 `523` |
| `§8` | 正向机制主要包括值模板、策略重定向、终止控制 | `B1`, `B2` | HARD | 可直接引用 | 用 case-level 证据，不要扩成“所有正例都如此” |
| `§8` | 负向机制主要包括域外误导与模板跳步 | `B4`, `B5`, `B6` | HARD | 可直接引用 | `workflow 优先于推理` 只能写 SOFT |
| `§9.1-9.2` | `P-1/P-2/P-3/N-1/N-2/N-3` 已逐条回源确认 | `B1`, `B2`, `B4`, `B5`, `B6` | HARD | 可直接引用 | 注意 `P-2/P-3` 的 task desc 必须用 eval task，不可回退到 exemplar |
| `§9.3` | 正向核心是正确操作模式，负向核心是不适用操作模式 | `B1`, `B2`, `B4`, `B5`, `B6` | SOFT | 可保留 | 这是跨 case 归纳，不是单一 case 可直接证明 |
| `§10.1` | workflow 可复用性、baseline CLICK 空间、task 异质性共同影响成功概率 | `A1`, `C4` | SOFT + qualitative | 可保留 | 必须写成结构化比较后的工作性总结 |
| `§10.2` | alignment rate 与性能不呈简单正相关 | `A6` | exploratory | 可保留 | 必须保留 `exploratory metric` 标签 |
| `§10.3` | AWM 成功依赖 workflow 可复用性 + baseline 提升空间 | `A1`, `C1`, `C4`, `A6` | SOFT / working hypothesis | 可保留 | 只能写 working hypothesis / post-hoc observation |
| final report compositionality note | Mind2Web 上存在扁平子流程复用，但缺少显式层级组合 | `C5` | qualitative | 可保留 | 只能写 flat subflow reuse / partial support，不可写成 strong hierarchical composition |
| `§11.1-11.2 (1)` | LM induction 产出更抽象的 sub-routine | `C1` | HARD | 可直接引用 | 文本层成立，不要自动扩展到全部性能层 |
| `§11.1-11.2 (2)` | 关键变量是 task-workflow 语义匹配度 | `A3`, `B4`, `B6`, `A6` | SOFT + exploratory | 可保留 | 不能升级成单一量化定律 |
| `§11.1-11.2 (3)` | workflow 只在少量步骤上真正改变行为 | `A2` | HARD | 可直接引用 | 范围值写法需和 paired total 口径一致 |
| `§11.1-11.2 (3)` | 模型倾向于遵循 workflow 而非独立推理 | `B4`, `B6` | SOFT | 可保留 | 只能写 `suggests / is consistent with` |
| `§11.1-11.2 (4)` | 正负影响在 trajectory 中累积 | `A1` | HARD | 可直接引用 | 需保留站点差异说明 |
| `§11.1-11.2 (5)` | 最终 Step SR delta 可理解为 positive minus negative 的聚合结果 | `A2` | HARD | 可直接引用 | 这是解释框架，不是严格因果识别 |
| `§11.3` | 论文的“普适有效”应改写成“有条件有效” | `A1`, `A2`, `A3`, `A4`, `A5` | HARD + SOFT | 可直接引用 | 是总结合成，不是单点证据 |

## 3. Claim-Level Safe Citations

以下句型已足够稳，可以在 final report 中直接使用，后面挂 appendix。

1. `AWM’s gains in C1 mainly come from stable TYPE-side value guidance and site-dependent CLICK grounding effects (Appendix A1).`
2. `On reproduced sites, workflow rarely harms the agent; on not-reproduced sites, negative interventions substantially outnumber positive ones (Appendix A2).`
3. `Cross-site degradation is explained more by workflow-content mismatch than by target-site collapse alone, with Tripadvisor showing a mixed failure mode and Reddit showing primarily content mismatch (Appendix A3, B6).`
4. `LM-induced workflows are consistently more abstract than rule-induced workflows at the text level, but this abstractness does not guarantee site-wise superiority in performance (Appendix C1-C3).`
5. `The NL-vs-HTML claim was not reproduced in the three-site first run, while prompt-level code and text workflows behaved similarly on kayak (Appendix A4).`
6. `The C5 quality results support compact workflow libraries with low function overlap, but utility and coverage should be interpreted as prompt-level proxies rather than strict adherence measures (Appendix A5).`
7. `The current Mind2Web evidence suggests an offline-vs-online trade-off rather than a simple ranking: offline workflows are broader and steadier on CLICK-side grounding, while online workflows are more test-proximate and stronger on local TYPE/value guidance, but more vulnerable to trajectory-shaped transfer errors under larger shift (Appendix A7).`
8. `Under the current first-run evidence, online memory shows genuine very-small-budget gains on kayak, but this early-gain pattern does not generalize reliably to tripadvisor or reddit (Appendix A8).`
9. `On Mind2Web, AWM shows signs of subflow reuse mainly as a flat library of reusable routines, not as explicit hierarchical workflow composition (Appendix C5).`

## 4. Claims That Must Stay Soft

这些结论在正文里可以出现，但必须保留限定词。

| 结论 | 推荐限定词 | 推荐 appendix |
|---|---|---|
| workflow 优先于推理 | `suggests`, `is consistent with`, `case-level evidence indicates` | `B4`, `B6` |
| 模板跳步是重要负向机制 | `case-level mechanism`, `illustrated by` | `B5` |
| alignment 越高越差 / 越低越好 | 不可写成规律；只能写 `does not show a positive monotonic relation` | `A6` |
| 67-72% 是成功阈值 | 不可写成阈值；只能写 `post-hoc pattern in first-run evidence` | `A1`, `A6` |
| workflow 可复用性 + baseline 空间是双重条件 | `working hypothesis`, `supported by first-run evidence` | `A1`, `C1`, `C4`, `A6` |

## 5. Remaining Risk Checks Before Final Report

1. 若正文再次引用 `P-2/P-3`，必须核对 task desc 仍然是 eval task，而不是 few-shot exemplar。
2. 若正文再次给出 function overlap 百分比，必须沿用 `A5` 口径，不得回到 `17%`。
3. 若正文再次提到对齐率，必须同时说明：
   - 来源是 `alignment_rate.py`
   - 这是关键词重叠 heuristic
   - `newegg` 是反例，说明它不是单调规律
4. 若正文再次谈 “Rule 更好”，必须同时标注 `c3-runbook: unclear`，不能覆盖主结果判定。
5. 若正文需要一个较精简的 appendix 集合，优先使用：`A1`, `A2`, `A3`, `A6`, `A7`, `A8`, `B4`, `B6`, `C1`, `C5`。
6. 若 final report 要补论文 `§3.2.2` 的 offline-vs-online trade-off 讨论，优先挂 `A7`，不要只复用 `A3` 的 cross-site 结果。
7. 若 final report 要讨论 online memory 的 small-data efficiency，只能挂 `A8`，并明确限定为 first-run Mind2Web evidence。
8. 若 final report 要讨论 compositionality，应优先写成 `flat subflow reuse`，并挂 `C5`，不要直接借用论文在更开放环境中的强组合叙事。

## 6. Minimal Final-Report Appendix Set

若 final report 只能挂少量 appendix，推荐以下 14 个：

- `A1` step-level breakdown
- `A2` paired-case summary
- `A3` cross-site diagnosis
- `A4` C4 result table
- `A5` C5 quality table
- `A6` alignment-rate note
- `A7` offline-vs-online trade-off note
- `A8` online small-data efficiency note
- `B2` united positive case
- `B4` sixflags negative case
- `B6` tripadvisor cross-site negative case
- `C1` LM-vs-rule text evidence
- `C4` site-feature qualitative coding
- `C5` Mind2Web compositionality reading

这组 appendix 已经足够支撑 `mechanism-analysis.md` 中绝大多数关键结论，包括 `§10` 的 qualitative site-feature 判断。
