# AWM 机制分析与边界识别（阶段二 & 三）

> 本文档服务于 [research-roadmap.md](../design/research-roadmap.md) 中定义的层次二（论文结论为什么成立）与层次三（论文没有说清楚的部分）。
> 它建立在 C1-C5 首轮复现结果的基础上，直接使用现有日志与分析产物进行深入分析。
> 当前文档已完成全部 12 节：§1-§6 量化分析，§7 失败分类，§8 结论，§9-§10 案例实证与站点特征分析，§11 统一因果模型。

---

## 0. 数据基础

本文档的分析基于以下已有产物：

| 来源 | 日志数量 | 覆盖 condition | 覆盖 website |
|------|------:|------|------|
| C1 | ~140 | no_workflow / offline_wf | budget, yellowpages, kohls, newegg, sixflags, united, kayak |
| C2 | ~50 | no_workflow / online_wf | kayak (test_task), tripadvisor (test_website), reddit (test_domain) |
| C3 | ~110 | no_workflow / lm_wf / rule_wf | newegg, united, kayak |
| C4 | 69 | text_wf / code_wf / desc_only / html_only / desc_html | kayak, newegg, united |
| C5 | 19 + workflow texts | lm_wf quality stats | kayak, newegg, united |

日志路径：`experiments/mind2web/results/{model}/{split}/{website}/{condition}/`

每份 JSON 包含：完整 prompt（system + workflow + trajectory + observation）、模型输出、ground truth、逐步四项指标。

---

## 1. 指标分解：workflow 改善了什么环节

> 核心问题：AWM 的收益主要来自 element grounding（选对元素）还是 action guidance（选对操作+值）？

### 1.1 分析方法

从 C1 日志中，按以下维度交叉统计 baseline vs offline_wf 的逐步指标差异：

- **按 action type**（CLICK / TYPE / SELECT）：区分"值模板效应"与"元素定位效应"
- **按 step position**（前半 / 后半）：区分"启动引导"与"全程辅助"
- **按 website**：对比 reproduced 站点（newegg, kayak）与 not reproduced 站点（budget, sixflags）的分解差异

### 1.2 预期产物

- 指标分解表：Element Acc / Action F1 / Step SR 按维度交叉的 delta 值
- 收益归因结论：workflow 的主要贡献环节是什么

### 1.3 结果

**数据来源**：`scripts/step_breakdown.py` → `step_breakdown_output.txt` / `step_breakdown_results.csv`

#### 1.3.1 按 Action Type 的 Delta（offline_wf - no_workflow, gpt-4o/test_task）

| website | status | dElem CLICK | dStepSR CLICK | dActF1 TYPE | dStepSR TYPE |
|---------|--------|------:|------:|------:|------:|
| kayak | reproduced | +10.7% | +10.7% | +1.4% | +0.0% |
| newegg | reproduced | +9.1% | +6.1% | +50.0% | +33.3% |
| united | reproduced-leaning | +0.0% | +0.0% | +19.5% | +28.6% |
| yellowpages | unclear | +3.6% | +3.6% | +2.8% | +0.0% |
| kohls | unclear | +0.0% | +0.0% | +22.2% | +0.0% |
| budget | not reproduced | **-12.1%** | **-12.1%** | +8.4% | +9.1% |
| sixflags | not reproduced | **-6.1%** | **-6.1%** | +0.0% | +0.0% |

#### 1.3.2 按 Step Half 的 Delta（offline_wf - no_workflow, gpt-4o/test_task）

| website | status | dStepSR first | dStepSR second |
|---------|--------|------:|------:|
| kayak | reproduced | +0.0% | **+13.0%** |
| newegg | reproduced | +4.4% | +7.1% |
| united | reproduced-leaning | +0.0% | +7.1% |
| budget | not reproduced | -1.9% | **-10.9%** |
| sixflags | not reproduced | -5.9% | -3.3% |

#### 1.3.3 归因结论

1. **TYPE 步骤收益最稳定**：即使在整体 not reproduced 的站点（budget），TYPE 的 Action F1 也有 +8.4% 提升。workflow 提供了"值模板"（例如城市名、搜索关键词），帮助模型选择正确的输入值。[Appendix A1]

2. **CLICK 步骤是胜负手**：reproduced 站点（kayak, newegg）在 CLICK 上有 +9~11% 的 Element Acc 提升；not reproduced 站点则反向退化 -6~12%。这说明 workflow 对 element grounding 的帮助**高度依赖站点匹配度**——workflow 中的元素描述如果匹配目标 HTML 结构就帮忙，不匹配就误导。[Appendix A1]

3. **后半段收益在 kayak 上尤其明显**：kayak 后半段 +13% vs 前半段 +0%。这暗示 workflow 的价值不只是"启动引导"，还可能体现在随着 trajectory 变长，帮助模型保持正确的操作模式。newegg / united 的方向相符，但强度更弱。[Appendix A1]

4. **后半段退化在 budget 上尤其明显**：budget 后半段 -10.9%。这与 workflow 的累积误导效应一致；sixflags 的对应现象较弱，因此更稳妥的说法是 budget 提供了最强支持。[Appendix A1]

---

## 2. 因果路径：workflow 如何影响模型输出

> 核心问题：模型是真的"遵循"了 workflow，还是 workflow 只是无关上下文噪声？

### 2.1 分析方法：配对案例对比

从同一 task 的 baseline 与 offline_wf 日志中，按逐步 step_success 变化分为四类：

| 类型 | baseline | +workflow | 分析价值 |
|------|----------|-----------|---------|
| **正向贡献** | 0 | 1 | workflow 真正帮了什么 |
| **负向干扰** | 1 | 0 | workflow 误导了什么 |
| **无效** | 0 | 0 | workflow 没能解决的 |
| **冗余** | 1 | 1 | workflow 没有额外贡献 |

对每类挑 5-10 个典型 case，打开 prompt 逐步对比：

- 模型输出差异是否可归因于 workflow 文本
- workflow 中是否有直接对应当前 step 的指令
- 模型是否在输出中引用或复述了 workflow 内容

### 2.2 预期产物

- 四类配对的数量统计表
- 5-10 个正向 + 5-10 个负向的详细案例分析
- "workflow 遵循率"的粗略估计

### 2.3 结果

**数据来源**：`scripts/paired_case.py` → `paired_case_output.txt` + `case_studies/`

#### 2.3.1 四类配对统计（gpt-4o/test_task, offline_wf vs no_workflow）

| website | C1 status | positive | negative | ineffective | redundant | net gain |
|---------|-----------|------:|------:|------:|------:|------:|
| kayak | reproduced | 3 | **0** | 22 | 23 | **+3** |
| newegg | reproduced | 5 | **0** | 56 | 26 | **+5** |
| united | unclear | 3 | 2 | 35 | 23 | +1 |
| yellowpages | unclear | 4 | 2 | 30 | 25 | +2 |
| kohls | unclear | 2 | 2 | 33 | 16 | 0 |
| budget | not reproduced | 6 | **12** | 53 | 28 | **-6** |
| sixflags | not reproduced | 3 | **6** | 23 | 32 | **-3** |

#### 2.3.2 Cross-site 配对（online_wf vs no_workflow）

| target site | positive | negative | net | Pos/(Pos+Neg) |
|-------------|------:|------:|------:|------:|
| tripadvisor (qwen) | 4 | **18** | **-14** | 18.2% |
| reddit (qwen) | 2 | **5** | **-3** | 28.6% |

#### 2.3.3 按 Action Type 的负向干扰分布

tripadvisor 的 18 个 negative 步骤中：
- CLICK: 14 (78%) — workflow 引导模型选择了错误的元素
- TYPE: 4 (22%) — workflow 提供了略有偏差的值（如 `Eiffel Tower Paris` vs `Eiffel Tower`）

