# Cross-Episode Consolidation

## Source Set
- source_set_id: hp_relation_chain_bridge_set_01
- cluster: bridge

## Shared Structure
- Multi-hop kinship chains where the target relation is not directly linked to the initial subject.
- Chains frequently traverse a "spouse bridge" (e.g., Subject -> Spouse -> Spouse's Relative) before reaching the final target.
- Evidence often requires linking two distinct entities (e.g., a nominee and their spouse) to establish the path.
- The reasoning label is consistently "bridge," indicating a gap-filling step between immediate and distant relations.
- Support titles typically include the primary subject, the bridging spouse, and the final target entity.

## Applicability
- **Likely Useful**: When the question asks for a relative of a spouse, a parent of a spouse, or a sibling of a child derived from a specific marriage.
- **Not Applicable**: When the question asks for a direct relative of the subject (e.g., "Who is the brother of X?") without any mention of a spouse or in-law connection.

## Operational Heuristic
1. Identify the initial subject and the first explicit relation mentioned in the question.
2. Check if the target relation requires traversing a **spouse link** (e.g., "wife of," "husband of," "daughter-in-law").
3. **Branch-Sensitive Instruction**: If a spouse branch is present, prioritize retrieving the spouse's profile first to access their kinship network; do not skip this step to find the subject's own siblings.
4. Verify the connection between the spouse and the final target entity using the retrieved context.
5. **Warning**: Do not switch to the subject's own siblings or parents unless the context explicitly supports that specific branch; strictly follow the chain defined by the question's relational operators.

## Boundary / Failure Risk
- Risk of ignoring the explicitly named spouse branch in favor of the subject's direct family tree due to over-emphasis on missing information.
- Failure to distinguish between the subject's direct relatives and the relatives of their spouse when the chain involves an in-law.
- Over-generalizing the chain structure when the specific kinship link (e.g., brother vs. sister) is critical to the answer.
