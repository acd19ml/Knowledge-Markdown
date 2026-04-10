# notebooks/

Colab notebooks for each experiment phase. Run on Google Colab (GPU for agent runs, CPU for data prep).

| Notebook | Phase | GPU needed? |
|---|---|---|
| [01_sampling.ipynb](01_sampling.ipynb) | Sample first 20 tasks from HotpotQA + 2WikiMultiHopQA | No (CPU) |
| 02_agent_runs.ipynb | Run ReAct agent under each condition | Yes (RTX 4090 recommended) |
| 03_analysis.ipynb | Aggregate results, split-level metrics, case review | No (CPU) |

Notebooks 02 and 03 will be created when needed.
