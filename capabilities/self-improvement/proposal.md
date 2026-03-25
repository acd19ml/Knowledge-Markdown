# Topic 6 — From Episodic Experience to Reusable Lessons

## Evaluating Experience Abstraction for Cross-Task Reuse in LLM Agents

### Background

Large language model agents have shown promising performance on multi-step reasoning and interactive decision-making tasks. However, many agents remain weak at **reusing experience across tasks**. Existing systems often store one of three broad forms of experience:

- **episodic traces**: concrete past trajectories or failures,
- **semantic lessons**: abstracted natural-language insights,
- **procedural routines**: workflows or executable skills.

Recent work has shown that these forms can help in some settings. For example, **Reflexion** stores verbal reflections after failed attempts, **ExpeL** extracts reusable insights from past trajectories, and **AWM** induces workflows from successful experiences. Yet these works do not cleanly answer a more basic question:

> **When does a concrete episode become a reusable lesson?**

This project focuses on that abstraction step. Instead of studying whether an agent’s internal diagnosis is “truly correct,” it studies a more controllable and measurable question: **how changing the abstraction level of the same source experience changes later cross-task reuse.**

---

### Why the original proposal was revised

The original proposal centered on assumptions such as:

- whether Reflexion correctly diagnoses the real cause of failure,
- whether ExpeL’s retrieved experiences are “truly relevant,”
- whether self-reflection is causally responsible for later recovery.

These questions are interesting, but they are difficult to operationalize cleanly. They depend on latent ground truth, subjective failure attribution, and confounds between model capability, environment protocol, retrieval quality, and prompt design. As a result, they risk producing interpretations that are difficult to defend quantitatively.

The revised proposal therefore shifts from **latent reasoning correctness** to **behaviorally testable experience abstraction**:

- the source experience is fixed,
- the retrieval pipeline is fixed,
- the prompt position is fixed,
- the main manipulated variable is the **abstraction level of the stored experience**.

This revised framing is closer to the style of the course topics: it defines a bounded empirical comparison with explicit conditions, benchmarks, and metrics.

---

### Central research question

> **How does abstraction from episodic experience to reusable lessons affect cross-task reuse in LLM agents?**

More concretely, the project asks whether a concrete past experience is more useful when preserved as an **episode** or when abstracted into a **lesson**, and what information is lost during that abstraction.

---

## Core concepts

This project uses two experience units.

### 1. Episodic memory

A concrete, context-rich description of a past experience:

- specific task instance,
- specific objects or entities,
- concrete failure or success event,
- local execution details.

Example form:

> “In a kitchen task, the agent failed when placing the cooled tomato into the microwave after earlier steps had already succeeded.”

### 2. Lesson memory

A conditional, reusable abstraction distilled from the same experience:

- preserves the actionable lesson,
- removes task-instance-specific details,
- aims to support reuse in later tasks.

Example form:

> “When a task requires placing an object into a target container, first verify that the target is in a valid state for placement before executing the final placement step.”

The proposal intentionally stops at this `episode -> lesson` transition. It does **not** attempt to solve the larger problem of deriving full procedural skills or executable tool APIs.

---

## Research questions

### RQ1. Reuse effect

When the same source experience is stored as an **episode** versus a **lesson**, how does later cross-task performance change?

### RQ2. Information loss

When an episode is abstracted into a lesson, which lost information most often causes reuse failure?

### RQ3. Over-generalization

Do lessons transfer more broadly than episodes, but also create a higher risk of false generalization on superficially similar tasks?

---

## Experimental design

### Benchmark choice

The primary benchmark will be **ALFWorld**, used in a **controlled subset setting** rather than full-scale reproduction.

Reasons:

- it is text-only and comparatively lightweight,
- it supports controlled manipulation of task instructions and outcomes,
- it allows direct observation of success/failure after memory injection,
- it is already available in the current project infrastructure.

However, the project will not treat ALFWorld as a perfect proxy for all forms of experience reuse. A known limitation is that some ALFWorld failures come from interaction protocol issues rather than meaningful semantic lessons. Therefore, the experiment will focus on a **filtered subset of tasks** where reusable lessons are interpretable and not dominated by formatting artifacts.

---

### Experiment 1: Episode vs Lesson

For each selected source case:

1. collect a source success/failure episode,
2. construct an **episodic memory** version,
3. construct a **lesson memory** version from the same case,
4. evaluate target tasks under three conditions:
   - `No memory`
   - `Episode memory`
   - `Lesson memory`

Primary metrics:

- **Success Rate (SR)**
- **Transfer Gain** over the no-memory baseline
- **Prompt Length** as a compactness proxy

Why this experiment matters:

- It directly isolates the project’s main variable: abstraction from episode to lesson.
- Existing work compares trajectories, insights, workflows, or skills across systems, but does not cleanly compare **two abstraction levels of the same source experience**.

Critical reflection:

- This experiment is meaningful.
- It is not fully solved by AWM, ExpeL, or SkillWeaver.
- But it will only be convincing if all other variables remain fixed; otherwise, any effect could be explained by retrieval or prompt differences instead of abstraction itself.

---

### Experiment 2: Information-loss analysis

For each source case, the lesson version will be annotated for information removed relative to the original episode. Candidate information-loss categories include:

- object-specific details,
- environment-specific constraints,
- preconditions,
- exception or failure cues,
- local action-order details.

For target-task failures, the analysis will ask which missing information most plausibly accounts for the failure.

Primary outputs:

- failure counts by missing-information type,
- per-category comparison between episode and lesson memory,
- a compact qualitative table of representative cases.

Why this experiment matters:

- It moves beyond “which works better” and asks **why abstraction fails**.

Critical reflection:

- This is the most analysis-heavy part of the project.
- It introduces manual judgment, so the scale must remain small and carefully controlled.
- Still, it matches the style of course topics that explicitly allow taxonomy analysis and targeted human assessment.

---

### Experiment 3: Reuse vs over-generalization

Target tasks will be divided into three groups:

- **Reusable**: the source lesson should plausibly help,
- **Near-miss**: superficially similar but with a key changed constraint,
- **Unrelated**: no plausible reuse relation.

Episode and lesson memory will then be compared across these groups.

Primary metrics:

- **Positive Transfer Gain**
- **Negative Transfer Count**
- **Net Utility** = positive transfer benefit minus harmful cases

Why this experiment matters:

- It prevents the project from collapsing into the simplistic claim that “more abstraction is always better.”

Critical reflection:

- This experiment is important but delicate.
- The hardest part is defining `Reusable / Near-miss / Unrelated` consistently.
- To stay defensible, these categories must be defined before running the experiments, not after observing outcomes.

---

## Scope control

To keep the project tractable, the following are explicitly **out of scope**:

- designing a new retrieval algorithm,
- studying progressive disclosure or staged context injection as the main problem,
- automatically generating the best lessons from raw trajectories at scale,
- full procedural-skill induction or executable API synthesis,
- proving whether an agent’s internal explanation is “truly correct.”

These are valuable extensions, but including them now would blur the main variable and recreate the methodological problems of the earlier proposal.

---

## Expected contribution

This project aims to contribute a **controlled empirical analysis** of one specific but under-studied transition in agent memory:

> the shift from **concrete episodic experience** to **reusable semantic lesson**.

If successful, the project will clarify:

- whether lesson-level abstraction improves cross-task reuse,
- which kinds of information should not be abstracted away,
- and when abstraction begins to over-generalize.

This would provide a tighter and more defensible contribution than a broader claim about whether parameter-free self-improvement “works” in general.

---

## Limitations

- The benchmark is controlled and simplified; conclusions may not transfer directly to richer GUI or real-world environments.
- Lesson construction will likely involve manual or template-based abstraction, so the project studies the **effect** of abstraction rather than fully automating abstraction.
- The project addresses only the `episodic -> lesson` step, not the later `lesson -> procedural skill` transition.

These limitations are acceptable for a course project because the goal is not to solve the full lifelong-memory problem, but to isolate one clear and measurable open question within it.

---

## References

1. Shinn N, Cassano F, Labash A, et al. Reflexion: Language agents with verbal reinforcement learning. *Advances in Neural Information Processing Systems*, 2023, 36.
2. Zhao A, Huang D, Xu Q, et al. ExpeL: LLM agents are experiential learners. *Proceedings of the AAAI Conference on Artificial Intelligence*, 2024, 38(17): 19632–19642.
3. Wang Z Z, Mao J, Fried D, et al. Agent workflow memory. *arXiv preprint*, 2024.
4. Zheng B, Fatemi M Y, Jin X, et al. SkillWeaver: Web agents can self-improve by discovering and honing skills. *arXiv preprint*, 2025.
5. Park J S, O’Brien J C, Cai C J, et al. Generative agents: Interactive simulacra of human behavior. *Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology*, 2023.
6. Shridhar M, Yuan X, Côté M A, et al. ALFWorld: Aligning text and embodied environments for interactive learning. *International Conference on Learning Representations*, 2021.
