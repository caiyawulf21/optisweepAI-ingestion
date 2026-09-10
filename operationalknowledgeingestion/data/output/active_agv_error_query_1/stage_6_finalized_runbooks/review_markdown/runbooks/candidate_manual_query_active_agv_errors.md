# Query Active AGV Errors From the WCS Database

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_query_active_agv_errors_from_the_wcs_database_v1` |
| Title | Query Active AGV Errors From the WCS Database |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | None |
| Support Safe | Yes |
| Capability Tags | `agv_active_errors`, `wcs_service_health` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Retrieve current active AGV error records from the WCS database by logging into the WCS primary server, opening the WCS database, creating a new query tab, entering the documented SQL query against [Helix2x_1Prod_Robotics].[dbo].[SystemActiveErrorModel], executing it, and reviewing the returned results.

## When To Use

Use this procedure when active AGV error records need to be retrieved from the WCS database for investigation or visibility.

## Do Not Use For

* Do not use this procedure as a corrective action for AGV errors; the source only provides retrieval steps.
* Do not use this procedure when WCS primary server or WCS database access is unavailable.

## Safety And Operational Notes

* This is a source-backed diagnostic retrieval procedure.
* The source does not provide corrective actions for returned errors; use the output for investigation only.

## Access Or Tools Needed

* Access to the WCS primary server
* Access to the WCS database
* Database query interface with a new query tab
* The documented SQL query text

## Related Operational Context

* ctx_manual_wcs_primary_server_access_v1
* ctx_manual_systemactiveerrormodel_reference_v1
* ctx_manual_active_agv_error_fields_v1
* ctx_manual_query_tab_results_screen_v1

## Procedure Steps

### Step 1 — Log into the WCS primary server

**Responsible role:** L2_support

**Instruction:**
Log into the WCS primary server.

**Expected result:**
You are logged into the WCS primary server and can continue to the database access step.

**Screens / Images:**

- `artifact_manual_active_agv_error_query_1_page_1_image_1`: Initial server access or login entry point associated with the first procedure step.
- `artifact_manual_active_agv_error_query_1_page_1_image_2`: Initial server access or login entry point associated with the first procedure step.

**Stop or Escalate If:**

* Escalate if access to the WCS primary server is not available.

---

### Step 2 — Open the WCS database

**Responsible role:** L2_support

**Instruction:**
Open the WCS database.

**Expected result:**
The WCS database is open and ready for query entry.

**Screens / Images:**

- `artifact_manual_active_agv_error_query_1_page_1_image_1`: Database access point or initial database selection area after server login.
- `artifact_manual_active_agv_error_query_1_page_1_image_2`: Database access point or initial database selection area after server login.

**Stop or Escalate If:**

* Escalate if access to the WCS database is not available.

---

### Step 3 — Open a new query tab

**Responsible role:** L2_support

**Instruction:**
Open a new query tab by clicking the indicated control.

**Expected result:**
A new query tab opens and is ready for SQL entry.

**Screens / Images:**

- `artifact_manual_active_agv_error_query_1_page_2_image_1`: UI control used to open a new query tab and where the new tab appears.
- `artifact_manual_active_agv_error_query_1_page_2_image_2`: UI control used to open a new query tab and where the new tab appears.

**Stop or Escalate If:**

* Escalate if the query interface does not allow a new query tab to be opened.

---

### Step 4 — Paste the documented SQL query into the new tab

**Responsible role:** L2_support

**Instruction:**
Copy and paste the provided SQL query into the newly opened query tab.

**Expected result:**
The query editor contains the documented SQL statement.

**Screens / Images:**

- `artifact_manual_active_agv_error_query_1_page_2_image_1`: Query editor area where the SQL statement should be entered.
- `artifact_manual_active_agv_error_query_1_page_2_image_2`: Query editor area where the SQL statement should be entered.

**Stop or Escalate If:**

* Escalate if the documented query cannot be entered into the query tab.

---

### Step 5 — Use the documented active AGV error query text

**Responsible role:** L2_support

**Instruction:**
Use the provided query text exactly as documented: SELECT TOP (1000) [Id], [EntityInserted], [EntityLastUpdate], [Name], [Area], [Error], [LastSeen], [SystemErrorDescription], [SystemErrorResolution] FROM [Helix2x_1Prod_Robotics].[dbo].[SystemActiveErrorModel].

**Expected result:**
The query text references the documented fields and the [Helix2x_1Prod_Robotics].[dbo].[SystemActiveErrorModel] table.

**Screens / Images:**

- `artifact_manual_active_agv_error_query_1_page_2_image_1`: Query editor area containing the pasted SQL statement.
- `artifact_manual_active_agv_error_query_1_page_2_image_2`: Query editor area containing the pasted SQL statement.

**Stop or Escalate If:**

* Escalate if the documented query text cannot be confirmed or does not match the source.

---

### Step 6 — Execute the query

**Responsible role:** L2_support

**Instruction:**
Right click on the query and click execute.

**Expected result:**
The query runs and the interface proceeds to display returned results.

**Screens / Images:**

- `artifact_manual_active_agv_error_query_1_page_2_image_1`: Query area where the execute action is initiated.
- `artifact_manual_active_agv_error_query_1_page_2_image_2`: Query area where the execute action is initiated.

**Stop or Escalate If:**

* Escalate if the query cannot be executed.

---

### Step 7 — Review the results area

**Responsible role:** L2_support

**Instruction:**
Review the results area where the active errors appear.

**Expected result:**
A results area displays the active AGV errors returned by the query.

**Screens / Images:**

- `artifact_manual_active_agv_error_query_1_page_4_image_1`: Results panel or table where active AGV errors are shown after execution.
- `artifact_manual_active_agv_error_query_1_page_4_image_2`: Results panel or table where active AGV errors are shown after execution.

**Stop or Escalate If:**

* Escalate if the results area does not display returned active errors.

---

### Step 8 — Check the returned fields in the results

**Responsible role:** L2_support

**Instruction:**
Check the returned fields in the results, including Id, EntityInserted, EntityLastUpdate, Name, Area, Error, LastSeen, SystemErrorDescription, and SystemErrorResolution.

**Expected result:**
The results include the documented identifier, timestamp, area, error, description, and resolution fields.

**Screens / Images:**

- `artifact_manual_active_agv_error_query_1_page_4_image_1`: Returned results table and the displayed columns for active AGV errors.
- `artifact_manual_active_agv_error_query_1_page_4_image_2`: Returned results table and the displayed columns for active AGV errors.

**Stop or Escalate If:**

* Escalate if expected fields are not present in the returned results.

---

## Success Criteria

* The WCS primary server is accessed successfully.
* The WCS database is opened successfully.
* A new query tab is opened.
* The documented SQL query against [Helix2x_1Prod_Robotics].[dbo].[SystemActiveErrorModel] is entered.
* The query executes successfully.
* The results area displays active AGV error records.
* Returned results include Id, EntityInserted, EntityLastUpdate, Name, Area, Error, LastSeen, SystemErrorDescription, and SystemErrorResolution.

## Failure Conditions

* Access to the WCS primary server is not available.
* Access to the WCS database is not available.
* A new query tab cannot be opened.
* The query cannot be executed.
* The results area does not display returned active errors.
* Expected fields are missing from the returned results.

## Escalation Guidance

* Escalate if access to the WCS primary server or WCS database is not available.
* Escalate if the query cannot be executed or the results area does not display returned active errors.
* Use the output for investigation only; the source does not provide corrective actions for returned errors.

## Missing Details / Known Gaps

* The source does not provide an estimated completion time.
* The source does not specify whether production stop is required.
* The source does not specify whether LOTO is required.
* The source does not provide exact login credentials, server path, or database navigation details.
* The source does not provide interpretation logic for specific returned error values.
* The source does not provide corrective actions for returned active AGV errors.
* The source does not explicitly document the exact UI location of the execute control beyond the instruction to right click on the query and click execute.

## Source Lineage

- Candidate IDs: candidate_manual_query_active_agv_errors
- Source ID: `active_agv_error_query_1`
- Source Type: `manual`
