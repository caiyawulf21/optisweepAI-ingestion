# Stage 8 — Playbook Finalization & Runbook Linking

**Mode:** LLM Assisted (retrieval-first; LLM refines links and branches)

## Purpose

Link incident playbook candidates to canonical runbooks from Shared Stage 7 and
finalize playbooks for review and runtime orchestration.

## Inputs

You receive a JSON packet with:

- `case_id`
- `playbook_candidate`
- `branch_hints`
- `node_runbook_candidates` (top retrieval matches per node)
- `linking_policy`

## Rules

0. Preserve the Stage 5 playbook candidate as the workflow authority. Emit one
   finalized node for every input node, preserving its `node_id`, title,
   objective, intent, reasoning, evidence, outcomes, source references, and
   branch meaning. Stage 8 may add enrichment fields but must not rewrite,
   merge, or remove Stage 5 workflow content.
1. Keep the workflow layer separate from the procedure layer. A node explains
   what must be determined, why it matters, what evidence is required, how
   observations are interpreted, and which branch follows. A linked procedure
   explains how evidence is collected.
2. Return procedure references, never embedded runbook bodies. Each reference
   may contain only the procedure ID, title, purpose, required role, link
   confidence, rationale, and match gaps. Do not copy runbook steps, SQL,
   click paths, or images into the playbook node.
3. Keep healthy, unhealthy, and inconclusive indicators visible. Do not invent
   evidence, outcomes, or troubleshooting paths when the catalog does not
   support them; emit a catalog gap instead.
4. Keep source-backed reasoning and source references visible in the finalized
   node. Catalog gaps are first-class output and must state the missing
   reusable capability.
4a. Treat Stage 5 `observed_surfaces` and `source_used_surfaces` as historical
    evidence only. Their presence does not make that surface the preferred
    current support method. Use `required_evidence_concepts` to determine what
    must be diagnosed. Treat `stage8_candidate_surfaces` as advisory only, and
    preserve an empty Stage 5 `recommended_diagnostic_surfaces` unless the
    source explicitly dictated a required surface.
5. Every `diagnostic_decision` node must include an action plan with
   `primary_action`, `performed_by`, `primary_surface`, `evidence_to_collect`,
   healthy/unhealthy/inconclusive interpretations, optional corroboration,
   a single linked primary procedure when available, generated guidance,
   ontology evidence, confidence, and `requires_sme_review`.
   Return these fields directly on the node (or under
   `diagnostic_action_plan`) with the requested types. The pipeline preserves
   the LLM action plan; missing or malformed fields are surfaced for SME
   review and are not silently rewritten.
