# Negative Cases: qwen/qwen3.5-397b-a17b_test_task_kayak_html_only

Total negative steps: 2, showing top 2


## Case 1: task=3, step=1/8

**Task:** Task: From Birmingham (BHX) to Paris search for packages with casinos, restaurant, fitness and a free internet from April 7th to 11th.

**Target:** `TYPE [7202] [Las Vegas]`

**Baseline pred:** `TYPE [7202] [Las Vegas]` (ea=1, af=1.00)

**Workflow pred:** `TYPE [7202] [LAS VEGAS]` (ea=1, af=0.33)


## Case 2: task=4, step=11/14

**Task:** Task: check cheap flights from NYC to London on 23rd of April for students over 18 years.

**Target:** `CLICK [97197]`

**Baseline pred:** `CLICK [97197]` (ea=1, af=1.00)

**Workflow pred:** `CLICK [97672]` (ea=0, af=1.00)
