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
runbook_ref: restart_optisweep_ignition_service_v1
fallback_if_missing_runbook: create_runbook_gap
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
          "expected_or_observed_result": "",
          "runbook_placeholder": "<plain-text procedure placeholder required for every node>",
          "allowed_roles": ["operator | L1_support | L2_support | L3_support"],
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
observable symptom pattern, its `runbook_placeholder` must describe specific
questions to ask the site and specific tools or views to check — not a generic
"procedure needed to collect and interpret site-reported symptoms" description.

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
Procedure needed to confirm with the site which specific zone is reporting
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

## Safety Rules

1. Return at least one playbook candidate, but mark it low confidence when the
   technical playbook pattern is weak or incomplete.
2. Do not split one troubleshooting flow into multiple candidates unless the
   split test is satisfied.
3. Keep nodes lightweight and non-procedural.
4. Do not include exact commands, screen sequences, click paths, SQL, service
   restart steps, or tool navigation steps.
5. Do not create support call, bridge call, communication, Salesforce,
   case-management, or intake nodes.
6. Do not create category labels or final issue classifications.
7. Do not invent root cause as fact.
8. Do not invent canonical runbook IDs or runbook relationships.
9. Every node must include a non-empty plain-text `runbook_placeholder`.
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
