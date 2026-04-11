# Field Dictionary

Use these canonical fields so that official facts, community evidence, and judgement outputs stay separable.

## 1. Applicant Profile Fields

Required when available:

- `assessment_run_id`
- `applicant_profile_version`
- `target_intake`
- `target_countries`
- `target_directions`
- `identity_status`
  Examples: `HK local`, `HK non-local`, `domestic`, `international`
- `highest_degree`
- `current_or_last_institution`
- `institution_country`
- `major`
- `minor_or_second_major`
- `gpa_value`
- `gpa_scale`
- `average_score`
- `grading_formula_status`
  Examples: `official formula confirmed`, `non-standard formula pending`, `unknown`
- `language_tests`
  Store test type, overall, subscores, test date
- `work_experience_summary`
- `internship_summary`
- `research_summary`
- `portfolio_status`
- `budget_range`
- `missing_critical_info`

## 2. Program Identity Fields

- `program_id`
- `program_country`
- `university_name`
- `faculty_or_school`
- `program_name_en`
- `program_name_zh`
- `degree_award`
- `study_mode`
- `duration`
- `intake_term`
- `project_status`
  Examples: `open`, `not accepting`, `suspended`, `discontinued`

## 3. Official Facts Fields

Store every field with `value`, `raw_snippet`, `source_url`, `captured_at`, `explicit_or_inferred`.

Recommended metadata for each fact object:

- `fact_id`
- `source_id`
- `page_title`
- `applicable_intake`
- `freshness_status`
- `review_required`

- `admission_page_url`
- `tuition_page_url`
- `application_page_url`
- `teaching_language`
- `teaching_language_basis`
- `language_requirement_summary`
- `ielts_requirement`
- `ielts_subscore_requirement`
- `toefl_requirement`
- `toefl_subscore_requirement`
- `other_language_requirement`
  Examples: CET-6, HSK, Chinese proficiency, Cantonese
- `language_waiver_policy`
- `academic_requirement_summary`
- `degree_class_requirement`
- `major_restriction`
- `preferred_background`
- `prerequisite_courses`
- `minimum_core_courses`
- `work_experience_requirement`
- `portfolio_requirement`
- `test_requirement`
  Examples: GMAT, GRE, written test, entrance exam
- `interview_requirement`
- `supervisor_requirement`
- `other_hard_requirements`
- `application_open_date`
- `application_deadline`
- `deadline_type`
  Examples: `rolling`, `rounds`, `fixed deadline`
- `tuition_local_or_domestic`
- `tuition_non_local_or_international`
- `tuition_currency`
- `tuition_basis_year`
- `tuition_notes`
- `living_cost_note`

## 4. Evidence Fields

Keep these outside the official facts table.

- `evidence_id`
- `program_id`
- `source_id`
- `source_type`
  Examples: `forum`, `reddit`, `xiaohongshu`, `university webinar`, `official FAQ`
- `source_url`
- `page_title`
- `post_date`
- `intake_if_known`
- `result_type`
  Examples: `offer`, `reject`, `waitlist`, `interview`, `pending`
- `applicant_background_summary`
- `gpa_or_average_if_stated`
- `language_score_if_stated`
- `soft_background_if_stated`
- `credibility_score`
- `similarity_score`
- `evidence_notes`

## 5. Judgement Fields

- `eligibility_status`
  Recommended labels: `eligible`, `likely_eligible`, `unclear`, `likely_ineligible`, `ineligible`
- `competitiveness_band`
  Recommended labels: `稳保`, `主申偏保底`, `主申`, `主申偏冲刺`, `冲刺`
- `estimated_probability_range`
  Optional. Use only when evidence sufficiency is adequate.
- `assessment_confidence`
  Recommended labels: `high`, `medium`, `low`
- `evidence_sufficiency`
  Recommended labels: `strong`, `moderate`, `weak`
- `direction_fit`
- `budget_fit`
- `key_risks`
- `manual_review_required`
- `action_recommendation`
- `judgement_reason`
- `supporting_fact_refs`
- `supporting_case_refs`
- `ruleset_version`

## 6. Minimum Final Output Columns

If the user wants a compact output, keep at least:

- `university_name`
- `program_name_en`
- `study_mode`
- `intake_term`
- `teaching_language`
- `ielts_requirement`
- `academic_requirement_summary`
- `prerequisite_courses`
- `tuition_local_or_domestic`
- `tuition_non_local_or_international`
- `application_deadline`
- `eligibility_status`
- `competitiveness_band`
- `assessment_confidence`
- `direction_fit`
- `key_risks`
- `admission_page_url`
- `tuition_page_url`
