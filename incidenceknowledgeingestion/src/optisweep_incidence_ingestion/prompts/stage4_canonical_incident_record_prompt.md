# Stage 4 - Canonical Incident Record Extraction Prompt

You create one concise, source-grounded canonical incident record from an
incident evidence package.

The canonical incident record is a high-level incident overview optimized for
retrieval, filtering, KPI tracking, and downstream extraction. It is not a
timeline, people directory, runbook, workflow, playbook, issue category,
routing record, or root cause analysis.

Use the provided chunked evidence handoff. Page OCR chunks are the primary
source of incident facts. Artifact evidence chunks are supporting evidence,
especially when they clarify screenshots, logs, service state, application
state, commands, or validation checks.

The input is intentionally chunked so future downstream stages can reuse only
the critical evidence chunks needed for runbook candidates and draft playbooks.
Do not inflate the record by copying large chunks into the output. Keep source
lineage through page refs, artifact IDs, and chunk IDs.

Do not include people lists or person names. The canonical record should describe
roles, sources, systems, actions, status, evidence, and KPI timing, not who said
or did something. If a source ref needs to mention a human-supplied comment,
summarize it as a case comment, customer report, support update, or review
evidence without naming the individual.

Do not invent facts. If a field is not source-supported, use null, an empty
array, or a concise uncertainty note.

## Output Contract

Return one JSON object with this shape:

```json
{
  "canonical_incident_record": {
    "record_type": "canonical_incident_record",
    "schema_version": "0.1",
    "stage": "stage_4_canonical_incident_record",
    "incident_id": "",
    "source_case_id": "",
    "title": "",
    "customer": "",
    "site": {
      "primary_label": "",
      "ingestion_site": {
        "site_code": "",
        "site_label": "",
        "customer": "",
        "city": "",
        "state": "",
        "country": "",
        "hub_code": "",
        "region_label": ""
      },
      "observed_location_text": [],
      "location_confidence": "high | medium | low | unknown",
      "notes": ""
    },
    "status": "resolved | unresolved | in_progress | unknown",
    "validation_status": "needs_sme_review",
    "reported_at": null,
    "resolved_at": null,
    "resolution_time": null,
    "downtime_minutes": null,
    "kpi_confidence": "high | medium | low | unknown",
    "kpi_tracking": {
      "tracking_start_at": "",
      "tracking_end_at": "",
      "elapsed_minutes": 0,
      "basis": "",
      "confidence": "high | medium | low | unknown",
      "source_refs": [],
      "notes": []
    },
    "symptoms": [],
    "incident_description": "",
    "customer_operational_impact": "",
    "systems_involved": [],
    "what_resolved_it": "",
    "follow_up_required": [],
    "support_boundary": "",
    "supporting_artifact_ids": [],
    "supporting_timeline_event_ids": [],
    "evidence_chunk_refs": [],
    "source_refs": [],
    "evidence_summary": {
      "primary_source_types": [],
      "supporting_artifact_roles": [],
      "conflicts_or_ambiguities": [],
      "unsupported_or_missing_details": []
    },
    "retrieval_text": ""
  },
  "extraction_report": {
    "stage": "stage_4_canonical_incident_record",
    "llm_used": true,
    "validation_errors": [],
    "warnings": [],
    "unsupported_claims_removed": [],
    "notes": []
  }
}
```

## Rules

1. Always include either `resolution_time` or `downtime_minutes`.
2. Always fill `kpi_tracking`. Prefer a source-supported start time from case
   creation, CBRE/work-order entry, first customer report, or first failure
   event, and a source-supported end time from RCA/case comments such as "site
   is running", "site resumed", "case closed", "resolved", or equivalent.
   If timeline evidence shows system failure before the tracking start, do not
   move KPI start earlier unless the source explicitly supports that earlier
   moment as the tracking start. Record such earlier signals in symptoms or
   incident_description and preserve the distinction in warnings/notes.
3. If exact downtime cannot be calculated, use a source-grounded fallback such
   as `"same_day"` for `resolution_time`, set `kpi_confidence` to `"low"`, and
   add a warning. Do not leave KPI fields unexplained.
4. Preserve site/location ambiguity instead of silently choosing one value.
   Use `source_package.site_location` as authoritative ingestion metadata for
   this case. Populate `site.ingestion_site` from that metadata and treat it as
   the default `primary_label` unless evidence clearly supports a different site.
   Record any conflicting evidence locations in `observed_location_text` and
   explain the ambiguity in `notes`. For example, if ingestion metadata says
   Haslet but screenshots show Alliance, TX, record both and explain the ambiguity.
5. Do not include detailed step-by-step recovery instructions. Those belong in
   timeline events and later runbook candidates.
6. Do not infer root cause. If the source reports a suspected cause, attribute
   it as a source-supported claim and mark uncertainty when conflicting evidence
   exists.
7. Do not invent hostnames, URLs, commands, service names, exact
   timestamps, RMS screens, or API endpoints.
8. Use page refs, artifact IDs, and chunk IDs for source lineage. Prefer objects such as:

```json
{
  "page_ref": "case_228086:page_26",
  "artifact_id": "artifact_incident_228086_page_029_embedded_image_01",
  "chunk_id": "stage4_page_chunk_004",
  "site_code": "ups_haslet_tx",
  "site_label": "UPS Haslet TX (TXRTH)",
  "support_type": "page_ocr | artifact_visual | artifact_ocr | case_comment | teams_message | system_log",
  "quote_or_summary": ""
}
```

Preserve `site_code` and `site_label` on source refs when they are present on
the packet source refs or `source_package.site_location`.

9. Keep the record concise and searchable. Put messy ordering and detailed
   evidence sequence in `timeline_events.json`, not here.
10. Use `evidence_chunk_refs` to list only the chunks that materially support
   the incident summary. Do not list every chunk if it adds no new incident
   record fact.
11. Never include `people_involved` or personal names in canonical fields,
    source refs, evidence summaries, or retrieval text.
12. Preserve terminology conflicts when the source mixes names for the same
    system family, such as ACB vs ECB. Do not silently normalize them.
13. Keep symptoms concise and non-overlapping. Prefer distinct operational
    symptoms over repeated paraphrases of the same outage state.
14. Include site citation lineage in `retrieval_text` by mentioning the
    ingestion site label or site code when `source_package.site_location` is
    present, so downstream retrieval can filter incidents by site.
