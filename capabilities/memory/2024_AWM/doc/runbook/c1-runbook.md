# C1 Runbook: Mind2Web Offline Cross-Task 主结果复现

> 本文档是 C1 的可执行 runbook。
> 它服务于 [experiment-design.md](../design/experiment-design.md) 中定义的 C1 目标，并细化 [experiment-protocol.md](../design/experiment-protocol.md) 中的执行协议。
> 本 runbook 的目标不是覆盖全部 C1 变体，而是确保你能按统一流程、统一命名、统一验收口径，稳定产出一组可以进入“论文结论复现状态表”的结果。

---

## 1. C1 的目标与完成标准

### 1.1 要复现的论文结论

- Offline AWM 在 Mind2Web `cross-task` 上优于对应 baseline
- 提升主要体现在 `Element Acc` 与 `Step SR`
- `Action F1` 不一定同步提升

### 1.2 C1 的最低完成标准

满足以下条件时，C1 可进入“已完成首轮复现”状态：

1. 至少完成一个网站的 baseline 与 offline AWM 成对实验
2. 两个条件都有完整逐样本 JSON 结果
3. 两个条件都完成统一脚本打分
4. 已对 `Element Acc / Action F1 / Step SR / SR` 做并排比较
5. 已给出本轮的“复现成功 / 未成功 / 暂不确定”判断

### 1.3 C1 的正式成功判据

满足以下任意两条，可初步视为 C1 复现成功：

- offline AWM 在 `Step SR` 上优于 baseline
- offline AWM 在 `Element Acc` 上优于 baseline
- 提升结构与论文一致，即收益主要来自元素选择而不是动作 F1

---

## 2. Runbook 结构

本 runbook 分成 11 个阶段：

1. 固定工作目录
2. 环境与输入检查
3. 运行单位选择
4. 命名与目录冻结
5. Offline workflow induction
6. Baseline inference
7. Offline AWM inference
8. 统一打分
9. C1 结果判定
10. 归档
11. 从单网站扩展到正式 C1

每个阶段都包含：

- 目标
- 输入
- 命令
- 产物
- 验收点
- 失败时怎么处理

---

## 3. 阶段 0：固定工作目录

### 3.1 目标

确保后续所有相对路径都在正确根目录下执行。

