# Stage 3 WebArena Task Split

> **Status**: Draft v0.2
> **Role**: WebArena pilot 任务池、3 层 transfer split、官方 task binding
> **Parent Protocol**: [experiment-protocol.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/design/experiment-protocol.md)
> **Binding Workspace**: [README.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/README.md)
> **Formal Binding Table**: [webarena-task-binding.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena-task-binding.md)
> **Minimal Audit**: [webarena-motif-audit.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena-motif-audit.md)
> **Paper-Grounded Prep**: [webarena-task-binding-prep.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena-task-binding-prep.md)
> **Official Source**: `webarena/source/test.raw.json` from the WebArena repo

---

## 1. Scope

这份表仍然是 **Stage 3 pilot split**，但已经不再停留在纯 slot 命名层。当前版本直接绑定到了 WebArena 官方 `test.raw.json` 中的真实 `task_id / site / intent / intent_template_id`，因此可以作为 Stage 3 的 benchmark grounding 入口。

当前仍然**没有**完成的部分是 `page path`。由于官方原始配置大量使用 `__MAP__`、`__GITLAB__`、`__SHOPPING__`、`__SHOPPING_ADMIN__` 这类 placeholder token，而不是最终生成后的 URL，这一列暂时统一记为 `TBD from generated config`。

因此，这份文档的定位是：

- Stage 3：足够支撑方法设计、pilot split、ablation 规划
- 下一阶段：再补 generated config 级别的真实 page path 与 final holdout 审核

当前采用的 official WebArena site inventory：

- `reddit`
- `shopping`
- `shopping_admin`
- `gitlab`
- `map`
- `wikipedia`

当前 pilot split 只绑定前五个 site，`wikipedia` 暂列为下一阶段扩展项，而不是 Stage 3 必须项。

---

## 2. Split Principle

任务不是按 benchmark 原始 domain 名字硬切，而是按 **interaction motif** 来组。

每个 motif 都要有三层测试：

- **L1 Repeated Task**
  同一任务模板重复执行，测“第一次不会，第二次会”
- **L2 Same-Site Cross-Task**
  同一站点内相邻任务复用，测“不是 literal replay”
- **L3 Near-Domain Transfer**
  不同站点但相似 interaction archetype，测“不是 site cache”

---

## 3. Site Family View

| Official Site | Task Count in `test.raw.json` | Working Family in This Split | High-Value Motifs |
|---|---:|---|---|
| `reddit` | 129 | community/forum | post/comment forms, forum creation, thread interaction |
| `shopping` | 192 | ecommerce | search/filter, refund/contact forms, order/product lookup |
| `shopping_admin` | 184 | admin/CMS-like backoffice | page settings, review moderation, catalog/admin actions |
| `gitlab` | 204 | developer SaaS | settings/admin navigation, issue/MR forms, repo/member search |
| `map` | 128 | utility/search | search/filter/refine, route grounding, panel reset |
| `wikipedia` | 23 | background expansion only | multi-site composition, knowledge lookup |

---

## 4. Pilot Task Families

### TF-1 Hidden Navigation and Settings Discovery

**Target EDPM rule type**:

- hidden entry discovery
- overflow / profile / secondary menu heuristic
- re-ground after entering nested settings

Binding decision：WebArena 官方 task 中，`reddit` 并没有足够稳定的 settings-heavy 模板，因此这组 family 改为以 `gitlab` 为主站点，再用 `shopping_admin` 作为跨站 admin surface。

| Level | Slot | Task ID | Site | Intent Template ID | Intent | Page Path |
|---|---|---:|---|---:|---|---|
| L1 | `G-HN-1` | 448 | `gitlab` | 331 | set the homepage URL on my GitLab profile to https://egg.tart.com | `TBD from generated config` |
| L1 | `G-HN-2` | 449 | `gitlab` | 331 | set the homepage URL on my GitLab profile to https://helloworld.xyz | `TBD from generated config` |
| L2 | `G-HN-3` | 480 | `gitlab` | 293 | Invite yjlou as collaborator to solarized-prism-theme | `TBD from generated config` |
| L2 | `G-HN-4` | 533 | `gitlab` | 330 | Follow ['convexegg', 'yjlou'] on Gitlab | `TBD from generated config` |
| L3 | `SA-HN-1` | 486 | `shopping_admin` | 275 | Change the page title of "404 Not Found" page on my site to "Bruh bro you clicked the wrong page". | `TBD from generated config` |
| L3 | `SA-HN-2` | 489 | `shopping_admin` | 275 | Change the page title of "Privacy Policy" page on my site to "No privacy policy is needed is this dystopian world". | `TBD from generated config` |

### TF-2 Form Prerequisite and Silent Failure Recovery

**Target EDPM rule type**:

- hidden prerequisite detection
- submit-failure diagnosis
- local recovery without blind repeated clicking

这里保留 shopping 作为主站点，因为 `contact us` / refund 类任务最接近 failure-driven write-back 想验证的“局部前提缺失 + 表单补全 + 不盲点提交”。

