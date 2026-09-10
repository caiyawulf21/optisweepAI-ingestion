# Hospital HMI shows a fault during bag-out/tote flow: acknowledge/retry and confirm tote identity

## Playbook Header

| Field | Value |
| --- | --- |
| Playbook ID | `playbook_incident_218550_hospital_hmi_fault_acknowledge_retry_tote_id` |
| Case ID | `218550` |
| Extraction Mode | `one_or_more_playbook_candidates_when_separable` |
| Confidence | `medium` |
| Validation Status | `needs_sme_review` |

## Entry Symptoms

- “The HMI at the hospital is showing a fault.”
- “Should I unplug it?”
- Fault appears on the hospital/tote screen during bag-out activity.
- After acknowledge/retry, the site reports “all good.”

## Affected Systems

- Hospital HMI / lane UI
- tote/bag-out workflow state (as reflected on HMI)

## Nodes

### 1 — Confirm hospital HMI fault and whether tote identity matches the workflow expectation (`diagnostic_decision`)

**Intent:** Determine whether the operator-visible hospital HMI fault is present and whether the tote ID shown/expected matches the tote actually present/being processed.

**Expects capability:** lane_or_chute_state, tote_exchange_sequence
**Expects surface:** hospital_hmi
**Preferred audience:** operator, L1_support

**Runbook Links:**

- unresolved
  - catalog gap: Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=hospital Hmi): Hospital HMI fault is confirmed present, and tote ID on the hospital HMI matches the tote physically present/being processed after site/operator confirmation.
- `unhealthy` (observer=site_or_remote; tool=hospital Hmi): Fault is present and tote ID cannot be confirmed or appears inconsistent with the tote physically present/being processed.
- `inconclusive` (observer=site_or_remote; tool=hospital Hmi): Hospital HMI fault is present but tote ID confirmation is not possible (HMI unreadable, missing tote ID field, or operator cannot validate).
- `escalate` (observer=site; tool=hospital Hmi): Hospital HMI fault cannot be verified or operator reports inability to access/operate Hospital HMI required controls for acknowledgement/retry or tote ID confirmation.

**Branches:**

- `unhealthy` → `node_2` when Unhealthy
- `healthy` → `` when Healthy/Not matched
- `inconclusive` → `node_2` when Inconclusive

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

### 2 — Acknowledge the hospital HMI fault and retry the operation (`procedure_reference`)

**Intent:** Execute the approved HMI fault handling approach (acknowledge and retry) without physical power actions like unplugging unless explicitly authorized by a runbook.

**Expects capability:** n/a
**Expects surface:** hospital_hmi
**Preferred audience:** operator

**Runbook Links:**

- `proc_acknowledge_hmi_fault_and_retry_v1` (medium, support, score=0.6826, boosted=0.8226) — Acknowledge HMI fault at the hospital area and retry operation
  - gaps: Limited domain-term overlap between placeholder and runbook.

**Decision Outcomes:**

- `healthy` (observer=site_or_remote; tool=hospital Hmi): After acknowledge and retry, the Hospital HMI fault state clears or workflow advances; operator can proceed to validation of tote ID consistency.
- `unhealthy` (observer=site_or_remote; tool=hospital Hmi): After acknowledge and retry, the fault returns immediately or tote identity mismatch appears unresolved.
- `inconclusive` (observer=site_or_remote; tool=hospital Hmi): Acknowledge/retry attempted but the operator cannot determine whether the fault cleared (e.g., HMI unreadable or communication lag).
- `escalate` (observer=site; tool=hospital Hmi): Acknowledge/retry cannot be performed safely or at all (controls unavailable/disabled; persistent fault blocks progression).

**Branches:**

- `healthy` → `node_3` when Acknowledge/retry executed

**Linked Runbook Procedures:**

<details><summary><strong>Support runbooks</strong> (1)</summary>

<details><summary>Acknowledge HMI fault at the hospital area and retry operation (`proc_acknowledge_hmi_fault_and_retry_v1`)</summary>

##### Runbook: Acknowledge HMI fault at the hospital area and retry operation

