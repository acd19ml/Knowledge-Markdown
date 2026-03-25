# Reflexion：基于语言反馈强化学习的 Language Agents（Verbal Reinforcement Learning）

Noah Shinn Federico Cassano  
Northeastern University Northeastern University  
noahshinn024@gmail.com cassano.f@northeastern.edu  

Edward Berman Ashwin Gopinath  
Northeastern University Massachusetts Institute of Technology  
berman.ed@northeastern.edu agopi@mit.edu  

Karthik Narasimhan Shunyu Yao  
Princeton University Princeton University  
karthikn@princeton.edu shunyuy@princeton.edu  

---

## 摘要（Abstract）

**Large language models（LLMs）** 越来越多地被用作与外部环境（例如 games、compilers、**APIs**）交互的、目标驱动的 **agents**。然而，这些 **language agents** 仍难以像传统 **reinforcement learning（RL）** 那样快速、高效地从 **trial-and-error** 中学习——后者往往需要大量 **training samples** 与昂贵的 **model fine-tuning**。我们提出 **Reflexion**，一种不通过更新权重、而通过**语言反馈**来强化 **language agents** 的新框架。具体而言，**Reflexion** **agents** 对任务 **feedback signals** 进行**口头反思（verbally reflect）**，随后在 **episodic memory buffer** 中维护其反思文本，以在后续试验中诱导更好的 **decision-making**。**Reflexion** 足够灵活，可纳入多种类型（标量或自由形式语言）与来源（外部或内部模拟）的 **feedback signals**，并在多种任务（**sequential decision-making**、**coding**、**language reasoning**）上相对 **baseline agent** 取得显著提升。例如，**Reflexion** 在 **HumanEval** **coding benchmark** 上达到 **91%** **pass@1** **accuracy**，超过此前 **state-of-the-art**、达到 **80%** 的 **GPT-4**。我们还使用不同 **feedback signals**、**feedback incorporation** 方法与 **agent** 类型进行消融与分析，并讨论它们如何影响性能。代码、**demos** 与 **datasets** 见 https://github.com/noahshinn024/reflexion  

---

## 1 引言（Introduction）

近期工作如 **ReAct** [30]、**SayCan** [1]、**Toolformer** [22]、**HuggingGPT** [23]、**generative agents** [19] 与 **WebGPT** [17] 表明，在 **large language model（LLM）** 核心之上构建自主 **decision-making** **agents** 是可行的。这些方法用 **LLM** 生成文本与可用于 **API** 调用并在环境中执行的 **「actions」**。由于依赖参数量巨大的模型，此类方法迄今多限于用 **in-context examples** 来「教」**agents**，因为更传统的优化方案（如带 **gradient descent** 的 **reinforcement learning**）需要大量 **compute** 与时间。

本文提出一种替代方法 **Reflexion**，使用 **verbal reinforcement** 帮助 **agents** 从先前失败中学习。**Reflexion** 将环境中的二元或标量 **feedback** 转为**文本摘要**形式的口头 **feedback**，并在下一 **episode** 中作为额外 **context** 提供给 **LLM agent**。这种**自我反思式 feedback** 充当「**semantic**」**gradient signal**：为 **agent** 提供可改进的具体方向，帮助其从先前错误中学习并在任务上表现更好。这类似于人类以 **few-shot** 方式迭代完成复杂任务——反思先前失败，为下一次尝试形成改进的「攻击计划」。例如，在图 1 中，**Reflexion agent** 通过 **trial**、**error** 与 **self-reflection** 学习优化自身行为，以求解 **decision-making**、**programming** 与 **reasoning** 任务。

生成有用的反思式 **feedback** 具有挑战性：需要理解模型何处出错（即 **credit assignment problem** [25]），并能生成包含可执行改进洞见的摘要。我们探索三种做法——简单二元环境 **feedback**、针对常见失败情形的**预定义启发式**，以及 **self-evaluation**（例如用 **LLM** 做二元分类（**decision-making**）或自写 **unit tests**（**programming**））。在所有实现中，**evaluation signal** 被放大为可存入 **long-term memory** 的自然语言 **experience summaries**。

相对 **policy** 或 **value-based learning** 等传统 **RL** 方法，**Reflexion** 有多项优势：1）轻量，无需 **fine-tuning** **LLM**；2）允许更细粒度的 **feedback**（例如针对 **actions** 的目标化修改），相较难以做精确 **credit assignment** 的标量或向量 **rewards**；3）对过往 **experiences** 提供更显式、可解释的 **episodic memory** 形式；4）在未来 **episodes** 中为 **actions** 提供更明确的提示。同时，它也有依赖 **LLM** **self-evaluation** 能力（或启发式）、且对成功缺乏形式化保证的缺点。随着 **LLM** 能力提升，我们预期该范式会随时间改善。

我们在（1）**decision-making** 任务上测试长 **trajectories** 上的 **sequential action** 选择；（2）**reasoning** 任务上测试知识密集、单步生成的改进；（3）**programming** 任务上教导 **agent** 有效使用 **compilers** 与 **interpreters** 等外部工具。三类任务上，**Reflexion** **agents** 均是更好的 **decision-makers**、**reasoners** 与 **programmers**。更具体地，在 **AlfWorld** [24] **decision-making** 上，**12** 次迭代学习步骤内相对强基线绝对提升 **22%**；在 **HotPotQA** [28] **reasoning** 问题上提升 **20%**；在 **HumanEval** [6] **Python programming** 上最多提升 **11%**。

**贡献**总结如下：

- 提出 **Reflexion**，一种「**verbal**」**reinforcement** 新范式：将 **policy** 参数化为 **agent** 的 **memory encoding** 与所选 **LLM** **parameters** 的组合。  
- 探索 **LLM** 中 **self-reflection** 这一涌现性质，并经验性地表明 **self-reflection** 在少数几次试验中学习复杂任务极为有用。  
- 引入 **LeetcodeHardGym**：由 **40** 道挑战性 **Leetcode** 题（**hard-level**）、**19** 种 **programming languages** 构成的 **code-generation RL gym** 环境。  
- 表明 **Reflexion** 在多项任务上超越强基线，并在多种 **code generation benchmarks** 上达到 **state-of-the-art**。

---

## 2 相关工作（Related work）

### Reasoning and decision-making