典型模式（tripadvisor task 2, 3, 7, 10, 13, 22）：baseline 正确执行 CLICK 进入搜索页，但 workflow 诱导模型改为 TYPE 输入城市名——因为 workflow 中从 kayak 归纳的搜索流程是"先 TYPE 地点，再 CLICK 建议"，但 tripadvisor 的首页需要先 CLICK 类别链接。

#### 2.3.4 核心发现

1. **reproduced 站点的 negative = 0**：workflow 在匹配站点上是"无害"的——要么帮忙，要么不影响，绝不误导。这是 AWM work 的关键前提。[Appendix A2]

2. **not reproduced 站点的 negative >> positive**：workflow 不匹配时变成有害噪声。budget 的 12 个 negative 中有 11 个是 CLICK（91%），说明 workflow 中的元素描述直接误导了 element grounding。[Appendix A2]

3. **ineffective 占比最大（45-65%）**：大部分步骤 workflow 既不帮忙也不妨碍——主要是 SKIP 步骤（ground truth 不在 candidate 中）和本身就困难的步骤。这意味着 **AWM 的实际影响面有限**：只在一小部分步骤上产生影响，但在匹配站点上这个影响是净正向的。[Appendix A2]

4. **workflow 遵循率粗估**：在 positive + negative 步骤中（即 workflow 真正改变了模型行为的步骤），占总步骤的 6-18%。workflow 不是"每一步都在引导"，而是在关键步骤上偶尔介入。[Appendix A2]

---

## 3. 泛化边界：为什么 cross-site 退化

> 核心问题：C2 中 tripadvisor 和 reddit 的退化根因是什么？

### 3.1 分析方法

从 C2 日志中定位退化的具体环节：

**3.1.1 退化定位**

- 按 action type 分组：退化集中在 CLICK / TYPE / SELECT 的哪一类？
- 按 step position 分组：是全程退化，还是特定阶段退化？
- baseline 在新站点的绝对水平：是 baseline 本身就弱，还是 baseline 正常但 workflow 拖了后腿？

**3.1.2 workflow 适配度**

- 对比 online_wf 的 workflow 文本与目标站点实际操作流程的匹配度
- workflow 中的步骤模板是否与目标站点的 HTML 结构/元素命名相容

**3.1.3 两种退化假说**

- **假说 A：workflow 内容不适配** — workflow 从 kayak 归纳而来，不适用于 tripadvisor/reddit 的操作逻辑
- **假说 B：observation 格式变化** — 新站点的 HTML 结构导致 element grounding 整体崩溃，与 workflow 无关

### 3.2 预期产物

- cross-site 退化的指标分解表
- 假说 A vs B 的证据对照
- 退化根因的初步判定

### 3.3 结果

**数据来源**：`scripts/cross_site_diag.py` → `cross_site_diag_output.txt`

#### 3.3.1 Baseline 绝对水平对比

| site | role | skip rate | CLICK EA | CLICK SR | TYPE EA | TYPE SR |
|------|------|------:|------:|------:|------:|------:|
| kayak (qwen) | source | 29.2% | 75.0% | 75.0% | 83.3% | 50.0% |
| tripadvisor (qwen) | target | **44.9%** | 81.2% | 81.2% | 65.2% | 34.8% |
| reddit (qwen) | target | 33.9% | 84.2% | 82.2% | 94.4% | 44.4% |

关键观察：
- tripadvisor 的 skip rate 高出源站 **+16pp**，说明其 HTML 结构导致更多 ground truth 元素未出现在 candidate 中
- reddit 的 baseline CLICK 性能反而**高于** kayak，排除了"baseline 本身崩溃"的可能

#### 3.3.2 假说判定

**tripadvisor: 假说 A + B 混合**

- **B 证据**：skip rate +16pp（HTML 结构差异导致 candidate 质量下降）
- **A 证据**：18 个 negative 步骤中 14 个是 CLICK（78%），5 个 task 有 2+ 个 negative 步骤（系统性不匹配）
- 典型模式：workflow 中 kayak 的搜索流程是 TYPE 地点 → CLICK 建议，但 tripadvisor 首页需要先 CLICK 类别链接再进入搜索。workflow 诱导模型跳过 CLICK 直接 TYPE，导致元素选错。
- **判定**：混合退化——HTML 结构变化削弱了 baseline 的 candidate 质量（B），同时 workflow 从 kayak 归纳的操作逻辑不适配 tripadvisor 的导航结构（A）。[Appendix A3, Appendix B6]

**reddit: 主要假说 A**

- **B 证据**：无（skip rate 仅 +4.7pp，baseline CLICK EA 反而更高）
- **A 证据**：5 个 negative 中 4 个是 CLICK（80%），workflow 关键词（`search reddit`, `Join`, `Sort`）与实际 task 的操作流程不完全匹配
- **判定**：baseline 本身表现正常，退化主要来自 workflow 内容不适配。[Appendix A3]

#### 3.3.3 退化根因总结

| target site | 主要假说 | 退化机制 |
|-------------|---------|---------|
| tripadvisor | A+B 混合 | HTML 差异 + 操作逻辑不匹配 |
| reddit | A（workflow 不适配） | workflow 步骤模板不适配 reddit 导航 |

#### 3.3.4 Offline vs Online 的机制差异

上面的 cross-site 结果解释了 `online_wf` 为什么会退化，但还没有正面回答：`offline_wf` 和 `online_wf` 在机制上到底有什么不同。

基于同一站点 `kayak` 的 step-level / paired-case 对照，以及 `tripadvisor / reddit` 的 online 负例，可得到一个更完整的 trade-off 读法（见 `Appendix A7`）：

- **offline_wf 更像训练集归纳出的广义操作库**：在 `kayak` 上，它对 `CLICK` grounding 的帮助更强（`dStepSR CLICK = +10.7%`，高于 online 的 `+7.1%`），并且 direct pair 中 online 相对 offline 的唯一负例也是一个 `CLICK` 选错结果项。
- **online_wf 更像测试时成功 trajectory 压缩出的局部 routine**：在 `kayak` 上，它对 `TYPE` 的局部值/格式修正更强（`dActF1 TYPE = +19.2%`，`dStepSR TYPE = +16.7%`），而 direct pair 中 online 相对 offline 的唯一正例正是一个 `TYPE` 值格式修正。
- **因此，两者更像 trade-off，而不是简单排序**：offline 在 `CLICK` 侧更稳，online 在 `TYPE/value guidance` 侧更强；两者在 `kayak` 上都提升 `Step SR`，但收益类型不同。

这个对照也让论文 `§3.2.2` 中的 offline/online trade-off 更容易被具体化：

- **offline 的风险**：workflow 来源于训练数据，文本上更广、更可复用，但当 train-test gap 增大、语义不匹配时，会受到 distribution gap 拖累。
- **online 的风险**：workflow 来源于模型自身成功 trajectory，更贴近当前 test distribution，但也更容易把局部 routine 或错误子流程固化下来，并在更大 shift 下重放。`tripadvisor` 提供了较强支持，`reddit` 提供了方向一致但更弱的支持。

更保守地说，当前 Mind2Web 首轮证据支持以下工作性结论：**offline 与 online 的差别，不只是“哪个更好”，而是“广义可复用性”与“测试时贴近性”之间的权衡**。论文正文对这一点主要停留在 verbal trade-off 层面，而当前复现至少把它推进到了 step-level 与 case-level 的可追溯证据。

#### 3.3.5 Online 的 small-data 效率是条件性的

