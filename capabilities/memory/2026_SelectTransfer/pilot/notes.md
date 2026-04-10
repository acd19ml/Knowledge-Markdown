# Pilot Notes

这份文件是 `2026_SelectTransfer` 的前期实验日志。

用途不是写总结散文，而是：

- 记录每一步做了什么
- 记录关键判断依据
- 记录边界 case
- 记录是否满足进入下一步的条件

如果某一步没有写进这里，后面就很难追溯为什么当时做了那个决定。

## 使用规则

- 每完成一个阶段，就在对应栏目下补记录
- 每条记录尽量带日期
- 先写观察，再写判断
- 如果某一步导致规则变化，必须在这里留下原因

## 当前目标

当前 pilot 的目标是：

- 先验证 taxonomy 是否稳定
- 先构造第一批 clean source sets
- 先构造第一批 defendable relevant / irrelevant pairs
- 先检查 memory artifacts 是否可用
- 先确认 setup 是否能产出可解释的 selective-transfer 现象

## 相关文件

- [../protocol/taxonomy_guideline.md](../protocol/taxonomy_guideline.md)
- [../protocol/first-20-task-sampling-strategy.md](../protocol/first-20-task-sampling-strategy.md)
- [../protocol/first-20-annotation-workflow.md](../protocol/first-20-annotation-workflow.md)
- [../protocol/first-source-set-selection-workflow.md](../protocol/first-source-set-selection-workflow.md)
- [../protocol/first-pairing-workflow.md](../protocol/first-pairing-workflow.md)
- [../protocol/pilot-run-checklist.md](../protocol/pilot-run-checklist.md)
- [../design/experiment-contract.md](../design/experiment-contract.md)

## Log Template

每次记录建议使用下面的最小结构：

```md
### YYYY-MM-DD - Short Title

What was done:

- ...

What was observed:

- ...

Decision:

- ...

Next step:

- ...
```

---

## Sampling Log

记录第一轮 20 题是怎么抽出来的。

建议记录：

- 使用了哪个 benchmark split
- 抽样方式（简单随机 / 轻度分层）
- 是否过滤掉异常样本
- 最终保留多少题

### Entry Template

```md
### YYYY-MM-DD - Sampling Round X

What was done:

- sampled 10 tasks from HotpotQA
- sampled 10 tasks from 2WikiMultiHopQA

What was observed:

- ...

Decision:

- ...

Next step:

- start taxonomy annotation
```

### 2026-04-10 - Sampling Round 1 (Planned)

What was done:

- defined the first-round sampling target as 20 tasks in total
- fixed the initial allocation to:
  - 10 tasks from `HotpotQA`
  - 10 tasks from `2WikiMultiHopQA`
- decided to use simple random sampling first, followed by minimal filtering only for malformed items

What was observed:

- the goal of this round is to test taxonomy stability rather than maximize coverage
- the sampling step should avoid manual cherry-picking
- the final sample should still contain some uncomfortable or ambiguous cases, so taxonomy weaknesses can surface early

Decision:

- keep the first round small
- do not force class balance at the sampling stage
- do not filter tasks just because they look difficult or atypical

Next step:

- sample the first 10 `HotpotQA` tasks and first 10 `2WikiMultiHopQA` tasks under the agreed rule
- write the finalized sampling record after the actual sample is collected

### Sampling Round 1 Finalized Record Template

在真正抽完第一轮 20 题后，复制下面这个模板，改成带日期的实际记录。

```md
### YYYY-MM-DD - Sampling Round 1 (Finalized)

What was done:

- sampled 10 tasks from `HotpotQA`
- sampled 10 tasks from `2WikiMultiHopQA`
- removed X malformed / unusable items before finalizing the pool

What was observed:

- whether one benchmark contributed more ambiguous tasks
- whether the sample looked too repetitive on the surface
- whether any obvious anomalies appeared

Decision:

- keep the current 20-task sample as Round 1 input
- or resample specific tasks if there were obvious malformed items

Next step:

- fill the 20 tasks into `taxonomy.csv`
- start Round 1 taxonomy annotation
```

---

## Taxonomy Log

记录 taxonomy 标注阶段的关键信息。

建议记录：

- 哪些标签最常见
- 哪些边界 case 最麻烦
- `drop` 比例
- 规则是否需要调整

### Entry Template

```md
### YYYY-MM-DD - Taxonomy Round X

What was done:

- annotated 20 tasks

What was observed:

- bridge vs comparison ambiguity appeared in ...
- drop rate was ...

Decision:

- keep current guideline / revise specific rule

Next step:

- build first source sets
```

