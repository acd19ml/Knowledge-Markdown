# Phase 4：GUI Agent

**前置条件：** Phase 3A（LLM Agent）+ 3B（PPO）+ 3C（多模态）全部完成

---

## 知识汇合

```
CS5489  → 神经网络 / CNN                →  VLM 视觉编码器的基础
CS6493  → Transformer + LLM Agent      →  LLM 规划 + ReAct 框架
SDS6007 → MDP + PPO                    →  Agent 决策优化 + RLHF
CS5494  → CLIP + VLM + Prompt          →  截图理解 + Agent 控制接口
```

---

## 论文阅读（按顺序）

| 论文 | 状态 | 核心贡献一句话 | 对我的启发 |
|------|------|--------------|----------|
| ReAct (2022) | [ ] | | |
| AppAgent (2023) | [ ] | | |
| UFO (2024) | [ ] | | |
| OS-Copilot (2024) | [ ] | | |

**论文笔记模板**（每篇建一个 `.md` 文件放在 `papers/` 下）：
```
# 论文标题
## 一句话总结
## 解决什么问题（之前方法的不足）
## 核心方法（关键创新点）
## 与我研究方向的关联
## 值得复现的实验
## 遗留问题
```

---

## 第一个项目：Mini GUI Agent

```python
# 核心循环（Phase 4 实现）
while not task_done:
    screenshot = capture_screen()          # 截图
    action = vlm.decide(screenshot, task)  # VLM 决策
    execute(action)                         # PyAutoGUI 执行
    done = evaluate(screenshot, task)       # 任务完成判断（研究难点）
```

**技术栈：** `mss`（截图）+ `openai` / `transformers`（VLM）+ `pyautogui`（执行）

**里程碑：**
- [ ] M1：截图 → VLM → 返回结构化 JSON 动作（先不执行，只看输出质量）
- [ ] M2：解析动作，PyAutoGUI 执行点击和输入
- [ ] M3：完成完整任务：打开浏览器 → 搜索 → 返回结果标题
- [ ] M4：加入错误恢复：无效坐标时的处理策略
- [ ] M5：设计评估模块：如何判断任务成功？

---

## 架构演化时间线（Phase 2 完成后画）

```
LeNet(1998) → AlexNet(2012) → ResNet(2015) → Transformer(2017)
→ BERT(2018) → GPT-2(2019) → GPT-3(2020) → CLIP(2021)
→ GPT-4(2023) → GPT-4V(2023) → Qwen-VL → ... → GUI Agent
```

---

## GUI Agent 面试题

- Q: GUI Agent 和普通 LLM Agent 的核心区别？A: _____
- Q: 如何把 GUI 操作建模为 MDP？A: S=截图+任务, A=点击/输入, R=完成度, π=VLM
- Q: VLM 理解 GUI 截图的主要挑战？A: _____（坐标精度 / 动态元素 / 小图标识别）
- Q: GUI Agent 的评估指标有哪些？A: _____（Task Success Rate / Step Efficiency）

---

**开始日期：** _____