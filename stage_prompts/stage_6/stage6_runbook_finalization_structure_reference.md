# Runbook Finalization Structure Reference

Stage 6 produces one finalized source-specific runbook per candidate. Match this structure exactly. Populate every field from the supplied candidate and packet evidence only.

Stage 6 `metadata.merge_status` must be `source_finalized` (not `new` or `canonical`).

---

## Required Top-Level Sections

Every finalized runbook must cover these concepts in the JSON output (and they should be reflected in review markdown):

1. Runbook header (procedure identity, type, roles, safety flags, validation status)
2. Summary
3. When to use (including explicit "do not use for" cases when supported by source)
4. Roles and responsibilities (when role boundaries are supported by source)
5. Safety and operational notes (source-supported only)
6. Prerequisites (access, system preconditions, external references)
7. Related operational context IDs (from packet only)
8. Visual references / artifact attachments (from packet only)
9. Procedure steps (fully expanded from candidate `rough_steps`)
10. Success criteria
11. Healthy conditions
12. Failure conditions
13. Escalation guidance
14. Commands (empty if source provides none — do not invent)
15. Missing details / known gaps
16. Source refs, image refs, source lineage, source candidate IDs

Incident-derived runbooks may also include `related_event_ids` on the runbook and on individual steps when supported by the packet.

---

## Header Fields

| Field | Requirement |
| --- | --- |
| `procedure_id` | `proc_<slug>_v1` derived from candidate title or `candidate_id` |
| `title` | From candidate |
| `procedure_type` | One of: `operation`, `diagnostic`, `recovery`, `reference` |
| `role_required` | One of: `operator`, `L1_support`, `L2_support`, `L3_support`. Respect the Role / Component Access Matrix appended at runtime (site E-stop only; RMS soft stop L2/L3 only; AVEVA site-only; FORTNA remotes on Zscaler). |
| `supporting_roles` | Subset of allowed roles |
| `support_safe` | Boolean when known from candidate/source |
| `requires_production_stop` | Boolean; omit or null if unknown |
| `requires_loto` | Boolean; omit or null if unknown |
| `estimated_time_minutes` | Integer only if source supports an estimate |
| `validation_status` | `needs_sme_review` for Stage 6 outputs |
| `capability_tags` | List of taxonomy capability IDs (1–3 preferred). Constrained vocab appended at runtime. |
| `access_surface` | List of taxonomy access-surface IDs (e.g. `rms_ui`, `wcs_sql`). How the job is done. |
| `audience_roles` | List of taxonomy audience role IDs; align with `role_required` / access matrix. |
| `failure_pattern_tags` | Optional list of taxonomy failure-pattern IDs when source-supported. |

---

## Step Template

Each `rough_step` from the candidate should become one structured step. Use this shape:

### Step N — `<step title from source>`

- `step_number`: integer
- `title`: concise action title
- `responsible_role`: primary executor role
- `supporting_role`: guide/reviewer role when applicable
- `purpose`: why this step exists
- `instruction`: operator/support-facing instruction on the **live** tool/surface (name SSMS/DB/module/API Dog/HMI — not “training material”)
- `expected_result`: observable live outcome (field/value/state/response/ownership) — not “documented intent captured” or a restatement of the step title
- `healthy_condition`: what "good" looks like on that live surface
- `failure_condition`: what "bad" looks like on that live surface
- `actions`: one or more action objects:

| Field | Requirement |
| --- | --- |
| `action_type` | e.g. `inspection_action`, `physical_inspection`, `physical_action`, `hmi_action`, `hmi_inspection`, `command_action` — use only types justified by source |
| `label` | Short action label |
| `exact_action` | Exact user-facing action from source |
| `role_required` | Allowed role |

