# Knowledge-Base Expansion Guide
## 从综述到选题：知识库驱动的研究路径

---

## 一、你的研究路径与知识库的角色

```
阶段 1: 广泛检索          → 知识库角色：收集与分类
阶段 2: 综述写作(Interim)  → 知识库角色：提供对比证据、暴露 Gap
阶段 3: 选题与方法论确立    → 知识库角色：提供强支撑论据
阶段 4: 投稿              → 知识库角色：快速定位引用、回应审稿
```

核心原则：**知识库不是论文仓库，而是你的"外部研究记忆"**——每条笔记都应该服务于最终的 Gap 发现和方案论证。

---

## 二、知识库扩展策略：如何系统地找到你需要的论文

### 2.1 从现有知识库出发的三步扩展法

**Step 1: 种子论文的引用追踪（Backward + Forward）**

你已有的两篇综述（Agent Memory Survey、Self-Evolving Agents Survey）是极佳的种子。

- **Backward**：从这两篇综述的参考文献中，筛选与 GUI Agent 相关的论文
- **Forward**：在 Semantic Scholar / Google Scholar 中查看"谁引用了这两篇综述"，找最新的跟进工作
- **交叉点优先**：优先关注同时出现在两篇综述引用列表中的论文

**Step 2: 关键词组合检索**

在 Semantic Scholar、arXiv、Google Scholar 上使用以下组合：

| 核心组合 | 搜索关键词示例 |
|---------|-------------|
| GUI Agent + Memory | `"GUI agent" memory`, `"web agent" episodic memory`, `"computer use agent" experience` |
| GUI Agent + Self-Evolving | `"GUI agent" self-improvement`, `"web agent" self-evolving`, `"GUI agent" continual learning` |
| 三者交叉 | `"GUI agent" memory self-improvement`, `"web agent" experience-driven evolution` |
| 相关变体 | `"computer use agent"`, `"digital agent"`, `"UI automation" LLM` |

**Step 3: 关键作者与团队追踪**

当你发现高质量论文后，追踪其作者的其他工作。GUI Agent 领域的活跃团队产出往往高度相关。

### 2.2 论文筛选优先级

面对十几篇候选论文时，按以下优先级排序阅读：

```
P0 - 必读（直接定义你的研究空间）:
    ├── 与你选题直接相关的综述论文
    ├── 提出核心框架/基准的开创性论文
    └── 近 6 个月的 SOTA 论文

P1 - 精读（构建你的论证链）:
    ├── 你计划对比的 baseline 方法
    ├── 明确指出 limitation 且与你方向相关的论文
    └── 提出你可能采用的技术手段的论文

P2 - 泛读（补充背景和广度）:
    ├── 相邻领域的参考论文
    ├── 应用场景的案例论文
    └── 早期工作（用于 background 章节）
```

---

## 三、论文处理流程：从 PDF 到可用笔记的标准工作流

### 3.1 三遍阅读法（适配知识库记录）

```
第一遍（15分钟）: 扫描式阅读
   读：Title → Abstract → Introduction 最后两段 → Conclusion
   记：填写笔记模板的 [元信息] 和 [一句话总结]
   判：决定该论文的优先级（P0/P1/P2）

第二遍（1-2小时）: 结构化阅读
   读：全文，跳过证明和实验细节
   记：填写 [核心方法]、[关键结果]、[与我的关系]
   标：在 PDF 上标记需要第三遍深入的部分

第三遍（按需）: 深度阅读
   读：实验设置、消融实验、附录
   记：填写 [方法论细节]、[可复用的实验设计]
   思：更新 [Research Gap 观察] 和 [对我研究的启发]
```

### 3.2 知识库文件组织建议

```
Knowledge-Markdown/
├── GUI_Agent/                          # 新增：GUI Agent 核心文献
│   ├── README.md                       # 本主题索引 + 领域概览
│   ├── papers/                         # 单篇论文笔记
│   │   ├── 2025_CogAgent.md
│   │   ├── 2025_WebVoyager.md
│   │   └── ...
│   ├── comparison-matrix.md            # 跨论文对比矩阵（见下文）
│   └── gap-tracker.md                  # Gap 追踪文档（见下文）
│
├── Cross_Topic/                        # 新增：交叉主题分析
│   ├── gui-agent-x-memory.md           # GUI Agent × Memory 交叉分析
│   ├── gui-agent-x-self-evolving.md    # GUI Agent × Self-Evolving 交叉分析
│   └── taxonomy-draft.md              # 你自己综述的分类框架草稿
│
├── Interim_Report/                     # 新增：综述写作素材
│   ├── outline.md                      # 综述大纲
│   ├── evidence-map.md                 # 每个论点的证据来源映射
│   └── drafts/                         # 各章节草稿
│
├── Agent_Memory/                       # 已有
├── Self_Evolve/                        # 已有
└── ...
```

