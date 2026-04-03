# Negative Cases: gpt-4o_test_task_united_offline_wf

Total negative steps: 2, showing top 2


## Case 1: task=1, step=1/4

**Task:** Task: Book me a flight from BWI to NYC for 2 for August 2nd-August 7th

**Target:** `TYPE [44062] [10987654]`

**Baseline pred:** `TYPE [44062] [10987654]` (ea=1, af=1.00)

**Workflow pred:** `TYPE [44062] 10987654` (ea=1, af=0.67)

**Workflow (excerpt):**
```
### Workflow 3: find_trip_by_confirmation
**Description:** This workflow finds a trip using a confirmation number and passenger name.
- [tab] MY TRIPS -> CLICK
- [link or combobox] Find trip by confirmation number -> CLICK
- [textbox/input] Confirmation or ticket number -> TYPE: {confirmation-number}
- [textbox/input] Last Name -> TYPE: {passenger-last-name}
- [button] SUBMIT/SEARCH -> CLICK

### Workflow 4: view_baggage_information
**Description:** Navigates to baggage information and calculate
```


## Case 2: task=3, step=18/27

**Task:** Task: Book a round-trip flight from Santa Fe, New Mexico to Phoenix, Arizona for 1 adult on August 13th and returning on August 28th.

**Target:** `CLICK [57840]`

**Baseline pred:** `CLICK [57840]` (ea=1, af=1.00)

**Workflow pred:** `CLICK [60556]` (ea=0, af=1.00)

**Workflow (excerpt):**
```
### Workflow 3: find_trip_by_confirmation
**Description:** This workflow finds a trip using a confirmation number and passenger name.
- [tab] MY TRIPS -> CLICK
- [link or combobox] Find trip by confirmation number -> CLICK
- [textbox/input] Confirmation or ticket number -> TYPE: {confirmation-number}
- [textbox/input] Last Name -> TYPE: {passenger-last-name}
- [button] SUBMIT/SEARCH -> CLICK

### Workflow 4: view_baggage_information
**Description:** Navigates to baggage information and calculate
```