- `commands`: terminal/API/service commands only when explicitly present in source evidence; otherwise `[]`
- `screens_or_images`: attach packet artifact IDs with `what_to_look_at`; convert Stage 5 `[Image support needed: ...]` notes into structured refs when matching artifacts exist
- **Do not duplicate images on a step** when the same `artifact_id` is already on the runbook-level `screens_or_images` / `image_refs` / `visual_references`. Keep the runbook-level ref; leave the step's `screens_or_images` empty (or omit that artifact) rather than repeating it.
- `stop_or_escalate_if`: bullet list of stop/escalate triggers supported by source
- `source_evidence`: source refs / quotes / page refs / event refs supporting this step
- `related_event_ids` (incident only): event IDs from packet when applicable

Do not collapse multiple distinct rough steps into one step unless the source clearly treats them as one action.

---

## JSON Output Contract

Return:

```json
{
  "runbook": {}
}
```

The `runbook` object must include:

```json
{
  "procedure_id": "proc_<slug>_v1",
  "candidate_id": "",
  "title": "",
  "procedure_type": "operation",
  "summary": "",
  "role_required": "operator",
  "responsible_role": "operator",
  "supporting_roles": [],
  "capability_tags": ["agv_active_errors"],
  "access_surface": ["rms_ui"],
  "audience_roles": ["operator", "L1_support"],
  "failure_pattern_tags": [],
  "support_safe": true,
  "requires_production_stop": false,
  "requires_loto": false,
  "estimated_time_minutes": null,
  "when_to_use": "",
  "not_for": [],
  "roles_and_responsibilities": [],
  "safety_notes": [],
  "access_or_tools_needed": [],
  "prerequisites": {
    "access_required": [],
    "system_preconditions": [],
    "external_references": []
  },
  "related_context_ids": [],
  "related_event_ids": [],
  "visual_references": [
    {
      "artifact_id": "",
      "description": "",
      "required_level": "required|recommended|optional"
    }
  ],
  "steps": [
    {
      "step_number": 1,
      "title": "",
      "responsible_role": "",
      "supporting_role": "",
      "purpose": "",
      "instruction": "",
      "expected_result": "",
      "healthy_condition": "",
      "failure_condition": "",
      "actions": [
        {
          "action_type": "",
          "label": "",
          "exact_action": "",
          "role_required": ""
        }
      ],
      "commands": [],
      "screens_or_images": [
        {
          "artifact_id": "",
          "what_to_look_at": ""
        }
      ],
      "stop_or_escalate_if": [],
      "source_evidence": [],
      "related_event_ids": []
    }
  ],
  "success_criteria": [],
  "healthy_conditions": [],
  "failure_conditions": [],
  "escalation_guidance": [],
  "commands": [],
  "screens_or_images": [],
  "source_refs": [],
  "image_refs": [],
  "source_candidate_ids": [],
  "source_lineage": [],
  "missing_details": [],
  "validation_status": "needs_sme_review",
  "metadata": {
    "product": "OptiSweep",
    "version": 1,
    "merge_status": "source_finalized",
    "created_by": "stage_6_runbook_finalization",
    "source_id": "",
    "source_type": "",
    "source_title": "",
    "source_version": "",
    "ingestion_batch_id": "",
    "source_quality": "",
    "incident_context": {
      "case_id": "",
      "site": "",
      "site_code": "",
      "site_location": {
        "site_code": "",
        "site_label": "",
        "customer": "",
        "city": "",
        "state": "",
        "country": "",
        "hub_code": "",
        "region_label": ""
      }
    }
  }
}
```

Preserve `site_code` and `site_label` on `source_refs` and step-level
`source_evidence` when they are present on the packet source refs or
`source_package.site_location`.

---

## Grounding Rules

- Use only IDs, text, commands, screens, and outcomes present in the user packet.
- Preserve candidate `source_refs` and `evidence_source_refs`; add step-level evidence where needed.
- If the source does not support a field, leave it empty or note the gap in `missing_details`.
- Do not create playbook nodes, workflow logic, trigger conditions, routing keys, or canonical cross-source merge decisions.
- Do not bind to published/canonical runbook IDs from other sources.
- For training-derived runbooks: write live-support steps on named surfaces (SSMS/DB/API Dog/HMI). Do not use “from the training material” / “record that the source says.” `expected_result` must be observable on the live job.
