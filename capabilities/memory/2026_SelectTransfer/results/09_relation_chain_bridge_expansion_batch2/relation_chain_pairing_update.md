# Relation-Chain Pairing Update

Date: 2026-04-11

## Purpose

After constructing `hp_relation_chain_bridge_set_01`, the working pairing table should no longer treat all `bridge` targets as if `hp_bridge_set_01` were automatically relevant.

This note records the minimum subtype-aware pairing update needed before any rerun.

## Updated Targets

### `wiki_dev_2639`

- old relevant source: `hp_bridge_set_01`
- new relevant source: `hp_relation_chain_bridge_set_01`
- new irrelevant source: `hp_bridge_set_01`

reason:

- target is a `relation_chain_bridge` case
- old relevant source was only cluster-matched at coarse `bridge` level
- new irrelevant source should now be subtype-mismatched `attribute_bridge`, not just cross-cluster `comparison`

### `wiki_dev_1379`

- old relevant source: `hp_bridge_set_01`
- new relevant source: `hp_relation_chain_bridge_set_01`
- new irrelevant source: `hp_bridge_set_01`

reason:

- this target is also relation-chain style on the target side
- it should be rerouted to the new subtype-matched source set for any future rerun

## What Did Not Change

The following bridge targets remain mapped to `hp_bridge_set_01`:

- `wiki_dev_0092`
- `wiki_dev_10378`
- `wiki_dev_7019`
- `wiki_dev_6083`

because they still behave more like `attribute_bridge` than `relation_chain_bridge`.

## Immediate Implication

The project is now ready for:

1. artifact generation for `hp_relation_chain_bridge_set_01`
2. a minimal subtype-aware rerun focused on the rerouted relation-chain targets

It is **not** necessary to reopen generic bridge pairing for all targets.
