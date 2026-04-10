# r1_episodic_trace_wiki_dev_0123_irrelevant

- target_task_id: wiki_dev_0123
- split: irrelevant
- condition: episodic_trace
- source_set_id: hp_bridge_set_01
- gold_answer: Leave It To Henry
- pred_answer: Leave It To Henry
- em: 1
- f1: 1.0
- token_usage: 2731
- prompt_chars: 10643
- failure_status: ok

---

## Prompt

```
You are a question-answering agent. Your task is to answer a multi-hop reasoning question using the provided context paragraphs.



## Context

### The Last Night (1936 film)
The Last Night is a 1936 Soviet drama film directed by Yuli Raizman.

### Leave It to Me (1955 film)
Leave It to Me  is a 1955 Czech comedy film directed by Martin Frič.

### The Last Night of the Barbary Coast
The Last Night of the Barbary Coast( 1913) was an early example of the exploitation film, showing what was purported to be the last night of the Barbary Coast red-light section of San Francisco. In reality, the Barbary Coast was n't shut down until 1917. The film, directed by Hal Mohr and Sol Lesser, is now considered a lost film. Mohr, later an Academy Award winner, did the cinematography, and Lesser went on to become a Hollywood producer.

### Leave It to Henry
Leave It to Henry is a 1949 American comedy film directed by Jean Yarbrough and written by D.D. Beauchamp. The film stars Raymond Walburn, Walter Catlett, Gary Gray, Mary Stuart, Barbara Brown and Houseley Stevenson. The film was released on June 12, 1949, by Monogram Pictures.

### Takhir Sabirov
Takhir Sabirov( December 21, 1929 – May 30, 2002) is a Tajik film director, actor, screenwriter, art director, and one of the most notable figures of the Tajik cinema. He is known as the" founding father" of the" One Thousand and One Nights" dynasty of the film industry due to his creation of the' Scheherazade' trilogy. He is also known by his formal name Takhir Mukhtorovich Sabirov. His mother" Mastona Sobir Zoda" was the daughter of Duke" Sobir- kaloni Tura-zoda" of Samarkand( now part of the Samarqand Province, Uzbekistan), from the Duchy of Greater Khorasan, known as" Tura- zoda", who were eminent members of Central Asia's Aristocracy. Takhir was the youngest of five children. He was married twice and has two sons and three daughters. He completed the Performing Arts discipline at the Tashkent State Art Institute of Theatrical Arts in Tashkent, Uzbekistan. In 1951, he then continued further by obtaining his Directorial discipline under faculty of Yuri Zavadsky at The Russian Academy of Theatre Arts( GITIS) in Moscow, Russia. His first film," Roh"( 1955) ( Russian title:" Дорога") produced by Mosfilm initiated him into the film industry, but the role of" Yodgor" in" Dokhunda"( 1956) sparked his career and was followed by several successful roles. His directorial debut was in" Vaqti zangirii pisar rasid"( Russian title:" Sinu para jinitsa", 1959), which was the first comedy musical motion picture in the Cinema of Tajikistan. With his films he introduced the Tajik film industry onto international scenebasis with his nomination in International film festivals. His film" Margi Sudkhur"( Russian title:" Smert' Rostovshika", 1966) was nominated at the International Film Festival of Asia and Africa in 1968. His trilogy of" New Tales of ScheherazadeAnother Night of Scheherazade" and" The Last Night of Scheherazade" that were based on the Arabic folktale" One Thousand and One Nights" had made a great impact in the Cinema of Tajikistan by opening it to European audiences and borders. The Scheherazade trilogies were among one of the first Tajik film productions that achieved distribution beyond Russian( former USSR) borders, placing Tajik film on the map of International Film Festivals. Not only has he directed and co-written the Scheherazade trilogies, but also starred as King Shahryar( Sultan); which coincidentally is more true to his own lineage of royalty. He became a cultural icon gaining more acknowledgement and respect. Regardless of the obstacles he had faced in his lifetime, he never stopped filming. He is known in the Tajik film industry as one of the major film directors of his time. He broadened his entertainment field as he established entrepreneurial joint venture" Movarounnahr Joint Venture" as an Art Director. Although he was involved in many fields of the film industry, he always had time to instruct and inspire students and apprentices. In 1999, he was part of the judging committee in the 21st( XXI) Moscow International Film Festival. He became the first Tajik film director to be honored with the position of a film judge. In 2002, he was an honorary guest at the 55th( LV) Cannes Film Festival. Even in his seventy years of age he was involved in film production. However, on May 30, 2002 he died with his film" Khoja Kamoli Khujandi" still in production. In 2003, a street," Takhir Sabirov Street" was named after his death for his contributions in the Cinema of Tajikistan( Tajikfilm, Tajik Film Studio).

### Leave It to Me (1933 film)
Leave It to Me is a 1933 British comedy film directed by Monty Banks and starring Gene Gerrard, Olive Borden and Molly Lamont. It was made at Elstree Studios. The film's sets were designed by the art director David Rawnsley. It is an adaptation of the play" Leave It to Psmith"( 1930) by Ian Hay and P.G. Wodehouse, which is based on Wodehouse's novel" Leave It to Psmith"( 1923).

### Frank Bank
Frank Bank( April 12, 1942 – April 13, 2013) was an American actor, particularly known for his role as Clarence" Lumpy" Rutherford on the 1957 – 1963 situation comedy television series" Leave It to Beaver". Bank was cast in fifty episodes of" Leave It to Beaver" between January 24, 1958, until the series finale on May 30, 1963. Thereafter, he was cast as Clarence Rutherford in 101 episodes of the series sequel," The New Leave It to Beaver", which aired on cable television from 1985 to 1989. Beginning in 1973, Bank became a bond broker in his native Los Angeles. His autobiography," Call Me Lumpy: My Leave It To Beaver Days and Other Wild Hollywood Life," was published in 1997. Bank died of cancer on April 13, 2013, in Rancho Mirage, California, one day after his 71st birthday. He was survived by his third wife, Rebecca, four daughters, and five grandchildren. He is interred at Hillside Memorial Park Cemetery in Culver City, California.

### Henry Moore (cricketer)
Henry Walter Moore( 1849 – 20 August 1916) was an English- born first- class cricketer who spent most of his life in New Zealand.

### Jean Yarbrough
Jean Yarbrough (August 22, 1901 – August 2, 1975) was an American film director.

### The Last Night of Scheherazade
The Last Night of Scheherazade is a 1987 Soviet- Syrian children's fantasy film directed by Takhir Sabirov based on" One Thousand and One Nights". It is the last film of the trilogy, started with the films" New Tales of Scheherazade" and" And another night of Scheherazade". The heroes of the film are the shoemaker Maruf and the daughter of the Caliph, Esmagül, who despite falling in love with a young man, nevertheless forces him to fight for his own happiness.



## Question

Which film has the director born first, Leave It To Henry or The Last Night Of Scheherazade?



## Past Experience

The following notes summarize patterns from previously solved tasks that may or may not be relevant to the current question. Use them only if they help your reasoning — do not force-apply them.

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



## Instructions

- Read all context paragraphs carefully.
- Identify the reasoning chain needed to answer the question.
- Provide your final answer as a short phrase (not a full sentence).
- If the question asks "which", "who", or "what", respond with the specific entity name.
- If the question asks for a comparison, respond with the entity that satisfies the comparison.



## Answer
```

## Raw Model Output

```
Leave It To Henry
```
