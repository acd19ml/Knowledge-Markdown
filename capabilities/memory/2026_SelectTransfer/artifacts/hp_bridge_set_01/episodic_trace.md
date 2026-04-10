# Episodic Trace

## Source Set
- source_set_id: hp_bridge_set_01
- cluster: bridge

## Episode Summaries
### 1. hp_dev_2054
- question: When did the park at which Tivolis Koncertsal is located open?
- answer: 15 August 1843
- key lookup path: Tivolis Koncertsal -> location (Tivoli Gardens) -> park opening date
- minimal support: Tivolis Koncertsal is a concert hall located at Tivoli Gardens in Copenhagen, Denmark.
- reusable cue: Identify the specific venue's parent park or garden entity to retrieve the establishment date.

### 2. hp_dev_3245
- question: The school in which the Wilmslow Show is held is designated as what?
- answer: Centre of Excellence
- key lookup path: Wilmslow Show -> venue (Wilmslow High School) -> school designation
- minimal support: Wilmslow Show is held at Wilmslow High School; Wilmslow High School is a designated Centre of Excellence.
- reusable cue: Trace the event to its host institution to find specific designations or awards associated with that institution.

### 3. hp_dev_1119
- question: Who will Billy Howle be seen opposite in the upcoming British drama film directed by Dominic Cooke?
- answer: Saoirse Ronan
- key lookup path: Billy Howle -> co-star in film -> verify film director (Dominic Cooke)
- minimal support: Howle will next be seen opposite Saoirse Ronan in "On Chesil Beach", directed by Dominic Cooke.
- reusable cue: Use the actor's co-star list to find the specific film, then cross-reference the director to confirm the match.

### 4. hp_dev_1668
- question: Tommy's Honour was a drama film that included the actor who found success with what 2016 BBC miniseries?
- answer: War & Peace
- key lookup path: Tommy's Honour -> cast member (Jack Lowden) -> actor's 2016 BBC miniseries
- minimal support: Jack Lowden starred in the 2016 BBC miniseries "War & Peace" following his stage career.
- reusable cue: Identify the actor in the source film and retrieve their notable television work from the specified year.

### 5. hp_dev_4237
- question: "Tunak", is a bhangra/pop love song by an artist born in which year ?
- answer: 1967
- key lookup path: "Tunak" -> artist (Daler Mehndi) -> artist birth year
- minimal support: "Tunak" is a song by Indian artist Daler Mehndi.
- reusable cue: Extract the performer's name from the song description and look up their biographical birth year.

## Local Pattern Notes
- Bridge queries consistently require a two-step entity resolution: first identifying the intermediate entity (venue, school, film, actor, or singer), then retrieving the target attribute from that intermediate entity.
- Supporting sentences often contain the direct link between the query entity and the bridge entity within the same sentence or adjacent sentences.
- Verification steps are critical in film/actor bridges to ensure the correct co-star or director is matched before retrieving the final answer.
- Event-based bridges (shows, songs) rely heavily on the "held at" or "by" relationship to pivot to the institutional or biographical data.
- All episodes in this set share a "hard" difficulty rating due to the necessity of chaining distinct facts rather than direct retrieval.
