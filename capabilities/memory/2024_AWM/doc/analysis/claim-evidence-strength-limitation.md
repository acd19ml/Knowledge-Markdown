# Claim -> Evidence -> Strength -> Limitation

> Purpose:
> - provide a one-page audit-facing summary of the main mechanism claims
> - link each claim to its primary appendix evidence
> - make the evidential strength and reporting limitation explicit

## Core table

| Claim | Primary evidence | Strength | Main limitation | Main appendix |
|---|---|---|---|---|
| AWM 的 C1 收益主要来自稳定的 TYPE-side value guidance 与站点相关的 CLICK grounding | step-level breakdown by action type and step half | `HARD` | 仅覆盖当前 Mind2Web / first-run / C1 setting | `A1` |
| reproduced 站点上 workflow 基本无害，而 not reproduced 站点上 negative 干预显著多于 positive | paired-case distribution across audited C1 sites | `HARD` | 这是配对结果，不是严格因果识别 | `A2` |
| cross-site 退化主要由 workflow-content mismatch 驱动；tripadvisor 额外叠加 observation/candidate 质量问题 | cross-site diagnostic table + tripadvisor negative case | `HARD` | 当前仅有 tripadvisor/reddit 两个 C2 目标站 | `A3`, `B6` |
| offline vs online 更像 trade-off，而不是简单排序 | same-site kayak contrast + cross-site online negatives | `SOFT + source-driven` | 机制对比基于首轮 evidence，不是重复试验后的稳定定律 | `A7` |
| online memory 的 very-small-budget 早期收益是条件性的，只在 source-style setting 上明显 | prefix-level online curve on kayak/tripadvisor/reddit | `SOFT + source-driven` | small-data 曲线来自 prefix reconstruction，不是论文原生 learning curve | `A8` |
| LM-induced workflows 在文本层面稳定地比 rule-induced workflows 更抽象、更短、更少、更参数化 | workflow text comparison + counting rules | `HARD` | 文本层结论不能自动推出性能层优势 | `C1`, `C2`, `C3` |
| LM 的抽象性优势并不自动等于 site-wise 性能优势 | C3 score table + LM/Rule text contrast | `HARD`（文本层）+ `SOFT`（性能层） | `newegg` 只能写成 mixed / unclear，不能写 Rule 明显更好 | `A3`, `C1` |
| `code_wf` 与 `text_wf` 在 `kayak` 首轮上差异不大，但两者都未超过 baseline | C4 code/text first-run result table | `HARD` | 目前只完成 `kayak` 单站点 | `A4` |
| `NL vs HTML` 在三站点首轮整体 not reproduced | C4 three-site result table | `HARD` | 仅为 first-run；不排除多轮后站点波动 | `A4` |
| C5 支持紧凑 workflow 库与低 overlap，但 utility/coverage 只能按 prompt-level proxy 解读 | workflow quality table + counting note | `HARD` | 不等于 strict behavioral adherence | `A5` |
| Mind2Web 上更像 flat subflow reuse，而不是显式 hierarchical composition | workflow reading across kayak/newegg/united/budget | `qualitative` | 这是文本与案例阅读结论，不是结构学习指标 | `C5` |
| AWM 的成功更像“workflow 可复用性 × baseline 提升空间”的双重条件 | cross-site/site-feature comparison + alignment heuristic + text evidence | `SOFT / working hypothesis` | post-hoc，且依赖 qualitative coding 与 exploratory metric | `A1`, `C1`, `C4`, `A6` |
| 表层 alignment rate 不能当作强预测指标 | keyword-overlap heuristic across four sites | `exploratory` | 指标定义较弱，无法替代语义级匹配 | `A6` |
| workflow 过度引导在具体案例中可见：域外误导、模板跳步、workflow-first behavior | prompt-level negative cases | `HARD`（case-level）/ `SOFT`（generalization） | 只能支持 case-level mechanism，不足以直接推出普适规律 | `B4`, `B5`, `B6` |

## Minimal final-report set

If the final report needs a compact appendix set, prioritize:

- `A1`
- `A2`
- `A3`
- `A4`
- `A5`
- `A7`
- `A8`
- `B4`
- `B6`
- `C1`
- `C4`
- `C5`

## Usage note

- Use this page for report drafting and review response.
- Use [mechanism-appendix-mapping.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/mechanism-appendix-mapping.md) when you need section-by-section, sentence-level mapping.
- Use [appendix/README.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/README.md) as the canonical appendix inventory.
