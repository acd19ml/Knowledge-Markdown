# A Reproduction Study of Agent Workflow Memory on Mind2Web

**Author:** Li Mengxiao  
**Date:** April 2026

---

## Abstract

Agent Workflow Memory (AWM) is a representative approach for equipping LLM-based web agents with reusable procedural knowledge extracted from past trajectories. The original paper presents AWM as a broadly effective memory mechanism, reporting substantial gains on Mind2Web and WebArena and emphasizing the value of abstract LM-induced workflows. We present a **Mind2Web-focused reproduction study** of AWM with step-level and case-level analysis. Rather than stopping at aggregate score comparison, the study evaluates the paper's main Mind2Web claims and then traces the method's effects through step-level decomposition, a 475-step paired-case analysis, first-run target-site result tracing, workflow text comparison, and manually verified prompt-level case studies.

The strongest support is found for the paper's **mechanistic** claims rather than its broadest **performance** claims. We confirm that LM-induced workflows are consistently more abstract than rule-induced workflows at the text level, that prompt-level code and text workflows behave similarly, and that induced workflow libraries are compact and low-overlap. In contrast, in our first-run evidence, offline AWM is mixed rather than uniformly superior across seven sites, online AWM does not become stronger under larger distribution shift, and the claim that natural-language observations are generally better than HTML is not supported in the three-site evaluation.

The main contribution of this report is to explain **why** AWM helps on some sites and harms on others. On positive-outcome sites, workflow produces zero negative interventions; on negative-outcome sites, negative interventions substantially outnumber positive ones. AWM's actual influence window is narrow, changing behavior on only 6–18% of steps through specific mechanisms: strategy redirection, value format correction, and premature termination prevention on matched sites; domain misdirection, template step-skipping, and workflow-first behavior on mismatched sites. We identify eight boundary conditions not discussed in the original paper and summarize a mechanism-consistent interpretive framework connecting workflow induction quality, task-workflow semantic match, and sparse step-level intervention to aggregate outcomes.

The most defensible conclusion is that, on Mind2Web, AWM is best understood as a **conditionally effective prompting mechanism** rather than a uniformly reliable memory method. Its core idea survives reproduction better than its strongest performance narrative.

---

## 1. Introduction

### 1.1 Background

Large language model web agents often solve tasks in a stateless manner: each episode is treated as independent, and the agent discards the procedural patterns it just discovered. Human web users, by contrast, accumulate reusable know-how: where search boxes usually live, how date selection interfaces behave, when to browse versus when to search, and how to recognize repeated UI motifs.

Agent Workflow Memory (AWM), proposed by Wang et al. (2024), aims to endow web agents with this kind of reusable procedural guidance. The core idea is simple: induce workflows from successful trajectories, store them as reusable memory, and inject them back into the prompt on future tasks. The paper evaluates AWM in two modes:

- **Offline AWM**, where workflows are induced from annotated training examples before test time.
- **Online AWM**, where workflows are induced incrementally from the agent's own successful test-time trajectories in a streaming fashion.

The original paper reports a 24.6% relative improvement in step success rate on Mind2Web and a 51.1% relative improvement in task success rate on WebArena, with further gains under cross-website and cross-domain generalization.

### 1.2 Why Deep Reproduction Is Needed

For AWM, a shallow reproduction would be inadequate. Matching a few aggregate numbers cannot answer the most important questions:

1. Does the method really work across tasks, websites, and domains?
2. If it works, what exact step-level mechanism produces the gains?
3. If it fails, under what boundary conditions does it fail?

These are especially important because AWM makes several ambitious claims at once:

- Workflows can be abstracted from experience.
- Those workflows transfer across related tasks.
- Online induction becomes especially useful under larger distribution shift.
- Natural-language environment descriptions outperform HTML.
- Compact workflow libraries can still be highly useful.

We therefore adopt a deeper reproduction strategy: first verify the main claims, then explain the mechanisms, and finally identify the boundary conditions.

### 1.3 Research Objectives

Our study proceeds in three stages:

- **Layer 1: Reproduction of Main Claims.** Do the paper's main Mind2Web claims hold under independent reproduction?
- **Layer 2: Mechanism Explanation.** Through what specific mechanisms does AWM improve or degrade step-level agent behavior?
- **Layer 3: Boundary Identification.** What trade-offs, failure modes, and conditional patterns are left unclear or unreported in the original paper?

### 1.4 Scope

This study is restricted to **Mind2Web** and reports **first-run results only**.

- The main evidence base is **Mind2Web only**.
- All positive / negative / mixed judgments are **first-run judgments**.
- The paper's `AWM_AS` action-space extension experiment is **not covered**.
- Alignment-rate analysis is used only as an **exploratory heuristic**, not as a strong semantic metric.

These limits are deliberate. They reduce overclaiming and make the status of each conclusion explicit.

### 1.5 Main Contributions

Relative to a typical reproduction report, this study contributes:

1. A **site-level reproduction analysis** of the paper's main Mind2Web claims.
2. A **step-level decomposition** of AWM's effects by action type and trajectory position, revealing that gains are driven by narrow, site-dependent interventions rather than uniformly distributed step-level help.
3. A **475-step paired-case analysis** that quantifies when workflows help, hurt, do nothing, or are unnecessary, showing that AWM's actual influence window covers only 6–18% of steps.
4. **Six manually verified prompt-level case studies** tracing both positive and negative workflow mechanisms to specific workflow–action correspondences under explicit causal limits.
5. An **offline-vs-online trade-off analysis** that concretizes a verbal claim in the original paper.
6. A **failure taxonomy and interpretive framework** that qualifies where AWM is conditionally effective and where it becomes harmful.

---

## 2. Related Work

### 2.1 Web Agent Benchmarks

