# C2 Runbook: Online AWM 泛化结果复现

> 本文档是 C2 的可执行 runbook。
> 它服务于 [experiment-design.md](../design/experiment-design.md) 中定义的 C2 目标，并细化 [experiment-protocol.md](../design/experiment-protocol.md) 中的执行协议。
> 本 runbook 的目标是把 C2 拆成可执行阶段，并明确当前代码库下哪些结论可以直接跑、哪些需要标记为实现约束，而不是在执行时临时猜测口径。

---

## 1. C2 的目标与完成标准

### 1.1 要复现的论文结论

- online 在 `cross-task`、`cross-website`、`cross-domain` 上优于基线
- 随着 distribution gap 增大，online 相对 offline 更有优势
- offline 在分布较匹配时可保持竞争力

### 1.2 C2 需要的证据

至少需要以下结果：

- `cross-task / cross-website / cross-domain` 三档结果
- baseline、offline AWM、online AWM 的并排结果
- 对 split 间趋势的解释，而不是只看单个数字

### 1.3 C2 的最低完成标准

满足以下条件时，C2 可进入“已完成首轮复现”状态：

1. 至少完成一个 split 的 baseline 与 online AWM 成对实验
2. 若该 split 的 offline AWM 在当前代码口径下可定义，也完成 offline 对照
3. 所有已运行条件都保留逐样本 JSON 结果
4. 已形成按 split 组织的分数表
5. 已明确区分：
   - 结果性结论
   - 实现约束导致的缺口

### 1.4 C2 的最低成功判据

满足以下条件之一，可视为较强复现信号：

- online 相对 baseline 在三个 split 上都方向一致地更好
- online 相对 offline 的优势在更大 gap 的 split 上更明显
- offline 与 online 在 `cross-task` 上接近，而在 `cross-website` / `cross-domain` 上差异拉开

---

## 2. Runbook 结构

本 runbook 分成 9 个阶段：

1. 固定工作目录
2. 环境与输入检查
3. 代码口径与实现约束确认
4. split 级运行策略冻结
5. `cross-task` 运行
6. `cross-website` 运行
7. `cross-domain` 运行
8. 打分、判定与主结果表
9. 归档与下一步

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

## 4. 阶段 1：环境与输入检查

### 4.1 目标

确认 C2 所需的数据、依赖、鉴权和 C1 遗留产物可用。

### 4.2 必须具备的输入

- `data/test_task/*.json`
- `data/test_website/*.json`
- `data/test_domain/*.json`
- OpenAI 可用鉴权环境变量
- `pipeline.py`
- `online_induction.py`
- `run_mind2web.py`

### 4.3 命令

```bash
python -V
python -c "import openai; print(openai.__version__)"
find data/test_task -maxdepth 1 -name '*.json' | wc -l
find data/test_website -maxdepth 1 -name '*.json' | wc -l
find data/test_domain -maxdepth 1 -name '*.json' | wc -l
python -c "import os; print(bool(os.environ.get('OPENAI_API_KEY') or os.environ.get('API_KEY')))"
```

### 4.4 验收点

- 三个 split 的文件数都大于 0
- OpenAI 鉴权检查输出 `True`

---

## 5. 阶段 2：代码口径与实现约束确认

### 5.1 当前代码入口

- `run_mind2web.py`
  - 按 `benchmark + website` 运行单网站测试
- `online_induction.py`
  - 从当前测试过程的结果中归纳 online workflow
- `pipeline.py`
  - 能把 inference 与 online induction 串起来
- `offline_induction.py`
  - 从 `train` 中按 `domain / subdomain / website` 归纳 offline workflow

### 5.2 当前实现约束

当前仓库下，`offline_induction.py` 是按网站从 `train` 归纳 workflow。

这意味着：

- `cross-task`：
  - 适合同时比较 baseline / offline / online
- `cross-website`：
  - 若目标网站不在 `train` 中，则无法按当前脚本定义“同网站 offline induction”
- `cross-domain`：
  - 同理，很多目标网站不在 `train` 中，无法直接按 C1 的方式构造 offline workflow

### 5.3 运行原则

因此在 C2 中要明确区分两种情况：

1. 当前代码口径下可直接运行：
   - baseline
   - online
   - 以及 `cross-task` 上的 offline
