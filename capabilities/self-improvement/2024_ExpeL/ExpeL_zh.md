# ExpeL：LLM Agent 是 Experiential Learner（经验型学习者）

**Andrew Zhao,♠ Daniel Huang,♣ Quentin Xu,♣ Matthieu Lin,♣ Yong-Jin Liu,♣ Gao Huang♠\***

♠ Department of Automation, BNRist, Tsinghua University  
♣ Department of Computer Science, BNRist, Tsinghua University  

{zqc21, huang-jy22, xgd22, lyh21}@mails.tsinghua.edu.cn,  
{liuyongjin, gaohuang}@tsinghua.edu.cn  

\*通讯作者。

Copyright © 2024, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved.

---

## 摘要

近期将 large language models (LLMs) 应用于 decision-making 任务的研究兴趣激增，其动力在于利用嵌入在 LLM 中的广泛世界知识。虽然将 LLM 定制用于特定 decision-making 任务的需求日益增长，但针对具体任务对它们进行 finetuning 资源密集，并可能削弱模型的泛化能力。此外，GPT-4 和 Claude 等最先进的语言模型主要通过 API 调用访问，其参数权重仍为专有且不对公众开放。这一情形凸显了：需要新的方法论，使系统能够在**无需 parametric updates** 的情况下从 agent experiences 中学习。为应对这些问题，我们引入 **Experiential Learning (ExpeL)** agent。我们的 agent 从一组 training tasks 中自主收集 experiences，并使用 natural language 从中提取 knowledge。在 inference 时，agent 回忆其提取的 insights 与 past experiences，以做出知情决策。我们的实证结果突出了 ExpeL agent 的稳健学习效能，表明其性能随着 experiences 的积累而持续提升。我们通过定性观察与额外实验进一步探讨了 ExpeL agent 的新兴能力与 transfer learning 潜力。¹

> 若某计算机程序关于某类任务 \(T\) 与性能度量 \(P\)，其性能（由 \(P\) 衡量）随经验 \(E\) 而提高，则称该程序从经验 \(E\) 中学习。  
> — Tom Mitchell

¹ 项目页见 https://andrewzh112.github.io/expel ，代码见 https://github.com/LeapLabTHU/ExpeL 。

---

## 1 Introduction（引言）

机器学习研究长期被 autonomous agents 及其能力的潜力所吸引。近来，将 large language models 纳入这些 agents（Wang et al. 2023b; Xi et al. 2023），已揭示出广泛的应用谱系，甚至超越学术界（Yang et al. 2023a; Nakajima 2023; Significant-Gravitas 2023）。LLM 的重要优势之一在于其 world knowledge，使其能够天然地适用于多种场景（Zhao et al. 2023b）。

一方面，先前工作研究了通过大量 environment interactions（Yao et al. 2023c）或大量 human-labeled datasets（Nakano et al. 2021; Shaw et al. 2023）来 finetuning LLM。这类方法计算成本高，且需要访问 LLM 的 parametric weights。此外，finetuning 会限制 LLM 的功能并可能损害其泛化能力（Du et al. 2022）。另一方面，prompting 方法可以仅用少量 in-context examples 就增强 LLM 的 sequential decision-making planning 能力（Hao et al. 2023; Lin et al. 2023b; Sun et al. 2023）。然而，由于当前 LLM 受 context window size 所限（Tworkowski et al. 2023），这些 agents 无法“记住”所见内容，因而除少数 demonstrations 外无法学习。那么，如何在这两种范式之间取得平衡？

我们提出 **Experiential Learning (ExpeL)** agent 作为解决方案。我们的 agent 通过 trial and error 从一组 training tasks 中自主收集 experiences。从这些 experiences 中，它推导出 natural language insights，并在 test time 将其自身的 successful experiences 用作 in-context examples。我们 agent 的学习过程类似于学生备考后单次应试，反映许多真实世界情形。与 Reflexion（Shinn et al. 2023）等 self-improvement 方法不同，我们的方法强调**跨多个任务保留 experiences** 以提升 agent 性能。此外，ExpeL 无需 parameter updates 即可学习，因而与 GPT-4 或 Claude 等强大的闭源模型兼容。最后，experience gathering 步骤不需要大量数据或 human labels。

我们在三个截然不同的领域上评估了 ExpeL，并持续优于强基线。此外，我们展示了一个 transfer learning 场景：从 source tasks 积累知识的 agent 对 target tasks 表现出正向 forward transfer。最后，我们强调了 ExpeL agent 获得的一些意外涌现能力。

**我们的主要贡献如下：** (1) 我们提出 ExpeL，一种无需 gradient updates 即可从 experience 自主学习的 novel LLM agent；(2) 我们在多样化任务集上评估 ExpeL，展示其学习能力及对现有 planning 方法的改进；(3) 我们展示了我们 LLM agent 的一种 novel transfer learning 设定，并演示从 source tasks 到 target tasks 的 forward transferability。最后，我们相信随着 planning algorithms 与 foundational models 的持续改进，ExpeL 的范式将从其性能提升中获得显著收益。

---

## 2 Related Work（相关工作）

本节讨论最相关的相关工作。更详细的讨论见 Appendix A。

**Prompt-based Learning：** Prompt-based learning 通过修改输入 context 来细化 label prediction 任务，便于以最少数据快速适应新任务（Liu et al. 2023a）。该方法利用 LLM 作答而无需调参，因其可通过 in-context learning（Brown et al. 2020）进行增强。LAMA（Petroni et al. 2019）与 GPT-3（Brown et al. 2020）是推动该表述的早期工作。减轻 prompt 设计复杂度的努力包括面向 NLP 的 automatic reasoning chains（Kojima et al. 2022; Zhang et al. 2023）。类似地，ExpeL agent 也通过修改 execution prompt，使用提取的 insights 与自生成的 in-context trajectories 从 experiences 自主学习。

**Retrieval Augmented Generation (RAG)：** Retrieval 使 LLM 能够访问数据库，缓解 hallucinations（Li et al. 2022; Wang, Yang, and Wei 2023; Rubin, Herzig, and Berant 2022; Liu et al. 2022）。Retrieval 也被用于增强 decision-making agents 的能力（Humphreys et al. 2022; Zhao et al. 2023a）。与这些工作相比，我们聚焦于检索 ExpeL agent **自生成的 experiences**，从而降低对 gold examples 的依赖，并利用 domain-specific corpus。

**Planning for LLM Agents：** 在机器人、自然科学、游戏与工作流等领域应用 LLM agents 激增，强调其在 few-shot 设定下的 world knowledge（Ha, Florence, and Song 2023; Mu et al. 2023; Bran et al. 2023; Boiko, MacKnight, and Gomes 2023; Yang et al. 2023b; Lin et al. 2023a; Nakano et al. 2021; Wang et al. 2023c; Liu et al. 2023b）。此外，LLM 在多种配置下展现了有前景的 zero/few-shot planning 与 reasoning 能力（Sumers et al. 2023），包括 embodied environments 与 reasoning 任务（Huang et al. 2022; Yao et al. 2023a; Wei et al. 2022b; Yao et al. 2023b; Gong et al. 2023）。

**Self-improvement and Memory for LLM Agents：** 像 Reflexion 这样的 agents 展示了基于 feedback 的改进，但往往缺乏 cross-task memory（Shinn et al. 2023）。其他 agents 在多 agent 情境中展现了 persistent memory 的潜力（Park et al. 2023; Maas et al. 2023）。我们的 ExpeL agent 结合这些思路，聚焦于 task-solving，同时受益于自生成的 in-context examples 与从 memory 中抽象出的 insights。

---

## 3 Preliminaries（预备知识）

**Complex Interactive Tasks：** 我们处理 complex interactive tasks：在每个时间步 \(i \in \{0,\ldots,H\}\)，agent 接收 observation \(o \in \mathcal{O}\)，并基于其 observation history \(\mathcal{H}\) 决定执行 action \(a \in \mathcal{A}\)。agent 的目标是达成某 goal \(g \in \mathcal{G}\)。本文仅考虑 deterministic environments。

**Large Language Models：** Large language model 是自然语言的统计模型，通常为 neural network。在我们的设定中，我们使用 autoregressive language model（OpenAI 2023; Brown et al. 2020; Touvron et al. 2023b,a; Chowdhery et al. 2023），给定已有 token 的有序列表 \(x = \{x_1, x_2, \ldots, x_{l-1}\}\)，输出下一 token 的概率 \(p(x_l \mid x_{<l})\)。**Instruction-following LLM**（Thoppilan et al. 2022; Chung et al. 2022; Wei et al. 2022a）通常在格式化为 instruction、input、response 元组的各类 NLP tasks 上 finetuned（Taori et al. 2023）。Instruction-tuned models 更擅长遵循 natural language instructions，从而减轻 heavy prompt engineering 的需要（Wei et al. 2022a）。

**ReAct and Reflexion：** ReAct（Yao et al. 2023b）与 Reflexion（Shinn et al. 2023）是有前景的框架，使上述 LLM 在 reasoning 与 self-improvement 方面的能力得以发挥。ReAct 显式交织 observations、actions 与 thoughts，为稳健的 planning 与 reasoning 能力提供基础。在此基础上，Reflexion 在同一任务的后续 trial 重试之前引入额外的 reflective 步骤，增强模型的 adaptive learning 过程。

