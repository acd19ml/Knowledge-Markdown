# Reading Guide: 多模态大模型中的视觉 Grounding 与空间理解

> 基于 `CS6487-skeleton.md` 骨架，为 `grounding_review_full_zh.md` 编写的阅读导航。
> 目标：让你在读综述任何一段时，都知道**自己在哪、这段在回答什么问题、该去哪篇论文找细节**。

---

## 全局地图：一条能力链

综述**不是**六块独立话题，而是一条**因果链**：

```
像素 ──→ 视觉表征 ──→ Grounding 输出 ──→ 空间推理 ──→ 生成文本
         (§2)          (§3)              (§4)         (§5 失效)
        「能看多细」   「怎么指」        「关系对不对」 「说着说着就编了」
```

**一句话总论点：** Grounding 是连接「看见」与「推理空间关系」的中间层；幻觉是这条链变弱时的典型崩法。

---

## §1 Introduction（L17–51）

| 项目 | 内容 |
|------|------|
| **核心问题** | 为什么 MLLM 能写出好描述，却在最基本的空间判断上频频出错？ |
| **核心论点** | 不是模型「说不好」，是「语言和图像绑得不稳」—— grounding 不稳导致链条逐级崩溃 |
| **读这节的收获** | 理解综述的四个子问题（§2–§5 各回答一个），以及它们为什么要串成一条链 |

**关键引用（建立问题严重性）：**

| 论文 | 笔记文件 | 它说了什么 |
|------|----------|-----------|
| VSR (Liu et al.) | [Visual Spatial Reasoning.md](papers/markdown/Visual%20Spatial%20Reasoning.md) | 简单空间判断接近随机猜测 |
| What'sUp (Kamath et al.) | 综述内引用 | 18 个模型判断 above/below 都不行 |
| Eyes Wide Shut (Tong et al.) | [Eyes Wide Shut.md](papers/markdown/Eyes%20Wide%20Shut.md) | CLIP 编码器对 9 类视觉模式「视而不见」 |
| POPE (Li et al.) | [Evaluating Object Hallucination.md](papers/markdown/Evaluating%20Object%20Hallucination.md) | 模型会编造不存在的物体 |

---

## §2 视觉表征：Grounding 的底层基础（L53–168）

| 项目 | 内容 |
|------|------|
| **回答的问题** | 从像素到语言模型输入，还能剩下多少空间信息？ |
| **核心论点** | Grounding 能力的**上限**由三件事决定：编码器、分辨率策略、图文连接器。表征好 ≠ 输出一定 grounded，但表征差则一定不行 |
| **类比** | 像一个漏斗——每一层都可能丢信息，到了下游就无法找回 |

### 分步阅读建议

**§2.1 视觉编码器选择**——先读这三篇，理解「主流用什么、还缺什么」：

| 论文 | 笔记文件 | 一句话要点 |
|------|----------|-----------|
| LLaVA-1.5 | [Visual Instruction Tuning.md](papers/markdown/Visual%20Instruction%20Tuning.md) | CLIP ViT + 两层 MLP 就能强，奠定基线 |
| InternVL | [InternVL.md](papers/markdown/InternVL.md) | 把视觉编码器做到 6B，证明视觉侧容量被低估 |
| Cambrian-1 | [Cambrian-1.md](papers/markdown/Cambrian-1.md) | 系统比较 23 种骨干，DINOv2 补空间/几何信息 |

**§2.2 分辨率策略**——综述里有一张表（L86–95），**这张表是全节的锚**。建议：

1. 先看表，记住从 224px 到 1536px 的演进
2. 记住一个结论：「很多看似数据噪声的问题，其实是看得不够细」
3. 对照读 [Mini-Gemini.md](papers/markdown/Mini-Gemini.md)（双编码器方案） 和 [LLaVA-OneVision.md](papers/markdown/LLaVA-OneVision.md)（AnyRes 方案）

**§2.3 图文连接器**——这是**最容易读不懂的部分**，因为有 6 种连接器。建议按「信息保留量」排序理解：

