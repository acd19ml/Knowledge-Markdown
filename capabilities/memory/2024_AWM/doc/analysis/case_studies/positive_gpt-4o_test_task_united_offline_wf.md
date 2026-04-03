# Positive Cases: gpt-4o_test_task_united_offline_wf

Total positive steps: 3, showing top 3


## Case 1: task=0, step=3/8

**Task:** Task: Find the TSA Guidelines to travel with Children

**Target:** `CLICK [14032]`

**Baseline pred:** `CLICK [14587]` (ea=0, af=1.00)

**Workflow pred:** `CLICK [14032]` (ea=1, af=1.00)

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


## Case 2: task=3, step=21/27

**Task:** Task: Book a round-trip flight from Santa Fe, New Mexico to Phoenix, Arizona for 1 adult on August 13th and returning on August 28th.

**Target:** `CLICK [77661]`

**Baseline pred:** `CLICK [78125]` (ea=0, af=1.00)

**Workflow pred:** `CLICK [77661]` (ea=1, af=1.00)

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


## Case 3: task=4, step=1/12

**Task:** Task: Compare the fare types to book a 1-adult ticket from Springfiels, IL to Austin, TX for April 29th 2023

**Target:** `TYPE [4116] [Chicago]`

**Baseline pred:** `TYPE [4116] [CHICAGO]` (ea=1, af=0.50)

**Workflow pred:** `TYPE [4116] [Chicago]` (ea=1, af=1.00)

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