我们旨在增强 planning LLM agent（如 ReAct）的**学习能力**，使其能够通过 **inter-task experiences** 改进而**无需任何 parameter updates**。受人类学习中固有认知能力、自学习 autonomous agents 中观察到的益处，以及 prompt-based methods 的进展启发，我们开发了 **Experiential Learning (ExpeL)** agent。在 **training stage**，agent 与 environment 交互，通过 trial and error 收集 experiences。这些 experiences 存储在 **experience pool**（Lin 1992）中。之后 agent 从该 pool 中提取 insights，类似于 **off-policy learning**（Watkins and Dayan 1992），其中 agent 可以从 behavior policy 的 experiences 中学习。在 **evaluation stage**，agent 以单次尝试完成 unseen tasks，并用从 training stage 收集的 extracted insights 与 successful trajectories（存于其 experience pool）进行增强。详见 Fig. 1 了解我们 agent 框架的详细信息。

---

## 4 ExpeL: An Experiential Learning Agent

### 4.1 Gathering Experiences

为收集可用于提取信息的多样化 experiences，我们利用 Reflexion（Shinn et al. 2023）对 training task 持续重试，最多 \(Z\) 次。具体而言，在第 \(z\) 次 trial，agent 获得 training task \(t_n\)、fewshot examples \(F_{\text{manual}}\) 与 past reflections \(\nu_{n,z}\)（初始时 \(\nu_{n,0}\) 为空串）。首先，agent 以 fewshot examples 与其当前 trajectory \(\tau_{n,0}\) 拼接作为 context 尝试任务，并以 ReAct（Yao et al. 2023b）为 base planning algorithm：\(\text{LLM}_{\text{ReAct}}(\cdot \mid \tau_{n,0}, F_{\text{manual}}, \nu_{n,0})\)。在第 \(z\) 次 trial，当 agent 完成任务或达到最大步数 \(H\) 时，ExpeL agent 的 experience pool \(\mathcal{B}\) 吸收 trajectory \(\tau_{n,z}\)。若成功，则进入下一任务；若失败，则查看失败 trajectory 并 self-reflect，产生 \(\nu_{n,z+1} = \text{concat}(\nu_{n,z}, \text{LLM}_{\text{reflect}}(\tau_{n,z}))\)，以在下次重试中改进。下一次重试中，agent 用 reflection \(\nu_{n,z+1}\) 增强 context，作为 LLM policy 的输入：\(\text{LLM}_{\text{ReAct}}(\cdot \mid \tau_{n,z+1}, F_{\text{manual}}, \nu_{n,z+1})\)。

强调：这种 trial and error 的 experience gathering 不仅提高 evaluation 时获得更多 positive examples 以供 experience recall 的几率，还便于收集宝贵的 success/failure pairs，用于 insight extraction 阶段的对比（Sec. 4.2）。伪代码见 Alg. 1。

**Learning from Successes and Failures：** 为利用 experience collection 阶段收集的多样化结果，我们认为 agent 应以两种方式分析 experiences。第一，让 agent 将**同一任务**的失败 trajectory 与成功 trajectory 对比。该对比提供对 agent 不足之处的具体理解，突出正确与错误 actions。第二，让 agent 在一组来自不同任务的成功 trajectories 中识别模式。该方法揭示 agent 可采纳的常见“good practices”，以确保在 evaluation tasks 中成功。

实现上，我们给予 agent 的 instruction-following LLM 若干可作用于已有 insights 集合 \(\hat{\iota}\) 的 **operators**。我们将 insights 集合初始化为空 \(\hat{\iota} = \emptyset\)，并迭代地向 LLM 提供来自 experience pool 的 fail/success pairs 或长度为 \(L\) 的成功列表（通过无放回抽样构造）。LLM 可执行的操作包括：**ADD** 新 insight、**EDIT** 已有 insight 的内容、**DOWNVOTE** 表示不同意某 insight，或 **UPVOTE** 表示同意。新加入的 insight 初始 **importance count** 为 2；若后续 **UPVOTE** 或 **EDIT** 作用于该 insight，则计数增加；**DOWNVOTE** 则减少。若某 insight 的 importance count 归零，则移除。该设计选择使过程更稳健，因为即使成功 trajectory 也可能次优并误导生成的 insights。所用 prompt template 见 Fig. 2。我们将成功列表的最大规模保持为 \(L\)，并以 **gpt-4-0613** 作为默认 \(\text{LLM}_{\text{insights}}\)。经验上 **gpt-4-0613** 在遵循 insight extraction operators 使用说明方面优于 **gpt-3.5-turbo-0613**，且 hallucinate 更少。该过程伪代码见 Alg. 2。最后，ExpeL 在 **task inference** 阶段使用生成的 insights \(\hat{\iota}\)，见下文。

### 4.2 Learning from Experiences

人类学习主要通过：在记忆中存储成功 trajectories（之后可作为具体 examples 回忆），或从 experiences 中提取 high-level insights（以泛化到新情境）。ExpeL 同时考虑这两种学习模式以提升 task performance。具体而言，给予 LLM agent 的 instruction \(I\) 可分解为 task specifications 与 fewshot examples。我们可用 agent 从过去 experiences 中提取的 insights 来增强 task specifications，并可利用 instruction-following LLM（OpenAI 2023）紧密遵循它们。对于 fewshot examples，我们允许 agent 从其 experience pool 中以 top-k 相关 examples 检索以辅助决策。下文详述 **experience recall** 与 **insight extraction** 机制。

**Similar Experiences as Demonstrations：** 研究表明，使用与当前任务语义相似的 **in-context examples** 性能更好（Liu et al. 2022）。此外，面对新情境时，人类也会从记忆中回忆类似已解决任务作为参考（Kahneman 2011）。受这些观察启发，我们提出 **experience recall**，根据 **task similarity** 从 training 期间收集的 experience pool 中检索 successful trajectories。具体地，我们使用 **Faiss vectorstore**（Johnson, Douze, and Jégou 2019）作为 experience pool、**kNN retriever** 与 **all-mpnet-base-v2** embedder（Song et al. 2020），获得与 evaluation task 具有最大内积 **task similarity** 的 top-k 成功 trajectories。使用 task similarity 作为检索排序的优势在于：若 agent 重复某任务或执行与 experience pool 中已有成功 trajectory 相似的任务，只需紧密模仿该成功 trajectory，对能力外推的负担更小。

### 4.3 Task Inference

在 agent 收集 experiences、从中提取 insights，并建立成功 trajectories 的 vector store 之后，即可进行 evaluation。对每个任务，task specifications 将用完整提取 insights 列表的拼接 \(\hat{\iota} = \text{concat}(\iota_1, \iota_2, \iota_3, \ldots)\) 增强，并检索 task similarity 最高的 top-k trajectories 作为 fewshot in-context examples，\(F_{\text{similar tasks}}\)。Fig. 3 展示示例 prompt template 结构；该步骤伪代码见 Alg. 3。我们相信随着提取 insights 列表增长，retrieval 可以是管理 context window size 的可行方案。

**Figure 3 说明：** evaluation 时 ExpeL 的 prompt template。白底区域与 base ReAct agent 的输入相同。差异在于（紫色区域）额外包含从过去 experience 提取的 insights，以及基于 task similarity 从过去 experiences **动态检索**的成功 in-context examples。

### 4.4 Transfer Learning

在展示如何利用 training set 上的 experiences 学习以使 LLM agent 受益、从而在同一 task distribution 上解决 unseen task 之后，我们研究另一有趣设定：从 **source task distribution** 积累的知识是否可在 **target task distribution** 上对 ExpeL agent 有用，且仅需极少 target task examples。与多数 transfer learning 设定类似，我们假设 source 与 target tasks 共享 common knowledge。因此，从 source tasks 积累的 experiences 可帮助 agent 解决新的 target tasks 集合。

类似于 transfer learning 文献中在 source task 上 pretraining、在 target task 上 finetuning（Zhuang et al. 2020），我们提出使用来自 source task 的提取 insights \(\hat{\iota}\) 与来自 target task 的 fewshot examples 来“**finetune**” insights，使其在 target task 中更适用。我们假设使用 target task 的 fewshot examples 能更好将 insights 锚定到 target task 并缓解 hallucinations。将 insights 从 source domain “finetune” 到 target domain 的示例 prompt template 见 Fig. 4。

### 4.5 ExpeL’s Strengths

本节概述我们框架的主要优势。首先，ExpeL 具有固有的 **interpretability**：提取的 experiences 与成功 trajectories 均以 natural language 呈现。用户可轻松检查、修改或移除潜在有害的 trajectories/insights——这在 finetuned models 中较难。此外，用户可无缝向 ExpeL agent 添加 expert insights 或 trajectories。其次，我们的学习方法**可及性高**：需要更少数据、降低计算资源、实现直接。再者，Reflexion（Shinn et al. 2023）等 self-improvement 方法促进 **intra-task** 改进，而 ExpeL 实现 **inter-task** 学习。ExpeL 不依赖 deployment 时的 retries，而某些领域有此要求。在灵活性方面，ExpeL agent 通用性强：不限于特定 language models，且可补充旨在增强 LLM agent planning 的现有策略；与之一同应用时，ExpeL 甚至可能提升 finetuned agents 的能力。另一优势是**持续改进**：我们的方法可从 foundational models 的持续增强中受益；例如实验表明用 **gpt-4** 提取 insights 优于 **gpt-3.5-turbo**（见 Sec. 5.6）。最后，我们引入了一种 transfer 方法（见上文）。

