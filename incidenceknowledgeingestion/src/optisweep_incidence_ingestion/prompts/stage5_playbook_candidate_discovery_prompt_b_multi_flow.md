# Stage 5 - Incident Playbook Candidate Discovery Variant B

Variant B allows one incident to produce one or more playbook candidates, but
only when clearly separable troubleshooting flows are present.

Use the same playbook boundary rules as the standard Stage 5 playbook
candidate prompt:

- Playbooks describe troubleshooting orchestration, not runbook steps.
- Keep exact how-to instructions in runbooks/procedures.
- Do not create intake, support coordination, communication, routing,
  classification, or case-management nodes.
- Do not infer root cause as fact. You may capture source-supported suspected
  internal patterns as tentative context for future ML, retrieval, and
  knowledge graph enrichment, but these patterns must not be treated as
  confirmed diagnosis or user-facing entry criteria.
- Do not create a finalized canonical playbook.
- Do not bind nodes to production automation.
- Use only the provided incident packet.

## Site Location Rules

Use `source_package.site_location` as authoritative ingestion metadata for which
customer site this case belongs to. Populate `incident_context.site`,
`incident_context.site_code`, and `incident_context.site_location` from that
metadata when present. Preserve `site_code` and `site_label` on source refs.
If evidence location text conflicts with ingestion metadata, note the ambiguity
in `extraction_notes` rather than silently replacing the ingestion site.

## Cardinality Rule

Return one or more `playbook_candidates`.

Return at least one candidate for every incident packet in this test run. If the
incident does not strongly support a playbook, return one low-confidence
candidate that captures the best source-supported troubleshooting shape and
explains why it may not be useful.

Return one candidate when the incident has one dominant troubleshooting flow,
even if it contains multiple phases.

Return multiple candidates only when the incident clearly contains separable
technical troubleshooting flows with distinct troubleshooting goals and
different observable symptom entry patterns.

A separate candidate may be justified when a future user could enter that flow
from a different observable symptom pattern and the incident evidence supports a
distinct troubleshooting goal.

A separate candidate is usually not justified when the second flow only occurs
after completing the first flow, when it is only an exact procedure, or when it
is better represented as a branch, validation gate, or runbook placeholder inside
the main candidate.

Do not split candidates merely because the incident includes multiple tools,
multiple people, multiple messages, several screenshots, several recovery
actions, or multiple follow-up checks.

## Split Test

Create separate playbook candidates only when all of these are true:

1. Each flow has a distinct troubleshooting goal.
2. Each flow could reasonably be selected at runtime from a different observable
   symptom pattern.
3. Each flow has enough source-supported evidence to produce a useful
   lightweight orchestration path.
4. The flows can be reviewed or reused independently.
5. Combining them would obscure the troubleshooting intent.

If the second flow would only happen after executing the first flow, prefer a
branch, validation gate, escalation gate, or runbook placeholder inside the main
candidate.

## Entry Symptoms and Internal Pattern Context

Each playbook candidate must separate user-observable entry symptoms from
internal technical interpretation.

Entry symptoms should describe what an operator, L1 support user, or
customer-facing support person could reasonably observe or say before the root
cause is known.

`support_user_language_examples` must include short operator speech, not just
polished symptom sentences. Prefer phrases callers actually type or say
(for example "AGVs stopped", "AGVs are stopped", "robots stopped",
"nothing is moving", "zone can't get a pair"). Include near-paraphrases that
match sparse turn-1 queries. Stage 10 embeds title + entry symptoms + these
examples only — missing operator speech cannot be recovered by a fatter vector.

Internal patterns are tentative technical interpretations extracted from the
incident evidence. They are useful for later ML training, retrieval improvement,
knowledge graph relationships, and SME review, but they are not final
classifications and should not be required for runtime entry into the playbook.

Do not use internal engineering labels as the main user-facing title unless the
incident evidence shows that support users would actually describe the issue
that way.

The playbook should be entered from observable symptoms and then use diagnostic
decisions, procedure placeholders, escalation gates, and validation gates to
move toward resolution.

This keeps it generic without hardcoding "AGV state mismatch" or
"service crash" everywhere.

## Valid Node Types

Allowed `node_type` values:

