# r1_cross_episode_consolidation_wiki_dev_0123_irrelevant

- target_task_id: wiki_dev_0123
- split: irrelevant
- condition: cross_episode_consolidation
- source_set_id: hp_bridge_set_01
- gold_answer: Leave It To Henry
- pred_answer: Leave It To Henry
- em: 1
- f1: 1.0
- token_usage: 2601
- prompt_chars: 10582
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

# Cross-Episode Consolidation

## Source Set
- source_set_id: hp_bridge_set_01
- cluster: bridge

## Shared Structure
- **Multi-Hop Entity Chaining**: All tasks require traversing a chain of at least two distinct entities (e.g., Event → Venue, Song → Artist, Film → Actor) to reach the final answer.
- **Explicit Linking via Titles**: The reasoning path is anchored by specific entity titles (e.g., "Tivolis Koncertsal", "Wilmslow Show") that serve as the bridge nodes connecting the query context to the knowledge base.
- **Attribute Extraction from Secondary Context**: The target attribute (e.g., opening date, designation, birth year) is rarely found in the sentence describing the primary query entity; it resides in the supporting sentence of the linked entity.
- **High Difficulty via Indirection**: The "hard" difficulty rating correlates directly with the necessity of resolving the intermediate entity before the final fact can be retrieved.

## Applicability
- **Use when**: The question explicitly asks for a property of an entity that is not directly mentioned in the query, requiring the model to identify a related entity first (e.g., "Where is X located?" where X is an event, not a place).
- **Use when**: The supporting evidence contains a list of works or roles for an entity, and the query targets a specific item within that list to derive a new fact.
- **Avoid when**: The answer is contained within a single sentence describing the queried entity without requiring a jump to a different entity's profile.
- **Avoid when**: The relationship between entities is implicit or requires external world knowledge not present in the provided supporting sentences (e.g., knowing that a specific school is a venue without it being stated).

## Operational Heuristic
1. **Identify the Gap**: Determine if the requested attribute (date, name, role) is absent from the sentence describing the main subject of the question.
2. **Locate the Bridge Entity**: Scan supporting titles and sentences for an entity explicitly linked to the main subject (e.g., "held at", "directed by", "by").
3. **Retrieve Linked Context**: Extract the full profile or relevant sentences for this bridge entity.
4. **Extract Final Attribute**: Search the bridge entity's context for the specific attribute requested in the original question.

## Boundary / Failure Risk
- **Ambiguous Links**: Failure occurs if the supporting text mentions a relationship (e.g., "actor in a film") but does not explicitly name the specific film or attribute needed to proceed to the next hop.
- **Title Mismatch**: Errors arise if the model conflates similarly named entities (e.g., different films or venues) when the bridge relies on a specific title match.
- **Missing Intermediate Step**: The model may attempt to answer directly from the first sentence, failing to recognize that the answer requires data from a secondary entity's description.
- **Over-Reliance on Titles**: If the bridge entity is not listed in the "Supporting Titles" but is only mentioned in passing within a sentence, the standard retrieval path may fail.



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
