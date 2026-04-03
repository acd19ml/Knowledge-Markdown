# C3 Runbook: LM Induction vs Rule Induction

> 本文档是 C3 的可执行 runbook。
> 它服务于 [experiment-design.md](../design/experiment-design.md) 中定义的 C3 目标，并细化 [experiment-protocol.md](../design/experiment-protocol.md) 中的执行协议。
> 本 runbook 的重点是把 `rule induction` 这条关键对照落实成可执行入口，并在统一口径下完成 C3 首轮方法比较。

---

## 1. C3 的目标与完成标准

### 1.1 要复现的论文结论

- LM induction 优于 rule induction
- LM 的优势主要来自更抽象、可复用的 sub-routine
- rule induction 更容易保留完整、具体 trajectory 的偏差

### 1.2 C3 需要的证据

至少需要以下三类证据：

- baseline / rule induction / LM induction 的并排结果
- workflow 示例或人工审计样例
- 指标分解，尤其是 `Element Acc`、`Step SR`、`SR`

### 1.3 C3 的最低完成标准

满足以下条件时，C3 可进入“已完成首轮复现”状态：

1. 至少完成一个网站的 baseline / rule / LM 三条件实验
2. 三个条件都有完整逐样本 JSON 结果
3. 已保存 rule workflow 与 LM workflow 文本
4. 已完成一次 workflow 风格审计
5. 已给出 split 级判定

### 1.4 C3 的最低成功判据

满足以下任意两条，可初步视为 C3 复现成功：

- LM induction 在 `Step SR` 上优于 rule induction
- LM induction 在 `SR` 上优于 rule induction
- LM workflow 更抽象，rule workflow 更接近完整具体 trajectory

---

## 2. Runbook 结构

本 runbook 分成 9 个阶段：

1. 固定工作目录
2. 当前代码实现审计
3. 冻结论文中的 rule induction 定义
4. 冻结 C3 首轮实验口径
5. 规则归纳实现准备
6. 首轮单网站实验
7. workflow 审计
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

## 4. 阶段 1：当前代码实现审计

### 4.1 目标

先确认当前 repo 是否已经实现 `rule induction`，不要直接假设它存在。

### 4.2 命令

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web

rg -n "rule_wf|rule induction|rule-based|rule based" .
find workflow -maxdepth 1 -type f | sort
```

### 4.3 当前审计结论

截至目前：

- repo 中有 `offline_induction.py` 与 `online_induction.py`
- repo 中现已补充 `rule_induction.py`
- `workflow/` 下已有首个本地生成样例：`kayak_rule_wf.txt`

因此，当前 C3 的状态不是 `blocked`，而是：

```text
ready for first run
```

### 4.4 验收点

- 明确记录：当前 repo 已具备可直接运行的 rule induction 实现

---

## 5. 阶段 2：冻结论文中的 rule induction 定义

### 5.1 目标

先把论文里的 rule-based 方法定义固定下来，避免后面临时发明不一致的 rule baseline。

### 5.2 论文中的两步 rule induction

根据论文附录 B，rule-based workflow induction 包含两步：

1. experience deduplication
2. invalid action filtering

### 5.3 规则定义

#### 5.3.1 deduplication

- 从 trajectory 中抽取 action sequence
- 例如把：
  - `CLICK('12') -> CLICK('30') -> TYPE('44', "cat")`
- 抽象成：
  - `CLICK -> CLICK -> TYPE`
- 按 action sequence 分组
- 每组随机保留 `n=1` 条 experience

#### 5.3.2 invalid action filtering

- 对 `CLICK` 和 `TYPE`
- 要求第一个参数必须是字符串形式整数
- 不满足该条件的 action 从 trajectory 中删除

### 5.4 Runbook 口径

在当前复现中，只有满足上面两步定义的 workflow，才记为 `rule induction`。

不接受以下替代品：

- 直接把某条原始 trajectory 当作 rule workflow
- 手写启发式摘要但不做 deduplication
- 没有 invalid action filtering 的原始经验摘录

---

## 6. 阶段 3：冻结 C3 首轮实验口径

### 6.1 首轮 split

首轮只做：

- `test_task`

原因：

- C1 已经在 `test_task` 上有成熟口径
- C3 的目标是方法比较，不需要一上来覆盖所有 split
- 先在单 split 上看 LM vs rule 的相对方向，更容易解释

### 6.2 首轮网站

建议优先：

- `website=kayak`
- `domain=Travel`
- `subdomain=Airlines`

原因：

- C1 和 C2 已经在 `kayak` 上有基线结果
- 样本量虽不大，但执行成本低
- 适合先完成一轮方法对照

### 6.3 首轮条件

首轮至少比较：

- baseline：`no_workflow`
- LM induction：`lm_wf`
- rule induction：`rule_wf`

### 6.4 命名冻结

- baseline suffix: `no_workflow`
- LM suffix: `lm_wf`
- rule suffix: `rule_wf`
- LM workflow: `workflow/{website}_lm_wf.txt`
- rule workflow: `workflow/{website}_rule_wf.txt`

---

## 7. 阶段 4：规则归纳实现准备

### 7.1 目标

确认 `rule_induction.py` 已经能生成与现有 prompt 兼容的 `rule workflow` 文本。

### 7.2 当前实现

当前 repo 已新增：

- `rule_induction.py`

它完成以下逻辑：

1. 从 `train` 中选出对应 `domain / subdomain / website` 的 experiences
2. 提取 action sequence
3. 按 action sequence 去重，每组保留 `n=1`
4. 对 `CLICK / TYPE` 执行与当前数据结构兼容的 invalid-action filtering
5. 输出与现有 workflow prompt 兼容的具体 trajectory blocks

### 7.3 当前脚本接口

```bash
python rule_induction.py \
  --domain {DOMAIN} \
  --subdomain "{SUBDOMAIN}" \
  --website {WEBSITE} \
  --output_path workflow/{WEBSITE}_rule_wf.txt