---

## 5 Experiments

### 5.1 Experimental Setup

与 ReAct（Yao et al. 2023b）一致，实验基于四个基于文本的 benchmark：**HotpotQA**（Yang et al. 2018）——知识密集型数据集，挑战 agent 使用搜索工具 Wikipedia Docstore API 进行 reasoning 与 question answering；**ALFWorld** 与 **WebShop**（Shridhar et al. 2021; Yao et al. 2022）——要求 agent 分别在家庭与在线购物网站环境中执行 interactive multi-step decision-making；**FEVER**（Thorne et al. 2018）——使用与 HotpotQA 相同 API 的 fact verification，适合 knowledge transfer（Sec. 5.4）。所有实验使用 **four-fold validation**，并报告各 fold 上的均值与标准误。

遵循 ReAct，对所有环境，我们以 **success rate** 为 evaluation metric：HotpotQA 与 FEVER 为 exact matching；ALFWorld 为在时限内完成任务；WebShop 为购买符合全部属性的商品。环境若提供额外指标则一并报告：WebShop 的 mean reward（Appendix 中 Eq. 1 计算）\(r_{\text{score}} \in [0,1]\)；ALFWorld 按 task type 的 score breakdown。

我们以 ReAct 与 **Act** 为主要 baseline planning LLM agents（Yao et al. 2023b），其中 Act 无 ReAct 式的 reasoning steps。包括 ExpeL 在内的所有 agents 在 evaluation 执行 actions 时使用 **gpt-3.5-turbo-0613**。所有文本生成 temperature 为 0，**greedy decoding**。**Imitation learning (IL)** 结果取自 ReAct 论文（Yao et al. 2023b）。实验设置更多细节见 Appendix D。

### 5.2 Main Results

本研究主要发现见 **Fig. 5**。基于 IL 的方法在 WebShop 与 ALFWorld 上难以高效表现，可能因其需要更强的 prior 与 reasoning 能力，而从零开始的常规训练无法提供。该局限显示利用 knowledge-based language models 应对这些挑战的前景。以下论断基于：(1) 对各环境的深入理解；(2) 提取的 insights 与可检索的 in-context examples；(3) 各次运行的统计（如每 trial 的 invalid actions 数量）。

**Experiential learning：** 以抽象 insights 与回忆成功 trajectories 的能力增强 agents，相较 baseline agents 在所有环境中均提升性能。当将 ExpeL 限制为仅一种学习模式（**insights-only** 或 **retrieval-only**）时，HotpotQA 与 ALFWorld 呈现对比鲜明的定量差异（HotpotQA 与 ALFWorld 分别为 36%/31% 与 50%/55%）。HotpotQA 上 insights 的突出影响可能因其依赖分析（Wikipedia 结果）能力，凸显跨问题类型的通用指南需求。相反，ALFWorld 的任务完成依赖特定 action sets，更受益于过去 experiential trajectories。此外，WebShop 提出独特挑战，既需基于网站的 reasoning（价格比较、query reformulation 等），又需精确执行 actions（搜索、点击、选项选择等）。因此这些任务上的性能在 success rate 与 score 上接近平衡（insights/retrieve-only 分别为 37%/38% 与 0.675/0.67，见 Appendix Tab. 5）。这些观察强调 experiential learning 中 abstraction 与 recollection 的协同，ExpeL 相对 baseline/受限学习模式 agent 具有定量优势。

**Cross-task learning：** 另一重要发现是与 Reflexion agent（Shinn et al. 2023）的比较。ExpeL 在 HotpotQA 上与 Reflexion 性能相当（R3 上 40% vs. 39%），在 ALFWorld 上甚至在不重复尝试的情况下优于 Reflexion（R3 上 54% vs. 59%）。Reflexion 通过反复执行任务（R1, R2, R3…）迭代细化 insights 以改进结果；我们的 ExpeL agent 则通过积累 **cross-task** experience 来学习。值得注意的是，WebShop 任务上仍有改进空间，接近 Reflexion success rates 的下沿。

### 5.3 Agent Behavioral Analysis

本节强调通过手动检查 ReAct 与 ExpeL agents 的 trajectories 得到的观察，并指出某些意外行为的可能成因。完整 trajectory 演示见论文网页 https://andrewzh112.github.io/expel 。

**Hypothesis Formulation & Constraints Adaptation：** 从 training set 收集的 experiences 提取 insights 后，我们注意到 agent 随后获得在**最后几步**重新评估整条 trajectory 并**果断结束任务**的能力，而非表达无法给出解答。该能力在 HotpotQA 中尤为明显（Appendix Fig. 16, 17），可能受影响的 insight 指出 agent 应“考虑答案可能已在已有 observations 中”。因此 agent 会基于过去 observations 提出最可能答案，而非以 “Unknown” 或 “Information not available” 结束。

**World Model Belief Update：** 我们注意到 ExpeL agent 通过 insights 与累积 experience **更新信念**。该信念更新使 agent 避免不必要 actions、提高解决给定任务的效率。例如在 ALFWorld 中，agent 完全改变了 ReAct 中对 pan 可能位置（从 drawers/countertops/cabinets 变为 stove-burners）的先验。该行为来自提取的 insight。

**Self-correction：** 尽管 ReAct 有时在尝试解题时无法重新评估处境，ExpeL 展现了识别并纠正错误步骤的能力。尤其在 ALFWorld 中错误拿取物体时，agent 已展示将其放回并继续任务、搜索正确物体的能力（Appendix Fig. 19）。这突出 ExpeL 在完成任务时从错误恢复、且完成时不 hallucinate 的能力；该行为可能由生成的 insight 所鼓励——若“某次尝试未推进任务”，则“reassess the situation 并考虑 alternative actions”。

**（WebShop 与 item 检索）** 在检查 trajectories 时，我们注意到 ExpeL agent 在搜索流程早期就展现出更强的 item 识别能力，声称在“搜索商品（searching for an item）”时需要“考虑其性质与典型用法（consider its nature and its typical usage）”（Appendix Fig. 18），从而使 agent 在第一步就迅速准确找到正确商品，而 ReAct agent 往往无法及时找到。

### 5.4 Transfer Learning

本实验使用 HotpotQA（Yang et al. 2018）作为 **source tasks**，FEVER（Thorne et al. 2018）作为 **target tasks**。与 HotpotQA 类似，我们为 agent 配备 Wikipedia Docstore API 导航能力；因此假设从 HotpotQA 获得的部分知识转移到 FEVER 任务中有益。我们使用 **gpt-4-0613** 将 HotpotQA insights 适配为 FEVER insights。用于 finetune insights 的 fewshot examples 与 task execution 时使用的相同。我们将 **ExpeLTransfer** agent 的 transfer learning 能力与 (1) ReAct；(2) Act；(3) 无 task demonstrations 而“finetune” insights 的 agent 比较。注意 source 与 target tasks 本质不同，故无 experience pool 可供检索；因此 ExpeLTransfer agents 使用现有固定 fewshot examples 作为 in-context examples。

**Tab. 1** 展示 transfer learning 结果。两种从 source domain 迁移知识的 agents 均获得性能提升。值得注意的是，有少量 in-context examples 的 agent 比没有的改进更显著，表明所提 transfer 场景中 “finetuning” 方法有效。

| Method | FEVER (SR%) |
|--------|-------------|
| Act | 58±0.0 |
| ReAct | 63±0.4 |
| ExpeLTransfer w/o Task Demos | 65±1.7 |
| **ExpeLTransfer** | **70±0.7** |

*Table 1: Transfer Results. 将 HotpotQA 提取的 insights 转移到 FEVER。Act 与 ReAct 为 baseline agents；ExpeL w/o Task Demos 在针对 target task 修改 insights 时不使用 fewshot examples。*

### 5.5 ExpeL with Task Reattempts

虽非本文核心，我们给出在 evaluation 阶段将 **task reattempts** 纳入 ExpeL 的初步结果（从 R0 的失败 checkpoint 恢复）。ExpeL 与 Reflexion 结合的表现，以及 ReAct+Reflexion 与 ExpeL 无 insights（ExpeL retrieve-only）两基线，见 **Table 2**。结果表明 ExpeL 与 Reflexion 配对时 success rate 显著提升，且随 task reattempts 次数增加而上升。

| | R0 | R1 | R2 | R3 |
|--|-----|-----|-----|-----|
| ReAct+Reflexion | 40.3% | 47.8% | 52.2% | 54.4% |
| ExpeL retrieve only | 54.5% | 57.5% | 59.7% | 60.4% |
| **ExpeL+Reflexion** | **59.0%** | **60.4%** | **63.4%** | **64.2%** |