```
信息保留少 ◄────────────────────────────► 信息保留多

Q-Former        Cross-Attn       MLP        Visual Expert
(BLIP-2)        (Qwen-VL)      (LLaVA)      (CogVLM)
32个查询,        压缩但加位置编码  每个patch→    每一层都做
空间信息被冲掉                   一个token     视觉融合
```

| 论文 | 笔记文件 | 连接器类型 |
|------|----------|-----------|
| BLIP-2 | [BLIP-2.md](papers/markdown/BLIP-2.md) | Q-Former（信息瓶颈，不适合 grounding） |
| Qwen-VL | [Qwen-VL.md](papers/markdown/Qwen-VL.md) | Cross-Attn + 2D 位置编码（压缩但保位置） |
| CogVLM | [CogVLM.md](papers/markdown/CogVLM.md) | Visual Expert 每层融合（最强但最贵） |

**§2.4 横向对比表**（L145–154）是本节的**总结表**，建议读完 §2.1–2.3 后回来看这张表检验理解。

---

## §3 Grounding 方法：从坐标到区域（L170–258）

| 项目 | 内容 |
|------|------|
| **回答的问题** | 模型怎么把「看到的空间信息」变成「可用的定位输出」？ |
| **核心论点** | 方法从简单到复杂有三级跳：坐标当文本 → 区域级对话 → 像素级分割。越远离纯 token generation，表达力越强 |
| **核心张力** | 既要保持「文本进、文本出」的灵活接口，又要做结构化的空间预测 |

### 分步阅读建议

**§3.1 坐标预测**——理解三种范式的演进：

| 范式 | 代表论文 | 笔记文件 | 做法 |
|------|---------|----------|------|
| 离散位置 token | Kosmos-2 | [Kosmos-2.md](papers/markdown/Kosmos-2.md) | 框坐标离散到 32×32 格子 |
| 纯文本数字 | Shikra | [Shikra.md](papers/markdown/Shikra.md) | 框写成 `[x_min, y_min, x_max, y_max]` 普通数字 |
| 隐状态解码 | NExT-Chat | [NExT-Chat.md](papers/markdown/NExT-Chat.md) | `<trigger>` token 的 hidden state 解码为框/mask |

> **阅读顺序建议：** Kosmos-2 → Shikra → NExT-Chat，三者刚好构成一条「坐标怎么表示」的演进线。

**§3.2 区域级理解**——从「指哪」到「理解那一块」：

| 论文 | 笔记文件 | 关键创新 |
|------|----------|---------|
| Ferret | [Ferret.md](papers/markdown/Ferret.md) | 混合区域表征：坐标 + 从 mask 采样的视觉特征，支持任意形状输入 |
| Ferret-v2 | [Ferret-v2.md](papers/markdown/Ferret-v2.md) | AnyRes + DINOv2 局部块 + 三阶段课程训练 |
| Osprey | [Osprey.md](papers/markdown/Osprey.md) | mask 级输入（比框更精确），部件级理解 |

**§3.3 分割级 Grounding**——最高粒度：

| 论文 | 笔记文件 | 关键创新 |
|------|----------|---------|
| LISA | [LISA.md](papers/markdown/LISA.md) | `<SEG>` token → SAM mask decoder，最简洁的 mask 方案 |
| GLaMM | [GLaMM.md](papers/markdown/GLaMM.md) | 多短语 × 多 mask 的 grounded conversation |

**§3.4 训练策略**——不读论文也要记住的五个模式：

1. **自动大规模数据**（GrIT、GranD）—— 噪声大但覆盖广
2. **已有数据 instruction 化**（RefCOCO 等改写成对话）
3. **从粗到细课程**（先学全局，再学局部，最后学用户意图）
4. **困难负样本**（教模型说"不是那个"）
5. **多任务双向迁移**（grounding 帮对话更精确，对话帮 grounding 更稳定）

**§3.5 横向对比表**（L238–251）是本节最重要的表，建议打印出来对照读。

---

## §4 空间关系推理（L260–383）

| 项目 | 内容 |
|------|------|
| **回答的问题** | 模型能判断「谁在谁上面、谁离得更近」吗？ |
| **核心论点** | Grounding 是空间推理的**必要不充分条件**：指对物体有助于推理，但深度、距离、遮挡需要额外的 3D 感知 |
| **现状** | 极差——多个 benchmark 显示接近随机猜测 |

