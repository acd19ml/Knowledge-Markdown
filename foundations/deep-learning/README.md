# Phase 2：深度学习核心

**时长：** 约4周 ｜ **资源：** CS5489 Lec5-7 + Tutorial 5-6，CS6487 Jan14（选读）

---

## ⭐ 里程碑项目：纯 numpy 实现两层神经网络跑 MNIST（目标 > 97%）

```python
# 只能用 numpy，禁止 import torch
def forward(X, W1, b1, W2, b2): ...    # 矩阵乘法 + ReLU + softmax
def backward(X, y, cache):    ...       # 链式法则手写
def update(params, grads, lr): ...      # SGD 更新
```

完成后用 PyTorch 实现同样的网络，逐层对比梯度数值，验证反向传播正确性。

---

## 任务清单

### 2.1 神经网络基础（CS5489 Lec5）
- [ ] 读 Lec5 讲义
- [ ] **完成里程碑项目**（预计 2-3 天）
- [ ] PyTorch 版本验证：每层梯度与 numpy 版本一致
- [ ] 自问：去掉 ReLU，深层网络会退化成什么？

### 2.2 CNN（CS5489 Lec6 + Tutorial 5/6）
- [ ] 读 Lec6，复现 Tutorial 5/6
- [ ] **可视化：** 卷积核响应图（哪个滤波器对边缘/纹理响应最强）
- [ ] **手算验证：** `Conv2d(3, 64, kernel_size=3, padding=1)` 的参数量，自算再用代码验证
- [ ] 修改层数/核大小，记录准确率变化规律

### 2.3 训练技巧（CS5489 Lec7）
- [ ] 读 Lec7 讲义
- [ ] **实验：** 故意过拟合（大网络+少数据），加 Dropout/BatchNorm 后对比改善效果
- [ ] **对比：** SGD vs Adam，同一任务画两条 loss 曲线，找交叉点

### 2.4 架构演化（CS6487 Jan14，选读）
- [ ] 读 CS6487 Jan14：CV & NLP 架构 20 年演化
- [ ] **输出：** 画时间线（LeNet → ResNet → Transformer → GPT-4V），存入 `06-gui-agent/`

---

## 核心问题（能回答才算过关）

- 梯度消失的原因，ResNet 如何解决？
- BatchNorm 在训练和推理时行为有何不同？
- Dropout 防止过拟合的直觉解释？
- 为什么深层网络需要残差连接？

---

## 我的笔记
_（学完后填）_

**反向传播的直觉（用自己的话）：**

**ResNet 解决梯度消失的方式：**

**BatchNorm 训练 vs 推理的区别：**

---

## 卡住点记录

---

**完成日期：** _____　　**自评：** ___/10