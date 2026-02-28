# 为 Claude 构建 Skill 的完整指南（中文版）

---

## 目录

- 引言 — 3  
- 基础概念 — 4  
- 规划与设计 — 7  
- 测试与迭代 — 14  
- 分发与分享 — 18  
- 模式与故障排查 — 21  
- 资源与参考 — 28  

---

## 引言

一个 **Skill**（技能）是一组指令，打包成一个简单的文件夹，用来教 Claude 如何处理特定任务或工作流。Skill 是定制 Claude 以满足你特定需求的最强方式之一。与其在每次对话中重复讲解你的偏好、流程和领域知识，不如通过 Skill 一次性教会 Claude，此后在任何支持 Skill 的场景中都能受益。

当你有 **可重复的工作流** 时，Skill 的威力最大：例如根据规格自动生成前端设计、用一致的方法做调研、创建遵守团队风格指南的文档，或者编排多步流程。Skill 可以很好地与 Claude 的内置能力配合，比如代码执行和文档生成。对于构建 MCP 集成的人而言，Skill 又增加了一层强大的「知识与流程」抽象层，帮助把原始工具访问转化为稳定且优化的工作流。

本指南覆盖了构建高效 Skill 所需的全部内容 —— 从规划与结构，到测试与分发。无论你是为自己、为团队，还是为社区构建 Skill，都能在这里找到实践范式和真实案例。

**你将学习到：**

- Skill 结构的技术要求与最佳实践  
- 适用于「纯 Skill」和「Skill + MCP」工作流的模式  
- 我们在不同用例中验证有效的一些设计模式  
- 如何测试、迭代和分发你的 Skill  

**适用人群：**

- 希望 Claude 严格遵循特定工作流的开发者  
- 希望 Claude 能稳定执行固定流程的高阶用户  
- 希望在组织内统一 Claude 使用方式的团队  

> **阅读路径建议**
>
> - 只构建「纯 Skill」、不依赖 MCP？重点阅读「基础概念」「规划与设计」和第 1–2 类用例。  
> - 用 Skill 增强 MCP 集成？重点看「Skill + MCP」章节和第 3 类用例。  
> 两条路径共享同一套技术要求，你可以只关注与你用例相关的部分。
>
> **阅读完能得到什么？**  
> 在熟悉 `skill-creator` 的帮助下，你应该能在一次完整的坐席（约 15–30 分钟）内构建并测试出一个可用的 Skill。

让我们开始。

---

## 第 1 章 — 基础概念（Fundamentals）

### 什么是 Skill？

一个 Skill 就是一个文件夹，包含：

- **`SKILL.md`（必需）**：带 YAML frontmatter 的 Markdown 指令文件  
- **`scripts/`（可选）**：可执行代码（Python、Bash 等）  
- **`references/`（可选）**：按需加载的文档资料  
- **`assets/`（可选）**：在输出中需要用到的模板、字体、图标等  

### 核心设计原则

#### 渐进式暴露（Progressive Disclosure）

Skill 采用三层信息结构：

- **第一层（YAML frontmatter）**：  
  总会被加载进 Claude 的 system prompt。只提供足够的信息，让 Claude 知道「什么时候考虑使用这个 Skill」，而不用把所有细节都装进上下文。
- **第二层（`SKILL.md` 正文）**：  
  当 Claude 判断这个 Skill 与当前任务相关时再加载。包含完整的指令和指导。
- **第三层（链接文件）**：  
  同一 Skill 目录下打包的额外文件，Claude 只有在需要时才会主动打开和探索。

这种渐进式暴露既节省 Token，又保留了专业知识的表达能力。

#### 可组合性（Composability）

Claude 可以同时加载多个 Skill。你的 Skill 不应假设自己是「唯一能力」，而应该能和其他 Skill 协同工作。

#### 可移植性（Portability）

Skill 在 Claude.ai、Claude Code 和 API 间行为一致。只要运行环境满足 Skill 所需的依赖，你只需编写一次 Skill，就能在所有界面使用。

---

### 面向 MCP 构建者：Skill + Connector

> 💡 **只做纯 Skill、暂不用 MCP？**  
> 可以直接跳到「规划与设计」，以后再回来读这一节。

如果你已经有了可用的 MCP 服务器，那么最难的一部分其实已经完成。Skill 是其上的「知识层」—— 把你对工具的经验、最佳实践和工作流固化下来，让 Claude 能稳定执行。

#### 厨房类比

- **MCP**：提供专业厨房 —— 工具、食材和设备的访问能力。  
- **Skill**：提供菜谱 —— 如何一步步做出有价值的东西。

二者结合，可以让用户在不知道每个细节的情况下完成复杂任务。

#### 它们如何协同工作？

| MCP（连接性） | Skill（知识） |
|---|---|
| 把 Claude 连接到你的服务（Notion、Asana、Linear 等） | 教 Claude 如何高效地使用这些服务 |
| 提供实时数据访问和工具调用 | 固化工作流与最佳实践 |
| 告诉 Claude **能做什么** | 告诉 Claude **应该怎么做** |

#### 为什么这对 MCP 用户很重要？