- `diagnostic_decision`
- `procedure_reference`
- `escalation_gate`
- `validation_gate`
- `branching_condition`
- `recovery_phase_marker`

Each node should answer:

```text
What troubleshooting direction should we take next?
```

Each node should not answer:

```text
How exactly do I perform the action?
```

## Node Runbook Placeholder Boundary

Every playbook node must include a non-empty `runbook_placeholder`.

This does not mean every node is a recovery action. It means every node must
point to the procedure, diagnostic check, reference aid, validation check,
branching rubric, or escalation handoff procedure needed to execute that node
safely and consistently.

Use the node type to describe the orchestration purpose:

- `diagnostic_decision`: placeholder describes the diagnostic or reference
  procedure needed to collect and interpret the evidence for the decision.
- `branching_condition`: placeholder describes the decision rubric or check
  procedure needed to choose the branch.
- `procedure_reference`: placeholder describes the operational, diagnostic, or
  recovery procedure needed for the action.
- `validation_gate`: placeholder describes the validation or monitoring
  procedure needed to confirm recovery.
- `escalation_gate`: placeholder describes the escalation handoff procedure,
  evidence package, stop criteria, or role-gate procedure needed when the path
  cannot continue safely.
- `recovery_phase_marker`: placeholder describes the phase-entry or phase-exit
  checklist needed to move between recovery phases.

If answering a node requires support to inspect a system, tool, UI, telemetry
source, logs, service state, asset state, task state, queue, mapping, roster,
configuration, operational state, screen, status field, alarm, or visual state,
the node's `runbook_placeholder` must describe that procedure capability.

Do not leave a node with an empty placeholder because a future support user
would still need a runbook to perform the check, interpret the evidence, choose
the branch, validate recovery, or escalate with the right evidence.

The placeholder must name the specific system, tool, component, service, or
log source when the incident evidence supports it. If the incident evidence
names components such as the OptiSweep service, Windows Event Viewer, Windows
Services, RMS, Ignition gateway status page, or another specific tool or
service, the placeholder must name those by name and describe what to inspect
within them — for example, which log view (System vs. Application), event ID
category (Service Control Manager termination events), status field, roster
view, or API endpoint to check. Do not use generic phrases like "approved
support tools" or "fleet management tools" when the incident evidence names
specific tools and components.

The placeholder must not include exact click paths, commands, exact screen
navigation sequences, or invented canonical runbook names.

Good:

```yaml
node_type: diagnostic_decision
intent: Determine whether the robotic control service is in an abnormal state
  that correlates with the site-wide motion stoppage.
runbook_placeholder: >
  Procedure needed to check named service status in Windows Event Viewer
  (System log, Service Control Manager termination events for the specific
  robotic control service) and in Windows Services, and to check the relevant
  RMS or HMI interface for abnormal state indicators such as a blank page or
  connection-lost error message.
```

Good:

```yaml
node_type: diagnostic_decision
intent: Determine whether fleet synchronization state requires correction after
  service recovery.
runbook_placeholder: >
  Procedure needed to inspect the AGV fleet or roster view in RMS for
  out-of-sync, unmapped, or otherwise abnormal-state assets, and to identify
  which specific asset IDs require correction before the site can resume normal
  operation.
```

Good:

```yaml
node_type: validation_gate
intent: Confirm service responsiveness and AGV status after recovery.
runbook_placeholder: >
  Procedure needed to confirm service state in Windows Services, validate AGV
  status through the API endpoint used in this incident (checking HTTP status
  code and returned AGV records), and verify the fleet management view in RMS
  shows the expected AGV roster in a normal state before declaring recovery.
```

Good:

```yaml
node_type: escalation_gate
intent: Stop and escalate if supported recovery does not restore stable
  operation.
runbook_placeholder: >
  Procedure needed to prepare escalation handoff evidence including Event
  Viewer System and Application log screenshots, Windows Services state
  screenshot, RMS fleet view screenshot, API response evidence, and a summary
  of all recovery actions attempted and their outcomes.
```

Weak (too generic — name the specific tools from the incident and what to check
within them):