论文的 online-memory 叙事还隐含另一层意思：少量成功 trajectory 可能已经足以让 workflow 变得有用。当前日志可用 prefix-level 方式近似重建这一点（见 `Appendix A8`）。

结果不是单向支持，而是明显条件化：

- **kayak**：在 `budget=1`（即仅有 1 个先前归纳样本）时，累计 `Step SR` 已达 `+5.00pp`；最终 prefix 为 `+5.63pp`。这说明 very-small-budget 的早期收益在 source-style setting 上确实存在。
- **tripadvisor**：从 `budget=1` 开始，累计 `Step SR` 就是负的（`-3.57pp`），且后续没有出现正 prefix；最终为 `-11.74pp`。这里 small-data 并没有带来“早期学习”，而是更像“早期固化错误模式”。
- **reddit**：直到 `budget=10` 才出现一个较弱的正 prefix（`+2.02pp`），最终又回到负值（`-2.16pp`）。因此它不构成稳定的 small-data success case。

更稳妥的结论是：**online memory 的 small-data 收益主要出现在 source-style setting，而不是一个可直接推广到 cross-site 场景的普适性质**。换句话说，“少量样本即可起效”在当前证据下不是 false，但它只在 workflow 与测试分布已经较接近时才更容易成立。

**对论文主张的影响**：论文声称"online AWM 在更大 distribution gap 下更有优势"。但实际上，当 distribution gap 增大时，online 归纳出的 workflow 恰恰因为源自少量成功 trajectory，更容易过拟合源站的操作模式，反而在目标站产生负迁移。这一机制论文没有讨论。

---

## 4. LM vs Rule：抽象性差异的具体体现

> 核心问题：LM induction 和 rule induction 产生的 workflow 在文本层面到底有什么不同？这种不同如何映射到性能差异？

### 4.1 分析方法

**4.1.1 workflow 文本对比**

- 从 `workflow/` 目录中取出同一 website 的 lm_wf 和 rule_wf 文本
- 人工标注差异维度：抽象程度、步骤粒度、是否保留具体值、是否包含条件分支

**4.1.2 性能差异的逐步归因**

- 从 C3 日志中，找 lm_wf 对但 rule_wf 错（及反向）的 step
- 对比这些 step 中 workflow 提供的指令差异
- 判断：是 LM workflow 的抽象表述帮助了泛化，还是 rule workflow 的具体值反而误导了模型？

### 4.2 预期产物

- LM vs rule workflow 的文本特征对比表
- 性能差异的逐步归因案例
- "抽象有利于泛化"这一论文解释的证据强度评估

### 4.3 结果

**数据来源**：`scripts/wf_text_compare.py` → `wf_text_compare_output.txt`

#### 4.3.1 文本特征量化对比

> **计数口径说明**：本节沿用 `wf_text_compare.py` 的文本比较口径，因此 workflow 数量与平均步骤数按“文本块”统计，并将 `Summary Workflows` 计入对比范围。`§6` 的 workflow 库统计则沿用 C5/runbook 口径，不计入 summary block。因此 `§4` 与 `§6` 的 `#workflows / avg steps/WF` 数值不应被当作同一指标直接比较。

| 特征 | kayak LM | kayak Rule | newegg LM | newegg Rule | united LM | united Rule |
|------|------:|------:|------:|------:|------:|------:|
| Workflow 数量 | 8 | 17 | 6 | 19 | 6 | 24 |
| 总步骤数 | 14 | 213 | 10 | 149 | 16 | 217 |
| 平均步骤/WF | **1.8** | 12.5 | **1.7** | 7.8 | **2.7** | 9.0 |
| Placeholder 数 | **13** | 0 | **6** | 0 | **15** | 0 |
| 具体值数 | 0 | **25** | 0 | **16** | 0 | **41** |
| 抽象/可复用 WF | **8** | 0 | **6** | 0 | **6** | 0 |
| Task-specific WF | 0 | **17** | 0 | **19** | 0 | **24** |

#### 4.3.2 结构性差异总结

**LM workflow 的特征**：
- 少量（6-8 个）高度抽象的 sub-routine
- 每个 sub-routine 只有 2-3 步
- 全部使用 `{placeholder}` 表示变量，无具体值
- 标题是动词短语，如 `enter_search_location`, `apply_amenity_filter`
- 相当于一份"操作字典"——模型遇到类似操作模式时查阅

**Rule workflow 的特征**：
- 大量（17-24 个）完整的具体 trajectory
- 每条 trajectory 7-13 步，包含完整的从头到尾操作序列
- 保留所有具体值（城市名、数字、产品名）
- 标题是完整 task 描述，如 `Concrete Trajectory for Find hotels in Las Vegas...`
- 相当于一份"案例库"——模型通过匹配最近似的完整案例来执行

#### 4.3.3 论文主张评估

论文声称"LM induction produces more abstract, reusable sub-routines"。

三个站点均 **4/4 指标支持**：
1. ✅ LM 使用更多 placeholder（LM 6-15 vs Rule 0）
2. ✅ Rule 保留更多具体值（Rule 16-41 vs LM 0）
3. ✅ LM workflow 更紧凑（LM 1.7-2.7 步/WF vs Rule 7.8-12.5 步/WF）
4. ✅ LM workflow 数量更少（LM 6-8 vs Rule 17-24）

**判定**：论文关于 LM vs Rule 抽象性差异的解释性主张**在文本层面完全成立**。这是 C1-C3 中得到最强支持的论文主张。[Appendix C1, Appendix C2, Appendix C3]

#### 4.3.4 但抽象性 ≠ 性能优势

需要注意的是：文本层面的抽象性差异是清晰的，但这**不自动意味着 LM 的性能总是更好**。从 C3 的配对数据看：

| website | LM net gain | Rule net gain | 性能差异方向 |
|---------|------:|------:|------|
| newegg (qwen) | +2 | +4 | Rule ≥ LM |
| united (qwen) | +1 | -2 | LM > Rule |
| kayak (qwen) | 0 | -1 | LM ≥ Rule |

united 上 LM 确实优于 Rule（Rule 的具体值误导了模型），但 newegg 上 Rule 在配对净收益上有竞争力（Rule 的具体值恰好匹配了 test task 的操作模式，因为 newegg 的 cross-task 泛化场景中操作模式相对固定；注：c3-runbook 对 newegg 的正式判定为 `unclear`）。

这暗示：**抽象性的价值取决于 test task 与 train task 的操作模式差异程度**。差异大时，抽象有利；差异小时，具体案例反而更有用。论文没有展开讨论这个条件。[Appendix C1, Appendix A3]

---

## 5. 表示形式的影响

> 对应 C4：code vs text workflow、NL vs HTML 环境表示

### 5.1 分析方法

C4 包含两个子实验：

1. **Code vs Text workflow**：同一 LM 归纳内容，以 Python 函数格式（`code_wf`）vs 自然语言格式（`text_wf`/`lm_wf`）注入 prompt
2. **NL vs HTML 环境表示**：observation 中使用 `desc_only`（纯 NL 描述）、`html_only`（纯 HTML）、`desc_html`（NL + HTML）

- **Code vs Text workflow**：当前只在 `kayak` 上完成首轮
- **NL vs HTML**：当前在 `kayak / newegg / united` 三站点上完成首轮

### 5.2 结果

#### 5.2.1 Code vs Text Workflow（kayak, qwen）

| condition | Elem Acc | Act F1 | Step SR | SR |
|-----------|------:|------:|------:|------:|
| no_workflow | 53.6 | 64.9 | 51.2 | 0.0 |
| text_wf (NL) | 55.3 | 60.8 | 45.8 | 0.0 |
| code_wf (Python) | 52.4 | 63.4 | 48.0 | 0.0 |
| lm_wf (NL, same content) | 56.5 | 62.7 | 49.1 | 0.0 |