```

### 7.4 当前样例检查命令

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web

python rule_induction.py \
  --domain Travel \
  --subdomain "Airlines" \
  --website kayak \
  --output_path workflow/kayak_rule_wf.txt

sed -n '1,80p' workflow/kayak_rule_wf.txt
```

### 7.5 当前阶段判定

当前阶段已完成，可以进入正式跑分。

建议在总状态表中写：

```text
C3 的 rule induction 入口已在当前 repo 中补齐，现已具备首轮 baseline / rule / LM 三条件比较所需的最小实现。
```

---

## 8. 阶段 5：首轮单网站实验

### 8.1 当前状态

本阶段现在已可直接运行。

### 8.2 可直接复制的首轮命令

推荐模型：

- `qwen/qwen3.5-397b-a17b`

#### baseline

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web

python run_mind2web.py \
  --domain Travel \
  --subdomain "Airlines" \
  --website kayak \
  --workflow_path workflow/_empty.txt \
  --model qwen/qwen3.5-397b-a17b \
  --benchmark test_task \
  --log_dir results \
  --suffix no_workflow
```

#### LM induction

```bash
python offline_induction.py \
  --mode auto \
  --domain Travel \
  --subdomain "Airlines" \
  --website kayak \
  --model_name qwen/qwen3.5-397b-a17b \
  --output_dir workflow \
  --output_suffix lm_wf

python run_mind2web.py \
  --domain Travel \
  --subdomain "Airlines" \
  --website kayak \
  --workflow_path workflow/kayak_lm_wf.txt \
  --model qwen/qwen3.5-397b-a17b \
  --benchmark test_task \
  --log_dir results \
  --suffix lm_wf
```

#### rule induction

```bash
python rule_induction.py \
  --domain Travel \
  --subdomain "Airlines" \
  --website kayak \
  --output_path workflow/kayak_rule_wf.txt

python run_mind2web.py \
  --domain Travel \
  --subdomain "Airlines" \
  --website kayak \
  --workflow_path workflow/kayak_rule_wf.txt \
  --model qwen/qwen3.5-397b-a17b \
  --benchmark test_task \
  --log_dir results \
  --suffix rule_wf
```

#### scoring

```bash
python results/calc_score.py \
  --results_dir results/qwen/qwen3.5-397b-a17b/test_task/kayak/no_workflow

python results/calc_score.py \
  --results_dir results/qwen/qwen3.5-397b-a17b/test_task/kayak/lm_wf

