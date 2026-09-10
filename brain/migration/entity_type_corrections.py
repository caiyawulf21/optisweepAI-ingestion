"""Hand-judged entity_type corrections — a category-confusion audit pass
distinct from (and complementary to) the capability state-vs-action fix
(capability_state_pairings.py) and the near-duplicate merges
(entity_duplicate_merges.py). Found during the operational-source re-audit
(2026-09-02/03) by reading a full, representative sample of the `symptom`
and `state` entity_type buckets directly — not by any keyword rule.

Two distinct sub-patterns found, both retyped the same way (change
entity_type, let the id regenerate, since entity_id() is
type-prefixed):

1. **Reference/data-description content mistyped as `symptom`.** A
   `symptom` should be an anomaly/problem condition — something wrong. Six
   entities instead describe neutral facts: a pointer to external
   documentation, a database model's stored contents, normal (non-anomalous)
   API interaction patterns, a verification action's context. None of these
   describe something wrong with the system; they describe what a thing IS
   or CONTAINS. Corrected to `component` (a real, look-up-able thing that
   doesn't fit a more specific type).

2. **Recovery-procedure descriptions mistyped as `symptom`.** A `symptom`
   entity's own description should assert an anomaly; several instead
   describe THE RESPONSE to one ("the procedure involves...", "the
   corrective action involves..."). The underlying symptom (an obstruction,
   a motionless AGV, too many AGVs at hospital) is real and often already
   exists as its own bare `symptom` entity elsewhere in the corpus (e.g.
   `entity:symptom:object_blocking_agv`) — these seven records are
   describing the KNOWN RESPONSE, which is procedure-shaped content, not
   the condition itself. Corrected to `component`, matching how the
   analogous, already-correctly-typed
   `entity:component:agv_fault_during_exchange_recovery_concept` (from
   entity_description_rewrites.py, §6.7) models the same kind of content.

3. **Database table content mistyped as `state`.** A `state` should be a
   checkable condition ("is X true right now"); seven entities instead
   describe a database model's schema/stored-field content — the same
   category confusion as #1, just landing on `state` instead of `symptom`
   because these came from training-video segments about the robotics
   database rather than the failure-pattern catalog. Corrected to
   `database_table`.

**Why this needed real reading, not a bigger rule set**: several of these
were only distinguishable from a legitimately-typed neighbor by content —
`entity:symptom:operator_station_chute_debris` ("a known issue... debris
accumulation") is a genuine symptom sitting right next to
`entity:symptom:log_records_for_tipper_issue_analysis` ("logs can provide
information... narrowing down tipper issues") which is not — no name
pattern or keyword separates them; only reading what each description
actually asserts does.

**Interaction with entity_duplicate_merges.py**: retyping several of these
produces a same-name, same-entity_type collision with an ALREADY-EXISTING,
correctly-typed record — a fourth duplicate-creation mechanism found this
pass, distinct from the three already documented in
entity_duplicate_merges.py's docstring (structural cross-reference,
applies_to self-echo, casing/spacing collision): two entities with the
IDENTICAL name but DIFFERENT entity_type, created independently because
different migration paths processed the same source content and happened
to classify it differently. Once retyped here, these collisions are
handled as ordinary same-type merges in entity_duplicate_merges.py — this
script must run BEFORE that one (see BRAIN_BUILD_PROCESS.md's rebuild
order).

4. **System/API action mistyped as `component`.** A dedicated fourth
   pattern, added 2026-09-08 at the user's direction: AGENT_DESIGN_NOTES.md
   §2 already named this as a real, distinct third shape (neither a human
   Capability nor a persistent state/symptom Entity — "a system/API action
   is something the system does when called") but deferred giving it its
   own EntityType. Corrected to the new `system_action` EntityType (see
   brain/schemas/entity.py's SystemActionPayload) rather than left as
   `component`, which was only ever "correct" in the weak sense of being a
   catch-all for "a named, look-up-able thing" — `system_action` is the
   actually-correct, more specific type now that real evidence (the WCS
   API catalog's own objects[] array, with group/access_surface detail)
   grounds a dedicated payload for it.

Each entry: old_entity_id -> new_entity_type (a string value of
EntityType). The record's name/description/aliases/payload/source_refs all
carry over unchanged — only entity_type (and therefore id, since
entity_id() is type-prefixed) changes.
"""

