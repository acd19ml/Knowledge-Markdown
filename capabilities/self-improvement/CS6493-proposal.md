## Topic 6 - From Verbal Reflection to Experiential Learning: Reproducing and Comparing Reflexion and ExpeL

> 💡 **【选题解析】**
>
> - **中文题目**: 从语言反思到经验学习——复现并对比 Reflexion 与 ExpeL 两条自我进化路线
> - **技术背景分析**: 当前 LLM Agent 在多步决策任务中无法从历史经验中学习，每次执行都从零出发。本课题聚焦"无参数更新的 Agent 自我改进"这一前沿方向，沿一条清晰的技术演化主线展开：**Reflexion**（Shinn et al., NeurIPS 2023）让 Agent 在单任务失败后生成语言反思并写入本轮记忆；**ExpeL**（Zhao et al., AAAI 2024）将这一机制升级为跨任务经验池——把历次成功/失败轨迹抽象成可检索的 insight，在新任务推理时注入。两篇论文使用同一套 benchmark（ALFWorld、HotpotQA），天然适合在统一实验框架下做对比分析，研究问题明确：**跨任务经验积累在单任务语言反思的基础上，究竟能带来多大提升？**
> - **潜在的技术解决方案**:
>   1. **Reflexion 复现**: 基于公开代码库（`noahshinn/reflexion`）在 ALFWorld 和 HotpotQA 上复现三层架构（Actor / Evaluator / Self-Reflection），建立单任务语言反思基线。
>   2. **ExpeL 复现与扩展**: 基于公开代码库（`LeapLabTHU/ExpeL`）复现跨任务经验池机制（experience gathering → insight extraction → task-similarity retrieval），并在相同 benchmark 上与 Reflexion 直接对比。
>   3. **对比分析与消融**: 统一评测协议下，量化"跨任务 insight + 轨迹检索"在单任务反思基础上的增益；消融检索策略（task similarity vs random）和 insight 生成模型（GPT-4o-mini vs Llama-3）的影响。
>   4. **适合团队类型**: 适合以 API 调用为主要计算手段、希望训练研究实验设计能力的团队。两套代码库均开源，无需 GPU，Colab + OpenAI / Groq 免费 API 即可完成全部实验。

LLM-based agents have shown strong performance on multi-step decision-making tasks. However, a fundamental limitation remains: most agents are **stateless across tasks** — they neither retain knowledge from prior failures nor accumulate reusable insights over time. Two lines of work address this at different levels of granularity. **Reflexion** (Shinn et al., NeurIPS 2023) introduces verbal reinforcement learning, enabling an agent to reflect on a single-task failure in natural language and store that reflection in a short-term memory buffer for use in the next attempt. **ExpeL** (Zhao et al., AAAI 2024) takes this further: it maintains a persistent cross-task experience pool, extracts generalizable insights from accumulated success/failure trajectories, and retrieves the most task-relevant examples at inference time — achieving cross-task transfer without any parameter updates.

Because both systems are evaluated on the same benchmarks (ALFWorld, HotpotQA), this project offers a unique opportunity to reproduce and directly compare the two paradigms under a unified experimental protocol. The central research question is:

> *What does cross-task experiential learning (ExpeL) add over single-task verbal reflection (Reflexion), and under what conditions does the gap widen or narrow?*

You are encouraged to:

1. **Reproduce Reflexion** as the single-task reflection baseline on two benchmarks:
  - **ALFWorld**: A text-based household planning environment (134 tasks across 6 types). Primary metric: success rate (SR%) across three retry rounds (R1/R2/R3) and a single-attempt proxy (R0).
  - **HotpotQA**: Multi-hop open-domain QA. Primary metrics: exact match (EM) and F1 score.
   Faithfully implement the three-component architecture: an **Actor** generating actions from context and memory, an **Evaluator** providing binary success signals, and a **Self-Reflection** module producing a verbal summary written into a sliding-window buffer. Report results with and without reflection enabled.
2. **Reproduce ExpeL** and compare against the Reflexion baseline on the same benchmarks:
  - Implement the three-phase pipeline: (a) **experience gathering** using Reflexion-style retries to collect success/failure trajectory pairs; (b) **insight extraction** via structured LLM operations (ADD/EDIT/UPVOTE/DOWNVOTE) over the trajectory pool; (c) **task inference** by jointly injecting retrieved top-*k* similar successful trajectories and the ranked insight set into the agent prompt.
  - Report the incremental gain of ExpeL over Reflexion in both single-attempt (R0) and multi-attempt (R3) settings, to separate cross-task memory benefit from online retry benefit.
3. **Extend with controlled analysis** along the following dimensions:
  - **Retrieval strategy ablation**: Compare task-similarity ranking (ExpeL default) against random retrieval and reasoning-similarity ranking on ALFWorld, reproducing the finding in Table 3 of the original paper and evaluating whether the same ranking holds across LLM backends.
  - **Cross-model generalization**: Run both systems using at least two LLM backends (e.g., GPT-4o-mini via OpenAI API and Llama-3.3-70B via Groq free API). Investigate whether weaker models benefit more or less from cross-task experience, and whether insight quality degrades with smaller models.
  - **Failure mode taxonomy**: Classify agent failures across both systems into categories (e.g., planning error, hallucinated action, reflection-not-followed, insight-retrieval mismatch) to characterize what each mechanism succeeds and fails to fix.

> **Hint**: ALFWorld evaluation is computationally light (text-only environment). Use the Groq API free tier for Llama-3.3-70B inference. Limit each experimental run to 50–80 ALFWorld tasks and 200–300 HotpotQA samples to control API token consumption. ExpeL's experience pool can be seeded with a small training split (50–100 tasks) before evaluation begins.

### References

1. Shinn N, Cassano F, Labash A, et al. Reflexion: Language agents with verbal reinforcement learning. *Advances in Neural Information Processing Systems*, 2023, 36.
2. Zhao A, Huang D, Xu Q, et al. ExpeL: LLM agents are experiential learners. *Proceedings of the AAAI Conference on Artificial Intelligence*, 2024, 38(17): 19632–19642.
3. Shridhar M, Yuan X, Côté M A, et al. ALFWorld: Aligning text and embodied environments for interactive learning. *International Conference on Learning Representations*, 2021.
4. Yang Z, Qi P, Zhang S, et al. HotpotQA: A dataset for diverse, explainable multi-hop question answering. *Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing*, 2018.
5. Yao S, Zhao J, Yu D, et al. ReAct: Synergizing reasoning and acting in language models. *International Conference on Learning Representations*, 2023.
6. Madaan A, Tandon N, Gupta P, et al. Self-refine: Iterative refinement with self-feedback. *Advances in Neural Information Processing Systems*, 2024, 36.