*Table 2: ALFWorld 上带 Reflexion Rounds 的 Success Rate。ExpeL 与 Reflexion 在 ALFWorld 上呈协同（Highlight = 单次尝试的 ExpeL）。R1–R3 来自失败的 R0 checkpoints。*

### 5.6 Ablation Studies

ExpeL 的主要组件之一是 agent **自主收集**有益于自身学习的 valuable experiences。因此我们研究 **useful experiences 数量**是否影响 ExpeL 的下游性能。设计两种 agents 对比：其一仅有初始 fewshot examples 并从中提取 insights；其二用 **无重试的 ReAct** 收集 experience（成功 trajectory 更少，且 insight extraction 无 success/failure pairs）。在 HotpotQA 上实验，结果见 **Fig. 6**。可见仅从现有 fewshot 提取 insights 相较 ReAct **无优势**，说明 **experience 对 ExpeL 学习至关重要**。拥有更多 experience 的另两种 agents 表现显著更好。此外，使用 Reflexion 获得失败与成功对的**更丰富 experiences** 的 agent 优于仅使用 ReAct 进行 experience gathering 的 agent。

接下来审视 ExpeL 的 **insight extraction** 步骤有效性。由于 insights 对 HotpotQA 环境影响最大（Fig. 5），我们在该环境对 insights 做消融。从三个维度构造 ExpeL 变体：(1) **human-crafted insights**（Appendix Fig. 12）——人工根据 experience gathering 阶段 agent 错误精心设计；(2) 在 fail/success pairs 与成功列表之外将 reflections \(\nu\) 加入 insights 构造；(3) 使用 **gpt-3.5-turbo-0613** 作为 \(\text{LLM}_{\text{insights}}\)。**Tab. 3** 显示若干重要发现：(1) agent 学习的 insights 优于手工 insights；(2) 额外使用 reflections **不利**，可能因 reflections 有时输出 hallucinations、误导 insight extraction；(3) 更好的 LLM 更有利于提升 ExpeL 性能，表明 agent 将随 base foundation models 改进而“免费”获得性能提升。

最后我们研究以 **task similarity** 作为 ALFWorld 中检索成功 in-context examples 的排序分数的设计选择。特别地，我们使用 (1) **reasoning similarity**——检索与当前 trajectory 最新 reasoning step 最相似的 reasoning step 的 top-k trajectories；(2) 从 experience pool **随机抽样**成功 trajectories。**Tab. 3** 显示按 task similarity 检索（ExpeL）表现最佳。Reasoning similarity 仍有优势但略降，可能因单次 trajectory 中 fewshots 动态变化导致不稳定。随机抽样性能显著下降，表明选择最相关 in-context example 的设计有利。

**Tab. 3（节选，与原文表一致）**

| HotpotQA (SR%) | |
|----------------|--|
| ReAct | 28.0±1.4 |
| Hand-crafted insights | 32.0±1.1 |
| Insights with reflections | 29.0±0.4 |
| gpt-3.5-turbo insights | 32.0±0.4 |
| **ExpeL (ours)** | **39.0±1.7** |

| ALFWorld (SR%) | |
|----------------|--|
| ReAct | 40.0±0.3 |
| Reasoning similarity | 48.5±2.1 |
| Random sampled | 42.5±0.8 |
| **ExpeL (ours)** | **59.0±0.3** |

*Table 3: Ablations Results. Upper: Ablations on insight extraction. Hand-crafted insights enjoyed a performance boost over ReAct but were less effective than LLM-generated ones. Furthermore, adding reflections to the insight-generating process hurt performance. Lastly, better LLM base models give better insights. Lower: Ablations on in-context examples selection strategy. Randomly selected baseline has a significant drop in performance while ranking using reason similarity also has a noticeable dip.*

---

## 6 Conclusion and Limitations

**Limitations：** 本文研究的是 **textual observation** 的任务，在真实场景中有限制。因此纳入 **image observations** 将使方法更通用。使用 Vision-Language Models 或 captioning models 补充 LLM 以支持图像观察是有趣的研究方向。此外，我们通过闭源 API LLMs 评估方法效力，在某些应用中可能不可行。探索使用 **open-source LLMs** 的 LLM agents 是未来有前景的工作（Zeng et al. 2023）。另外，由于提取的 insights 不超过当前 LLM 的 token 限制，可放入 agent 的 context window；但对真正的 **lifelong learning** agents，可能需要额外的 insights retrieval 步骤以保证可管理的 context window size。最后，与 reinforcement learning 方法不同，prompting 技术缺乏可能影响所得策略效率的理论支撑。未来研究应探索整合这些途径以获得更有效、更优的解。

**总结：** 我们提出 ExpeL，一种从一组 training tasks 自主收集 experience、在无模型参数访问的情况下改进解决 evaluation tasks 能力的 novel learning LLM agent。我们通过与 vanilla ReAct、Act agents 对比展示其学习收益；并研究 transfer learning 场景——从 source tasks 提取 insights 有益于 ExpeL agent 解决 target task。最后，我们呈现训练结束时 agent 发展的若干意外涌现能力。我们相信从 experience 自主学习对发展类人 intelligent agents 至关重要，而 ExpeL agent 是朝该目标迈出的一步。

---

## Acknowledgement

本工作部分得到国家重点研发计划（2022ZD0114900）、国家自然科学基金（62022048, U2336214, 62332019）以及清华大学国强研究院的支持。

---

## References（参考文献）

下列条目与论文英文 **References** 对齐；作者与 venue 按 `ExpeL_clean.txt`（第 605–809 行）及 AAAI 惯例整理。OCR 双栏导致 **Nakano et al. 2021** 与 **Thoppilan et al. 2022** 在原文本中粘连于同一行，此处已拆分为两条；**Nakano et al.** 在 WebGPT 论文中尚有更多作者，请以官方 bib 为准。

Anthropic. 2023. Introducing Claude.

Boiko, D. A.; MacKnight, R.; and Gomes, G. 2023. Emergent Autonomous Scientific Research Capabilities of Large Language Models. arXiv preprint.

Bran, A. M.; Cox, S.; White, A. D.; and Schwaller, P. 2023. ChemCrow: Augmenting Large-Language Models with Chemistry Tools. arXiv preprint.

Brown, T.; Mann, B.; Ryder, N.; Subbiah, M.; Kaplan, J. D.; Dhariwal, P.; Neelakantan, A.; Shyam, P.; Sastry, G.; Askell, A.; et al. 2020. Language Models are Few-Shot Learners. NeurIPS.

Chase, H. 2023. Langchain.

Chowdhery, A.; Narang, S.; Devlin, J.; Bosma, M.; Mishra, G.; Roberts, A.; Barham, P.; Chung, H. W.; Sutton, C.; Gehrmann, S.; Schuh, P.; Shi, K.; Tsvyashchenko, S.; Maynez, J.; Rao, A.; Barnes, P.; Tay, Y.; Shazeer, N.; Prabhakaran, V.; Reif, E.; Du, N.; Hutchinson, B.; Pope, R.; Bradbury, J.; Austin, J.; Isard, M.; Gur-Ari, G.; Yin, P.; Duke, T.; Levskaya, A.; Ghemawat, S.; Dev, S.; Michalewski, H.; Garcia, X.; Misra, V.; Robinson, K.; Fedus, L.; Zhou, D.; Ippolito, D.; Luan, D.; Lim, H.; Zoph, B.; Spiridonov, A.; Sepassi, R.; Dohan, D.; Agrawal, S.; Omernick, M.; Dai, A. M.; Pillai, T. S.; Pellat, M.; Lewkowycz, A.; Moreira, E.; Child, R.; Polozov, O.; Lee, K.; Zhou, Z.; Wang, X.; Saeta, B.; Diaz, M.; Firat, O.; Catasta, M.; Wei, J.; Meier-Hellstern, K.; Eck, D.; Dean, J.; Petrov, S.; and Fiedel, N. 2023. PaLM: Scaling Language Modeling with Pathways. JMLR.

Chung, H. W.; Hou, L.; Longpre, S.; Zoph, B.; Tay, Y.; Fedus, W.; Li, E.; Wang, X.; Dehghani, M.; Brahma, S.; et al. 2022. Scaling Instruction-Finetuned Language Models. arXiv preprint.

Du, M.; He, F.; Zou, N.; Tao, D.; and Hu, X. 2022. Shortcut Learning of Large Language Models in Natural Language Understanding: A Survey. arXiv preprint.

Gong, R.; Huang, Q.; Ma, X.; Vo, H.; Durante, Z.; Noda, Y.; Zheng, Z.; Zhu, S.-C.; Terzopoulos, D.; Fei-Fei, L.; et al. 2023. MindAgent: Emergent Gaming Interaction. arXiv preprint.

Gur, I.; Furuta, H.; Huang, A.; Safdari, M.; Matsuo, Y.; Eck, D.; and Faust, A. 2023. A Real-World Web Agent with Planning, Long Context Understanding, and Program Synthesis. arXiv preprint.

Ha, H.; Florence, P.; and Song, S. 2023. Scaling Up and Distilling Down: Language-Guided Robot Skill Acquisition. In CoRL. PMLR.