**Self-Refine** [15] 采用 **self-refinement** 的迭代框架，通过 **self-evaluation** 自主改进生成。这些 **self-evaluation** 与 **self-improvement** 步骤以给定任务约束为条件，例如「How can this generation be written in a more positive way」。**Self-Refine** 有效，但限于单步生成的 **reasoning** 任务。**Pryzant et al.** [21] 做类似的 **semantic prompt-writing optimization**，同样限于单步生成。**Paul et al.** [20] **fine-tune critic models** 以在 **trajectories** 内提供中间 **feedback** 来改进 **reasoning** 回答。**Xie et al.** [27] 对 **actions** 使用随机 **beam search**，实现更高效的 **decision-making** **search**，使 **agent** 能利用 **self-evaluation** 带来的前瞻优势。**Yoran et al.** [31] 与 **Nair et al.** [16] 使用 **decider models** 在多代上 **reason**。**Kim et al.** [10] 在固定步数上使用 **retry pattern** 而无 **evaluation** 步骤。**Goodman** [9] 执行定性 **evaluation** 步骤，对前一代提出优化。本文表明，若干概念可通过 **self-reflection** 增强，以构建持久的 **self-reflective experiences** **memory**，使 **agent** 能识别自身错误并自我建议从错误中学习的教训。

**图 1 说明（对应原文 Figure 1；源 PDF 第 3 页为流程示意图）**：**Reflexion** 作用于 §4.1 **decision-making**、§4.3 **programming** 与 §4.2 **reasoning** 任务。

**相关工作（reasoning & decision-making）对照表**

| Approach | Self refine | Hidden constraints | Decision making | Binary reward | Memory |
|----------|-------------|-------------------|-----------------|---------------|--------|
| Self-refine [15] | ✓ | ✗ | ✗ | ✗ | ✗ |
| Beam search [27] | ✓ | ✓ | ✓ | ✓ | ✗ |
| Reflexion (ours) | ✓ | ✓ | ✓ | ✓ | ✓ |

### Programming

既往与近期工作采用 **test-driven development** 或 **code debugging** 的变体。**AlphaCode** [14] 在 **hidden test cases** 上评估一组生成。**CodeT** [5] 使用 **self-generated unit tests** 为生成的函数实现打分。**Self-Debugging** [7] 使用 **debugging** 组件，在给定 **code execution environment** **feedback** 下改进现有实现。**CodeRL** [12] 将问题置于 **RL** 框架，用 **actor-critic** 设置在给定 **execution environment** **feedback** 下调试程序。**AlphaCode**、**Self-Debugging** 与 **CodeRL** 在修复较简单程序 **bug** 上有效，但依赖 **ground truth test cases**，使 **pass@1** 资格失效，且未用 **self-reflection** 弥合 **error identification** 与 **implementation improvement** 之间的鸿沟。**CodeT** 不访问 **hidden test cases**，也未实现 **self-learning** 步骤以改进代码写作。

**相关工作（programming）对照表**

| Approach | Test execution | Debugging execution | Self-generated tests | Multiple languages | Self-reflection |
|----------|----------------|---------------------|----------------------|--------------------|-----------------|
| AlphaCode [14] | ✓ | ✗ | ✗ | ✓ | ✗ |
| CodeT [5] | ✓ | ✗ | ✓ | ✗ | ✗ |
| Self-debugging [7] | ✓ | ✓ | ✗ | ✗ | ✗ |
| CodeRL [12] | ✓ | ✓ | ✗ | ✗ | ✗ |
| Reflexion (ours) | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## 3 Reflexion：通过口头反思实现强化（Reinforcement via verbal reflection）

我们为 **Reflexion** 建立模块化表述，使用三个不同模型：**Actor**，记为 \(M_a\)，生成文本与 **actions**；**Evaluator** 模型 \(M_e\)，对 \(M_a\) 产生的输出打分；**Self-Reflection** 模型 \(M_{sr}\)，生成 **verbal reinforcement cues** 以辅助 **Actor** **self-improvement**。下文分别详述各模型及其在 **Reflexion** 框架内的协作。

### 算法 1：通过自我反思实现强化（Reinforcement via self-reflection）

（与原文 **Figure 2(b)** 一致：**Agent** 初始化 **Actor**、**Evaluator**、**Self-Reflection**：\(M_a, M_e, M_{sr}\)；初始化 **policy** \(\pi_\theta(a_i|s_i)\)，\(\theta=\{M_a, \texttt{mem}\}\)；用 \(\pi_\theta\) 生成初始 **trajectory**；用 \(M_e\) 评估 \(\tau_0\)；用 \(M_{sr}\) 生成初始 **self-reflection** \(sr_0\)；令 \(\texttt{mem} \leftarrow [sr_0]\)，\(t=0\)；当 \(M_e\) 未通过且 \(t<\texttt{max trials}\) 时：用 \(\pi_\theta\) 生成 \(\tau_t=[a_0,o_0,\ldots,a_i,o_i]\)；用 \(M_e\) 评估 \(\tau_t\)；用 \(M_{sr}\) 生成 \(sr_t\)；将 \(sr_t\) 追加到 **mem**；\(t \leftarrow t+1\)；结束。）

**图 2**：（a）**Reflexion** 示意图。（b）**Reflexion** **reinforcement** 算法。

### Actor

**Actor** 建立在经专门 **prompt** 的 **LLM** 之上，在给定状态 **observations** 条件下生成所需文本与 **actions**。类比传统 **policy-based RL**，我们在时刻 \(t\) 从当前 **policy** \(\pi_\theta\) 采样 **action** 或生成 \(a_t\)，从环境接收 **observation** \(o_t\)。我们探索多种 **Actor** 模型，包括 **Chain of Thought** [26] 与 **ReAct** [30]。这些不同生成模型使我们能在 **Reflexion** 框架内探索文本与 **action** 生成的不同方面。此外，我们加入 **memory** 组件 `mem`，为该 **agent** 提供额外 **context**；该改编受 **Brooks et al.** [3] 启发，其提出用 **in-context learning** 做 **policy iteration**。`mem` 如何填充见下文。

### Evaluator

**Evaluator** 在评估 **Actor** 生成输出质量上起关键作用。输入为生成的 **trajectory**，计算反映其在给定任务上下文中表现的 **reward score**。在 **semantic spaces** 上定义有效的 **value** 与 **reward functions** 较难，因此我们考察 **Evaluator** 的多种变体。对 **reasoning** 任务，我们探索基于 **exact match（EM）** 打分的 **reward functions**；对 **decision-making** 任务，采用针对具体评估准则定制的**预定义启发式** **functions**。此外，我们实验用 **LLM** 的另一实例作为 **Evaluator**，为 **decision-making** 与 **programming** 任务生成 **rewards**。这种多面的 **Evaluator** 设计使我们能考察不同打分策略，及其在不同任务上的有效性与适用性。

