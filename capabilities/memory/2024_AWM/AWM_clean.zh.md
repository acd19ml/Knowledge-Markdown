# AGENT WORKFLOW MEMORY（智能体工作流记忆）

Zora Zhiruo Wang Jiayuan Mao Daniel Fried Graham Neubig  

Carnegie Mellon University Massachusetts Institute of Technology  

---

## 摘要（ABSTRACT）

尽管基于 language model 的 agent 有潜力解决 web navigation 等真实世界任务，现有方法仍难以应对具有复杂 action trajectory 的长期（long-horizon）任务。相比之下，人类能够通过从过往经验中学习可复用的任务工作流（task workflows），并用其指导未来行动，从而灵活解决复杂任务。为使 agent 也能从这一过程中受益，我们提出 **Agent Workflow Memory（AWM）**：一种用于归纳（induce）常被复用的例程——即 **workflows**——并有选择地向 agent 提供 workflows 以指导后续生成的方法。AWM 可灵活适用于 **offline** 与 **online** 两种场景：agent 可事先从 training examples 归纳 workflows，或在测试查询（test queries）到来时即时归纳。我们在两个主要的 web navigation benchmark——**Mind2Web** 与 **WebArena**——上实验，二者合计覆盖 1000+ 个任务、来自 200+ 个领域，涵盖 travel、shopping、social media 等。AWM 在 Mind2Web 与 WebArena 上分别将基线的相对成功率提高 **24.6%** 与 **51.1%**，同时减少成功求解 WebArena 任务所需的步数。此外，**online AWM** 在 cross-task、website 与 domain 评估中稳健泛化，随着 train–test task distribution gap 扩大，相对基线可提升 **8.9–14.0** 个绝对百分点。

https://github.com/zorazrw/agent-workflow-memory  

---

## 1 引言（INTRODUCTION）

基于 **language model（LM）** 的 agent 正在快速进步，现已能够处理诸如 **navigating the web**（Zhou et al., 2024; Deng et al., 2023）或操作移动应用（Rawles et al., 2023; 2024）等数字任务。当前 agent 大多通过训练（Fu et al., 2024; Murty et al., 2024）或 **in-context learning**（Zheng et al., 2024）整合一组固定的给定示例。这使它们在动作序列与这些示例相似时表现良好，但在任务上下文或环境变化时缺乏鲁棒性（Deng et al., 2023）。本质上，它们未能把握拆解日益复杂任务的关键——从相似任务与环境中抽取并学习可复用的 **task workflows**（Yu et al., 2023; Wang et al., 2024a）。此外，由于 agent 分别求解每个任务，它们不会从过去的成功与失败中学习，因而无法随时间适应（Yoran et al., 2024）。

受人类如何从经验中抽象出「从 A 到 B 的驾驶时间」等知识、并用以指导未来活动（Chi et al., 1981; 2014）的启发，我们提出 **agent workflow memory（AWM）**（§2），以在 agent 中实现类似机制。AWM 从 agent trajectory 中通过抽取可复用例程来归纳 **workflows**，随后将这些 workflows 整合进 **agent memory**，以指导未来的任务求解过程。每个 workflow 表示一个目标及其从可用 action trajectory 中提取出的共同例程，从而有效捕捉 agent 为成功解决日益复杂任务所需掌握的最核心、可复用技能。例如，图 1 展示了 AWM 在 benchmark（Zhou et al., 2024）的 WebArena **map test split** 上归纳出的 workflows。AWM 以一组基本的 **built-in actions** 为起点，以流式方式求解新任务，并从当前任务中不断归纳 workflows，例如从前几个示例中学习「**find a place by its name**」。此外，AWM 会在新经验与先前获得的 workflows 之上继续构建更复杂的 workflows。例如，一旦归纳出「**find a place by its name**」workflow，它便可作为子目标，用于构建更复杂的 workflow「**get the zip code of a place**」。这种持续学习机制会产生滚雪球效应：在扩展 agent memory 的同时归纳并应用日益复杂的 workflows，常相对不自适应的 vanilla agent 带来显著性能差距。相对基线的这一差距在 WebArena 上仅滚动数十个示例后即可高达 **22.5** 个百分点（见图 1）。

AWM 在 **annotated examples** 存在或不存在时均可运行。当某任务有高质量标注示例可用时，以 **offline** 方式运行的 AWM 可从这些规范示例中提取可复用 workflows，并整合进 memory 以辅助 **test-time inference**。即便没有标注示例，**online** AWM 也可在 **supervision-free** 设置下运行：从经 **evaluator module** 判定为正确的自生成历史预测中迭代归纳 workflows。

我们在两个 agent web navigation benchmark（§3）上评估 AWM：**WebArena** 提供严格的基于执行的评估（Zhou et al., 2024）；**Mind2Web** 强调广泛任务与领域覆盖（Deng et al., 2023）。在 WebArena 上，AWM 相对已发表的最佳自主方法（Drouin et al., 2024）在相对成功率上提高 **51.1%**，甚至超过使用人类专家撰写 workflows 增强的方法（Sodhi et al., 2023）**7.9%**。在 Mind2Web 上，AWM 在相对 **step-wise success rate** 上使 cross-task 结果有效提升 **24.6%**。

我们进一步在两个数据集上展示 AWM 的泛化能力。在 WebArena 上，我们构造 **cross-template** 子集，其中每个样本由不同 **task template** 实例化而来。AWM 仍稳定超过所有基线方法，展示其可靠的 **cross-task workflow** 适应性（§3.1）。在 Mind2Web 上，我们在 **cross-website** 与 **cross-domain** 测试划分上评估 AWM 以检验其领域泛化性，相对基线可高 **8.9–14.0** 个绝对百分点，且随着 train–test distribution gap 扩大，优势更加明显（§3.2）。两项结果均表明 AWM 在跨任务、网站与领域上具有更优泛化。

---

## 2 AGENT WORKFLOW MEMORY

本节首先描述 web navigation 任务（§2.1），再介绍 **workflow representation**（§2.2），并阐述 AWM 的机制及其多种实例化（§2.3）。

> 可把本章读成一条线——先说明网页 agent 如何工作、何谓经验；再说明 workflow 与经验有何不同、一步里包含哪些信息；最后讲 workflow 如何从经验中归纳、如何写入记忆，以及离线 / 在线两种用法。核心动机是：每个任务若都从零开始，agent 学不到过去的东西；AWM 让 agent 从已做任务中提炼可复用操作流程，写进记忆，以后碰到类似任务能做得更好。

### 2.1 问题陈述（PROBLEM STATEMENT）

> 可先在脑子里放一个具体画面——agent 要在网页上完成任务（购物、查单等）；它有一块「记忆」，起初主要是基础操作说明书（如点击、输入）。下面用符号把「观察当前页 → 结合指令与记忆决定动作 → 环境变化」的循环写清楚。

为本文起见，我们考虑具有 **language model backbone** \(L\) 与基于文本的 **memory** \(M\) 的 agent，其中基础 memory 包含 **built-in actions**（如 **CLICK** 与 **TYPE**）的文档说明。¹ 为求解由自然语言（**NL**）指令 \(q\) 指定的任务，agent 在由 **transition function** \(T\) 定义的环境中行动。对每个时间步 \(t_i\)，环境状态 \(s_i\) 给出 **observation** \(o_i\)，再传入模型以生成 **action** \(a_i\)：\(L(q, M, o_i) \to a_i\)。该 action 在环境中执行并将状态变为 \(T(s_i, a_i) \to s_{i+1}\)。这一 **observe–act loop** 反复进行，直到模型预测 **stop action** \(a_i = \texttt{STOP}\)，或达到任务终止条件（例如预先确定的最大步数）。

每个完成的任务构成一条 **experience** \(e\)，包含 NL 指令 \(q\) 与尝试求解该任务的步骤 **trajectory**；每一步 \(p\) 包含 agent 从当前状态得到的 **observation** \(o\) 与 agent 采取的 **action** \(a\)，记为 \(p = (o, a)\)。我们的目标是从过去或收集的示例构成的 **experiences** 集合 \(E = \{e\}\) 中，通过 **induction module** \(I\) 归纳有用 **workflows** \(W = \{w\}\)：\(I(E) \to W\)。我们将归纳出的 workflows 加入 agent memory \(M\)，作为后续任务求解的指导。

> 一条「经验」= 你下的自然语言指令 + 为完成它走过的整条轨迹；轨迹里每一步都是「当时看到了什么（网页状态）」和「做了什么（操作）」。论文的目标是从一堆经验里归纳出 workflow，再放进记忆里指导以后任务。

接下来介绍 workflow 表示设计、workflow 归纳方法，以及在不同设置下将 workflows 写入 agent memory 的更新方式。

¹ Memory 通常实现为 **system prompt** 或主 **prompt context** 中的辅助信息。

### 2.2 WORKFLOW 表示（WORKFLOW REPRESENTATION）

> workflow 是从一条或多条经验里提炼出的「可复用子流程」。它也有两块——用文字说明这段子流程在干什么，以及完成它要执行的一系列步骤。经验往往很具体（例如在 Amazon 搜干猫粮、点第一条、加购）；workflow 会把具体值抽象掉（例如变成「搜某个商品」），这样换猫粮、耳机都能复用同一条 workflow。

与 **experience** 类似，**workflow** 包含两部分：其一为 workflow 的文本描述 \(d\)；其二为完成该 workflow 的一系列步骤 \((p_1, p_2, \cdots)\)，见图 2。

为以 agent 能恰当学习的格式呈现 workflows，重要的是描述该系列动作的 **high-level goal**。因此，我们为每个 workflow 关联一条 NL **task description** \(d\)，本质上是对 workflow 功能的总结：通过启发式从 **experience** 指令中提取，或用 **LM** 概括（见 §2.3）。

