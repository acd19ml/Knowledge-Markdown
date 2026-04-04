# Appendix A5. C5 Workflow Quality Table

> Purpose: support `C5` claims about workflow compactness, overlap, and prompt-level usage proxies.
>
> Primary source:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/runbook/c5-runbook.md`

## A5.1 Verified claims this appendix can support

1. Under the current approximation, the workflow libraries are compact.
2. Under the current approximation, pairwise function overlap is low.
3. `coverage` and `utility rate` are high under the current prompt-level proxy definition.
4. These metrics should still be interpreted as approximation-level evidence, not strict behavioral adherence.

## A5.2 First-run quality table

| Website | Condition | #workflows | coverage | function overlap | utility rate | Runbook status |
|---|---|---:|---:|---:|---:|---|
| `kayak` | `lm_wf` | 7 | 1.0 | 0.0 | 1.0 | `reproduced (first run)` |
| `newegg` | `lm_wf` | 5 | 1.0 | 0.0333 | 1.0 | `reproduced (first run)` |
| `united` | `lm_wf` | 5 | 1.0 | 0.0 | 1.0 | `reproduced (first run)` |

## A5.3 Runbook verdict excerpt

```text
first run completed; quality metrics reproduced under current approximation, but utility proxy remains loose
```

## A5.4 Supporting excerpt

```text
在 runbook 的当前近似定义下，三站点结果都支持 workflow quality 的方向性结论，
但 `utility rate` 仍应被理解为宽口径 proxy，而非真实遵循率。
```

## A5.5 Boundary notes

- `coverage = 1.0` and `utility rate = 1.0` here are prompt-level proxies.
- These values should not be reworded as “the model always followed the workflow.”
- The current safe wording is: the workflow text was consistently present and detectable in the prompt context under the runbook’s current approximation.