**判定**：text_wf 与 code_wf 的差异确实不大（Step SR 差 2.2pp），但**两者均低于 baseline**（51.2%）。论文声称"code vs text 差异不大"在方向上成立，但论文隐含的前提——两种表示都优于 baseline——在 kayak/qwen 上未成立。[Appendix A4]

`lm_wf`（49.1%）略优于 `text_wf`（45.8%）和 `code_wf`（48.0%），可能因为 exemplar 选择差异。

#### 5.2.2 NL vs HTML 环境表示（3 站点, qwen）

**kayak:**

| condition | Elem Acc | Act F1 | Step SR | SR |
|-----------|------:|------:|------:|------:|
| no_workflow | 53.6 | 64.9 | **51.2** | 0.0 |
| desc_only | 54.8 | 61.2 | 45.3 | 0.0 |
| html_only | 52.4 | 63.5 | 48.0 | 0.0 |
| desc_html | 54.8 | 63.5 | **50.3** | 0.0 |

**newegg:**

| condition | Elem Acc | Act F1 | Step SR | SR |
|-----------|------:|------:|------:|------:|
| no_workflow | 35.0 | 44.8 | 25.5 | 0.0 |
| desc_only | **42.0** | 44.3 | **30.5** | 0.0 |
| html_only | 36.2 | 42.6 | 23.9 | 0.0 |
| desc_html | 38.0 | 42.4 | 30.3 | 0.0 |

**united:**

| condition | Elem Acc | Act F1 | Step SR | SR |
|-----------|------:|------:|------:|------:|
| no_workflow | 60.6 | 64.3 | **60.6** | 33.3 |
| desc_only | 57.9 | 61.9 | 55.9 | 33.3 |
| html_only | 61.2 | 64.5 | **60.6** | 33.3 |
| desc_html | 57.9 | 61.1 | 51.7 | 16.7 |

#### 5.2.3 NL vs HTML 判定

论文声称"Desc only 优于加入 HTML"。逐站点检查 Step SR：

| 站点 | desc_only | html_only | desc_html | 论文主张 |
|------|------:|------:|------:|------|
| kayak | 45.3 | 48.0 | 50.3 | **NOT supported** — desc_only 最低 |
| newegg | **30.5** | 23.9 | 30.3 | **Supported** — desc_only 最高 |
| united | 55.9 | **60.6** | 51.7 | **NOT supported** — html_only 最高 |

**整体判定**：not reproduced after three-site first run。只有 newegg 呈现 `desc_only` 最优，但 kayak 与 united 都不支持论文主张，而且 newegg 的 `desc_html` 与 `desc_only` 基本持平，未形成论文要求的稳定收益结构。一个可能的解释是：united 的 HTML 元素命名本身就具有高可读性（如 `tab TRAVEL INFO`、`heading Check-in`），此时加入 NL 描述反而引入了冗余甚至噪声。[Appendix A4]

#### 5.2.4 论文未讨论的发现

1. **desc_html 并非"两全其美"**：在 united 上 desc_html 的 Step SR（51.7%）显著低于 html_only（60.6%）和 desc_only（55.9%），SR 从 33.3% 降到 16.7%。一种与当前结果相一致的解释是：混合两种表示增加了 prompt 长度和冗余，进而干扰了模型对关键线索的聚焦。[Appendix A4]
2. **表示层的最优选择是站点相关的**：newegg 适合 desc_only，united 适合 html_only。论文给出了一个跨站点的统一推荐，但实际上不存在一致最优的表示策略。[Appendix A4]

---

## 6. Workflow 质量与性能关系

> 对应 C5：workflow 数量、coverage、utility rate、function overlap

### 6.1 分析方法

从 `workflow/` 目录中提取各 workflow 文件的结构特征，结合对应 condition 的性能数据，检验论文关于 workflow 质量的主张。

### 6.2 结果

#### 6.2.1 Workflow 库基本统计

**LM induction（offline）：**

| website | #workflows | #steps | avg steps/WF | #placeholders | #concrete vals | function overlap |
|---------|------:|------:|------:|------:|------:|------:|
| kayak | 7 | 14 | 2.0 | 13 | 1 | 0.0 |
| newegg | 5 | 10 | 2.0 | 6 | 2 | 0.0333 |
| united | 5 | 16 | 3.2 | 15 | 5 | 0.0 |

**Rule induction：**

| website | #workflows | #steps | avg steps/WF | #placeholders | #concrete vals |
|---------|------:|------:|------:|------:|------:|
| kayak | 17 | 213 | 12.5 | 0 | 25 |
| newegg | 19 | 149 | 7.8 | 0 | 16 |
| united | 24 | 217 | 9.0 | 0 | 41 |

**Online induction：**

| website | #workflows | #steps | #placeholders |
|---------|------:|------:|------:|
| kayak | 5 | ~10 | 7 |
| tripadvisor (qwen) | 5 | 8 | 6 |
| reddit (qwen) | 5 | 10 | 7 |

#### 6.2.2 论文主张逐条检验

**主张 1："workflow 数量较精简"**

- LM/offline: 5-7 个 workflow — ✅ 精简
- Rule: 17-24 个 — 不精简，但论文主要指 LM induction
- Online: 5 个 — ✅ 精简

**判定**：supported（LM 和 online induction 产出紧凑的 workflow 库）。[Appendix A5, Appendix C3]

**主张 2："utility rate 较高"**

所有 workflow condition 中，workflow 文本均被注入 prompt（100% injection rate）。但这里的 utility 不等于"被模型遵循"。从 §2 的配对分析看，workflow 真正改变模型行为的步骤只占 6-18%。

**判定**：在当前近似统计口径下 supported，但 proxy 偏宽。prompt 注入率为 100%，而"实际被遵循"的比例从 §2 的配对分析看只有 6-18%。因此，这里支持的是“workflow 进入 prompt 并具备可用性”的宽口径 utility，而不是“workflow 被模型真实遵循”的强口径 utility。[Appendix A5]

**主张 3："function overlap 较低"**

LM workflow 的 function overlap 极低（0-3.33%；来源：`c5-runbook.md` 正式口径），每个 workflow 覆盖不同的操作类型（enter_location, select_date, apply_filter 等），无明显冗余。

**判定**：supported。[Appendix A5]

**主张 4："coverage 不必很高"**

这是论文对 Mind2Web cross-task 场景的特殊说明。确实，5-7 个抽象 workflow 不可能覆盖所有可能的 test task 操作。但从 §2 的数据看，ineffective 步骤占 45-65%，这意味着大量步骤没有被任何 workflow 覆盖。

**判定**：在当前近似统计口径下支持 coverage 足够高，但这与论文中“coverage 不必很高”的陈述并不完全等价。runbook 里的 coverage 统计更接近“workflow 文本进入 prompt 并在样本中可见”的宽口径 proxy，而不是严格的功能覆盖率。因此，这一项应被理解为：当前 workflow 具备高 prompt-level coverage proxy，而不是已经证明“低 coverage 也无损价值”。[Appendix A5]

#### 6.2.3 Workflow 质量与性能的交叉分析

| website | induction | #WFs | Step SR delta vs baseline | 判读 |
|---------|-----------|------:|------:|------|
| kayak | LM (offline) | 7 | +2.3pp (gpt-4o) | 精简库 + 匹配站点 → 正向 |
| newegg | LM | 5 | +3.4pp (qwen) | 同上 |
| united | LM | 5 | +0.6pp (qwen) | 精简但收益很小 |
| kayak | Rule | 17 | -2.1pp (qwen) | 大量具体 trajectory → 轻微负向 |
| newegg | Rule | 19 | +2.5pp (qwen) | 操作模式固定，具体案例恰好有用 |
| united | Rule | 24 | -4.3pp (qwen) | 过多具体值误导 |