Web-agent evaluation has evolved from constrained environments like MiniWoB (Shi et al., 2017) and MiniWoB++ (Liu et al., 2018) to more realistic benchmarks. WebShop (Yao et al., 2022) provides a simulated e-commerce site with crowdsourced instructions. WebArena (Zhou et al., 2024) integrates five websites with execution-based functional correctness evaluation. Mind2Web (Deng et al., 2023) emphasizes broad coverage across tasks, websites, and domains, with step-level evaluation metrics including element accuracy, action F1, and step success rate. Our reproduction focuses exclusively on Mind2Web because its explicit cross-task, cross-website, and cross-domain evaluation splits make it especially suitable for testing AWM's generalization claims.

### 2.2 Memory and Experience Reuse in LLM Agents

Several approaches have explored equipping LLM agents with memory beyond the current episode. Synapse (Zheng et al., 2024) retrieves relevant training examples as trajectory-level context. AutoGuide (Fu et al., 2024) generates and selects state-aware guidelines. Voyager (Wang et al., 2024a) maintains a growing library of executable skills in an open-ended embodied setting. AWM occupies a distinctive point in this design space: it learns **prompt-level workflow memories** rather than retrieving full trajectories or executing code-level skills.

This makes AWM particularly interesting as a test case for two broader questions:

- Can language models induce reusable procedural abstractions from trajectory data?
- Can those abstractions actually improve future execution rather than merely serving as descriptive summaries?

### 2.3 Workflow Abstraction and Procedural Reuse

The idea of extracting reusable procedures from experience has roots in program synthesis and library learning (Ellis et al., 2023; Grand et al., 2023; Bowers et al., 2023). In the agent context, the key question is whether LM-based induction can produce workflows that are simultaneously abstract enough to generalize across tasks and grounded enough to improve step-level execution. AWM tests this by comparing LM-based induction (which abstracts away example-specific values using placeholders) against rule-based induction (which preserves complete concrete trajectories).

### 2.4 Reproduction as Mechanistic Analysis

Traditional ML reproduction focuses on matching aggregate metrics. Recent work has recognized the need for deeper reproduction practices that go beyond score tables: decomposing results by subgroup, tracing gains to specific model behaviors, and identifying boundary conditions (Dodge et al., 2019; Bouthillier et al., 2019). Our study adopts this stronger standard, using step-level decomposition, paired-case analysis, and prompt-level case studies as complementary evidence modalities.

---

## 3. The AWM Method

### 3.1 Problem Setting

A web navigation agent equipped with an LLM backbone *L* and text-based memory *M* (initially containing built-in action documentation) solves tasks specified by natural language instructions. At each time step, the agent observes the current page state and generates an action. AWM augments this loop by inducing reusable workflows from past experiences and injecting them into *M*.

### 3.2 Workflow Representation

Each workflow consists of two components: (1) a natural language description summarizing the workflow's high-level goal, and (2) a series of step templates, each containing an environment state description, a reasoning trace, and an executable action. Critically, LM-induced workflows replace example-specific values with parameterized placeholders (e.g., `{search-term}` instead of "dry cat food"), enhancing cross-task reusability.

### 3.3 Offline Induction

When annotated training examples are available, AWM operates in offline mode. All training examples for a given website are concatenated into a single prompt, and the LM extracts common sub-routines as workflows. These workflows are frozen before test time and injected uniformly into the prompt for all test examples. The method's promise here is that workflows induced from training data should be abstract enough to transfer to unseen tasks on the same site.

### 3.4 Online Induction

Without training examples, AWM operates in online mode. The agent processes test queries sequentially; after each task, an LM-based evaluator judges success. Successful trajectories are used to induce new workflows, which accumulate in memory for subsequent tasks. This creates a snowball effect: later tasks benefit from workflows induced from earlier successes. The paper presents this as especially useful under larger distribution shift because the workflows are derived from test-time rather than training-time experience.

### 3.5 Rule-Induction Baseline

As an ablation, the paper proposes rule-based induction, which extracts each unique experience's action sequence directly without abstraction. This produces complete concrete trajectory copies rather than parameterized sub-routines, serving as a comparison point for isolating the contribution of LM-based abstraction.

### 3.6 Mind2Web Evaluation Protocol

On Mind2Web, each task has a fixed number of steps. Per-step evaluation measures:

- **Element Accuracy** — whether the correct page element is selected
- **Action F1** — whether the action on that element is correct
- **Step Success Rate (SR)** — whether both element and action are correct
- **Task Success Rate** — whether all steps in a task succeed

The benchmark provides three evaluation splits: **cross-task** (same website, different tasks), **cross-website** (same domain, different website), and **cross-domain** (different domain entirely).

---

## 4. Experimental Setup and Analysis Protocol

### 4.1 Evaluated Claims

We evaluate five groups of claims from the Mind2Web portion of the paper:

| Setting | Paper Claim | Evaluation in This Study |
|--------|-------------|-------------------------|
| **Offline cross-task memory** | Offline AWM improves cross-task Step SR | Offline workflow vs. no-workflow on 7 websites |
| **Online cross-site generalization** | Online AWM generalizes under larger distribution gap | Online workflow on cross-task (kayak), cross-website (tripadvisor), cross-domain (reddit) |
| **LM vs. rule induction** | LM induction outperforms rule induction | LM vs. rule workflow on 3 websites (newegg, united, kayak) |
| **Representation ablations** | Code/text difference is small; NL > HTML observation | Code/text on kayak; NL/HTML on 3 websites |
| **Workflow quality** | Compact workflow libraries with high utility and low overlap | Workflow text analysis on 3 websites |

### 4.2 Models and Data

