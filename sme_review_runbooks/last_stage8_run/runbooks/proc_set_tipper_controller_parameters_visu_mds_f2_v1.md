# Set Tipper Controller Parameters on Operator Station HMI (Visu_MDs F2)

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_set_tipper_controller_parameters_visu_mds_f2_v1` |
| Procedure Type | `operation` |
| Primary Role | `L2_support` |
| Capability Tags | `tipper_station_fault` |
| Access Surface | `tipper_hmi` |
| Audience Roles | `L2_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_smeme_review` |
| Merge Status | `pass_through` |

## Summary

Use the operator station HMI to open the “Visu_MDs” screen (F2) and set the initial controller parameters for each tipper axis. Maintenance or admin login is required to change the settings.

## When To Use

When a tipper component has been replaced and the tipper needs to be re-commissioned by setting the initial controller parameters for each tipper axis.

## Source Procedure References

- proc_set_tipper_controller_parameters_visu_mds_f2_v1

## Procedure Steps

### Step 1 — Navigate to the Visu_MDs screen (F2) on the operator station HMI

**Responsible role:** L2_support

**Instruction:**
On the operator station HMI, navigate to the “Visu_MDs” screen using F2.

**Expected result:**
The “Visu_MDs” screen is open on the operator station HMI.

---

### Step 2 — Confirm maintenance or admin login before changing settings

**Responsible role:** L2_support

**Instruction:**
Confirm you are logged in as maintenance or admin (required to be able to change the settings).

**Expected result:**
The current login level is maintenance or admin, enabling the controller parameter fields/settings to be changed.

---

### Step 3 — Set initial controller parameters for each tipper axis on Visu_MDs

**Responsible role:** L2_support

**Instruction:**
On the Visu_MDs screen, set the initial parameters for each axis of the tippers.

**Expected result:**
The initial controller parameters for each tipper axis are updated on the Visu_MDs screen (i.e., the settings were editable and changes were applied).

---

## Success Criteria

- Visu_MDs (F2) screen is open.
- Maintenance/admin login is confirmed and controller parameter settings are editable.
- Initial controller parameters for each tipper axis are updated on the Visu_MDs screen.

## Failure Conditions

- Visu_MDs screen cannot be accessed.
- Settings cannot be edited because login is not maintenance/admin.
- Axis parameter fields are missing or locked such that initial parameters cannot be set.

## Escalation Guidance

- If you cannot edit the settings, verify you are logged in as maintenance or admin.
- Stop and escalate if the Visu_MDs screen cannot be accessed or if axis parameter fields are missing/locked in a way that prevents setting initial parameters.

## Missing Details / Known Gaps

- The packet does not include the specific field names/controls on the Visu_MDs screen for each axis parameter (only that initial parameters must be set).
