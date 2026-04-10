# Round 1b Pairing / Artifact Audit

Date: 2026-04-11

这份文件用于记录 Round 1b 之后，对关键 smoke cases 的 `pairing / artifact` 审计结果。

固定写法：

1. `Observed effect`
2. `Pairing judgment`
3. `Artifact judgment`
4. `Most likely explanation`
5. `Implication for next round`

---

## Case: `wiki_dev_8896`

相关文件：

- [pairing_table_round1.csv](../../pilot/archive/pairing_table_round1.csv)
- [r1b_no_memory_wiki_dev_8896_relevant.md](../05_round1b_run/raw_outputs/r1b_no_memory_wiki_dev_8896_relevant.md)
- [r1b_episodic_trace_wiki_dev_8896_relevant.md](../05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_8896_relevant.md)
- [r1b_episodic_trace_wiki_dev_8896_irrelevant.md](../05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_8896_irrelevant.md)
- [r1b_cross_episode_consolidation_wiki_dev_8896_relevant.md](../05_round1b_run/raw_outputs/r1b_cross_episode_consolidation_wiki_dev_8896_relevant.md)
- [r1b_cross_episode_consolidation_wiki_dev_8896_irrelevant.md](../05_round1b_run/raw_outputs/r1b_cross_episode_consolidation_wiki_dev_8896_irrelevant.md)
- [artifacts/hp_bridge_set_01/episodic_trace.md](../../artifacts/hp_bridge_set_01/episodic_trace.md)
- [artifacts/hp_bridge_set_01/cross_episode_consolidation.md](../../artifacts/hp_bridge_set_01/cross_episode_consolidation.md)
- [artifacts/hp_comparison_set_01/episodic_trace.md](../../artifacts/hp_comparison_set_01/episodic_trace.md)
- [artifacts/hp_comparison_set_01/cross_episode_consolidation.md](../../artifacts/hp_comparison_set_01/cross_episode_consolidation.md)

### Observed effect

这个 case 在所有 6 个条件下都答对，因此它不提供 outcome-level gain。  
但它提供了当前最清晰的 process-level selectivity：

- `episodic_trace + relevant` 出现了 `explicit_use`
- `episodic_trace + irrelevant` 出现了 `explicit_reject`
- `cross_episode_consolidation` 两个 split 都答对，但都保持 `implicit_or_none`

也就是说，这个 case 的价值不在分数变化，而在于模型开始显式区分什么 memory 值得引用、什么 memory 应该拒绝。

### Pairing judgment

当前 pairing 基本成立。

- target `wiki_dev_8896` 是一个干净的 `comparison` case，问题核心是比较两个出生日期
- relevant source `hp_comparison_set_01` 与它在 reasoning structure 上明显匹配
- irrelevant source `hp_bridge_set_01` 在 cluster 层面也确实不匹配，因为它强调的是通过中间实体链找到属性，而不是双实体属性比较

因此，这个 case 上的 `relevant / irrelevant` 区分是可信的，不像某些 bridge cases 那样容易混淆。

### Artifact judgment

artifact 差异在这个 case 上也比较健康。

- `hp_comparison_set_01/episodic_trace.md` 明确包含 temporal comparison 的 episode，例如 “born first” 和 “newer/older” 这类 pattern
- `hp_bridge_set_01/episodic_trace.md` 更像两跳 entity chaining，不直接支持出生日期比较
- 两个 consolidation 都有较抽象的步骤，但 `comparison` consolidation 更接近当前任务结构

需要注意的是：`comparison` consolidation 并没有像 episodic trace 那样被显式引用，这说明更抽象的 artifact 不一定更容易被 verbalize。

### Most likely explanation

这个 case 最可能说明的是：

- 当前 scaffold 已经足以让模型在简单、干净的 comparison case 上做出“该用时用，不该用时拒绝”的显式判断
- observed distinction 更像真实的 task-structure sensitivity，而不是偶然的 token 扰动

但它还不能证明：

- explicit use 本身带来了 accuracy improvement

因为 no-memory baseline 本来就已经正确。

### Implication for next round

`wiki_dev_8896` 可以继续保留为 Round 1b / Round 2 的 process-level sanity check。

它最适合回答：

- 模型是否还会显式引用 relevant memory
- 模型是否还会显式拒绝 irrelevant memory

它不适合回答：

- 哪种 memory form 在 outcome 上更强