Hao, S.; Gu, Y.; Ma, H.; Hong, J. J.; Wang, Z.; Wang, D. Z.; and Hu, Z. 2023. Reasoning with Language Model is Planning with World Model. arXiv preprint.

Huang, W.; Abbeel, P.; Pathak, D.; and Mordatch, I. 2022. Language Models as Zero-Shot Planners: Extracting Actionable Knowledge for Embodied Agents. In ICML. PMLR.

Humphreys, P.; Guez, A.; Tieleman, O.; Sifre, L.; Weber, T.; and Lillicrap, T. 2022. Large-scale Retrieval for Reinforcement Learning. NeurIPS.

Johnson, J.; Douze, M.; and Jégou, H. 2019. Billion-scale Similarity Search with GPUs. IEEE Transactions on Big Data.

Kahneman, D. 2011. Thinking, Fast and Slow. Farrar, Straus and Giroux.

Kojima, T.; Gu, S. S.; Reid, M.; Matsuo, Y.; and Iwasawa, Y. 2022. Large Language Models are Zero-Shot Reasoners. NeurIPS.

Knight, M.; Chess, B.; and Schulman, J. 2021. WebGPT: Browser-Assisted Question-Answering with Human Feedback. arXiv preprint.

Li, H.; Su, Y.; Cai, D.; Wang, Y.; and Liu, L. 2022. A Survey on Retrieval-Augmented Text Generation. arXiv preprint.

Lin, B. Y.; Fu, Y.; Yang, K.; Ammanabrolu, P.; Brahman, F.; Huang, S.; Bhagavatula, C.; Choi, Y.; and Ren, X. 2023a. SwiftSage: A Generative Agent with Fast and Slow Thinking for Complex Interactive Tasks. NeurIPS.

Lin, K.; Agia, C.; Migimatsu, T.; Pavone, M.; and Bohg, J. 2023b. Text2Motion: From Natural Language Instructions to Feasible Plans. Autonomous Robots.

Lin, L.-J. 1992. Self-Improving Reactive Agents Based on Reinforcement Learning, Planning and Teaching. Machine learning.

Liu, J.; Shen, D.; Zhang, Y.; Dolan, B.; Carin, L.; and Chen, W. 2022. What Makes Good In-Context Examples for GPT-3? In DeeLIO. Association for Computational Linguistics.

Liu, P.; Yuan, W.; Fu, J.; Jiang, Z.; Hayashi, H.; and Neubig, G. 2023a. Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing. ACM Computing Surveys.

Liu, X.; Yu, H.; Zhang, H.; Xu, Y.; Lei, X.; Lai, H.; Gu, Y.; Ding, H.; Men, K.; Yang, K.; et al. 2023b. AgentBench: Evaluating LLMs as Agents. arXiv preprint.

Liu, Z.; Bahety, A.; and Song, S. 2023. REFLECT: Summarizing Robot Experiences for Failure Explanation and Correction. In CoRL. PMLR.

Maas; Carey; Wheeler; Saatchi; Billington; and Shamash. 2023. To Infinity and Beyond: SHOW-1 and Showrunner Agents in Multi-Agent Simulations. arXiv preprint. *(著者全名以 PDF 为准；OCR 仅存姓氏片段。)*

Mirchandani, S.; Xia, F.; Florence, P.; Ichter, B.; Driess, D.; Arenas, M. G.; Rao, K.; Sadigh, D.; and Zeng, A. 2023. Large Language Models as General Pattern Machines. In CoRL. PMLR.

Mu, Y.; Zhang, Q.; Hu, M.; Wang, W.; Ding, M.; Jin, J.; Wang, B.; Dai, J.; Qiao, Y.; and Luo, P. 2023. EmbodiedGPT: Vision-Language Pre-Training via Embodied Chain of Thought. NeurIPS.

Nakajima, Y. 2023. BabyAGI. https://github.com/yoheinakajima/babyagi

Nakano, R.; Hilton, J.; Balaji, S. A.; Wu, J.; Ouyang, L.; Kim, C.; Hesse, C.; Jain, S.; Kosaraju, V.; Saunders, W.; Jiang, X.; Cobbe, K.; Eloundou, T.; Krueger, G.; Button, K.; et al. 2021. WebGPT: Browser-assisted question-answering with human feedback. arXiv preprint.

OpenAI. 2023. GPT-4 Technical Report.

Ouyang, L.; Wu, J.; Jiang, X.; Almeida, D.; Wainwright, C.; Mishkin, P.; Zhang, C.; Agarwal, S.; Slama, K.; Ray, A.; Schulman, J.; Hilton, J.; Kelton, F.; Miller, L.; Simens, M.; Askell, A.; Welinder, P.; Christiano, P. F.; Leike, J.; and Lowe, R. 2022. Training Language Models to Follow Instructions with Human Feedback. NeurIPS.

Park, J. S.; O’Brien, J.; Cai, C. J.; Morris, M. R.; Liang, P.; and Bernstein, M. S. 2023. Generative Agents: Interactive Simulacra of Human Behavior. In ACM Symposium on User Interface Software and Technology.

Petroni, F.; Rocktäschel, T.; Riedel, S.; Lewis, P.; Bakhtin, A.; Wu, Y.; and Miller, A. 2019. Language Models as Knowledge Bases? In EMNLP-IJCNLP. Association for Computational Linguistics.

Qian, C.; Cong, X.; Yang, C.; Chen, W.; Su, Y.; Xu, J.; Liu, Z.; and Sun, M. 2023. Communicative Agents for Software Development. arXiv:2307.07924.

Rubin, O.; Herzig, J.; and Berant, J. 2022. Learning To Retrieve Prompts for In-Context Learning. In NAACL. Association for Computational Linguistics.

Schaul, T.; Quan, J.; Antonoglou, I.; and Silver, D. 2015. Prioritized Experience Replay. In ICLR.

Shaw, P.; Joshi, M.; Cohan, J.; Berant, J.; Pasupat, P.; Hu, H.; Khandelwal, U.; Lee, K.; and Toutanova, K. 2023. From Pixels to UI Actions: Learning to Follow Instructions via Graphical User Interfaces. NeurIPS.

Shinn, N.; Cassano, F.; Gopinath, A.; Narasimhan, K. R.; and Yao, S. 2023. Reflexion: Language Agents with Verbal Reinforcement Learning. In NeurIPS.

Shridhar, M.; Yuan, X.; Côté, M.-A.; Bisk, Y.; Trischler, A.; and Hausknecht, M. 2021. ALFWorld: Aligning Text and Embodied Environments for Interactive Learning. In ICLR.

Significant-Gravitas. 2023. AutoGPT. https://github.com/Significant-Gravitas/Auto-GPT

Song, K.; Tan, X.; Qin, T.; Lu, J.; and Liu, T.-Y. 2020. MPNet: Masked and Permuted Pre-training for Language Understanding. NeurIPS.

Sumers, T. R.; Yao, S.; Narasimhan, K.; and Griffiths, T. L. 2023. Cognitive Architectures for Language Agents. arXiv preprint.

Sun, H.; Zhuang, Y.; Kong, L.; Dai, B.; and Zhang, C. 2023. AdaPlanner: Adaptive Planning from Feedback with Language Models. NeurIPS.

Sutton, R. S.; and Barto, A. G. 2018. Reinforcement Learning: An Introduction. MIT press.

Taori, R.; Gulrajani, I.; Zhang, T.; Dubois, Y.; Li, X.; Guestrin, C.; Liang, P.; and Hashimoto, T. B. 2023. Stanford Alpaca: An Instruction-Following LLaMA Model. https://github.com/tatsu-lab/stanford_alpaca

Thorne, J.; Vlachos, A.; Christodoulopoulos, C.; and Mittal, A. 2018. FEVER: a Large-scale Dataset for Fact Extraction and VERification. In NAACL.

Thoppilan, R.; De Freitas, D.; Hall, J.; Shazeer, N.; Kulshreshtha, A.; Cheng, H.-T.; Jin, A.; Bos, T.; Baker, L.; Du, Y.; et al. 2022. LaMDA: Language Models for Dialog Applications. arXiv preprint.

Touvron, H.; Lavril, T.; Izacard, G.; Martinet, X.; Lachaux, M.-A.; Lacroix, T.; Rozière, B.; Goyal, N.; Hambro, E.; Azhar, F.; et al. 2023a. LLaMA: Open and Efficient Foundation Language Models. arXiv preprint.

Touvron, H.; Martin, L.; Stone, K.; Albert, P.; Almahairi, A.; Babaei, Y.; Bashlykov, N.; Batra, S.; Bhargava, P.; Bhosale, S.; et al. 2023b. Llama 2: Open Foundation and Fine-Tuned Chat Models. arXiv preprint.

Tworkowski, S.; Staniszewski, K.; Pacek, M.; Wu, Y.; Michalewski, H.; and Miłos, P. 2023. Focused Transformer: Contrastive Training for Context Scaling. In NeurIPS.

Wang, G.; Xie, Y.; Jiang, Y.; Mandlekar, A.; Xiao, C.; Zhu, Y.; Fan, L.; and Anandkumar, A. 2023a. Voyager: An Open-Ended Embodied Agent with Large Language Models. arXiv preprint.