python results/calc_score.py \
  --results_dir results/qwen/qwen3.5-397b-a17b/test_task/kayak/rule_wf
```

---

## 9. 阶段 6：workflow 审计

### 9.1 目标

不仅比较分数，还要检查 LM workflow 与 rule workflow 的风格差异是否符合论文解释。

### 9.2 最低审计要求

至少人工检查：

- `workflow/kayak_lm_wf.txt`
- `workflow/kayak_rule_wf.txt`

### 9.3 审计维度

| 维度 | LM workflow 预期 | rule workflow 预期 |
|------|------|------|
| 抽象程度 | 更抽象 | 更贴近具体 trajectory |
| 可复用子程序 | 更明显 | 更弱 |
| 具体元素 / 参数残留 | 更少 | 更多 |
| 步骤冗余 | 更低 | 更高 |

### 9.4 审计结论模板

```text
LM workflow 更偏向抽象 sub-routine，而 rule workflow 更接近具体轨迹摘录，这与论文对两者差异的解释一致 / 不一致。
```

---

## 10. 阶段 7：打分、判定与主结果表

### 10.1 主结果表（当前版本）

| website | condition | Element Acc | Action F1 | Step SR | SR |
|------|------|------:|------:|------:|------:|
| kayak | no_workflow | 53.6 | 64.9 | 51.2 | 0.0 |
| kayak | lm_wf | 56.5 | 62.7 | 49.1 | 0.0 |
| kayak | rule_wf | 53.6 | 61.2 | 49.1 | 0.0 |
| newegg | no_workflow | 35.0 | 44.8 | 25.5 | 0.0 |
| newegg | lm_wf | 40.4 | 45.4 | 28.9 | 0.0 |
| newegg | rule_wf | 37.2 | 46.8 | 28.0 | 0.0 |
| united | no_workflow | 60.6 | 64.3 | 60.6 | 33.3 |
| united | lm_wf | 61.8 | 64.5 | 61.2 | 33.3 |
| united | rule_wf | 58.3 | 63.1 | 56.3 | 33.3 |

### 10.2 判定模板

| run_id | website | C3 status | evidence | notes |
|------|------|------|------|------|
| C3-R1 | kayak | unclear | LM 相对 rule 在 `Element Acc` 与 `Action F1` 上更高，但 `Step SR` 与 `SR` 未改善；workflow 风格差异与论文解释一致 | 当前只完成单网站首轮，且关键成功判据只满足一半 |

### 10.3 状态标签

填 `reproduced`：

- LM induction 明显优于 rule induction
- 且 workflow 风格差异与论文解释一致

填 `not reproduced`：

- LM induction 未优于 rule induction
- 或 workflow 风格差异没有出现

填 `unclear`：

- 分数方向混合
- 或 workflow 审计不能稳定支持论文解释

### 10.4 当前阶段结论

截至目前，C3 的正确状态应记为：

```text
first run completed
```

原因是：

- 当前 repo 已补齐可运行的 rule induction 脚本
- `kayak / test_task` 的 baseline / rule / LM 三条件结果已跑出
- 但当前结果不足以把 C3 直接记为 `reproduced`

### 10.5 当前执行记录：C3-R1（test_task / kayak）

本轮实际结果：

| website | condition | Element Acc | Action F1 | Step SR | SR |
|------|------|------:|------:|------:|------:|
| kayak | no_workflow | 53.6 | 64.9 | 51.2 | 0.0 |
| kayak | lm_wf | 56.5 | 62.7 | 49.1 | 0.0 |
| kayak | rule_wf | 53.6 | 61.2 | 49.1 | 0.0 |

本轮判定：

| run_id | website | C3 status | evidence | notes |
|------|------|------|------|------|
| C3-R1 | kayak | unclear | LM 相对 rule 在 `Element Acc` 与 `Action F1` 上更高，但 `Step SR` 与 `SR` 持平；LM workflow 更抽象，而 rule workflow 更接近具体 trajectory | workflow 风格解释成立，但分数证据不足以支持完整复现 |

workflow 审计结论：

```text
LM workflow 明显更偏向抽象 sub-routine，而 rule workflow 更接近具体轨迹摘录，这与论文对两者差异的解释一致。
```

建议写入状态表的说明：

```text
在 test_task / kayak 的首轮 C3 实验中，LM induction 相对 rule induction 在 Element Acc 与 Action F1 上更高，且 LM workflow 更抽象、rule workflow 更具体；但 Step SR 与 SR 没有提升。因此，本轮将 C3 记为 unclear，而不是 reproduced。
```

### 10.6 当前执行记录：C3-R2（test_task / newegg）

本轮实际结果：

| website | condition | Element Acc | Action F1 | Step SR | SR |
|------|------|------:|------:|------:|------:|
| newegg | no_workflow | 35.0 | 44.8 | 25.5 | 0.0 |
| newegg | lm_wf | 40.4 | 45.4 | 28.9 | 0.0 |
| newegg | rule_wf | 37.2 | 46.8 | 28.0 | 0.0 |

本轮判定：

| run_id | website | C3 status | evidence | notes |
|------|------|------|------|------|
| C3-R2 | newegg | unclear | LM 相对 rule 在 `Element Acc` 与 `Step SR` 上更高，但 `Action F1` 低于 rule，`SR` 持平 | 关键方向部分支持，但仍不足以形成稳定复现 |

建议写入状态表的说明：

```text
在 test_task / newegg 的首轮 C3 实验中，LM induction 相对 rule induction 在 Element Acc 与 Step SR 上更高，但 Action F1 低于 rule，SR 仍持平为 0.0，因此本轮将 C3 记为 unclear。
```

### 10.7 当前阶段汇总

截至目前的运行状态：

| run_id | website | C3 status |
|------|------|------|
| C3-R1 | kayak | unclear |
| C3-R2 | newegg | unclear |
| C3-R3 | united | reproduced |

### 10.8 当前执行记录：C3-R3（test_task / united）

本轮实际结果：

| website | condition | Element Acc | Action F1 | Step SR | SR |
|------|------|------:|------:|------:|------:|
| united | no_workflow | 60.6 | 64.3 | 60.6 | 33.3 |
| united | lm_wf | 61.8 | 64.5 | 61.2 | 33.3 |
| united | rule_wf | 58.3 | 63.1 | 56.3 | 33.3 |

本轮判定：

| run_id | website | C3 status | evidence | notes |
|------|------|------|------|------|
| C3-R3 | united | reproduced | LM 相对 rule 在 `Element Acc`、`Action F1`、`Step SR` 上均更高，且 LM workflow 更抽象、rule workflow 更具体 | `SR` 与 rule 持平，但已满足 C3 最低成功判据中的两条 |

workflow 审计结论：

```text
LM workflow 更偏向抽象 sub-routine，而 rule workflow 更接近具体轨迹摘录，这与论文对两者差异的解释一致。
```

建议写入状态表的说明：

```text
在 test_task / united 的首轮 C3 实验中，LM induction 相对 rule induction 在 Element Acc、Action F1 与 Step SR 上均更高，且 LM workflow 更抽象、rule workflow 更具体；虽然 SR 持平，但本轮仍满足 C3 的最低成功判据，因此记为 reproduced。
```

当前阶段性结论：

- LM workflow 的抽象性解释在 `kayak` 与 `united` 上都成立
- `LM > rule` 在 `united` 上已经形成较完整的分解指标优势
- `kayak` 与 `newegg` 仍然是混合信号

因此，当前更合理的整体判断是：

```text
C3 在已运行的 3 个网站上呈 mixed evidence，但方向比前一轮更接近支持论文解释。当前结果已经较稳定地支持“LM workflow 更抽象、rule workflow 更具体”的解释性结论，并在 united 上支持“LM induction 优于 rule induction”；但由于 kayak 与 newegg 仍为 unclear，现阶段仍不宜把 C3 记为整体 reproduced。
```

---

## 11. 阶段 8：归档与下一步

### 11.1 当前推荐推进顺序

1. `kayak / test_task` 已完成
2. `newegg / test_task` 已完成
3. `united / test_task` 已完成
4. 继续保留 workflow 审计样例
5. 汇总 C3 主结果表后再决定是否进入 `C4`

### 11.1.1 下一批优先网站

建议优先补两个网站：

1. `newegg`
   - `domain=Shopping`
   - `subdomain=Digital`
   - 理由：C1 上属于较强支持案例，适合检查 LM vs rule 的优势是否更容易出现
2. `united`
   - `domain=Travel`
   - `subdomain=Airlines`
   - 理由：Travel 类站点更接近 `kayak`，但 `SR` 信号更敏感，适合检查 rule workflow 是否更容易过拟合具体轨迹

### 11.1.2 可直接复制的 `newegg` 命令

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web

python run_mind2web.py \
  --domain Shopping \
  --subdomain "Digital" \
  --website newegg \
  --workflow_path workflow/_empty.txt \
  --model qwen/qwen3.5-397b-a17b \
  --benchmark test_task \
  --log_dir results \
  --suffix no_workflow

python offline_induction.py \
  --mode auto \
  --domain Shopping \
  --subdomain "Digital" \
  --website newegg \
  --model_name qwen/qwen3.5-397b-a17b \
  --output_dir workflow \
  --output_suffix lm_wf

python run_mind2web.py \
  --domain Shopping \
  --subdomain "Digital" \
  --website newegg \
  --workflow_path workflow/newegg_lm_wf.txt \
  --model qwen/qwen3.5-397b-a17b \
  --benchmark test_task \
  --log_dir results \
  --suffix lm_wf

python rule_induction.py \
  --domain Shopping \
  --subdomain "Digital" \
  --website newegg \
  --output_path workflow/newegg_rule_wf.txt

python run_mind2web.py \
  --domain Shopping \
  --subdomain "Digital" \
  --website newegg \
  --workflow_path workflow/newegg_rule_wf.txt \
  --model qwen/qwen3.5-397b-a17b \
  --benchmark test_task \
  --log_dir results \
  --suffix rule_wf

python results/calc_score.py \
  --results_dir results/qwen/qwen3.5-397b-a17b/test_task/newegg/no_workflow

python results/calc_score.py \
  --results_dir results/qwen/qwen3.5-397b-a17b/test_task/newegg/lm_wf

python results/calc_score.py \
  --results_dir results/qwen/qwen3.5-397b-a17b/test_task/newegg/rule_wf
```

