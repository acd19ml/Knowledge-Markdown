# Master Comparison Matrix — 跨综述交叉视角

> **定位**：本矩阵不重复各子领域综述已有的单域对比（GUI_Agent/comparison-matrix.md 覆盖了 23个系统的单域维度）。
> 本矩阵聚焦于：**GUI Agent 方法在 Memory 和 Self-Evolving 两个维度上的能力分布**，以及哪些位置是空白。

---

## 维度说明

| 列 | 来源 | 说明 |
|---|---|---|
| **记忆认知类型** | Agent_Memory 综述 § 3.2 | 五种认知机制：Sensory / Working / Episodic / Semantic / Procedural |
| **记忆持久性** | Agent_Memory 综述 § 2.1 | 任务内 / 跨任务 / 跨会话 / 永久 |
| **记忆主体** | Agent_Memory 综述 § 3.3 | Agent-centric / User-centric / 无 |
| **自进化类型** | Self_Evolve 综述 § III–IV | 推理时 / 离线经验 / 在线经验 / 终身学习 |
| **进化时机** | Self_Evolve 综述 § III–IV | 任务内（单步纠错）/ 任务后（离线）/ 跨任务持续 |
| **跨任务迁移** | 综合分析 | 否 / 任务级 / 应用级 / 跨应用 |

---

## 矩阵

| 系统 | 来源 | 任务类型 | 记忆认知类型 | 记忆持久性 | 记忆主体 | 自进化类型 | 进化时机 | 跨任务迁移 | 最接近的成熟方案（来自其他综述） |
|------|------|---------|-----------|----------|---------|----------|---------|----------|------|
| **AppAgent** | GUI_Agent | Mobile | Procedural（雏形）| 跨任务（应用级）| Agent-centric | Trial & Error | 任务前探索 | 应用级，不可跨 App | AWM（Self_Evolve: 离线经验→程序记忆） |
| **MobileGPT** | GUI_Agent | Mobile | Procedural（雏形）| 跨任务（应用级）| Agent-centric | Trial & Error | 任务前探索 | 应用级 | SkillWeaver（Self_Evolve: 技能库管理） |
| **AutoDroid** | GUI_Agent | Mobile | Semantic（雏形）| 跨任务（应用级）| Agent-centric | Trial & Error | 任务前探索 | 应用级 | AgentKB（Self_Evolve: 跨领域知识库） |
| **Mobile-Agent-v2** | GUI_Agent | Mobile | Working | 任务内 | Agent-centric | 推理时自我修正 | 任务内（实时）| 否 | Reflexion（Self_Evolve: 顺序自我修正） |
| **MMAC-Copilot** | GUI_Agent | Desktop | Working + 检索 | 任务内 | Agent-centric | 无（Reflection 不持久）| 任务内 | 否 | MemoryBank（Agent_Memory: 外部向量存储）|
| **Friday** | GUI_Agent | Desktop | Semantic（用户画像）| 跨会话 | User-centric | 无 | — | 否 | A-Mem（Agent_Memory: 动态用户记忆）|
| **UFO** | GUI_Agent | Desktop | Working | 任务内 | Agent-centric | 无 | — | 否 | — |
| **WebAgent** | GUI_Agent | Web | Working | 任务内 | Agent-centric | 无 | — | 否 | — |
| **WebVoyager** | GUI_Agent | Web | Working | 任务内 | Agent-centric | 无 | — | 否 | — |
| **CogAgent** | GUI_Agent | Web+Desktop | 无 | — | — | 无 | — | 否 | — |
| — | — | — | — | — | — | — | — | — | — |
| **AWM** | Self_Evolve | Web（通用）| Procedural | 跨任务 | Agent-centric | 离线经验 | 任务后 | 跨任务（同类）| ← **GUI Agent 急需的能力** |
| **SkillWeaver** | Self_Evolve | Web | Procedural | 跨任务 | Agent-centric | 离线经验 | 任务后 | 跨任务 | ← GUI Agent 探索知识持久化的答案 |
| **AgentKB** | Self_Evolve | 通用 | Semantic | 跨任务 | Agent-centric | 离线经验 | 任务后 | 跨领域 | ← GUI 跨 App 知识迁移的答案 |
| **ArcMemo / FLEX** | Self_Evolve | 通用 | Episodic+Semantic | 终身 | Agent-centric | 终身学习 | 持续 | 跨任务 | ← GUI Agent 终身学习的路径 |
| — | — | — | — | — | — | — | — | — | — |
| **A-Mem** | Agent_Memory | 对话 | Semantic | 跨会话 | User-centric | 无 | — | — | ← GUI Agent 个性化的现成方案 |
| **MemGPT** | Agent_Memory | 通用 | Episodic+Semantic | 跨会话 | Agent-centric | 无 | — | — | ← GUI Agent 长期记忆管理 |
| **Generative Agents** | Agent_Memory | 模拟 | Episodic | 跨会话 | Agent-centric | 无 | — | — | ← GUI Agent 情节记忆的蓝图 |

---

## 空白格局可视化

```
                  ┌────────────────────────────────────────────────────┐
                  │           GUI Agent 的记忆 × 自进化能力空间         │
                  │                                                    │
 自进化能力        │  终身学习  ○                               ●AWM    │
 （Self_Evolve）  │  离线经验  ○           ●SkillWeaver  ●AgentKB      │
                  │  在线经验  ○                                        │
                  │  推理时    ●MobAgv2                                 │
                  │  无        ●(大多数GUI Agent)  ●Friday(仅Semantic)  │
                  └──────┬──────────┬──────────┬──────────┬───────────┘
                         无      Working   Episodic  Semantic  Procedural
                                         ←─── 记忆认知类型（Agent_Memory）───→

● = 已有研究    ○ = 空白区域（当前 GUI Agent 研究缺失）
```

**结论**：GUI Agent 方法集中在左下角（无记忆 + 无/弱自进化）。右上角（Episodic/Procedural Memory + 离线/终身自进化）是完全空白的研究空间，而这些能力在 Self_Evolve 和 Agent_Memory 领域已有成熟方案。

---

## 交叉参考索引

| 主题 | 详细分析 |
|------|---------|
| GUI Agent × Memory | [gui-agent-x-memory.md](gui-agent-x-memory.md) |
| GUI Agent × Self-Evolving | [gui-agent-x-self-evolving.md](gui-agent-x-self-evolving.md) |
| 全局 Gap 分层 | [gap-tracker.md](gap-tracker.md) |
| 综述分类框架草稿 | [taxonomy-draft.md](taxonomy-draft.md) |