**核心发现**：workflow 数量本身不是决定因素。首轮结果更支持 content-match 比 raw count 更重要。newegg 的 Rule workflow（19 个）在配对净收益上与 LM（5 个）有竞争力（c3-runbook 判定为 `unclear`），因为 newegg 的 cross-task 操作模式相对固定，具体案例直接可用。[Appendix A5, Appendix A3]

---

## 7. Failure Taxonomy 初稿

> 汇总第 1-4 节分析中发现的失败模式，形成分类体系。

### 7.1 分类框架

| 失败类型 | 描述 | 来源章节 | 严重程度 |
|---------|------|---------|---------|
| **workflow 误导** | workflow 模板不适用于当前 step，导致模型偏离正确操作 | 2, 3 | 高：直接导致 not reproduced |
| **workflow 无效** | workflow 存在但未影响模型输出，性能无变化 | 2 | 低：不产生负面影响 |
| **cross-site 不适配** | workflow 从源站归纳，不适配目标站操作逻辑 | 3 | 高：是 cross-site 退化的主因 |
| **element grounding 崩溃** | 目标站 HTML 结构差异过大，element 选择整体失败 | 3 | 中：tripadvisor skip rate +16pp |
| **过度具体** | rule workflow 保留了过多源站具体值，妨碍泛化 | 4 | 中：仅 united 上明显 |
| **ground truth 缺失** | 正确元素不在 candidate 中，被迫跳过 | 1 | 低：影响绝对分但不影响相对比较 |
| **表示层噪声** | desc_html 混合表示增加 prompt 长度，导致注意力分散 | 5 | 中：united desc_html SR 从 33.3% 降到 16.7% |
| **workflow 覆盖有限** | 5-7 个抽象 workflow 无法覆盖大部分 test 步骤 | 6 | 结构性：45-65% 步骤无 workflow 可用 |

### 7.2 各类失败的占比统计

基于 paired_case 分析（gpt-4o/test_task 7 站点，offline_wf vs no_workflow，共 475 个配对步骤；来源：`paired_case_output.txt`）：

| 失败类型 | 对应 paired 类别 | 步骤数 | 占比 | 典型站点 |
|---------|-----------------|------:|------:|---------|
| **workflow 误导** | negative | 24 | 4.6% | budget (12), sixflags (6) |
| **workflow 无效** | ineffective | 252 | 48.2% | 所有站点 |
| **ground truth 缺失** | ineffective 中的 SKIP | ~195 | 37.3% | kohls, newegg（SKIP 密集） |
| **cross-site 不适配** | negative (cross-site) | 23 | — | tripadvisor (18), reddit (5) |
| **过度具体** | negative (rule_wf) | ~8 | — | united (rule_wf 4 neg) |

注：冗余（redundant = 173, 33.1%）不算失败，但说明 workflow 大部分时候是旁观者。

### 7.3 与论文叙事的对照

| 失败模式 | 论文是否讨论 | 评价 |
|---------|-------------|------|
| workflow 在不匹配站点上产生负迁移 | **未讨论** | 论文只报告了 online 在 cross-site 上"优于 baseline"，没有展示 workflow 误导的案例 |
| SKIP 步骤占比高（37%） | **未讨论** | ground truth 不在 candidate 中的步骤被强制计为 0 分，拉低了所有 condition 的绝对分数，但不影响相对比较 |
| workflow 有效窗口窄（仅 6-18% 步骤受影响） | **未讨论** | 论文呈现的是聚合分数，没有报告 workflow 在多大比例的步骤上真正改变了模型行为 |
| 抽象性优势依赖于 task 差异程度 | **未讨论** | 论文只报告了 LM > Rule 的性能结论，没有分析在什么条件下这个优势成立 |
| 后半段 trajectory 的累积误导效应 | **未讨论** | budget 后半段 -10.9%，workflow 的误导会随 trajectory 变长被放大 |

---

## 8. 阶段性结论模板

> 当第 1-4 节分析完成后，填写此处。

### 层次二结论：AWM 为什么 work

基于 C1-C3 日志的逐步分析和 §9 的 prompt-level 案例实证，AWM 在匹配站点上 work 的机制可以总结为：

1. **值模板效应（TYPE 步骤）**：workflow 为 TYPE 操作提供了输入值的格式和类型提示（如"搜索地点名"、"输入价格上限"），帮助模型选择正确的输入值。这个效应在所有站点上都是正向的，即使在整体 not reproduced 的站点上也有 +8% 的 Action F1 提升。这里的最强证据来自 §1 的 step-level 汇总，而不是单个 case。[Appendix A1]

2. **元素定位效应（CLICK 步骤）**：workflow 中的元素描述（如 `[checkbox] {filter_option}`）帮助模型在候选元素中选对目标。但这个效应**高度依赖站点匹配度**——workflow 描述与实际 HTML 结构一致时帮忙（kayak +10.7%），不一致时反而误导（budget -12.1%）。[Appendix A1]

3. **策略重定向**（§9 新发现）：workflow 在关键决策点提供正确的操作模式。P-2 中 workflow 将模型从"浏览分类"策略重定向为"搜索优先"策略。P-1 中 workflow 阻止了模型的 premature termination。这类收益在聚合指标中不可见，但在 prompt-level 案例中清晰呈现。[Appendix B1, Appendix B2]

4. **标签格式校正**（§9 新发现）：workflow 有时不仅提供操作方向，还会约束输出格式。P-3 中 workflow 引导模型输出 `SELECT [Most Reviews]` 而非数字 index `SELECT [5]`。这说明 workflow 对模型的帮助不只体现在“做什么”，也体现在“怎么表达动作参数”。[Appendix B2]

5. **实际影响面有限但在匹配站点上净正向**：workflow 只在 6-18% 的步骤上真正改变模型行为。在匹配站点上，这些改变是净正向的（negative = 0）。AWM 不是"每一步都在引导"，而是"在关键步骤偶尔介入，且介入时不犯错"。[Appendix A2]

6. **后半段辅助效应**：在匹配站点上，workflow 的收益在 kayak 的 trajectory 后半段尤其明显（+13% vs 前半段 +0%），暗示 workflow 帮助模型在长 trajectory 中保持正确的操作模式，而不只是提供"第一步怎么做"的启动引导。[Appendix A1]

### 层次三结论：论文没有说清楚的部分

1. **workflow 在不匹配站点上是有害的**（§2, §3）：论文只报告了 online AWM 在 cross-site 上优于 baseline，但我们的复现显示 tripadvisor 和 reddit 上 online 均低于 baseline。workflow 从源站归纳的操作逻辑在目标站产生负迁移，negative 步骤远多于 positive（tripadvisor: 18 vs 4）。论文没有讨论 workflow 何时有害。[Appendix A2, Appendix A3, Appendix B6]

2. **抽象性优势是有条件的**（§4）：LM workflow 在文本层面确实更抽象（4/4 指标支持），但性能优势取决于 test task 与 train task 的操作模式差异程度。在操作模式固定的站点（newegg），Rule workflow 在配对净收益上有竞争力（c3-runbook 判定 `unclear`）。论文只报告了 LM > Rule 的总体结论，没有讨论这个边界条件。[Appendix C1, Appendix A3]

3. **workflow 的有效窗口很窄**（§2）：大部分步骤（45-65%）属于 ineffective，workflow 既不帮忙也不妨碍。AWM 的聚合分数提升掩盖了一个事实：workflow 真正起作用的步骤很少。论文用聚合分数呈现结果，没有报告 workflow 的实际影响面。[Appendix A2]

