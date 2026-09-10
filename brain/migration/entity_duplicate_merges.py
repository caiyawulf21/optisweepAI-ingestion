"""Hand-judged entity merge pairs, found via the identical-source_refs +
name-overlap signal reported in the "Duplicate & Thin Entity Report"
artifact (2026-09-01) and confirmed by reading each pair's actual cited
evidence text and relationships (2026-09-02) — not merged on the report's
signal alone, since that signal is known-weak on this corpus (see
`BRAIN_BUILD_PROCESS.md` §6.8: 41 groups shared identical source_refs, most
were false alarms, e.g. 27 distinct WCS API endpoints sharing one evidence
pool, or "AGVs with totes" / "AGVs without totes" being opposite states not
duplicates).

Every pair below shares a specific, repeating root cause distinct from the
report's general signal: a `component` entity built from a context record's
own subject, and a bare, empty-description `system` entity built from that
SAME context record's `applies_to` self-reference to its own subject —
i.e. the migration created a component describing "X" and a system entity
literally named "X" (or a trivial rephrasing of it) with no independent
content of its own. Confirmed per-pair by reading the cited evidence text:
each system-typed loser has zero description, zero payload, and its only
relationships are the same `applies_to` link (and duplicate evidence
`supports` edges) back to the very component it was extracted alongside —
there is no second, independent fact about a broader "system" here, just
one fact named twice.

`entity:component:barcode_interface_application` is a 3-way instance of the
same pattern: one rich component plus two bare system echoes from two
different context records that both happened to reference it.

Each entry: (winner_id, [loser_id, ...]). The winner is always the richer,
already-populated record (has a real description/aliases); the loser(s)
are the bare `system` echoes. Applied by
`apply_entity_duplicate_merges.py`.

**`entity:component:database_walkthrough` / `entity:system:database_walkthrough_training_slide`**
added during the §6.12 re-judge pass (a full-corpus scan for the same
bare-echo shape, not limited to the original 7 reported pairs): both exist
purely to record that a training video segment is titled "Database
Walkthrough" — same `applies_to` parent
(`entity:system:fortna_optisweep_training_day_2`), same 2 supported
runbook procedures, near-identical evidence citations. Textbook instance of
this file's pattern.

**A second, distinct duplicate mechanism found in the same §6.12 sweep**:
casing/spacing collisions, not `applies_to` echoes. `entity_id()` slugifies
the entity's `name` — so a database/API/table referenced once as
"GeekAgv" (PascalCase, from a diagram or code reference) and once as
"geek_agv" (lowercase-with-underscore, from spoken/transcript text)
produces two DIFFERENT ids for the same real thing, since slugification
doesn't normalize case or word-boundary style. Found by grouping all
entities of the same `entity_type` by a fully-normalized name
(lowercased, non-alphanumeric stripped) and looking for groups of 2+ — 7
such pairs exist corpus-wide. Unlike the bare-echo pattern, THIS pattern
has no reliable "richer side always wins" rule: which side accumulated the
real relationships/refs depends on which spelling happened to get used
more in the source material, not on data quality. Each pair judged
individually by reading its actual relationships:
- `entity:database:geek_agv` / `entity:database:geekagv`: `geek_agv` (5
  refs) carries the real `contains` relationships to 2 database_table
  entities; `geekagv` (1 ref) carries only the description. Winner:
  `geek_agv` (structurally load-bearing), absorbing `geekagv`'s
  description.
- `entity:database:opc_comms` / `entity:database:opccomms`: same shape —
  `opc_comms` (8 refs) carries the real `contains` relationships;
  `opccomms` (2 refs) carries only the description. Winner: `opc_comms`.
- `entity:database:sorter_sweeper` / `entity:database:sortersweeper`: same
  shape — `sorter_sweeper` (42 refs) carries all 24 `contains`
  relationships to its database_table entities; `sortersweeper` (1 ref)
  carries only the description. Winner: `sorter_sweeper`.
- `entity:system:location_dwell_activity` / `entity:system:locationdwellactivity`:
  both describe the same real `LocationDwellActivity` archive table from
  two different moments in the same training video, with genuinely
  complementary content (one explains what dwell time means, the other
  lists the table's actual field names) — confirmed by reading both
  evidence texts, not assumed from the name match alone. Winner:
  `location_dwell_activity` (fuller initial description), absorbing the
  field-list detail from `locationdwellactivity`.

**A fifth pattern, found during the 2026-09-02/03 operational-source
re-audit, applying entity_type_corrections.py first**: retyping an entity
sometimes produces a same-name, same-entity_type collision with an
already-existing, correctly-typed record — two independently-created
records with the IDENTICAL name but DIFFERENT entity_type (only possible
because entity_id() is type-prefixed, so they never collided as ids until
one was retyped). `apply_entity_type_corrections.py` handles this
automatically via `merge_record()` at retype time — it is not a manual
entry in this file — but two of the entities added below
(`system_active_error_model`/`system_error_activity_model`) are a related
but distinct case: after retyping `state` -> `database_table`, they land
on a NEW id that collides with an ALREADY-EXISTING, richer, independently-
created `database_table` sibling that was never a type-correction target
itself (`entity:database_table:systemactiveerrormodel` /
`entity:database_table:systemerroractivitymodel`, both pre-existing,
field-level-detailed records). That collision is NOT automatic (different
raw names: "System Active Error model" vs. "SystemActiveErrorModel"), so
it needs its own entry here, applied after entity_type_corrections.py runs
(see BRAIN_BUILD_PROCESS.md's rebuild order).

Two more entries below are the ordinary same-source-content-twice pattern
(a terse extraction pass and a fuller one hitting the identical manual
section) — not the retype/collision pattern, just confirmed the normal way
(read both descriptions, same E-stop -> remove -> reset procedure verbatim
in both, different context_ctx_manual_troubleshooting_* vs.
context_ctx_manual_* evidence refs from two separate extraction passes).

NOT included (genuine cross-source duplicates and boundary issues,
deliberately deferred to their own dedicated review rather than folded
into either merge pattern above):
- `entity:component:tote_exchange_thresholds` (from the manual) vs.
  `entity:component:tote_exchange_threshold_categories` (from training
  video day1) — both real, independently-sourced, non-bare component
  records describing the same real screen from two different sources.
- `entity:ui_screen:overall_system_agv_status_page` vs.
  `entity:state:overall_system_agv_status_page` (found during §6.12): the
  `state`-typed one is not a bare echo — it has its own applies_to targets,
  a fact beyond the page title ("this page will show the current status"),
  and independently supports 3 runbook procedures. Also mistyped
  (`state` for what is actually a `ui_screen`, per the boundary in
  `AGENT_DESIGN_NOTES.md` §2 — a page is not itself a state, though its
  contents can describe one), which a plain merge doesn't address on its
  own.
- `entity:component:exchangesortersidezone` / `entity:component:exchange_sorter_side_zone`
  (found in the casing-collision sweep, but NOT merged like the 4 above):
  `exchangesortersidezone` (38 refs) is the identity used by `apidog`/
  `wcs_api` `uses` relationships and `supports` a capability; but
  `exchange_sorter_side_zone` (1 ref, has a real description) is ALSO
  independently wired into 20+ real runbook-procedure `supports`
  relationships from training_video_day2 — not a bare echo, a second
  legitimate record. Needs the same cross-source-duplicate review as the
  `tote_exchange_thresholds` pair above, not a casing-collision merge.
- `entity:component:initializetote` / `entity:component:initialize_tote`:
  same reasoning — `initializetote` (38 refs, used by `apidog`) and
  `initialize_tote` (79 refs, used by `aveva_hmi`) are both real,
  independently-cited references to the same underlying operation from two
  different systems (Apidog vs. Aveva HMI), not a bare echo of one
  another.
- `entity:system:close_out` / `entity:system:closeout`: reading both
  evidence texts shows these are not quite the same thing even though the
  names collide — `close_out` (day1) describes the closeout ACTION/concept
  ("closes all chutes and exchanges totes with items"), while `closeout`
  (day2) is a STATE FIELD tracked on the system state model (one of
  several state values the system tracks). Both are currently typed
  `system`, which is arguably wrong for both (the state field looks more
  like `state`; the action concept doesn't cleanly fit `system` either) —
  a naming collision sitting on top of an unresolved type-boundary
  question, not a same-thing duplicate. Left open for a dedicated pass
  rather than merged or retyped without further review.
"""

