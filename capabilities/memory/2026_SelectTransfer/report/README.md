# report/

这一层现在同时承担两种职责：

- `progress report` 轮次写作素材
- final report assembly 与 supporting layers

它和其他目录的分工是：

- `design/` 回答：项目为什么这样定义
- `protocol/` 回答：实验应该怎么做
- `pilot/` 回答：当前具体做到了哪里
- `report/` 回答：这些过程如何被写成可提交的 `progress report` 与最终课程报告

## 当前文件

- [progress-report-draft.md](./progress-report-draft.md)
  - 可直接用于 `progress report` 的段落草稿（写于 taxonomy + source-set feasibility 阶段，尚未包含 pilot 结果）
- [progress-report-round1-pilot.md](./progress-report-round1-pilot.md)
  - Round 1 pilot 完整结果分析：60 runs 的 case-level 诊断、sensitivity deficit 根因分析、下一步方向建议
  - 重点写：
    - 问题如何收缩
    - protocol 如何建立
    - 当前真实发现是什么
    - 这些发现如何改变设计决策
    - 下一步是什么
- [progress-report-round1b-prompt-diagnosis.md](./progress-report-round1b-prompt-diagnosis.md)
  - Round 1b prompt diagnosis 结果分析：6 个 smoke targets 上的 structured reasoning 输出、memory use/reject 证据、以及为什么当前还不能直接下 selective transfer 结论
  - 重点写：
    - prompt scaffold 是否修复了 Round 1 的单行直答问题
    - process-level evidence 是否出现
    - 哪些 case 出现了 memory-induced degradation / recovery
    - 为什么下一步应先收紧 scoring、process analysis 与 case role reclassification
- [../results/05_round1b_prep/round1c_role_aware_smoke_summary.md](../results/05_round1b_prep/round1c_role_aware_smoke_summary.md)
  - Round 1c 前置摘要：把 Round 1b 的 run-level 结果按 `case role` 重组，明确哪些 case 只能做 process sanity、哪些是 artifact / format / boundary case
  - 重点写：
    - 哪些 runs 已经不该进入 transfer aggregate
    - 哪些 case 仍可保留作 process-level signal
    - 为什么下一轮应先修 case selection，而不是继续求混合平均
- [../results/05_round1b_prep/round1c_aggregate_rules.md](../results/05_round1b_prep/round1c_aggregate_rules.md)
  - Round 1c 的聚合规则：明确哪些平均数以后禁止再报，哪些 case 只能作为 process / diagnostic / boundary 使用
- [progress-report-round1c-role-aware-smoke-repair.md](./progress-report-round1c-role-aware-smoke-repair.md)
  - Round 1c 结果分析：把 Round 1b 的 run-level 结果重新组织为 `process sanity`、`diagnostic`、`audit / boundary` 三类 allowed aggregate views
  - 重点写：
    - 为什么当前 6 个 smoke cases 不能再被视为统一 benchmark
    - 哪些 case 只保留作 process-level signal
    - 哪些 case 应从 transfer evidence 中排除
    - 为什么下一步必须先按 role 选 case，再决定是否 rerun
- [progress-report-round1d-bridge-subtype-repair.md](./progress-report-round1d-bridge-subtype-repair.md)
  - Round 1d 结果分析：把粗粒度 `bridge` 进一步拆成 `attribute_bridge` 与 `relation_chain_bridge`，解释为什么 `wiki_dev_2639` 的 relevant derailment 实际上是 subtype mismatch
  - 重点写：
    - 当前 `hp_bridge_set_01` 实际只代表什么
    - 哪些 `bridge` target 仍然 subtype-matched
    - 为什么 `wiki_dev_2639` 不能再被当作 “relevant memory hurts” 证据
    - 为什么下一步必须先补 source-side subtype coverage
