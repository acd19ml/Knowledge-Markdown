# WebArena Paper Extraction

> **Source PDF**: [WEBARENA.pdf](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/source/WEBARENA.pdf)
> **Extraction Date**: 2026-03-08
> **Method**: `pdfplumber` text extraction
> **Related Files**:
> - [webarena_extracted.txt](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena_extracted.txt)
> - [webarena_extracted_clean.txt](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena_extracted_clean.txt)

---

## 1. Extraction Status

### What Was Successfully Extracted

- 全文 `22` 页
- 主文 `§1-§7`
- Appendix `A.1-A.10`
- benchmark 规模、任务模板、任务类别、评测机制、环境重置、用户角色模拟

### Visual Check Status

- 已成功渲染首页预览到：
  [page1.png](/Users/mac/studyspace/Knowledge-Markdown/tmp/pdfs/webarena_preview/page1.png)
- 当前环境缺少 `pdfinfo / pdftoppm / pdftotext`，所以没有走 Poppler 路线
- 但 `pdfplumber` 抽取对这篇 paper 已足够支撑 benchmark facts 提取

### Important Limitation

这篇 paper **没有提供官方 task id 列表或逐任务 page path 清单**。它给了：

- benchmark 设计原则
- 任务模板数量
- 网站与用户角色配置
- 评测方式

但**不足以单靠论文正文把 pilot slot 绑定到真实官方 task id**。后续若要做精确 task binding，仍需要官方 task list / repo 配置文件。

---

## 2. Bibliographic Metadata

