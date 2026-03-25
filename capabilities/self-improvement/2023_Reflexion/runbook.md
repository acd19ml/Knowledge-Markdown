# Reflexion Runbook

> Workspace: [2023_Reflexion](/Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2023_Reflexion)
> Code root: [experiments](/Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2023_Reflexion/experiments)
> Primary current target: ALFWorld pilot for Topic 6 progress report

---

## 1. Purpose

This runbook records all CLI-facing work needed to run Reflexion in a reproducible way for the Topic 6 project.

It should answer:

- why a run is being executed,
- what result is expected,
- how the environment is configured,
- what commands need to be run,
- what environment variables are required,
- and what the current status / blockers are.

---

## 2. Current Research Role

Reflexion is used in this project for two purposes:

1. establish a runnable baseline for parameter-free self-improvement;
2. support **Analysis A: Reflection Diagnostic Accuracy** on ALFWorld.

Current priority:

- get a minimal ALFWorld pilot running,
- collect first-round failures,
- and preserve logs for later annotation.

---

## 3. Environment Isolation Plan

### Conda environment

Use a dedicated conda environment:

```bash
conda create -n Reflexion python=3.10 -y
conda activate Reflexion
```

Reasoning:

- the Reflexion repo contains multiple subprojects with partially separate dependencies;
- the current Topic 6 priority is ALFWorld and possibly HotpotQA, not the programming or WebShop tracks;
- a dedicated environment avoids collisions with ExpeL.

### Current known package sources

Reflexion has separate requirement files:

- [alfworld_runs/requirements.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2023_Reflexion/experiments/alfworld_runs/requirements.txt)
- [hotpotqa_runs/requirements.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2023_Reflexion/experiments/hotpotqa_runs/requirements.txt)

For ALFWorld, the repo requirement file only includes:

- `openai==0.27.0`
- `tenacity==8.1.0`

This is not sufficient by itself, because ALFWorld environment installation is external.

---

## 4. Environment Variables

### Required

```bash
export OPENAI_API_KEY="<your_openai_api_key>"
```

### Required for OpenAI-compatible third-party endpoints

If you use a third-party OpenAI-compatible provider, also set:

```bash
export OPENAI_API_BASE="<your_host_url>/v1"
```

### Likely required for ALFWorld

If ALFWorld is installed separately and expects a data path:

```bash
export ALFWORLD_DATA="<path_to_alfworld_data>"
```

Status:

- `OPENAI_API_KEY`: required by Reflexion OpenAI calls
- `OPENAI_API_BASE`: required when using an OpenAI-compatible third-party provider
- `ALFWORLD_DATA`: now fixed to the local ALFWorld dataset path

---

## 5. Planned CLI Setup

### Step 1. Activate environment

```bash
conda activate Reflexion
```

### Step 2. Install Reflexion ALFWorld run dependencies

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2023_Reflexion/experiments/alfworld_runs
pip install -r requirements.txt
```

### Step 3. Install ALFWorld environment package

This is not included in Reflexion’s own requirements file and must be handled separately.

Planned command:

```bash
pip install alfworld[full]
```

If needed later, we will pin a more specific version after first install feedback.

### Step 4. Configure API key

```bash
export OPENAI_API_KEY="<your_openai_api_key>"
export OPENAI_API_BASE="<your_host_url>/v1"
```

### Step 5. Inspect / edit run configuration

Default run script:

- [run_reflexion.sh](/Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2023_Reflexion/experiments/alfworld_runs/run_reflexion.sh)

Current default contents:

```bash
python main.py \
        --num_trials 10 \
        --num_envs 134 \
        --run_name "reflexion_run_logs" \
        --use_memory \
        --model "gpt-3.5-turbo"
```

For a pilot run, we should not start with the full 134-env, 10-trial configuration.

### Step 6. Pilot run

Planned pilot command:

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2023_Reflexion/experiments/alfworld_runs
python main.py \
  --num_trials 2 \
  --num_envs 10 \
  --run_name "topic6_reflexion_pilot" \
  --use_memory \
  --model "gpt-3.5-turbo"
```

### Step 7. Baseline run without memory

Planned baseline command:

```bash
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2023_Reflexion/experiments/alfworld_runs
python main.py \
  --num_trials 2 \
  --num_envs 10 \
  --run_name "topic6_reflexion_nomemory_pilot" \
  --model "gpt-3.5-turbo"
```

---

## 6. Expected Outputs

For the ALFWorld runs, expected outputs include:

- run logs under `alfworld_runs/root/<run_name>`
- trial-wise result files
- failure trajectories
- generated reflections when `--use_memory` is enabled

These outputs are needed for:

- baseline reporting in the progress report
- Analysis A failure annotation
- later comparison between correct vs incorrect reflection diagnoses

---

## 7. Current Run Status

### Status summary

- Environment created: yes
- Reflexion dependencies installed: yes
- ALFWorld Python package installed: yes
- ALFWorld dataset downloaded: yes
- Baseline smoke test completed: yes
- Memory-enabled smoke test completed: yes
- Memory-enabled `pilot8` run completed: yes

### Current blocker

- no immediate environment blocker remains for Reflexion ALFWorld smoke runs
- the next required step is to either expand the annotated sample beyond 10 cases or begin consolidating the pilot finding into the report

