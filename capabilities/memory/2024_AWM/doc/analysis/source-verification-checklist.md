# AWM 回源核对任务单

> 目的：把 `mechanism-analysis.md` 中的关键结论、案例和中间指标，逐条回挂到原始证据。
> 目标不是“所有文字都可追溯”，而是做到：
> 1. final report 正文中的每个关键结论，都能指向 appendix 中的支撑性证据；
> 2. appendix 只保留最关键、最能支撑结论的原始证据；
> 3. 每条 appendix 证据都能追溯到具体 JSON、脚本输出或 workflow 文件。

---

## 1. 使用原则

- 正文只保留“有证据编号可挂靠”的结论。
- appendix 证据分三类：
  - `A类`：脚本汇总表
  - `B类`：典型 case 对照
  - `C类`：workflow 文本证据
- 每个正文主张优先只挂 1-2 个最强证据，不堆砌。
- 若分析层表述强于 runbook 主结论，应优先收紧表述，而不是放大 secondary proxy。

---

## 2. 回源核对任务单

| 优先级 | 文中位置 | 当前问题 | 应核对的源 | 核对目标 | 通过后放入 appendix 的证据形式 |
|---|---|---|---|---|---|
| P0 | `mechanism-analysis.md` §9 P-1 | baseline 输出与 case_studies 不一致 | `results/gpt-4o/test_task/kayak/no_workflow/1.json`；`results/gpt-4o/test_task/kayak/offline_wf/1.json`；`case_studies/positive_gpt-4o_test_task_kayak_offline_wf.md` | 确认 task id、step id、baseline pred、workflow pred、step_success 是否一致 | `Appendix B1`：baseline vs workflow 单步对照表 + prompt excerpt |
| P0 | `mechanism-analysis.md` §9 P-2 | task 与 `TYPE [drone]` 语义错位 | `results/gpt-4o/test_task/newegg/no_workflow/4.json`；`results/gpt-4o/test_task/newegg/offline_wf/4.json`；`case_studies/positive_gpt-4o_test_task_newegg_offline_wf.md` | 确认这是数据本身如此，还是 case 选错 / task 写错 | 若证据成立则 `Appendix B2`；若不成立则换新 case |
| P0 | `mechanism-analysis.md` §9 P-3 | “Remove SSD” 与排序动作语义错位 | `results/gpt-4o/test_task/newegg/no_workflow/5.json`；`results/gpt-4o/test_task/newegg/offline_wf/5.json`；同名 case study | 确认 task/step/action 是否对应 | 当前未单独落 `B3`；若正文需要，可补第二个 newegg 正例块，或并入 `B2` 的说明 |
| P0 | `mechanism-analysis.md` §9 N-1 | 任务语义与 `Reservations` 动作可疑 | `results/gpt-4o/test_task/budget/no_workflow/0.json`；`results/gpt-4o/test_task/budget/offline_wf/0.json`；`case_studies/negative_gpt-4o_test_task_budget_offline_wf.md` | 确认这是有效负例，不是页面上下文被误读 | 当前未单独落 appendix；若正文需要可补 budget 负例块 |
| P0 | `mechanism-analysis.md` §9 N-2 | 机制解释强于原始证据 | `results/gpt-4o/test_task/sixflags/no_workflow/2.json`；`results/gpt-4o/test_task/sixflags/offline_wf/2.json`；`case_studies/negative_gpt-4o_test_task_sixflags_offline_wf.md` | 确认 prompt 中确有相关 workflow 步骤，observation 中确有对应按钮 | `Appendix B4`：workflow-content mismatch case |
| P0 | `mechanism-analysis.md` §9 N-3 | “模板跳步”需要前后轨迹支撑 | `results/gpt-4o/test_task/sixflags/no_workflow/1.json`；`results/gpt-4o/test_task/sixflags/offline_wf/1.json` | 确认 workflow 确实压缩了中间 UI 步骤，而不是单步误选 | `Appendix B5`：step-skipping case |
| P0 | `mechanism-analysis.md` §7.2 | `523` 总步数与配对输出不一致 | `paired_case_output.txt` | 重算 C1 7 站点 paired total、各类占比、SKIP 子集占比 | `Appendix A2`：paired-case summary table |
| P1 | `mechanism-analysis.md` §4.3.1 | LM workflow 数量与 C5 不同 | `wf_text_compare_output.txt`；`workflow/*_lm_wf.txt` | 统一是否把 `Summary Workflows` 计入 | `Appendix C1`：workflow counting rule |
| P1 | `mechanism-analysis.md` §6.2.1 | LM concrete values 与 §4 冲突 | `workflow/kayak_lm_wf.txt`；`workflow/newegg_lm_wf.txt`；`workflow/united_lm_wf.txt`；`wf_text_compare_output.txt` | 统一 “concrete value” 定义：正文 token 是否算具体值 | `Appendix C2`：value counting rule + examples |
| P1 | `mechanism-analysis.md` §6.2.2 function overlap | `0-17%` 与 runbook 冲突 | `c5-runbook.md`；当前计算脚本 | 确认真实是 `0-3.33%` 还是另一套定义 | `Appendix A5`：C5 quality stats table |
| P1 | `mechanism-analysis.md` §4.3.4 | `newegg` 被写成 Rule 更好，强于 runbook | `c3-runbook.md`；paired outputs；score tables | 把 secondary proxy 和主指标判定分开 | `Appendix A3`：C3 site-by-site score table |
| P1 | `mechanism-analysis.md` §8.1 item 1 | TYPE 机制引用了 P-3，但 P-3 是 SELECT | `§9` 最终保留案例 | 换成真正 TYPE case，或把表述改成 broader action-format effect | 优先回挂 `Appendix B2`，必要时再单独补 `B3` |
| P1 | `mechanism-analysis.md` §10.1 | workflow count / avg steps 与 §4/§6 口径不一致 | `workflow/*_wf.txt`；`wf_text_compare_output.txt` | 统一站点特征表中的 workflow stats | `Appendix C3`：site feature table with definitions |
| P1 | `mechanism-analysis.md` §10.2 | “对齐率”缺少明确源 | 若有脚本则补脚本；若无则回手动标注记录 | 给每个站点对齐率提供可追溯来源 | `Appendix A6`：alignment-rate calculation note |
| P2 | `mechanism-analysis.md` §10.3 | `65-72%` 像阈值结论，但证据更像 heuristic | `§1`；`§10.1`；runbook score breakdown | 将其降格为 first-run heuristic，避免过度声称 | 不单独做 appendix，可在 `Appendix A6` 或 `A1` 的注释里说明 |
| P2 | `mechanism-analysis.md` §11.1 | `4-19%` 等范围值口径需统一 | `paired_case_output.txt`；`§7.2` 重算结果 | 明确百分比是占总 steps 还是占 changed steps | `Appendix A2` 统一定义即可 |

