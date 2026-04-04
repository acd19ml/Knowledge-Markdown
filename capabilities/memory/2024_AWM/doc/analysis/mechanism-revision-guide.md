# `mechanism-analysis.md` Revision Guide

> 目标：
> - 不直接修改 [mechanism-analysis.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/mechanism-analysis.md)；
> - 先明确哪些段落可以原样保留，哪些必须降格，哪些需要换证据挂法或替换例子；
> - 为后续 final report 压缩与正文修订提供操作清单。

## 1. 判定标签

- `保留`：当前正文强度与证据匹配，可原样保留。
- `保留但降格`：方向正确，但必须保留限定词，或删去过强措辞。
- `保留但换挂证据`：正文方向可保留，但应换成更准确的 appendix/来源。
- `建议重写`：当前表述会误导，建议改写句子或改举例方式。
- `建议删除`：当前句子收益低于风险，不建议继续保留。

## 2. Section-by-Section Review

| 位置 | 当前主张/段落 | 判定 | 建议动作 | 推荐证据 |
|---|---|---|---|---|
| `§0` | 数据基础与覆盖范围表 | 保留 | 可原样保留 | runbook + results dirs |
| `§1.3.3 (1)` | `TYPE` 步骤收益最稳定 | 保留 | 原样保留 | `A1` |
| `§1.3.3 (2)` | `CLICK` 步骤是胜负手 | 保留 | 原样保留，但保留“依赖站点匹配度”限定 | `A1` |
| `§1.3.3 (3)` | reproduced 站点后半段收益更大 | 保留但降格 | 建议改成“在 kayak 上尤其明显，newegg/united 方向相符但更弱” | `A1` |
| `§1.3.3 (4)` | not reproduced 站点后半段退化更严重 | 保留但降格 | 建议改成“budget 显著成立，sixflags 仅弱支持” | `A1` |
| `§2.3.4 (1)` | reproduced 站点 `negative = 0` | 保留 | 原样保留 | `A2` |
| `§2.3.4 (2)` | not reproduced 站点 `negative >> positive` | 保留 | 原样保留 | `A2` |
| `§2.3.4 (3)` | ineffective 占比最大，AWM 有效窗口很窄 | 保留但降格 | 用“实际影响面有限”替代“窗口很窄”也可；两者都可，但后者更强 | `A2` |
| `§2.3.4 (4)` | `6-18%` 为 workflow 遵循率粗估 | 保留但降格 | 必须明确这是当前口径下的粗估，不可写成通用遵循率 | `A2` |
| `§3.3.2 tripadvisor` | A+B 混合退化 | 保留 | 原样保留 | `A3`, `B6` |
| `§3.3.2 reddit` | 主要是假说 A | 保留 | 原样保留，但保留“主要” | `A3` |
| `§3.3.3` | distribution gap 增大时 online AWM 可能负迁移 | 保留 | 原样保留，但限定为当前首轮 cross-site 证据 | `A3` |
| `§4.3.1` | LM vs Rule 文本特征量化对比 | 保留但换挂证据 | 正文可保留；引用时应挂 `C1-C3`，并说明这是 workflow text comparison 口径 | `C1`, `C2`, `C3` |
| `§4.3.3` | LM vs Rule 抽象性差异文本层完全成立 | 保留 | 原样保留 | `C1` |
| `§4.3.4` | 抽象性不自动等于性能优势 | 保留 | 原样保留 | `C1`, `A3` |
| `§4.3.4` 中 `newegg` 解释 | 保留但降格 | 保持 `Rule 在配对净收益上有竞争力；runbook 判定 unclear`，不要再写 Rule 更好 | `A3`, `c3-runbook` |
| `§5.2.1` | code vs text 差异不大，但两者均低于 baseline | 保留 | 原样保留；这是 kayak 首轮事实 | `A4` |
| `§5.2.3` | NL vs HTML 三站点整体 not reproduced | 保留 | 原样保留 | `A4` |
| `§5.2.4 (1)` | desc_html 可能导致注意力分散 | 保留但降格 | 改成“与注意力分散解释相一致”更稳 | `A4` |
| `§5.2.4 (2)` | 表示层最优策略是站点相关的 | 保留 | 原样保留 | `A4` |
| `§6.2.2` | utility rate 较高 | 保留但降格 | 必须同时保留“prompt-level proxy, not strict adherence” | `A5` |
| `§6.2.2` | function overlap 较低 | 保留 | 原样保留，数字必须沿用 `0-3.33%` | `A5` |
| `§6.2.3` | workflow 数量本身不是决定因素 | 保留但降格 | 用“首轮结果更支持 content-match 比 raw count 更重要” | `A5`, `A3` |
| `§7.2` | paired total = `475` 与各类占比 | 保留 | 原样保留 | `A2` |
| `§7.3` | 论文未讨论这些 failure mode | 保留 | 原样保留，但避免“论文完全忽略”这类超强措辞 | `A1`, `A2`, `A3` |
| `§8.1 (1)` | “值模板效应（TYPE 步骤）” + 例子 `P-3` | 建议重写 | `P-3` 是 `SELECT` 不是 `TYPE`。建议改成“值/标签格式校正”或换回真正 TYPE case `P-2` | `B2`, `B1` |
| `§8.1 (2)` | 元素定位效应（CLICK） | 保留 | 原样保留 | `A1` |
| `§8.1 (3)` | 策略重定向 | 保留 | 原样保留 | `B2` |
| `§8.1 (4)` | 有效窗口窄但无害 | 保留但降格 | “无害”仅适用于 reproduced 站点；建议写“在匹配站点上净正向且 negative=0” | `A2` |
| `§8.1 (5)` | 后半段辅助效应 | 保留但降格 | 保留站点差异说明 | `A1` |
| `§8.2 (1)` | workflow 在不匹配站点上是有害的 | 保留 | 原样保留，但限定为当前 not-reproduced / cross-site cases | `A2`, `A3` |
| `§8.2 (2)` | 抽象性优势是有条件的 | 保留 | 原样保留 | `C1`, `A3` |
| `§8.2 (3)` | workflow 的有效窗口很窄 | 保留但降格 | 仍建议替换成“实际影响面有限”更稳 | `A2` |
| `§8.2 (4)` | SKIP 步骤影响大 | 保留 | 原样保留 | `A1`, `A3` |
| `§8.2 (5)` | 累积误导效应 | 保留 | 原样保留 | `A1` |
| `§8.2 (6)` | 表示层最优策略站点相关 | 保留 | 原样保留 | `A4` |
| `§8.2 (7)` | workflow 收益天花板很低 | 建议重写 | “天花板很低”过强。建议改成“workflow 对总步骤的实际影响面有限” | `A2` |
| `§8.2 (8)` | 表层对齐率与性能不呈正相关 | 保留但降格 | 必须保留 `exploratory metric` 和 `newegg is an exception` | `A6` |
| `§8.2 (9)` | 成功需要双重条件 | 保留但降格 | 必须保留 `working hypothesis / first-run evidence` | `A1`, `C1`, `C3`, `A6` |
| `§9.1 P-1` | 防止过早终止 | 保留 | 原样保留 | `B1` |
| `§9.1 P-2` | 策略重定向 | 保留 | 原样保留，task desc 必须是 drone eval task | `B2` |
| `§9.1 P-3` | 值格式校正 | 保留 | 原样保留，task desc 必须是 bluetooth mouse eval task | 若需要单独 appendix，后续可补 `B3`; 当前正文可保留 |
| `§9.2 N-1` | 域外 workflow 误导 | 保留 | 原样保留 | 若需正文挂 appendix，可后补 budget case；当前可由 `B4/B6` 支撑同类结论 |
| `§9.2 N-2` | 全域误导 | 保留 | 原样保留 | `B4` |
| `§9.2 N-3` | 模板跳步 | 保留 | 原样保留，但作为 case-level 机制，不宜泛化为全局规律 | `B5` |
| `§9.3` | workflow 优先于推理 | 保留但降格 | 必须写成 `suggests / case-level evidence indicates` | `B4`, `B6` |
| `§10.1` | 四站点结构化对比表 | 保留但换挂证据 | 保留正文，但引用时应区分：`A1` for baseline/click, `C3` for workflow features | `A1`, `C3` |
| `§10.2` | alignment rate 反直觉 | 保留但降格 | 只能写 exploratory，不要写规律 | `A6` |
| `§10.3` | 双重条件成功预测假说 | 保留但降格 | 只能保留为 working hypothesis / post-hoc observation | `A1`, `C1`, `C3`, `A6` |
| `§10.4` | 与 §9 案例的统一解释 | 保留但降格 | 这是 synthesis，不是单一验证结论 | `B1`, `B2`, `B4`, `B5`, `B6` |
| `§11.1` 因果图 | 整体结构图 | 保留但降格 | 图可保留；图中 `CLICK acc 65-72%?` 必须被读作 heuristic | `A1`, `A2`, `A3`, `A6`, `C1` |
| `§11.2 (2)` | task-workflow 语义匹配度是关键变量 | 保留但降格 | `SOFT` 保持即可，不可升格 | `A3`, `B4`, `B6`, `A6` |
| `§11.2 (3)` | workflow 只在少量步骤上真正改变行为 | 保留 | 原样保留 | `A2` |
| `§11.2 (3)` | 模型倾向于遵循 workflow 而非独立推理 | 保留但降格 | 必须保留 `SOFT` | `B4`, `B6` |
| `§11.2 (5)` | `Step SR delta = Σ(positive) - Σ(negative)` | 保留但降格 | 作为解释框架可保留，但不要暗示严格因果识别 | `A2` |
| `§11.3` | 论文叙事 vs 实际机制总表 | 保留 | 原样保留；这是当前全文最适合进入 report 的汇总表之一 | `A1-A6`, `B2`, `B4`, `B6`, `C1` |
| `§12` | 脚本清单 | 保留 | 原样保留 | scripts dir |