因此后续使用方式应当是：

- 把它作为 selectivity visibility case 保留
- 但不要把它当作 transfer gain 的核心证据

---

## Case: `wiki_dev_2639`

相关文件：

- [pairing_table_round1.csv](../../pilot/archive/pairing_table_round1.csv)
- [r1b_no_memory_wiki_dev_2639_relevant.md](../05_round1b_run/raw_outputs/r1b_no_memory_wiki_dev_2639_relevant.md)
- [r1b_no_memory_wiki_dev_2639_irrelevant.md](../05_round1b_run/raw_outputs/r1b_no_memory_wiki_dev_2639_irrelevant.md)
- [r1b_episodic_trace_wiki_dev_2639_relevant.md](../05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_2639_relevant.md)
- [r1b_episodic_trace_wiki_dev_2639_irrelevant.md](../05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_2639_irrelevant.md)
- [r1b_cross_episode_consolidation_wiki_dev_2639_relevant.md](../05_round1b_run/raw_outputs/r1b_cross_episode_consolidation_wiki_dev_2639_relevant.md)
- [r1b_cross_episode_consolidation_wiki_dev_2639_irrelevant.md](../05_round1b_run/raw_outputs/r1b_cross_episode_consolidation_wiki_dev_2639_irrelevant.md)
- [artifacts/hp_bridge_set_01/episodic_trace.md](../../artifacts/hp_bridge_set_01/episodic_trace.md)
- [artifacts/hp_bridge_set_01/cross_episode_consolidation.md](../../artifacts/hp_bridge_set_01/cross_episode_consolidation.md)
- [artifacts/hp_comparison_set_01/episodic_trace.md](../../artifacts/hp_comparison_set_01/episodic_trace.md)
- [artifacts/hp_comparison_set_01/cross_episode_consolidation.md](../../artifacts/hp_comparison_set_01/cross_episode_consolidation.md)

### Observed effect

这个 case 是当前最明显的 memory-induced degradation case。

- `no_memory` 在 relevant / irrelevant 两个 split 上都答对：`Henry Pelham`
- `episodic_trace` 在 relevant / irrelevant 两个 split 上都退化成：`Cannot be determined from the provided context`
- `cross_episode_consolidation` 在 relevant split 上同样退化
- 只有 `cross_episode_consolidation + irrelevant` 回到了 baseline 正确答案

也就是说，当前现象不是简单的 “relevant helps / irrelevant hurts”，而更像：

- 加入 memory 后，模型有时会从可回答状态退回到保守拒答
- 而这种退化主要出现在 bridge-like artifact 注入之后

### Pairing judgment

当前 pairing 在表面上是成立的，但它并不如 `wiki_dev_8896` 那样干净。

- target `wiki_dev_2639` 被标为 `bridge`
- relevant source `hp_bridge_set_01` 的 cluster label 与它一致
- pairing note 也写的是 “same bridge pattern via intermediate relation chain”

问题在于：这个 target 虽然形式上是 relation chain，但它并不需要 source set 里那类典型的 `event -> venue -> attribute` 或 `song -> artist -> birth year` 桥接模式。  
它更像一种局部 kinship reasoning：

- Harriet → spouse (Thomas)
- Thomas → brother (Henry Pelham)

所以当前 pairing 的 label-level 判断虽然没错，但 **cluster matching 过粗**。  
`bridge` 这个大类内部，其实已经混入了不同子型：

- entity-to-attribute bridge
- kinship / relation-chain bridge

这意味着 relevant pairing 在这个 case 上不够精确。

### Artifact judgment

artifact 更像是当前退化的主要来源。

- `hp_bridge_set_01/episodic_trace.md` 和 `cross_episode_consolidation.md` 都在强调：
  - 先找中间实体
  - 再到第二个实体 profile 里取属性
  - 如果目标属性不在主句中，要继续跳转

这种模式对 `wiki_dev_2639` 并不是完全无关，但也不完全贴合。  
因为这个问题的关键其实不是继续跨 profile 查属性，而是：

- 识别 “husband's brother” 就是 “brother-in-law”

换句话说：

- relevant artifact 不是完全错误
- 但它把模型推向了一种“继续找缺失信息”的姿态
- 最后更容易导向 `Cannot be determined...`

反过来看，irrelevant `comparison` consolidation 反而更短、更抽象，对这个 case 的干扰更小，所以模型回到了 baseline 正确路径。

