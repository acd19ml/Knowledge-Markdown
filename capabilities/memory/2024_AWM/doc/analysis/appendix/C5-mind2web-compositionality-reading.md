# Appendix C5. Mind2Web Compositionality Reading

## Purpose

The AWM paper uses workflow composition as part of its broader narrative, especially in more open-ended settings. On Mind2Web, the question is subtler:

- do the induced workflows show any sign of reusable subflows?
- if yes, is that sign closer to true composition, or only to a flat library of reusable routines?

This note answers that question by reading the actual workflow texts and contrasting stronger vs weaker cases.

## Source Materials

- [kayak_offline_wf.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/kayak_offline_wf.txt)
- [kayak_lm_wf.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/kayak_lm_wf.txt)
- [kayak_online_wf.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/kayak_online_wf.txt)
- [united_offline_wf.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/united_offline_wf.txt)
- [united_lm_wf.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/united_lm_wf.txt)
- [newegg_offline_wf.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/newegg_offline_wf.txt)
- [newegg_lm_wf.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/newegg_lm_wf.txt)
- [budget_offline_wf.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/budget_offline_wf.txt)
- [C1-lm-vs-rule-text-evidence.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/C1-lm-vs-rule-text-evidence.md)

## C5.1 Three Senses of “Compositionality”

To avoid over-claiming, this appendix separates three different notions:

1. **Explicit hierarchical composition**
   - one workflow directly calls or nests another
   - this is **not observed** in the current Mind2Web workflow texts

2. **Flat subflow reuse**
   - a task can be completed by chaining several short reusable routines
   - this is **clearly present on some sites**

3. **Template bundling**
   - workflows are reusable only in a weak sense because they remain long, site- or task-specific bundles
   - this is also present, especially on weaker sites

The current Mind2Web evidence supports (2) much more than (1).

## C5.2 Stronger Evidence of Flat Subflow Reuse

### `kayak`

The `kayak` workflow libraries provide the cleanest evidence of subflow-style reuse.

In [kayak_lm_wf.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/kayak_lm_wf.txt), the workflow set is split into short units such as:

- `enter_search_location`
- `select_calendar_date`
- `apply_amenity_filter`
- `sort_search_results`
- `set_flight_trip_type`
- `adjust_guests_rooms`
- `book_selected_option`

These are not end-to-end task scripts. They are local routines that can plausibly be chained in different orders depending on the task:

- enter location
- select date
- adjust guest count
- sort/filter
- select a result

The older [kayak_offline_wf.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/kayak_offline_wf.txt) shows the same pattern in a slightly broader form:

- location entry
- travel date selection
- flight type selection
- filter selection
- deal viewing

This is the strongest Mind2Web evidence that AWM is not merely memorizing full trajectories. On `kayak`, the workflow library really looks like a set of reusable subroutines.

### `united`

`united` also shows substantial flat compositionality.

In [united_lm_wf.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/united_lm_wf.txt), the workflow set decomposes tasks into separable units:

- `enter_flight_locations`
- `select_travel_dates`
- `navigate_travel_info`
- `search_rental_car`
- `enter_trip_credentials`

Again, these are not one-shot whole-task solutions. They correspond to pieces of larger airline-site tasks:

- flight search setup
- date picking
- account/trip retrieval
- travel-information navigation
- car-rental branching

So `united`, like `kayak`, supports a library-style reading of composition: not nested function composition, but recombinable site routines.

## C5.3 Weaker or More Ambiguous Cases

### `newegg`

`newegg` still shows reuse, but the compositionality signal is weaker.

In [newegg_lm_wf.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/newegg_lm_wf.txt), the workflows include:

- `search_product`
- `apply_price_filter`
- `apply_selection_filter`
- `navigate_category_links`
- `open_site_menu_and_select`

These are reusable, but they are also closer to **site utilities** than to cleanly composable task fragments.

A task may use search + filter + category navigation, but the overall structure is less obviously decomposed into stable subflows than on `kayak` or `united`. The workflows look reusable, yet the library feels shallower and more page-local.

### `budget`

`budget` is the clearest counterexample to a strong compositionality story.

[budget_offline_wf.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/budget_offline_wf.txt) mixes:

- car-rental location search
- vehicle/extras selection
- date/time entry
- reservation lookup
- career-site job search
- deals browsing

Some of these routines are internally structured, but the library as a whole is heterogeneous and weakly unified. It is better described as a **bundle of extracted templates** than as a coherent compositional vocabulary.

This matters because it explains why “workflow reuse” on Mind2Web is highly site-dependent. A site can contain repeated sequences without supporting a strong composition story.

## C5.4 Online Workflow Compression

The online workflows weaken explicit compositionality even further.

For example, [kayak_online_wf.txt](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/kayak_online_wf.txt) contains routines such as:

- `search_for_cars_kayak`
- `select_location_kayak`
- `select_dates_for_rental_kayak`
- `browse_car_type_kayak`

These are useful, but more trajectory-shaped and narrower than the LM or offline libraries. So even when they are reusable, they look more like compressed routines tied to a recent successful path than like a broad compositional basis.

This is consistent with [A7-offline-vs-online-tradeoff.md](/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/appendix/A7-offline-vs-online-tradeoff.md): online memory is closer to local test behavior, but less robust as a general reusable library.

## C5.5 Bottom-Line Reading

The current Mind2Web evidence supports the following layered conclusion:

- **explicit hierarchical composition:** not supported
- **flat subflow reuse:** clearly supported on `kayak` and `united`
- **weaker, utility-style reuse:** present on `newegg`
- **template bundling rather than true composition:** visible on `budget`

So the fairest critical-reproduction statement is:

> On Mind2Web, AWM does show signs of subflow reuse, but mostly as a flat library of short reusable routines rather than as explicit hierarchical workflow composition. This makes the paper's composition narrative partially visible, but much weaker and flatter than the stronger composition story associated with more open-ended environments.

## C5.6 Boundary Note

- This appendix is a source-driven qualitative reading, not a formal graph-structure analysis.
- It should support qualitative discussion of composition, not be turned into a hard quantitative claim.
