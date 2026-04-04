# Appendix A2. Paired-Case Summary Evidence

> Purpose: support claims about how often workflow actually changes behavior, and whether changed steps are net positive or net negative.
>
> Primary source:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/paired_case_output.txt`

## A2.1 Verified claims this appendix can support

1. On reproduced `C1` sites such as `kayak` and `newegg`, `negative = 0`.
2. On not-reproduced `C1` sites such as `budget` and `sixflags`, `negative > positive`.
3. Workflow changes behavior on only a small minority of steps.
4. A large fraction of steps are either `ineffective` or `redundant`.

## A2.2 Corrected overall totals for the seven `C1` websites

> This table corrects the earlier erroneous denominator `523`.  
> The total paired-step count for the seven audited `C1` sites is `475`.

| Category | Count | Pct of all paired steps |
|---|---:|---:|
| `positive` | 26 | `5.5%` |
| `negative` | 24 | `5.1%` |
| `ineffective` | 252 | `53.1%` |
| `redundant` | 173 | `36.4%` |
| `changed = positive + negative` | 50 | `10.5%` |

Among changed steps only:

| Metric | Value |
|---|---:|
| `positive / (positive + negative)` | `26 / 50 = 52.0%` |
| `net gain` | `+2 steps` |

## A2.3 Site-wise evidence from `C1`

| Website | Total | Positive | Negative | Ineffective | Redundant | Verdict pattern |
|---|---:|---:|---:|---:|---:|---|
| `budget` | 99 | 6 | 12 | 53 | 28 | negative-dominated |
| `kayak` | 48 | 3 | 0 | 22 | 23 | reproduced, no negatives |
| `kohls` | 53 | 2 | 2 | 33 | 16 | mixed |
| `newegg` | 87 | 5 | 0 | 56 | 26 | reproduced, no negatives |
| `sixflags` | 64 | 3 | 6 | 23 | 32 | negative-dominated |
| `united` | 63 | 3 | 2 | 35 | 23 | slight positive edge |
| `yellowpages` | 61 | 4 | 2 | 30 | 25 | slight positive edge |

## A2.4 Source excerpts

### Kayak

```text
[Overall Distribution]
  positive             3    6.2%
  negative             0    0.0%
  ineffective         22   45.8%
  redundant           23   47.9%

[Workflow Impact]
  Positive / (Positive + Negative) = 3/3 = 100.0%
  Net gain (positive - negative)   = +3 steps
```

### Newegg

```text
[Overall Distribution]
  positive             5    5.7%
  negative             0    0.0%
  ineffective         56   64.4%
  redundant           26   29.9%
```

### Budget

```text
[Overall Distribution]
  positive             6    6.1%
  negative            12   12.1%
  ineffective         53   53.5%
  redundant           28   28.3%
```

### Sixflags

```text
[Overall Distribution]
  positive             3    4.7%
  negative             6    9.4%
  ineffective         23   35.9%
  redundant           32   50.0%
```

## A2.5 Boundary notes

- This appendix supports statements about behavioral footprint and sign of net change.
- It should not be used to claim that all changed steps are equally important.
- The corrected denominator `475` should be used consistently wherever these `C1` distributions are discussed.
