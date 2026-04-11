---
name: graduate-admissions-audit
description: Build an auditable graduate admissions shortlist and applicant-fit assessment for master's programs in Hong Kong, the UK, Canada, and Australia. Use this skill whenever the user wants to turn a client profile into a referenced program list, collect official admission requirements and tuition, compare local/non-local or domestic/international fees, infer teaching language from official requirements, gather community offer or reject cases as supporting evidence, or output a structured matrix with eligibility, competitiveness, direction fit, risk flags, and clickable sources. Trigger even when the user only provides partial information and asks for 定位、选校、项目初筛、录取概率评估、方向匹配度分析、案例整理、可追溯来源、院校专业清单、申请要求汇总, or similar admissions research work.
---

# Graduate Admissions Audit

## Purpose

Use this skill to produce a traceable admissions research output rather than a generic school list.
The deliverable must separate:

- **Official facts**: what the university explicitly says
- **Community evidence**: forum or social posts about real applicant outcomes
- **Judgement**: the model's eligibility and competitiveness assessment

This skill is for graduate admissions research and triage. It does not guarantee offers and it must not present inferred or anecdotal content as official fact.

## Scope

This skill is optimized for master's level program discovery and assessment across:

- Hong Kong
- United Kingdom
- Canada
- Australia

It can work with incomplete client profiles, but it must downgrade confidence and flag missing items instead of guessing.

## Read These References

Read these files before producing a final assessment:

- [references/source-policy.md](references/source-policy.md)
- [references/field-dictionary.md](references/field-dictionary.md)
- [references/assessment-framework.md](references/assessment-framework.md)

Also read the relevant country section when the target geography is known:

- [references/country-adapters.md](references/country-adapters.md)

When the user asks for Excel, XLSX, delivery-ready tables, or a handoff workbook, also read:

- [references/xlsx-workbook-template.md](references/xlsx-workbook-template.md)
- [references/standard-output-sample.md](references/standard-output-sample.md)

If the task is only about field collection or source auditing, `source-policy.md` and `field-dictionary.md` are enough. If the task includes shortlist or probability judgement, read all four. If the task includes delivery formatting, read the workbook references too.

## Core Rules

Follow these rules throughout the workflow:

1. **No citation, no claim.**
   Every field used in the final output must have a source URL or be marked `unknown`.

2. **Eligibility first, competitiveness second.**
   First decide whether the applicant can apply. Only then estimate how competitive they are.

3. **Unknown is not no.**
   If a requirement is not explicitly stated, do not convert it into a negative. Mark it `unknown` or `needs manual review`.

4. **Inference must be labeled.**
   Teaching language, waiver likelihood, and some fit judgements may be inferred. Mark them as `inferred`, show the basis, and lower confidence if the inference matters.

5. **Official facts and community evidence stay separate.**
   Do not merge forum cases into the official requirements table.

6. **Project-specific pages beat generic pages.**
   If the program page conflicts with the university-wide graduate admissions page, follow the program page and record the conflict.

## Required Inputs

Collect or normalize these applicant-side fields first:

- target countries
- intended direction or keyword set
- highest degree
- current school and major
- GPA or average and grading scale
- GPA conversion method if non-standard
- English scores and test date
- internships, work, research, portfolio, certifications
- identity status that affects fee category
- budget range
- target intake

If the user does not provide a field, keep it as `unknown` and note whether the missing value affects:

- eligibility
- competitiveness
- budget fit

Treat each assessment target as:

- `program + intake + study mode + applicant_profile_version`

Do not silently reuse a prior judgement if the applicant profile or target intake changed.

## Workflow

### Step 1: Normalize the Applicant Snapshot

Build a single applicant snapshot before looking at programs. Use the field names in [references/field-dictionary.md](references/field-dictionary.md).

Important:

- Do not invent a GPA conversion formula.
- If the grading policy is school-specific, mark conversion as `pending official school formula`.
- Treat each updated applicant profile as a new snapshot if material facts change.

### Step 2: Build the Candidate Program Pool

Start from official university or faculty program listings, not from agency blogs.

Use community sources only for:

- discovering candidate programs
- spotting common outcome patterns
- finding offer, reject, or waitlist examples

At this stage, keep programs broad. Remove only obviously irrelevant programs.

### Step 3: Collect Official Facts Field by Field

For each candidate program:

1. Find the program-specific admission page.
2. Find the tuition page for the same program or faculty.
3. Extract only the fields defined in [references/field-dictionary.md](references/field-dictionary.md).
4. For each field, store:
   - normalized value
   - raw quote or raw snippet
   - source URL
   - capture date
   - `explicit` or `inferred`

Follow the exact hierarchy and conflict rules in [references/source-policy.md](references/source-policy.md).

### Step 4: Collect Community Evidence

Community evidence is optional for simple fact collection, but required for shortlist and competitiveness work.

Collect both supporting and adverse evidence:

- offers
- rejects
- waitlists
- interview reports
- timeline posts

For every case, capture:

- source URL
- post date
- target intake if known
- applicant background
- result
- credibility notes

Do not convert a handful of offer posts into a precise probability. Community cases are supporting evidence, not ground truth.

### Step 5: Normalize, Audit, and Flag Gaps

Before making judgements:

- separate official facts from community evidence
- align fields to the canonical schema
- mark stale fee data
- mark conflicts across official pages
- mark JS-rendered or inaccessible pages
- mark missing prerequisites or transcript-dependent checks

If a blocking item remains unresolved, keep the final judgement conservative and lower confidence.

### Step 6: Assess

Use [references/assessment-framework.md](references/assessment-framework.md).

Always output these judgement layers:

- `eligibility_status`
- `competitiveness_band`
- `assessment_confidence`
- `direction_fit`
- `budget_fit`
- `key_risks`
- `manual_review_required`
- `action_recommendation`

Never output only a raw probability without explanation.

### Step 7: Produce an Auditable Deliverable

Preferred final structure:

1. **Applicant Snapshot**
   Include unknowns and assumptions.

2. **Program Facts Table**
   Official facts only, one row per `program + intake + study mode`.

3. **Community Evidence Table**
   Case-by-case links, dates, result type, similarity notes.

4. **Assessment Table**
   Judgement fields with reasons and supporting references.

5. **Open Issues / Manual Review Queue**
   Anything that blocks a confident recommendation.

If the user wants an Excel-ready export, use the columns from [references/field-dictionary.md](references/field-dictionary.md).
Prefer the workbook structure in [references/xlsx-workbook-template.md](references/xlsx-workbook-template.md) and mirror the phrasing style in [references/standard-output-sample.md](references/standard-output-sample.md).

If evidence is strong enough, you may add an optional `estimated_probability_range` that matches the competitiveness band. If evidence is weak, omit the range and rely on the band plus confidence.

## Stop Rules

Do not present a confident final recommendation if any of these are true:

- no official admission page was found
- tuition comes only from non-official aggregators
- official pages conflict on a critical field
- a key field is based only on inference
- prerequisites depend on transcript details the user did not provide
- community evidence is too thin to support a competitiveness claim

In these cases, output `needs manual review` with the exact blocker.

## Quality Checklist

- [ ] Every official field used in judgement has a source URL
- [ ] Every inferred field is labeled as inferred
- [ ] Official facts and community cases are separated
- [ ] Eligibility is stated separately from competitiveness
- [ ] Country-specific checks were applied
- [ ] Major unknowns and stale fields are surfaced
- [ ] The output includes a manual review queue when needed

## Final Reminder

The goal is not to sound certain. The goal is to produce a useful, reviewable admissions research artifact that a human can audit quickly.