- [progress-report-round1e-relation-chain-feasibility.md](./progress-report-round1e-relation-chain-feasibility.md)
  - Round 1e 结果分析：通过 Batch 1 / Batch 2 的 source-side feasibility check，证明 `HotpotQA` 可以支持一个最小 `relation_chain_bridge` source set
  - 重点写：
    - generic relation-term expansion 为什么失败
    - high-precision template expansion 为什么成功
    - draft `relation_chain_bridge` source set 是如何构造出来的
    - 为什么下一步已经从 feasibility 转入 artifact generation + minimal rerun prep
- [progress-report-round1g-relation-chain-minirun.md](./progress-report-round1g-relation-chain-minirun.md)
  - Round 1g 结果分析：在固定 `Round 1b` scaffold 和 scoring 的前提下，只 rerun 两个被 reroute 的 relation-chain targets，检查 subtype repair 是否真的修复了此前的 diagnostic case
  - 重点写：
    - `wiki_dev_2639` 上 subtype repair 为什么对 `episodic_trace` 有效
    - 为什么 `cross_episode_consolidation` 仍然失败
    - `wiki_dev_1379` 为什么只能算 ceiling / sanity case
    - 为什么下一步应该转入 consolidation-only diagnosis
- [progress-report-round1h-consolidation-diagnosis.md](./progress-report-round1h-consolidation-diagnosis.md)
  - Round 1h 结果分析：在固定 subtype-matched source、固定 prompt scaffold 和 scoring 的前提下，只重写 `relation_chain` consolidation，并在 `wiki_dev_2639` 上比较 original vs revised consolidation
  - 重点写：
    - 为什么 revised consolidation 修复了 formatting 但没修复 correctness
    - 为什么当前 failure 已经不再主要来自 subtype mismatch
    - 为什么剩余问题应被收缩成 `kinship operator interpretation`
    - 为什么下一步应该只修关系词的 executable interpretation，而不是继续 full rerun
- [progress-report-round1i-kinship-operator-repair.md](./progress-report-round1i-kinship-operator-repair.md)
  - Round 1i 结果分析：在固定 model / routing / scoring / scaffold 的前提下，只修 `sibling-in-law` 这类 kinship operator 的 executable interpretation，并验证 relevant consolidation 是否能被恢复
  - 重点写：
    - 为什么 operator repair 可以把 relevant consolidation 从 wrong 拉回 correct
    - 为什么 irrelevant consolidation 仍然保持错误
    - 为什么 `wiki_dev_2639` 不应再被写成 derailment evidence
    - 为什么下一步更应该做 patchback / synthesis，而不是继续单-case prompt polishing
- [progress-report-round1-final-synthesis.md](./progress-report-round1-final-synthesis.md)
  - Round 1 高层综合：把 `Round 1 -> 1i -> 1j` 的方法修复链条统一成一个最终可 defend 的结论
  - 重点写：
    - 为什么早期 aggregate 结论会误导
    - 为什么 `wiki_dev_2639` 的旧解释必须撤回
    - Round 1 最终真正支持的 methodological takeaway 是什么
    - 为什么下一步应转入 final report synthesis，而不是继续单-case rerun
- [final-report-round1-section.md](./final-report-round1-section.md)
  - 面向课程最终报告的 Round 1 成品段落，不再按 progress report 口吻写，而是直接按 final report 的 objective / findings / interpretation / limitations 组织
  - 重点写：
    - Round 1 的真正研究目标
    - repair chain 如何改变最终解释
    - 哪些 claim 可以成立、哪些不能成立
    - 可以直接作为最终报告中的 Round 1 主体部分
- [final-report-round1-section-v2.md](./final-report-round1-section-v2.md)
  - 用户修改后的 Round 1 final-report 主体版本；当前应优先以这份为最终正文基底，而不是继续扩写 progress 风格文档
- [round1-evidence-map.md](./round1-evidence-map.md)
  - L2 supporting layer：每条 claim / non-claim 对应的 progress report、result CSV、raw output、artifact version
- [round1-case-appendix.md](./round1-case-appendix.md)
  - L3 supporting layer：关键 case 的 before/after raw evidence
