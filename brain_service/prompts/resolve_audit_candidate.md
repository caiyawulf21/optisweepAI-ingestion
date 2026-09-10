You are resolving one audit candidate against the OptiSweep Brain. You
have been given every record the candidate names, in full — not just the
names/ids that caused them to be flagged, but their actual descriptions,
relationships, and evidence. A name match or shared evidence pool is NOT
sufficient grounds to merge on its own; you must find a structural or
relationship-shape reason two records are the same real thing (what is
each one actually connected to, independently of the other?).

Decide exactly one of: MERGE, RETYPE, RECLASSIFY, NOT-A-DUPLICATE, or
NEEDS-HUMAN. If MERGE, name the winner (prefer the more complete,
non-garbled record — never the longer name alone) and specify every
Relationship and payload-embedded id reference that must be rewritten so
nothing dangles (checking Claims' `subject_entity_id`/`object.entity_id`
and Capability's `support_contract` id lists, not just `Relationship`
endpoints — this class of bug has recurred three times in this corpus's
history; do not repeat it). If RETYPE, check whether the new id would
collide with an already-existing record before finalizing — if it would,
your answer is MERGE against that existing record, not a silent
overwrite. RETYPE only ever applies to an `Entity` record whose own
`entity_type` is wrong (e.g. a `state` that should be a `symptom`) — if
the record itself is the wrong KIND (a Claim that should have been an
Entity, or similar), that is RECLASSIFY, not RETYPE; RECLASSIFY is never
auto-applied, so choose it plainly rather than forcing RETYPE onto a
problem RETYPE cannot actually solve. It is a complete, correct answer to
conclude NOT-A-DUPLICATE or NEEDS-HUMAN — do not force a merge or a fix
to make the candidate queue shorter.

Output: your decision, the specific records/fields affected, and your
reasoning citing what each record is actually connected to. If your
decision is RETYPE, `fields_to_rewrite` MUST contain
`{"entity_type": "<the corrected EntityType value, e.g. \"symptom\">"}`
— this is the one piece of information the execution step cannot infer on
its own, and RETYPE cannot be applied without it.
