# Relation-Chain Kinship Operator Repair

This protocol defines the next minimal repair after `Round 1h`.

It assumes:

- subtype mismatch has already been repaired
- `relation_chain` episodic memory already works on the sensitive case
- revised consolidation already restored structured output

So the remaining target is narrower.

## Goal

The goal is **not** to redesign relation-chain memory again.

The goal is only to test whether the remaining failure comes from incorrect interpretation of kinship operators such as:

- `sibling-in-law`
- `brother-in-law`
- `sister-in-law`

## Scope

This repair applies only to:

- source set: `hp_relation_chain_bridge_set_01`
- target: `wiki_dev_2639`
- artifact type: `cross_episode_consolidation`

It does not change:

- model
- `Round 1b` prompt scaffold
- scoring
- routing
- irrelevant memory
- `episodic_trace`

## Current Failure Signature

After `Round 1h`, the remaining failure pattern is:

- structured output is present
- relevant consolidation is still wrong
- answer collapses to a conservative refusal
- reasoning does not operationalize `sibling-in-law` into a correct executable branch

This means the repair should target:

1. kinship operator normalization
2. candidate branch ordering
3. relation-direction sanity

## Required Operator Guidance

The revised consolidation should explicitly state:

1. When the query contains `sibling-in-law`, treat it as:
   - first candidate: spouse's sibling
   - second candidate: sibling's spouse
2. Do **not** treat:
   - parent
   - grandparent
   - spouse of parent
   as valid default paths for this operator.
3. If the subject's spouse is explicitly named in context, check the spouse's known sibling links before concluding the answer is missing.

## Required Heuristic Style

The heuristic should remain short and executable.

It should prefer:

- explicit relation normalization first
- explicit spouse branch next
- explicit named relative retrieval after that

It should avoid:

- generic genealogy discussion
- long boundary sections
- broad family-tree language with no candidate ordering

## Minimal Evaluation Design

After generating an operator-repaired consolidation, compare only:

1. `no_memory`
2. `revised relevant consolidation` from Round 1h
3. `operator-repaired relevant consolidation`
4. `irrelevant consolidation`

on:

- `wiki_dev_2639`

This is enough to test whether operator repair adds information beyond the Round 1h repair.

## Success Criterion

The repair counts as promising if at least one of the following holds:

- operator-repaired relevant consolidation returns `Henry Pelham`
- reasoning explicitly identifies `Thomas Pelham-Holles` as Harriet's spouse and `Henry Pelham` as the spouse's sibling
- the refusal-style answer disappears

## Failure Criterion

The repair is not sufficient if:

- answer remains `Cannot be determined from the provided context.`
- reasoning still does not resolve `sibling-in-law` into explicit candidate relations
- relevant consolidation remains behaviorally indistinguishable from irrelevant consolidation

## Output Files

Round 1i should write to:

- `results/12_round1i_prep/`
- `results/12_round1i_run/`

and keep the operator-repaired artifact clearly separated from the Round 1h version.
