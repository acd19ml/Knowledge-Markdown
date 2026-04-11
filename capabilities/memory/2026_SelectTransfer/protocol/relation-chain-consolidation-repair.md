# Relation-Chain Consolidation Repair

This protocol defines how to diagnose and repair the remaining `relation_chain_bridge` consolidation failure after `Round 1g`.

It is intentionally narrower than previous rounds.

## Goal

The goal is **not** to improve the whole project at once.

The goal is only to test whether the current `relation_chain` consolidation artifact fails because it is:

- too abstract
- too conservative in `Applicability / Boundary`
- too weak on branch direction

## Scope

This repair applies only to:

- source set: `hp_relation_chain_bridge_set_01`
- target: `wiki_dev_2639`

It does not change:

- model
- `Round 1b` prompt scaffold
- scoring
- `episodic_trace`
- irrelevant `attribute_bridge` artifacts

## Current Failure Signature

The current relevant consolidation failure on `wiki_dev_2639` shows:

- explicit memory use
- drift toward definition checking
- loss of `## Final Answer`
- wrong kinship branch selection

So the repair should target:

1. branch selection
2. output stability
3. over-dominant boundary language

## Revised Consolidation Requirements

The revised consolidation should keep the same markdown structure, but it should be more operational.

It should explicitly reinforce:

- when the query asks about an in-law relation, first test the spouse branch
- if a named spouse is present in context, do not default to searching the subject's own siblings first
- prefer explicit named kinship links over abstract family-tree reasoning

It should explicitly avoid:

- long meta-discussion about possible definitions
- boundary notes that dominate the heuristic
- generic genealogy language that does not specify which branch to follow first

## Suggested Prompt Adjustment

When regenerating the consolidation, add constraints such as:

- make the `Operational Heuristic` branch-sensitive
- include one bullet for `in-law via spouse`
- include one bullet for `do not switch to the subject's own siblings unless the context supports that branch`
- keep `Boundary / Failure Risk` to 2 or 3 concise bullets
- require that the heuristic prioritizes explicit named relatives already present in context

## Minimal Evaluation Design

After generating a revised consolidation, compare only:

1. `no_memory`
2. original relevant consolidation
3. revised relevant consolidation
4. irrelevant consolidation

on:

- `wiki_dev_2639`

This is enough to answer whether the repair works better than the original consolidation without reopening the full run matrix.

## Success Criterion

The repair counts as promising if at least one of the following holds:

- revised relevant consolidation returns the correct answer
- revised relevant consolidation restores a valid `## Final Answer`
- revised relevant consolidation stays on the spouse branch instead of switching to Harriet's own siblings

## Failure Criterion

The repair is not sufficient if:

- revised relevant consolidation still fails in the same way
- the answer remains wrong and the reasoning still over-focuses on missing sibling mentions
- output formatting remains unstable

## Output Files

Round 1h should write to:

- `results/11_round1h_prep/`
- `results/11_round1h_run/`

and keep the revised artifact clearly separated from the original generated one.
