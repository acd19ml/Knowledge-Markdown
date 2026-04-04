# AWM `mechanism-analysis.md` 结论/主张审计

> 本文件只做两件事：
> 1. 判断 [mechanism-analysis.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/mechanism-analysis.md) 中的关键结论/主张是 `正确`、`部分成立`、`不正确` 还是 `证据不足`；
> 2. 给出可直接进入 appendix 的候选支撑证据。
>
> 审计依据优先级：
> - 原始结果 JSON
> - `doc/analysis/*.txt` 与脚本输出
> - `doc/runbook/*.md` 的正式判定
> - `doc/analysis/case_studies/*.md`
>
> 说明：
> - `正确`：当前已有证据足以支撑，且不强于 runbook 主结论
> - `部分成立`：方向大体对，但表述过强、口径混合，或还需要补限定词
> - `不正确`：与回源结果或正式 runbook 判定冲突
> - `证据不足`：目前缺少可追溯来源，或只有解释没有硬证据

---

## 1. 可直接保留的结论

### 1.1 §1 指标分解

| 结论/主张 | 审计结果 | 证据 | 候选 appendix |
|---|---|---|---|
| `TYPE` 步骤收益最稳定 | 正确 | [step_breakdown_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/step_breakdown_output.txt) 中 budget/kayak/newegg 等站点的 TYPE `dActF1` 为非负，budget 为 `+8.4%` | [A1-step-level-breakdown.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A1-step-level-breakdown.md) |
| `CLICK` 步骤是胜负手 | 正确 | 同上；kayak/newegg 的 CLICK `dElem` 为 `+10.7%/+9.1%`，budget/sixflags 为 `-12.1%/-6.1%` | [A1-step-level-breakdown.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A1-step-level-breakdown.md) |
| reproduced 站点的 `negative = 0` | 正确 | [paired_case_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/paired_case_output.txt) 中 kayak `0`，newegg `0` | [A2-paired-case-summary.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A2-paired-case-summary.md) |
| not reproduced 站点 `negative >> positive` | 正确 | 同上；budget `12 vs 6`，sixflags `6 vs 3` | [A2-paired-case-summary.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A2-paired-case-summary.md) |
| `tripadvisor` 为 A+B 混合退化 | 正确 | [cross_site_diag_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/cross_site_diag_output.txt)：skip rate `+16pp` 且 negative 中 CLICK 占 `78%` | [A3-cross-site-diagnosis.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A3-cross-site-diagnosis.md) |
| `reddit` 主要是假说 A（workflow content mismatch） | 正确 | 同上；skip rate 只 `+4.7pp`，baseline CLICK 更高，negative 中 CLICK 占 `80%` | [A3-cross-site-diagnosis.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A3-cross-site-diagnosis.md) |
| LM workflow 在文本层面更抽象、更可复用 | 正确 | [wf_text_compare_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/wf_text_compare_output.txt) 对三站点均给出 `SUPPORTED (4/4 indicators)` | [C1-lm-vs-rule-text-evidence.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/C1-lm-vs-rule-text-evidence.md) |
| `NL vs HTML` 三站点首轮整体 `not reproduced` | 正确 | [c4-runbook.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/runbook/c4-runbook.md) 的 `C4-R1/R2/R3` 全部是 `not reproduced` | [A4-c4-result-table.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A4-c4-result-table.md) |
| C5 在当前近似口径下支持“workflow 库紧凑、低 overlap、高 utility proxy” | 正确 | [c5-runbook.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/runbook/c5-runbook.md) 的三站点表：`#workflows=7/5/5`，`function overlap=0/0.0333/0`，`utility=1.0` | [A5-c5-quality-table.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A5-c5-quality-table.md) |

### 1.2 可直接作为 appendix 候选的强证据

- [step_breakdown_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/step_breakdown_output.txt)
- [paired_case_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/paired_case_output.txt)
- [cross_site_diag_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/cross_site_diag_output.txt)
- [wf_text_compare_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/wf_text_compare_output.txt)
- [c4-runbook.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/runbook/c4-runbook.md)
- [c5-runbook.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/runbook/c5-runbook.md)

---

## 2. 方向基本对，但必须收紧的结论