### 分步阅读建议

**§4.1 先确立问题有多严重**——读 VSR 和 What'sUp 的笔记：

| 论文 | 笔记文件 | 震撼结论 |
|------|----------|---------|
| VSR | [Visual Spatial Reasoning.md](papers/markdown/Visual%20Spatial%20Reasoning.md) | 最好模型 <70%，人类 95.4% |
| Eyes Wide Shut | [Eyes Wide Shut.md](papers/markdown/Eyes%20Wide%20Shut.md) | CLIP 对方向、形状、空间关系系统性盲区 |

**§4.2 空间关系分类**——综述表（L288–298）将关系分为四类：

```
拓扑关系 (on, in, near)        ← 最常测试，相对最容易
方向关系 (左/右, 上/下, 前/后)  ← 看似简单但视角依赖，很不可靠
距离/深度 (更近/更远, 度量距离)  ← 需要 3D 感知，单目图像困难
遮挡 (部分遮挡, 完全遮挡)      ← 研究最少，最难
```

**§4.4 三种解决路线**——这是本节最值得精读的部分：

| 路线 | 论文 | 笔记文件 | 核心思路 |
|------|------|----------|---------|
| 数据驱动 | SpatialVLM | [SpatialVLM.md](papers/markdown/SpatialVLM.md) | 合成 20 亿条空间 QA，暴力补数据缺口 |
| 区域感知 3D | SpatialRGPT | [SpatialRGPT.md](papers/markdown/SpatialRGPT.md) | 区域级 + 深度插件，81% vs GPT-4V 的 56% |
| 多视角 3D | MM-Spatial | [MM-Spatial.md](papers/markdown/MM-Spatial.md) | 多视角重建 3D，3B 模型打到 SOTA |

**§4.5 关键结论**（L359–367）值得反复读：
- Grounding 是空间推理的**必要条件**（不指对物体就没法比）
- Grounding **不是充分条件**（指对了也不一定判断对深度和距离）
- 二者构成**依赖链**，而非合并的单一技能

---

## §5 失败模式与 Grounding 幻觉（L385–497）

| 项目 | 内容 |
|------|------|
| **回答的问题** | Grounding 弱或不稳定时，具体怎么崩的？能救吗？ |
| **核心论点** | 幻觉本质是 grounding 的失效模式——语言与视觉证据的绑定在某处断裂 |
| **统一机制** | 幻觉出现在 grounding 信号相对 prior 信号**变弱**之时 |

### 分步阅读建议

**§5.1 失败分类**——五种崩法，从简单到复杂：

| 失败类型 | 通俗解释 | 关键论文 |
|----------|---------|---------|
| 1. 编造物体 | 说图里有但其实没有 | [Evaluating Object Hallucination.md](papers/markdown/Evaluating%20Object%20Hallucination.md) (POPE) |
| 2. 属性/关系错 | 找对物体但说错颜色/位置/数量 | [Hallu-PI.md](papers/markdown/Hallu-PI.md) |
| 3. 先验主导 | 不看图，从记忆回答 | [HallusionBench.md](papers/markdown/HallusionBench.md) |
| 4. 视觉误读 | 看了图但读错信息 | [HallusionBench.md](papers/markdown/HallusionBench.md) |
| 5. 退化证据 | 图模糊/裁剪/误导时崩得更厉害 | [Hallu-PI.md](papers/markdown/Hallu-PI.md) |

**§5.3 传播机制**——理解「为什么越写越离谱」：

| 论文 | 笔记文件 | 揭示的机制 |
|------|----------|-----------|
| LURE | 综述内引用 | 共现偏差 + 不确定性 + 位置效应，幻觉集中在描述后段 |
| OPERA | [OPERA.md](papers/markdown/OPERA.md) | 注意力逐渐偏离前端视觉 token，越写越依赖已生成文本 |
| VCD | [VCD.md](papers/markdown/VCD.md) | 图像扰动时模型系统性回退到语言先验 |

