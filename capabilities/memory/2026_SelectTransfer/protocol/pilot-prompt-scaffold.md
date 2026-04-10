# Pilot Prompt Scaffold

这份文件定义 Round 1 pilot run 中三个条件的 prompt 结构。

核心原则：**三个条件除了 memory 注入部分，其余完全一致。**

## 1. 条件定义

| Condition | Memory Injected | Memory Content |
|---|---|---|
| `no_memory` | No | — |
| `episodic_trace` | Yes | `artifacts/<source_set_id>/episodic_trace.md` |
| `cross_episode_consolidation` | Yes | `artifacts/<source_set_id>/cross_episode_consolidation.md` |

## 2. Base Prompt（所有条件共享）

```text
You are a question-answering agent. Your task is to answer a multi-hop reasoning question using the provided context paragraphs.

## Context

{context_paragraphs}

## Question

{question}

## Instructions

- Read all context paragraphs carefully.
- Identify the reasoning chain needed to answer the question.
- Provide your final answer as a short phrase (not a full sentence).
- If the question asks "which", "who", or "what", respond with the specific entity name.
- If the question asks for a comparison, respond with the entity that satisfies the comparison.

## Answer
```

### 字段说明

- `{context_paragraphs}`：从 target task 的 `raw.context` 中提取，每个 title 下的 sentences 拼成段落
- `{question}`：target task 的 `question` 字段

## 3. Memory Block（仅 memory 条件注入）

在 Base Prompt 的 `## Instructions` 之前插入：

```text
## Past Experience

The following notes summarize patterns from previously solved tasks that may or may not be relevant to the current question. Use them only if they help your reasoning — do not force-apply them.

{memory_content}
```

### 字段说明

- `{memory_content}`：对应 artifact 文件的完整 markdown 内容
- 注意措辞："may or may not be relevant" — 不暗示 memory 一定有用，避免 bias

## 4. 三个条件的完整结构

### Condition: `no_memory`

```
[Base Prompt]
```

### Condition: `episodic_trace`

```
[Base Prompt — Context section]
[Base Prompt — Question section]
[Memory Block with episodic_trace.md content]
[Base Prompt — Instructions section]
[Base Prompt — Answer section]
```

### Condition: `cross_episode_consolidation`

```
[Base Prompt — Context section]
[Base Prompt — Question section]
[Memory Block with cross_episode_consolidation.md content]
[Base Prompt — Instructions section]
[Base Prompt — Answer section]
```

## 5. Context 构造规则

从 target task 的 `raw.context` 字段提取：

```python
def build_context_paragraphs(raw_context):
    """
    raw_context: JSON string -> list of [title, [sent1, sent2, ...]]
    Note: in sampled_20_full.json, context is stored as a JSON string, not a Python list.
    """
    import json
    if isinstance(raw_context, str):
        raw_context = json.loads(raw_context)
    paragraphs = []
    for entry in raw_context:
        title = entry[0]
        sentences = entry[1] if len(entry) > 1 else []
        text = " ".join(str(s) for s in sentences)
        paragraphs.append(f"### {title}\n{text}")
    return "\n\n".join(paragraphs)
```

所有 context 段落都保留（包括 distractor 段落），不做过滤。这是因为：

- 原始 benchmark 本身包含 distractor
- 过滤掉 distractor 会改变任务难度，引入额外变量

## 6. Prompt Assembly 伪代码

```python
def assemble_prompt(target_task, condition, artifact_content=None):
    context = build_context_paragraphs(target_task['raw']['context'])
    question = target_task['question']

    base_header = (
        "You are a question-answering agent. "
        "Your task is to answer a multi-hop reasoning question "
        "using the provided context paragraphs."
    )

    context_section = f"## Context\n\n{context}"
    question_section = f"## Question\n\n{question}"

    if condition == 'no_memory':
        memory_section = ""
    else:
        memory_section = (
            "## Past Experience\n\n"
            "The following notes summarize patterns from previously solved tasks "
            "that may or may not be relevant to the current question. "
            "Use them only if they help your reasoning — do not force-apply them.\n\n"
            f"{artifact_content}"
        )

    instructions_section = (
        "## Instructions\n\n"
        "- Read all context paragraphs carefully.\n"
        "- Identify the reasoning chain needed to answer the question.\n"
        "- Provide your final answer as a short phrase (not a full sentence).\n"
        "- If the question asks \"which\", \"who\", or \"what\", "
        "respond with the specific entity name.\n"
        "- If the question asks for a comparison, "
        "respond with the entity that satisfies the comparison."
    )

    answer_section = "## Answer"

    parts = [base_header, "", context_section, "", question_section]
    if memory_section:
        parts += ["", memory_section]
    parts += ["", instructions_section, "", answer_section]

    return "\n\n".join(parts)
```

