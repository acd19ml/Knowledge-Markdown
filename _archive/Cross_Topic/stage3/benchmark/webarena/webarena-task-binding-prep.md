# WebArena Task Binding Prep

> **Status**: Draft v0.1
> **Purpose**: 在缺少官方 task json / repo task files 时，先把论文中可确认的 task-binding 相关锚点收齐
> **Sources**:
> - [webarena-paper-extraction.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/webarena-paper-extraction.md)
> - [WEBARENA.pdf](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena/source/WEBARENA.pdf)

---

## 1. What This File Can and Cannot Do

### It Can Do

- 确认 WebArena 的站点 inventory
- 确认 benchmark task 类型与 evaluator 类型
- 提取 paper 中出现过的真实 URL / route anchors
- 为 [webarena-task-split.md](/Users/mac/studyspace/Knowledge-Markdown/Cross_Topic/stage3/benchmark/webarena-task-split.md) 提供 benchmark-grounded pilot exemplars

### It Cannot Do

- 生成官方 `task id`
- 声称某个 pilot slot 已对应官方 benchmark 某一条 task
- 给出完整 page path inventory

这些仍需要 benchmark repo 或 task json。

---

## 2. Paper-Grounded Site Inventory

| Site Family | Concrete Site Mentioned in Paper | Notes |
|---|---|---|
| E-commerce | `OneStopShop` / `onestopmarket.com` | shopping site built from Adobe Magento |
| Social forum | Reddit-like site via `Postmill` | forum/community tasks |
| Collaborative development | `GitLab` | issue / MR / repo / settings tasks |
| CMS | Adobe Magento admin portal | content/config/admin tasks |
| Map | `OpenStreetMap` | northeast US constrained map tasks |
| Knowledge site | `Wikipedia` | cross-site info lookup |
| Utility | `calculator`, `scratchpad` | tool support sites |

---

## 3. URLs and Route Anchors Explicitly Appearing in the Paper

These are the strongest route-level anchors that can be cited without guessing.

| Anchor Type | Exact String in Paper | Where It Appears | Use for Stage 3 |
|---|---|---|---|
| Homepage | `http://homepage.com` | baseline agent prompt | confirms canonical hub page for cross-site navigation |
| Password page | `http://homepage.com/password.html` | baseline agent prompt | confirms credential lookup route |
| Shopping product page | `http://onestopmarket.com/office-products/office-electronics.html` | direct-agent example | confirms one concrete shopping route |
| Map page | `http://openstreetmap.org` | direct-agent example | confirms map site base route |
| GitLab merge request filter | `gitlab.com/merge_requests?assignee_username=byteblaze` | evaluation table | confirms one programmatic target route pattern |
| Reddit target path fragment | `/f/nyc` | evaluation table | confirms subreddit path fragment used in evaluator |
| Cross-site figure anchor | `webarena.wikipedia.com` | Figure 2 | confirms Wikipedia site in cross-site tasks |
| Cross-site figure anchor | `webarena.openstreetmap.com` | Figure 2 | confirms map site in cross-site tasks |
| Cross-site figure anchor | `webarena.gitlab.com` | Figure 2 | confirms GitLab site in cross-site tasks |

---

## 4. Paper-Provided Example Tasks

### Example A: Information Seeking on Shopping

- **Objective**: `What is the price of HP Inkjet Fax Machine`
- **Observed URL**: `http://onestopmarket.com/office-products/office-electronics.html`
- **Interaction Type**: information-seeking
- **Evaluation Type**: likely `r_info`
- **Value for Stage 3**:
  - good anchor for low-complexity shopping info tasks
  - not ideal as a main EDPM pilot, because it may rely too much on direct lookup rather than procedural reuse

### Example B: Search on Map

- **Objective**: `Show me the restaurants near ABC`
- **Observed URL**: `http://openstreetmap.org`
- **Interaction Type**: site navigation / search refinement
- **Evaluation Type**: likely `r_info` or hybrid answer-style evaluation
- **Value for Stage 3**:
  - useful for `TF-3 Search/Refinement`
  - good anchor for search-first interaction motifs

