# Phase 3A：NLP → LLM → Agent

**时长：** 约5周 ｜ **资源：** CS6493 全部，CS6487 Jan21

---

## 任务清单

### 3A.1 Word Embedding（CS6493 W2-3）
- [ ] 读讲义：为什么 one-hot 不够用？
- [ ] **实现：** 训练简单 word2vec（skip-gram），100 维
- [ ] **可视化：** t-SNE 降维，验证 `king - man + woman ≈ queen` 是否成立

### 3A.2 Transformer & Attention（CS6493 W4 + CS6487 Jan21）
- [ ] **⭐ 核心实现：** 从零手写 scaled dot-product attention
  ```python
  def attention(Q, K, V):
      d_k = Q.shape[-1]
      scores = Q @ K.T / np.sqrt(d_k)
      weights = softmax(scores, axis=-1)
      return weights @ V
  ```
- [ ] 扩展到 Multi-Head Attention，理解为什么多头比单头好
- [ ] 读 CS6487 Jan21（Transformer 在多模态系统中的应用）
- [ ] 自问：Attention 复杂度是 O(n²)，对处理高分辨率 GUI 截图有什么影响？

### 3A.3 NLP 任务（CS6493 W5-6）
- [ ] 用 HuggingFace 跑文本分类 pipeline，逐行理解每个步骤
- [ ] 理解 BERT（Encoder-only）vs GPT（Decoder-only）的结构差异
- [ ] 自问：GUI Agent 为什么用 GPT 类而不是 BERT 类？

### 3A.4 LLM + Alignment（CS6493 W7-8）
- [ ] **实验：** zero-shot / few-shot / CoT 三种方式对比同一问题，记录准确率差异
- [ ] 理解 RLHF 三步：SFT → Reward Model → PPO（与 Phase 3B 的 PPO **汇合点**！）
- [ ] **实践：** 用 LoRA 微调 Qwen-1.5B 或 Llama-3.2-1B 完成一个分类任务

### 3A.5 ⭐ LLM Agents（CS6493 W9）
- [ ] 精读 ReAct 论文，理解 Reasoning + Acting 循环
- [ ] 理解 Tool Use / Function Calling 的实现机制
- [ ] **实现：** 最简单的 LLM Agent：能调用搜索 + 能调用计算器
- [ ] 连接 GUI Agent：把"点击/输入"建模为一种 Tool Call

### 3A.6 高效训练 & RAG（CS6493 W10-11）
- [ ] 理解 LoRA：为什么只训练低秩矩阵就够用？
- [ ] **实现：** 最小 RAG pipeline（文档向量化 → FAISS 检索 → 注入 context → 生成）

---

## 核心问题（能回答才算过关）

- Attention 机制的直觉解释（用一句话）？
- 为什么 Transformer 能并行训练，RNN 不能？
- RLHF 三步，缺少任何一步会怎样？
- RAG vs Fine-tuning 的选择标准？
- LLM Agent 的主要挑战（幻觉 / 规划 / 工具调用）？

---

## 我的笔记
_（学完后填）_

**Attention 的直觉（一句话）：**

**BERT vs GPT 核心区别：**

**RLHF 三步，我的理解：**

---

## 卡住点记录

---

**完成日期：** _____　　**自评：** ___/10