4. **SKIP 步骤的影响**（§7）：37% 的步骤因为 ground truth 元素不在 candidate 中被强制跳过并计为 0 分。这些步骤拉低了所有 condition 的绝对分数但不影响相对比较。然而，不同站点的 skip rate 差异很大（kayak 29% vs tripadvisor 45%），这意味着跨站点的绝对分数不可直接比较。论文没有报告 skip rate 的站点间差异。[Appendix A1, Appendix A2]

5. **累积误导效应**（§1）：在 not reproduced 站点上，workflow 的误导在 trajectory 后半段被放大（budget 后半段 -10.9%）。这与匹配站点上的"后半段辅助效应"恰好相反，暗示 workflow 的正/负影响都会随 trajectory 长度累积。论文没有分析 workflow 影响的时序特征。[Appendix A1]

6. **表示层最优策略是站点相关的**（§5）：论文统一推荐"Desc only 优于 HTML"，但 3 站点中仅 newegg 支持，united 上 html_only 反而最好（因为 HTML 元素命名本身可读性高）。此外 desc_html 混合表示在 united 上导致 SR 从 33.3% 降至 16.7%，论文没有讨论混合表示可能带来的注意力分散问题。[Appendix A4]

7. **workflow 的实际影响面有限**（§6）：5-7 个抽象 workflow 只在 6-18% 的步骤上真正改变了模型行为，45-65% 的步骤属于 ineffective。论文用聚合分数呈现 AWM 的提升，但没有讨论这种"稀疏影响"的结构特征。这意味着 AWM 的实际价值主要集中在少量关键步骤，而不是均匀覆盖整个 trajectory。[Appendix A2, Appendix A5]

8. **表层对齐率与性能不呈正相关**（§10，exploratory metric）：基于关键词匹配 heuristic 的 workflow-target 对齐率在 not reproduced 站点反而偏高（budget 97.2%, sixflags 94.2%），kayak 最低（70.6%）。newegg（90.9%, reproduced）是例外。这提示表层覆盖 ≠ 语义适配。该发现基于 `alignment_rate.py` 的 exploratory metric，匹配方法的 validity 有限。[Appendix A6]

9. **AWM 成功可能需要双重条件**（§10, §11，working hypothesis）：workflow 可复用性（短小参数化 sub-routine，而非完整任务序列）+ baseline 提升空间。这是基于首轮 4 站点观察的工作假说，不是经过独立验证的规律。缺少任一条件的站点在首轮中表现为 AWM 无效（sixflags baseline 已高）或有害（budget workflow 域外误导）。论文没有讨论这一成功前提。[Appendix A1, Appendix C1, Appendix C4, Appendix A6]

---

## 9. Prompt-Level 案例实证

> 核心问题：workflow 到底怎样改变了模型的逐步输出？§2 给出了统计，本节给出具体 prompt→output 对比。

### 9.1 正向案例（reproduced 站点：baseline 错 → workflow 对）

#### P-1: kayak / task 1 / step 9 — 防止过早终止

> **Source**: `results/gpt-4o/test_task/kayak/{no_workflow,offline_wf}/1.json`，step_success 索引 9。已回源核对：CONFIRMED。

**Task:** "Find the cheapest Hawaii package for two adults from June 18 to 21"（eval task；few-shot exemplar 为 Las Vegas 酒店任务）

| | baseline | workflow |
|---|---|---|
| step_success | 0 | **1** |
| 模型输出 | pred_act 为空字符串；output 为自然语言总结 "The cheapest small car rental deal… $381."（幻觉，与当前 task 无关） | `CLICK [57318]`（Sort by Cheapest） |
| target_act | `CLICK [57318]` | `CLICK [57318]` |
| 失败模式 | 模型幻觉任务已完成，输出无关的"结果描述"而非 grounded action | — |

**workflow 介入机制**：Workflow 8 (`View and Select Deals`) 提示"在搜索结果页上，应 HOVER/CLICK 查看 deal"，阻止了模型 premature termination。

#### P-2: newegg / task 4 / step 0 — 策略重定向

> **Source**: `results/gpt-4o/test_task/newegg/{no_workflow,offline_wf}/4.json`，step_success 索引 0。已回源核对：CONFIRMED（task description 已修正）。

**Task:** "Find a new drone priced between 25 to 50 dollar and ships from USA with average customer rating of 4 and upwards and save the search at the end."（eval task；few-shot exemplar 为 gaming desktop 任务）

| | baseline | workflow |
|---|---|---|
| step_success | 0 | **1** |
| 模型输出 | `CLICK [10463]`（点击 Electronics 分类导航） | `TYPE [126] [drone]`（在搜索框输入） |
| target_act | `TYPE [126] [drone]` | `TYPE [126] [drone]` |
| 失败模式 | 默认"浏览分类"策略，未使用搜索功能 | — |

**workflow 介入机制**：`search_and_apply_filters` workflow 第一步就是 `[searchbox] Search Site -> TYPE: {search-term}`，将模型从"browse-first"策略重定向为"search-first"策略。

> **注**：原文曾误将 few-shot exemplar task（"Find gaming desktop with rtx4000"）作为 eval task。实际 eval task 为 drone 搜索任务，与 `TYPE [126] [drone]` 语义一致。

#### P-3: newegg / task 5 / step 3 — 值格式校正

> **Source**: `results/gpt-4o/test_task/newegg/{no_workflow,offline_wf}/5.json`，step_success 索引 3。已回源核对：CONFIRMED（task description 已修正）。

**Task:** "Find bluetooth vertical mouse with most reviews and add two to my shopping cart."（eval task；few-shot exemplar 为 "Remove SSD from cart" 任务）

| | baseline | workflow |
|---|---|---|
| step_success | 0 | **1** |
| 模型输出 | `SELECT [112591] [5]`（数字索引） | `SELECT [112591] [Most Reviews]`（字符串标签） |
| target_act | `SELECT [112591] [Most Reviews]` | `SELECT [112591] [Most Reviews]` |
| 失败模式 | 元素选对了，但 SELECT 的值用了数字 index 而非标签文本 | — |

**workflow 介入机制**：`search_and_sort_items` workflow 模板使用 `SELECT: {Sorting criterion}` 且示例为人类可读标签（"Lowest Price"），引导模型输出标签字符串而非数字 index。

> **注**：原文曾误将 few-shot exemplar task（"Remove SSD from cart"）作为 eval task。实际 eval task 为 bluetooth mouse 搜索任务，与 `SELECT [Most Reviews]` 语义一致。

### 9.2 负向案例（not reproduced 站点：baseline 对 → workflow 错）

#### N-1: budget / task 0 / step 0 — 域外 workflow 误导

> **Source**: `results/gpt-4o/test_task/budget/{no_workflow,offline_wf}/0.json`，step_success 索引 0。已回源核对：CONFIRMED。

**Task:** "View the Emergency Sickness Plan policy certificates for Connecticut."

| | baseline | workflow |
|---|---|---|
| step_success | **1** | 0 |
| 模型输出 | `CLICK [128]`（Reservations 按钮） | `TYPE [1326] [08817]`（在位置输入框输入邮编） |
| 失败模式 | — | workflow 是"租车搜索位置"流程，但任务是查看保险政策，完全不在 workflow 覆盖范围内 |

**误导机制**：`search_and_select_location` workflow 引导模型在 textbox 中输入位置信息，模型跟随了最近似的 workflow 步骤，跳过了正确的导航路径。

#### N-2: sixflags / task 2 / step 0 — 全域误导

> **Source**: `results/gpt-4o/test_task/sixflags/{no_workflow,offline_wf}/2.json`，step_success 索引 0。已回源核对：CONFIRMED。

