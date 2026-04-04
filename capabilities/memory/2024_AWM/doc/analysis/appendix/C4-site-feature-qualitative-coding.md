# Appendix C4. Site-Feature Qualitative Coding from Source Materials

> Purpose: derive site-feature observations from source materials themselves, rather than reverse-engineering evidence for prewritten claims.
>
> This appendix is meant to support or challenge the qualitative rows in `§10.1` of [mechanism-analysis.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/mechanism-analysis.md), especially:
> - `WF specificity`
> - `Task diversity`
>
> Primary sources:
> - workflow texts in `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/*_offline_wf.txt`
> - [wf_text_compare_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/wf_text_compare_output.txt)
> - [step_breakdown_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/step_breakdown_output.txt)
> - case-study files in `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/case_studies/`
>
> Boundary:
> - This is a qualitative coding memo, not a hard quantitative appendix.
> - The goal is to surface what the source materials actually show about site structure and task-family alignment.

## C4.1 Coding questions

Instead of starting from the paper’s conclusions, this appendix asks four source-driven questions:

1. **How specific is the workflow library?**
   - Does it mostly encode reusable sub-routines, or end-to-end task scripts?
   - Does it rely on placeholders or concrete values?

2. **How broad is the observed task family at evaluation time?**
   - Across the case studies and workflow failures/successes, do tasks cluster around one operational family, or span unrelated site functions?

3. **How aligned are workflow families and observed task families?**
   - Even if a workflow library is abstract, does it cover the dominant task family seen in evaluation?

4. **What mechanism implication follows?**
   - Is AWM likely to help through reusable guidance, fail through mismatch, or contribute little because baseline headroom is small?

## C4.2 Coding dimensions

The following labels are used as qualitative summaries:

- **WF specificity**
  - `Low`: mostly short parameterized primitives
  - `Medium`: mixed primitives plus narrow domain patterns
  - `High`: long or strongly task-family-specific sequences

- **Observed task-family breadth**
  - `Low`: tasks mostly stay within one narrow operational family
  - `Medium`: tasks vary, but still share a dominant site interaction pattern
  - `High`: tasks span multiple unrelated functional areas

- **WF-task alignment**
  - `Strong`: workflows clearly target the dominant eval task family
  - `Partial`: workflows cover only part of the observed task family
  - `Weak`: workflows and eval task families visibly diverge

## C4.3 Site-by-site source observations

### Kayak

**Workflow-text observations**

- The offline workflow file contains short reusable primitives:
  - `Enter Location for Car or Hotel Search`
  - `Select Travel Dates`
  - `Select One-Way Flight`
  - `Select Hotel Filters`
  - `View and Select Deals`
- Most workflows are 1 to 4 steps and heavily parameterized:
  - `{your-location}`
  - `{start-date}`
  - `{filter}`
  - `{best-popup-option}`
- This is consistent with [wf_text_compare_output.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/wf_text_compare_output.txt), where kayak LM workflows are short and placeholder-heavy.

**Observed eval-task observations**

- Positive cases cover:
  - hotel search with amenity constraints
  - cheap flights from NYC to London
  - Hawaii package selection
- Across these cases, the dominant pattern is still a travel-search pipeline:
  - enter location
  - pick date
  - filter or sort
  - choose a deal

**Coding**

- WF specificity: `Low`
- Observed task-family breadth: `Medium`
- WF-task alignment: `Strong`

**Mechanism implication**

Kayak looks like the cleanest case where abstract sub-routines line up with a diverse but still coherent search-oriented task family. This supports the claim that reusable workflows help when variation happens inside one stable interaction grammar.

### Newegg

**Workflow-text observations**

- The offline workflow file is still fairly abstract, but less purely primitive than kayak:
  - `search_and_apply_filters`
  - `search_and_sort_items`
  - `shopping_cart_management`
  - `build_custom_pc`
  - `custom_pc_finder`
- Some workflows are generic search/filter modules; others are narrower feature flows (`build_custom_pc`, `custom_pc_finder`).
- `wf_text_compare_output.txt` still shows the LM version as abstract relative to rule induction, but the workflow family is more commerce-specific than kayak’s travel primitives.

**Observed eval-task observations**

- Positive cases include:
  - projector search
  - gaming desktop search
  - cart-related operations
  - bluetooth mouse sorting
- These tasks vary, but the interaction family remains recognizably e-commerce:
  - search
  - filter
  - sort
  - cart management

**Coding**

- WF specificity: `Medium-Low`
- Observed task-family breadth: `Medium`
- WF-task alignment: `Strong`

**Mechanism implication**