```yaml
node_type: diagnostic_decision
intent: Determine whether the affected asset or subsystem is in an abnormal state.
runbook_placeholder: Procedure needed to inspect and interpret affected asset or subsystem state in approved support tools.
```

Bad:

```yaml
node_type: diagnostic_decision
intent: Check the support system and decide what is wrong.
runbook_placeholder: ""
```

## Escalation Gate Rule

Use `escalation_gate` only when the playbook should stop or hand off because the
path is unsafe, unauthorized, outside the current role, not source-supported
enough to continue, or unresolved after the available diagnostic, procedure, and
validation path has been attempted.

Do not create an escalation gate merely because the historical incident was
unfamiliar, because support asked someone else for advice, because a bridge or
handoff occurred, or because a higher-tier person participated in the case.
Those are support-coordination facts, not reusable playbook nodes.

If the next action is a check or recovery that an authorized role can perform
with an approved procedure, use `procedure_reference` with `allowed_roles`
instead of `escalation_gate`.

Good escalation gate:

```yaml
node_type: escalation_gate
intent: Stop and escalate if the approved checks do not identify a supported recovery path or validation fails after recovery.
```

Bad escalation gate:

```yaml
node_type: escalation_gate
intent: Escalate because this case was new to support.
```

## Branch Hint Topology Rules

`branch_hints` become executable Stage 8 edges. Incomplete or wrong-polarity
hints will cause the app to skip recovery or loop.

1. Cover every diagnostic / branching node with both an unhealthy-style edge
   (fault/pattern indicated → continue investigation or recovery) and a
   healthy-style edge (fault/pattern not indicated → exit, retriage, or a true
   alternate investigation node).
2. Healthy means leave this path or take an alternate check. Do **not** point
   healthy exits at nodes whose title/intent assumes recovery already happened
   (for example "after service recovery", residual AGV sync after recovery).
3. Post-recovery checks may be reached only from an explicit recovery
   `procedure_reference` / recovery-phase edge whose condition is recovery
   completed (or equivalent). Example: node_5 recovery completed → node_6.
4. Recovery-completed conditions are success/progress edges, not unhealthy.
5. Do not emit self-loops on healthy outcomes unless the label is an intentional
   wait/retry/monitor state.
6. Entry diagnostic nodes must include an explicit next node for the confirmed
   pattern (usually the next diagnostic) and an explicit exit/retriage destination
   when the pattern is not matched.

Good:

```yaml
# From entry diagnostic
- from: node_1
  condition: Confirmed site-wide stoppage / abnormal RMS-HMI presentation
  next: node_2
- from: node_1
  condition: Localized or normal presentation; pattern not matched
  next: ""   # exit / retriage

# From recovery procedure
- from: node_5
  condition: Primary service or gateway recovery completed
  next: node_6   # residual AGV check AFTER recovery
```

Bad:

```yaml
# Healthy/filler exit jumping to a post-recovery residual check
- from: node_1
  condition: Diagnostic check does not indicate the fault condition
  next: node_6
```

## Runbook Placeholder Rule

Every playbook node must use `runbook_placeholder` to describe the supporting
runbook capability needed for that node.

At this discovery stage, do not create or reference canonical runbook IDs. The
runbook linking layer has not been performed yet.

Use a plain-text `runbook_placeholder` that describes the needed procedure
capability at a high level.

The placeholder should describe what procedure is needed and must name the
specific tool, component, or log source when the incident evidence supports it.
It must not describe how to perform the procedure in procedural detail.

Good:

```yaml
node_type: diagnostic_decision
intent: Determine whether the named robotic control service is in an abnormal
  state correlated with the reported site-wide stoppage.
runbook_placeholder: >
  Procedure needed to check the named service status in Windows Event Viewer
  (System log for Service Control Manager termination events) and Windows
  Services, and to inspect the relevant RMS or HMI interface for abnormal
  blank-state or connection-lost indicators.
```

Good:

```yaml
node_type: procedure_reference
intent: Perform approved recovery for the affected service or gateway if
  authorized.
runbook_placeholder: >
  Procedure needed for authorized recovery of the named robotic control service
  or related gateway, including required safety preconditions and role limits.
```

Good:

```yaml
node_type: validation_gate
intent: Validate that the affected workflow has recovered and remains stable.
runbook_placeholder: >
  Procedure needed to confirm service state in Windows Services, validate AGV
  status through the incident-evidenced API endpoint, check the RMS fleet view
  for normal AGV roster state, and verify with the site that automated
  operation has resumed.
```

Bad:

```yaml
runbook_placeholder: Procedure needed for authorized recovery of the source-named service.
```

Bad:

```yaml
steps:
  - Open Windows Services
  - Restart the service
  - Run a command
```

Do not invent runbook IDs, canonical procedure names, or links between
runbooks. Those relationships will be created later by the runbook extraction,
normalization, and linking stages.

## Required JSON

Return JSON only:

```json
{
  "source_id": "",
  "source_type": "incident_case",
  "source_title": "",
  "source_version": "",
  "ingestion_batch_id": "",
  "extraction_mode": "one_or_more_playbook_candidates_when_separable",
  "candidate_count": 1,
  "candidate_count_reason": "",
  "playbook_candidates": [
    {
      "playbook_candidate_id": "playbook_candidate_incident_<case_id>_<short_slug>",
      "title": "",
      "user_facing_summary": "",
      "playbook_goal": "",
      "observed_entry_symptoms": [],
      "negative_or_absent_signals": [],
      "support_user_language_examples": [],
      "tentative_internal_patterns": [],
      "internal_pattern_notes": "",
      "affected_systems_or_components": [],
      "separability_reason": "",
      "confidence": "high | medium | low",
      "confidence_reason": "",
      "nodes": [
        {
          "node_id": "node_1",
          "node_order": 1,
          "node_type": "diagnostic_decision | procedure_reference | escalation_gate | validation_gate | branching_condition | recovery_phase_marker",
          "title": "",
          "intent": "",
          "expected_or_observed_result": "<who observes + source-grounded tool/view when present + healthy / unhealthy / inconclusive signals>",
          "runbook_placeholder": "<plain-text procedure placeholder required for every node>",
          "observed_surfaces": [],
          "source_used_surfaces": [],
          "required_evidence_concepts": [],
          "recommended_diagnostic_surfaces": [],
          "stage8_candidate_surfaces": [],
          "ontology_capabilities": [],
          "backend_observability": [],
          "ontology_gaps": [],
          "healthy_indicators": [],
          "unhealthy_indicators": [],
          "inconclusive_indicators": [],
          "allowed_roles": ["operator | L1_support | L2_support | L3_support"],
          "preferred_audience": ["operator", "L2_support"],
          "stop_or_escalation_note": "",
          "source_supported_description": "",
          "related_artifact_ids": [],
          "related_event_ids": [],
          "source_refs": []
        }
      ],
      "branch_hints": [
        {
          "from_node_id": "",
          "condition_or_signal": "",
          "suggested_next_node_id": "",
          "reason": "",
          "source_refs": []
        }
      ],
      "escalation_gates": [
        {
          "condition_or_signal": "",
          "required_role": "operator | L1_support | L2_support | L3_support",
          "reason": "",
          "source_refs": []
        }
      ],
      "validation_gates": [
        {
          "validation_goal": "",
          "expected_recovery_signal": "",
          "failure_outcome": "",
          "source_refs": []
        }
      ],
      "runbook_placeholders": [
        {
          "needed_procedure": "",
          "why_needed": "",
          "suggested_role": "operator | L1_support | L2_support | L3_support",
          "risk_note": "",
          "source_refs": []
        }
      ],
      "ignored_non_playbook_content": [
        {
          "content_type": "intake | routing | communication | support_coordination | exact_procedure | reference_background | other",
          "example_from_incident": "",
          "reason_ignored": ""
        }
      ],
      "source_refs": [],
      "evidence_source_refs": [],
      "extraction_notes": []
    }
  ],
  "rejected_candidate_splits": [
    {
      "possible_split": "",
      "reason_rejected": "",
      "better_representation": "branch_hint | validation_gate | escalation_gate | runbook_placeholder | ignored_non_playbook_content | not_enough_evidence"
    }
  ]
}
```

## Placeholder Specificity and First-Node Distinctiveness