**只有 MCP、没有 Skill 的情况：**

- 用户连上你的 MCP 后，不知道下一步该干什么  
- 不断收到「如何用你们的集成做 X？」这样的工单  
- 每次对话都从零开始  
- 因为用户提示词不同，结果风格也不一致  
- 用户把工作流问题误认为是「你们的 Connector 有问题」  

**有 MCP 也有 Skill 的情况：**

- 预设的工作流在需要时自动激活  
- 工具使用更稳定、可预期  
- 最佳实践被嵌入每一次交互  
- 用户学习成本明显降低  

---

## 第 2 章 — 规划与设计（Planning and Design）

### 从用例出发

在写任何代码之前，先明确 2–3 个希望这个 Skill 能支持的 **具体用例**。

**一个好的用例定义示例：**

> **用例：** 项目冲刺计划（Project Sprint Planning）  
>  
> **触发方式：** 用户说「帮我规划这次 sprint」或「创建 sprint 任务」  
>  
> **步骤：**  
> 1. 通过 MCP 从 Linear 拉取当前项目状态  
> 2. 分析团队速度与产能  
> 3. 给出任务优先级建议  
> 4. 在 Linear 中创建任务，并加上标签和预估  
>  
> **结果：** 一次完整规划好的 sprint，相关任务已在 Linear 中创建  

**自问几个问题：**

- 用户真正想完成的事情是什么？  
- 这件事拆成几个步骤？中间的工作流是什么？  
- 需要哪些工具（Claude 内置？MCP？）  
- 哪些领域知识 / 最佳实践需要固化在 Skill 里？  

---

### 常见 Skill 用例分类

在 Anthropic，我们大致看到了三类常见 Skill 用法：

#### 类别 1：文档与资产生成（Document & Asset Creation）

**用途：** 生成结构稳定、质量高的文档、PPT、应用、设计、代码等。

真实示例：`frontend-design` Skill（以及一系列 docx、pptx、xlsx 相关 Skill）

> 「用于创建具有高设计质量、可投产的前端界面。适用于构建 Web 组件、页面、海报或应用等视觉成果。」

**关键技巧：**

- 内嵌的样式指南与品牌规范  
- 通过模板结构保证输出一致性  
- 在最终完成前使用质量检查清单  
- 无需额外工具 —— 使用 Claude 内置能力即可  

---

#### 类别 2：工作流自动化（Workflow Automation）

**用途：** 多步骤、需要统一方法论的流程；可跨多个 MCP server 协调。

真实示例：`skill-creator` Skill

> 「一个交互式向导，用于创建新的 Skill。会引导用户完成用例定义、frontmatter 生成、指令撰写和校验。」

**关键技巧：**

- 清晰的分步工作流 + 校验关卡  
- 提供常见结构模板  
- 内置复盘与改进建议  
- 支持多轮迭代优化  

---

#### 类别 3：MCP 能力增强（MCP Enhancement）

**用途：** 在 MCP 提供工具访问的基础上，提供工作流与领域经验。

真实示例：`sentry-code-review`（来自 Sentry）

> 「基于 Sentry 错误监控数据，通过其 MCP server 自动分析并修复 GitHub PR 中的 bug。」

**关键技巧：**

- 串联多次 MCP 调用  
- 内置领域专业知识  
- 提供用户 otherwise 需要自己说明的上下文  
- 对常见 MCP 错误做容错与恢复  

---

### 定义成功标准（Success Criteria）

你如何知道一个 Skill「算是好用」了？

这些指标更像是 **目标区间 / 参考值**，而非严格阈值。目前我们也在持续建设更系统的评估工具。

**量化指标示例：**

- **在 90% 的相关请求中能被正确触发**  
  - *测量方式：* 准备 10–20 条应该触发该 Skill 的请求，统计自动加载 vs 手动调用的比例。
- **用更少的 Tool 调用完成同样任务**  
  - *测量方式：* 比较开启与关闭 Skill 时，同一任务所需的工具调用次数与 Token 消耗。
- **每个工作流中 0 次失败的 API 调用**  
  - *测量方式：* 在测试期间监控 MCP 日志，统计重试率和错误码。  

**定性指标示例：**

- **用户不需要再提示 Claude 下一步该干嘛**  
  - *评估方式：* 测试时记录你需要纠正 / 引导 Claude 的次数；让试用用户给主观反馈。
- **工作流能一次跑完，用户无需大量修正**  
  - *评估方式：* 重复运行同一请求 3–5 次，对比输出在结构和质量上的一致性。
- **不同会话之间表现一致**  
  - *评估方式：* 新用户在基本无指导的情况下，是否能一次成功完成任务？  

---

### 技术要求（Technical Requirements）

#### 文件结构

```text
your-skill-name/
├── SKILL.md          # 必需 - 主 Skill 文件
├── scripts/          # 可选 - 可执行脚本
│   ├── process_data.py   # 示例
│   └── validate.sh       # 示例
├── references/       # 可选 - 文档/参考资料
│   ├── api-guide.md      # 示例
│   └── examples/         # 示例
└── assets/           # 可选 - 模板等
    └── report-template.md  # 示例
```

