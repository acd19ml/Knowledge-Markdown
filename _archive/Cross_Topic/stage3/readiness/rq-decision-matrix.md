# Stage 3 RQ Decision Matrix

> **Status**: Final support artifact
> **Purpose**: 把 “明显优于 / 稳定增益” 改成可执行的 Stage 3 pilot 判定规则
> **Parent Docs**: [rq-proof-sheet.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/readiness/rq-proof-sheet.md), [experiment-protocol.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/design/experiment-protocol.md), [webarena-task-split.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena-task-split.md)

---

## 1. Decision Conventions

- **Condition names** follow [experiment-protocol.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/design/experiment-protocol.md):
  - `C0` = no memory
  - `C1` = raw retrieval
  - `C2` = coarse workflow memory
  - `C3` = EDPM success-only
  - `C4` = EDPM failure-aware
  - `C5` = EDPM + policy constraint
- **Primary pilot arena**: 24-task WebArena split with `L1 / L2 / L3` separation.
- **Aggregation rule**: report macro-average by task family first, then macro-average across families. Do not let one site with many tasks dominate the judgment.
- **Minimum repetition budget**: use the current split budget from [webarena-task-split.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena-task-split.md): `L1 x3`, `L2 x2`, `L3 x2`.
- **Support labels**:
  - `Support`: meets the exact decision rule below.
  - `Borderline`: primary comparison is positive, but one guardrail fails.
  - `Fail`: does not meet the primary comparison or collapses to `L1`-only gains.

---

## 2. Operational Matrix

| Claim | Primary comparison | Primary split | Primary metric | Executable decision rule | Falsification trigger |
|---|---|---|---|---|---|
| **Final RQ**: EDPM + failure-aware write-back yields reusable experience gain beyond task replay | `max(C4, C5)` vs `max(C1, C2)` | `L2` primary, `L3` guardrail | task success rate | Mark `Support` only if: `L2` macro success gain is `>= 8` absolute points; at least `3/4` families show non-negative `L2` gain; `L3` is not negative overall and at least `2/4` families are non-negative; `C4` also beats `C3` on failure recovery by `>= 10` points | `L1` gain exists but `L2` gain is `< 8` points; or `L3` turns net negative; or `C4` fails to beat `C3`, meaning the result is better explained by cache/retrieval alone |
| **H1 Memory Unit**: EDPM rule is better than raw retrieval and coarse workflow memory | `C3` vs `max(C1, C2)` | `L2` primary, `L1` sanity, `L3` secondary | task success rate | Mark `Support` only if `C3` beats both `C1` and `C2` by `>= 8` absolute points on `L2`, and retrieval precision is not worse than the stronger baseline by more than `5` points | `C3` only wins on `L1`; or `C3 <= C2` on `L2`; or success improves only by over-triggering memory while retrieval precision drops by `> 5` points |
| **H2 Retrieval/Application Separation**: policy constraint beats pure context injection | `C5` vs `C4` | `L2 + L3` combined | false-memory rate | Mark `Support` only if `C5` reduces false-memory rate by `>= 10` absolute points, while overall success is non-inferior (`C5 >= C4 - 2` points), and at least one transfer level (`L2` or `L3`) gains `>= 3` success points | false-memory rate does not improve meaningfully; or success drops by `> 2` points without a compensating precision gain; or any gain is visible only on `L1` |
| **H3 Failure Write-Back**: failure-aware write-back improves post-failure reuse | `C4` vs `C3` | failure-first episodes in `L1 + L2` | failure recovery rate after write-back | Mark `Support` only if, among tasks with an initial failure, `C4` improves next-attempt recovery by `>= 10` absolute points and reduces repeated-failure rate by `>= 10` points | `C4` does not beat `C3` after failures; or recovery improves on one family but repeated-failure rate stays flat; or write-back raises false-memory rate by `> 5` points |
| **RQ non-cache guardrail**: learned content is not just literal replay | `C4` across `L1/L2/L3` | `L2` and `L3` | transfer gain relative to `C0` | Treat the whole RQ as only `Borderline` unless `L2` remains positive (`>= 5` points over `C0`) and `L3` remains non-negative overall | only `L1` improves; or `L2/L3` collapse to baseline, indicating the memory is a task cache |
| **Nearest-work claim**: EDPM is not just workflow memory with a rename | `C3` vs `C2`, plus `C4` vs `C3` | `L2` primary | success rate plus revision success rate | Claim this only if both are true: `C3 > C2` on `L2` by `>= 8` points, and `C4 > C3` on revision success by `>= 10` points | if `C3 ~= C2`, then the unit is still acting like workflow memory; if `C4 ~= C3`, then failure-aware revision is not doing real work |

---

## 3. Reporting Template

每次 pilot 报告至少给出以下一行摘要，避免回到“看起来有提升”式表述：

```text
Claim: H1 Memory Unit
Comparison: C3 vs C1/C2
Primary split: L2
Observed: +X pp over C1, +Y pp over C2; retrieval precision delta = Z pp
Judgment: Support / Borderline / Fail
Reason: <which exact threshold was met or missed>
```

---

## 4. What This Matrix Does Not Replace

- 它不替代 [webarena-motif-audit.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena-motif-audit.md)；如果 split 自身有 leakage，任何阈值判断都不可信。
- 它不替代正式统计检验；当前目标是先把 Stage 3 pilot 的 go/no-go 规则固定下来。
- 它不保证最终论文阈值就用这些数字；这些阈值是为了防止方法设计阶段继续用模糊措辞推进。