---

## 3. 建议的 Appendix 结构

不要按章节组织 appendix，而按证据类型组织。

### Appendix A. Aggregated Quantitative Evidence

- `A1` step-level breakdown
- `A2` paired-case summary
- `A3` cross-site degradation diagnostics
- `A4` C4 result table
- `A5` C5 quality stats
- `A6` alignment-rate note

### Appendix B. Prompt-Level Case Evidence

- `B1/B2/B4/B5/B6` 各放 1 个最强正例 / 负例
- 每个 case 固定模板：
  - task id / step id
  - target action
  - baseline pred
  - treatment pred
  - relevant workflow excerpt
  - relevant observation excerpt
  - one-sentence interpretation

### Appendix C. Workflow Text Evidence

- `C1` LM vs Rule text evidence
- `C2` concrete value counting rule
- `C3` workflow counting and site features

---

## 4. 正文结论如何挂 Appendix

建议 final report 中的关键主张按这种方式挂证据：

- `AWM’s gains mainly come from stable value-template effects and site-dependent CLICK grounding effects (Appendix A1).`
- `Cross-site degradation is driven primarily by workflow-content mismatch, with additional candidate-quality degradation on Tripadvisor (Appendix A3, B4-B6).`
- `LM-induced workflows are consistently more abstract than rule-induced workflows at the text level, although this does not guarantee better performance on every site (Appendix A3, C1-C3).`
- `The utility and coverage metrics used in C5 should be interpreted as prompt-level proxies rather than strict behavioral adherence measures (Appendix A5).`