#### 关键规则

**关于 `SKILL.md` 命名：**

- 文件名必须精确为 `SKILL.md`（大小写敏感）  
- 不接受变体（如 `SKILL.MD`、`skill.md` 等）  

**Skill 文件夹命名：**

- 使用 kebab-case：`notion-project-setup` ✅  
- 禁止空格：`Notion Project Setup` ❌  
- 禁止下划线：`notion_project_setup` ❌  
- 禁止驼峰 / 大写：`NotionProjectSetup` ❌  

**不要在 Skill 目录中放 `README.md`：**

- Skill 目录里不要有 `README.md`  
- 所有说明文档写在 `SKILL.md` 或 `references/` 中  
- 若用 GitHub 分发，可以在仓库根目录放 README（面向人类读者），但 Skill 目录本身不要再有 README  

---

### YAML frontmatter：最关键的部分

YAML frontmatter 决定了 Claude 什么时候会加载你的 Skill，这部分写好非常重要。

**最小必需格式：**

```yaml
---
name: your-skill-name
description: 它做什么。用户在何种请求下使用它（用自然语言描述触发条件）。
---
```

有了这些，你就已经能开始了。

#### 字段要求

**`name`（必需）：**

- 只能使用 kebab-case  
- 不含空格、大写字母  
- 建议与 Skill 文件夹名一致  

**`description`（必需）：**

- **必须同时包含：**
  - 这个 Skill 做什么  
  - 什么时候应该用它（触发条件）  
- 字数 < 1024 字符  
- 不允许出现 XML 标签字符（`<` 或 `>`）  
- 尽量包含用户可能说出的具体任务用语  
- 若与特定文件类型有关，请在描述中提及  

**`license`（可选）：**

- 若以开源形式发布 Skill，可在此声明协议  
- 常见：`MIT`、`Apache-2.0` 等  

**`compatibility`（可选）：**

- 1–500 字符  
- 用来说明运行环境需求：支持的产品、系统依赖、是否需要网络等  

**`metadata`（可选）：**

- 任意自定义键值对  
- 常见建议：`author`、`version`、`mcp-server` 等  

```yaml
metadata:
  author: ProjectHub
  version: 1.0.0
  mcp-server: projecthub
```

#### 安全限制

**在 frontmatter 中禁止的内容：**

- XML 尖括号（`< >`）  
- `name` 中包含「claude」或「anthropic」的 Skill 名（保留字）  

*原因：* frontmatter 会进入 Claude 的 system prompt，恶意内容可能用来做 Prompt Injection。

---

### 如何撰写高质量的 Skill

#### `description` 字段

根据 Anthropic 工程博客的说法：  
> 「这个元数据……提供了恰到好处的信息，让 Claude 知道何时使用某个 Skill，而无需把所有内容载入上下文。」  

这就是渐进式暴露中的**第一层**。

**推荐结构：**

```text
[做什么] + [在何种情境使用] + [关键能力]
```

**好的示例：**

```yaml
# 示例 1：具体且可操作
description: Analyzes Figma design files and generates developer handoff
  documentation. Use when user uploads .fig files, asks for "design specs",
  "component documentation", or "design-to-code handoff".

# 示例 2：包含触发短语
description: Manages Linear project workflows including sprint planning, task
  creation, and status tracking. Use when user mentions "sprint", "Linear tasks",
  "project planning", or asks to "create tickets".

# 示例 3：价值主张清晰
description: End-to-end customer onboarding workflow for PayFlow. Handles account
  creation, payment setup, and subscription management. Use when user says "onboard
  new customer", "set up subscription", or "create PayFlow account".
```

**不好的示例：**

```yaml
# 太模糊
description: Helps with projects.

# 缺少触发条件
description: Creates sophisticated multi-page documentation systems.

# 过于技术化，没有用户视角的触发语
description: Implements the Project entity model with hierarchical relationships.
```

---

### 撰写主体指令（`SKILL.md` 正文）

frontmatter 之后，就是 Skill 的实际指令内容（Markdown）。

**推荐结构：**

```markdown
---
name: your-skill
description: [它做什么；在何种情况下使用]
---

# Your Skill Name

## Instructions（使用说明）

### Step 1: [第一大步]
解释该步骤做什么、如何做。

### Step 2: [下一步]
...

## Examples（示例）

### Example 1: [常见场景]
User says: "Set up a new marketing campaign"

Actions:
1. Fetch existing campaigns via MCP
2. Create new campaign with provided parameters

Result: Campaign created with confirmation link

## Troubleshooting（故障排查）

### Error: [常见错误信息]
**Cause:** [原因]
**Solution:** [解决方案]
```

---

### 指令撰写最佳实践

#### 具体且可执行（Be Specific and Actionable）

✅ **好的写法：**

```text
Run `python scripts/validate.py --input {filename}` to check data format.
If validation fails, common issues include:
- Missing required fields (add them to the CSV)
- Invalid date formats (use YYYY-MM-DD)
```

❌ **不好的写法：**

```text
Validate the data before proceeding.
```

---

#### 包含错误处理逻辑