5a. `procedure_reference` nodes may also set `primary_action`, describing in
    plain workflow terms what the support role does at this step (e.g. "Place
    the site in E-stop, then apply the authorized RMS correction for the
    identified AGV before releasing E-stop."). Do not refer to "this
    procedure," "this runbook," "that specific runbook scope," or any other
    meta-reference to the linked procedure itself -- the reader sees the
    linked procedure directly below the action text, so describing it in the
    third person is redundant and reads oddly. State the action as an
    instruction, not as a description of a document.
6. Prefer evidence sources in this order for remote support when the required
   evidence concept is available on those surfaces and the source does not
   dictate another authoritative surface: WCS/OptiSweep SQL or SSMS read-only
   state, supported API, Windows Services/Event Viewer/host logs, AVEVA or
   another support application, RMS, then site observation. Do not use this
   preference to rewrite Stage 5 indicators or historical evidence.
   Operator nodes should prefer site HMI, AVEVA, scanner, and physical
   observation. Recovery nodes must use the approved action-owning surface.
7. Select at most one primary diagnostic procedure and one distinct optional
   corroboration procedure. Reject capability or surface mismatches, recovery
   procedures on diagnostic nodes, generic tool-access procedures, and
   duplicate evidence paths. Do not ask the support engineer to choose among
   several semantically similar procedures.
7a. "Generic tool-access procedure" means a procedure that only opens a tool
    or surface without checking anything specific (e.g. "open RMS"). It does
    not mean a broad overall-system/fault-summary check. If the node's own
    `suggested_database_checks` or evidence description names a system-fault,
    active-error, or fleet-status concept, and `node_runbook_candidates`
    contains a procedure that reads that same concept (even a broad
    overall-system check, not a narrowly-scoped one), attach it as the
    primary procedure rather than leaving the node unlinked. An imperfect but
    on-topic match is more useful to the support engineer than no linked
    procedure.
7b. `optional_corroboration` must be a JSON array of objects, never an array
    of plain strings. Each entry is an object with at least one key (e.g.
    `{"note": "..."}` or `{"procedure_id": "...", "reason": "..."}`) — do not
    emit `["some corroboration text"]`. If there is nothing to add, emit `[]`.
8. Separate evidence retrieval from diagnosis. A successful query, loaded
   screen, populated grid, or HTTP response means only that evidence retrieval
   succeeded; interpret the returned evidence separately as healthy, unhealthy,
   or inconclusive.
9. Database guidance must use only ontology-validated entities, fields, joins,
   and read-only filters. Any generated SQL must be SELECT-only. If mappings
   are incomplete, provide conceptual guidance and a catalog/ontology gap
   rather than executable SQL.

10. Select runbook IDs only from `node_runbook_candidates` for each node.
11. Never invent `procedure_id` values.
12. Prefer incident-derived runbooks only for `procedure_reference` nodes when within the incident preference margin of the top score.
13. Allow at most one primary and one optional corroboration procedure for a diagnostic node.
14. Use low-confidence links when no strong match exists; document `match_gaps`.
15. Emit explicit `branches[]` on branching nodes, seeded from `branch_hints`.
16. For diagnostic, branching, and validation nodes, emit `decision_outcomes[]` with healthy/unhealthy/inconclusive descriptors.
17. Use `high` link confidence when the selected runbook clearly matches normalized placeholder intent, node type, procedure type, and domain anchor terms.
18. Do not link recovery runbooks to diagnostic or branching nodes unless the node type is `procedure_reference`.
19. Prefer manual or SOP canonical runbooks over training_video sources when both match the node intent within retrieval margin.

20. Select by decision realization first. A runbook must explain how an operator or
    support role can observe the node's healthy, unhealthy, or inconclusive result
    and proceed to the corresponding branch. Use `expected_or_observed_result`,
    branch conditions, `tool_or_view`, runbook healthy/failure conditions, and
    concrete steps before considering surface labels.
21. Preserve a case-local runbook for a `procedure_reference` node when it is in
    the candidate list and its procedure type is compatible. Do not replace a
    case-local recovery procedure with a generic RMS/HMI neighbor merely because
    the latter has a higher lexical score.

## Capability / surface / role linking policy

### Current experiment: ontology-first, capability-soft linking

For the current Stage 8 experiment, do **not** treat `expects_capability`,
`capability_tags`, or their overlap as a hard constraint. They are diagnostic
metadata only. Use the node title, intent, placeholder, expected result,
healthy/unhealthy/inconclusive outcomes, branch hints, and the supplied ontology
snippets as the primary evidence for linking.

`expects_surface` is a hint, not a requirement. Prefer a runbook whose live
surface matches the expected surface, but do not reject a semantically stronger
runbook solely because its surface or capability tags differ. If no runbook
matches the actual evidence path, leave the node unresolved rather than using a
nearest RMS/Aveva neighbor.

The retrieval implementation is running with
`STAGE8_USE_CAPABILITY_TAG_CONSTRAINTS=0` by default. It removes capability IDs
from the embedding query and applies only a small surface/audience hint. The
ontology snippets in the packet are authoritative grounding context for the
LLM's intent judgment.

Use node `expects_surface` and `preferred_audience` as ranking hints together
with runbook `access_surface` and `audience_roles` / `role_required`.
Capability fields may explain a match in the rationale, but must not be used as
an eligibility gate in this experiment. This does not weaken item 2a below:
the backend-vs-UI SQL/SSMS pairing is a structural evidence-completeness
requirement, enforced regardless of capability_tags overlap -- not a
capability-tag eligibility gate.

1. **Use surface corroboration when semantically supported.** If the node names multiple
   live surfaces, link corroborating runbooks only when their intent and evidence path
   match; surface overlap alone is insufficient.
2. **Do not default every `wcs_sql` slot to active AGV error SQL.** Stage 7 has multiple
   WCS/SSMS database procedures (robot location, SystemDatabaseModel lifecycle, robot
   commands, dwell/shutdown staging, SSMS connectivity). Choose the SQL runbook whose
   `capability_tags` / model family match the node's expected capability and title/intent.
   Active-error SQL (`SystemActiveErrorModel`) is appropriate only when the node is
   actually about active AGV errors/faults — not merely because the placeholder mentions
   SSMS boilerplate. For mixed expects (e.g. hospital + pairing + `agv_active_errors`),
   prefer the non-error capability's SQL peer or leave a gap rather than force active-error SQL.
2a. **WCS/SSMS is the ground-truth backend for every operational surface.**
    RMS, Ignition, AVEVA, the hospital HMI, and the WCS API are all interfaces
    reading from or writing to the same underlying WCS SQL (Helix/SSMS)
    databases — they do not hold independent truth. For any diagnostic node
    investigating system state (AGV/robot state, roster or mapping, tote or
    task state, hospital flow, tipper state, sequence or exchange state, zone
    pairing, or validation after a state-changing action), always pair at
    most one RMS/UI evidence check with exactly one WCS/SSMS backend
    evidence check as the authoritative corroborating source — even when the
    RMS/UI check alone looks sufficient. Do not treat "the UI already shows
    the answer" as a reason to omit the SQL/SSMS check for these node
    categories; the backend query is what confirms the UI is not itself
    stale or wrong. This pairing is enforced by the pipeline as a guaranteed
    completion step after your initial link selection, so your job is to
    choose the *best* SQL/SSMS candidate from `node_runbook_candidates` when
    one is named, rather than omitting it.

    Exceptions (do not force this pairing): operator-required-by-source
    nodes, Ignition/OptiSweep/WCS service-health nodes, service-restart
    nodes, gateway-health nodes, and Event Viewer/Windows Services/
    API-responsiveness nodes — these categories are source-supported by a
    different surface, and pairing a SQL check onto them would be a
    fabricated evidence path, not corroboration.
3. **Different roles may support one evidence path.** Example: operator/L1 RMS
   observation plus L2/L3 WCS/SSMS corroboration, but only when the node intent
   requires both.
4. Prefer runbooks whose `audience_roles` / `role_required` intersect `preferred_audience`.
5. Prefer runbooks whose `access_surface` intersects `expects_surface`.
6. Do not use capability overlap or empty overlap as a ranking or eligibility signal
   in this experiment.
7. **Prefer audience-compatible runbooks.** Prefer `audience_roles ∩ preferred_audience`
   (operator / L1 / L2–L3). **RMS (`rms_ui`) is mostly operator** (site), with L1 for remote
   overview triage; **WCS/SSMS (`wcs_sql`) is L2/L3**. Dual-surface nodes may link an
   operator/L1 RMS runbook and an L2/L3 SQL runbook for the same capability. Do not block a
   capability match solely because roles differ when the surface is allowed by `expects_surface`.
8. **Do not substitute a different evidence path** because titles look similar
   (hospital HMI bump screen ≠ AGV active-error roster; tipper VISU ≠ fleet RMS).
9. **Physical / on-floor procedures** (`physical_floor`, grid entry) only when the node
   explicitly needs them — not as remote diagnostic substitutes.
10. Keep playbook↔procedure separation: playbook nodes name the job + surface class;
   SQL statements and click paths stay in runbooks.

## Component–Symptom Linking Hints

The tables below are **advisory only**. They help interpret placeholder intent and
rank candidates from `node_runbook_candidates`. They do **not** override the Rules
above, invent procedure IDs, or force a link when retrieval and type compatibility
disagree. When hints conflict with scores, prefer listed candidates, lower
confidence, or `unresolved`, and document `match_gaps`. Capability/surface/role policy
above outranks lexical similarity to RMS-only wording when tags agree.

Incident-specific zone numbers, robot IDs, and site names belong in the canonical
incident record (`case_id`), not in node outcome rubrics.

### Catalog component families (399 merged runbooks, approximate counts)

| Component domain | ~Runbooks | Anchor terms (placeholder / runbook text) | Coverage note |
| --- | ---: | --- | --- |
| Operator / tipper HMI (VISU) | 151 | `visu_io`, `visu_data`, `visu_mcp`, `operator station`, `tipper`, `tipping station`, `feedrate override`, `pneumatic` | Strong catalog |
| RMS / fleet status | 78 | `overall system RMS`, `AGV status screen`, `map monitor`, `robot roster`, `robot selection`, `error codes`, `zone pairing`, `AGV locations` | Strong catalog |
| OptiSweep / WCS API | 56 | `optisweep`, `GetAgvStatuses`, `WCSWebApplication`, `WCS web app` | Moderate; often paired with Ignition validation |
| AGV physical recovery / removal | 36 | `remove AGV`, `add AGV`, `remove robot`, `bump fault`, `recover AGV`, `motionless`, `out of service` | Moderate |
| Hospital HMI / lane UI | 35 | `hospital HMI`, `hospital lane`, `hospital station`, `stacklight`, `hospital alarm`, `ACB system statistics` | Moderate |
| Teknic / motor / axis | 31 | `teknic`, `motor parameter`, `z-axis`, `axis fault`, `manual axis referencing`, `cable carrier` | Moderate; mechanical subsystems |
| LOTO / safety isolation | 21 | `LOTO`, `lockout`, `tagout`, `shut-off valve`, `energy isolation` | Narrow; usually operator-station scoped |
| Building / ACB overview HMI | 11 | `building overview`, `ACB system overview`, `bin status`, `smalls overview`, `message panel`, `area status` | Moderate |
| Network / connectivity | 12 | `network`, `connectivity`, `M12 connector`, `communication fault`, `IP address` | Sparse; often embedded in other domains |
| Tote / material handling recovery | 6 | `add tote`, `tote recovery`, `exchange fault`, `backfill`, `zone with no empty AGV` | Sparse |
| Ignition gateway | 2 | `Ignition`, `gateway`, `Systems Overview`, `memory trend`, `gateway responsiveness` | **Thin catalog** |
| Windows Event Viewer / services | 0 | `Event Viewer`, `Application log`, `7031`, `service control manager`, `Windows Services` | **Catalog gap** |

### Symptom / failure pattern → component hints

Use the **Primary component(s)** column to interpret placeholder intent. Use
**Secondary / corroboration** when the node explicitly names multiple views. Use
**Avoid mistaking for** when lexical similarity points at the wrong UI family.

| Observable pattern or node intent | Primary component(s) | Secondary / corroboration | Example runbook families | Avoid mistaking for |
| --- | --- | --- | --- | --- |
| Zone cannot get a pair / zone balance failure / empty AGV in zone | RMS / fleet status | Tote / material handling recovery (if exchange/backfill named) | Overall system RMS faults; zone pairing views; AGV locations | Hospital HMI alone; tipper VISU |
| AMRs routing to hospital lane / hospital diversion / all AMRs go to hospital | RMS / fleet status + Hospital HMI / lane UI | AGV physical recovery (if recent add/remove) | Hospital lane status; fleet routing; hospital station stacklight | Ignition; Event Viewer; building overview |
| Robot not mapped / roster abnormal / map vs system presence | RMS / fleet status | AGV physical recovery (if isolation next) | Map monitor; robot roster; distinguish in-system vs in-map | Tipper VISU; hospital IO diagnostics |
| System down / ACB outage / production stoppage (fleet symptom entry) | RMS / fleet status | Building / ACB overview HMI (area status corroboration) | Overall system RMS; active AGV faults; blank RMS access check | Hospital stacklight-only runbooks |
| AGV bump fault / exception 21057/21060 / recover from bump | AGV physical recovery / removal | RMS / fleet status (pre-check) | Bump fault recovery; AGV status before recovery | Infra logs; operator tipper unless bump at station |
| Motionless / faulted AGV on floor / needs physical removal | AGV physical recovery / removal | RMS / fleet status | Remove AGV via API; remove motionless AGV; out-of-service isolation | Bump recovery when node does not mention bump |
| Add / remove / replace robot / recent roster change validation | RMS / fleet status + AGV physical recovery / removal | Hospital HMI (if diversion symptom) | Robot selection; add/remove AGV; mapping validation | Generic building overview |
| Tipper fault / operator station alarm / clink-clearlink / Z-axis at station | Operator / tipper HMI (VISU) | LOTO / safety isolation (if pneumatic/energy work) | Tipping station HMI; VISU_IO diagnostics; axis referencing | RMS fleet overview |
| Hospital stacklight color / hospital HMI IO / hospital station alarm | Hospital HMI / lane UI | RMS (if fleet routing cause suspected) | Hospital HMI IO diagnostics; stacklight interpretation; hospital alarms screen | Tipper VISU; message panel on map monitor |
| Building / area / bin status / smalls layout concern | Building / ACB overview HMI | RMS (if fleet-wide outage also reported) | Building overview; bin statuses; smalls color-coded layout | Hospital lane UI |
| Teknic motor replacement / axis fault / cable carrier / end stop | Teknic / motor / axis | Operator / tipper HMI (VISU) (screen navigation) | Backup Teknic parameters; manual axis referencing; axis fault recovery | AGV fleet removal |
| Tote exchange fault / trailing AGV backfill / add tote back | Tote / material handling recovery | RMS / fleet status | Add tote; exchange fault recovery; zone empty AGV recovery | Generic AGV removal |
| Clustered WCSWebApplication / Application Error in Event Viewer | Windows Event Viewer / services | OptiSweep / WCS API (downstream validation) | *(no catalog runbooks today)* | RMS, hospital HMI, VISU, message panel |
| Ignition crash / gateway slow / memory trend / Systems Overview concern | Ignition gateway | OptiSweep / WCS API (dependent service check) | Restart Ignition + verify GetAgvStatuses | AGV removal; hospital HMI |
| OptiSweep API / GetAgvStatuses not responding / WCS service dependency | OptiSweep / WCS API | Ignition gateway (if gateway recovery preceded) | GetAgvStatuses validation; core OptiSweep component overview | Operator tipper screens |
| Site-reported history / recent handling timeline (branch only) | *(orchestration rubric — often no runbook)* | RMS (only if branch decided from fleet evidence) | Decision rubric placeholders | Fleet inspection runbooks on interview-only branches |
| Symptom pattern confirmation (pairing + hospital + recent robot activity) | RMS / fleet status | Hospital HMI / lane UI (corroboration) | Fleet status + hospital routing views together | Map/system-vs-map reference unless roster/mapping is the explicit check |
| Post-recovery validation / monitoring window / function restored | RMS / fleet status or domain of prior recovery node | Same component used for recovery validation | Validation/monitoring procedures in matching domain | Unrelated reference runbooks |

### How to apply hints during linking

1. Read the node placeholder and identify the **named primary component** first;
   use retrieval scores second.
2. Treat **Secondary / corroboration** as optional second links only when the
   placeholder explicitly names multiple tools/views (Rules 4 and 9 still apply).
3. If the primary component has **thin or zero catalog coverage**, prefer
   `unresolved` or `low` with explicit `match_gaps` — do not substitute an
   unrelated HMI family just because it scored higher lexically.
4. Site-interview or history branches usually need a **decision rubric**, not a
   fleet diagnostic runbook, unless RMS evidence is explicit in the placeholder.
5. Keep `decision_outcomes[]` generic; do not embed incident-specific zone or
   robot identifiers in descriptors. Each outcome must be **attainable evidence**:
   who observes (`observer`: site | remote | site_or_remote), which
   `tool_or_view` (RMS, WCS/SSMS read-only, Event Viewer, HMI, API, site interview),
   and concrete healthy / unhealthy / inconclusive signals. Include remote SSMS
   when the node `expects_surface` includes `wcs_sql` or the placeholder names it.

For long-term structured enrichment (knowledge graph edges, runbook
`checks_component` metadata), see
[Stage 8 Playbook Finalization — Future Design Considerations](../../docs/design_decisions/stage_8_playbook_finalization.md#future-design-considerations-knowledge-graph-component-enrichment).

## Required JSON Output

```json
{
  "playbook_id": "",
  "nodes": [
    {
      "node_id": "",
      "primary_action": "",
      "performed_by": "",
      "primary_surface": "",
      "evidence_to_collect": [],
      "healthy_interpretation": "",
      "unhealthy_interpretation": "",
      "inconclusive_interpretation": "",
      "optional_corroboration": [
        {"note": "If active errors are suspected, corroborate with SSMS/API evidence before escalating."}
      ],
      "linked_primary_procedure": null,
      "generated_guidance": "",
      "ontology_evidence": [],
      "confidence": "high | medium | low | unresolved",
      "requires_sme_review": true,
      "query_mode": "none | validated_template | ontology_generated_read_only | conceptual_inspection_only",
      "evidence_retrieval_success": "",
      "diagnostic_interpretation": "",
      "runbook_links": [
        {
          "procedure_id": "",
          "link_confidence": "high | medium | low | unresolved",
          "link_rationale": "",
          "match_gaps": [],
          "preferred_incident_source": false
        }
      ],
      "decision_outcomes": [
        {
          "outcome_label": "healthy | unhealthy | inconclusive | escalate",
          "descriptor": "",
          "observable_signal": "",
          "observer": "site | remote | site_or_remote",
          "tool_or_view": "RMS / AGV status UI | WCS/SSMS (read-only) | ...",
          "source": "runbook_healthy_condition | runbook_step | playbook_expected_result",
          "linked_runbook_id": "",
          "linked_step_number": null,
          "next_node_id": ""
        }
      ],
      "branches": [
        {
          "branch_id": "",
          "condition_label": "",
          "condition_descriptor": "",
          "outcome": "healthy | unhealthy | inconclusive | escalate",
          "next_node_id": "",
          "source_branch_hint_ids": [],
          "linked_runbook_step_ref": "",
          "source_refs": []
        }
      ]
    }
  ],
  "branches": []
}
```

Return one entry in `nodes` for every playbook node. Preserve all node IDs.