Wang, L.; Ma, C.; Feng, X.; Zhang, Z.; Yang, H.; Zhang, J.; Chen, Z.; Tang, J.; Chen, X.; Lin, Y.; et al. 2023b. A Survey on Large Language Model Based Autonomous Agents. arXiv preprint.

Wang, L.; Yang, N.; and Wei, F. 2023. Learning to Retrieve In-Context Examples for Large Language Models. arXiv preprint.

Wang, S.; Liu, C.; Zheng, Z.; Qi, S.; Chen, S.; Yang, Q.; Zhao, A.; Wang, C.; Song, S.; and Huang, G. 2023c. Avalon’s Game of Thoughts: Battle Against Deception through Recursive Contemplation. arXiv preprint.

Watkins, C. J.; and Dayan, P. 1992. Q-learning. Machine learning.

Wei, J.; Bosma, M.; Zhao, V.; Guu, K.; Yu, A. W.; Lester, B.; Du, N.; Dai, A. M.; and Le, Q. V. 2022a. Finetuned Language Models are Zero-Shot Learners. In ICLR.

Wei, J.; Wang, X.; Schuurmans, D.; Bosma, M.; Xia, F.; Chi, E.; Le, Q. V.; Zhou, D.; et al. 2022b. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. NeurIPS.

Wu, J.; Antonova, R.; Kan, A.; Lepert, M.; Zeng, A.; Song, S.; Bohg, J.; Rusinkiewicz, S.; and Funkhouser, T. 2023. TidyBot: Personalized Robot Assistance with Large Language Models. Autonomous Robots.

Xi, Z.; Chen, W.; Guo, X.; He, W.; Ding, Y.; Hong, B.; Zhang, M.; Wang, J.; Jin, S.; Zhou, E.; et al. 2023. The Rise and Potential of Large Language Model Based Agents: A Survey. arXiv preprint.

Yang, S.; Nachum, O.; Du, Y.; Wei, J.; Abbeel, P.; and Schuurmans, D. 2023a. Foundation Models for Decision Making: Problems, Methods, and Opportunities. arXiv preprint.

Yang, Z.; Li, L.; Wang, J.; Lin, K.; Azarnasab, E.; Ahmed, F.; Liu, Z.; Liu, C.; Zeng, M.; and Wang, L. 2023b. MM-REACT: Prompting ChatGPT for Multimodal Reasoning and Action. arXiv preprint.

Yang, Z.; Qi, P.; Zhang, S.; Bengio, Y.; Cohen, W.; Salakhutdinov, R.; and Manning, C. D. 2018. HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering. In EMNLP. Association for Computational Linguistics.

Yao, S.; Chen, H.; Yang, J.; and Narasimhan, K. 2022. WebShop: Towards Scalable Real-World Web Interaction with Grounded Language Agents. In NeurIPS.

Yao, S.; Yu, D.; Zhao, J.; Shafran, I.; Griffiths, T. L.; Cao, Y.; and Narasimhan, K. 2023a. Tree of Thoughts: Deliberate Problem Solving with Large Language Models. NeurIPS.

Yao, S.; Zhao, J.; Yu, D.; Du, N.; Shafran, I.; Narasimhan, K.; and Cao, Y. 2023b. ReAct: Synergizing Reasoning and Acting in Language Models. In ICLR.

Yao, W.; Heinecke, S.; Niebles, J. C.; Liu, Z.; Feng, Y.; Xue, L.; Murthy, R.; Chen, Z.; Zhang, J.; Arpit, D.; Xu, R.; Mui, P.; Wang, H.; Xiong, C.; and Savarese, S. 2023c. Retroformer: Retrospective Large Language Agents with Policy Gradient Optimization.

Yue, Y.; Kang, B.; Ma, X.; Huang, G.; Song, S.; and Yan, S. 2023. Offline Prioritized Experience Replay. arXiv preprint.

Zeng, A.; Liu, M.; Lu, R.; Wang, B.; Liu, X.; Dong, Y.; and Tang, J. 2023. AgentTuning: Enabling Generalized Agent Abilities for LLMs. arXiv preprint.

Zhang, Z.; Zhang, A.; Li, M.; and Smola, A. 2023. Automatic Chain of Thought Prompting in Large Language Models. In ICLR.

Zhao, A.; Zhu, E.; Lu, R.; Lin, M.; Liu, Y.-J.; and Huang, G. 2023a. Augmenting Unsupervised Reinforcement Learning with Self-Reference. arXiv preprint.

Zhao, W. X.; Zhou, K.; Li, J.; Tang, T.; Wang, X.; Hou, Y.; Min, Y.; Zhang, B.; Zhang, J.; Dong, Z.; et al. 2023b. A Survey of Large Language Models. arXiv preprint.

Zhuang, F.; Qi, Z.; Duan, K.; Xi, D.; Zhu, Y.; Zhu, H.; Xiong, H.; and He, Q. 2020. A Comprehensive Survey on Transfer Learning. Proceedings of the IEEE.

Zitkovich, B.; Yu, T.; Xu, S.; Xu, P.; Xiao, T.; Xia, F.; Wu, J.; Wohlhart, P.; Welker, S.; Wahid, A.; et al. 2023. RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control. In CoRL. PMLR.

---

## Appendix

### A Detailed Related Works（附录 A：相关工作详解）

**A.1 Prompt-based Learning**  
Prompt-based learning 是一种范式：原本从 context \(c\) 输出 label \(y\) 的语言模型，在修改后的 context \(\hat{c}\) 上于 label prediction 任务中得到改进（Liu et al. 2023a）。该框架很有吸引力，因其使得可以使用在海量文本上预训练的 LLM。此外，新的 prompting 函数支持 few-shot 或 zero-shot learning，从而以极少或无标注数据快速适应任务。具体地，**tuning-free prompting** 直接使用预训练语言模型的 prompt 生成答案而不改变其参数。该方法可通过 answered prompts 增强，该策略称为 **in-context learning**（Brown et al. 2020）。例子包括 LAMA（Petroni et al. 2019）、GPT-3（Brown et al. 2020）与 CoT（Wei et al. 2022b）。其益处包括高效、无参数更新、避免 catastrophic forgetting、以及适用于 zero/few-shot 设定。然而，它需要精细的 prompt engineering 与领域知识专长以提高准确率。AutoPrompt、Zero-shot-CoT（Kojima et al. 2022; Zhang et al. 2023）等工作通过为 NLP reasoning 任务自动生成 reasoning chains 来减轻工程师负担。同样，ExpeL agent 在 sequential decision-making tasks 中自动收集 experiences、生成自身 insights，并将这些 insights 与成功的 in-context examples 一起用于决策，从而减轻 heavy manual prompt engineering 与 expert domain knowledge 的要求。

**A.2 Retrieval Augmented Generation**  
Retrieval augmented generation 已广为流行，有助于减少 hallucination 并使 LLM 访问内部数据库（Li et al. 2022）。NLP 领域若干工作已证明从 gold demonstrations 数据库检索 in-context examples 的有效性（Wang, Yang, and Wei 2023; Rubin, Herzig, and Berant 2022）。相反，我们的工作探索 LLM agents 从**自身生成的 experiences** 中检索，从而减轻用户工程努力与领域专长负担。

**A.3 LLM Agents**  
使用 LLM 作为 agent “大脑”的研究近年激增。LLM agents 已在诸多领域实例化，例如机器人学（Ha, Florence, and Song 2023; Zitkovich et al. 2023; Mu et al. 2023; Mirchandani et al. 2023; Wu et al. 2023）、自然科学（Bran et al. 2023; Boiko, MacKnight, and Gomes 2023）与自动化工作流（Yang et al. 2023b; Gur et al. 2023）。这些工作多数利用 LLM 的强 commonsense knowledge，以 zero 或 few-shot 方式完成下游任务，以保持 LLM 的强 world knowledge priors。我们的 ExpeL agent 同样利用 LLM 的强大 world knowledge。具体地，我们在 gathering experience、extracting insights 与 downstream execution 步骤中使用 LLM。

**Planning：** LLM 已展示在 embodied environments 中以 zero-shot 方式规划的能力（Huang et al. 2022）。然而许多工作表明，通过提升 reasoning 能力可进一步增强 LLM 的规划能力（Yao et al. 2023a; Wei et al. 2022b）。ReAct agent（Yao et al. 2023b）展示了 reasoning 与 acting 的结合。该方法不仅被证明在多种场景下优于仅输出 actions 的 agents，还提供了对 agent 行动时“在想什么”的洞察。因其简洁有效，我们采用 ReAct 作为 base planning algorithm。

**Self-improvement：** 一类方法利用 LLM 基于环境 feedback 进行 self-reflect 的能力，相较没有“第二次做任务”意识的算法表现更优（Shinn et al. 2023; Liu, Bahety, and Song 2023）。特别地，Reflexion agent（Shinn et al. 2023）基于失败 trajectory/环境 feedback 对任务失败原因给出 verbal hypothesis，并在第二次机会时改进。然而，self-reflecting 方法假设任务可重复，且 test time 可获得环境 feedback。此外，self-reflection 方法是无状态的，无法学习 cross-task insights。相反，我们的方法利用 Reflexion 的长处，用它收集更多失败/成功 trajectories 以从中提取 insights，并在 test time 表现更好。Voyager（Wang et al. 2023a）等工作在 Minecraft 等特定环境中探索了 skill learning。

