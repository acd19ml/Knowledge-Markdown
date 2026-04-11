Write an operator-repaired `cross_episode_consolidation.md` for the following source set.

Source Set ID: hp_relation_chain_bridge_set_01
Cluster: bridge
Source Set Note: draft Hotpot relation-chain bridge set after Batch 2 final feasibility check

Input episodes:

### hp_dev_7398
- question: Who was the brother of the wife of the Democratic Party nomination for Vice President in 1972?
- answer: President John F. Kennedy
- reasoning_label: bridge
- taxonomy_note: vice-presidential nominee -> wife -> brother is a clean kinship chain
- raw_type: bridge
- level: hard
- support_titles: Sargent Shriver, Sargent Shriver, Eunice Kennedy Shriver
- minimal_support:
  - [Sargent Shriver#1] 
  - [Sargent Shriver#3] 
  - [Eunice Kennedy Shriver#0] 


### hp_dev_2485
- question: Who is the mother of Mary, Crown Princess of Denmark's husband?
- answer: Queen Margrethe II
- reasoning_label: bridge
- taxonomy_note: wife -> husband -> mother is a clean spouse-to-parent continuation
- raw_type: bridge
- level: hard
- support_titles: Mary, Crown Princess of Denmark, Frederik, Crown Prince of Denmark
- minimal_support:
  - [Mary, Crown Princess of Denmark#0] Mary, Crown Princess of Denmark, Countess of Monpezat, {'1': ", '2': ", '3': 'R.E.', '4': "} (Mary Elizabeth; "née" Donaldson; born 5 February 1972) is the wife of Frederik, Crown Prince of Denmark.
  - [Frederik, Crown Prince of Denmark#1] 


### hp_dev_1892
- question: Matilda of Chester, Countess of Huntingdon's father was the son of which woman?
- answer: Maud of Gloucester
- reasoning_label: bridge
- taxonomy_note: daughter -> father -> his mother is an explicit parent-child chain
- raw_type: bridge
- level: hard
- support_titles: Matilda of Chester, Countess of Huntingdon, Hugh de Kevelioc, 5th Earl of Chester
- minimal_support:
  - [Matilda of Chester, Countess of Huntingdon#1] She was a daughter of Hugh de Kevelioc, 5th Earl of Chester, and the wife of David of Scotland, Earl of Huntingdon.
  - [Hugh de Kevelioc, 5th Earl of Chester#0] 


### hp_dev_5315
- question: Barnstable County Hospital was the location of the autopsy of the son of President John F. Kennedy and Jacqueline Kennedy, and the younger brother of who?
- answer: Caroline Kennedy
- reasoning_label: bridge
- taxonomy_note: son -> younger sister is a direct relation-chain target
- raw_type: bridge
- level: hard
- support_titles: Barnstable County Hospital, John F. Kennedy Jr.
- minimal_support:
  - [Barnstable County Hospital#3] The hospital was the location of the autopsy of John F. Kennedy Jr., his wife, and her sister after their deaths.
  - [John F. Kennedy Jr.#1] He was a son of President John F. Kennedy and First Lady Jacqueline Kennedy, and a younger brother of former Ambassador to Japan Caroline Kennedy.


### hp_dev_7220
- question: The eldest daughter of Princess Louise of Denmark and Norway was the wife of a king whose motto was what?
- answer: God and the just cause
- reasoning_label: bridge
- taxonomy_note: daughter -> wife of king -> motto is a clear multi-relation chain
- raw_type: bridge
- level: hard
- support_titles: Princess Louise of Denmark (1750–1831), Princess Louise of Denmark (1750–1831), Frederick VI of Denmark, Frederick VI of Denmark
- minimal_support:
  - [Princess Louise of Denmark (1750–1831)#0] Princess Louise of Denmark and Norway (Danish: "Louise af Danmark" ; Norwegian: "Louise av Danmark" ) (20 January 1750 – 12 January 1831) was born to Frederick V of Denmark and Louise of Great Britain.
  - [Princess Louise of Denmark (1750–1831)#1] Her eldest daughter, Marie of Hesse-Kassel, was the wife of Frederick VI of Denmark.
  - [Frederick VI of Denmark#0] 
  - [Frederick VI of Denmark#2] 

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
- explicitly normalize kinship operators for in-law questions
- for `sibling-in-law`, specify this candidate ordering:
  1. spouse's sibling
  2. sibling's spouse
- if a spouse is explicitly named in context, check the spouse branch before refusal
- explicitly warn: do not switch to parent / grandparent / spouse-of-parent branches unless the question asks for them

## Boundary / Failure Risk
- 2 to 3 bullets only
- keep this section shorter than the heuristic

Important distinction:
- this artifact must remain more abstract than episodic_trace
- but it must be operational enough to preserve the correct kinship operator interpretation
- avoid long meta-level genealogy discussion

