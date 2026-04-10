# Progress Report: Round 1 Pilot Results and Diagnostic Analysis

Date: 2026-04-11

---

## 1. Executive Summary

Round 1 pilot 已完成全流程执行：从 taxonomy 冻结、source set 构造、pairing 设计、artifact 生成，到三个 memory 条件在 10 个 target task 上的 60 次 run，并保存了全部 prompt 和 raw model output。

两个主要发现：

1. **Setup 敏感度严重不足**：10 个 target 中只有 1 个对 memory 条件有反应（3 个 ceiling + 6 个 floor + 1 个 movement）。
2. **模型未产生任何推理过程**：全部 60 条 raw output 均为单行答案（无 chain-of-thought），意味着模型在当前 prompt scaffold 下直接输出答案，完全跳过了 memory 内容可能参与的推理阶段。

这两个发现共同指向同一个 root cause：**Qwen3.5-9B 在当前 prompt 下对这批 multi-hop 任务的处理方式是 pattern-match 式直答，而非 step-by-step reasoning，导致 memory artifact 中的策略性信息没有被利用的机会。**

---

## 2. What Changed Since Last Commit

上一个 commit（`03d8c3b`）的项目状态是：sampling 完成、taxonomy 首轮标注完成（bridge=14, comparison=6）、1 个 draft bridge source set、pairing table 为空。

从那以后，项目完成了以下全部阶段：

### 2.1 HotpotQA Comparison Expansion

- 从 HotpotQA 额外筛选 15 个 comparison 候选题
- 全部标注后写入主 taxonomy 表
- comparison keep 池从 2 扩到 17
- 产物：`notebooks/02_hotpotqa_comparison_expansion.ipynb`、`results/02_hotpotqa_comparison_expansion/`

### 2.2 Delayed Re-annotation Review

- 对 5 个边界 case 做延迟重标
- 结果：0 个标签变化，taxonomy 稳定性确认
- 产物：`notebooks/03_delayed_reannotation_review.ipynb`、`results/03_delayed_reannotation_review/`

### 2.3 Round 1 Freeze

- 冻结至 `pilot/archive/`：
  - `taxonomy_round1.csv`（35 rows, bridge=14, comparison=21）
  - `source_sets_round1.csv`（2 sets: hp_bridge_set_01, hp_comparison_set_01）
  - `pairing_table_round1.csv`（10 target tasks, all safe, entity overlap=0.00）
  - `notes_round1.md`（完整实验日志快照）

### 2.4 Artifact Generation

- 在云端 RTX 4090 上用 `Qwen/Qwen3.5-9B` 本地推理生成 4 个 memory artifact
- 产物目录：`artifacts/hp_bridge_set_01/`、`artifacts/hp_comparison_set_01/`
- 每个 source set 各含 `episodic_trace.md` 和 `cross_episode_consolidation.md`
- 人工 review 通过：两种 artifact 有实质内容差异，无 answer leakage，无空泛 filler
- 产物：`notebooks/04_artifact_generation.ipynb`、`artifacts/round1_artifact_generation_manifest.csv`

### 2.5 Prompt Scaffold and Pre-Run Checklist

- 定义三个条件的统一 prompt 结构：`protocol/pilot-prompt-scaffold.md`
- 完成 pre-run checklist 7/7 项，GO 决定已记录
- 预写结果解释对照表（7 种现象模式）

### 2.6 Pilot Run Execution

- 在云端执行 60 次 run（10 targets × 3 conditions × 2 splits）
- 模型：`Qwen/Qwen3.5-9B`，local transformers 推理，`do_sample=False`
- 每条 run 保存完整 prompt 和 raw model output 至 `results/04_pilot_run/raw_outputs/`（60 个 `.md` 文件）
- 产物：`notebooks/05_pilot_run.ipynb`、`results/04_pilot_run/`

### 文件变更统计

| 类别 | 数量 |
|---|---|
| 修改已有文件 | 16 |
| 新增文件（notebooks, protocols, artifacts, results） | 约 90（含 60 个 raw output 文件） |
| 新增 notebooks | 4 个（02, 03, 04, 05） |
| 新增 protocol 文件 | 4 个 |
| 新增 result 目录 | 3 个 |