> **一句话理解传播：** 回答**起始于**视觉锚定，随后**越来越多地**由已生成文本中介。

**§5.5 缓解策略**——七种方法按干预时机排列：

```
训练时 ◄────────────────────────────────► 推理时/事后

LRV-Instruction  RLHF-V   ViGoR   OPERA   VCD   LURE  Woodpecker
(平衡正负数据)  (细粒度偏好) (奖励)  (解码)  (解码) (改写) (外部验证)

效果越根本，成本越高 ◄──────────► 效果越表面，成本越低
```

| 论文 | 笔记文件 | 干预层 |
|------|----------|-------|
| LRV-Instruction | [LRV-Instruction.md](papers/markdown/LRV-Instruction.md) | 训练数据（加负样本教模型说"不"） |
| RLHF-V | [RLHF-V.md](papers/markdown/RLHF-V.md) | 对齐（片段级人类修正） |
| ViGoR | [ViGoR.md](papers/markdown/ViGoR.md) | 奖励（逐句评分 + 检测器验证） |
| OPERA | [OPERA.md](papers/markdown/OPERA.md) | 解码（惩罚过度信任摘要 token） |
| VCD | [VCD.md](papers/markdown/VCD.md) | 解码（对比原图 vs 扰动图的分布） |
| Woodpecker | [Woodpecker.md](papers/markdown/Woodpecker.md) | 外部验证（检测器 + VQA 五阶段修正） |

---

## §6 Discussion & Future Directions（L499–553）

| 项目 | 内容 |
|------|------|
| **回答的问题** | 当前方法的共同短板在哪？下一步该做什么？ |
| **不需要对照论文**，这节是综合讨论，直接读即可 |

### 三个共性瓶颈
1. **小物体/细粒度**——分辨率仍是结构性约束，每一阶段都在丢小物体信息
2. **密集/杂乱场景**——benchmark 偏简单场景，真实世界组合爆炸
3. **跨图像/时间推理**——几乎所有方法只看单张图

### 四个开放问题
1. 统一的 grounding 评测框架
2. 2D→3D 的鸿沟（能否仅从 2D 数据学到 3D 结构？）
3. 组合式多物体空间推理
4. 置信度校准（模型知不知道自己 grounding 不靠谱？）

### 三句话终极结论
1. Grounding 是连接感知与推理的**中间能力**，不是小众 benchmark 技能
2. 当前弱点不在语言流利度，在于**稳定的视觉锚定**
3. 未来进展需要**整条链联合优化**，单点补丁效果有限

---

## 推荐阅读顺序

根据你的目标选择路线：

### 路线 A：快速理解全貌（~2 小时）
1. 读本 guide 的全局地图和每节的「核心论点」
2. 读综述 §1（L17–51）建立问题意识
3. 读 §2.4 横向对比表（L145–162）和 §3.5 横向对比表（L238–252）
4. 读 §5.1 失败分类（L391–405）
5. 读 §6.5 终极结论（L543–553）

### 路线 B：深入某一节（按需）
1. 先读本 guide 该节的「分步阅读建议」
2. 按建议顺序读对应论文笔记（`papers/markdown/` 下）
3. 再回综述读该节正文，此时每句话都有上下文

### 路线 C：36 篇论文的优先级排序

**第一梯队（6 篇，理解能力链的骨干）：**
- LLaVA-1.5、Shikra、Ferret、LISA、SpatialRGPT、POPE

**第二梯队（6 篇，理解各阶段的关键补充）：**
- Cambrian-1、CogVLM、Kosmos-2、GLaMM、HallusionBench、OPERA

**第三梯队（其余，按兴趣选读）**

---

## 36 篇论文速查索引

