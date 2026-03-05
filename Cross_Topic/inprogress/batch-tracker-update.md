# Batch Gap Tracker Update — 19 Papers
> Generated: 2026-03-06 | Status: UPDATE PROPOSAL — do NOT merge directly; review all ⚠️ NEEDS YOUR INPUT items first.
> Coverage: Gaps A-1, A-2, A-3, A-4, B-1, B-2, B-3 | New Gap signals: 2

---

## 🔄 Update to A-1: GUI Agent 的程序性记忆机制

### New Evidence from MobileGPT

| # | Location | Evidence Content | Evidence Type |
|---|----------|-----------------|---------------|
| 1 (原始 A-1 证据已有) | — | — | — |
| 新-1 | Lee et al. (2024), §9, p.14 | "Cross App Task execution ... MobileGPT can be extended to maintain a global dataset of known tasks across apps." — 作者明确将跨 app 程序性记忆列为未来工作 | Direct statement (author-stated limitation) |
| 新-2 | Lee et al. (2024), §9, p.14 | "MobileGPT currently stores memory on a local basis, meaning each device has its own version of app memory." — 确认程序性记忆无法跨用户/设备共享 | Direct statement |
| 新-3 | Lee et al. (2024), §4.1, p.6 | "these graphs exist per app, not per task" — 子任务图是 per-app 孤岛，跨 app 无法复用技能 | Direct statement |

**Impact on evidence level**: A-1 证据等级从 B（单一综述推断）升级为 **A（多个原文直接证据）**
- 原证据（对照矩阵推断）+ MobileGPT 原文直接承认跨 app 迁移是 future work + AppAgent 原文 "different apps have unique GUIs ... it remains uncertain whether these adapted models can effectively generalize to unseen apps" (Introduction, p.2)
- **符合 A 级标准**：≥2 篇原文明确陈述该 Gap

**Impact on status**: 建议从 `待验证` 升级为 `精读确认`（有 MobileGPT + AppAgent 两篇原文证据，可满足 §6.1 A级要求）

**Counter-evidence Check**:
| Paper | What it did | What it didn't do (why Gap still holds) |
|-------|------------|----------------------------------------|
| MAGNET (Sun et al., 2026) | 实现了 abstract workflow-level Procedural Memory + 动态进化；AndroidWorld 42.62% SOTA | 程序性记忆仍为 per-app clustering-based，跨 app 原子技能复用不支持；作者承认"clustering-based workflow extraction may struggle with highly diverse task structures" (Limitations, p.9) |
| MobileGPT (Lee et al., 2024) | 实现了 sub-task 级程序性记忆（三层层级），跨任务 sub-task 共享 | 仅限 per-app；跨 app 迁移明确列为 future work |
| AWM (Wang et al., 2024) | 轨迹→可复用 workflow，WebArena +51.1% | 文本 web 环境验证，未适配 GUI 截图的高维多模态特性 |
| SkillWeaver (Zheng et al., 2025) | 可执行 API 技能库，跨 agent 迁移有效 | 仍为 per-website，不覆盖 GUI visual grounding 问题 |

> **Counter-evidence Conclusion**: 现有最接近的工作（MAGNET）已在 GUI 场景实现了 workflow-level Procedural Memory，但受限于：(1) 仅从成功轨迹构建，失败学习能力缺失；(2) workflow 粒度较粗，细粒度跨 app 原子技能不支持。A-1 Gap 在"原子技能跨 app 复用"这一维度仍完全空白。

**Suggested addition to Update Log**:
| Date | Event | Change |
|------|-------|--------|
| 2026-03-06 | MobileGPT + AppAgent 精读 | 新增原文证据 新-1/2/3；证据等级 B→A；状态 待验证→精读确认；MAGNET 加入 counter-evidence check |

---

## 🔄 Update to A-2: GUI Agent 的情节记忆与跨会话学习

### New Evidence from Generative Agents + MemGPT + Mobile-Agent-v3.5

