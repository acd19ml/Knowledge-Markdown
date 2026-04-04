# Appendix A6. Alignment-Rate Note

> Purpose: provide a traceable source block for the exploratory alignment-rate numbers used in `§10.2`.
>
> Primary sources:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/scripts/alignment_rate.py`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/alignment_rate_output.txt`

## A6.1 What this metric is

`alignment_rate.py` computes a workflow-target alignment heuristic using keyword overlap between:

- workflow pattern descriptions
- target-element context extracted from the observation HTML

It is explicitly **not** a semantic-match metric.

## A6.2 Current site-wise values

| Website | Alignment rate | C1 status |
|---|---:|---|
| `budget` | 97.2% | not reproduced |
| `sixflags` | 94.2% | not reproduced |
| `newegg` | 90.9% | reproduced |
| `kayak` | 70.6% | reproduced |

## A6.3 Safe interpretation

- The metric is suitable for supporting the claim that **surface alignment does not reliably predict performance**.
- It is **not** strong enough to support semantic-fit claims on its own.
- `newegg` is an explicit exception to any monotonic “higher alignment = worse performance” story.

## A6.4 Source excerpt

```text
Heuristic: keyword overlap between workflow pattern descriptions
           and observation element context for each target action.
Limitations: label-lag, keyword ambiguity, placeholder fallback,
             no value-level matching for TYPE/SELECT.

SUMMARY TABLE
  kayak               17      6     34       24    70.6%
  newegg              14      7     44       40    90.9%
  budget              35     10     71       69    97.2%
  sixflags            18      7     52       49    94.2%
```