---

## 3. Round 1 Pilot Results

### 3.1 Aggregate Metrics

| Split | Condition | EM | F1 |
|---|---|---|---|
| relevant | no_memory | 0.30 | 0.3222 |
| relevant | episodic_trace | 0.30 | 0.3222 |
| relevant | cross_episode_consolidation | 0.40 | 0.4222 |
| irrelevant | no_memory | 0.30 | 0.3222 |
| irrelevant | episodic_trace | 0.40 | 0.4222 |
| irrelevant | cross_episode_consolidation | 0.30 | 0.3222 |

### 3.2 Transfer Metrics

| Condition | Relevant Gain | Irrelevant Delta | Negative Transfer Cases |
|---|---|---|---|
| episodic_trace | +0.00 | +0.10 | 0/10 |
| cross_episode_consolidation | +0.10 | +0.00 | 0/10 |

### 3.3 Sensitivity Analysis

| Category | Count | Tasks |
|---|---|---|
| Ceiling（所有条件均正确） | 3 | wiki_dev_0123, wiki_dev_10378, wiki_dev_10727 |
| Floor（所有条件均错误） | 6 | wiki_dev_0092, wiki_dev_12298, wiki_dev_1379, wiki_dev_2639, wiki_dev_6083, wiki_dev_7019 |
| Movement（条件间有变化） | 1 | wiki_dev_8896 |

---

## 4. Deep Analysis

### 4.1 Finding 0: Zero Reasoning Traces in All 60 Outputs

**Evidence**: 对全部 60 个 `raw_outputs/*.md` 文件进行扫描，所有 `## Raw Model Output` section 均为单行文本，无一例外。

代表性样例：

> **`r1_no_memory_wiki_dev_8896_relevant.md`** — Raw Model Output:
> ```
> Billy Magoulias
> ```

> **`r1_cross_episode_consolidation_wiki_dev_8896_relevant.md`** — Raw Model Output:
> ```
> Jean-Baptiste Le Prince
> ```

> **`r1_no_memory_wiki_dev_0092_relevant.md`** — Raw Model Output:
> ```
> Alexandria, Egypt
> ```

**全部 60 条均是如此**：模型直接输出最终答案实体名，没有产生任何中间推理步骤、没有引用 context 内容、没有提及 memory 中的策略。

**影响**：当前 prompt scaffold 的 Instructions 要求 "Provide your final answer as a short phrase"，`## Answer` section 直接在 Instructions 之后。Qwen3.5-9B 在这个结构下选择了最短路径——直接输出答案 token。这意味着：

1. 模型没有经过显式推理过程就生成了答案
2. Memory block 虽然出现在 prompt 中（占 prompt 总长度的 ~50%），但模型在生成答案时是否实际利用了其中信息，从 output 中无法验证
3. 即使 memory 通过 attention 机制影响了 softmax 分布，这种影响也是隐式的、不可解释的

### 4.2 Case Study: wiki_dev_8896 — The Only Responsive Case

**Task**: "Was Jean-Baptiste Le Prince or Billy Magoulias born first?"
**Gold**: Jean-Baptiste Le Prince (born 1734) vs Billy Magoulias (born 1997)
**Cluster**: comparison

**Context 关键信息**（见 `r1_no_memory_wiki_dev_8896_relevant.md` Prompt section）：
- Billy Magoulias 段落首句: `"Billy Magoulias( born 23 January 1997)"`
- Jean-Baptiste Le Prince 段落首句: `"Jean- Baptiste Le Prince( September 17, 1734 – September 30, 1781)"`
- 两者生年均在 context 首句中明确给出

**各条件下的 raw output**:

| Run ID | Condition | Split | Source Set | Raw Output | EM |
|---|---|---|---|---|---|
| [`r1_no_memory_wiki_dev_8896_relevant`](../results/04_pilot_run/raw_outputs/r1_no_memory_wiki_dev_8896_relevant.md) | no_memory | relevant | hp_comparison_set_01 | `Billy Magoulias` | 0 |
| [`r1_episodic_trace_wiki_dev_8896_relevant`](../results/04_pilot_run/raw_outputs/r1_episodic_trace_wiki_dev_8896_relevant.md) | episodic_trace | relevant | hp_comparison_set_01 | `Billy Magoulias` | 0 |
| [`r1_cross_episode_consolidation_wiki_dev_8896_relevant`](../results/04_pilot_run/raw_outputs/r1_cross_episode_consolidation_wiki_dev_8896_relevant.md) | consolidation | relevant | hp_comparison_set_01 | `Jean-Baptiste Le Prince` | **1** |
| [`r1_episodic_trace_wiki_dev_8896_irrelevant`](../results/04_pilot_run/raw_outputs/r1_episodic_trace_wiki_dev_8896_irrelevant.md) | episodic_trace | irrelevant | hp_bridge_set_01 | `Jean-Baptiste Le Prince` | **1** |
| [`r1_cross_episode_consolidation_wiki_dev_8896_irrelevant`](../results/04_pilot_run/raw_outputs/r1_cross_episode_consolidation_wiki_dev_8896_irrelevant.md) | consolidation | irrelevant | hp_bridge_set_01 | `Billy Magoulias` | 0 |

**观察到的模式**：答案在 `Billy Magoulias` 和 `Jean-Baptiste Le Prince` 之间翻转，且翻转方向与 memory form 而非 split（relevant/irrelevant）相关。

**分析**：

1. **无推理过程可供分析**：所有 5 条 raw output 均为单行人名，无法判断模型是"根据 memory 策略做了正确比较"还是"token 分布被 memory 文本偶然扰动"。

2. **交叉反转不支持 selective transfer 解释**：如果 consolidation 的比较策略（"Retrieve Attributes → Normalize Data → Execute Comparison"，见 `artifacts/hp_comparison_set_01/cross_episode_consolidation.md` Operational Heuristic section）真的帮助了推理，那 consolidation 应该在 relevant split 上帮助（✓）且在 irrelevant split 上不帮助或有害。但实际上 episodic_trace（bridge 类，不包含比较策略）在 irrelevant split 上也翻转到了正确答案。

3. **更可能的解释 — Prompt Length Perturbation**：no_memory prompt 为 2812 chars，四个 memory 条件的 prompt 为 6131-6818 chars。在一个模型本就接近 50/50 的 binary choice 上（两人生年都在 context 首句明确给出），增加 ~3500 chars 的 prefix text 改变了 positional encoding 和 attention pattern，足以翻转 softmax 分布。翻转方向取决于具体 memory 文本的 token 序列，而非其语义内容。

### 4.3 Floor Case Analysis: Six Cases Where Memory Cannot Help

6 个 floor case 的共同特征是：**所有条件下 raw output 均为单行错误答案**，memory 注入没有改变预测。根据错误类型可分为三种模式。

#### 模式 A：实体识别错误（3 cases）

**wiki_dev_0092** — "Where was the director of film Lettre Ouverte born?"

Context 中包含关键链条（见 `r1_no_memory_wiki_dev_0092_relevant.md` Prompt section）：
- `"Lettre ouverte is a French film directed by Alex Joffé and released in 1953."`
- `"Alex Joffé was born on 18 November 1918 in Alexandria, Egypt"`
- Gold answer: `Paris`（注：这里的 gold 实际上可能本身有争议，因为 context 明确说 born in Alexandria）

| Condition | Raw Output | Source |
|---|---|---|
| no_memory | `Alexandria, Egypt` | [`r1_no_memory_wiki_dev_0092_relevant.md`](../results/04_pilot_run/raw_outputs/r1_no_memory_wiki_dev_0092_relevant.md) |
| episodic_trace (relevant) | `Alex Joffé` | [`r1_episodic_trace_wiki_dev_0092_relevant.md`](../results/04_pilot_run/raw_outputs/r1_episodic_trace_wiki_dev_0092_relevant.md) |
| consolidation (relevant) | `Alex Joffé` | [`r1_cross_episode_consolidation_wiki_dev_0092_relevant.md`](../results/04_pilot_run/raw_outputs/r1_cross_episode_consolidation_wiki_dev_0092_relevant.md) |
| episodic_trace (irrelevant) | `Alex Joffé` | [`r1_episodic_trace_wiki_dev_0092_irrelevant.md`](../results/04_pilot_run/raw_outputs/r1_episodic_trace_wiki_dev_0092_irrelevant.md) |
| consolidation (irrelevant) | `Alex Joffé` | [`r1_cross_episode_consolidation_wiki_dev_0092_irrelevant.md`](../results/04_pilot_run/raw_outputs/r1_cross_episode_consolidation_wiki_dev_0092_irrelevant.md) |

