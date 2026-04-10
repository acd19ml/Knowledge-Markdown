# Progress Report: Round 1b Prompt Diagnosis Results

Date: 2026-04-11

---

## 1. Executive Summary

Round 1b 已完成预定的 `smoke subset` 诊断运行：在 6 个 target task 上，对 `no_memory`、`episodic_trace`、`cross_episode_consolidation` 三个条件分别在 `relevant / irrelevant` 两个 split 上执行，共 36 次 run，并保存了全部 structured prompt 与 raw model output。

Round 1b 的目标不是直接重复 Round 1 的平均分比较，而是验证新的 prompt scaffold 是否真正迫使模型显式产生推理过程，并观察 memory 是被使用、被拒绝，还是继续被静默忽略。

三个最重要的结论：

1. **Prompt diagnosis 成功**：36/36 runs 均产生了 `## Reasoning` 与 `## Final Answer`，`parse_success = 36/36`。这说明 Round 1 的核心问题确实在 prompt scaffold，而不是 artifact 无法被读入。
2. **Process-level evidence 已出现，但 outcome-level gain 仍不稳定**：memory runs 中已出现显式 `use` 与显式 `reject`，但整体上 relevant memory 并未稳定优于 `no_memory`，甚至 `cross_episode_consolidation` 在 irrelevant split 上表现最好。
3. **当前最可信的解释不是 “memory 无效”，而是 “memory effects 仍被 benchmark 边界、case heterogeneity 与 answer-format effects 强烈干扰”**。Round 1b 已经把问题推进到可解释层，但还不足以支持更大的 memory efficacy 结论。

---

## 2. What Changed Since Round 1

相对于 [progress-report-round1-pilot.md](./progress-report-round1-pilot.md)，Round 1b 只改了一个核心变量：**prompt scaffold**。

### 2.1 Pre-run Audit and Smoke Subset Construction

- 完成 Round 1 target audit：
  - [round1_target_audit.md](../results/05_round1b_prep/round1_target_audit.md)
  - [round1_target_audit.csv](../results/05_round1b_prep/round1_target_audit.csv)
- 固定 6 个 smoke target：
  - [round1b_smoke_subset.csv](../results/05_round1b_prep/round1b_smoke_subset.csv)
- 这 6 个 target 覆盖：
  - 唯一 movement case：`wiki_dev_8896`
  - benchmark ambiguity case：`wiki_dev_0092`
  - scoring boundary case：`wiki_dev_6083`
  - memory-sensitive failure candidates：`wiki_dev_2639`, `wiki_dev_7019`
  - 一个干净 comparison ceiling：`wiki_dev_10727`

### 2.2 Prompt Scaffold Revision

- 新 scaffold 定义于：
  - [pilot-prompt-scaffold-round1b.md](../protocol/pilot-prompt-scaffold-round1b.md)
- 从 Round 1 的单段 `## Answer` 输出，改为强制：
  - `## Reasoning`
  - `## Final Answer`
- 解析器也同步改为只从 `## Final Answer` 提取答案。

### 2.3 Round 1b Execution

- Notebook：
  - [06_round1b_prompt_diagnosis.ipynb](../notebooks/06_round1b_prompt_diagnosis.ipynb)
- 结果目录：
  - [results/05_round1b_run](../results/05_round1b_run)
- 输出文件：
  - [round1b_smoke_results.csv](../results/05_round1b_run/round1b_smoke_results.csv)
  - [round1b_smoke_results_detail.csv](../results/05_round1b_run/round1b_smoke_results_detail.csv)
  - [raw_outputs/](../results/05_round1b_run/raw_outputs)

Round 1b 继续使用：
- model: `Qwen/Qwen3.5-9B`
- backend: local `transformers`
- `RUN_GENERATION = True`
- `USE_API = False`
- `MAX_NEW_TOKENS = 1600`

---

## 3. Round 1b Results

### 3.1 Aggregate Metrics

| Split | Condition | EM | F1 |
|---|---|---|---|
| relevant | no_memory | 0.50 | 0.5833 |
| relevant | episodic_trace | 0.3333 | 0.3333 |
| relevant | cross_episode_consolidation | 0.3333 | 0.4237 |
| irrelevant | no_memory | 0.50 | 0.5833 |
| irrelevant | episodic_trace | 0.3333 | 0.3333 |
| irrelevant | cross_episode_consolidation | 0.6667 | 0.6667 |

### 3.2 Process Metrics

