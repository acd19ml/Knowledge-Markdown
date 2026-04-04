# Appendix A1. Step-Level Breakdown Evidence

> Purpose: support step-level claims about where AWM gains and losses come from in `C1`.
>
> Primary source:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/step_breakdown_output.txt`

## A1.1 Verified claims this appendix can support

1. `TYPE`-side gains are more stable than `CLICK`-side gains.
2. `CLICK` performance is highly site-dependent and often determines whether a site-level result is reproduced.
3. On some reproduced sites, gains concentrate more strongly in later steps; on not-reproduced sites, later-step degradation can be larger.

## A1.2 Representative step-level deltas from the source output

| Website | Condition | `CLICK dElem / dStepSR` | `TYPE dElem / dActF1 / dStepSR` | `first_half dStepSR` | `second_half dStepSR` |
|---|---|---:|---:|---:|---:|
| `budget` | `offline_wf - no_workflow` | `-12.1 / -12.1` | `+0.0 / +8.4 / +9.1` | `-1.9` | `-10.9` |
| `kayak` | `offline_wf - no_workflow` | `+10.7 / +10.7` | `+0.0 / +1.4 / +0.0` | `+0.0` | `+13.0` |
| `newegg` | `offline_wf - no_workflow` | `+9.1 / +6.1` | `+33.3 / +50.0 / +33.3` | `+4.4` | `+7.1` |
| `sixflags` | `offline_wf - no_workflow` | `-6.1 / -6.1` | `+0.0 / +0.0 / +0.0` | `-5.9` | `-3.3` |
| `united` | `offline_wf - no_workflow` | `+3.6 / +3.6` | `+16.7 / +2.8 / +0.0` | `+3.0` | `+0.0` |
| `yellowpages` | `offline_wf - no_workflow` | `+0.0 / +0.0` | `+28.6 / +19.5 / +28.6` | `+0.0` | `+7.1` |

## A1.3 Source excerpts

### Kayak

```text
[Delta: offline_wf - no_workflow] by action_type
  CLICK                   +10.7%     +3.6%    +10.7%
  SKIP                     +0.0%     +0.0%     +0.0%
  TYPE                     +0.0%     +1.4%     +0.0%

[Delta: offline_wf - no_workflow] by step_half
  first_half               +0.0%     +0.3%     +0.0%
  second_half             +13.0%     +4.3%    +13.0%
```

### Budget

```text
[Delta: offline_wf - no_workflow] by action_type
  CLICK                   -12.1%     -1.7%    -12.1%
  SELECT                   +0.0%     +0.0%     +0.0%
  SKIP                     +0.0%     +0.0%     +0.0%
  TYPE                     +0.0%     +8.4%     +9.1%

[Delta: offline_wf - no_workflow] by step_half
  first_half               -3.8%     +3.6%     -1.9%
  second_half             -10.9%     -4.3%    -10.9%
```

### Newegg

```text
[Delta: offline_wf - no_workflow] by action_type
  CLICK                    +9.1%     -3.0%     +6.1%
  SELECT                   +0.0%    +20.0%    +25.0%
  SKIP                     +0.0%     +0.0%     +0.0%
  TYPE                    +33.3%    +50.0%    +33.3%
```

## A1.4 Boundary notes

- This appendix supports direction-of-effect claims, not causal proof.
- `TYPE` counts are small on several sites, so the main robust use is qualitative: `TYPE` gains are often non-negative while `CLICK` varies sharply by site.
- Later-step accumulation is strongest on `kayak`; other sites show weaker or mixed support.