## 7. 固定约束

以下在 Round 1 中不允许变化：

- Base Prompt 措辞
- Memory Block 位置（Instructions 之前）
- Memory Block 引导语（"may or may not be relevant"）
- Context 构造方式（全量保留，不过滤 distractor）
- Instructions 内容
- Answer 格式要求

如果需要修改上述任何一项，必须停止当前 round，开新版本。

## 8. 评分规则

从模型输出中提取 `## Answer` 之后的文本作为 predicted answer。

```python
def extract_answer(model_output):
    """Extract the answer after '## Answer' marker."""
    if '## Answer' in model_output:
        return model_output.split('## Answer')[-1].strip()
    # Fallback: take the last non-empty line
    lines = [l.strip() for l in model_output.strip().split('\n') if l.strip()]
    return lines[-1] if lines else ''


def compute_em(pred, gold):
    """Exact match after normalization."""
    return normalize(pred) == normalize(gold)


def compute_f1(pred, gold):
    """Token-level F1."""
    pred_tokens = set(normalize(pred).split())
    gold_tokens = set(normalize(gold).split())
    if not pred_tokens or not gold_tokens:
        return 0.0
    precision = len(pred_tokens & gold_tokens) / len(pred_tokens)
    recall = len(pred_tokens & gold_tokens) / len(gold_tokens)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def normalize(text):
    """Lowercase, strip articles/punctuation, collapse whitespace."""
    import re, string
    text = text.lower()
    # Remove articles
    text = re.sub(r'\b(a|an|the)\b', ' ', text)
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Collapse whitespace
    text = ' '.join(text.split())
    return text
```

## 9. Logging 字段确认

每次 run 写入 `results/pilot_results.csv`，字段如下：

| Field | Round 1 规则 |
|---|---|
| `run_id` | `r1_{condition}_{target_task_id}_{split}` |
| `target_task_id` | 来自 pairing table |
| `split` | `relevant` / `irrelevant` |
| `condition` | `no_memory` / `episodic_trace` / `cross_episode_consolidation` |
| `source_set_id` | 来自 pairing table，`no_memory` 条件下仍填写对应 source set id 以保持可追溯性 |
| `routing_decision` | Round 1 固定为 `n/a`（无 judgment 条件） |
| `memory_attached` | `no_memory` = `false`；其余 = `true` |
| `em` | 0 或 1 |
| `f1` | 0.00 到 1.00 |
| `token_usage` | prompt + completion tokens |
| `failure_status` | `ok` / `error` / `timeout` |
| `note` | case-level 观察 |

## 10. 结果解释对照表

在跑之前预设好"现象 -> 解释 -> 下一步"：

| 现象 | 解释 | 下一步 |
|---|---|---|
| relevant 涨，irrelevant 不掉 | memory 有 selective transfer value | 继续加 judgment 条件 |
| relevant 涨，irrelevant 也掉 | memory 被滥用，存在 negative transfer | 检查 artifact 质量 / pairing 是否不干净 |
| relevant 不涨，irrelevant 不掉 | setup 不敏感 | 先查 pairing / artifact / prompt scaffold |
| relevant 不涨，irrelevant 也掉 | memory 纯损害 | 停止，彻底检查 artifact + pairing |
| episodic 和 consolidation 无差异 | memory form 变量没有拉开 | 检查 artifact 是否实质不同 |
| episodic 涨但 consolidation 不涨 | 抽象化损失了有效信息 | 考虑 consolidation prompt 修订 |
| consolidation 涨但 episodic 不涨 | 抽象化帮助了 pattern 识别 | 支持后续加 judgment 条件 |