| # | Location | Evidence Content | Evidence Type |
|---|----------|-----------------|---------------|
| 原-1 | (已有矩阵推断) | GUI Agent 主要停留在任务内记忆 | — |
| 新-1 | Park et al. (2023), §1, p.1 | "Fully general agents that ensure long-term coherence would be better suited by architectures that manage constantly-growing streams of events and memories." — 情节记忆的必要性已在文本 agent 领域验证，技术可行 | Direct statement |
| 新-2 | Packer et al. (2023), Abstract, p.1 | "virtual context management, a technique drawing inspiration from hierarchical memory systems" — 三层存储（Working/Archival/Recall）提供情节记忆管理的工程蓝图 | Direct statement |
| 新-3 | Xu et al. (2026), §3.2.2, p.17 | MemGUI-Bench: native agent models reach 27.1 vs workflow agents 41.7 (14pp gap) — GUI 场景记忆能力缺口的直接量化证据 | Experimental gap |
| 新-4 | Park et al. (2023), §4.2, p.9 | "Generative agents, when equipped with only raw observational memory, struggle to generalize or make inferences." — 支持 Reflection 必要性，间接说明 GUI 场景截图存储不够 | Indirect implication |

**Impact on evidence level**: A-2 证据等级升级为 **A（多来源直接/实验证据）**
- Generative Agents 证明情节记忆技术可行（文本域） + MemGUI-Bench 量化 GUI 记忆缺口 14pp + 对照矩阵显示 GUI Agent 普遍缺失跨会话机制

**Impact on status**: 建议升级为 `精读确认`（技术可行性由 GenerativeAgents/MemGPT 验证；GUI 缺口由 MemGUI-Bench 量化）

**Suggested addition to Update Log**:
| Date | Event | Change |
|------|-------|--------|
| 2026-03-06 | GenerativeAgents + MemGPT + MobileAgentV3.5 精读 | 新增证据 新-1~4；A-2 升级为 A 级；技术蓝图（三维检索 + 三层存储）已明确 |

---

## 🔄 Update to A-4: 探索阶段的经验驱动自进化

### New Evidence (multiple papers)

| # | Location | Evidence Content | Evidence Type |
|---|----------|-----------------|---------------|
| 原-1 | (已有综述推断) | GUI 探索阶段仅记录不学习 | — |
| 新-1 | Wang et al. (2024), §3.5, p.6 | "Neither erroneous nor ineffective operations are recorded in the operation history to prevent the agent from following these operations." — 失败轨迹被主动丢弃，明确无离线学习 | Direct statement |
| 新-2 | Wang et al. (2024), §4.3, p.8 | "automating the generation of high-quality operation knowledge can further improve the performance of Mobile-Agent-v2" — 作者承认缺乏自动化知识生成 | Direct statement (author-stated) |
| 新-3 | Sun et al. (2026), Limitations, p.9 | "The framework requires successful trajectories for memory construction, making it less effective in completely novel domains where initial exploration fails." — MAGNET 明确承认无法从失败轨迹构建记忆 | Direct statement (author-stated limitation) |
| 新-4 | Xu et al. (2026), §1, p.2 | "short-term and long-term memory" listed as capability requirement but only in-context memory implemented — 部署后无演化机制 | Experimental gap |

**Impact on evidence level**: A-4 证据等级升级为 **A（≥2 原文直接陈述）**
- Mobile-Agent-v2 明确丢弃失败轨迹（新-1）+ MAGNET 明确依赖成功轨迹（新-3）+ MobileGPT 需 HITL 修复才能学习
- **Counter-evidence check 需要更新**（见下方）

**Counter-evidence Check**:
| Paper | What it did | What it didn't do (why Gap still holds) |
|-------|------------|----------------------------------------|
| AWM (Wang et al., 2024) | 从成功+失败轨迹对归纳 workflow；cross-domain 最高 +16.9% | 仅在文本 web 环境（WebArena/Mind2Web），未适配 GUI 截图高维特性；online+offline 融合存在兼容性问题 |
| ExpeL (Zhao et al., 2024) | 从 success/failure trajectory pairs 提取 insight；FEVER transfer +7% | 仅文本环境验证；"tasks with textual observation, which is limiting in real-world scenarios" (§6, p.10) |
| SkillRL (Xia et al., 2026) | 失败轨迹→反事实教训；ALFWorld +12.3% vs GRPO | 仅文本/结构化环境；GUI 视觉观测下蒸馏质量未验证；依赖 teacher model (o3) |
| EvoCUA (Xue et al., 2026) | Step-level DPO 利用失败轨迹（critical forking point + reflection） | 仅训练阶段；"limits of offline learning from synthesized traces alone" (§9, p.18)；部署后无演化 |
| MAGNET (Sun et al., 2026) | 动态记忆进化，从成功轨迹更新 | 明确不支持失败轨迹：Limitations p.9 直接陈述 |

