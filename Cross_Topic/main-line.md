## Main Line v2

### 1. Taxonomy Problem

当前主线首先是一个 **taxonomy-grounded problem**，而不是直接跳到方法。

不是所有 GUI “skill” 都值得存成 memory。强 VLM/LLM 已经具备不少通用 GUI 先验，例如识别按钮、输入框、保存/返回等。真正缺的，是那些只有通过交互才能获得、且能在后续任务中复用的 **experience-dependent procedural knowledge**。

因此 taxonomy 层要先回答三件事：

- **What**: 哪些经验对象值得积累？
  - 重点不是 generic GUI prior，而是 `Skills / World / Episodes / User` 中真正来源于交互经验的部分
- **When**: 这些经验是在何时写入？
  - 当前主线关注的不是 `pre-task` 和 `in-task` 本身，而是 `post-task -> cross-task` 的连接
- **How**: 这些经验如何复用？
  - 必须拆成两层：
  - `Match Operator`: 精确匹配 / 相似性检索 / 规则泛化
  - `Application Carrier`: 上下文注入 / 外部工具调用 / 策略约束 / 记忆改写

这一步的结论是：

- 现有 GUI 系统在 `post-task / Skills / 相似性检索 × 上下文注入` 上已有弱占位（MAGNET）
- 但在 `post-task / Skills / 规则泛化`、`cross-task / Skills / 相似性检索或规则泛化`、以及 `记忆改写` 这个 carrier 上仍基本空白

所以主问题不是“GUI agent 有没有 memory”，而是：

> **在 taxonomy 上，GUI agent 缺少的是一种能把 post-task experience 写成 cross-task reusable rule 的 procedural memory。**

### 2. Method Problem

在 taxonomy 结论确定后，方法问题才被正式定义为：

> **如何把交互中获得的、超出基础模型先验的程序性经验，表示成可检索、可更新、可复用的 memory，并在后续任务中稳定发挥作用？**

对应的方法对象不是 generic skill，而是 **experience-delta procedural memory**。

这种 memory 不存：

- 搜索按钮通常长什么样
- 保存按钮一般在右上角
- 弹窗通常需要先关闭

这些更像模型先验。

它应该存的是：

- 哪类页面的搜索入口经常藏在二级菜单 / profile / overflow menu
- 哪类表单只有先填字段 A，字段 B 才会激活
- 哪类“保存失败”通常不是点击失败，而是缺少隐藏前置条件
- 哪类返回操作会丢失输入状态，应优先局部提交
- 哪类弹窗关闭后会重置焦点，需要重新 grounding

因此一个 memory unit 不应是裸动作，而应包含：

- **Context / Trigger**: 在什么界面状态、任务意图或失败模式下触发
- **Procedure / Policy**: 推荐的局部操作策略
- **Constraint / Preconditions**: 必须满足的前置条件
- **Failure Signal**: 什么现象说明旧策略失效
- **Revision Rule**: 失败后如何改写这条记忆
- **Scope**: 适用范围是单 app、app family、还是更广

主方法框架收敛成四个模块：

1. **经验筛选**
   - 只保留 base model 首次不稳定且对成功率影响大的交互片段
2. **程序性抽象**
   - 把成功/失败轨迹里的局部流程抽象成带条件的 procedural rule，而不是整段 workflow 原样缓存
3. **检索与施加**
   - 用 `Match Operator × Application Carrier` 的两层结构检索并施加经验
4. **失败驱动写回**
   - 失败后不只重试，而是对 memory 执行 edit / split / downweight / rewrite

也就是说，主线本质上是 **A-1（程序性记忆） + A-4（失败驱动写回）** 的组合。

### 3. Evaluation Problem

最后，评测问题不是“overall success rate 有没有涨”，而是：

> **如何证明这套 memory 学到的不是模型本来就会的 GUI 常识，而是真正可复用、可迁移、可修正的经验差分知识？**

评测必须回答四个判别性问题：

1. **首次不会，第二次会**
   - repeated exposure 后是否显著提升
2. **不是通用常识，而是经验增益**
   - zero-shot 强模型本来就稳做对的简单技能，不应构成主要增益
3. **不是死记硬背，而是可迁移**
   - 至少要证明同 app 跨任务复用；更好则证明 app-family 内部分迁移
4. **不是静态 cache，而是能被失败修正**
   - failure write-back 后，是否优于 success-only memory

因此最小实验包至少需要：

- `no memory`
- `raw trajectory retrieval`
- `success-only memory`
- `failure-aware memory update`
- `coarse workflow memory`
- `fine-grained delta procedural memory`

并围绕三层迁移边界展开：

1. 同任务重复执行
2. 同 app 跨任务复用
3. 同 app-family 部分迁移

开放跨 app 泛化可以作为 bonus，而不应成为主线成立的前提。

### Condensed Paper Statement

> Current GUI agents rely either on generic model priors or app-bound workflow hints. We argue that the missing capability is not generic GUI skill, but reusable experience-dependent procedural knowledge: localized strategies, constraints, and repair rules that arise only through interaction. We therefore formulate the problem in three stages: taxonomy identifies the missing `post-task -> cross-task` procedural memory slots; method instantiates them as experience-delta procedural memory with failure-driven write-back; evaluation tests whether the learned memory goes beyond base-model priors and supports repeated-task and near-domain transfer.

### Sharp Objections

1. **这些“程序性记忆”会不会只是 prompt engineering 版经验提示，而不是真正的 memory？**
2. **所谓经验差分知识，真的超出了基础模型先验吗？还是只是把模型偶尔做错的常识重新编码？**
3. **如果 skill 既不能跨 app，也不能跨 app-family，那它和 task cache / workflow memo 的本质差别是什么？**
4. **失败写回真的在改进程序规则，还是只是把错误案例做成 case-based retrieval？**
5. **为什么要做 external procedural memory，而不是继续靠更强 backbone、更长上下文或更强 training recipe 解决？**
