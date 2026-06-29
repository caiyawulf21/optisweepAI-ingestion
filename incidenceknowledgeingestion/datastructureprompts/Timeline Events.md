# Good Timeline Events Example — Case 228086

<!--
Stage 4 - Create canonical incident records and timeline.
Example prompt/schema for ordering source-supported incident events from page
OCR, Teams/Salesforce context, and linked enriched artifacts.
-->

## Purpose

This file is an example of a simple incident timeline event output.

Timeline events should preserve what happened, in order, using only source-supported details.

Do not infer root cause.
Do not create workflow logic.
Do not create runbook instructions.
Do not learn patterns from the case.
Do not invent missing timestamps, people, commands, systems, or outcomes.

---

# Incident Timeline Events

```json
{
  "incident_id": "incident_228086",
  "source_case_id": "228086",
  "record_type": "incident_timeline_events",
  "source_package": "Case 228086.docx",
  "timestamp_timezone": "unknown",
  "events": [
    {
      "event_id": "incident_228086_event_001",
      "event_order": 1,
      "timestamp": "2026-02-20T06:36:00",
      "event_type": "system_event",
      "actor_name": "unknown",
      "actor_role": "unknown",
      "summary": "OptiSweep web application faulted.",
      "details": "Source states the web application faulted at 6:36 AM.",
      "systems": [
        "OptiSweep web application"
      ],
      "source_refs": [
        "Optisweep Issue Categories.docx",
        "Case 228086.docx"
      ]
    },
    {
      "event_id": "incident_228086_event_002",
      "event_order": 2,
      "timestamp": "2026-02-20T08:11:00",
      "event_type": "symptom_reported",
      "actor_name": "Kevin Buczek",
      "actor_role": "support",
      "summary": "Gauri reported that 4-6 bots were not moving after a heartbeat issue.",
      "details": "Message states that Gauri had called and that 4-6 bots were currently not moving in various areas after a heartbeat issue.",
      "systems": [
        "AGV fleet"
      ],
      "source_refs": [
        "Case 228086.docx"
      ]
    },
    {
      "event_id": "incident_228086_event_003",
      "event_order": 3,
      "timestamp": "2026-02-20T08:14:00",
      "event_type": "symptom_reported",
      "actor_name": "Kevin Buczek",
      "actor_role": "support",
      "summary": "Site could not remove totes from hospital and question marks were shown on HMI.",
      "details": "Message states they could not remove totes from hospital either, question marks were on HMI, and asks whether Ignition crashed.",
      "systems": [
        "Hospital station",
        "HMI",
        "Ignition"
      ],
      "source_refs": [
        "Case 228086.docx"
      ]
    },
    {
      "event_id": "incident_228086_event_004",
      "event_order": 4,
      "timestamp": "2026-02-20T08:21:00",
      "event_type": "symptom_reported",
      "actor_name": "Jinhao Liu",
      "actor_role": "support",
      "summary": "Site reported nothing was moving with no fault or failed AGVs.",
      "details": "Message states Jinhao was talking with Garrett from site and that Garrett said nothing was moving, but there was no fault or any failed AGVs. A follow-up message states this happened during normal operation.",
      "systems": [
        "AGV fleet"
      ],
      "source_refs": [
        "Case 228086.docx"
      ]
    },
    {
      "event_id": "incident_228086_event_005",
      "event_order": 5,
      "timestamp": "2026-02-20T08:32:00",
      "event_type": "support_coordination",
      "actor_name": "Jinhao Liu",
      "actor_role": "support",
      "summary": "Support was on the technical support hotline and waiting for CBRE while remoting in.",
      "details": "Message states they were still on the tech support hotline and waiting for CBRE while remoting in.",
      "systems": [
        "remote access"
      ],
      "source_refs": [
        "Case 228086.docx"
      ]
    },
    {
      "event_id": "incident_228086_event_006",
      "event_order": 6,
      "timestamp": "2026-02-20T08:44:00",
      "event_type": "support_coordination",
      "actor_name": "Jinhao Liu",
      "actor_role": "support",
      "summary": "Support received CBRE and was trying to verify it.",
      "details": "Message states they got the CBRE and were trying to verify it. The message also asks whether somebody else RDP'd in to take a look.",
      "systems": [
        "CBRE",
        "RDP"
      ],
      "source_refs": [
        "Case 228086.docx"
      ]
    },
    {
      "event_id": "incident_228086_event_007",
      "event_order": 7,
      "timestamp": "2026-02-20T08:45:00",
      "event_type": "support_coordination",
      "actor_name": "Zane Bubb",
      "actor_role": "support",
      "summary": "Zane confirmed he was on the RDP session.",
      "details": "Message states: I am on the RDP.",
      "systems": [
        "RDP"
      ],
      "source_refs": [
        "Case 228086.docx"
      ]
    },
    {
      "event_id": "incident_228086_event_008",
      "event_order": 8,
      "timestamp": "2026-02-20T08:53:00",
      "event_type": "diagnostic_question",
      "actor_name": "Kevin Buczek",
      "actor_role": "support",
      "summary": "Support asked whether anyone could determine if Ignition crashed.",
      "details": "Message asks if anyone was able to quickly determine if Ignition crashed or not.",
      "systems": [
        "Ignition"
      ],
      "source_refs": [
        "Case 228086.docx"
      ]
    },
    {
      "event_id": "incident_228086_event_009",
      "event_order": 9,
      "timestamp": "2026-02-20T09:03:00",
      "event_type": "diagnostic_request",
      "actor_name": "Darrell Halterman",
      "actor_role": "support",
      "summary": "Support requested a 24-hour Ignition server memory snapshot.",
      "details": "Message asks Zane to take a 24-hour snapshot of Ignition Server memory usage to see if it crashed.",
      "systems": [
        "Ignition Server"
      ],
      "source_refs": [
        "Case 228086.docx"
      ]
    },
    {
      "event_id": "incident_228086_event_010",
      "event_order": 10,
      "timestamp": "2026-02-20T09:17:00",
      "event_type": "diagnostic_evidence_shared",
      "actor_name": "Zane Bubb",
      "actor_role": "support",
      "summary": "Memory trend screenshot was shared.",
      "details": "A memory trend image was posted in the chat.",
      "systems": [
        "Ignition Server"
      ],
      "source_refs": [
        "Case 228086.docx"
      ],
      "source_artifacts": [
        "memory_trend_screenshot"
      ]
    },
    {
      "event_id": "incident_228086_event_011",
      "event_order": 11,
      "timestamp": "2026-02-20T09:24:00",
      "event_type": "status_update",
      "actor_name": "Christopher White",
      "actor_role": "support",
      "summary": "Site was finishing bag-out and planned to un-E-stop the system afterward.",
      "details": "Message states the site was currently finishing the bag-out process, support needed to wait for them to finish and un-E-stop the system to continue, and the site said it should be another 10-15 minutes.",
      "systems": [
        "E-stop",
        "bag-out process"
      ],
      "source_refs": [
        "Case 228086.docx"
      ]
    },
    {
      "event_id": "incident_228086_event_012",
      "event_order": 12,
      "timestamp": "2026-02-20T09:24:00",
      "event_type": "diagnostic_note",
      "actor_name": "Michael Langley",
      "actor_role": "support",
      "summary": "Memory trend did not indicate memory caused a crash.",
      "details": "Message states there was no indication that memory caused a crash and that CPU trend could also be checked.",
      "systems": [
        "Ignition Server"
      ],
      "source_refs": [
        "Case 228086.docx"
      ]
    },
    {
      "event_id": "incident_228086_event_013",
      "event_order": 13,
      "timestamp": "2026-02-20T09:42:00",
      "event_type": "support_coordination",
      "actor_name": "Mitchel Flynn",
      "actor_role": "support",
      "summary": "Mitchel requested a bridge with someone onsite.",
      "details": "Message states a bridge was needed with whoever was onsite and that support could help if they E-stopped and did whatever was needed.",
      "systems": [
        "E-stop",
        "support bridge"
      ],
      "source_refs": [
        "Case 228086.docx"
      ]
    },
    {
      "event_id": "incident_228086_event_014",
      "event_order": 14,
      "timestamp": "2026-02-20T09:45:00",
      "event_type": "status_update",
      "actor_name": "Zane Bubb",
      "actor_role": "support",
      "summary": "Site needed to start the tippers.",
      "details": "Message states: They need to start the tippers.",
      "systems": [
        "tippers"
      ],
      "source_refs": [
        "Case 228086.docx"
      ]
    },
    {
      "event_id": "incident_228086_event_015",
      "event_order": 15,
      "timestamp": "2026-02-20T09:52:00",
      "event_type": "diagnostic_note",
      "actor_name": "Mitchel Flynn",
      "actor_role": "support",
      "summary": "System state showed bag-out never started.",
      "details": "Message states: From the system state it never started bag out. A follow-up message says to start a bridge.",
      "systems": [
        "system state",
        "bag-out process",
        "support bridge"
      ],
      "source_refs": [
        "Case 228086.docx"
      ]
    },
    {
      "event_id": "incident_228086_event_016",
      "event_order": 16,
      "timestamp": "2026-02-20T10:04:00",
      "event_type": "support_coordination",
      "actor_name": "Kevin Buczek",
      "actor_role": "support",
      "summary": "Support asked whether the meeting had started with UPS.",
      "details": "Message asks whether it was started with them and includes a UPS contact email reference.",
      "systems": [
        "support bridge"
      ],
      "source_refs": [
        "Case 228086.docx"
      ]
    },
    {
      "event_id": "incident_228086_event_017",
      "event_order": 17,
      "timestamp": "2026-02-20T17:21:00",
      "event_type": "follow_up_procedure_detail",
      "actor_name": "Mitchel Flynn",
      "actor_role": "support",
      "summary": "Mitchel shared restart guidance in case the system needed to be restarted later.",
      "details": "Message states the memory trend was looking better and provides restart guidance: first E-stop the system, restart Ignition using the shown command, wait for Ignition to come back up, verify the OptiSweep service responds using an API dog Get AGV Statuses request, restart OptiSweep if no response is given, confirm by sending another request, then release the E-stop.",
      "systems": [
        "E-stop",
        "Ignition",
        "OptiSweep service",
        "API dog"
      ],
      "source_refs": [
        "Case 228086.docx"
      ],
      "source_artifacts": [
        "memory_trend_screenshot",
        "estop_system_screenshot",
        "ignition_restart_command_screenshot",
        "ignition_gateway_status_screenshot",
        "api_dog_get_agv_statuses_screenshot",
        "windows_services_screenshot"
      ]
    }
  ]
}
```

---

## Notes for Codex / Extraction Agent

This is a good timeline example because it only stores source-supported event data.

The extractor should follow these rules:

1. Every event must have a non-null timestamp.
2. If a source does not provide a timestamp, do not create a timeline event from it.
3. Use the timestamp shown in the source message, case note, RCA entry, or log.
4. Do not infer missing timestamps from nearby messages.
5. Do not infer root cause from the timeline.
6. Do not turn the timeline into a runbook.
7. Do not turn the timeline into a playbook.
8. Keep each event short and factual.
9. Preserve actor name when visible.
10. Use `unknown` only for actor name or role when the source does not show it.
11. Store screenshots, command screenshots, and memory trend images as source artifacts, not inline timeline instructions.
12. Detailed recovery steps should later become runbook candidates only if they are source-supported.

---

## What Does Not Belong In Timeline Events

Do not include:

* ML labels
* issue categories
* routing confidence
* workflow branches
* recommendations
* generalized lessons learned
* inferred root cause
* inferred ownership
* invented timestamps
* invented resolution time
* invented commands
* invented service names
* invented screen names

```
```