CORRECTIONS: dict[str, str] = {
    # --- Reference/data-description content mistyped as symptom -> component
    "entity:symptom:external_troubleshooting_references": "component",
    "entity:symptom:log_records_for_tipper_issue_analysis": "component",
    "entity:symptom:api_request_and_response_behavior": "component",
    "entity:symptom:sql_server_connection_verification_context": "component",
    "entity:symptom:lane_activity_model_and_sort_confirmation_data": "component",
    "entity:symptom:agv_fault_recovery_guidance": "component",
    # --- Recovery-procedure descriptions mistyped as symptom -> component
    "entity:symptom:agv_fault_during_exchange_recovery_concept": "component",
    "entity:symptom:obstruction_parcel_on_floor_troubleshooting": "component",
    "entity:symptom:obstruction_or_parcel_on_floor_troubleshooting": "component",
    "entity:symptom:agv_motionless_on_floor_troubleshooting": "component",
    "entity:symptom:agv_motionless_on_floor_fault_troubleshooting": "component",
    "entity:symptom:too_many_agvs_directed_to_hospital_troubleshooting": "component",
    "entity:symptom:pneumatic_air_line_clogged_troubleshooting": "component",
    # --- Database table content mistyped as state -> database_table
    "entity:state:system_active_error_model": "database_table",
    "entity:state:system_error_activity_model": "database_table",
    "entity:state:system_database_model_status_values": "database_table",
    "entity:state:system_database_status_values": "database_table",
    "entity:state:status_alarm_and_safety_related_database_fields": "database_table",
    "entity:state:lane_activity_status_and_classification_labels": "database_table",
    "entity:state:lane_activity_status_and_classification_indicators": "database_table",
    # --- System/API action mistyped as component -> system_action
    # (2026-09-08, user-directed: promote the third shape AGENT_DESIGN_NOTES.md
    # §2 already named but deferred — "a system/API action is something the
    # system does when called, not a human action and not a persistent
    # state" — into its own EntityType rather than leaving it a sub-case of
    # component. All 26 real entries are the canonical objects[] array of
    # docs/ontology/catalogs/wcs_api_catalog.json (the WCS API's own closed,
    # authoritative endpoint list), migrated as bare `component` entities by
    # Pass 0 before this type existed. Two more (initialize_tote,
    # exchange_sorter_side_zone) are the same real actions under a second,
    # differently-formatted name from a different source — already known,
    # deliberately-NOT-merged duplicates of initializetote/
    # exchangesortersidezone (BRAIN_BUILD_PROCESS.md §6.12's "genuinely
    # independently-real-record" case), retyped here too so both spellings
    # land in the correct class; whether they should ALSO be merged with
    # each other is the separate, already-open near-duplicate question
    # entity_duplicate_merges.py's docstring tracks, not something this
    # correction resolves.
    "entity:component:openallchutes": "system_action",
    "entity:component:cancelcloseout": "system_action",
    "entity:component:getagvfaultstats": "system_action",
    "entity:component:systemstate": "system_action",
    "entity:component:systemstartup": "system_action",
    "entity:component:systemshutdown": "system_action",
    "entity:component:closeout": "system_action",
    "entity:component:purge": "system_action",
    "entity:component:resetmetrics": "system_action",
    "entity:component:getzoneconfig": "system_action",
    "entity:component:updatezoneconfig": "system_action",
    "entity:component:removeagv": "system_action",
    "entity:component:recoveragv": "system_action",
    "entity:component:pauseagvs": "system_action",
    "entity:component:resumeagvs": "system_action",
    "entity:component:executedagvcommand": "system_action",
    "entity:component:getagvstatuses": "system_action",
    "entity:component:resendgeekcommand": "system_action",
    "entity:component:exchangesortersidezone": "system_action",
    "entity:component:removetote": "system_action",
    "entity:component:gettotetask": "system_action",
    "entity:component:resendtotetask": "system_action",
    "entity:component:initializetote": "system_action",
    "entity:component:exchangetote": "system_action",
    "entity:component:exchangelane": "system_action",
    "entity:component:getexchangesettings": "system_action",
    "entity:component:updateexchange": "system_action",
    "entity:component:initialize_tote": "system_action",
    "entity:component:exchange_sorter_side_zone": "system_action",
}

