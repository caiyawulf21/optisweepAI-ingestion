# Check Tipper Model Station, Printer, and Tipper Status Fields

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_check_tipper_model_station_printer_and_tipper_status_fields_v1` |
| Title | Check Tipper Model Station, Printer, and Tipper Status Fields |
| Procedure Type | `diagnostic` |
| Primary Role | `L2_support` |
| Supporting Roles | `L3_support` |
| Support Safe | Yes |
| Capability Tags | `tipper_station_fault` |
| Access Surface | `wcs_sql` |
| Audience Roles | `L2_support`, `L3_support` |
| Failure Pattern Tags | `tipper_fault` |
| Validation Status | `needs_sme_review` |
| Merge Status | `source_finalized` |

## Summary

Use the WCS / Helix DB (SSMS) read-only surface to inspect the Sorter Sweeper Database Tipper model for the relevant operator station. Verify the Tipper ID and station association, Printer Name and printer IP when configured, Location ID, and Tipper Status.

## When To Use

Use this diagnostic when support needs to verify the live tipper configuration used by the system, including the station-to-tipper association, printer configuration, location association, or current Tipper Status in the WCS / Helix DB (SSMS).

## Do Not Use For

* Changing printer, location, station, or tipper-status configuration.
* Operating or recovering a tipper through the Tipper HMI / WebVisu / VISU.
* Replacing a live equipment fault investigation with configuration inspection alone.

## Safety And Operational Notes

* Use read-only inspection only. This procedure does not authorize changing printer, location, station, or status configuration.
* A Not Ready or Disabled value is an observed configuration/status condition and requires escalation rather than an in-procedure change.

## Access Or Tools Needed

* WCS / Helix DB (SSMS)
* Sorter Sweeper Database
* Tipper model
* Tipper ID
* Printer Name and printer IP
* Location ID
* Tipper Status

## Related Operational Context

* ctx_training_video_tipper_stations_v1
* ctx_training_video_configuration_tables_v1

## Procedure Steps

### Step 1 — Open the Tipper model in the Sorter Sweeper Database

**Responsible role:** L2_support

**Instruction:**
In the WCS / Helix DB (SSMS), use the read-only view of the Sorter Sweeper Database and locate the Tipper model records for the relevant operator station.

**Expected result:**
The relevant Tipper model record or records are available for inspection in the Sorter Sweeper Database.

**Stop or Escalate If:**

* Escalate to L2/L3 support if the relevant Tipper model record is missing.

---

### Step 2 — Verify Tipper ID and station association

**Responsible role:** L2_support

**Instruction:**
In the live Tipper model record in the WCS / Helix DB (SSMS), inspect the Tipper ID and station association. Confirm the documented left/right representation used for the station.

**Expected result:**
The record identifies a Tipper ID associated with the relevant operator station and shows the applicable left/right representation.

**Stop or Escalate If:**

* Escalate to L2/L3 support if the station or Tipper ID association is inconsistent.

---

### Step 3 — Check printer name and printer IP

**Responsible role:** L2_support

**Instruction:**
In the live Tipper model record in the WCS / Helix DB (SSMS), inspect Printer Name and the associated printer IP. Perform this check when a printer is configured for the tipper.

**Expected result:**
The Tipper model shows the configured Printer Name and associated printer IP when printer configuration is applicable.

**Stop or Escalate If:**

* Escalate to L2/L3 support if printer information is absent when required.

---

### Step 4 — Verify the Location ID

**Responsible role:** L2_support

**Instruction:**
In the live Tipper model record in the WCS / Helix DB (SSMS), inspect the Location ID and compare it with the expected location for the relevant operator station.

**Expected result:**
The Tipper model contains a Location ID that can be compared with the expected station location.

**Stop or Escalate If:**

* Escalate to L2/L3 support if the location association is inconsistent.

---

### Step 5 — Inspect Tipper Status

**Responsible role:** L2_support

**Instruction:**
In the live Tipper model record in the WCS / Helix DB (SSMS), inspect Tipper Status and record whether the value is Ready, Not Ready, or Disabled.

**Expected result:**
The Tipper Status field displays one of the documented values: Ready, Not Ready, or Disabled.

**Stop or Escalate If:**

* Escalate to L2/L3 support if Tipper Status is Not Ready or Disabled.

---

## Success Criteria

* The relevant Tipper model record is located in the WCS / Helix DB (SSMS) Sorter Sweeper Database.
* Tipper ID and station association, including left/right representation, are observable.
* Printer Name and printer IP are observable when a printer is configured for the tipper.
* Location ID is observable and can be compared with the expected station location.
* Tipper Status is observable as Ready, Not Ready, or Disabled, with Ready representing the healthy status for this inspection.

## Failure Conditions

* The Tipper model record is missing.
* Tipper ID, station association, or left/right representation is inconsistent.
* Printer Name or printer IP is absent when required.
* Location ID is missing or inconsistent with the expected station location.
* Tipper Status is Not Ready or Disabled.

## Escalation Guidance

* Escalate to L2/L3 support when the Tipper model record is missing or station, location, or printer associations are inconsistent.
* Escalate to L2/L3 support when Tipper Status is Not Ready or Disabled.
* Do not modify the Tipper model configuration as part of this read-only diagnostic.

## Missing Details / Known Gaps

* The packet does not provide the exact Tipper model table name or SSMS navigation/query needed to locate the record.
* The packet does not provide a site-specific mapping of expected operator-station locations or printer requirements.
* The supplied artifacts do not show a matching Tipper model table; no visual artifact is attached to avoid using unrelated database, API, RMS, or Ignition frames as evidence.
* The source lists Ready, Not Ready, and Disabled but does not define the underlying operational cause or remediation for each status.
* The candidate is based on low-confidence manual extraction and requires SME validation.

## Source Lineage

- Candidate IDs: candidate_training_video_tipper_model_status_mapping
- Source ID: `training_video_day2`
- Source Type: `training_video`
