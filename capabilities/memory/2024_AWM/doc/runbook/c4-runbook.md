# C4 Runbook: 表示层消融

> 本文档是 C4 的可执行 runbook。
> 它服务于 [experiment-design.md](../design/experiment-design.md) 中定义的 C4 目标，并细化 [experiment-protocol.md](../design/experiment-protocol.md) 中的执行协议。
> 本 runbook 的重点是先明确当前 repo 到底支持哪些表示层对照，哪些结论在实现上仍然缺口明显；并优先把成本最低的 `NL vs HTML` 子实验跑通。

---

## 1. C4 的目标与完成标准

### 1.1 要复现的论文结论

C4 包含两类子结论：

1. `code workflow` vs `text workflow`
   - 论文声称两者差异不大
2. `NL` vs `HTML` 环境表示
   - 论文声称 `Desc only` 优于加入 `HTML`

### 1.2 C4 需要的证据

至少需要：

- code workflow 与 text workflow 的并排结果
- `Desc only / HTML only / Desc + HTML` 的并排结果
- 统一指标：
  - `Element Acc`
  - `Action F1`
  - `Step SR`
  - `SR`

### 1.3 C4 的最低完成标准

满足以下条件时，C4 才可进入“已完成首轮复现”状态：

1. 至少完成一个网站的 `text workflow` 与 `code workflow` 对照
2. 至少完成一个网站的 `Desc only / HTML only / Desc + HTML` 对照
3. 每个条件都有逐样本 JSON 结果
4. 已形成 C4 表示层消融表

### 1.4 C4 的最低成功判据

对于 `code vs text workflow`：

- 两种 workflow 的核心指标接近
- 没有出现一方对另一方的稳定大幅优势

对于 `NL vs HTML`：

- `Desc only` 的 `Step SR` 不低于 `HTML only`
- `Desc + HTML` 不优于 `Desc only`，或方向一致地更差

---

## 2. Runbook 结构

本 runbook 分成 8 个阶段：

1. 固定工作目录
2. 当前代码实现审计
3. `code vs text workflow` 子实验口径
4. `NL vs HTML` 子实验口径
5. 当前实现缺口登记
6. 主结果表模板
7. 当前状态判定
8. 下一步

---

## 3. 阶段 0：固定工作目录

### 3.1 命令

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web
pwd
```

### 3.2 预期

```text
/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web
```

---

## 4. 阶段 1：当前代码实现审计

### 4.1 目标

先确认当前 repo 是否真的支持：

- `code workflow`
- `text workflow`
- `Desc only`
- `HTML only`
- `Desc + HTML`

### 4.2 现有可见入口

当前 repo 中已确认存在：

- `offline_induction.py`
- `online_induction.py`
- `rule_induction.py`
- `run_mind2web.py`
- `memory.py`
- `utils/env.py`

### 4.3 审计结果

当前 repo 中：

- `text workflow`：有
  - 现有所有 `*_wf.txt` 都属于 text workflow
- `code workflow`：现已补齐最小 prompt-level 转换闭环
  - 新增 `workflow_to_code.py`
  - 可把现有 LM text workflow 转成 code-style workflow prompt
- `Desc only / HTML only / Desc + HTML`：现已补齐
  - `run_mind2web.py` 新增 `--obs_mode`
  - 当前支持：
    - `desc_only`
    - `html_only`
    - `desc_html`

### 4.4 当前审计结论

截至目前，C4 的状态不是“全 blocked”，而是：

```text
first run completed
```

原因是：

- `code vs text workflow` 已具备首轮运行条件
- `NL/HTML` 三条件切换已经具备实验开关

---

## 5. 阶段 2：`code vs text workflow` 子实验口径

### 5.1 论文要求的条件

至少需要：

- baseline
- AWM text workflow
- AWM code workflow

### 5.2 当前 repo 实际情况

当前 repo 只具备：

- baseline
- AWM text workflow
- AWM code workflow（通过 code-style prompt 表示）

### 5.3 当前实现口径

当前 `code workflow` 的运行口径是：

1. 保留同一组 LM-induced workflow 的语义内容
2. 使用 `workflow_to_code.py` 将 text workflow 转成 code-style 函数表示
3. 在相同模型、相同网站、相同 benchmark 下比较：
   - `text_wf`
   - `code_wf`

这足以支持 C4 所需的首轮 `code vs text workflow` 表示层对照。

### 5.4 可直接复制的首轮命令（`kayak`）

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web

python workflow_to_code.py \
  --input_path workflow/kayak_lm_wf.txt \
  --output_path workflow/kayak_code_wf.txt

python run_mind2web.py \
  --domain Travel \
  --subdomain "Airlines" \
  --website kayak \
  --workflow_path workflow/kayak_lm_wf.txt \
  --model qwen/qwen3.5-397b-a17b \
  --benchmark test_task \
  --log_dir results \
  --suffix text_wf

python run_mind2web.py \
  --domain Travel \
  --subdomain "Airlines" \
  --website kayak \
  --workflow_path workflow/kayak_code_wf.txt \
  --model qwen/qwen3.5-397b-a17b \
  --benchmark test_task \
  --log_dir results \
  --suffix code_wf

python results/calc_score.py \
  --results_dir results/qwen/qwen3.5-397b-a17b/test_task/kayak/text_wf

python results/calc_score.py \
  --results_dir results/qwen/qwen3.5-397b-a17b/test_task/kayak/code_wf
```