### Most likely explanation

这个 case 最可能说明的不是：

- irrelevant memory 更好

而是：

- 当前 `bridge` artifact 对某些 relation-chain 问题施加了过强的 procedural bias
- 这种 bias 把模型从本来已经足够的局部推理，带向了“不足以回答”的保守拒答

因此，这条现象更应解释为：

- **artifact-induced derailment**

而不是：

- selective transfer 失败本身

### Implication for next round

`wiki_dev_2639` 的意义在于提醒：

- 当前 `bridge` cluster 太粗
- `bridge` artifact 里混杂了不止一种可迁移模式

对下一轮的含义是：

1. 在 full rerun 之前，应该至少把 bridge 内部再做一次子型检查  
   尤其区分：
   - entity-to-attribute bridge
   - kinship / relation-chain bridge

2. 当前 `hp_bridge_set_01` 不应被直接视为 “所有 bridge target 都该 relevant”  
   在某些 target 上，它更可能制造 procedural interference。

3. 这个 case 应继续保留，因为它是目前最强的 evidence，说明：
   - pairing label 一致，不等于 artifact 真正适用

---

## Case: `wiki_dev_7019`

相关文件：

- [pairing_table_round1.csv](../../pilot/archive/pairing_table_round1.csv)
- [r1b_no_memory_wiki_dev_7019_relevant.md](../05_round1b_run/raw_outputs/r1b_no_memory_wiki_dev_7019_relevant.md)
- [r1b_no_memory_wiki_dev_7019_irrelevant.md](../05_round1b_run/raw_outputs/r1b_no_memory_wiki_dev_7019_irrelevant.md)
- [r1b_episodic_trace_wiki_dev_7019_relevant.md](../05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_7019_relevant.md)
- [r1b_episodic_trace_wiki_dev_7019_irrelevant.md](../05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_7019_irrelevant.md)
- [r1b_cross_episode_consolidation_wiki_dev_7019_relevant.md](../05_round1b_run/raw_outputs/r1b_cross_episode_consolidation_wiki_dev_7019_relevant.md)
- [r1b_cross_episode_consolidation_wiki_dev_7019_irrelevant.md](../05_round1b_run/raw_outputs/r1b_cross_episode_consolidation_wiki_dev_7019_irrelevant.md)
- [artifacts/hp_bridge_set_01/episodic_trace.md](../../artifacts/hp_bridge_set_01/episodic_trace.md)
- [artifacts/hp_bridge_set_01/cross_episode_consolidation.md](../../artifacts/hp_bridge_set_01/cross_episode_consolidation.md)
- [artifacts/hp_comparison_set_01/episodic_trace.md](../../artifacts/hp_comparison_set_01/episodic_trace.md)
- [artifacts/hp_comparison_set_01/cross_episode_consolidation.md](../../artifacts/hp_comparison_set_01/cross_episode_consolidation.md)

### Observed effect

这个 case 的 baseline 行为是“答得过长，但部分包含 gold”。

- `no_memory` 两个 split 都输出过长答案：`Sanremo Music Festival 2015 and Eurovision Song Contest 2015 (televoting)`，F1 只有 0.5
- relevant `episodic_trace` 和 relevant `consolidation` 都没有修好这个问题
- irrelevant `episodic_trace` 反而进一步偏到 `First place in the televoting...`
- 只有 irrelevant `cross_episode_consolidation` 把最终答案收束成：`Sanremo Music Festival`

因此，当前 improvement 是存在的，但它不是典型的 “relevant helps” pattern，而是：

- 只有一个 irrelevant consolidation case 精准命中了 gold phrasing

### Pairing judgment

当前 pairing 在标签层面是合理的，但解释力有限。

- target 被标为 `bridge`
- relevant source `hp_bridge_set_01` 在 cluster 上一致
- irrelevant source `hp_comparison_set_01` 在 cluster 上不一致

问题在于，这个 target 虽然可以被视为 “song performer -> performer award” 的 bridge，但实际难点并不只是找中间实体，而是：

- 从多个候选奖项 / event mentions 中选出回答层级最合适的那一个

也就是说，这个 case 同时带有：

- bridge retrieval
- answer granularity selection

所以 relevant / irrelevant 的 label 判断没有错，但它不能完全解释为什么 `comparison` consolidation 会在这里更好。

### Artifact judgment

