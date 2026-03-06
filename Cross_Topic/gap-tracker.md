# 全局 Research Gap 追踪 — 跨综述分层视角 v2

> **三层分类**：
> - **A类**：跨领域交叉 Gap —— 领域 X 的技术未被应用到领域 Y。竞争者少，发表价值最高。
> - **B类**：单领域问题 + 另一领域有成熟解答。需验证移植有效性，工作量可控。
> - **C类**：单领域内残留问题，无跨领域连接需求。
>
> **格式版本**：v2（per-gap 详细条目 + 证据来源标注）
> **参考文件**：
> - 矩阵：[comparison-matrix.md](comparison-matrix.md)
> - GUI Agent 细节：[../GUI_Agent/README.md](../GUI_Agent/README.md)
> - taxonomy 与主线：[taxonomy-draft.md](taxonomy-draft.md) | [main-line.md](main-line.md)

---

## A 类 Gap：跨领域交叉（最高价值）

### A-1: GUI Agent 的程序性记忆机制（Procedural Memory for GUI）

**Status**: `精读确认`

**Statement**: GUI Agent 探索阶段积累的操作序列知识以原始列表存储，无法归纳为可复用的跨任务（尤其是跨 App）技能，而 Self_Evolve 领域的 AWM/SkillWeaver 已实现此能力但未适配 GUI 场景。

**Evidence Level**: A

**Primary Evidence**:
| # | Paper | Location | Evidence Content | Evidence Type |
|---|-------|----------|-----------------|---------------|
| 1 | Zhang et al. (2023/2025 CHI) | Introduction, p.2 | "different apps have unique GUIs with varying icon meanings and operational logic" — 新 app 需要重新探索，无法复用已有技能 | Direct statement |
| 2 | Lee et al. (2024, ACM MobiCom) | §9, p.14 | "Cross App Task execution ... MobileGPT can be extended to maintain a global dataset of known tasks across apps." — 作者明确将跨 app 程序性记忆列为未来工作 | Direct statement (author-stated limitation) |
| 3 | Lee et al. (2024, ACM MobiCom) | §9, p.14 | "MobileGPT currently stores memory on a local basis, meaning each device has its own version of app memory." — 程序性记忆无法跨用户/设备共享 | Direct statement |
| 4 | Lee et al. (2024, ACM MobiCom) | §4.1, p.6 | "these graphs exist per app, not per task" — 子任务图是 per-app 孤岛，跨 app 无法复用技能 | Direct statement |
| 5 | Xu et al. (2026, arXiv:2602.16851) | §3.2.2, p.17 | MemGUI-Bench: GUI-Owl-1.5-32B = 27.1, workflow agents = 41.7 — 即使最强 native GUI model 仍明显落后于显式 workflow/external-memory orchestration | Experimental gap |

> **Evidence Analysis**: AppAgent（新-1）从架构设计层面证明 GUI App 间知识壁垒的客观存在；MobileGPT（新-2/3/4）是早期最接近 Procedural Memory 的 GUI 工作，但作者自己明确承认跨 app 迁移是未来工作。MobileAgentV3.5（新-5）进一步从 benchmark 侧量化了这一缺口：即使最强 native model，遇到需要长期 workflow / external memory orchestration 的任务仍显著落后。多源直接陈述 + 量化实验共同支撑 A 级判断。

**Current Best Partial Solution**: MAGNET (Sun et al., 2026) — 目前最强 GUI 侧正例，已实现 workflow-level Procedural Memory + dynamic evolution，并在 AndroidWorld 达到 42.62%；但其程序记忆仍受 per-app clustering abstraction 约束，且不能抽象成跨 app 可迁移的原子技能，因此只能算 A-1 的 closest partial solution，而非真正解决方案。

**Counter-evidence Check**:
| Paper | What it did | What it didn't do (why Gap still holds) |
|-------|------------|----------------------------------------|
| MAGNET (Sun et al., 2026) | 实现了 abstract workflow-level Procedural Memory + Ebbinghaus 动态进化；AndroidWorld 42.62% SOTA | 程序性记忆仍为 per-app clustering-based，跨 app 原子技能复用不支持；作者承认"clustering-based workflow extraction may struggle with highly diverse task structures" (Limitations, p.9) |
| ActionEngine (Zhong et al., 2026) | 用 state-machine graph 建立全局应用结构记忆，WebArena Reddit 95% success；在线可局部 re-grounding 修补 graph | 记忆仍绑定单站点 topology 和 action template；解决的是 structural planning，不是开放式跨 App procedural skill 抽象 |
| IntentCUA (Lee et al., 2026) | 从 traces 抽象 subgroup skill hints + shared plan memory，286 个任务 74.8% SR | skill / plan 仍依赖离线 traces 与人工批准 plan cache；偏 workflow-level reuse，不是开放世界跨 App procedural memory |
| MobileGPT (Lee et al., 2024) | 实现了 sub-task 级程序性记忆（三层层级），跨任务 sub-task 共享 | 仅限 per-app；跨 app 迁移明确列为 future work |
| AWM (Wang et al., 2024) | 轨迹→可复用 workflow，WebArena +51.1% | 文本 web 环境验证，未适配 GUI 截图的高维多模态特性 |
| SkillWeaver (Zheng et al., 2025) | 可执行 API 技能库，跨 agent 迁移有效 | 仍为 per-website，不覆盖 GUI visual grounding 问题 |

