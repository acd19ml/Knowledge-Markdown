# AWM 复现实验执行协议（第一阶段）

> 本文档服务于 [experiment-design.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/experiment-design.md) 中定义的第一阶段目标：**逐条复现论文已报告的核心实验结论**。
> 本文档回答的是“每条结论具体怎么复现”，而不是“还能进一步挑战什么”。

---

## 1. 文档定位

本阶段的执行协议必须服从一个原则：

> 优先完整覆盖论文已报告的关键实验，再考虑新增问题。

因此，这里的组织方式不再是“脚本介绍优先”，而是“结论优先”：

- C1 需要跑什么
- C2 需要跑什么
- C3 需要跑什么
- C4 需要跑什么
- C5 需要保存和提取什么

脚本、命令、目录与产物都只是服务这些复现目标。

---

## 2. 代码入口与其在复现中的角色

> 代码位于 `experiments/ mind2web/`。

### 2.1 `offline_induction.py`

作用：

- 从训练集归纳 offline workflows

对应复现目标：

- C1：offline cross-task 主结果
- C3：LM induction vs rule induction
- C5：workflow quality analysis

### 2.2 `run_mind2web.py`

作用：

- 在测试集上运行 agent，并把 workflow 作为 memory 注入

对应复现目标：

- C1：offline 结果
- C2：online / offline 泛化结果
- C4：表示层消融
- C5：utility rate 与 coverage 所需原始结果

### 2.3 `online_induction.py`

作用：

- 从测试过程产生的成功轨迹中继续归纳 workflows

对应复现目标：

- C2：online AWM 泛化结果

### 2.4 `pipeline.py`

作用：

- 串联 induction 与 inference

说明：

- 适合作为批量运行入口
- 但不应取代你对“当前是在复现哪条论文结论”的控制

### 2.5 `results/calc_score.py`

作用：

- 汇总总体指标

对应复现目标：

- C1-C4 的总体分数检查

限制：

- 只能回答“结果是多少”
- 不能替代 C5 需要的中间分析

### 2.6 `workflow/retrieve.py`

说明：

- 当前第一阶段复现中不是主入口
- 只有在你确认论文对应设置确实依赖 retrieval 时才应纳入

---

## 3. 第一阶段复现路线图

本阶段按 `C1 -> C2 -> C3 -> C4 -> C5` 推进。

### Step A：先站住主结果

先复现：

- C1：Mind2Web offline cross-task 主结果

如果 C1 还没有稳定结果，不要提前分散到大量消融。

### Step B：再复现泛化结论

在 C1 基础上继续：

- C2：online vs offline 在不同 split 下的泛化关系

### Step C：再复现机制相关消融

当 C1、C2 已经有可读结果后，再做：

- C3：LM vs rule induction
- C4：code/text、NL/HTML 等表示层消融

### Step D：最后补中间指标

最后补：

- C5：workflow quality analysis

原因很直接：C5 需要较完整的中间产物，而这些产物往往建立在前面的运行结果之上。

---

## 4. C1：Mind2Web offline cross-task 主结果

### 4.1 要复现的结论

- Offline AWM 优于对应基线
- 提升主要来自 `element accuracy` 与 `step success rate`
- `action F1` 不一定同步提升

### 4.2 需要的实验条件

至少需要两组条件：

- baseline
- offline AWM

如果条件允许，建议同时保留论文中的两个参照思路：

- 不使用 workflow 的基本条件
- 使用 workflow memory 的 offline 条件

### 4.3 需要的输出

每组条件至少保留：

- `Elem Acc`
- `Action F1`
- `Step SR`
- `SR`

此外必须保留：

- 逐样本 JSON 结果

因为后续 C5 和失败分析都依赖它。

### 4.4 最低复现判据

满足以下任意两条，可初步视为 C1 复现成功：

- offline AWM 在 `Step SR` 上优于 baseline
- offline AWM 在 `Elem Acc` 上优于 baseline
- offline AWM 的提升结构与论文一致，即主要来自元素选择而非动作 F1

---

## 5. C2：Online AWM 的泛化结果

### 5.1 要复现的结论

- online 在 `cross-task`、`cross-website`、`cross-domain` 上优于基线
- 随着 distribution gap 增大，online 相对 offline 更有优势
- offline 在分布较匹配时可保持竞争力

### 5.2 需要的实验条件

至少需要三类结果：

- baseline
- offline AWM
- online AWM

并按三个 split 组织：

- `cross-task`
- `cross-website`
- `cross-domain`

### 5.3 需要的输出

每个 split、每个条件都至少保留：

- `Elem Acc`
- `Action F1`
- `Step SR`
- `SR`

最后形成一个并排结果表，结构上尽量接近论文表 4。

### 5.4 最低复现判据

满足以下条件之一，可视为较强复现信号：

- online 相对 baseline 在三个 split 上都方向一致地更好
- online 相对 offline 的优势在更大 gap 的 split 上更明显
- offline 与 online 在 `cross-task` 上接近，而在 `cross-website` / `cross-domain` 上差异拉开

---

## 6. C3：LM induction vs rule induction

### 6.1 要复现的结论

- LM induction 优于 rule induction
- LM 的优势主要来自抽象 sub-routine，而不是保留完整具体 trajectory

### 6.2 需要的实验条件

至少需要三组条件：

- baseline
- AWM with rule induction
- AWM with LM induction

### 6.3 需要的输出

