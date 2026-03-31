# 基础知识学习骨架：读懂 Grounding 综述 36 篇论文

> 目标：补齐读懂论文技术实现所需的基础知识。
> 组织方式：按**依赖关系**分层，每层依赖上一层；同层内无严格先后。
> 不是学完再读论文——每层学完就可以去读对应论文。

---

## 依赖关系总览

```
Layer 0  数学与机器学习基础
   │
Layer 1  核心架构原语
   │
   ├─────────────────────┐
Layer 2a 视觉基础        Layer 2b 语言模型基础
   │                        │
   ├────────────┬───────────┘
Layer 3  预训练范式（CLIP / DINO / GPT）
   │
Layer 4  视觉任务（检测 / 分割 / 深度估计）
   │
Layer 5  多模态融合（怎么把图接到 LLM）
   │
Layer 6  本综述的专题技术
```

---

## Layer 0：数学与机器学习基础

> 如果你能看懂 PyTorch 代码里 `loss.backward()` 在干什么，这层可以跳过。

| 知识点 | 为什么需要 | 在论文中的体现 |
|--------|-----------|---------------|
| 向量/矩阵乘法、点积 | Attention 的核心运算就是矩阵乘 | Q·K^T 计算注意力分数 |
| Softmax | 把分数变成概率分布 | 注意力权重、分类输出 |
| 交叉熵损失 (Cross-Entropy) | 几乎所有论文的训练目标 | 「next-token prediction」的损失函数 |
| 梯度下降 / 反向传播 | 模型怎么学习 | 所有论文的训练过程 |
| MLP（多层感知机） | 最基本的网络组件 | LLaVA 的连接器就是两层 MLP |

**学习建议：** 3Blue1Brown 的神经网络系列视频（4 集），或 Andrej Karpathy 的 micrograd 教程。不需要推公式，需要**直觉**。

**验证标准：** 能回答「为什么 softmax 之后所有值加起来等于 1」「cross-entropy loss 在预测正确时为什么接近 0」。

---

## Layer 1：核心架构原语

> 这是最关键的一层。36 篇论文中**每一篇**都假设你懂这些。

### 1.1 卷积神经网络 (CNN) 基础

| 知识点 | 为什么需要 | 在论文中的体现 |
|--------|-----------|---------------|
| 卷积操作（filter 在图上滑动） | 理解视觉特征是怎么从像素提取的 | ConvNeXt 编码器（Cambrian-1, Mini-Gemini） |
| 特征图 (Feature Map) | 「高层特征」「低层特征」的含义 | 多尺度特征提取（Ferret, Osprey） |
| 池化 (Pooling) | 特征压缩与下采样 | ROI Pooling, Average Pooling 在区域特征提取中 |

**学习建议：** CS231n 的卷积讲义（1 篇），重点理解 filter、stride、feature map 的概念。不需要深入 ResNet 架构细节。

### 1.2 注意力机制 (Attention)

**这是最重要的单一概念。** 综述中几乎每个技术创新都是注意力的某种变体。

| 知识点 | 为什么需要 | 在论文中的体现 |
|--------|-----------|---------------|
| Query-Key-Value (QKV) | 注意力的基本框架 | 所有 Transformer 模型 |
| Self-Attention | 序列内部的元素互相关注 | ViT 的 patch 互相关注；LLM 的 token 互相关注 |
| Cross-Attention | 一个序列关注另一个序列 | 视觉 token 关注文本 token（CogVLM）；Q-Former 的查询关注图像特征（BLIP-2） |
| Multi-Head Attention | 多个注意力头各看不同方面 | 所有 Transformer |
| Causal Mask（因果掩码） | 生成时只能看前面的 token | LLM 的自回归生成 |
| 注意力分数的含义 | 「谁在关注谁」 | OPERA 分析注意力漂移导致幻觉 |

**学习建议：**
- Jay Alammar 的 "The Illustrated Transformer" 博文
- 然后看 Andrej Karpathy 的 "Let's build GPT from scratch" 视频（注意力部分）
- 动手用 PyTorch 写一个简单的 self-attention（~20 行代码）

**验证标准：** 能画出 QKV 的计算流程图；能解释「cross-attention 和 self-attention 的区别就是 Q 来自一个序列、KV 来自另一个序列」。

