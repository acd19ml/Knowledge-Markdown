# Cross-Episode Consolidation

## Source Set
- source_set_id: hp_relation_chain_bridge_set_01
- cluster: bridge

## Shared Structure
- Decompose multi-hop questions into a linear sequence of atomic relation steps.
- Identify the starting entity and the target attribute to define the chain endpoints.
- Retrieve intermediate entities that explicitly link the current node to the next required relation.
- Validate the final retrieved entity against the target attribute before concluding.
- Maintain strict adherence to the specific kinship operator requested, avoiding semantic drift.

## Applicability
- **Use when**: The query requires traversing a chain of at least two distinct relational hops (e.g., A is related to B, who is related to C) where the intermediate entity is not directly named in the question.
- **Do not use when**: The question asks for a direct relation between two entities, or when the required intermediate entity is explicitly provided in the context.

## Operational Heuristic
1. **Parse and Isolate**: Extract the starting entity and the final target attribute from the question text.
2. **Normalize Kinship Operators**: Convert natural language kinship terms into explicit candidate relation pairs.
   - For `sibling-in-law`, strictly evaluate candidates in this order:
     1. `spouse_of` -> `sibling`
     2. `sibling` -> `spouse_of`
   - For other terms (e.g., `wife`, `mother`, `son`), map directly to the corresponding atomic relation.
3. **Execute Forward Chain**:
   - Retrieve the entity connected by the first normalized relation.
   - If the retrieved entity is a person, check if a spouse is explicitly named in the context.
   - **If a spouse is named**: Immediately pivot to the `spouse_of` branch to continue the chain.
   - **If no spouse is named**: Proceed to the next relation in the sequence.
4. **Validate Termination**: Verify the final entity possesses the target attribute. If the chain breaks or the attribute is missing, halt and report failure.
5. **Enforce Operator Boundaries**: Do not substitute the requested kinship operator with `parent`, `grandparent`, or `spouse-of-parent` unless the question explicitly requests those specific relations.

## Boundary / Failure Risk
- High risk of hallucinating intermediate entities if the context lacks explicit links between the first and second hop.
- Failure to normalize `sibling-in-law` into the two specific candidate orders often leads to retrieving the wrong branch of the family tree.
- Prematurely assuming a parent/grandparent relationship when the question asks for an in-law relation due to insufficient context checking.
