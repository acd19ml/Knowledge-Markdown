# Phase 3C：生成模型

**时长：** 约4周 ｜ **资源：** CS5494 全部

> 前置要求：Phase 2 完成，Phase 3A 的 Transformer 部分（W4）完成后再开始 W3

---

## 各周优先级

| Week | 主题 | 优先级 | 备注 |
|------|------|--------|------|
| W1 | Perception vs Generation | ⭐⭐ | 建立框架 |
| W2 | 概率分布基础 | ⭐ 快速过 | Phase 1 已学 |
| W3 | AR Model | ⭐⭐⭐ | 理解 GPT 生成机制 |
| W4 | VAE | ⭐⭐⭐ | 潜在空间概念 |
| W5 | GAN | ⭐⭐ | 理解对抗训练 |
| W6 | Diffusion Model | ⭐⭐⭐ | 图像生成主流 |
| W7 | 3D 生成 | ⭐ 跳过 | 与 GUI Agent 无关 |
| **W8** | **Multimodal + Agent** | **⭐⭐⭐⭐⭐** | **GUI Agent 直接前置** |
| **W9** | **Prompt Engineering** | **⭐⭐⭐⭐⭐** | **与 CS6493 W8 互补** |
| W10 | Advanced Topics | ⭐⭐⭐ | 跟进前沿 |

---

## 任务清单

### W1：Perception vs Generation
- [ ] 理解核心区别：判别模型学 P(y|x)，生成模型学 P(x)
- [ ] 自问：GUI Agent 需要"判别"还是"生成"？（答案：两者都需要）

### W2：概率分布（快速过）
- [ ] 确认已掌握：高斯分布 / 伯努利分布 / KL 散度，能用代码演示

### W3：AR Model
- [ ] 理解自回归：每次生成一个 token，基于之前所有 token
- [ ] 联系 CS6493 的 GPT：GPT = AR Model + Transformer（两门课在这里汇合）
- [ ] **实现：** 字符级 AR 模型，在莎士比亚文本上训练，能生成文字

### W4：VAE
- [ ] 理解潜在空间：图像压缩到低维向量，且映射的是**分布**不是点
- [ ] 理解 Reparameterization Trick：为什么 `z = μ + σ * ε` 而不是直接采样？
- [ ] **实现：** PyTorch VAE 在 MNIST 上训练，可视化 2D 潜在空间
- [ ] 连接 GUI Agent：VLM 把截图编码到潜在空间，这是视觉理解的底层原理

### W5：GAN
- [ ] 理解博弈：Generator vs Discriminator，两者对抗共同进步
- [ ] **实现：** 最简单的 GAN 生成 MNIST，观察 Mode Collapse 现象
- [ ] 对比 VAE 和 GAN 的生成质量与训练稳定性

### W6：Diffusion Model
- [ ] 理解直觉：训练时加噪，生成时去噪，网络学的是"每步噪声长什么样"
- [ ] **实验：** 用 HuggingFace `diffusers` 跑预训练模型，可视化逐步去噪过程
- [ ] 自问：为什么 Diffusion 比 GAN 训练更稳定？

### ⭐ W8：Multimodal + Agent（最重要）
- [ ] 理解 CLIP：图文对比学习，把图像和文字映射到同一向量空间
  ```
  训练：(图像, 文字描述) 对 → 相似对向量靠近，不匹配对向量远离
  结果：模型能理解"这张图和这段文字是否匹配"
  这就是 GPT-4V / Qwen-VL 能看懂截图的基础
  ```
- [ ] 理解 VLM 结构：视觉编码器（CLIP）+ LLM
- [ ] **实验：** 用 GPT-4V 或 Qwen-VL 分析一张 GUI 截图，识别 UI 元素
- [ ] **关键问题（记录你的思考）：** VLM 如何精确定位界面元素的坐标？

### ⭐ W9：Prompt Engineering（与 CS6493 W8 互补）
- [ ] 读 CS5494 W9 讲义（结合 CS6493 W8 的 Prompting 内容，两门课互相印证）
- [ ] **实验：** 同一 GUI 任务，对比以下策略效果差异

| 策略 | GUI 任务表现 |
|------|------------|
| Zero-shot | _（实验后填）_ |
| Few-shot | _（实验后填）_ |
| Chain-of-Thought | _（实验后填）_ |
| ReAct | _（实验后填）_ |

- [ ] **输出：** 写 `gui-agent-prompt-guide.md`，总结什么场景用什么策略

### W10：Advanced Topics
- [ ] 跟进 W10 内容，记录与 GUI Agent 相关的前沿方向

---

## 核心问题（能回答才算过关）

- VAE 和普通 AE 的根本区别？
- Diffusion 为什么比 GAN 训练更稳定？
- CLIP 如何实现图文对齐，训练数据是什么？
- VLM 的视觉编码器和 LLM 是如何连接的？
- CoT 为什么能提升推理能力？

---

## 我的笔记
_（学完后填）_

**VAE 的 Reparameterization Trick 解决了什么问题：**

**Diffusion 的直觉（一句话）：**

**CLIP 工作原理（一句话）：**

---

## 卡住点记录

---

**完成日期：** _____　　**自评：** ___/10