### Self-reflection

实例化为 **LLM** 的 **Self-Reflection** 模型通过生成**口头自我反思**，为未来试验提供有价值的 **feedback**。给定稀疏 **reward signal**（如二元成功/失败）、当前 **trajectory** 与持久 **memory** `mem`，**self-reflection** 模型生成细致、具体的 **feedback**。该 **feedback** 比标量 **rewards** 信息更丰富，存入 **agent** **memory**（`mem`）。例如，在多步 **decision-making** 中，**agent** 收到失败信号时，可推断某 **action** \(a_i\) 导致后续错误 **actions** \(a_{i+1}, a_{i+2}\)；**agent** 可口头说明本应采取不同 **action** \(a'_i\)，从而得到 \(a'_{i+1}, a'_{i+2}\)，并将该 **experience** 存入 **memory**。后续试验中，**agent** 可利用过往 **experiences**，在时刻 \(t\) 选择 \(a'_i\) 以适应 **decision-making**。**trial**、**error**、**self-reflection** 与持久 **memory** 的迭代过程，使 **agent** 通过信息丰富的 **feedback signals** 在各环境中快速提升 **decision-making** 能力。

### Memory

**Reflexion** 的核心概念包括 **short-term** 与 **long-term memory**。**Inference** 时，**Actor** 的决策以短、长程 **memory** 为条件，类似人类既记住近期细节，又从 **long-term memory** 调取提炼过的重要 **experiences**。在 **RL** 设置中，**trajectory** 历史充当 **short-term memory**；**Self-Reflection** 模型输出存入 **long-term memory**。二者共同提供既具体又受多轮试验所学教训影响的 **context**，这是 **Reflexion** **agents** 相对其他 **LLM** **action** 选择工作的重要优势。

### Reflexion 过程

**Reflexion** 形式化为算法 1 中的迭代优化。首次试验中，**Actor** 通过与环境交互产生 **trajectory** \(\tau_0\)。**Evaluator** 给出分数 \(r_0\)，计算为 \(r_t = M_e(\tau_t)\)。\(r_t\) 仅为试验 \(t\) 的标量 **reward**，随任务相关性能提高而改善。首次试验后，为将 \(r_0\) 放大为可供 **LLM** 用于改进的 **feedback**，**Self-Reflection** 模型分析 \(\{\tau_0, r_0\}\)，生成摘要 \(sr_0\) 存入 **memory** `mem`。\(sr_t\) 为试验 \(t\) 的**口头 experience feedback**。**Actor**、**Evaluator** 与 **Self-Reflection** 在循环中协同，直到 **Evaluator** 认为 \(\tau_t\) 正确。如 §3 所述，**memory** 对 **Reflexion** 有效性至关重要。每次试验 \(t\) 后，将 \(sr_t\) 追加到 `mem`。实践中，我们将 `mem` 限制为最多存储 \(\Omega\) 条 **experiences**（通常 **1–3**），以遵守 **max context** **LLM** 限制。

---

## 4 实验（Experiments）

我们在 **decision-making**、**reasoning** 与 **code generation** 任务上评估多种自然语言 **RL** 设置。具体地，要求 **agent** 在 **HotPotQA** [28] 上做基于搜索的问答，在 **AlfWorld** [24] 的常见家庭环境中做多步任务，并在 **HumanEval** [6]、**MBPP** [2] 与新建 **benchmark** **LeetcodeHard** 等类竞赛环境中进行代码写作（含 **interpreters** 与 **compilers**）。最突出的是，**Reflexion** 相对强基线在 **AlfWorld** 上提升 **22%**，**HotPotQA** 上 **20%**，**HumanEval** 上 **11%**。

### 4.1 Sequential decision-making：ALFWorld

**AlfWorld** 是一组基于文本的环境，要求 **agent** 在多种交互环境中解决多步任务，建立在 **TextWorld** [8] 之上。遵循 **Yao et al.** [30]，我们在 **134** 个 **AlfWorld** 环境、**six** 类任务上运行 **agent**，包括寻找隐藏物体（如在抽屉里找 spatula）、移动物体（如把刀移到案板）、以及用其他物体操作物体（如把西红柿放入冰箱冷藏）。我们用 **ReAct** [30] 作为 **action generator**，因 **Yao et al.** [30] 表明显式中间 **thoughts** 有助于长 **trajectory** **decision-making**。**AlfWorld** 任务自然需要 **self-evaluation** 步骤，因环境只能信号化任务是否完成。为实现完全自主行为，我们实现两种 **self-evaluation** 技术：**LLM** 自然语言分类与**手写启发式**。启发式很简单：若 **agent** 执行相同 **action** 并收到相同响应超过 **3** 个周期，或当前环境中 **actions** 数超过 **30**（低效规划），则进行 **self-reflect**。在基线运行中，若建议 **self-reflection**，则跳过 **self-reflection**、重置环境并开始新试验。在 **Reflexion** 运行中，**agent** 用 **self-reflection** 找错、更新 **memory**、重置环境并开始新试验。为避免 **prompt** 窗口过长超过上限，将 **agent** **memory** 截断为最近 **3** 条 **self-reflections**（**experiences**）。

为避免语法错误，向 **agent** 提供两条领域相关的 **few-shot trajectories**。对 **LLM** 使用与 **Yao et al.** [30] 相同的 **few-shot trajectory** 示例及 **GPT-3**。**AlfWorld** 任务、**ReAct few-shot prompts** 与 **Reflexion** 示例见附录。

**结果**：**ReAct + Reflexion** 用简单启发式检测 **hallucinations** 与低效规划，在 **134** 项任务中完成 **130** 项，显著优于 **ReAct**。**ReAct + Reflexion** 在 **12** 次连续试验中通过学习额外解决更多任务。仅 **ReAct** 时，性能提升在试验 **6** 与 **7** 之间停滞。

**分析**：基线失败 **AlfWorld trajectory** 的常见错误是 **agent** 认为已拿到物品但实际没有，随后在长 **trajectory** 中执行多个 **actions** 且无法回溯找到错误。**Reflexion** 通过 **self-reflection** 将长失败 **trajectory** 提炼为可在未来用作「**self-hints**」的相关 **experiences**，几乎消除此类情况。**Long-term memory** 在 **AlfWorld** 帮助 **agent** 主要有两类：1）长 **trajectory** 中的早期错误易被识别，**agent** 可建议新 **action** 选择甚至新长期计划；2）需检查的台面/容器过多，**agent** 可利用多轮试验的 **experience memory** 彻底搜索房间。图 3 的学习曲线表明学习发生在多段 **experiences** 上：**agent** 成功平衡两类情况——前两轮试验间改进陡升，随后 **11** 轮试验稳步提升至近完美表现。另一方面，图 3 显示仅 **ReAct** 的 **agent** 在 **hallucination rate** **22%** 处收敛，无长期恢复迹象。