When the first node in a playbook is a `diagnostic_decision` that confirms the
observable symptom pattern, its `runbook_placeholder` must describe the
**generic** questions to ask the site and the named tools or views to check.
Use "the affected zone" or "the reported robot" rather than hardcoding zone
numbers or robot IDs from one source incident.

Do not embed incident-specific identifiers in reusable node fields, playbook
titles, or `playbook_id` values. Those facts belong in the canonical incident
record, which Stage 8 links to the finalized playbook via `case_id`.

A generic first-node placeholder like the one below will produce nearly
identical first nodes across different prompt variants and gives responders no
actionable guidance:

```text
Procedure needed to collect and interpret site-reported symptoms, affected zone
behavior, and recent robot handling history using approved support tools and
incident questioning guidance.
```

A specific first-node placeholder names the observable state to confirm, the
questions to ask the site, and the named tools or views to check:

```text
Procedure needed to confirm with the site which affected zone is reporting
unable to get a pair, whether AMRs are actively routing to the hospital lane,
and whether the issue began after recent robot replacement or remove/add
activity. In RMS, check the zone pairing view for the affected zone and the
AMR routing display for active hospital diversion.
```

When this prompt produces multiple candidates for an incident, ensure that each
candidate's first node placeholder is distinctive and specific to that
candidate's entry symptom pattern and the tools or views relevant to that flow.
Do not produce identical or near-identical first-node placeholders across
different candidates.

Apply the same specificity standard to all diagnostic, branching, and
validation node placeholders — not only the first node.

## Component and Domain Vocabulary

When writing node placeholders, name a **component or interface** only when the
incident source names it or a readable source artifact visibly shows it. The
following vocabulary is an interpretation aid, not permission to introduce a
surface. Stage 8 links runbooks by domain match. Prefer one primary component
per node.

| Component / interface | Use when the node checks… |
| --- | --- |
| **RMS / fleet status** | Pairing failures, zone balance, fleet-wide faults, robot roster/mapping, AGV locations, active error codes, system-down overview |
| **WCS database / SSMS (read-only)** | Remote L1/L2 corroboration of AGV errors, robot/roster state, dwell/shutdown staging, WcsError/Robotics/SorterSweeper table state — name the **surface**, not SQL text |
| **Hospital HMI / lane UI** | Hospital lane routing, hospital station status, stacklight/alarm indications, hospital workflow diversion |
| **Operator / tipper HMI (VISU)** | Tipper faults, operator station alarms, VISU_IO/VISU_DATA screens, pneumatic/mechanical operator actions |
| **Building / ACB overview HMI** | Building/area overview, bin status, message panel, smalls layout |
| **Ignition gateway** | Gateway health, memory trend, Systems Overview responsiveness, gateway restart validation |
| **OptiSweep / WCS API** | GetAgvStatuses/API responsiveness, WCSWebApplication faults, dependent-service validation after gateway recovery |
| **Windows Event Viewer / services** | Application/System log errors, service crash/recovery (7031, service control manager) |
| **AGV physical recovery / removal** | Remove/add AGV, bump fault recovery, motionless AGV, isolation from active fleet |
| **AVEVA HMI** | Floor/site AVEVA screens only (`operator`); FORTNA has no access |

**Same-capability multi-surface:** Name multiple surfaces only when the incident
source supports each one and they corroborate the same check. Leave
query/table detail to runbooks.

**Cross-domain rule:** Do not combine **unrelated** components in one placeholder
(for example Event Viewer log review + RMS fleet inspection). Split into separate
nodes or keep site-interview portions orchestration-only with no runbook link.

**Good placeholder (surface yes, procedure detail no):**
`Procedure needed to confirm active AGV errors via RMS fleet status and/or WCS/SSMS read-only query (L2 remote)`

**Bad placeholder (SQL detail in playbook):**
`Procedure needed to run SELECT * FROM SystemActiveErrorModel in Helix2x_1Prod_Robotics`

## Expects tags (diagnostic / branching / validation nodes)

For every `diagnostic_decision`, `branching_condition`, and `validation_gate` node, emit
taxonomy IDs (see `docs/ontology/taxonomy/runbook_capability_taxonomy.json`):