### 11.1.3 可直接复制的 `united` 命令

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web

python run_mind2web.py \
  --domain Travel \
  --subdomain "Airlines" \
  --website united \
  --workflow_path workflow/_empty.txt \
  --model qwen/qwen3.5-397b-a17b \
  --benchmark test_task \
  --log_dir results \
  --suffix no_workflow

python offline_induction.py \
  --mode auto \
  --domain Travel \
  --subdomain "Airlines" \
  --website united \
  --model_name qwen/qwen3.5-397b-a17b \
  --output_dir workflow \
  --output_suffix lm_wf

python run_mind2web.py \
  --domain Travel \
  --subdomain "Airlines" \
  --website united \
  --workflow_path workflow/united_lm_wf.txt \
  --model qwen/qwen3.5-397b-a17b \
  --benchmark test_task \
  --log_dir results \
  --suffix lm_wf

python rule_induction.py \
  --domain Travel \
  --subdomain "Airlines" \
  --website united \
  --output_path workflow/united_rule_wf.txt

python run_mind2web.py \
  --domain Travel \
  --subdomain "Airlines" \
  --website united \
  --workflow_path workflow/united_rule_wf.txt \
  --model qwen/qwen3.5-397b-a17b \
  --benchmark test_task \
  --log_dir results \
  --suffix rule_wf

python results/calc_score.py \
  --results_dir results/qwen/qwen3.5-397b-a17b/test_task/united/no_workflow

python results/calc_score.py \
  --results_dir results/qwen/qwen3.5-397b-a17b/test_task/united/lm_wf

python results/calc_score.py \
  --results_dir results/qwen/qwen3.5-397b-a17b/test_task/united/rule_wf
```

### 11.2 当前可直接写入状态表的说明

```text
C3 的 rule induction 入口已在当前 repo 中补齐，并已在 kayak / test_task 上完成首轮 baseline / rule / LM 三条件比较。当前结果显示 workflow 风格差异与论文解释一致，但关键指标上 LM 相对 rule 的优势尚不充分，因此当前更合理的阶段判定是 unclear。
```
