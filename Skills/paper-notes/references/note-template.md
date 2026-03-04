# Paper Note Template

Use this exact structure for every paper note. Fill all sections. Leave a section blank only if the information is genuinely not available in the paper — don't omit it.

---

```markdown
# [论文简称] — [一句话描述核心贡献]
<!-- 例: CogAgent — 首个支持高分辨率 GUI 理解的视觉语言 Agent -->

## 元信息
- **标题**: [完整英文标题]
- **作者**: [第一作者 et al.] | [团队/机构]
- **发表**: [会议/期刊, 年份] | arXiv:[ID]
- **链接**: [[PDF](<url>)] [[Code](<url>)] [[Project Page](<url>)]
- **阅读日期**: YYYY-MM-DD
- **优先级**: P0 / P1 / P2
- **阅读状态**: 第一遍 / 第二遍 / 第三遍

## 一句话总结
<!-- 格式: 本文提出了 [方法名]，通过 [核心手段]，在 [任务/场景] 中实现了 [主要结果]。 -->
<!-- 要求: 别人读这一句话就应该知道论文做了什么、怎么做的、效果如何。 -->

## 问题与动机
- **要解决的核心问题**:
- **为什么现有方案不够**（作者指出的 limitation）:
- **这个问题对 GUI Agent / Memory / Self-Evolving 领域的意义**:

## 核心方法
<!-- 用自己的话描述，不要复制 abstract。2-3 段。 -->

**方法概述**:

**关键技术组件**:
- [Component Name 1]:
- [Component Name 2]:
- [Component Name 3]:

**与现有方法的核心区别**:

## 关键结果

**使用的 Benchmark / Dataset**:

**主要指标与表现**:
| Benchmark | 本文方法 | 最强 Baseline | 提升幅度 |
|-----------|---------|-------------|---------|
| ...       | ...     | ...         | ...     |

**消融实验关键发现**（哪些组件贡献最大）:

## 局限性与未解决的问题
- **作者自述的 limitation**:
- **我观察到的 limitation**（作者没提但我认为存在的）:
- **实验设计的不足**（数据集覆盖不全？评测指标有偏？）:

## ⭐ 与我的研究的关系（最重要的部分）

### 在综述中的定位
- **对应综述的哪个章节/分类**:
- **作为正面案例还是对比对象**:

### Research Gap 信号
<!-- 记录任何暗示 research gap 的线索，越具体越好 -->
- Gap 1:
- Gap 2:

### 可借鉴的元素
- **方法论上可借鉴的**:
- **实验设计上可借鉴的**:
- **写作/论证方式上可借鉴的**:

### 与知识库中其他论文/文档的关联
<!-- 明确关联到已有文件，e.g., Agent_Memory/03_operations.md, Self_Evolve/05_xxx.md -->
- 与 [论文/文件 X] 的关系: ...（互补 / 竞争 / 扩展 / 提供了 X 所缺少的...）
- 与 [论文/文件 Y] 的关系: ...

## 关键引用追踪
<!-- 这篇论文引用的、值得继续读的论文 -->
- [ ] [论文名 (Year)]: [为什么值得读]
- [ ] [论文名 (Year)]: [为什么值得读]

## 原文关键段落摘录
<!-- 只摘录对你论证关键的 1-3 句，标明位置。未来写综述时精确引用用。 -->
> "..." (Section X, p.Y)
```
