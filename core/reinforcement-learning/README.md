# Phase 3B：强化学习

**时长：** 约4周 ｜ **资源：** SDS6007 全部

---

## GUI Agent 视角（学习时始终记住这个映射）

```
RL 概念     →   GUI Agent 对应
State S     →   当前屏幕截图 + 任务描述
Action A    →   点击(x,y) / 输入文字 / 滚动 / 按键
Reward R    →   任务完成度（这是研究难点！）
Policy π    →   VLM 的决策函数
Episode     →   从任务开始到完成（或失败）的完整交互
```

---

## 任务清单

### 3B.1 MDP & 动态规划（SDS6007）
- [ ] 读讲义：Bellman 方程的直觉（"当前价值 = 即时奖励 + 折扣后未来价值"）
- [ ] **实现：** 手写 GridWorld 环境（不用 gym）
  - 4×4 网格，有障碍物和终点
  - `step(action)` 返回 `(next_state, reward, done)`
  - `render()` 打印当前状态
- [ ] 在 GridWorld 上跑通 Q-table

### 3B.2 Value / Policy Iteration（SDS6007）
- [ ] **实现：** Value Iteration，可视化每轮迭代后的价值函数热力图
- [ ] **实现：** Policy Iteration，对比两者收敛速度
- [ ] 自问：折扣因子 γ=0 和 γ=1 分别代表什么行为偏好？

### 3B.3 Q-learning & TD（SDS6007）
- [ ] **实现：** Q-learning 在 GridWorld 上收敛，画出 Q 值随 episode 的变化曲线
- [ ] 用 gym 的 CartPole 测试 Q-learning（需要离散化状态空间）

### 3B.4 DQN（SDS6007：Value Function Approximation）
- [ ] 理解为什么 Q-table 无法处理高维状态（GUI 截图就是高维！）
- [ ] 理解两个关键技巧：
  - **Experience Replay**：打破数据时序相关性
  - **Target Network**：稳定训练目标
- [ ] **实现：** PyTorch DQN，CartPole avg reward > 195

### 3B.5 ⭐ Policy Gradient & PPO（SDS6007）
- [ ] **实现：** REINFORCE 算法（最基础的 PG）
- [ ] 理解 PPO clip 操作：防止策略更新步子太大崩溃
- [ ] 理解 RLHF = PPO + Reward Model（与 Phase 3A 的 RLHF **汇合点**！）

### 3B.6 Multi-Armed Bandit（SDS6007）
- [ ] 实现 ε-greedy，可视化 regret 曲线
- [ ] 理解 Exploration vs Exploitation（GUI Agent 也需要探索未知操作）

---

## 核心问题（能回答才算过关）

- Q-learning 和 Policy Gradient 的根本区别？
- DQN 的 Experience Replay 解决了什么问题？
- PPO clip 操作的直觉解释？
- 为什么 RLHF 用 PPO 而不是更简单的 REINFORCE？

---

## 我的笔记
_（学完后填）_

**Q-learning vs Policy Gradient 的本质区别：**

**PPO clip 的直觉：**

**RLHF 为什么用 PPO：**

---

## 卡住点记录

---

**完成日期：** _____　　**自评：** ___/10