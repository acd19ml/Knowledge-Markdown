# Research Gap 追踪 — GUI Agent

## Gap 候选列表

---

### Gap 1：GUI Agent 缺乏跨任务、跨会话的记忆机制

- **证据强度**：强（几乎所有现有系统均无此能力）
- **支撑证据**：
  - 论文 Section 3.2.1：个性化服务"通常通过记忆模块实现"，但仅 Friday 有初步尝试
  - 论文 Section 4（Table 1）：23个系统中无一设计跨会话记忆
  - 论文 Section 6.2：安全性问题限制了用户数据的跨会话保留
  - [comparison-matrix.md](comparison-matrix.md)：21/23 系统无长期记忆
  - [Agent_Memory/](../Agent_Memory/) 综述指出：长期记忆（Episodic + Semantic）是基础 Agent 能力，但在 GUI 领域几乎缺失
- **潜在研究方向**：
  - 将 Agent_Memory 综述中的 Episodic Memory 机制移植到 GUI Agent：记录"在 App X 中，任务 Y 的操作序列是 Z"
  - 设计 GUI 专用的记忆检索机制（基于截图相似性 / 任务类型匹配）
- **可行性评估**：高（技术基础成熟，主要是领域应用工作）
- **所需资源**：跨会话 GUI 任务数据集（目前不存在，需自建）

---

### Gap 2：GUI 知识无法跨应用迁移

- **证据强度**：强（探索型系统均报告此问题）
- **支撑证据**：
  - 论文 Section 4：AppAgent、MobileGPT、AutoDroid 的探索知识库均为 App 级别，无法共享
  - 论文 Section 4："Given the diversity of currently available applications and websites, it is impractical to collect a large amount of data for training in every unfamiliar GUI environment."
  - [comparison-matrix.md](comparison-matrix.md) 观察 2：AppAgent/MobileGPT/AutoDroid 的知识均不可跨 App 迁移
- **潜在研究方向**：
  - 构建跨 App 的通用 GUI 元素知识图谱（"返回按钮通常在左上角"类型的通用规律）
  - 使用 Self-Evolving 机制：探索多个 App 后，提炼通用 GUI 操作规律（类比 [Self_Evolve/](../Self_Evolve/) 中的知识泛化）
- **可行性评估**：中（需要大规模跨 App 探索数据 + 知识提炼机制设计）
- **所需资源**：多 App 探索数据集、知识图谱构建工具

---

### Gap 3：从单任务 Reflection 到跨任务自我进化的缺失

- **证据强度**：强（Reflection 存在但不持久化）
- **支撑证据**：
  - Mobile-Agent-v2 的 Reflection Agent 监测动作前后屏幕变化，但反思结果不写入长期记忆
  - MMAC-Copilot 的 Mentor 角色提供反馈，同样仅用于当前任务
  - 论文 Section 4："GUI Agents utilize knowledge obtained from memory or files during the exploration stage"——但未涉及如何将反思结果转化为长期知识
  - [Self_Evolve/](../Self_Evolve/) 综述中的 Reflection + Memory 结合方案在 GUI 场景中尚无对应研究
- **潜在研究方向**：
  - 设计 GUI Agent 的"反思→沉淀"机制：将每次任务的 Reflection 结果写入长期记忆，供后续任务调用
  - 构建 GUI 场景下的 Self-Evolving 闭环：探索 → 执行 → 反思 → 沉淀 → 改进策略
- **可行性评估**：高（Reflection + Memory 的组合是成熟技术，缺的是 GUI 场景适配）
- **所需资源**：跨任务评估框架（现有基准均为单任务）

---

### Gap 4：GUI Agent 的个性化能力几乎为空白

- **证据强度**：强（仅1个系统有初步尝试）
- **支撑证据**：
  - 论文 Section 3.2.1："Presently, personalization is usually realized through the memory modules of the agents"，但仅 Friday 将用户画像写入声明性记忆
  - 论文 Section 6.2：Data Masking 方案限制了个性化数据的利用
  - [comparison-matrix.md](comparison-matrix.md)：23/23 系统无跨会话用户偏好记忆
  - 对比 [Agent_Memory/02_taxonomy/](../Agent_Memory/02_taxonomy/)：User-Centric Memory 是独立的研究维度，但在 GUI Agent 中几乎未出现
- **潜在研究方向**：
  - 将 Agent_Memory 中 User-Centric Memory 的设计迁移到 GUI Agent：记录用户的 App 使用偏好、常用操作路径
  - 隐私保护的个性化方案：本地存储用户画像，仅允许匿名化聚合
- **可行性评估**：中（技术可行，但隐私-性能权衡设计困难）
- **所需资源**：用户纵向 GUI 使用数据（极难获取）

---

### Gap 5：评估体系无法衡量跨任务学习效果

- **证据强度**：中（从现有 benchmark 设计推断）
- **支撑证据**：
  - 论文 Section 5（Table 2）：24个数据集均为单次任务，无跨会话 benchmark
  - Success Rate 为 0/1 指标，无法测量"第二次完成同类任务是否更快"
  - GPT-4V 自动评估（85.3% 一致率）提供了可扩展的评估基础
- **潜在研究方向**：
  - 设计跨会话 GUI benchmark：同一 Agent 在多次接触同类任务后的成功率和效率变化曲线
  - 借鉴 [Self_Evolve/07_benchmarks.md](../Self_Evolve/07_benchmarks.md) 中的自进化评估方法
- **可行性评估**：中（需要设计新数据集和评估协议）
- **所需资源**：纵向实验数据收集框架

---

## Gap 优先级排序

1. **Gap 3（单任务 Reflection → 跨任务自进化）** — 技术可行性最高，现有 Reflection 机制只需扩展持久化；与 Self_Evolve 知识库直接打通；是 GUI Agent + Memory + Self-Evolve 三者的交叉点
2. **Gap 1（跨任务跨会话记忆）** — 影响最广（23/23 系统缺失），但需新数据集支撑
3. **Gap 2（跨 App 知识迁移）** — 研究价值高，但数据获取难度大
4. **Gap 4（个性化）** — 方向明确，但隐私壁垒高
5. **Gap 5（跨任务评估体系）** — 是其他 Gap 得以量化的前提，但属于基础设施工作
