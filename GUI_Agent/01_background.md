# Background Knowledge

> Section 2（Pages 6–9）

---

## 2.1 大语言模型（LLM）基础概念

### LLM 架构类型

| 类型 | 代表模型 | 特征 | 在 GUI Agent 中的适用性 |
|------|---------|------|----------------------|
| **Encoder-Only** | BERT 系列 | 全局理解，不擅长生成 | 低（缺乏生成能力） |
| **Decoder-Only** | GPT 系列（因果解码器）/ PaLM（前缀解码器） | 自回归生成 | 高（主流选择） |
| **Encoder-Decoder** | T5, FLAN-T5 | 同时理解与生成 | 中（部分任务用于过滤阶段） |

### 规模定律与训练范式

- **Scaling Law**：增大参数量与数据规模能有效提升下游任务性能
- **预训练 + 微调**：先在大规模语料上预训练，再在特定下游任务上微调
- GUI Agent 任务中，LLM 同时处理：**用户指令**（自然语言）+ **GUI 环境表示**（VH/DOM 结构或截图）

---

## 2.2 赋予 LLM 感知能力（Multimodal LLM）

### 为何需要多模态能力

LLM 原生只处理文本，面对 GUI 任务时面临两大挑战：
1. VH/DOM 输入**过长**，信息密度低
2. 截图中的图标、图表、空间关系**无法用文本充分表达**

### MLLM（Multimodal LLM）架构

```
输入截图
   │
视觉编码器（frozen）          <- 提取图像特征
   │
可学习映射层                  <- 对齐视觉与文本空间
  ┌─────────────────────┐
  │  MLP（LLaVA）         │
  │  Cross-attention     │   <- Flamingo：视觉特征增强文本 token
  │  Q-Former (BLIP-2)   │   <- 可学习 query 提取相关视觉信息
  └─────────────────────┘
   │
LLM（自回归生成）
   │
输出（动作 / 代码 / 文本）
```

### 关键里程碑

| 模型 | 映射层 | 创新点 |
|------|--------|-------|
| **VISPROG** | 外部专家视觉工具（无映射层） | 最早用 LLM 调用视觉工具 |
| **Flamingo** | Cross-attention | 视觉增强文本，无需额外视觉 token |
| **BLIP-2 / Q-Former** | 可学习 query | 从视觉特征中提取与文本相关的信息 |
| **LLaVA** | 简单 MLP | 视觉 + 文本拼接对齐 |
| **CogAgent** | 双编码器（高分辨率 + 低分辨率） | 专为 GUI 设计，解决高分辨率输入问题 |

### GUI 场景的特殊挑战

1. **细粒度定位（Fine-grained Localization）**：截图中的小图标、文本链接难以精确定位
   - 商业模型方案："Image Caption" 策略（红框 + 字母标注）
   - 开源模型方案：训练 MLLM 直接输出边界框坐标

2. **高分辨率输入**：1120×1120 截图 → 6400 个额外视觉 token，计算代价极高
   - CogAgent 的解法：轻量级高分辨率编码器 + Cross-attention 传递高分辨率信息

---

## 2.3 LLM-based Agent 概念

### Agent 演进路径

```
符号化 Agent（规则/知识库）
      ↓
反应式 Agent（感知-动作循环）
      ↓
RL Agent（环境交互 + 奖励函数）  <- 样本效率低，训练不稳定
      ↓
LLM-based Agent                  <- 当前主流：规划 + 记忆 + 工具调用
```

### LLM-based Agent 的三大核心能力

| 能力 | 关键技术 | 说明 |
|------|---------|------|
| **规划（Planning）** | CoT, ToT | CoT 逐步分解；ToT 树形多路径探索 |
| **记忆（Memory）** | Short-term (ICL) + Long-term (Vector DB) | 短期受 context window 限制；长期通过外部检索扩展 |
| **工具调用（Tool Use）** | API 格式输出 | 扩展功能边界 |

### 任务执行中的关键方法

- **ReAct**：推理（Reason）+ 行动（Act）交替迭代
- **Reflexion**：反思过去决策，迭代修正错误

### 多智能体范式

| 范式 | 机制 | 代表 |
|------|------|------|
| **协作（Cooperation）** | 共同目标，分工协作 | UFO, Mobile-Agent-v2 |
| **辩论（Discussion）** | 各自观点 → 达成共识 | — |
| **竞争（Competition）** | 各自目标，相互博弈 | — |

---

## 与知识库的连接

| 本节概念 | 扩展阅读 |
|---------|---------|
| LLM-based Agent 的记忆机制 | [Agent_Memory/01_background.md](../Agent_Memory/01_background.md) — Episodic / Semantic / Procedural Memory |
| Agent 自我改进与持续学习 | [Self_Evolve/01_background.md](../Self_Evolve/01_background.md) |
| GUI 能力（GUI 理解 / 设备控制） | [02_capabilities/2.1_gui-comprehension.md](02_capabilities/2.1_gui-comprehension.md) |

---

## Personal Research Notes

- [ ] 本节的 Short-term / Long-term Memory 划分是粗粒度的；Agent_Memory 综述提供了更细的五类认知机制（Episodic, Semantic, Sensory, Working, Procedural）—— GUI Agent 中哪类记忆最重要？
- [ ] CogAgent 的双编码器设计是否可迁移到更通用的多模态 Agent 框架中？
- [ ] VH/DOM 文本与截图的**信息互补性**尚未被充分探索（Hybrid 范式优势明显但研究不多）