### 2026-04-10 - Taxonomy Round 1 (Planned)

What was done:

- fixed the first-round annotation target to the initial 20-task sample
- decided that each task will receive:
  - one `reasoning_label`
  - one `keep` / `drop` decision
  - one short `note`
- decided to follow the existing taxonomy order strictly:
  - `comparison`
  - `temporal`
  - `bridge`
  - `distractor-heavy`
  - otherwise `drop`

What was observed:

- the main purpose of Round 1 is to test taxonomy stability, not to maximize labeled volume
- borderline cases are expected and should be recorded rather than hidden
- `distractor-heavy` must not be used as a default fallback label

Decision:

- keep Round 1 small and controlled
- prioritize consistency over coverage
- drop ambiguous tasks rather than forcing unstable labels

Next step:

- annotate the 20 sampled tasks in `taxonomy.csv`
- identify the most difficult boundary cases for review

### Taxonomy Round 1 Finalized Record Template

在真正完成第一轮 taxonomy 标注后，复制下面这个模板，改成带日期的实际记录。

```md
### YYYY-MM-DD - Taxonomy Round 1 (Finalized)

What was done:

- annotated 20 tasks in `taxonomy.csv`
- assigned one dominant `reasoning_label` to each kept task
- marked ambiguous tasks as `drop`

What was observed:

- label distribution:
  - bridge: X
  - comparison: X
  - temporal: X
  - distractor-heavy: X
  - drop: X
- the most common ambiguity was ...
- the most unstable boundary was ...

Decision:

- keep the current guideline as-is
- or revise one specific labeling rule before scaling up

Next step:

- identify clean candidates for the first source sets
- archive the stable result as `taxonomy_round1.csv`
```

### 2026-04-10 - Taxonomy Round 1 (First Pass Completed)

What was done:

- reviewed the 20 sampled tasks using `sampled_20_full.json`
- read the question together with supporting titles and evidence structure
- filled `reasoning_label`, `keep_drop`, and `note` in `taxonomy.csv`

What was observed:

- current first-pass label distribution is:
  - bridge: 14
  - comparison: 6
  - temporal: 0
  - distractor-heavy: 0
  - drop: 0
- the main ambiguity is still `bridge` vs `comparison`, especially for `bridge_comparison` items in `2WikiMultiHopQA`
- the two `inference` items were mapped to `bridge` because the dominant pattern is still relation chaining through an intermediate entity
- this 20-task sample does not expose stable `temporal` or `distractor-heavy` cases

Decision:

- keep the current first-pass labels as the working Round 1 annotation
- treat this sample as an effective `bridge + comparison` pilot subset
- do not archive this round as final yet, because the delayed re-annotation check has not been completed

Next step:

- re-annotate 5 tasks after a delay to check intra-annotator stability
- recommended re-annotation set:
  - `wiki_dev_0123`
  - `wiki_dev_12298`
  - `wiki_dev_2639`
  - `wiki_dev_1379`
  - `wiki_dev_10727`
- if the labels remain stable, start constructing the first source sets from the kept pool

---

## Source Set Log

记录第一批 source sets 的构造过程。

建议记录：

- 每个 cluster 是否足够稳定
- 哪些题被纳入 source set
- 哪些题被排除，为什么
- 哪些 source set 质量不够好

### Entry Template

```md
### YYYY-MM-DD - Source Set Round X

What was done:

- built bridge_set_01
- built comparison_set_01

What was observed:

- ...

Decision:

- keep / revise / drop certain source sets

Next step:

- construct first pairing table
```

### 2026-04-10 - Source Set Round 1 (Planned)

What was done:

- fixed the Round 1 source-set goal to a small number of clean sets rather than broad coverage
- decided that each source set must:
  - contain exactly `N = 5` tasks
  - stay within one dominant reasoning cluster
  - avoid near-duplicate surface forms
  - be as `entity-disjoint` as possible
- decided that Round 1 only needs 2 to 3 clean source sets if that is all the data can support

What was observed:

- the main purpose of Round 1 source-set construction is to create usable memory units for pilot experiments
- source-set quality matters more than the number of sets
- forcing all clusters into Round 1 would likely introduce noisy or unstable sets

Decision:

- prioritize clean and explainable source sets over balanced cluster coverage
- exclude borderline taxonomy cases from the first source-set pool
- allow some clusters to be skipped in Round 1 if they are not yet stable