```markdown
## Common Issues

### MCP Connection Failed
If you see "Connection refused":
1. Verify MCP server is running: Check Settings > Extensions
2. Confirm API key is valid
3. Try reconnecting: Settings > Extensions > [Your Service] > Reconnect
```

#### 清晰引用打包的参考资源

```markdown
Before writing queries, consult `references/api-patterns.md` for:
- Rate limiting guidance
- Pagination patterns
- Error codes and handling
```

#### 利用渐进式暴露

让 `SKILL.md` 聚焦在核心指令上，把更详细的文档放到 `references/`，并在正文中链接。  
（参见前文「核心设计原则」中对三层结构的说明。）

---

## 第 3 章 — 测试与迭代（Testing and Iteration）

Skill 的测试可以有不同严格程度，取决于你的需求：

- **在 Claude.ai 上手动测试**：直接运行查询、观察行为。无需额外配置，迭代速度最快。  
- **在 Claude Code 中脚本化测试**：用脚本自动运行测试用例，便于在修改后重复验证。  
- **通过 Skills API 做程序化测试**：对一批测试集系统性地跑评估。  

选择与你的质量要求以及 Skill 的「曝光度」相匹配的方式：  
一个只在小团队内部使用的 Skill，和一个要部署给上千企业用户的 Skill，测试需求显然不同。

> **经验提示：先把一个任务打磨好，再扩展范围**
>
> 我们观察到，最有效的 Skill 创建者会围绕一个有挑战性的任务不断迭代，直到 Claude 表现稳定，然后把那套做法提炼成 Skill。这种方式能充分利用 Claude 的 In-Context Learning，比「一开始就做大而全的测试」更快获得信号。  
> 有了扎实的基础之后，再扩展到多种测试用例，做覆盖度检查。

---

### 推荐的测试方案

根据早期经验，一个有效的 Skill 测试通常覆盖三方面：

#### 1. 触发测试（Triggering Tests）

**目标：** 确保在「该触发时」能触发 Skill，而在其他情况不会乱触发。

**测试点：**

- ✅ 对明显相关的请求会触发  
- ✅ 对同义改写的请求会触发  
- ❌ 对无关话题不会触发  

**示例测试集：**

应该触发：

- "Help me set up a new ProjectHub workspace"  
- "I need to create a project in ProjectHub"  
- "Initialize a ProjectHub project for Q4 planning"  

不应触发：

- "What's the weather in San Francisco?"  
- "Help me write Python code"  
- "Create a spreadsheet"（除非 Skill 确实负责这类任务）  

---

#### 2. 功能测试（Functional Tests）

**目标：** 验证 Skill 的输出是否正确。

**测试点：**

- 输出结构与内容正确  
- API 调用成功  
- 错误处理逻辑生效  
- 边界情况能正确处理  

**示例：**

```text
Test: Create project with 5 tasks
Given: Project name "Q4 Planning", 5 task descriptions
When:  Skill executes workflow
Then:
  - Project created in ProjectHub
  - 5 tasks created with correct properties
  - All tasks linked to project
  - No API errors
```

---

#### 3. 性能与效果对比（Performance Comparison）

**目标：** 证明「有 Skill」比「没 Skill」更好。

可以用「定义成功标准」一节中的指标。示例对比：

**基线（无 Skill）：**

- 用户每次都要重复说明流程  
- 约 15 条来回对话  
- 3 次失败的 API 调用，需要手动重试  
- 共消耗 ~12,000 tokens  

**启用 Skill 后：**

- 自动执行标准工作流  
- 仅 2 条澄清问题  
- 0 次失败的 API 调用  
- Token 消耗 ~6,000  

---

### 使用 `skill-creator` Skill

`skill-creator` Skill 已集成在 Claude.ai 的插件目录中，也可用于 Claude Code，能帮助你构建和迭代 Skill。  
如果你已经有 MCP server 且清楚 2–3 个核心工作流，通常可以在 15–30 分钟内构建并测试一个可用 Skill。

**在创建阶段：**

- 根据自然语言描述生成 Skill 雏形  
- 产出格式正确的 `SKILL.md` + frontmatter  
- 给出触发短语和结构建议  

**在 Review 阶段：**

- 标记常见问题（描述过于模糊、触发条件不全、结构问题等）  
- 识别过度触发 / 触发不足的风险  
- 根据 Skill 的用途提出测试用例建议  

**迭代优化：**

- 使用 Skill 时如果遇到边界情况或失败案例，可以把对话示例拿回给 `skill-creator`  
- 示例提示语：  
  > "Use the issues & solution identified in this chat to improve how the skill handles [specific edge case]"

**调用方式：**

```text
Use the skill-creator skill to help me build a skill for [your use case]
```

*注意：`skill-creator` 只负责设计和改写 Skill，本身不会执行自动化测试或生成定量评估结果。*

---

### 基于反馈做迭代

Skill 是**活文档**，需要随使用反馈不断优化。

**触发不足（Undertriggering）的信号：**

- 很少自动触发，即使在应该触发的场景  
- 用户频繁手动启用它  
- 有人问「什么时候该用这个 Skill？」  