### 1.3 Transformer 架构

| 知识点 | 为什么需要 | 在论文中的体现 |
|--------|-----------|---------------|
| Encoder-Decoder 结构 | 理解 ViT（encoder）和 LLM（decoder）的分工 | MLLM = 视觉 encoder + 语言 decoder |
| 位置编码 (Positional Encoding) | Transformer 本身不知道顺序 | RoPE（CogVLM）、2D 位置编码（Qwen-VL）、可学习位置嵌入 |
| Layer Norm、残差连接 | Transformer block 的内部结构 | 理解 CogVLM 的 Visual Expert 在每层加了什么 |
| Feed-Forward Network (FFN) | Transformer block 的另一半 | CogVLM 的视觉专家 = 独立的 FFN |

**学习建议：** 在 1.2 的基础上，看完整的 Transformer 架构图。重点区分 encoder（双向注意力，ViT 用）和 decoder（因果注意力，LLM 用）。

---

## Layer 2a：视觉基础

### 2a.1 Vision Transformer (ViT)

| 知识点 | 为什么需要 | 在论文中的体现 |
|--------|-----------|---------------|
| 图像切 patch → 展平 → 加位置编码 → 送入 Transformer | ViT 的全部核心思路 | 所有 MLLM 的视觉编码器 |
| Patch size 与 token 数量的关系 | 理解分辨率 vs 序列长度的矛盾 | LLaVA 336px / InternVL 448px 的选择 |
| [CLS] token | 全局表征 vs 每个 patch 的局部表征 | BLIP-2 用 [CLS]，LLaVA 用所有 patch token |
| ViT 变体命名规则 | 读论文时知道 ViT-L/14 是什么意思 | L=Large, 14=patch size 14px |

**学习建议：** 读 ViT 原论文的 Figure 1 和 Section 3.1（约 2 页），或 Yannic Kilcher 的 ViT 讲解视频。

### 2a.2 图像的基本表示

| 知识点 | 为什么需要 | 在论文中的体现 |
|--------|-----------|---------------|
| 像素坐标系 (x, y) | 理解 bounding box 坐标 | Shikra 的归一化坐标 `[x_min, y_min, x_max, y_max]` |
| 归一化坐标 (0~1 或 0~1000) | 论文中坐标的表示方式 | Kosmos-2 的离散化 bin、Shikra 的文本数字 |
| Bounding Box (边界框) | 定位物体的最基本方式 | 几乎所有 grounding 论文 |
| 像素级 Mask (掩码) | 比框更精确的定位 | LISA, GLaMM, Osprey |

---

## Layer 2b：语言模型基础

### 2b.1 Tokenization（分词）

| 知识点 | 为什么需要 | 在论文中的体现 |
|--------|-----------|---------------|
| 文本 → token 序列 | LLM 的输入不是字符串，是整数序列 | 所有论文 |
| 词表 (Vocabulary) | 模型能输出的所有可能 token | Kosmos-2 扩展词表加入 location token |
| 特殊 token | `<image>`, `<SEG>`, `<box>` 等 | LISA 的 `<SEG>` token、Kosmos-2 的 `<grounding>` |
| Embedding（嵌入） | 把离散 token 变成连续向量 | 视觉 token 和文本 token 需要在同一个嵌入空间 |

### 2b.2 自回归语言生成

| 知识点 | 为什么需要 | 在论文中的体现 |
|--------|-----------|---------------|
| Next-token prediction | LLM 的训练目标：预测下一个词 | Grounding 被表述为「也生成坐标 token」 |
| 自回归生成过程 | 一个一个 token 往外蹦 | 理解为什么长文本生成会「越写越飘」（OPERA） |
| Temperature / Top-k / Top-p | 控制生成的随机性 | VCD 在 logit 层面做对比解码 |
| Beam Search | 同时维护多个候选序列 | OPERA 的 retrospection 回滚机制 |
| Logits | softmax 之前的原始分数 | OPERA 和 VCD 都在 logit 层面干预 |

**学习建议：** Andrej Karpathy 的 "Let's build GPT from scratch" 视频覆盖 2b.1 和 2b.2。

### 2b.3 Decoder-Only LLM 架构