> **Counter-evidence Conclusion**: 现有 GUI partial solutions 已扩展到 workflow memory（MAGNET）、structural graph memory（ActionEngine）和 intent-level skill / plan cache（IntentCUA），但它们仍共同受限于 per-app / per-site / per-workflow 绑定和离线整理成本。Self_Evolve 领域的 AWM/SkillWeaver 已解决"文本域"的 Procedural Memory，但 GUI 视觉定位、跨 app 特征提取等高维问题均未解决。A-1 Gap 在"原子技能跨 app 复用"维度仍完全空白。

**Cross-domain Intersection**:
- Self_Evolve → GUI_Agent: AWM 的"轨迹→参数化 workflow 模板"归纳机制（Wang et al., 2024, §2.2, p.3）+ SkillWeaver 的可执行 API 技能库（Zheng et al., 2025, §2, p.3）
- Agent_Memory → GUI_Agent: Procedural Memory 形式定义（持久、可执行的行动策略）
- Why no one has done this: GUI Agent 作者不熟悉 Self_Evolve 的技能归纳方法；AWM/SkillWeaver 在通用 Web 场景验证，未适配 GUI 截图的高维特性（视觉定位、UI 元素识别）

**Potential Approach**: 将 AWM 的"轨迹→模板"归纳机制应用于 GUI 探索轨迹；结合多模态 embedding 实现跨 App 原子技能（如"找到任意 App 的返回入口"）的迁移复用

**Feasibility Assessment**:
- Technical feasibility: High（AWM workflow 归纳框架成熟；GUI 探索数据从 AndroidEnv/WebArena 可生成；与 A-4 共享技术栈）
- Required resources: GUI 探索轨迹数据集（AndroidEnv/WebArena 可生成）+ 多模态 embedding 模型
- Relation to RQ: 对应核心 Sub-RQ（GUI Agent 跨任务知识积累）

**Priority**: P0

**Update Log**:
| Date | Event | Change |
|------|-------|--------|
| 2026-03-06 | 初始创建 | 综述推断，证据等级 B，状态 待验证 |
| 2026-03-06 | MobileGPT + AppAgent 精读 | 新增原文证据 新-1/2/3/4；证据等级 B→A；状态 待验证→精读确认；MAGNET/AWM/SkillWeaver 加入 counter-evidence check |
| 2026-03-06 | ActionEngine + IntentCUA 精读 | 补充 GUI structural / intent-level memory 的 partial solutions；确认其仍未解决跨 App procedural skill 抽象 |
| 2026-03-06 | MAGNET + MobileAgentV3.5 精读 | 补充 A-1 的 current best partial solution 与 benchmark-side gap evidence；确认 strongest native GUI model 仍明显落后于 workflow orchestration |

---

### A-2: GUI Agent 的情节记忆与跨会话学习（Episodic Memory for GUI）

**Status**: `精读确认`

**Statement**: GUI Agent 每次任务结束后，完整交互轨迹（屏幕状态、操作序列、成功/失败）被丢弃，下次任务从零开始，而 Agent_Memory 领域的 Generative Agents/MemGPT 已实现情节记忆的持久化与检索，MemGUI-Bench 量化了 GUI 场景记忆能力缺口达 14pp。

**Evidence Level**: A

**Primary Evidence**:
| # | Paper | Location | Evidence Content | Evidence Type |
|---|-------|----------|-----------------|---------------|
| 1 | Park et al. (2023, UIST) | §1, p.1 | "Fully general agents that ensure long-term coherence would be better suited by architectures that manage constantly-growing streams of events and memories." — 情节记忆的必要性已在文本 agent 领域验证，技术可行 | Direct statement |
| 2 | Packer et al. (2023) | Abstract, p.1 | "virtual context management, a technique drawing inspiration from hierarchical memory systems" — 三层存储（Working/Archival/Recall）提供情节记忆管理的工程蓝图 | Direct statement |
| 3 | Xu et al. (2026, arXiv:2602.16851) | §2.1, p.4 | "sliding window mechanism with hierarchical context compression" retains recent turns in full and compresses earlier turns into text summary — 当前实现仍是 in-task working memory，而非跨会话 episodic store | Direct statement |
| 4 | Xu et al. (2026, arXiv:2602.16851) | §3.2.2, p.17 | MemGUI-Bench: GUI-Owl-1.5-32B = 27.1 vs workflow agents = 41.7 — GUI 场景记忆能力缺口的直接量化证据 | Experimental gap |
| 5 | Park et al. (2023, UIST) | §4.2, p.9 | "Generative agents, when equipped with only raw observational memory, struggle to generalize or make inferences." — 支持 Reflection 必要性，间接说明 GUI 场景截图存储不够 | Indirect implication |

> **Evidence Analysis**: Generative Agents（证据1/5）证明情节记忆在智能体系统中的技术可行性；MemGPT（证据2）提供三层存储的工程蓝图，可适配 GUI 场景；MobileAgentV3.5（证据3/4）则明确展示当前 GUI native model 实现的只是 compressed working memory，并在 MemGUI-Bench 上暴露出 14.6pp 的长期记忆缺口。多来源直接陈述 + 专项 benchmark 量化共同支撑 A 级判断。

**Counter-evidence Check**:
| Paper | What it did | What it didn't do (why Gap still holds) |
|-------|------------|----------------------------------------|
| Generative Agents (Park et al., 2023) | 完整的情节记忆实现：timestamped Memory Stream + Reflection Tree + 三因素检索（相关性/时近性/重要性） | 仅文本/模拟环境；无视觉 GUI 观测；无任务转移评估 |
| MemGPT (Packer et al., 2023) | 三层虚拟上下文管理；跨会话记忆已验证（document QA） | 仅文本；无 GUI 截图处理能力 |
| M2 (Yan et al., 2026) | internal summary + external insight retrieval；WebVoyager +16.2pp，OnlineMind2Web +19.6pp | insight bank 是静态离线成功轨迹资产，不是部署后 agent 自己积累的 episodic memory；无跨会话 autobiographical history 维护 |

