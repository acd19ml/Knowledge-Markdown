# 精读笔记语言与定位规范

## 1. 文档定位

本仓库中的精读笔记不是：

- 最终综述稿
- 纯摘抄式读书笔记
- 临时 TODO 草稿

它是一个 **研究中间层工件**，同时服务三个下游：

1. **知识库同步**
   - 为 [comparison-matrix.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/comparison-matrix.md) 和 [gap-tracker.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/gap-tracker.md) 提供可回溯证据
2. **综述写作**
   - 为 Stage 2 的 related work / gap analysis 提供可直接提炼的材料
3. **方法设计**
   - 为 [main-line.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/main-line.md) 提供设计前驱、反证材料、实验模板

一句话定义：

> **精读笔记 = 中文分析骨架 + 英文证据锚点 + 主线导向判断。**

---

## 2. 写作目标

每篇精读笔记必须同时满足四个目标：

- **可追溯**：关键判断能回到论文原文、表格或实验数字
- **可比较**：不同论文之间 section 结构和术语稳定
- **可复用**：能直接支撑矩阵、gap、taxonomy、survey prose
- **可收口**：不保留混乱的半成品语气，不把 TODO 留在正式笔记里

因此，精读笔记优先级排序是：

1. 判断稳定
2. 证据可追
3. 结构统一
4. 语言清楚
5. 文风美观

---

## 3. 语言总原则

### 3.1 主语言

**默认规则：中文为主，英文保真。**

- 中文负责：
  - 分析
  - 判断
  - 主线定位
  - limitations 解释
  - 与其他论文关系
- 英文负责：
  - 论文标题、作者、venue
  - benchmark 名、模型名、指标名
  - 方法名、模块名、公式符号
  - 原文引句

### 3.2 英文保留的范围

以下内容保留英文，不强行翻译：

- `Procedural Memory`, `Episodic Memory`, `Semantic Memory`
- `Match Operator`, `Application Carrier`
- `Working Memory`, `UserProfile`, `Tool Repository`
- benchmark / dataset / metric 名称
- 原文章节名和直接引句

### 3.3 中文化的范围

以下内容优先用中文表达：

- “这篇论文解决什么问题”
- “为什么这个设计选择重要”
- “它对我的主线意味着什么”
- “这是不是 counter-evidence”
- “哪些地方只是 weak occupancy”

---

## 4. 禁止出现的语言问题

### 4.1 中英混句失控

不允许这种写法：

> 这个 paper 提出了一个 very strong memory architecture，然后在 benchmark 上有不错 gain，但是 limitation 也比较 obvious。

应改成：

> 这篇论文提出了一个较强的 memory architecture，并在 benchmark 上取得了稳定增益，但其 limitation 也很明确。

### 4.2 同一概念反复换名

同一篇笔记内，同一个概念必须固定叫法。

例如不能在同一篇里混用：

- `procedural memory`
- 程序性记忆
- 技能记忆
- skill memory

正确做法：

> 第一次出现：`Procedural Memory（程序性记忆）`
> 后文固定：`程序性记忆`

### 4.3 把笔记写成综述 prose

精读笔记不是 survey 正文，不要写成大段“论文式过渡段”。

不推荐：

> In the broader landscape of GUI agents, this work offers an intriguing perspective on...

推荐：

> 这篇论文在当前知识库里的价值是：它补的是哪条线，而不是“整体上很有意思”。

### 4.4 把笔记写成聊天或口语

不允许：

- “这篇还挺强的”
- “感觉作者这里没讲清楚”
- “我觉得大概就是”

统一改成：

- “该方法是当前较强的 partial solution”
- “作者未明确说明这一点”
- “从实验结果推断”

### 4.5 把 TODO 留在正式笔记里

正式笔记中不保留：

- `TBD`
- `TODO`
- `maybe`
- 模糊括号批注
- 未收口的 `⚠️ NEEDS YOUR INPUT`

如果确实有不确定性，应写成：

> `未在原文中明确说明`
> `当前判断基于 Table X + Section Y 的间接证据`

---

## 5. Section 级语言规范

### 5.1 `One-line Summary`

目标：一句话说清楚“谁、做了什么、在什么场景、比谁强/弱多少”。

格式：

> `[Paper] 提出/构建了 [核心方法]，在 [benchmark] 上达到 [结果]，相对 [baseline] 有 [增益]。`

要求：

- 中文句式
- 英文术语只保留方法名、benchmark 名、指标名
- 不写空泛评价词，如“有趣”“重要”“创新”

### 5.2 `Problem Setting`

目标：忠实还原作者的问题设定，不提前掺入你的主线判断。

要求：

- 先写作者显式问题
- 再写前提假设
- 再写已有方法不足
- 这一节尽量“paper-faithful”，少做延伸

### 5.3 `Core Method`

目标：解释方法，不复述摘要。

要求：

- 先概括系统结构
- 再拆 design choices
- 再总结和 prior work 的核心差异

语言要求：

- 中文句子解释
- 英文模块名保留
- 不要把结构图说明写成流水账

### 5.4 `Key Results`

目标：保留“可比较的结果”，而不是罗列所有表格。

要求：

- 只留与主线相关的 benchmark / ablation / failure cases
- 数字必须带比较对象
- 尽量写成“结果 + 含义”

示例：

> `pass@3` 从 `55.2 -> 73.9`，说明 shared experience layer 在 reasoning setting 下确实能带来稳定增益。

