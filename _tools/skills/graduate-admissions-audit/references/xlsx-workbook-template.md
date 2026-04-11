# XLSX Workbook Template

Use this workbook structure when the user wants a delivery-ready spreadsheet.

Template asset:

- `assets/graduate-admissions-template.xlsx`

Sample asset:

- `assets/graduate-admissions-sample.xlsx`

If either asset is missing or needs regeneration, run:

```bash
python3 _tools/skills/graduate-admissions-audit/scripts/generate_workbooks.py
```

## Workbook Design Principles

- One workbook per `assessment_run_id`
- One row per `program + intake + study mode` in `program_facts`
- One row per community post or case in `community_cases`
- One row per assessed program in `assessment`
- One row per unresolved blocker in `review_queue`
- Keep URLs as plain text so Excel can auto-link them
- Do not merge cells
- Freeze the first row on every sheet
- Use `unknown` instead of blank when the field was checked but not found

## Sheet Order

1. `README`
2. `applicant_snapshot`
3. `program_facts`
4. `community_cases`
5. `assessment`
6. `review_queue`
7. `source_registry`

## 1. README

Purpose:

- explain workbook grain
- record delivery conventions
- remind the reviewer that official facts and community evidence are separated

Columns:

- `section`
- `content`

## 2. applicant_snapshot

Purpose:

- preserve the exact applicant version used for this assessment

Recommended columns in order:

- `assessment_run_id`
- `applicant_profile_version`
- `target_intake`
- `target_countries`
- `target_directions`
- `identity_status`
- `highest_degree`
- `current_or_last_institution`
- `institution_country`
- `major`
- `minor_or_second_major`
- `gpa_value`
- `gpa_scale`
- `average_score`
- `grading_formula_status`
- `language_tests`
- `internship_summary`
- `research_summary`
- `work_experience_summary`
- `portfolio_status`
- `budget_range`
- `missing_critical_info`
- `snapshot_notes`

## 3. program_facts

Purpose:

- store official fact collection only

Recommended columns in order:

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
- `teaching_language`
- `teaching_language_basis`
- `language_requirement_summary`
- `ielts_requirement`
- `ielts_subscore_requirement`
- `toefl_requirement`
- `toefl_subscore_requirement`
- `other_language_requirement`
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
- `interview_requirement`
- `supervisor_requirement`
- `other_hard_requirements`
- `application_open_date`
- `application_deadline`
- `deadline_type`
- `tuition_local_or_domestic`
- `tuition_non_local_or_international`
- `tuition_currency`
- `tuition_basis_year`
- `tuition_notes`
- `admission_source_id`
- `tuition_source_id`
- `deadline_source_id`
- `captured_at`
- `fact_quality_status`
- `fact_notes`

`fact_quality_status` recommended labels:

- `complete`
- `partial`
- `inferred`
- `stale`
- `conflicting`
- `js_not_captured`

## 4. community_cases

Purpose:

- store offer, reject, waitlist, or interview evidence separately from official facts

Recommended columns in order:

- `evidence_id`
- `program_id`
- `source_id`
- `source_type`
- `source_url`
- `page_title`
- `post_date`
- `intake_if_known`
- `result_type`
- `applicant_background_summary`
- `gpa_or_average_if_stated`
- `language_score_if_stated`
- `soft_background_if_stated`
- `credibility_score`
- `similarity_score`
- `evidence_notes`

## 5. assessment

Purpose:

- store judgement output, not raw facts

Recommended columns in order:

- `program_id`
- `university_name`
- `program_name_en`
- `intake_term`
- `eligibility_status`
- `competitiveness_band`
- `estimated_probability_range`
- `assessment_confidence`
- `evidence_sufficiency`
- `direction_fit`
- `budget_fit`
- `key_risks`
- `manual_review_required`
- `action_recommendation`
- `judgement_reason`
- `supporting_fact_refs`
- `supporting_case_refs`
- `assessor_notes`

## 6. review_queue

Purpose:

- show what still needs a human decision

Recommended columns in order:

- `issue_id`
- `program_id`
- `issue_type`
- `severity`
- `blocking`
- `description`
- `required_human_action`
- `owner`
- `status`

## 7. source_registry

Purpose:

- create a reusable source ledger so every ID in the workbook can be traced back

Recommended columns in order:

- `source_id`
- `program_id`
- `source_category`
- `source_tier`
- `page_title`
- `source_url`
- `captured_at`
- `applicable_intake`
- `freshness_status`
- `notes`

`source_tier` recommended labels:

- `program_official`
- `university_official`
- `official_pdf`
- `community`

## Cell Conventions

- Multi-value fields: separate with `; `
- Date format: `YYYY-MM-DD`
- Boolean-style fields: `yes` / `no`
- Missing but checked: `unknown`
- Not applicable: `n/a`
- Keep Chinese and English mixed only when needed for fidelity
- Do not put final reasoning into `program_facts`

## Delivery Rules

- `program_facts` and `assessment` must never be collapsed into one sheet
- If `estimated_probability_range` is omitted, keep `competitiveness_band` and `assessment_confidence`
- If a field is inferred, the basis must appear in either `teaching_language_basis`, `fact_notes`, or `judgement_reason`
- Every row in `assessment` should reference at least one official source via `supporting_fact_refs`