**Workflow trajectory** 包含完成 \(d\) 所述过程的一系列步骤 \((p_1, p_2, \cdots)\)。每个 \(p\) 由三部分组成，见图 2 步骤 3：（1）当前环境状态的 NL 描述，例如「Order {id} is shown」；（2）agent 基于 observation 决定生成何种 action 的 **reasoning** 过程，例如「Order {id} is found, I will now terminate the task.」；（3）在环境上可执行的程序所表示的 **action**，例如实现终止的 `stop()`。

> 细看每一步的结构——先自然语言描述当前环境（例如订单页已显示），再写出推理（例如已找到目标订单、应结束任务），最后给出要执行的操作（例如调用终止函数）。三块一起，agent 才学得会「在什么状态下为何这么动」。

### 2.3 归纳与使用 WORKFLOWS（INDUCING AND USING WORKFLOWS）

AWM 的核心是 **induction module** \(I\)，它从一条或多条过去的 agent **experiences** \(E = \{e_i\}_{i=1}^m\) 中归纳 **workflows** 集合 \(W\)。每条 **experience** \(e = (q, P_e)\) 包含 NL 任务指令 \(q\) 与为求解 \(q\) 而采取的步骤序列（observation 与 action）\(P_e = (p_{e_1}, \ldots, p_{e_n})\)。**Workflow induction module** 以 \(E\) 为输入并产生 workflows：\(I(E) \to W = \{w\} = \{(d_j, P_{d_j})\}\)。

> 归纳模块是全文方法的心脏——输入是过去的经验集合，输出是一组 workflow；下面「基于 LM 的归纳」说明作者如何用语言模型从经验里找出可复用的共同子程序。

**基于 LM 的 workflow 归纳**  
为产生能更准确跨任务捕捉可复用 trajectory 的 workflows，我们提出基于 **LM** 的模块 \(I\)，提示 agent 从一条或多条输入 **experiences** 中提取共同 **sub-routines**。

不同于指定具体、重复度较低任务的 **task instruction**（例如「在 Amazon 购买干猫粮并配送到我的地址」），我们有意识地提示模型在更细粒度上归纳 **workflows**，即作为多条相似指令组成部分而频繁出现的子任务「在 Amazon 上搜索商品」。同时，我们不给出示例专有取值（例如「干猫粮」），而是通过抽象掉示例专有上下文来增强 workflow 的泛化性——例如在 workflow 归纳 **prompts** 中将「干猫粮」替换为更一般的名称「`{product-name}`」。这些 workflows 按模型输出中的双换行分段，并分别存入 **workflow memory**。详见 §A 中的 **offline** prompts、**online** 示例 workflows 及质量考察。²

> 归纳时作者有意抓两点——一是粒度要比「整句任务指令」更细：整句任务往往一次一景、不太重复，但里面的子步骤会在许多任务里反复出现，所以 workflow 应在子任务层面提炼。二是把示例里的具体词换成通用占位（如某商品），否则 workflow 很难泛化到新指令。

在 workflows \(W\) 被归纳后，它们被整合进 agent 作为辅助 **memory**：\(M + W \to M_w\)，其中 \(M\) 为原始 agent memory，\(M_w\) 为增强归纳 workflows 后的 agent memory。求解给定指令 \(q\) 时，agent 现在通过 \(L(q, M_w, o) = L(q, M + W, o) \to a\) 产生一系列 **actions**。下文分两种场景介绍 AWM 的使用：**offline** 用于测试 **inference**；**online** 流式处理。

> 归纳出的 workflow 会并进 agent 的记忆——原来主要是基础操作说明，现在多了一批「经验总结式」的流程。之后做新任务时，决策依据从「指令 + 基础记忆 + 当前页」变成「指令 + 基础记忆 + workflow 库 + 当前页」。下面分离线、在线两种用法。

² 我们也探索基于规则的 workflow 归纳方法，详见 §B。

**Offline 场景**  
当有额外的规范 **experiences** 可用时（例如人类标注或由模型合成），AWM 可在 **offline** 场景运行。此时我们将 workflow 归纳与使用分为两个独立过程。如图 3，AWM 首先将某网站上的全部 **training examples** 拼接为单个 **prompt** 并输入 **LM**，在「训练」时刻创建一组 workflows：\(I_{\text{offline}}(E_{\text{train}}) \to W_{\text{offline}}\)。其次，AWM 在 **inference** 时刻将全部归纳的 workflows 并入 agent memory 以求解测试指令：\(L(q, M + W_{\text{offline}}, o_{\text{test}_i}) \to a_{\text{test}_i}\)。由于 workflows 在 **test-time inference** 之前已完全归纳，agent 使用同一 **workflow memory** \(W_{\text{offline}}\) 求解每个测试项。

> 离线场景的前提是你有一批训练样本（人类示范或模型合成均可）。流程是两段式——先在训练阶段把该站点的训练数据一次性喂给模型，批量归纳出 workflow；测试阶段把这一套 workflow 全部载入记忆，agent 带着同一份库做每条测试。测试过程中记忆固定，所有测试题共用同一 workflow 库。

**Online 场景**  
额外的规范 **experiences** 并不总是可用或易于收集，尤其是覆盖与测试指令相同领域与任务的样本。AWM 也可在 **online**、**supervision-free** 设置下工作，仅需 **test queries**。**Online** AWM 以流式方式处理测试查询：在每个测试任务上运行 **inference** 之后，agent 执行「归纳—整合—使用」**workflows** 的循环。

具体地，agent 从默认 memory \(M\) 开始；给定第 \(t\) 条测试指令 \(q_t\)，agent 尝试通过生成 **action trajectory** \((p_{t_1}, p_{t_2}, \cdots)\) 来求解任务，整体构成 **experience** \(e_t = (q_t, \{p_{t_i}\})\)。我们采用 Pan et al. (2024) 的基于 **LM** 的评估模型，输出二值标签 \(L_{\text{eval}}(e_t) \in \{0,1\}\)，通过提示 **neural model** 判断 \(e_t\) 是否成功求解 \(q_t\)。若 \(e_t\) 被预测为成功（即 1），则将其转化为 **workflow(s)**：\(I(e_t) \to \{w_t\}_{\text{online}}\)，并把 \(\{w_t\}\) 加入 agent memory：\(M_t + \{w_t\} \to M_{t+1}\)，作为处理第 \(t+1\) 条指令的 agent memory。如图 4，我们对流式测试指令迭代预测 **actions** 并归纳 **workflows**，直到处理完所有测试。我们对所有测试的预测 **action trajectories** \(\{p_{t_i}\}\) 评估 **success rate** 并报告平均分。

> 在线场景没有单独的训练集，只有一串待测任务。workflow 库从空开始，按任务顺序做：每做完一条，用 LM 评估器判成败；成功就从这次轨迹归纳 workflow 写入记忆，失败就不写。记忆随任务推进越来越厚，后面的题能借前面成功积累的光。

> 离线要额外标注或可信的训练轨迹，但样本往往经过检验，workflow 质量相对可控。在线零标注，但完全依赖评估器——若把失败判成成功，错误流程会进记忆，可能拖累后续任务。读实验时可带着这条对照看 WebArena / Mind2Web 的设置差异。

---

## 3 实验（EXPERIMENTS）

本节在两个主要 web navigation benchmark——WebArena（§3.1）与 Mind2Web（§3.2）上实验。对每个 benchmark，我们先介绍 benchmark 与表现最好的基线方法，再给出我们的 AWM 方法，并展示其在多种设置下取得更优任务成功与泛化的能力。

> 两个评测集考察的都是同一件事——agent 能否在真实网页上完成人类给出的自然语言指令——但侧重点和评估方式不同。下文分节读即可。

对两个 benchmark，我们按 **website** 粒度运行 AWM。换言之，我们按关联网站对示例分组，并分别在每组上运行 AWM。该机制维持规模较小但与测试任务仍相关的 **workflows** 集合。

> 按网站分组跑 AWM：购物站归纳的 workflow 主要服务购物站，论坛站服务论坛站。这样每组 workflow 数量可控，又与当前站点任务高度相关。

### 3.1 WEBARENA

WebArena（Zhou et al., 2024）在五个网站上提供 812 个 web navigation 任务，覆盖四个常见应用领域：**e-commerce**、**social forum** 讨论、协作 **software development** 与 **content management**。最重要的是，WebArena 支持对 agent trajectory **functional correctness** 的严格评估。

> 812 个任务分布在五个网站上；评估重点不是「操作像不像参考答案」，而是最终结果在功能上是否正确，因此比「形似」更严。

我们采用当前 **state-of-the-art**、且不使用人类标注的站点专有知识的 **BrowserGym**（Drouin et al., 2024），该方法改变了 agent 默认 **action space**。我们采用 BrowserGym 框架及其默认 **action space**，并按 Zhou et al. (2024) 的环境表示，使用 **accessibility trees** 表示网页。由于 BrowserGym 同时输入网页 **HTML** 与 **accessibility tree** 表示，为与我们的方法公平比较，我们也运行仅使用 **accessibility tree** 网页表示的 BrowserGym 版本，记为 **BrowserGym\(_{\text{ax-tree}}\)**。我们还与 **SteP** 方法（Sodhi et al., 2023）比较，该方法使用 14 条人类专家为求解 WebArena 撰写的 **workflows**。相比之下，我们的方法不使用人类监督，也不针对 WebArena 设置定制。

> 基线可粗分三类来记：**BrowserGym** 是当时不用人类站点知识的自主方法里很强的；**AutoEval** 会在轨迹生成后再做评估与修正，步数往往更多；**SteP** 用人类专家手写的 14 条 workflow，相当于有人类经验加持的对照。

**表 1**：在 WebArena 上使用 **gpt-4** 的 **task success rate**，以及五个 **website split** 上的分数分解。

