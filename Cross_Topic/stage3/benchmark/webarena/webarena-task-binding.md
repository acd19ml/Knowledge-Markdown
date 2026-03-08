# WebArena Task Binding

> **Status**: Official-binding v0.1
> **Role**: Stage 3 pilot slots 到 WebArena 官方 task 的正式映射表
> **Primary Source**: [test.raw.json](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/source/test.raw.json)
> **Upstream Split**: [webarena-task-split.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena-task-split.md)

---

## 1. Scope

这份表把当前 Stage 3 选中的 24 个 pilot slots，正式绑定到 WebArena 官方 `test.raw.json` 中的真实任务。

当前版本已经固定：

- `task_id`
- `site`
- `start_url` token
- `intent`
- `intent_template_id`
- `transfer level`
- `interaction motif`

当前版本仍然保留为 `TBD from generated config` 的字段：

- `page path`
- placeholder token 展开后的真实 URL

因此，这份 artifact 的定位是：**Stage 3 benchmark grounding 已完成，Stage 4 再做 generated config 级解析与 walkthrough audit**。

Formal set note:

- `task 774` has been downgraded to `dev-only` because it reused the L1 deletion template and carried avoidable L2 leakage risk.

---

## 2. Binding Table

| Family | Level | Pilot Slot | Task ID | Site | Start URL Token | Page Path | Intent Template ID | Official Goal / Intent | Interaction Motif | Expected EDPM Rule | Notes |
|---|---|---|---:|---|---|---|---:|---|---|---|---|
| TF-1 Hidden Navigation | L1 | `G-HN-1` | 448 | `gitlab` | `__GITLAB__` | `TBD from generated config` | 331 | set the homepage URL on my GitLab profile to https://egg.tart.com | hidden navigation / profile settings | discover profile-setting entry and re-ground inside nested account surface | repeated-task anchor on same template |
| TF-1 Hidden Navigation | L1 | `G-HN-2` | 449 | `gitlab` | `__GITLAB__` | `TBD from generated config` | 331 | set the homepage URL on my GitLab profile to https://helloworld.xyz | hidden navigation / profile settings | discover profile-setting entry and re-ground inside nested account surface | repeated-task variant |
| TF-1 Hidden Navigation | L2 | `G-HN-3` | 480 | `gitlab` | `__GITLAB__` | `TBD from generated config` | 293 | Invite yjlou as collaborator to solarized-prism-theme | hidden member-management path discovery | move from profile editing to repo/member settings navigation | same-site, different template |
| TF-1 Hidden Navigation | L2 | `G-HN-4` | 533 | `gitlab` | `__GITLAB__` | `TBD from generated config` | 330 | Follow ['convexegg', 'yjlou'] on Gitlab | secondary action discovery from user pages | locate non-primary social action after navigation and re-ground | same-site, different target surface |
| TF-1 Hidden Navigation | L3 | `SA-HN-1` | 486 | `shopping_admin` | `__SHOPPING_ADMIN__` | `TBD from generated config` | 275 | Change the page title of "404 Not Found" page on my site to "Bruh bro you clicked the wrong page". | hidden admin page discovery / settings navigation | transfer nested-settings discovery from SaaS profile to admin backoffice | cross-site admin transfer |
| TF-1 Hidden Navigation | L3 | `SA-HN-2` | 489 | `shopping_admin` | `__SHOPPING_ADMIN__` | `TBD from generated config` | 275 | Change the page title of "Privacy Policy" page on my site to "No privacy policy is needed is this dystopian world". | hidden admin page discovery / settings navigation | transfer nested-settings discovery from SaaS profile to admin backoffice | cross-site admin transfer variant |
| TF-2 Form Recovery | L1 | `S-FM-1` | 653 | `shopping` | `__SHOPPING__` | `TBD from generated config` | 153 | Fill the "contact us" form in the site for a refund on the phone screen protector I bought, stating that it broke after just three days of use. Also, ensure to include the order number #000000180 and the product SKU. Don't submit yet, I will check. | form prerequisite completion / silent failure avoidance | recover missing fields by diagnosing local prerequisites before submit | repeated-task anchor |
| TF-2 Form Recovery | L1 | `S-FM-2` | 654 | `shopping` | `__SHOPPING__` | `TBD from generated config` | 153 | Fill the "contact us" form in the site for a refund on the bluetooth speaker I bought, stating that it broke after just three days of use. Also, ensure to include the order number #161 and the product SKU. Don't submit yet, I will check. | form prerequisite completion / silent failure avoidance | recover missing fields by diagnosing local prerequisites before submit | repeated-task variant |
| TF-2 Form Recovery | L2 | `S-FM-3` | 528 | `shopping` | `__SHOPPING__` | `TBD from generated config` | 154 | Draft a refund message via their "contact us" form for the phone screen protector I bought March 2023. It broke after three days of use. The shop requires the order id, the reason and the amount to refund in the message. Don't submit yet | contact-form drafting with hidden requirements | generalize prerequisite completion from form filling to message drafting | same-site, different template |
| TF-2 Form Recovery | L2 | `S-FM-4` | 693 | `shopping` | `__SHOPPING__` | `TBD from generated config` | 163 | Draft an email to the shop owner via their contact us function for a coupon as my refund is suppoed to be replaced by a coupon | contact-form exception handling | adapt form strategy when refund path changes to coupon path | same-site exception variant |
| TF-2 Form Recovery | L3 | `G-FM-1` | 658 | `gitlab` | `__GITLAB__` | `TBD from generated config` | 327 | Create an issue in a11yproject repo with title "401 bad gateway". Assign the issue to Roshanjossey. Set due date to be the end of 2030 | structured creation form with prerequisites | transfer field-completion and local validation to issue creation surface | cross-site form-heavy transfer |
| TF-2 Form Recovery | L3 | `R-FM-1` | 581 | `reddit` | `__REDDIT__` | `TBD from generated config` | 7 | Create a new forum named cmu_lti, with a description of Language Technologies Institute at Carnegie Mellon University, and include ['announcement', 'paper', 'alumni'] in the sidebar? | multi-field creation form | transfer prerequisite completion to forum-creation workflow | cross-site form-heavy transfer |
| TF-3 Search/Refinement | L1 | `S-SR-1` | 269 | `shopping` | `__SHOPPING__` | `TBD from generated config` | 139 | Show me products under $25 in "women shoes" category | search / filter / refinement | sequence category selection and price filtering without losing grounding | repeated-task anchor |
| TF-3 Search/Refinement | L1 | `S-SR-2` | 270 | `shopping` | `__SHOPPING__` | `TBD from generated config` | 139 | Show me products under $30 in "men shoes" category | search / filter / refinement | sequence category selection and price filtering without losing grounding | repeated-task variant |
| TF-3 Search/Refinement | L2 | `S-SR-3` | 158 | `shopping` | `__SHOPPING__` | `TBD from generated config` | 171 | I have a lot of Nintendo Switch game cards now, help me find the best storage option to fit all 11 cards | search-first vs navigation-first selection | pick search/retrieval strategy based on constraint-bearing product lookup | same-site, different template |
| TF-3 Search/Refinement | L2 | `S-SR-4` | 279 | `shopping` | `__SHOPPING__` | `TBD from generated config` | 204 | Provide me with the complete names of Bluetooth headphones from Sony, and also share the price range for the available models | search / brand filter / result summarization | refine result list while maintaining brand and attribute constraints | same-site, different template |
| TF-3 Search/Refinement | L3 | `M-SR-1` | 57 | `map` | `__MAP__` | `TBD from generated config` | 69 | Tell me the closest restaurant(s) to university center at Carnegie Mellon University | spatial search / result refinement | transfer refinement rule to map search and nearest-result grounding | cross-site utility transfer |
| TF-3 Search/Refinement | L3 | `G-SR-1` | 102 | `gitlab` | `__GITLAB__` | `TBD from generated config` | 349 | Display the list of issues in the a11yproject/a11yproject.com repository that have labels related to help needed | repository search / label filter | transfer refinement to issue-list filtering under textual constraints | cross-site SaaS transfer |
| TF-4 State Change / Re-Ground | L1 | `SA-MD-1` | 772 | `shopping_admin` | `__SHOPPING_ADMIN__` | `TBD from generated config` | 246 | Delete all pending negative reviews for Circe fleece | destructive action / confirmation / re-ground | handle destructive moderation flow and re-ground after state change | repeated-task anchor |
| TF-4 State Change / Re-Ground | L1 | `SA-MD-2` | 773 | `shopping_admin` | `__SHOPPING_ADMIN__` | `TBD from generated config` | 246 | Delete all pending negative reviews | destructive action / confirmation / re-ground | handle destructive moderation flow and re-ground after state change | repeated-task variant |
| TF-4 State Change / Re-Ground | L2 | `SA-MD-3` | 453 | `shopping_admin` | `__SHOPPING_ADMIN__` | `TBD from generated config` | 242 | Disable Teton pullover hoodie from the site, they are facing some quality issues. | backend state toggle / save / re-ground | generalize post-action re-grounding from review moderation to product-status update | same-site, different template |
| TF-4 State Change / Re-Ground | L2 | `SA-MD-4` | 771 | `shopping_admin` | `__SHOPPING_ADMIN__` | `TBD from generated config` | 243 | Approve the positive reviews to display in our store. | state-changing moderation / re-ground | re-ground after non-destructive but state-changing admin action | same-site state-change variant |
| TF-4 State Change / Re-Ground | L3 | `G-MD-1` | 391 | `gitlab` | `__GITLAB__` | `TBD from generated config` | 348 | Post "close because non reproducible" for the merge request related to focus edge cases in a11yproject/a11yproject.com project | action confirmation / comment-and-return | transfer re-grounding after action into MR discussion surface | cross-site SaaS transfer |
| TF-4 State Change / Re-Ground | L3 | `M-MD-1` | 763 | `map` | `__MAP__` | `TBD from generated config` | 75 | Find the walkway to the closest Trader Joe's from 401 Shady Ave, Pittsburgh. | route panel reset / post-action re-ground | transfer post-action re-grounding to map result panel updates | cross-site utility transfer |