Next step:

- select the first clean candidates from `taxonomy.csv`
- fill `source_sets.csv` with the first Round 1 source sets

### Source Set Round 1 Finalized Record Template

在真正完成第一轮 source set 构造后，复制下面这个模板，改成带日期的实际记录。

```md
### YYYY-MM-DD - Source Set Round 1 (Finalized)

What was done:

- built X source sets from the Round 1 taxonomy pool
- each set used exactly 5 tasks from one dominant cluster
- excluded borderline or repetitive items from the first set pool

What was observed:

- usable clusters:
  - bridge: ...
  - comparison: ...
  - temporal: ...
  - distractor-heavy: ...
- the main quality issue was ...
- the main exclusion reason was ...

Decision:

- keep the following source sets for Round 1 pilot
- defer unstable clusters to a later round if needed

Next step:

- construct the first relevant / irrelevant pairs
- archive the stable result as `source_sets_round1.csv`
```

### 2026-04-10 - Source Set Round 1 (First Draft)

What was done:

- reviewed the kept `HotpotQA` tasks as the current source-side candidate pool
- enforced the source benchmark restriction from the current proposal:
  - source benchmark = `HotpotQA`
  - target benchmark = `2WikiMultiHopQA`
- built one draft bridge source set in `source_sets.csv`:
  - `hp_bridge_set_01`

What was observed:

- current source-side pool supports one clean `bridge` set of size `N = 5`
- the selected members are:
  - `hp_dev_2054`
  - `hp_dev_3245`
  - `hp_dev_1119`
  - `hp_dev_1668`
  - `hp_dev_4237`
- this set is reasonably `entity-disjoint` and has mixed surface forms across venue, school, film, series, and song queries
- the current source-side `comparison` pool is not yet sufficient:
  - only `hp_dev_0478`
  - and `hp_dev_6149`
- because `N = 5` is fixed in the current design, no comparison source set should be forced from this sample

Decision:

- keep `hp_bridge_set_01` as the working Round 1 draft source set
- do not draft a comparison source set by borrowing `2WikiMultiHopQA` tasks, because that would violate the current source-target setting
- treat comparison-source insufficiency as a real protocol signal rather than patching it ad hoc

Next step:

- complete the delayed re-annotation check for the 5 selected taxonomy items
- then decide whether Round 1 pairing should proceed with:
  - bridge-only target subsets
  - or a revised source-pool expansion before pairing

---

## Pairing Log

记录 relevant / irrelevant pairs 的构造判断。

建议记录：

- 哪些 relevant pairs 最干净
- 哪些 irrelevant pairs 最容易混淆
- 哪些 pairing 最终被放弃

### Entry Template

```md
### YYYY-MM-DD - Pairing Round X

What was done:

- paired 8 relevant targets
- paired 8 irrelevant targets

What was observed:

- ...

Decision:

- freeze / revise pairing table

Next step:

- generate artifacts
```

### 2026-04-10 - Pairing Round 1 (Planned)

What was done:

- fixed the Round 1 pairing goal to a small set of clean and defensible pairs
- decided that each target task should be paired with:
  - one `relevant` source set
  - one `irrelevant` source set
- decided that pairing quality is more important than pair count in Round 1

What was observed:

- the purpose of pairing is not to maximize task coverage, but to make the `Relevant Split` and `Irrelevant Split` interpretable
- if the pair itself is ambiguous, later transfer results will be hard to explain
- irrelevant pairs must be structurally mismatched, not just topically different

Decision:

- prioritize pairs that can be explained in one short sentence
- avoid using unstable source sets or borderline target tasks
- allow the first pairing table to stay small if that improves clarity

Next step:

- construct the first relevant / irrelevant pairs in `pairing_table.csv`
- record why each pair is defensible in `pairing_note`

### Pairing Round 1 Finalized Record Template

在真正完成第一轮 pairing 后，复制下面这个模板，改成带日期的实际记录。

```md
### YYYY-MM-DD - Pairing Round 1 (Finalized)

What was done:

- paired X target tasks with one relevant source set each
- paired the same X target tasks with one irrelevant source set each
- filtered out pairs with obvious overlap or leakage risks

What was observed:

- the cleanest relevant pattern was ...
- the cleanest irrelevant mismatch was ...
- the most common pairing difficulty was ...

Decision:

- keep the current pairing table for Round 1 pilot
- or revise specific pairs before generating artifacts

Next step:

- generate the first memory artifacts
- archive the stable result as `pairing_table_round1.csv`
```