**Task:** "Show the balance sheet and cash flow statement for the fiscal year 2021 of Six Flags."

| | baseline | workflow |
|---|---|---|
| step_success | **1** | 0 |
| 模型输出 | `CLICK [103]`（Investors 链接） | `CLICK [1042]`（Browse the Parks Below） |
| 失败模式 | — | 所有 5 个 sixflags workflow 都是公园/门票导航，完全不覆盖 Investors/财务报告 |

**误导机制**：`select_park` workflow 第一步就是 `[button] Browse the Parks Below -> CLICK`，页面上恰好有这个按钮。这个 case-level evidence 与“模型优先执行 workflow 模式而非局部纠偏到正确导航”这一解释相一致（见 `Appendix B4`）。

#### N-3: sixflags / task 1 / step 5 — 模板跳步

> **Source**: `results/gpt-4o/test_task/sixflags/{no_workflow,offline_wf}/1.json`，step_success 索引 5。已回源核对：CONFIRMED。

**Task:** "Buy a single day pass to Six Flags, Magic Mountain."

| | baseline | workflow |
|---|---|---|
| step_success | **1** | 0 |
| 模型输出 | `CLICK [46822]`（选择日期） | `CLICK [47084]`（Book Now 链接） |
| 失败模式 | — | workflow 模板压缩了实际 UI 步骤，模型跳过日期选择直接到 Book Now |

**误导机制**：`browse_ticket_options` workflow 只有 2 步（CLICK Tickets → CLICK 具体选项），跳过了中间的日历/日期选择步骤。模型将当前状态映射到模板的后续步骤，导致"跳步"（见 `Appendix B5`）。

### 9.3 案例总结：三种正向机制 vs 三种负向机制

| 方向 | 机制类型 | 案例 | 论文是否讨论 |
|------|---------|------|------------|
| **正向** | 防止过早终止 | P-1 | 未讨论 |
| **正向** | 策略重定向（browse→search） | P-2 | 论文提到 workflow 提供"高层指导"但未给案例 |
| **正向** | 值格式校正（index→label） | P-3 | 未讨论 |
| **负向** | 域外 workflow 误导 | N-1, N-2 | 未讨论 |
| **负向** | 模板跳步（步骤压缩） | N-3 | 未讨论 |
| **负向** | workflow 优先于推理 | N-1, N-2 | 未讨论 |

**关键发现**：正向机制的核心是 workflow 在关键决策点提供了**正确的操作模式**（搜索而非浏览、标签而非索引、继续而非终止）。负向机制的核心是 workflow 提供了**不适用的操作模式**。当前案例级证据还表明，模型的行为**与“优先遵循 workflow 而非独立推理”这一解释相一致**。这解释了 §2 中"reproduced 站点 negative=0"的现象：只要 workflow 内容匹配当前站点，它的"模式提示"就是无害的；一旦不匹配，模型对 workflow 的这种“顺从”就可能转化为误导源。

---

## 10. 站点特征与 AWM 成功预测

> 核心问题：什么站点特征决定了 AWM 是帮忙还是有害？

### 10.1 四站点结构化对比

> **数值来源**：Step SR / SKIP / CLICK 相关指标来自 `step_breakdown_output.txt`（§1 同源）；Workflow count / Avg steps 来自 `workflow/*_offline_wf.txt` 直接计数（已验证）；WF specificity / Task diversity 的定性编码见 `Appendix C4`，其结论来自 workflow 文本、case studies 与 step-level outputs 的联合阅读。

| 维度 | kayak (WORKS) | newegg (WORKS) | budget (HURTS) | sixflags (HURTS) |
|---|---|---|---|---|
| Step SR delta | **+6.3%** | **+5.7%** | **-6.1%** | **-4.7%** |
| Total steps (n) | 48 | 87 | 99 | 64 |
| SKIP % | 29% | 49% | 28% | 19% |
| CLICK % (non-SKIP) | 82% | 75% | 82% | **94%** |
| Baseline CLICK acc | 71.4% | 66.7% | 63.8% | **73.5%** |
| AWM CLICK delta | **+10.7%** | **+6.1%** | **-12.1%** | **-6.1%** |
| Workflow count | 8 | 6 | 6 | 5 |
| Avg steps/WF | **2.1** | **3.2** | **5.8** | 3.6 |
| WF specificity | 低：参数化、模块化 `[定性; Appendix C4]` | 中低：参数化电商子流程 `[定性; Appendix C4]` | 高：多功能站点特化流程 `[定性; Appendix C4]` | 中：窄而浅的 park-centric 模板 `[定性; Appendix C4]` |
| Task diversity | 中：任务多样但共享搜索语法 `[定性; Appendix C4]` | 中：任务多样但共享电商语法 `[定性; Appendix C4]` | 高：异质（跨多个站点功能区）`[定性; Appendix C4]` | 中：以 park/ticket 为主，但含 out-of-family 信息任务 `[定性; Appendix C4]` |

### 10.2 Workflow-Target 对齐率的反直觉发现

> **⚠ Exploratory metric**：对齐率由 `scripts/alignment_rate.py` 基于关键词匹配 heuristic 计算（来源：`alignment_rate_output.txt`）。匹配方法为 workflow pattern 描述文本与 observation 中 target 元素上下文的关键词重叠，不涉及语义级匹配。结果受 label-lag、关键词歧义和 placeholder fallback 的影响。

| 站点 | 对齐率 | C1 状态 | 解释 |
|------|------:|------|------|
| budget | **97.2%** | not reproduced | workflow 覆盖几乎所有 action type，但覆盖的是租车操作——test task 涉及保险、求职等域外功能 |
| sixflags | **94.2%** | not reproduced | workflow 覆盖了公园导航操作——但 test task 涉及财务报告 |
| newegg | **90.9%** | reproduced | CLICK/SELECT/TYPE 均有较高覆盖 |
| kayak | **70.6%** | reproduced | workflow 覆盖主要搜索流程，日期选择和二级 TYPE 操作未覆盖 |

**对齐率与复现状态不呈简单正相关，也不呈单调关系**：budget / sixflags 高对齐但性能差，kayak 对齐最低但性能最好；newegg（90.9%, reproduced）则是一个明确反例。

**解释**：budget 和 sixflags 的高对齐率是"虚高"——workflow 模板覆盖了大量租车/公园操作的 CLICK 关键词，但 test task 中的保险/财务类任务使用了这些关键词的*不同语义实例*。对齐率度量了 action type 的表层匹配，而非 task intent 的语义匹配。newegg 的高对齐率与正向性能并存，可能因为 newegg 的 test task 操作模式确实与 workflow 覆盖的搜索/筛选/排序流程高度一致——不仅表层关键词匹配，语义也匹配。

> **注**：这组数值应被视为 exploratory metric，用于提出"表层对齐 ≠ 语义适配"的假说，而非最终结论的定量依据。

### 10.3 AWM 成功预测假说

> **性质**：以下为基于首轮 4 站点观察提出的工作假说（working hypothesis），不是经过验证的规律。

**AWM 有效性 = f（Workflow 可复用性 × Baseline 提升空间）**

当前首轮证据支持 AWM 产生正向收益需要**两个条件同时满足**：