> **Counter-evidence Conclusion**: 情节记忆技术已成熟（文本域），而 M2 证明 GUI / Web agent 确实能从 summary + retrieval memory 获益；但 GUI 场景仍缺少真正 deployment-generated、可跨会话增长的 episodic memory。MemGUI-Bench 的 14pp 缺口证明此 Gap 的实用价值已可量化。

**Cross-domain Intersection**:
- Agent_Memory → GUI_Agent: Generative Agents 的三因素检索（相关性/时近性/重要性）+ MemGPT 三层虚拟存储（Park et al., 2023, §3.1, p.5; Packer et al., 2023, §2, p.3）
- Self_Evolve → GUI_Agent: ArcMemo/FLEX 的终身学习架构可扩展到 GUI 跨会话场景
- Why no one has done this: GUI 轨迹包含截图（高维视觉），现有情节记忆的检索机制多用于文本；跨会话 GUI 数据集不存在（需自建）

**Potential Approach**: 多模态情节记忆 (截图嵌入, 任务描述, 操作序列, 结果) → 向量化存储 → 相似任务检索历史轨迹 → 注入当前任务上下文

**Feasibility Assessment**:
- Technical feasibility: Medium（多模态检索库已有基础；跨会话 GUI 数据集需自建是主要瓶颈）
- Required resources: 多模态检索库 + 跨会话 GUI 数据集（需自建或从 MemGUI-Bench 扩展）
- Relation to RQ: 对应 Sub-RQ（GUI Agent 跨会话学习与记忆持久化）

**Priority**: P0

**Update Log**:
| Date | Event | Change |
|------|-------|--------|
| 2026-03-06 | 初始创建 | 综述推断，证据等级 B，状态 待验证 |
| 2026-03-06 | GenerativeAgents + MemGPT + MobileAgentV3.5 精读 | 新增证据 1~5；A-2 升级为 A 级；状态 待验证→精读确认；技术蓝图（三因素检索 + 三层存储）已明确；MobileAgentV3.5 同时补足 working-memory implementation 与 MemGUI-Bench 量化缺口 |
| 2026-03-06 | M2 精读 | 补充 GUI / Web 侧 summary + retrieval memory 的 partial solution；确认静态 insight bank 仍不等于跨会话 episodic memory |

---

### A-3: GUI Agent 的用户中心记忆与个性化（User-Centric Memory for GUI）

**Status**: `待验证`

**Statement**: GUI Agent 个性化能力极度缺失（仅 Friday 初步尝试），而 Agent_Memory 领域已有完整 User-Centric Memory 理论框架（A-Mem、MemoCRS），GUI 操作路径、偏好设置等天然用户信号尚未被利用。

**Evidence Level**: B

**Primary Evidence**:
| # | Paper | Location | Evidence Content | Evidence Type |
|---|-------|----------|-----------------|---------------|
| 1 | (综述推断) | GUI_Agent 综述 §3.3.1 | 仅 Friday 初步尝试 User-Centric Memory，其余 GUI Agent 均为 Agent-centric | Indirect implication |
| 2 | (综述推断) | Agent_Memory 综述 §3.3 | A-Mem（动态用户记忆）、MemoCRS（偏好追踪）已提供完整用户偏好存储、检索、更新机制 | Direct statement |
| 3 | Kim et al. (2026, ICML) | Abstract, p.1 | "current agents lack personalization capabilities" — personalized web agents 的问题被原文直接提出 | Direct statement |
| 4 | Kim et al. (2026, ICML) | §5.3, p.7 | "all agents fail completely on ambiguous queries, achieving a 0% success rate" — 没有用户历史时个性化 GUI / Web agent 直接失效 | Experimental gap |

> **Evidence Analysis**: Persona2Web 提供了第一篇直接针对 personalized web agent 的原文与实验数据，说明 A-3 已不再只是综述推断；但目前仍主要依赖单一 original paper，且 Friday 原文尚未精读，因此证据等级维持 B，未达到 A 级所需的多源独立确认。

**Counter-evidence Check**:
| Paper | What it did | What it didn't do (why Gap still holds) |
|-------|------------|----------------------------------------|
| Friday | 用户偏好建模初步尝试（跨会话 User-centric） | 仅 Desktop 场景；个性化机制细节不清晰（待精读原文确认） |

> **Counter-evidence Conclusion**: Friday 仍是最接近的 system-level user-centric 尝试，但 Persona2Web 已从 benchmark 侧直接证明"缺少用户历史 / 不会利用用户历史"会让个性化任务崩溃。A-3 已从纯推断升级为单篇原文确认，但 system-side 解决方案仍明显不足。

**Cross-domain Intersection**:
- Agent_Memory → GUI_Agent: A-Mem 动态用户记忆 + MemoCRS 偏好追踪框架
- GUI 场景有独特的用户信号：操作路径（走哪条菜单路径）、偏好设置、历史任务频率、常用 App
- Why no one has done this: GUI Agent 研究以任务自动化为主，用户偏好建模被视为"软性"问题；Agent_Memory 中的 User-Centric Memory 主要在对话场景验证

