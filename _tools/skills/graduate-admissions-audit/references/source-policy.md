# Source Policy

This skill is built around auditable sourcing. The priority order below is mandatory.

## 1. Source Hierarchy

### First Priority: Program-Specific Official Pages

Use program or faculty pages for:

- admission requirements
- language requirements
- special requirements
- tuition
- application dates

Preferred examples:

- program admission page
- faculty program page
- program tuition page
- program FAQ page if maintained by the same official unit

### Second Priority: University-Wide Graduate Admissions Pages

Use these only when the program-specific page is incomplete or silent.

Examples:

- graduate school admissions pages
- official international qualifications pages
- university-wide English language requirement pages

If the generic page conflicts with the program page, the program page wins unless the program page is clearly outdated.

### Third Priority: Current Official PDFs

Use an official PDF only when:

- the HTML page is missing critical information
- the page is JS-rendered and inaccessible
- the PDF clearly applies to the target intake or recent cycle

If the PDF year is stale, mark the field as `stale_official_source`.

### Community Sources: Evidence Only

Community sources can be used for:

- discovering programs
- collecting offer, reject, or waitlist examples
- understanding applicant anecdotes

Community sources must not be used as the official source for:

- tuition
- language requirements
- degree requirements
- deadlines
- prerequisites

## 2. Field-Level Rules

### Language Requirements

- Pull language requirements from the program admission page first.
- Do not apply the university-wide English minimum to every program by default.
- If the program page requires Chinese proficiency but does not mention IELTS or TOEFL, record exactly that and mark English requirement as `unknown` unless the page clearly grants a waiver.

### Teaching Language

Do not guess from marketing copy alone.

Infer only from official evidence:

- Chinese proficiency required without English test: likely Chinese-medium
- English test required without Chinese requirement: likely English-medium
- both required: likely bilingual or mixed requirements

When inferred, store:

- inferred value
- basis
- lower confidence

### Tuition

- Always distinguish `local_or_domestic` from `non_local_or_international` when available.
- If the official page lists one figure only, record `not separated`.
- Record the tuition year or academic year.
- If the tuition year is older than the target intake by more than two cycles, mark it `needs update`.
- Note special lock-in rules when the school publishes them.

### GPA and Degree Equivalency

- Do not use a generic GPA conversion formula when the applicant's school uses a special method.
- If official conversion is unavailable, keep the original scale and mark comparability as limited.

### Deadlines

- Capture the full date when available.
- Distinguish `rolling`, `rounds`, and `fixed deadline`.
- If multiple rounds exist, keep each round or note that multiple rounds apply.

## 3. Conflict Handling

When official sources disagree:

1. Prefer program-specific over generic.
2. Prefer the source with a clearer intake year.
3. Prefer the source with the later update date if both are official and same level.
4. If unresolved, mark the field `conflicting_official_sources` and send it to manual review.

## 4. JS-Rendered or Empty Pages

If an official page loads but does not expose the needed data:

- record the URL anyway
- mark the field `js_rendered_not_captured`
- look for an official PDF or alternate official page
- do not fill the field with a guessed value

## 5. Auditability Requirements

Every fact used in the final output should preserve:

- normalized field value
- raw snippet
- source URL
- capture date
- explicit or inferred status
- applicable intake when known

If one of these is missing, the field is not audit-ready.

## 6. Prohibited Sources for Facts

Do not use these as official fact sources:

- agency blogs
- content farms
- generic rankings or aggregator pages
- old handbooks without a valid target year
- reposted screenshots without a clickable original source