**解决思路：**  
在 `description` 中增加细节与关键字（尤其是领域术语）。

**触发过多（Overtriggering）的信号：**

- 在与任务无关的话题中也频繁加载  
- 用户主动把它关掉  
- 用户对 Skill 的「用途边界」感到困惑  

**解决思路：**  
- 添加「不该使用」的反触发提示  
- 把描述写得更具体，缩小范围  

**执行问题（Execution Issues）：**

- 输出不稳定，质量时好时坏  
- MCP / API 调用频繁失败  
- 需要用户频繁纠正  

**解决思路：**  
- 改进 `SKILL.md` 中的指令  
- 增加错误处理、重试逻辑  

---

## 第 4 章 — 分发与分享（Distribution and Sharing）

Skill 能让你的 MCP 集成更「完整」。  
当用户比较不同的 Connector 时，带 Skill 的方案往往能更快创造价值，相比只有 MCP 的方案更具优势。

---

### 当前分发模式（截至 2026 年 1 月）

**普通用户如何获取 Skill：**

1. 下载 Skill 文件夹  
2. 如有需要，将其打包为 zip  
3. 在 Claude.ai 中：Settings > Capabilities > Skills 上传  
4. 或放到 Claude Code 的 skills 目录下  

**组织级 Skill：**

- 管理员可以在 Workspace 级部署 Skill（功能于 2025-12-18 上线）  
- 支持自动更新  
- 集中管理与控制  

---

### 开放标准（Open Standard）

我们把 Agent Skills 作为一种 **开放标准** 发布。  
类似 MCP，我们认为 Skill 应该对不同工具和平台是可移植的 —— 同一个 Skill 应该能在 Claude 以及其他 AI 平台上工作。当然，有些 Skill 会专门针对某个平台的能力做优化，作者可以在 `compatibility` 字段中注明这一点。  
我们也在和生态伙伴一起迭代该标准，并已经看到一些早期采用者。

---

### 通过 API 使用 Skill

如果你要构建应用、Agent 或自动化工作流，并希望以编程方式使用 Skill，那么可以通过 API 直接管理和调用 Skill。

**关键能力：**

- `/v1/skills` 接口：列出和管理 Skill  
- 在 Messages API 请求里通过 `container.skills` 指定要启用的 Skill  
- 通过 Claude Console 做版本管理  
- 可与 Claude Agent SDK 联合使用，构建自定义 Agent  

**何时用 API，何时用 Claude.ai / Claude Code？**

| 场景 | 推荐界面 |
|---|---|
| 终端用户直接与 Skill 交互 | Claude.ai / Claude Code |
| 开发阶段的手动测试与迭代 | Claude.ai / Claude Code |
| 一次性的个人工作流 | Claude.ai / Claude Code |
| 程序化地在应用中使用 Skill | API |
| 规模化的生产部署 | API |
| 自动化流水线与 Agent 系统 | API |

*注意：在 API 中使用 Skill 需要启用「Code Execution Tool」测试版，它提供 Skill 运行所需的安全环境。*

详细实现可参考：

- Skills API Quickstart  
- Create Custom skills  
- Skills in the Agent SDK  

---

### 目前推荐的分发方式

当前的推荐做法是：

1. 把 Skill 放在一个 GitHub 公共仓库中  
2. 用清晰的 README（面向人类读者）介绍安装方式和使用示例  
3. 在 MCP 的官方文档中添加一个章节，链接到该 Skill，并说明 MCP + Skill 搭配使用的价值  

#### 1. 在 GitHub 托管

- 开源 Skill 使用公共仓库  
- README 中写清安装方式  
- 加上示例与截图  

#### 2. 在 MCP 仓库文档中说明

- 在 MCP 文档中链接相关 Skill  
- 解释二者结合的价值  
- 提供一个快速上手指南  

#### 3. 编写安装指南示例

```markdown
# Installing the [Your Service] skill

1. Download the skill:
   - Clone repo: `git clone https://github.com/yourcompany/skills`
   - Or download ZIP from Releases

2. Install in Claude:
   - Open Claude.ai > Settings > Skills
   - Click "Upload skill"
   - Select the skill folder (zipped)

3. Enable the skill:
   - Toggle on the [Your Service] skill
   - Ensure your MCP server is connected

4. Test:
   - Ask Claude: "Set up a new project in [Your Service]"