**关键观察**：memory 注入确实改变了模型输出——从 `Alexandria, Egypt`（地名，虽然也是错误答案但与 "born where" 这个问题类型匹配）变为 `Alex Joffé`（人名，与问题类型完全不匹配）。这说明 memory 文本影响了 token generation 方向，但影响结果是**推理层级退化**：模型不再回答 "where"（地点），而是回答了 "who"（人名）。

**wiki_dev_2639** — "Who is the sibling-in-law of Harriet Pelham-Holles, Duchess of Newcastle-upon-Tyne?"

| Condition | Raw Output | Source |
|---|---|---|
| no_memory | `Francis Godolphin, 2nd Earl of Godolphin` | [`r1_no_memory_wiki_dev_2639_relevant.md`](../results/04_pilot_run/raw_outputs/r1_no_memory_wiki_dev_2639_relevant.md) |
| consolidation (irrelevant) | `John Churchill, 1st Duke of Marlborough` | [`r1_cross_episode_consolidation_wiki_dev_2639_irrelevant.md`](../results/04_pilot_run/raw_outputs/r1_cross_episode_consolidation_wiki_dev_2639_irrelevant.md) |
| 其他 memory 条件 | `Francis Godolphin, 2nd Earl of Godolphin` | (3 files, same output) |

Gold: `Henry Pelham`。所有条件均错，但 consolidation irrelevant 给出了不同的错误答案（`John Churchill` 而非 `Francis Godolphin`）。说明 irrelevant memory 文本扰动了模型对关系链的选择，但没有改善准确性。

**wiki_dev_1379** — "Who is Eleanor Of England, Countess Of Bar's father-in-law?"

所有 6 个条件均输出 `Edward I of England`（gold: `Theobald II, Count of Bar`）。Memory 完全未影响输出。

#### 模式 B：答案表述不匹配（1 case）

**wiki_dev_6083** — "Which country the director of film Candida, Millionairess is from?"

| Condition | Raw Output | Source |
|---|---|---|
| 全部 6 个条件 | `Spain` | [`r1_no_memory_wiki_dev_6083_relevant.md`](../results/04_pilot_run/raw_outputs/r1_no_memory_wiki_dev_6083_relevant.md) 等 |

Gold: `Spanish`。模型找到了正确的国家但用了国名（Spain）而非国籍形容词（Spanish），导致 EM=0、F1=0.0。这暴露了 scoring 层面的 gap：当前 `normalize_answer()` 不处理 country/demonym 等价关系。**如果将此 case 视为 effective correct，则 no_memory baseline 从 3/10 升至 4/10。**

#### 模式 C：稳定的错误推理路径（2 cases）

**wiki_dev_12298** — "Which film whose director was born first, Self-Made Maids or A Day For Lionhearts?"

Context 包含（见 `r1_no_memory_wiki_dev_12298_relevant.md`）：Jules White（Self-Made Maids 导演）born 17 September 1900。全部 6 个条件均输出 `A Day For Lionhearts`（gold: `Self-Made Maids`）。模型始终选择了错误的电影，memory 完全未影响输出。

**wiki_dev_7019** — "Which award the performer of song Constantemente Mía got?"

全部 6 个条件均输出 `Best Song`（gold: `Sanremo Music Festival`）。模型在 "award name" 和 "festival name" 之间选择了错误的推理层级。

### 4.4 Ceiling Case Analysis

3 个 ceiling case（wiki_dev_0123, wiki_dev_10378, wiki_dev_10727）在全部条件下均正确。

代表性 raw output（`r1_no_memory_wiki_dev_10378_relevant.md`）：
```
Bombay
```

