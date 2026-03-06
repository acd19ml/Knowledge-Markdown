# 综述分类框架草稿 —— GUI Agent × Memory × Self-Evolving

> **状态**: Draft v0.3 — 已将第三维重构为严格的两层 taxonomy (`Match Operator × Application Carrier`)
> **核心问题**: 如何从 `记忆` 和 `自进化` 两个维度，对现有 GUI Agent 系统进行系统性分类，并定位 `experience-dependent procedural knowledge` 尚未被覆盖的研究空间？

---

## 一、Formalized Research Questions

本草稿不再使用泛化的“GUI Agent 如何从经验中学习”表述，而是正式收敛到当前主线：

> **Main RQ**: **LLM-based GUI Agent 如何表示、写回并复用那些超出基础模型先验的 `experience-dependent procedural knowledge`，使其在重复任务、同 app 跨任务和近邻 app-family 场景中稳定提升执行表现？**

为支撑这个 Main RQ，综述/分类框架需要回答四个 Sub-RQ：

- **Sub-RQ1（What）**: 哪些知识对象值得被视为可积累的经验资产？如何区分 `generic GUI prior` 与真正值得持久化的 `Skills / World / Episodes / User`？
- **Sub-RQ2（When）**: GUI 经验是在 `pre-task / in-task / post-task / cross-task` 的哪个阶段被写入或改写？现有系统的写回时机有什么结构性缺口？
- **Sub-RQ3（How）**: 经验知识通过什么机制被复用？能否将“如何找到经验”和“如何施加经验”拆成严格的两层 taxonomy？
- **Sub-RQ4（Gap Mapping）**: 当前矩阵中的哪些格子已经被占据、哪些只是 weakly occupied、哪些是高价值空白？这些空白如何映射到 A-1 / A-2 / A-3 / A-4？

这个问题连接了三个已有综述的核心主题：

- **GUI Agent**（GA Survey）: GUI 理解 + 任务自动化
- **Agent Memory**（AM Survey）: 知识的存储、检索、更新机制
- **Self-Evolving Agents**（SE Survey）: 从经验中改进策略的能力

---

## 二、ME/CE 检验结果

为避免 taxonomy 只是“直觉上有用”，这里先对草稿做一次 ME/CE 检验。

### 2.1 检验单位

- **检验单位**应是 `capability pattern / memory module`，而不是整篇系统论文。
- 原因：一个系统可以同时包含多种知识对象和多种复用机制。例如 MAGNET 同时覆盖 `Skills + World`，且既有 similarity retrieval，也最终通过 prompt/context injection 生效。

### 2.2 逐维检验

| 维度 | 当前定义 | ME 结果 | CE 结果 | 结论 |
|------|----------|---------|---------|------|
| **What** | Skills / World / Episodes / User | **部分通过** | **通过** | 对单个 memory unit 基本互斥；但对整系统不互斥，因为同一系统可同时含多类 memory |
| **When** | pre-task / in-task / post-task / cross-task | **基本通过** | **通过** | 对单次写回事件是互斥的；对混合系统则一篇论文可覆盖多个时机 |
| **How (old)** | 精确 / 相似 / 泛化 / 注入 | **不通过** | **部分通过** | `注入` 是 application carrier，而前三者是 matching operator，不在同一抽象层 |
| **How (new)** | Match Operator × Application Carrier | **通过** | **通过** | 两层后每层内部语义统一；组合后可形成严格的 capability descriptor |

### 2.3 正式判定

- **当前 taxonomy draft 通过 CE（Collectively Exhaustive）用于主线问题诊断**:
  对“经验知识学什么、何时学、如何复用”三件事已经形成覆盖。
- **重构后 taxonomy draft 在维度定义层面通过 ME/CE**:
  第三维已正式拆成两层，因此“找经验”和“施加经验”不再混杂。
- **但在 system-level 映射层面仍不是严格单标签分类**:
  同一系统依然可能同时包含多个 knowledge type、多个 timing 和多个 carrier。这是系统本身多模块化导致的，不是 taxonomy 失效。
- **因此本文件现在可同时承担两种用途**:
  1. 作为严格 taxonomy 定义（层级本身）
  2. 作为 diagnostic occupancy map（系统落位）

---

## 三、分类框架（草稿）

### 维度 1：知识积累的对象是什么？（What is learned?）