---

## Artifact Log

记录 `episodic_trace` 和 `cross_episode_consolidation` 的人工检查结果。

建议记录：

- 哪些 artifacts 可用
- 哪些 artifacts 过于空泛
- 哪些 source sets 需要重做

### Entry Template

```md
### YYYY-MM-DD - Artifact Review Round X

What was done:

- reviewed artifacts for bridge_set_01

What was observed:

- episodic trace was ...
- consolidation was ...

Decision:

- keep / regenerate / revise prompt

Next step:

- start pilot runs
```

### 2026-04-10 - Artifact Review Round 1 (Planned)

What was done:

- fixed the Round 1 artifact review goal to manual quality inspection before any pilot run
- decided that each selected source set must generate:
  - one `episodic_trace`
  - one `cross_episode_consolidation`
- decided that artifact quality must be checked before comparing conditions

What was observed:

- low-quality artifacts would make later results uninterpretable
- `episodic_trace` and `cross_episode_consolidation` must differ in substance, not only in formatting
- answer leakage or generic empty summaries would invalidate the corresponding source set

Decision:

- review artifacts manually before entering any pilot run
- reject or regenerate artifacts that are too generic, too noisy, or structurally weak

Next step:

- inspect the first generated artifacts and record which source sets are ready for pilot

### Artifact Review Round 1 Finalized Record Template

在真正完成第一轮 artifact review 后，复制下面这个模板，改成带日期的实际记录。

```md
### YYYY-MM-DD - Artifact Review Round 1 (Finalized)

What was done:

- reviewed artifacts for X source sets
- checked both `episodic_trace` and `cross_episode_consolidation`

What was observed:

- strong artifacts:
  - ...
- weak artifacts:
  - ...
- the main failure mode was ...

Decision:

- keep / regenerate / revise specific artifacts

Next step:

- enter Round 1 pilot run with the approved artifact set
```

---

## Pilot Run Log

记录第一轮实际运行中的关键信号。

建议记录：

- relevant split 上是否有帮助趋势
- irrelevant split 上是否观察到 negative transfer
- 哪些 case 最值得保留

### Entry Template

```md
### YYYY-MM-DD - Pilot Run Round X

What was done:

- ran No Memory / Episodic Trace / Cross-Episode Consolidation

What was observed:

- ...

Decision:

- proceed / stop / revise setup

Next step:

- add applicability judgment / refine pairing / improve artifacts
```

### 2026-04-10 - Pilot Run Round 1 (Planned)

What was done:

- fixed the Round 1 pilot goal to a small-scale comparison of `memory form`
- decided to compare:
  - `No Memory`
  - `Episodic Trace`
  - `Cross-Episode Consolidation`
- postponed `Cross-Episode Consolidation + Applicability Judgment` until the basic setup becomes interpretable

What was observed:

- the purpose of Round 1 is not statistical significance
- the purpose is to see whether the current setup can produce explainable case-level phenomena
- negative transfer must be observable before the project can meaningfully study selective transfer

Decision:

- keep the first pilot small
- prioritize clean cases and interpretable logs over coverage
- do not add more conditions until the current round is understandable

Next step:

- run the first pilot conditions on the approved Round 1 pairs
- record split-level behavior and representative cases

### Pilot Run Round 1 Finalized Record Template

在真正完成第一轮 pilot run 后，复制下面这个模板，改成带日期的实际记录。

```md
### YYYY-MM-DD - Pilot Run Round 1 (Finalized)

What was done:

- ran the Round 1 pilot on X relevant pairs and X irrelevant pairs
- compared `No Memory`, `Episodic Trace`, and `Cross-Episode Consolidation`

What was observed:

- relevant split trend: ...
- irrelevant split trend: ...
- strongest positive case: ...
- strongest negative-transfer case: ...

Decision:

- proceed / revise setup / stop and debug

Next step:

- add applicability judgment
- or refine taxonomy / source sets / pairing / artifacts first
```

---

## Go / No-Go Notes

每一轮进入下一阶段前，在这里写一句明确判断：

- `GO`: 当前阶段已经足够稳定，可以进入下一步
- `NO-GO`: 当前阶段还不够稳，必须先修正

### Entry Template

```md
### YYYY-MM-DD - Gate Decision

Stage:

- taxonomy / source sets / pairing / artifacts / pilot runs

Decision:

- GO / NO-GO

Reason:

- ...
```
