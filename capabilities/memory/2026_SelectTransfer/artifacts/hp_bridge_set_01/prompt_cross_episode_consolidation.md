Write `cross_episode_consolidation.md` for the following frozen source set.

Source Set ID: hp_bridge_set_01
Cluster: bridge
Source Set Note: clean Hotpot bridge set for Round 1 draft

Input episodes:
- Task ID: hp_dev_2054
  - Question: When did the park at which Tivolis Koncertsal is located open?
  - Answer: 15 August 1843
  - Reasoning Label: bridge
  - Raw Type: bridge
  - Difficulty: hard
  - Taxonomy Note: bridge via venue to park opening
  - Supporting Titles: Tivolis Koncertsal, Tivoli Gardens
  - Supporting Sentences:
    - [Tivolis Koncertsal / sent 0] Tivolis Koncertsal is a 1,660-capacity concert hall located at Tivoli Gardens in Copenhagen, Denmark.

- Task ID: hp_dev_3245
  - Question: The school in which the Wilmslow Show is held is designated as what?
  - Answer: Centre of Excellence
  - Reasoning Label: bridge
  - Raw Type: bridge
  - Difficulty: hard
  - Taxonomy Note: bridge via event venue to school
  - Supporting Titles: Wilmslow Show, Wilmslow High School
  - Supporting Sentences:
    - [Wilmslow Show / sent 0] Wilmslow Show is held at Wilmslow High School, Wilmslow, Cheshire, England, as a one-day event on a Sunday – usually the second Sunday in July.
    - [Wilmslow High School / sent 0] Wilmslow High School is a mixed-sex 11–18 comprehensive secondary school in Wilmslow, Cheshire, and a designated Centre of Excellence.

- Task ID: hp_dev_1119
  - Question: Who will Billy Howle be seen opposite in the upcoming British drama film directed by Dominic Cooke?
  - Answer: Saoirse Ronan
  - Reasoning Label: bridge
  - Raw Type: bridge
  - Difficulty: hard
  - Taxonomy Note: bridge via film to co-star
  - Supporting Titles: Billy Howle, On Chesil Beach (film)
  - Supporting Sentences:
    - [Billy Howle / sent 3] Howle will next be seen opposite Saoirse Ronan in the drama, "On Chesil Beach", in the adaptation of Anton Chekhov's iconic play, "The Seagull", and in Netflix film "Outlaw King".
    - [On Chesil Beach (film) / sent 0] On Chesil Beach is an upcoming British drama film directed by Dominic Cooke in his motion picture directorial debut.

- Task ID: hp_dev_1668
  - Question: Tommy's Honour was a drama film that included the actor who found success with what 2016 BBC miniseries?
  - Answer: War & Peace
  - Reasoning Label: bridge
  - Raw Type: bridge
  - Difficulty: hard
  - Taxonomy Note: bridge via cast actor to series
  - Supporting Titles: Tommy's Honour, Jack Lowden, Jack Lowden
  - Supporting Sentences:
    - [Jack Lowden / sent 0] Jack Andrew Lowden (born 2 June 1990) is a Scottish stage, television, and film actor.
    - [Jack Lowden / sent 1] Following a highly successful and award-winning four-year stage career, his first major international onscreen success was in the 2016 BBC miniseries "War & Peace", which led to starring roles in feature films.

- Task ID: hp_dev_4237
  - Question: "Tunak", is a bhangra/pop love song by an artist born in which year ?
  - Answer: 1967
  - Reasoning Label: bridge
  - Raw Type: bridge
  - Difficulty: hard
  - Taxonomy Note: bridge via song performer to birth year
  - Supporting Titles: Tunak Tunak Tun, Daler Mehndi
  - Supporting Sentences:
    - [Tunak Tunak Tun / sent 0] "Tunak Tunak Tun" (Punjabi: ਤੁਣਕ ਤੁਣਕ ਤੁਣ ) or simply "Tunak", is a bhangra/pop love song by Indian artist Daler Mehndi released in 1998.

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