```

---

### 如何定位和描述你的 Skill

Skill 的对外描述决定了用户是否能理解其价值、愿不愿意试用。在 README、文档和营销材料中，建议遵循这些原则：

**聚焦「结果 / 价值」，而不是实现细节：**

✅ **好的描述：**

> 「ProjectHub Skill 能让团队在数秒内创建完备的项目工作空间 —— 包括页面、数据库和模板 —— 而不是花 30 分钟手动搭建。」

❌ **不好的描述：**

> 「ProjectHub Skill 是一个包含 YAML frontmatter 和 Markdown 指令的文件夹，会调用我们的 MCP 工具。」

**突出 MCP + Skill 整体故事：**

> 「我们的 MCP server 让 Claude 能访问你的 Linear 项目；我们的 Skill 则教会 Claude 如何按照你团队的冲刺规划方法来使用 Linear。两者结合，即是 AI 驱动的项目管理方案。」

---

## 第 5 章 — 模式与故障排查（Patterns and Troubleshooting）

本章的模式来源于早期使用者与内部团队构建的大量 Skill，它们是我们观察到「经常有效」的方式，而非必须照抄的模板。

---

### 选方案前：问题优先 vs 工具优先

可以把场景想象成逛五金店：

- 有人带着**问题**去（「我要修一个厨房柜门」），店员根据问题推荐合适的工具。  
- 有人先选中一个**工具**（比如新电钻），再问「可以用它解决哪些问题？」  

Skill 也是类似：

- **问题优先（Problem-first）：**  
  「我想搭一个项目工作空间」→ Skill 负责编排合适的 MCP 调用顺序。用户只描述目标，工具细节交给 Skill。
- **工具优先（Tool-first）：**  
  「我已经连接了 Notion MCP」→ Skill 负责教 Claude 如何用 Notion 做最好的实践工作流。用户已经有能力，Skill 提供「经验」。

大多数 Skill 会稍微偏向其中一种；搞清楚自己属于哪种，有助于选对下面的模式。

---

### 模式 1：顺序工作流编排（Sequential Workflow Orchestration）

**适用场景：** 用户需要多步骤、且步骤顺序固定的流程。

```markdown
# Workflow: Onboard New Customer

## Step 1: Create Account
Call MCP tool: `create_customer`
Parameters: name, email, company

## Step 2: Setup Payment
Call MCP tool: `setup_payment_method`
Wait for: payment method verification

## Step 3: Create Subscription
Call MCP tool: `create_subscription`
Parameters: plan_id, customer_id (from Step 1)

## Step 4: Send Welcome Email
Call MCP tool: `send_email`
Template: welcome_email_template
```

**关键技巧：**

- 明确的步骤顺序  
- 步骤之间的依赖与数据传递  
- 每个阶段的校验  
- 失败时的回滚或补救说明  

---

### 模式 2：多 MCP 协调（Multi-MCP Coordination）

**适用场景：** 工作流横跨多个服务 / MCP。

*示例：设计到开发的交接（Design-to-Development Handoff）*

```markdown
## Phase 1: Design Export (Figma MCP)
1. Export design assets from Figma
2. Generate design specifications
3. Create asset manifest

## Phase 2: Asset Storage (Drive MCP)
1. Create project folder in Drive
2. Upload all assets
3. Generate shareable links

## Phase 3: Task Creation (Linear MCP)
1. Create development tasks
2. Attach asset links to tasks
3. Assign to engineering team

## Phase 4: Notification (Slack MCP)
1. Post handoff summary to #engineering
2. Include asset links and task references
```

**关键技巧：**

- 分阶段组织（Phase）  
- 在不同 MCP 间传递数据  
- 每阶段前的预校验  
- 统一的错误处理策略  

---

### 模式 3：迭代式优化（Iterative Refinement）

**适用场景：** 输出质量可以通过多轮迭代显著提升。

*示例：报告生成*

```markdown
# Iterative Report Creation

## Initial Draft
1. Fetch data via MCP
2. Generate first draft report
3. Save to temporary file

## Quality Check
1. Run validation script: `scripts/check_report.py`
2. Identify issues:
   - Missing sections
   - Inconsistent formatting
   - Data validation errors

## Refinement Loop
1. Address each identified issue
2. Regenerate affected sections
3. Re-validate
4. Repeat until quality threshold met

## Finalization
1. Apply final formatting
2. Generate summary
3. Save final version
```

**关键技巧：**

- 明确的质量标准  
- 清晰的「迭代循环」结构  
- 借助脚本做客观校验  
- 知道何时停止迭代（避免无限改稿）  

---

### 模式 4：基于上下文的工具选择（Context-aware Tool Selection）

**适用场景：** 同一目标可以用多种工具完成，需要根据具体情况二选一 / 多选一。

*示例：智能文件存储*

```markdown
# Smart File Storage

## Decision Tree
1. Check file type and size
2. Determine best storage location:
   - Large files (>10MB): Use cloud storage MCP
   - Collaborative docs: Use Notion/Docs MCP
   - Code files: Use GitHub MCP
   - Temporary files: Use local storage

## Execute Storage
Based on decision:
- Call appropriate MCP tool
- Apply service-specific metadata
- Generate access link

## Provide Context to User
Explain why that storage was chosen
```

**关键技巧：**

- 清晰的决策标准  
- 合理的回退方案（fallback）  
- 向用户透明解释决策原因  

---

### 模式 5：领域特化智能（Domain-specific Intelligence）

**适用场景：** Skill 需要提供超出「工具访问」本身的专业知识。

*示例：支付合规（Financial Compliance）*

```markdown
# Payment Processing with Compliance

## Before Processing (Compliance Check)
1. Fetch transaction details via MCP
2. Apply compliance rules:
   - Check sanctions lists
   - Verify jurisdiction allowances
   - Assess risk level
3. Document compliance decision