---

## 6. 阶段 3：`NL vs HTML` 子实验口径

### 6.1 论文要求的条件

至少需要：

- `Desc only`
- `HTML only`
- `Desc + HTML`

### 6.2 当前 repo 实际情况

当前 repo 的 observation 构造逻辑主要在：

- `memory.py`
- `utils/env.py`

当前已新增显式参数：

```bash
python run_mind2web.py \
  ... \
  --obs_mode desc_only
```

支持三种值：

- `desc_only`
- `html_only`
- `desc_html`

### 6.3 当前可直接运行口径

建议首轮固定：

- `website=kayak`
- `domain=Travel`
- `subdomain=Airlines`
- `workflow_path=workflow/kayak_lm_wf.txt`
- `model=qwen/qwen3.5-397b-a17b`
- `benchmark=test_task`

这样可以把 workflow 本身固定住，只比较 observation 表示差异。

### 6.4 可直接复制的首轮命令

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web

python run_mind2web.py \
  --domain Travel \
  --subdomain "Airlines" \
  --website kayak \
  --workflow_path workflow/kayak_lm_wf.txt \
  --model qwen/qwen3.5-397b-a17b \
  --benchmark test_task \
  --log_dir results \
  --suffix desc_only \
  --obs_mode desc_only

python run_mind2web.py \
  --domain Travel \
  --subdomain "Airlines" \
  --website kayak \
  --workflow_path workflow/kayak_lm_wf.txt \
  --model qwen/qwen3.5-397b-a17b \
  --benchmark test_task \
  --log_dir results \
  --suffix html_only \
  --obs_mode html_only

python run_mind2web.py \
  --domain Travel \
  --subdomain "Airlines" \
  --website kayak \
  --workflow_path workflow/kayak_lm_wf.txt \
  --model qwen/qwen3.5-397b-a17b \
  --benchmark test_task \
  --log_dir results \
  --suffix desc_html \
  --obs_mode desc_html

python results/calc_score.py \
  --results_dir results/qwen/qwen3.5-397b-a17b/test_task/kayak/desc_only

python results/calc_score.py \
  --results_dir results/qwen/qwen3.5-397b-a17b/test_task/kayak/html_only

python results/calc_score.py \
  --results_dir results/qwen/qwen3.5-397b-a17b/test_task/kayak/desc_html