The experiments use **GPT-4o** and **Qwen-3.5-397B-A17B** (referred to as Qwen throughout) on Mind2Web. The evaluated sites include kayak, newegg, united, budget, sixflags, yellowpages, and kohls, plus cross-site targets Tripadvisor and Reddit for the online generalization setting.

### 4.3 Analysis Methods

To go beyond aggregate score comparison, we use four complementary analysis tools.

#### 4.3.1 Step-Level Decomposition

We decomposed the workflow-minus-baseline delta along three dimensions:

- **By action type** (CLICK / TYPE / SELECT): isolates whether gains come from element grounding or action/value guidance.
- **By step position** (first half / second half): tests whether workflow helps at task initiation or throughout the trajectory.
- **By website**: contrasts reproduced vs. not-reproduced sites.

#### 4.3.2 Paired-Case Analysis

For each step in each task, we classified the baseline–workflow pair into four categories:

| Category | Baseline | +Workflow | Interpretation |
|----------|----------|-----------|---------------|
| **Positive** | 0 | 1 | Workflow genuinely helped |
| **Negative** | 1 | 0 | Workflow caused harm |
| **Ineffective** | 0 | 0 | Workflow made no difference |
| **Redundant** | 1 | 1 | Workflow was unnecessary |

This produces a distribution that reveals how many steps are actually affected by workflow injection and whether the net effect is positive or negative.

#### 4.3.3 Prompt-Level Case Study

Selected paired cases are traced back to raw JSON prompts and action outputs. This allows mechanism interpretation at the case level: whether the output change is causally attributable to a specific workflow instruction.

#### 4.3.4 Auxiliary Analyses

We additionally use first-run target-site result tracing, workflow-text comparison, an exploratory alignment heuristic, a direct offline-vs.-online comparison, and prefix-level online learning curves to sharpen the main reproduction findings.

---

## 5. Reproduction Results

### 5.1 Main Reproduction Findings

**Table 1. Summary of main reproduction findings.**

| Claim | Evidence Base | Main Finding |
|-------|----------------|--------------|
| **Offline cross-task memory**: Offline AWM improves cross-task Step SR | Mind2Web first run | Mixed; positive on 2/7 sites, negative on 2/7 sites, and mixed on 3/7 sites |
| **Online cross-site generalization**: Online AWM generalizes under larger gap | Mind2Web first run | Overall direction unsupported |
| **LM vs. rule induction**: LM induction outperforms rule induction | Mind2Web first run | Text-level difference strongly supported; performance advantage mixed |
| **Representation ablations**: Code/text similar; NL > HTML | Mind2Web first run | Code/text supported on kayak; NL > HTML not supported after a three-site evaluation |
| **Workflow quality**: Compact, high-utility, low-overlap library | Mind2Web first run | Supported under prompt-level proxy; utility proxy remains loose |

This already reveals an asymmetry: the paper's **mechanistic and structural** claims hold up better than its strongest **performance and generalization** claims.

### 5.2 Offline AWM on Cross-Task Generalization

The offline story is mixed rather than uniformly positive. Some sites benefit, some degrade, and some remain genuinely mixed.

#### 5.2.1 Step-Level Decomposition by Action Type

**Table 2. Step-level delta by action type (offline_wf − no_workflow, GPT-4o, cross-task).**

| Website | Outcome | CLICK ΔElem | CLICK ΔSR | TYPE ΔActF1 | TYPE ΔSR |
|---------|---------|------:|------:|------:|------:|
| kayak | positive | +10.7% | +10.7% | +1.4% | +0.0% |
| newegg | positive | +9.1% | +6.1% | +50.0% | +33.3% |
| united | mixed | +0.0% | +0.0% | +19.5% | +28.6% |
| budget | negative | **−12.1%** | **−12.1%** | +8.4% | +9.1% |
| sixflags | negative | **−6.1%** | **−6.1%** | +0.0% | +0.0% |

**TYPE-side value guidance is the most stable positive effect.** Even on negative-outcome sites, TYPE Action F1 improves (budget +8.4%). Workflows provide value templates — city names, search keywords, price ranges — that help the model choose correct input values regardless of site match quality.

**CLICK-side grounding is the main source of divergence across sites.** Positive-outcome sites show +9–11% CLICK Element Accuracy gains; negative-outcome sites show −6 to −12% degradation. Workflow-provided element descriptions help when they match the target HTML structure and actively mislead when they do not. CLICK performance is the primary factor separating positive and negative outcomes. Appendix A1 provides the underlying step-level summary behind these action-type claims.

#### 5.2.2 Step-Level Decomposition by Trajectory Position

**Table 3. Step SR delta by trajectory half (offline_wf − no_workflow, GPT-4o, cross-task).**

| Website | Outcome | First Half ΔSR | Second Half ΔSR |
|---------|---------|------:|------:|
| kayak | positive | +0.0% | **+13.0%** |
| newegg | positive | +4.4% | +7.1% |
| budget | negative | −1.9% | **−10.9%** |
| sixflags | negative | −5.9% | −3.3% |

Workflow effects accumulate over the trajectory. On kayak, the entire gain comes from the second half (+13% vs. +0%). On budget, degradation worsens in the second half (−10.9% vs. −1.9%). AWM is not merely a "first-step hint" — its influence grows as the trajectory lengthens, amplifying either help or harm.

#### 5.2.3 Paired-Case Distribution

**Table 4. Paired-case distribution (GPT-4o, cross-task, 475 paired steps across 7 sites).**

| Website | Outcome | Positive | Negative | Ineffective | Redundant | Net |
|---------|---------|------:|------:|------:|------:|------:|
| kayak | positive | 3 | **0** | 22 | 23 | +3 |
| newegg | positive | 5 | **0** | 56 | 26 | +5 |
| united | mixed | 3 | 2 | 35 | 23 | +1 |
| budget | negative | 6 | **12** | 53 | 28 | −6 |
| sixflags | negative | 3 | **6** | 23 | 32 | −3 |

