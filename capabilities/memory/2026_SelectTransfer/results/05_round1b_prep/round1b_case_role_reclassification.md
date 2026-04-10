# Round 1b Case Role Reclassification

Date: 2026-04-11

这份文件把 [round1b_pairing_artifact_audit.md](./round1b_pairing_artifact_audit.md) 的 case-level 结论，压缩成下一轮可直接执行的 `case role` 决策。

目的不是重复 audit，而是明确：

- 哪些 case 还能继续保留
- 保留时是作为什么角色保留
- 哪些 case 不能再拿来做 `selective transfer` aggregate evidence

对应表格：

- [round1b_case_role_reclassification.csv](./round1b_case_role_reclassification.csv)

---

## 1. 总体结论

当前 6 个 smoke cases 不应再被当作一个同质的 “mini benchmark” 来看待。

更准确地说，它们已经分化成四类不同角色：

1. **process sanity cases**
   - 用来观察模型是否显式 `use / reject` memory
   - 不用于支持 outcome-level transfer claim

2. **artifact-sensitive diagnostic cases**
   - 用来检查当前 `pairing` 与 `artifact wording` 是否在制造额外干扰
   - 不应直接进入 aggregate

3. **audit / boundary cases**
   - 用来提醒 benchmark ambiguity 或 scoring noise
   - 只保留作边界说明

4. **answer-format sensitive cases**
   - 用来区分 reasoning improvement 与 output compression
   - 不应被误判为 strong transfer evidence

换句话说：

**Round 1b 的 6 个 case 现在更像一个“诊断包”，而不是一个可以直接汇总成 split-level 结论的小 benchmark。**

---

## 2. 逐类解释

### 2.1 Process Sanity Cases

#### `wiki_dev_8896`

- 当前最干净的 process-level selectivity case
- relevant episodic 被显式使用，irrelevant episodic 被显式拒绝
- 但 baseline 本来就正确，因此不提供 transfer gain

角色：

- 继续保留
- 作为下一轮主要的 process sanity check

#### `wiki_dev_10727`

- 干净的 comparison ceiling case
- 即使 irrelevant episodic 出现了 `explicit_use`，也没有改变答案

角色：

- 继续保留
- 作为次级 process case，用来区分：
  - verbalized memory use
  - outcome dependence

### 2.2 Artifact-Sensitive Diagnostic Case

#### `wiki_dev_2639`

- relevant bridge artifact 把正确 baseline 拉成拒答
- 当前更像 `artifact-induced derailment`
- 它提示 `bridge` cluster 在当前粒度下过粗，relation-chain case 与一般 attribute-bridge 并不等价

角色：

- 继续保留
- 但不是 transfer evidence
- 用来驱动下一轮的 `bridge subtype` 检查

### 2.3 Answer-Format Sensitive Case

#### `wiki_dev_7019`

- irrelevant consolidation 的 improvement 更像把过长答案压缩成更贴近 gold 的形式
- 不能直接解释成更强的 strategy reuse

角色：

- 继续保留
- 用来检查 memory 是否改变 `answer granularity / answer type`

### 2.4 Audit / Boundary Cases

#### `wiki_dev_0092`

- benchmark ambiguity case
- 只适合观察 `use / reject / ignore`
- 不应再纳入 transfer aggregate

#### `wiki_dev_6083`

- scoring boundary case
- `Spain` vs `Spanish` 不应再被当作 memory effect 证据

角色：

- 两条都继续保留
- 但只保留作 audit / boundary 说明

---

## 3. 对下一轮的直接含义

### 3.1 不要原样复用这 6 条来做 aggregate

当前最重要的决策是：

- **下一轮不能再把这 6 个 case 当作一个统一 smoke subset 直接汇总 EM/F1 来解读**

因为它们当前承担的是不同实验角色，而不是同一类 evidence。

### 3.2 下一轮应改成 role-aware smoke subset

更合理的结构是：

- `process sanity set`
  - `wiki_dev_8896`
  - `wiki_dev_10727`

- `artifact-sensitive diagnostic set`
  - `wiki_dev_2639`
  - `wiki_dev_7019`

- `audit / boundary set`
  - `wiki_dev_0092`
  - `wiki_dev_6083`

然后分别回答不同问题，而不是再求一个混合平均。

### 3.3 下一轮 full rerun 的前提

在进入更大 rerun 之前，至少还需要三件事更清楚：

1. `wiki_dev_6083` 这类 normalization 是否要调整 scoring
2. `wiki_dev_2639` 暴露出的 `bridge subtype` 是否需要 refinement
3. `wiki_dev_7019` 这类 answer compression 是否需要单独 process metric

如果这三件事不先处理，full rerun 只会把当前 case-role 混杂的问题放大。

---

## 4. 一句话结论

**Round 1b 的 6 个 smoke cases 不该再被视为一个统一的小 benchmark，而应被重构成一个 role-aware diagnostic bundle。**