**Potential Approach**: 将 GUI 操作历史作为用户偏好信号 → 构建 GUI 专用用户画像（偏好路径、常用 App、操作习惯）→ 注入未来任务规划

**Feasibility Assessment**:
- Technical feasibility: Medium-High（理论路径清晰；难点是隐私-性能权衡设计和用户纵向数据获取）
- Required resources: 用户纵向 GUI 操作数据（极难获取）
- Relation to RQ: 差异化方向，隐私壁垒高，独立成文更合适

**Priority**: P2

**Update Log**:
| Date | Event | Change |
|------|-------|--------|
| 2026-03-06 | 初始创建 | 综述推断，证据等级 B，状态 待验证 |
| 2026-03-06 | Persona2Web 精读 | 新增 personalized web agent 的原文与实验数据；A-3 从纯综述推断升级为单篇原文确认；证据等级维持 B，状态维持 待验证 |

---

### A-4: 探索阶段的经验驱动自进化（Trial & Error → Offline Experience Evolution）

**Status**: `精读确认`

**Statement**: GUI Agent 探索阶段（AppAgent/MobileGPT）已有"尝试→观察→记录"雏形，但记录结果是静态的——失败轨迹被主动丢弃，无法从失败中更新策略；Self_Evolve 领域的 AWM/ExpeL/SkillRL 已实现从失败轨迹提炼经验，但未适配 GUI 场景。

**Evidence Level**: A

**Primary Evidence**:
| # | Paper | Location | Evidence Content | Evidence Type |
|---|-------|----------|-----------------|---------------|
| 1 | Wang et al. (2024, arXiv:2406.01014) | §3.5, p.6 | "Neither erroneous nor ineffective operations are recorded in the operation history to prevent the agent from following these operations." — 失败轨迹被主动丢弃，明确无离线学习 | Direct statement |
| 2 | Wang et al. (2024, arXiv:2406.01014) | §4.3, p.8 | "automating the generation of high-quality operation knowledge can further improve the performance of Mobile-Agent-v2" — 作者承认缺乏自动化知识生成 | Direct statement (author-stated) |
| 3 | Sun et al. (2026, arXiv:2601.19992) | Limitations, p.9 | "The framework requires successful trajectories for memory construction, making it less effective in completely novel domains where initial exploration fails." — MAGNET 明确承认无法从失败轨迹构建记忆 | Direct statement (author-stated limitation) |
| 4 | Xu et al. (2026, arXiv:2602.16851) | §2.2-§2.4, p.3-11 | GUI-Owl-1.5 的 "self-evolving trajectory synthesis workflow"、Unified CoT synthesis 与 MRPO 都发生在 pre-deployment data/training pipeline 中；部署后仅保留 in-context note/compression，未描述从真实执行轨迹写回经验库 | Experimental gap |
| 5 | Xue et al. (2026, arXiv:2601.15867v2) | §9, p.18 | "This disparity highlights the limits of offline learning from synthesized traces alone." — 即便 failure-aware Step-level DPO 已引入，训练期离线/合成经验仍未闭环为部署后可持续离线进化 | Direct statement |

> **Evidence Analysis**: Mobile-Agent-v2（证据1/2）直接陈述失败轨迹被主动丢弃且作者承认知识生成自动化为未来工作；MAGNET（证据3）是 GUI 领域当前最佳 partial solution，却仍只能从成功轨迹更新 memory；MobileAgentV3.5（证据4）和 EvoCUA（证据5）则进一步表明，即便最新经验驱动路线已经引入 self-evolving data flywheel、MRPO 或 failure-aware Step-level DPO，进化仍主要停留在训练期/pre-deployment pipeline，而不是部署后可持续的 offline experience evolution。GUI 侧对 A-4 的真正闭环仍未出现。

**Counter-evidence Check**:
| Paper | What it did | What it didn't do (why Gap still holds) |
|-------|------------|----------------------------------------|
| AWM (Wang et al., 2024) | 从成功+失败轨迹对归纳 workflow；cross-domain 最高 +16.9% | 仅在文本 web 环境（WebArena/Mind2Web），未适配 GUI 截图高维特性；online+offline 融合存在兼容性问题（Appendix C, p.16） |
| ExpeL (Zhao et al., 2024, AAAI) | 从 success/failure trajectory pairs 提取 insight；FEVER transfer +7% | 仅文本环境验证；"tasks with textual observation, which is limiting in real-world scenarios" (§6, p.10) |
| SkillRL (Xia et al., 2026) | 失败轨迹→反事实教训；ALFWorld +12.3% vs GRPO | 仅文本/结构化环境；GUI 视觉观测下蒸馏质量未验证；依赖 teacher model (o3) |
| EvoCUA (Xue et al., 2026) | Step-level DPO 利用失败轨迹（critical forking point + reflection） | 仅训练阶段；"limits of offline learning from synthesized traces alone" (§9, p.18)；部署后无演化 |
| MAGNET (Sun et al., 2026) | 动态记忆进化，从成功轨迹更新 | 明确不支持失败轨迹：Limitations p.9 直接陈述 |

> **Counter-evidence Conclusion**: Self_Evolve 领域已有多个方法解决"从失败中学习"（AWM/ExpeL/SkillRL），但均在文本/web 环境验证，尚无方法将其适配到 GUI 场景（截图高维、视觉定位、跨 app 工作流）。GUI Agent 领域最先进的 MAGNET 仍依赖成功轨迹。A-4 Gap 在 GUI 场景仍完全空白。

