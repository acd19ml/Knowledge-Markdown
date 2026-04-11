# Standard Output Sample

Use this file as a style guide for delivery phrasing. The values below are illustrative examples only, not real admissions facts.

Related asset:

- `assets/graduate-admissions-sample.xlsx`

## Sheet-Level Sample

### applicant_snapshot

| assessment_run_id | applicant_profile_version | target_intake | target_countries | target_directions | identity_status | highest_degree | current_or_last_institution | major | gpa_value | language_tests | budget_range | missing_critical_info |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RUN-EXAMPLE-001 | AP-V1 | 2027 Fall | Hong Kong; United Kingdom | Cultural Heritage; Museum Studies | HK local | Bachelor's | Example Metropolitan University | Cultural Industries Management | unknown | IELTS 6.5 overall, no subscore below 6.0 | HKD 250000 tuition cap | GPA conversion formula; final average |

### program_facts

| program_id | university_name | program_name_en | teaching_language | teaching_language_basis | ielts_requirement | academic_requirement_summary | tuition_local_or_domestic | tuition_non_local_or_international | application_deadline | fact_quality_status |
|---|---|---|---|---|---|---|---|---|---|---|
| HK-EXU-MUS-2027FT | Example University Hong Kong | MA Museum and Heritage Practice | Chinese | inferred from official page requiring Chinese proficiency and not listing IELTS | unknown | Bachelor's degree in relevant or related discipline | HKD 138000 | HKD 172000 | 2027-03-15 | inferred |
| UK-EXU-HER-2027FT | Example University UK | MA Heritage Policy and Practice | English | explicit on official admission page | IELTS 6.5 overall | 2:1 equivalent in relevant subject area | not separated | GBP 24900 | rolling | complete |

### community_cases

| evidence_id | program_id | result_type | applicant_background_summary | gpa_or_average_if_stated | language_score_if_stated | credibility_score | similarity_score | evidence_notes |
|---|---|---|---|---|---|---|---|---|
| CASE-001 | HK-EXU-MUS-2027FT | offer | HK local, humanities major, museum internship | 83/100 | IELTS not stated | 0.68 | 0.72 | detailed timeline post, no screenshot |
| CASE-002 | UK-EXU-HER-2027FT | reject | Mainland applicant, arts management major | 78/100 | IELTS 6.5 | 0.74 | 0.51 | included decision email date |

### assessment

| program_id | eligibility_status | competitiveness_band | estimated_probability_range | assessment_confidence | evidence_sufficiency | direction_fit | budget_fit | manual_review_required | action_recommendation |
|---|---|---|---|---|---|---|---|---|---|
| HK-EXU-MUS-2027FT | likely_eligible | 主申 | 60-80% | medium | moderate | high | within_budget | yes | manual_review_before_decision |
| UK-EXU-HER-2027FT | eligible | 主申偏冲刺 | 40-55% | medium | moderate | medium_high | stretch | yes | manual_review_before_decision |

### review_queue

| issue_id | program_id | issue_type | severity | blocking | description | required_human_action | status |
|---|---|---|---|---|---|---|---|
| ISSUE-001 | HK-EXU-MUS-2027FT | language-rule-interpretation | medium | no | Teaching language is inferred from Chinese proficiency wording and should be confirmed manually if English waiver matters. | Re-open the official page or contact admissions for clarification. | open |
| ISSUE-002 | UK-EXU-HER-2027FT | gpa-conversion | high | yes | Applicant GPA conversion formula is unknown, so competitiveness cannot be upgraded confidently. | Confirm the applicant's official undergraduate grading policy. | open |

## Standard Phrasing

Use this style for `judgement_reason`:

### Good

- Meets the published degree baseline and the visible language threshold, but competitiveness remains medium-confidence because the applicant's GPA conversion method is not yet confirmed.
- Official tuition is available, but local and non-local fees differ materially, so identity status must remain explicit in the recommendation.
- The program appears Chinese-medium based on the admission page wording. Because this is an inference rather than an explicit statement, manual confirmation is still recommended.

### Avoid

- High chance, should be fine.
- Probably English-taught.
- Similar backgrounds got in, so this one is safe.

## Recommended Delivery Summary

When summarizing the workbook to a client or colleague, use this structure:

1. `事实层`
   Example: Official requirements, tuition, deadline, and special conditions have been separated from anecdotal evidence.

2. `判断层`
   Example: Programs are labeled by eligibility, competitiveness band, confidence, and direction fit.

3. `待确认层`
   Example: Any inferred language rules, GPA conversion risks, stale tuition, or prerequisite gaps are listed in `review_queue`.