### Example C: GitLab Navigation via Programmatic Evaluation

- **Objective**: `Checkout merge requests assigned to me`
- **Target URL check**: `gitlab.com/merge_requests?assignee_username=byteblaze`
- **Interaction Type**: site navigation
- **Evaluation Type**: `r_prog`
- **Value for Stage 3**:
  - useful anchor for GitLab navigation and filtered-list tasks
  - good candidate family for same-site cross-task reuse

### Example D: Reddit Content Operation via Programmatic Evaluation

- **Objective**: `Post to ask “whether I need a car in NYC”`
- **Programmatic checks**:
  - URL must include `/f/nyc`
  - body must include `acarinNYC`
- **Interaction Type**: content/config operation
- **Evaluation Type**: `r_prog`
- **Value for Stage 3**:
  - useful anchor for Reddit posting flows
  - likely good for form-like submission and post-submission verification motifs

### Example E: Cross-Site Planning Task

- **Objective**: `Create an efficient itinerary to visit all of Pittsburgh's art museums with minimal driving distance starting from Schenley Park. Log the order in my “awesome-northeast-us-travel” repository`
- **Sites involved**:
  - `webarena.wikipedia.com`
  - `webarena.openstreetmap.com`
  - `webarena.gitlab.com`
- **Interaction Type**: cross-site information gathering + planning + content update
- **Evaluation Value**:
  - strong realism example
  - too compositional for first EDPM pilot
  - better reserved for later cross-site transfer checks

---

## 5. Task Categories the Paper Explicitly Defines

The paper groups tasks into:

- **Information-seeking**
- **Site navigation**
- **Content and configuration operation**

For Stage 3, these should be treated as **benchmark-level labels**, not the main experimental split. Your main split should remain interaction-motif-based:

- hidden navigation
- form prerequisite recovery
- search/filter refinement
- modal / focus reset / re-grounding

---

## 6. Evaluator Implications for Pilot Design

### Strongest Pilot-Friendly Category

`r_prog`-style tasks are the best fit for EDPM pilot because they:

- have outcome-based validation
- are less sensitive to answer wording
- better support repeated-task and cross-task comparison

### Weaker Pilot Category

Pure `r_info` tasks are still useful, but many are closer to retrieval/lookup than procedural reuse.

Recommendation:

- use `r_prog`-like site navigation and content/config tasks as the pilot core
- use selected `r_info` tasks as auxiliary cases

---

## 7. Pre-Binding Suggestions for Current Pilot Slots

These are **not official bindings**. They are benchmark-grounded suggestions based only on paper evidence.

| Pilot Family | Best Paper-Grounded Site Anchor | Confidence | Reason |
|---|---|---:|---|
| `TF-1 Hidden Navigation` | GitLab, CMS | Medium | benchmark has rich settings/admin/navigation surfaces; GitLab route filtering example exists |
| `TF-2 Form Recovery` | Reddit posting, Shopping checkout, CMS content forms | Medium | paper confirms content/config tasks and shopping/CMS sites; exact form task ids unavailable |
| `TF-3 Search/Refinement` | OpenStreetMap, Shopping, GitLab | High | paper provides explicit map search example and filtered GitLab route |
| `TF-4 Modal/Re-grounding` | CMS, GitLab | Low-Medium | sites are appropriate, but paper does not give modal-specific task examples |

---

## 8. Suggested First Binding Order Once Repo Files Arrive

1. Bind `TF-3 Search/Refinement`
   - paper evidence is strongest here
2. Bind `TF-2 Form Recovery`
   - likely present in shopping/CMS/Reddit content operations
3. Bind `TF-1 Hidden Navigation`
   - requires task-level route details
4. Bind `TF-4 Modal/Re-grounding`
   - probably needs real task traces, not just task statements

---

## 9. Concrete Next Files to Produce

As soon as official task files arrive, the next output should be:

- `webarena-task-binding.md`
  - official `task id -> pilot slot` map
- `webarena-route-anchors.md`
  - page path / URL pattern inventory
- `webarena-task-family-notes.md`
  - per-family rationale and leakage checks