- **Procedure ID:** `proc_acknowledge_hmi_fault_and_retry_v1`
- **Procedure Type:** `recovery`
- **Role:** `L2_support`
- **Audience:** `support`
- **Merge Status:** `pass_through`

**Summary:**
Source-specific incident recovery for an HMI fault reported at the hospital area within the UPS Haslet TX (TXRTH) incident context. The evidence supports viewing the faulted HMI, not unplugging the HMI, using the on-screen acknowledge action, retrying, confirming whether the tote is ID 28, and validating that the condition is cleared and reported as all good.

**When To Use:**
Use when the HMI associated with the hospital area is reported as showing a fault in the UPS Haslet TX (TXRTH) incident context, and the source-supported response is to acknowledge the fault on the HMI and retry the operation without unplugging the HMI.

**Safety Notes:**

- Do not unplug the HMI during this procedure; the source-supported response explicitly rejected unplugging.
- Use only the on-screen acknowledge-and-retry action supported by the incident evidence.
- Do not perform undocumented HMI changes or recovery modifications based on this case alone.

- **Source:** `incident_case` / `source_case_218550`

**Procedure Steps:**

###### Step 1 — View the hospital-area HMI fault

**Responsible role:** operator

**Instruction:**
Open or view the HMI associated with the hospital area and confirm that it is showing a fault before taking further action.

**Healthy condition:**
The HMI can be viewed and the reported fault context is identifiable.

**Expected result:**
The HMI fault is visible or confirmed in the same hospital-area context referenced in the incident.

**Step Images:**

![artifact_incident_218550_page_012_nested_image_01](assets/f881e4f18fba4f76.png)

*HMI-like screen associated with the chat message stating that the HMI at the hospital is showing a fault.*

---

###### Step 2 — Keep the HMI connected

**Responsible role:** operator

**Instruction:**
Do not unplug the HMI. Keep the device connected and prepare to use the on-screen acknowledge action instead.

**Healthy condition:**
The HMI stays connected and no unplug action is taken.

**Expected result:**
The HMI remains connected and available for the acknowledge-and-retry action.

**Step Images:**

![artifact_incident_218550_page_012_nested_image_01](assets/f881e4f18fba4f76.png)

*Use the same faulted HMI context; do not disconnect the device shown in this incident context.*

---

###### Step 3 — Acknowledge the fault and retry

**Responsible role:** operator

**Instruction:**
Use the HMI acknowledge control, then try the operation again.

**Healthy condition:**
The HMI accepts the acknowledge action and the retry proceeds.

**Expected result:**
The fault is acknowledged and the operation is retried without unplugging the HMI.

**Step Images:**

![artifact_incident_218550_page_012_nested_image_01](assets/f881e4f18fba4f76.png)

*Faulted HMI interface where the acknowledge action would be taken; screenshot text is unreadable, so rely on the chat-supported acknowledge instruction.*

---

###### Step 4 — Confirm whether the tote is ID 28

**Responsible role:** operator

**Instruction:**
Check the HMI context or confirm with site personnel whether the tote involved at the hospital area is tote ID 28.

**Healthy condition:**
The tote ID is confirmed from the HMI context or site confirmation.

**Expected result:**
The tote involved is identified and can be reported back to support.

**Step Images:**

![artifact_incident_218550_page_012_nested_image_01](assets/f881e4f18fba4f76.png)

*Hospital-area HMI/tote context associated with the support question about whether the tote ID is 28.*

---

###### Step 5 — Validate recovery status

**Responsible role:** L2_support

**Instruction:**
Verify with the site or from the HMI context that the tote at the hospital is 28 and that the condition is now cleared or reported as all good.

**Healthy condition:**
The issue is reported cleared and the site confirms normal status.

**Expected result:**
The site confirms the tote at the hospital is 28 and reports that the condition is all good.

---

**Success Criteria:**

- The hospital-area HMI fault is acknowledged without unplugging the HMI.
- The operation is retried successfully.
- The tote involved is confirmed as ID 28.
- The site reports the condition is all good.

