# WebArena Pilot Motif Audit

> **Status**: Minimal audit v0.1
> **Purpose**: 对 24 个 WebArena pilot tasks 做最小版 `motif-hit + anti-leakage` 审计
> **Scope**: 只使用官方 `test.raw.json` 中的 `task_id / site / intent_template_id / intent_template / intent / reference_url`
> **Parent Docs**: [webarena-task-split.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena-task-split.md), [webarena-task-binding.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena-task-binding.md)

---

## 1. Audit Rule

- **Motif-hit**
  - `Strong`: task intent directly instantiates the declared interaction motif.
  - `Acceptable`: task still exercises the same local strategy, but surface form or evaluator is less direct.
  - `Weak`: task can only be justified by a broad family label; local strategy overlap is uncertain.
- **L2 anti-leakage rule**
  - `Pass`: not the same `intent_template_id` as the L1 anchor, and not reducible to simple entity/parameter swap.
  - `Risk`: same template or near-identical action path, even if target values differ.
- **L3 anti-leakage rule**
  - `Pass`: cross-site and not plausibly the same workflow skeleton.
  - `Risk`: cross-site on paper, but still likely solvable by nearly the same ordered path.

This is intentionally a **minimal** audit. It does not replace the deferred browser walkthrough.

---

## 2. Family-by-Family Judgment

| Family | L1 anchor | L2 judgment | L3 judgment | Overall verdict |
|---|---|---|---|---|
| `TF-1 Hidden Navigation` | `448/449` on GitLab profile homepage setting | `480/533` are different templates and different target surfaces; not a parameter swap | `486/489` move to Shopping Admin page editing; still nested settings discovery, not the same GitLab path | `Pass` |
| `TF-2 Form Recovery` | `653/654` on Shopping contact form | `528/693` change template and local objective; same contact surface but not just value substitution | `658/581` shift to GitLab issue creation and Reddit forum creation; still form-heavy prerequisite handling, not the same workflow skeleton | `Pass` |
| `TF-3 Search/Refinement` | `269/270` on Shopping category + price filtering | `158/279` use different templates and different refinement goals; not a parameter swap | `57/102` are cross-site and mechanism-divergent; `57` is weaker because it is partly lookup-like, but it still tests search-first refinement | `Pass with one weak slot` |
| `TF-4 State Change / Re-Grounding` | `772/773` on Shopping Admin review deletion | `453/771` are different templates and different target objects; not a parameter swap | `391/763` are cross-site and not the same skeleton, but the family is no longer purely “destructive action” | `Pass` |

---

## 3. Slot-Level Audit