# Hand-judged SystemActionPayload content for the component -> system_action
# corrections above, grounded directly in wcs_api_catalog.json's own
# objects[] fields — group -> invocation_kind, the catalog's single
# top-level access_surface ("wcs_api") -> access_surface_entity_ids, and
# mutates_state judged per action from its own name/notes (a `Get*` query
# or `SystemState` read does not mutate; every create/update/remove/pause/
# resume/exchange/initialize/close/purge/reset/start/shutdown/resend action
# does — ExecutedAgvCommand specifically confirmed by its own catalog note,
# "re-exec active command if OptiSweep missed Geek callbacks," not guessed
# from its name alone). Never fabricated beyond what the catalog states.
SYSTEM_ACTION_PAYLOAD_OVERRIDES: dict[str, dict] = {
    "entity:component:openallchutes": {"invocation_kind": "system", "mutates_state": True},
    "entity:component:cancelcloseout": {"invocation_kind": "system", "mutates_state": True},
    "entity:component:getagvfaultstats": {"invocation_kind": "system", "mutates_state": False},
    "entity:component:systemstate": {"invocation_kind": "system", "mutates_state": False},
    "entity:component:systemstartup": {"invocation_kind": "system", "mutates_state": True},
    "entity:component:systemshutdown": {"invocation_kind": "system", "mutates_state": True},
    "entity:component:closeout": {"invocation_kind": "system", "mutates_state": True},
    "entity:component:purge": {"invocation_kind": "system", "mutates_state": True},
    "entity:component:resetmetrics": {"invocation_kind": "system", "mutates_state": True},
    "entity:component:getzoneconfig": {"invocation_kind": "system", "mutates_state": False},
    "entity:component:updatezoneconfig": {"invocation_kind": "system", "mutates_state": True},
    "entity:component:removeagv": {"invocation_kind": "agvs", "mutates_state": True},
    "entity:component:recoveragv": {"invocation_kind": "agvs", "mutates_state": True},
    "entity:component:pauseagvs": {"invocation_kind": "agvs", "mutates_state": True},
    "entity:component:resumeagvs": {"invocation_kind": "agvs", "mutates_state": True},
    "entity:component:executedagvcommand": {"invocation_kind": "agvs", "mutates_state": True},
    "entity:component:getagvstatuses": {"invocation_kind": "agvs", "mutates_state": False},
    "entity:component:resendgeekcommand": {"invocation_kind": "agvs", "mutates_state": True},
    "entity:component:exchangesortersidezone": {"invocation_kind": "totes", "mutates_state": True},
    "entity:component:removetote": {"invocation_kind": "totes", "mutates_state": True},
    "entity:component:gettotetask": {"invocation_kind": "totes", "mutates_state": False},
    "entity:component:resendtotetask": {"invocation_kind": "totes", "mutates_state": True},
    "entity:component:initializetote": {"invocation_kind": "totes", "mutates_state": True},
    "entity:component:exchangetote": {"invocation_kind": "totes", "mutates_state": True},
    "entity:component:exchangelane": {"invocation_kind": "totes", "mutates_state": True},
    "entity:component:getexchangesettings": {"invocation_kind": "totes", "mutates_state": False},
    "entity:component:updateexchange": {"invocation_kind": "totes", "mutates_state": True},
    # Same-action-different-spelling pair — same judgment as their canonical
    # counterpart above.
    "entity:component:initialize_tote": {"invocation_kind": "totes", "mutates_state": True},
    "entity:component:exchange_sorter_side_zone": {"invocation_kind": "totes", "mutates_state": True},
}

# Deliberately NOT included, checked and confirmed correctly-typed on this
# pass: entity:symptom:operator_station_chute_debris (genuine anomaly),
# entity:symptom:unplanned_restart_and_job_cleanup_issue (genuine
# anomaly), entity:symptom:state_transition_fault_visibility_during_startup_and_shutdown
# (legitimately fault-related), entity:symptom:ai1_data_availability_and_default_dimensions
# (borderline but defensible — does describe a real anomaly chain: AI1 not
# sending data -> totes overflowing), and all 27 bare failure_pattern-catalog
# symptom entities (agv_tracking_or_path_lost, gateway_unhealthy, etc. —
# correctly symptom-shaped by their own real name, just empty description
# since they're Pass-0-generated stubs, not a type error).