Three patterns emerge:

1. **On positive-outcome sites, workflow never harms the agent** (negative = 0). AWM either helps or does nothing, but never misleads. This "do no harm" property is the key precondition for AWM to work.
2. **On negative-outcome sites, negative interventions substantially outnumber positive ones.** Budget shows 12 negative vs. 6 positive; sixflags shows 6 vs. 3. When the workflow does not match the target site, it becomes a net source of harm.
3. **AWM's actual influence window is narrow.** Ineffective steps constitute 45–65% of all steps. Workflow genuinely changes model behavior on only 6–18% of steps. The aggregate Step SR improvement is driven by a small number of decisive interventions, not by uniform all-step guidance.

Appendix A2 records the corrected 475-step paired-case totals used in this subsection.

### 5.3 Online AWM Under Larger Distribution Shift

This is the clearest challenge to the paper's global narrative.

#### 5.3.1 Cross-Site Results

**Table 5. Online workflow paired-case results on cross-site targets (Qwen).**

| Target Site | Positive | Negative | Net | Pos/(Pos+Neg) |
|-------------|------:|------:|------:|------:|
| tripadvisor | 4 | **18** | **−14** | 18.2% |
| reddit | 2 | **5** | **−3** | 28.6% |

The paper claims that "online AWM shows larger advantage under larger distribution gap." Our first-run results show the opposite: online workflows produce net negative outcomes on both target sites, with tripadvisor suffering particularly severe degradation.

#### 5.3.2 Cross-Site Degradation Diagnosis

Two competing hypotheses were tested:

- **Hypothesis A (Workflow-content mismatch):** Workflows from kayak encode operational patterns that do not apply to the target site's navigation structure.
- **Hypothesis B (Observation/candidate quality):** The target site's HTML structure causes ground-truth elements to fall outside the candidate set, degrading all conditions equally.

**Table 6. First-run target-site result tracing.**

| Target Site | Descriptive Reading | Key Evidence |
|-------------|-------------------|----------|
| tripadvisor | first-run underperformance with weaker baseline candidate quality | Skip rate +16pp; 14/18 negatives are CLICK |
| reddit | first-run underperformance without obvious baseline collapse | Skip rate only +4.7pp; baseline CLICK EA higher than source; 4/5 negatives are CLICK |

**The safest reading is a result-level one.** In the current first run, online workflows underperform baseline on both target sites. On tripadvisor, the result trace also shows weaker baseline candidate quality. Appendix A3 summarizes these first-run facts, and Appendix B6 provides a manually verified prompt-level case in which workflow memory is already present when the wrong first action is produced. These materials should be read as result tracing and case-level evidence, not as standalone causal proof.

### 5.4 LM-Induced vs Rule-Induced Workflows

This is the strongest explanatory finding in the study.

#### 5.4.1 Text-Level Differences

**Table 7. Workflow text features: LM vs. rule induction.**

| Feature | kayak LM | kayak Rule | newegg LM | newegg Rule | united LM | united Rule |
|---------|------:|------:|------:|------:|------:|------:|
| Workflow count | 8 | 17 | 6 | 19 | 6 | 24 |
| Total steps | 14 | 213 | 10 | 149 | 16 | 217 |
| Avg steps/WF | **1.8** | 12.5 | **1.7** | 7.8 | **2.7** | 9.0 |
| Placeholders | **13** | 0 | **6** | 0 | **15** | 0 |
| Concrete values | 0 | **25** | 0 | **16** | 0 | **41** |

LM-induced workflows are consistently more abstract at the text level: fewer (6–8 vs. 17–24), shorter (1.7–2.7 vs. 7.8–12.5 steps/WF), fully parameterized, and contain zero concrete values. All four text-level indicators confirm the paper's abstraction narrative on all three sites (see the appendices on LM-vs.-rule text evidence, concrete-value counting, and workflow counting conventions).

#### 5.4.2 Performance-Level Qualification

However, textual abstraction does not automatically translate to performance superiority.

**Table 8. LM vs. rule net paired gains (Qwen, cross-task).**

| Website | LM Net Gain | Rule Net Gain | Direction |
|---------|------:|------:|------|
| newegg | +2 | +4 | Rule ≥ LM |
| united | +1 | −2 | LM > Rule |
| kayak | 0 | −1 | LM ≥ Rule |

On newegg, where cross-task operational patterns are relatively fixed (search → filter → sort → cart), rule workflows' concrete values happen to match the test tasks well. For newegg, the evidence therefore remains mixed. On united, where task diversity is higher, LM's abstraction provides clearer benefit. The paper reports only the aggregate LM > Rule conclusion without discussing this boundary condition.

### 5.5 Representation Ablations

#### 5.5.1 Code vs Text Workflow

On kayak (Qwen), code and text workflows perform similarly (Step SR difference: 2.2pp), consistent with the paper's claim that format itself is not the decisive factor. However, both perform below the no-workflow baseline (51.2%), so the stronger implied reading that both formats are reliably beneficial is only directionally supported.

#### 5.5.2 NL vs HTML Observation

**Table 9. Step SR by observation representation (Qwen, three sites).**

| Site | desc_only | html_only | desc_html | Paper Prediction |
|------|------:|------:|------:|------|
| kayak | 45.3 | 48.0 | 50.3 | NOT supported |
| newegg | **30.5** | 23.9 | 30.3 | Supported |
| united | 55.9 | **60.6** | 51.7 | NOT supported |