**Failure Conditions:**

- The HMI cannot be accessed or the fault cannot be confirmed.
- The only contemplated next step is unplugging the HMI.
- Acknowledge-and-retry does not clear the fault.
- The tote ID cannot be confirmed.
- The site does not confirm that the condition is all good after retry.


</details>

</details>

---

### 3 — Validate HMI fault cleared and tote ID is consistent (`validation_gate`)

**Intent:** Confirm that the hospital HMI fault is cleared and that the tote ID confirmation matches the tote actually present/processed.

**Expects capability:** bag_out_or_closeout_state, tote_lifecycle_state
**Expects surface:** hospital_hmi
**Preferred audience:** operator, L1_support

**Runbook Links:**

- `proc_extract_arriving_tote_hospital_station_hmi_green_scanner_v1` (low, operator, score=0.8987, boosted=1.0) — Extract an Arriving Tote at the Hospital Station Using Hospital HMI and Green Scanner
  - gaps: Missing corroboration for `bag_out_or_closeout_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.
- `proc_check_hospital_hmi_operations_menu_induct_extract_status_v1` (low, operator, score=0.4883, boosted=0.5183) — Check Hospital HMI Operations Screen Induct/Extract Position Read-Only Data and WCS Status Messages
  - gaps: Missing corroboration for `bag_out_or_closeout_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Missing corroboration for `tote_lifecycle_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.; Limited domain-term overlap between placeholder and runbook.; Placeholder wording differs materially from matched runbook title.

**Catalog Gaps:**

- Missing corroboration for `bag_out_or_closeout_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.
- Missing corroboration for `tote_lifecycle_state`: no linked runbook covers this capability; prefer catalog peers with matching capability_tags / expects_surface.

**Decision Outcomes:**

- `healthy` (observer=site; tool=hospital Hmi): Hospital HMI fault cleared and tote ID is consistent with the tote physically present/processed; site reports “all good.”
- `unhealthy` (observer=site_or_remote; tool=hospital Hmi): Hospital HMI fault persists or tote ID mismatch remains unresolved.
- `inconclusive` (observer=site_or_remote; tool=hospital Hmi): Fault state is unclear and/or tote ID cannot be verified reliably.

**Branches:**

- `healthy` → `` when Confirmed recovery
- `unhealthy` → `node_4` when Validation failure

**Linked Runbook Procedures:**

<details><summary><strong>Operator runbooks</strong> (2)</summary>

<details><summary>Extract an Arriving Tote at the Hospital Station Using Hospital HMI and Green Scanner (`proc_extract_arriving_tote_hospital_station_hmi_green_scanner_v1`)</summary>

##### Runbook: Extract an Arriving Tote at the Hospital Station Using Hospital HMI and Green Scanner

- **Procedure ID:** `proc_extract_arriving_tote_hospital_station_hmi_green_scanner_v1`
- **Procedure Type:** `operation`
- **Role:** `operator`
- **Audience:** `operator`
- **Merge Status:** `pass_through`

**Summary:**
When an AGV brings a tote to the Hospital Station, use the Hospital HMI to open the correct tote-extraction screen based on the status fields, scan the tote barcode with the green scanner to populate the Tote ID field, and then perform the task indicated by the status fields. If the tote is being returned into the system, place it on the induct side (left) and ensure it is flush against the end stops.

**When To Use:**
Use this procedure when an AGV arrives at the Hospital Station with a tote and you need to extract the tote using the Hospital HMI workflow (screen selection driven by status fields), scan the tote barcode with the green scanner, and then execute the task indicated by the status fields.

**Safety Notes:**

- If the Tote ID field does not populate after scanning, stop and escalate for assistance rather than proceeding with the task.
- If the tote cannot be positioned flush against the induct-side end stops, stop and escalate for assistance.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Confirm a tote has arrived at the Hospital Station (right side)

**Responsible role:** operator

**Instruction:**
Visually confirm the AGV has brought a tote to the right side of the Hospital Station.

