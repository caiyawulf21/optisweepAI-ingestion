# Good Canonical Incident Record Example — Case 228086

<!--
Stage 4 - Create canonical incident records and timeline.
Example prompt/schema showing how one source-grounded incident summary should
look after Stages 1-2.5 provide source bundle text and enriched artifacts.
-->

## Purpose

This file is an example of a clean canonical incident record.

A canonical incident record should summarize one real incident in a way that is searchable, source-grounded, and useful for support review.

It should not become a runbook, playbook, workflow, or full timeline.

---

# Canonical Incident Record

```json
{
  "incident_id": "incident_228086",
  "source_case_id": "228086",
  "title": "AGVs Not Moving After OptiSweep Web Application Fault",
  "customer": "UPS",
  "site": "Haslet, TX",
  "status": "resolved",
  "validation_status": "needs_sme_review",

  "reported_at": null,
  "resolved_at": null,
  "resolution_time": "same_day",
  "downtime_minutes": null,
  "kpi_confidence": "low",

  "people_involved": [
    {
      "name": null,
      "role": "operator",
      "organization": "site_operations",
      "involvement": "Reported that AGVs were not moving and resumed auto bag-out after recovery."
    },
    {
      "name": null,
      "role": "L2_support_or_L3_support",
      "organization": "support",
      "involvement": "Restarted OptiSweep Windows service and corrected AGV state in RMS."
    },
    {
      "name": null,
      "role": "infrastructure",
      "organization": "infrastructure",
      "involvement": "Required for follow-up on memory usage and log sizing."
    }
  ],

  "symptoms": [
    "AGVs not moving",
    "No fault shown",
    "System appeared to be in standard operation mode",
    "OptiSweep web application faulted"
  ],

  "incident_description": "The site reported that AGVs were not moving even though no fault was shown and the system appeared to be in standard operation mode. The OptiSweep web application faulted. After service recovery, AGVs had to be corrected in RMS before the site could resume auto bag-out.",

  "customer_operational_impact": "AGV movement was interrupted and the site could not continue normal OptiSweep operation until the service was restarted and AGV state was corrected.",

  "systems_involved": [
    "OptiSweep Windows service",
    "OptiSweep web application",
    "RMS",
    "AGV fleet"
  ],

  "what_resolved_it": "Support restarted the OptiSweep Windows service, opened RMS, identified AGVs in incorrect or out-of-sync state, corrected each affected AGV one by one, and the site resumed auto bag-out to complete the sort.",

  "follow_up_required": [
    "Infrastructure follow-up required for memory usage and log sizing.",
    "Original case source should be reviewed for exact service restart steps, RMS screens, commands, screenshots, and timestamps."
  ],

  "support_boundary": "This incident is not operator-resolvable. Operators can report symptoms and resume approved site procedures after recovery. Service restart and RMS correction require approved L2/L3 support access.",

  "source_refs": [
    {
      "source_id": "source_case_228086",
      "source_type": "salesforce_case_or_rca",
      "source_case_id": "228086",
      "notes": "Use original case source as authority when available. Normalized summaries may collapse detailed recovery actions."
    }
  ],

  "retrieval_text": "Case 228086 involved AGVs not moving at UPS Haslet with no fault shown while the system appeared to be in standard operation mode. The OptiSweep web application faulted. Recovery involved restarting the OptiSweep Windows service, opening RMS, correcting AGVs that were in incorrect or out-of-sync state one by one, and having the site resume auto bag-out. The case was resolved, with infrastructure follow-up required for memory usage and log sizing."
}
```

---

## Required KPI Rule

The incident record must include a real `resolution_time` or `downtime_minutes` value.

Do not leave both blank.

If exact timestamps are available from Teams, RCA, Salesforce, or logs, calculate:

```json
{
  "reported_at": "source timestamp",
  "resolved_at": "source timestamp",
  "resolution_time": "calculated duration",
  "downtime_minutes": 123,
  "kpi_confidence": "high"
}
```

If only partial evidence is available, use the best source-grounded value:

```json
{
  "reported_at": null,
  "resolved_at": null,
  "resolution_time": "same_day",
  "downtime_minutes": null,
  "kpi_confidence": "low"
}
```

But the extractor must add a warning to the extraction report when exact downtime cannot be calculated.

---

## What Does Not Belong Here

Do not include:

* issue category
* ML labels
* routing confidence
* workflow branches
* detailed step-by-step runbook instructions
* full timeline events
* invented timestamps
* invented names
* invented service names
* invented commands
* invented RMS screens

Those belong in later pipeline outputs or should be recorded as missing details.

---

## Extraction Agent Instructions

When creating a canonical incident record:

1. Keep the record concise.
2. Use symptoms instead of observed signal taxonomy unless the source clearly supports structured signals.
3. Preserve site, customer, incident description, systems involved, people/roles involved, resolution summary, operational impact, KPI timing, and source references.
4. Always include `resolution_time` or `downtime_minutes`.
5. Calculate downtime from source timestamps when possible.
6. Do not invent timestamps or people.
7. If exact downtime cannot be calculated, use the closest source-grounded value and record a warning in the extraction report.
8. Keep detailed actions in timeline events and runbook candidates, not the canonical incident record.
