# GUI Agent 方法对比矩阵

## 维度定义

- **GUI 理解方式**：Text-Based / Vision-Based / Hybrid Text-Vision
- **记忆机制**：无 / 短期（In-Context）/ 长期（外部存储）/ 用户画像
- **自我进化能力**：无 / Trial & Error 探索 / Reflection 纠错 / 持续学习
- **任务类型**：Mobile / Web / Desktop / 通用
- **控制方式**：UI-based / Code-based / 混合
- **多智能体**：单 Agent / 多 Agent

## 论文对比


| 系统                  | 年份   | GUI 理解       | 记忆机制      | 自我进化            | 任务类型          | 控制方式       | 多智能体    | 核心 Benchmark | 主要局限          |
| ------------------- | ---- | ------------ | --------- | --------------- | ------------- | ---------- | ------- | ------------ | ------------- |
| **SpotLight**       | 2022 | Vision-Based | 无         | 无               | Mobile        | UI-based   | 单       | —            | 无跨任务经验积累      |
| **WebGPT**          | 2021 | Text-Based   | 短期        | 无               | Web           | Code-based | 单       | —            | 仅限搜索任务        |
| **AppAgent**        | 2023 | Hybrid       | 短期+探索知识库  | Trial & Error   | Mobile        | UI-based   | 单       | —            | 探索知识不可迁移      |
| **MobileGPT**       | 2023 | Vision-Based | 探索知识库     | Trial & Error   | Mobile        | UI-based   | 单       | —            | 探索代价高         |
| **DroidBot-GPT**    | 2023 | Text-Based   | 无         | 无               | Mobile        | UI-based   | 单       | —            | 依赖 VH 访问权限    |
| **WebAgent**        | 2023 | Text-Based   | 短期        | 无               | Web           | Code-based | 单       | Mind2Web     | VH/DOM 冗长     |
| **WebWISE**         | 2023 | Vision-Based | 无         | 无               | Web           | Code-based | 单       | —            | 依赖 Pix2Struct |
| **MM-Navigator**    | 2023 | Vision-Based | 短期        | 无               | Mobile        | UI-based   | 单       | —            | 依赖 GPT-4V     |
| **WebGUM**          | 2023 | Hybrid       | 短期        | 无               | Web           | UI-based   | 单       | Mind2Web     | —             |
| **AutoDroid**       | 2024 | Text-Based   | 探索知识库     | Trial & Error   | Mobile        | UI-based   | 单       | —            | 知识不可跨 App     |
| **MindAct**         | 2024 | Text-Based   | 短期        | 无               | Web           | UI-based   | 单       | Mind2Web     | —             |
| **Mobile-Agent**    | 2024 | Vision-Based | 短期        | 无               | Mobile        | UI-based   | 单       | —            | 无长期记忆         |
| **Mobile-Agent-v2** | 2024 | Vision-Based | 短期（任务压缩）  | Reflection 纠错   | Mobile        | UI-based   | 3 Agent | —            | 仅单任务内反思       |
| **SeeClick**        | 2024 | Vision-Based | 无         | 无               | Mobile        | UI-based   | 单       | ScreenSpot   | —             |
| **CocoAgent**       | 2024 | Vision-Based | 短期        | 无               | Mobile        | UI-based   | 单       | —            | —             |
| **SeeAct**          | 2024 | Hybrid       | 短期        | 无               | Web           | UI-based   | 单       | Mind2Web     | —             |
| **WebVoyager**      | 2024 | Hybrid       | 短期        | 无               | Web           | UI-based   | 单       | WebVoyager   | —             |
| **DUAL-VCR**        | 2024 | Hybrid       | 短期        | 无               | Web           | UI-based   | 单       | —            | —             |
| **UFO**             | 2024 | Vision-Based | 短期        | 无               | Desktop (Win) | UI-based   | 2 Agent | —            | 仅 Windows     |
| **AutoWebGLM**      | 2024 | Text-Based   | 短期        | 无               | Web           | UI-based   | 单       | WebArena     | —             |
| **MMAC-Copilot**    | 2024 | Vision-Based | 短期+检索     | 无（有 Reflection） | Desktop       | UI+Code    | 6 Agent | —            | 推理成本高         |
| **CogAgent**        | 2024 | Vision-Based | 无         | 无               | Web+Desktop   | UI-based   | 单       | Mind2Web     | 无记忆           |
| **Friday**          | 2024 | ?            | 用户画像（声明性） | 无               | Desktop       | UI-based   | 单       | —            | 个性化初步         |


## 从矩阵中观察到的模式

- **观察 1**：23个系统中，**21个无长期记忆机制**，仅 AppAgent/MobileGPT/AutoDroid 有基于探索的任务级知识库，Friday 有初步用户画像
- **观察 2**：**自我进化能力极为有限**：Trial & Error（3个）、Reflection 纠错（1个，仅单任务内）、持续学习（0个）
- **观察 3**：**Vision-Based 占主导**（13/23），Text-Based 次之（6/23），Hybrid 最少（4/23）——尽管 Hybrid 理论上更强
- **观察 4**：**多智能体仅3个系统**，且均无跨 Agent 的共享长期记忆
- **观察 5**：所有系统均为**单次任务**框架，无跨会话持续学习设计

## 由此产生的 Research Gap 候选

- **Gap A**：跨任务、跨会话的 GUI 经验记忆机制（23/23 系统缺失）
- **Gap B**：跨应用的 GUI 知识迁移（即使是同类型操作也需重新探索）
- **Gap C**：从单任务 Reflection 到跨任务自我进化的机制设计
- **Gap D**：GUI Agent 的个性化能力（仅 Friday 初步尝试）
- **Gap E**：Hybrid 范式的系统化研究（理论优势未被充分挖掘）