**Cross-domain Intersection**:
- Self_Evolve → GUI_Agent: AWM"轨迹对→workflow 归纳"（Wang et al., 2024, §2.2-2.3, p.3）+ ExpeL ADD/EDIT/UPVOTE/DOWNVOTE insight 维护（Zhao et al., 2024, §4.2, p.4）
- Why no one has done this: GUI 探索轨迹包含高维截图；失败原因在视觉场景中更难自动归纳；GUI 场景的失败分类（错误点击/页面误判/流程中断）与文本环境不同

**Potential Approach**: GUI 探索轨迹（成功+失败）→ LLM 分析失败原因（结合截图前后变化）→ 提炼"在 App X 中，避免操作 Y，改用 Z" → 写入程序记忆 → 供后续同类任务检索

**Feasibility Assessment**:
- Technical feasibility: High（与 A-1 高度协同，共享技术栈；AWM/ExpeL 框架直接可移植；GUI 探索数据易得）
- Required resources: GUI 探索轨迹数据集 + 多模态 LLM（用于失败分析）
- Relation to RQ: 与 A-1 协同，可作为同一论文的两个贡献模块

**Priority**: P0

**Update Log**:
| Date | Event | Change |
|------|-------|--------|
| 2026-03-06 | 初始创建 | 综述推断，证据等级 B，状态 待验证 |
| 2026-03-06 | MobileAgentV2 + MAGNET + MobileGPT + MobileAgentV3.5 + AWM + ExpeL + SkillRL + EvoCUA 精读 | 新增 GUI/Computer-use 端原文证据 1~5；A-4 升级为 A 级；状态 待验证→精读确认；确认当前最强路线仍停留在成功轨迹或训练期经验闭环，Self_Evolve 领域有解答但未迁移到 GUI 部署阶段 |

---

### A-5: GUI Agent 训练阶段 vs 部署阶段自进化断层

**Status**: `待验证`

> ⚠️ NEEDS YOUR INPUT: 这是否构成独立的 A 类 Gap，还是应归并到 A-4 的子问题？
> 初步建议：(1) 若你的 RQ 包含"部署后持续学习"，可独立追踪为 A-5；(2) 若仅关注探索阶段的经验利用，可作为 A-4 的扩展证据。
> 与 A-4 的区别：A-4 关注"从失败中学习"；A-5 关注"部署后持续学习 vs 训练阶段封闭"。

**Statement**: 当前 GUI Agent 的自进化即便不再停留在一次性预训练，也仍主要依赖显式 post-training / continual RL adaptation loops（EvoCUA、GUI-Owl、GUI-Owl-1.5、GUI-GENESIS、ACuRL）；部署后 agent 仍无法从真实用户交互轨迹中通过 runtime memory 持续学习，而 Self_Evolve 领域的 MemRL 已实现 frozen-backbone + runtime memory RL 的部署后演化。

**Evidence Level**: A

**Primary Evidence**:
| # | Paper | Location | Evidence Content | Evidence Type |
|---|-------|----------|-----------------|---------------|
| 1 | Xue et al. (2026) | §9, p.18 | "This disparity highlights the limits of offline learning from synthesized traces alone." — 仅靠离线合成轨迹难触及 human-level reliability | Direct statement |
| 2 | Xu et al. (2026, arXiv:2602.16851) | §1, p.2 | "short-term and long-term memory" listed as capability but only in-context implementation — 部署后无记忆演化 | Experimental gap |
| 3 | Ye et al. (2025) | §6, p.17 | "we develop a self-evolving GUI trajectory data production pipeline" — 自进化在训练阶段；inference 时无持续学习 | Direct statement |

> **Evidence Analysis**: 三篇独立 GUI Agent 原文分别从不同角度说明演化被限制在训练阶段，且与 MemRL（Zhang et al., 2026, §1, p.1）的"部署后持续演化无需修改 backbone"形成明确技术对比。

**Counter-evidence Check**:
| Paper | What it did | What it didn't do (why Gap still holds) |
|-------|------------|----------------------------------------|
| ACuRL (Xue et al., 2026) | zero-human-data continual RL in target environments；Impress +9.6，Thunderbird +22.3 | 仍是显式训练循环（exploration + curriculum + evaluator），不是部署期 runtime memory adaptation |
| GUI-GENESIS (Cao et al., 2026) | synthetic GUI environments + code-native rewards 支持高效 post-training；真实环境 SR 36.91→42.28 | 解决的是训练环境与 reward 基础设施，不是部署后持续学习；依赖 reward-verifiable synthetic envs |
| MemRL (Zhang et al., 2026) | frozen-backbone + runtime non-parametric RL；部署后 utility 持续更新 | 仅文本/结构化任务（OS tasks, ALFWorld）；GUI 视觉观测下的 intent-experience 匹配未验证 |

> **Counter-evidence Conclusion**: GUI 领域已经出现 ACuRL 和 GUI-GENESIS 这类更强的 adaptation / post-training partial solutions，但它们都依赖显式训练基础设施，而不是部署期可持续增长的 runtime memory。MemRL 证明部署后演化技术上可行，但仅在文本域验证。A-5 的核心断层已经从"完全没人做"收缩为"GUI 端仍缺 runtime memory-based continual improvement"。

**Cross-domain Intersection**:
- Self_Evolve → GUI_Agent: MemRL 的 Intent-Experience-Utility triplet + Monte-Carlo utility update（Zhang et al., 2026, §4.3, p.5）
- Why no one has done this: GUI Agent 研究重心在感知和规划；"部署后演化"需要 runtime 环境反馈收集基础设施，工程成本高