| Metric | Value |
|---|---|
| total runs | 36 |
| `failure_status = ok` | 36/36 |
| `reasoning_present = 1` | 36/36 |
| `final_answer_present = 1` | 36/36 |
| `parse_success = 1` | 36/36 |
| explicit memory use | 3/24 memory runs |
| explicit memory reject | 2/24 memory runs |

### 3.3 Immediate Interpretation

Round 1b 和 Round 1 的根本区别，不在于分数更高，而在于：

- Round 1：模型几乎全部是单行直答，无法判断 memory 是否被读到
- Round 1b：模型稳定地产生了显式推理文本，因此现在可以真正分析：
  - memory 是否被提及
  - memory 是否被拒绝
  - memory 是否改变了 reasoning path

这意味着 Round 1b 首先是一次 **measurement repair**，其次才是一次 memory 对比实验。

---

## 4. Deep Analysis

### 4.1 Finding 1: Structured Reasoning Was Successfully Elicited

Round 1b 最清楚的成功，是新的 scaffold 真的改变了模型输出形态。

代表性样例：

- [r1b_episodic_trace_wiki_dev_8896_relevant.md](../results/05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_8896_relevant.md)
- [r1b_episodic_trace_wiki_dev_8896_irrelevant.md](../results/05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_8896_irrelevant.md)

这两条 run 都清楚地给出了：

- 多步 `## Reasoning`
- 单独的 `## Final Answer`

而且 irrelevant episodic case 明确写出了 rejection：

> the provided past experience regarding multi-hop entity resolution is not useful here

这与 Round 1 的单行答案行为形成了直接对比。  
因此，Round 1b 已经验证了一个重要判断：

**如果 scaffold 强制模型先写 reasoning，再写 final answer，那么 memory interaction 就至少可以被显式观察，而不再只是隐式 token 扰动。**

### 4.2 Finding 2: Selective Transfer Signal Still Does Not Hold

虽然 process-level visibility 提高了，但 outcome-level 模式并没有按最初假设收敛到：

- relevant memory 更好
- irrelevant memory 更差或被拒绝

相反，当前 aggregate 呈现的是：

- `no_memory` 在两个 split 上都维持 `EM = 0.50`
- `episodic_trace` 在两个 split 上都下降到 `0.3333`
- `cross_episode_consolidation` 在 irrelevant split 上反而达到最好结果 `0.6667`

这说明：

1. memory 的引入已经能进入生成过程  
2. 但它并没有形成稳定的 “relevant helps / irrelevant hurts” 结构  
3. 当前 smoke subset 更像是在暴露 **case-level interaction**，而不是在支持一个清晰的 split-level transfer law

### 4.3 Case Study A: `wiki_dev_8896` Shows Process-Level Selectivity Without Outcome Gain

Task:
- `wiki_dev_8896`
- question: “Was Jean-Baptiste Le Prince or Billy Magoulias born first?”
- gold: `Jean-Baptiste Le Prince`

这个 case 在所有 6 个条件下都答对，但 memory interaction 方式不同：

| Condition | Split | EM | Memory Reference |
|---|---|---|---|
| no_memory | relevant / irrelevant | 1 | implicit_or_none |
| episodic_trace | relevant | 1 | explicit_use |
| episodic_trace | irrelevant | 1 | explicit_reject |
| consolidation | relevant / irrelevant | 1 | implicit_or_none |

这说明：

- 这不是一个能证明 “memory improves accuracy” 的 case
- 但它是一个很强的 **process-level sanity check**

同一个 target 上，模型已经能区分：

- comparison-like episodic trace 可以被引用
- bridge-like episodic trace 应该被拒绝

所以至少在这一个 clean case 上，Round 1b 已经观察到了你最想测的东西：

**memory 不是一律被套用，而是开始出现 “该用时用，不该用时拒绝” 的显式行为。**

### 4.4 Case Study B: `wiki_dev_2639` Reveals Memory-Induced Degradation

Task:
- `wiki_dev_2639`
- gold: `Henry Pelham`

结果如下：

| Condition | Split | Pred | EM |
|---|---|---|---|
| no_memory | relevant | `Henry Pelham` | 1 |
| no_memory | irrelevant | `Henry Pelham` | 1 |
| episodic_trace | relevant | `Cannot be determined...` | 0 |
| episodic_trace | irrelevant | `Cannot be determined...` | 0 |
| consolidation | relevant | `Cannot be determined...` | 0 |
| consolidation | irrelevant | `Henry Pelham` | 1 |

对应文件：