2. 当前代码口径下不能直接定义的 offline 比较：
   - 不要临时发明 workaround
   - 在结果表中记为 `not available in current repo setup`

这不是研究结论，而是实现约束。

---

## 6. 阶段 3：split 级运行策略冻结

### 6.1 C2 当前执行策略

按 split 组织：

| split | baseline | offline | online | status |
|------|------|------|------|------|
| `test_task` | yes | yes | yes | 直接可跑 |
| `test_website` | yes | repo 口径下通常不可直接定义 | yes | 标记实现约束 |
| `test_domain` | yes | repo 口径下通常不可直接定义 | yes | 标记实现约束 |

### 6.2 为什么这样组织

- 符合当前脚本能力
- 不把 repo 没有实现的对照强行伪造出来
- 仍然能先复现 C2 最关键的趋势部分：
  - online 是否比 baseline 更稳
  - 在更大 distribution gap 的 split 上是否更有优势

### 6.3 当前优先网站

为保证命令可直接复制，先选每个 split 一个代表网站做首轮：

| split | website | domain | subdomain | count |
|------|------|------|------|------:|
| `test_task` | `kayak` | Travel | Airlines | 6 |
| `test_website` | `tripadvisor` | Travel | Restaurant | 23 |
| `test_domain` | `reddit` | Info | Social media | 33 |

说明：

- `kayak` 已在 C1 中跑过，便于复用 baseline/offline 口径
- `tripadvisor` 与 `reddit` 在对应 split 中样本较多，适合作为首轮 online pilot

---

## 7. 阶段 4：`cross-task` 运行

### 7.1 目标

在 `test_task` 上形成 baseline / offline / online 三者并排结果。

### 7.2 推荐首轮网站

- `website=kayak`
- `domain=Travel`
- `subdomain=Airlines`

### 7.3 当前口径

- baseline：直接运行
- offline：可直接复用 C1 同网站命令
- online：用 `pipeline.py --setup online` 串联运行

### 7.3.1 Online 执行原则

当前 `pipeline.py` 已支持：

- 子步骤失败自动重试
- 失败后停止，而不是跳到下一步
- 基于 checkpoint 的 `--resume` 续跑

因此：

- 首次启动时，如果存在旧的 partial online 产物，先清理
- 一旦本轮已开始，后续不要手工删中间产物
- 若中断，直接重复同一条 `python pipeline.py ... --resume` 命令即可

### 7.4 可直接复制运行的命令

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web

python run_mind2web.py \
  --domain Travel \
  --subdomain "Airlines" \
  --website kayak \
  --workflow_path workflow/_empty.txt \
  --model gpt-4o \
  --benchmark test_task \
  --suffix no_workflow

python run_mind2web.py \
  --domain Travel \
  --subdomain "Airlines" \
  --website kayak \
  --workflow_path workflow/kayak_offline_wf.txt \
  --model gpt-4o \
  --benchmark test_task \
  --suffix offline_wf

touch workflow/kayak_online_wf.txt
rm -f workflow/kayak_online_wf.txt.checkpoint
rm -rf results/gpt-4o/test_task/kayak/online_wf

python pipeline.py \
  --setup online \
  --benchmark test_task \
  --domain Travel \
  --subdomain "Airlines" \
  --website kayak \
  --workflow_path workflow/kayak_online_wf.txt \
  --results_dir results/gpt-4o/test_task/kayak/online_wf \
  --model gpt-4o \
  --induce_steps 1 \
  --command_retries 2 \
  --retry_delay 5 \
  --resume

python results/calc_score.py \
  --results_dir results/gpt-4o/test_task/kayak/no_workflow

python results/calc_score.py \
  --results_dir results/gpt-4o/test_task/kayak/offline_wf

python results/calc_score.py \
  --results_dir results/gpt-4o/test_task/kayak/online_wf
```

如果中途中断，直接重复下面这一条，不要清理：

```bash
python pipeline.py \
  --setup online \
  --benchmark test_task \
  --domain Travel \
  --subdomain "Airlines" \
  --website kayak \
  --workflow_path workflow/kayak_online_wf.txt \
  --results_dir results/gpt-4o/test_task/kayak/online_wf \
  --model gpt-4o \
  --induce_steps 1 \
  --command_retries 2 \
  --retry_delay 5 \
  --resume