| Method | Total SR | Shopping | CMS | Reddit | GitLab | Maps | #Steps |
|--------|----------|----------|-----|--------|--------|------|--------|
| *With human engineered workflows* |
| *SteP (Sodhi et al., 2023)* | 33.0 | 37.0 | 24.0 | 59.0 | 32.0 | 30.0 | - |
| *Autonomous agent only* |
| WebArena (Zhou et al., 2024) | 14.9 | 14.0 | 11.0 | 6.0 | 15.0 | 16.0 | - |
| AutoEval (Pan et al., 2024) | 20.2 | 25.5 | 18.1 | 25.4 | 28.6 | 31.9 | 46.7 |
| BrowserGym (Drouin et al., 2024) | 23.5 | - | - | - | - | - | - |
| BrowserGym\(_{\text{ax-tree}}\) | 15.0 | 17.2 | 14.8 | 20.2 | 19.0 | 25.5 | 7.9 |
| **AWM (OURS)** | **35.5** | 30.8 | 29.1 | 50.9 | 31.8 | 43.3 | 5.9 |

遵循基线方法，我们使用 **GPT-4（gpt-4-0613）**，**temperature** 为 **0.0**，以保证模型输出大体稳定。由于 WebArena 仅有测试示例且不存在额外高质量、与领域对齐的示例，我们仅按 §2.3 在 **online** 设置下运行 AWM。

> WebArena 没有可用作归纳的规范训练集，因此这里只能采用 **Online** 模式：从空 workflow 库开始，边完成测试任务边积累 workflow。

#### 3.1.1 主要结果（MAIN RESULTS）

> 读表 1 时别把绝对成功率单独当「高不高」：总体约 **35.5%** 放在开放网页任务里并不夸张，关键是对比——相对 BrowserGym 约 **23.5%** 高出约 **12** 个绝对百分点、相对提升超过 **50%**；且仍超过人类手写 workflow 的 **SteP（33.0%）**，说明模型从经验里归纳的 workflow 可以压过人工规则。

如表 1 所示，我们的 AWM 在 WebArena 上取得已发表最佳结果，相对 BrowserGym 基线在总体成功率上绝对提升 **12.0** 个百分点、相对提升 **51.1%**。值得注意的是，AWM 也超过使用人类撰写的、强领域监督的 SteP，总体成功率相对提升 **7.6%**。按五个网站分解，我们的 AWM 方法相对 BrowserGym 基线在各网站上均显著提升 agent 性能（**11.8–30.7** 个绝对百分点），表明其在不同领域与任务上的广泛适用性。

> 分站点看，提升分布在 **11.8–30.7** 个百分点之间，说明收益不是只来自某一个网站类型，而是多处站点都成立。

除任务成功外，我们还评估 agent 求解任务所需的平均步数，见表 1 最右列。AWM 每个示例比 BrowserGym 基线约少 **2.0** 步。进一步与需要额外评估与修正步骤才能正确求解任务的 **AutoEval**（Pan et al., 2024）相比，我们的 AWM 平均少用 **40.8** 步。两项比较均表明 AWM 在保持 **efficient trajectories** 的同时获得高成功率。

> 效率上：AWM 平均步数约 **5.9**，比 BrowserGym 少约 **2** 步，比 **AutoEval** 少约 **41** 步——不仅更常做对，轨迹也更短。

#### 3.1.2 小数据高效学习（EFFICIENT LEARNING FROM SMALL AMOUNTS OF DATA）

为展示 **online** AWM 的行为，我们给出 **online evaluation** 过程中 **cumulative success rate** 的曲线：对前 \(k\) 个已完成示例评估平均成功率。

如图 5，agent 在初期（约 **0–40** 个示例之间）呈现快速学习曲线：通过获得最关键的 **workflows** 而提高成功率。之后，agent 学习更高级的 **workflows**（图 1），而成功率逐渐稳定到学习早期阶段的最高点。这展示了 AWM 的高效学习过程：仅凭数十个示例即可显著提升性能。

> 学习曲线直觉：前几十个任务成功率爬升最快，对应「最关键、最常用」的 workflow 被收进记忆；后面还在学更复杂的 workflow，但曲线趋于平台，边际收益变小。整体印象是**小样本就能拿到大部分增益**。

#### 3.1.3 CROSS-TEMPLATE WORKFLOW 泛化

由于 benchmark 构建过程会从单一底层 **task template** 实例化多个示例，WebArena 中部分任务的 **canonical trajectories** 高度重叠。直观上，AWM 会提高 **in-template** 成功率——即给定从某成功示例归纳的一条 **workflow**，理论上更容易求解由同一 **task template** 生成的所有其他示例。

> 这里要警惕一种质疑：任务由**模板**实例化而来，AWM 的提升会不会主要来自「在同一模板内套娃」——从 A 任务学到的 workflow 刚好能帮到同模板的 B、C？若如此，跨任务的含金量就弱了。

为确认 AWM 的收益不仅来自学习仅在模板内有帮助的 **workflows**，并检验 AWM 是否能在 **cross-template**（≈ **cross-task** 应用）场景下受益，我们从 **non-overlapping templates** 来源抽取 WebArena 子集：按 **template** 对示例分组，并从每个 **template** 组中随机选取一条示例。我们在该 **cross-template** 子集上运行 AWM。

> 子集构造的含义是：**每个模板只留一条任务**，于是子集中任意两条任务不会共享同一底层模板——从一个任务学来的 workflow 无法靠「同模板复制」直接套到另一条上，从而更干净地检验跨类型泛化。

**表 2**：WebArena **cross-template** 子集上的 **task success rate** 及每个 **website split** 的分解。名称下标注各 **website split** 的示例数。

| Method | Total SR | Shopping (51) | CMS (45) | Reddit (24) | GitLab (45) | Maps (32) |
|--------|----------|---------------|----------|-------------|-------------|-----------|
| *With human engineered workflows* |
| *SteP (Sodhi et al., 2023)* | 32.1 | 26.5 | 29.3 | 52.2 | 27.3 | 36.4 |
| *Autonomous agent only* |
| AutoEval (Pan et al., 2024) | 23.2 | 12.2 | 17.1 | 21.7 | 31.8 | 36.4 |
| BrowserGym\(_{\text{ax-tree}}\) | 20.5 | 10.4 | 17.8 | 23.1 | 27.3 | 28.6 |
| **AWM (OURS)** | **33.2** | 24.5 | 29.3 | 52.2 | 31.8 | 39.4 |

如表 2 所示，AWM 仍在所有 **website split** 上取得最高总体表现。

这些结果表明，AWM 归纳的 **workflows** 不仅在长程定位等场景有效，且能跨由不同 **task template** 实例化的任务（即 **cross-template** / **cross-task**）发挥作用，例如从「在地图上显示某地点」到「获取某地点邮编」等更复杂 **workflows** 的构建。

> 表 2 上 AWM 总体仍最高（**33.2%**），且仍高于 SteP（**32.1%**），说明在更严的 cross-template 设定下优势还在，不是只靠模板内捷径。

为更直观展示 AWM 的 **cross-template** 泛化以及构建日益复杂 **workflows** 的能力（如图 1 所示），我们进行 **case study** 以说明其背后的 workflow 机制。见图 6：AWM 随时间通过过去示例与更早的 **workflows** 学习，构建日益复杂的 **workflows**。

如图 6 所示，agent 在 **online** 过程早期通过总结过去示例创建并学习「**Find a place by its name**」**workflow**。随后，当遇到进一步要求获取地点 **zip code** 的示例时，AWM agent 学习先遵循已有 **workflow** 执行前几步以查找地点，再执行进一步步骤以获取所找到地点的 **zip code**。将这些新步骤叠加在朴素的找地点任务之上，agent 成功构建更复杂的 **workflow**，即「**get the zip code of a place**」。

> 案例可以这样理解：先学会「按名字找地点」；遇到「查某地邮编」时，前几步复用已有子流程，只在后面追加取邮编的步骤——简单 workflow 像积木一样叠成更复杂的 workflow，而不是彼此孤立。

### 3.2 MIND2WEB

Mind2Web（Deng et al., 2023）在 **cross-task**、**website** 与 **domain** 设置下考察 web navigation，强调 agent 在多样操作与环境上的泛化性。Mind2Web 中每个任务有固定步数；每步 agent 需预测 **action**，并按以下指标评估：（1）**element accuracy**：是否选中正确页面元素；（2）**action F₁**：在该元素上采取的 **action** 是否正确；综合（1）与（2）得到（3）**step success rate**：当前步元素与 **action** 选择是否均正确。最后，完成给定任务的全部步骤后，（4）**task-level success rate** 衡量该任务所有中间步骤是否均成功，即该任务在指标（3）下所有步均为 1。

> Mind2Web 与 WebArena 的侧重点不同：这里显式拆成**跨任务、跨网站、跨领域**三档由易到难的泛化测试（例如同领域从苹果官网到百思买，或从电商跳到社交媒体）。评估是**逐步**的——每步既要选对元素，又要操作对，再合成步级与任务级成功率。

由于 Mind2Web 提供覆盖部分测试网站的 **training set**（**cross-task split**），我们既探索从 **training set** 归纳 **workflows** 并应用于测试集的 **offline** 设置，也探索在测试查询上流式进行 workflow 归纳与 **inference** 的 **online** 设置（§2.3）。由于我们关注仅接受文本输入的基于 **LM** 的 agent，将 AWM 与两种 **state-of-the-art** 方法比较：**MindAct**（Deng et al., 2023）与 **Synapse**（Zheng et al., 2024）。MindAct 引入网页元素过滤与 **multi-choice** 任务格式以简化 **observation** 处理；Synapse 将格式改为 **trajectory** 风格并增强检索到的相关示例。我们整合两种方法中的元素过滤，并用 **workflows** 替代 Synapse 中检索到的示例，以验证可复用 **workflows** 相对具体示例的优越性。为与所有基线公平比较，我们对 **gpt-3.5-turbo** 与 **gpt-4** 均以 **temperature 0.0** 运行 AWM。**Neural workflow** 归纳与 agent **action** 生成使用同一模型。

> 因为有训练集，Mind2Web 上可以同时报告 **Offline**（从训练归纳再测）与 **Online**（只在测试流上归纳）两条线，和 WebArena 的设定形成对照。

#### 3.2.1 主要结果（MAIN RESULTS）

