# GUI Agent

北极星：VLM 感知 + LLM 规划 + RL 决策，在 GUI 上自主完成用户任务。

综合使用所有上游能力（memory、self-improvement、grounding、planning、alignment）。

## 内容

- [survey/](./survey/) — 来自 "GA: A Comprehensive Survey on LLM-based GUI Agents"（Huang et al., 2025）的结构化笔记
- [papers/](./papers/) — 单篇论文精读（AppAgent、MobileAgent、MAGNET、EvoCUA 等 17 篇）
- [2025-12_CUA-Slow-Thinking-Podcast.md](./2025-12_CUA-Slow-Thinking-Podcast.md) — 实践者视角：CUA 慢思考播客笔记

## 实践

**Mini GUI Agent 项目：**

```python
# 核心循环
while not task_done:
    screenshot = capture_screen()          # 截图
    action = vlm.decide(screenshot, task)  # VLM 决策
    execute(action)                         # PyAutoGUI 执行
    done = evaluate(screenshot, task)       # 任务完成判断
```

**里程碑：**
- [ ] M1：截图 → VLM → 返回结构化 JSON 动作
- [ ] M2：解析动作，PyAutoGUI 执行点击和输入
- [ ] M3：完成完整任务：打开浏览器 → 搜索 → 返回结果标题
- [ ] M4：加入错误恢复：无效坐标时的处理策略
- [ ] M5：设计评估模块：如何判断任务成功？