**Potential Approach**: 将 MemRL 的 frozen-backbone + memory RL 迁移到 GUI 场景；使用 task success/failure 作为 reward signal 更新 memory utility

**Feasibility Assessment**:
- Technical feasibility: Medium（MemRL 框架理论上可迁移；GUI 场景 intent-experience 匹配的多模态化是主要挑战）
- Required resources: 部署环境反馈收集系统 + GUI 任务 reward 定义
- Relation to RQ: 与 A-4 协同；若 RQ 覆盖部署后学习则为独立贡献

**Priority**: P1

**Update Log**:
| Date | Event | Change |
|------|-------|--------|
| 2026-03-06 | EvoCUA + MobileAgentV3 + MobileAgentV3.5 + MemRL 精读 | 新 Gap 信号识别；证据等级直接为 A（≥3 原文直接陈述 + MemRL 技术对照）；状态 待验证；等待研究者确认是否独立追踪 |
| 2026-03-06 | ACuRL + GUI-GENESIS 精读 | 补充 GUI 端最强 adaptation / post-training partial solutions；确认当前最佳路线仍依赖显式训练循环而非 runtime memory update |

---

## B 类 Gap：单领域问题 + 跨领域已有解答

### B-1: Reflection 结果的持久化（单任务 → 跨任务）

**Status**: `待验证`

**Statement**: Mobile-Agent-v2 和 PC-Agent 的 Reflection Agent 能发现并纠正错误，但反思结果在任务结束后丢弃，无法积累为跨任务可复用的经验，而 Reflexion 已验证文本 agent 的反思持久化技术可行。

**Evidence Level**: A

**Primary Evidence**:
| # | Paper | Location | Evidence Content | Evidence Type |
|---|-------|----------|-----------------|---------------|
| 1 | Shinn et al. (2023) | §3, p.5 | Reflexion memory stores verbal self-reflections persistently across trials — 证明文本 agent 的反思持久化技术可行 | Direct statement |
| 2 | Wang et al. (2024, arXiv:2406.01014) | §3.5, p.6 | "Neither erroneous nor ineffective operations are recorded in the operation history" — Mobile-Agent-v2 的 Reflection 结果在任务结束后丢失 | Experimental gap |
| 3 | Liu et al. (2025) | §3.3, p.7 | "removing RA leads to a very significant performance decrease (27.9% SSR, 44.0% SR)" — 反射对 PC 场景至关重要，但 RA 反馈无跨任务持久化 | Experimental gap |

> **Evidence Analysis**: Reflexion（证据1）验证技术可行路径；MobileAgentV2（证据2）和 PCAgent（证据3）从两个独立 GUI 系统分别证明 Reflection 对性能关键但不持久化。构成 A 级：技术可行（文本域）+ GUI 场景缺失（两个独立系统量化）。

**Counter-evidence Check**:
| Paper | What it did | What it didn't do (why Gap still holds) |
|-------|------------|----------------------------------------|
| DEACTION (Ning et al., 2026) | detect misaligned actions + structured feedback + iterative correction；MISACTBENCH F1 最高 82.8 | correction 信号只服务当前任务，未沉淀为跨任务 reflection memory；依赖外部 alignment judge |

> **Counter-evidence Conclusion**: DEACTION 说明 GUI runtime detect-and-correct 已经有效，但 correction 结果仍停留在单任务内，没有形成 Reflexion 式可检索的跨任务记忆。B-1 结论不变。

**Cross-domain Intersection**:
- Self_Evolve → GUI_Agent: Reflexion 的 verbal self-reflection 持久化到 long-term memory（Shinn et al., 2023, §3, p.5）
- Migration path: Reflection 输出（"在 App X 执行 Y 时，应先做 Z"）→ 写入外部记忆 → 供后续任务检索

**Potential Approach**: GUI Reflection 输出结构化为 (context, error_pattern, correction) 三元组 → 存储到向量数据库 → 未来任务检索相似错误模式并注入上下文

**Feasibility Assessment**:
- Technical feasibility: High（实现成本低；可作为 A-1/A-4 系统的基础组件；Reflexion 框架成熟可移植）
- Required resources: Reflection 输出的结构化 prompt + 向量存储库
- Relation to RQ: 对应 Sub-RQ（反思结果持久化）；可作为 A-1/A-4 主贡献的基础模块

**Priority**: P1

**Update Log**:
| Date | Event | Change |
|------|-------|--------|
| 2026-03-06 | 初始创建 | 综述推断，证据等级 B |
| 2026-03-06 | Reflexion + MobileAgentV2 + PCAgent 精读 | 新增证据 1~3；B-1 升级为 A 级；Reflexion 提供直接技术迁移路径；两个独立 GUI 系统证实缺失 |
| 2026-03-06 | DEACTION 精读 | 新增 GUI 端 detect-and-correct partial solution；确认 correction 仍不持久化，B-1 核心结论不变 |

---

### B-2: GUI 探索知识的跨 App 迁移

**Status**: `待验证`

**Statement**: AppAgent/MobileGPT 的探索知识是 App 级的孤岛，无法复用于新 App，而 SkillWeaver 已验证跨 agent 技能迁移在 web 域可行（+54.3%），MobileGPT 作者明确将跨 App 列为未来工作。

**Evidence Level**: A

