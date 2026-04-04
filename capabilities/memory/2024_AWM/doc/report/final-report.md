# Deep Reproduction and Mechanism Audit of Agent Workflow Memory on Mind2Web

**Author:** Li Mengxiao

**Date:** April 2026

---

## Abstract

Agent Workflow Memory (AWM) is a representative method for equipping LLM-based web agents with reusable procedural knowledge extracted from past interaction trajectories. The original paper reports substantial gains on both Mind2Web and WebArena benchmarks, framing AWM as a broadly effective memory mechanism. This report presents a **Mind2Web-centered, first-run reproduction and mechanism audit** of AWM. Rather than merely checking whether aggregate scores can be replicated, we decompose AWM's effects at the step level, paired-case level, and prompt level to answer three progressively deeper questions: (1) which of the paper's five core claims hold under independent reproduction, (2) what specific mechanisms drive AWM's gains and failures, and (3) what boundary conditions, failure modes, and trade-offs does the paper leave undiscussed.

Our reproduction covers five experimental lines (C1–C5) across seven Mind2Web websites with two backbone models (GPT-4o and Qwen-3.5). Key findings include: AWM's benefits are highly site-dependent, with reproduced sites showing zero negative interventions while not-reproduced sites show negative interventions that substantially outnumber positive ones; the paper's cross-site generalization claim is not supported under our first-run evidence, with online workflows producing negative transfer on both target sites; LM-induced workflows are demonstrably more abstract than rule-induced workflows at the text level, but this abstractness does not guarantee performance superiority; and the offline–online distinction is better understood as a trade-off between breadth and test-proximity rather than a simple ranking. We identify eight boundary conditions not discussed in the original paper, supported by a 475-step paired-case analysis and six source-verified prompt-level case studies. All reproduced/not-reproduced judgments are first-run judgments under the current implementation and should be interpreted accordingly.

---

## 1. Introduction

### 1.1 Background

LLM-based agents for web navigation have progressed rapidly, yet most current approaches treat each task as an independent episode. The agent solves the current task, discards the experience, and starts fresh on the next one. This stands in contrast to how humans operate: we extract reusable know-how from past interactions—workflows, shortcuts, and heuristics—and apply them to accelerate future tasks.

Agent Workflow Memory (AWM), proposed by Wang et al. (2024), addresses this gap by inducing reusable workflow sub-routines from successful agent trajectories and injecting them into the agent's prompt as memory. AWM operates in two modes: **offline**, where workflows are induced from annotated training examples before test time; and **online**, where workflows are induced from the agent's own successful test-time trajectories in a streaming fashion. The paper reports a 24.6% relative improvement in step success rate on Mind2Web and a 51.1% relative improvement in task success rate on WebArena, with further gains under cross-website and cross-domain generalization.

### 1.2 Motivation for Deep Reproduction

AWM is a particularly important case study within the broader landscape of experience-dependent procedural knowledge for GUI agents, because it instantiates two key capabilities that the field has widely discussed but rarely verified at the mechanism level:

1. **Workflow abstraction**: Can an LLM reliably extract reusable sub-routines from raw trajectories, and does abstractness actually improve downstream performance?
2. **Cross-task transfer**: Do workflows learned from one set of tasks genuinely help on different tasks, websites, or domains?

A surface-level reproduction that merely checks whether aggregate scores match the paper's tables would not answer these questions. The field needs a deeper kind of reproduction—one that traces the paper's reported gains back to specific step-level mechanisms, identifies where and why the method fails, and maps the boundary conditions that the paper's aggregate reporting obscures.

### 1.3 Objectives

This study pursues three progressively deeper objectives, following a layered research roadmap:

- **Layer 1 (Claim Verification):** Do the paper's five core claims (C1–C5) hold under independent reproduction on Mind2Web?
- **Layer 2 (Mechanism Explanation):** Through what specific mechanisms does AWM improve or degrade agent performance at the step level?
- **Layer 3 (Boundary Identification):** What failure modes, trade-offs, and conditions does the paper not discuss?

### 1.4 Scope

This report should be read as a **Mind2Web-centered first-run reproduction and mechanism audit**. All conclusions are derived from Mind2Web experiments and should be interpreted as Mind2Web-specific evidence rather than benchmark-independent claims about AWM. The study does not include the paper's WebArena branch or the `AWM_AS` action-space extension experiment (paper §5, Table 9). All reproduced/not-reproduced judgments are first-run judgments under the current implementation rather than repeated-estimate conclusions with variance bounds. These boundaries are intentional and should be treated as part of the study's reporting discipline rather than as hidden omissions.

### 1.5 Contribution

This study goes beyond numeric reproduction by turning the paper's verbal claims into step-level, paired-case, and prompt-level evidence, and by identifying where the original AWM narrative is supported, weakened, or needs to be rewritten conditionally. Specifically:

1. A **step-level decomposition** of AWM's effects by action type (CLICK/TYPE/SELECT), step position (first half/second half), and website, revealing that gains are driven by narrow, site-dependent interventions rather than uniform all-step help.
2. A **475-step paired-case analysis** across seven websites that quantifies positive, negative, ineffective, and redundant interventions, showing that AWM's actual influence window covers only 6–18% of steps.
3. **Six source-verified prompt-level case studies** (three positive, three negative) that trace AWM's mechanisms to specific workflow–output causal paths.
4. An **offline-vs-online mechanism contrast** showing that the two modes trade off different strengths rather than forming a simple ranking.
5. A **failure taxonomy** identifying eight boundary conditions not discussed in the original paper.

---

## 2. Related Work

### 2.1 Web Agent Benchmarks

Web agent evaluation has evolved from constrained environments like MiniWoB (Shi et al., 2017) and MiniWoB++ (Liu et al., 2018) to more realistic benchmarks. WebShop (Yao et al., 2022) provides a simulated e-commerce site with crowdsourced instructions. WebArena (Zhou et al., 2024) integrates five websites with execution-based functional correctness evaluation. Mind2Web (Deng et al., 2023) emphasizes broad coverage across tasks, websites, and domains, with step-level evaluation metrics including element accuracy, action F1, and step success rate. Our reproduction focuses exclusively on Mind2Web due to its explicit cross-task, cross-website, and cross-domain evaluation splits, which allow systematic testing of AWM's generalization claims.

### 2.2 Memory and Experience Reuse in LLM Agents

Several approaches have explored equipping LLM agents with memory beyond the current episode. Synapse (Zheng et al., 2024) retrieves relevant training examples as trajectory-level context. AutoGuide (Fu et al., 2024) generates and selects state-aware guidelines. Voyager (Wang et al., 2024a) maintains a growing library of executable skills in an open-ended embodied setting. AWM differs from retrieval-based approaches like Synapse by inducing abstract sub-routines rather than retrieving concrete examples, and from skill libraries like Voyager by operating within a prompt-injection paradigm rather than an executable function paradigm.

### 2.3 Workflow Induction and Procedural Knowledge

The idea of extracting reusable procedures from experience has roots in program synthesis and library learning (Ellis et al., 2023; Grand et al., 2023; Bowers et al., 2023). In the agent context, the key question is whether LM-based induction can produce workflows that are simultaneously abstract enough to generalize across tasks and grounded enough to improve step-level execution. AWM tests this by comparing LM-based induction (which abstracts away example-specific values using placeholders) against rule-based induction (which preserves complete concrete trajectories).

### 2.4 Reproduction Methodology

Traditional ML reproduction focuses on matching aggregate metrics. Recent work has recognized the need for deeper reproduction practices that go beyond score tables: decomposing results by subgroup, tracing gains to specific model behaviors, and identifying boundary conditions (Dodge et al., 2019; Bouthillier et al., 2019). Our study adopts this deeper approach, using step-level decomposition, paired-case analysis, and prompt-level case studies as complementary evidence modalities.

---

## 3. The AWM Method

This section describes the AWM method as presented in the original paper, providing the necessary background for understanding our reproduction design.

### 3.1 Problem Setting

A web navigation agent equipped with an LLM backbone *L* and text-based memory *M* (initially containing built-in action documentation) solves tasks specified by natural language instructions. At each time step, the agent observes the current page state and generates an action. AWM augments this loop by inducing reusable workflows from past experiences and injecting them into *M*.

### 3.2 Workflow Representation

Each workflow consists of two components: (1) a natural language description *d* summarizing the workflow's high-level goal, and (2) a series of steps, each containing an environment state description, a reasoning trace, and an executable action. Critically, LM-induced workflows replace example-specific values with parameterized placeholders (e.g., `{search-term}` instead of "dry cat food"), enhancing cross-task reusability.

### 3.3 Offline Induction

When annotated training examples are available, AWM operates in offline mode. All training examples for a given website are concatenated into a single prompt, and the LM extracts common sub-routines as workflows. These workflows are frozen before test time and injected uniformly into the prompt for all test examples.

### 3.4 Online Induction

Without training examples, AWM operates in online mode. The agent processes test queries sequentially; after each task, an LM-based evaluator judges success. Successful trajectories are used to induce new workflows, which accumulate in memory for subsequent tasks. This creates a snowball effect: later tasks benefit from workflows induced from earlier successes.

### 3.5 Rule-Based Induction Baseline

As an ablation, the paper also proposes rule-based induction, which extracts each unique experience's action sequence directly without abstraction. This produces complete concrete trajectory copies rather than parameterized sub-routines, serving as a baseline to isolate the contribution of LM-based abstraction.

### 3.6 Mind2Web Evaluation Protocol

On Mind2Web, each task has a fixed number of steps. Per-step evaluation measures: (1) **Element Accuracy** — whether the correct page element is selected; (2) **Action F1** — whether the action on that element is correct; (3) **Step Success Rate** — whether both element and action are correct; (4) **Task Success Rate** — whether all steps in a task succeed. The benchmark provides three evaluation splits: **cross-task** (same website, different tasks), **cross-website** (same domain, different website), and **cross-domain** (different domain entirely).

---

## 4. Reproduction Methodology

### 4.1 Experimental Design

We designed five experimental lines (C1–C5) to cover the paper's main Mind2Web claims:

| Line | Paper Claim | Our Experimental Design |
|------|-------------|------------------------|
| **C1** | Offline AWM improves cross-task Step SR | Offline workflow vs. no-workflow on 7 websites |
| **C2** | Online AWM generalizes under larger distribution gap | Online workflow on cross-task (kayak), cross-website (tripadvisor), cross-domain (reddit) |
| **C3** | LM induction outperforms rule induction | LM vs. rule workflow on 3 websites (newegg, united, kayak) |
| **C4** | Code and text workflows perform similarly; NL > HTML observation | Code/text on kayak; NL/HTML/both on 3 websites |
| **C5** | Compact workflow libraries with high utility and low overlap | Workflow text analysis on 3 websites |

**Models**: GPT-4o and Qwen-3.5-397B-A17B (referred to as Qwen throughout).

**Websites**: kayak, newegg, united, budget, sixflags, yellowpages, kohls.

### 4.2 Analysis Methodology

Beyond aggregate score comparison, we developed three complementary analysis methods:

#### 4.2.1 Step-Level Decomposition

We decomposed the step-level delta (workflow minus baseline) along three dimensions:

- **By action type** (CLICK / TYPE / SELECT): isolates whether gains come from element grounding or action/value guidance.
- **By step position** (first half / second half): tests whether workflow helps at task initiation or throughout the trajectory.
- **By website**: contrasts reproduced vs. not-reproduced sites.

Implementation: `scripts/step_breakdown.py`.

#### 4.2.2 Paired-Case Analysis

For each step in each task, we classified the baseline–workflow pair into four categories:

| Category | Baseline | +Workflow | Interpretation |
|----------|----------|-----------|---------------|
| **Positive** | 0 | 1 | Workflow genuinely helped |
| **Negative** | 1 | 0 | Workflow caused harm |
| **Ineffective** | 0 | 0 | Workflow made no difference |
| **Redundant** | 1 | 1 | Workflow was unnecessary |

This produces a distribution that reveals how many steps are actually affected by workflow injection and whether the net effect is positive or negative.

Implementation: `scripts/paired_case.py`.

#### 4.2.3 Prompt-Level Case Study

For selected positive and negative paired cases, we opened the full JSON prompt and performed manual comparison of:

- The workflow text present in the prompt
- The model's output with vs. without workflow
- Whether the output change is causally attributable to a specific workflow instruction

This provides the strongest evidence for mechanism attribution but is limited to case-level generalization.

#### 4.2.4 Additional Analysis Scripts

| Script | Purpose |
|--------|---------|
| `cross_site_diag.py` | Diagnose cross-site degradation root cause |
| `wf_text_compare.py` | Quantify LM vs. rule workflow text features |
| `alignment_rate.py` | Compute exploratory workflow-target alignment heuristic |
| `offline_online_tradeoff.py` | Direct paired comparison of offline vs. online on kayak |
| `online_small_data_curve.py` | Reconstruct prefix-level online learning curves |

---

## 5. Results and Analysis

### 5.1 C1–C5 Reproduction Status

Table 1 summarizes the first-run reproduction status for each claim.

**Table 1. Reproduction status summary.**

| Claim | Status | Judgment |
|-------|--------|----------|
| **C1**: Offline AWM improves cross-task Step SR | First run complete | Mixed: 2/7 sites reproduced, 2/7 not reproduced, 3/7 unclear |
| **C2**: Online AWM generalizes under larger distribution gap | First run complete | Overall direction not reproduced; only kayak (test_task) positive |
| **C3**: LM induction outperforms rule induction | First run complete | Text-level abstraction difference strongly supported; performance advantage mixed |
| **C4**: Code/text similar; NL > HTML | First run complete | Code/text reproduced on kayak; NL > HTML not reproduced after three-site first run |
| **C5**: Compact library, high utility, low overlap | First run complete | Supported under prompt-level proxy; utility proxy remains loose |

The strongest support comes from C3's text-level conclusion (LM workflows are more abstract) and C5's structural properties (compact libraries with low overlap). The weakest support comes from C2's cross-site generalization claim and C4's NL-vs-HTML claim. C1's core performance claim shows insufficient stability across sites to be recorded as a blanket "reproduced."

### 5.2 C1 Mechanism Decomposition

#### 5.2.1 Step-Level Breakdown by Action Type

AWM's gains and losses decompose sharply along action type (Table 2).

**Table 2. Step-level delta by action type (offline_wf − no_workflow, GPT-4o, cross-task).**

| Website | C1 Status | CLICK ΔElem | CLICK ΔSR | TYPE ΔActF1 | TYPE ΔSR |
|---------|-----------|------:|------:|------:|------:|
| kayak | reproduced | +10.7% | +10.7% | +1.4% | +0.0% |
| newegg | reproduced | +9.1% | +6.1% | +50.0% | +33.3% |
| united | unclear | +0.0% | +0.0% | +19.5% | +28.6% |
| budget | not reproduced | **−12.1%** | **−12.1%** | +8.4% | +9.1% |
| sixflags | not reproduced | **−6.1%** | **−6.1%** | +0.0% | +0.0% |