The paper's claim that NL descriptions are generally superior to HTML is not supported in the three-site evaluation. Only NewEgg supports it. On United, html_only is best — likely because United's HTML element names are inherently readable (e.g., `tab TRAVEL INFO`, `heading Check-in`). The mixed representation (desc_html) causes the most severe degradation on united: task SR drops from 33.3% to 16.7%, consistent with attention dilution from increased prompt length and redundancy.

**The broader takeaway is that representation preference is site-dependent, not globally uniform.** Appendix A4 collects the first-run result table behind this subsection.

### 5.6 Workflow Quality

Under current proxy definitions, the paper's workflow-quality story is broadly supported: workflow libraries are compact (5–7 LM workflows per site), overlap is low (0–3.33%), and prompt-level utility is high (100% injection rate).

But this must be reported carefully. Prompt-level utility is not the same as behavior-level adherence. When paired-case evidence is taken into account, AWM's actual causal reach is much sparser than a naive reading of "high utility" would suggest. The gap between "workflow is present in the prompt" and "workflow changes the model's behavior" is large: only 6–18% of steps show actual behavioral change. Appendix A5 gives the workflow-quality table and its proxy limitations.

---

## 6. Mechanistic Analysis

### 6.1 Where the Gains Come From

The most stable gain channel is **TYPE-side value guidance**. Workflows help the model supply the correct kind of parameter, value format, or label target. This channel remains positive even on sites where AWM is overall harmful.

The more fragile channel is **CLICK-side grounding**. This channel works only when workflow language matches the site's operational structure. On a matched site, it is helpful; on a mismatched site, it becomes a source of false anchoring.

### 6.2 Sparse Intervention Rather Than Uniform Guidance

The paired-case analysis shows that workflow is not exerting continuous control. Most steps are ineffective or redundant. AWM should not be understood as "guiding the entire trajectory." It is better understood as a **sparse intervention mechanism** that occasionally changes high-leverage decisions.

### 6.3 Prompt-Level Positive Mechanisms

Six manually verified case studies (three positive, three negative) were traced back to raw JSON prompts. All six have been confirmed against the original data files. Representative positive cases are shown in Appendices B1 and B2.

#### P-1: Preventing Premature Termination (kayak, task 1, step 9)

**Task:** "Find the cheapest Hawaii package for two adults from June 18 to 21"

| | Baseline | Workflow |
|---|---|---|
| step_success | 0 | **1** |
| Model output | Empty pred_act; outputs natural language summary about car rental (hallucination) | `CLICK [57318]` (Sort by Cheapest) |
| Failure mode | Model hallucinates task completion, outputs ungrounded text | — |

**Mechanism:** Workflow 8 (`View and Select Deals`) prompts "HOVER/CLICK to view deals on the results page," preventing premature termination.

#### P-2: Strategy Redirection (newegg, task 4, step 0)

**Task:** "Find a new drone priced between 25 to 50 dollar and ships from USA..."

| | Baseline | Workflow |
|---|---|---|
| step_success | 0 | **1** |
| Model output | `CLICK [10463]` (Electronics category navigation) | `TYPE [126] [drone]` (search box) |
| Failure mode | Defaults to "browse categories" strategy | — |

**Mechanism:** `search_and_apply_filters` workflow's first step is `[searchbox] Search Site → TYPE: {search-term}`, redirecting from "browse-first" to "search-first" strategy.

#### P-3: Value Format Correction (newegg, task 5, step 3)

**Task:** "Find bluetooth vertical mouse with most reviews and add two to my shopping cart."

| | Baseline | Workflow |
|---|---|---|
| step_success | 0 | **1** |
| Model output | `SELECT [112591] [5]` (numeric index) | `SELECT [112591] [Most Reviews]` (string label) |
| Failure mode | Correct element, wrong value format | — |

**Mechanism:** `search_and_sort_items` workflow uses `SELECT: {Sorting criterion}` with human-readable labels, guiding the model to output label strings rather than numeric indices.

### 6.4 Prompt-Level Negative Mechanisms

Representative negative cases are shown in Appendices B4, B5, and B6.

#### N-1: Out-of-Domain Workflow Misdirection (budget, task 0, step 0)

**Task:** "View the Emergency Sickness Plan policy certificates for Connecticut."

| | Baseline | Workflow |
|---|---|---|
| step_success | **1** | 0 |
| Model output | `CLICK [128]` (Reservations) | `TYPE [1326] [08817]` (zip code in location search) |
| Failure mode | — | Workflow encodes car-rental search routine; task requires insurance navigation |

**Mechanism:** `search_and_select_location` workflow redirects the agent to type a location in a search box, jumping over the correct navigation path.

#### N-2: Full-Domain Misdirection (sixflags, task 2, step 0)

**Task:** "Show the balance sheet and cash flow statement for fiscal year 2021 of Six Flags."

| | Baseline | Workflow |
|---|---|---|
| step_success | **1** | 0 |
| Model output | `CLICK [103]` (Investors link) | `CLICK [1042]` (Browse the Parks Below) |
| Failure mode | — | All 5 sixflags workflows are park/ticket navigation; none covers Investors/financial |

**Mechanism:** `select_park` workflow's first step `[button] Browse the Parks Below → CLICK` matches a visible on-page button, and the model executes it instead of reasoning toward the correct Investors link.

#### N-3: Template Step-Skipping (sixflags, task 1, step 5)

**Task:** "Buy a single day pass to Six Flags, Magic Mountain."

| | Baseline | Workflow |
|---|---|---|
| step_success | **1** | 0 |
| Model output | `CLICK [46822]` (select date) | `CLICK [47084]` (Book Now link) |
| Failure mode | — | Workflow compresses actual UI flow into 2 steps, skipping date selection |

