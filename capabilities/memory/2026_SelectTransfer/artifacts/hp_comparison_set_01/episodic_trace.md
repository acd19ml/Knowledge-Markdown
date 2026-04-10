# Episodic Trace

## Source Set
- source_set_id: hp_comparison_set_01
- cluster: comparison

## Episode Summaries
### 1. hp_dev_0478
- question: What is the shared country of ancestry between Art Laboe and Scout Tufankjian?
- answer: Armenian
- key lookup path: Art Laboe (born Arthur Egnoian) -> Armenian American; Scout Tufankjian -> Armenian-American
- minimal support: Both individuals are explicitly identified with "Armenian" or "Armenian-American" descriptors in their biographical introductions.
- reusable cue: When comparing ancestry, look for explicit ethnic adjectives attached to the subject's name or birth description.

### 2. hp_dev_4705
- question: Of these two publication--Báiki and Sick--what type of publication is the one that was published most frequently?
- answer: satirical-humor magazine
- key lookup path: Identify publication types for both; determine frequency metric (implied by answer derivation); select type associated with higher frequency.
- minimal support: The solution requires distinguishing the specific genre of the more frequent publication between the two entities.
- reusable cue: In multi-step comparison queries, the final attribute (type) is often dependent on resolving an intermediate metric (frequency) first.

### 3. hp_dev_5052
- question: Who was born first, Ana Kasparian or Andre Agassi?
- answer: Andre Kirk Agassi
- key lookup path: Retrieve birth dates for Ana Kasparian and Andre Agassi; compare chronological order.
- minimal support: Direct comparison of birth dates reveals Andre Agassi's birth date precedes Ana Kasparian's.
- reusable cue: Temporal comparisons ("born first") require extracting specific dates for all entities before performing a linear sort.

### 4. hp_dev_2574
- question: Which airport served more people in 2015 Asheville Regional Airport or Orlando International Airport ?
- answer: Orlando International Airport
- key lookup path: Search for 2015 passenger data; note that Asheville data is explicitly 2016 (826,648), requiring inference or external knowledge for 2015 vs direct retrieval for Orlando.
- minimal support: The provided text gives a 2016 record for Asheville, but the answer identifies Orlando as the 2015 leader, implying a data gap in the snippet or a known fact outside the specific sentence provided.
- reusable cue: When a specific year is queried but the text provides adjacent year data (e.g., 2016 for a 2015 query), verify if the trend supports the answer or if the answer relies on the other entity's unmentioned data.

### 5. hp_dev_0989
- question: Which film is newer, The Apple Dumpling Gang or Heavyweights?
- answer: Heavyweights
- key lookup path: Extract release year for The Apple Dumpling Gang (1975); compare with Heavyweights release year.
- minimal support: The Apple Dumpling Gang is explicitly dated 1975; Heavyweights is the newer film, implying a release date later than 1975.
- reusable cue: For "newer/older" queries, extract the explicit year from the text for one entity and compare against the known or retrieved year of the other.

## Local Pattern Notes
- Comparison tasks frequently require extracting a specific attribute (ancestry, date, frequency) from short biographical or descriptive sentences.
- Temporal comparisons often hinge on finding explicit year markers (e.g., "1975") within the supporting text.
- Some queries involve a slight mismatch between the query year and the provided text year (e.g., 2015 query vs. 2016 text), requiring careful handling of data boundaries.
- The "key lookup path" often involves a direct string match of the entity name followed by the extraction of the target attribute.
- Answers are typically single entities or specific categories derived directly from the explicit descriptors in the source sentences.