```

### 6.5 下一批优先网站

建议优先补：

1. `united`
   - `domain=Travel`
   - `subdomain=Airlines`
   - 已有 workflow：`workflow/united_lm_wf.txt`
2. `newegg`
   - `domain=Shopping`
   - `subdomain=Digital`
   - 已有 workflow：`workflow/newegg_lm_wf.txt`

理由：

- 两个网站都已在 C3 中生成过 `lm_wf`
- 可以直接复用 workflow，只比较 observation 表示
- 一个是 Travel 类，一个是 Shopping 类，足够判断 `kayak` 结果是不是单网站现象

### 6.6 可直接复制的 `united` 命令

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web

python run_mind2web.py \
  --domain Travel \
  --subdomain "Airlines" \
  --website united \
  --workflow_path workflow/united_lm_wf.txt \
  --model qwen/qwen3.5-397b-a17b \
  --benchmark test_task \
  --log_dir results \
  --suffix desc_only \
  --obs_mode desc_only

python run_mind2web.py \
  --domain Travel \
  --subdomain "Airlines" \
  --website united \
  --workflow_path workflow/united_lm_wf.txt \
  --model qwen/qwen3.5-397b-a17b \
  --benchmark test_task \
  --log_dir results \
  --suffix html_only \
  --obs_mode html_only

python run_mind2web.py \
  --domain Travel \
  --subdomain "Airlines" \
  --website united \
  --workflow_path workflow/united_lm_wf.txt \
  --model qwen/qwen3.5-397b-a17b \
  --benchmark test_task \
  --log_dir results \
  --suffix desc_html \
  --obs_mode desc_html

python results/calc_score.py \
  --results_dir results/qwen/qwen3.5-397b-a17b/test_task/united/desc_only

python results/calc_score.py \
  --results_dir results/qwen/qwen3.5-397b-a17b/test_task/united/html_only

python results/calc_score.py \
  --results_dir results/qwen/qwen3.5-397b-a17b/test_task/united/desc_html
```

### 6.7 可直接复制的 `newegg` 命令

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web

python run_mind2web.py \
  --domain Shopping \
  --subdomain "Digital" \
  --website newegg \
  --workflow_path workflow/newegg_lm_wf.txt \
  --model qwen/qwen3.5-397b-a17b \
  --benchmark test_task \
  --log_dir results \
  --suffix desc_only \
  --obs_mode desc_only

python run_mind2web.py \
  --domain Shopping \
  --subdomain "Digital" \
  --website newegg \
  --workflow_path workflow/newegg_lm_wf.txt \
  --model qwen/qwen3.5-397b-a17b \
  --benchmark test_task \
  --log_dir results \
  --suffix html_only \
  --obs_mode html_only

python run_mind2web.py \
  --domain Shopping \
  --subdomain "Digital" \
  --website newegg \
  --workflow_path workflow/newegg_lm_wf.txt \
  --model qwen/qwen3.5-397b-a17b \
  --benchmark test_task \
  --log_dir results \
  --suffix desc_html \
  --obs_mode desc_html

python results/calc_score.py \
  --results_dir results/qwen/qwen3.5-397b-a17b/test_task/newegg/desc_only

python results/calc_score.py \
  --results_dir results/qwen/qwen3.5-397b-a17b/test_task/newegg/html_only

python results/calc_score.py \
  --results_dir results/qwen/qwen3.5-397b-a17b/test_task/newegg/desc_html