| 类别 | 内容 | 对应 AM 认知类型 | GUI 场景示例 |
|------|------|------------------|-------------|
| **操作技能（Skills）** | 可复用的 GUI 操作序列、局部策略与异常处理规则 | Procedural Memory | “在该类页面找搜索入口时，优先检查 overflow menu” |
| **环境知识（World）** | App 功能图谱、UI 元素语义、界面局部稳定性 | Semantic Memory | “底部导航包括聊天/通讯录/发现/我” |
| **任务经验（Episodes）** | 特定任务的完整历史轨迹、失败/成功案例 | Episodic Memory | “上次完成这个任务的完整操作记录” |
| **用户偏好（User）** | 用户的操作习惯和个人偏好 | User-Centric Memory | “该用户习惯用语音发送消息而非文字” |

### 维度 2：知识在何时积累？（When is it learned?）

| 时机 | 对应 SE 框架 | GUI 场景 | 代表系统 |
|------|-------------|---------|---------|
| **任务前探索** | Environment-Centric × Static | 探索 App 功能 | AppAgent, MobileGPT |
| **任务中反思** | Inference-Based × Sequential | 实时纠错 | Mobile-Agent-v2 |
| **任务后归纳** | Environment-Centric × Offline | 从成功/失败轨迹提炼规则 | MAGNET（弱占位）, AWM 可移植 |
| **跨任务持续** | Lifelong Learning | 持续积累更新 | Friday（仅 User）, FLEX/MemRL 可移植 |

### 维度 3：知识如何被复用？（How is it retrieved and applied?）

#### Layer 3A：Match Operator（如何找到经验）

| 类别 | 技术机制 | GUI 挑战 |
|------|---------|---------|
| **精确匹配** | 同一 App + 同一任务类型 | 匹配率低（任务无重复） |
| **相似性检索** | 向量嵌入 + 近似搜索 | 截图的高维嵌入成本 |
| **规则泛化** | 提炼 App 无关的操作规则 | 跨 App 的语义统一难 |

#### Layer 3B：Application Carrier（如何施加经验）

| 类别 | 技术机制 | GUI 挑战 |
|------|---------|---------|
| **上下文注入** | 将 memory 直接拼接到 planner / actor prompt | 上下文长度限制；易被噪声淹没 |
| **外部工具调用** | memory 作为外部检索器 / API / workflow executor 输出 | 工程复杂；需要额外 control flow |
| **策略约束** | memory 作为 action prior / reranker / verifier constraint | 需要稳定的结构化表示 |
| **记忆改写** | failure 后对 memory 本身执行 edit / split / downweight / rewrite | revision quality 难；容易退化成 case patching |

> **Interpretation rule**: 一个完整的 `How` descriptor 应写成 `Match Operator × Application Carrier`，例如 `相似性检索 × 上下文注入`，或 `规则泛化 × 策略约束`。

---

## 四、分类矩阵

基于上述三个维度，现有 GUI Agent 系统的分布：

```viz-matrix
id: knowledge-reuse-pattern
title: 匹配方式 × 任务阶段（Carrier 见单元格标签）
xAxis: [精确匹配, 相似性检索, 规则泛化]
rows:
  - key: pre_task
    label: 任务前探索
    lanes: [Skills, World]
  - key: in_task
    label: 任务中反思
    lanes: [Skills, World]
  - key: post_task
    label: 任务后归纳
    lanes: [Skills, World, Episodes, User]
  - key: cross_task
    label: 跨任务持续
    lanes: [Skills, Episodes, User]
cells:
  - row: pre_task/Skills
    col: 精确匹配
    status: existing
    label: AppAgent | 上下文注入
    link: ../GUI_Agent/03_task-automation-pipeline.md
  - row: pre_task/World
    col: 精确匹配
    status: existing
    label: AutoDroid | 上下文注入
    link: ../GUI_Agent/03_task-automation-pipeline.md
  - row: in_task/Skills
    col: 精确匹配
    status: existing
    label: Mobile-Agent-v2 | 策略约束
    link: ../GUI_Agent/03_task-automation-pipeline.md
  - row: post_task/Skills
    col: 相似性检索
    status: existing
    label: MAGNET | 上下文注入
    link: comparison-matrix.md
  - row: post_task/World
    col: 相似性检索
    status: existing
    label: MAGNET | 上下文注入
    link: comparison-matrix.md
  - row: cross_task/User
    col: 精确匹配
    status: existing
    label: Friday | 上下文注入
    link: ../GUI_Agent/02_capabilities/2.4_advanced-capabilities.md
  - row: post_task/Skills
    col: 规则泛化
    status: gap
  - row: post_task/World
    col: 规则泛化
    status: gap
  - row: post_task/Episodes
    col: 相似性检索
    status: gap
  - row: post_task/Episodes
    col: 规则泛化
    status: gap
  - row: post_task/User
    col: 相似性检索
    status: gap
  - row: post_task/User
    col: 规则泛化
    status: gap
  - row: cross_task/Skills
    col: 相似性检索
    status: gap
  - row: cross_task/Skills
    col: 规则泛化
    status: gap
  - row: cross_task/Episodes
    col: 相似性检索
    status: gap
  - row: cross_task/Episodes
    col: 规则泛化
    status: gap
  - row: cross_task/User
    col: 相似性检索
    status: gap
  - row: cross_task/User
    col: 规则泛化
    status: gap
```

