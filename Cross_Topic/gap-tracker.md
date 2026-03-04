# 全局 Research Gap 追踪 — 跨综述分层视角

> **三层分类**：
> - **A类**：跨领域交叉 Gap —— 领域 X 的技术未被应用到领域 Y。竞争者少，发表价值最高。
> - **B类**：单领域问题 + 另一领域有成熟解答。需验证移植有效性，工作量可控。
> - **C类**：单领域内残留问题，无跨领域连接需求。
>
> **参考文件**：
> - 矩阵：[master-comparison-matrix.md](master-comparison-matrix.md)
> - GUI Agent 细节：[../GUI_Agent/gap-tracker.md](../GUI_Agent/gap-tracker.md)
> - 领域交叉分析：[gui-agent-x-memory.md](gui-agent-x-memory.md) | [gui-agent-x-self-evolving.md](gui-agent-x-self-evolving.md)

---

## A 类 Gap：跨领域交叉（最高价值）

### A-1：GUI Agent 的程序性记忆机制（Procedural Memory for GUI）

**核心问题**：GUI Agent 探索阶段积累的操作序列知识以原始列表存储，无法归纳为可复用的跨任务技能。

**跨领域交叉点**：
- **Self_Evolve 提供了技术**：AWM 从成功轨迹提取参数化工作流模板；SkillWeaver 管理可复用技能库 → 这是 GUI 探索知识的正确组织形态
- **Agent_Memory 提供了概念框架**：Procedural Memory（持久、可执行的行动策略）→ GUI 操作技能的形式定义

**为何没有人做**：GUI_Agent 作者不熟悉 Self_Evolve 的技能归纳方法；AWM/SkillWeaver 在通用 Web 场景验证，未适配 GUI 截图的高维特性。

**潜在方案**：将 AWM 的"轨迹→模板"归纳机制应用于 GUI 探索轨迹；提取跨 App 可复用技能（如"找到任意 App 的返回入口"）

**支撑证据**：
- [GUI_Agent/comparison-matrix.md](../GUI_Agent/comparison-matrix.md)：21/23 系统无持久化 Procedural Memory
- [Self_Evolve/03_env-centric/3.2_dynamic-experience.md](../Self_Evolve/03_env-centric/3.2_dynamic-experience.md)：AWM、SkillWeaver 在通用场景验证
- [Agent_Memory/02_taxonomy/2.2_cognitive-mechanisms.md](../Agent_Memory/02_taxonomy/2.2_cognitive-mechanisms.md)：Procedural Memory 形式定义

**可行性**：高 | **所需资源**：GUI 探索轨迹数据（AndroidEnv/WebArena 可生成）

---

### A-2：GUI Agent 的情节记忆与跨会话学习（Episodic Memory for GUI）

**核心问题**：GUI Agent 每次任务结束后，完整交互轨迹（屏幕状态、操作序列、成功/失败）被丢弃，下次任务从零开始。

**跨领域交叉点**：
- **Agent_Memory 提供了蓝图**：Generative Agents 和 MemGPT 将过去经历存储为情节记忆，通过相似性检索注入当前上下文
- **Self_Evolve 提供了终身框架**：ArcMemo / FLEX / Evolver 的终身学习架构可扩展到 GUI 场景

**难点**：GUI 轨迹包含截图（高维视觉），现有情节记忆的检索机制多用于文本；跨会话 GUI 数据集不存在。

**潜在方案**：多模态情节记忆 (截图嵌入, 任务描述, 操作序列, 结果) → 向量化存储 → 相似任务检索历史轨迹

**支撑证据**：
- [GUI_Agent/gap-tracker.md Gap 1](../GUI_Agent/gap-tracker.md)：23/23 系统无跨任务记忆
- [Agent_Memory/02_taxonomy/2.2_cognitive-mechanisms.md](../Agent_Memory/02_taxonomy/2.2_cognitive-mechanisms.md)：情节记忆定义与实现

**可行性**：中 | **所需资源**：多模态检索库 + 跨会话 GUI 数据集（需自建）

---

### A-3：GUI Agent 的用户中心记忆与个性化（User-Centric Memory for GUI）

**核心问题**：GUI Agent 个性化能力极度缺失（仅 Friday 初步尝试），Agent_Memory 领域已有完整 User-Centric Memory 理论框架。

**跨领域交叉点**：
- **Agent_Memory § 3.3.1**：A-Mem（动态用户记忆）、MemoCRS（偏好追踪）提供了完整的用户偏好存储、检索、更新机制
- **GUI 场景有独特的用户信号**：操作路径（走哪条菜单路径）、偏好设置、历史任务频率、常用 App

**为何没有人做**：GUI Agent 研究以任务自动化为主，用户偏好建模被视为"软性"问题；Agent_Memory 中的 User-Centric Memory 主要在对话场景验证。

**潜在方案**：将 GUI 操作历史作为用户偏好信号 → 构建 GUI 专用用户画像（偏好路径、常用 App、操作习惯）→ 注入未来任务规划

**支撑证据**：
- [GUI_Agent/02_capabilities/2.4_advanced-capabilities.md](../GUI_Agent/02_capabilities/2.4_advanced-capabilities.md)：仅 Friday 初步尝试
- [Agent_Memory/02_taxonomy/2.3_memory-subjects.md](../Agent_Memory/02_taxonomy/2.3_memory-subjects.md)：User-Centric Memory 完整框架

**可行性**：中高 | **难点**：隐私-性能权衡设计；用户纵向数据极难获取