当前 observed improvement 更像是 artifact wording 对答案粒度的影响，而不是结构迁移。

- `hp_bridge_set_01` 的 artifacts 更强调两跳 entity chaining 和属性检索
- 但这个问题在找到 `Il Volo` 与其奖项相关信息之后，真正的难点变成了：
  - 该输出 “festival”
  - 还是输出 “contest placement / televoting result”

`hp_comparison_set_01/cross_episode_consolidation.md` 中有较强的：

- parse entities
- retrieve attributes
- normalize data
- verify the exact scope of the question

这类 wording 更可能把模型推向“压缩到一个更核心、更短的答案表达”，从而偶然更贴近 gold。

因此，这条 improvement 更像：

- **answer compression / answer granularity correction**

而不是：

- 真的把 comparison strategy 迁移到了 bridge task

### Most likely explanation

这个 case 最可能说明的是：

- irrelevant consolidation 没有真正提供更相关的 task structure
- 但它给了模型一种更强的“收短答案、只保留核心 attribute”偏置

所以最终从：

- `Sanremo Music Festival 2015 and Eurovision Song Contest 2015 (televoting)`

收束成了：

- `Sanremo Music Festival`

这是一个真实 improvement，但它更接近 **output-layer correction**，而不是更强的 transfer evidence。

### Implication for next round

`wiki_dev_7019` 不适合作为 selective transfer 的核心证据。

它更适合被用来提醒：

1. 当前 scoring 很容易把 “答案粒度更贴近 gold” 与 “真正的 reasoning improvement” 混在一起  
2. artifact wording 可能会影响回答层级，而不仅仅影响推理路径  
3. 在 full rerun 前，最好加入一类更细的 process metric：
   - memory 是否改变了 answer type / answer granularity

因此后续应当：

- 保留这个 case 作为 answer-format sensitive example
- 但不要把它当作 “irrelevant memory better than relevant memory” 的直接证据

---

## Case: `wiki_dev_0092`

相关文件：

- [round1_target_audit.md](./round1_target_audit.md)
- [pairing_table_round1.csv](../../pilot/archive/pairing_table_round1.csv)
- [r1b_no_memory_wiki_dev_0092_relevant.md](../05_round1b_run/raw_outputs/r1b_no_memory_wiki_dev_0092_relevant.md)
- [r1b_no_memory_wiki_dev_0092_irrelevant.md](../05_round1b_run/raw_outputs/r1b_no_memory_wiki_dev_0092_irrelevant.md)
- [r1b_episodic_trace_wiki_dev_0092_relevant.md](../05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_0092_relevant.md)
- [r1b_episodic_trace_wiki_dev_0092_irrelevant.md](../05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_0092_irrelevant.md)
- [r1b_cross_episode_consolidation_wiki_dev_0092_relevant.md](../05_round1b_run/raw_outputs/r1b_cross_episode_consolidation_wiki_dev_0092_relevant.md)
- [r1b_cross_episode_consolidation_wiki_dev_0092_irrelevant.md](../05_round1b_run/raw_outputs/r1b_cross_episode_consolidation_wiki_dev_0092_irrelevant.md)

### Observed effect

这个 case 在所有 6 个条件下都稳定输出：`Alexandria, Egypt`。  
即使 memory interaction 有所不同：

- `episodic_trace + irrelevant` 出现了 `explicit_use`
- `cross_episode_consolidation + irrelevant` 出现了 `explicit_reject`

最终答案仍然完全不变。

所以这条 case 的关键信号不是 transfer，而是：

- 模型会在 reasoning 里 verbalize 对 memory 的 use/reject
- 但最终仍然跟随 context 中最强的字面证据

### Pairing judgment

当前 pairing 在 label 层面没有明显问题。

- target 被标为 `bridge`
- relevant source `hp_bridge_set_01` 在结构上也确实更接近 “film -> director -> birthplace” 这类两跳模式
- irrelevant source `hp_comparison_set_01` 与其不匹配

但这条 case 的 pairing 好坏其实不再重要，因为 benchmark 本身已经不干净。  
即使 relevant / irrelevant 判得再好，这个 case 也不适合拿来支撑 transfer 结论。

### Artifact judgment

artifact 在这条 case 上并没有显著改变最终 reasoning path。

- relevant bridge artifacts 没有把模型从 `Alexandria, Egypt` 拉开
- irrelevant comparison artifacts 也没有把模型拉偏到别的方向
- 唯一变化只体现在 reasoning 文本里对 memory 的 verbal stance 上

