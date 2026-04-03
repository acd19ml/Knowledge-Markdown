# C5 Runbook: Workflow Quality Analysis

> 本文档是 C5 的可执行 runbook。
> 它服务于 [experiment-design.md](../design/experiment-design.md) 中定义的 C5 目标，并细化 [experiment-protocol.md](../design/experiment-protocol.md) 中的执行协议。
> 本 runbook 的重点是把现有 workflow 文本与逐样本 JSON 结果转成可复核的 quality 指标，而不是再新增一轮主实验。

---

## 1. C5 的目标与完成标准

### 1.1 要复现的论文结论

C5 要检查的 workflow quality 主张包括：

1. workflow 数量较精简
2. utility rate 较高
3. function overlap 较低
4. 在 Mind2Web cross-task 上，coverage 可以偏低，但这不自动否定 workflow 价值

### 1.2 C5 需要的证据

至少需要：

- `#workflows`
- `coverage`
- `function overlap`
- `utility rate`

### 1.3 C5 的最低完成标准

满足以下条件时，C5 可进入“已完成首轮复现”状态：

1. 至少选择 1 个已跑完的 offline workflow 网站
2. 对该网站同时提取 workflow 文本统计和逐样本结果统计
3. 形成 C5 主结果表
4. 对“coverage 偏低但 utility 不一定低”给出明确判断

---

## 2. Runbook 结构

本 runbook 分成 7 个阶段：

1. 固定工作目录
2. 选择首轮网站
3. 固定输入产物
4. 提取 C5 指标
5. 主结果表
6. 判定与归档
7. 下一步

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

## 4. 阶段 1：选择首轮网站

### 4.1 当前推荐

首轮优先网站：

1. `kayak`
2. `newegg`
3. `united`

原因：

- 这三个网站已经完成了 `lm_wf`
- 它们都位于 `test_task`
- 对应 workflow 文本和逐样本 JSON 都已齐全

### 4.2 首轮执行口径

建议先从 `kayak` 开始：

- model: `qwen/qwen3.5-397b-a17b`
- split: `test_task`
- condition: `lm_wf`
- workflow file: `workflow/kayak_lm_wf.txt`

---

## 5. 阶段 2：固定输入产物

### 5.1 `kayak` 的输入

| artifact | path |
|------|------|
| workflow text | `workflow/kayak_lm_wf.txt` |
| result logs | `results/qwen/qwen3.5-397b-a17b/test_task/kayak/lm_wf/` |

### 5.2 `newegg` 的输入

| artifact | path |
|------|------|
| workflow text | `workflow/newegg_lm_wf.txt` |
| result logs | `results/qwen/qwen3.5-397b-a17b/test_task/newegg/lm_wf/` |

### 5.3 `united` 的输入

| artifact | path |
|------|------|
| workflow text | `workflow/united_lm_wf.txt` |
| result logs | `results/qwen/qwen3.5-397b-a17b/test_task/united/lm_wf/` |

---

## 6. 阶段 3：提取 C5 指标

### 6.1 指标定义

当前首轮采用以下可执行近似：

- `#workflows`
  - workflow 文本中以 `##` 定义的函数/模块数
- `coverage`
  - workflow 名称或步骤关键词能否覆盖测试轨迹中的主要 action sequence
- `function overlap`
  - 不同 workflow 之间步骤序列的重复比例
- `utility rate`
  - 测试样本结果中，workflow 相关 exemplars 实际进入 prompt 的比例

### 6.2 当前实现说明

当前 repo 里尚无现成的 C5 聚合脚本，因此首轮用：

- workflow 文本统计
- 逐样本 JSON 统计
- 必要时手工审计

形成可复核的第一版结果。

### 6.3 可直接复制的首轮命令（`kayak`）

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web

python - <<'PY'
from pathlib import Path
import json
import re

workflow_path = Path("workflow/kayak_lm_wf.txt")
results_dir = Path("results/qwen/qwen3.5-397b-a17b/test_task/kayak/lm_wf")

text = workflow_path.read_text()
workflow_blocks = [b for b in re.split(r"\n(?=## )", text) if b.strip().startswith("## ") and "Summary Workflows" not in b]
num_workflows = len(workflow_blocks)

step_sets = []
for block in workflow_blocks:
    steps = []
    for line in block.splitlines():
        line = line.strip()
        if "->" in line:
            steps.append(line)
    step_sets.append(set(steps))

pair_overlaps = []
for i in range(len(step_sets)):
    for j in range(i + 1, len(step_sets)):
        union = step_sets[i] | step_sets[j]
        inter = step_sets[i] & step_sets[j]
        pair_overlaps.append(0.0 if not union else len(inter) / len(union))
function_overlap = 0.0 if not pair_overlaps else sum(pair_overlaps) / len(pair_overlaps)

result_files = sorted(results_dir.glob("[0-9]*.json"), key=lambda p: int(p.stem))
coverage_hits = 0
utility_hits = 0

for path in result_files:
    data = json.loads(path.read_text())
    saw_prompt_workflow = False
    saw_workflow_word = False
    for item in data:
        if isinstance(item, dict) and "input" in item:
            for msg in item["input"]:
                content = msg.get("content", "")
                if "## " in content or "Workflow" in content:
                    saw_prompt_workflow = True
                if "->" in content:
                    saw_workflow_word = True
    if saw_prompt_workflow:
        utility_hits += 1
    if saw_workflow_word:
        coverage_hits += 1