---

## 5. 最关键的 6 份证据

如果时间有限，只优先保这 6 份 appendix：

1. `A1`：C1 step-level breakdown 总表
2. `A3`：C2 cross-site 诊断表
3. `C1`：C3 LM vs Rule 文本证据
4. `A5`：C5 quality stats 表
5. `B1`：一个最强正例
6. `B4`：一个最强负例

这样正文里大多数核心判断都能挂到最关键的支撑性证据。

---

## 6. 推荐执行顺序

1. 先修 `§9` 六个 case
2. 再修 `§7.2` 的总数分母和占比
3. 再统一 `§4 / §6 / §10` 的 workflow 计数与 feature 定义
4. 最后收紧 `§10 / §11` 中带 heuristic 色彩的预测性表述

---

## 7. 第一轮回源结果（已确认）

> 本节记录“已经回到原始 JSON / 分析输出核对过”的发现。

### 7.1 `§9` 六个 case 的当前状态

| case | 当前状态 | 当前结论 | 后续动作 |
|---|---|---|---|
| `P-1` | 已回源 | **CONFIRMED**：pred_act 为空字符串，output 为 NL 幻觉；正文描述与原始 JSON 一致 | 保留，补 Source 标注 |
| `P-2` | 已回源 | **DESCRIPTION_MISMATCH 已修正**：原误读来自 few-shot exemplar；实际 eval task 为 drone 搜索任务，与 `TYPE [126] [drone]` 一致 | 保留，使用修正后的 task desc |
| `P-3` | 已回源 | **DESCRIPTION_MISMATCH 已修正**：原误读来自 few-shot exemplar；实际 eval task 为 bluetooth mouse 搜索任务，与 `SELECT [Most Reviews]` 一致 | 保留，使用修正后的 task desc |
| `N-1` | 已回源 | **CONFIRMED**：负例事实成立，且已补 Source 标注 | 保留 |
| `N-2` | 已回源 | **CONFIRMED**：负例事实成立，且已补 prompt/workflow excerpt | 保留 |
| `N-3` | 已回源 | **CONFIRMED**：负例事实成立，且已补前后轨迹支撑“模板跳步”解释 | 保留 |

### 7.2 已确认并已修正的跨章节问题

| 位置 | 已确认的问题 | 当前状态 |
|---|---|---|
| `§7.2` | 文中写“共 523 个配对步骤” | **已修正为 `475`**，并回挂 `paired_case_output.txt` |
| `§4.3.1` vs `§6.2.1` vs `C5` | LM workflow 数量前后不一致（`8/6/6` vs `7/5/5`） | **已统一口径**：`wf_text_compare` 计入 `Summary Workflows`；`C5` 不计入，见 `C3` appendix |
| `§6.2.1` vs `§4.3.1` | LM concrete values 前后不一致（`0/0/0` vs `1/2/5`） | **已统一口径**：task-instantiated concrete values 计数为 `0/0/0`，见 `C2` appendix |
| `§6.2.2` | function overlap 写成 `0-17%` | **已修正为 `0-3.33%`**，按 `c5-runbook` 口径 |
| `§4.3.4` | `newegg` 被表述为 “Rule ≥ LM / Rule 反而更好” | **已降格**为“Rule 在配对净收益上有竞争力（runbook: unclear）” |