MERGES: dict[str, list[str]] = {
    "entity:component:get_zone_configuration_function": [
        "entity:system:get_zone_configuration",
    ],
    "entity:component:update_zone_configuration_function": [
        "entity:system:update_zone_configuration",
    ],
    "entity:component:tote_exchange_threshold_categories": [
        "entity:system:tote_exchange_thresholds",
    ],
    "entity:component:tote_exchange_method_options": [
        "entity:system:tote_exchange_method",
    ],
    "entity:component:shutdown_staging_database_model": [
        "entity:system:shutdown_staging_table",
    ],
    "entity:component:sorter_side_charger_assignment": [
        "entity:system:sorter_side_charger_mapping",
    ],
    "entity:component:barcode_interface_application": [
        "entity:system:barcode_interface_application",
        "entity:system:barcode_interface_exe",
    ],
    "entity:component:database_walkthrough": [
        "entity:system:database_walkthrough_training_slide",
    ],
    "entity:database:geek_agv": [
        "entity:database:geekagv",
    ],
    "entity:database:opc_comms": [
        "entity:database:opccomms",
    ],
    "entity:database:sorter_sweeper": [
        "entity:database:sortersweeper",
    ],
    "entity:system:location_dwell_activity": [
        "entity:system:locationdwellactivity",
    ],
    # --- Found 2026-09-02/03 re-audit: post-retype collision with an
    # already-existing, richer database_table sibling (see docstring above)
    "entity:database_table:systemactiveerrormodel": [
        "entity:database_table:system_active_error_model",
    ],
    "entity:database_table:systemerroractivitymodel": [
        "entity:database_table:system_error_activity_model",
    ],
    # --- Found 2026-09-02/03 re-audit: ordinary same-content-twice pattern
    # (terse + full extraction of the identical manual procedure)
    "entity:component:obstruction_or_parcel_on_floor_troubleshooting": [
        "entity:component:obstruction_parcel_on_floor_troubleshooting",
    ],
    "entity:component:agv_motionless_on_floor_fault_troubleshooting": [
        "entity:component:agv_motionless_on_floor_troubleshooting",
    ],
}
