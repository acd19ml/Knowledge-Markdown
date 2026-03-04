# Task Automation Pipeline：从探索到利用

> 论文 Section 4（Pages 18–20）

---

## 核心问题

> "How can agents efficiently automate complex tasks?"

GUI 任务的多样性决定了不可能对每个新 GUI 环境都预先收集大量训练数据：
- 不同应用的操作方式各异
- 相同图标在不同 GUI 上可能代表不同功能
- 探索阶段是应对这种多样性的可行解决方案

---

## 两阶段自动化流程

```
┌──────────────────────────────────────────────────────────┐
│                    Two-Stage Pipeline                     │
│                                                          │
│   ┌─── Explore Phase ────┐    ┌─── Exploitation Phase ──┐│
│   │                      │    │                          ││
│   │  弱 Agent 随机探索    │→→→│  强 Agent 利用知识执行    ││
│   │  记录交互方式 + 子任务 │    │  规划 → 动作 → 反思      ││
│   │  构建知识数据库        │    │  Critic 评估完成状态     ││
│   └──────────────────────┘    └──────────────────────────┘│
│                                           ↑               │
│                                        Memory             │
└──────────────────────────────────────────────────────────┘
```

---

## 探索阶段（Exploration Phase）

**目标**：在执行任务之前，先自主探索 GUI 环境，建立关于该环境的知识库。

| 系统 | 探索策略 | 记录内容 |
|------|---------|---------|
| **AppAgent** | Trial & Error：随机交互 UI 元素，观察界面变化 | 功能描述、操作规律 |
| **MobileGPT** | 随机探索器（AndroidEnv）+ 用户轨迹监控器 → 访问尽可能多的屏幕 | 每个屏幕的可执行子任务列表 |
| **AutoDroid** | 随机探索所有 UI 元素 → 总结功能 | 应用的完整功能图谱 + UI 元素对应任务 |

**WESE 框架的系统化表述**：
> 弱 Agent（Weak）负责探索积累知识 → 强 Agent（Strong）利用知识高效执行

---

## 利用阶段（Exploitation Phase）

**目标**：利用探索阶段积累的知识，高效、准确地执行用户任务。

标准执行循环：

```
任务输入
  │
规划（Planning）→ 分解子任务
  │
动作（Action）→ 执行，参考 Memory 中的知识
  │
反思（Reflection）→ Critic 评估是否完成
  │ (如未完成)
重规划/纠错 → 回到动作步骤
  │ (完成)
结果输出
```

**Critic 的作用**：
- 判断当前子任务是否完成
- 提供纠错建议
- 评估是否需要重组子任务

**代表系统 MMAC-Copilot 的 Exploitation 实现**：
- Planner 观察任务并分解
- Viewer + Video Analyst 细化子任务
- Viewer + Programmer 执行子任务
- Mentor 评估并反馈是否需要调整

---

## 与 Self-Evolving Agents 的关联

| 两阶段流程 | Self-Evolve 对应概念 |
|-----------|-------------------|
| 探索阶段（随机探索积累知识） | 自我进化中的"数据收集"或"经验积累"阶段 |
| 利用阶段（基于知识执行） | 策略优化 + 反馈学习 |
| 知识数据库（Memory） | [Agent_Memory/03_operations/](../Agent_Memory/03_operations/) 中的记忆存储与检索 |
| Reflection/Critic | [Self_Evolve/02_model-centric/](../Self_Evolve/02_model-centric/) 中的自我反思机制 |

---

## 关键 Research Gap

1. **探索效率**：当前探索策略均为**随机探索**，缺乏目标导向的智能探索策略
2. **知识迁移**：每个新应用都需要独立探索，**跨应用的知识迁移**几乎没有研究
3. **知识更新**：GUI 应用会随版本更新改变界面，探索得到的知识可能过时，**持续更新机制**缺失
4. **探索与任务的协同**：能否在执行任务的同时持续积累探索知识？（在线学习）

---

## Personal Research Notes

- [ ] **最强 Gap**：探索阶段的知识**无法跨应用共享**。同为"设置"按钮，Android 系统下不同 App 的位置各异，但存在共性规律——能否建立跨 App 的通用 GUI 知识图谱？
- [ ] 两阶段流程本质上是 [Self_Evolve/](../Self_Evolve/) 中"探索→利用"框架在 GUI 场景的具体实例化，两者理论基础相同
- [ ] Reflection/Critic 机制目前仅作用于**单次任务内**，如果将 Critic 的反馈结果持久化存储（写入 Memory），就能实现跨任务的自我进化——这正是 GUI Agent + Self-Evolve 的交叉点
- [ ] MobileGPT 在探索阶段让 LLM 生成"可执行子任务列表"，这实际上是在建立 Procedural Memory（程序性记忆）——与 [Agent_Memory/02_taxonomy/2.2_cognitive-mechanisms.md](../Agent_Memory/02_taxonomy/) 直接关联
