# Relation-Chain Bridge Expansion Batch 1 Prefilter Diagnosis

Date: 2026-04-11

## Observation

当前第一批 relation-chain 扩池虽然成功产出了：

- `candidate_batch_raw.csv`
- `candidate_batch_filtered.csv`
- `candidate_batch_for_subtype_annotation.csv`

但这一批候选题 **不能直接进入人工标注**。

原因很明确：

- 当前 relation-term 预筛对 `son` 使用了普通子串命中
- 因此大量非 relation-chain 题被错误纳入

典型假阳性来源包括：

- `first person`
- `season`
- `Tysons`

所以当前 15 条候选题不应被解释为：

- benchmark 中存在 15 条 relation-looking bridge 候选

更准确的说法是：

- 当前 prefilter 规则生成了一批混杂假阳性的候选

## Diagnosis

这不是 benchmark 不支持 `relation_chain_bridge` 的证据。

它只说明一件事：

- **当前 batch 1 的 prefilter 规则过松。**

因此，这一批失败的原因首先是：

- prefilter bug / heuristic too loose

而不是：

- `HotpotQA` 中没有这个 subtype

## Immediate Decision

当前 `candidate_batch_for_subtype_annotation.csv` 不建议继续人工标注。

更合理的顺序是：

1. 先修 notebook 中的 relation-term 匹配逻辑
2. 重新生成 batch 1
3. 再对新的候选题做 subtype annotation

## Repair Direction

下一版 prefilter 至少应满足：

1. relation term 必须按 **word / phrase boundary** 匹配  
2. `father-in-law`、`brother-in-law` 这类多词关系应按完整 phrase 命中  
3. `son`、`father`、`mother` 等高歧义词不能再以普通 substring 方式命中

## Current Status

因此，这一批现在的更准确状态是：

- `batch generated`
- `batch invalid for annotation`
- `need prefilter repair before continuing`
