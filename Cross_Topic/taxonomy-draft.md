# 综述分类框架草稿 —— GUI Agent × Memory × Self-Evolving

> **状态**：Draft v0.1 —— 待文献阅读充实后更新
> **核心问题**：如何从"记忆"和"自进化"两个维度，对现有 GUI Agent 系统进行系统性分类，并定位未覆盖的研究空间？

---

## 一、核心研究问题

本综述尝试回答：

> **"LLM-based GUI Agent 如何从经验中学习，以在不同任务、应用和用户之间积累可复用的操作知识？"**

这个问题连接了三个已有综述的核心主题：
- **GUI Agent**（GA Survey）：GUI 理解 + 任务自动化
- **Agent Memory**（AM Survey）：知识的存储、检索、更新机制
- **Self-Evolving Agents**（SE Survey）：从经验中改进策略的能力

---

## 二、分类框架（草稿）

### 维度 1：知识积累的对象是什么？（What is learned?）

| 类别 | 内容 | 对应 AM 认知类型 | GUI 场景示例 |
|------|------|---------------|------------|
| **操作技能（Skills）** | 可复用的 GUI 操作序列 | Procedural Memory | "在微信中发送文件的操作步骤" |
| **环境知识（World）** | App 功能图谱、UI 元素语义 | Semantic Memory | "微信的底部导航包括聊天/通讯录/发现/我" |
| **任务经验（Episodes）** | 特定任务的完整历史轨迹 | Episodic Memory | "上次完成这个任务的完整操作记录" |
| **用户偏好（User）** | 用户的操作习惯和个人偏好 | User-Centric Memory | "该用户习惯用语音发送消息而非文字" |

### 维度 2：知识在何时积累？（When is it learned?）

| 时机 | 对应 SE 框架 | GUI 场景 | 代表系统 |
|------|------------|---------|---------|
| **任务前探索** | Environment-Centric × Static | 探索 App 功能 | AppAgent, MobileGPT |
| **任务中反思** | Inference-Based × Sequential | 实时纠错 | Mobile-Agent-v2 |
| **任务后归纳** | Environment-Centric × Offline | 从轨迹提炼技能 | （空白，AWM 可移植）|
| **跨任务持续** | Lifelong Learning | 持续积累更新 | （空白，FLEX 可移植）|

### 维度 3：知识如何被复用？（How is it retrieved and applied?）

| 复用方式 | 技术机制 | GUI 挑战 |
|---------|---------|---------|
| **精确匹配** | 同一 App + 同一任务类型 | 匹配率低（任务无重复） |
| **相似性检索** | 向量嵌入 + 近似搜索 | 截图的高维嵌入成本 |
| **规则泛化** | 提炼 App 无关的操作规则 | 跨 App 的语义统一难 |
| **提示注入** | 历史经验直接放入 LLM 上下文 | 上下文长度限制 |

---

## 三、分类矩阵

基于上述三个维度，现有 GUI Agent 系统的分布：

```
                    知识复用方式
                精确  相似  泛化  注入
                 │     │     │     │
任务前   Skills  │  [AppAgent]    │
探索     World   │  [AutoDroid]   │
─────────────────┼─────────────────
任务中   Skills  │              │ [Mobile-Agent-v2]
反思     World   │              │
─────────────────┼─────────────────
任务后   Skills  │    ○    ○    ○   （完全空白）
归纳     World   │    ○    ○    ○
         User    │    ○    ○    ○
─────────────────┼─────────────────
跨任务   Skills  │    ○    ○    ○   （完全空白）
持续     User    │  [Friday]  ○    ○

● = 已有研究    ○ = 空白
```

**关键观察**：右下角（任务后归纳 + 跨任务持续）几乎全部空白，而这些位置正是影响 GUI Agent 长期效用的核心能力。

---

## 四、本综述的拟定贡献框架

### 贡献 1：统一分类体系

提出一个三维分类框架（What × When × How），系统描述 GUI Agent 的"经验学习"能力，覆盖已有研究并定位空白。

### 贡献 2：跨领域 Gap 分析

基于 GUI_Agent × Agent_Memory × Self_Evolve 三个综述的交叉分析（本目录内的所有文件），指出：
- **A-1**：Procedural Memory 机制在 GUI 场景的空白
- **A-2**：Episodic Memory 机制在 GUI 场景的空白
- **A-3**：User-Centric Memory 在 GUI 场景的空白
- **A-4**：离线经验演化在 GUI 场景的空白

### 贡献 3（可选）：原型实现与验证

选择可行性最高的 Gap（A-1 + A-4）进行原型实现，在现有 benchmark（AndroidEnv/Mind2Web）上验证"GUI Procedural Memory"的有效性。

---

## 五、待补充论文清单（来自关键引用追踪）

| 论文 | 来源 | 需要补充的原因 |
|------|------|-------------|
| **AWM**（Wang et al., 2024）| Self_Evolve SE-3.2 | A-1 的核心技术来源，需精读 |
| **SkillWeaver**（Zheng et al., 2025）| Self_Evolve SE-3.2 | A-1 的扩展方案，需精读 |
| **Generative Agents**（Park et al., 2023）| Agent_Memory AM-3.2.3 | A-2 的情节记忆蓝图，需精读 |
| **MemGPT** | Agent_Memory AM 综述引用 | A-2 的记忆管理机制，需精读 |
| **A-Mem** | Agent_Memory AM-3.3.1 | A-3 的用户记忆方案，需精读 |
| **WESE**（Huang et al., 2024）| GUI_Agent SE-4 | 探索→利用框架的系统化表述 |
| **Friday** | GUI_Agent SE-3.2.1 | 当前最接近 A-3 的 GUI 系统 |

---

## 六、综述章节初步设计

```
1. Introduction
   - GUI Agent 的能力边界与"记忆短板"
   - 三个领域的交叉点

2. Background
   - LLM-based GUI Agent 基础（from GUI_Agent survey）
   - Agent Memory 的认知类型框架（from AM survey）
   - Self-Evolving Agents 的进化机制（from SE survey）

3. GUI Agent 的现有"经验学习"能力综述（三维分类框架）
   - 3.1 任务前探索型（AppAgent、MobileGPT、AutoDroid）
   - 3.2 任务中反思型（Mobile-Agent-v2）
   - 3.3 持久化记忆型（Friday）—— 极少

4. 跨域 Gap 分析（本文核心贡献）
   - A-1: Procedural Memory for GUI
   - A-2: Episodic Memory for GUI
   - A-3: User-Centric Memory for GUI
   - A-4: Offline Experience Evolution for GUI

5. 方法论设计（可选）
   - GUI Procedural Memory 框架（A-1 + A-4 的融合）
   - 实验设计

6. 挑战与机遇
   - 计算成本
   - 隐私
   - 评估体系（B-3）

7. Conclusion
```

---

## 七、关联文件

| 主题 | 文件 |
|------|------|
| GUI Agent × Memory 详细分析 | [gui-agent-x-memory.md](gui-agent-x-memory.md) |
| GUI Agent × Self-Evolving 详细分析 | [gui-agent-x-self-evolving.md](gui-agent-x-self-evolving.md) |
| 矩阵视角（现有系统分布）| [master-comparison-matrix.md](master-comparison-matrix.md) |
| 全局 Gap 优先级 | [gap-tracker.md](gap-tracker.md) |