## Processing
IF compliance passed:
- Call payment processing MCP tool
- Apply appropriate fraud checks
- Process transaction
ELSE:
- Flag for review
- Create compliance case

## Audit Trail
- Log all compliance checks
- Record processing decisions
- Generate audit report
```

**关键技巧：**

- 把领域规则显式编码进逻辑  
- 合规检查先于实际动作  
- 记录完整审计日志  
- 确保有明确的治理与复核路径  

---

### 故障排查（Troubleshooting）

#### Skill 无法上传

**错误：** "Could not find SKILL.md in uploaded folder"

**原因：** 主文件名不是精确的 `SKILL.md`。

**解决方案：**

- 把文件名改为 `SKILL.md`（大小写敏感）  
- 在命令行用 `ls -la` 确认  

---

**错误：** "Invalid frontmatter"

**原因：** YAML 格式错误。

**常见错误示例：**

```yaml
# 错：缺少分隔符
name: my-skill
description: Does things

# 错：引号未闭合
name: my-skill
description: "Does things

# 对：有 --- 分隔
---
name: my-skill
description: Does things
---
```

---

**错误：** "Invalid skill name"

**原因：** 名称中包含空格或大写字母。

```yaml
# 错误示例
name: My Cool Skill

# 正确示例
name: my-cool-skill
```

---

#### Skill 不会自动触发

**症状：** 无论如何都不会自动加载该 Skill。

**修复思路：** 重写 `description` 字段，参考前文「The Description Field」中的好坏示例。

**快速检查清单：**

- 是否过于泛泛？（如 "Helps with projects" 这类描述基本无用）  
- 是否包含用户真实会说的触发短语？  
- 若与某类文件相关，是否在描述中提到？  

**调试技巧：**

> 在对话中问 Claude：「When would you use the [skill name] skill?」  
> Claude 会把当前解析到的 description 说出来，根据缺失点进行修改。

---

#### Skill 触发频率过高

**症状：** 在与任务无关的场景中也频繁加载。

**解决方案：**

1. 添加反触发说明（negative triggers）：

```yaml
description: Advanced data analysis for CSV files. Use for statistical modeling,
  regression, clustering. Do NOT use for simple data exploration (use data-viz
  skill instead).
```

2. 提高描述精度：

```yaml
# 过于宽泛
description: Processes documents

# 更具体的版本
description: Processes PDF legal documents for contract review
```

3. 明确界定范围：

```yaml
description: PayFlow payment processing for e-commerce. Use specifically for
  online payment workflows, not for general financial queries.
```

---

#### MCP 连接问题

**症状：** Skill 被加载了，但 MCP 调用失败。

**检查清单：**

1. **确认 MCP server 已连接**
   - Claude.ai：Settings > Extensions > [Your Service]  
   - 状态应显示为「Connected」  

2. **检查认证配置**
   - API Key 是否仍然有效  
   - 权限 / Scope 是否足够  
   - OAuth Token 是否过期  

3. **单独测试 MCP 是否正常**
   - 不借助 Skill，直接让 Claude 调 MCP：  
     "Use [Service] MCP to fetch my projects"  
   - 若也失败，则是 MCP 本身的问题  

4. **检查工具名是否正确**
   - Skill 中引用的 MCP 工具名与文档是否一致  
   - 注意大小写敏感  

---

#### 指令没有被很好遵守

**症状：** Skill 被触发，但 Claude 没按 `SKILL.md` 里的说明做。

**常见原因：**

1. **指令太啰嗦 / 太长**
   - 保持简洁  
   - 使用项目符号和编号列表  
   - 把长篇参考文档拆到 `references/`  

2. **关键信息埋得太深**
   - 把最重要的规则放在顶部  
   - 使用 `## Important` / `## Critical` 等醒目标题  
   - 必要时适当重复关键点  

3. **语言含糊不清**

```markdown
# 不好
Make sure to validate things properly

# 较好
CRITICAL: Before calling create_project, verify:
- Project name is non-empty
- At least one team member assigned
- Start date is not in the past
```

**进阶技巧：**  
对于至关重要的检查，优先考虑用脚本实现（例如 Python 校验脚本），而不是仅依赖自然语言说明。代码是确定性的，语言解释则不然。可以参考 Office 相关 Skill 的做法。

4. **模型「偷懒」现象**

```markdown
# Performance Notes
- Take your time to do this thoroughly
- Quality is more important than speed
- Do not skip validation steps
```

*注意：把这些写在**用户提示词**里，比写在 `SKILL.md` 里通常更有效。*

---

#### 大上下文问题（Large Context Issues）

**症状：** 使用 Skill 时感觉变慢，或输出质量下降。

**可能原因：**

- `SKILL.md` 过大  
- 同时启用的 Skill 数量过多  
- 没有好好利用渐进式暴露，一次性载入了过多内容  

**解决方案：**

1. **优化 `SKILL.md` 体积**
   - 把详细说明移到 `references/`  
   - 通过链接引用而非内嵌大段内容  
   - 尽量让 `SKILL.md` 控制在 ~5,000 字以内  

