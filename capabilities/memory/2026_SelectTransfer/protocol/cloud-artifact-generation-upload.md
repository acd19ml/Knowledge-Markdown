# Cloud Artifact Generation Upload Guide

这份说明只服务于一个目标：

在云机器上运行 [04_artifact_generation.ipynb](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2026_SelectTransfer/notebooks/04_artifact_generation.ipynb)，生成：

- `episodic_trace.md`
- `cross_episode_consolidation.md`

## 推荐做法

最稳的方案不是零散拷文件，而是直接把整个 [2026_SelectTransfer](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2026_SelectTransfer) 目录上传到云机器。

这样做的好处是：

- notebook 不需要再改路径
- `pilot / archive / results / artifacts / notebooks` 的相对关系保持不变
- 后面继续做 `05_agent_runs.ipynb` 时也不需要重新整理目录

云端建议目录：

```text
/workspace/2026_SelectTransfer/
```

如果上传到别的位置，只要在 notebook 运行前设置：

```python
import os
os.environ["SELECT_TRANSFER_ROOT"] = "/你的/云端/2026_SelectTransfer"
```

即可。

## 最小上传方案

如果你现在只想跑 `04_artifact_generation.ipynb`，最少需要上传这些内容：

```text
2026_SelectTransfer/
├── notebooks/
│   └── 04_artifact_generation.ipynb
├── pilot/
│   └── archive/
│       ├── taxonomy_round1.csv
│       ├── source_sets_round1.csv
│       ├── pairing_table_round1.csv
│       └── notes_round1.md
├── results/
│   ├── 01_sampling/
│   │   └── sampled_20_full.json
│   └── 02_hotpotqa_comparison_expansion/
│       └── candidate_batch_filtered_full.json
└── artifacts/
```

其中：

- `pairing_table_round1.csv` 虽然这一步不直接参与 artifact 文本生成，但 notebook 当前会统一读取 frozen Round 1 输入，所以保留它更稳
- `notes_round1.md` 不是硬依赖，但建议一起保留，方便云端回看当前 frozen round 的来源
- `artifacts/` 可以一开始为空目录，notebook 会自动写入输出

## 云端运行前检查

在云机器中，至少确认：

- 目录里真的存在 `pilot/archive/taxonomy_round1.csv`
- 目录里真的存在 `results/01_sampling/sampled_20_full.json`
- `04_artifact_generation.ipynb` 能正确打印出 `PROJECT_ROOT`

只要这三项成立，路径通常就没有问题。

## 对应的当前默认模型

建议优先使用：

- `Qwen/Qwen3.5-9B`

如果显存不稳，回退到：

- `Qwen/Qwen3.5-4B`

不建议为了这一阶段的 artifact generation 一开始就上更大的 `Qwen3.5-27B`。