**图 3**：（a）**134** 项 **AlfWorld** 任务上的表现，展示使用 **(Heuristic)** 与 **(GPT)** 二元分类 **self-evaluation** 时已解决任务的累积比例。（b）按失败原因对 **AlfWorld trajectories** 的分类。

### 4.2 Reasoning：HotpotQA

**HotPotQA** [28] 是基于 Wikipedia 的数据集，含 **113k** 问答对，要求 **agents** 解析内容并在多篇支撑文档上 **reason**。为单独测试 **reasoning** 能力，我们实现 **Reflexion + Chain-of-Thought（CoT）** [26] 的逐步 **Q→A** 与 **Q, C_gt→A**，其中 **Q** 为问题，**C_gt** 为数据集中的 **ground truth context**，**A** 为最终答案。因 **CoT** 非多步 **decision-making**，向 **agent** 提供 **C_gt** 以隔离对大段给定文本的 **reasoning**。为测试需要 **reasoning** 与 **action** 选择的整体问答，实现 **Reflexion + ReAct** [30] **agent**，用 **Wikipedia API** 检索相关 **context** 并以逐步显式思考推断答案。**CoT** 用 **6-shot prompting**；**ReAct** 用 **2-shot**；**self-reflection** 用 **2-shot**。示例见附录。

稳健评估自然语言回答是 **NLP** 长期难题。因此，在试验间用环境中的 **exact match** 答案打分，向 **agent** 提供二元成功信号。每次试验后，采用 **self-reflection** 循环放大二元信号，类似 **AlfWorld** §4.1 **decision-making** 设置，**memory** 大小为 **3** 条 **experiences**。

**结果**：**Reflexion** 在多个学习步上显著优于所有基线。此外，仅 **ReAct**、仅 **CoT**、仅 **CoT(GT)** 的实现无法在概率意义上改进任何任务——即任一基线在首次试验失败的任务，在 **temperature 0.7** 下后续试验均未能解出。在 **Reflexion** 运行中，允许 **agent** 积累经验并对失败任务重试，直到该任务连续 **3** 次失败。自然，**CoT(GT)** 因可访问问题的 **ground truth context** 而 **accuracy** 更高。但 **CoT(GT) agent** 仍有 **39%** 问题无法正确推断答案；**Reflexion** 帮助 **agent** 在无 **ground truth answer** 访问下纠错，**accuracy** 提升 **14%**。

**图 4**：**CoT** 与 **ReAct**。**Reflexion** 在 **100** 个 **HotPotQA** 问题上提升搜索、信息检索与 **reasoning**。（a）**Reflexion ReAct** vs **Reflexion CoT**（b）**Reflexion CoT(GT)** 仅 **reasoning**（c）**Reflexion** vs **episodic memory** 消融。

**分析**：我们做消融以隔离 **self-reflective** 步骤在 **reasoning** 上的优势，以 **CoT(GT)** 为基线（脚注 4）。**CoT(GT)** 在提供 **ground truth context** 下用 **Chain-of-Thought** **reasoning**，测试长 **context** **reasoning**。接着加入 **episodic memory（EPM）**：纳入最近 **trajectory**。**Reflexion agent** 将标准 **self-reflection** 步骤作为最终一遍。直观上，检验 **agent** 是否通过第一人称语言的书面口头解释更有效地迭代学习。图 4 表明 **self-reflection** 相对 **episodic memory** 学习优势带来 **8%** 绝对提升。该结果支持：**refinement-only** 方法不如 **self-reflection** 引导的 **refinement** 有效。

### 4.3 Programming

我们在 **Python** 与 **Rust** 代码写作上评估基线与 **Reflexion**，**benchmark** 为 **MBPP** [2]、**HumanEval** [6] 与我们新数据集 **LeetcodeHardGym**。**MBPP** 与 **HumanEval** 在给定自然语言描述下衡量函数体生成 **accuracy**。我们用 **benchmark** 语言 **compiler** **MultiPL-E** [4] 将 **HumanEval** 与 **MBPP** 子集译为 **Rust**。**MultiPL-E** 是一组可将 **Python benchmark** 题目译为 **18** 种其他语言的小型 **compilers**。我们包含 **Rust** **code generation** 实验，以表明 **Reflexion** 实现与语言无关，可用于解释型与编译型语言。最后介绍新 **benchmark** **LeetcodeHardGym**：交互式 **programming gym**，含 **40** 道 **Leetcode hard** 题目，发布日晚于 **2022** 年 **10** 月 **8** 日（**GPT-4** [18] 的 **pre-training cutoff**）。

**Programming** 任务为使用更**落地**的 **self-evaluation** 实践（如 **self-generated unit test suites**）提供独特机会。因此，基于 **Reflexion** 的 **programming** 实现符合 **pass@1** **accuracy** 报告。为生成 **test suite**，用 **Chain-of-Thought prompting** [26] 生成多样、广泛的 **tests** 及对应自然语言描述；通过尝试为每个提议 **test** 构造有效 **abstract syntax tree（AST）** 过滤语法有效 **test** 语句；最后从生成的 **unit tests** 中采样 \(n\) 个 **tests** 构成 **test suite** \(\mathcal{T}=\{t_0,t_1,\ldots,t_n\}\)，\(n\) 最多 **6** 个 **unit tests**。除 **unit test suite** 外，**Reflexion programming agent** 的学习循环与 **reasoning**、**decision-making** **agents** 相同，**max memory** 限制为 **1** 条 **experience**。

**表 1**：不同模型–策略–语言组合的 **pass@1** **accuracy**。基础策略为单次代码生成采样。所有 **instruction-based** 模型遵循 **zero-shot code generation**。

| Benchmark + Language | Prev SOTA Pass@1 | SOTA Pass@1 | Reflexion Pass@1 |
|----------------------|------------------|-------------|------------------|
| HumanEval (PY) | 65.8 (CodeT [5] + GPT-3.5) | 80.1 (GPT-4) | 91.0 |
| HumanEval (RS) | – | 60.0 (GPT-4) | 68.0 |
| MBPP (PY) | 67.7 (CodeT [5] + Codex [6]) | 80.1 (GPT-4) | 77.1 |
| MBPP (RS) | – | 70.9 (GPT-4) | 75.4 |
| LeetcodeHard (PY) | – | 7.5 (GPT-4) | 15.0 |

