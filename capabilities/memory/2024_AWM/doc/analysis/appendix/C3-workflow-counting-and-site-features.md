# Appendix C3. Workflow Counting and Site-Feature Definitions

> Purpose: fix the counting drift around LM workflow counts and average steps per workflow.
>
> Primary sources:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/wf_text_compare_output.txt`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/kayak_lm_wf.txt`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/newegg_lm_wf.txt`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/united_lm_wf.txt`

## C3.1 Two valid counting conventions

There are two defensible workflow-count conventions in the current materials:

1. **Include `Summary Workflows` as a workflow block**
   - This is the convention implicitly used by `wf_text_compare_output.txt`
   - Counts: `kayak 8`, `newegg 6`, `united 6`

2. **Exclude `Summary Workflows` and count only executable named workflows**
   - This is the convention used in `C5`
   - Counts: `kayak 7`, `newegg 5`, `united 5`

## C3.2 Conversion table

| Website | Total steps | Count incl. summary | Avg steps/WF incl. summary | Count excl. summary | Avg steps/WF excl. summary |
|---|---:|---:|---:|---:|---:|
| `kayak` | 14 | 8 | 1.75 | 7 | 2.00 |
| `newegg` | 10 | 6 | 1.67 | 5 | 2.00 |
| `united` | 16 | 6 | 2.67 | 5 | 3.20 |

## C3.3 Supporting excerpts

### Kayak

```text
## Summary Workflows:
## enter_search_location
...
## select_calendar_date
...
## apply_amenity_filter
...
## sort_search_results
...
## set_flight_trip_type
...
## adjust_guests_rooms
...
## book_selected_option
...
```

### Newegg

```text
Website: Shopping,Digital,newegg
## Summary Workflows:
## search_product
...
## apply_price_filter
...
## apply_selection_filter
...
## navigate_category_links
...
## open_site_menu_and_select
...
```

## C3.4 Recommended use

- Use **include-summary** counts when comparing directly against `wf_text_compare_output.txt`.
- Use **exclude-summary** counts when discussing `C5` quality metrics.
- Do not mix the two in one table without labeling the convention.

## C3.5 Safe wording in正文

The safe wording is:

> “The LM workflow count is 8/6/6 if the summary block is treated as a workflow header block, and 7/5/5 if only executable named workflows are counted. The report should label which convention it is using.”