---

## 四、论文笔记模板（核心标准）

以下是针对你"综述→发现 Gap→确立方法论"目标设计的笔记模板。每篇论文一个 `.md` 文件。

---

### 模板正文

```markdown
# [论文简称] — [一句话描述核心贡献]
<!-- 例: CogAgent — 首个支持高分辨率 GUI 理解的视觉语言 Agent -->

## 元信息
- **标题**: [完整英文标题]
- **作者**: [第一作者 et al.] | [团队/机构]
- **发表**: [会议/期刊, 年份] | [arXiv ID]
- **链接**: [PDF] [Code] [Project Page]
- **阅读日期**: YYYY-MM-DD
- **优先级**: P0 / P1 / P2
- **阅读状态**: 第一遍 / 第二遍 / 第三遍

## 一句话总结
<!-- 用一句话概括：这篇论文做了什么、怎么做的、效果如何 -->

## 问题与动机
- **要解决的核心问题是什么？**
- **为什么现有方案不够？**（作者指出的 limitation）
- **这个问题对 GUI Agent / Memory / Self-Evolving 领域的意义？**

## 核心方法
- **方法概述**:（2-3 段，用自己的话描述）
- **关键技术组件**:
  - 组件 1: ...
  - 组件 2: ...
- **与现有方法的核心区别**:

## 关键结果
- **使用的基准/数据集**:
- **主要指标与表现**:
  | Benchmark | 本文方法 | 最强 Baseline | 提升幅度 |
  |-----------|---------|-------------|---------|
  | ...       | ...     | ...         | ...     |
- **消融实验关键发现**:（哪些组件贡献最大）

## 局限性与未解决的问题
- **作者自述的 limitation**:
- **我观察到的 limitation**:（作者没提但我认为存在的）
- **实验设计的不足**:（数据集覆盖不全？评测指标有偏？）

## ⭐ 与我的研究的关系（最重要的部分）

### 在我的综述中的定位
- **对应我综述的哪个章节/分类**:
- **作为正面案例还是对比对象**:

### Research Gap 信号
<!-- 记录任何暗示 research gap 的线索 -->
- Gap 1: ...
- Gap 2: ...

### 可借鉴的元素
- **方法论上可借鉴的**: 
- **实验设计上可借鉴的**:
- **写作/论证方式上可借鉴的**:

### 与知识库中其他论文的关联
- 与 [论文 X] 的关系: ...（互补/竞争/扩展）
- 与 [论文 Y] 的关系: ...

## 关键引用追踪
<!-- 这篇论文引用的、值得我去读的论文 -->
- [ ] [论文名]: 原因...
- [ ] [论文名]: 原因...

## 原文关键段落摘录
<!-- 少量直接摘录，用于未来写综述时精确引用 -->
> "..." (Section X, p.Y)
<!-- 只摘录对你论证关键的 1-3 句，标明页码 -->
```

---

## 五、跨论文分析工具：对比矩阵与 Gap 追踪

### 5.1 Comparison Matrix（comparison-matrix.md）

这个矩阵是综述写作的核心武器，帮你系统对比现有方案的优劣。

```markdown
# GUI Agent 方法对比矩阵

## 维度定义
<!-- 根据你的分类框架定义对比维度 -->

| 论文 | 年份 | 输入模态 | 记忆机制 | 自我进化能力 | 任务类型 | 核心基准 | 最佳结果 | 主要局限 |
|------|------|---------|---------|------------|---------|---------|---------|---------|
| CogAgent | 2024 | 截图 | 无 | 无 | Web+Desktop | Mind2Web | XX% | 无记忆，无法从经验学习 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

## 从矩阵中观察到的模式
- 观察 1: 大多数 GUI Agent 缺少 ___ 能力
- 观察 2: Memory 机制在 ___ 方面尚未被充分探索
- 观察 3: Self-Evolving 在 GUI Agent 中仅有 ___ 尝试

## 由此产生的 Research Gap
- Gap A: ...
- Gap B: ...
```

### 5.2 Gap Tracker（gap-tracker.md）

独立维护的 Gap 追踪文档，持续更新。