**Primary Evidence**:
| # | Paper | Location | Evidence Content | Evidence Type |
|---|-------|----------|-----------------|---------------|
| 1 | Lee et al. (2024, ACM MobiCom) | §9, p.14 | "MobileGPT can be extended to maintain a global dataset of known tasks across apps" — 作者承认跨 app 是当前局限和未来方向 | Direct statement (author-stated) |
| 2 | Zheng et al. (2025) | §4.2, p.7-8 | GPT-4o-mini 使用 GPT-4o 探索的技能库后 WebArena +54.3% relative gain — 跨 agent 技能迁移成功验证（web 域） | Experimental evidence |

> **Evidence Analysis**: MobileGPT 作者直接陈述跨 App 为局限和未来工作（直接正证）；SkillWeaver 在 web 域证明技能跨 agent 迁移有效（技术可行性正证）。GUI App 跨域迁移仍无实现。

**Counter-evidence Check**:
| Paper | What it did | What it didn't do (why Gap still holds) |
|-------|------------|----------------------------------------|
| SkillWeaver (Zheng et al., 2025) | 跨 agent（strong→weak）技能迁移，+54.3% | 仍为 per-website；GUI App 的视觉多样性远高于 web，跨 App 迁移特征提取更难 |
| AgentKB | 跨领域知识库（通用） | 未在 GUI 场景验证；未精读原文 `[S]` |

> **Counter-evidence Conclusion**: SkillWeaver 证明跨 agent 技能迁移技术上可行，但 per-website 粒度与 GUI per-app 场景的特征差异（视觉 UI vs DOM 文本）仍需解决。B-2 Gap 在 GUI 跨 App 迁移维度仍空白。

**Cross-domain Intersection**:
- Self_Evolve → GUI_Agent: SkillWeaver 技能库跨 agent 迁移（Zheng et al., 2025, §4.2, p.7-8）+ AgentKB 跨领域知识库（待精读）
- Migration path: 提取 GUI 操作的 App 无关特征（UI 元素类型、页面层级结构），构建跨 App 通用知识图谱

**Potential Approach**: 抽取 App 无关的 GUI 原子操作（scroll/tap/type 及其语义含义）→ 建立 cross-app skill graph → 新 App 探索时从 graph 检索并适配

**Feasibility Assessment**:
- Technical feasibility: Medium（依赖 A-1 的技术基础；跨 App UI 特征对齐是主要挑战）
- Required resources: 多 App 探索数据集 + App 无关特征提取模型
- Relation to RQ: 可作为 A-1 的扩展实验

**Priority**: P1

**Update Log**:
| Date | Event | Change |
|------|-------|--------|
| 2026-03-06 | 初始创建 | 综述推断，证据等级 B |
| 2026-03-06 | MobileGPT + SkillWeaver 精读 | 新增证据 1~2；B-2 升级为 A 级；SkillWeaver 验证跨 agent 技能迁移可行性（web 域），GUI 域迁移仍空白 |

---

### B-3: 跨任务学习效果的评估框架

**Status**: `待验证`

> ⚠️ NEEDS YOUR INPUT: MemGUI-Bench 的出现使 B-3 从"完全空白"变为"有初步方案但不完整"。建议决策：
> (1) 将 MemGUI-Bench 加入"已有部分解答"字段并降低优先级；
> (2) 将 MemGUI-Bench 作为自己研究的评测 benchmark（直接使用而非重造）。
> 请确认后更新本条目状态。

**Statement**: 现有 GUI benchmark 虽已开始覆盖记忆 recall（MemGUI-Bench）、ambiguity / clarification（AmbiBench）和 personalization reasoning（Persona2Web），但仍基本停留在单次任务诊断，无法衡量"第二次完成同类任务是否更快/更准"这类 repeated-exposure learning curve。

**Evidence Level**: B

**Primary Evidence**:
| # | Paper | Location | Evidence Content | Evidence Type |
|---|-------|----------|-----------------|---------------|
| 1 | Xu et al. (2026, arXiv:2602.16851) | §3.2.2, p.17 | MemGUI-Bench: native models 27.1 vs workflow agents 41.7 — 首个专门评测 GUI agent 记忆能力的基准；证明记忆能力可量化 | Experimental evidence |
| 2 | Xu et al. (2026, arXiv:2602.16851) | §3.2.2, p.17 | MemGUI-Bench only reports "Easy" tasks — medium/hard task performance unreported | Experimental gap |
| 3 | (多篇 GUI Agent 论文) | — | 现有 GUI benchmark 均为单次任务评测，无跨会话学习曲线设计 | Indirect implication |

> **Evidence Analysis**: MemGUI-Bench、AmbiBench、Persona2Web 说明 GUI / Web agent evaluation 已开始从单一 success rate 走向 memory recall、interaction quality 和 personalization reasoning 等 richer diagnostics；但这些 benchmark 仍是"单次任务如何表现"的切片，不是"多次接触后是否学会"的 repeated-exposure protocol。B-3 Gap 在学习曲线维度仍完全空白。

**Counter-evidence Check**:
| Paper | What it did | What it didn't do (why Gap still holds) |
|-------|------------|----------------------------------------|
| MemGUI-Bench (Liu et al., 2026) | 首个 GUI 记忆评测基准；量化 14pp 记忆能力缺口 | 仅覆盖 Easy 任务；评测记忆 recall，非学习曲线；跨会话效率提升无法测量 |
| AmbiBench (Sun et al., 2026) | 引入 outcome + execution + interaction 三维评测；诊断 ambiguity / clarification failure | 仍是单次任务评测；不衡量 repeated exposure 后的学习收益 |
| Persona2Web (Kim et al., 2026) | reasoning-aware personalization rubric；区分 history retrieval failure 与 utilization failure | 评测的是历史利用与个性化推理，不是跨会话学习曲线或 repeated-task improvement |