### 3.2 命令

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web
pwd
```

### 3.3 预期

输出应为：

```text
/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web
```

### 3.4 验收点

- 当前目录必须是 `experiments/mind2web`

### 3.5 失败处理

- 若目录不对，停止运行，不要继续执行后续命令

---

## 4. 阶段 1：环境与输入检查

### 4.1 目标

确认 C1 所需的数据、依赖和密钥都已准备好。

### 4.2 必须具备的输入

- `data/train/*.json`
- `data/test_task/*.json`
- `data/scores_all_data.pkl`
- OpenAI 可用鉴权环境变量

### 4.3 命令

```bash
python -V
python -c "import openai; print(openai.__version__)"
test -f data/scores_all_data.pkl && echo "scores ok"
find data/train -maxdepth 1 -name '*.json' | wc -l
find data/test_task -maxdepth 1 -name '*.json' | wc -l
python -c "import os; print(bool(os.environ.get('OPENAI_API_KEY') or os.environ.get('API_KEY')))"
```

### 4.4 产物

- 一次环境检查记录

建议手工记录：


| 字段              | 值                  |
| --------------- | ------------------ |
| date            | 2026-03-31         |
| machine         | Ollies-MacBook-Pro |
| cwd             | mind2web           |
| python version  | 3.14.3             |
| openai version  | 2.29.0             |
| model           | gpt-4o             |
| api key present | True               |


### 4.5 验收点

- `scores ok` 出现
- `train` 与 `test_task` 文件数大于 0
- OpenAI 鉴权检查输出 `True`

### 4.6 失败处理

- 若缺数据，先运行 `experiments/download_official_data.sh`
- 若缺 `OPENAI_API_KEY` 或 `API_KEY`，先设置环境变量
- 若 `openai` 包不可导入，先补依赖再继续

---

## 5. 阶段 2：选择本轮运行单位

### 5.1 目标

固定本轮 C1 的单网站运行对象，避免一开始就做大规模并行实验。

### 5.2 建议起步网站

建议先使用：

- `website=budget`
- `domain=Travel`
- `subdomain=Car rental`

理由：

- `train` 中样本较多
- `test_task` 中样本也较多
- 适合作为首轮 C1 验证对象

### 5.3 命令

```bash
jq -r '.[] | select(.website=="budget") | .website' data/test_task/*.json | wc -l
jq -r '.[] | select(.website=="budget") | [.domain,.subdomain,.website] | @tsv' data/train/*.json | sort | uniq -c
```

### 5.4 产物

- 本轮固定运行对象

建议手工登记：


| run_id | benchmark | domain | subdomain  | website | train（budget） | test_task（budget） |
| ------ | --------- | ------ | ---------- | ------- | ------------- | ----------------- |
| C1-R1  | test_task | Travel | Car rental | budget  | 24            | 10                |


### 5.5 验收点

- 目标网站在 `train` 和 `test_task` 中都存在
- 三元组 `domain/subdomain/website` 已固定，不在同一轮中途更换

### 5.6 失败处理

- 若该网站在 `test_task` 样本太少，换另一个 `train` 和 `test_task` 交集更大的站点
- 但一轮 runbook 只跑一个网站，避免分析口径混乱

---

## 6. 阶段 3：冻结命名与目录

### 6.1 目标

在运行前先固定输出命名，避免出现 `test1`、`final` 这类无法映射到 C1 的目录名。

### 6.2 本 runbook 使用的命名

- benchmark: `test_task`
- baseline suffix: `no_workflow`
- offline suffix: `offline_wf`
- workflow output: `workflow/{website}_offline_wf.txt`

### 6.3 命令

```bash
mkdir -p workflow
touch workflow/_empty.txt
```

### 6.4 预期产物

- `workflow/_empty.txt`
- 后续将生成 `workflow/budget_offline_wf.txt`
- 后续将生成：
  - `results/gpt-4o/test_task/budget/no_workflow/`
  - `results/gpt-4o/test_task/budget/offline_wf/`

### 6.5 验收点

- 目录命名已与结论语义绑定
- baseline 与 offline 条件在路径层面可直接区分

### 6.6 失败处理

- 若已有旧目录，保留但不要混用
- 新一轮结果应使用本 runbook 的固定命名

---

## 7. 阶段 4：Offline workflow induction

### 7.1 目标

从训练集为目标网站归纳 offline workflow。

### 7.2 输入

- `data/train/*.json`
- `data/scores_all_data.pkl`
- `prompt/instruction_action.txt`
- `prompt/one_shot_action.txt`

### 7.3 命令

```bash
python offline_induction.py \
  --mode auto \
  --domain Travel \
  --subdomain "Car rental" \
  --website budget \
  --model_name gpt-4o \
  --output_dir workflow \
  --output_suffix offline_wf
```

### 7.4 预期产物

- `workflow/budget_offline_wf.txt`

### 7.5 验收点

- 输出文件存在
- 文件非空
- 文件内容看起来是 workflow，而不是模型拒答或异常文本

### 7.6 快速检查命令

```bash
test -s workflow/budget_offline_wf.txt && echo "workflow ok"
sed -n '1,80p' workflow/budget_offline_wf.txt
```

### 7.7 失败处理

- 若脚本报鉴权错误，回到阶段 1
- 若输出文件为空，记录失败原因并重跑一次
- 若输出内容明显异常，保留异常文件，不要覆盖，先复制一份再重跑

建议做法：

```bash
cp workflow/budget_offline_wf.txt workflow/budget_offline_wf.bad_run1.txt
```

---

## 8. 阶段 5：Baseline inference

### 8.1 目标

建立不使用 workflow 的对照组。

### 8.2 命令

```bash
python run_mind2web.py \
  --domain Travel \
  --subdomain "Car rental" \
  --website budget \
  --workflow_path workflow/_empty.txt \
  --model gpt-4o \
  --benchmark test_task \
  --suffix no_workflow
```

### 8.3 预期产物

- `results/gpt-4o/test_task/budget/no_workflow/*.json`

### 8.4 验收点

- 结果目录存在
- 目录下 JSON 文件数大于 0
- 每个结果文件最后一项包含：
  - `element_acc`
  - `action_f1`
  - `step_success`
  - `success`

### 8.5 快速检查命令

```bash
find results/gpt-4o/test_task/budget/no_workflow -maxdepth 1 -name '*.json' | wc -l
sed -n '1,40p' "$(find results/gpt-4o/test_task/budget/no_workflow -maxdepth 1 -name '*.json' | head -n 1)"
```

### 8.6 失败处理

- 若运行被中断，不删除已有 JSON，先确认是否需要续跑
- 若部分样本缺失，记录当前文件数，并考虑按索引范围补跑
- 若输出目录为空，停止进入下一阶段

---

## 9. 阶段 6：Offline AWM inference

### 9.1 目标

在同一网站、同一 benchmark 下运行 offline workflow 条件。

### 9.2 命令

```bash
python run_mind2web.py \
  --domain Travel \
  --subdomain "Car rental" \
  --website budget \
  --workflow_path workflow/budget_offline_wf.txt \
  --model gpt-4o \
  --benchmark test_task \
  --suffix offline_wf
```

### 9.3 预期产物

- `results/gpt-4o/test_task/budget/offline_wf/*.json`

### 9.4 验收点

- 结果目录存在
- JSON 文件数大于 0
- 文件结构与 baseline 保持一致
- 结果文件数原则上应与 baseline 一致

### 9.5 快速检查命令

```bash
find results/gpt-4o/test_task/budget/offline_wf -maxdepth 1 -name '*.json' | wc -l
sed -n '1,40p' "$(find results/gpt-4o/test_task/budget/offline_wf -maxdepth 1 -name '*.json' | head -n 1)"
```

### 9.6 失败处理

- 若 workflow 条件结果数少于 baseline，先补齐再打分
- 若 workflow 文件被误改，保留当前版本，重新生成新文件，不覆盖分析记录

---

## 10. 阶段 7：统一打分

### 10.1 目标

用同一脚本对 baseline 与 offline 条件做并排汇总。

### 10.2 命令

```bash
python results/calc_score.py \
  --results_dir results/gpt-4o/test_task/budget/no_workflow

python results/calc_score.py \
  --results_dir results/gpt-4o/test_task/budget/offline_wf
```

### 10.3 需要记录的指标

- `Element Acc`
- `Action F1`
- `Step SR`
- `SR`

### 10.4 建议登记表


| website | condition   | Element Acc | Action F1 | Step SR | SR  |
| ------- | ----------- | ----------- | --------- | ------- | --- |
| budget  | no_workflow | 52.7        | 59.7      | 44.0    | 10.0 |
| budget  | offline_wf  | 44.0        | 59.0      | 36.4    | 10.0 |


### 10.5 验收点

- 两个条件都已打分
- 指标记录在同一张表里
- 不允许只保留终端输出，不落表

### 10.6 失败处理

- 若某目录为空，先回到阶段 5 或阶段 6
- 若打分报 JSON 结构错误，先抽查该目录下最后写入的结果文件

---

## 11. 阶段 8：C1 结果判定

### 11.1 目标

把一轮实验结果转化为论文结论层面的判断，而不是只保留原始分数。

### 11.2 判定模板

建议对每轮填写：


| run_id | website | C1 status | evidence | notes |
| ------ | ------- | --------- | -------- | ----- |
| C1-R1  | budget  |           |          |       |


其中：

- `C1 status` 只能填：
  - `reproduced`
  - `not reproduced`
  - `unclear`

### 11.3 判断规则

填 `reproduced`：

- offline `Element Acc` 和 `Step SR` 至少有两条证据支持论文方向

填 `not reproduced`：

- offline 相对 baseline 方向相反，或核心指标无改善

填 `unclear`：

- 样本不完整
- 结果数不对齐
- 有异常运行但尚未排除实现问题

### 11.4 解释模板

推荐写成一句话：

```text
在 budget 的 cross-task 首轮实验中，offline AWM 相对 baseline 在 Element Acc 与 Step SR 上同步提升，Action F1 未明显改善，因此本轮将 C1 暂记为 reproduced。
```

### 11.5 当前执行记录：C1-R1（budget）

本轮实际结果：

| website | condition | Element Acc | Action F1 | Step SR | SR |
|------|------|------:|------:|------:|------:|
| budget | no_workflow | 52.7 | 59.7 | 44.0 | 10.0 |
| budget | offline_wf | 44.0 | 59.0 | 36.4 | 10.0 |

本轮判定：

| run_id | website | C1 status | evidence | notes |
|------|------|------|------|------|
| C1-R1 | budget | not reproduced | offline 在 `Element Acc`、`Step SR` 上均低于 baseline，`SR` 持平 | 当前仅单网站结果，不能直接外推到整体 C1 |

建议写入状态表的说明：

```text
在 budget 的 cross-task 首轮实验中，offline AWM 相对 baseline 在 Element Acc 与 Step SR 上均下降，Action F1 也未提升，SR 持平，因此本轮将 C1 记为 not reproduced。
```

这一判定只作用于 `C1-R1 / budget` 这一轮，不等同于整体 C1 已失败。

### 11.6 当前执行记录：C1-R2（yellowpages）

本轮实际结果：

| website | condition | Element Acc | Action F1 | Step SR | SR |
|------|------|------:|------:|------:|------:|
| yellowpages | no_workflow | 54.3 | 60.2 | 49.2 | 12.5 |
| yellowpages | offline_wf | 54.8 | 56.3 | 50.1 | 0.0 |

本轮判定：

| run_id | website | C1 status | evidence | notes |
|------|------|------|------|------|
| C1-R2 | yellowpages | unclear | offline 在 `Element Acc`、`Step SR` 上略高于 baseline，但 `Action F1` 下降且 `SR` 从 12.5 降到 0.0 | 指标方向混合，不能直接记为 reproduced |

建议写入状态表的说明：

```text
在 yellowpages 的 cross-task 首轮实验中，offline AWM 相对 baseline 在 Element Acc 与 Step SR 上略有提升，但 Action F1 下降且 SR 从 12.5 降到 0.0，因此本轮将 C1 记为 unclear。
```

这一判定只作用于 `C1-R2 / yellowpages` 这一轮，不等同于整体 C1 已成功或失败。

### 11.7 当前执行记录：C1-R3（kohls）

本轮实际结果：

| website | condition | Element Acc | Action F1 | Step SR | SR |
|------|------|------:|------:|------:|------:|
| kohls | no_workflow | 38.8 | 53.3 | 38.8 | 0.0 |
| kohls | offline_wf | 40.1 | 54.7 | 38.1 | 0.0 |

本轮判定：

| run_id | website | C1 status | evidence | notes |
|------|------|------|------|------|
| C1-R3 | kohls | unclear | offline 在 `Element Acc`、`Action F1` 上略高于 baseline，但 `Step SR` 略低，`SR` 持平为 0.0 | 关键指标方向不一致，不能直接记为 reproduced |

建议写入状态表的说明：

```text
在 kohls 的 cross-task 首轮实验中，offline AWM 相对 baseline 在 Element Acc 与 Action F1 上略有提升，但 Step SR 略低且 SR 持平为 0.0，因此本轮将 C1 记为 unclear。
```

### 11.8 当前执行记录：C1-R4（newegg）

本轮实际结果：

| website | condition | Element Acc | Action F1 | Step SR | SR |
|------|------|------:|------:|------:|------:|
| newegg | no_workflow | 41.2 | 43.8 | 30.6 | 0.0 |
| newegg | offline_wf | 44.9 | 46.6 | 35.4 | 0.0 |

本轮判定：

| run_id | website | C1 status | evidence | notes |
|------|------|------|------|------|
| C1-R4 | newegg | reproduced | offline 在 `Element Acc`、`Step SR` 上均高于 baseline，满足 C1 最低成功判据 | `SR` 仍为 0.0，说明复现信号主要来自分解指标 |

建议写入状态表的说明：

```text
在 newegg 的 cross-task 首轮实验中，offline AWM 相对 baseline 在 Element Acc 与 Step SR 上同步提升，Action F1 也有所改善，因此本轮将 C1 记为 reproduced。
```

### 11.9 当前执行记录：C1-R5（sixflags）

本轮实际结果：

| website | condition | Element Acc | Action F1 | Step SR | SR |
|------|------|------:|------:|------:|------:|
| sixflags | no_workflow | 62.5 | 74.6 | 62.5 | 0.0 |
| sixflags | offline_wf | 57.0 | 78.2 | 57.0 | 0.0 |

本轮判定：

| run_id | website | C1 status | evidence | notes |
|------|------|------|------|------|
| C1-R5 | sixflags | not reproduced | offline 在 `Element Acc`、`Step SR` 上均低于 baseline，虽然 `Action F1` 更高，但不符合 C1 的关键提升结构 | `SR` 持平为 0.0 |

建议写入状态表的说明：

```text
在 sixflags 的 cross-task 首轮实验中，offline AWM 相对 baseline 在 Element Acc 与 Step SR 上均下降，虽然 Action F1 提升，但不符合论文声称的关键收益结构，因此本轮将 C1 记为 not reproduced。
```

### 11.10 当前阶段汇总（前 5 个网站）

截至目前的运行状态：

| run_id | website | C1 status |
|------|------|------|
| C1-R1 | budget | not reproduced |
| C1-R2 | yellowpages | unclear |
| C1-R3 | kohls | unclear |
| C1-R4 | newegg | reproduced |
| C1-R5 | sixflags | not reproduced |

当前阶段性结论：

- 已有 1 个网站支持 C1
- 已有 2 个网站不支持 C1
- 已有 2 个网站结果混合，暂记为 `unclear`

因此，当前更合理的整体判断是：

```text
C1 在已运行的 5 个网站上呈现 mixed evidence，尚不能记为整体 reproduced；当前证据更接近“部分网站支持、部分网站不支持、整体尚不稳定”。
```

### 11.11 当前执行记录：C1-R6（united）

本轮实际结果：

| website | condition | Element Acc | Action F1 | Step SR | SR |
|------|------|------:|------:|------:|------:|
| united | no_workflow | 60.6 | 64.5 | 57.2 | 33.3 |
| united | offline_wf | 64.7 | 63.8 | 56.5 | 16.7 |

本轮判定：

| run_id | website | C1 status | evidence | notes |
|------|------|------|------|------|
| C1-R6 | united | unclear | offline 在 `Element Acc` 上高于 baseline，但 `Step SR`、`Action F1` 和 `SR` 均未改善 | 分解指标与最终成功率方向不一致 |

建议写入状态表的说明：

```text
在 united 的 cross-task 首轮实验中，offline AWM 相对 baseline 在 Element Acc 上提升，但 Step SR、Action F1 和 SR 均未改善，且 SR 从 33.3 降到 16.7，因此本轮将 C1 记为 unclear。
```

### 11.12 当前执行记录：C1-R7（kayak）

本轮实际结果：

| website | condition | Element Acc | Action F1 | Step SR | SR |
|------|------|------:|------:|------:|------:|
| kayak | no_workflow | 51.9 | 59.5 | 47.5 | 0.0 |
| kayak | offline_wf | 54.8 | 64.4 | 51.5 | 0.0 |

本轮判定：

| run_id | website | C1 status | evidence | notes |
|------|------|------|------|------|
| C1-R7 | kayak | reproduced | offline 在 `Element Acc`、`Step SR` 上均高于 baseline，满足 C1 最低成功判据 | `Action F1` 也同步提升，但 `SR` 仍为 0.0 |

建议写入状态表的说明：

```text
在 kayak 的 cross-task 首轮实验中，offline AWM 相对 baseline 在 Element Acc 与 Step SR 上同步提升，Action F1 也提升，因此本轮将 C1 记为 reproduced。
```

### 11.13 当前阶段汇总（前 7 个网站）

截至目前的运行状态：

| run_id | website | C1 status |
|------|------|------|
| C1-R1 | budget | not reproduced |
| C1-R2 | yellowpages | unclear |
| C1-R3 | kohls | unclear |
| C1-R4 | newegg | reproduced |
| C1-R5 | sixflags | not reproduced |
| C1-R6 | united | unclear |
| C1-R7 | kayak | reproduced |

当前阶段性结论：

- 已有 2 个网站支持 C1
- 已有 2 个网站不支持 C1
- 已有 3 个网站结果混合，暂记为 `unclear`

因此，当前更合理的整体判断是：

```text
C1 在已运行的 7 个网站上仍呈现 mixed evidence。现有结果不足以支持“offline AWM 在 cross-task 上稳定优于 baseline”的整体结论，但也不能据此断言 C1 整体失败；更准确的说法是：当前复现结果显示该结论在不同网站上的稳定性不足。
```

### 11.14 C1 主结果表（当前版本）

| website | baseline Elem Acc | offline Elem Acc | baseline Action F1 | offline Action F1 | baseline Step SR | offline Step SR | baseline SR | offline SR | C1 status |
|------|------:|------:|------:|------:|------:|------:|------:|------:|------|
| budget | 52.7 | 44.0 | 59.7 | 59.0 | 44.0 | 36.4 | 10.0 | 10.0 | not reproduced |
| yellowpages | 54.3 | 54.8 | 60.2 | 56.3 | 49.2 | 50.1 | 12.5 | 0.0 | unclear |
| kohls | 38.8 | 40.1 | 53.3 | 54.7 | 38.8 | 38.1 | 0.0 | 0.0 | unclear |
| newegg | 41.2 | 44.9 | 43.8 | 46.6 | 30.6 | 35.4 | 0.0 | 0.0 | reproduced |
| sixflags | 62.5 | 57.0 | 74.6 | 78.2 | 62.5 | 57.0 | 0.0 | 0.0 | not reproduced |
| united | 60.6 | 64.7 | 64.5 | 63.8 | 57.2 | 56.5 | 33.3 | 16.7 | unclear |
| kayak | 51.9 | 54.8 | 59.5 | 64.4 | 47.5 | 51.5 | 0.0 | 0.0 | reproduced |

可直接用于状态表的汇总统计：

| status | count |
|------|------:|
| reproduced | 2 |
| not reproduced | 2 |
| unclear | 3 |

建议在后续文档中引用这张表作为当前版本的 C1 主结果表，而不是再逐条翻阅各轮运行记录。

---

## 12. 阶段 9：归档

### 12.1 目标

确保这一轮结果后续可以被复查、复算、复用。

### 12.2 最低归档要求

至少保留：

- `workflow/budget_offline_wf.txt`
- `results/gpt-4o/test_task/budget/no_workflow/*.json`
- `results/gpt-4o/test_task/budget/offline_wf/*.json`
- 本轮指标登记表
- 本轮结论判断

对于当前 `C1-R1 / budget`，归档时应明确保留：

- 上述两组原始结果目录
- 本轮分数表
- `not reproduced` 的判定记录
- 一句原因说明

### 12.3 建议归档表


| artifact         | path                                           | status |
| ---------------- | ---------------------------------------------- | ------ |
| workflow         | `workflow/budget_offline_wf.txt`               |        |
| baseline results | `results/gpt-4o/test_task/budget/no_workflow/` |        |
| offline results  | `results/gpt-4o/test_task/budget/offline_wf/`  |        |
| score table      | manual log                                     |        |
| C1 judgment      | manual log                                     |        |

### 12.4 当前归档记录：C1-R1（budget）

本轮应归档为：

| artifact | path | status | note |
|------|------|------|------|
| workflow | `workflow/budget_offline_wf.txt` | ready | offline induction 已完成 |
| baseline results | `results/gpt-4o/test_task/budget/no_workflow/` | ready | 共 10 个 JSON |
| offline results | `results/gpt-4o/test_task/budget/offline_wf/` | ready | 共 10 个 JSON |
| score table | manual log | ready | 已记录四项指标 |
| C1 judgment | manual log | ready | 当前判定为 `not reproduced` |

建议手工补一条归档摘要：

```text
C1-R1 / budget 已归档。baseline 与 offline_wf 各有 10 个结果文件；offline AWM 在 Element Acc 与 Step SR 上均低于 baseline，因此本轮记为 not reproduced。
```

### 12.6 当前归档记录：C1-R2（yellowpages）

本轮应归档为：

| artifact | path | status | note |
|------|------|------|------|
| workflow | `workflow/yellowpages_offline_wf.txt` | ready | offline induction 已完成 |
| baseline results | `results/gpt-4o/test_task/yellowpages/no_workflow/` | ready | 结果已打分 |
| offline results | `results/gpt-4o/test_task/yellowpages/offline_wf/` | ready | 结果已打分 |
| score table | manual log | ready | 已记录四项指标 |
| C1 judgment | manual log | ready | 当前判定为 `unclear` |

建议手工补一条归档摘要：

```text
C1-R2 / yellowpages 已归档。offline AWM 在 Element Acc 与 Step SR 上略高于 baseline，但 Action F1 下降且 SR 降为 0.0，因此本轮记为 unclear。
```

### 12.7 当前归档记录：C1-R3（kohls）

本轮应归档为：

| artifact | path | status | note |
|------|------|------|------|
| workflow | `workflow/kohls_offline_wf.txt` | ready | offline induction 已完成 |
| baseline results | `results/gpt-4o/test_task/kohls/no_workflow/` | ready | 结果已打分 |
| offline results | `results/gpt-4o/test_task/kohls/offline_wf/` | ready | 结果已打分 |
| score table | manual log | ready | 已记录四项指标 |
| C1 judgment | manual log | ready | 当前判定为 `unclear` |

建议手工补一条归档摘要：

```text
C1-R3 / kohls 已归档。offline AWM 在 Element Acc 与 Action F1 上略高于 baseline，但 Step SR 略低且 SR 持平为 0.0，因此本轮记为 unclear。
```

### 12.8 当前归档记录：C1-R4（newegg）

本轮应归档为：

| artifact | path | status | note |
|------|------|------|------|
| workflow | `workflow/newegg_offline_wf.txt` | ready | offline induction 已完成 |
| baseline results | `results/gpt-4o/test_task/newegg/no_workflow/` | ready | 结果已打分 |
| offline results | `results/gpt-4o/test_task/newegg/offline_wf/` | ready | 结果已打分 |
| score table | manual log | ready | 已记录四项指标 |
| C1 judgment | manual log | ready | 当前判定为 `reproduced` |

建议手工补一条归档摘要：

```text
C1-R4 / newegg 已归档。offline AWM 在 Element Acc 与 Step SR 上同步高于 baseline，Action F1 也提升，因此本轮记为 reproduced。
```

### 12.9 当前归档记录：C1-R5（sixflags）

本轮应归档为：

| artifact | path | status | note |
|------|------|------|------|
| workflow | `workflow/sixflags_offline_wf.txt` | ready | offline induction 已完成 |
| baseline results | `results/gpt-4o/test_task/sixflags/no_workflow/` | ready | 结果已打分 |
| offline results | `results/gpt-4o/test_task/sixflags/offline_wf/` | ready | 结果已打分 |
| score table | manual log | ready | 已记录四项指标 |
| C1 judgment | manual log | ready | 当前判定为 `not reproduced` |

建议手工补一条归档摘要：

```text
C1-R5 / sixflags 已归档。offline AWM 在 Element Acc 与 Step SR 上均低于 baseline，虽然 Action F1 更高，但不符合论文声称的关键收益结构，因此本轮记为 not reproduced。
```

### 12.10 当前归档记录：C1-R6（united）

本轮应归档为：

| artifact | path | status | note |
|------|------|------|------|
| workflow | `workflow/united_offline_wf.txt` | ready | offline induction 已完成 |
| baseline results | `results/gpt-4o/test_task/united/no_workflow/` | ready | 结果已打分 |
| offline results | `results/gpt-4o/test_task/united/offline_wf/` | ready | 结果已打分 |
| score table | manual log | ready | 已记录四项指标 |
| C1 judgment | manual log | ready | 当前判定为 `unclear` |

建议手工补一条归档摘要：

```text
C1-R6 / united 已归档。offline AWM 在 Element Acc 上高于 baseline，但 Step SR、Action F1 和 SR 均未改善，且 SR 从 33.3 降到 16.7，因此本轮记为 unclear。
```

### 12.11 当前归档记录：C1-R7（kayak）

本轮应归档为：

| artifact | path | status | note |
|------|------|------|------|
| workflow | `workflow/kayak_offline_wf.txt` | ready | offline induction 已完成 |
| baseline results | `results/gpt-4o/test_task/kayak/no_workflow/` | ready | 结果已打分 |
| offline results | `results/gpt-4o/test_task/kayak/offline_wf/` | ready | 结果已打分 |
| score table | manual log | ready | 已记录四项指标 |
| C1 judgment | manual log | ready | 当前判定为 `reproduced` |

建议手工补一条归档摘要：

```text
C1-R7 / kayak 已归档。offline AWM 在 Element Acc 与 Step SR 上同步高于 baseline，Action F1 也更高，因此本轮记为 reproduced。
```

### 12.5 阶段 9 完成判据

当以下条件都满足时，可视为阶段 9 已完成：

1. `workflow/budget_offline_wf.txt` 已保留
2. baseline 与 offline 结果目录都存在且文件数一致
3. 本轮分数表已登记
4. 本轮 C1 判定已登记

只有阶段 9 完成后，才进入阶段 10 的网站扩展。


---

## 13. 阶段 10：从单网站扩展到正式 C1

### 13.1 目标

把首轮可运行样例扩展成 C1 的正式证据。

### 13.2 扩展顺序

1. 先完成 `budget` 的首轮
2. 再挑选更多 `train` 与 `test_task` 交集较大的网站
3. 对每个网站重复阶段 2 到阶段 9
4. 汇总成 C1 主结果表

对当前状态，下一步不需要改 runbook 的阶段顺序。

正确顺序仍然是：

1. 先完成阶段 9 归档，把 `C1-R1 / budget` 的结果和判定落盘
2. 再进入阶段 10，继续按同样口径扩展 2 到 4 个 `train / test_task` 交集较大的网站
3. 等多网站结果齐了，再判断这是个别网站现象，还是整体 C1 站不住

建议优先扩展的网站选择原则：

- 在 `train` 和 `test_task` 中都有足够样本
- 使用和 `budget` 相同的命名与运行口径
- 每个网站都显式传 `domain / subdomain / website`

### 13.3 正式 C1 何时算完成

当以下条件满足时，可将 C1 从“首轮验证”升级为“正式完成”：

1. 不止一个网站有可比结果
2. 大多数运行对象都保留逐样本 JSON
3. 已形成跨网站汇总表
4. 已对论文主张给出整体判断，而不是单网站判断

### 13.4 下一批网站候选

为保持与 `budget` 同样的执行口径，下一批优先从 `train` 与 `test_task` 交集较大的站点中选择。

建议优先级如下：

| priority | website | domain | subdomain | train | test_task |
|------|------|------|------|------:|------:|
| 1 | yellowpages | Travel | Restaurant | 15 | 8 |
| 2 | kohls | Shopping | Department | 15 | 8 |
| 3 | newegg | Shopping | Digital | 21 | 7 |
| 4 | sixflags | Travel | Other | 15 | 7 |

备选：

| website | domain | subdomain | train | test_task |
|------|------|------|------:|------:|
| united | Travel | Airlines | 24 | 6 |
| kayak | Travel | Airlines | 19 | 6 |
| carmax | Shopping | Auto | 16 | 6 |
| amtrak | Travel | Ground | 15 | 6 |

### 13.5 下一步执行建议

完成 `budget` 的阶段 9 归档后，建议按以下顺序继续：

1. `yellowpages`
2. `kohls`
3. `newegg`
4. `sixflags`

理由：

- 这些站点在 `train` 与 `test_task` 中都有相对更多样本
- 覆盖了 `Travel` 与 `Shopping` 两类站点
- 能较快判断 `budget` 的负结果是个别站点现象，还是更广泛的趋势

当前进度更新后，建议顺序调整为：

1. `kohls`
2. `newegg`
3. `sixflags`

原因：

- `budget` 已给出 `not reproduced`
- `yellowpages` 已给出 `unclear`
- 继续补 `Shopping` 与 `Travel` 两类站点，可更快判断目前的混合结果是否具有普遍性

当前已完成上述三站后，下一步建议更新为：

1. 若只要求完成一轮 C1 中期判断，则先停在这里，整理跨网站汇总表
2. 若要继续增强结论稳定性，则从备选中再补 2 个站点，优先：
   - `united`
   - `kayak`

原因：

- 当前已经有 5 个网站结果，足够支持一次中期结论
- 若要进一步确认 Travel 类网站上的趋势，`united` 与 `kayak` 是更合适的下一批补充

### 13.6 可直接复制运行的命令

以下命令默认你已经位于：

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web
```

#### `kohls`

```bash
python offline_induction.py \
  --mode auto \
  --domain Shopping \
  --subdomain "Department" \
  --website kohls \
  --model_name gpt-4o \
  --output_dir workflow \
  --output_suffix offline_wf

python run_mind2web.py \
  --domain Shopping \
  --subdomain "Department" \
  --website kohls \
  --workflow_path workflow/_empty.txt \
  --model gpt-4o \
  --benchmark test_task \
  --suffix no_workflow

python run_mind2web.py \
  --domain Shopping \
  --subdomain "Department" \
  --website kohls \
  --workflow_path workflow/kohls_offline_wf.txt \
  --model gpt-4o \
  --benchmark test_task \
  --suffix offline_wf

python results/calc_score.py \
  --results_dir results/gpt-4o/test_task/kohls/no_workflow

python results/calc_score.py \
  --results_dir results/gpt-4o/test_task/kohls/offline_wf
```

#### `newegg`

```bash
python offline_induction.py \
  --mode auto \
  --domain Shopping \
  --subdomain "Digital" \
  --website newegg \
  --model_name gpt-4o \
  --output_dir workflow \
  --output_suffix offline_wf

python run_mind2web.py \
  --domain Shopping \
  --subdomain "Digital" \
  --website newegg \
  --workflow_path workflow/_empty.txt \
  --model gpt-4o \
  --benchmark test_task \
  --suffix no_workflow

python run_mind2web.py \
  --domain Shopping \
  --subdomain "Digital" \
  --website newegg \
  --workflow_path workflow/newegg_offline_wf.txt \
  --model gpt-4o \
  --benchmark test_task \
  --suffix offline_wf

python results/calc_score.py \
  --results_dir results/gpt-4o/test_task/newegg/no_workflow

python results/calc_score.py \
  --results_dir results/gpt-4o/test_task/newegg/offline_wf
```

#### `sixflags`

```bash
python offline_induction.py \
  --mode auto \
  --domain Travel \
  --subdomain "Other" \
  --website sixflags \
  --model_name gpt-4o \
  --output_dir workflow \
  --output_suffix offline_wf

python run_mind2web.py \
  --domain Travel \
  --subdomain "Other" \
  --website sixflags \
  --workflow_path workflow/_empty.txt \
  --model gpt-4o \
  --benchmark test_task \
  --suffix no_workflow

python run_mind2web.py \
  --domain Travel \
  --subdomain "Other" \
  --website sixflags \
  --workflow_path workflow/sixflags_offline_wf.txt \
  --model gpt-4o \
  --benchmark test_task \
  --suffix offline_wf

python results/calc_score.py \
  --results_dir results/gpt-4o/test_task/sixflags/no_workflow

python results/calc_score.py \
  --results_dir results/gpt-4o/test_task/sixflags/offline_wf
```

#### `united`

```bash
python offline_induction.py \
  --mode auto \
  --domain Travel \
  --subdomain "Airlines" \
  --website united \
  --model_name gpt-4o \
  --output_dir workflow \
  --output_suffix offline_wf

python run_mind2web.py \
  --domain Travel \
  --subdomain "Airlines" \
  --website united \
  --workflow_path workflow/_empty.txt \
  --model gpt-4o \
  --benchmark test_task \
  --suffix no_workflow

python run_mind2web.py \
  --domain Travel \
  --subdomain "Airlines" \
  --website united \
  --workflow_path workflow/united_offline_wf.txt \
  --model gpt-4o \
  --benchmark test_task \
  --suffix offline_wf

python results/calc_score.py \
  --results_dir results/gpt-4o/test_task/united/no_workflow

python results/calc_score.py \
  --results_dir results/gpt-4o/test_task/united/offline_wf
```

#### `kayak`

```bash
python offline_induction.py \
  --mode auto \
  --domain Travel \
  --subdomain "Airlines" \
  --website kayak \
  --model_name gpt-4o \
  --output_dir workflow \
  --output_suffix offline_wf

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

python results/calc_score.py \
  --results_dir results/gpt-4o/test_task/kayak/no_workflow

python results/calc_score.py \
  --results_dir results/gpt-4o/test_task/kayak/offline_wf
```

---

## 14. 常见失败模式

### 14.1 workflow 文件为空

优先检查：

- API key
- 模型调用是否成功
- 输出文件是否被异常覆盖

### 14.2 baseline 和 offline 文件数不一致

优先判断：

- 是否中途中断
- 是否同一网站
- 是否同一 benchmark

### 14.3 打分正常但结果方向异常

不要立刻下结论说论文错。

先排查：

- benchmark 是否真的是 `test_task`
- workflow 是否来自对应网站
- 是否误用了旧文件
- 是否结果目录混入旧运行产物

### 14.4 结果可以跑，但没有中间记录

这不算合格 runbook 执行。

至少补齐：

- 环境检查记录
- 指标表
- C1 判断表

---

## 15. 每轮运行后必须回答的 5 个问题

每完成一轮 C1，都必须写下：

1. 这轮跑的是哪个网站？
2. baseline 和 offline 是否都完整跑完？
3. 两者结果文件数是否一致？
4. offline 的收益主要来自哪个指标？
5. 这一轮应判为 `reproduced`、`not reproduced` 还是 `unclear`？

如果这 5 个问题答不出来，这一轮就还不能进入“论文结论复现状态表”。

---

## 16. 最小执行摘要

如果只保留最短版本，C1 的 runbook 可以压缩成：

1. 固定目录与环境
2. 固定网站与命名
3. 归纳 offline workflow
4. 跑 baseline
5. 跑 offline AWM
6. 用同一脚本打分
7. 记录四项指标
8. 给出本轮 C1 判定
9. 归档 workflow、JSON 和结果表

但正式执行时，仍建议按本文档的分阶段检查点运行。
