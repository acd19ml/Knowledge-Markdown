# Positive Cases: gpt-4o_test_task_kayak_offline_wf

Total positive steps: 3, showing top 3


## Case 1: task=1, step=9/10

**Task:** Task: Find hotels in Las Vegas, NV that offer free airport shuttle service.

**Target:** `CLICK [57318]`

**Baseline pred:** `` (ea=0, af=0.00)

**Workflow pred:** `CLICK [57318]` (ea=1, af=1.00)

**Workflow (excerpt):**
```
## Workflow 1: Enter Location for Car or Hotel Search
Given that you are on the car or hotel search page, this workflow enters the pick-up/drop-off location or city for your search.
- [textbox] Pick-up/Enter location -> CLICK
- [textbox] Pick-up/Enter location -> TYPE: {your-location}
- [span] {best-popup-option} -> CLICK

## Workflow 2: Select Travel Dates
Given that you are on the search page for flights, cars, or hotels, this workflow selects the travel dates.
- [generic/button] Start date/En
```


## Case 2: task=4, step=8/14

**Task:** Task: check cheap flights from NYC to London on 23rd of April for students over 18 years.

**Target:** `CLICK [59393]`

**Baseline pred:** `CLICK [63241]` (ea=0, af=1.00)

**Workflow pred:** `CLICK [59393]` (ea=1, af=1.00)

**Workflow (excerpt):**
```
## Workflow 1: Enter Location for Car or Hotel Search
Given that you are on the car or hotel search page, this workflow enters the pick-up/drop-off location or city for your search.
- [textbox] Pick-up/Enter location -> CLICK
- [textbox] Pick-up/Enter location -> TYPE: {your-location}
- [span] {best-popup-option} -> CLICK

## Workflow 2: Select Travel Dates
Given that you are on the search page for flights, cars, or hotels, this workflow selects the travel dates.
- [generic/button] Start date/En
```


## Case 3: task=5, step=5/6

**Task:** Task: Find the cheapest Hawaii package for two adults from June 18 to 21, and the hotel must be near a beach, have a beachfront, hot tub, and pool, and provides towels.

**Target:** `CLICK [44607]`

**Baseline pred:** `CLICK [45034]` (ea=0, af=1.00)

**Workflow pred:** `CLICK [44607]` (ea=1, af=1.00)

**Workflow (excerpt):**
```
## Workflow 1: Enter Location for Car or Hotel Search
Given that you are on the car or hotel search page, this workflow enters the pick-up/drop-off location or city for your search.
- [textbox] Pick-up/Enter location -> CLICK
- [textbox] Pick-up/Enter location -> TYPE: {your-location}
- [span] {best-popup-option} -> CLICK

## Workflow 2: Select Travel Dates
Given that you are on the search page for flights, cars, or hotels, this workflow selects the travel dates.
- [generic/button] Start date/En
```