## 3. Highest-Priority Edits When You Eventually Touch正文

若后面开始实际改正文，优先顺序建议如下：

1. 修 `§8.1 (1)` 的例子错配  
   当前把 `P-3` 当 TYPE 例子不稳。最好的处理是把这一点改成“值/标签格式校正”，并让 `P-2` 承担 TYPE/search-term 的例子。

2. 把所有“阈值 / 规律”句子降格  
   重点看：
   - `§8.2 (7)` 的 “收益天花板很低”
   - `§10.2` 的 alignment 叙述
   - `§10.3` 的双重条件
   - `§11.1` 图中的 `65-72%?`

3. 统一所有 workflow feature 引用口径  
   - `§4` 主要挂 `C1/C2/C3`
   - `§6` 主要挂 `A5`
   - `§10.1` 同时挂 `A1 + C3`

4. 对 `workflow 优先于推理` 保持案例级表述  
   不要升格为普遍规律，只保留为 `case-level evidence suggests...`

## 4. Minimal Safe Claims for Final Report

如果你需要一版最稳的 mechanism narrative，这些句子风险最低：

- `AWM’s gains in C1 mainly come from stable TYPE-side value guidance and site-dependent CLICK grounding effects.`
- `On reproduced sites, workflow rarely harms the agent; on not-reproduced sites, negative interventions substantially outnumber positive ones.`
- `Cross-site degradation is driven primarily by workflow-content mismatch, with Tripadvisor showing a mixed failure mode.`
- `LM-induced workflows are more abstract than rule-induced workflows at the text level, but this abstractness does not guarantee site-wise performance superiority.`
- `The NL-vs-HTML claim was not reproduced in the three-site first run.`
- `C5 supports compact workflow libraries with low overlap, but utility and coverage remain prompt-level proxies rather than strict adherence measures.`

## 5. Files to Use Together

- [mechanism-analysis.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/mechanism-analysis.md)
- [mechanism-claim-audit.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/mechanism-claim-audit.md)
- [mechanism-appendix-mapping.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/mechanism-appendix-mapping.md)
- [appendix/README.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/README.md)

这四份文件合起来，已经足够作为后续 final report 写作时的“正文改写控制面板”。