| Field | Required | Purpose |
| --- | --- | --- |
| `expects_capability` | Yes (at least one) | Job this node confirms for its healthy/unhealthy branch (full taxonomy; ontology-informed) |
| `expects_surface` | Recommended | How to do this job. Emit only surfaces the node needs; when RMS and SSMS both corroborate, list both as equal weight (RMS is not preferred). |
| `preferred_audience` | Recommended | Who should execute. **RMS ≈ `operator` (+ optional L1); WCS/SSMS ≈ L2/L3.** Dual-surface nodes often use e.g. `["operator", "L2_support"]`. |

### Ontology snippets → expects

Use packet `ontology_snippets` (models, capability cards, surfaces) to author **detailed** nodes — especially `expected_or_observed_result` healthy/unhealthy/inconclusive signals.

1. Ground evidence in ontology tools/views (RMS pages and/or SSMS models such as `SystemDatabaseModel` / `SystemActiveErrorModel`).
2. Emit `expects_*` only when supported by the node job + ontology cards — do not invent tags.
3. **RMS is not preferred over SSMS.** System state and active errors live in SSMS; when both corroborate, name both as equal-weight surfaces.
4. Incident evidence wins on conflicts; do not paste snippet prose into placeholders.
5. For each selected ontology capability, emit an `ontology_capabilities` item with
   `id`, the supplied `support_contract`, and only the relevant evidence.
6. Emit `backend_observability` mappings with `concept`, `surface`, `database`,
   `model`, `fields`, `correlation_keys`, and `freshness_field` when supplied.
7. Treat WCS SQL/SSMS as the default remote read surface whenever a validated
   WCS-backed UI mapping exists. The exception is VPN/connectivity failure.

### Expects rules

1. Pick capabilities from evidence + ontology — full taxonomy, no fixed shortlist.
2. Do not rely on pipeline post-process to fill missing `expects_*`.
3. `procedure_reference` / `escalation_gate` may omit `expects_*`.
4. Follow the appended **Playbook expects_* Guidance**.

## Attainable-evidence contract

For the same node types, `expected_or_observed_result` must state **attainable evidence**, not a vague label:

1. **Who observes** — site/operator vs remote L1/L2 (or either)
2. **Tool / view** — RMS page, WCS/SSMS read-only, Event Viewer, HMI, API, site interview
3. **Healthy signal** — concrete observable
4. **Unhealthy signal** — concrete observable
5. **Inconclusive** — what is missing or ambiguous

Include remote SSMS when the capability is L1/L2-attainable. Escalation for unsupported
database **changes** is not a substitute for naming read-only SSMS diagnostics.

Entry symptoms and playbook titles should describe **generic observable patterns**
(for example "a zone unable to get a pair"), not incident-specific zone numbers,
robot IDs, or site names. Those facts belong in the canonical incident record.

## Role / Component Access Matrix

When assigning `allowed_roles`, `required_role`, or `suggested_role`, follow this matrix.
Do not assign a role that has **No access** to a component the node requires.

**Role meanings:** `operator` = site/customer (not FORTNA). `L1_support` / `L2_support` / `L3_support` = FORTNA remote on Zscaler. **Access** = may interact.

| Component | `operator` (site) | `L1_support` | `L2_support` / `L3_support` |
| --- | --- | --- | --- |
| RMS (fleet / AGV status web) | Access | Access | Access |
| RMS soft stop (pause — **not** E-stop) | — | No access | Access |
| E-stop (physical) | Access | No access | No access |
| OptiSweep / WCS API | No access | Access | Access |
| WCS / Helix DB (SSMS) | No access | Access | Access |
| Event Viewer / Windows Services | No access | Access | Access |
| Ignition gateway | No access | Access | Access |
| Tipper HMI / WebVisu / VISU | Access | Access | Access |
| Hospital HMI / lane UI | Access | Access | Access |
| Building / ACB overview HMI | Access | Access | Access |
| AVEVA HMI | Access | No access | No access |

Hard rules: only `operator` may E-stop; RMS soft stop is L2/L3 only; AVEVA is site-only.

## Safety Rules

1. Return at least one playbook candidate, but mark it low confidence when the
   technical playbook pattern is weak or incomplete.
2. Do not split one troubleshooting flow into multiple candidates unless the
   split test is satisfied.