| Slot | Task ID | Site | Template ID | Motif-hit | Leakage judgment | Why |
|---|---:|---|---:|---|---|---|
| `G-HN-1` | 448 | `gitlab` | 331 | Strong | L1 anchor | hidden profile/settings navigation to edit homepage URL |
| `G-HN-2` | 449 | `gitlab` | 331 | Strong | L1 anchor | same template as `G-HN-1`, intentionally used for repeated-task reuse |
| `G-HN-3` | 480 | `gitlab` | 293 | Acceptable | L2 pass | collaborator invite uses repo/member settings discovery, not profile edit replay |
| `G-HN-4` | 533 | `gitlab` | 330 | Acceptable | L2 pass | following users shifts to user-page secondary action discovery, not a parameter swap of `448/449` |
| `SA-HN-1` | 486 | `shopping_admin` | 275 | Acceptable | L3 pass | admin page-title edit still needs hidden settings/page-location discovery on a different site family |
| `SA-HN-2` | 489 | `shopping_admin` | 275 | Acceptable | L3 pass | same as `SA-HN-1`; cross-site repeated variant is acceptable for `L3` anchor pair |
| `S-FM-1` | 653 | `shopping` | 153 | Strong | L1 anchor | canonical contact-form completion with hidden prerequisites |
| `S-FM-2` | 654 | `shopping` | 153 | Strong | L1 anchor | same template as `S-FM-1`, intentionally repeated |
| `S-FM-3` | 528 | `shopping` | 154 | Strong | L2 pass | draft-only refund message adds message composition and required fields, not a direct replay |
| `S-FM-4` | 693 | `shopping` | 163 | Acceptable | L2 pass | same contact surface, but coupon path changes local objective and expected content |
| `G-FM-1` | 658 | `gitlab` | 327 | Acceptable | L3 pass | issue creation transfers multi-field completion and prerequisite checking to GitLab |
| `R-FM-1` | 581 | `reddit` | 7 | Acceptable | L3 pass | forum creation is a different site and skeleton, but still a multi-field creation form |
| `S-SR-1` | 269 | `shopping` | 139 | Strong | L1 anchor | direct category + price filter refinement |
| `S-SR-2` | 270 | `shopping` | 139 | Strong | L1 anchor | repeated-task variant of the same filter template |
| `S-SR-3` | 158 | `shopping` | 171 | Acceptable | L2 pass | product fit search changes from fixed filter path to search-and-selection under a constraint |
| `S-SR-4` | 279 | `shopping` | 204 | Strong | L2 pass | brand-constrained search plus result summarization is not a value swap of `269/270` |
| `M-SR-1` | 57 | `map` | 69 | Weak | L3 pass | closest-place lookup is cross-site and refinement-like, but more answer-oriented than the shopping anchors |
| `G-SR-1` | 102 | `gitlab` | 349 | Strong | L3 pass | issue-list label filtering is a clean cross-site refinement task |
| `SA-MD-1` | 772 | `shopping_admin` | 246 | Strong | L1 anchor | destructive moderation flow with deletion and re-grounding |
| `SA-MD-2` | 773 | `shopping_admin` | 246 | Strong | L1 anchor | repeated-task variant of the same deletion template |
| `SA-MD-3` | 453 | `shopping_admin` | 242 | Acceptable | L2 pass | product-status toggle changes target object and admin path; still tests state change plus post-save re-grounding |
| `SA-MD-4` | 771 | `shopping_admin` | 243 | Acceptable | L2 pass | approval flow keeps post-action re-grounding but breaks away from the deletion template |
| `G-MD-1` | 391 | `gitlab` | 348 | Acceptable | L3 pass | merge-request comment action tests post-action re-grounding after state change on a different site |
| `M-MD-1` | 763 | `map` | 75 | Acceptable | L3 pass | route-panel reset is not destructive, but it is a genuine re-grounding-after-state-change case |

---

## 4. Strict Conclusions

### 4.1 What Passes Today

- `TF-1` to `TF-4` now pass the **minimal** audit for the formal pilot set.
- The current 24-task split is good enough to support Stage 3 method design and pilot planning.
- `L2` is mostly protected from trivial parameter substitution because most slots move to different `intent_template_id` values.

### 4.2 Remaining Cautions

- `TF-4` now passes the **minimal** audit after replacing the leaky L2 slot with `task 453`.
- The family is still semantically broader than pure destructive action, so the name should remain `State Change / Re-Grounding`.

### 4.3 Minimum Fix Before Final Transfer Reporting

1. Keep `SA-MD-3 / 453` and `SA-MD-4 / 771` as the formal L2 pair.
2. Keep `task 774` only as `dev-only` debugging material, not as formal transfer evidence.
3. Keep the family name as `State Change / Re-Grounding`, so `391` and `763` are not forced into an artificially destructive label.

Dev-only note:

- `task 774` (`Delete all pending reviews with less than 4 stars`) remains useful for implementation debugging, but it is excluded from the formal L2 set because it shares the same deletion template as the L1 anchors.

---

## 5. What Remains Deferred

- browser walkthrough to confirm motif-hit from actual UI traces
- generated config expansion to real page path / URL
- stronger workflow-skeleton leakage audit using concrete routes rather than task text alone