**Mechanism:** `browse_ticket_options` workflow has only 2 steps (CLICK Tickets → CLICK option), omitting the intermediate date-selection step. The model maps its current state to the workflow's later step and jumps ahead.

### 6.5 Mechanism Synthesis

The positive mechanisms share a common structure: workflow provides the **correct operational mode** at a critical decision point (search rather than browse, label rather than index, continue rather than stop). The negative mechanisms share a different structure: workflow provides an **inapplicable operational mode** that the model follows instead of reasoning independently.

Case-level evidence is consistent with a "workflow-first" behavioral tendency — the model appears to preferentially follow workflow instructions over independent reasoning when both are available. This should be interpreted as suggestive case-level evidence rather than a demonstrated universal law.

### 6.6 Unified Causal Model

The findings integrate into a five-stage interpretive chain. (The compiled PDF includes a TikZ figure of this model; the schematic below is an equivalent ASCII summary.)

```
[Workflow Induction Quality]
   │
   ├──→ [Reusability] ──→ ┐
   │    (short/parameterized?)   │
   │                    ▼
   │              ┌─────────────┐
   │              │  Task-WF    │     [Baseline Headroom]
   │              │  Semantic   │ ←── (CLICK acc ~65-72%?)
   │              │  Match      │
   │              └─────┬───────┘
   │                    │
   │           match ──→ │ ←── mismatch
   │                    │
   │    ┌───────────────┼───────────────┐
   │    ▼               │               ▼
   │ [Positive]         │         [Negative]
   │  · strategy        │          · domain
   │    redirection     │            misdirection
   │  · value format    │          · step skipping
   │    correction      │          · workflow-first
   │  · termination     │            behavior
   │    prevention      │
   │    │               │               │
   │    ▼               ▼               ▼
   │ positive steps  ineffective    negative steps
   │ (6-18%)         (45-65%)       (4-19%)
   │    │               │               │
   │    └───────┬───────┘───────┬───────┘
   │            ▼               ▼
   │     [Aggregate SR]   [Accumulation]
   │                      · matched: 2nd half +13%
   │                      · mismatched: 2nd half -11%
   └──────────────────────────────────────────→ [Final Outcome]
```

**Table 10. Paper narrative vs. observed mechanism.**

| Paper Narrative | Observed Mechanism | Evidence Level |
|----------------|-------------------|---------------|
| AWM is broadly effective | Conditionally effective: requires workflow reusability + baseline headroom | SOFT (4-site post-hoc) |
| Online AWM superior under larger gap | Current first-run target-site results do not reproduce that trend | HARD |
| Workflow provides "high-level guidance" | Workflow changes behavior on a small fraction of steps via specific mechanisms | HARD |
| LM induction better than rule | Abstractness advantage depends on task-train divergence | HARD (text) + SOFT (performance) |
| High utility rate | Prompt-level utility high; behavioral adherence much lower | HARD + exploratory |

---

## 7. Offline vs Online Trade-Off

The original paper verbally frames offline and online induction as a trade-off, but does not operationalize that distinction. **Our results sharpen this contrast.**

**Table 11. Offline vs. online mechanism comparison on kayak.**

| Delta vs. no_workflow | CLICK ΔSR | TYPE ΔActF1 | TYPE ΔSR |
|-----------------------|------:|------:|------:|
| offline_wf | +10.7% | +1.4% | +0.0% |
| online_wf | +7.1% | +19.2% | +16.7% |

- **Offline workflows** look like a broad operation library induced from training data. On kayak, they are stronger on CLICK-side grounding. They contain general travel-search primitives (`enter location`, `select travel dates`, `select hotel filters`).
- **Online workflows** look like compressed routines induced from recent trajectories. On kayak, they are stronger on TYPE/value guidance. They contain narrower, trajectory-shaped routines (`search_for_cars_kayak`, `select_location_kayak`).

This means offline vs online should not be interpreted as a simple ranking:

- Offline is **broader and steadier**, at least in the current kayak first-run contrast.
- Online is **more test-proximate** on kayak, but the additional target-site readings should be treated as exploratory context rather than a standalone mechanism proof.

That is a much more precise reading than simply saying "online helps more under larger gap." Appendix A7 collects the supporting trade-off evidence.

---

## 8. Small-Data Efficiency

The paper implies that online memory can become useful with only a small number of examples. The current evidence suggests that this is **conditionally true**.

**Table 12. Online workflow prefix-level Step SR deltas.**

| Site | Earliest Positive Prefix | Best Prefix | Final Prefix |
|------|--------------------------|-------------|-------------|
| kayak | budget=1, +5.00pp | budget=5, +5.63pp | +5.63pp |
| tripadvisor | none | best still negative | −11.74pp |
| reddit | budget=10, +2.02pp | budget=10, +2.02pp | −2.16pp |

- On kayak, a real early gain appears after just one induced example.
- On tripadvisor, there is no early gain at any prefix — the first induced example already introduces bias.
- On reddit, the signal is delayed and unstable.

The right conclusion is not that the small-data story is simply false, but that it is **conditional in the current first-run evidence**. Early gains appear on kayak, but the same prefix-level pattern is not reproduced on tripadvisor or reddit. Appendix A8 provides the prefix-level evidence block.

---

## 9. Site Features, Reusability, and Composition

### 9.1 Structural Comparison

**Table 13. Site-level structural comparison.**

| Dimension | kayak (positive outcome) | newegg (positive outcome) | budget (negative outcome) | sixflags (negative outcome) |
|---|---|---|---|---|
| Step SR delta | +6.3% | +5.7% | −6.1% | −4.7% |
| Baseline CLICK acc | 71.4% | 66.7% | 63.8% | 73.5% |
| AWM CLICK delta | +10.7% | +6.1% | −12.1% | −6.1% |
| Avg steps/WF | 2.1 | 3.2 | 5.8 | 3.6 |
| WF-task alignment | Strong | Strong | Weak | Partial to Weak |

