# Final Report — Results Section

> **Support**
> - Main Round 1 narrative: [final-report-round1-section-v2.md](./final-report-round1-section-v2.md)
> - Claim traceability: [round1-evidence-map.md](./round1-evidence-map.md)
> - Key case evidence: [round1-case-appendix.md](./round1-case-appendix.md)

## 1. Overview

Round 1 did not produce a single headline score. Its main result is a **repair chain** that changed the interpretation of early negative-transfer evidence.

The strongest example is `wiki_dev_2639`, a `relation_chain_bridge` task. Early runs seemed to suggest that relevant memory could actively harm performance. After a sequence of controlled repairs, that interpretation no longer held.

The results are therefore best understood in three stages:

1. making memory behavior observable
2. repairing pairing granularity
3. repairing operator-level abstraction

## 2. Stage I: Making the Experiment Observable

The original pilot established the pipeline, but its outputs were hard to interpret because the model often answered in short, opaque lines.

Round 1b repaired this by introducing a structured scaffold with `## Reasoning` and `## Final Answer`. This produced two immediate outcome-level improvements:

- all smoke runs became parseable
- process-level behaviors such as **explicit memory use** and **explicit memory rejection** became visible

This did not, by itself, prove selective transfer. But it established that the experiment could now observe the difference between:

- using memory
- rejecting memory
- ignoring memory

Round 1c then showed that the six smoke cases could not be treated as a single mini-benchmark. Once cases were reassigned into `process sanity`, `diagnostic`, and `boundary` roles, the mixed aggregate lost its authority as a summary statistic.

## 3. Stage II: Repairing Pairing Granularity

The next major finding was that the original `bridge` label was too coarse. The experiment had paired a `relation_chain_bridge` target (`wiki_dev_2639`) with an `attribute_bridge` source set. What looked like "relevant memory hurts" was in fact a subtype mismatch.

After the source side was expanded and a new `relation_chain_bridge` source set was constructed, Round 1g reran only the affected targets. On `wiki_dev_2639`:

- **No Memory** remained correct
- **Relevant Episodic Trace** changed from wrong to correct
- **Irrelevant Episodic Trace** remained wrong

This is the strongest evidence that the earlier episodic failure was a **false negative created by coarse pairing**, not a genuine case of relevant negative transfer.

At this point, however, `Cross-Episode Consolidation` still failed on the same target. This shifted the bottleneck from pairing to the memory-form layer.

## 4. Stage III: Repairing Operator-Level Abstraction

Round 1h revised the relation-chain consolidation artifact, mainly by improving its structure and wording. This made the artifact cleaner, but it did not restore correctness on `wiki_dev_2639`.

The remaining failure was narrowed to a specific issue: the artifact still treated `sibling-in-law` as a vague natural-language category rather than an executable reasoning operator.

Round 1i repaired only this operator layer. It rewrote the `sibling-in-law` interpretation into explicit candidate paths and explicitly ruled out several irrelevant default branches.

This single change produced the following pattern on `wiki_dev_2639`:

- **Revised Relevant Consolidation (pre-operator repair):** still wrong
- **Operator-Repaired Relevant Consolidation:** correct
- **Irrelevant Consolidation:** still wrong

This is the strongest evidence that relevant consolidation did not fail because consolidation is inherently unhelpful. It failed because the abstraction was not executable enough for the target operator structure.

## 5. The Key Diagnostic Case

`wiki_dev_2639` is the single most informative case in the project. It is valuable because it supports a full before/after interpretation shift:

- the no-memory baseline is correct
- relevant memory initially degrades
- subtype-aware rerouting repairs episodic memory
- operator-aware repair repairs consolidation
- irrelevant memory remains wrong

This case therefore supports two distinct conclusions:

1. coarse pairing can manufacture false negative-transfer evidence
2. relevant abstract memory must remain executable at the operator level

The detailed reasoning traces for this case are documented in [round1-case-appendix.md](./round1-case-appendix.md).

## 6. What Round 1 Actually Shows

The Round 1 results support the following positive findings:

- process-level selectivity is observable once the scaffold is repaired
- mixed-role aggregate is not a valid summary
- subtype-aware pairing changes outcome on the strongest diagnostic case
- executable operator repair changes outcome for relevant consolidation on that same case

At the same time, the results do **not** support strong claims about large-scale benchmark gain. The repaired evidence remains concentrated in a small number of sensitive cases, especially `wiki_dev_2639`.

## 7. Final Result Interpretation

The most important outcome of Round 1 is not "memory improves performance." The real result is a methodological correction:

> Evidence that initially looked like relevant negative transfer was not stable under protocol repair.

Once the experiment repaired:

- observability
- case-role discipline
- subtype-level pairing
- operator-level abstraction

the strongest early negative example no longer supported the original negative interpretation.

This means the project's main contribution is not a broad efficacy claim. It is a demonstration that **selective-transfer evaluation is highly sensitive to how relevance and abstraction are operationalized**.