```

---

## 7. 阶段 4：当前实现缺口登记

### 7.1 当前缺口表

| 子实验 | 论文需要 | 当前 repo 状态 | 当前判定 |
|------|------|------|------|
| code vs text workflow | baseline + text + code | 缺 code workflow 实现 | blocked |
| NL vs HTML | desc_only + html_only + desc_html | 已具备 obs_mode 切换 | running |

### 7.2 当前可直接写入状态表的说明

```text
C4 已进入部分可运行状态。当前 repo 已补齐 prompt-level `code workflow` 转换闭环，`code vs text workflow` 已可首跑；与此同时，`Desc only / HTML only / Desc + HTML` 的 observation mode 切换也已补齐，并已完成首轮跑分。
```

---

## 8. 阶段 5：主结果表

### 8.1 `code vs text workflow`

| website | condition | Element Acc | Action F1 | Step SR | SR |
|------|------|------:|------:|------:|------:|
| kayak | no_workflow | 53.6 | 64.9 | 51.2 | 0.0 |
| kayak | text_wf | 55.3 | 60.8 | 45.8 | 0.0 |
| kayak | code_wf | 52.4 | 63.4 | 48.0 | 0.0 |

### 8.2 `NL vs HTML`

| website | condition | Element Acc | Action F1 | Step SR | SR |
|------|------|------:|------:|------:|------:|
| kayak | desc_only | 54.8 | 61.2 | 45.3 | 0.0 |
| kayak | html_only | 52.4 | 63.5 | 48.0 | 0.0 |
| kayak | desc_html | 54.8 | 63.5 | 50.3 | 0.0 |
| united | desc_only | 57.9 | 61.9 | 55.9 | 33.3 |
| united | html_only | 61.2 | 64.5 | 60.6 | 33.3 |
| united | desc_html | 57.9 | 61.1 | 51.7 | 16.7 |
| newegg | desc_only | 42.0 | 44.3 | 30.5 | 0.0 |
| newegg | html_only | 36.2 | 42.6 | 23.9 | 0.0 |
| newegg | desc_html | 38.0 | 42.4 | 30.3 | 0.0 |

---

## 9. 阶段 6：当前状态判定

当前 C4 的正确状态应记为：

```text
first run completed
```

更具体地说：

- `code vs text workflow`：已完成一站点首轮运行
- `NL vs HTML`：已完成三站点首轮运行

### 9.1 当前执行记录：C4-R1（test_task / kayak / NL vs HTML）

本轮实际结果：

| website | condition | Element Acc | Action F1 | Step SR | SR |
|------|------|------:|------:|------:|------:|
| kayak | desc_only | 54.8 | 61.2 | 45.3 | 0.0 |
| kayak | html_only | 52.4 | 63.5 | 48.0 | 0.0 |
| kayak | desc_html | 54.8 | 63.5 | 50.3 | 0.0 |

本轮判定：

| run_id | sub_experiment | website | C4 status | evidence | notes |
|------|------|------|------|------|------|
| C4-R1 | NL vs HTML | kayak | not reproduced | `Desc only` 的 `Step SR` 低于 `HTML only`，且 `Desc + HTML` 高于 `Desc only` | 当前首轮结果方向与论文主张相反 |

建议写入状态表的说明：

```text
在 test_task / kayak 的首轮 C4（NL vs HTML）实验中，Desc only 的 Step SR 低于 HTML only，而 Desc + HTML 又高于 Desc only，因此本轮不支持“仅用 NL 描述优于加入 HTML”的结论，记为 not reproduced。
```

### 9.2 当前执行记录：C4-R2（test_task / united / NL vs HTML）

本轮实际结果：

| website | condition | Element Acc | Action F1 | Step SR | SR |
|------|------|------:|------:|------:|------:|
| united | desc_only | 57.9 | 61.9 | 55.9 | 33.3 |
| united | html_only | 61.2 | 64.5 | 60.6 | 33.3 |
| united | desc_html | 57.9 | 61.1 | 51.7 | 16.7 |

本轮判定：

| run_id | sub_experiment | website | C4 status | evidence | notes |
|------|------|------|------|------|------|
| C4-R2 | NL vs HTML | united | not reproduced | `Desc only` 的 `Step SR` 低于 `HTML only`，且 `Desc + HTML` 明显低于两者 | 当前结果同样不支持论文主张 |

建议写入状态表的说明：

```text
在 test_task / united 的首轮 C4（NL vs HTML）实验中，Desc only 的 Step SR 低于 HTML only，而 Desc + HTML 进一步下降到 51.7，因此本轮同样不支持“仅用 NL 描述优于加入 HTML”的结论，记为 not reproduced。
```

### 9.3 当前执行记录：C4-R3（test_task / newegg / NL vs HTML）

本轮实际结果：

| website | condition | Element Acc | Action F1 | Step SR | SR |
|------|------|------:|------:|------:|------:|
| newegg | desc_only | 42.0 | 44.3 | 30.5 | 0.0 |
| newegg | html_only | 36.2 | 42.6 | 23.9 | 0.0 |
| newegg | desc_html | 38.0 | 42.4 | 30.3 | 0.0 |

本轮判定：

| run_id | sub_experiment | website | C4 status | evidence | notes |
|------|------|------|------|------|------|
| C4-R3 | NL vs HTML | newegg | not reproduced | `Desc only` 在 `Step SR` 上高于 `HTML only`，但 `Desc + HTML` 仍未劣于 `Desc only` 的幅度不足以支持论文结论 | 当前结果仍不构成论文所需的稳定方向 |

建议写入状态表的说明：

```text
在 test_task / newegg 的首轮 C4（NL vs HTML）实验中，Desc only 的 Step SR 高于 HTML only，但 Desc + HTML 与 Desc only 基本持平，未形成论文所要求的稳定收益结构。因此，本轮仍不支持“仅用 NL 描述优于加入 HTML”的结论，记为 not reproduced。
```

### 9.4 当前执行记录：C4-R4（test_task / kayak / code vs text workflow）

本轮实际结果：

| website | condition | Element Acc | Action F1 | Step SR | SR |
|------|------|------:|------:|------:|------:|
| kayak | text_wf | 55.3 | 60.8 | 45.8 | 0.0 |
| kayak | code_wf | 52.4 | 63.4 | 48.0 | 0.0 |

本轮判定：

| run_id | sub_experiment | website | C4 status | evidence | notes |
|------|------|------|------|------|------|
| C4-R4 | code vs text workflow | kayak | reproduced | `Element Acc`、`Action F1`、`Step SR` 各有小幅差异，但 `SR` 持平且未出现单边稳定大幅优势 | 在当前 prompt-level code 表示口径下，符合“差异不大”的最低成功判据 |

建议写入状态表的说明：

```text
在 test_task / kayak 的首轮 C4（code vs text workflow）实验中，text workflow 与 code workflow 在 Element Acc、Action F1、Step SR 上存在小幅波动，但 SR 同为 0.0，且未出现单边稳定大幅优势。因此，在当前 prompt-level code 表示口径下，本轮支持“code workflow 与 text workflow 差异不大”的结论，记为 reproduced。
```

### 9.5 当前阶段性结论

当前 C4 的更准确状态是：

```text
first run completed; NL/HTML not reproduced after three-site first run; code/text reproduced on one-site first run
```

这表示：

- `NL vs HTML` 子实验已经有了三站点结果
- 三轮结果都不足以支持论文结论
- `code vs text workflow` 子实验已在 `kayak` 上完成首轮，并支持“差异不大”

### 9.6 当前归档记录

#### C4-R1（test_task / kayak / NL vs HTML）

| artifact | path | status | note |
|------|------|------|------|
| workflow | `workflow/kayak_lm_wf.txt` | ready | 固定 text workflow |
| desc_only results | `results/qwen/qwen3.5-397b-a17b/test_task/kayak/desc_only/` | ready | 正式结果目录 |
| html_only results | `results/qwen/qwen3.5-397b-a17b/test_task/kayak/html_only/` | ready | 正式结果目录 |
| desc_html results | `results/qwen/qwen3.5-397b-a17b/test_task/kayak/desc_html/` | ready | 正式结果目录 |
| C4 judgment | manual log | ready | 当前判定为 `not reproduced` |

建议手工补一条归档摘要：

```text
C4-R1 / test_task / kayak / NL vs HTML 已归档。当前结果显示 Desc only 的 Step SR 低于 HTML only，而 Desc + HTML 又高于 Desc only，因此本轮不支持论文中“仅用 NL 描述优于加入 HTML”的结论。
```

#### C4-R2（test_task / united / NL vs HTML）

| artifact | path | status | note |
|------|------|------|------|
| workflow | `workflow/united_lm_wf.txt` | ready | 固定 text workflow |
| desc_only results | `results/qwen/qwen3.5-397b-a17b/test_task/united/desc_only/` | ready | 正式结果目录 |
| html_only results | `results/qwen/qwen3.5-397b-a17b/test_task/united/html_only/` | ready | 正式结果目录 |
| desc_html results | `results/qwen/qwen3.5-397b-a17b/test_task/united/desc_html/` | ready | 正式结果目录 |
| C4 judgment | manual log | ready | 当前判定为 `not reproduced` |

建议手工补一条归档摘要：

```text
C4-R2 / test_task / united / NL vs HTML 已归档。当前结果显示 Desc only 的 Step SR 低于 HTML only，而 Desc + HTML 又进一步下降，因此本轮同样不支持论文中“仅用 NL 描述优于加入 HTML”的结论。
```

#### C4-R3（test_task / newegg / NL vs HTML）

| artifact | path | status | note |
|------|------|------|------|
| workflow | `workflow/newegg_lm_wf.txt` | ready | 固定 text workflow |
| desc_only results | `results/qwen/qwen3.5-397b-a17b/test_task/newegg/desc_only/` | ready | 正式结果目录 |
| html_only results | `results/qwen/qwen3.5-397b-a17b/test_task/newegg/html_only/` | ready | 正式结果目录 |
| desc_html results | `results/qwen/qwen3.5-397b-a17b/test_task/newegg/desc_html/` | ready | 正式结果目录 |
| C4 judgment | manual log | ready | 当前判定为 `not reproduced` |

建议手工补一条归档摘要：

```text
C4-R3 / test_task / newegg / NL vs HTML 已归档。当前结果显示 Desc only 虽高于 HTML only，但 Desc + HTML 与 Desc only 基本持平，整体仍未形成论文要求的稳定收益结构，因此本轮仍记为 not reproduced。
```

#### C4-R4（test_task / kayak / code vs text workflow）

| artifact | path | status | note |
|------|------|------|------|
| text workflow | `workflow/kayak_lm_wf.txt` | ready | LM text workflow |
| code workflow | `workflow/kayak_code_wf.txt` | ready | 由 `workflow_to_code.py` 转换生成 |
| text_wf results | `results/qwen/qwen3.5-397b-a17b/test_task/kayak/text_wf/` | ready | 正式结果目录 |
| code_wf results | `results/qwen/qwen3.5-397b-a17b/test_task/kayak/code_wf/` | ready | 正式结果目录 |
| C4 judgment | manual log | ready | 当前判定为 `reproduced` |

建议手工补一条归档摘要：

```text
C4-R4 / test_task / kayak / code vs text workflow 已归档。当前结果显示 text workflow 与 code workflow 在主要指标上仅有小幅波动，SR 持平，未出现单边稳定大幅优势。因此，在当前 prompt-level code 表示口径下，本轮支持“code workflow 与 text workflow 差异不大”的结论。
```

---

## 10. 阶段 7：下一步

当前最合理的推进顺序：

1. `NL vs HTML` 的三站点结果已完成
2. 先冻结 `NL vs HTML` 子结论
3. `code vs text workflow` 已完成首轮，可决定是否补第二个网站
4. 若要收尾 C4，优先冻结当前阶段性结论

### 10.1 当前建议

从工程成本看，当前最合理的下一步是先冻结 C4 的当前阶段性结论，因为：

- 三个网站的首轮结果都未支持论文结论
- `kayak` 与 `united` 明确呈现反方向
- `newegg` 虽不完全反向，但也没有形成论文要求的稳定收益结构
- `code/text workflow` 已在 `kayak` 上给出一个支持“差异不大”的首轮信号

### 10.2 当前可直接写入状态表的说明

```text
C4 首轮已完成。`NL vs HTML` 已在 kayak、united、newegg 三个网站上完成首轮运行，现有结果不足以支持论文所声称的“Desc only 优于 HTML only”，因此该子结论可先冻结为 not reproduced。与此同时，`code vs text workflow` 已在 kayak 上完成首轮对照，并在当前 prompt-level code 表示口径下支持“差异不大”的结论。下一步可根据时间决定是否再补第二个网站，否则可先冻结 C4 的阶段性结论。
```
