# Negative Cases: qwen/qwen3.5-397b-a17b_test_task_kayak_desc_only

Total negative steps: 3, showing top 3


## Case 1: task=1, step=9/10

**Task:** Task: Search for the cheapest two rooms near Kashi Vishwanath Temple in India for three adults and a 7-year-old kid from June 6 to 10 in any 3-star and up air-conditioned family hotel with a review score of at least 8, free internet.

**Target:** `CLICK [57318]`

**Baseline pred:** `CLICK [57318]` (ea=1, af=1.00)

**Workflow pred:** `CLICK [60634]` (ea=0, af=1.00)


## Case 2: task=2, step=1/5

**Task:** Task: Get the hotel with highest review score having free internet and free cancelation in Chennai for 20/03/23

**Target:** `TYPE [5037] [Qatar Airways]`

**Baseline pred:** `TYPE [5037] [Qatar Airways]` (ea=1, af=1.00)

**Workflow pred:** `TYPE [5037] [qatar airways]` (ea=1, af=0.33)


## Case 3: task=3, step=1/8

**Task:** Task: From Birmingham (BHX) to Paris search for packages with casinos, restaurant, fitness and a free internet from April 7th to 11th.

**Target:** `TYPE [7202] [Las Vegas]`

**Baseline pred:** `TYPE [7202] [Las Vegas]` (ea=1, af=1.00)

**Workflow pred:** `TYPE [7202] [las vegas]` (ea=1, af=0.33)
