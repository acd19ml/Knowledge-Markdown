Write `cross_episode_consolidation.md` for the following frozen source set.

Source Set ID: hp_comparison_set_01
Cluster: comparison
Source Set Note: clean Hotpot comparison set for Round 1 draft after expansion batch 1

Input episodes:
- Task ID: hp_dev_0478
  - Question: What is the shared country of ancestry between Art Laboe and Scout Tufankjian?
  - Answer: Armenian
  - Reasoning Label: comparison
  - Raw Type: comparison
  - Difficulty: hard
  - Taxonomy Note: comparison of ancestry attribute
  - Supporting Titles: Art Laboe, Scout Tufankjian
  - Supporting Sentences:
    - [Art Laboe / sent 0] Art Laboe (born Arthur Egnoian on August 7, 1925) is an Armenian American disc jockey, songwriter, record producer, and radio station owner, generally credited with coining the term "Oldies But Goodies".
    - [Scout Tufankjian / sent 0] Scout Tufankjian is an Armenian-American photojournalist and author based in Brooklyn, New York.

- Task ID: hp_dev_4705
  - Question: Of these two publication--Báiki and Sick--what type of publication is the one that was published most frequently?
  - Answer: satirical-humor magazine
  - Reasoning Label: comparison
  - Raw Type: comparison
  - Difficulty: hard
  - Taxonomy Note: comparison of publication frequency then type
  - Supporting Titles: Báiki, Sick (magazine)

- Task ID: hp_dev_5052
  - Question: Who was born first, Ana Kasparian or Andre Agassi?
  - Answer: Andre Kirk Agassi
  - Reasoning Label: comparison
  - Raw Type: comparison
  - Difficulty: hard
  - Taxonomy Note: comparison of birth dates
  - Supporting Titles: Ana Kasparian, Andre Agassi

- Task ID: hp_dev_2574
  - Question: Which airport served more people in 2015 Asheville Regional Airport or Orlando International Airport ?
  - Answer: Orlando International Airport
  - Reasoning Label: comparison
  - Raw Type: comparison
  - Difficulty: hard
  - Taxonomy Note: comparison of passenger traffic
  - Supporting Titles: Asheville Regional Airport, Orlando International Airport, Orlando International Airport
  - Supporting Sentences:
    - [Asheville Regional Airport / sent 3] In 2016 it served an all-time record number of passengers for the airport, 826,648, an increase of 5% over 2015 and the third consecutive year of record traffic.

- Task ID: hp_dev_0989
  - Question: Which film is newer, The Apple Dumpling Gang or Heavyweights?
  - Answer: Heavyweights
  - Reasoning Label: comparison
  - Raw Type: comparison
  - Difficulty: hard
  - Taxonomy Note: comparison of film release dates
  - Supporting Titles: The Apple Dumpling Gang (film), Heavyweights
  - Supporting Sentences:
    - [The Apple Dumpling Gang (film) / sent 0] The Apple Dumpling Gang is a 1975 American comedy-western film produced by Walt Disney Productions about a slick gambler named Russell Donovan (Bill Bixby) who is duped into taking care of a group of orphans who eventually strike gold during the California Gold Rush.

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