**Finding 1: TYPE-side value guidance is the most stable benefit.** Even on not-reproduced sites, TYPE Action F1 improves (budget +8.4%). Workflows provide value templates (city names, search keywords, price ranges) that help the model choose correct input values regardless of site match quality.

**Finding 2: CLICK-side grounding is the decisive variable.** Reproduced sites show +9–11% CLICK Element Accuracy gains; not-reproduced sites show −6 to −12% degradation. This means workflow-provided element descriptions help when they match the target HTML structure and actively mislead when they do not. CLICK performance is the "swing vote" that determines whether a site is reproduced or not.

#### 5.2.2 Step-Level Breakdown by Position

**Table 3. Step SR delta by trajectory half (offline_wf − no_workflow, GPT-4o, cross-task).**

| Website | Status | First Half ΔSR | Second Half ΔSR |
|---------|--------|------:|------:|
| kayak | reproduced | +0.0% | **+13.0%** |
| newegg | reproduced | +4.4% | +7.1% |
| budget | not reproduced | −1.9% | **−10.9%** |
| sixflags | not reproduced | −5.9% | −3.3% |

**Finding 3: Workflow effects accumulate over the trajectory.** On kayak, the entire gain comes from the second half (+13% vs. +0%). On budget, degradation worsens in the second half (−10.9% vs. −1.9%). This suggests that workflows do not merely provide a "how to start" hint—their influence grows as the trajectory lengthens, amplifying both benefits and harms.

#### 5.2.3 Paired-Case Distribution

Across 475 paired steps (seven sites, GPT-4o, offline_wf vs. no_workflow):

**Table 4. Paired-case distribution by C1 status.**

| Website | C1 Status | Positive | Negative | Ineffective | Redundant | Net |
|---------|-----------|------:|------:|------:|------:|------:|
| kayak | reproduced | 3 | **0** | 22 | 23 | +3 |
| newegg | reproduced | 5 | **0** | 56 | 26 | +5 |
| budget | not reproduced | 6 | **12** | 53 | 28 | −6 |
| sixflags | not reproduced | 3 | **6** | 23 | 32 | −3 |

**Finding 4: On reproduced sites, workflow never harms the agent (negative = 0).** This is a striking pattern: AWM either helps or does nothing, but never misleads. This "do no harm" property is the key precondition for AWM to work.

**Finding 5: On not-reproduced sites, negative interventions substantially outnumber positive ones.** Budget shows 12 negative vs. 6 positive; sixflags shows 6 vs. 3. When the workflow does not match the target site, it becomes a net source of harm.

**Finding 6: AWM's actual influence window is narrow.** Ineffective steps constitute 45–65% of all steps. Workflow genuinely changes model behavior on only 6–18% of steps. The aggregate Step SR improvement reported in the paper is driven by a small number of decisive interventions, not by uniform all-step guidance.

### 5.3 Cross-Site Generalization (C2)

#### 5.3.1 Online Workflow on Target Sites

**Table 5. Online workflow paired-case results on cross-site targets.**

| Target Site | Positive | Negative | Net | Pos/(Pos+Neg) |
|-------------|------:|------:|------:|------:|
| tripadvisor (Qwen) | 4 | **18** | **−14** | 18.2% |
| reddit (Qwen) | 2 | **5** | **−3** | 28.6% |

The paper claims that "online AWM in cross-website and cross-domain shows larger advantage under larger distribution gap." Our first-run results show the opposite: online workflows produce net negative outcomes on both target sites, with tripadvisor suffering particularly severe degradation.

#### 5.3.2 Degradation Diagnosis

We tested two competing hypotheses for the cross-site degradation:

- **Hypothesis A (Workflow-content mismatch):** Workflows from kayak encode operational patterns (TYPE location → CLICK suggestion) that do not apply to the target site's navigation structure.
- **Hypothesis B (Observation/candidate quality):** The target site's HTML structure causes ground-truth elements to fall outside the candidate set, degrading all conditions equally.

**Table 6. Cross-site degradation diagnosis.**

| Target Site | Primary Hypothesis | Evidence |
|-------------|-------------------|----------|
| tripadvisor | A + B mixed | Skip rate +16pp (B); 14/18 negatives are CLICK with systematic pattern mismatch (A) |
| reddit | A (workflow mismatch) | Skip rate only +4.7pp; baseline CLICK EA actually higher than source; 4/5 negatives are CLICK |

**Finding 7: Cross-site degradation is driven primarily by workflow-content mismatch.** The typical failure pattern on tripadvisor is that workflows induce a "TYPE location first" routine inherited from kayak, but tripadvisor requires a "CLICK category link first" entry point. The workflow does not just fail to help—it actively redirects the agent away from the correct first action.

### 5.4 Offline vs. Online Trade-Off

The paper presents online AWM as generally superior under larger distribution gaps. Our analysis reveals a more nuanced trade-off.

**Table 7. Offline vs. online mechanism comparison on kayak.**

| Delta vs. no_workflow | CLICK ΔSR | TYPE ΔActF1 | TYPE ΔSR |
|-----------------------|------:|------:|------:|
| offline_wf | +10.7% | +1.4% | +0.0% |
| online_wf | +7.1% | +19.2% | +16.7% |

