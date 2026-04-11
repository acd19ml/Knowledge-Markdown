# Assessment Framework

Use this after official facts and community evidence are collected and normalized.

## 1. Assessment Order

Always assess in this order:

1. `eligibility_status`
2. `competitiveness_band`
3. `direction_fit`
4. `budget_fit`
5. `assessment_confidence`
6. `action_recommendation`

Do not skip straight to probability labels.

## 2. Eligibility Rules

`ineligible`
- clear hard requirement failure
- missing required degree type
- missing mandatory language threshold with no official waiver path
- required prerequisite clearly absent

`likely_ineligible`
- one probable hard failure remains unresolved

`unclear`
- critical data is missing
- official sources conflict
- transcript-level checks cannot be completed

`likely_eligible`
- no visible hard failure, but one or more items still need manual confirmation

`eligible`
- official evidence supports that the applicant meets the stated baseline requirements

## 3. Competitiveness Band

Use the user's preferred five-band structure:

- `稳保`
- `主申偏保底`
- `主申`
- `主申偏冲刺`
- `冲刺`

Judge competitiveness from these dimensions:

- language gap
- GPA and school-background fit
- background and prerequisite fit
- competition intensity
- extra hard requirements

Important:

- This is a heuristic band, not a statistical guarantee.
- If eligibility is `unclear` or worse, competitiveness should not be presented as high confidence.

## 4. Direction Fit

Assess direction fit separately from competitiveness:

- `high`
- `medium_high`
- `medium`
- `low`

Consider:

- academic background match
- curriculum match
- career-outcome match
- narrative or application-story fit

## 5. Budget Fit

Recommended labels:

- `within_budget`
- `stretch`
- `out_of_budget`
- `unknown`

If tuition is stale or incomplete, lower confidence even if the visible number looks affordable.

## 6. Assessment Confidence

Use:

- `high`
- `medium`
- `low`

Lower confidence when any of these apply:

- missing applicant facts that affect hard requirements
- stale or conflicting official sources
- teaching language is inferred rather than explicit
- community evidence sample is small
- only offer cases exist and no adverse cases were found
- judgment depends on transcript-level prerequisites

## 7. Evidence Sufficiency

Use:

- `strong`
- `moderate`
- `weak`

Recommended guide:

- `strong`: official facts are complete on all critical fields and community evidence includes multiple recent, non-duplicative cases
- `moderate`: official facts are usable but one or two critical items still depend on inference or limited cases
- `weak`: critical fields are missing, conflicting, stale, or supported mostly by anecdotal evidence

If evidence sufficiency is `weak`, avoid a numeric-looking probability range.

## 8. Community Evidence Scoring

For each case, estimate:

- `credibility_score`
  Higher when the post includes dates, scores, detailed background, or screenshots
- `similarity_score`
  Higher when the case resembles the applicant in school tier, GPA, major, language, identity status, and target program

Also record:

- recency
- result type
- whether the post reads like an ad

Community evidence can shift a band slightly, but it should not override a clear official hard rule.

## 9. Optional Probability Range

Use a probability-style range only when it helps the user and evidence sufficiency is at least `moderate`.

Suggested mapping:

- `稳保`: `95%+`
- `主申偏保底`: `80-90%`
- `主申`: `60-80%`
- `主申偏冲刺`: `40-55%`
- `冲刺`: `20-40%`

Important:

- This range is an explanatory shorthand, not a statistical truth.
- When confidence is low or evidence is weak, omit the range rather than pretending precision.

## 10. Manual Review Triggers

Mark `manual_review_required = yes` when any of these are true:

- official pages conflict on a critical field
- JS-rendered page prevents capture of a critical field
- teaching language is only inferred and matters to the recommendation
- UK institution list is not confirmed
- Canada prerequisites need transcript review
- supervisor expectations are unclear
- tuition year is stale
- deadline structure is incomplete
- community evidence is too sparse or too one-sided

## 11. Action Recommendation

Use one of:

- `apply_now`
- `apply_after_language`
- `apply_after_prerequisite_check`
- `apply_as_reach_only`
- `not_recommended_now`
- `manual_review_before_decision`

## 12. Reasoning Format

Every final judgement should be explainable in 2 parts:

1. concise judgement summary
2. evidence-backed reasons

Example:

- `eligibility_status`: `likely_eligible`
- `competitiveness_band`: `主申偏冲刺`
- `assessment_confidence`: `medium`
- `evidence_sufficiency`: `moderate`
- `judgement_reason`: Meets the stated degree and language baseline, but prerequisite coverage is not transcript-verified and recent similar cases are limited.

## 13. Final Safety Rule

When evidence is weak, show the weakness. The framework should degrade to `unclear` or `low confidence` rather than pretending the signal is strong.