2. **减少一次性启用的 Skill 数量**
   - 如果同时启用了 20–50 个以上的 Skill，评估是否有必要  
   - 推荐根据场景按需启用  
   - 考虑做成按领域组合的「Skill Pack」  

---

## 第 6 章 — 资源与参考（Resources and References）

如果你是第一次构建 Skill，建议先看「最佳实践指南」，再按需查阅 API 文档。

### 官方文档

**Anthropic 相关文档：**

- Best Practices Guide（Skill 最佳实践指南）  
- Skills Documentation（Skill 官方文档）  
- API Reference（API 参考）  
- MCP Documentation（MCP 文档）  

**博客文章：**

- Introducing Agent Skills  
- Engineering Blog: Equipping Agents for the Real World  
- Skills Explained  
- How to Create Skills for Claude  
- Building Skills for Claude Code  
- Improving Frontend Design through Skills  

### 示例 Skill

**公开 Skill 仓库：**

- GitHub: `anthropics/skills`  
- 包含由 Anthropic 构建、可供你定制的 Skill  

### 工具与辅助

**`skill-creator` Skill：**

- 已集成在 Claude.ai，也可用于 Claude Code  
- 能从自然语言描述生成 Skill 草稿  
- 能审阅现有 Skill，并给出改进建议  
- 调用示例："Help me build a skill using skill-creator"  

**Skill 评估：**

- 可以让 `skill-creator` 审查你的 Skill  
- 示例提示语："Review this skill and suggest improvements"  

### 支持渠道

**技术问题：**

- 可以在 Claude Developers Discord 社区频道提问  

**Bug 报告：**

- 在 GitHub 仓库 `anthropics/skills` 提 Issue  
- 请附带：Skill 名称、错误信息、复现步骤等  

---

## 附录 A：快速检查清单（Quick Checklist）

在上传前后可以用这份清单自查。  
如果你想更快开始，可以先用 `skill-creator` 生成初稿，再用本清单逐项核对。

### 开始之前

- [ ] 已确定 2–3 个具体用例  
- [ ] 已识别需要的工具（内置或 MCP）  
- [ ] 已浏览本指南和示例 Skill  
- [ ] 已规划好 Skill 目录结构  

### 开发过程中

- [ ] Skill 文件夹名为 kebab-case  
- [ ] 存在 `SKILL.md`（拼写精确）  
- [ ] YAML frontmatter 前后都有 `---` 分隔符  
- [ ] `name` 字段为 kebab-case，无空格无大写  
- [ ] `description` 同时说明「做什么」+「什么时候用」  
- [ ] 任意位置均未出现 `<` / `>`  
- [ ] 指令清晰、可执行  
- [ ] 已包含错误处理说明  
- [ ] 提供了至少一个完整示例  
- [ ] 所有引用的参考文件都能找到  

### 上传前

- [ ] 用典型任务测试了触发情况  
- [ ] 用同义改写测试触发情况  
- [ ] 确认不会在无关场景触发  
- [ ] 功能测试通过  
- [ ] （如有 MCP）确认工具集成正常  
- [ ] Skill 目录已压缩为 `.zip`  

### 上传后

- [ ] 在真实对话中做过试用  
- [ ] 观察触发不足 / 触发过多的迹象  
- [ ] 收集到少量用户反馈  
- [ ] 根据反馈迭代 `description` 与指令  
- [ ] 在 `metadata` 中更新版本号  

---

## 附录 B：YAML frontmatter 参考

### 必需字段

```yaml
---
name: skill-name-in-kebab-case
description: What it does and when to use it. Include specific trigger phrases.
---
```

### 包含所有可选字段的示例

```yaml
name: skill-name
description: [required description]
license: MIT                              # 可选：开源协议
allowed-tools: "Bash(python:*) Bash(npm:*) WebFetch"  # 可选：限制可用工具
metadata:                                 # 可选：自定义字段
  author: Company Name
  version: 1.0.0
  mcp-server: server-name
  category: productivity
  tags: [project-management, automation]
  documentation: https://example.com/docs
  support: support@example.com
```

### 安全注意事项

**允许：**

- 标准 YAML 类型（字符串、数字、布尔、列表、对象）  
- 任意自定义 `metadata` 字段  
- 最长 1024 字符的描述文本  

**禁止：**

- XML 尖括号 `< >`（安全原因）  
- 在 YAML 中做代码执行（解析器使用安全模式）  
- Skill 名包含「claude」或「anthropic」前缀（保留字）  

---

## 附录 C：完整 Skill 示例

要查看与本指南模式一一对应的、可投入生产的 Skill 示例，可以参考：

- **Document Skills** —— PDF、DOCX、PPTX、XLSX 等文档创建  
- **Example Skills** —— 多种典型工作流模式  
- **Partner Skills Directory** —— 来自 Asana、Atlassian、Canva、Figma、Sentry、Zapier 等伙伴的 Skill  

这些仓库会持续更新，且包含本指南未完全展开的附加示例。  
你可以直接克隆、按自己用例修改，并把它们当作模板使用。

---

*claude.ai（本指南中文整理版基于原始英文文档翻译与润色，仅供学习参考）*

