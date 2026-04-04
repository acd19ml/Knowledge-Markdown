# AWM Appendix 证据候选清单

> **Status: deprecated as an active source of truth.**
> 当前 appendix 的正式文件集合以 [appendix/README.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/README.md) 为准；
> 正文主张到 appendix 的正式挂靠关系以 [mechanism-appendix-mapping.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/mechanism-appendix-mapping.md) 为准。
>
> 本文件保留为**历史候选池/取舍记录**，用于解释早期为什么选了某些 case、放弃了某些 case。

> 本文件只收录“当前已经较干净、可作为 final report appendix 候选”的证据。
> 不等于最终版本，但优先从这里选。

> 说明：
> - 已经实际落成的 appendix block 见 `/doc/analysis/appendix/README.md`
> - 本文件现在更偏“候选池与取舍理由”

---

## 1. 最值得优先做成 Appendix 的汇总证据

### A1. Step-level breakdown 总表

- 作用：
  - 支撑 `TYPE` 稳定正向
  - 支撑 `CLICK` 决定 reproduced / not reproduced
  - 支撑后半段累积效应
- 主来源：
  - [step_breakdown_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/step_breakdown_output.txt)
  - [step_breakdown_results.csv](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/step_breakdown_results.csv)
- 正文可挂结论：
  - “AWM gains mainly come from stable TYPE-side value guidance and site-dependent CLICK grounding effects.”

### A2. Paired-case distribution 总表

- 作用：
  - 支撑 `negative = 0` vs `negative >> positive`
  - 支撑 workflow 的有效窗口有限
  - 支撑 workflow 在很多步骤上只是旁观者
- 主来源：
  - [paired_case_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/paired_case_output.txt)
- 注意：
  - 正文里不要再使用 `523` 这个错误总数，需基于实际输出重算

### A3. Cross-site degradation diagnosis

- 作用：
  - 支撑 `tripadvisor = A+B mixed`
  - 支撑 `reddit = primarily A`
  - 支撑 C2 中 “workflow mismatch causes negative transfer”
- 主来源：
  - [cross_site_diag_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/cross_site_diag_output.txt)

### A4. C4 result table

- 作用：
  - 支撑 `NL vs HTML` 三站点首轮 `not reproduced`
  - 支撑 `code vs text` 在 `kayak` 上“差异不大”
- 主来源：
  - [c4-runbook.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/runbook/c4-runbook.md)

### A5. C5 quality table

- 作用：
  - 支撑 `#workflows` 紧凑
  - 支撑 `function overlap` 低
  - 支撑 `utility rate` 仅为宽口径 proxy
- 主来源：
  - [c5-runbook.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/runbook/c5-runbook.md)

### C1. LM vs Rule workflow text comparison

- 作用：
  - 支撑 LM workflow 文本层更抽象、更参数化
  - 支撑 Rule workflow 更像具体 trajectory 库
- 主来源：
  - [wf_text_compare_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/wf_text_compare_output.txt)

---

## 2. 正向案例候选

> 当前优先选“task 语义与 action 语义一致”的案例。

### B1. Kayak 正例：hotel/flight 场景中的 element grounding 修正

- 候选来源：
  - [positive_gpt-4o_test_task_kayak_offline_wf.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/case_studies/positive_gpt-4o_test_task_kayak_offline_wf.md)
- 当前更推荐的子例：
  - `Case 2: task=4, step=8/14`
  - `Case 3: task=5, step=5/6`
- 原因：
  - 都是 `CLICK wrong -> CLICK right`
  - task 语义与 action 语义相对一致
  - 比 `Case 1` 更稳定，因为 `Case 1` 的 baseline 输出与正文现有写法不一致
- 适合支撑：
  - “workflow can improve element grounding on matched sites”

### B2. United 正例：从错误 action type 到正确 TYPE

- 候选来源：
  - [positive_qwen_qwen3_5-397b-a17b_test_task_united_lm_wf.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/case_studies/positive_qwen_qwen3_5-397b-a17b_test_task_united_lm_wf.md)
- 当前推荐子例：
  - `Case 1: task=3, step=5/27`
