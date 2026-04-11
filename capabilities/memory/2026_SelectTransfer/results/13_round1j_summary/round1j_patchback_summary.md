# Round 1j Patchback Summary

Date: 2026-04-11

## Objective

Patch the repaired relation-chain evidence for `wiki_dev_2639` back into the role-aware interpretation layer.

## Why This Patchback Is Needed

- The original Round 1c table still reflects the coarse-bridge / pre-repair behavior for `wiki_dev_2639`.
- After Round 1g and Round 1i, that case no longer supports the same diagnosis.

## Before vs After on `wiki_dev_2639`

| condition | split | Round 1c status | patched status | interpretation |
|---|---|---|---|---|
| episodic_trace | relevant | EM=0 / Cannot be determined from the provided context. | EM=1 / Henry Pelham | relevant episodic is now recovered by subtype-aware routing |
| episodic_trace | irrelevant | EM=0 / Cannot be determined from the provided context | EM=0 / Cannot be determined from the provided context. | irrelevant memory remains harmful / refusal-prone |
| cross_episode_consolidation | relevant | EM=0 / Cannot be determined from the provided context. | EM=1 / Henry Pelham | relevant consolidation is now recovered after operator repair |
| cross_episode_consolidation | irrelevant | EM=1 / Henry Pelham | EM=0 / Cannot be determined from the provided context. | irrelevant memory remains harmful / refusal-prone |

## Updated Interpretation

- `wiki_dev_2639` should no longer be described as a case where relevant bridge memory harms an originally correct baseline.
- After subtype-aware rerouting and operator repair, the relevant memory path becomes recoverable in both `episodic_trace` and `cross_episode_consolidation`.
- The more accurate interpretation is now: this case exposed a false negative caused by coarse pairing granularity plus incomplete operator guidance inside consolidation.

## Implication for Round 1 Synthesis

- The strongest remaining diagnostic message is no longer `relevant memory can hurt on this bridge case`.
- The stronger message is `selective transfer claims are highly sensitive to pairing granularity and to how abstract memory operationalizes relation operators`.

## Next Step

- Use this patched interpretation in the final Round 1 synthesis instead of the original Round 1c wording for `wiki_dev_2639`.
