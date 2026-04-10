# First HotpotQA Comparison Expansion Batch

这份文件只回答一个问题：

**第一批 `HotpotQA comparison` 扩池，具体应该怎么做？**

它是 [expand-hotpotqa-comparison-source-pool.md](./expand-hotpotqa-comparison-source-pool.md) 的执行版，不再讲原则，而是把第一批扩池拆成可直接照着做的动作。

## 1. 这一批要完成什么

第一批扩池的目标不是“把 comparison 一次补完”，而是：

- 新增一小批高命中率的 `HotpotQA comparison` 候选题
- 对这批题完成增量 taxonomy 标注
- 看 `HotpotQA comparison keep` 是否能从 2 提升到至少 5

当前起点是：

- 已有 `HotpotQA comparison keep = 2`
  - `hp_dev_0478`
  - `hp_dev_6149`

第一批的最低成功标准是：

- 新增至少 3 个 `comparison keep`

更稳的成功标准是：

- 新增 4 到 6 个 `comparison keep`

## 2. 这一批的固定前提

这一批开始前，不要改变下面这些前提：

- `source benchmark = HotpotQA`
- `target benchmark = 2WikiMultiHopQA`
- `N = 5`
- 现有 taxonomy 规则不变
- 现有 `comparison` 定义不变

如果你在这一步改了这些前提，那就不是“扩池”，而是在改整个实验设计。

## 3. 推荐批量大小

第一批固定做：

- **15 个候选题**

这个数字不是理论最优，而是当前最实用的折中：

- 太少：命中率不够，补不出 5 个 `keep`
- 太多：工作量突然膨胀

所以这一批就按：

- `15 raw candidates`

来执行。

## 4. 数据来源

这一批候选题只从：

- 当前使用的 `HotpotQA` 同一 split

里取。

如果当前 rehearsal 用的是 `HotpotQA dev`，那这一批也继续用：

- `HotpotQA dev`

不要：

- 混进 train
- 换别的 split
- 从 target benchmark 借题

## 5. 候选题怎么找

### 方法优先级

优先用：

- `HotpotQA raw type = comparison`

做预筛。

如果当前 notebook / 脚本能直接读取原始 `type` 字段，这就是第一优先方法。

### 不够时再用题面模式补

如果你从 `type = comparison` 里拿到的候选还不够，才补：

- `Which ... , A or B?`
- `What is the shared ...`
- `Was A or B ...`

但第一批默认优先只用 `type = comparison`。

## 6. 原始候选题的最小过滤

从 raw candidate list 进入正式标注前，只做下面三类过滤：

### 过滤 1：坏数据

去掉：

- 文本损坏
- 缺题目
- 缺答案
- 缺支撑信息

### 过滤 2：明显近重复

去掉和现有 `comparison keep` 或同一批候选几乎同模板的题：

- 同一类问句结构
- 同样的实体关系
- 一眼看上去只是轻微改写

### 过滤 3：表面像 comparison，实际不依赖显式比较

如果一题虽然题面带两个实体，但本质上不是比较主导，就不要进这一批。

目标不是“看起来像 comparison”，而是“高概率真的会被标成 comparison”。

## 7. 第一批执行步骤

### Step 1. 先产出 15 个 raw candidates

建议保存到：

- `results/02_hotpotqa_comparison_expansion/candidate_batch_raw.csv`

每行至少有：

- `task_id`
- `question`
- `answer`
- `raw_type`

### Step 2. 做最小过滤

把 15 个 raw candidates 过滤成：

- `candidate_batch_filtered.csv`

目标是保留：

- 10 到 15 个可进入人工标注的题

### Step 3. 追加到 `pilot/taxonomy.csv`

把这批 filtered candidates 追加进：

- [pilot/taxonomy.csv](../pilot/taxonomy.csv)

注意：

- 不要新建第二份 taxonomy 主表
- working table 继续保持单一来源

### Step 4. 做增量标注

对这一批新增候选题，逐题填写：

- `reasoning_label`
- `keep_drop`
- `note`

仍然只使用：

- [taxonomy_guideline.md](./taxonomy_guideline.md)

### Step 5. 统计新增 `comparison keep`

这一批标完后，立即统计：

- 新增了多少 `comparison keep`
- 当前 `HotpotQA comparison keep` 总数变成多少

### Step 6. 判断是否足够构 set

如果总数已经：

- `>= 5`

就进入 comparison source set 构造。

如果总数仍然：

- `< 5`

再决定是否做第二批扩池。

## 8. 这一批必须记录到哪里

第一批扩池做完后，至少更新 3 个地方。

### 1. `pilot/taxonomy.csv`

这是主工作表，必须有最终标注结果。

### 2. `pilot/notes.md`

补一条 expansion log，至少写：

- 扩池触发原因
- 这一批扩了多少候选题
- 过滤后剩多少
- 最终新增多少 `comparison keep`
- 是否足够构造 `hp_comparison_set_01`

### 3. `results/02_hotpotqa_comparison_expansion/`

建议至少放：

- `candidate_batch_raw.csv`
- `candidate_batch_filtered.csv`
- `candidate_batch_full.json`
- 相关 notebook 或脚本输出

## 9. 第一批完成后的判断标准

### 可以继续往下走

如果满足：

- 当前 `HotpotQA comparison keep >= 5`
- 其中至少 5 题你自己敢拿来构 `source set`
- 不是 5 个近重复模板

那就继续：

- 构造 `hp_comparison_set_01`

### 暂时不要往下走

如果出现下面任一情况，就不要急着构 set：

- 仍然不到 5 个 `comparison keep`
- 虽然达到 5 个，但 2 到 3 个是明显边界题
- 5 个题几乎同模板

这时更合理的是：

- 继续第二批小规模扩池

## 10. 一个最短版本的执行清单

如果你现在就要开做，直接照这个 checklist：

1. 从当前 `HotpotQA` split 里预筛 15 个 `type = comparison` 的 raw candidates  
2. 去掉坏数据和明显近重复  
3. 把剩余候选题追加到 [pilot/taxonomy.csv](../pilot/taxonomy.csv)  
4. 用现有 taxonomy 规则做增量标注  
5. 统计 `HotpotQA comparison keep` 总数  
6. 如果总数达到 5，就开始构 `hp_comparison_set_01`  
7. 如果没达到 5，再计划第二批扩池  

## 11. 最重要的提醒

第一批扩池的目的不是“把 comparison 做大”，而是：

**尽快回答当前最卡住 round_01 的那个问题：source-side `comparison` coverage 到底能不能补出来。**