这说明：

- 对当前 case 来说，artifact 的作用主要停留在 process-level wording
- 没有形成真正的 answer-level effect

### Most likely explanation

这条 case 最可能说明的是：

- 当前 benchmark / gold 自身存在 ambiguity
- 模型按 context strongest evidence 给出 `Alexandria, Egypt` 是稳定且可预期的
- memory 在这里最多只能改变 reasoning 中的“姿态表达”，很难改变最终答案

因此，这条 case 不应再被解释为：

- memory helped / harmed
- relevant / irrelevant worked / failed

它更准确的角色是：

- **audit case**

### Implication for next round

`wiki_dev_0092` 应继续保留，但用途必须固定：

1. 只用来观察 memory 的 `use / reject / ignore` 是否改变了 reasoning 文字  
2. 不纳入默认 aggregate evidence  
3. 不把它的 outcome 用来支持任何 selective transfer 结论

这条 case 的存在价值在于提醒：

- 即使 process metric 已经变好，benchmark ambiguity 仍然会限制我们能得出的结论

---

## Case: `wiki_dev_6083`

相关文件：

- [round1_target_audit.md](./round1_target_audit.md)
- [pairing_table_round1.csv](../../pilot/archive/pairing_table_round1.csv)
- [r1b_no_memory_wiki_dev_6083_relevant.md](../05_round1b_run/raw_outputs/r1b_no_memory_wiki_dev_6083_relevant.md)
- [r1b_no_memory_wiki_dev_6083_irrelevant.md](../05_round1b_run/raw_outputs/r1b_no_memory_wiki_dev_6083_irrelevant.md)
- [r1b_episodic_trace_wiki_dev_6083_relevant.md](../05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_6083_relevant.md)
- [r1b_episodic_trace_wiki_dev_6083_irrelevant.md](../05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_6083_irrelevant.md)
- [r1b_cross_episode_consolidation_wiki_dev_6083_relevant.md](../05_round1b_run/raw_outputs/r1b_cross_episode_consolidation_wiki_dev_6083_relevant.md)
- [r1b_cross_episode_consolidation_wiki_dev_6083_irrelevant.md](../05_round1b_run/raw_outputs/r1b_cross_episode_consolidation_wiki_dev_6083_irrelevant.md)

### Observed effect

这个 case 在所有 6 个条件下都稳定输出 `Spain`，gold 为 `Spanish`。

- `no_memory` 两个 split 都输出 `Spain`
- relevant / irrelevant `episodic_trace` 都输出 `Spain`
- relevant / irrelevant `cross_episode_consolidation` 也都输出 `Spain`

也就是说，这里既没有 transfer gain，也没有 memory-induced degradation。  
当前唯一稳定现象是：

- 所有条件都收敛到同一个 country form
- scoring 一直按 `Spain != Spanish` 记为失败

### Pairing judgment

当前 pairing 在结构层面没有明显问题。

- target `wiki_dev_6083` 被标为 `bridge`
- relevant source `hp_bridge_set_01` 与它在 “film -> director -> nationality / birthplace attribute” 这类两跳结构上是匹配的
- irrelevant source `hp_comparison_set_01` 也确实是 cluster mismatch

但这条 case 的关键不在 pairing。  
因为 relevant / irrelevant 再怎么区分，模型最终都没有沿不同方向分叉，而是统一落到 `Spain`。

所以这条 case 不适合拿来检验 pairing 是否精确；它更像一个被 scoring boundary 主导的 case。

### Artifact judgment

artifact 在这个 case 上几乎没有产生可见差异。

- relevant bridge artifacts 没有把答案推向更贴近 gold 的 demonym form
- irrelevant comparison artifacts 也没有把答案带偏到别的方向
- `memory_reference_type` 也始终是 `implicit_or_none`

这说明：

- 当前 artifacts 至少没有在这里制造额外干扰
- 但它们也没有提供足够强的 signal，去促使模型把国家名规范成国籍形容词

换句话说，这条 case 上看不出 pairing / artifact 的主要问题；更强的问题来自 evaluation 层。

### Most likely explanation

这条 case 最可能说明的是：

- 当前 benchmark / scoring 仍然存在 normalization gap
- 模型已经找到了正确国家，但没有输出 gold 期待的 demonym form
- 这类差异被当前 EM/F1 直接当成失败，掩盖了“内容基本正确但表述形态不同”的情况