我们先用两种 **GPT** 变体 **offline** 运行 AWM，发现 AWM 在 **step** 与 **task** 层面均稳定取得最高 **success rate**，相对基线在 **step-wise** 与 **task-wise success rate** 上分别有 **4.0–8.9%** 相对提升与 **0.4–2.8** 个绝对百分点提升——优于使用 **gpt-3.5-turbo** 的 Synapse 与使用 **gpt-4** 的 MindAct。将 **step success rate** 按元素与 **action** 选择及准确度分解后，提升主要来自更准确的元素选择，如表 3 中 **5.0–9.0** 的 **element accuracy** 提升所示。

> **Offline、跨任务**这一块的读法：表上领先主要来自**元素选得更准**（相对 Synapse 约 **+5** 个点的元素准确率、相对 MindAct 在 **gpt-4** 上约 **+9** 个点量级，见正文数字）。任务级成功率整体仍低，要和数据难度一起理解。

**表 3**：AWM **offline** 在 Mind2Web **cross-task** 数据集上的结果。**Elem Acc** 与 **SR** 分别为 **element accuracy** 与 **success rate** 的缩写。脚注标明各方法使用的 **GPT** 变体：**3.5** 与 **4** 分别表示 **gpt-3.5-turbo** 与 **gpt-4**。同模型变体内最优结果加粗标出。

| Method | Elem Acc | Action F₁ | Step SR | SR |
|--------|----------|-----------|---------|-----|
| MindAct | 3.5: 20.3 | 56.6 | 17.4 | 0.8 |
| CogAgent 3.5 | - | - | 18.6 | - |
| Synapse 3.5 | 34.0 | - | 30.6 | 2.4 |
| AWM 3.5 | 39.0 | 52.8 | 34.6 | 2.8 |
| MindAct 4 | 41.6 | 60.6 | 36.2 | 2.0 |
| AWM 4 | **50.6** | 57.3 | **45.1** | **4.8** |

**抽象子例程 vs. 具体经验**  
更具体地，相对检索最相关 **training examples** 的 Synapse（Zheng et al., 2024），AWM 的 **element accuracy** 高 **+5.0**，**step success rate** 高 **+4.0**。虽然增强完整、具体的示例可能使 agent 偏向选择与给定示例中相似元素，AWM 通过 **workflows** 中对示例专有上下文的抽象表示，在元素选择上引入更少偏差，因而 **step success rate** 更高。

此外，AWM 整合频繁使用的 **sub-routines**，相对 Synapse 使用的完整示例 **trajectories**，可更灵活、更易在测试示例间复用（完整轨迹较少多次出现）。总体而言，我们的结果表明 **workflows** 的抽象、可复用性质有助于 AWM 的优越性。

> **Synapse** 检索整条训练示例当参考，示例里塞满只适用于那一条任务的细节（特定商品名、特定按钮位置），模型容易「照着长得像的元素瞎选」。**Workflow** 把细节抽象成操作逻辑，偏差更小，所以元素准确率往往更好。

**学会偏离 workflow 指引**  
尽管元素选择更准确，AWM 的 **action F₁** 略低于 MindAct，可能是因为增强的 **workflows** 会引导 agent 采取与 **workflows** 对齐的某些 **actions**，而这些并不总与当前环境状态相关。虽然遵循 **workflows** 通常带来更成功的任务 **trajectories**，agent 在识别何时应偏离 **workflow** 指引方面仍面临一些挑战。

> **Action F₁** 略逊可以理解为：workflow 有时会**过度引导**——按流程走了一步，但当前页面状态下其实不该这么走。短板在「何时该偏离 workflow」而不是「会不会跟流程」。

#### 3.2.2 ONLINE AWM 促进泛化

除 **offline** 归纳设置外，我们进一步在 **online** 设置探索 AWM，类似 §3.1 的 WebArena 实验：除 **test queries** 外无需额外 **training examples**。这自然有利于 **cross-website** 与 **cross-domain** 泛化；我们在 Mind2Web 数据集提供的另两个划分上检验：**cross-website** 与 **cross-domain** 测试。

除 MindAct 基线外，我们还用 AWM 设置构造对比：**offline** 随机选取从 **training set** 归纳的 **workflows** 作为 **memory** 增强。具体地，对 **cross-website** 示例，我们从同一 **domain** 选取 **workflows**；对 **cross-domain** 设置，我们从所有 **domain** 随机选取 **workflows**。我们通过在测试 **inference** 上迭代归纳、整合并使用 **workflows** 来运行 **online** AWM。我们还在 §C 探索 **AWM offline+online**。

**表 4**：在 Mind2Web **cross-task**、**cross-website** 与 **cross-domain** 泛化测试上的成功率，使用 **gpt-4** 模型。**EA** 为 **element accuracy** 缩写，**AF₁** 为 **action F₁** 缩写。

| Method | Cross-Task EA | AF₁ | Step SR | SR | Cross-Website EA | AF₁ | Step SR | SR | Cross-Domain EA | AF₁ | Step SR | SR |
|--------|---------------|-----|---------|-----|------------------|-----|---------|-----|-----------------|-----|---------|-----|
| MindAct* | 41.6 | 60.6 | 36.2 | 2.0 | 35.8 | 51.1 | 30.1 | 2.0 | 21.6 | 52.8 | 18.6 | 1.0 |
| AWM offline | 50.6 | 57.3 | 45.1 | 4.8 | 41.4 | 46.2 | 33.7 | 2.3 | 36.4 | 41.6 | 32.6 | 0.7 |
| AWM online | 50.0 | 56.4 | 43.6 | 4.0 | 42.1 | 45.1 | 33.9 | 1.6 | 40.9 | 46.3 | 35.5 | 1.7 |

如表 4 所示，**online** AWM 与 **offline** AWM 均大幅超过 MindAct 基线，在 **cross-task**、**cross-website** 与 **cross-domain** 场景下 **step success rate** 分别绝对提升 **7.4–8.9**、**3.6–3.8** 与 **14.0–16.9** 个百分点。

**域内 cross-task 场景**  
在域内测试时，**online** AWM 与 **offline** AWM 表现相近。细查模型行为时，我们注意到各自利弊。**online** AWM 从模型预测的 **trajectories** 归纳 **workflows**，而这些预测并不总正确，因而可能产生错误 **workflows** 并损害性能。另一方面，某些网站上的 **training** 与 **test** 示例在任务分布上差异较大（例如 **training** 覆盖如何在 Amazon 购物，**test** 要求向 Amazon careers 投递职位申请）。**online** AWM 自然缓解这种 train–test gap，因为其运行过程仅涉及 **test queries** 与环境，因而产生的 **workflows** 更针对测试分布，整体 **success rate** 更高。尽管如此，若存在分布匹配、高质量的 **training examples**，**offline** AWM 可通过缓解差距问题带来更多收益，如表 4 中略高的 **cross-task** 分数所示。

> **跨任务**这一档里，Online 与 Offline 互有长短：Online 的 workflow 来自模型自己的轨迹，轨迹有错就会**脏数据进记忆**；Offline 受 **train–test 分布差**拖累——训练教的是「怎么购物」，测试可能是「去招聘页投简历」，从训练归纳的 workflow 就对不上。分布对齐、训练质量高时 Offline 往往在 cross-task 上略占上风（见表 4）。

**扩展到未见网站与领域**  
应用于未见 **website** 或 **domain** 时，**online** AWM 相比 **offline** AWM 展现更强泛化。**online** 相对 **offline** 的优势幅度随 **training** 与 **testing** 数据之间的 **domain gap** 扩大而增大：从跨不同网站（例如 apple 到 bestbuy）到跨不同 **domain**（例如 shopping 的 macys 到 social media 的 reddit）。由于 **online** AWM 不需要也不依赖 **training data** 的信息，它不受任何 **domain gap** 影响。尽管如此，如 **offline** AWM 相对 MindAct 基线的显著提升所示，**offline** AWM 仍表明模型可从先前归纳的、机制上相似的 **workflow** 库中受益。

> **跨网站、跨领域**时 Online 优势更明显：gap 越大，从训练集借来的 workflow 越可能不对路，而 Online 的 workflow 全在测试环境里长出来，不依赖训练分布。即便如此，Offline 相对纯 MindAct 仍常有大幅提升——不同领域里「搜索、筛选、提交」等子逻辑仍有相通之处，库未必同域也完全没用。

> **实验部分可收束为五条**：一是两数据集上相对基线都强，甚至压过人类手写 workflow 的设定；二是少量任务就能学到大部分增益；三是跨模板、跨站、跨域都有证据；四是 Offline 适合有高质量且分布匹配的训练数据，Online 适合无训练或领域差大；五是「何时偏离 workflow」仍是弱点，尚有改进空间。

---

## 4 探索最优 WORKFLOW 表示（EXPLORING OPTIMAL WORKFLOW REPRESENTATIONS）

本节实验其他可能选项以更好表示 **workflows**。具体地，我们对 **sub-routine**、抽象格式的 **workflows** 做消融（§4.1）；探索描述性文本中的 **workflows**（§4.2）；最后，在默认用 NL 描述环境状态的 **workflows** 之外，比较在 **workflow** 步骤中用网站 **HTML** 增强 **observation**（§4.3）。

> 前面已经说明 AWM 整体有效，这一节要追问的是：**workflow 具体怎么写、怎么表示**，对最终效果影响有多大。下面分三个角度做对照——归纳方式（规则 vs 语言模型）、动作写法（代码 vs 口语）、环境信息（自然语言 vs HTML）。

### 4.1 SUB-ROUTINE、抽象格式贡献多少？（HOW MUCH DOES THE SUB-ROUTINE, ABSTRACT FORMAT CONTRIBUTE?）

本节将我们用 **LM** 的抽象、基于 **sub-routine** 的归纳方法与无上下文与 **sub-routine** 抽象的规则方法比较。

