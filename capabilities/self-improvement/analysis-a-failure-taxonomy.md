# Analysis A Failure Taxonomy Draft

> Project: Topic 6 — Stress-Testing the Assumptions of Parameter-Free Agent Self-Improvement
> Target system: Reflexion
> Goal: create an annotation scheme for judging whether generated reflections correctly diagnose failure causes

---

## 1. Purpose

This document defines an initial failure taxonomy for **Analysis A: Reflection Diagnostic Accuracy**.

The purpose is to make manual annotation consistent across failed Reflexion trajectories.

For each failed trajectory, we want to label:

1. the most likely ground-truth failure cause;
2. whether the generated reflection correctly identifies that cause;
3. whether the next-attempt plan is actionable or generic.

---

## 2. Draft Failure Categories

### F1. Formatting / interaction protocol failure

Definition:

- the agent fails because it does not follow the expected action-output interaction format of the environment.

Typical signals:

- repeated meta-planning instead of executable actions
- malformed action syntax
- failure to issue valid environment commands

### F2. Goal misunderstanding

Definition:

- the agent misreads or incompletely interprets the task objective.

Typical signals:

- wrong target object
- wrong target receptacle
- wrong operation sequence

### F3. Search failure

Definition:

- the agent understands the goal but fails to find the required object or location.

Typical signals:

- incomplete exploration
- repeatedly checking non-promising locations
- stopping before sufficient search coverage

### F4. Repetitive loop / stuck policy

Definition:

- the agent repeats similar actions without gaining new state information.

Typical signals:

- revisiting the same location
- retrying the same invalid or unproductive action
- reflection itself mentions being stuck in a loop

### F5. Missing prerequisite action

Definition:

- the agent does not execute a necessary intermediate step.

Typical signals:

- failing to open a receptacle before retrieving an object
- forgetting to clean / cool / heat before placement
- forgetting to pick up the object before transport

### F6. Object-state or environment-state misunderstanding

Definition:

- the agent fails because it misunderstands the current state of an object or the environment.

Typical signals:

- assuming an object is already cooled / cleaned / available
- assuming an appliance is ready when it is not

### F7. Generic or non-actionable reasoning failure

Definition:

- the agent produces vague planning text that does not translate into concrete executable steps.

Typical signals:

- abstract statements without environment-grounded actions
- broad advice like "be more careful" or "avoid repetition" without specific next steps

---

## 3. Annotation Fields

For each failed trial, annotate the following:

| Field | Description |
|------|-------------|
| `run_name` | experiment directory |
| `env_id` | environment id within the run |
| `task_summary` | short paraphrase of the task |
| `ground_truth_failure_type` | one primary label from F1-F7 |
| `secondary_failure_type` | optional secondary label |
| `reflection_mentions_true_cause` | yes / partial / no |
| `reflection_actionable` | yes / partial / no |
| `notes` | short qualitative note |

---

## 4. Current Pilot Observations

From the first memory-enabled smoke run:

- one reflection explicitly mentions formatting / interaction problems
- another reflection emphasizes structured search and avoiding repetition

These suggest that at least the following categories are immediately relevant:

- F1. Formatting / interaction protocol failure
- F3. Search failure
- F4. Repetitive loop / stuck policy
- F7. Generic or non-actionable reasoning failure

This is still only a draft; final labels should be assigned after reading the full `trial_0.log`.

---

## 5. Next Step

Before doing formal annotation, inspect:

- the no-memory smoke `trial_0.log`
- the memory-enabled smoke `trial_0.log`

The full action-observation traces are needed before assigning reliable ground-truth labels.

---

## 6. Pilot Annotation on the First Two Reflexion Failures

Using the no-memory smoke `trial_0.log` together with the memory-enabled smoke artifacts, we can already annotate two pilot cases.

### Case 1: `env_0` — "put a cool tomato in microwave"

Observed behavior:

- the agent never transitions into valid environment actions;
- it repeatedly outputs meta-explanations, troubleshooting text, and restatements of the task;
- almost every turn receives `Nothing happens.`

Most likely ground-truth failure type:

- **Primary**: F1. Formatting / interaction protocol failure
- **Secondary**: F7. Generic or non-actionable reasoning failure

Why:

- the agent appears to misunderstand the environment as a conversational interface rather than a command-based simulator;
- it produces explanatory prose instead of executable actions.

Generated reflection quality:

- **reflection_mentions_true_cause**: `partial`
- **reflection_actionable**: `partial`

Reason:

- the reflection correctly notices an interaction / formatting issue;
- however, it mixes that diagnosis with a generic high-level plan rather than a precise fix in the command format actually required by the environment.

### Case 2: `env_1` — "put a clean spatula in drawer"

Observed behavior:

- again, the agent fails to issue valid simulator actions;
- it repeatedly says it will proceed step by step but remains trapped in explanatory text;
- the environment keeps returning `Nothing happens.`

Most likely ground-truth failure type:

- **Primary**: F1. Formatting / interaction protocol failure
- **Secondary**: F7. Generic or non-actionable reasoning failure

Why:

- the failure is not due to misunderstanding the task itself;
- the task decomposition is broadly correct, but execution never begins because the interaction format is wrong.

Generated reflection quality:

- **reflection_mentions_true_cause**: `yes`
- **reflection_actionable**: `partial`

Reason:

- this reflection explicitly identifies formatting / interaction issues more clearly than in Case 1;
- however, the repair suggestion is still only moderately actionable because it remains abstract and does not fully commit to concrete environment commands.

---

## 7. Preliminary Interpretation

Even from just two pilot failures, an important pattern already emerges:

- the dominant early failure is not goal misunderstanding;
- it is **interface-use failure**.

This matters for Analysis A because it suggests a possible mismatch between:

- what Reflexion is supposed to improve,
- and what actually causes failure in practice.

If many early failures are due to interaction formatting rather than strategic planning, then even a diagnostically correct reflection may have limited downstream benefit unless it produces a strongly executable repair plan.

This gives Analysis A a sharper research question:

> Is Reflexion failing because it diagnoses the wrong cause, or because even correct diagnoses remain too generic to repair behavior?