**Memory Mechanisms：** 具有持久 long-term memory 的 agents 在多 agent 设定中展现了令人振奋的结果（Park et al. 2023; Maas et al. 2023; Qian et al. 2023）。这些工作通常有多个 generative agents 实例彼此交互，模拟人类社会或虚构设定。在 generative agents（Park et al. 2023）中，agents 具备 memory 机制，可基于 recency、relevance 与 importance 检索信息，颇似人类在一天中会引用并关联不同记忆。这类工作通常是 open-ended 的，而 ExpeL agents 面向 task-solving。与 generative agents 类似，我们的工作也使用 memory：成功的 in-context examples 与提取的 insights 作为 condensed memory，二者均来自 agent 自身 experience。

**A.4 Reinforcement Learning**  
我们的 agent 自主收集 experience，令人联想到 online reinforcement learning 方法（Sutton and Barto 2018）。尤其我们的方法使用 **off-policy learning**（Watkins and Dayan 1992）：policy 在 experience gathering 时使用 Reflexion，并通过 insight extraction 与将相似任务检索为 in-context examples 实现 policy improvement。具体地，retrieval 步骤类似于 **experience replay**（Lin 1992），已有研究探讨应选择哪些 examples 给 agent 用于训练（Schaul et al. 2015; Yue et al. 2023）。然而，与这些现有方法不同，ExpeL **不需要**访问 model parameters、设计复杂的 reward 或 loss 函数，或大量 environment interactions。

### B Broader Impacts

本研究聚焦 LLM agents。若这些自主程序被赋予互联网访问，存在造成意外伤害的风险。但 RLHF 等技术可能缓解这些不利影响（Nakano et al. 2021; Ouyang et al. 2022）。

### C Computational Resources

所有实验在一台台式机上完成：Intel(R) Core(TM) i9-9900K CPU @ 3.60GHz，16 核，64GB RAM，单块 NVIDIA GeForce RTX 2080 Ti。

### D Environment Details

**D.1 Evaluation Task Set**  
所有实验采用 **four-fold validation**。在一半数据上训练、另一半评估，反之亦然。所有结果包含各 fold 的均值与标准误。HotpotQA：使用 HotpotQA distractor dev split 中 100 个 validation tasks（与 ReAct、Reflexion 相同）。ALFWorld：134 个可解任务（与 ReAct、Reflexion 相同）。WebShop：100 个任务（与 ReAct、Reflexion 相同）。

**D.2 Prompts / Fewshot Examples**  
在相应阶段使用与 ReAct、Reflexion（Yao et al. 2023b; Shinn et al. 2023）相同的 fewshot examples/prompts。WebShop 额外增加一个 fewshot，使环境有两个 fewshot examples。Prompt templates 见 Appendix F；代码将公开。

**D.3 WebShop Environment Specific Detail**  
我们对 https://github.com/princeton-nlp/WebShop 上的 WebShop 环境略作修改，目标是使每次实验实例 **deterministic**。原版中商品价格与指令中的价格约束由均匀区间抽样生成；我们改用**平均值**。平均而言结果应接近原版实现，但保证不同实例间一致性以便复现。最后将每页 items 从 3 增至 10，因近期 LLM context window 增大可容纳更多 observations。

**D.4 WebShop Reward Function**  
WebShop（Yao et al. 2022）引入的另一指标为 reward function，将期望产品属性与所购产品属性之间的相似度映射为 0 到 1 的值：

\[
r = \frac{|U_{\text{att}} \cap Y_{\text{att}}| + |U_{\text{opt}} \cap Y_{\text{opt}}| + \mathbb{I}[y_{\text{price}} \le u_{\text{price}}]}{|U_{\text{att}}| + |U_{\text{opt}}| + 1} \cdot r_{\text{type}}
\tag{1}
\]

其中 \(r_{\text{type}}\) 按 **TextMatch** 分段定义为（原文 Eq. (2)）：

\[
r_{\text{type}} = \begin{cases}
0, & \text{if TextMatch} = 0 \\
0.1, & \text{if TextMatch} < 0.1 \\
0.5, & \text{if TextMatch} \le 0.2 \text{ and query not match and category not match} \\
1, & \text{otherwise}
\end{cases}
\]

因单次 query 可对应多个合适商品，WebShop 使用 matching reward 评估。**TextMatch** 表示所选商品标题与目标商品标题之间代词、名词与专有名词的文本重叠（Liu et al. 2023b）。

**D.5 Base Language Model**  
所有实验使用 Langchain（Chase 2023）调用 OpenAI API。Experience gathering 中的 Reflexion 使用 **gpt-3.5-turbo-0613**，超出 context window 时使用 **gpt-3.5-turbo-16k-0613**。Insight extraction 使用 **gpt-4-0613**。Evaluation stage 所有 agents 使用 **gpt-3.5-turbo-0613**。实验时间为 2023 年 7 月 10 日至 2023 年 8 月 10 日。

### E Environment, Agent, Retrieval Parameters

与原文 **Table 4: Environment, Retrieval and Agent Parameters** 对齐如下。

**Retrieval Parameters**

| Parameter | Value |
|-----------|-------|
| Vectorstore | Faiss |
| Retriever type | kNN |
| Embedder | all-mpnet-base-v2 |

**Agent Hyperparameters**

| Parameter | Value |
|-----------|-------|
| Max Reflection Retries | 3 |
| Reflection LLM | gpt-3.5-turbo-0613 |
| Policy LLM | gpt-3.5-turbo-0613 |
| Insight Extraction LLM | gpt-4-0613 |
| Decoding Temperature | 0 |
| Decoding Strategy | greedy |

**HotpotQA-specific Parameters**

| Parameter | Value |
|-----------|-------|
| Number of Success Examples in Insight Extraction \(L\) | 8 |
| Max Number of Environment Steps \(H\) | 7 |
| Max Number of Fewshot Examples \(k\) | 6 |
| Max Number of Reflection Fewshot Examples \(k_{\text{reflections}}\) | 2 |

**WebShop-specific Parameters**

| Parameter | Value |
|-----------|-------|
| Number of Success Examples in Insight Extraction \(L\) | 4 |
| Max Number of Environment Steps \(H\) | 15 |
| Max Number of Fewshot Examples \(k\) | 2 |
| Max Number of Reflection Fewshot Examples \(k_{\text{reflections}}\) | 2 |
| Searched items per page | 10 |

**ALFWorld-specific Parameters**

| Parameter | Value |
|-----------|-------|
| Number of Success Examples in Insight Extraction \(L\) | 8 |
| Max Number of Environment Steps \(H\) | 20 |
| Max Number of Fewshot Examples \(k\) | 2 |
| Max Number of Reflection Fewshot Examples \(k_{\text{reflections}}\) | 2 |

**FEVER-specific Parameters**

| Parameter | Value |
|-----------|-------|
| Max Number of Environment Steps \(H\) | 7 |
| Max Number of Fewshot Examples \(k\) | 3 |

### F–J（Figures, Example Insights, Trajectories, Additional Results）

原文 **Appendix F**（Policy/Actor Prompt Templates）、**G**（Example Insights）、**H**（Emergent Abilities）、**I**（Example Trajectories）、**J**（Additional Quantitative Results）以图表为主；文字说明已在上文相应章节译出。**Table 6** 全表见上文；**Fig. 25–27** 为训练/评估结果分解图（标题见 `ExpeL_clean.txt`）。

**Table 5（环境分项得分，与原文一致）**

| Benchmark | Env.Name | Gradient-based IL | Prompt-based Act | ReAct | ExpeL(insights) | ExpeL(retrieve) | ExpeL(ours) |
|-----------|----------|-------------------|------------------|-------|-----------------|-----------------|-------------|
| ALFWorld (SR%) | put | 46 | 46 | 50 | 61 | 73 | 83 |
| | clean | 39 | 39 | 61 | 87 | 74 | 74 |
| | heat | 74 | 4 | 13 | 12 | 43 | 43 |
| | cool | 100 | 48 | 71 | 76 | 71 | 67 |
| | look | 22 | 11 | 0 | 0 | 17 | 39 |
| | puttwo | 24 | 6 | 0 | 29 | 29 | 29 |
| WebShop (\(r_{\text{score}}\)) | shop | 0.599 | 0.666 | 0.665 | 0.675 | 0.67 | 0.701 |

*Table 5: Environment-Specific Scores. ALFWorld 按环境名称分解的 success rate 与 WebShop 按环境的平均 reward（reward 函数见 Appendix D.4）。*

**Table 6（Additional Statistical Metrics，与 `ExpeL_clean.txt` 第 1091–1132 行逐值对齐）**

每条 trajectory 上的平均统计；所有字符串使用 tiktoken（https://github.com/openai/tiktoken）分词。