The qualitative coding behind these structural rows is documented in the appendix on site-feature qualitative coding.

### 9.2 Alignment Rate (Exploratory)

An exploratory keyword-overlap heuristic measuring workflow-target surface alignment yields a counter-intuitive pattern:

**Table 14. Alignment rate vs. cross-task outcome.**

| Site | Alignment Rate | Cross-task Outcome |
|------|------:|------|
| budget | 97.2% | negative |
| sixflags | 94.2% | negative |
| newegg | 90.9% | positive |
| kayak | 70.6% | positive |

Surface alignment does not show a positive monotonic relation with success. Budget and sixflags have high surface alignment because their workflow templates cover common action-type keywords — but the test tasks involve different semantic instances of those keywords. Newegg (90.9%, positive outcome) is an explicit exception to any "higher alignment = worse" story. This metric is exploratory and should not be treated as a causal indicator. Appendix A6 documents the heuristic and its boundary conditions.

### 9.3 Working Hypothesis: Dual-Condition Success

Based on the first-run four-site evidence, we propose a working hypothesis (not a validated rule):

> AWM effectiveness ≈ f(Workflow Reusability × Baseline Improvement Headroom)

Both conditions appear necessary:

1. **Workflow reusability**: Short, parameterized sub-routines that can match multiple test tasks. Kayak/NewEgg satisfy this (2–3 steps/WF, fully parameterized); budget does not (5.8 steps/WF, domain-specific sequences).
2. **Baseline improvement headroom**: Sites where baseline CLICK accuracy is in the mid-range, indicating room for element-grounding assistance. SixFlags (73.5% baseline CLICK) already performs well without help.

This is a post-hoc observation from four sites, not a validated threshold.

### 9.4 Compositionality on Mind2Web

The paper highlights workflow composition as a key capability, showing how simple workflows combine into more complex ones on WebArena. On Mind2Web, our reading of the workflow texts reveals a flatter picture:

- **Explicit hierarchical composition** (one workflow calling another): not observed in any Mind2Web workflow file.
- **Flat subflow reuse** (tasks completed by chaining short reusable routines): clearly present on kayak and united, where 1–4 step parameterized primitives can be flexibly combined.
- **Template bundling** (long, site-specific sequences serving as reusable units only in a weak sense): visible on budget.

On Mind2Web, AWM shows signs of subflow reuse mainly as a flat library of reusable routines, not as explicit hierarchical workflow composition. This makes the paper's composition narrative partially visible but considerably weaker and flatter than the WebArena-based narrative suggests. The appendix on Mind2Web compositionality provides the source-based reading behind this interpretation.

---

## 10. Failure Taxonomy

The analysis identifies a richer failure taxonomy than the paper discusses.

**Table 15. Failure taxonomy.**

| Failure Mode | Description | Severity | Source |
|-------------|-------------|----------|--------|
| **Workflow mismatch** | Workflow template does not apply to current step, redirecting agent away from correct action | High | Section 5.2, 6.4 |
| **Target-site first-run underperformance** | Current target-site results show wrong early action patterns and weaker candidate quality in some settings; this remains result tracing rather than standalone mechanism proof | High | Section 5.3 |
| **Cumulative misdirection** | Workflow harm amplifies in the second half of trajectories | Medium | Section 5.2.2 |
| **Over-specificity** | Rule workflows preserve too many source-site concrete values | Medium | Section 5.4.2 |
| **Representation noise** | Mixed desc_html representation increases prompt length and dilutes attention | Medium | Section 5.5.2 |
| **Workflow ineffectiveness** | Workflow exists but does not affect model output (45–65% of steps) | Low | Section 5.2.3 |
| **SKIP-step inflation** | Ground truth elements absent from candidates, inflating failure counts across all conditions | Structural | Section 5.2 |
| **Limited coverage** | 5–7 abstract workflows cannot cover all test-step operation types | Structural | Section 5.6 |

These failures are not all the same type. Some come from workflow mismatch, some from candidate quality, some from sparse coverage, and some from prompt-structure effects. The paper does not discuss any of them.

---

## 11. Overall Assessment

### 11.1 Main Supported Findings

The strongest supported conclusions are:

- LM-induced workflows are more abstract than rule-induced ones (4/4 text-level indicators, all three sites).
- Prompt-level code and text workflow representations behave similarly on the tested site.
- Workflow libraries are compact and low-overlap.
- On matched sites, workflows genuinely improve local step-level execution with zero negative interventions.

### 11.2 Main Unsupported Claims

The current Mind2Web evidence does not support:

- Online AWM becoming stronger under larger distribution gap.
- Natural-language observations being generally better than HTML.
- A uniformly site-robust reading of AWM.

### 11.3 What Becomes More Precise

After reproduction, the paper's broadest claims can be rewritten more carefully:

- AWM is not uniformly effective; it is **conditionally effective**.
- Workflow usefulness is sparse rather than pervasive, changing behavior on only 6–18% of steps.
- Online memory is not broadly superior under shift; it is **more test-proximate but more brittle**.
- Abstraction helps, but only under the right operational-divergence conditions.
- AWM's gains come from specific mechanisms (strategy redirection, value guidance, termination prevention), not from generic "high-level operational guidance."

---

## 12. Threats to Validity

This study has four main limitations.

1. **Mind2Web only.** The paper also reports WebArena results, which are outside the present scope. Some of the paper's stronger narratives (especially around workflow composition) are primarily supported by WebArena evidence.

2. **First-run judgments.** The current positive / negative / mixed decisions are informative but are not repeated-trial estimates with variance bounds. "Unsupported" should be read as "unsupported in the current first-run setting," not as "definitively false."