- [r1b_no_memory_wiki_dev_2639_relevant.md](../results/05_round1b_run/raw_outputs/r1b_no_memory_wiki_dev_2639_relevant.md)
- [r1b_episodic_trace_wiki_dev_2639_relevant.md](../results/05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_2639_relevant.md)
- [r1b_cross_episode_consolidation_wiki_dev_2639_relevant.md](../results/05_round1b_run/raw_outputs/r1b_cross_episode_consolidation_wiki_dev_2639_relevant.md)
- [r1b_cross_episode_consolidation_wiki_dev_2639_irrelevant.md](../results/05_round1b_run/raw_outputs/r1b_cross_episode_consolidation_wiki_dev_2639_irrelevant.md)

这个 case 的意义很大，因为它表明：

- memory 不只是“没帮忙”
- memory 确实可能把一个原本正确的 baseline 拉坏

而且更反直觉的是：

- relevant memory 拉坏了
- irrelevant consolidation 却回到了 baseline 正确答案

这对当前研究问题是重要信号：  
它说明目前还不能把 `relevant / irrelevant` 当作直接可解释的因果轴，因为 **artifact wording、task form、model preference** 仍然可能比 split 标签更强。

### 4.5 Case Study C: `wiki_dev_7019` Shows Output Compression Rather Than Clear Strategy Reuse

Task:
- `wiki_dev_7019`
- gold: `Sanremo Music Festival`

结果如下：

| Condition | Split | Pred | EM |
|---|---|---|---|
| no_memory | relevant / irrelevant | overly long answer | 0 |
| episodic_trace | relevant / irrelevant | still wrong | 0 |
| consolidation | relevant | still wrong | 0 |
| consolidation | irrelevant | `Sanremo Music Festival` | 1 |

对应文件：

- [r1b_no_memory_wiki_dev_7019_relevant.md](../results/05_round1b_run/raw_outputs/r1b_no_memory_wiki_dev_7019_relevant.md)
- [r1b_cross_episode_consolidation_wiki_dev_7019_irrelevant.md](../results/05_round1b_run/raw_outputs/r1b_cross_episode_consolidation_wiki_dev_7019_irrelevant.md)

这个 improvement 更像是：

- 模型在 consolidation 条件下把答案压缩到了更短、更接近 gold 的表述

而不是：

- 明确执行了某种可解释的 relevant transfer strategy

所以它是一个真实 improvement，但仍然更接近 **answer-format correction**，而不是理论上更强的 selective transfer 证据。

### 4.6 Case Study D: `wiki_dev_0092` Still Functions as an Audit Case, Not a Memory Case

Task:
- `wiki_dev_0092`
- gold: `Paris`
- model prediction across all 6 conditions: `Alexandria, Egypt`

对应文件：

- [r1b_cross_episode_consolidation_wiki_dev_0092_irrelevant.md](../results/05_round1b_run/raw_outputs/r1b_cross_episode_consolidation_wiki_dev_0092_irrelevant.md)

这条仍然不适合被拿来判断 memory 成败。原因和 Round 1 一样：

- context 明确写的是 Alex Joffé “was born ... in Alexandria, Egypt”
- gold 却是 `Paris`

Round 1b 在这里的价值不是纠正答案，而是显示模型已经能显式写出：

- memory 被拒绝
- 但最终仍沿着 context strongest evidence 做出 `Alexandria, Egypt`

所以 `wiki_dev_0092` 继续应当被视为 **audit / ambiguity case**，而不是 transfer signal。

### 4.7 Scoring Boundary Still Exists: `wiki_dev_6083`

`wiki_dev_6083` 在所有 6 个条件下继续输出 `Spain`，gold 为 `Spanish`。

这说明：

- Round 1b 修好了 reasoning visibility
- 但没有修掉 scoring 层面的 normalization gap

所以 `Spain` vs `Spanish` 仍然是后续 aggregate 解读中的噪声源。

### 4.8 Pairing / Artifact Audit Summary

在 [round1b_pairing_artifact_audit.md](../results/05_round1b_prep/round1b_pairing_artifact_audit.md) 和 [round1b_case_role_reclassification.md](../results/05_round1b_prep/round1b_case_role_reclassification.md) 中，我们对 6 个 smoke cases 做了逐条审计，并把它们重新压成下一轮可执行的 `case role`。高层结论已经比较清楚：

1. **当前最干净的正信号是 process-level selectivity，而不是 outcome gain**
   - `wiki_dev_8896` 是目前最可信的 sanity check：
     - relevant episodic 被显式使用
     - irrelevant episodic 被显式拒绝
     - 但因为 baseline 本来就正确，它不能证明 memory 带来了 accuracy gain

