Write `cross_episode_consolidation.md` for the following frozen source set.

Source Set ID: hp_relation_chain_bridge_set_01
Cluster: bridge
Source Set Note: draft Hotpot relation-chain bridge set after Batch 2 final feasibility check

Input episodes:
- Task ID: hp_dev_7398
  - Question: Who was the brother of the wife of the Democratic Party nomination for Vice President in 1972?
  - Answer: President John F. Kennedy
  - Reasoning Label: bridge
  - Raw Type: bridge
  - Difficulty: hard
  - Taxonomy Note: vice-presidential nominee -> wife -> brother is a clean kinship chain
  - Supporting Titles: Sargent Shriver, Sargent Shriver, Eunice Kennedy Shriver

- Task ID: hp_dev_2485
  - Question: Who is the mother of Mary, Crown Princess of Denmark's husband?
  - Answer: Queen Margrethe II
  - Reasoning Label: bridge
  - Raw Type: bridge
  - Difficulty: hard
  - Taxonomy Note: wife -> husband -> mother is a clean spouse-to-parent continuation
  - Supporting Titles: Mary, Crown Princess of Denmark, Frederik, Crown Prince of Denmark
  - Supporting Sentences:
    - [Mary, Crown Princess of Denmark / sent 0] Mary, Crown Princess of Denmark, Countess of Monpezat, {'1': ", '2': ", '3': 'R.E.', '4': "} (Mary Elizabeth; "née" Donaldson; born 5 February 1972) is the wife of Frederik, Crown Prince of Denmark.

- Task ID: hp_dev_1892
  - Question: Matilda of Chester, Countess of Huntingdon's father was the son of which woman?
  - Answer: Maud of Gloucester
  - Reasoning Label: bridge
  - Raw Type: bridge
  - Difficulty: hard
  - Taxonomy Note: daughter -> father -> his mother is an explicit parent-child chain
  - Supporting Titles: Matilda of Chester, Countess of Huntingdon, Hugh de Kevelioc, 5th Earl of Chester
  - Supporting Sentences:
    - [Matilda of Chester, Countess of Huntingdon / sent 1] She was a daughter of Hugh de Kevelioc, 5th Earl of Chester, and the wife of David of Scotland, Earl of Huntingdon.

- Task ID: hp_dev_5315
  - Question: Barnstable County Hospital was the location of the autopsy of the son of President John F. Kennedy and Jacqueline Kennedy, and the younger brother of who?
  - Answer: Caroline Kennedy
  - Reasoning Label: bridge
  - Raw Type: bridge
  - Difficulty: hard
  - Taxonomy Note: son -> younger sister is a direct relation-chain target
  - Supporting Titles: Barnstable County Hospital, John F. Kennedy Jr.
  - Supporting Sentences:
    - [Barnstable County Hospital / sent 3] The hospital was the location of the autopsy of John F. Kennedy Jr., his wife, and her sister after their deaths.
    - [John F. Kennedy Jr. / sent 1] He was a son of President John F. Kennedy and First Lady Jacqueline Kennedy, and a younger brother of former Ambassador to Japan Caroline Kennedy.

- Task ID: hp_dev_7220
  - Question: The eldest daughter of Princess Louise of Denmark and Norway was the wife of a king whose motto was what?
  - Answer: God and the just cause
  - Reasoning Label: bridge
  - Raw Type: bridge
  - Difficulty: hard
  - Taxonomy Note: daughter -> wife of king -> motto is a clear multi-relation chain
  - Supporting Titles: Princess Louise of Denmark (1750–1831), Princess Louise of Denmark (1750–1831), Frederick VI of Denmark, Frederick VI of Denmark
  - Supporting Sentences:
    - [Princess Louise of Denmark (1750–1831) / sent 0] Princess Louise of Denmark and Norway (Danish: "Louise af Danmark" ; Norwegian: "Louise av Danmark" ) (20 January 1750 – 12 January 1831) was born to Frederick V of Denmark and Louise of Great Britain.
    - [Princess Louise of Denmark (1750–1831) / sent 1] Her eldest daughter, Marie of Hesse-Kassel, was the wife of Frederick VI of Denmark.

Required output structure:

# Cross-Episode Consolidation

## Source Set
- source_set_id: ...
- cluster: ...

## Shared Structure
- 3 to 5 bullets

## Applicability
- when this memory is likely useful
- when it is not the right memory to use

## Operational Heuristic
- a short ordered checklist for applying this memory form

## Boundary / Failure Risk
- 2 to 4 bullets

Important distinction:
- this artifact must be meaningfully more abstract than `episodic_trace`
- it should emphasize shared structure, applicability, and boundary conditions
- avoid empty advice like "read carefully" or "reason step by step" unless grounded in the episodes above