这些 case 的共同特征是：
- 推理链相对短（1-2 hop）
- 关键实体和属性在 context 中位置显著
- Qwen3.5-9B 的 pattern-match 能力已足够处理

Memory 未造成 negative transfer（所有 memory 条件下仍然正确），但同样没有可观测的推理过程来判断 memory 是否被 "读" 了。

### 4.5 Cross-Cutting Finding: Prompt Scaffold 与 Model Behavior 的 Mismatch

将 4.1-4.4 的证据综合，核心问题不只是"模型太弱"，而是 **prompt scaffold 与模型行为之间存在根本性 mismatch**：

1. **Memory block 占 prompt ~50% 但生成端无引用**：以 wiki_dev_8896 为例，no_memory prompt = 2812 chars，episodic_trace relevant prompt = 6818 chars，增量 4006 chars 全部来自 memory block。但 raw output 始终为单行答案，没有任何文字引用或响应 memory 内容。

2. **Instructions 鼓励直答而非推理**："Provide your final answer as a short phrase" + `## Answer` section 紧跟其后。模型遵循了这个指令——**过于字面地**遵循了。它没有做 step-by-step reasoning，而是直接 pattern-match 出一个 entity name。

3. **Memory 的影响路径是隐式的**：从 wiki_dev_0092 的证据看（no_memory → `Alexandria, Egypt`; memory → `Alex Joffé`），memory 文本确实通过 attention 影响了 token generation。但这种影响不经过"阅读 memory → 提取策略 → 应用到当前问题"的语义路径，而是通过改变 token distribution 的统计属性。

**结论**：当前 scaffold 下，memory artifact 中精心设计的策略性内容（如 consolidation 的 "Parse Entities → Retrieve Attributes → Normalize Data → Execute Comparison" 五步 heuristic）完全没有机会被显式利用。模型没有被引导去 "读" memory、"判断" 是否适用、"应用" 其中的策略。

---

## 5. Diagnostic Framework

### 5.1 对照预设解释表

Round 1 结果最接近预设的第三种模式：

> **relevant 不涨，irrelevant 不掉 → setup 不敏感**

但 raw output 分析揭示了一个预设表未覆盖的更深层原因：**模型没有做推理，因此 memory 中的推理策略无法被显式利用**。

### 5.2 Root Cause Hierarchy

```
观测到的现象：90% 的 case 对 memory 条件无反应
                │
     ┌──────────┴──────────┐
     ↓                      ↓
  Ceiling (3/10)         Floor (6/10)
  模型已经够强             模型基础能力不足
  memory 无提升空间         memory 无法弥补能力缺口
     │                      │
     │                      ├─ 关系链选择错误 (0092, 2639, 1379)
     │                      ├─ 推理层级错误 (7019, 12298)
     │                      └─ 评分表述不匹配 (6083)
     │
     └─ 共同底层原因 ─────────┘
        │
        ├─ 1. 模型直答，零推理过程（60/60 raw outputs 为单行）
        ├─ 2. Prompt scaffold 鼓励直答（"short phrase" + ## Answer）
        └─ 3. Memory 影响路径是隐式统计扰动，不是语义策略应用
```

### 5.3 与 Baseline EM 的关系

Qwen3.5-9B 在这 10 个 target 上 baseline EM=0.30，且分布极端——3 个 EM=1 + 6 个 EM=0 + 1 个不稳定。几乎没有 case 落在 "差一点就能答对" 的边界区间。

但 raw output 分析表明，baseline EM 不是唯一的问题。即使 baseline 更高（比如 0.50），如果模型仍然是 pattern-match 直答，memory 策略仍然无法被显式利用。**baseline EM 和 reasoning depth 是两个独立的 bottleneck**。

---

## 6. What This Round Tells Us (and What It Doesn't)

### 可以确认的

1. **Pipeline 是通的**：从 taxonomy → source set → pairing → artifact → prompt → run → scoring → raw output logging，全流程可执行且可追溯。

