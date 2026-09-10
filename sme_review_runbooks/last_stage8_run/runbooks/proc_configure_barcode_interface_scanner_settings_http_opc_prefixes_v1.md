# Configure Barcode Interface scanner settings (password, prefixes, HTTP/OPC URLs) for AGV and Hospital control IPs

## Runbook Header

| Field | Value |
| --- | --- |
| Procedure ID | `proc_configure_barcode_interface_scanner_settings_http_opc_prefixes_v1` |
| Procedure Type | `operation` |
| Primary Role | `L1_support` |
| Capability Tags | `gateway_health` |
| Access Surface | `apidog` |
| Audience Roles | `L1_support` |
| Failure Pattern Tags | None |
| Validation Status | `needs_sme_review` |
| Merge Status | `pass_through` |

## Summary

On the Windows laptop used for scanner setup, update the replacement Zebra DS3608-SR scanner’s Barcode Interface settings so tote/location label prefixes match and the HTTP/OPC URLs point to the correct AGV control and Hospital control IP addresses, then save the settings.

## When To Use

Use when a scanner is replaced and the new scanner must be set up so Barcode Interface settings use the correct tote/location prefixes and the correct AGV/Hospital control IP addresses in the HTTP and OPC URL fields.

## Source Procedure References

- proc_configure_barcode_interface_scanner_settings_http_opc_prefixes_v1

## Procedure Steps

### Step 1 — Launch Barcode Interface on the scanner setup laptop

**Responsible role:** L1_support

**Instruction:**
On the Windows laptop used for scanner setup, launch the Barcode Interface application (Barcode Interface.exe).

**Expected result:**
Barcode Interface is open and ready for interaction (scanner setup workflow visible).

---

### Step 2 — Open Settings and enter the default password

**Responsible role:** L1_support

**Instruction:**
In Barcode Interface, click the "settings" button and supply the default password "Opti".

**Expected result:**
The settings panel accepts the password and the settings fields are available for editing.

---

### Step 3 — Verify tote/location label prefixes match

**Responsible role:** L1_support

**Instruction:**
Verify the configured prefixes match the labels on the totes and locations.

**Expected result:**
Prefix values shown in the settings match the tote/location label prefixes you physically verify.

---

### Step 4 — Update HTTP and OPC URLs to correct AGV/Hospital control IPs

**Responsible role:** L1_support

**Instruction:**
Change the URL for both the HTTP and OPC settings so the HTTP URL contains the AGV control IP address and the OPC URL contains the Hospital control IP address.

**Expected result:**
HTTP URL field includes the AGV control IP address; OPC URL field includes the Hospital control IP address.

---

### Step 5 — Save the scanner settings

**Responsible role:** L1_support

**Instruction:**
Save the settings using the "Save Settings" button.

**Expected result:**
Settings are saved (the updated prefix/URL values are committed after clicking "Save Settings").

---

## Success Criteria

- After saving, the Barcode Interface settings reflect prefixes matching tote/location labels.
- After saving, the HTTP URL contains the AGV control IP address and the OPC URL contains the Hospital control IP address.

## Failure Conditions

- Prefixes do not match tote/location labels.
- HTTP/OPC URLs cannot be updated to include the correct AGV control and Hospital control IP addresses.
- Settings do not persist after clicking "Save Settings".

## Escalation Guidance

- If prefixes do not match tote/location labels, stop and escalate.
- If HTTP/OPC URLs cannot be updated to include the correct AGV control and Hospital control IP addresses, stop and escalate.

## Missing Details / Known Gaps

- The packet does not provide the exact field labels/names for the prefix fields, HTTP URL field, and OPC URL field as they appear in the Barcode Interface UI; only the actions and their intent are specified.