**Healthy condition:**
Tote is at the right side of the Hospital Station ready for extraction.

**Expected result:**
A tote is physically present at the Hospital Station right side designated for AGV tote delivery/extraction.

---

###### Step 2 — Open the corresponding Hospital HMI screen for tote extraction (based on status fields)

**Responsible role:** operator

**Instruction:**
On the Hospital HMI / lane UI, open the corresponding screen used to extract the tote from the system. Select the screen based on the information shown in the status fields.

**Healthy condition:**
You can see the status fields on the Hospital HMI screen that determine the extraction workflow.

**Expected result:**
The Hospital HMI tote-extraction screen corresponding to the arriving tote is open, showing status-field information used to determine the workflow.

---

###### Step 3 — Scan the tote barcode using the green scanner

**Responsible role:** operator

**Instruction:**
Scan the tote barcode using the green scanner.

**Healthy condition:**
The green scanner input is successfully read for the arriving tote barcode.

**Expected result:**
The scan is accepted by the Hospital HMI workflow and the Tote ID field begins to populate after scanning.

---

###### Step 4 — Verify Tote ID field auto-populates after scanning

**Responsible role:** operator

**Instruction:**
Verify that the Tote ID field automatically populates after scanning.

**Healthy condition:**
Tote ID field shows a value after the barcode scan.

**Expected result:**
The Tote ID field on the Hospital HMI is populated with the scanned tote ID.

---

###### Step 5 — Perform the task indicated by the status fields

**Responsible role:** operator

**Instruction:**
Perform whatever task needs to be performed as determined by the information in the status fields.

**Healthy condition:**
The task corresponding to the status fields is completed on the Hospital HMI workflow for that tote.

**Expected result:**
The required Hospital Station action for the arriving tote is executed according to the status fields on the active Hospital HMI screen.

---

###### Step 6 — If returning tote into the system, place it on the induct side (left) flush against end stops

**Responsible role:** operator

**Instruction:**
If the tote is going back into the system, put the tote on the induct side (left side) of the station and ensure it is flush against the end stops.

**Healthy condition:**
Tote is flush against the end stops on the induct side (left).

**Expected result:**
The tote is positioned on the induct side (left) and is flush against the induct-side end stops.

---

**Success Criteria:**

- Hospital HMI tote-extraction screen is opened for the arriving tote based on the status fields.
- Tote barcode scan is performed with the green scanner and the Tote ID field populates automatically after scanning.
- The task indicated by the status fields is performed.
- If returning the tote into the system, the tote is placed on the induct side (left) and is flush against the end stops.

**Failure Conditions:**

- Tote ID field does not populate after scanning.
- Tote cannot be positioned flush against the induct-side end stops.


</details>

<details><summary>Check Hospital HMI Operations Screen Induct/Extract Position Read-Only Data and WCS Status Messages (`proc_check_hospital_hmi_operations_menu_induct_extract_status_v1`)</summary>

##### Runbook: Check Hospital HMI Operations Screen Induct/Extract Position Read-Only Data and WCS Status Messages

- **Procedure ID:** `proc_check_hospital_hmi_operations_menu_induct_extract_status_v1`
- **Procedure Type:** `diagnostic`
- **Role:** `operator`
- **Audience:** `operator`
- **Merge Status:** `pass_through`