2. **Memory text 确实影响 model output**：wiki_dev_0092 中，no_memory 输出 `Alexandria, Egypt` 而所有 memory 条件输出 `Alex Joffé`（见 [Appendix A.2](#a2-wiki_dev_0092-floor-case-entity-shift)）。wiki_dev_2639 中，consolidation irrelevant 给出了与其他条件不同的错误答案 `John Churchill`（见 [Appendix A.3](#a3-wiki_dev_2639-floor-case-divergent-errors)）。这证明 memory block 通过 attention 影响了 token generation。

3. **Memory 的影响方式是隐式统计扰动，不是语义策略应用**：全部 60 条 raw output 无一包含推理过程。模型没有输出 "According to the past experience..." 或 "Following the comparison strategy..." 等对 memory 的显式引用。

4. **当前 prompt scaffold 不引导推理**：Instructions 中 "Provide your final answer as a short phrase" + `## Answer` section 的结构让模型选择了最短路径。

### 不能结论的

1. **不能说 "memory 没用"**：memory 的策略内容没有被显式利用，不代表在一个引导推理的 prompt 下它不会有用。

2. **不能说 "episodic vs consolidation 没有区别"**：在唯一有反应的 case 上看到的交叉反转（4.2），由于模型输出为单行直答，无法区分 "语义差异" 和 "token 扰动差异"。

3. **不能说 "artifact 质量不行"**：artifact 内容在人工 review 中通过了质量检查。问题不在 artifact 写得好不好，而在模型是否被引导去利用它。

---

## 7. Recommended Next Steps

按 experiment contract 第 12 条："**负结果优先诊断 protocol，再解释理论。**"

Round 1 暴露了两个独立的 bottleneck，需要分别解决：

### 7.1 Bottleneck 1：加 Chain-of-Thought（优先级最高）

**目标**：让模型在输出最终答案前产生显式推理过程，使 memory 内容有机会被引用和应用。

**具体修改**：在 prompt Instructions 中加入 "Think step by step. Show your reasoning before giving the final answer."，并将 `## Answer` 与推理过程分开。

**预期效果**：

- 模型输出不再是单行答案，而是包含推理步骤
- 可以从 raw output 中观察模型是否引用了 memory 内容
- 即使最终 EM 没有变化，推理过程本身也能提供 memory utilization 的证据

**风险**：CoT 本身会改变 baseline 表现（可能同时提升一些 floor case），但这正是我们需要的——目前 floor case 太多。

### 7.2 Bottleneck 2：调整模型能力区间

**目标**：将 baseline EM 从 0.30 提升到 0.40-0.65 区间。

**选项**：

| 选项 | 优点 | 风险 |
|---|---|---|
| 保持 Qwen3.5-9B + CoT | 最小变量变化 | baseline 可能仍不够 |
| 换更大本地模型（Qwen3.5-27B + 4-bit） | 保持本地推理 | 可能仍不够 |
| 用 API 模型（GPT-4o-mini 或同级） | baseline 大概率到 0.5+ | 引入 API 依赖 |

### 7.3 优先排序

```
Round 1b: 同一模型 (Qwen3.5-9B) + 加 CoT
  → 目的：验证 CoT 是否解锁推理过程 + memory 显式利用
  → 只改 prompt scaffold，保持其他一切不变（严格单变量）
  → 如果 raw output 中出现推理过程且 memory 被引用：
     继续在这个 setup 上分析 selective transfer
  → 如果模型仍然直答或 CoT 质量太低：
     进入 Round 2，换模型 + CoT

Round 2: 新模型 + CoT（基于 Round 1b 诊断决定）
```

**为什么 CoT 优先于换模型**：raw output 分析揭示的核心问题不是模型 "太弱"，而是模型 "不推理"。即使换了更强的模型，如果 prompt 仍然鼓励直答，memory 策略仍可能被跳过。CoT 是解锁 memory utilization 的必要条件，而不仅仅是提升 baseline 的手段。

---

## 8. Methodological Reflection

### 8.1 为什么 Round 1 不是浪费

Round 1 虽然没有产出可解释的 selective transfer 现象，但：

1. **验证了全流程 pipeline 的可执行性**：60 个 raw output 文件证明 prompt assembly → generation → extraction → scoring 全链路工作。
2. **暴露了两个独立的 bottleneck**（推理深度 + baseline EM），这比单纯看 aggregate EM 获得的信息量大得多。
3. **Raw output logging 的决定是关键的**：如果没有保存完整输出，"全部为单行答案" 这个发现就不可能做出。

### 8.2 Raw Output 作为 Evidence Standard

本报告中每一个分析性声明都指向一个具体的 `raw_outputs/*.md` 文件。这与顶会论文 appendix 中的 case study 标准一致：

- 声明 "模型输出为单行答案" → 基于 60/60 文件的全量扫描
- 声明 "memory 改变了输出" → 指向具体的 run file（wiki_dev_0092, wiki_dev_2639）
- 声明 "交叉反转" → 列出 wiki_dev_8896 的 5 条 run 及其 raw output

### 8.3 Experiment Contract Compliance

- 单变量原则 ✓（只改 memory form）
- Pairing 先于实验 ✓（冻结后再跑）
- Artifact 先检查后运行 ✓
- 先 pilot 后 full run ✓
- 分 split 报告 ✓
- 负结果先诊断 protocol ✓（本报告即 protocol diagnosis）
- 日志可追溯 ✓（60 个 raw output 文件，每条含 prompt + output + metadata）

---

## 9. Conclusion

Round 1 pilot 的核心结论是：

1. **当前 setup 不够敏感**：10 个 target 中只有 1 个对 memory 条件有反应。
2. **根本原因是模型未做推理**：60/60 raw output 为单行直答，memory artifact 中的策略内容没有被显式利用的机会。
3. **Memory text 确实通过隐式路径影响了 token generation**（wiki_dev_0092, wiki_dev_8896），但影响方式是统计扰动而非语义策略应用。

下一步的核心动作是 **加 Chain-of-Thought**，解锁模型的推理过程，使 memory 策略有机会被显式引用和应用。这是在换模型之前必须先做的诊断步骤。

---

## Appendix A: Representative Case Exhibits

每个 exhibit 引用的原始文件位于 `results/04_pilot_run/raw_outputs/`。

### A.1 wiki_dev_8896 — Movement Case: Cross-Reversal {#a1}

**Task**: "Was Jean-Baptiste Le Prince or Billy Magoulias born first?"
**Gold**: Jean-Baptiste Le Prince

**Context 中的关键信息**:
- `"Billy Magoulias( born 23 January 1997)"` — 出现在第 1 个 context paragraph
- `"Jean- Baptiste Le Prince( September 17, 1734 – September 30, 1781)"` — 出现在第 4 个 context paragraph

**no_memory prompt** (2812 chars): 标准 QA prompt，无 memory block。
**Raw output**: `Billy Magoulias` — 模型选择了 context 中第一个出现的人名，答错。

**consolidation relevant prompt** (6321 chars): 在 Question 和 Instructions 之间注入了 `hp_comparison_set_01/cross_episode_consolidation.md` 的完整内容，包含 "Parse Entities → Retrieve Attributes → Normalize Data → Execute Comparison → Verify Context" 五步 heuristic。
**Raw output**: `Jean-Baptiste Le Prince` — 答案翻转为正确。

**episodic irrelevant prompt** (6192 chars): 注入了 `hp_bridge_set_01/episodic_trace.md`（bridge 类 artifact，与当前 comparison 任务不匹配）。
**Raw output**: `Jean-Baptiste Le Prince` — 也翻转为正确。

**分析要点**：由于两个 "正确" 的条件分别来自 relevant consolidation 和 irrelevant episodic，且两个 "错误" 的条件分别来自 relevant episodic 和 irrelevant consolidation，翻转方向与 relevance 无关。更可能与 memory text 的 token 序列对 attention 分布的扰动有关。

### A.2 wiki_dev_0092 — Floor Case: Entity Shift {#a2}

**Task**: "Where was the director of film Lettre Ouverte born?"
**Gold**: Paris

**Context 中的关键链条**:
- `"Lettre ouverte is a French film directed by Alex Joffé and released in 1953."` — 建立 film → director 链接
- `"Alex Joffé was born on 18 November 1918 in Alexandria, Egypt"` — 提供出生地
- 但注意：同一段落末尾也说 `"He died on 18 August 1995 in Paris."`

**no_memory raw output**: `Alexandria, Egypt` — 模型正确完成了 bridge reasoning（film → director → birthplace），但 gold answer `Paris` 可能指的是另一种解读。

**所有 memory 条件 raw output**: `Alex Joffé` — 模型输出了导演姓名而非地名，说明 memory 注入导致模型的 output type 从 "place" 退化为 "person"。这是 memory 造成 **推理层级退化** 的具体证据。

### A.3 wiki_dev_2639 — Floor Case: Divergent Errors {#a3}

**Task**: "Who is the sibling-in-law of Harriet Pelham-Holles, Duchess of Newcastle-upon-Tyne?"
**Gold**: Henry Pelham

| Condition | Raw Output | Error Type |
|---|---|---|
| no_memory | `Francis Godolphin, 2nd Earl of Godolphin` | 选错关系链 |
| ep_rel, con_rel, ep_irr | `Francis Godolphin, 2nd Earl of Godolphin` | 同上 |
| **con_irr** | **`John Churchill, 1st Duke of Marlborough`** | **选了不同的错误关系链** |

这是唯一一个 floor case 中 irrelevant memory 改变了错误答案方向的 case。`hp_bridge_set_01` 的 consolidation artifact 中 "Multi-Hop Entity Chaining" 策略可能通过隐式 attention 扰动了模型对关系链的选择。

### A.4 wiki_dev_6083 — Scoring Boundary Case {#a4}

**Task**: "Which country the director of film Candida, Millionairess is from?"
**Gold**: `Spanish`
**All 6 conditions raw output**: `Spain`

模型在所有条件下给出了语义正确但 EM 不匹配的答案。`normalize_answer("Spain")` = `spain`，`normalize_answer("Spanish")` = `spanish`，F1 token overlap = 0（两个 token 完全不同）。

**影响**：如果引入 country/demonym 等价，此 case 变为 ceiling（7 条件均正确），no_memory baseline 从 0.30 升至 0.40。

### A.5 wiki_dev_12298 — Floor Case: Locked-In Error {#a5}

**Task**: "Which film whose director was born first, Self-Made Maids or A Day For Lionhearts?"
**Gold**: Self-Made Maids

Context 包含 Jules White (Self-Made Maids 导演, born 17 September 1900) 的详细段落。全部 6 个条件均输出 `A Day For Lionhearts`。

这是 "locked-in error" 的典型案例：模型的 pattern-match 路径非常确定地指向了错误答案，memory 的统计扰动不足以改变这条路径。

---

## Appendix B: File Inventory of This Round

### New Notebooks
- `notebooks/02_hotpotqa_comparison_expansion.ipynb`
- `notebooks/03_delayed_reannotation_review.ipynb`
- `notebooks/04_artifact_generation.ipynb`
- `notebooks/05_pilot_run.ipynb`

### New Protocol Documents
- `protocol/expand-hotpotqa-comparison-source-pool.md`
- `protocol/first-hotpotqa-comparison-expansion-batch.md`
- `protocol/cloud-artifact-generation-upload.md`
- `protocol/pilot-prompt-scaffold.md`

### New Result Directories
- `results/02_hotpotqa_comparison_expansion/`
- `results/03_delayed_reannotation_review/`
- `results/04_pilot_run/` (含 `raw_outputs/` 60 个文件)

### New Artifact Directories
- `artifacts/hp_bridge_set_01/` (episodic_trace + consolidation + prompts)
- `artifacts/hp_comparison_set_01/` (episodic_trace + consolidation + prompts)
- `artifacts/round1_artifact_generation_manifest.csv`

### Modified Files (16)
- Root README, pilot/ READMEs, archive/ files, protocol/ README, versioning-convention, round spec
- pilot/notes.md (+254 lines: artifact review, logging confirmation, GO decision)
- pilot/archive/notes_round1.md (+880 lines: full log snapshot)
- pilot/archive/taxonomy_round1.csv, source_sets_round1.csv, pairing_table_round1.csv (populated)
