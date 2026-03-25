# Progress Report for Topic 6

## Abstract

This progress report documents both the empirical work already completed and the resulting revision of the project proposal. The original project aimed to study parameter-free self-improvement in LLM agents through Reflexion and ExpeL, with emphasis on reflection correctness, cross-task transfer, and retrieval utility. Pilot experiments succeeded in establishing runnable local pipelines for both systems and produced initial artifacts, including a 10-case Reflexion failure set and a smoke-train ExpeL run on ALFWorld. However, these pilots also revealed that the original research questions were difficult to answer cleanly because they depended on latent and confounded constructs such as “true failure cause” and “true transferability.” In response, the project was reformulated into a more bounded empirical study: how abstraction from episodic experience to reusable lessons affects cross-task reuse in LLM agents. This revised proposal better matches the style of the course topics because it uses a fixed benchmark, a controlled comparison, and interpretable metrics. The report therefore presents the project not as a failed first attempt, but as a methodologically informed narrowing process that now leads to a clearer final-study design.

## 1. Project Context

The project originally focused on **parameter-free self-improvement** in LLM agents, using two representative systems:

- **Reflexion**, which stores natural-language self-reflections after failure and reuses them on retry
- **ExpeL**, which stores trajectories, extracts reusable insights, and retrieves cross-task experience

The initial motivation was to move beyond overall benchmark scores and ask mechanism-level questions:

- Does Reflexion correctly diagnose why a task failed?
- Do ExpeL’s extracted insights produce useful cross-task transfer?
- Does retrieval similarity correspond to actual operational usefulness?

This was a strong starting point because it aimed to evaluate agent memory and self-improvement more critically than a simple reproduction project. However, pilot work later showed that this framing was not well suited to a bounded course project.

## 2. Completed Work Under the Original Proposal

### 2.1 Reflexion Pipeline

The project successfully established a runnable local Reflexion pipeline for ALFWorld in a dedicated conda environment. Two stages were completed:

- a no-memory smoke run
- a memory-enabled smoke run with reflection generation and logging

The no-memory smoke run used `num_trials = 1`, `num_envs = 2`, and `model = gpt-4o`, producing:

- `SUCCESS: 0`
- `FAIL: 2`
- `TOTAL: 2`

The memory-enabled run confirmed that retry-with-reflection works end to end and that generated reflections are stored in the logs.

### 2.2 Reflexion Failure Pilot

To move beyond anecdotal examples, a larger memory-enabled pilot was run on `8` ALFWorld environments. Together with the earlier 2-environment memory run, this produced a set of **10 failed Reflexion cases** with non-empty reflections.

The 10-case annotation set suggested the following early pattern:

- primary formatting / interaction protocol failure: `10 / 10`
- secondary generic or non-actionable reasoning failure: `8 / 10`
- reflections that mention the likely issue clearly: `6 / 10`
- reflections that mention it only partially: `4 / 10`
- reflections judged fully actionable: `0 / 10`

This was already a meaningful pilot result: Reflexion often notices something close to the failure mode, but the reflection is usually too generic to function as an executable repair policy.

### 2.3 ExpeL Pipeline

ExpeL was also brought into a runnable local state, although it required more compatibility work than Reflexion. The project resolved issues involving OpenAI-compatible API routing, ALFWorld environment compatibility, package-version mismatches, `tiktoken` support for `gpt-4o`, and a hard-coded assumption that every run contains exactly 134 tasks.

After these fixes, a 4-task ALFWorld smoke-train run completed successfully and produced standard ExpeL artifacts. The observed outcome was:

- `Success: 1`
- `Fail: 2`
- `Halted: 1`

At this stage, ExpeL has not yet produced the evidence needed for the original transfer or retrieval analyses, but it has established a working train-stage path and persistent artifacts for later inspection.

## 3. Why the Original Proposal Was Revised

The most important outcome of the pilot stage was not just engineering progress. It was methodological clarification.

The original proposal depended on questions such as:

- whether a reflection was “truly” correct
- whether an experience was “truly” transferable
- whether retrieved memories were “really” relevant

These turned out to be difficult to answer cleanly in the current setting because they rely on weakly defined or latent constructs:

- a task failure often has multiple plausible causes
- interactive benchmarks can mix reasoning errors with interface and protocol failures
- transferability is entangled with task wording, benchmark structure, and retrieval design
- relevance can mean semantic similarity, procedural overlap, or causal usefulness

As a result, scaling the original plan would likely have produced more annotations and more artifacts, but still a weak central claim. The problem was not insufficient engineering. The problem was that the original research question was not yet clean enough for a clear empirical answer.

