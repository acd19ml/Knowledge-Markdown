# Episodic Trace

## Source Set
- source_set_id: hp_relation_chain_bridge_set_01
- cluster: bridge

## Episode Summaries
### 1. hp_dev_7398
- question: Who was the brother of the wife of the Democratic Party nomination for Vice President in 1972?
- answer: President John F. Kennedy
- key lookup path: 1972 VP Nominee (Sargent Shriver) -> Wife (Eunice Kennedy Shriver) -> Brother (John F. Kennedy)
- minimal support: Sargent Shriver was the nominee; his wife was Eunice Kennedy Shriver; her brother was President John F. Kennedy.
- reusable cue: Kinship chains often require traversing a spouse link to reach the target relative.

### 2. hp_dev_2485
- question: Who is the mother of Mary, Crown Princess of Denmark's husband?
- answer: Queen Margrethe II
- key lookup path: Mary (Crown Princess) -> Husband (Frederik, Crown Prince) -> Mother (Queen Margrethe II)
- minimal support: Mary is the wife of Frederik, Crown Prince of Denmark; Frederik's mother is Queen Margrethe II.
- reusable cue: Spouse-to-parent queries require identifying the immediate partner before accessing the parent node.

### 3. hp_dev_1892
- question: Matilda of Chester, Countess of Huntingdon's father was the son of which woman?
- answer: Maud of Gloucester
- key lookup path: Matilda -> Father (Hugh de Kevelioc) -> Mother (Maud of Gloucester)
- minimal support: Matilda was the daughter of Hugh de Kevelioc, 5th Earl of Chester; Hugh's mother was Maud of Gloucester.
- reusable cue: Parent-child chains are explicit; the target is the mother of the identified father.

### 4. hp_dev_5315
- question: Barnstable County Hospital was the location of the autopsy of the son of President John F. Kennedy and Jacqueline Kennedy, and the younger brother of who?
- answer: Caroline Kennedy
- key lookup path: JFK Jr. (autopsy at Barnstable) -> Sibling (Caroline Kennedy)
- minimal support: John F. Kennedy Jr. died at Barnstable County Hospital; he was the younger brother of Caroline Kennedy.
- reusable cue: Location-based entity anchors can lead directly to a sibling relation if the entity's biography is linked to the location.

### 5. hp_dev_7220
- question: The eldest daughter of Princess Louise of Denmark and Norway was the wife of a king whose motto was what?
- answer: God and the just cause
- key lookup path: Princess Louise -> Eldest Daughter (Marie of Hesse-Kassel) -> Husband (Frederick VI of Denmark) -> Motto (God and the just cause)
- minimal support: Marie of Hesse-Kassel was the eldest daughter of Princess Louise; she married Frederick VI of Denmark; his motto was "God and the just cause".
- reusable cue: Multi-hop chains involving royal titles often require traversing a "daughter -> wife of" link to reach the monarch.

## Local Pattern Notes
- Bridge reasoning in this set consistently involves a three-step kinship traversal (e.g., Nominee -> Wife -> Brother).
- Specific entity titles (e.g., "Crown Princess," "Countess of Huntingdon") serve as critical anchors for disambiguating parent-child relationships.
- Queries frequently require identifying an intermediate spouse or child before accessing the final target attribute (motto, mother, sibling).
- Supporting sentences often explicitly define the immediate relationship (e.g., "was the wife of," "was a daughter of") which must be chained sequentially.
- Difficulty is driven by the necessity to maintain the correct lineage direction (e.g., finding the mother of the husband, not the husband of the mother).