```

### 7.5 需要记录的输出

- `Element Acc`
- `Action F1`
- `Step SR`
- `SR`

---

## 8. 阶段 5：`cross-website` 运行

### 8.1 目标

在 `test_website` 上先验证 online 相对 baseline 的表现。

### 8.2 推荐首轮网站

- `website=tripadvisor`
- `domain=Travel`
- `subdomain=Restaurant`

### 8.3 当前口径

- baseline：可直接运行
- online：可直接运行
- offline：当前 repo 口径下通常不可直接定义为“同网站 offline induction from train”

### 8.4 可直接复制运行的命令

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web

python run_mind2web.py \
  --domain Travel \
  --subdomain "Restaurant" \
  --website tripadvisor \
  --workflow_path workflow/_empty.txt \
  --model gpt-4o \
  --benchmark test_website \
  --suffix no_workflow

touch workflow/tripadvisor_online_wf.txt
rm -f workflow/tripadvisor_online_wf.txt.checkpoint
rm -rf results/gpt-4o/test_website/tripadvisor/online_wf

python pipeline.py \
  --setup online \
  --benchmark test_website \
  --domain Travel \
  --subdomain "Restaurant" \
  --website tripadvisor \
  --workflow_path workflow/tripadvisor_online_wf.txt \
  --results_dir results/gpt-4o/test_website/tripadvisor/online_wf \
  --model gpt-4o \
  --induce_steps 1 \
  --command_retries 2 \
  --retry_delay 5 \
  --resume

python results/calc_score.py \
  --results_dir results/gpt-4o/test_website/tripadvisor/no_workflow

python results/calc_score.py \
  --results_dir results/gpt-4o/test_website/tripadvisor/online_wf
```

如果中途中断，直接重复下面这一条，不要清理：

```bash
python pipeline.py \
  --setup online \
  --benchmark test_website \
  --domain Travel \
  --subdomain "Restaurant" \
  --website tripadvisor \
  --workflow_path workflow/tripadvisor_online_wf.txt \
  --results_dir results/gpt-4o/test_website/tripadvisor/online_wf \
  --model gpt-4o \
  --induce_steps 1 \
  --command_retries 2 \
  --retry_delay 5 \
  --resume
```

### 8.5 结果登记要求

在 `test_website` 首轮表里显式写：

- baseline：已运行
- online：已运行
- offline：`not available in current repo setup`

---

## 9. 阶段 6：`cross-domain` 运行

### 9.1 目标

在 `test_domain` 上先验证 online 相对 baseline 的表现。

### 9.2 推荐首轮网站

- `website=reddit`
- `domain=Info`
- `subdomain=Social media`

### 9.3 当前口径

- baseline：可直接运行
- online：可直接运行
- offline：当前 repo 口径下通常不可直接定义为“同网站 offline induction from train”

### 9.4 可直接复制运行的命令

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web

python run_mind2web.py \
  --domain Info \
  --subdomain "Social media" \
  --website reddit \
  --workflow_path workflow/_empty.txt \
  --model gpt-4o \
  --benchmark test_domain \
  --suffix no_workflow

touch workflow/reddit_online_wf.txt
rm -f workflow/reddit_online_wf.txt.checkpoint
rm -rf results/gpt-4o/test_domain/reddit/online_wf

python pipeline.py \
  --setup online \
  --benchmark test_domain \
  --domain Info \
  --subdomain "Social media" \
  --website reddit \
  --workflow_path workflow/reddit_online_wf.txt \
  --results_dir results/gpt-4o/test_domain/reddit/online_wf \
  --model gpt-4o \
  --induce_steps 1 \
  --command_retries 2 \
  --retry_delay 5 \
  --resume

python results/calc_score.py \
  --results_dir results/gpt-4o/test_domain/reddit/no_workflow

python results/calc_score.py \
  --results_dir results/gpt-4o/test_domain/reddit/online_wf