- 原因：
  - baseline 从 `CLICK` 走偏
  - workflow 纠正为正确 `TYPE`
  - 这是比当前 `§9 P-2/P-3` 更干净的“策略/值模板”类证据
- 适合支撑：
  - “workflow can redirect the action mode at key steps”

### B3. Newegg 正例：value-format / label-format 修正

- 候选来源：
  - [positive_gpt-4o_test_task_newegg_offline_wf.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/case_studies/positive_gpt-4o_test_task_newegg_offline_wf.md)
- 当前推荐子例：
  - `Case 4: task=4, step=11/13`
  - `Case 5: task=5, step=3/7`
- 注意：
  - 这两个例子当前 task 语义有错位风险
  - 如果要进正文，必须先回源再确认是否保留
- 适合支撑：
  - “workflow can correct label-format / selection-format errors”

---

## 3. 负向案例候选

### B4. Sixflags 负例：域外 workflow 误导

- 候选来源：
  - [negative_gpt-4o_test_task_sixflags_offline_wf.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/case_studies/negative_gpt-4o_test_task_sixflags_offline_wf.md)
- 当前推荐子例：
  - `Case 3: task=2, step=0/6`
- 原因：
  - baseline 正确，workflow 错误
  - 任务是财务报告，workflow 却把模型拉回公园/门票导航
  - 这是“workflow content mismatch”最干净的负例之一
- 适合支撑：
  - “workflow can become harmful when its operation pattern is semantically mismatched”

### B5. Sixflags 负例：模板跳步候选

- 候选来源：
  - 同上文件
- 当前推荐子例：
  - `Case 2: task=1, step=5/14`
- 原因：
  - baseline 正确选择日期
  - workflow 直接跳到 `Book Now`
- 注意：
  - 要作为正文中的“模板跳步”证据，必须补前后轨迹
- 适合支撑：
  - “compressed workflow templates may encourage step skipping”

### B6. Tripadvisor 负例：cross-site workflow mismatch

- 候选来源：
  - [negative_qwen_qwen3_5-397b-a17b_test_website_tripadvisor_online_wf.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/case_studies/negative_qwen_qwen3_5-397b-a17b_test_website_tripadvisor_online_wf.md)
- 当前推荐子例：
  - `Case 4: task=2, step=0/13`
  - `Case 5: task=3, step=0/15`
  - `Case 10: task=10, step=0/3`
- 原因：
  - 都属于 baseline 正确先 `CLICK`
  - workflow 错误地改成 `TYPE [location]`
  - 和 `cross_site_diag_output.txt` 的结论高度一致
- 适合支撑：
  - “online workflows learned from the source site can misfire on structurally different targets”

---

## 4. 当前不建议直接进 Appendix 的案例

| 案例 | 原因 |
|---|---|
| `§9 P-1` 当前写法 | 正文 baseline 输出与 raw JSON 不一致 |
| `§9 P-2` | task 与 action 明显跨 task 拼接 |
| `§9 P-3` | task 与 action 明显错位 |
| `budget N-1` | 虽然方向成立，但任务语义和动作语义仍显著异常，需要更多上下文才能放心进入正文 |

---

## 5. 正文主张与证据挂靠建议

| 正文主张 | 推荐证据 |
|---|---|
| AWM gains mainly come from stable TYPE-side guidance and site-dependent CLICK grounding | `A1 + A2` |
| Workflow mismatch is the main reason for cross-site degradation | `A3 + B4/B6` |
| LM workflows are more abstract than rule workflows at the text level | `C1` |
| LM abstraction does not guarantee site-wise superiority | `A3 + C1` |
| NL vs HTML is not reproduced after the three-site first run | `A4` |
| C5 metrics should be read as proxy-level quality evidence | `A5` |

---

## 6. 下一步建议

1. 优先使用已生成的 `B1/B2/B4/B5/B6`
2. 不要继续使用当前 `§9` 中的 `P-2 / P-3`
3. 若后续要再补正例，优先回到 `kayak` 或 `united` 的 raw JSON，而不是继续沿用 `newegg` 的语义错位案例
