## Topic 6 - From Episodic Experience to Reusable Lessons

> This document does not merely restate [proposal.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2026_Epi2Lesson/proposal.md). Its purpose is to test whether the revised proposal is methodologically sound, sufficiently open-ended for Topic 6, and still bounded enough to become a defensible course project.

---

## 1. What Changed

The earlier project framing focused on **stress-testing Reflexion and ExpeL** through questions such as:

- whether Reflexion correctly diagnosed failure causes,
- whether ExpeL’s retrieved experiences were “truly relevant,”
- whether reflective or experiential memory helped for the reasons claimed by the original papers.

These are interesting questions, but they are methodologically unstable. They depend on:

- subjective failure attribution,
- latent reasoning correctness,
- confounds between model ability, prompt design, retrieval quality, and environment protocol,
- weakly defined ground truth for concepts such as “diagnostic correctness” or “true relevance.”

The revised proposal moves away from such latent claims and instead studies a more controllable question:

> **How does abstraction from episodic experience to reusable lessons affect cross-task reuse in LLM agents?**

This change is not cosmetic. It fundamentally shifts the project from **interpreting internal cognition** to **measuring the behavioral effect of a manipulated memory representation**.

---

## 2. Why This New Direction Is Better

### 2.1 It uses a controllable variable

The key manipulated object is now the **same source experience expressed at different abstraction levels**:

- episodic memory,
- lesson memory.

This is much cleaner than asking whether a model’s explanation is “actually right.”

### 2.2 It aligns with the repo’s memory-theoretic foundations

The repo’s memory survey already identifies the transition among:

- **episodic memory**: concrete past experiences,
- **semantic memory**: abstract stable knowledge,
- **procedural memory**: reusable routines and strategies.

See:

- [2.2_cognitive-mechanisms.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/survey/02_taxonomy/2.2_cognitive-mechanisms.md)
- [3.2_dynamic-experience.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/survey/03_env-centric/3.2_dynamic-experience.md)

The revised proposal studies one specific step inside that broader memory ladder:

> **episodic experience -> semantic lesson**

This makes the project theoretically grounded without becoming too large.

### 2.3 It matches the style of the official course topics

The five official topics are not asking students to solve fully open-ended unsolved frontier problems. They instead ask for:

- a bounded empirical question,
- controlled comparisons,
- explicit metrics,
- interpretable analysis,
- limited but meaningful extension beyond direct reproduction.

The revised proposal follows this pattern. It does not claim to solve lifelong memory. It asks one narrower question that can be tested with a clear experimental matrix.

---

## 3. Critical Reflection: Is This Still Too Broad?

Yes, it could easily become too broad again if the scope is not explicitly constrained.

### 3.1 Danger: “semantic abstraction” becomes a vague slogan

If the project says only:

> “I study semantic abstraction levels.”

then the variable remains underspecified. Abstraction can remove many different kinds of information:

- object identity,
- environment-specific constraints,
- failure cues,
- preconditions,
- action-order details.

The revised proposal therefore avoids generic “low / medium / high abstraction” language and uses only two units:

- **Episode**
- **Lesson**

This is deliberate. It keeps the problem interpretable.

### 3.2 Danger: the project turns into retrieval research

The user correctly identified that:

- whether memory is triggered is mostly a retrieval problem,
- progressive disclosure is mostly a context-engineering problem.

If these become central, the main variable is no longer abstraction. The project therefore treats retrieval and injection style as **controlled background choices**, not the main contribution.

### 3.3 Danger: the project turns into prompt engineering

If lesson construction is informal or ad hoc, then any observed gain could simply reflect better writing style rather than a principled abstraction step.

Therefore, the proposal must state clearly:

- lesson construction will be **template-based or manually controlled**,
- the project studies the **effect** of abstraction,
- it does **not** attempt to solve automatic abstraction generation.

This restriction is necessary, not a weakness.

---

## 4. Is This Problem Already Solved?

Not fully, but parts of it have already been addressed indirectly.