---

### A-4：探索阶段的经验驱动自进化（Trial & Error → Offline Experience Evolution）

**核心问题**：GUI Agent 探索阶段（AppAgent/MobileGPT）已有"尝试→观察→记录"雏形，但记录结果是静态的，不能从失败中更新策略。

**跨领域交叉点**：
- **Self_Evolve 的离线经验演化**：从轨迹（含失败）提炼经验 → 更新 Agent 策略（[Self_Evolve/03_env-centric/3.2_dynamic-experience.md](../Self_Evolve/03_env-centric/3.2_dynamic-experience.md)）
- **COPS** 提供跨任务经验共享的形式化保证

**潜在方案**：GUI 探索轨迹（成功+失败）→ LLM 分析失败原因 → 提炼"在 App X 中，避免操作 Y，改用 Z" → 写入程序记忆

**支撑证据**：
- [GUI_Agent/03_task-automation-pipeline.md](../GUI_Agent/03_task-automation-pipeline.md)：探索阶段仅记录不学习
- [Self_Evolve/03_env-centric/3.2_dynamic-experience.md](../Self_Evolve/03_env-centric/3.2_dynamic-experience.md)：离线经验演化框架

**可行性**：高 | **与 A-1 高度协同，可作为同一工作的两个模块**

---

## B 类 Gap：单领域问题 + 跨领域已有解答

### B-1：Reflection 结果的持久化（单任务 → 跨任务）

**问题**：Mobile-Agent-v2 的 Reflection Agent 能发现错误，但反思结果在任务结束后丢弃。

**已有解答**：Self_Evolve 的 Reflexion 和 Self-Refine 提供了将反思结果持久化到 Memory 的机制。

**移植路径**：Reflection 输出（"在 App X 执行 Y 时，应先做 Z"）→ 写入外部记忆 → 供后续任务检索。

**证据**：[GUI_Agent/gap-tracker.md Gap 3](../GUI_Agent/gap-tracker.md) | [Self_Evolve/02_model-centric/2.1_inference-based.md](../Self_Evolve/02_model-centric/2.1_inference-based.md)

---

### B-2：GUI 探索知识的跨 App 迁移

**问题**：AppAgent/MobileGPT 的探索知识是 App 级的，无法复用于新 App。

**已有解答**：Self_Evolve 的 AgentKB（跨领域知识库）和 COPS（可证明的跨任务经验共享）。

**移植路径**：提取 GUI 操作的 App 无关特征（UI 元素类型、页面层级结构），构建跨 App 通用知识图谱。

**证据**：[GUI_Agent/gap-tracker.md Gap 2](../GUI_Agent/gap-tracker.md) | [Self_Evolve/03_env-centric/3.2_dynamic-experience.md](../Self_Evolve/03_env-centric/3.2_dynamic-experience.md)

---

### B-3：跨任务学习效果的评估框架

**问题**：现有 24 个 GUI benchmark 均为单次任务，Success Rate 无法衡量"第二次完成同类任务是否更快"。

**已有解答**：Self_Evolve 综述的 benchmark 设计（[07_benchmarks.md](../Self_Evolve/07_benchmarks.md)）和 LlamaTouch 的多级别 UI 状态匹配。

**移植路径**：设计跨会话 GUI benchmark：同一 Agent 多次接触同类任务后的成功率和效率变化曲线。

**证据**：[GUI_Agent/04_evaluation.md](../GUI_Agent/04_evaluation.md) | [Self_Evolve/07_benchmarks.md](../Self_Evolve/07_benchmarks.md)

---

## C 类 Gap：单领域内残留问题

| Gap | 领域 | 描述 | 单领域方案 |
|-----|------|------|----------|
| **C-1：GUI 计算成本** | GUI_Agent §6.1 | 高分辨率截图 + 多步推理 = 极高成本 | 模型压缩、小骨干模型、KV Cache 优化 |
| **C-2：Agent Memory 遗忘策略** | Agent_Memory §Future | 记忆积累后旧内容如何有效遗忘 | 时间衰减、基于重要性删除、记忆整合 |
| **C-3：Self-Evolve 模型崩溃** | Self_Evolve §VI | 持续自训练可能导致分布外漂移 | 保留金标准数据、对抗性验证 |
| **C-4：GUI 幻觉与安全性** | GUI_Agent §6.2 | Feasibility/Completeness/Security 研究不足 | ResponsibleTA 框架扩展 |

---

## 全局优先级排序

| 排名 | Gap | 类型 | 核心理由 |
|------|-----|------|---------|
| **1** | **A-1（Procedural Memory + GUI）** | A | 可行性最高；AWM 直接可移植；与 A-4 协同，可构成一篇完整论文 |
| **2** | **A-4（探索 → 离线自进化）** | A | 与 A-1 共享技术栈；GUI 探索数据易得；可作为同一工作的第二贡献 |
| **3** | **B-1（Reflection 持久化）** | B | 实现成本低；可作为 A-1/A-4 的基础组件 |
| **4** | **A-2（Episodic Memory + GUI）** | A | 影响最广（23/23 缺失）；多模态检索挑战需单独解决 |
| **5** | **B-2（跨 App 迁移）** | B | 依赖 A-1 的技术基础；可作为扩展实验 |
| **6** | **A-3（User-Centric + GUI）** | A | 差异化方向；隐私壁垒高，独立成文更合适 |
| **7** | **B-3（评估框架）** | B | 是所有 Gap 验证的前提，但属于基础设施工作 |