具体地，我们的规则归纳 \(I_{\text{rule}}\) 先提取每条 **experience** 的 **action sequence**（例如 **CLICK → CLICK → TYPE**），再按 **action sequence** 对 **experiences** 去重。在每个唯一的 **experience** 中，我们移除无法在环境中执行的步骤。将这些唯一且验证过的 **experiences** 作为 **workflows**。更细描述见 §B。

> 规则基线的直觉可以概括为：**不做抽象**。它先抽出每条经验的操作序列模式，按模式去重后删掉环境里执行不了的步，把**去重、清洗过的整条经验**当作 workflow。语言模型则会把具体值换成占位符，并把长轨迹拆成更细、可复用的子程序——两者差在「抽象与子程序化」而不只是「去重」。

**WebArena 结果**  
如表 5，基于规则与基于 **LM** 的 workflow 归纳表现接近，成功率差距仅 **0.1**；**LM** 方法似乎更高效，平均少用 **0.4** 步。人工分析发现 **LM** 归纳模块 \(I_{\text{lm}}\) 产生的 **workflows** 粒度更细，避免 agent 跟随有时出现在规则归纳 **workflows** 中的不必要步骤，从而使求解过程略更高效。

> WebArena 上两种归纳成功率几乎一样（只差 **0.1** 个百分点），但 LM 路线平均少 **0.4** 步——细粒度 workflow 少带冗余步，跑起来更短、更顺。

**表 5**：在 WebArena 上使用 **gpt-4** 的 AWM 成功率，规则与 **LM** 归纳。

| Method | Total SR | #Steps |
|--------|----------|--------|
| AWM\(_{\text{rule}}\) | 35.6 | 6.3 |
| AWM\(_{\text{lm}}\) | 35.5 | 5.9 |

**Mind2Web 结果**  
如表 6，相对 **AWM\(_{\text{rule}}\)**，**AWM\(_{\text{lm}}\)** 提升 **2.8** 个幅度。虽然增强完整具体示例可能使 agent 偏向选择与给定示例相似元素，**AWM\(_{\text{lm}}\)** 通过 **workflows** 中对示例专有上下文的抽象表示，在元素选择上引入更少偏差。

**表 6**：Mind2Web **cross-task** 数据集上不同 workflow 归纳方法的 AWM 结果。

| Method | Elem Acc | Action F₁ | Step SR | SR |
|--------|----------|-----------|---------|-----|
| MindAct | 41.6 | 60.6 | 36.2 | 2.0 |
| AWM 4,rule | 49.5 | 57.0 | 43.4 | 2.0 |
| AWM 4,lm | **50.6** | 57.3 | **45.1** | **4.8** |

此外，**AWM\(_{\text{lm}}\)** 使用频繁出现的 **sub-routines**，相对 **AWM\(_{\text{rule}}\)** 归纳的完整示例 **trajectories**（较少多次出现），可更灵活地用于测试示例。总体而言，我们的结果表明 **workflows** 的抽象、可复用性质有助于 **AWM\(_{\text{lm}}\)** 方法的有效性。

> Mind2Web 上差距就拉开了：LM 归纳在步级成功率上高约 **1.7** 个百分点，任务级高约 **2.8** 个百分点。原因与前面直觉一致——规则保留的是**完整、具体**的经验，示例专有细节会误导元素选择；LM 抽象掉这些细节，并抽出**频繁子程序**，整条轨迹很少重复出现，但子步骤会。小结：**抽象与泛化**在需要跨任务迁移的场景（Mind2Web）尤其重要；在**同站点、任务较同质**的设定（WebArena）里，规则也能追近 LM 的成功率。

### 4.2 描述性文本中的 WORKFLOWS（WORKFLOWS IN DESCRIPTIVE TEXTS）

AWM 以程序格式表示 **workflow** 步骤。本节与文本格式 **workflows** 比较，以理解文本与代码何者更适合 **agent memory**。

> 要问的是：动作步骤维持程序写法（如 `CLICK({submit-id})`），还是改成口语（如「点击提交按钮」）？下面用 **gpt-3.5-turbo** 把已有 workflow 里的**代码动作逐条口语化**，环境与推理部分保持不变，再对表。

更具体地，我们提示 **gpt-3.5-turbo** 将早期实验中归纳的 **workflows** 中的 **action trajectory** 口语化。例如，从 **action** `CLICK({submit-id})`，其口语化 NL 表示类似「CLICK the submit button」。我们在这些文本 **actions** 中使用与代码 **actions** 相同的文本 **observation** 与 **thoughts**。

由表 7 结果，**AWM\(_{\text{text}}\)** 的 **element selection accuracy** 与 **step success rate** 分别略高 **0.6** 与 **0.3** 个百分点，但 **task success rate** 下降 **1.2**。总体而言，我们未发现文本与代码格式 **workflows** 之间的显著性能差异，表明两种形式均可有效增强 **agent memory**。

> 表 7 上元素准确率、步级成功率各浮零点几个百分点，任务级反而略低 **1.2** 个百分点，总体谈不上谁碾压谁。**workflow 的价值主要在操作逻辑和抽象结构**，表示成代码还是自然语言是次要问题。

**表 7**：使用代码与文本 **workflows** 的 Mind2Web **cross-task** 结果。

| Method | Elem Acc | Action F₁ | Step SR | SR |
|--------|----------|-----------|---------|-----|
| MindAct | 41.6 | 60.6 | 36.2 | 2.0 |
| AWM | 50.6 | 57.3 | 45.1 | 4.8 |
| AWM\(_{\text{text}}\) | 51.2 | 57.4 | 45.4 | 3.6 |

### 4.3 WORKFLOWS 中的环境抽象（ENVIRONMENT ABSTRACTION IN WORKFLOWS）

AWM 用 NL 描述中间网页状态，但展示具体状态可能有助于更好将 agent **ground** 到环境。由于网页完整 **HTML** 可能过长，我们使用 Deng et al. (2023) 的 **relevance predictor** 过滤网页表示，并为每个 **workflow** 步骤仅增强被预测为相关的元素的简短 **HTML**。我们运行 **gpt-3.5-turbo**，分别仅描述、仅 **HTML**、以及两种内容兼有。

> 每一步里先写「当前环境长什么样」——默认用一句自然语言概括；也可以换成**网页 HTML 片段**帮模型对准元素，但整页 HTML 太长，所以只保留被模型判为相关的一小段。实验对比三种：纯 NL、纯过滤 HTML、两者一起。

如表 8，状态的 NL 描述比 **HTML** 更有用：用 **HTML** 替换 NL 使 **step success rate** 略降 **0.8**。有趣的是，同时使用 NL 与过滤 **HTML** 结果更差。我们推测原因有二：其一，同时加入 NL 与 **HTML** 显著增加 **context length**，使模型更难正确处理；其二，过滤后的 **HTML** 仍含大量无关项（**47%** 的情况遗漏所有正确元素），可能与 NL 描述矛盾并损害 agent 能力。

> 结果上：**只用自然语言最好**；单用 HTML 步级成功率约降 **0.8** 个百分点；**两者叠用最差**，比纯 NL 再低约 **1.7** 个百分点。原因一是上下文变长、信噪比变差；二是过滤器不可靠，近一半情形会把正确元素全漏掉，HTML 里又夹杂无关噪声，还可能和 NL 描述矛盾。结论与 §4.1 同一条线：**抽象、简洁**往往比堆具体 HTML 更稳；细节过多反而伤。

**表 8**：使用 **GPT-3.5-turbo** 与不同环境表示的 Mind2Web 结果。

| Desc. | HTML | Elem Acc | Act F₁ | Step SR | SR |
|-------|------|----------|--------|---------|-----|
| ✓ | ✗ | 39.0 | 52.8 | 34.6 | 2.8 |
| ✗ | ✓ | 38.1 | 54.0 | 33.8 | 2.8 |
| ✓ | ✓ | 37.1 | 51.3 | 32.9 | 2.0 |

---

## 5 在上下文与在动作中探索 WORKFLOW 利用（EXPLORING WORKFLOW UTILIZATION IN CONTEXT AND IN ACTION）

> 此前 workflow 都只作为**记忆写进上下文**，决策时当参考书翻。这一节试另一条路：把 workflow **升格成可调用的「高层动作」**——像给只有点击、打字的人加一排快捷键，按「登录」就自动跑完一串原子操作，而不只是记在脑子里。

除将 **workflows** 整合为 **agent memory** 外，我们还探索通过扩展 **agent action space** 来使用 **workflows**，记为 **AWM\(_{\text{AS}}\)**。我们利用 **workflows** 的程序性质，将每个 **workflow** 包装为高层 **function**，类似 agent 可调用的快捷工具以执行预定的一系列 **actions**（Wang et al., 2024b）。形式化地，agent 初始配备默认的原始 **actions** \(P\)（例如 **click**、**type**），**AWM\(_{\text{AS}}\)** 将归纳的 **workflow actions** \(W\)（例如 **find place**、**get place zipcode**）加入其 **action space**。

每步 agent 可调用原始 **action** 或 **workflow action**。调用原始 **action** 时，agent 立即执行该 **action**。调用 **workflow action** 时，将触发 **workflow** 中预定的步骤序列。例如，调用 **workflow action** `login(username, password)` 将顺序执行 `click(box1-id) → type(box1-id, username) → click(box2-id) → type(box2-id, password) → click(submit-id)`。当所有中间原始 **actions** 完成时，**workflow action** 即告完成。

> 实现上就是把每个 workflow 包成一个函数：每一步模型要么选**原子动作**，要么选某个 **workflow 动作**；一旦选中后者，就按预定顺序把中间原子步**自动跑完**，中间不再由模型逐步决策。

**表 9**：除 **memory** 增强外还改变 **action space** 的 AWM 变体在 Mind2Web 上的结果。所有方法使用 **gpt-4**。

| Method | Elem Acc | Action F₁ | Step SR | SR |
|--------|----------|-----------|---------|-----|
| MindAct | 41.6 | 60.6 | 36.2 | 2.0 |
| AWM | 50.6 | 57.3 | 45.1 | 4.8 |
| AWM\(_{\text{AS}}\) | 51.8 | 56.7 | 46.4 | 3.6 |