| Metric | Method | HotpotQA | ALFWorld | WebShop |
|--------|--------|----------|----------|---------|
| Number of thoughts | Act | 0.0 | 0.0 | 0.0 |
| Number of thoughts | ReAct | 5.19 | 8.96 | 3.08 |
| Number of thoughts | Insights-only | 5.28 | 7.57 | 3.26 |
| Number of thoughts | Retrieve-only | 4.65 | 7.9 | 2.91 |
| Number of thoughts | ExpeL | 5.02 | 8.16 | 3.2 |
| Number of actions | Act | 5.08 | 11.13 | 4.32 |
| Number of actions | ReAct | 5.18 | 14.82 | 4.47 |
| Number of actions | Insights-only | 5.04 | 14.0 | 4.72 |
| Number of actions | Retrieve-only | 4.63 | 13.08 | 4.24 |
| Number of actions | ExpeL | 4.8 | 14.3 | 4.33 |
| Number of observations | Act | 5.08 | 23.37 | 4.37 |
| Number of observations | ReAct | 5.19 | 20.01 | 7.68 |
| Number of observations | Insights-only | 5.12 | 18.1 | 8.05 |
| Number of observations | Retrieve-only | 4.63 | 17.22 | 7.55 |
| Number of observations | ExpeL | 4.87 | 18.32 | 7.56 |
| Number of invalid actions | Act | 0.0 | 6.25 | 0.16 |
| Number of invalid actions | ReAct | 0.0 | 2.84 | 0.42 |
| Number of invalid actions | Insights-only | 0.01 | 2.34 | 0.26 |
| Number of invalid actions | Retrieve-only | 0.01 | 1.95 | 0.61 |
| Number of invalid actions | ExpeL | 0.03 | 2.32 | 0.35 |
| Tokens | Act | 1920.48 | 1498.63 | 2191.57 |
| Tokens | ReAct | 1319.75 | 2051.49 | 2575.41 |
| Tokens | Insights-only | 3525.7 | 2790.05 | 3224.95 |
| Tokens | Retrieve-only | 3609.43 | 2190.35 | 2889.57 |
| Tokens | ExpeL | 4310.06 | 2856.7 | 3291.31 |
| Thought tokens | Act | 0.0 | 0.0 | 0.0 |
| Thought tokens | ReAct | 192.51 | 282.28 | 116.41 |
| Thought tokens | Insights-only | 231.48 | 241.62 | 118.8 |
| Thought tokens | Retrieve-only | 176.71 | 260.27 | 103.52 |
| Thought tokens | ExpeL | 212.13 | 262.66 | 111.51 |
| Action tokens | Act | 58.79 | 81.19 | 43.8 |
| Action tokens | ReAct | 68.07 | 104.14 | 45.33 |
| Action tokens | Insights-only | 71.4 | 98.98 | 50.39 |
| Action tokens | Retrieve-only | 60.34 | 93.75 | 44.35 |
| Action tokens | ExpeL | 66.41 | 100.78 | 44.99 |
| Observation tokens | Act | 445.72 | 416.46 | 41.52 |
| Observation tokens | ReAct | 625.46 | 393.16 | 58.27 |
| Observation tokens | Insights-only | 560.42 | 384.54 | 58.97 |
| Observation tokens | Retrieve-only | 496.69 | 376.1 | 56.66 |
| Observation tokens | ExpeL | 547.23 | 393.19 | 57.23 |

*Table 6: Additional Statistical Metrics. Average counts per trajectory for each benchmark.*

---

## Figures（图题译文，与原文一一对应）

- **Figure 1：** ExpeL Agent 概览。左：ExpeL 分三阶段运行：(1) 将成功与失败 experiences 收集入池；(2) 从这些 experiences 中提取/抽象跨任务 knowledge；(3) 在 evaluation tasks 中应用所得 insights 并回忆过去成功。右：(A) 说明通过 Reflexion（Shinn et al. 2023）进行 experience gathering 的过程，在失败上 self-reflection 后可重试任务。(B) 说明 insight extraction 步骤。当给定 success/failure pairs 或长度为 \(L\) 的成功列表时，agent 用操作 **ADD**、**UPVOTE**、**DOWNVOTE**、**EDIT** 动态修改已有 insights 列表 \(\hat{\iota}\)。该过程强调提取普遍失败模式或 best practices。

- **Figure 2：** Insight Extraction Prompt Template。ExpeL agents 用于 insight extraction 的 prompt template。同一 template 既用于 success/fail pairs（A，黄色）也用于 \(L\) 个成功（B，绿色）。

- **Figure 3：** Task Inference Prompt Template。展示 evaluation 时 ExpeL 的 prompt template。白底区域与 base ReAct agent 的输入相同。差异为（紫色区域）额外包含从过去 experience 提取的 insights，以及基于 task similarity 从过去 experiences **动态检索**的成功 in-context examples。

- **Figure 4：** Transfer Learning Finetuning Prompt Template。用于将知识从 source 到 target domain 进行 finetune 的 prompt template。灰色高亮处应以任务的简洁描述格式化。

- **Figure 5：** Main Results。三个不同领域上的平均任务 success rates（灰色箭头为标准误）：HotpotQA、ALFWorld、WebShop。ReAct 与 Act 作为 baselines。ExpeL 在所有领域上持续优于 baselines，凸显从 experience 学习的重要性。此外将 ExpeL 与 ExpeL（retrieve-only）和 ExpeL（insights-only）比较，以说明 insight extraction 与 task similarity retrieval 均必要且协同。

- **Figure 6：** Effects of Experience on Performance。强调多样化 experience 样本数量与最终性能的相关性。具体比较 ExpeL 与 (1) ReAct；(2) 仅有 fewshot examples 的 ExpeL；(3) experience gathering 步骤仅使用 ReAct 的 ExpeL。可见**额外自主收集的 experiences** 对 ExpeL 成功至关重要，且用 Reflexion 收集的 success/failure 数据多样性优于仅用 ReAct。

---

## Algorithms（算法 1–3，符号与原文一致）

### Algorithm 1: ExpeL-Experience Gathering

```
Initialize:
  Policy LLM: LLM_ReAct
  Self-reflection model: LLM_reflect
  Collection of tasks: T_train
  Fewshot examples: F_manual
  Experience pool: B ← F_manual
  Number of training tasks: N
  Maximum retry number: Z
  Maximum step number: H
  Current task index: n ← 1

while task n ≤ N do
  t_n ← T_train[n]
  Reflection: ν_{n,0} ← ""
  for trial z = 0 to Z do
    o_0 ← env.reset(t_n)
    Initialize trajectory: τ_{n,z} ← o_0
    for timestep i = 0 to H do
      a_i ← LLM_ReAct(a_i | τ_{n,z}, F_manual, ν_{n,z})
      o_{i+1}, r_{i+1}, done ← env.step(a_i)
      τ_{n,z} ← τ_{n,z} ∪ {(o_i, a_i, o_{i+1}, r_{i+1})}
      if done then break
    end for
    B ← B ∪ τ_{n,z}
    if done or z = Z then
      n ← n + 1
      break
    else
      ν_{n,z+1} ← concat(ν_{n,z} + LLM_reflect(τ_{n,z}))
    end if
  end for
end while
return B
```

### Algorithm 2: ExpeL-Insight Extraction

```
Initialize:
  Experience pool B (from Alg. 1)
  Insight extraction model: LLM_insights
  Set of insights: î ← ∅

Divide the successes in B into L-sized chunks:
  C_success = { {τ^success_1, …, τ^success_L}, {τ^success_{L+1}, …, τ^success_{2L}}, … }

Construct fail/success tuples of the same tasks in B:
  C_compare = { (τ^success_1, τ^fail_{1,0}), (τ^success_1, τ^fail_{1,1}), …, (τ^success_2, τ^fail_{2,0}), … }

for each c in C_compare do
  î ← LLM_insights(c, î)
end for

for each c in C_success do
  î ← LLM_insights(c, î)
end for

return î
```

### Algorithm 3: ExpeL-Evaluation

```
Initialize:
  ExpeL agent LLM: LLM_ExpeL
  Text Embedder: E
  Experience pool B (from Alg. 1)
  Set of insights î (from Alg. 2)
  Collection of evaluation tasks: T_evaluation
  Number of evaluation tasks: M
  Number of fewshots: k
  Number of successes: S ← 0

for task m = 1 to M do
  t_m ← T_evaluation[m]
  o_0 ← env.reset(t_m)
  Initialize trajectory: τ_m ← o_0
  F_similar_tasks ← Faiss(t_m, B, E, k)
  for timestep i = 1 to H do
    a_i ← LLM_ExpeL(a_i | τ_m, F_similar_tasks, î)
    o_{i+1}, r_{i+1}, done ← env.step(a_i)
    τ_m ← τ_m ∪ {(o_i, a_i, o_{i+1}, r_{i+1})}
    if done then break
  end for
  if r_{i+1} = 1 then
    S ← S + 1
  end if
end for

return S_M
```

---

*本文件由 `ExpeL_clean.txt` 与 `ExpeL_tables.json` 对照翻译；Figure、Table、公式编号与 AAAI 原稿一致。参考文献条目以英文著录；正文为中文并保留技术术语英文。*