**表 2**：**HumanEval** 与 **MBPP** 的总体 **accuracy** 与 **test generation** 表现。**Rust** 下 **HumanEval** 为经 **MultiPL-E** [4] 从 **HumanEval Python** 翻译的最难 **50** 题。**TP**：**unit tests** 通过且解答通过；**FN**：**unit tests** 失败但解答通过；**FP**：**unit tests** 通过但解答失败；**TN**：**unit tests** 失败且解答失败。

| Benchmark + Language | Base | Reflexion | TP | FN | FP | TN |
|----------------------|------|-----------|----|----|----|-----|
| HumanEval (PY) | 0.80 | 0.91 | 0.99 | 0.40 | 0.01 | 0.60 |
| MBPP (PY) | 0.80 | 0.77 | 0.84 | 0.59 | 0.16 | 0.41 |
| HumanEval (RS) | 0.60 | 0.68 | 0.87 | 0.37 | 0.13 | 0.63 |
| MBPP (RS) | 0.71 | 0.75 | 0.84 | 0.51 | 0.16 | 0.49 |

**结果**：**Reflexion** 超越所有基线 **accuracy**，在 **Python** 与 **Rust** 各 **benchmark** 上均设新 **state-of-the-art**，**除 MBPP（Python）外**¹。我们进一步分析 **Reflexion** 在 **MBPP Python** 上较差的原因。

**分析**：我们承认，**self-reflecting code-generation agents** 受其编写多样、全面 **tests** 的能力约束。若模型生成 **flaky test suite**，可能出现所有 **tests** 在错误解答上通过，从而在 **code completion** 上产生**假阳性**标签 [11]。反之，若 **test suite** 写错，部分 **tests** 可能在正确解答上失败，导致以**假阴性** **code completion** 为条件的 **self-reflection** 生成。给定 **Reflexion** 实现，**false negatives** 优于 **false positives**：**agent** 可能通过 **self-reflection** 识别错误 **test(s)** 并提示自身保留原始 **code completion**。另一方面，若无效 **test suite** 返回假阳性完成（内部 **test cases** 全通过但实现错误），**agent** 会过早报告无效提交。表 2 测量多种情形以分析 **pass@1** 之外的性能。此前我们展示 **Reflexion** 相对基线 **GPT-4** 在 **MBPP Python** 上较差。表 2 中，**false positive** 标签（内部 **test** 执行产生）存在显著差异：**P(非 pass@1 生成正确 | tests 通过)**，即在通过所有 **unit tests** 条件下提交仍失败的概率。**HumanEval** 与 **MBPP Python** 的基线 **pass@1** **accuracy** 相近（**82%** 与 **80%**），但 **MBPP Python** 的 **false positive test execution rate** 为 **16.3%**，**HumanEval Python** 仅 **1.4%**，从而整体 **accuracy** 为 **91%**¹。

**表 3**：在 **HumanEval Rust-50** 最难子集上，以 **GPT-4** 为基模型，**Reflexion** 各受损方法的 **pass@1** **accuracy**。

| Approach | Test Generation | Self-reflection | Pass@1 (Acc) |
|----------|-----------------|-----------------|--------------|
| Base model | False | False | 0.60 |
| Test generation omission | False | True | 0.52 |
| Self-reflection omission | True | False | 0.60 |
| Reflexion | True | True | 0.68 |

**消融研究**：在 **HumanEval Rust** 最难 **50** 题子集上测试 **Reflexion** 中 **test generation** 与 **self-reflection** 协同的复合方法。我们的 **Rust compiler** 环境提供详细 **error logs** 与有用 **debugging hints**，适合测试受损方案。首先省略内部 **test generation** 与执行步骤，检验无当前实现指导下的 **self-reflect**；表 3 显示 **52%** vs **60%**（基线）**accuracy**，表明无 **unit tests** 无法判断当前实现是否正确，**agent** 必须参与所有迭代且无提前返回选项，对实现做有害编辑。其次省略失败 **unit test suite** 评估后的自然语言解释步骤以测试 **self-reflection** 贡献；直观上，这要求 **agent** 在所有失败 **tests** 上合并 **error identification** 与 **implementation improvement**。有趣的是，受损 **agent** 相对基线运行无改进。我们观察到 **test generation** 与 **code compilation** 能捕捉语法与逻辑错误，但实现修复未反映这些信号。经验结果表明，若干近期提出的、无 **self-reflection** 的盲目 **trial-and-error debugging** 在更难任务（如 **Rust** 复杂程序）上无效。

---

## 5 局限性（Limitations）

本质上，**Reflexion** 是用自然语言做 **policy optimization** 的优化技术。**Policy optimization** 能通过 **experience** 改进 **action** 选择，但仍可能陷入非最优**局部极小**。本研究将 **long-term memory** 限制为带最大容量的**滑动窗口**；我们鼓励未来用 **vector embedding databases** 或传统 **SQL databases** 等更先进结构扩展 **Reflexion** 的 **memory**。针对 **code generation**，**test-driven development** 在指定精确输入–输出映射上有许多实际限制，如非确定性 **generator functions**、与 **API** 交互的非纯函数、随硬件规格变化的输出、或难以预测的并行/并发行为。

---

## 6 更广泛影响（Broader impact）

**Large language models** 越来越多地与外部环境（如 Internet、**software**、**robotics** 等）及人类交互。我们的工作有潜力强化并赋能这些 **agents** 以实现更高自动化与工作效率，但也放大误用风险。我们认为该研究方向需在安全与伦理考量上投入更多努力。

另一方面，**reinforcement learning** 长期受 **black-box policy** 与优化设置困扰，**interpretability** 与 **alignment** 困难。我们提出的「**verbal**」**reinforcement learning** 或可缓解部分问题，使自主 **agents** 更可解释、可诊断。例如，对人类过难理解的 **tool-use**，可监控 **self-reflections** 以确保使用工具前意图正确。

---

## 7 结论（Conclusion）

本文提出 **Reflexion**，利用 **verbal reinforcement** 教导 **agents** 从过去错误中学习。我们经验性地表明，**Reflexion** **agents** 通过 **self-reflection** 显著优于当前广泛使用的 **decision-making** 方法。未来可将 **traditional RL** 中已充分研究的技术（如自然语言中的 **value learning** 或 **off-policy exploration**）用于 **Reflexion**。

