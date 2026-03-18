# GUI Agent 核心能力（Section 3）

> 本目录对应论文 Section 3，涵盖 GUI Agent 的五项能力。

## 能力层次结构

```
GUI Agent 核心能力
│
├── 基础能力（Basic Capabilities）——完成基本任务自动化的前提
│   ├── 3.1.1 GUI 环境理解（GUI Environment Comprehension）
│   │       └── → 2.1_gui-comprehension.md
│   ├── 3.1.2 设备控制（Device Control）
│   │       └── → 2.2_device-control.md
│   └── 3.1.3 用户交互（User Interaction）
│           └── → 2.3_user-interaction.md
│
└── 高级能力（Advanced Capabilities）——提升体验与效率的扩展能力
    ├── 3.2.1 个性化服务（Personalized Services）
    │       └── → 2.4_advanced-capabilities.md
    └── 3.2.2 Agent 协同（Agent Synergy）
            └── → 2.4_advanced-capabilities.md
```

## 论文中的代表性系统（Table 1）

| 系统 | 平台 | GUI 理解方式 | 控制方式 | 年份 |
|------|------|------------|---------|------|
| **SpotLight** | Mobile | Vision-Based | UI-based | 2022 |
| **AppAgent** | Mobile | Hybrid Text-Vision | UI-based | 2023 |
| **DroidBot-GPT** | Mobile | Text-Based | UI-based | 2023 |
| **Mobile-Agent** | Mobile | Vision-Based | UI-based | 2024 |
| **Mobile-Agent-v2** | Mobile | Vision-Based | UI-based | 2024 |
| **SeeClick** | Mobile | Vision-Based | UI-based | 2024 |
| **WebGPT** | Computer | Text-Based | Code-based | 2021 |
| **WebAgent** | Computer | Text-Based | Code-based | 2023 |
| **WebVoyager** | Computer | Hybrid Text-Vision | UI-based | 2024 |
| **SeeAct** | Computer | Hybrid Text-Vision | UI-based | 2024 |
| **UFO** | Computer | Vision-Based | UI-based | 2024 |
| **MMAC-Copilot** | Computer | Vision-Based | UI+Code | 2024 |
| **CogAgent** | Computer | Vision-Based | UI-based | 2024 |
| **WebWISE** | Computer | Vision-Based | Code-based | 2023 |

## 关键 Research Gap（从能力角度）

- 现有系统大多**无跨会话记忆**：每次任务从零开始
- GUI Agent 的**个性化能力**极为初级（仅 Friday 有初步尝试）
- **多智能体协同**研究有限（仅 UFO, MMAC-Copilot, Mobile-Agent-v2）