| 知识点 | 为什么需要 | 在论文中的体现 |
|--------|-----------|---------------|
| GPT 式架构 | 几乎所有 MLLM 的语言侧都是这个 | LLaMA, Vicuna, Qwen 等 |
| Hidden state（隐状态） | 每个 token 在每一层有一个向量表示 | NExT-Chat 用 `<trigger>` 的 hidden state 解码出框/mask |
| KV Cache | 推理时的加速机制 | 理解为什么长文本推理慢 |

---

## Layer 3：预训练范式

> 理解「模型在做具体任务之前先学了什么」。这是理解 §2 编码器选择的关键。

### 3.1 对比学习 (Contrastive Learning) — 重点是 CLIP

| 知识点 | 为什么需要 | 在论文中的体现 |
|--------|-----------|---------------|
| 图文对的相似度学习 | CLIP 的训练方式：拉近匹配的图文、推远不匹配的 | 所有用 CLIP 编码器的模型 |
| InfoNCE 损失 | CLIP 的标准损失 | LLaVA-OneVision 换成 SigLIP 的 sigmoid 损失 |
| 图文对齐的特征空间 | 图像和文本在同一空间中可以用点积比较 | 这就是为什么 CLIP 编码器接 LLM 比较容易 |
| CLIP 的局限 | 图文对比学习不保证学到空间结构 | Eyes Wide Shut 论文的核心发现 |

**学习建议：** 读 CLIP 原论文的 Figure 1（对比学习示意图）和 Section 2.3（约 3 页）。

### 3.2 自监督视觉学习 — 重点是 DINO/DINOv2

| 知识点 | 为什么需要 | 在论文中的体现 |
|--------|-----------|---------------|
| 不用标签，靠数据增强自己教自己 | DINOv2 的训练方式 | Cambrian-1 发现 DINOv2 补空间/几何信息 |
| DINO vs CLIP 的区别 | CLIP 靠文字监督，DINO 靠自监督 | 这解释了为什么二者学到的特征互补 |
| MAE (Masked Autoencoder) | 遮住一部分 patch，预测被遮的部分 | Cambrian-1 测试了 MAE 变体 |

**学习建议：** 不需要深入 DINO 的技术细节。理解「自监督 = 不用文字标签，靠图像本身的结构学」和「DINO 学到的特征保留了更多几何信息」即可。

### 3.3 大语言模型预训练

| 知识点 | 为什么需要 | 在论文中的体现 |
|--------|-----------|---------------|
| 在大量文本上做 next-token prediction | LLM 的预训练方式 | LLaMA → Vicuna → 接视觉编码器 |
| 指令微调 (Instruction Tuning) | 让预训练模型听懂人话 | 所有 MLLM 的关键训练阶段 |
| SFT vs RLHF | 两种对齐方式 | RLHF-V 论文的核心话题 |
| LoRA（低秩适配） | 不改原始权重，只训小矩阵 | LISA 用 LoRA 微调 LLM 部分 |

**学习建议：** 理解 LLaMA → Alpaca/Vicuna 的训练流程（预训练 → SFT → 可选 RLHF）。

---

## Layer 4：视觉任务

> 理解综述中反复出现的任务定义和评价指标。

### 4.1 目标检测 (Object Detection)

| 知识点 | 为什么需要 | 在论文中的体现 |
|--------|-----------|---------------|
| 输入图像 → 输出一组 (框, 类别, 置信度) | 检测任务的定义 | Grounding DINO 的输出格式 |
| IoU (Intersection over Union) | 评价框预测准不准的指标 | 所有 grounding 评测 |
| GIoU 损失 | 可微分的 IoU 变体，用于训练 | NExT-Chat 的定位损失 |
| Anchor-free 检测 | 不预设候选框，直接预测 | Grounding DINO 的思路 |
| Open-vocabulary 检测 | 不限于固定类别，用文本指定要检测什么 | Grounding DINO、SpatialVLM 的数据构建 |

**学习建议：** 理解 IoU 的计算（两个框的交集面积 / 并集面积）和 bounding box 回归的概念。不需要深入 YOLO/Faster R-CNN 的架构。

### 4.2 图像分割 (Segmentation)