| 结论/主张 | 当前状态 | 原因 | 推荐收紧方式 | 候选证据 |
|---|---|---|---|---|
| reproduced 站点后半段收益更大 | 部分成立 | kayak 强支持（`+13%`），newegg/united 仅轻度支持 | 改成“在 kayak 上尤其明显，newegg/united 方向相符但强度较弱” | `Appendix A1` |
| not reproduced 站点后半段退化更严重 | 部分成立 | budget 强支持，sixflags 不明显 | 改成“budget 显著成立，sixflags 仅弱支持” | `Appendix A1` |
| workflow 有效窗口很窄（6-18%） | 部分成立 | C1 大体成立，但 qwen/reddit 仅约 `3.9%`；范围口径需统一 | 改成“在大多数已审计设置中，workflow 只在少量步骤上改变行为” | `Appendix A2` |
| utility rate 高，但真实遵循率只有 6-18% | 部分成立 | 逻辑方向对，但“6-18%”与不同 split 口径混用 | 改成“prompt-level utility 高，但 behavior-level adherence 远低于 100%” | `Appendix A2 + A5` |
| code vs text 差异不大，但两者均低于 baseline | 部分成立 | runbook 支持“差异不大”；“两者都低于 baseline”是 kayak 首轮事实，但未必是论文隐含前提 | 保留结果事实，删除“论文隐含前提”这类推断 | `Appendix A4` |
| desc_html 增加长度，导致注意力分散 | 部分成立 | united 上结果支持现象，但“注意力分散”是解释，不是直接观测 | 改成“与注意力分散相一致的一种解释” | `Appendix A4 + B-case` |
| workflow 数量本身不是决定因素 | 部分成立 | 方向合理，但主要靠 newegg/united 少数点支撑 | 改成“首轮结果更支持 content-match 比 raw count 更重要” | `Appendix A3 + A5` |
| AWM 有条件有效，需要 workflow 可复用性 + baseline 提升空间 | 部分成立 | 是很好的工作假说，但目前仍是 first-run heuristic，不是验证完成的规律 | 改成“当前首轮证据支持的工作假说” | `Appendix A1 + A5` |

---

## 3. 当前不正确或强于证据的结论

| 结论/主张 | 审计结果 | 问题 | 依据 | 处理建议 |
|---|---|---|---|---|
| `§9` P-1 当前正文案例表述 | ~~不正确~~ → **正确** | 二次回源确认：pred_act 为空字符串，output 为 NL 幻觉，与正文描述一致。原审计误读。 | `results/gpt-4o/test_task/kayak/{no_workflow,offline_wf}/1.json` | 已保留，补 Source 标注 |
| `§9` P-2 作为”策略重定向”主正例 | ~~不正确~~ → **部分成立（已修正）** | action 和 step_success 正确；task desc 错误是因为读了 few-shot exemplar 而非 eval task。实际 eval task 为”Find a new drone...”，与 `TYPE [drone]` 一致。 | `results/gpt-4o/test_task/newegg/{no_workflow,offline_wf}/4.json` | 已修正 task desc，保留案例 |
| `§9` P-3 作为”值格式校正”主正例 | ~~不正确~~ → **部分成立（已修正）** | 同上：eval task 为”Find bluetooth vertical mouse with most reviews...”，与 `SELECT [Most Reviews]` 一致。 | `results/gpt-4o/test_task/newegg/{no_workflow,offline_wf}/5.json` | 已修正 task desc，保留案例 |
| `§7.2` “共 523 个配对步骤” | ~~不正确~~ → **已修正** | 已改为 `475`，补 `paired_case_output.txt` 来源标注 | [paired_case_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/paired_case_output.txt) | 已修正 |
| `§6.2.2` function overlap 为 `0-17%` | ~~不正确~~ → **已修正** | 已改为 `0-3.33%`，补 `c5-runbook.md` 来源标注 | [c5-runbook.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/runbook/c5-runbook.md) | 已修正 |
| `newegg` 上 “Rule 反而更好” | ~~不正确~~ → **已修正** | 已降格为”Rule 在配对净收益上有竞争力”，补 c3-runbook `unclear` 判定 | [c3-runbook.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/runbook/c3-runbook.md) | 已修正 |

---

## 4. 当前证据不足，不能直接下定论的结论