3. **No AWM_AS coverage.** The paper's action-space extension branch (Section 5, Table 9) is not covered. This is a scope limitation of the current study rather than a contradictory finding.

4. **Exploratory alignment rate.** The alignment-rate measure is based on keyword overlap, not semantic matching. It is suitable for generating hypotheses but not for causal claims.

These limitations should be understood as reporting discipline, not as hidden caveats.

---

## 13. Conclusion and Future Work

### 13.1 Summary

This deep reproduction supports a more qualified picture of AWM than the original paper presents.

The method has a real mechanism. Reusable workflows can improve step-level decisions, especially through TYPE-side value guidance and matched CLICK-side grounding. LM-induced workflows are genuinely more abstract than rule-induced ones, and workflow libraries are indeed compact. These are substantive, reproducible aspects of the paper's story.

At the same time, in the current first-run evidence, the reproduction does not support the strongest version of the paper's performance narrative. Online AWM does not become more reliable under larger distribution shift on the tested Mind2Web settings. The NL-over-HTML claim also does not generalize in the three-site evaluation. AWM's gains are sparse, site-dependent, and highly contingent on workflow–task match.

The most defensible final judgment is therefore:

**AWM is a plausible and interpretable prompting mechanism, but not a uniformly reliable memory method. Its core idea survives reproduction better than its strongest universality claims.**

That is precisely what a critical reproduction should reveal.

### 13.2 Future Work

1. **Repeated trials with variance estimation.** Converting first-run judgments into statistically grounded conclusions requires multiple runs with different random seeds and confidence intervals.

2. **Failure-driven workflow revision.** AWM currently has no mechanism for revising or retracting workflows that cause harm. A write-back loop that detects harmful patterns and modifies or removes offending workflows could address the method's most severe failure mode.

3. **Semantic workflow selection.** The current approach injects all workflows uniformly. A retrieval mechanism that selects workflows based on task-workflow semantic similarity could reduce mismatch-induced harm.

4. **WebArena reproduction.** Extending the analysis to WebArena would test whether the boundary conditions identified here are Mind2Web-specific or structural properties of AWM.

5. **Cross-model robustness.** Testing with a wider range of backbone models would help distinguish method-level properties from model-specific behaviors.

---

## References

- Bouthillier, X., et al. (2019). Unreproducible research is reproducible. *ICML*.
- Bowers, M., et al. (2023). Top-down synthesis for library learning. *Proc. ACM Program. Lang.*, 7(POPL).
- Deng, X., et al. (2023). Mind2Web: Towards a generalist agent for the web. *NeurIPS Datasets and Benchmarks*.
- Dodge, J., et al. (2019). Show your work: Improved reporting of experimental results. *EMNLP*.
- Ellis, K., et al. (2023). DreamCoder: Growing generalizable, interpretable knowledge with wake-sleep Bayesian program learning. *Phil. Trans. Royal Society A*.
- Fu, Y., et al. (2024). AutoGuide: Automated generation and selection of state-aware guidelines for LLM agents. *arXiv:2403.08978*.
- Grand, G., et al. (2023). LILO: Learning interpretable libraries by compressing and documenting code. *arXiv:2310.19791*.
- Liu, E. Z., et al. (2018). Reinforcement learning on web interfaces using workflow-guided exploration. *ICLR*.
- Pan, J., et al. (2024). Autonomous evaluation and refinement of digital agents. *arXiv:2404.06474*.
- Shi, T., et al. (2017). World of Bits: An open-domain platform for web-based agents. *ICML*.
- Sodhi, P., et al. (2023). HEAP: Hierarchical policies for web actions using LLMs. *arXiv:2310.03720*.
- Wang, Z., Mao, J., Fried, D., & Neubig, G. (2024). Agent Workflow Memory. *arXiv*.
- Wang, G., et al. (2024a). Voyager: An open-ended embodied agent with large language models. *TMLR*.
- Yao, S., et al. (2022). WebShop: Towards scalable real-world web interaction with grounded language agents. *NeurIPS*.
- Zheng, L., et al. (2024). Synapse: Trajectory-as-exemplar prompting with memory for computer control. *ICLR*.
- Zhou, S., et al. (2024). WebArena: A realistic web environment for building autonomous agents. *ICLR*.

---

## Appendix

The full appendix is included in the LaTeX build via `appendix-content.tex`. The evidence blocks that most directly support the core claims of this report are indexed below.

**Table A-index. Appendix index.**

| ID | Title | Supports |
|----|-------|----------|
| A1 | Step-Level Breakdown | Section 5.2 |
| A2 | Paired-Case Summary | Section 5.2.3 |
| A3 | First-Run Target-Site Result Note | Section 5.3 |
| A4 | C4 Result Table | Section 5.5 |
| A5 | C5 Quality Table | Section 5.6 |
| A6 | Alignment-Rate Note (exploratory) | Section 9.2 |
| A7 | Offline vs. Online Trade-off | Section 7 |
| A8 | Online Small-Data Efficiency | Section 8 |
| B1 | Kayak Positive Case (P-1) | Section 6.3 |
| B2 | United Positive Case | Section 6.3 |
| B4 | Sixflags Negative Case (N-2) | Section 6.4 |
| B5 | Sixflags Step-Skipping Case (N-3) | Section 6.4 |
| B6 | Tripadvisor Online-Workflow Mismatch | Section 5.3, 6.4 |
| C1 | LM vs. Rule Text Evidence | Section 5.4 |
| C4 | Site-Feature Qualitative Coding | Section 9.1 |
| C5 | Mind2Web Compositionality Reading | Section 9.4 |

Markdown appendix excerpts and source-verified materials are stored under `doc/analysis/appendix/`.