| 知识点 | 为什么需要 | 在论文中的体现 |
|--------|-----------|---------------|
| 语义分割：每个像素一个类别 | 最基本的像素级任务 | LISA 的输出目标 |
| 实例分割：区分同类不同个体 | 比语义分割更难 | GLaMM 的多物体 mask |
| Referring Segmentation | 根据文字描述分割出特定物体 | LISA 的核心任务 |
| DICE 损失 + BCE 损失 | 分割任务的标准损失组合 | LISA 的训练目标 |
| SAM (Segment Anything Model) | 给一个提示（点/框/文字）→ 输出 mask | LISA 用 SAM 的 decoder；SpatialRGPT 用 SAM 做数据标注 |

**学习建议：** 理解 SAM 的 prompt → mask 范式（看 SAM 论文的 Figure 1 即可）。LISA 的核心创新就是「把 LLM 的 hidden state 当作 SAM 的 prompt」。

### 4.3 深度估计 (Depth Estimation)

| 知识点 | 为什么需要 | 在论文中的体现 |
|--------|-----------|---------------|
| 单目深度估计：从一张 2D 图推测每个像素的深度 | 空间推理需要 3D 信息 | SpatialVLM, SpatialRGPT, MM-Spatial |
| 相对深度 vs 度量深度 | 相对深度只知道远近顺序，度量深度有具体数值 | SpatialRGPT 用度量深度 |
| 深度图 (Depth Map) | 一张和原图同尺寸的灰度图，每个像素值 = 深度 | MM-Spatial 把 depth map 作为额外输入 |

**学习建议：** 理解「从 2D 推 3D 是一个病态问题（同一张图对应无穷多种 3D 场景）」，以及为什么现在的模型能做到还不错（大量数据学到了统计规律）。

---

## Layer 5：多模态融合

> 这一层直接对应综述 §2.3 的连接器和 §3 的 grounding 方法。学完这层就可以读综述了。

### 5.1 怎么把图接到 LLM

| 知识点 | 为什么需要 | 在论文中的体现 |
|--------|-----------|---------------|
| 核心问题：视觉特征和文本 token 不在同一空间 | 这是所有 MLLM 要解决的第一个问题 | 所有论文 |
| 方案 1：线性投影 / MLP | 最简单，每个 visual patch → 一个 token | LLaVA 的两层 MLP |
| 方案 2：可学习查询 + 交叉注意力 | 用固定数量的查询「摘要」视觉信息 | BLIP-2 的 Q-Former |
| 方案 3：深层融合（每层都融） | 最贵但最强 | CogVLM 的 Visual Expert |
| 冻结 vs 解冻编码器 | 训练时是否更新视觉编码器 | Cambrian-1 实验了解冻的效果 |
| 视觉 token 数量的矛盾 | 多了信息丰富但序列太长，少了丢失空间信息 | 整个 §2 的核心张力 |

### 5.2 多模态指令微调

| 知识点 | 为什么需要 | 在论文中的体现 |
|--------|-----------|---------------|
| 多模态 SFT 的数据格式 | `<image> 用户问题 → 模型回答` | LLaVA 的对话格式 |
| 多阶段训练 | 先对齐特征空间，再学任务 | LLaVA: stage1 特征对齐 → stage2 指令微调 |
| 多任务训练 | 一个模型同时学 grounding + VQA + captioning | Ferret, CogVLM, Shikra |

### 5.3 RLHF 与 DPO

| 知识点 | 为什么需要 | 在论文中的体现 |
|--------|-----------|---------------|
| RLHF 的流程：SFT → 训练 reward model → PPO 优化 | 理解人类反馈对齐的完整流程 | RLHF-V 的背景 |
| DPO：跳过 reward model，直接从偏好数据优化 | 更简单的对齐方法 | RLHF-V 的 DDPO |
| 偏好数据的格式：(prompt, chosen, rejected) | DPO 的训练数据 | RLHF-V 的片段级人类修正 |

**学习建议：** 理解 RLHF 的动机（「光靠 SFT 不够，还需要教模型什么该说什么不该说」）和 DPO 的简化（「不用单独训 reward model」）。

---

## Layer 6：本综述的专题技术

> 到这一步你已经可以读论文了。这些技术在论文中会有解释，这里只列出概念名供你遇到时不陌生。