| 结论/主张 | 审计结果 | 问题 | 当前可用证据 | 缺什么 |
|---|---|---|---|---|
| “workflow 优先于推理” | 部分成立（SOFT） | 这是模式归纳，不是直接可观测变量 | `N-1/N-2` 已有 prompt excerpt 与负例对照 | 只能作为 soft mechanism claim 使用 |
| “模板跳步” | 部分成立 | `N-3` 现在已有前后轨迹与 workflow 模板片段 | `B5-sixflags-step-skipping-case.md` | 可作为 case-level mechanism claim，不应泛化过度 |
| “对齐率与性能呈反向趋势” | ~~证据不足~~ → **部分成立（exploratory）** | 已有 `alignment_rate.py` 脚本和输出。反向趋势在 budget/sixflags/kayak 成立，newegg 为例外。正文已标注为 exploratory metric。 | `alignment_rate_output.txt` | 匹配方法 validity 有限，newegg 打破单调性 |
| “65-72% baseline CLICK 是成功阈值” | ~~证据不足~~ → **已降格** | 正文已改为 “post-hoc 从 4 站点观察到的 pattern，不是独立验证的阈值” | `step_breakdown_output.txt` | 已标注为 working hypothesis |
| “desc_html 的问题主要来自 prompt 长度” | 证据不足 | 目前只是合理解释 | united 上 `desc_html` 明显更差 | 需要额外长度/注意力证据 |
| “workflow 收益天花板很低” | 证据不足/可保留方向 | 方向合理，但“天花板”是强表述 | paired-case 中 changed-step 比例低 | 更适合改成“实际影响面有限” |

---

## 5. `§9` 案例审计结果

| case | 审计结果 | 是否可直接进 appendix | 说明 |
|---|---|---|---|
| `P-1` | ~~不通过~~ → **通过** | 是 | 二次回源确认：pred_act 空字符串 + NL 幻觉输出，与正文一致 |
| `P-2` | ~~不通过~~ → **通过（已修正 task desc）** | 是 | action 正确；task desc 从 exemplar `gaming desktop` 改为 eval task `new drone` |
| `P-3` | ~~不通过~~ → **通过（已修正 task desc）** | 是 | action 正确；task desc 从 exemplar `Remove SSD` 改为 eval task `bluetooth mouse` |
| `N-1` | ~~候选~~ → **通过** | 是 | 二次回源确认，已补 Source 标注 |
| `N-2` | 通过 | 是 | 二次回源确认 |
| `N-3` | ~~候选~~ → **通过** | 是 | 二次回源确认，已补 Source 标注 |

### 5.1 当前推荐保留的案例候选

- **负例首选**：[`B4-sixflags-negative-case.md`](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/B4-sixflags-negative-case.md)
- **负例备选**：[`B5-sixflags-step-skipping-case.md`](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/B5-sixflags-step-skipping-case.md)
- **跨站点负例**：[`B6-tripadvisor-cross-site-negative.md`](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/B6-tripadvisor-cross-site-negative.md)
- **正例首选**：[`B2-united-positive-case.md`](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/B2-united-positive-case.md)
- **正例备选**：[`B1-kayak-positive-case.md`](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/B1-kayak-positive-case.md)

---

## 6. 推荐进入 appendix 的证据

### 6.1 最关键的 6 份证据

1. `Appendix A1`：C1 step-level/action-type delta 总表  
   来源：[step_breakdown_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/step_breakdown_output.txt)

2. `Appendix A2`：paired-case summary  
   来源：[paired_case_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/paired_case_output.txt)

3. `Appendix A3`：cross-site degradation diagnostics  
   来源：[cross_site_diag_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/cross_site_diag_output.txt)

4. `Appendix A4`：C4 result table  
   来源：[c4-runbook.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/runbook/c4-runbook.md)

5. `Appendix A5`：C5 quality table  
   来源：[c5-runbook.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/runbook/c5-runbook.md)

6. `Appendix C1`：LM vs Rule text comparison  
   来源：[wf_text_compare_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/wf_text_compare_output.txt)

### 6.2 当前建议的正文-证据挂法

- `AWM’s gains mainly come from stable TYPE-side value guidance and site-dependent CLICK grounding effects (Appendix A1).`
- `Workflow mismatch, rather than generic target-site collapse alone, explains most cross-site degradation (Appendix A2-A3).`
- `LM-induced workflows are more abstract than rule-induced workflows at the text level, but this does not guarantee site-wise performance superiority (Appendix C1 and A3).`
- `The C5 utility and coverage results should be interpreted as prompt-level proxies rather than strict behavioral adherence evidence (Appendix A5).`

---

## 7. 当前阶段建议

1. 当前主线 source gap 已基本闭环。
2. 后续若改正文，优先把 `§10.2/§10.3/§11` 的 exploratory 与 working-hypothesis 标签保留住。
3. 不要再把 `P-2/P-3` 误写回 few-shot exemplar task。