> **Counter-evidence Conclusion**: Self_Evolve 领域已有多个方法解决"从失败中学习"（AWM/ExpeL/SkillRL），但均在文本/web 环境验证，尚无方法将其适配到 GUI 场景（截图高维、视觉定位、跨 app 工作流）。A-4 Gap 在 GUI 场景仍完全空白。

**Impact on status**: 建议升级为 `精读确认`

**Suggested addition to Update Log**:
| Date | Event | Change |
|------|-------|--------|
| 2026-03-06 | MobileAgentV2 + MAGNET + MobileGPT + AWM + ExpeL + SkillRL + EvoCUA 精读 | 新增 GUI 端原文证据 新-1~4；A-4 升级为 A 级；Counter-evidence check 填充完整；Self_Evolve 领域有解答但未迁移到 GUI |

---

## 🔄 Update to B-1: Reflection 结果的持久化

### New Evidence from Reflexion + Mobile-Agent-v2 + PC-Agent

| # | Location | Evidence Content | Evidence Type |
|---|----------|-----------------|---------------|
| 新-1 | Shinn et al. (2023), §3, p.5 | Reflexion memory stores verbal self-reflections persistently across trials — 证明文本 agent 的反思持久化技术可行 | Direct statement |
| 新-2 | Wang et al. (2024), §3.5, p.6 | "Neither erroneous nor ineffective operations are recorded in the operation history" — Mobile-Agent-v2 的 Reflection Agent 结果在任务结束后丢失 | Experimental gap |
| 新-3 | Liu et al. (2025), §3.3, p.7 | "removing RA leads to a very significant performance decrease (27.9% SSR, 44.0% SR)" — 反射对 PC 场景至关重要，但 RA 反馈无跨任务持久化 | Experimental gap |

**Impact on evidence level**: B-1 证据等级升级为 **A（直接技术实现 + 多个 GUI 应用缺失证据）**

**Suggested addition to Update Log**:
| Date | Event | Change |
|------|-------|--------|
| 2026-03-06 | Reflexion + MobileAgentV2 + PCAgent 精读 | 新增证据 新-1~3；B-1 升级为 A 级；Reflexion 提供直接技术迁移路径 |

---

## 🔄 Update to B-2: GUI 探索知识的跨 App 迁移

### New Evidence from MobileGPT + SkillWeaver

| # | Location | Evidence Content | Evidence Type |
|---|----------|-----------------|---------------|
| 新-1 | Lee et al. (2024), §9, p.14 | "MobileGPT can be extended to maintain a global dataset of known tasks across apps" — 作者承认跨 app 是当前局限和未来方向 | Direct statement |
| 新-2 | Zheng et al. (2025), §4.2, p.7-8 | GPT-4o-mini 使用 GPT-4o 探索的技能库后 WebArena +54.3% relative gain — 跨 agent 技能迁移成功验证（web 域） | Experimental evidence |

**Impact on evidence level**: B-2 升级为 **A（原文直接陈述 + 跨域迁移实验证据）**

**Suggested addition to Update Log**:
| Date | Event | Change |
|------|-------|--------|
| 2026-03-06 | MobileGPT + SkillWeaver 精读 | 新增证据；B-2 升级为 A 级；SkillWeaver 验证了跨 agent 技能迁移可行性（web 域），GUI 域迁移仍空白 |

---

## ⚠️ Counter-evidence for A-3: GUI Agent 的用户中心记忆

本批次 19 篇论文中无直接针对 A-3 的新证据。
- MobileGPT 的 per-device memory 间接触及"记忆可共享性"问题（§9, p.14），但仍是 agent-centric 视角。
- A-3 证据等级和状态维持不变。

---

## 🔄 Update to B-3: 跨任务学习效果的评估框架

### New Evidence from GUI-Owl-1.5 / Mobile-Agent-v3.5

| # | Location | Evidence Content | Evidence Type |
|---|----------|-----------------|---------------|
| 新-1 | Liu et al. (2026, in Xu et al., 2026, §3.2.2, p.17) | MemGUI-Bench: native models 27.1 vs workflow agents 41.7 — 首个专门评测 GUI agent 记忆能力的基准 | Experimental evidence |
| 新-2 | Xu et al. (2026), §3.2.2, p.17 | "GUI-Owl-1.5-32B achieves 27.1, substantially outperforming all prior baselines ... Even our 8B variant surpasses all existing native baselines" — MemGUI-Bench 显示原生模型与 workflow 型 agent 仍有 14pp 差距 | Experimental gap |

