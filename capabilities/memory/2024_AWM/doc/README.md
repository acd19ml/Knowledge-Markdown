# AWM Deep Reproduction — Documentation Hub

> AWM (Agent Workflow Memory) 深度复现项目的文档中心。
> 本项目的目标不是简单复现论文分数，而是完成从"结论验证"到"机制解释"再到"边界识别"的完整闭环。

---

## Directory Structure

```
doc/
├── README.md                 ← 本文件
├── design/                   # 路线层 + 设计层
│   ├── research-roadmap.md       项目总路线图：三层研究问题 & 三阶段推进策略
│   ├── experiment-design.md      第一阶段实验设计：C1-C5 待复现结论 & 判据
│   └── experiment-protocol.md    第一阶段执行协议：脚本入口、命令模板、产物规范
├── runbook/                  # C1-C5 执行记录
│   ├── c1-runbook.md             C1 offline cross-task 主结果（7 站点）
│   ├── c2-runbook.md             C2 online 泛化结果（3 split）
│   ├── c2-summary.md             C2 首轮结果摘要
│   ├── c3-runbook.md             C3 LM vs rule induction
│   ├── c4-runbook.md             C4 表示层消融（首轮已完成）
│   └── c5-runbook.md             C5 workflow quality analysis
├── analysis/                 # 阶段二三：机制分析 & 边界识别
│   ├── mechanism-analysis.md     机制分析主文档（层次二 & 三）
│   ├── reproduction-status.md    C1-C5 复现总状态表
│   └── scripts/                  分析脚本
│       ├── step_breakdown.py         指标按维度交叉分解
│       ├── paired_case.py            同 task 配对案例提取
│       ├── cross_site_diag.py        cross-site 退化诊断
│       └── wf_text_compare.py        LM vs rule workflow 文本对比
└── report/                   # 最终产物
    ├── Interim.tex               中期报告 TeX 源文件
    └── final.md                  最终报告骨架
```

---

## Research Roadmap Overview

项目按三个层次递进：

| 层次 | 核心问题 | 对应阶段 | 状态 |
|------|---------|---------|------|
| 一 | 论文声称是否成立 | 阶段一：结论复现 (C1-C5) | ✅ 全部完成首轮 |
| 二 | 论文结论为什么成立 | 阶段二：机制解释 | ✅ 已完成（§1-§6） |
| 三 | 论文没有说清楚的部分 | 阶段三：边界识别 | ✅ 已完成（§7-§8, 7 个边界条件） |

详见 [design/research-roadmap.md](design/research-roadmap.md)。

---

## C1-C5 Reproduction Status

| stage | claim | status | judgment |
|-------|-------|--------|----------|
| C1 | offline AWM cross-task 优于 baseline | ✅ 完成 | mixed; 稳定性不足 |
| C2 | online AWM 在更大 distribution gap 下更优 | ✅ 完成 | mixed → not reproduced |
| C3 | LM induction 优于 rule induction | ✅ 完成 | 解释性结论成立; 性能 mixed |
| C4 | 表示层消融 (code/text, NL/HTML) | ✅ 完成 | code/text reproduced; NL/HTML not reproduced |
| C5 | workflow quality analysis | ✅ 完成 | reproduced under current approximation |

详见 [analysis/reproduction-status.md](analysis/reproduction-status.md)。

---

## Layer 2-3 Analysis Plan

基于 C1-C5 的首轮日志与分析产物，层次二三的分析按优先级排列：

1. **指标分解** — TYPE 步骤收益最稳定，CLICK 步骤高度站点相关 ✅
2. **配对案例** — reproduced 站点 negative=0，not reproduced 站点 workflow 有害 ✅
3. **cross-site 退化诊断** — tripadvisor 混合退化，reddit 主要 workflow 不适配 ✅
4. **LM vs rule 文本对比** — 4/4 抽象性指标支持论文主张 ✅
5. **表示形式影响** — code/text 差异不大; NL/HTML 三站点首轮不支持论文统一主张 ✅
6. **workflow 质量与性能** — 库精简且低冗余；当前 utility proxy 高，但真实影响率仅 6-18% ✅

详见 [analysis/mechanism-analysis.md](analysis/mechanism-analysis.md)。

---

## Data Pointers

| 数据 | 路径 |
|------|------|
| 实验代码 | `experiments/mind2web/` |
| 结果日志 | `experiments/mind2web/results/{model}/{split}/{website}/{condition}/` |
| Workflow 文本 | `experiments/mind2web/workflow/` |
| 评分脚本 | `experiments/mind2web/results/calc_score.py` |
