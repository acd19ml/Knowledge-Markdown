# C2 Summary: Online AWM 泛化结果首轮复现结论

> 本文档是 C2 的首轮结果摘要页。
> 它从 [c2-runbook.md](c2-runbook.md) 中抽取主结果、判定与阶段性结论，用于状态表、周报和汇报引用。

---

## 1. 复现目标

C2 要检查的核心主张是：

- online AWM 在 `cross-task`、`cross-website`、`cross-domain` 上优于 baseline
- 随着 distribution gap 增大，online 相对 offline 更有优势

在当前代码库口径下，本轮首要检验的是：

- online 相对 baseline 的方向是否成立

需要单独注明的是：

- `cross-website` 与 `cross-domain` 的 offline 对照在当前 repo 中无法按 C1 同口径直接构造，因此本轮不把这部分缺口误写成研究结论

---

## 2. 运行口径

### 2.1 已完成的三个 split

| split | website | model | compared conditions |
|------|------|------|------|
| `test_task` | `kayak` | `gpt-4o` | baseline / offline / online |
| `test_website` | `tripadvisor` | `qwen/qwen3.5-397b-a17b` | baseline / online |
| `test_domain` | `reddit` | `qwen/qwen3.5-397b-a17b` | baseline / online |

### 2.2 当前实现约束

- `test_task`：可以比较 baseline / offline / online
- `test_website`：offline 记为 `N/A`
- `test_domain`：offline 记为 `N/A`

---

## 3. 主结果表

| split | website | baseline | offline | online | C2 status | notes |
|------|------|------|------|------|------|------|
| `test_task` | `kayak` | complete | complete | complete | `reproduced` | online > baseline, online ~= offline |
| `test_website` | `tripadvisor` | complete | N/A | complete | `not reproduced` | online < baseline on all four metrics |
| `test_domain` | `reddit` | complete | N/A | complete | `not reproduced` | online < baseline on all four metrics |

---

## 4. 分轮结果

### 4.1 C2-R1: `test_task / kayak`

| condition | Element Acc | Action F1 | Step SR | SR |
|------|------:|------:|------:|------:|
| no_workflow | 50.3 | 59.4 | 47.9 | 0.0 |
| offline_wf | 55.9 | 61.2 | 53.5 | 0.0 |
| online_wf | 54.7 | 62.4 | 53.5 | 0.0 |

判定：

- `reproduced`
- online 相对 baseline 在 `Element Acc`、`Action F1`、`Step SR` 上均更好
- online 与 offline 在 `cross-task` 上接近

### 4.2 C2-R2: `test_website / tripadvisor`

| condition | Element Acc | Action F1 | Step SR | SR |
|------|------:|------:|------:|------:|
| no_workflow | 47.0 | 56.9 | 43.9 | 4.3 |
| online_wf | 37.0 | 52.0 | 32.1 | 0.0 |

判定：

- `not reproduced`
- online 相对 baseline 在四个指标上均下降

### 4.3 C2-R3: `test_domain / reddit`

| condition | Element Acc | Action F1 | Step SR | SR |
|------|------:|------:|------:|------:|
| no_workflow | 58.8 | 63.3 | 53.0 | 9.1 |
| online_wf | 55.6 | 62.6 | 50.8 | 6.1 |

判定：

- `not reproduced`
- online 相对 baseline 在四个指标上均下降

---

## 5. 阶段性结论

建议写入状态表的版本：

```text
C2 首轮已完成三个 split 的 baseline / online 对比。结果显示：online AWM 仅在 test_task / kayak 上优于 baseline，而在 test_website / tripadvisor 与 test_domain / reddit 上均低于 baseline。因此，当前结果不支持“online AWM 在更大 distribution gap 下稳定优于 baseline”的结论。更准确的表述是：C2 首轮证据呈 mixed，但整体方向偏向 not reproduced。
```

建议写入周报或汇报的版本：

```text
在当前 repo 口径下，我们完成了 C2 的首轮 split-level 复现。online AWM 在 cross-task（kayak）上表现为 reproduced，但在 cross-website（tripadvisor）与 cross-domain（reddit）上均未超过 baseline。基于这三组结果，现阶段不能支持论文中“online AWM 在更大 distribution gap 下更具优势”的主张。需要注意的是，cross-website 与 cross-domain 的 offline 对照在当前代码库中无法按同口径直接构造，因此当前结论主要针对 online 相对 baseline 的趋势，而不是对 online/offline 差异的完整复现。
```

---

## 6. 当前建议

1. 先冻结 C2 首轮结果，不再继续扩网站
2. 在总状态表里把 C2 记为：
   - `已完成首轮`
   - `阶段性结论：mixed`
   - `整体方向：not reproduced`
3. 若继续深挖，优先做：
   - `tripadvisor` / `reddit` 的退化原因分析
   - 或直接进入 `C3`
