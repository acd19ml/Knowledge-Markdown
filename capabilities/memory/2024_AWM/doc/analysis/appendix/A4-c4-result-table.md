# Appendix A4. C4 Result Table

> Purpose: support `C4` claims about `NL vs HTML` and `code vs text workflow`.
>
> Primary source:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/runbook/c4-runbook.md`

## A4.1 Verified claims this appendix can support

1. `NL vs HTML` is `not reproduced` after the three-site first run.
2. In the current prompt-level code representation, `code workflow` and `text workflow` are similar on the first `kayak` run.

## A4.2 `NL vs HTML` first-run results

| Website | Condition | Element Acc | Action F1 | Step SR | SR |
|---|---|---:|---:|---:|---:|
| `kayak` | `desc_only` | 54.8 | 61.2 | 45.3 | 0.0 |
| `kayak` | `html_only` | 52.4 | 63.5 | 48.0 | 0.0 |
| `kayak` | `desc_html` | 54.8 | 63.5 | 50.3 | 0.0 |
| `united` | `desc_only` | 57.9 | 61.9 | 55.9 | 33.3 |
| `united` | `html_only` | 61.2 | 64.5 | 60.6 | 33.3 |
| `united` | `desc_html` | 57.9 | 61.1 | 51.7 | 16.7 |
| `newegg` | `desc_only` | 42.0 | 44.3 | 30.5 | 0.0 |
| `newegg` | `html_only` | 36.2 | 42.6 | 23.9 | 0.0 |
| `newegg` | `desc_html` | 38.0 | 42.4 | 30.3 | 0.0 |

## A4.3 `code vs text workflow` first-run result

| Website | Condition | Element Acc | Action F1 | Step SR | SR |
|---|---|---:|---:|---:|---:|
| `kayak` | `text_wf` | 55.3 | 60.8 | 45.8 | 0.0 |
| `kayak` | `code_wf` | 52.4 | 63.4 | 48.0 | 0.0 |

## A4.4 Runbook verdict excerpts

### `NL vs HTML`

```text
C4 首轮已完成。`NL vs HTML` 已在 kayak、united、newegg 三个网站上完成首轮运行，
现有结果不足以支持论文所声称的“Desc only 优于 HTML only”，因此该子结论可先冻结为 not reproduced。
```

### `code vs text workflow`

```text
C4-R4 / test_task / kayak / code vs text workflow 已归档。当前结果显示 text workflow 与 code workflow
在主要指标上仅有小幅波动，SR 持平，未出现单边稳定大幅优势。
因此，在当前 prompt-level code 表示口径下，本轮支持“code workflow 与 text workflow 差异不大”的结论。
```

## A4.5 Boundary notes

- This appendix supports first-run result claims only.
- `code vs text workflow` currently has one audited site (`kayak`), not a three-site result.