```text
                      Match Operator
                精确匹配  相似性检索  规则泛化
                   │         │         │
任务前   Skills    │ [AppAgent|注入]  │
探索     World     │ [AutoDroid|注入] │
───────────────────┼───────────────────
任务中   Skills    │ [MobileAgentV2|约束]
反思     World     │
───────────────────┼───────────────────
任务后   Skills    │      ●           ○
归纳     World     │      ●           ○
         Episodes  │      ○           ○
         User      │      ○           ○
───────────────────┼───────────────────
跨任务   Skills    │      ○           ○
持续     Episodes  │      ○           ○
         User      │ [Friday|注入]     ○

● = 已有研究    ○ = 空白
```

**关键观察**:

- `post_task/Skills × 相似性检索 × 上下文注入` 与 `post_task/World × 相似性检索 × 上下文注入` 已被 MAGNET 弱占位，说明“任务后归纳”不再是完全空白。
- 但 `post_task/Skills × 规则泛化`、`cross_task/Skills × 相似性检索/规则泛化` 仍为空；而且在 **carrier** 层，`外部工具调用 / 记忆改写` 几乎无人系统化实现。
- 这意味着真正缺的不是“有没有 memory”，而是**有没有可持续写回、可跨任务增长、并超出模型先验的 experience-dependent memory**。

### 4.1 Carrier Occupancy（第二层）

| Carrier | 已有弱占位 | 代表系统 | 当前缺口 |
|---------|-----------|---------|---------|
| **上下文注入** | 有 | AppAgent, MAGNET, Friday | 最常见，但最容易受 context budget 限制 |
| **外部工具调用** | 几乎无 | — | GUI memory 很少被做成独立可调用模块 |
| **策略约束** | 弱占位 | Mobile-Agent-v2 | 仅限 in-task reflection / verifier，不是 persistent memory |
| **记忆改写** | 几乎无 | — | 这正是 A-4 要填的关键层 |

---

## 五、空白格子分析（基于当前已知系统）

### 5.1 已被弱占位的格子

- **post_task / Skills / 相似性检索 × 上下文注入**: MAGNET 说明 GUI agent 已开始在任务后从成功轨迹中提炼 workflow memory，并用 similarity retrieval 复用。
- **post_task / World / 相似性检索 × 上下文注入**: MAGNET 的 stationary memory 说明任务后 world knowledge（UI element/function pairs）也已出现可检索实现。

这些格子不应再叫“完全空白”，而应叫 **weakly occupied**：

- 已有 system-level 正例
- 但仍局限于 per-app / success-only / similarity retrieval
- 还没有达到 main-line 所要求的 `experience-dependent procedural delta memory`

### 5.2 仍然高价值的结构性空白

- **post_task / Skills / 规则泛化**
  - 对应 **A-1 的核心空白**
  - 目前没有系统能把任务后归纳得到的 GUI 技能稳定提升到 app-family 甚至跨 app 的规则泛化层
- **post_task / Episodes / 相似性检索 / 规则泛化**
  - 对应 **A-2 的核心空白**
  - 当前 GUI taxonomy 若不显式加入 `Episodes`，会把情节记忆问题直接隐藏掉
- **post_task / Skills / 任意 Match Operator × 记忆改写**
  - 对应 **A-4 的核心空白**
  - 真正缺的不是“能不能检索旧经验”，而是 failure 后能否系统性改写 memory
- **post_task / User / 全部**
  - 对应 **A-3**
  - Friday 只弱占位 `cross_task/User/精确`，任务后用户画像归纳仍几乎空白
