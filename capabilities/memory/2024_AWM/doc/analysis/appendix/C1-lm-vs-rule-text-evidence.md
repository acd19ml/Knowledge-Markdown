# Appendix C1. LM vs Rule Workflow Text Evidence

> Purpose: support the claim that LM-induced workflows are more abstract and reusable than rule-induced workflows at the text level.
>
> Primary source:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/wf_text_compare_output.txt`

## C1.1 Verified claims this appendix can support

1. LM workflows are shorter and more compact than rule workflows on `kayak`, `newegg`, and `united`.
2. LM workflows use placeholders while rule workflows preserve concrete values.
3. LM workflows are more abstract at the text level, but this evidence alone does not prove stronger site-wise performance.

## C1.2 Summary table from the source output

| Website | LM workflows | Rule workflows | LM avg steps/WF | Rule avg steps/WF | LM placeholders | Rule concrete values | Source verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| `kayak` | 8 | 17 | 1.8 | 12.5 | 13 | 25 | `SUPPORTED (4/4 indicators)` |
| `newegg` | 6 | 19 | 1.7 | 7.8 | 6 | 16 | `SUPPORTED (4/4 indicators)` |
| `united` | 6 | 24 | 2.7 | 9.0 | 15 | 41 | `SUPPORTED (4/4 indicators)` |

## C1.3 Source excerpts

### Kayak

```text
[Abstraction Indicators]
  + LM uses more placeholders (13 vs 0)
  + Rule retains more concrete values (25 vs 0)
  + LM workflows are more compact (1.8 vs 12.5 steps/wf)
  + LM has more abstract/reusable workflows (8 vs 0)

[Paper Claim: 'LM induction produces more abstract, reusable sub-routines']
  -> SUPPORTED (4/4 indicators)
```

### Newegg

```text
[Abstraction Indicators]
  + LM uses more placeholders (6 vs 0)
  + Rule retains more concrete values (16 vs 0)
  + LM workflows are more compact (1.7 vs 7.8 steps/wf)
  + LM has more abstract/reusable workflows (6 vs 0)
```

### United

```text
[Abstraction Indicators]
  + LM uses more placeholders (15 vs 0)
  + Rule retains more concrete values (41 vs 0)
  + LM workflows are more compact (2.7 vs 9.0 steps/wf)
  + LM has more abstract/reusable workflows (6 vs 0)
```

## C1.4 Representative workflow excerpts

### LM workflow example (`united`)

```text
## enter_flight_locations
[combobox]  Enter your departing city, airport name, or airpor... -> TYPE: {origin-city}
[button]  {origin-option} -> CLICK
[combobox]  Enter your destination city, airport name, or airp... -> TYPE: {destination-city}
[button]  {destination-option} -> CLICK
```

### Rule workflow example (`united`)

```text
Workflow 5: Concrete Trajectory for Find a round trip from Phoenix to Miami with...
Steps: [combobox]  Flying from -> TYPE: Phoenix; [button]  Phoenix, AZ, US (PHX) -> CLICK; [button]  Search -> CLICK ...
```

## C1.5 Boundary notes

- These counts currently follow the `wf_text_compare_output.txt` counting rule, which includes the `Summary Workflows` block.
- This appendix is text-structural evidence. It should be paired with score tables if the正文 wants to discuss performance consequences.