### 4.1 What AWM already answered

AWM already studies several questions about workflow representation:

- LM-induced abstraction vs rule-based reuse,
- code workflow vs text workflow,
- NL environment description vs HTML-enhanced description.

These results already imply:

- abstraction matters,
- surface format matters less,
- adding more concrete detail does not always help.

So the revised proposal should **not** ask:

- whether workflow should be code or text,
- whether more HTML detail improves memory,
- whether sub-routine abstraction helps at all.

Those questions have already been substantially explored.

### 4.2 What remains open

AWM, ExpeL, and SkillWeaver all compare **different memory objects across systems**, but they do not cleanly isolate:

> the behavioral difference between an **episode** and a **lesson distilled from the same episode**.

That is the gap this proposal uses.

### 4.3 Why this gap is still meaningful

This is not a novelty claim of the form:

> “nobody has ever discussed abstraction.”

Instead, the claim is narrower and stronger:

> existing work does not yet provide a controlled comparison of **same-source episodic vs lesson-level memory** and the information-loss tradeoff between them.

That is enough for a course project.

---

## 5. Experimental Logic

The revised proposal should be evaluated as a controlled empirical study, not as a broad architecture project.

### Experiment 1: Episode vs Lesson

Compare:

- no memory,
- episode memory,
- lesson memory.

This experiment answers whether abstraction changes reuse performance.

### Experiment 2: Information-loss analysis

Track what information is dropped when converting an episode into a lesson, then analyze which types of removed information are associated with later failure.

This is where the project becomes more than a benchmark table.

### Experiment 3: Positive reuse vs over-generalization

Evaluate episode and lesson memory on:

- reusable targets,
- near-miss targets,
- unrelated targets.

This prevents the project from degenerating into the simplistic claim that “more abstraction is better.”

---

## 6. Is ALFWorld a Reasonable Benchmark?

Yes, but only with explicit caveats.

### Why ALFWorld is attractive

- already available in the current repo,
- text-only and affordable,
- supports controlled memory injection,
- success/failure is easy to observe.

### Why ALFWorld is dangerous

The current repo’s own pilot work has already shown that some failures are dominated by:

- formatting mismatch,
- interaction protocol issues,
- repetitive invalid command behavior.

This means ALFWorld can easily measure interface brittleness instead of reusable experience.

### Resulting design decision

ALFWorld should be used only as a **controlled subset benchmark**:

- select task families where reusable lessons are interpretable,
- exclude cases dominated by pure formatting collapse,
- make the benchmark serve the question rather than define it.

This is consistent with the course-topic style: a project does not need to evaluate everything if a smaller controlled subset better matches the question.

---

## 7. Expected Contribution

If executed well, the project can make a contribution at the following level:

> A controlled empirical analysis of how a concrete experience changes in utility when abstracted into a reusable lesson.

More specifically, it can clarify:

- whether lesson-level abstraction improves reuse over episode-level memory,
- what information should not be abstracted away,
- when abstraction begins to over-generalize.

This is narrower than a general theory of agent memory, but strong enough for Topic 6 because it is:

- theoretically grounded,
- empirically testable,
- clearly scoped,
- not already fully answered by existing papers.

---

## 8. What This Proposal Is Not

To avoid repeating the problems of the earlier framing, the revised proposal should explicitly state that it is **not**:

- a project on whether an agent internally “understands” its own failures,
- a retrieval-paper disguised as a memory paper,
- a prompt-engineering study about staged context release,
- a full skill-induction or lifelong-learning system,
- a claim that episodic-to-semantic abstraction is universally optimal.

This matters because the project becomes stronger when it defines its non-goals clearly.

---

## 9. One-Sentence Judgment

> The revised proposal is substantially more defensible than the original one because it replaces latent correctness claims with a controlled memory-representation question; however, it remains viable only if it stays tightly focused on the `episode -> lesson` abstraction step and does not expand into retrieval, orchestration, or full procedural-skill learning.