### Immediate next action

- preserve the current 10-case annotation result as the first pilot-scale Analysis A finding
- decide whether to expand Reflexion annotations to 15-20 cases or pivot to ExpeL environment setup
- avoid overwriting prior run directories; create a fresh `run_name` for every new run

### Last attempted commands

```bash
conda create -n Reflexion python=3.10 -y
conda activate Reflexion
cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2023_Reflexion/experiments/alfworld_runs
pip install -r requirements.txt
pip install "alfworld[full]"
```

### Latest successful run commands

```bash
conda activate Reflexion
export OPENAI_API_KEY="<your_openai_api_key>"
export OPENAI_API_BASE="<your_host_url>/v1"
export ALFWORLD_DATA="/Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2023_Reflexion/experiments/alfworld_runs/data/alfworld"

cd /Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2023_Reflexion/experiments/alfworld_runs

python main.py \
  --num_trials 1 \
  --num_envs 2 \
  --run_name "root/topic6_reflexion_nomemory_smoke" \
  --model "gpt-4o"

python main.py \
  --num_trials 1 \
  --num_envs 2 \
  --run_name "root/topic6_reflexion_memory_smoke_v2" \
  --use_memory \
  --model "gpt-4o"

python main.py \
  --num_trials 1 \
  --num_envs 8 \
  --run_name "root/topic6_reflexion_memory_pilot8" \
  --use_memory \
  --model "gpt-4o"
```

### Current observed pilot outcome

- `topic6_reflexion_nomemory_smoke`: `0 / 2` success
- `topic6_reflexion_memory_smoke_v2`: `0 / 2` success, with non-empty reflections
- `topic6_reflexion_memory_pilot8`: `0 / 8` success, with non-empty reflections in all environments

Interpretation:

- the current value of the Reflexion pipeline is not yet benchmark performance;
- it is the availability of analysis-ready failure traces and reflection artifacts for Analysis A.

### Verification already completed

```bash
which alfworld-download
echo "$ALFWORLD_DATA"
find . -maxdepth 3 -type d \( -name "json_2.1.1" -o -name "logic" \) 2>/dev/null
```

Observed state:

- `alfworld-download` exists in the `Reflexion` conda environment
- `ALFWORLD_DATA` was initially empty
- ALFWorld data was then downloaded to:
  - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/self-improvement/2023_Reflexion/experiments/alfworld_runs/data/alfworld`
- verified directories now include:
  - `logic`
  - `detectors`
  - `json_2.1.1`

### Additional project-specific adjustments

- added `.gitignore` entry for `experiments/alfworld_runs/data/`
- patched Reflexion ALFWorld code to support `OPENAI_API_BASE`
- patched Reflexion ALFWorld code to use `alfworld.agents.environment.get_environment(...)`
  instead of direct `getattr(...)`, to match the installed `alfworld` package API
- patched reflection generation so that `--use_memory` uses the same runtime model
  instead of hardcoding `text-davinci-003`

### First successful smoke run

Command:

```bash
python main.py \
  --num_trials 1 \
  --num_envs 2 \
  --run_name "root/topic6_reflexion_nomemory_smoke" \
  --model "gpt-4o"
```

Observed output summary:

- output directory created successfully
- files produced:
  - `env_results_trial_0.json`
  - `trial_0.log`
  - `world.log`
- result summary in `world.log`:
  - `SUCCESS: 0`
  - `FAIL: 2`
  - `TOTAL: 2`
  - `ACCURACY: 0.0`

Interpretation:

- environment + ALFWorld + API + logging pipeline are working
- this run is sufficient as a baseline smoke test artifact for the progress report

### First successful memory-enabled smoke run

Command:

```bash
python main.py \
  --num_trials 1 \
  --num_envs 2 \
  --run_name "root/topic6_reflexion_memory_smoke_v2" \
  --use_memory \
  --model "gpt-4o"
```

Observed output summary:

- output directory created successfully
- files produced:
  - `env_results_trial_0.json`
  - `trial_0.log`
  - `world.log`
- result summary in `world.log`:
  - `SUCCESS: 0`
  - `FAIL: 2`
  - `TOTAL: 2`
  - `ACCURACY: 0.0`
- `env_results_trial_0.json` now contains generated reflection text in each failed environment's `memory` field

Interpretation:

- the memory path is functioning end-to-end
- reflection generation is working with the configured third-party OpenAI-compatible endpoint
- the project now has the minimum required artifacts to begin Analysis A on a very small pilot scale

### Failed intermediate memory run retained intentionally

- existing directory:
  - `root/topic6_reflexion_memory_smoke`
- this earlier run failed before the memory path was repaired, due to hardcoded `text-davinci-003` usage
- the directory is intentionally preserved as an implementation/debugging artifact and is not to be treated as a valid experimental result

---

## 8. Notes for Report Writing

Once the first pilot run succeeds, record immediately:

- run date,
- environment name,
- command used,
- number of environments,
- number of trials,
- model used,
- output directory,
- whether reflections were produced,
- notable failure examples.

This information will later feed directly into:

- progress report `Implementation Progress`
- final report `Methodology`
- final report `Experiments`
