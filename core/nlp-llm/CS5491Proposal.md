# CS5491 AI Project Proposal
# CS5491 人工智能项目提案

## PROPOSAL: THOUGHTS-AUGMENTED FUNSEARCH FOR ONLINE BIN PACKING HEURISTIC DESIGN
## 提案：面向在线装箱启发式设计的思维增强型 FunSearch

---

## 1 Problem Selection and Rationale
## 1 问题选择与动机

We choose **Topic 2a: Thoughts-augmented FunSearch for the Online Bin Packing Problem**. In this task, items arrive sequentially and must be immediately assigned to bins of fixed capacity to minimize total usage.

我们选择 **课题 2a：面向在线装箱问题的思维增强型 FunSearch**。在该任务中，物品依次到达，需立即分配到固定容量的箱子中，目标是最小化使用的箱子总数。

> **注释：** 在线装箱问题（Online Bin Packing）是经典的组合优化问题。"在线"指物品逐个到来、无法预知未来，必须即时做决策，无法回溯——这比离线版本难得多，也更贴近现实场景（如服务器资源分配、货物装载等）。

**Rationale:** Traditional FunSearch evolves raw code, which often lacks high-level strategic reasoning. We propose adding natural language "thoughts" before code generation to activate the LLM's Chain-of-Thought (CoT) capabilities. This allows the model to conceptualize complex strategies (e.g., adaptive capacity management) before implementation, leading to more robust heuristics and faster convergence than raw code mutation.

**动机：** 传统 FunSearch 直接进化原始代码，往往缺乏高层次的策略推理。我们提议在代码生成前加入自然语言"思维"，以激活 LLM 的链式思维（CoT）能力。这使模型能在实现前先构建复杂策略（例如自适应容量管理），从而得到比单纯代码变异更稳健的启发式算法，并实现更快的收敛。

> **注释：** FunSearch（Romera-Paredes et al., 2024）是 DeepMind 提出的方法，用 LLM 作为"变异算子"在程序空间中进行进化搜索。其核心缺陷在于 LLM 只看到代码片段，没有显式推理过程。本提案的创新点是在代码前插入自然语言"Thought"，相当于让 LLM 先"想清楚再动手"，是 CoT Prompting 与进化计算的结合。

---

## 2 Tentative Plan
## 2 初步方案

We will implement an enhanced evolutionary loop based on the project template:

我们将在项目模板的基础上实现一个增强型进化循环：

- **Thought-Augmented Mutation:** The LLM will be prompted to first generate a reasoning "Thought" (strategic intent) and then the corresponding Python code.

- **思维增强变异（Thought-Augmented Mutation）：** 提示 LLM 先生成一段推理性"思维"（描述策略意图），再生成对应的 Python 代码。

  > **注释：** 这是核心改动。Prompt 格式大致为：`# Thought: <策略描述>\n# Code:\ndef priority(...):`。通过结构化 prompt 迫使模型显式规划，而非直接输出代码。

- **Program Database:** We will store (Thought, Code) pairs, allowing the LLM to retrieve and refine successful logical patterns rather than just raw code snippets.

- **程序数据库（Program Database）：** 存储（思维, 代码）对，使 LLM 能检索并改进成功的逻辑模式，而非仅仅是原始代码片段。

  > **注释：** 原始 FunSearch 的数据库只存代码岛（code island）。扩展为存储（Thought, Code）对后，进化压力同时作用于"策略层"和"实现层"，理论上可以跨越局部最优——因为两段代码看似不同，但背后的 Thought 可能相同，反之亦然。

- **Feedback Loop:** Heuristics will be evaluated in the provided sandbox. The scores will reinforce both the successful "thoughts" and their code implementations.

- **反馈循环（Feedback Loop）：** 启发式算法在沙箱中评估，评分同时强化成功的"思维"及其对应代码实现。

  > **注释：** 评分机制直接决定进化方向。将 Thought 纳入反馈意味着系统可以学习"哪类策略描述通常对应高分代码"，为后续变异提供更好的先验。

---

## 3 Evaluation Plan
## 3 评估方案

We will evaluate whether "thoughts" improve heuristic discovery via the following setup:

我们将通过以下实验设置评估"思维"是否能改善启发式算法的发现效果：

- **Datasets:** We will use OR-Library and WeiBull datasets, covering diverse item distributions to ensure the generalizability of our heuristics.

- **数据集：** 使用 OR-Library 和 WeiBull 数据集，涵盖多样化的物品分布，以确保启发式算法的泛化能力。

  > **注释：** OR-Library 是运筹学标准基准库；WeiBull 数据集以威布尔分布生成物品大小，模拟现实中的长尾分布场景。两者结合可验证算法在不同分布下的鲁棒性。

- **Baselines:** We will compare our results against (1) Vanilla FunSearch (code-only) and (2) Human Heuristics (Best-Fit and Least Remaining Capacity).

- **基线对比：** 与以下方法比较：① Vanilla FunSearch（纯代码，无思维增强）；② 人工启发式算法（Best-Fit 和 Least Remaining Capacity）。

  > **注释：** Best-Fit（最优适应）将物品放入剩余空间最小但仍能容纳的箱子；Least Remaining Capacity（最小剩余容量）是类似策略。两者均是在线装箱的经典贪心算法，是衡量 LLM 进化方法是否有实际价值的重要参照。

- **Metrics:** The primary metric is the **number of bins used**. We also measure search efficiency by tracking the iterations required to outperform baselines.

- **评估指标：** 主要指标为**使用的箱子数量**（越少越好）。同时通过追踪超越基线所需的迭代次数来衡量搜索效率。

  > **注释：** 箱子数量直接反映解的质量（与最优解的比值即近似比）。迭代次数则反映样本效率——如果思维增强能用更少的 LLM 调用达到相同质量，则证明 CoT 提升了进化搜索的效率，而非只是增加了计算开销。
