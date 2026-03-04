# Quality Checklist

Run through every item before saving the note. Fix failures — don't just note them.

## Checklist

- [ ] **一句话总结** 清晰到：别人读这一句就知道论文做了什么、怎么做的、效果如何
- [ ] **问题与动机** 回答了"为什么"而不只是"是什么"（即解释了为什么现有方案不够）
- [ ] **核心方法** 用自己的话描述，没有直接复制 abstract 或 introduction 的句子
- [ ] **关键结果** 包含具体数字（百分比、分数等），而非"效果很好"、"大幅提升"
- [ ] **局限性** 包含至少一条作者未提及的观察（来自批判性阅读，不是复述作者的话）
- [ ] **与我的研究的关系** 已填写，且明确指出与知识库中已有文件的关联
- [ ] **Research Gap 信号** 记录了至少一条（即使是初步的、弱证据的）
- [ ] **跨论文关联** 已标注至少一篇相关论文或知识库文件的关系
- [ ] **关键引用追踪** 至少有一条待读论文（来自论文本身的参考文献）
- [ ] **语言规范**: 引用链接、benchmark 名称、技术术语、模型名称均为英文；分析内容均为中文

## Common failure modes

**"一句话总结"太宽泛**:
- ✗ "本文提出了一种新的 GUI Agent 框架，取得了较好效果。"
- ✓ "本文提出了 CogAgent，通过双视觉编码器（高分辨率 + 低分辨率）分别处理 GUI 细节与语义理解，在 Mind2Web 上达到 XX% SR，超越此前 SOTA YY%。"

**"核心方法"照抄 abstract**:
- ✗ "We propose a novel framework that leverages..."（直接照抄）
- ✓ 用中文重新描述方法的核心思路，体现理解

**"局限性"只有作者自述**:
- 必须补充一条"我观察到的 limitation"，例如：测试集较小、未与最新 baseline 对比、依赖特定 UI 框架等

**"与我的研究的关系"过于笼统**:
- ✗ "与本方向相关"
- ✓ "本文的 Episodic Memory 设计与 Agent_Memory/03_operations.md 中的检索增强记忆方案形成互补：本文侧重存储效率，而该文档讨论的方案侧重遗忘机制。"
