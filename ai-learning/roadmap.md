# 进度看板

> 这里只记录**在哪、完成了什么、下一步是什么**  
> 任务细节在各 Phase 文件夹的 README 里

---

## 当前位置

```
阶段：Phase 0 — 尚未开始
下一个里程碑：CS5489 Tutorial 1 跑通，能解释每一行
```

---

## 总览

| Phase | 内容 | 时长 | 状态 | 完成日期 | 自评 |
|-------|------|------|------|---------|------|
| [0 Python 基础](./00-python-ml-basics/README.md) | numpy / pandas / matplotlib / jupyter | 1.5周 | ⬜ 未开始 | — | — |
| [1 ML 底座](./01-ml-foundations/README.md) | 贝叶斯 / 分类器 / 梯度下降 | 3周 | ⬜ 未开始 | — | — |
| [2 DL 核心](./02-deep-learning-core/README.md) | 神经网络 / 反向传播 / CNN | 4周 | ⬜ 未开始 | — | — |
| [3A NLP → LLM](./03-nlp-llm/README.md) | Transformer / 微调 / Agent | 5周 | ⬜ 未开始 | — | — |
| [3B RL](./04-reinforcement-learning/README.md) | MDP / DQN / PPO / RLHF | 4周 | ⬜ 未开始 | — | — |
| [3C 生成模型](./05-generative-models/README.md) | AR / VAE / GAN / Diffusion / VLM | 4周 | ⬜ 未开始 | — | — |
| [4 GUI Agent](./06-gui-agent/README.md) | 论文 + 项目 | 持续 | ⬜ 未开始 | — | — |

**自评说明：** 1-4 背了概念 / 5-6 能解释 / 7-8 能写代码 / 9-10 能教别人

---

## 3A / 3B / 3C 并行建议

```
建议顺序：
Phase 2 完成后，三条线可以部分并行：

周次   3A（CS6493）              3B（SDS6007）           3C（CS5494）
 1    Word Embedding             MDP + GridWorld         —
 2    Word Embedding             Value/Policy Iteration  —
 3    Transformer ⭐             Q-learning              AR Model（需Transformer基础）
 4    Transformer                DQN                     AR Model
 5    NLP Tasks                  Policy Gradient         VAE
 6    LLM + Alignment            PPO ⭐                  GAN
 7    LLM Agents ⭐              Bandit                  Diffusion ⭐
 8    高效训练 / RAG             —                       Multimodal ⭐⭐
```

---

## 卡住点日志

> 遇到卡了超过2小时还没解决的问题，记在这里，不要一直死磕

| 日期 | Phase | 问题描述 | 解决方式 |
|------|-------|---------|---------|
| — | — | — | — |

---

## 里程碑记录

| 里程碑 | 描述 | 完成日期 |
|--------|------|---------|
| M1 | 纯 numpy 实现神经网络，MNIST > 97% | — |
| M2 | 手写 attention 函数，结果与 PyTorch 一致 | — |
| M3 | LoRA 微调一个小模型完成分类任务 | — |
| M4 | PPO 在 CartPole 平均 reward > 195 | — |
| M5 | VLM 分析截图，返回结构化 UI 元素 | — |
| M6 | Mini GUI Agent 完成第一个完整任务 | — |