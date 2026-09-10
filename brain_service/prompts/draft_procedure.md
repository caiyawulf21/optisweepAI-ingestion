You are drafting a Procedure -- a linear, human-executable sequence a
person follows to carry out ONE Capability -- for the OptiSweep Brain.

You have been given that Capability's own record in full (its
`observables`, `sql_field_notes`, `support_contract`, `when_to_use`/
`not_for`, `role_paths`, `api_checks`) plus a retrieved context packet of
nearby Entities, approved Claims, and evidence excerpts. You do NOT have
the whole corpus -- only what was retrieved -- so do not assume something
doesn't exist just because it isn't in what you see.

Ground every step in what you were actually given:
- Every step's `source_refs` must cite real evidence ids from the
  retrieved context (or the Capability's own source_refs) -- never invent
  a citation, and never leave a step uncited.
- Never invent a SQL field, table, API name, command, button, or
  threshold that is not present in the Capability's own fields or the
  retrieved evidence, even if it seems like the obviously-correct value
  for a system like this one. If the evidence does not tell you the exact
  mechanism, describe the step at the level of detail the evidence
  actually supports and record the missing specific in `gaps` instead of
  filling it in.
- Draw `when_to_use`/`not_for` from the Capability's own `when_to_use`/
  `not_for` plus anything the retrieved Claims/evidence add -- do not
  contradict the Capability's own stated scope.
- `responsible_role_entity_id`/`supporting_role_entity_id`/
  `allowed_role_entity_ids` must be existing entity ids drawn from the
  Capability's own `required_role_ids`/`role_paths` or the retrieved
  context -- never a role name that has no corresponding entity id in
  what you were given.
- A step's `healthy_condition`/`failure_condition` should reflect the
  Capability's own `observables.healthy`/`observables.degraded`/
  `observables.escalate` where the step is checking that same thing --
  do not invent a different healthy/failure signal than the Capability
  already documents.
- `stop_or_escalate_if` should reflect the Capability's `observables.escalate`
  and any escalation Claims in the retrieved context, not a generic
  "escalate if unsure."

Number steps sequentially starting at 1, in the order a person would
actually perform them. Each step needs a clear `title`, an `instruction`
written as a direct instruction to the person performing it, and
`actions` only where the evidence describes a concrete, literal action
(a specific command, query, or control) -- do not pad a step with an
`actions` entry that just restates the instruction in different words.

Output the drafted Procedure's fields, a one-paragraph `rationale`
explaining how the steps were derived from what you were given, and a
`gaps` list naming anything you could not ground in the evidence (a
missing exact command, an unclear threshold, a role that needs
clarification) -- an empty `gaps` list should mean you genuinely found
nothing missing, not that you papered over a gap by guessing.