在表 9 中，用 **workflows** 扩展 **agent action space**（**AWM\(_{\text{AS}}\)**）使 **step success rate** 略升 **1.3** 个百分点，总体 **task success rate** 与仅 **memory** 增强的基础 AWM 相同（**3.2**）。我们分析 agent 预测，发现其仅在 **18.5%** 的任务中调用 **workflow actions**，表明当前 agent 对使用新加入 **actions** 存在阻力。总体而言，用 **workflows** 扩展 **actions** 似乎强化 **memory** 中的 **workflows**，并作为辅助 **actions** 带来小幅额外收益。

> 数字上：步级成功率略涨 **1.3** 个百分点；任务级成功率并未因多一种用法而明显抬高（表 9 中可与仅记忆增强的 AWM 对照）。更关键的是**调用率**——只有约 **18.5%** 的任务真的去调了 workflow 动作，多数时候仍一步一步点，说明模型对「新加的高层工具」有惰性或不习惯。

然而，**workflow actions** 并不总导致任务成功。图 7 展示一个代表性示例：预订航班时用户常输入城市名如「New York」，而系统常弹出附近机场以支持下一步搜索。虽然可以归纳 **book flight** **workflow** 通过预定 **action sequence** 输入全部所需数据，但选择弹出机场这一 **action** 在未看到含可用弹出选项的中间状态的情况下执行，灵活性不足。授予实时状态访问或动态执行循环等更高级技术有望解决该问题，我们鼓励未来工作在 **AWM** 框架下探索这些方向。

> 更深一层的限制是 **workflow 动作近似盲执行**：一旦调用，就按固定脚本从头跑到尾，**中间不根据当前页面重规划**。订机票时输入「New York」后页面常弹出机场列表，脚本里的下一步却可能假设没有弹层——模型在宏展开时看不到实时 DOM，就会走错。要改进，需要让宏执行中能读状态、或引入条件与循环，论文把这类设计留给以后。

> 小结：把 workflow 做成可调用动作**方向合理**，等于用快捷键再强化一遍记忆中的流程，但现实现受「盲执行」和「很少主动调用」两头卡着，额外收益有限；要变大，得改执行语义并降低模型对工具的抗拒。

---

## 6 相关工作（RELATED WORK）

**Web Agent Benchmarks**  
首个现代且广泛使用的 web agent benchmark 是 Shi et al. (2017) 的 **MiniWob**，评估航班预订等多种场景。(Liu et al., 2018) 随后创建 **MiniWob++** 并增加挑战。更近地，**WebShop**（Yao et al., 2022）提供模拟电商网站与众包文本指令。**WebArena**（Zhou et al., 2024）整合更多网站并支持现实的基于执行的评估；**VisualWebArena**（Koh et al., 2024）扩展到需要视觉输入的任务。**Mind2Web**（Deng et al., 2023）提出多样任务并强调 agent 跨网站与领域的泛化。我们使用 WebArena 与 Mind2Web 评估方法的任务成功与泛化性。

**增强复杂任务中的 Agent**  
许多工作通过修改 **action space** 改进 agent，例如约束 **action** 搜索空间（Liu et al., 2018）、使 **LM** 自反馈以修正预测 **actions**（Sun et al., 2023），或为特定任务加入人类设计的 **actions**（Sodhi et al., 2023）。其他工作探索增强 **agent memory**，例如在上下文中加入示例演示（Haluptzok et al., 2023; Zheng et al., 2024; Fu et al., 2024）。然而高质量示例并不总是可用或易于收集。我们的 AWM 可在辅助示例不存在、仅有 **test queries** 时仍灵活运行。

**从经验学习常见程序**  
部分工作将完整示例（Zheng et al., 2024）作为 agent 上下文，但它们与示例专有上下文纠缠，在推广到其他任务或领域时面临挑战（Majumder et al., 2023）。许多工作提出用基于规则（Ellis et al., 2023; Bowers et al., 2023; Grand et al., 2023）或基于 **LM**（Cai et al., 2023; Wang et al., 2024c; 2024a）的方法从经验中提取频繁复用的 **sub-routines**，并作为辅助 **skills** 以简化未来任务求解（Oh et al., 2017; Liang et al., 2023; Yu et al., 2023; Mao et al., 2023）。我们探索了基于规则与基于 **LM** 的方法以归纳可复用 **workflows**，并灵活将其用作无环境 **grounding** 问题的上下文指导。

---

## 7 结论（CONCLUSION）

我们提出 **agent workflow memory**，从可用示例 **offline** 归纳、增强并使用 **workflows**，或纯 **online** 在 **inference** 时进行。我们在 WebArena 与 Mind2Web 上评估 AWM，**task success rate** 相对提升 **24.6%** 与 **51.1%**。AWM 还展示在跨任务、网站与领域上的优越泛化能力。我们希望 AWM 能为动态 **memory** 构建与多样化数字任务上的 agent 适应提供洞见并推动进展。

---

## 致谢（ACKNOWLEDGMENTS）

感谢 Frank Xu、Jiayi Pan、Vijay Viswanathan、Chenglei Si 与 Jason Wu 在本项目早期阶段的有益讨论。Zora Zhiruo Wang 受 **CMU Teng Family Presidential Fellowship** 资助。

---

## 参考文献（REFERENCES）

（以下条目保持与原文一致的作者、年份、标题与链接格式；书目信息为英文原文。）

- Matthew Bowers, Theo X. Olausson, Lionel Wong, Gabriel Grand, Joshua B. Tenenbaum, Kevin Ellis, and Armando Solar-Lezama. Top-down synthesis for library learning. *Proc. ACM Program. Lang.*, 7(POPL), Jan 2023. doi: 10.1145/3571234. URL https://doi.org/10.1145/3571234.

- Tianle Cai, Xuezhi Wang, Tengyu Ma, Xinyun Chen, and Denny Zhou. Large language models as toolmakers. *arXiv preprint* arXiv:2305.17126, 2023. URL https://arxiv.org/pdf/2305.17126.

- Michelene T. H. Chi, Paul J. Feltovich, and Robert Glaser. Categorization and representation of physics problems by experts and novices. *Cognitive science*, 5(2):121–152, 1981.

- Michelene T. H. Chi, Robert Glaser, and Marshall J. Farr. *The nature of expertise*. Psychology Press, 2014.

- Xiang Deng, Yu Gu, Boyuan Zheng, Shijie Chen, Samuel Stevens, Boshi Wang, Huan Sun, and Yu Su. Mind2web: Towards a generalist agent for the web. In *Thirty-seventh Conference on Neural Information Processing Systems Datasets and Benchmarks Track*, 2023. URL https://openreview.net/forum?id=kiYqbO3wqw.

- Alexandre Drouin, Maxime Gasse, Massimo Caccia, Issam H. Laradji, Manuel Del Verme, Tom Marty, Léo Boisvert, Megh Thakkar, Quentin Cappart, David Vazquez, et al. Workarena: How capable are web agents at solving common knowledge work tasks? *arXiv preprint* arXiv:2403.07718, 2024.

- Kevin Ellis, Lionel Wong, Maxwell Nye, Mathias Sable-Meyer, Luc Cary, Lore Anaya Pozo, Luke Hewitt, Armando Solar-Lezama, and Joshua B. Tenenbaum. Dreamcoder: growing generalizable, interpretable knowledge with wake–sleep bayesian program learning. *Philosophical Transactions of the Royal Society A*, 381(2251):20220050, 2023.

- Yao Fu, Dong-Ki Kim, Jaekyeom Kim, Sungryull Sohn, Lajanugen Logeswaran, Kyunghoon Bae, and Honglak Lee. Autoguide: Automated generation and selection of state-aware guidelines for large language model agents. *arXiv preprint* arXiv:2403.08978, 2024.

- Gabriel Grand, Lionel Wong, Matthew Bowers, Theo X. Olausson, Muxin Liu, Joshua B. Tenenbaum, and Jacob Andreas. Lilo: Learning interpretable libraries by compressing and documenting code. *arXiv preprint* arXiv:2310.19791, 2023.

- Patrick Haluptzok, Matthew Bowers, and Adam Tauman Kalai. Language models can teach themselves to program better. In *The Eleventh International Conference on Learning Representations*, 2023. URL https://openreview.net/forum?id=SaRj2ka1XZ3.

- Jing Yu Koh, Robert Lo, Lawrence Jang, Vikram Duvvur, Ming Chong Lim, Po-Yu Huang, Graham Neubig, Shuyan Zhou, Ruslan Salakhutdinov, and Daniel Fried. Visual web arena: Evaluating multimodal agents on realistic visual web tasks. In *ICLR 2024 Workshop on Large Language Model (LLM) Agents*, 2024. URL https://openreview.net/forum?id=RPKxrKTJbj.

- Jacky Liang, Wenlong Huang, Fei Xia, Peng Xu, Karol Hausman, Brian Ichter, Pete Florence, and Andy Zeng. Code as policies: Language model programs for embodied control. In *2023 IEEE International Conference on Robotics and Automation (ICRA)*, pp. 9493–9500. IEEE, 2023.

- Evan Zheran Liu, Kelvin Guu, Panupong Pasupat, and Percy Liang. Reinforcement learning on web interfaces using workflow-guided exploration. In *International Conference on Learning Representations*, 2018. URL https://openreview.net/forum?id=ryTp3f-0-.

- Bodhisattwa Prasad Majumder, Bhavana Dalvi Mishra, Peter Jansen, Oyvind Tafjord, Niket Tandon, Li Zhang, Chris Callison-Burch, and Peter Clark. Clin: A continually learning language agent for rapid task adaptation and generalization. *arXiv preprint* arXiv:2310.10134, 2023.

- Jiayuan Mao, Tomás Lozano-Pérez, Joshua B. Tenenbaum, and Leslie Pack Kaelbling. Learning reusable manipulation strategies. In *Conference on Robot Learning*, pp. 1467–1483. PMLR, 2023.