**Finding 8: Offline and online workflows trade off different strengths.** Offline workflows are broader and steadier on CLICK-side grounding (derived from curated training data). Online workflows are more test-proximate and stronger on TYPE/value guidance (derived from the model's own recent successful trajectories). This is a genuine trade-off rather than a simple ranking.

The workflow texts confirm this structural difference: offline workflows contain broad travel-search primitives (`enter location`, `select travel dates`, `select hotel filters`), while online workflows are narrower and more trajectory-shaped (`search_for_cars_kayak`, `select_location_kayak`). The source-proximity that helps online workflows on the source site becomes a liability under distribution shift, as the learned routines encode kayak-specific operational patterns that do not transfer.

### 5.5 Small-Data Efficiency

The paper implies that online AWM achieves gains from only a small number of successful examples. We reconstructed prefix-level learning curves from the online evaluation logs.

**Table 8. Online workflow prefix-level Step SR deltas.**

| Site | Earliest Positive Prefix | Best Prefix | Final Prefix |
|------|--------------------------|-------------|-------------|
| kayak | budget=1, +5.00pp | budget=5, +5.63pp | +5.63pp |
| tripadvisor | none | best still negative | −11.74pp |
| reddit | budget=10, +2.02pp | budget=10, +2.02pp | −2.16pp |

**Finding 9: Very-small-budget gains are conditional, not universal.** On kayak (source-style setting), one induced example already yields +5pp. On tripadvisor, no positive prefix appears at any budget—the first induced example already introduces bias. On reddit, a small positive appears only at budget 10 and then disappears. The small-data efficiency story holds only when the induced workflow matches the target task distribution.

### 5.6 LM vs. Rule Induction (C3)

#### 5.6.1 Text-Level Differences

**Table 9. Workflow text features: LM vs. rule induction.**

| Feature | kayak LM | kayak Rule | newegg LM | newegg Rule | united LM | united Rule |
|---------|------:|------:|------:|------:|------:|------:|
| Workflow count | 8 | 17 | 6 | 19 | 6 | 24 |
| Total steps | 14 | 213 | 10 | 149 | 16 | 217 |
| Avg steps/WF | **1.8** | 12.5 | **1.7** | 7.8 | **2.7** | 9.0 |
| Placeholders | **13** | 0 | **6** | 0 | **15** | 0 |
| Concrete values | 0 | **25** | 0 | **16** | 0 | **41** |

**Finding 10: LM-induced workflows are consistently more abstract at the text level.** Across all three sites, LM workflows are fewer (6–8 vs. 17–24), shorter (1.7–2.7 vs. 7.8–12.5 steps/WF), fully parameterized (6–15 placeholders vs. 0), and contain zero concrete values. This is the most strongly supported claim in the entire reproduction: 4/4 text-level indicators confirm the paper's abstraction narrative on all three sites.

#### 5.6.2 Performance-Level Qualification

However, text-level abstractness does not automatically translate to performance superiority.

**Table 10. LM vs. rule net paired gains (Qwen, cross-task).**

| Website | LM Net Gain | Rule Net Gain | Direction |
|---------|------:|------:|------|
| newegg | +2 | +4 | Rule ≥ LM |
| united | +1 | −2 | LM > Rule |
| kayak | 0 | −1 | LM ≥ Rule |

**Finding 11: The abstractness advantage is conditional on task-train divergence.** On newegg, where cross-task operational patterns are relatively fixed (search → filter → sort → cart), rule workflows' concrete values happen to match the test tasks well. The formal C3-runbook judgment for newegg is `unclear`. On united, where task diversity is higher, LM's abstraction provides clearer benefit. The paper reports only the aggregate LM > Rule conclusion without discussing this boundary condition.

### 5.7 Representation Ablations (C4)

#### 5.7.1 Code vs. Text Workflow

On kayak (Qwen), code and text workflows perform similarly (Step SR difference: 2.2pp), consistent with the paper's claim. However, both perform below the no-workflow baseline (51.2%), so the claim that "both formats effectively augment agent memory" is only directionally supported.

#### 5.7.2 NL vs. HTML Observation

**Table 11. Step SR by observation representation (Qwen, three sites).**

| Site | desc_only | html_only | desc_html | Paper Prediction |
|------|------:|------:|------:|------|
| kayak | 45.3 | 48.0 | 50.3 | NOT supported |
| newegg | **30.5** | 23.9 | 30.3 | Supported |
| united | 55.9 | **60.6** | 51.7 | NOT supported |

**Finding 12: The NL-vs-HTML claim was not reproduced in the three-site first run.** Only newegg supports the paper's recommendation that NL descriptions are superior. On united, HTML-only is best, likely because united's HTML element names are inherently readable (e.g., `tab TRAVEL INFO`, `heading Check-in`). On united, the mixed representation (desc_html) causes the most severe degradation: task SR drops from 33.3% to 16.7%, consistent with attention dilution from increased prompt length and redundancy.

**Finding 13: The optimal representation strategy is site-dependent.** The paper offers a cross-site unified recommendation, but no single representation strategy is consistently optimal. This is a boundary condition the paper does not discuss.

### 5.8 Workflow Quality (C5)

The C5 quality results support compact workflow libraries (5–7 LM workflows per site) with low function overlap (0–3.33%). However, the utility and coverage metrics require careful interpretation:

- **Utility rate** is high at the prompt level (100% injection rate), but workflow genuinely changes model behavior on only 6–18% of steps (from §5.2.3). The gap between prompt-level availability and behavioral adherence is large.
- **Coverage** as reported approximates "workflow text is present in the prompt and visible to the model," which is a weaker proxy than strict functional coverage of test-step operations.

**Finding 14: C5 supports compact workflow libraries with low overlap, but utility and coverage should be interpreted as prompt-level proxies rather than strict adherence measures.**

### 5.9 Compositionality on Mind2Web

The paper highlights workflow composition as a key capability, showing how simple workflows combine into more complex ones on WebArena (e.g., "find a place" → "get the zip code of a place"). On Mind2Web, our reading of the workflow texts across four sites reveals a flatter picture:

- **Explicit hierarchical composition** (one workflow calling another): not observed in any Mind2Web workflow file.
- **Flat subflow reuse** (tasks completed by chaining short reusable routines): clearly present on kayak and united, where 1–4 step parameterized primitives can be flexibly combined.
- **Template bundling** (long, site-specific sequences serving as reusable units only in a weak sense): visible on budget, where workflows mix several distinct functional domains.

**Finding 15: On Mind2Web, AWM shows signs of subflow reuse mainly as a flat library of reusable routines, not as explicit hierarchical workflow composition.** This makes the paper's composition narrative partially visible but considerably weaker and flatter than the WebArena-based narrative suggests.

### 5.10 Failure Taxonomy

We identified eight failure modes from the combined analysis, organized by severity.

**Table 12. Failure taxonomy.**

| Failure Mode | Description | Severity | Source Section |
|-------------|-------------|----------|--------------|
| **Workflow mismatch** | Workflow template does not apply to current step, redirecting the agent away from correct action | High | §5.2, §5.3 |
| **Cross-site transfer failure** | Workflows from source site encode operational logic incompatible with target site | High | §5.3 |
| **Cumulative misdirection** | Workflow harm amplifies in the second half of trajectories | Medium | §5.2.2 |
| **Over-specificity** | Rule workflows preserve too many source-site concrete values | Medium | §5.6 |
| **Representation noise** | Mixed desc_html representation increases prompt length and dilutes attention | Medium | §5.7.2 |
| **Workflow ineffectiveness** | Workflow exists but does not affect model output (45–65% of steps) | Low | §5.2.3 |
| **SKIP-step inflation** | Ground truth elements absent from candidates, inflating failure counts across all conditions | Structural | §5.2 |
| **Limited coverage** | 5–7 abstract workflows cannot cover all test-step operation types | Structural | §5.8 |

The paper does not discuss any of these failure modes. In particular, the paper does not report that workflows can be actively harmful, does not analyze the narrow influence window, and does not discuss how SKIP-step rates vary across sites (kayak 29% vs. tripadvisor 45%), making cross-site absolute scores incomparable.

### 5.11 Prompt-Level Mechanism Evidence

To ground the statistical findings in concrete causal evidence, we performed source-verified case studies on six paired cases.

#### 5.11.1 Positive Mechanisms

**P-1: Preventing premature termination** (kayak, task 1, step 9). The baseline model hallucinates that the task is complete and outputs a natural language summary instead of a grounded action. The workflow's `View and Select Deals` routine prompts the agent to continue interacting with search results, producing the correct `CLICK [Sort by Cheapest]` action.

**P-2: Strategy redirection** (newegg, task 4, step 0). The baseline model defaults to a "browse categories" strategy, clicking the Electronics navigation menu. The workflow's `search_and_apply_filters` routine redirects the model to a "search first" strategy, correctly typing `drone` into the search box.

**P-3: Value format correction** (newegg, task 5, step 3). The baseline model selects the correct element but outputs `SELECT [112591] [5]` (numeric index). The workflow's template uses human-readable labels (e.g., "Lowest Price"), guiding the model to output `SELECT [112591] [Most Reviews]` (correct string label).

#### 5.11.2 Negative Mechanisms

**N-1: Out-of-domain workflow misdirection** (budget, task 0, step 0). The task requires viewing an insurance policy. The workflow, which encodes car-rental search routines, redirects the agent to type a zip code into a location search box instead of clicking the correct navigation link.

**N-2: Full-domain misdirection** (sixflags, task 2, step 0). The task requires accessing financial statements. All five sixflags workflows cover park/ticket navigation. The agent clicks "Browse the Parks Below" instead of the correct "Investors" link, because the workflow's first step matches a visible on-page button.

**N-3: Template step-skipping** (sixflags, task 1, step 5). The workflow compresses the actual UI interaction into 2 steps (CLICK Tickets → CLICK option), skipping the intermediate date-selection step. The agent maps its current state to a later template step and clicks "Book Now" before selecting a date.

**Synthesis:** The positive mechanisms share a common structure: workflow provides the **correct operational mode** at a critical decision point. The negative mechanisms share a different common structure: workflow provides an **inapplicable operational mode** that the model follows instead of reasoning independently. Case-level evidence is consistent with a "workflow-first" behavioral tendency—the model appears to preferentially follow workflow instructions over independent reasoning when both are available—though this pattern should be interpreted as suggestive rather than as a demonstrated universal law.

### 5.12 Site Characteristics and Success Prediction

#### 5.12.1 Structural Comparison

**Table 13. Site-level structural comparison (values from step_breakdown_output.txt and workflow file counting).**

| Dimension | kayak (WORKS) | newegg (WORKS) | budget (HURTS) | sixflags (HURTS) |
|---|---|---|---|---|
| Step SR delta | +6.3% | +5.7% | −6.1% | −4.7% |
| Baseline CLICK acc | 71.4% | 66.7% | 63.8% | 73.5% |
| AWM CLICK delta | +10.7% | +6.1% | −12.1% | −6.1% |
| Avg steps/WF | 2.1 | 3.2 | 5.8 | 3.6 |
| WF-task alignment | Strong | Strong | Weak | Partial to Weak |

#### 5.12.2 Alignment Rate (Exploratory)

An exploratory keyword-overlap heuristic measuring workflow-target surface alignment yields a counter-intuitive pattern:

| Site | Alignment Rate | C1 Status |
|------|------:|------|
| budget | 97.2% | not reproduced |
| sixflags | 94.2% | not reproduced |
| newegg | 90.9% | reproduced |
| kayak | 70.6% | reproduced |

Surface alignment does not show a positive monotonic relation with success. Budget and sixflags have high surface alignment because their workflow templates cover common action-type keywords—but the test tasks involve different semantic instances of those keywords (insurance vs. rental, financial statements vs. park tickets). Newegg is an explicit exception to any "higher alignment = worse performance" story. This metric is exploratory and should not be treated as a causal indicator.

#### 5.12.3 Working Hypothesis

Based on the first-run four-site evidence, we propose a working hypothesis (not a validated rule):

> AWM effectiveness ≈ f(Workflow Reusability × Baseline Improvement Headroom)

Both conditions appear necessary:

1. **Workflow reusability**: Short, parameterized sub-routines that can match multiple test tasks. kayak/newegg (2–3 steps/WF, fully parameterized) satisfy this; budget (5.8 steps/WF, domain-specific sequences) does not.
2. **Baseline improvement headroom**: Sites where baseline CLICK accuracy is in the mid-range (~65–72%), indicating room for element-grounding assistance. sixflags (73.5% baseline CLICK) already performs well without help.

This is a post-hoc observation from four sites, not a validated threshold. The 65–72% range should not be written as a decision boundary.

### 5.13 Unified Causal Model

The findings above integrate into a five-stage causal chain:

1. **Induction stage**: Offline or online induction produces a workflow library. LM induction yields abstract sub-routines; rule induction yields concrete case libraries. [HARD evidence]

2. **Matching stage**: At test time, workflows are injected into the prompt. The critical variable is not workflow count or surface alignment, but **task-workflow semantic match**: whether the workflow's operational pattern applies to the current step. [SOFT evidence: inferred from §5.12 exploratory metric + §5.11 cases]

3. **Intervention stage**: On a small fraction of steps (6–18%), workflow genuinely changes model behavior. When matched: strategy redirection, value format correction, termination prevention. When mismatched: domain misdirection, step skipping. [HARD evidence: paired-case + prompt-level cases]

4. **Accumulation stage**: Positive and negative interventions accumulate over the trajectory. On matched sites, second-half gains reach +13% on kayak. On mismatched sites, second-half losses reach −10.9% on budget. [HARD evidence, but effect strength varies across sites]

5. **Aggregation**: Final Step SR delta = Σ(positive) − Σ(negative). Reproduced sites have negative=0, yielding net positive. Not-reproduced sites have negative >> positive, yielding net negative. [HARD evidence]

**Table 14. Paper narrative vs. observed mechanism.**

| Paper Narrative | Observed Mechanism | Evidence Level |
|----------------|-------------------|---------------|
| AWM is broadly effective | AWM is conditionally effective: requires workflow reusability + baseline headroom | SOFT (4-site post-hoc) |
| Online AWM is superior under larger distribution gap | Online AWM produces negative transfer under cross-site shift | HARD |
| Workflow provides "high-level operational guidance" | Workflow changes behavior on a small fraction of steps via specific mechanisms | HARD |
| LM induction is better than rule induction | Abstractness advantage depends on task-train divergence | HARD (text) + SOFT (performance) |
| High utility rate | Prompt-level utility is high; behavioral adherence is much lower | HARD + exploratory |

---

## 6. Discussion

### 6.1 What This Reproduction Reveals About AWM

The most important finding is not that AWM "does not work"—on matched sites, it clearly does, and its "do no harm" property (negative = 0 on reproduced sites) is genuinely impressive. Rather, the key insight is that AWM's effectiveness is **site-dependent in a structured way** that the paper's aggregate reporting obscures. The method works through a narrow window of decisive interventions on a small fraction of steps, and the sign of those interventions flips from positive to negative depending on semantic match between the workflow library and the target task.

This has implications for how the field should evaluate workflow memory methods more broadly: aggregate benchmark scores are insufficient. Step-level and paired-case analysis should become standard practice for understanding *where* and *how* a memory mechanism helps.

### 6.2 Implications for the Broader Research Agenda

Within the framework of experience-dependent procedural knowledge for GUI agents, AWM validates the core idea that abstract, reusable sub-routines can improve agent performance through prompt-level injection. However, our analysis also reveals two structural limitations:

1. **No failure-driven revision**: AWM induces workflows from successes but has no mechanism for revising or retracting workflows when they cause harm. The negative cases (N-1, N-2, N-3) show that harmful workflows persist and are replayed without correction.

2. **Flat reuse only**: On Mind2Web, workflows function as a flat library of independent routines rather than as composable building blocks. The stronger composition narrative from WebArena may not generalize to all environments.

These limitations align with the broader survey's identification of failure-driven write-back and procedural rule generalization as the most pressing research gaps.

### 6.3 Scope and Limitations

1. **Mind2Web only.** All conclusions are Mind2Web-specific. The paper's WebArena results, which support stronger claims about workflow composition and task success rate, are not covered.

2. **First-run judgments.** All reproduced/not-reproduced judgments are based on single runs without variance estimates. "Not reproduced" should be read as "not reproduced in the current first-run setting," not as "definitively false."

3. **No AWM_AS coverage.** The paper's action-space extension experiment is not reproduced. This is a scope limitation, not a contradictory finding.

4. **Alignment rate is exploratory.** The keyword-overlap heuristic is useful for generating hypotheses about surface-vs-semantic alignment but should not be treated as a validated metric.

5. **Model-specific.** Results may differ with other backbone models. Our use of Qwen-3.5 alongside GPT-4o provides some breadth but does not constitute comprehensive model robustness testing.

---

## 7. Conclusion and Future Work

### 7.1 Summary

This study presents a deep reproduction and mechanism audit of Agent Workflow Memory on Mind2Web. Going beyond aggregate score comparison, we decompose AWM's effects at three complementary levels of granularity:

- **Step-level**: AWM's benefits are driven by stable TYPE-side value guidance and site-dependent CLICK grounding effects, not by uniform all-step improvement.
- **Paired-case**: On reproduced sites, workflow never harms the agent (negative = 0); on not-reproduced sites, negative interventions substantially outnumber positive ones. AWM's actual influence window covers only 6–18% of steps.
- **Prompt-level**: Three positive mechanisms (strategy redirection, value format correction, premature termination prevention) and three negative mechanisms (domain misdirection, step-skipping, workflow-first behavior) are identified through source-verified case studies.

We find that the paper's cross-site generalization claim is not supported under first-run evidence, that the offline–online distinction is a trade-off rather than a ranking, that LM-induced abstractness does not automatically yield performance superiority, and that eight boundary conditions—none discussed in the original paper—significantly qualify AWM's effectiveness.

### 7.2 Future Work

1. **Repeated trials with variance estimation.** Converting the current first-run judgments into statistically grounded conclusions requires multiple runs with different random seeds and confidence intervals.

2. **Failure-driven workflow revision.** AWM currently has no mechanism for revising or retracting workflows. A write-back loop that detects harmful patterns (e.g., sustained negative paired-case counts) and modifies or removes offending workflows could address the method's most severe failure mode.

3. **Semantic matching for workflow selection.** The current approach injects all workflows uniformly. A retrieval mechanism that selects workflows based on task-workflow semantic similarity (rather than keyword overlap) could reduce mismatch-induced harm.

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

The following appendix evidence blocks support the main-text claims. Each appendix is a self-contained evidence document with source traceability.

### Appendix Index

| ID | Title | Supports |
|----|-------|----------|
| A1 | Step-Level Breakdown | §5.2 Finding 1–3 |
| A2 | Paired-Case Summary | §5.2.3 Finding 4–6 |
| A3 | Cross-Site Diagnosis | §5.3 Finding 7 |
| A4 | C4 Result Table | §5.7 Finding 12–13 |
| A5 | C5 Quality Table | §5.8 Finding 14 |
| A6 | Alignment-Rate Note | §5.12.2 (exploratory) |
| A7 | Offline vs. Online Trade-off | §5.4 Finding 8 |
| A8 | Online Small-Data Efficiency | §5.5 Finding 9 |
| B1 | Kayak Positive Case (P-1) | §5.11.1 |
| B2 | United Positive Case (P-2) | §5.11.1 |
| B4 | Sixflags Negative Case (N-2) | §5.11.2 |
| B5 | Sixflags Step-Skipping Case (N-3) | §5.11.2 |
| B6 | Tripadvisor Cross-Site Negative | §5.3, §5.11.2 |
| C1 | LM vs. Rule Text Evidence | §5.6 Finding 10–11 |
| C4 | Site-Feature Qualitative Coding | §5.12.1 |
| C5 | Mind2Web Compositionality Reading | §5.9 Finding 15 |

Full appendix documents are maintained in `doc/analysis/appendix/` and are available upon request.