| Level | Slot | Task ID | Site | Intent Template ID | Intent | Page Path |
|---|---|---:|---|---:|---|---|
| L1 | `S-FM-1` | 653 | `shopping` | 153 | Fill the "contact us" form in the site for a refund on the phone screen protector I bought, stating that it broke after just three days of use. Also, ensure to include the order number #000000180 and the product SKU. Don't submit yet, I will check. | `TBD from generated config` |
| L1 | `S-FM-2` | 654 | `shopping` | 153 | Fill the "contact us" form in the site for a refund on the bluetooth speaker I bought, stating that it broke after just three days of use. Also, ensure to include the order number #161 and the product SKU. Don't submit yet, I will check. | `TBD from generated config` |
| L2 | `S-FM-3` | 528 | `shopping` | 154 | Draft a refund message via their "contact us" form for the phone screen protector I bought March 2023. It broke after three days of use. The shop requires the order id, the reason and the amount to refund in the message. Don't submit yet | `TBD from generated config` |
| L2 | `S-FM-4` | 693 | `shopping` | 163 | Draft an email to the shop owner via their contact us function for a coupon as my refund is suppoed to be replaced by a coupon | `TBD from generated config` |
| L3 | `G-FM-1` | 658 | `gitlab` | 327 | Create an issue in a11yproject repo with title "401 bad gateway". Assign the issue to Roshanjossey. Set due date to be the end of 2030 | `TBD from generated config` |
| L3 | `R-FM-1` | 581 | `reddit` | 7 | Create a new forum named cmu_lti, with a description of Language Technologies Institute at Carnegie Mellon University, and include ['announcement', 'paper', 'alumni'] in the sidebar? | `TBD from generated config` |

### TF-3 Search, Filter, and Result Refinement

**Target EDPM rule type**:

- search-first vs navigation-first selection
- filter sequencing
- re-ground after result list refresh

| Level | Slot | Task ID | Site | Intent Template ID | Intent | Page Path |
|---|---|---:|---|---:|---|---|
| L1 | `S-SR-1` | 269 | `shopping` | 139 | Show me products under $25 in "women shoes" category | `TBD from generated config` |
| L1 | `S-SR-2` | 270 | `shopping` | 139 | Show me products under $30 in "men shoes" category | `TBD from generated config` |
| L2 | `S-SR-3` | 158 | `shopping` | 171 | I have a lot of Nintendo Switch game cards now, help me find the best storage option to fit all 11 cards | `TBD from generated config` |
| L2 | `S-SR-4` | 279 | `shopping` | 204 | Provide me with the complete names of Bluetooth headphones from Sony, and also share the price range for the available models | `TBD from generated config` |
| L3 | `M-SR-1` | 57 | `map` | 69 | Tell me the closest restaurant(s) to university center at Carnegie Mellon University | `TBD from generated config` |
| L3 | `G-SR-1` | 102 | `gitlab` | 349 | Display the list of issues in the a11yproject/a11yproject.com repository that have labels related to help needed | `TBD from generated config` |

### TF-4 State Change and Re-Grounding

**Target EDPM rule type**:

- destructive-action confirmation handling
- backend state-toggle handling
- post-action re-grounding
- stale target suppression after panel / route refresh

这里沿用 `MD` family code，但 family 名称正式收紧为 **State Change / Re-Grounding**。`shopping_admin` 现在同时覆盖 review moderation 与 product status toggle，`gitlab` 和 `map` 则提供 post-action / panel reset 场景。

最小审计结论见 [webarena-motif-audit.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena-motif-audit.md)：原先的 `SA-MD-3 / task 774` 因与 L1 共用 `intent_template_id = 246`，已降级为 `dev-only`；正式 L2 改为不同 template 的 `task 453`。

| Level | Slot | Task ID | Site | Intent Template ID | Intent | Page Path |
|---|---|---:|---|---:|---|---|
| L1 | `SA-MD-1` | 772 | `shopping_admin` | 246 | Delete all pending negative reviews for Circe fleece | `TBD from generated config` |
| L1 | `SA-MD-2` | 773 | `shopping_admin` | 246 | Delete all pending negative reviews | `TBD from generated config` |
| L2 | `SA-MD-3` | 453 | `shopping_admin` | 242 | Disable Teton pullover hoodie from the site, they are facing some quality issues. | `TBD from generated config` |
| L2 | `SA-MD-4` | 771 | `shopping_admin` | 243 | Approve the positive reviews to display in our store. | `TBD from generated config` |
| L3 | `G-MD-1` | 391 | `gitlab` | 348 | Post "close because non reproducible" for the merge request related to focus edge cases in a11yproject/a11yproject.com project | `TBD from generated config` |
| L3 | `M-MD-1` | 763 | `map` | 75 | Find the walkway to the closest Trader Joe's from 401 Shady Ave, Pittsburgh. | `TBD from generated config` |

Dev-only note:

- `task 774` (`Delete all pending reviews with less than 4 stars`) is kept only for debugging and implementation shakeout. It is no longer part of the formal L2 transfer set.

---

## 5. Recommended Pilot Size

### Minimal Pilot

| Family | L1 | L2 | L3 | Total Slots |
|---|---:|---:|---:|---:|
| TF-1 Hidden Navigation | 2 | 2 | 2 | 6 |
| TF-2 Form Recovery | 2 | 2 | 2 | 6 |
| TF-3 Search/Filter | 2 | 2 | 2 | 6 |
| TF-4 State Change / Re-Ground | 2 | 2 | 2 | 6 |
| **Total** | **8** | **8** | **8** | **24** |

### Suggested Repetition Budget

- L1 tasks: each task template run `3` times
- L2 tasks: each task template run `2` times
- L3 tasks: each target template run `2` times

这会先形成一个足够看 learning curve 的小型 pilot，而不至于把 Stage 3 卡死在 benchmark 枚举。

---

## 6. Task Naming Convention

推荐命名：

`[SiteCode]-[FamilyCode]-[Index]`

例如：

- `G-HN-1` = GitLab / Hidden Navigation / slot 1
- `S-FM-3` = Shopping / Form Recovery / slot 3
- `SA-MD-2` = Shopping Admin / state change + re-grounding / slot 2

Family code:

- `HN` = Hidden Navigation
- `FM` = Form Recovery
- `SR` = Search and Refinement
- `MD` = State Change / Re-grounding

Site code:

- `R` = `reddit`
- `S` = `shopping`
- `SA` = `shopping_admin`
- `G` = `gitlab`
- `M` = `map`
- `W` = `wikipedia`

---

## 7. Holdout and Leakage Rules

为了避免 workflow cache 伪装成 rule transfer，当前 split 必须满足：

- L2 任务与 L1 任务不能只是参数替换
- L3 任务不能复用同一站点的相同 workflow skeleton
- 同一具体页面路径不应同时出现在 memory construction 与 final transfer test

在当前 official-binding v0.2 中，进一步操作化为：

- L1：允许共享同一 `intent_template_id`，因为本来就在测 repeated-task gain
- L2：优先使用同站点不同 `intent_template_id` 的任务，只有 motif 很稀缺时才允许同模板变体
- L3：必须跨站点，且默认不复用同一 `intent_template_id`

推荐的操作性规则：

- 同一 motif 保留“相似机制，不同最终目标”
- 只允许共享 local interaction pattern，不允许共享完整 action path

---

## 8. What Counts as Positive Evidence

### For L1

- 同一任务第二次/第三次明显更稳
- 步数下降
- 失败模式减少

### For L2

- 不同任务但相同 motif 的成功率提升
- 检索到的 rule 与新任务局部问题高度匹配

### For L3

- 不同站点下仍命中相同 interaction archetype
- 提升虽小于 L1/L2，但稳定为正

---

## 9. What Would Invalidate the Split

以下情况说明当前 split 设计太弱：

- L2 任务本质只是 L1 的参数替换
- L3 任务只在表面 UI 相似，但 interaction mechanism 完全不同
- 一个 family 的 target task 需要的是完全不同的 capability，而不是同类 procedural rule

出现这些情况时，应优先修改任务池，而不是急着修改方法。

---

## 10. Stage 3 Exit Status

截至当前版本，Stage 3 所需的最小 benchmark grounding 已经具备：

1. 24 个 pilot slots 已绑定到真实 `task_id / site / intent / intent_template_id`
2. `page path` 明确保留为 `TBD from generated config`
3. `shopping_admin` 已作为真实 official site 替代早期 draft 里的泛化 `CMS`
4. `wikipedia` 被明确降级为下一阶段扩展项，而非当前阻塞项
5. 最小版 `motif-hit + anti-leakage` 审计已完成，见 [webarena-motif-audit.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena-motif-audit.md)

需要保留的严格备注：

- `TF-1` 到 `TF-4` 当前 formal pilot 均通过最小审计
- `task 774` 已降级为 `dev-only`，不再计入正式 L2 transfer claim

## 11. Deferred TODOs for the Next Phase

以下事项应**保留**，但不再阻塞当前 Stage 3 完成度判断：

1. 解析 generated config，把 `__MAP__`、`__GITLAB__`、`__SHOPPING__`、`__SHOPPING_ADMIN__` 展开为真实 page path。
2. 对 24 个已绑定 task 做一次 browser walkthrough，验证它们是否真的命中当前定义的 interaction motif。
3. 对 L2/L3 做 stronger leakage audit，确认没有共享过强的 workflow skeleton；重点从 route-level 再验证新引入的 `task 453`。
4. 视 pilot 结果决定是否把 `wikipedia` 引入 TF-3 或跨站组合任务，作为 Stage 4 扩展。
5. 把当前 binding 继续细化成 execution-ready 实验配置表，补 evaluator type、login state、storage state 与 generated page path。