**MemGUI-Bench 说明**:
- MemGUI-Bench (Liu et al., 2026, arXiv:2602.06075) 评测 GUI agent 在长期交互历史回放任务中的记忆能力
- 这是 B-3 Gap"缺乏跨会话记忆评估框架"的一个初步解答，但注意：MemGUI-Bench 目前只报告了 Easy 任务子集

**Impact on B-3**: 现有 MemGUI-Bench 部分填补了"记忆评测框架缺失"的空白，但：
(1) 仅覆盖 Easy 任务；(2) 主要评测 memory recall，而非"多次执行同类任务后效率提升"曲线

> ⚠️ NEEDS YOUR INPUT: B-3 是否应从"完全空白"修改为"有初步方案（MemGUI-Bench）但不完整"？建议将 MemGUI-Bench 加入 B-3 的"已有解答"字段并降低优先级，或将 MemGUI-Bench 作为你研究的评测 benchmark。

**Suggested addition to Update Log**:
| Date | Event | Change |
|------|-------|--------|
| 2026-03-06 | MobileAgentV3.5 精读 | 发现 MemGUI-Bench 存在；B-3 从完全空白变为有初步评测框架；建议更新优先级描述 |

---

## 🆕 New Gap Signal #1: GUI Agent 训练阶段 vs 部署阶段自进化断层

**Statement**: Current GUI agent self-evolution occurs only during pre-deployment training phases (EvoCUA, GUI-Owl, GUI-Owl-1.5), but deployed agents cannot learn from real-user interaction trajectories after deployment.

**Provisional evidence level**: A

**Evidence**:
| # | Paper | Location | Evidence Content | Evidence Type |
|---|-------|----------|-----------------|---------------|
| 1 | Xue et al. (2026) | §9, p.18 | "This disparity highlights the limits of offline learning from synthesized traces alone." — 仅靠离线合成轨迹难触及 human-level reliability | Direct statement |
| 2 | Xu et al. (2026) | §1, p.2 | "short-term and long-term memory" listed as capability but only in-context implementation — 部署后无记忆演化 | Experimental gap |
| 3 | Ye et al. (2025) | §6, p.17 | "we develop a self-evolving GUI trajectory data production pipeline" — 自进化在训练阶段；inference 时无持续学习 | Direct statement |

**Potential classification**: A 类 Gap（跨领域交叉：Self_Evolve 领域有部署后 runtime RL（MemRL），但 GUI 场景无此机制）

**Reasoning**:
- MemRL 证明 frozen-backbone + runtime memory RL 在文本任务可行
- GUI 场景所有自进化均发生在训练前，与 Self_Evolve 的"部署后持续学习"最佳实践存在领域隔离
- 与 A-4 高度相关但侧重点不同：A-4 关注"从失败中学习"，此 Gap 关注"部署后持续学习 vs 训练阶段封闭"

> ⚠️ NEEDS YOUR INPUT: 这是否构成独立的 A 类 Gap，还是应归并到 A-4 的子问题？初步建议：(1) 若你的 RQ 包含"部署后持续学习"，可独立追踪为 A-5；(2) 若仅关注探索阶段的经验利用，可作为 A-4 的扩展证据。

---

## 🆕 New Gap Signal #2: GUI 记忆能力评测框架不完整（MemGUI-Bench 初步但不充分）

**Statement**: No established benchmark exists for evaluating whether a GUI agent improves efficiency across repeated exposures to similar tasks (learning curve measurement), though MemGUI-Bench (2026) partially addresses memory recall.

**Provisional evidence level**: B

**Evidence**:
| # | Paper | Location | Evidence Content | Evidence Type |
|---|-------|----------|-----------------|---------------|
| 1 | Xu et al. (2026) | §3.2.2, p.17 | MemGUI-Bench shows 14pp gap between native models and workflow agents — 记忆能力可量化 | Experimental evidence |
| 2 | Xu et al. (2026) | §3.2.2, p.17 | MemGUI-Bench only reports "Easy" tasks — medium/hard task performance unreported | Experimental gap |
| 3 | (多篇 GUI Agent 论文) | — | 现有 24 个 GUI benchmark 均为单次任务评测，无跨会话学习曲线设计 | Indirect implication |