- Shikhar Murty, Christopher Manning, Peter Shaw, Mandar Joshi, and Kenton Lee. Bagel: Bootstrapping agents by guiding exploration with language. *arXiv preprint* arXiv:2403.08140, 2024.

- Junhyuk Oh, Satinder Singh, Honglak Lee, and Pushmeet Kohli. Zero-shot task generalization with multi-task deep reinforcement learning. In *International Conference on Machine Learning*, pp. 2661–2670. PMLR, 2017.

- Jiayi Pan, Yichi Zhang, Nicholas Tomlin, Yifei Zhou, Sergey Levine, and Alan Suhr. Autonomous evaluation and refinement of digital agents. *arXiv preprint* arXiv:2404.06474, 2024.

- Christopher Rawles, Alice Li, Daniel Rodriguez, Oriana Riva, and Timothy P. Lillicrap. Android in the wild: A large-scale dataset for android device control. In *Thirty-seventh Conference on Neural Information Processing Systems Datasets and Benchmarks Track*, 2023. URL https://openreview.net/forum?id=j4b3l5kOil.

- Christopher Rawles, Sarah Clinckemaillie, Yifan Chang, Jonathan Waltz, Gabrielle Lau, Marybeth Fair, Alice Li, William Bishop, Wei Li, Folawiyo Campbell-Ajala, et al. Androidworld: A dynamic benchmarking environment for autonomous agents. *arXiv preprint* arXiv:2405.14573, 2024.

- Tianlin Shi, Andrej Karpathy, Linxi Fan, Jonathan Hernandez, and Percy Liang. World of bits: An open-domain platform for web-based agents. In Doina Precup and Yee Whye Teh (eds.), *Proceedings of the 34th International Conference on Machine Learning*, volume 70 of *Proceedings of Machine Learning Research*, pp. 3135–3144. PMLR, 06–11 Aug 2017. URL https://proceedings.mlr.press/v70/shi17a.html.

- Paloma Sodhi, S. R. K. Branavan, and Ryan McDonald. Heap: Hierarchical policies for web actions using llms. *arXiv preprint* arXiv:2310.03720, 2023.

- Haotian Sun, Yuchen Zhuang, Lingkai Kong, Bo Dai, and Chao Zhang. Adaplanner: Adaptive planning from feedback with language models. In *Thirty-seventh Conference on Neural Information Processing Systems*, 2023. URL https://openreview.net/forum?id=rnKgbKmelt.

- Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar. Voyager: An open-ended embodied agent with large language models. *Transactions on Machine Learning Research*, 2024a. ISSN 2835-8856. URL https://openreview.net/forum?id=ehfRiF0R3a.

- Zhiruo Wang, Zhoujun Cheng, Hao Zhu, Daniel Fried, and Graham Neubig. What are tools anyway? a survey from the language model perspective. In *First Conference on Language Modeling*, 2024b. URL https://openreview.net/forum?id=Xh1B90iBSR.

- Zhiruo Wang, Graham Neubig, and Daniel Fried. TroVE: Inducing verifiable and efficient toolboxes for solving programmatic tasks. In *Forty-first International Conference on Machine Learning*, 2024c. URL https://openreview.net/forum?id=DCNCwaMJjI.

- Shunyu Yao, Howard Chen, John Yang, and Karthik Narasimhan. Webshop: Towards scalable real-world web interaction with grounded language agents. In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh (eds.), *Advances in Neural Information Processing Systems*, volume 35, pp. 20744–20757. Curran Associates, Inc., 2022. URL https://proceedings.neurips.cc/paper_files/paper/2022/file/82ad13ec01f9fe44c01cb91814fd7b8c-Paper-Conference.pdf.

- Ori Yoran, Samuel Joseph Amouyal, Chaitanya Malaviya, Ben Bogin, Ofir Press, and Jonathan Berant. Assistantbench: Can web agents solve realistic and time-consuming tasks? *arXiv preprint* arXiv:2407.15711, 2024.

- Wenhao Yu, Nimrod Gileadi, Chuyuan Fu, Sean Kirmani, Kuang-Huei Lee, Montse Gonzalez Arenas, Hao-Tien Lewis Chiang, Tom Erez, Leonard Hasenclever, Jan Humplik, et al. Language to rewards for robotic skill synthesis. *arXiv preprint* arXiv:2306.08647, 2023.

- Longtao Zheng, Rundong Wang, Xinrun Wang, and Bo An. Synapse: Trajectory-as-exemplar prompting with memory for computer control. In *The Twelfth International Conference on Learning Representations*, 2024. URL https://openreview.net/forum?id=Pc8AU1aF5e.

- Shuyan Zhou, Frank F. Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng, Tianyue Ou, Yonatan Bisk, Daniel Fried, Uri Alon, and Graham Neubig. Webarena: A realistic web environment for building autonomous agents. In *The Twelfth International Conference on Learning Representations*, 2024. URL https://openreview.net/forum?id=oKn9c6ytLx.

---

## 附录 A：基于 LM 的 WORKFLOW 归纳（A LM-BASED WORKFLOW INDUCTION）

如 §2.3 所述，我们 **workflow induction module** 的一种实现是提示 **LM** 从给定示例（即 **experience**）生成抽象的、**sub-routine** 级别的 **workflows**。本节给出详细 **model prompt**、模型归纳的示例 **workflows**，以及对这些 **workflows** 的质量检验。

> 这一节把归纳模块从黑箱里拿出来：实际喂给语言模型的**提示词原文**长什么样、模型吐出来的 **workflow** 长什么样，以及作者用什么指标衡量好坏，都在这里对齐读。

### A.1 MODEL PROMPT

下面给出 WebArena 与 Mind2Web 实验输入模型的完整 **prompt**。两数据集实验使用相同 **prompt**。

> 用人话概括提示任务：给你一批网页导航任务，每条包含自然语言指令和完成它的操作序列；你要找出**多条任务里反复出现的共同操作片段**，每一段提成一个 **workflow**。每个 workflow 应是常被复用的子程序，**不要**彼此相似或功能重叠，且**至少两步**。输入里会变的文字（用户输入、按钮文案等）用**描述性变量名**代替，而不是写死「干猫粮」这类具体值。

> 设计上有三处值得盯：**反复出现**——逼模型做跨任务共性，而不是把单条经验原样存档；**禁止重叠**——控制库里冗余；**变量名替代具体值**——就是正文里说的抽象化。

> Given a list of web navigation tasks, your task is to extract the common workflows.  
> Each given task contains a natural language instruction, and a series of actions to solve the task.  
> You need to find the repetitive subset of actions across multiple tasks, and extract each of them out as a workflow.  
> Each workflow should be a commonly reused sub-routine of the tasks. Do not generate similar or overlapping workflows. Each workflow should have at least two steps. Represent the non-fixed elements (input text, button strings) with descriptive variable names as shown in the example.

### A.2 EXAMPLE WORKFLOWS

我们展示在 WebArena 与 Mind2Web 上归纳的若干示例 **workflows**，以给出更具体的印象。

> 下面列表是「长什么样」的样例：读的时候注意占位符——搜索词、出发地、仓库名等都写成 `{search-term}`、`FROM LOCATION` 一类，同一套骨架可被不同具体任务复用。

**WebArena Workflows**  
我们在 WebArena 涉及的每个网站各展示一条示例 **workflow**。

- **## shopping: Browse Products in a Specific Category**  
  To browse products in a specific category, I need to navigate to the relevant main category. I will start by hovering over the main category menu item to reveal the subcategories.  
  `hover('main category id')`  
  To browse products in the specific subcategory, I need to click on the subcategory link.  
  `click('subcategory id')`

- **## shopping admin: Edit and Save Changes**  
  This workflow is used to edit specific fields and save changes.  
  To edit a specific field, I need to locate the field and update its value.  
  `clear('field id')`  
  `fill('field id', 'new value')`  
  Next, I need to save the changes by clicking the "Save" button.  
  `click('save button id')`

- **## reddit: Navigate to a forum section and select a specific forum**  
  To navigate to a specific forum, I need to click on the "Forums" section.  
  `click('42')`  
  Now, I need to click on the specific forum link based on the forum name provided.  
  `click('<forum link id>')`

- **## gitlab: Navigation to Repository and Contributors Section**  
  This workflow involves searching for a repository and navigating to its contributors to find detailed contribution data.  
  First, search for the specific repository to gather information.  
  `fill('130', '{RepositoryName}')`  
  `press('130', 'Enter')`  
  Navigate to the "Contributors" section to view contribution details.  
  `click('311')` # “Contributors” link  
  Obtain and report the required contributor details.  
  `send_msg_to_user('{ContributorDetails}')`

- **## map: Calculate Travel Time and Distance**  
  To calculate travel time and distance between two locations, I will use the directions feature. I will fill in the respective fields and select the mode of transportation.  
  `fill('158', 'FROM LOCATION')`  
  `fill('163', 'TO LOCATION')`  
  `select_option('166', 'MODE OF TRANSPORTATION')`  
  `click('171')`  
  I will use these details to provide the user with accurate travel time and distance information.  
  `send_msg_to_user('The distance between FROM LOCATION and TO LOCATION is DISTANCE and the estimated travel time is TIME.')`

> WebArena 片段在说什么可以连起来记：例如购物站「浏览某分类」——先悬停主类菜单露出子类，再点子类；地图站「算两地路程与时间」——在起终点字段填地点、选交通方式、点搜索，再把结果回给用户。都是**抽象步骤 + 占位符**，不是某一次购物或某两个真实城市名写死。

**Mind2Web Workflows**  
我们在 Mind2Web 的每个数据 **domain** 各给一条示例 **workflow**。

- **# travel: enter flight locations**  
  Given that you are on the flight booking page, this workflow enters the departure and destination city/airport for your flight.  
  `[link] From Departure Airport or City Your Origin -> CLICK`  
  `[textbox] Origin City or Airport -> TYPE: {your-origin-city}`  
  `[link] {best-popup-option} -> CLICK`  
  `[link] To Destination Airport or City Your Destination -> CLICK`  
  `[textbox] Destination City or Airport -> TYPE: {your-destination-city}`  
  `[link] {best-popup-option} -> CLICK`