| # | 论文 | 综述章节 | 笔记文件 |
|---|------|---------|----------|
| 1 | BLIP-2 | §2 | [BLIP-2.md](papers/markdown/BLIP-2.md) |
| 2 | LLaVA-1.5 (Visual Instruction Tuning) | §2 | [Visual Instruction Tuning.md](papers/markdown/Visual%20Instruction%20Tuning.md) |
| 3 | Qwen-VL | §2 | [Qwen-VL.md](papers/markdown/Qwen-VL.md) |
| 4 | CogVLM | §2 | [CogVLM.md](papers/markdown/CogVLM.md) |
| 5 | InternVL | §2 | [InternVL.md](papers/markdown/InternVL.md) |
| 6 | LLaVA-OneVision | §2 | [LLaVA-OneVision.md](papers/markdown/LLaVA-OneVision.md) |
| 7 | Cambrian-1 | §2 | [Cambrian-1.md](papers/markdown/Cambrian-1.md) |
| 8 | Mini-Gemini | §2 | [Mini-Gemini.md](papers/markdown/Mini-Gemini.md) |
| 9 | Kosmos-2 | §3 | [Kosmos-2.md](papers/markdown/Kosmos-2.md) |
| 10 | Shikra | §3 | [Shikra.md](papers/markdown/Shikra.md) |
| 11 | NExT-Chat | §3 | [NExT-Chat.md](papers/markdown/NExT-Chat.md) |
| 12 | Ferret | §3 | [Ferret.md](papers/markdown/Ferret.md) |
| 13 | Ferret-v2 | §3 | [Ferret-v2.md](papers/markdown/Ferret-v2.md) |
| 14 | Osprey | §3 | [Osprey.md](papers/markdown/Osprey.md) |
| 15 | LISA | §3 | [LISA.md](papers/markdown/LISA.md) |
| 16 | GLaMM | §3 | [GLaMM.md](papers/markdown/GLaMM.md) |
| 17 | Grounding DINO | §3 | [Grounding DINO.md](papers/markdown/Grounding%20DINO.md) |
| 18 | Towards Visual Grounding (Xiao et al.) | §1 | [Towards Visual Grounding.md](papers/markdown/Towards%20Visual%20Grounding.md) |
| 19 | VSR | §4 | [Visual Spatial Reasoning.md](papers/markdown/Visual%20Spatial%20Reasoning.md) |
| 20 | Eyes Wide Shut | §4 | [Eyes Wide Shut.md](papers/markdown/Eyes%20Wide%20Shut.md) |
| 21 | SpatialVLM | §4 | [SpatialVLM.md](papers/markdown/SpatialVLM.md) |
| 22 | SpatialRGPT | §4 | [SpatialRGPT.md](papers/markdown/SpatialRGPT.md) |
| 23 | SpatialBench | §4 | [SpatialBench.md](papers/markdown/SpatialBench.md) |
| 24 | spatial reasoning (An Empirical Analysis) | §4 | [spatial reasoning.md](papers/markdown/spatial%20reasoning.md) |
| 25 | MM-Spatial | §4 | [MM-Spatial.md](papers/markdown/MM-Spatial.md) |
| 26 | POPE (Evaluating Object Hallucination) | §5 | [Evaluating Object Hallucination.md](papers/markdown/Evaluating%20Object%20Hallucination.md) |
| 27 | Analyzing and Mitigating Object Hallucination | §5 | [Analyzing and Mitigating Object Hallucination.md](papers/markdown/Analyzing%20and%20Mitigating%20Object%20Hallucination.md) |
| 28 | Hallu-PI | §5 | [Hallu-PI.md](papers/markdown/Hallu-PI.md) |
| 29 | HallusionBench | §5 | [HallusionBench.md](papers/markdown/HallusionBench.md) |
| 30 | LRV-Instruction | §5 | [LRV-Instruction.md](papers/markdown/LRV-Instruction.md) |
| 31 | OPERA | §5 | [OPERA.md](papers/markdown/OPERA.md) |
| 32 | VCD | §5 | [VCD.md](papers/markdown/VCD.md) |
| 33 | RLHF-V | §5 | [RLHF-V.md](papers/markdown/RLHF-V.md) |
| 34 | Woodpecker | §5 | [Woodpecker.md](papers/markdown/Woodpecker.md) |
| 35 | ViGoR | §5 | [ViGoR.md](papers/markdown/ViGoR.md) |
| 36 | An Empirical Analysis | §4 | [An Empirical Analysis.md](papers/markdown/An%20Empirical%20Analysis.md) |