**Cross-domain Intersection**:
- Self_Evolve → GUI_Agent: Self_Evolve 综述的 benchmark 设计 + LlamaTouch 的多级别 UI 状态匹配
- Migration path: 设计跨会话 GUI benchmark：同一 Agent 多次接触同类任务后的成功率和效率变化曲线

**Potential Approach**: 设计"学习曲线"评测协议：Task × Repetition 矩阵，记录 SR/效率随执行次数的变化；在现有 benchmark（如 AndroidWorld）上扩展多轮设置

**Feasibility Assessment**:
- Technical feasibility: Medium（MemGUI-Bench 已有基础；扩展到学习曲线评测需要重新设计实验协议）
- Required resources: 可控的跨会话 GUI 测试环境
- Relation to RQ: 是所有 Gap 验证的前提，但属于基础设施工作；可使用 MemGUI-Bench 而非重造

**Priority**: P2

**Update Log**:
| Date | Event | Change |
|------|-------|--------|
| 2026-03-06 | 初始创建 | 综述推断，证据等级 B，状态 待验证；完全空白 |
| 2026-03-06 | MobileAgentV3.5 精读 | 发现 MemGUI-Bench 存在；B-3 从完全空白变为有初步评测框架（但不完整）；新增 counter-evidence 行；建议降低优先级或直接使用 MemGUI-Bench |
| 2026-03-06 | AmbiBench + Persona2Web 精读 | 补充 ambiguity / personalization evaluation partial solutions；确认 richer diagnostics 已出现，但 repeated-exposure learning curve 仍缺失 |

---

## C 类 Gap：单领域内残留问题

| Gap | 领域 | 描述 | 单领域方案 |
|-----|------|------|----------|
| **C-1：GUI 计算成本** | GUI_Agent §6.1 | 高分辨率截图 + 多步推理 = 极高成本 | 模型压缩、小骨干模型、KV Cache 优化、GUIPruner 式时空 token pruning、M2 式摘要压缩 |
| **C-2：Agent Memory 遗忘策略** | Agent_Memory §Future | 记忆积累后旧内容如何有效遗忘 | 时间衰减、基于重要性删除、记忆整合 |
| **C-3：Self-Evolve 模型崩溃** | Self_Evolve §VI | 持续自训练可能导致分布外漂移 | 保留金标准数据、对抗性验证 |
| **C-4：GUI 幻觉与安全性** | GUI_Agent §6.2 | Feasibility/Completeness/Security 研究不足 | ResponsibleTA / DEACTION 式 intent-alignment guardrails |

---

## 全局优先级排序（更新后）

| 排名 | Gap | 类型 | 证据等级 | 状态 | 核心理由 |
|------|-----|------|---------|------|---------|
| **1** | **A-1（Procedural Memory + GUI）** | A | **A** | **精读确认** | 可行性最高；AWM 直接可移植；与 A-4 协同，可构成一篇完整论文；MobileGPT+AppAgent 双原文确认 |
| **2** | **A-4（探索→离线自进化）** | A | **A** | **精读确认** | 与 A-1 共享技术栈；GUI 探索数据易得；可作为同一工作的第二贡献；MobileAgentV2+MAGNET 双原文确认 |
| **3** | **B-1（Reflection 持久化）** | B | **A** | 待验证 | 实现成本低；可作为 A-1/A-4 的基础组件；Reflexion 技术成熟可移植 |
| **4** | **A-2（Episodic Memory + GUI）** | A | **A** | **精读确认** | MemGUI-Bench 量化 14pp 缺口；GenerativeAgents+MemGPT 验证技术蓝图；多模态检索挑战需单独解决 |
| **5** | **A-5（训练 vs 部署自进化断层）** | A | A | 待验证 | ⚠️ 待确认是否独立追踪；MemRL 证明部署后演化可行（文本域）；与 A-4 高度协同 |
| **6** | **B-2（跨 App 迁移）** | B | **A** | 待验证 | 依赖 A-1 的技术基础；SkillWeaver 验证跨 agent 迁移；可作为扩展实验 |
| **7** | **A-3（User-Centric + GUI）** | A | B | 待验证 | Persona2Web 已给出第一篇原文与实验支撑，但 system-side user memory 方案仍薄弱；隐私壁垒仍高 |
| **8** | **B-3（评估框架）** | B | B | 有初步方案 | MemGUI-Bench 部分填补；建议直接使用而非重造；优先级降低 |

---

## 证据等级汇总

| Gap | 初始等级 | 当前等级 | 变化原因 |
|-----|---------|---------|---------|
| A-1 | B | **A** | MobileGPT + AppAgent 双原文直接陈述 |
| A-2 | B | **A** | GenerativeAgents + MemGUI-Bench 量化 |
| A-3 | B | B | Persona2Web 提供首个 personalized web agent 原文与实验支撑，但仍属单一来源 |
| A-4 | B | **A** | MobileAgentV2 + MAGNET 双原文直接陈述 |
| A-5 | 新建 | A | EvoCUA + GUI-Owl + GUI-Owl-1.5 三原文 + MemRL 技术对照 |
| B-1 | B | **A** | Reflexion 技术可行 + MobileAgentV2/PCAgent 量化缺失 |
| B-2 | B | **A** | MobileGPT 直接陈述 + SkillWeaver 实验验证 |
| B-3 | B | B | MemGUI-Bench + AmbiBench + Persona2Web 提供 richer diagnostics，但 repeated-exposure learning curve 仍缺失 |