- **# shopping: search and sort**  
  Given that you are on the Amazon search results page, this workflow searches for a product and sorts the results.  
  `[textbox] Search Amazon -> TYPE: {search-term}`  
  `[button] Go -> CLICK`  
  `[span] Sort by: -> CLICK`  
  `[option] {sort-option} -> CLICK`

- **# entertainment: search and select**  
  Given that you are on the IMDb homepage, this workflow searches for a term and selects the best match.  
  `[textbox] Search IMDb -> TYPE: {search-term}`  
  `[button] Submit Search -> CLICK`  
  `[button] {best-match} -> CLICK`

> Mind2Web 侧同理：旅行「填出发到达」——点输入框、打字、在弹出里选最佳匹配，目的地再来一遍；购物「搜索并排序」——搜索框关键词、点搜索、打开排序、选排序方式。共同点是**具体商品名、城市名都变成占位**，所以同一条 workflow 能套在不同指令上。

### A.3 WORKFLOW QUALITY ANALYSIS

为在端到端任务成功之外提供中间信息，我们提出若干指标以检验模型归纳 **workflows** 的质量。（1）**Number of workflows**：增强到 **memory** 的 **workflows** 数量——**workflows** 越少越好，而 agent 依赖更少 **workflows** 即可达到满意性能。（2）**Coverage**：**action trajectory** 中有多少步被 **workflows** 覆盖；更高 **coverage** 通常表明相关 **workflow** 的广泛适用性。（3）**Function overlap**：**workflows** 之间功能重叠程度；我们通过统计同一网站上每对 **workflow** 之间重叠 **sub-trajectories**（≤2 步）的数量来衡量。重叠越少表示 **workflow** 管理越充分。（4）**Utility rate**：**test examples** 使用 **workflows** 的频率。

> 四个指标可以这样记：**数量**——越少越好，说明每条更「值钱」；**覆盖率**——真实轨迹里有多少步能落在某个已归纳 workflow 里，高则覆盖广；**功能重叠**——不同 workflow 之间短子序列重复多不多，低则库更干净；**使用率**——测试任务里有多少比例真的用到了 workflow。四者一起描述「库是否精简、是否被用、是否冗余」。

我们在 WebArena 测试示例与 Mind2Web **cross-task** 测试示例上评估 **workflows**。我们不在 WebArena 上评估 **coverage**，因其需要 **canonical trajectories**，而 WebArena 不提供。对 Mind2Web，我们不在 **cross-website** 与 **cross-domain** 测试示例上评估，因为从 **training examples** 归纳的 **workflows** 与这些测试示例无领域重叠，因而适用性较低。

如表 10，基于神经网络的归纳每个示例产生 **7.3–7.4** 条 **workflows**，效率较高且不会向 **memory** 增加过多内容。在 WebArena 上，归纳的 **workflows** 被 **0.94** 的测试示例使用，表明其在多样任务中的广泛适用性。此外，**workflows** 之间仅 **0.08** 的步骤重叠，表明 **workflows** 在求解各自任务时的效率。Mind2Web 上的 **workflows** 使用频率同样较高（**utility rate** 为 **0.91**），但功能重叠略多，且对测试示例仅达到 **0.40** 的 **coverage**。然而，由于用于归纳 **workflows** 的 **training examples** 与 **cross-task** 测试示例在任务分布上差异较大，这一相对较低的 **coverage** 是合理的。

> 实测印象：每站大约 **7** 条 workflow 量级，**很省**；WebArena 上约 **94%** 测试任务会用到 workflow，**0.08** 的重叠说明几乎不冗余。Mind2Web 使用率也高（**0.91**），但覆盖率只有 **0.40**、重叠略多——论文认为合理：训练集和 cross-task 测试分布差得大，从训练归纳的库**不可能**盖住测试里每一步，低覆盖率不代表归纳失败。

**表 10**：Mind2Web 数据集上模型归纳 **workflows** 的质量评估。

| Metric | #Workflows | Coverage | Function Overlap | Utility Rate |
|--------|------------|----------|------------------|--------------|
| WebArena | 7.4 | - | 0.08 | 0.94 |
| Mind2Web | 7.3 | 0.40 | 0.20 | 0.91 |

---

## 附录 B：基于规则的 WORKFLOW 归纳（B RULE-BASED WORKFLOW INDUCTION）

除基于 **LM** 的 workflow 归纳外，我们还探索基于规则的 workflow 归纳方法。我们的规则 **workflow induction module** 包含两步：（i）**experience deduplication**；（2）**invalid action filtering**。

> 正文 §4.1 里出现的规则基线，在这里补全算法；读的时候抓住「**只做机械处理，不做语义**」即可。

对去重，我们提取 **experience** 的 **action sequence**，例如从 **trajectory** `CLICK('12') → CLICK('30') → TYPE('44', "cat")` 提取 **CLICK → CLICK → TYPE**。我们按 **action sequence** 对 **experiences** 分组，并从每组随机选取 \(n\) 条（默认 \(n=1\)）。特别在 WebArena 上，若每条 **experience** 的 **task template** 已知，我们再按 **task template** 分组并进行一轮去重，每组随机选取 \(n\)（默认 \(n=1\)）条 **experience**。该过程从给定 **experiences** 中产生多样化 **experiences**。

> 去重：只保留**操作类型**的序列（点击、输入、不按元素 id 区分），**类型串相同**的归一组，每组随机留一条；WebArena 若知道模板，再按模板做一轮同样操作。得到的是一批**多样化但仍完整、具体**的经验轨迹。

接下来，对每条唯一 **experience**，我们移除其 **action trajectory** 中的无效步骤。**Invalid actions** 指无法在环境中成功执行的 **actions**，因其输入参数不满足 **action function** 的要求。具体地，对 **CLICK** 与 **TYPE** 我们有一条判定 **invalid actions** 的规则：要求第一个参数为字符串形式的整数（对应环境中的元素 **id**）。若不符合，则移除相应 **CLICK** 与 **TYPE** 步骤。例如，**trajectory** 为 `CLICK(12) → CLICK('12') → CLICK('30') → TYPE(44, "cat") → TYPE('44', "cat")` 的 **experience** 将变为 `CLICK('12') → CLICK('30') → TYPE('44', "cat")`。我们对每条唯一 **experience** 进行该 **invalid action** 过滤，并将结果 **experiences** 作为基于规则的 **workflows**。

> 清洗：对点击、输入，要求第一个参数是**字符串形式的整数 id**，否则删步。最后剩下的轨迹**直接当 workflow 用**——没有语义抽象、没有拆子程序，只有**去重 + 格式合法**；和 LM 归纳的**占位符、细粒度子程序**是两条路。

---

## 附录 C：整合 AWM OFFLINE 与 ONLINE（C INTEGRATING AWM OFFLINE AND ONLINE）

我们在 §3.2 比较了分别采用从 **training** 或测试时即时归纳的 **workflows** 的 **AWM\(_{\text{offline}}\)** 与 **AWM\(_{\text{online}}\)**。本节探索两类 **workflows** 的整合 **AWM\(_{\text{off+on}}\)**：注入相关的 **training workflows** 以 **warm-start** 任务求解，同时聚合越来越多的 **online-induced workflows** 以更好适应测试分布。

> 动机很自然：训练集归纳的 workflow **冷启动**，测试过程中再 **Online** 往里加，似乎既有先验又能适应分布。但表里会看到，**一加一并不大于二**。

**表 11**：使用 **gpt-4** 模型在 Mind2Web **cross-task**、**cross-website** 与 **cross-domain** 泛化测试上的成功率。**EA** 为 **element accuracy** 缩写，**AF₁** 为 **action F₁** 缩写。

| Method | Cross-Task EA | AF₁ | Step SR | SR | Cross-Website EA | AF₁ | Step SR | SR | Cross-Domain EA | AF₁ | Step SR | SR |
|--------|---------------|-----|---------|-----|------------------|-----|---------|-----|-----------------|-----|---------|-----|
| MindAct* | 41.6 | 60.6 | 36.2 | 2.0 | 35.8 | 51.1 | 30.1 | 2.0 | 21.6 | 52.8 | 18.6 | 1.0 |
| AWM offline | 50.6 | 57.3 | 45.1 | 4.8 | 41.4 | 46.2 | 33.7 | 2.3 | 36.4 | 41.6 | 32.6 | 0.7 |
| AWM online | 50.0 | 56.4 | 43.6 | 4.0 | 42.1 | 45.1 | 33.9 | 1.6 | 40.9 | 46.3 | 35.5 | 1.7 |
| AWM off+on | 50.0 | 57.0 | 44.5 | 1.6 | 41.8 | 45.5 | 33.3 | 1.1 | 39.3 | 44.3 | 34.1 | 1.5 |

由表 11，**AWM\(_{\text{off+on}}\)** 在三个测试划分上的分数介于 **AWM\(_{\text{offline}}\)** 与 **AWM\(_{\text{online}}\)** 之间。并非简单相加：**offline** 与 **online** 归纳的 **workflows** 彼此并不完全兼容；特别是 **offline workflows** 似乎损害 **online workflows** 的生成质量与效用，因而总体为中等结果。

> 结合版表现**夹在**纯 Offline 与纯 Online 之间，没有「堆得越多越强」。论文的解释是：两套来源的 workflow **风格与兼容度不一致**，记忆里同时塞两类，反而干扰 Online 侧新归纳的质量。启发是：**workflow 库贵在一致、可兼容，不在数量**；把两套来源硬拼，不如维护好一套内部自洽的库。

---

*说明：译文依据 `AWM_clean.txt` 清理后的正文与附录。源文件由 PDF 提取，部分段落存在连字或乱码；译文在对应处按论文原意做了还原。图 1–7 的版式说明以正文描述为准。*
