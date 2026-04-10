# Cross-Episode Consolidation

## Source Set
- source_set_id: hp_comparison_set_01
- cluster: comparison

## Shared Structure
- **Dual-Entity Retrieval**: The core task requires identifying and retrieving specific factual attributes (e.g., ancestry, birth date, passenger count) for exactly two distinct entities named in the query.
- **Attribute Extraction & Normalization**: Success depends on extracting raw values from supporting sentences and normalizing them into a comparable format (e.g., converting years to integers, identifying specific categories like "satirical-humor magazine").
- **Scalar or Categorical Comparison**: The reasoning process invariably involves a direct comparison between the two extracted values to determine a relative ordering (earlier/later, more/less) or a classification based on the magnitude of the attribute.
- **Multi-Hop Dependency**: The entities are rarely defined by a single sentence; the agent must often navigate multiple supporting titles and sentences to locate the specific data point for each entity before performing the comparison.

## Applicability
- **Use when**: The query explicitly asks to rank, order, or differentiate between two specific entities based on a quantifiable metric (time, quantity, frequency) or a specific categorical attribute.
- **Use when**: The problem requires synthesizing information from separate knowledge sources (titles) to form a complete picture of two subjects before making a judgment call.
- **Not useful when**: The query asks for a single entity's attribute without a comparative element, or when the task requires complex logical deduction beyond simple attribute retrieval and comparison.

## Operational Heuristic
1. **Parse Entities**: Isolate the two specific entities mentioned in the question.
2. **Retrieve Attributes**: Locate the specific sentence or section containing the relevant attribute (e.g., birth year, traffic count) for *each* entity individually.
3. **Normalize Data**: Convert the retrieved values into a common unit or category (e.g., ensure both dates are in YYYY format, or both counts are integers).
4. **Execute Comparison**: Apply the relational operator implied by the question (e.g., "born first" = lower year; "more people" = higher count) to determine the winner.
5. **Verify Context**: Ensure the comparison is based on the specific constraints in the question (e.g., "in 2015" vs. general history) before finalizing the answer.

## Boundary / Failure Risk
- **Attribute Ambiguity**: Failure occurs if the retrieved attribute is not the specific one requested (e.g., retrieving total traffic instead of 2015 traffic, or general ancestry instead of specific country of origin).
- **Entity Confusion**: Risk of mixing up attributes between the two entities, especially if they share similar names or if the supporting sentences are dense with multiple dates/numbers.
- **Temporal Scope Errors**: Incorrectly applying a comparison when the question restricts the scope to a specific time window (e.g., comparing 2015 data against a general historical fact).
- **Category Mismatch**: Misclassifying a publication type or other categorical attribute when the question requires a specific sub-category (e.g., distinguishing "magazine" from "satirical-humor magazine").
