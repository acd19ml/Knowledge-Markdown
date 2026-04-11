# Cross-Episode Consolidation

## Source Set
- source_set_id: hp_relation_chain_bridge_set_01
- cluster: bridge

## Shared Structure
- **Multi-hop Kinship Navigation**: The core task involves traversing a sequence of familial relations (e.g., spouse → parent, child → sibling) where the target entity is not directly linked to the query subject in a single hop.
- **Explicit Intermediate Anchoring**: Successful resolution relies on identifying a specific intermediate entity (the "bridge") that connects the starting subject to the final target through documented parent-child or spousal relationships.
- **Contextual Disambiguation**: Entities often share names or titles across different generations or families; the reasoning process requires filtering supporting sentences to confirm the specific lineage (e.g., distinguishing between different "Princess Louise" or "John F. Kennedy" figures).
- **Attribute Retrieval via Chain**: The final answer is frequently a non-person attribute (e.g., a motto, a specific name) that is only accessible after completing the full relational chain to the correct individual.

## Applicability
- **Use when**: The query explicitly asks for a relationship that requires traversing at least two distinct relational steps (e.g., "X's Y's Z") and the provided text contains explicit statements defining those intermediate links.
- **Use when**: The problem involves resolving ambiguity in historical or genealogical data where multiple individuals with similar titles exist, requiring sentence-level verification of lineage.
- **Not useful when**: The answer is directly stated in the text without requiring intermediate relational inference (single-hop retrieval).
- **Not useful when**: The required relational links are implied but not explicitly stated in the supporting sentences, as this specific cluster relies on explicit "A is the B of C" phrasing.

## Operational Heuristic
1. **Identify the Gap**: Determine the number of relational hops required to connect the query subject to the target (e.g., Subject → Relation A → Bridge Entity → Relation B → Target).
2. **Locate the Bridge**: Scan supporting sentences for the entity that serves as the pivot point between the known subject and the unknown target.
3. **Verify Lineage**: Cross-reference titles and dates in the text to ensure the bridge entity belongs to the correct branch of the family tree, avoiding false positives from similarly named individuals.
4. **Execute Final Hop**: Once the bridge is confirmed, retrieve the final attribute or relation from the sentence describing the bridge's connection to the target.

## Boundary / Failure Risk
- **Ambiguous Titles**: Failure to distinguish between individuals with identical or similar titles (e.g., different Princesses of Denmark) can lead to traversing the wrong branch of the family tree.
- **Missing Explicit Links**: If the text describes a relationship indirectly (e.g., "X married Y's brother") without explicitly naming the intermediate person, this specific bridge pattern may fail.
- **Contextual Noise**: Supporting sentences may contain multiple unrelated family members; extracting the wrong sentence can break the chain logic.
- **Directionality Errors**: Confusing the direction of the relation (e.g., treating "mother of" as "child of") will result in retrieving the wrong intermediate entity.