**Potential classification**: B 类 Gap（单领域问题；Self_Evolve 综述已有 lifelong benchmark 设计方案）

> ⚠️ NEEDS YOUR INPUT: 这与现有 B-3 高度重叠。建议：将此证据合并到 B-3 的"已有部分解答（MemGUI-Bench）但不完整"描述中，不单独追踪。

---

## 全局优先级调整建议

基于本批次精读，建议更新 gap-tracker.md 末尾的"全局优先级排序"：

| 排名 | Gap | 类型 | 证据等级变化 | 状态变化 | 更新原因 |
|------|-----|------|-----------|---------|---------|
| **1** | **A-1（Procedural Memory + GUI）** | A | B→**A** | 待验证→**精读确认** | MobileGPT + AppAgent 双原文直接陈述；MAGNET counter-evidence check 完成 |
| **2** | **A-4（探索→离线自进化）** | A | B→**A** | 待验证→**精读确认** | MobileAgentV2 + MAGNET 双原文直接陈述；Self_Evolve 领域有技术解答但未迁移 GUI |
| **3** | **B-1（Reflection 持久化）** | B | B→**A** | — | Reflexion 验证技术可行；MobileAgentV2 + PCAgent 验证 GUI 缺失 |
| **4** | **A-2（Episodic Memory + GUI）** | A | B→**A** | 待验证→**精读确认** | GenerativeAgents + MemGPT 验证技术蓝图；MemGUI-Bench 量化 14pp 差距 |
| **5** | **B-2（跨 App 迁移）** | B | B→**A** | — | MobileGPT 直接陈述 + SkillWeaver 实验验证跨 agent 迁移 |
| **6** | **A-3（User-Centric + GUI）** | A | 不变（B） | — | 本批次无新证据 |
| **7** | **B-3（评估框架）** | B | — | 有初步方案 | MemGUI-Bench 部分填补；优先级可降低 |

---

## 需要合并到现有文件的操作清单

### gap-tracker.md 每个条目需要：
1. **A-1**: 添加 MobileGPT 新-1/2/3 证据；更新证据等级 B→A；更新状态；补充 MAGNET/MobileGPT counter-evidence 行
2. **A-2**: 添加 Generative Agents + MemGPT + MemGUI-Bench 证据；更新证据等级 B→A；更新技术蓝图描述
3. **A-3**: 无更新
4. **A-4**: 添加 MobileAgentV2 + MAGNET 新证据；更新证据等级 B→A；补充 AWM/ExpeL/SkillRL/EvoCUA counter-evidence
5. **B-1**: 添加 Reflexion + MobileAgentV2 + PCAgent 证据；更新证据等级
6. **B-2**: 添加 MobileGPT + SkillWeaver 证据
7. **B-3**: 添加 MemGUI-Bench 说明；调整"完全空白"描述
8. **全局优先级表**: 更新证据等级列

### 新增内容：
- 🆕 New Gap #1（部署阶段 vs 训练阶段自进化断层）—— 待你确认是否独立追踪
- 🆕 New Gap #2（记忆评测框架）—— 建议合并入 B-3 而不单独追踪

### 各笔记中已有的证据（需要从笔记引用到 gap-tracker）：
完整证据字符串（Author, Year, §Section, p.Page）：
- MobileGPT: Lee et al. (2024, ACM MobiCom), §9, p.14
- AppAgent: Zhang et al. (2023/2025 CHI), Introduction, p.2 | §3.3, p.5
- Mobile-Agent-v2: Wang et al. (2024, arXiv:2406.01014), §3.5, p.6 | §4.3, p.8
- MAGNET: Sun et al. (2026, arXiv:2601.19992), Limitations, p.9
- GUI-Owl-1.5: Xu et al. (2026, arXiv:2602.16851), §3.2.2, p.17 | §1, p.2
- Generative Agents: Park et al. (2023, UIST), §1, p.1 | §4.2, p.9
- MemGPT: Packer et al. (2023), Abstract, p.1 | §2.3, p.3
- Reflexion: Shinn et al. (2023), §3, p.5 | §5, p.9
- AWM: Wang et al. (2024, arXiv:2409.07429), §2.2-2.3, p.3
- ExpeL: Zhao et al. (2024, AAAI), §4.2, p.4 | §6, p.10
- SkillRL: Xia et al. (2026, arXiv:2602.08234), §3.2, p.4
- EvoCUA: Xue et al. (2026), §9, p.18
