# Meeting Brief

## 一句话问题

我的核心问题不是泛泛地讨论 GUI agent 有没有 memory，  
而是：**GUI / web agent 能不能把交互中得到的 procedural memory 存下来，并且在失败后修正它？**

## 核心主张

- 我想做的是一个 **memory-layer contribution**
- 不是 broad agent improvement
- 不是 training-side self-evolution
- 不是 simple workflow cache
- 不是单纯“把历史轨迹塞进更长的 prompt”

## 方法核心

核心 memory object 是：**EDPM**

每个 memory unit 至少包含：

- `trigger`
- `procedure`
- `constraints / preconditions`
- `failure signal`
- `transfer scope`

一句话解释：
不是存 raw trajectory，  
而是存一个 **可复用、可修订的局部程序性规则**。

## 系统流程

可以先理解成四个模块：

1. `candidate mining`
  从 post-task trajectory 里找 reusable local pattern
2. `rule abstraction`
  把 pattern 压成 EDPM
3. `retrieval-application separation`
  分开 retrieval 和 application
4. `failure-aware write-back`
  failure 后做 edit / split / downweight / rewrite

## 实验真正想回答的问题

最核心不是 “does memory help?”

而是：

**在 cross-task reuse 条件下，可修订 procedural memory 能不能明显优于 raw retrieval 和 workflow memory？**

## 实验组

- `C0` no memory
- `C1` raw retrieval
- `C2` coarse workflow memory
- `C3` EDPM + success-only accumulation
- `C4` EDPM + failure-aware write-back
- `C5` EDPM + stronger policy constraint

最关键的对比是：

- `C3 vs C1/C2`: EDPM 是否比 raw trace / workflow 更好
- `C4 vs C3`: failure-aware revision 是否真的有额外价值

## 迁移层级

- `L1` repeated-task reuse
- `L2` same-site / same-app cross-task reuse
- `L3` near-domain site-family transfer

我现在的判断：

- `L1` = sanity check
- `L2` = main result
- `L3` = stress test

## Benchmark 选择

当前第一选择：**WebArena**

原因是：

- grounded multi-step web tasks
- 比较容易构造 reuse / transfer settings
- 适合 first-stage validation

## 什么样的结果才算真有效

- 在 `L2` 上有 gain，而不只是 `L1`
- `C3 > C1, C2`
- `C4 > C3` on failure-first cases
- revised memory 能减少重复失败
- 结果不能被简单解释成 longer prompt

## 主要风险 / 坑点

### 研究层面的风险

- scope 可能过大
- novelty boundary 可能不够清楚
- contribution 可能变成 “什么都做一点”

### 方法层面的风险

- rule abstraction 太虚
- trigger / scope 不够准
- `L3` 上出现 negative transfer
- failure source 可能不是 memory，而是 perception 或 environment noise

### 工程实现层面的风险

- write-back loop 比 memory schema 难很多
- repeated runs for accumulation + revision 会很花时间
- experiment orchestration 复杂

### 算力与资源风险

- 如果每个 condition 都要多轮 interaction，cost 会很快上去
- ablation + repeated trials + transfer settings 会放大算力需求

## 问题

### 1. 研究边界

- 我现在把问题收敛到 procedural memory + failure-aware revision，这个 scope 是否已经足够窄？
- 这个方向最容易被审稿人质疑的点，会是 novelty、problem framing，还是 evaluation？
- 我的贡献更应该被定义成 memory representation、write-back mechanism，还是 evaluation protocol？

### 2. 方法形式

- 第一阶段是否应该只做 **inference-time memory**，先不碰 model training？
- 这个方向如果不做 training / fine-tuning，只做 retrieval + write-back，是否已经足够形成 paper-level contribution？
- EDPM 这个 abstraction level 是否合适，还是仍然太抽象、太像 verbal idea？
- application stage 是否先只做 prompt injection 更稳，还是应该一开始就做 stronger policy constraint？

### 3. 实验设计

- `L2` 是否应该作为 primary target，而不是 `L1` 或更开放的 `L3`？
- `WebArena` 是否适合作为第一阶段 benchmark，还是应该先做更小、更可控的 custom setting？
- baseline 里最不能少的是哪几个？`C0/C1/C2/C3/C4` 是否已经足够？
- 什么样的结果才足以说明这不是 replay / cache，而是真正的 memory gain？

### 4. 工程可行性

- 这个项目最难实现的部分会是什么：candidate mining、rule abstraction、还是 write-back？
- failure-aware revision 需要做到多复杂才有说服力？第一版只做 `edit/downweight` 是否太弱？
- 是否需要人工标注或人工筛选 memory unit，还是应该坚持 fully automatic pipeline？

### 5. 算力与资源

- 这个方向如果基于 WebArena 做多轮 accumulation 和 revision，compute budget 大概会不会过高？
- 第一阶段是否应该固定 backbone，只比较 memory mechanism，避免 training cost 和变量过多？
- 如果算力有限，最值得保留的实验应该是哪几个，哪些 ablation 可以先不做？

### 6. 最小可发表版本

- 如果要把这个方向压成一个最小 publishable unit，最小系统和最小实验包应该是什么？
- 是不是应该先证明 `C3 > C1/C2`，再把 `C4 > C3` 作为第二阶段扩展？

## 我现在的判断

我现在最想证明的是：

**GUI / web agents 需要的是可修订 procedural memory，而不只是更多 context、更强 replay 或更大的模型。**