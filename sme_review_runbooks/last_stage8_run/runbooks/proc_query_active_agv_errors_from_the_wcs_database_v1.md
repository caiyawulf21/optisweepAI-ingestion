# Query Active AGV Errors From the WCS Database

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_query_active_agv_errors_from_the_wcs_database_v1` |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Capability Tags | `agv_active_errors`, `wcs_service_health` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

Retrieve current active AGV error records from the WCS database by logging into the WCS primary server, opening the WCS database, creating a new query tab, entering the documented SQL query against [Helix2x_1Prod_Robotics].[dbo].[SystemActiveErrorModel], executing it, and reviewing the returned results.

## When To Use

Use this procedure when active AGV error records need to be retrieved from the WCS database for investigation or visibility.

## Source Procedure References

- proc_query_active_agv_errors_from_the_wcs_database_v1

## Safety And Operational Notes

- This is a source-backed diagnostic retrieval procedure.
- The source does not provide corrective actions for returned errors; use the output for investigation only.

## Procedure Steps

### Step 1 — Log into the WCS primary server

**Responsible role:** L2_support

**Instruction:**
Log into the WCS primary server.

**Expected result:**
You are logged into the WCS primary server and can continue to the database access step.

---

### Step 2 — Open the WCS database

**Responsible role:** L2_support

**Instruction:**
Open the WCS database.

**Expected result:**
The WCS database is open and ready for query entry.

---

### Step 3 — Open a new query tab

**Responsible role:** L2_support

**Instruction:**
Open a new query tab by clicking the indicated control.

**Expected result:**
A new query tab opens and is ready for SQL entry.

---

### Step 4 — Paste the documented SQL query into the new tab

**Responsible role:** L2_support

**Instruction:**
Copy and paste the provided SQL query into the newly opened query tab.

**Expected result:**
The query editor contains the documented SQL statement.

---

### Step 5 — Use the documented active AGV error query text

**Responsible role:** L2_support

**Instruction:**
Use the provided query text exactly as documented: SELECT TOP (1000) [Id], [EntityInserted], [EntityLastUpdate], [Name], [Area], [Error], [LastSeen], [SystemErrorDescription], [SystemErrorResolution] FROM [Helix2x_1Prod_Robotics].[dbo].[SystemActiveErrorModel].

**Expected result:**
The query text references the documented fields and the [Helix2x_1Prod_Robotics].[dbo].[SystemActiveErrorModel] table.

---

### Step 6 — Execute the query

**Responsible role:** L2_support

**Instruction:**
Right click on the query and click execute.

**Expected result:**
The query runs and the interface proceeds to display returned results.

---

### Step 7 — Review the results area

**Responsible role:** L2_support

**Instruction:**
Review the results area where the active errors appear.

**Expected result:**
A results area displays the active AGV errors returned by the query.

---

### Step 8 — Check the returned fields in the results

**Responsible role:** L2_support

**Instruction:**
Check the returned fields in the results, including Id, EntityInserted, EntityLastUpdate, Name, Area, Error, LastSeen, SystemErrorDescription, and SystemErrorResolution.

**Expected result:**
The results include the documented identifier, timestamp, area, error, description, and resolution fields.

---

## Success Criteria

- The WCS primary server is accessed successfully.
- The WCS database is opened successfully.
- A new query tab is opened.
- The documented SQL query against [Helix2x_1Prod_Robotics].[dbo].[SystemActiveErrorModel] is entered.
- The query executes successfully.
- The results area displays active AGV error records.
- Returned results include Id, EntityInserted, EntityLastUpdate, Name, Area, Error, LastSeen, SystemErrorDescription, and SystemErrorResolution.

## Failure Conditions

- Access to the WCS primary server is not available.
- Access to the WCS database is not available.
- A new query tab cannot be opened.
- The query cannot be executed.
- The results area does not display returned active errors.
- Expected fields are missing from the returned results.

## Escalation Guidance

- Escalate if access to the WCS primary server or WCS database is not available.
- Escalate if the query cannot be executed or the results area does not display returned active errors.
- Use the output for investigation only; the source does not provide corrective actions for returned errors.

## Missing Details / Known Gaps

- The source does not provide an estimated completion time.
- The source does not specify whether production stop is required.
- The source does not specify whether LOTO is required.
- The source does not provide exact login credentials, server path, or database navigation details.
- The source does not provide interpretation logic for specific returned error values.
- The source does not provide corrective actions for returned active AGV errors.
- The source does not explicitly document the exact UI location of the execute control beyond the instruction to right click on the query and click execute.
