# Pilot Prompt Scaffold: Round 1b

这份文件定义 `Round 1b` 使用的 prompt scaffold。

目标不是一次性提升分数，而是做一个更干净的 prompt / measurement diagnosis：

- 让模型不再只输出单行答案
- 让 memory 是否被利用，至少在输出层可见
- 保持 `memory form`、target tasks、source sets、pairing、model 不变

## 1. Round 1b 唯一允许变化的变量

与 Round 1 相比，`Round 1b` 只改：

- prompt scaffold

具体变化：

- 要求模型输出 `## Reasoning`
- 要求模型输出 `## Final Answer`
- answer extractor 只从 `## Final Answer` 取答案

不变的内容：

- model
- source set
- pairing
- artifacts
- memory block 位置
- decoding params

## 2. Base Prompt

```text
You are a question-answering agent. Your task is to answer a multi-hop reasoning question using the provided context paragraphs.

## Context

{context_paragraphs}

## Question

{question}

## Instructions

- Read all context paragraphs carefully.
- Work through the reasoning chain explicitly before deciding the answer.
- In `## Reasoning`, write 3 to 6 short bullet points grounded in the provided context.
- If past experience is shown, either use it explicitly or state briefly why it is not useful here.
- Keep the reasoning concise and evidence-grounded.
- In `## Final Answer`, give only the final short answer phrase.

## Reasoning

## Final Answer
```

## 3. Memory Block

和 Round 1 相同，仍然放在 `## Instructions` 之前：

```text
## Past Experience

The following notes summarize patterns from previously solved tasks that may or may not be relevant to the current question. Use them only if they help your reasoning — do not force-apply them.

{memory_content}
```

这里故意不改 `memory block` 的措辞，避免把 `prompt scaffold` 的变化和 `memory policy` 混在一起。

## 4. 结构化输出要求

### 合法输出示例

```text
## Reasoning
- The question asks for a comparison between two entities.
- The context gives Billy Magoulias as born in 1997.
- The context gives Jean-Baptiste Le Prince as born in 1734.
- 1734 is earlier than 1997.

## Final Answer
Jean-Baptiste Le Prince
```

### 非法输出示例

- 只输出单行答案
- 没有 `## Final Answer`
- `## Final Answer` 后跟一整段解释

## 5. Answer Extraction Rule

Round 1 的 extractor 默认取 `## Answer` 之后文本。Round 1b 改成：

```python
def extract_final_answer(model_output):
    if '## Final Answer' in model_output:
        return model_output.split('## Final Answer')[-1].strip().splitlines()[0].strip()
    lines = [l.strip() for l in model_output.strip().split('\n') if l.strip()]
    return lines[-1] if lines else ''
```

## 6. 新增过程指标

除了 `EM` / `F1` 之外，Round 1b 还要记录：

- `reasoning_present`
  - 是否出现 `## Reasoning`
- `final_answer_present`
  - 是否出现 `## Final Answer`
- `memory_reference_type`
  - `explicit_use`
  - `explicit_reject`
  - `implicit_or_none`

这些指标的作用不是替代分数，而是判断新 scaffold 是否真的让 memory interaction 变得可观察。

## 7. Round 1b 成功信号

至少满足以下两条中的两条：

- 大多数 run 不再是单行直答
- `## Final Answer` 可稳定解析
- 至少 2 个 case 的 reasoning 中出现对 `Past Experience` 的显式使用或显式拒绝

## 8. Round 1b 失败信号

出现以下任一情况，就不进入 full rerun：

- 模型仍然基本只输出单行答案
- `## Final Answer` 解析频繁失败
- reasoning 只是模板空话，和 context / memory 无关

## 9. Scope

这份 scaffold 优先用于 `smoke subset`，不是默认直接替换 full round。

建议先在以下 case 上跑：

- `wiki_dev_8896`
- `wiki_dev_0092`
- `wiki_dev_2639`
- `wiki_dev_6083`
- `wiki_dev_7019`
- `wiki_dev_10727`