---

## 3. Coverage Summary

| Family | L1 | L2 | L3 | Total |
|---|---:|---:|---:|---:|
| TF-1 Hidden Navigation | 2 | 2 | 2 | 6 |
| TF-2 Form Recovery | 2 | 2 | 2 | 6 |
| TF-3 Search/Refinement | 2 | 2 | 2 | 6 |
| TF-4 State Change / Re-Ground | 2 | 2 | 2 | 6 |
| **Total** | **8** | **8** | **8** | **24** |

Site coverage:

- `gitlab`: 7 tasks
- `shopping`: 8 tasks
- `shopping_admin`: 6 tasks
- `reddit`: 1 task
- `map`: 2 tasks

Template coverage:

- Repeated-template anchors are intentionally preserved in L1 for repeated-task evaluation.
- L2 tasks are mostly shifted to different `intent_template_id` values to reduce literal replay.
- L3 tasks are cross-site by construction.

---

## 4. Deferred TODOs

这些事项保留到下一阶段，不阻塞当前 Stage 3：

1. 解析 generated config，把 `start_url` token 展开成真实 URL / page path。
2. 对 24 个 tasks 做 browser walkthrough，确认任务确实命中当前定义的 interaction motif。
3. 对 L2/L3 做一次 leakage audit，确认没有共享过强的 workflow skeleton。
4. 若后续 pilot 发现 `reddit` 在 TF-1 覆盖过弱，可考虑引入 `wikipedia` 或改配新的 cross-site target。
5. 若实验实现需要，可再补 evaluator type、login state、storage state 等 execution 字段。