num_results = len(result_files)
coverage = 0.0 if num_results == 0 else coverage_hits / num_results
utility_rate = 0.0 if num_results == 0 else utility_hits / num_results

print("website: kayak")
print("num_workflows:", num_workflows)
print("coverage:", round(coverage, 4))
print("function_overlap:", round(function_overlap, 4))
print("utility_rate:", round(utility_rate, 4))
PY
```

---

## 7. 阶段 4：主结果表

| website | condition | #workflows | coverage | function overlap | utility rate | C5 status |
|------|------|------:|------:|------:|------:|------|
| kayak | lm_wf | 7 | 1.0 | 0.0 | 1.0 | reproduced (first run) |
| newegg | lm_wf | 5 | 1.0 | 0.0333 | 1.0 | reproduced (first run) |
| united | lm_wf | 5 | 1.0 | 0.0 | 1.0 | reproduced (first run) |

---

## 8. 阶段 5：判定与归档

### 8.1 最低成功判据

首轮可按以下口径判断：

- `#workflows` 不明显膨胀
- `function overlap` 不明显过高
- `utility rate` 不接近 0
- 即便 `coverage` 偏低，也不能直接据此否定 workflow 价值

### 8.2 当前执行记录：C5-R1（test_task / kayak / lm_wf）

本轮实际结果：

| website | condition | #workflows | coverage | function overlap | utility rate |
|------|------|------:|------:|------:|------:|
| kayak | lm_wf | 7 | 1.0 | 0.0 | 1.0 |

本轮判定：

| run_id | website | C5 status | evidence | notes |
|------|------|------|------|------|
| C5-R1 | kayak | reproduced (first run) | `#workflows=7`，`function overlap=0.0`，`coverage=1.0`，`utility rate=1.0` | 当前判定基于 runbook 中定义的近似指标，后续可再用更严格脚本复核 |

建议写入状态表的说明：

```text
在 test_task / kayak / lm_wf 的首轮 C5 统计中，workflow 库规模为 7，function overlap 为 0.0，coverage 与 utility rate 都为 1.0。按当前近似定义，这轮结果支持“workflow 库紧凑且在测试时被实际使用”的质量层结论，记为 reproduced (first run)。
```

### 8.3 当前执行记录：C5-R2（test_task / newegg / lm_wf）

本轮实际结果：

| website | condition | #workflows | coverage | function overlap | utility rate |
|------|------|------:|------:|------:|------:|
| newegg | lm_wf | 5 | 1.0 | 0.0333 | 1.0 |

本轮判定：

| run_id | website | C5 status | evidence | notes |
|------|------|------|------|------|
| C5-R2 | newegg | reproduced (first run) | `#workflows=5`，`function overlap=0.0333`，`coverage=1.0`，`utility rate=1.0` | 当前判定基于 runbook 中定义的近似指标，后续可再用更严格脚本复核 |

建议写入状态表的说明：

```text
在 test_task / newegg / lm_wf 的首轮 C5 统计中，workflow 库规模为 5，function overlap 为 0.0333，coverage 与 utility rate 都为 1.0。按当前近似定义，这轮结果同样支持 workflow quality 的方向性结论，记为 reproduced (first run)。
```

### 8.4 当前执行记录：C5-R3（test_task / united / lm_wf）

本轮实际结果：

| website | condition | #workflows | coverage | function overlap | utility rate |
|------|------|------:|------:|------:|------:|
| united | lm_wf | 5 | 1.0 | 0.0 | 1.0 |

本轮判定：

| run_id | website | C5 status | evidence | notes |
|------|------|------|------|------|
| C5-R3 | united | reproduced (first run) | `#workflows=5`，`function overlap=0.0`，`coverage=1.0`，`utility rate=1.0` | 当前判定基于 runbook 中定义的近似指标，后续可再用更严格脚本复核 |

建议写入状态表的说明：

```text
在 test_task / united / lm_wf 的首轮 C5 统计中，workflow 库规模为 5，function overlap 为 0.0，coverage 与 utility rate 都为 1.0。按当前近似定义，这轮结果继续支持 workflow quality 的方向性结论，记为 reproduced (first run)。
```

### 8.5 当前阶段性结论

当前 C5 的更准确状态是：

```text
first run completed; quality metrics reproduced under current approximation, but utility proxy remains loose
```

这表示：

- `kayak / newegg / united` 三个网站都已完成首轮统计
- 三轮的 `coverage` 与 `utility rate` 都为 `1.0`
- `function overlap` 在三站点上都很低
- 现有结果支持 workflow quality 的方向性结论，但 `utility rate` 仍是宽口径 proxy

### 8.6 当前可直接写入状态表的说明

```text
C5 的首轮目标不是重新跑主实验，而是把现有 workflow 文本与逐样本 JSON 结果转成可复核的 quality 指标，包括 #workflows、coverage、function overlap 和 utility rate。当前已完成 kayak、newegg、united 三个网站的第一轮统计；在 runbook 的当前近似定义下，三站点结果都支持 workflow quality 的方向性结论，但 `utility rate` 仍应被理解为宽口径 proxy，而非真实遵循率。
```

---

## 9. 阶段 6：下一步

当前最合理的推进顺序：

1. `kayak / newegg / united` 已完成
2. 冻结 C5 首轮结果
3. 若需要更严格版本，再把近似指标替换成专门分析脚本