- [final-report-outline.md](./final-report-outline.md)
  - 最终课程报告装配计划：把已有 materials 收束成 `Introduction / Setting / Protocol / Results / Claims / Limitations / Future Work`
  - 重点写：
    - 现在为什么应从 experiment mode 切到 final-report assembly mode
    - 最终报告每一节应该吃哪些已有文件
    - 当前最该新增的成品段落是什么
- [final-report-method-section.md](./final-report-method-section.md)
  - 面向最终课程报告的 `Method` 成品段落
  - 重点写：
    - 实验 setting
    - source/pairing/evaluation protocol
    - 为什么 case-role discipline、subtype-aware pairing、executable abstraction 是方法的一部分
- [final-report-results-section.md](./final-report-results-section.md)
  - 面向最终课程报告的 `Results` 成品段落
  - 重点写：
    - Round 1 repair chain 如何逐步改变解释
    - `wiki_dev_2639` 为什么是关键 diagnostic case
    - 最终哪些结果可以被当作正式发现
- [final-report-discussion-section.md](./final-report-discussion-section.md)
  - 面向最终课程报告的 `Discussion` 成品段落
  - 重点写：
    - 理论含义
    - claims / non-claims 的边界
    - limitations 与下一步更合理的未来工作
- [final-report-master-outline.md](./final-report-master-outline.md)
  - 最终课程报告的总装配清单：明确章节顺序、每节应吃哪些已有文件、正文与 supporting layers 的分工
  - 重点写：
    - 最终报告的推荐结构
    - `Method / Results / Discussion` 应如何拼到主文档
    - L1 / L2 / L3 应分别承担什么角色
- [final-report-assembled-draft.md](./final-report-assembled-draft.md)
  - 最终课程报告的 assembled draft：把 `Introduction / Method / Results / Discussion / Limitations / Future Work` 真正拼成一篇完整草稿
  - 重点写：
    - 不再按 progress report 组织
    - 直接面向最终提交稿
    - 用 L2 / L3 作为 supporting evidence，而不是把所有证据塞进正文
- [final-report-assembled-draft-v3.md](./final-report-assembled-draft-v3.md)
  - `final-report-assembled-draft.md` 与 `final-report-assembled-draft-codex.md` 的折中版
  - 重点写：
    - 保留可读性更强的总叙述
    - 补回方法细节、claim 边界与 protocol 约束
    - 作为更适合继续做 final editorial pass 的主稿
- [final-report-assembled-draft-v4.md](./final-report-assembled-draft-v4.md)
  - 当前最接近 canonical 的完整最终报告草稿
  - 重点写：
    - 保留 assembled draft 的可读性
    - 吸收 L1 / L2 / L3 的证据约束
    - 作为当前最终提交稿的主要编辑对象
- [final-report-method-results-discussion.md](./final-report-method-results-discussion.md)
  - 较早的 `Method / Results / Discussion` 合并稿
- [final-report-method-results-discussion-v2.md](./final-report-method-results-discussion-v2.md)
  - 更完整的 `Method / Results / Discussion` 合并稿，可作为最终整合时的备份材料

## 使用方式

- 不要把整份文件原样无脑粘贴
- 先根据老师要求的篇幅，选用其中的段落
- 如果 report 需要更短版本，优先保留：
  - `摘要段落`
  - `问题收缩`
  - `当前发现`
  - `设计决策`
  - `下一步`

## 原则

- 只写已经发生、且能被文件或数据支持的内容
- 不把焦虑、犹豫、元讨论本身写成进展
- 把“问题发现 -> 证据 -> 决策 -> 下一步”写清楚

当前建议：

- final report 主稿优先编辑 [final-report-assembled-draft-v4.md](./final-report-assembled-draft-v4.md)
- 证据追溯优先看 [round1-evidence-map.md](./round1-evidence-map.md)
- 关键 raw case 优先看 [round1-case-appendix.md](./round1-case-appendix.md)