---

## 8 可复现性（Reproducibility）

强烈建议他人在运行自主代码写作实验时使用**隔离执行环境**，因生成代码在执行前未经充分验证。

---

## 参考文献（References）

[1] Ahn, M., Brohan, A., Brown, N., Chebotar, Y., Cortes, O., David, B., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., et al. (2022). Do as I can, not as I say: Grounding language in robotic affordances. *arXiv preprint* arXiv:2204.01691.

[2] Austin, J., Odena, A., Nye, M., Bosma, M., Michalewski, H., Dohan, D., Jiang, E., Cai, C., Terry, M., Le, Q., et al. (2021). Program synthesis with large language models. *arXiv preprint* arXiv:2108.07732.

[3] Brooks, E., Walls, L., Lewis, R. L., and Singh, S. (2022). In-context policy iteration. *arXiv preprint* arXiv:2210.03821.

[4] Cassano, F., Gouwar, J., Nguyen, D., Nguyen, S., Phipps-Costin, L., Pinckney, D., Yee, M.-H., Zi, Y., Anderson, C. J., Feldman, M. Q., Guha, A., Greenberg, M., and Jangda, A. (2022). MultiPL-E: A scalable and extensible approach to benchmarking neural code generation.

[5] Chen, B., Zhang, F., Nguyen, A., Zan, D., Lin, Z., Lou, J.-G., and Chen, W. (2022). CodeT: Code generation with generated tests. *arXiv preprint* arXiv:2207.10397.

[6] Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H. P. d. O., Kaplan, J., Edwards, H., Burda, Y., Joseph, N., Brockman, G., et al. (2021). Evaluating large language models trained on code. *arXiv preprint* arXiv:2107.03374.

[7] Chen, X., Lin, M., Schärli, N., and Zhou, D. (2023). Teaching large language models to self-debug. *arXiv preprint* arXiv:2304.05128.

[8] Côté, M.-A., Kádár, A., Yuan, X., Kybartas, B., Barnes, T., Fine, E., Moore, J., Hausknecht, M., El Asri, L., Adada, M., et al. (2019). TextWorld: A learning environment for text-based games. In *Computer Games: 7th Workshop, CGW 2018, Held in Conjunction with the 27th International Conference on Artificial Intelligence, IJCAI 2018, Stockholm, Sweden, July 13, 2018, Revised Selected Papers 7*, pages 41–75. Springer.

[9] Goodman, N. (2023). Meta-prompt: A simple self-improving language agent. noahgoodman.substack.com.

[10] Kim, G., Baldi, P., and McAleer, S. (2023). Language models can solve computer tasks. *arXiv preprint* arXiv:2303.17491.

[11] Lam, W., Winter, S., Wei, A., Xie, T., Marinov, D., and Bell, J. (2020). A large-scale longitudinal study of flaky tests. *Proc. ACM Program. Lang.*, 4 (OOPSLA).

[12] Le, H., Wang, Y., Gotmare, A. D., Savarese, S., and Hoi, S. C. H. (2022). CodeRL: Mastering code generation through pretrained models and deep reinforcement learning. *Advances in Neural Information Processing Systems*, 35:21314–21328.

[13] Li, R., Allal, L. B., Zi, Y., Muennighoff, N., Kocetkov, D., Mou, C., Marone, M., Akiki, C., Li, J., Chim, J., et al. (2023). StarCoder: may the source be with you! *arXiv preprint* arXiv:2305.06161.

[14] Li, Y., Choi, D., Chung, J., Kushman, N., Schrittwieser, J., Leblond, R., Eccles, T., Keeling, J., Gimeno, F., Dal Lago, A., et al. (2022). Competition-level code generation with AlphaCode. *Science*, 378(6624):1092–1097.

[15] Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao, L., Wiegreffe, S., Alon, U., Dziri, N., Prabhumoye, S., Yang, Y., et al. (2023). Self-refine: Iterative refinement with self-feedback. *arXiv preprint* arXiv:2303.17651.

[16] Nair, V., Schumacher, E., Tso, G., and Kannan, A. (2023). DERA: Enhancing large language model completions with dialog-enabled resolving agents. *arXiv preprint* arXiv:2303.17071.

[17] Nakano, R., Hilton, J., Balaji, S., Wu, J., Ouyang, L., Kim, C., Hesse, C., Jain, S., Kosaraju, V., Saunders, W., et al. (2021). WebGPT: Browser-assisted question-answering with human feedback. *arXiv preprint* arXiv:2112.09332.

[18] OpenAI (2023). GPT-4 technical report. *ArXiv*.

[19] Park, J. S., O’Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., and Bernstein, M. S. (2023). Generative agents: Interactive simulacra of human behavior. *arXiv preprint* arXiv:2304.03442.

[20] Paul, D., Ismayilzada, M., Peyrard, M., Borges, B., Bosselut, A., West, R., and Faltings, B. (2023). Refiner: Reasoning feedback on intermediate representations. *arXiv preprint* arXiv:2304.01904.

[21] Pryzant, R., Iter, D., Li, J., Lee, Y. T., Zhu, C., and Zeng, M. (2023). Automatic prompt optimization with "gradient descent" and beam search. *arXiv preprint* arXiv:2305.03495.

[22] Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N., and Scialom, T. (2023). Toolformer: Language models can teach themselves to use tools. *arXiv preprint* arXiv:2302.04761.

[23] Shen, Y., Song, K., Tan, X., Li, D., Lu, W., and Zhuang, Y. (2023). HuggingGPT: Solving AI tasks with ChatGPT and its friends in Hugging Face. *arXiv preprint* arXiv:2303.17580.

[24] Shridhar, M., Yuan, X., Côté, M.-A., Bisk, Y., Trischler, A., and Hausknecht, M. (2021). ALFWorld: Aligning Text and Embodied Environments for Interactive Learning. In *Proceedings of the International Conference on Learning Representations (ICLR)*.

[25] Sutton, R. S. and Barto, A. G. (2018). *Reinforcement Learning: An Introduction*. The MIT Press, second edition.

[26] Wei, J., Wang, X., Schuurmans, D., Bosma, M., Chi, E., Le, Q., and Zhou, D. (2022). Chain-of-thought prompting elicits reasoning in large language models. *arXiv preprint* arXiv:2201.11903.

[27] Xie, Y., Kawaguchi, K., Zhao, Y., Zhao, X., Kan, M.-Y., He, J., and Xie, Q. (2023). Decomposition enhances reasoning via self-evaluation guided decoding. *arXiv preprint* arXiv:2305.00633.

