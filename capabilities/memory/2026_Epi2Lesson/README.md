# Epi2Lesson

> Full name: **From Episodic Experience to Reusable Lessons**
>
> Research focus: **experience abstraction for cross-task reuse in LLM agents**

## Why this project belongs under `memory/`

Although the project was initially developed under `self-improvement/`, the revised core question is fundamentally a memory question rather than a generic self-improvement question:

> How does abstraction from episodic experience to reusable lessons affect cross-task reuse in LLM agents?

More specifically, the project studies one transition inside the memory hierarchy already used in this repo:

- `episodic memory -> semantic lesson`

This makes `memory/` the more appropriate long-term home for the research.

## Current active documents

- [proposal.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2026_Epi2Lesson/proposal.md) — current proposal
- [progress-report.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2026_Epi2Lesson/progress-report.md) — current progress report
- [proposal-analysis.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2026_Epi2Lesson/proposal-analysis.md) — proposal revision logic
- [experiment-plan.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2026_Epi2Lesson/experiment-plan.md) — experiment framework

## Current research question

> **How does abstraction from episodic experience to reusable lessons affect cross-task reuse in LLM agents?**

This project compares two memory units:

- **Episode memory**: a concrete, context-rich description of a past task event
- **Lesson memory**: a reusable abstraction distilled from the same experience

## Planned benchmark setting

- Primary benchmark: **ALFWorld**
- Strategy: use a controlled subset rather than a full leaderboard reproduction
- Goal: compare `No memory`, `Episode memory`, and `Lesson memory`

## Immediate next steps

1. Define a controlled ALFWorld subset where reusable lessons are interpretable.
2. Design a stable `episode -> lesson` construction template.
3. Run the first revised comparison among `No memory`, `Episode memory`, and `Lesson memory`.

## Naming note

`Epi2Lesson` is intentionally simple:

- `Epi` points to episodic memory
- `Lesson` points to semantic abstraction for reuse

It is descriptive enough for notes, experiments, and future report writing without committing too early to a larger framework name.