```markdown
# Research Gap 追踪

## Gap 候选列表
<!-- 每发现一个潜在 Gap 就记录，标注证据强度 -->

### Gap 1: [描述]
- **证据强度**: 强 / 中 / 弱
- **支撑证据**:
  - [论文 A] 指出 "..."（Section X）
  - [论文 B] 的实验表明 ...
  - 对比矩阵显示：N 篇论文中仅 M 篇涉及此问题
- **潜在研究方向**: 
- **可行性评估**: 高 / 中 / 低
- **所需资源**: 

### Gap 2: [描述]
...

## Gap 优先级排序
<!-- 定期回顾，根据证据强度和可行性排序 -->
1. Gap X — 理由: ...
2. Gap Y — 理由: ...
```

---

## 六、从论文到综述的证据链构建

### 6.1 Evidence Map（evidence-map.md）

当你开始写综述时，用这个文档确保每个论点都有充分的文献支撑。

```markdown
# 综述论点 — 证据映射

## Chapter: Background
| 论点 | 支撑论文 | 证据类型 | 强度 |
|------|---------|---------|------|
| GUI Agent 面临 XXX 挑战 | [A], [B], [C] | 实验数据 + 定性分析 | 强 |
| ... | ... | ... | ... |

## Chapter: Existing Solutions 对比
| 论点 | 支撑论文 | 证据类型 | 强度 |
|------|---------|---------|------|
| 方法类别 1 的优势在于... | [D], [E] | 实验对比 | 强 |
| 方法类别 1 的劣势在于... | [F], 对比矩阵 | 观察 | 中 |

## Chapter: Proposed Direction
| 论点 | 支撑论文 | 证据类型 | 强度 |
|------|---------|---------|------|
| Gap 存在的证据 | [G], [H], Gap Tracker | 多源汇聚 | 强 |
| 提出的方法的可行性依据 | [I], [J] | 相关技术已验证 | 中 |
```

### 6.2 综述各章节与知识库的对应关系

```
综述章节                          知识库数据来源
─────────────────────────────────────────────────────
Background & Objectives       ← Agent_Memory/01_background.md
                                 Self_Evolve/01_background.md
                                 GUI_Agent/README.md（你需要新建）

Problem & Related Work        ← GUI_Agent/papers/*.md（单篇笔记）
                                 comparison-matrix.md

Advantages & Disadvantages    ← comparison-matrix.md
                                 各论文笔记中的 [局限性] 部分

Relationship to Proposed      ← gap-tracker.md
Solution                         Cross_Topic/*.md

Methodology                   ← 各论文笔记中的 [可借鉴的元素]
                                 Self_Evolve/02_model-centric/
                                 Agent_Memory/03_operations/

Expected Outcome              ← gap-tracker.md 中的 [潜在研究方向]

References                    ← 所有论文笔记中的 [元信息]
```

---

## 七、实操建议：拿到十几篇论文后的执行顺序

```
Week 1: 快速扫描 + 分类
  ├── 所有论文做第一遍阅读，填写笔记模板的 [元信息] + [一句话总结]
  ├── 按 P0/P1/P2 排优先级
  └── 初始化 comparison-matrix.md，确定对比维度

Week 2-3: 精读 + 对比
  ├── P0 论文做第二遍+第三遍阅读，完整填写笔记模板
  ├── P1 论文做第二遍阅读
  ├── 持续更新 comparison-matrix.md
  └── 开始记录 gap-tracker.md

Week 3-4: 交叉分析 + 综述框架
  ├── 撰写 Cross_Topic/ 下的交叉分析文档
  ├── 确立你综述的 taxonomy（分类框架）
  ├── 创建 evidence-map.md
  └── 开始写综述大纲 outline.md

Week 4+: 综述撰写
  ├── 按章节撰写，每个论点查 evidence-map 确认有支撑
  ├── 写到薄弱处 → 回到知识库检查 → 必要时补充新论文
  └── Gap 自然浮现 → 更新 gap-tracker → 收敛选题
```

---

## 八、笔记质量检查清单

每篇论文笔记完成后，用以下清单检查是否达标：

- [ ] **一句话总结**清晰到：别人读这一句就知道论文做了什么
- [ ] **问题与动机**回答了"为什么"而不只是"是什么"
- [ ] **核心方法**用自己的话描述，而非复制 abstract
- [ ] **关键结果**包含具体数字，而非"效果很好"
- [ ] **局限性**包含至少一条作者未提及的观察
- [ ] **与我的研究的关系**已填写——这是最重要的部分
- [ ] **Research Gap 信号**有记录（即使是初步的）
- [ ] **跨论文关联**已标注至少一篇相关论文的关系
- [ ] 已同步更新 comparison-matrix.md
- [ ] 已同步更新 gap-tracker.md（如有新 Gap）