[28] Yang, Z., Qi, P., Zhang, S., Bengio, Y., Cohen, W. W., Salakhutdinov, R., and Manning, C. D. (2018). HotpotQA: A dataset for diverse, explainable multi-hop question answering. In *Conference on Empirical Methods in Natural Language Processing (EMNLP)*.

[29] Yao, S., Chen, H., Yang, J., and Narasimhan, K. (preprint). WebShop: Towards scalable real-world web interaction with grounded language agents. In *ArXiv*.

[30] Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., and Cao, Y. (2023). ReAct: Synergizing reasoning and acting in language models. In *International Conference on Learning Representations (ICLR)*.

[31] Yoran, O., Wolfson, T., Bogin, B., Katz, U., Deutch, D., and Berant, J. (2023). Answering questions by meta-reasoning over multiple chains of thought. *arXiv preprint* arXiv:2304.13007.

---

## 附录 A：更多模型的评估（Evaluation with additional models）

我们进一步研究了不同强度模型下 **trial-and-error** 问题求解的适用性。发现指定**自我纠正**的能力是更强、更大模型的**涌现性质**。

**表 4**：使用 **starchat-beta** [13] 在 **HumanEval Python** 上的 **pass@1** **accuracy**（**8** 次试验平均）。

| Approach | Pass@1 accuracy (avg over 8 trials) | Pass@1 accuracy (std) |
|----------|-------------------------------------|------------------------|
| Baseline | 0.26 | 0.00481 |
| Reflexion | 0.26 | 0.00305 |

**表 5**：多种模型在 **100** 个 **HotPotQA** 上的 **pass@1** **accuracy**。

| Model | Baseline accuracy | Reflexion accuracy |
|-------|-------------------|---------------------|
| CoT(GT)+text-davinci-003 | 0.60 | 0.77 |
| CoT(GT)+gpt-3.5-turbo | 0.57 | 0.71 |
| CoT(GT)+gpt-4 | 0.68 | 0.80 |
| ReAct+text-davinci-003 | 0.30 | 0.55 |
| ReAct+gpt-3.5-turbo | 0.26 | 0.38 |
| ReAct+gpt-4 | 0.39 | 0.51 |

---

## 附录 B：Decision-making

**环境（Environment）**：You are in the middle of a room. Looking quickly around you, you see a bed 1, a desk 2, a desk 1, a drawer 6, a drawer 5, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a garbage can 1, a laundry hamper 1, a safe 1, a shelf 6, a shelf 5, a shelf 4, a shelf 3, a shelf 2, and a shelf 1.

**任务（Task）**：examine the mug with the desk lamp.

**Trial #1**

`>think:` To solve the task, I need to find and take a mug, then find and use a desk lamp.  
`>think:` First I need to find a mug. A mug is more likely to appear in drawer (1-6), desk (1-2), shelf (1-6), garbage can (1), laundry hamper (1). I can check one by one, starting with drawer 1.  
`>go to drawer 1`  
The drawer 1 is closed.  
`...`（原文此处为省略号，表示中间若干步与环境反馈，与 `Reflexion_clean.txt` 一致）  
`>open drawer 6`  
You open the drawer 6. The drawer 6 is open. In it, you see a keychain 2.  
`>go to desk 1`  
On the desk 1, you see a credit card 3, a desk lamp 1, a laptop 2, a mug 1, a pen 1, and a pencil 1.  
`>think:` Now I find a mug (1). Next, I need to take it.  
`>take mug 1 from desk 1`  
You pick up the mug 1 from the desk 1.  
`>think:` Now I take a mug (1). Next, I need to find a desk lamp. A desk lamp is more likely to appear in desk (1-2), sidetable (1-2), shelf (1-6), bed (1), drawer (1-6). I can check one by one, starting with desk 1.  
`>go to desk 1`  
Nothing happens.  
`>go to desk 2`  
On the desk 2, you see a alarm clock 1, a bowl 1, a mug 3, a pencil 3, and a pencil 2.  
`>think:` Now I find a desk lamp (1). Next, I need to use it.  
`>use desklamp 1`  
Nothing happens.  
`>use desklamp 1`  
Nothing happens.  
**Status: Fail**

**Reflection:** In this environment, my plan was to find a mug then find and use a desk lamp. However, the task says to examine the mug with the desk lamp. I should have looked for the desk lamp first, then looked for the mug. I noticed that the desk lamp was found on desk 1. In the next trial, I will go to desk 1, find the lamp, then look for the mug and examine it with the desk lamp.

**Trial #2**

`>go to desk 1`  
On the desk 1, you see a credit card 3, a desk lamp 1, a laptop 2, a mug 1, a pen 1, and a pencil 1.  
`>think:` To solve the task, I need to find and take a mug, then find and use a desk lamp.  
`>take mug 1 from desk 1`  
You pick up the mug 1 from the desk 1.  
`>think:` To solve the task, I need to find and take a mug, then find and use a desk lamp.  
`>use desklamp 1`  
You turn on the desk lamp 1.  
**Status: Success**

**图 5（Figure 5）**：[上] 一段 **AlfWorld trajectory**，**agent** 因低效规划失败；在 **reflection** 中，**agent** 认识到应先找 desk lamp 再找 mug，而非先 mug 后 lamp。[下] **agent** 能修正其 **reasoning trace** 并以简洁方式执行 **action** 序列。

### B.1 WebShop 局限性（WebShop Limitation）

在 §5 中我们简要指出，**Reflexion** 难以克服需要极强创造性才能逃出的**局部极小**选择。我们在 **WebShop** [29] 上的实验观察到这一不足。**WebShop** 是基于 web 的问题求解 **benchmark**，测试 **agents** 导航电商网站以根据客户请求定位并购买商品。我们在 **100** 个环境上测试 **two-shot ReAct + Reflexion** **agent**。然而，仅在 **four** 次试验后我们就终止运行，因为 **agent** 没有表现出改进迹象（脚注 6）。此外，**agent** 在失败尝试后未生成有用、直观的 **self-reflections**。我们结论：**Reflexion** 无法解决需要大量多样性与探索的任务。在 **AlfWorld** 中，**agent** 能充分探索新环境，因为 **permissible actions** 可在 **observations** 中看到。在 **HotPotQA** 中，**agent** 面临与 **WebShop** 类似的搜索查询任务，但更成功，因为 Wikipedia 文章的搜索空间更多样、对精确搜索查询要求较低。电商搜索引擎的一个常见问题是如何妥善处理自然语言搜索解释中的歧义。因此，**WebShop** 呈现的任务要求 **Reflexion agent** 具备非常多样且独特的行为。