2. **当前最强的负信号更像 artifact-induced derailment，而不是 split 标签失效**
   - `wiki_dev_2639` 显示 relevant bridge artifact 会把原本正确的 baseline 拉成 `Cannot be determined`
   - 这更像 `bridge` cluster 过粗，artifact 对 relation-chain case 施加了错误 procedural bias

3. **某些 improvement 更像 output-layer correction，而不是 strategy transfer**
   - `wiki_dev_7019` 中，irrelevant consolidation 的收益主要体现在把过长答案压缩成更贴近 gold 的表达
   - 这更接近 answer granularity correction，而不是 comparison strategy 真正迁移到了 bridge task

4. **至少有两条 case 应从 transfer evidence 中降级**
   - `wiki_dev_0092`：benchmark ambiguity case
   - `wiki_dev_6083`：scoring-boundary case
   - 这两条都不应再被用于支持或反驳 memory effect

5. **还存在低信息量 ceiling case，需要谨慎解读**
   - `wiki_dev_10727` 在所有条件下都正确
   - 即使出现 irrelevant episodic 的 `explicit_use`，也没有 outcome change
   - 它更适合用来区分 “verbalized memory use” 和 “memory actually changes reasoning or answer”

因此，pairing / artifact audit 的整体结论不是：

- current pairing 完全不成立

而是：

- 当前 smoke subset 里同时混有
  - clean process-level cases
  - artifact-sensitive cases
  - scoring / benchmark boundary cases
  - low-information ceiling cases

这进一步支持一个更谨慎的判断：

**Round 1b 已经证明 measurement 与 case analysis 现在可行，但当前结果还不足以直接上升为稳定的 selective-transfer 结论。**

---

## 5. Diagnostic Conclusion

Round 1b 的真正贡献，不是证明了某种 memory 已经有效，而是把项目从：

- “模型有没有可能在隐式地被 memory 扰动”

推进到了：

- “模型何时显式使用 memory、何时显式拒绝 memory、以及 memory 何时会把 baseline 拉坏”

更具体地说，Round 1b 已经回答了三个问题：

1. **Round 1 的单行直答问题是 prompt scaffold 导致的吗？**  
   是。Round 1b 已经稳定 elicited reasoning traces。

2. **memory interaction 现在能被观测了吗？**  
   能。至少已经看到 explicit use / explicit reject。

3. **当前 smoke subset 是否已经支持 strong selective-transfer claim？**  
   还不支持。当前 signal 仍然过于 case-dependent，而且会被 benchmark ambiguity 和 scoring boundary 干扰。

因此，Round 1b 的更准确定位是：

**一次成功的 prompt/measurement repair，而不是一次已经完成的 memory efficacy validation。**

---

## 6. Next Step

基于这轮结果，下一步不建议直接扩大到 full rerun。更合理的顺序是：

1. **先修 scoring / audit 边界**
   - `wiki_dev_0092`：继续标记为 ambiguity / exclude-from-aggregate
   - `wiki_dev_6083`：考虑加入 `country/demonym` normalization 或单独作为 boundary case

2. **再收一轮更明确的 process metric**
   - 当前 `memory_reference_type` 还是过粗
   - 后面可以增加：
     - whether reasoning quotes memory pattern
     - whether memory changes answer type
     - whether memory shortens overlong answers

3. **把已完成的 pairing / artifact audit 转成下一轮筛选规则**
   - 当前 audit 已经表明：
     - `wiki_dev_0092` 应固定为 ambiguity / audit case
     - `wiki_dev_6083` 应固定为 scoring-boundary case
     - `wiki_dev_2639` 提示 `bridge` cluster 需要更细的子型判断
     - `wiki_dev_7019` 提示需要区分 reasoning improvement 与 answer-format correction
   - 对应执行文件：
     - [round1b_case_role_reclassification.csv](../results/05_round1b_prep/round1b_case_role_reclassification.csv)
     - [round1b_case_role_reclassification.md](../results/05_round1b_prep/round1b_case_role_reclassification.md)
   - 因此下一轮不该原样复用所有 smoke cases，而应先做 case role reclassification

4. **只有在 scoring、process、pairing 这三层都更稳后，再考虑 full rerun**
   - 否则 full rerun 只会把当前 case-level ambiguity 放大到更大表格里

一句话总结下一步：

**Round 1b 已经把“能不能看到 reasoning/memory interaction”这个门槛跨过去了；现在该先基于已完成的 audit 收紧 scoring、process analysis 和 case selection，再决定是否进入更大的 rerun。**
