# Final Report — Discussion Section

> **Support**
> - Main Round 1 narrative: [final-report-round1-section-v2.md](./final-report-round1-section-v2.md)
> - Claim traceability: [round1-evidence-map.md](./round1-evidence-map.md)
> - Key exhibits: [round1-case-appendix.md](./round1-case-appendix.md)

## 1. Main Interpretation

The main lesson of Round 1 is not that memory universally helps, nor that consolidation is categorically better or worse than episodic trace. The strongest lesson is methodological:

> selective-transfer claims are only as reliable as the operational definition of relevance and the executability of the memory abstraction.

This conclusion emerged because the project repeatedly found that early outcome-level patterns were not stable under protocol repair. In the most important case, what first appeared to be "relevant memory hurts" turned out to be a combination of:

- coarse pairing granularity
- mis-specified source subtype
- non-executable operator abstraction

Once those layers were repaired one by one, the negative interpretation no longer held.

## 2. Why This Matters Theoretically

The project started from a broader long-term question:

- when does experience become reusable knowledge rather than a stored trace?

Round 1 does not answer that large question directly. But it does support one narrower and useful theoretical implication:

**relevance alone is not enough.**

For memory to be usefully transferred, at least two additional conditions matter:

1. **The match must be defined at the right structural granularity.**  
   A coarse label such as `bridge` is too weak if the target actually depends on a more specific subtype such as `relation_chain_bridge`.

2. **The memory representation must preserve executable operator structure.**  
   For abstract memory, it is not enough to summarize "what kind of relation is involved." The artifact must encode how that relation should be checked.

This is why Round 1 is best interpreted as a clarification of what `selective transfer` should mean operationally, not as a final answer about the general usefulness of memory.

## 3. What Round 1 Can and Cannot Support

Round 1 can support:

- that process-level selectivity is observable
- that naive aggregates over mixed case roles are misleading
- that coarse pairing can create false negatives
- that executable abstraction is a necessary condition for some consolidation successes

Round 1 cannot support:

- strong claims about average benchmark gain
- large-scale demonstration of selective transfer
- universal ranking between episodic trace and consolidation
- broad generalization from a single repaired diagnostic case

These boundaries are not a weakness of the write-up. They are a consequence of the project's own experimental discipline.

## 4. Limitations

The current evidence has three important limitations.

### 4.1 Scale

The repaired evidence is concentrated in a small number of smoke and diagnostic cases. `wiki_dev_2639` is highly informative, but it is still one case.

### 4.2 Model Scope

All runs use `Qwen/Qwen3.5-9B`. A larger model might reduce some operator-level failures without explicit repair, but this was not tested here.

### 4.3 Outcome vs. Process Purity

The strongest repaired consolidation run becomes correct, but its reasoning still contains hesitation and self-correction. This means the repair is stronger at the outcome level than at the process level.

## 5. Implication for Future Work

If future work continues from this project, the next step should not be another long chain of single-case repairs. The better direction is:

- use the repaired protocol on a slightly broader but still carefully controlled diagnostic subset
- preserve case-role discipline
- keep subtype-aware pairing explicit
- test whether the `wiki_dev_2639` repair pattern generalizes to a few more relation-chain cases

The next round should therefore ask:

> Does the repaired workflow transfer beyond one key diagnostic case?

This is a much cleaner next question than reopening average-gain comparisons or adding more uncontrolled memory conditions.

## 6. Final Discussion Takeaway

Round 1 should be read as a **measurement and interpretation success**, not as a benchmark-win story.

Its value lies in showing that:

- apparent negative transfer may be an artifact of experimental granularity
- abstract memory fails when it is not executable enough
- careful repair can reverse an incorrect conclusion without changing the model itself

This makes the project useful even without large-scale gains. It provides a more defensible protocol for asking when memory is genuinely reusable and when it is merely present.
