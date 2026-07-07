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

1. Select runbook IDs only from `node_runbook_candidates` for each node.
2. Never invent `procedure_id` values.
3. Prefer incident-derived runbooks only for `procedure_reference` nodes when within the incident preference margin of the top score.
4. Allow up to `linking_policy.max_runbooks_per_node` IDs only when the placeholder clearly spans multiple distinct procedures (compound language and separate domain anchors).
5. Use low-confidence links when no strong match exists; document `match_gaps`.
6. Emit explicit `branches[]` on branching nodes, seeded from `branch_hints`.
7. For diagnostic, branching, and validation nodes, emit `decision_outcomes[]` with healthy/unhealthy/inconclusive descriptors.
8. Use `high` link confidence when the selected runbook clearly matches normalized placeholder intent, node type, procedure type, and domain anchor terms.
9. Do not link recovery runbooks to diagnostic or branching nodes unless the node type is `procedure_reference`.
10. Prefer manual or SOP canonical runbooks over training_video sources when both match the node intent within retrieval margin.

## Required JSON Output

```json
{
  "playbook_id": "",
  "nodes": [
    {
      "node_id": "",
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