**Summary:**
Use the Hospital HMI / lane UI Operations Menu screen to read the WCS-fed induct and extract position fields (AGV#, Tote ID, Bar Code, Status). Confirm the Status messages explain why the tote is there and what station operator menu/action to use.

**When To Use:**
When a tote arrives at the hospital station and you need to determine what tote/AGV is at the induct and extract positions and what the WCS status message requires the station operator to do next.

- **Source:** `manual` / `manual_optisweep_om_v3`

**Procedure Steps:**

###### Step 1 — Open Hospital HMI Operations Menu and locate Induct Position / Extract Position sections

**Responsible role:** operator

**Instruction:**
On the Hospital HMI / lane UI, navigate to the Operations Menu screen that contains the "Induct Position" and "Extract Position" sections.

**Healthy condition:**
"Induct Position" and "Extract Position" sections are visible on the Operations Menu screen.

**Expected result:**
The screen shows both "Induct Position" and "Extract Position" sections.

---

###### Step 2 — Read Induct Position read-only fields (AGV#, Tote ID, Bar Code, Status)

**Responsible role:** operator

**Instruction:**
In the "Induct Position" section, read the four read-only fields: AGV#, Tote ID, Bar Code, and Status.

**Healthy condition:**
AGV#, Tote ID, Bar Code, and Status are present in the "Induct Position" section as read-only WCS data.

**Expected result:**
The "Induct Position" section displays values for AGV#, Tote ID, Bar Code, and a Status message.

---

###### Step 3 — Read Extract Position read-only fields (AGV#, Tote ID, Bar Code, Status)

**Responsible role:** operator

**Instruction:**
In the "Extract Position" section, read the four read-only fields: AGV#, Tote ID, Bar Code, and Status.

**Healthy condition:**
AGV#, Tote ID, Bar Code, and Status are present in the "Extract Position" section as read-only WCS data.

**Expected result:**
The "Extract Position" section displays values for AGV#, Tote ID, Bar Code, and a Status message.

---

###### Step 4 — Confirm both Status messages are present and provide WCS explanation/action guidance

**Responsible role:** operator

**Instruction:**
Verify that the "Induct Position" Status and "Extract Position" Status messages are present and written as messages received from the WCS that explain why the tote is there and what menu/action the station operator needs to use.

**Healthy condition:**
Induct Position Status and Extract Position Status each provide a clear WCS message describing why the tote is there and what menu/action to perform.

**Expected result:**
Both Status fields contain non-blank WCS messages that provide explanation and action/menu guidance.

---

**Success Criteria:**

- Induct Position shows read-only AGV#, Tote ID, Bar Code, and a non-blank Status message.
- Extract Position shows read-only AGV#, Tote ID, Bar Code, and a non-blank Status message.
- Both Status messages explain why the tote is there and what menu/action the station operator needs to use.

**Failure Conditions:**

- Induct Position Status is blank/missing.
- Extract Position Status is blank/missing.
- Either Status message does not provide explanation/action guidance (why the tote is there and what menu/action to use).


</details>

</details>

---

### 4 — Escalate if hospital HMI fault persists after acknowledge/retry and tote ID confirmation (`escalation_gate`)

**Intent:** Stop when the HMI fault cannot be cleared via the evidence-supported acknowledge/retry and tote ID consistency checks.

**Runbook Links:**

- unresolved
  - catalog gap: No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.

**Decision Outcomes:**

- `escalate` (observer=site; tool=hospital Hmi): Hospital HMI fault persists after acknowledge/retry and tote ID confirmation attempt; prepare escalation package for L2/L3 support.

**Branches:**

- `escalate` → `` when Escalate

**Linked Runbook Procedures:**

*No linked runbook content available.*

---

## Branch Graph

| From Node | Outcome | Condition | Next Node |
| --- | --- | --- | --- |
| `node_1` | `unhealthy` | Unhealthy | `node_2` |
| `node_1` | `healthy` | Healthy/Not matched | `` |
| `node_1` | `inconclusive` | Inconclusive | `node_2` |
| `node_2` | `healthy` | Acknowledge/retry executed | `node_3` |
| `node_3` | `healthy` | Confirmed recovery | `` |
| `node_3` | `unhealthy` | Validation failure | `node_4` |
| `node_4` | `escalate` | Escalate | `` |

## Unresolved / Low-Confidence Links

- node_1: unresolved — Missing evidence path: site interview/history branch — confirm with the site; do not substitute a fleet diagnostic runbook.
- node_3: proc_extract_arriving_tote_hospital_station_hmi_green_scanner_v1 (low)
- node_3: proc_check_hospital_hmi_operations_menu_induct_extract_status_v1 (low)
- node_4: unresolved — No runbook link expected for escalation/exit — proceed/escalate with gathered evidence; no branch outcomes required beyond escalate.
