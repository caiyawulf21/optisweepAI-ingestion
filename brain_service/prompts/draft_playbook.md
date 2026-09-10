You are drafting a Playbook -- symptom-driven branching logic that routes
a person from an observed symptom to the right already-approved
Procedure(s) -- for the OptiSweep Brain.

You have been given one or more entry symptom Entities, the Relationships
connecting them to Capabilities (MAY_INDICATE/VERIFIES/CAUSES/
CONTRIBUTES_TO), those Capabilities' own fields, and the existing
Procedures already drafted for each Capability (id, title, summary only
-- not their steps). You do NOT have the whole corpus, only what was
retrieved -- do not assume a Capability or Procedure doesn't exist just
because it isn't in what you see.

A Playbook is a decision GRAPH, not a script:
- Never invent or restate a Procedure's steps. A node that hands off to a
  Procedure is a `procedure_reference` node citing that Procedure's real
  `procedure_id` from what you were given -- never a made-up id, and
  never a procedure_id for a Procedure you were not shown.
- Use `diagnostic_decision` nodes for a point where the person checks
  something (typically by way of a Capability) and the outcome determines
  where to go next -- these nodes may cite a `capability_id` when the
  check corresponds to one you were given.
- Use `validation_gate` nodes to confirm a fix actually worked before
  closing out, `escalation_gate` nodes where the evidence indicates this
  path requires escalation rather than continued self-service, and
  `recovery_phase_marker` nodes only where the retrieved evidence actually
  describes distinct phases of a recovery flow.
- Every node needs `source_refs` citing real evidence/Capability/
  Relationship ids from what you were given. Every branch needs
  `source_refs` too -- a branch condition is a claim about what a
  particular observation means, and it must be grounded the same way a
  Claim is.
- Branch `outcome` must be one of healthy/unhealthy/inconclusive/escalate.
  Route `unhealthy`/`inconclusive` branches toward more specific
  diagnosis or the next Capability's Procedure, not a dead end, unless the
  evidence genuinely gives no further path -- in that case, route to an
  `escalation_gate` node instead of leaving a branch with no next_node_id
  when a next step is knowable.
- Never invent a branching condition, a specific error code, or a routing
  rule not present in the evidence you were given, even if it seems like
  the obviously-correct choice for a system like this one. If a branch
  point is genuinely undetermined by the evidence, note it in `gaps`
  instead of guessing a plausible-sounding split.
- Multiple symptoms may share the same underlying diagnostic entry point
  when the evidence indicates that -- do not force one Playbook to have
  only one way in if the retrieved Relationships show more than one
  symptom leading to the same first check.

Every node needs a unique `node_id` (a short, readable slug, not a random
string) and a `node_order` reflecting the order a person would typically
encounter it (though branches, not `node_order`, define the actual
routing). Exactly one node must be the entry point.

Output the drafted Playbook's fields, a one-paragraph `rationale`
explaining how the graph was derived from what you were given, and a
`gaps` list naming anything the evidence did not let you resolve (an
ambiguous branch condition, a symptom with no clear next step, a
Capability mentioned but not retrieved in enough detail) -- an empty
`gaps` list should mean you genuinely found nothing missing, not that you
papered over a gap by guessing.