```

如果中途中断，直接重复下面这一条，不要清理：

```bash
python pipeline.py \
  --setup online \
  --benchmark test_domain \
  --domain Info \
  --subdomain "Social media" \
  --website reddit \
  --workflow_path workflow/reddit_online_wf.txt \
  --results_dir results/gpt-4o/test_domain/reddit/online_wf \
  --model gpt-4o \
  --induce_steps 1 \
  --command_retries 2 \
  --retry_delay 5 \
  --resume
```

### 9.5 结果登记要求

在 `test_domain` 首轮表里显式写：

- baseline：已运行
- online：已运行
- offline：`not available in current repo setup`

---

## 10. 阶段 7：打分、判定与主结果表

### 10.1 单轮登记模板

| split | website | condition | Element Acc | Action F1 | Step SR | SR |
|------|------|------|------:|------:|------:|------:|
| test_task | kayak | no_workflow |  |  |  |  |
| test_task | kayak | offline_wf |  |  |  |  |
| test_task | kayak | online_wf |  |  |  |  |

### 10.2 C2 主结果表模板

| split | website | baseline | offline | online | C2 status | notes |
|------|------|------|------|------|------|------|
| test_task | kayak |  |  |  |  |  |
| test_website | tripadvisor |  | N/A |  |  | offline unavailable in current repo setup |
| test_domain | reddit |  | N/A |  |  | offline unavailable in current repo setup |

### 10.3 C2 状态标签

- `reproduced`
- `not reproduced`
- `unclear`
- `blocked by current repo setup`

### 10.4 当前判定规则

填 `reproduced`：

- online 相对 baseline 明显更好
- 且 split 间趋势与论文解释一致

填 `not reproduced`：

- online 相对 baseline 无改善或方向相反

填 `unclear`：

- 指标混合
- split 级趋势未站稳

填 `blocked by current repo setup`：

- 当前代码下论文要求的对照无法按同口径构造

### 10.5 当前执行记录：C2-R1（test_task / kayak）

本轮实际结果：

| split | website | condition | Element Acc | Action F1 | Step SR | SR |
|------|------|------|------:|------:|------:|------:|
| test_task | kayak | no_workflow | 50.3 | 59.4 | 47.9 | 0.0 |
| test_task | kayak | offline_wf | 55.9 | 61.2 | 53.5 | 0.0 |
| test_task | kayak | online_wf | 54.7 | 62.4 | 53.5 | 0.0 |

本轮判定：

| run_id | split | website | C2 status | evidence | notes |
|------|------|------|------|------|------|
| C2-R1 | test_task | kayak | reproduced | online 相对 baseline 在 `Element Acc`、`Action F1`、`Step SR` 上均更好，且 online 与 offline 在 `cross-task` 上接近 | 当前仅是 `test_task` 单网站首轮信号，不等同于整体 C2 已复现 |

建议写入状态表的说明：

```text
在 test_task / kayak 的首轮实验中，online AWM 相对 baseline 在 Element Acc、Action F1 与 Step SR 上均提升，且 online 与 offline 的表现接近，因此本轮将 C2 记为 reproduced。
```

### 10.6 C2 主结果表（当前版本）

| split | website | baseline | offline | online | C2 status | notes |
|------|------|------|------|------|------|------|
| test_task | kayak | complete | complete | complete | reproduced | online > baseline, online ~= offline |
| test_website | tripadvisor | complete | N/A | complete | not reproduced | online < baseline on all four metrics; offline unavailable in current repo setup |
| test_domain | reddit | complete | N/A | complete | not reproduced | online < baseline on all four metrics; offline unavailable in current repo setup |

### 10.7 当前审核备注

对于 `test_task / kayak`，当前存在两个目录：

- 正式目录：`results/gpt-4o/test_task/kayak/online_wf`
- 废弃目录：`results/gpt-4o/test_task/kayak/workflow`

其中：

- `online_wf` 才是本轮 C2 正式结果目录
- `workflow` 是修复 `pipeline.py` 之前的 bug 遗留目录，不纳入 C2 结果表

对于 `test_website / tripadvisor`，当前正式结果目录为：

- baseline：`results/qwen/qwen3.5-397b-a17b/test_website/tripadvisor/no_workflow/`
- online：`results/qwen/qwen3.5-397b-a17b/test_website/tripadvisor/online_wf/`

其中：

- `online_wf` 目录下现有 `23` 个逐样本结果 JSON
- `_pipeline_state.json` 是 pipeline 状态文件，不计入样本数

对于 `test_domain / reddit`，当前正式结果目录为：

- baseline：`results/qwen/qwen3.5-397b-a17b/test_domain/reddit/no_workflow/`
- online：`results/qwen/qwen3.5-397b-a17b/test_domain/reddit/online_wf/`

其中：

- `online_wf` 目录下现有 `33` 个逐样本结果 JSON
- `_pipeline_state.json` 是 pipeline 状态文件，不计入样本数

### 10.8 当前执行记录：C2-R2（test_website / tripadvisor）

本轮实际结果：

| split | website | condition | Element Acc | Action F1 | Step SR | SR |
|------|------|------|------:|------:|------:|------:|
| test_website | tripadvisor | no_workflow | 47.0 | 56.9 | 43.9 | 4.3 |
| test_website | tripadvisor | online_wf | 37.0 | 52.0 | 32.1 | 0.0 |

本轮判定：

| run_id | split | website | C2 status | evidence | notes |
|------|------|------|------|------|------|
| C2-R2 | test_website | tripadvisor | not reproduced | online 相对 baseline 在 `Element Acc`、`Action F1`、`Step SR`、`SR` 上均更差 | 当前比较已按同模型 `qwen/qwen3.5-397b-a17b` 完成，offline 仍按 repo 约束记为 N/A |

建议写入状态表的说明：

```text
在 test_website / tripadvisor 的首轮实验中，online AWM 相对 baseline 在 Element Acc、Action F1、Step SR 与 SR 上均下降，因此本轮将 C2 记为 not reproduced。
```

### 10.9 当前执行记录：C2-R3（test_domain / reddit）

本轮实际结果：

| split | website | condition | Element Acc | Action F1 | Step SR | SR |
|------|------|------|------:|------:|------:|------:|
| test_domain | reddit | no_workflow | 58.8 | 63.3 | 53.0 | 9.1 |
| test_domain | reddit | online_wf | 55.6 | 62.6 | 50.8 | 6.1 |

本轮判定：

| run_id | split | website | C2 status | evidence | notes |
|------|------|------|------|------|------|
| C2-R3 | test_domain | reddit | not reproduced | online 相对 baseline 在 `Element Acc`、`Action F1`、`Step SR`、`SR` 上均更差 | 当前比较已按同模型 `qwen/qwen3.5-397b-a17b` 完成，offline 仍按 repo 约束记为 N/A |

建议写入状态表的说明：

```text
在 test_domain / reddit 的首轮实验中，online AWM 相对 baseline 在 Element Acc、Action F1、Step SR 与 SR 上均下降，因此本轮将 C2 记为 not reproduced。
```

---

## 11. 阶段 8：归档与下一步

### 11.1 最低归档要求

至少保留：

- online workflow 文本
- baseline 结果 JSON
- online 结果 JSON
- 若可定义则保留 offline 结果 JSON
- C2 主结果表
- split 级判定

### 11.1.1 当前归档记录：C2-R1（test_task / kayak）

本轮应归档为：

| artifact | path | status | note |
|------|------|------|------|
| online workflow | `workflow/kayak_online_wf.txt` | ready | 当前 online workflow 文本 |
| baseline results | `results/gpt-4o/test_task/kayak/no_workflow/` | ready | 正式结果目录 |
| offline results | `results/gpt-4o/test_task/kayak/offline_wf/` | ready | 正式结果目录 |
| online results | `results/gpt-4o/test_task/kayak/online_wf/` | ready | 正式结果目录，现有 6 个 JSON |
| deprecated results | `results/gpt-4o/test_task/kayak/workflow/` | deprecated | bug 修复前遗留目录，不纳入正式结果 |
| C2 judgment | manual log | ready | 当前判定为 `reproduced` |

建议手工补一条归档摘要：

```text
C2-R1 / test_task / kayak 已归档。online AWM 相对 baseline 在 Element Acc、Action F1 与 Step SR 上均提升，且与 offline 表现接近，因此本轮记为 reproduced。旧目录 results/.../workflow 为 bug 遗留产物，不纳入正式结果。
```

### 11.1.2 当前归档记录：C2-R2（test_website / tripadvisor）

本轮应归档为：

| artifact | path | status | note |
|------|------|------|------|
| online workflow | `workflow/tripadvisor_online_wf_qwen35.txt` | ready | 当前 online workflow 文本 |
| baseline results | `results/qwen/qwen3.5-397b-a17b/test_website/tripadvisor/no_workflow/` | ready | 正式结果目录 |
| online results | `results/qwen/qwen3.5-397b-a17b/test_website/tripadvisor/online_wf/` | ready | 正式结果目录，现有 23 个样本 JSON，另含 `_pipeline_state.json` |
| offline results | N/A | N/A | 当前 repo 口径下不直接定义 |
| C2 judgment | manual log | ready | 当前判定为 `not reproduced` |

建议手工补一条归档摘要：

```text
C2-R2 / test_website / tripadvisor 已归档。online AWM 相对 baseline 在 Element Acc、Action F1、Step SR 与 SR 上均下降，因此本轮记为 not reproduced。online_wf 目录中的 _pipeline_state.json 为 pipeline 状态文件，不纳入样本统计。
```

### 11.1.3 当前归档记录：C2-R3（test_domain / reddit）

本轮应归档为：

| artifact | path | status | note |
|------|------|------|------|
| online workflow | `workflow/reddit_online_wf_qwen35.txt` | ready | 当前 online workflow 文本 |
| baseline results | `results/qwen/qwen3.5-397b-a17b/test_domain/reddit/no_workflow/` | ready | 正式结果目录 |
| online results | `results/qwen/qwen3.5-397b-a17b/test_domain/reddit/online_wf/` | ready | 正式结果目录，现有 33 个样本 JSON，另含 `_pipeline_state.json` |
| offline results | N/A | N/A | 当前 repo 口径下不直接定义 |
| C2 judgment | manual log | ready | 当前判定为 `not reproduced` |

建议手工补一条归档摘要：

```text
C2-R3 / test_domain / reddit 已归档。online AWM 相对 baseline 在 Element Acc、Action F1、Step SR 与 SR 上均下降，因此本轮记为 not reproduced。online_wf 目录中的 _pipeline_state.json 为 pipeline 状态文件，不纳入样本统计。
```

### 11.2 当前推荐推进顺序

1. `test_task / kayak` 已归档
2. `test_website / tripadvisor` 已归档
3. `test_domain / reddit` 已归档
4. 汇总首轮 C2 主结果表
5. 再决定是否扩展更多网站

### 11.3 阶段性结论应该怎么写

首轮 C2 结束后，结论应同时回答两件事：

1. online 相对 baseline 的方向是否成立
2. 当前 repo 是否真的支持论文所需的 offline 对照

不要把“代码里没法严格构造 offline 对照”误写成研究结论。

### 11.3.1 当前可直接引用的阶段性结论

建议写入状态表的版本：

```text
C2 首轮已完成三个 split 的 baseline / online 对比。结果显示：online AWM 仅在 test_task / kayak 上优于 baseline，而在 test_website / tripadvisor 与 test_domain / reddit 上均低于 baseline。因此，当前结果不支持“online AWM 在更大 distribution gap 下稳定优于 baseline”的结论。更准确的表述是：C2 首轮证据呈 mixed，但整体方向偏向 not reproduced。
```

建议写入周报或汇报的版本：

```text
在当前 repo 口径下，我们完成了 C2 的首轮 split-level 复现。online AWM 在 cross-task（kayak）上表现为 reproduced，但在 cross-website（tripadvisor）与 cross-domain（reddit）上均未超过 baseline。基于这三组结果，现阶段不能支持论文中“online AWM 在更大 distribution gap 下更具优势”的主张。需要注意的是，cross-website 与 cross-domain 的 offline 对照在当前代码库中无法按同口径直接构造，因此当前结论主要针对 online 相对 baseline 的趋势，而不是对 online/offline 差异的完整复现。
```

### 11.3.2 当前最合理的下一步

1. 先冻结首轮 C2 结果，不再继续扩网站
2. 单独整理一页 `C2` 状态摘要，引用 10.6 的主结果表和上面的阶段性结论
3. 若还要继续深挖，优先转到：
   - 分析为什么 `tripadvisor` / `reddit` 上 online 退化
   - 或进入 `C3`
