# Design Decisions

This folder tracks cross-pipeline architecture decisions that are still being
validated or that affect more than one ingestion stage.

Current notes:

- [Stage 5–7 Runbook Architecture](stage_5_7_runbook_architecture.md)
- [Runbook Candidate Pool, Merge Review, And Azure Publishing Design Notes](runbook_candidate_pool_and_azure_review_design.md)
- [Stage 5/6 Playbook Extraction Mode Decision Notes](stage_5_6_playbook_extraction_modes.md)
- [Stage 8 Playbook Finalization & Runbook Linking](stage_8_playbook_finalization.md) — includes [future KG component enrichment plan](stage_8_playbook_finalization.md#future-design-considerations-knowledge-graph-component-enrichment) and [backend-vs-UI evidence rule](stage_8_playbook_finalization.md#backend-vs-ui-evidence-rule-2026-08-07)
- [Day 2 / Ontology Deep Dive: Backend Evidence Root Cause & Fixes](day2_ontology_backend_evidence_deep_dive.md) — Day2→backend mapping, capability_catalog.json `support_contract` wiring gap, new hospital-flow/sequence-backfill node predicates, remaining gaps
- [Stage 8 Link Scoring And Confidence](stage_8_link_scoring_and_confidence.md)
- [Stage 8 Capability Tags & Linking Quality Plan](stage_8_capability_tags_and_linking_plan.md) — taxonomy + Stage 6 tags, audit items #1–#5, upload-aligned sequence
- [Runbook capability taxonomy (frozen)](../ontology/taxonomy/README.md) — `capabilities` / `access_surfaces` / roles / failure patterns (`wcs_sql` included); schema **0.4**
- [Ontology surface catalogs & Stage 6 mini-RAG](ontology_surface_catalogs_and_stage6_rag.md) — per-surface catalogs, WCS SQL field semantics + provenance, Stage 6 snippet retrieval
- [Plan: catalog SQL runbooks for roster & hospital](../plan_catalog_sql_runbooks_roster_hospital.md) — deferred gold-style SSMS runbook generation from catalog `select_template`s
- [Stage 5/8 C2+B2+B1 changelog](stage_5_8_c2_b2_b1_changelog.md) — expects_* fields, linking guards, attainable-evidence outcomes
- [Support Roles, Components, and Runbook Adjacency](../ontology/support_roles_components_and_adjacency.md) — L1/L2–L3/L4 all remote; component catalog; playbook multi-link vs branching
- [SME Component Access Matrix](sme_component_access_matrix.md) — sendable sheet: components × site/operator · L1 · L2/L3 (also mirrored under `docs/ontology/`)
- [Handoff — Support Roles & Access Matrix](handoff_support_roles_access_matrix.md) — status for next agent (roles landed; linking tags still open)
- Canonical prompt snippet: [`stage_prompts/shared/role_component_access_matrix.md`](../../stage_prompts/shared/role_component_access_matrix.md)