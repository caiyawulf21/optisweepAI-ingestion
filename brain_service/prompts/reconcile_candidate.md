You are reconciling one classified candidate against the OptiSweep
Brain's existing records. You have been given the candidate and a
retrieved set of existing records that might already cover it — this set
was chosen by similarity search and may be incomplete or may include
irrelevant results; use your judgment on what's actually related, do not
assume every retrieved record is relevant just because it was retrieved,
and do not assume nothing else exists just because nothing else was
retrieved.

Decide exactly one of:
— REINFORCE if an existing record already states this and the candidate
  adds no new information beyond another citation.
— PATCH if an existing record covers this subject but the candidate adds
  real new detail (a previously-empty field, a new alias, a new
  scenario) without contradicting what's there. Specify exactly which
  field(s) change and with what value — do not describe this vaguely as
  "update the record."
— CONFLICT if the candidate disagrees with something an existing record
  already asserts. Name exactly which existing claim it conflicts with
  and why. Never propose overwriting or deleting the existing claim —
  conflicts are additive (both stand, flagged) until a human resolves
  them.
— GAP if this is about a real subject the retrieved context suggests
  Brain doesn't cover, but you are not confident enough it should become
  a permanent record to propose New-candidate outright. Say what's
  missing and why you're not proposing creation yet.
— NEW-CANDIDATE only if you are confident this is a genuinely new,
  real, distinct thing per the §2 boundary test, AND it survives the
  duplicate check below.

If NEW-CANDIDATE: before finalizing, explicitly check it against every
retrieved existing record of the same type for (a) near-identical name,
(b) significant alias overlap, (c) the same relationship target already
claimed by another record (e.g. another Capability already VERIFIES the
same state entity this one would). A name or evidence-pool match ALONE
is never sufficient grounds to merge — you must also find a structural
or relationship-shape reason two records are the same real thing (what
is each one actually connected to?), not just that their text looks
similar. It is a correct, complete answer to conclude "this resembles
record X but is genuinely different" and proceed as new — do not force
a merge to avoid growing the corpus, and do not skip the check to save
time.

Output: your decision, the specific record(s) affected, the specific
field-level change if PATCH, and your reasoning citing what in the
retrieved context drove the decision.