因此，这里更接近：

- **scoring-boundary case**

而不是：

- memory helped / harmed
- relevant / irrelevant 成立或失效

### Implication for next round

`wiki_dev_6083` 应继续保留，但角色必须固定：

1. 作为 `country / demonym` normalization 的边界 case  
2. 不作为 selective transfer 的核心证据  
3. 在 aggregate 解读时应单独标记，或加入一层更宽松的 normalization 说明

这条 case 的作用是提醒：

- 即使 prompt scaffold 已经修好、reasoning 已经可见，evaluation noise 仍然会直接污染你对 memory effect 的判断

---

## Case: `wiki_dev_10727`

相关文件：

- [round1_target_audit.md](./round1_target_audit.md)
- [pairing_table_round1.csv](../../pilot/archive/pairing_table_round1.csv)
- [r1b_no_memory_wiki_dev_10727_relevant.md](../05_round1b_run/raw_outputs/r1b_no_memory_wiki_dev_10727_relevant.md)
- [r1b_no_memory_wiki_dev_10727_irrelevant.md](../05_round1b_run/raw_outputs/r1b_no_memory_wiki_dev_10727_irrelevant.md)
- [r1b_episodic_trace_wiki_dev_10727_relevant.md](../05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_10727_relevant.md)
- [r1b_episodic_trace_wiki_dev_10727_irrelevant.md](../05_round1b_run/raw_outputs/r1b_episodic_trace_wiki_dev_10727_irrelevant.md)
- [r1b_cross_episode_consolidation_wiki_dev_10727_relevant.md](../05_round1b_run/raw_outputs/r1b_cross_episode_consolidation_wiki_dev_10727_relevant.md)
- [r1b_cross_episode_consolidation_wiki_dev_10727_irrelevant.md](../05_round1b_run/raw_outputs/r1b_cross_episode_consolidation_wiki_dev_10727_irrelevant.md)

### Observed effect

这个 case 在所有 6 个条件下都稳定答对：`Au revoir les enfants`。

- `no_memory` 两个 split 都正确
- relevant / irrelevant `episodic_trace` 都正确
- relevant / irrelevant `cross_episode_consolidation` 也都正确

其中唯一稍微值得注意的变化是：

- `episodic_trace + irrelevant` 出现了 `explicit_use`

但即使如此，最终答案、推理主路径和得分都没有变化。

### Pairing judgment

当前 pairing 基本成立，而且比多数 bridge cases 更干净。

- target `wiki_dev_10727` 是一个明确的 `comparison` case，核心就是比较两部电影的上映时间
- relevant source `hp_comparison_set_01` 与它在结构上高度匹配
- irrelevant source `hp_bridge_set_01` 在 cluster 层面也确实不匹配

因此，这条 case 不存在明显的 pairing ambiguity。  
它的问题不在 relevant / irrelevant 划分，而在于任务本身太容易，memory 很难产生 outcome-level effect。

### Artifact judgment

artifact 在这条 case 上的主要作用，仍然停留在 reasoning wording 层。

- relevant comparison artifacts 并没有比 baseline 提供更强的结果优势
- irrelevant bridge episodic 虽然被模型显式提到，但模型自己也明确说当前题可以直接从 context 比较年份，不需要真正套用 bridge pattern

所以这条 case 更像在说明：

- 模型会 verbalize 一种“past experience is applicable in a loose sense”
- 但 verbalized use 不等于实际 outcome dependence

### Most likely explanation

这条 case 最可能说明的是：

- 当前 prompt scaffold 已经足以让模型在简单 comparison ceiling case 上稳定产出结构化 reasoning
- 但在这种本来就很容易、context 直接给出关键年份的任务里，memory 不太可能显著改变结果

因此，这里的 `explicit_use` 更像：

- **process-level decoration**

而不是：

- 真实的 transfer gain

### Implication for next round

`wiki_dev_10727` 应继续保留，但角色应当非常克制：

1. 作为 clean comparison ceiling case  
2. 用来检查：
   - 结构化输出是否稳定
   - `explicit_use` 是否只是 verbal decoration
3. 不作为 selective transfer 的核心证据

这条 case 的主要提醒是：

- 后续 process analysis 需要区分：
  - merely mentions memory
  - memory materially changes reasoning or answer
