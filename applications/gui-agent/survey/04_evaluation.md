# 评估基准（Evaluation Benchmark）

> 论文 Section 5（Pages 20–23）

---

## 5.1 评估数据集

### 完整数据集概览（Table 2）

| 数据集 | 平台 | 观测方式 | 多轮对话 | 高级任务 | 领域数 | 实例数 |
|--------|------|---------|---------|---------|--------|--------|
| **Meta-GUI** | Mobile | Screenshot+VH | ✓ | ✓ | 11 | 1,125 |
| **MobileGPT** | Mobile | Screenshot+VH | ✓ | ✓ | 8 | 160 |
| **PixelHelp** | Mobile | Screenshot+VH | ✗ | ✓ | — | 187 |
| **RICOSCA** | Mobile | Screenshot+VH | ✗ | ✗ | 9.7k | 25,677 |
| **MoTiF** | Mobile | Screenshot+VH | ✗ | ✓ | 125 | 61K |
| **UGIF** | Mobile | Screenshot+VH | ✗ | ✓ | 11 | 4,184 |
| **MobileAgentBench** | Mobile | Screenshot+VH | ✗ | ✓ | 10 | 100 |
| **DroidTask** | Mobile | Screenshot+VH | ✗ | ✓ | 13 | 158 |
| **AndroidEnv** | Mobile | Screenshot | ✗ | ✓ | 30 | 100 |
| **MobileEnv** | Mobile | Screenshot+VH | ✗ | ✓ | — | 856,045 |
| **LlamaTouch** | Mobile | Screenshot+VH | ✗ | ✓ | 57 | 496 |
| **WebArena** | Computer | Screenshot+DOM | ✗ | ✓ | 6 | 812 |
| **VWA** | Computer | Screenshot+DOM | ✗ | ✓ | 3 | 910 |
| **WebVoyager** | Computer | Screenshot+DOM | ✗ | ✓ | 15 | 300 |
| **WebShop** | Computer | Screenshot+DOM | ✗ | ✓ | 1 | 12,087 |
| **MiniWoB++** | Computer | Screenshot+DOM | ✗ | ✗ | 100 | 100 |
| **WebLINX** | Computer | Screenshot+DOM | ✓ | ✓ | 155 | 2,337 |
| **RUSS** | Computer | Screenshot+DOM | ✓ | ✓ | 22 | 80 |
| **PhraseNode** | Computer | Screenshot+DOM | ✗ | ✗ | — | 51,663 |
| **UIBert** | Computer | Screenshot+DOM | ✗ | ✗ | — | 16,660 |
| **Mind2Web** | Computer | Screenshot+DOM | ✗ | ✓ | 137 | 2,350 |
| **AssistGUI** | Computer | Screenshot+Metadata | ✗ | ✓ | 9 | 100 |
| **AITW** | Mobile+Computer | Screenshot | ✗ | ✓ | 357 | 30K |
| **ScreenSpot** | Mobile+Computer | Screenshot | ✗ | ✗ | — | 1,200 |

### 数据集演进路径

```
低级任务（Low-Level）               高级任务（High-Level）
单步元素选择                  →    多步任务完成
PhraseNode, UIBert                PixelHelp, UGIF, MoTiF

单轮交互                      →    多轮对话
绝大多数数据集                      Meta-GUI, WebLINX, RUSS

单平台                        →    跨平台
Mobile-only / Web-only              AITW, ScreenSpot
```

### 特殊数据集亮点

- **AssistGUI**：桌面任务 + 教学视频辅助（结合视频理解）
- **MobileEnv**：最大规模（85万实例）
- **WebLINX**：最丰富的领域数（155个领域）+ 多轮对话
- **ScreenSpot**：专门评测 MLLM 在 GUI 元素定位的能力

---

## 5.2 评估指标

### 低级任务指标

| 指标 | 定义 | 使用场景 |
|------|------|---------|
| **Element Selection Accuracy** | 正确选择元素的比例 | PhraseNode, UIBert |
| **Click Accuracy** | 预测位置落在 Ground Truth 边界框内的比例 | SeeClick, ScreenSpot |

### 高级任务指标

| 指标 | 定义 | 局限性 |
|------|------|--------|
| **Success Rate (SR)** | 达到目标最终状态的实例比例 | 严格（0/1），无法评估部分完成 |
| **Step Success Rate (SSR)** | 成功步骤数 / 总步骤数 | Mind2Web 提出 |

### 对话任务指标（WebLINX）

任务目标在对话过程中动态演化，Success Rate 不适用，改用轮次级评估：

**Element Similarity**（针对点击、输入类操作）：
```
IM(a', a) × (B_reference ∪ B_predicted) / (B_reference ∩ B_predicted)
```
其中 IM（Intent Matching）= 1 表示意图一致，计算边界框 IoU。

**Text Similarity**（针对文本输出）：
```
IM(a', a) × chrF(a', a)    # chrF = character n-gram F1，n=6
```

### 其他评估方法

| 方法 | 原理 | 优缺点 |
|------|------|--------|
| **关键步骤奖励** | 手工设计奖励函数（MobileEnv） | 准确但繁琐 |
| **GPT-4V 自动评估** | 用 GPT-4V 评估轨迹（WebVoyager）| 85.3% 与人工评估一致率；可扩展 |
| **UI 状态比对** | 比较任务执行后的 UI 状态（MobileAgentBench, LlamaTouch） | LlamaTouch 支持多级别 UI 状态匹配 |

---

## 评估体系的 Research Gap

1. **部分完成无法量化**：Success Rate 是 0/1 指标，不能区分"完成了80%"与"完全失败"
2. **评估路径单一性**：同一任务可能有多种合法操作序列，但多数数据集只有单一 Ground Truth
3. **跨会话评估缺失**：所有数据集均为单次任务，无法评估 Agent 跨会话的个性化和学习能力
4. **真实世界评估难**：封闭环境（模拟器）与真实设备的评估差距大

---

## Personal Research Notes

- [ ] **跨会话评估**是最明显的空白：如果 Agent 在第二次完成同类任务时效率更高，现有基准无法捕捉这种改进
- [ ] GPT-4V 自动评估（85.3% 一致率）提示：用强 LLM 作为 Critic 是可行的——这是构建 Self-Evolving GUI Agent 评估体系的基础
- [ ] Mind2Web（137个领域，2350实例）是目前领域覆盖最广的高级 Web 任务数据集，适合作为通用 benchmark
- [ ] LlamaTouch 的多级别 UI 状态匹配是一个值得关注的评估创新——部分完成也能被量化