**图 6**：**WebShop** **100** 条客户购物请求上 **Reflexion** vs **ReAct**。**ReAct + Reflexion** 未能显著超过 **ReAct**。

---

## 附录 C：Programming

由于 **LLM** 经过大量 **dialogue** 训练，**Programming** 的 **LLM** 调用需要严格指令以仅产生函数体。下文给出少量 **programming** 示例（原文中 instruction 以蓝色高亮与模板呈现）。完整实现见 https://github.com/noahshinn024/reflexion  

### C.1 Programming function implementation example（HumanEval Python）

**示例函数签名（Sample function signature）：**

```python
def minSubArraySum(nums):
    """
    Given an array of integers nums, find the minimum sum of
    any non-empty sub-array of nums.
    Example
    minSubArraySum([2, 3, 4, 1, 2, 4]) == 1
    minSubArraySum([-1, -2, -3]) == -6
    """
```

**示例函数体实现（Sample function body implementation）：**

```python
min_sum = float('inf')
for i in range(len(nums)):
    current_sum = 0
    for j in range(i, len(nums)):
        current_sum += nums[j]
        if current_sum < min_sum:
            min_sum = current_sum
return min_sum
```

### C.2 Reflexion Actor instruction（中译）

你是 **Python** 写作助手。你将获得：你对某函数的先前实现、一系列 **unit tests** 结果、以及你对先前实现的 **self-reflection**。请在下方应用必要修改，**仅**回复改进后的函数体；**不要**在回复中包含 **signature**。你回复的第一行应有 **4** 个空格缩进，以便与用户提供的 **signature** 在语法上衔接。用户将给你少量示例。

**Reflexion Actor** 生成遵循形式：（Instruction）→（Function implementation）→（Unit test feedback）→（Self-reflection）→（Instruction for next function implementation）。完整示例见 https://github.com/noahshinn024/reflexion  

### C.3 Reflexion Self-reflection instruction and example（中译）

（与 **C.2** 开头指令相同，直至「用户将给你少量示例」。）**Reflexion Self-Reflection** 生成遵循形式：（Instruction）→（Function implementation）→（Unit test feedback）。

### C.4 Reflexion programming no Self-Reflection ablation example

**无 Self-Reflection 消融**的 **Actor** 生成形式：（Instruction）→（Function implementation）→（Unit test feedback）→（Self-reflection）→（Instruction for next function implementation）。

### C.5 Reflexion programming no test generation ablation example

**无 test generation 消融**的 **Actor** 生成形式：在 `Reflexion_clean.txt` 抽取结果中与 **C.4** 所列条目相同（均为 Instruction → Function implementation → Unit test feedback → Self-reflection → Instruction for next function implementation）。若以 **no test generation** 语义为准，应对应省略 **test generation / unit test** 相关步骤；请以原论文 PDF 版式为准。

---

## 附录 D：Reasoning

### D.1 Full example（HotPotQA + ReAct；要点中译）

**问题**：*Grown-Ups* 主演的演员在 *’Allo ’Allo!* 中以哪一角色最为人知？

**Trial #1**：**agent** 搜索 *Grown-Ups* 与 *’Allo ’Allo!*，试图先找主演再找其在 *’Allo ’Allo!* 中最知名的角色；对 *’Allo ’Allo!* 的搜索失败，改搜 *Gorden Kaye*，推断答案为 **Rene Artois**，判定 **INCORRECT**。

**Reflection（反思）**：我搜索了错误的剧目名称 *’Allo ’Allo!*，导致无结果。本应搜索该剧主角 **Gorden Kaye**，以找出他在剧中最知名的角色。

**Trial #2**：**agent** 改为搜索最适于 *’Allo ’Allo!* 角色的演员并找到 **Sam Kelly**，得出 **Captain Hans Geering**，判定 **CORRECT**。

**图 7**：同一环境与任务下的两次 **HotPotQA** **trial**。**Reflexion + ReAct** **agent** 用 **self-reflection** 在下次 **trial** 中确定更好的搜索方式。

### D.2 Chain-of-Thought + Reflexion（要点中译）

**问题**：John Lanchester 与 Alan Dean Foster 的共同职业是什么？

**Trial #1**：推理为 **novelist and screenwriter**，答案错误。  
**Reflection**：错误在于假设两人职业完全相同；未来应更仔细调研两人背景，并考虑他们可能有多项共同职业。  
**Trial #2**：给出 **novelist**，正确。

### D.3 HotPotQA Chain-of-Thought (GT) + Reflexion（要点中译）

**上下文**涉及美国独立战争期间 **White Plains** 附近战役等。**问题**要求：1776 年 10 月 28 日纽约州 **White Plains** 附近、为控制纽约市与新泽西而战的**一系列战役**是什么？

**Trial #1**：答 **Battle of White Plains**，错误。  
**Reflection**：问题要的是**一系列战役**，我只给了一场战役的名称；应给出 **campaign** 名称（**New York and New Jersey campaign**）并补充日期、地点等上下文。  
**Trial #2**：答 **The New York and New Jersey campaign**，正确。

### D.4 HotPotQA episodic memory（EPM）ablation prompts（要点中译）

**D.4.1 (EPM) CoT + Reflexion**：比较 Jonny Craig 与 Pete Doherty 谁加入的乐队更多；首次误判后 **reflection** 强调需同时考察过去与现在的乐队成员关系以准确比较。

**D.4.2 (EPM) CoT (GT) + Reflexion**：关于 **Rastriya Janashakti Party** 外事部门负责人所持学位缩写 **MS / M.S. / ScM** 所属**领域**；首次误答宽泛的「科学、工程、医学」类别；**reflection** 指出误将「学位类别」当作「具体领域」；第二次聚焦 **M.Sc. in Engineering**，答 **Engineering**，正确。

---

**脚注说明**

- 原文 **Preprint. Under review.** 及倒置 **arXiv** 页脚见 `Reflexion_clean.txt` 第 41–46 行。  
- **MBPP Python** 与 **91% overall accuracy**、**WebShop** 试验、**HotPotQA** 消融等脚注编号与原文句中上标对应。

**说明**：译文依据 `Reflexion_clean.txt`；**Reflexion_tables.json** 中第 3 页多为 PDF **CID** 碎片，可读表格以正文与本文对照表为准。源文件有连写词；**Figure 1** 流程图在 TXT 中为乱码，已用论文叙述与章节号（§4.1 / §4.2 / §4.3）说明其含义。