| 技术 | 简述 | 出现在 |
|------|------|--------|
| Pix2Seq 范式 | 把坐标当 token 序列生成 | Kosmos-2, Shikra |
| Hidden-state decoding | 用某个 token 的隐状态解码出框/mask | NExT-Chat, LISA |
| Spatial-aware visual sampler | 从不规则区域采样视觉特征 | Ferret |
| Dynamic tiling / AnyRes | 图像按需切块处理 | InternVL, LLaVA-OneVision |
| Contrastive decoding | 对比两种条件下的输出分布 | VCD |
| Attention penalty / rollback | 解码时惩罚异常注意力模式 | OPERA |
| 3D scene graph | 从 2D 图像重建 3D 物体关系图 | SpatialRGPT |
| Chain-of-thought depth | 先估深度再答空间问题 | MM-Spatial |
| Rejection sampling | 生成多个候选，用 reward 选最好的 | ViGoR |
| Negative instruction tuning | 用负样本教模型说「不」 | LRV-Instruction |

---

## 学习路线图（时间估算仅供参考）

```
Week 1-2: Layer 0 + Layer 1
  ├─ 3B1B 神经网络视频 (2h)
  ├─ CS231n 卷积讲义 (2h)
  ├─ Illustrated Transformer 博文 (2h)
  └─ Karpathy "build GPT" 视频 (2h)  ← 同时覆盖 Layer 2b
      验证：能手画 self-attention 的 QKV 流程

Week 3: Layer 2a + 2b
  ├─ ViT 原论文 Figure 1 + Section 3.1 (1h)
  ├─ 理解 bounding box 和 mask 的坐标表示 (0.5h)
  └─ 理解 tokenization 和自回归生成 (已在 Karpathy 视频覆盖)
      验证：能解释「ViT 把图切成 patch 然后当 token 处理」

Week 4: Layer 3
  ├─ CLIP 论文 Figure 1 + Section 2.3 (1.5h)
  ├─ 理解 DINO vs CLIP 的区别 (0.5h)
  ├─ 理解 LLaMA → SFT → RLHF 流程 (1h)
  └─ 理解 LoRA 的动机 (0.5h)
      验证：能解释「CLIP 学到的特征为什么缺空间信息」

Week 5: Layer 4
  ├─ IoU 计算和 bounding box 回归 (1h)
  ├─ SAM 论文 Figure 1 (0.5h)
  └─ 单目深度估计的概念 (0.5h)
      验证：能解释「SAM 的 prompt → mask 和 LISA 的 <SEG> token → mask 的关系」

Week 6: Layer 5
  ├─ LLaVA 原论文 (2h) ← 最佳的多模态入门论文
  ├─ 理解 Q-Former vs MLP vs Deep Fusion (1h)
  └─ DPO 的直觉理解 (0.5h)
      验证：能画出 MLLM 的完整数据流（图像 → 编码器 → 连接器 → LLM → 文本）

Week 7+: 开始读综述和论文
  用 reading-guide.md 按路线 B 逐节读
```

---

## 每层推荐资源

| Layer | 首选资源 | 语言 | 形式 |
|-------|---------|------|------|
| 0 | 3Blue1Brown: Neural Networks | EN (有中文字幕) | 视频 |
| 1 (CNN) | CS231n Convolutional Networks 讲义 | EN | 文本 |
| 1 (Attention) | Jay Alammar: The Illustrated Transformer | EN | 博文 |
| 1 (整合) | Andrej Karpathy: Let's build GPT from scratch | EN | 视频 |
| 2a | ViT 原论文 An Image is Worth 16x16 Words, Fig 1 + §3.1 | EN | 论文 |
| 3 (CLIP) | CLIP 原论文 Learning Transferable Visual Models, Fig 1 + §2.3 | EN | 论文 |
| 3 (LLM) | Andrej Karpathy: Intro to Large Language Models (1hr talk) | EN | 视频 |
| 4 (SAM) | SAM 原论文 Segment Anything, Fig 1 | EN | 论文 |
| 5 | **LLaVA 原论文 Visual Instruction Tuning** | EN | 论文 |
| 5 (RLHF) | Chip Huyen: RLHF 博文 | EN | 博文 |

> **最核心的一篇：LLaVA (Visual Instruction Tuning)**。它是这个领域最简洁的入门论文——架构简单（ViT + MLP + LLM）、解释清晰、且是综述中至少 8 篇后续论文的直接基线。读懂 LLaVA 就读懂了 MLLM 的基本范式。
