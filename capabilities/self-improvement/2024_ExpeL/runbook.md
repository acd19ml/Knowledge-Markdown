# ExpeL Runbook

> Workspace: [2024_ExpeL](/Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2024_ExpeL)
> Code root: [experiments](/Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2024_ExpeL/experiments)
> Primary current target: prepare ALFWorld pipeline for Topic 6

---

## 1. Purpose

This runbook records all CLI-facing work needed to run ExpeL in a reproducible way for the Topic 6 project.

It should track:

- why a run is being executed,
- what result is expected,
- how the environment is configured,
- required commands,
- environment variables,
- and current blockers.

---

## 2. Current Research Role

ExpeL is used in this project for:

1. establishing a cross-task experience-learning baseline;
2. supporting **Analysis B: Experience Transfer Matrix**;
3. supporting **Analysis C: Retrieval Precision vs Utility**.

Current priority:

- prepare the environment cleanly,
- understand the train / insight extraction / eval pipeline,
- and reach a small ALFWorld pilot after Reflexion baseline infrastructure is stable.

---

## 3. Environment Isolation Plan

### Conda environment

Use a dedicated conda environment:

```bash
conda create -n ExpeL python=3.9.17 -y
conda activate ExpeL
```

Reasoning:

- the official README explicitly recommends Python 3.9.17;
- ExpeL has a broader dependency set than Reflexion;
- separate isolation avoids conflicts with Reflexion and any ALFWorld/WebShop side installs.

### Core package install

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2024_ExpeL/experiments
pip install -r requirements.txt
```

Known requirements file:

- [requirements.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2024_ExpeL/experiments/requirements.txt)

---

## 4. Environment Variables

### Required

The official code checks for:

```bash
export OPENAI_API_KEY="<your_openai_api_key>"
```

If you use an OpenAI-compatible third-party endpoint, also set:

```bash
export OPENAI_API_BASE="<your_host_url>/v1"
```

### Required for ALFWorld

Official README indicates:

```bash
export ALFWORLD_DATA="data/alfworld"
```

If local absolute paths are preferred, replace with the resolved local path after installation.

### Optional

The README also allows storing the OpenAI key in a `.env` file:

```bash
OPENAI_API_KEY=<your_openai_api_key>
```

For this project, explicit shell export is preferred because it is easier to audit in the runbook.

---

## 5. Planned CLI Setup

### Step 1. Activate environment

```bash
conda activate ExpeL
```

### Step 2. Install core dependencies

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2024_ExpeL/experiments
pip install -r requirements.txt
```

### Step 3. Install ALFWorld

Official README command:

```bash
pip install alfworld[full]
```

### Step 4. Reuse existing ALFWorld data if available

If Reflexion has already downloaded ALFWorld data locally, prefer reusing it via symlink instead of downloading again:

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2024_ExpeL/experiments/data
mkdir -p alfworld
ln -sfn /Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2023_Reflexion/experiments/alfworld_runs/data/alfworld/json_2.1.1 alfworld/json_2.1.1
ln -sfn /Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2023_Reflexion/experiments/alfworld_runs/data/alfworld/logic alfworld/logic
ln -sfn /Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2023_Reflexion/experiments/alfworld_runs/data/alfworld/detectors alfworld/detectors
```

### Step 5. Download ALFWorld data if reuse is not possible

Official README command:

```bash
export ALFWORLD_DATA="data/alfworld"
alfworld-download
```

### Step 6. Configure API key

```bash
export OPENAI_API_KEY="<your_openai_api_key>"
export OPENAI_API_BASE="<your_host_url>/v1"
```

---

## 6. ExpeL Pipeline to Reproduce

ExpeL has three main stages.

### Stage 1. Experience Gathering

Planned ALFWorld command:

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2024_ExpeL/experiments
python train.py benchmark=alfworld run_name=topic6_alfworld_train testing=false resume=false
```

Expected result:

- trajectory logs
- training-time experience pool

### Stage 2. Insight Extraction

Planned command:

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2024_ExpeL/experiments
python insight_extraction.py \
  benchmark=alfworld \
  load_run_name=topic6_alfworld_train \
  run_name=topic6_alfworld_insights \
  agent.llm=gpt-4 \
  agent.max_num_rules=10 \
  agent.success_critique_num=8 \
  testing=false \
  resume=false
```

Expected result:

- extracted insight files
- structured rules for later retrieval

### Stage 3. Evaluation

Planned command:

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2024_ExpeL/experiments
python eval.py \
  benchmark=alfworld \
  load_run_name=extracted_insights/topic6_alfworld_insights \
  run_name=topic6_alfworld_eval \
  agent.fewshot_strategy=task_similarity \
  agent.retrieval_kwargs.max_fewshot_tokens=auto \
  testing=false \
  resume=false
```

Expected result:

- evaluation logs
- retrieval records
- task outcomes

These outputs are needed for:

- ExpeL baseline reporting
- transfer analysis
- retrieval relevance analysis

---

## 7. Pilot Strategy for Topic 6

We should not start with full-scale ExpeL runs.

Recommended current sequence:

1. get the environment installed cleanly;
2. verify ALFWorld dependency and data setup;
3. avoid the full ALFWorld task file on the first run;
4. run a very small pilot before any full train / extract / eval loop.

The immediate goal is not to match the paper in full, but to establish an analysis-ready pipeline.

Current pilot file prepared for this purpose:

- [alfworld_tasks_suffix_smoke4.json](/Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2024_ExpeL/experiments/data/alfworld/alfworld_tasks_suffix_smoke4.json)

---

## 8. Current Run Status

### Status summary

- Environment created: yes
- Core dependencies installed: yes
- ALFWorld installed: yes
- OpenAI-compatible base URL support patched: yes
- ALFWorld environment constructor patched for current package API: yes
- Small ALFWorld smoke task file prepared: yes
- Experience gathering pilot completed: yes
- Insight extraction completed: not yet
- Evaluation completed: not yet

### Current blocker

- no immediate train-stage blocker remains for the 4-task ALFWorld smoke setup
- the next step is to inspect the smoke train artifacts and decide whether to proceed to insight extraction or to first summarize the pilot in the report

### Immediate next action

- keep the current `ExpeL` environment,
- inspect `topic6_expel_train_smoke4_v2` artifacts,
- summarize what the train-stage smoke run proves and what it does not yet prove,
- then decide whether to run a small insight-extraction pilot,
- keep `benchmark.task_file=...alfworld_tasks_suffix_smoke4.json` for any further smoke-scale runs,
- and keep `benchmark.general.use_cuda=false` on this machine.

### Latest successful recovery sequence

Run the following sequence inside the existing `ExpeL` environment:

```bash
conda activate ExpeL
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2024_ExpeL/experiments

pip install -r requirements.txt
pip install "setuptools<81" wheel
pip install "spacy<3.8"
pip install --no-build-isolation "visdom==0.2.4"
pip install "alfworld[full]"
```

Observed result:

- core ExpeL requirements installed successfully
- `spacy 3.7.5` installed successfully
- `alfworld 0.4.2` installed successfully
- ALFWorld-related packages including `textworld`, `jericho`, `ai2thor`, and `opencv-python` installed successfully

### Latest train-time error

During the first `train.py` smoke run, ExpeL failed while constructing the embedder:

- installed `sentence_transformers`: `2.2.2`
- installed `huggingface_hub`: `0.36.2`
- failure symptom: `ImportError: cannot import name 'cached_download' from 'huggingface_hub'`

This is a version compatibility issue between old `sentence_transformers` and new `huggingface_hub`.

### Current recovery plan

Run the following inside the existing `ExpeL` environment:

```bash
conda activate ExpeL
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2024_ExpeL/experiments

pip install "huggingface_hub==0.14.1"
```

### Latest train-time error after the hub fix

After downgrading `huggingface_hub`, ExpeL progressed into the first ALFWorld task, but then failed in `utils.token_counter(...)` because:

- installed `tiktoken`: `0.4.0`
- runtime model name: `gpt-4o`
- failure symptom: `KeyError: Could not automatically map gpt-4o to a tokeniser`

Local fallback patch applied:

- if `tiktoken.encoding_for_model(llm)` raises `KeyError`,
- fall back to `tiktoken.get_encoding("cl100k_base")`.

Preferred fix for the project:

- upgrade the requirement pin from `tiktoken==0.4.0` to `tiktoken==0.7.0`
- then keep the fallback patch as an additional guard rather than the primary mechanism

Reasoning:

- `tiktoken 0.7.0` is new enough to support `encoding_for_model("gpt-4o")`
- it still has a `CPython 3.9 / macOS 11.0+ ARM64` wheel, which matches the current machine
- using a direct model mapping is cleaner than relying on fallback behavior during all future runs

### Latest post-processing error

After upgrading `tiktoken`, the ExpeL smoke run executed the task loop and produced:

- `Finished. Success: 1, Fail: 2, Halted: 1`

The remaining failure occurred only in final plotting because `plot_trial_stats(...)` assumed:

- `len(parsed_result) == 134` for every ALFWorld run

Local patch applied:

- make ALFWorld summary normalization depend on `len(parsed_result)` dynamically
- so both `smoke4` and full 134-task runs use the same summary path

### Latest successful smoke train run

Run name:

- `topic6_expel_train_smoke4_v2`

Observed artifact files:

- `topic6_expel_train_smoke4_v2.pkl`
- `topic6_expel_train_smoke4_v2.txt`
- `topic6_expel_train_smoke4_v2_true.txt`
- `topic6_expel_train_smoke4_v2_logs_stats.png`

Observed run summary from the task loop:

- `Finished. Success: 1, Fail: 2, Halted: 1`

Interpretation:

- the ExpeL ALFWorld train-stage smoke pipeline is now runnable locally,
- but this is still only a smoke-scale infrastructure result, not yet a transfer-analysis result.

---

## 9. Notes for Report Writing

When the first ExpeL pilot is run, record:

- environment name,
- command used,
- benchmark,
- run name,
- whether train / extract / eval each completed,
- where logs were saved,
- whether retrieval logs were produced.

This information will later feed into:

- progress report `Implementation Progress`
- final report `Methodology`
- final report `Experiments`
