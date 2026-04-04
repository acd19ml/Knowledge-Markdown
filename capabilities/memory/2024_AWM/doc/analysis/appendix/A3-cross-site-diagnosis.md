# Appendix A3. Cross-Site Degradation Diagnosis

> Purpose: support claims about why `C2` degrades under cross-site or cross-domain transfer.
>
> Primary source:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/cross_site_diag_output.txt`

## A3.1 Verified claims this appendix can support

1. `tripadvisor` is best characterized as a mixed case: workflow-content mismatch plus target-site grounding degradation.
2. `reddit` is better characterized as workflow-content mismatch without strong evidence of generic grounding collapse.
3. In both cases, negative steps are dominated by `CLICK` errors rather than pure value-format failures.

## A3.2 Summary table

| Target | Model / setup | Positive | Negative | Skip-rate shift vs source | CLICK share of negatives | Source verdict |
|---|---|---:|---:|---:|---:|---|
| `tripadvisor` | `qwen/qwen3.5-397b-a17b / online_wf` | 4 | 18 | `+16pp` (`44.9%` vs `29.2%`) | `78%` | mixed `A + B` |
| `reddit` | `qwen/qwen3.5-397b-a17b / online_wf` | 2 | 5 | `+4.7pp` (`33.9%` vs `29.2%`) | `80%` | primarily `A` |

## A3.3 Source excerpts

### Reddit

```text
[Degradation Profile: online_wf]
  Positive: 2, Negative: 5, Ineffective: 87, Redundant: 86

[Hypothesis B: Element grounding collapse]
  Skip rate (target baseline): 33.9%
  Skip rate (source baseline): 29.2%
  CLICK Elem Acc (target baseline): 84.2%
  CLICK Elem Acc (source baseline): 75.0%
  -> No strong B evidence (baseline performs similarly)

[Hypothesis A: Workflow content mismatch]
  Negative steps: 5
    CLICK: 4  TYPE: 1
    CLICK share of negatives: 80%
  -> A evidence: Negatives dominated by CLICK (element-level mismatch, not value mismatch)

[Preliminary Verdict]
  -> Primarily Hypothesis A: workflow content is mismatched
```

### Tripadvisor

```text
[Degradation Profile: online_wf]
  Positive: 4, Negative: 18, Ineffective: 131, Redundant: 72

[Hypothesis B: Element grounding collapse]
  Skip rate (target baseline): 44.9%
  Skip rate (source baseline): 29.2%
  CLICK Elem Acc (target baseline): 81.2%
  CLICK Elem Acc (source baseline): 75.0%
  -> B evidence: Skip rate +16pp higher on target site

[Hypothesis A: Workflow content mismatch]
  Negative steps: 18
    CLICK: 14  TYPE: 4
    CLICK share of negatives: 78%
  -> A evidence: Negatives dominated by CLICK (element-level mismatch, not value mismatch)

[Preliminary Verdict]
  -> Mixed: both element grounding degradation AND workflow mismatch
```

## A3.4 Boundary notes

- This appendix supports the *diagnostic direction* of the cross-site explanation.
- It should not be used to claim a full causal decomposition.
- The strongest safe summary is:
  - `reddit`: primarily workflow-content mismatch
  - `tripadvisor`: mismatch plus additional target-site grounding difficulty
