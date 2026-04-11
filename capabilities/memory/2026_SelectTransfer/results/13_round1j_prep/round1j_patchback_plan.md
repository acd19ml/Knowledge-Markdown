# Round 1j Patchback Plan

Date: 2026-04-11

## Goal

Update the role-aware interpretation layer so that `wiki_dev_2639` is no longer summarized using its pre-repair behavior.

## Why This Is Necessary

The original `Round 1c` role-aware table still reflects:

- coarse `bridge` routing
- pre-subtype relation-chain behavior
- pre-operator-repair consolidation behavior

That is no longer the best available evidence for `wiki_dev_2639`.

## Evidence to Patch Back

### From Round 1g

Use:

- `episodic_trace + relevant` on `wiki_dev_2639`
- `episodic_trace + irrelevant` on `wiki_dev_2639`

because these rows reflect subtype-aware routing.

### From Round 1i

Use:

- operator-repaired relevant `cross_episode_consolidation` on `wiki_dev_2639`
- irrelevant `cross_episode_consolidation` on `wiki_dev_2639`

because these rows reflect the best current consolidation evidence.

## Interpretation Update

The old interpretation:

- `wiki_dev_2639` = key derailment case where relevant bridge artifact harms an originally correct baseline

should be replaced with:

- `wiki_dev_2639` = repaired diagnostic case showing that coarse pairing granularity and incomplete operator abstraction can create a false negative transfer diagnosis

## Output

Round 1j should write:

- [../13_round1j_summary/round1j_wiki_dev_2639_patch_rows.csv](../13_round1j_summary/round1j_wiki_dev_2639_patch_rows.csv)
- [../13_round1j_summary/round1j_patchback_summary.md](../13_round1j_summary/round1j_patchback_summary.md)

## Next Step After Patchback

Use the patched interpretation in:

- Round 1 synthesis
- final project report

Do not continue treating `wiki_dev_2639` as primary evidence for “relevant memory can hurt” without qualification.