- **Title**: WebArena: A Realistic Web Environment for Building Autonomous Agents
- **Venue**: ICLR 2024
- **Authors**: Shuyan Zhou, Frank F. Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng, Tianyue Ou, Yonatan Bisk, Daniel Fried, Uri Alon, Graham Neubig
- **Project URL**: [https://webarena.dev/](https://webarena.dev/)
- **Paper Length**: 22 pages in extracted PDF

---

## 3. Core Benchmark Facts

### 3.1 Environment Goal

WebArena is presented as a **realistic and reproducible** web environment for evaluating language-guided autonomous agents. The key claim is that prior environments were either too synthetic, too static, or too weak in functional correctness evaluation.

### 3.2 Website Inventory

The environment contains four primary website categories:

- **E-commerce**
- **Social forum**
- **Collaborative software development**
- **Content management system**

Plus several utility and knowledge sites:

- **Map**
- **Calculator**
- **Scratchpad**
- **Wikipedia**
- **site manuals / documentation**

### 3.3 Concrete Implementations

From Appendix `A.1`, the paper states:

- Shopping site built as **OneStopShop** using Adobe Magento
- Social forum built from **Postmill**, serving as a Reddit-like environment
- Development platform built from **GitLab**
- CMS adapted from **Adobe Magento admin portal**
- Map service from **OpenStreetMap**
- Offline **English Wikipedia** hosted through **Kiwix**

### 3.4 Dataset Scale

The benchmark contains:

- **241 templates**
- **812 instantiated intents**

Average instantiations per template:

- **3.3**

### 3.5 Human Performance / Model Performance

Main headline numbers from the paper:

- **Best GPT-4 agent**: `14.41%` end-to-end task success
- **Human performance**: `78.24%`

This is one of the main motivations for using WebArena as a hard benchmark.

---

## 4. Environment and Reproducibility Facts

### 4.1 Deterministic Delivery

Appendix `A.2` states that each website is deployed in a **separate Docker image** with:

- website code
- database
- software dependencies
- pre-populated data

The environment can be reset by restarting the original containers, which is critical for repeated-task evaluation and write-back experiments.

### 4.2 Multi-Tab Support

The observation space includes:

- current URL
- open tabs
- page content of the focused tab

This matters because WebArena explicitly supports **multi-tab tasks**, which is relevant to tool use and cross-page reasoning.

### 4.3 Observation Modalities

The paper supports three page representations:

- raw HTML / DOM
- screenshot
- accessibility tree

It also supports viewport-limited content.

### 4.4 Action Space

The core actions listed in the paper are:

- `noop`
- `click(elem)`
- `hover(elem)`
- `type(elem, text)`
- `press(key_comb)`
- `scroll(dir)`
- `tab_focus(index)`
- `new_tab`
- `tab_close`
- `go_back`
- `go_forward`
- `goto(URL)`
- `stop[answer]`

This action inventory should be mirrored when designing EDPM-compatible task logging.

---

## 5. Website-Specific Facts Useful for Stage 3

### 5.1 Reddit-Like Forum

The paper states:

- built from Postmill as a Reddit counterpart
- sampled from top 50 subreddits
- manually selected northeast US city subreddits
- manually selected ML / deep learning related subreddits
- total of `95` subreddits, `127390` posts, `661781` users

This makes Reddit useful for:

- hidden navigation
- community search / lookup
- posting / editing content
- cross-site tasks with map

### 5.2 GitLab

The paper states:

- `300` repositories
- `1000+` accounts with at least one commit
- repositories sampled to include both large and small projects

This makes GitLab useful for:

- issue / merge request navigation
- admin/settings discovery
- content/config operations
- form-heavy interactions

### 5.3 OneStopShop / E-Commerce

The paper states:

- approximately `90k` products
- `300+` product categories
- includes prices, options, descriptions, images, reviews

This makes Shopping useful for:

- search/filter refinement
- cart/checkout forms
- order history information-seeking
- prerequisite and silent-failure form motifs

### 5.4 CMS

The paper uses Adobe Magento admin portal sample data for CMS.

This makes CMS useful for:

- modal interactions
- content creation/editing
- admin navigation
- settings/configuration tasks

### 5.5 Tools and Knowledge Resources

The paper explicitly includes:

- OpenStreetMap constrained to the northeast US
- calculator
- scratchpad
- offline Wikipedia
- GitLab manual
- Adobe Commerce Merchant documentation

This matters because many WebArena tasks are intentionally **cross-site** and **knowledge-supported**.

---

## 6. Benchmark Task Design

### 6.1 Intent Collection Criteria

The paper defines three criteria for intent creation:

- intents should be **abstract and high-level**
- intents should be **creative**
- intents should be **templated**, with replaceable variables and multiple instantiations

This is directly relevant to Stage 3 because your repeated-task and same-site transfer splits should probably be organized at the **template / motif** level, not just by literal task strings.

### 6.2 Task Categories

The benchmark classifies tasks into three main categories:

- **Information-seeking**
- **Site navigation**
- **Content and configuration operation**

This taxonomy is useful, but for EDPM experiments it is still too coarse. Your current `TF-1` to `TF-4` interaction-motif split is still the right abstraction level.

### 6.3 Cross-Site Tasks

The paper explicitly includes **cross-site intents** and Figure 6 reports:

- **Cross Site** accounts for `5.9%` of the intent distribution

This means:

- same-site and cross-site are both first-class parts of WebArena
- your current `near-domain transfer` design is aligned with benchmark spirit
- but pilot experiments should still begin with same-site transfer before cross-site composition

---

## 7. Evaluation Design

### 7.1 Two Evaluation Modes

The paper defines two kinds of evaluation:

- **`r_info`**
  for information-seeking tasks where a textual answer is expected
- **`r_prog`**
  for navigation / content / config tasks where success is checked programmatically

### 7.2 `r_info` Variants

The paper uses three scoring functions:

- `exact_match`
- `must_include`
- `fuzzy_match`

`fuzzy_match` uses GPT-4 as a semantic equivalence judge for flexible answer formats.

### 7.3 `r_prog` Mechanism

For site navigation and content/config tasks, the paper programmatically evaluates success by:

- locating relevant state or page content
- querying website state / DB / JS selectors / APIs
- checking expected properties against the intent

This is especially important for Stage 3, because your EDPM experiments should prefer `r_prog`-like outcome checks wherever possible. They are less gameable than action-sequence matching.

### 7.4 Unachievable Tasks

The paper includes unachievable tasks labeled `N/A`.

This is useful context, but for the first EDPM pilot:

- these should not be central
- they are more useful later when testing failure detection and write-back calibration

---

## 8. Human Annotation and Benchmark Construction

The paper states:

- intents were contributed by the authors
- information-seeking answers were double annotated
- disagreements were resolved by a third annotator
- programmatic evaluators were implemented by authors proficient in JavaScript

The paper also reports a human evaluation sample:

- one task from each of `170` templates
- performed by five CS graduate students

This suggests that:

- the paper is benchmark-heavy and carefully validated
- but it still does **not** publish per-task binding detail in the PDF itself

---

## 9. Facts Directly Relevant to EDPM

### 9.1 Strong Alignment

WebArena is a strong fit for EDPM because it provides:

- long-horizon tasks
- realistic websites
- deterministic resets
- multi-tab support
- programmatic success checking
- templated tasks with multiple instantiations

### 9.2 Especially Relevant Evidence

The paper’s template analysis explicitly notes that tasks from the same template may:

- require similar reasoning and planning
- still have different observations and execution traces

This is exactly the kind of setting needed to distinguish:

- workflow replay
- local procedural rule reuse

### 9.3 Important Limitation for Your Use

The paper’s PDF does **not** enumerate an official public table of:

- every task id
- its exact site
- exact page path
- exact template id to task id mapping

So for Stage 3, the paper alone is enough to justify WebArena and guide split design, but **not enough to finalize official task binding**.

---

## 10. Extraction Outputs You Can Use Immediately

### Already Ready

- [webarena_extracted.txt](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena_extracted.txt)
- [webarena_extracted_clean.txt](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena_extracted_clean.txt)
- [webarena-paper-extraction.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena-paper-extraction.md)

### Ready to Use for Stage 3

- benchmark rationale
- website inventory
- action space
- evaluation design
- template-based split logic

### Still Missing for Official Task Binding

- benchmark repo task definitions
- official task list or json
- any released template-to-task mapping
- page path or route-level task metadata

---

## 11. Recommended Next Step

If you want me to continue task binding, the next best input is one of:

- WebArena benchmark repo task files
- official task json / csv
- website seed data and route definitions

拿到这些后，我就可以把 [webarena-task-split.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena-task-split.md) 往下压成真实 `task id / page path` 绑定表。