### 7.3 当前仍需谨慎使用的正文表述

1. `§10.2` 的对齐率只能按 `exploratory metric` 使用，不能写成最终定量结论。
2. `§10.3` 的“成功双条件”只能按 `working hypothesis` 使用。
3. `§11` 中凡是依赖对齐率或 post-hoc 阈值的箭头，都应保持 `SOFT` 或 `exploratory`，不能升级为 `HARD`。

### 7.4 已生成的 appendix 证据块

目前已落到 `/doc/analysis/appendix/` 的 source-traceable block：

- `A1-step-level-breakdown.md`
- `A2-paired-case-summary.md`
- `A3-cross-site-diagnosis.md`
- `A4-c4-result-table.md`
- `A5-c5-quality-table.md`
- `B1-kayak-positive-case.md`
- `B2-united-positive-case.md`
- `B4-sixflags-negative-case.md`
- `B5-sixflags-step-skipping-case.md`
- `B6-tripadvisor-cross-site-negative.md`
- `C1-lm-vs-rule-text-evidence.md`
- `C2-concrete-value-counting-rule.md`
- `C3-workflow-counting-and-site-features.md`
- `A6-alignment-rate-note.md`

这些文件已经足以支撑当前多数“可保留”主张，并为后续 final report 提供可引用 appendix 编号。

### 7.5 已闭环的 source gap

1. ~~`§10.2` 的”对齐率”~~ → **已闭环**。`scripts/alignment_rate.py` 已写入，输出 `alignment_rate_output.txt`。新数值：budget 97.2%, sixflags 94.2%, newegg 90.9%, kayak 70.6%。正文已标注为 exploratory metric，并已补 `A6` appendix 说明。
2. ~~`§10.3` 的 `65-72%`~~ → **已闭环**。正文已降格为 “post-hoc 从 4 个站点中观察到的 pattern，不是经过独立验证的阈值”。
3. ~~`§10 / §11` 引用对齐率/阈值~~ → **已闭环**。§10-§11 所有主张已逐条标注证据级别（HARD/SOFT/exploratory/定性）。

### 7.6 §9 案例回源闭环

| case | 原审计结果 | 回源核对结果 | 处理 |
|---|---|---|---|
| P-1 | “不通过（baseline 输出不一致）” | **CONFIRMED**：pred_act 为空字符串，output 为 NL 幻觉——与正文描述一致 | 保留，补 Source 标注 |
| P-2 | “不通过（跨 task 拼接）” | **DESCRIPTION_MISMATCH**：action 正确，task desc 错误——读了 exemplar 而非 eval task | 修正 task desc（gaming desktop → drone），保留案例 |
| P-3 | “不通过（task 与 action 错位）” | **DESCRIPTION_MISMATCH**：同上——exemplar 为 “Remove SSD”，eval task 为 “bluetooth mouse” | 修正 task desc，保留案例 |
| N-1 | “候选” | **CONFIRMED** | 保留，补 Source 标注 |
| N-2 | “通过” | **CONFIRMED** | 保留，补 Source 标注 |
| N-3 | “候选” | **CONFIRMED** | 保留，补 Source 标注 |
| B1 | — | **CONFIRMED**（case-study 编号为 `8/14`；raw JSON step index 为 `6`） | 保留，明确双索引并统一说明 |
| B2 | — | **CONFIRMED** | 保留 |

---

## 8. 完成标准

当以下条件都满足时，可认为“回源核对”完成：

1. `mechanism-analysis.md` 中每个关键结论都能指向一个 appendix 证据编号
2. `§9` 中保留的每个 case 都能回挂到具体 JSON
3. 所有跨章节使用的统计定义（workflow 数、concrete values、coverage、utility、function overlap、对齐率）都只有一套明确口径
4. 不再出现“分析层结论强于 runbook 主结论”的情况
