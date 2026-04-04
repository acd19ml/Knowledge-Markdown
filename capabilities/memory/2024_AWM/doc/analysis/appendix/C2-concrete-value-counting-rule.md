# Appendix C2. Concrete-Value Counting Rule

> Purpose: fix the counting drift around “concrete values” in `mechanism-analysis.md`.
>
> Primary sources:
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/doc/analysis/wf_text_compare_output.txt`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/kayak_lm_wf.txt`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/newegg_lm_wf.txt`
> - `/Users/mac/studyspace/Knowledge-Markdown/capabilities/memory/2024_AWM/experiments/mind2web/workflow/united_lm_wf.txt`

## C2.1 Recommended counting rule

For the LM workflows, count a token as a `concrete value` only if it is a task-instantiated or user-instantiated value that could vary by task, such as:

- city names
- dates
- product names
- confirmation numbers
- personal identifiers

Do **not** count fixed UI labels as concrete task values, such as:

- `Increment`
- `View Deal`
- `APPLY`
- `TRAVEL INFO`
- `Find cars button.`

Under this rule, the LM workflow files for `kayak`, `newegg`, and `united` contain:

| Website | LM concrete values |
|---|---:|
| `kayak` | 0 |
| `newegg` | 0 |
| `united` | 0 |

## C2.2 Why this rule is needed

The earlier drift comes from mixing two things:

1. **task-variable values**, which should count as concrete values
2. **fixed UI labels**, which should not

The current LM workflow files are parameterized almost entirely with placeholders such as:

- `{location_name}`
- `{search-term}`
- `{origin-city}`
- `{destination-city}`
- `{start-date}`

## C2.3 Supporting excerpts

### Kayak

```text
[textbox]  {location_field} -> TYPE: {location_name}
[span]  {location_suggestion} -> CLICK
[button]  {date_input} -> CLICK
[div]  {date_day} -> CLICK
```

### Newegg

```text
[searchbox]  Search Site -> TYPE: {search-term}
[textbox]  price to -> TYPE: {max-price}
[span]  {filter-option} -> CLICK
[link]  {category-link} -> CLICK
```

### United

```text
[combobox]  Enter your departing city, airport name, or airpor... -> TYPE: {origin-city}
[button]  {origin-option} -> CLICK
[combobox]  Enter your destination city, airport name, or airp... -> TYPE: {destination-city}
[button]  {destination-option} -> CLICK
```

## C2.4 Safe usage in正文

The safe wording is:

> “Under the placeholder-vs-task-value counting rule used in the workflow text audit, the LM workflows contain no task-instantiated concrete values; their specificity is carried primarily by placeholders and fixed UI labels.”

## C2.5 Boundary note

If a later section wants to count fixed UI labels separately, it should use a different name such as `fixed interface literals`, not `concrete values`.