至少保留：

- `Elem Acc`
- `Action F1`
- `Step SR`
- `SR`

此外，建议额外保存：

- 各自归纳出的 workflow 示例

因为 C3 的结论不仅是“谁分高”，也是“为什么谁分高”。

### 6.4 最低复现判据

满足以下任意两条，可初步视为 C3 复现成功：

- LM induction 在 `Step SR` 上优于 rule induction
- LM induction 在 `SR` 上优于 rule induction
- LM induction 的 workflow 更抽象，rule induction 更接近完整具体 trajectory

---

## 7. C4：表示层消融

### 7.1 子结论一：code vs text workflow

要复现的结论：

- code workflow 与 text workflow 差异不大

需要的条件：

- baseline
- AWM code workflow
- AWM text workflow

最低判据：

- 两种 workflow 的核心指标接近
- 没有出现一方对另一方的稳定大幅优势

### 7.2 子结论二：NL vs HTML 环境表示

要复现的结论：

- 仅用 NL 描述优于加入 HTML

需要的条件：

- `Desc only`
- `HTML only`
- `Desc + HTML`

最低判据：

- `Desc only` 的 `Step SR` 不低于 `HTML only`
- `Desc + HTML` 不优于 `Desc only`，或方向一致地更差

---

## 8. C5：Workflow quality analysis

### 8.1 要复现的结论

- workflow 数量较精简
- utility rate 较高
- function overlap 较低
- Mind2Web cross-task 上 coverage 可以偏低，但这不自动推翻 offline workflow 的价值

### 8.2 需要保存的中间产物

为了完成 C5，运行时应尽量保留：

- workflow 文本
- induction 输入来源
- 逐样本推理结果
- workflow 被使用的痕迹

### 8.3 需要提取的指标

至少需要：

- `Number of workflows`
- `Coverage`
- `Function overlap`
- `Utility rate`

### 8.4 注意事项

不要把 C5 当成比 C1 更早的任务。

原因：

- workflow quality analysis 是中间解释层
- 它需要建立在主结果已跑出、产物已齐全的前提上

---

## 9. 运行前统一检查项

无论在复现 C1-C5 中哪一条，正式运行前都先检查：

| 检查项 | 原因 |
|------|------|
| 数据 split 是否对应论文设定 | 避免“复现的不是同一个实验” |
| baseline 是否存在且可比较 | 没有 baseline 就无法判断论文结论是否成立 |
| 输出目录命名是否统一 | 后处理和表格汇总依赖一致命名 |
| 是否保留逐样本结果 | 后续很多分析都依赖 raw results |
| 当前评测是否为 teacher-forcing | 影响结果解释口径 |

---

## 10. 建议命名规范

为了让第一阶段结果更容易整理成“论文结论复现状态表”，建议统一使用与结论对应的命名。

### 10.1 结果目录建议包含三层语义

- `split`
- `condition`
- `representation` 或 `induction mode`

例如：

- `cross_task/no_workflow`
- `cross_task/offline_wf`
- `cross_task/online_wf`
- `cross_task/rule_wf`
- `cross_task/text_wf`
- `cross_task/html_obs`

### 10.2 不建议继续只用模糊 suffix

例如单独使用 `workflow`、`test1`、`final` 这类命名会导致后续无法直接映射到 C1-C5。

---

## 11. 最小命令模板

这里只保留最小必要命令模板，详细运行顺序由你在具体阶段展开。

### 11.1 Offline induction

```bash
python offline_induction.py \
  --mode auto \
  --domain {DOMAIN} --subdomain {SUBDOMAIN} --website {WEBSITE} \
  --model_name gpt-4o \
  --output_dir workflow
```

### 11.2 Baseline inference

```bash
python run_mind2web.py \
  --website {WEBSITE} \
  --workflow_path workflow/_empty.txt \
  --model gpt-4o \
  --benchmark test_task \
  --suffix no_workflow
```

### 11.3 Offline workflow inference

```bash
python run_mind2web.py \
  --website {WEBSITE} \
  --workflow_path workflow/{WEBSITE}.txt \
  --model gpt-4o \
  --benchmark test_task \
  --suffix offline_wf
```

### 11.4 Score summary

```bash
python results/calc_score.py --results_dir results/gpt-4o/test_task/{WEBSITE}/no_workflow
python results/calc_score.py --results_dir results/gpt-4o/test_task/{WEBSITE}/offline_wf
```

---

## 12. 本阶段的交付物

第一阶段结束时，建议至少整理出三类交付物：

### 12.1 论文结论复现状态表

按 `C1-C5` 列：

- 是否已运行
- 是否复现成功
- 成功依据是什么
- 若未成功，最可能原因是什么

### 12.2 论文风格结果表

尽量整理出与论文相近结构的结果表：

- C1 主结果表
- C2 泛化结果表
- C3 消融对比表
- C4 表示层消融表
- C5 workflow quality 表

### 12.3 中间产物归档

至少归档：

- workflow 文本
- 结果 JSON
- 关键汇总表

这样第二阶段若要做批判性扩展，不需要重新补基础材料。

---

## 13. 与设计文档的边界

[experiment-design.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/experiment-design.md) 负责回答：

- 当前阶段到底要复现哪些论文结论
- 复现成功的判据是什么

本文件负责回答：

- 这些结论分别要跑哪些实验
- 需要保留哪些输出
- 如何组织结果，便于形成第一阶段复现结论