This point matters because the official course topics are not framed as broad interpretability problems. They are framed as bounded empirical studies with:

- a fixed benchmark or system setting
- a small number of controlled variables
- and interpretable metrics

The original proposal was too close to asking whether the agent was internally correct. That is an interesting research question, but it is not the best fit for the course format.

## 4. Revised Proposal

The revised project is now:

> **From Episodic Experience to Reusable Lessons: Evaluating Experience Abstraction for Cross-Task Reuse in LLM Agents**

Its central question is:

> **How does abstraction from episodic experience to reusable lessons affect cross-task reuse in LLM agents?**

This revised direction is narrower and more defensible because it replaces latent correctness with a controlled variable:

- the abstraction level of stored experience

The revised project is also grounded in the memory framework already developed in the repository:

- **episodic memory**: concrete past experiences
- **semantic memory**: abstract stable knowledge
- **procedural memory**: reusable routines and skills

The project now focuses only on the first transition:

> `episodic experience -> reusable lesson`

This is a more precise and better-bounded question than the earlier mechanism-level critique of Reflexion and ExpeL.

## 5. Why the New Proposal Is Better

The revised proposal is better in four specific ways.

### 5.1 It Uses a Controllable Variable

The project no longer tries to judge whether the model’s internal diagnosis is correct. Instead, it compares two explicit memory forms:

- **Episode memory**: a concrete, context-rich description of a past task event
- **Lesson memory**: a reusable abstraction distilled from the same experience

### 5.2 It Asks a Bounded Open Question

Existing work such as AWM, ExpeL, and SkillWeaver shows that abstraction matters, but these systems do not cleanly isolate the following question in the chosen setting:

> For the same source experience, what changes when that experience is stored as a concrete episode rather than an abstract lesson?

This is not a universally unsolved problem, but it is also not fully answered in the selected setting. That makes it appropriate for a course project.

### 5.3 It Fits the Style of the Course Topics

The official course topics generally ask students to investigate a bounded empirical problem by comparing methods, configurations, or strategies under a fixed benchmark. The revised proposal now follows the same structure:

- fixed benchmark
- controlled comparison
- small number of variables
- interpretable metrics

### 5.4 It Gives the Final Report a Cleaner Research Story

The project can now be presented as:

> initial hypothesis -> pilot evidence -> proposal reassessment -> sharper empirical question

This is much clearer than a report that merely accumulates mechanism-oriented annotations without a strong final claim.

## 6. Revised Experimental Plan

The benchmark remains **ALFWorld**, but not as a full-scale leaderboard reproduction. Instead, it will be used as a controlled subset benchmark in which reusable lessons are interpretable.

The revised plan centers on three experiments.

### 6.1 Experiment 1: Episode vs Lesson

Compare:

- `No memory`
- `Episode memory`
- `Lesson memory`

Main metrics:

- success rate
- transfer gain over the no-memory baseline
- prompt length

### 6.2 Experiment 2: Information-Loss Analysis

For each source experience, identify what information is removed when an episode is abstracted into a lesson, such as:

- object-specific details
- environment-specific constraints
- preconditions
- failure-specific cues

Then analyze which kinds of removed information most often correspond to reuse failure.

### 6.3 Experiment 3: Reuse vs Over-Generalization

Test episode and lesson memory on three target types:

- `Reusable`
- `Near-miss`
- `Unrelated`

Main metrics:

- positive transfer
- negative transfer
- net utility

## 7. Scope and Next Steps

The project deliberately does **not** make retrieval design, staged context injection, full workflow induction, or executable skill synthesis the main subject of study. Those are meaningful topics, but they would expand the scope too quickly.

The immediate next steps are:

1. define a controlled ALFWorld subset in which reusable lessons are interpretable
2. design a stable template for converting source experiences into episode and lesson memory
3. run the first revised comparison among `No memory`, `Episode memory`, and `Lesson memory`

## 8. Conclusion

The current stage of the project has already produced both real empirical artifacts and a more mature research direction. Reflexion and ExpeL are now runnable locally, and the pilot evidence has done more than demonstrate feasibility: it has shown why the original proposal was too methodologically unstable for a clear course-project contribution.

The revised proposal is therefore not a retreat from the original idea, but a better formulation of it. Instead of asking whether agents are internally correct about their own failures, the project now asks a more bounded and testable question:

> **How does abstraction from episodic experience to reusable lessons affect cross-task reuse in LLM agents?**

This gives the project a stronger path toward a final report that is both technically executable and empirically defensible.