1. **Workflow 可复用性**：workflow 必须是短小、参数化的 sub-routine，能匹配多个 test task。`[HARD: wf_text_compare_output.txt 量化支持]`
   - kayak/newegg 的 workflow（2-3 步/WF）是模块化的"操作字典"
   - 但这里的“可复用性”在 Mind2Web 上更接近 **flat subflow reuse**，而不是显式的层级组合：`kayak` 与 `united` 的 workflow 库最像可串联的短子流程集合，`newegg` 更接近站点 utility，`budget` 则更像异质模板包（见 `Appendix C5`）
   - budget 的 workflow（5.8 步/WF）包含完整的特定任务序列，不可复用
   - sixflags 的 workflow 虽短（3.6 步/WF），但更准确地说是窄而浅的 park-centric 模板；在 eval tasks 混合且 only partial alignment 的条件下，这类 workflow family 提供的增量有限甚至可能误导 `[定性判断; Appendix C4]`

2. **Baseline CLICK 提升空间**：站点的 baseline CLICK accuracy 处于中等水平，说明模型在元素识别上有困难。`[HARD: step_breakdown_output.txt]`
   - sixflags baseline CLICK 73.5%——模型已能正确导航简单 UI，workflow 只增加噪声
   - kayak/newegg baseline CLICK 67-71%——模型需要帮助，workflow 的元素描述提供了有效线索
   - 注：67-72% 的"中等水平"是 post-hoc 从 4 个站点中观察到的 pattern，不是经过独立验证的阈值

**辅助因素**：
- **Task 异质性** `[定性; Appendix C4]`：budget 的 test task 横跨站点多个功能区（租车、保险、求职），没有单一 workflow 集合能覆盖。kayak/newegg 的 task 虽多样，但分别共享较稳定的搜索/电商交互语法；sixflags 则介于两者之间，workflow family 较窄，而 eval task 并不只限于 park/ticket 主线。
- **CLICK 占比** `[HARD: step_breakdown_output.txt]`：sixflags 非 SKIP 步骤中 94% 是 CLICK，workflow 对 CLICK 的影响高度依赖站点匹配度（§1），因此高 CLICK 占比放大了 mismatch 风险。

### 10.4 与 §9 案例的统一解释

| 站点特征 | → Workflow 效果 | → 案例支撑 |
|---------|----------------|-----------|
| 参数化 WF + 中等 baseline CLICK | 正向：策略重定向 + 值格式校正 | P-1, P-2, P-3 |
| 域外 task + 高对齐率假象 | 负向：域外误导 | N-1, N-2 |
| 模板步骤压缩 + 高 baseline | 负向：模板跳步 | N-3 |

---

## 11. 统一因果模型

> 将 §1-§10 的发现串联为一条完整的因果链。
> **证据分级**：因果图中每条箭头标注为 `[HARD]`（有脚本输出/runbook 直接支持）、`[SOFT]`（多点合理推断，无单一直接来源）、或 `[UNGROUNDED]`（缺少可追溯证据）。

### 11.1 因果图

```
[Workflow 归纳质量]
   │
   ├──→ [可复用性] ──→ ┐
   │    (短/参数化?)    │
   │                    ▼
   │              ┌─────────────┐
   │              │  Task-WF    │     [Baseline 提升空间]
   │              │  语义匹配度 │ ←── (CLICK acc 65-72%?)
   │              └─────┬───────┘
   │                    │
   │           匹配 ──→ │ ←── 不匹配
   │                    │
   │    ┌───────────────┼───────────────┐
   │    ▼               │               ▼
   │ [正向介入]         │         [负向干扰]
   │  · 策略重定向      │          · 域外误导
   │  · 值格式校正      │          · 模板跳步
   │  · 防止过早终止    │          · WF 优先于推理
   │    │               │               │
   │    ▼               ▼               ▼
   │ positive steps  ineffective    negative steps
   │ (6-18%)         (45-65%)       (4-19%)
   │    │               │               │
   │    └───────┬───────┘───────┬───────┘
   │            ▼               ▼
   │     [聚合 Step SR]   [累积效应]
   │                      · 匹配站点后半段 +13%
   │                      · 不匹配站点后半段 -11%
   └──────────────────────────────────────────→ [最终 task 成功率]
```

### 11.2 因果链叙述

1. **归纳阶段**（offline/online）产生 workflow 库。LM induction 产出更抽象的 sub-routine（§4），rule induction 产出更具体的案例库。`[HARD: wf_text_compare_output.txt, 4/4 指标]`

2. **匹配阶段**（test time）：workflow 被注入 prompt。关键变量不是 workflow 数量或对齐率，而是 **task-workflow 语义匹配度**——workflow 描述的操作模式是否适用于当前 step。`[SOFT: 从 §10.2 exploratory metric + §9 案例归纳]`

3. **影响阶段**：在少量步骤上，workflow 真正改变了模型行为（paired_case 分析中 positive+negative 占总步骤的比例因站点和 split 而异）。`[HARD: paired_case_output.txt]`
   - 匹配时：正向介入——策略重定向、值格式校正、防止过早终止 `[HARD: §9 P-1/P-2/P-3 已回源确认]`
   - 不匹配时：负向干扰——域外误导、模板跳步 `[HARD: §9 N-1/N-2/N-3 已回源确认]`；模型倾向于遵循 workflow 而非独立推理 `[SOFT: 从 N-1/N-2 模式归纳，非直接观测]`

4. **累积阶段**：正/负影响在 trajectory 中累积。匹配站点后半段在 kayak 上尤其明显（+13%），不匹配站点 budget 后半段 -10.9%。`[HARD: step_breakdown_output.txt; 但 newegg/united/sixflags 的半段效应较弱]`

5. **聚合结果**：最终 Step SR delta = Σ(positive) - Σ(negative)。reproduced 站点 negative=0 → 净正向；not reproduced 站点 negative >> positive → 净负向。`[HARD: paired_case_output.txt]`

### 11.3 论文叙事 vs 实际机制

| 论文叙事 | 实际机制 | 证据级别 |
|---------|---------|---------|
| AWM 普适有效 | AWM 有条件有效：当前首轮证据支持需要 workflow 可复用性 + baseline 提升空间（working hypothesis） | `SOFT` — 4 站点 post-hoc |
| online AWM 在大 distribution gap 下更优 | online AWM 在 cross-site 上产生负迁移（workflow 过拟合源站） | `HARD` — cross_site_diag_output + paired_case |
| workflow 提供"高层操作指导" | workflow 在少数步骤上改变模型行为，通过具体的策略重定向/值模板/终止控制起效 | `HARD` — §9 案例已回源确认 |
| LM induction 优于 rule induction | 抽象性优势依赖 task 差异程度（差异小时具体案例有竞争力；c3-runbook newegg 判定 `unclear`） | `HARD`（文本层）+ `SOFT`（性能层） |
| 高 utility rate | prompt-level utility 高，但 behavior-level adherence 远低于 100%；表层对齐率与性能不呈正相关 | `HARD`（paired_case）+ `exploratory`（alignment_rate） |

---

## 12. 分析脚本清单

为支撑上述分析，需要编写以下脚本：

| 脚本 | 用途 | 对应章节 |
|------|------|---------|
| `step_breakdown.py` | 从 JSON 日志中按 action type / step position / website 交叉统计指标 | §1 |
| `paired_case.py` | 从同一 task 的两个 condition 中提取四类配对并导出典型 case | §2 |
| `cross_site_diag.py` | C2 退化诊断：按维度分解 + workflow 适配度检查 | §3 |
| `wf_text_compare.py` | LM vs rule workflow 的文本特征提取与对比 | §4 |
| `alignment_rate.py` | Workflow-target action 关键词对齐率（exploratory） | §10 |

§9 的案例已逐条回源到原始 JSON（见各案例 Source 标注）。§10-§11 的每条主张已标注证据级别（HARD/SOFT/exploratory/定性）。

脚本位置：`doc/analysis/scripts/`

分析产物位置：`doc/analysis/`（`.txt` 输出 + `.csv` 数据 + `case_studies/` 详细案例）