3. Keep nodes lightweight and non-procedural.
4. Ground source observations in the incident source or a readable source
   artifact. Use the supplied ontology snippets to identify validated
   capabilities, support surfaces, backend mappings, roles, prerequisites, and
   forbidden procedure families. Do not invent ontology IDs or fields.
5. For every node, separate source-observed surfaces and provenance-bearing
   `source_used_surfaces` from ontology-derived
   `recommended_diagnostic_surfaces`, `required_evidence_concepts`, and
   backend mappings. If the ontology cannot establish a mapping, emit a
   specific catalog or mapping gap rather than silently leaving the contract
   ambiguous.
6. Each `source_used_surfaces` item requires `surface`, `provenance`, and
   `source_evidence`. Allowed provenance values are `explicit_source`,
   `strongly_implied_by_source`, and `source_artifact_visible`.
7. Healthy, unhealthy, and inconclusive indicators describe operational state.
   A tool-specific indicator is allowed when the source or supplied ontology
   makes that tool state relevant. For remote support, prefer validated
   read-only WCS SQL/SSMS when the ontology maps the observed UI state to
   backend data. Treat VPN/connectivity failure as the exception; if the
   OptiSweep service is down, include Ignition, host/service, API, and SQL
   evidence paths because site UIs may be unavailable.
8. Do not include SQL statements, SELECT/FROM clauses, table schemas, column
   lists, click-by-click SSMS navigation, exact commands, screen sequences,
   service restart steps, or mutating database/config steps.
9. Do not create support call, bridge call, communication, Salesforce,
   case-management, or intake nodes.
10. Do not create category labels or final issue classifications.
11. Do not invent root cause as fact.
12. Do not invent canonical runbook IDs or runbook relationships.
13. Every node must include a non-empty plain-text `runbook_placeholder`.

## Stage 8 Linking Constraints

Playbook nodes become reusable orchestration templates. Keep incident-specific facts
in the canonical incident record and playbook-level entry context, not embedded in
reusable node decision rubrics.

- Do **not** put specific zone numbers, robot IDs, site names, or "in this incident"
  phrasing in `expected_or_observed_result`, branch `condition_or_signal`, or
  `decision_outcomes`. Use generic observable criteria instead.
- `expected_or_observed_result` should describe attainable evidence: who observes,
  which tool/view (RMS, WCS/SSMS, Event Viewer, HMI, API, site interview), and
  concrete healthy / unhealthy / inconclusive signals — not a vague label and not
  a restatement of what happened in the source incident.
- Do **not** combine unrelated procedure types in one placeholder when they require
  different catalog runbooks (for example site interview + RMS fleet inspection in a
  single node). Split into separate nodes or mark the site-interview portion as
  orchestration-only with no runbook placeholder for the interview itself.
- Name the system/tool domain in placeholders only when the incident source names
  it or a readable source artifact visibly shows it. Avoid vague "approved
  support tools" when the incident names a specific tool. Do not add SSMS
  corroboration when the case evidence showed only RMS/HMI screens; Stage 8
  selects current corroboration separately.
- `branching_condition` nodes that depend on site-reported history should describe a
  decision rubric placeholder, not a fleet diagnostic procedure, unless the branch is
  decided purely from RMS evidence.
- Follow **Branch Hint Topology Rules** above: healthy exits must not skip into
  post-recovery nodes; recovery-completed polarity is success/progress; diagnose
  nodes need both healthy and unhealthy next destinations.
- Use generic `playbook_id` and title patterns without embedded zone numbers, robot
  IDs, or site names. Link incident specifics through `case_id` and canonical record
  metadata, not reusable playbook identifiers.
10. Use placeholders for diagnostic, reference, branching, validation,
    escalation, and recovery procedure capabilities, not only recovery actions.
11. Include placeholders for approved tool, system, screen, status,
    operational-state, or evidence-interpretation checks needed to make
    diagnostic and branching decisions.
12. Do not use escalation gates to represent historical unfamiliarity,
    collaboration, or support handoff.
13. Keep source lineage on every meaningful node.
14. Use `rejected_candidate_splits` to explain likely splits that were
    considered but not emitted.