Newegg still supports reusable workflow guidance, but in a narrower commerce grammar than kayak. This helps explain why both LM and Rule can be competitive here: the task family is varied enough to benefit from abstractions, yet stable enough that some concrete routines still transfer.

### Budget

**Workflow-text observations**

- The offline workflow file mixes several distinct site functions:
  - rental location search
  - vehicle/extras selection
  - pickup/return dates
  - reservation lookup
  - careers search
  - deals/offers browsing
- Several workflows are more end-to-end and function-specific than kayak/newegg:
  - `search_for_job_in_usa_finance`
  - `find_and_view_reservation`
  - `learn_about_deals_and_offers`
- This makes the library not just longer on average, but also more functionally fragmented.

**Observed eval-task observations**

- Negative and positive cases together show tasks spanning:
  - insurance policy certificates
  - car-for-sale browsing
  - rental booking
  - finance job search
  - road-trip ideas / travel content
- The observed task family is therefore much broader than a single rental-booking loop.

**Coding**

- WF specificity: `High`
- Observed task-family breadth: `High`
- WF-task alignment: `Weak`

**Mechanism implication**

Budget is the clearest source-based example where the workflow library is internally fragmented and the observed eval tasks span unrelated functional areas. This supports a mismatch interpretation more strongly than a simple “workflow count too small” story.

### Sixflags

**Workflow-text observations**

- The offline workflow file is short and park-centric:
  - `select_park`
  - `browse_ticket_options`
  - `buy_group_tickets`
  - `select_event_options`
  - `find_park_information`
- These workflows are not highly specific in the same sense as budget; instead, they are shallow templates around park navigation and purchase flows.
- The file suggests a narrow operational grammar rather than a broad feature library.

**Observed eval-task observations**

- Case studies show tasks involving:
  - park security policy
  - buying a single day pass
  - financial statements
  - park hours
  - VIP tour confirmation
- So the observed eval task family is not simply “park and ticket variants only.” It includes both on-family park-navigation tasks and out-of-family informational/financial tasks.

**Coding**

- WF specificity: `Medium`
- Observed task-family breadth: `Medium`
- WF-task alignment: `Partial to Weak`

**Mechanism implication**

Sixflags does not fit a simple “low task diversity” story. A better source-based description is:

- the workflow library is **narrow and park-centric**
- the eval tasks are **mixed**, including both park/ticket flows and out-of-family information tasks
- baseline CLICK is already relatively strong, so the narrow workflow family adds little headroom and can become harmful when it overfires

## C4.4 Comparative summary table

| Site | WF specificity | Observed task-family breadth | WF-task alignment | Source-based reading |
|---|---|---|---|---|
| `kayak` | Low | Medium | Strong | Abstract travel-search primitives line up with a coherent search-oriented task family |
| `newegg` | Medium-Low | Medium | Strong | Commerce workflows are still reusable; site grammar is stable enough that both LM and Rule can compete |
| `budget` | High | High | Weak | Workflow library mixes several function-specific families; eval tasks span unrelated site functions |
| `sixflags` | Medium | Medium | Partial to Weak | Workflow library is narrow and park-centric, but eval tasks are more mixed than the current正文 label suggests |

## C4.5 What this appendix supports

This appendix strongly supports:

- `kayak` and `newegg` as sites where reusable workflow families align with observed task families
- `budget` as the clearest heterogeneity/mismatch case
- `sixflags` as a site where **narrow workflow family + limited headroom + partial mismatch** is a better explanation than simply “low task diversity”

This appendix does **not** fully support:

- a strong claim that `sixflags` has low task diversity
- a strong claim that `WF specificity` alone explains success/failure

## C4.6 Implication for `mechanism-analysis.md`

If `§10.1` keeps the current qualitative rows, the safest mapping is:

- `kayak`:
  - `WF specificity = 参数化、模块化`
  - `Task diversity = 高（但共享同一搜索语法）`
- `newegg`:
  - `WF specificity = 参数化、模块化`
  - `Task diversity = 中高（但共享同一电商语法）`
- `budget`:
  - `WF specificity = 高度特化`
  - `Task diversity = 高 / 异质`
- `sixflags`:
  - `WF specificity = 泛而浅的 park-centric 模板`
  - `Task diversity` 最好不要直接写“低”
  - 更稳妥的写法是：`任务族以 park/ticket 为主，但评测中存在明显 out-of-family 信息/财务任务`

## C4.7 Safe wording in正文

The safest wording is:

> “Budget is the clearest heterogeneity case, while Sixflags is better described as having a narrow park-centric workflow family with only partial alignment to the observed eval tasks, rather than simply low task diversity.”

This wording is closer to the source materials than the earlier shorthand labels.