### 5.5 `Limitations`

目标：区分作者自述 limitation 与你的观察。

固定结构：

- `Author-stated limitations`
- `My observed limitations`
- `Experimental design gaps`

要求：

- `Author-stated` 尽量贴原文
- `My observed` 必须服务主线
- `Experimental design gaps` 只写实验层缺口，不和方法局限混写

### 5.6 `Relation to My Research`

这是最需要统一口径的 section。

固定只回答四件事：

1. 它在 survey / taxonomy 里放哪
2. 它是主线答案、支撑线、外围线，还是 counter-evidence
3. 它暴露了什么 gap signal
4. 有什么可复用元素

这部分必须：

- 全中文主导
- 明确与 `A-1 / A-2 / A-3 / A-4 / B-1 / B-2 / B-3` 对应
- 不写空泛表扬

### 5.7 `Connections to Other Papers`

目标：形成知识网，而不是随便列名字。

每条连接必须说明关系类型：

- 前驱
- 互补
- 竞争
- counter-evidence
- blueprint
- partial solution

不允许只写：

> 和 MemGPT 有关系。

必须写成：

> 相比 [2023_MemGPT.md](/Users/mac/studyspace/Knowledge-Markdown/Agent_Memory/papers/notes/2023_MemGPT.md)，这篇更强调 memory revision，而不是 virtual context management。

### 5.8 `Key Passages`

目标：只保留高价值英文原句。

要求：

- 只放 2-4 条
- 每条都要能直接支撑一个判断
- 不放长段落
- 只放英文，不中英混改

---

## 6. 术语统一表

| 首次写法 | 后续固定写法 | 备注 |
|---------|-------------|------|
| `Procedural Memory（程序性记忆）` | 程序性记忆 | 不再改成“技能记忆” |
| `Episodic Memory（情节记忆）` | 情节记忆 | |
| `Semantic Memory（语义记忆）` | 语义记忆 | |
| `Working Memory（工作记忆）` | 工作记忆 | |
| `User-Centric Memory（用户中心记忆）` | 用户中心记忆 | |
| `Match Operator` | 匹配算子 | taxonomy 文中可保留英文括号 |
| `Application Carrier` | 施加载体 | taxonomy 文中可保留英文括号 |
| `experience-dependent procedural knowledge` | 经验依赖的程序性知识 | 主线核心对象 |
| `experience-delta procedural rule` | 经验差分程序规则 | 方法对象 |
| `failure-aware write-back` | 失败感知写回 | |
| `partial solution` | partial solution | 这是知识库中的固定角色词，不强行中文化 |
| `strongest baseline` | strongest baseline | 同上 |
| `blueprint` | blueprint | 同上 |
| `weak occupancy` | weak occupancy | taxonomy 固定词 |

---

## 7. 证据表达规范

### 7.1 允许的判断语气

- `原文直接陈述`
- `作者明确承认`
- `实验结果表明`
- `从 Table X 可见`
- `当前更适合视为`
- `可作为 ... 的 precedent / blueprint / partial solution`

### 7.2 不允许的判断语气

- `感觉`
- `大概`
- `似乎挺像`
- `应该差不多`
- `我猜`

### 7.3 不确定时的标准句式

- `原文未明确说明`
- `该结论主要基于 Section X 与 Table Y 的合并判断`
- `这更像是推断，而不是作者显式 claim`

---

## 8. 精读笔记的风格层级

每篇笔记按这四层控制语言：

### Layer 1: Metadata

- 简洁
- 标准化
- 不做分析

### Layer 2: Paper-faithful extraction

- `Problem Setting / Core Method / Key Results / Author-stated limitations`
- 目标是忠实，不是发挥

### Layer 3: Research-facing judgment

- `My observed limitations / Relation to My Research / Connections`
- 目标是统一主线口径

### Layer 4: Verbatim anchors

- `Key Passages`
- 只保留英文证据

---

## 9. 批量整理优先级

整理现有笔记时，按以下顺序，不要平均用力：

1. **先统一 section 结构**
   - 保证所有笔记字段一致
2. **再统一 `Relation to My Research`**
   - 这是最影响矩阵和 gap 的部分
3. **再统一 `One-line Summary / Core Method / Limitations` 的中文表达**
4. **最后才处理句子级润色**

原因：

- 结构不统一会直接影响知识库同步
- 主线口径不统一会直接导致 `comparison-matrix / gap-tracker / taxonomy` 冲突
- 纯语言润色收益最低

---

## 10. 通过标准

一篇精读笔记整理完成，至少满足：

- 术语前后一致
- 中文主导，英文只作术语和证据锚点
- `Relation to My Research` 口径与 `main-line / gap-tracker / taxonomy` 一致
- 不残留 TODO / 占位 / 口语
- `Key Results` 中的数字可直接回溯
- `Key Passages` 都是高价值原句

---

## 11. 对当前仓库的执行建议

当前仓库下一步不建议“逐篇自由润色”，而建议按下面流程批量整理：

1. 先统一所有笔记的 `One-line Summary`
2. 再统一 `Relation to My Research`
3. 再统一 `Connections to Other Papers`
4. 最后清理 `Core Method / Limitations` 中的中英混乱句

建议先从 `P0 + 已进入矩阵 / gap 主证据链` 的论文开始，再处理外围 `P1`。

一句话执行原则：

> **先统一判断，后统一语言；先统一知识库接口，后统一文风。**