- **cross_task / Skills / 相似性检索 或 规则泛化**
  - 对应 **A-1 + A-4 的交叉空白**
  - 真正缺的是部署后持续增长、可写回、可复用的 procedural memory，而不是一次性 pre-task exploration 或 training-time skill distillation
- **cross_task / Episodes / 相似性检索 或 规则泛化**
  - 对应 **A-2**
  - 也就是 GUI 场景下真正 deployment-generated episodic memory 几乎不存在

### 5.3 对主线的直接含义

如果当前主线锁定为 `experience-delta procedural memory`，那么最关键的目标格子不是所有空白格，而是这两个：

1. **post_task / Skills / 规则泛化**
   - 证明经验归纳不是 task cache / workflow memo
   - 而是真正能抽出带条件的 procedural rule
2. **cross_task / Skills / 相似性检索 或 规则泛化**
   - 证明这些规则不是写完即死，而是能在后续任务持续复用

而 **A-4** 的价值在于：

- 它不是额外再造一种 memory type
- 而是补上第二层 taxonomy 中最缺的 **Application Carrier = 记忆改写**
- 也就是提供 `post_task -> cross_task` 的写回机制，使这两个关键格子真正连起来

---

## 六、本综述的拟定贡献框架

### 贡献 1：统一分类体系

提出一个三维分类框架（What × When × How），其中第三维被严格拆成 `Match Operator × Application Carrier` 两层 taxonomy，用于系统描述 GUI Agent 的“经验学习”能力，覆盖已有研究并定位空白。

### 贡献 2：跨领域 Gap 分析

基于 GUI_Agent × Agent_Memory × Self_Evolve 三个综述的交叉分析，指出：

- **A-1**: Procedural Memory 机制在 GUI 场景的空白
- **A-2**: Episodic Memory 机制在 GUI 场景的空白
- **A-3**: User-Centric Memory 在 GUI 场景的空白
- **A-4**: Offline Experience Evolution 在 GUI 场景的空白

### 贡献 3（可选）：原型实现与验证

选择可行性最高的 Gap（A-1 + A-4）进行原型实现，在现有 benchmark 上验证 `experience-delta procedural memory` 的有效性。

---

## 七、待补充论文清单（来自关键引用追踪）

| 论文 | 来源 | 需要补充的原因 |
|------|------|----------------|
| **AWM**（Wang et al., 2024） | Self_Evolve SE-3.2 | A-1 的核心技术来源 |
| **SkillWeaver**（Zheng et al., 2025） | Self_Evolve SE-3.2 | A-1 的扩展方案 |
| **Generative Agents**（Park et al., 2023） | Agent_Memory AM-3.2.3 | A-2 的情节记忆蓝图 |
| **MemGPT** | Agent_Memory AM 综述引用 | A-2 的记忆管理机制 |
| **A-Mem** | Agent_Memory AM-3.3.1 | A-3 的用户记忆方案 |
| **Friday** | GUI_Agent SE-3.2.1 | 当前最接近 A-3 的 GUI 系统 |

---

## 八、综述章节初步设计

```text
1. Introduction
   - GUI Agent 的能力边界与“记忆短板”
   - 三个领域的交叉点

2. Background
   - LLM-based GUI Agent 基础
   - Agent Memory 的认知类型框架
   - Self-Evolving Agents 的进化机制

3. GUI Agent 的现有“经验学习”能力综述（三维分类框架）
   - 3.1 任务前探索型
   - 3.2 任务中反思型
   - 3.3 任务后归纳型
   - 3.4 跨任务持续型（极少）

4. 跨域 Gap 分析（本文核心贡献）
   - A-1: Procedural Memory for GUI
   - A-2: Episodic Memory for GUI
   - A-3: User-Centric Memory for GUI
   - A-4: Offline Experience Evolution for GUI

5. 方法论设计（可选）
   - experience-delta procedural memory
   - failure-driven memory write-back

6. 挑战与机遇
   - 计算成本
   - 隐私
   - 评估体系

7. Conclusion
```

---

## 九、关联文件

| 主题 | 文件 |
|------|------|
| 矩阵视角（现有系统分布） | [comparison-matrix.md](comparison-matrix.md) |
| 全局 Gap 优先级 | [gap-tracker.md](gap-tracker.md) |
| 当前主线定义 | [main-line.md](main-line.md) |
