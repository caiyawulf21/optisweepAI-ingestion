# Ontology

Machine-retrievable system documentation for Stage 5/6 mini-RAG packets and Stage 5/8 tagging.

| Path | Role |
| --- | --- |
| [`taxonomy/`](taxonomy/) | Constrained IDs (`schema_version` 0.4) + edge tables + `catalog_refs` |
| [`catalogs/surface_catalog_schema.json`](catalogs/surface_catalog_schema.json) | Shared shape for every access-surface catalog |
| [`catalogs/capability_catalog.json`](catalogs/capability_catalog.json) | Rich capability cards (surfaces, DBs/models, APIs, activities, observables, roles) |
| [`catalogs/`](catalogs/) | Per-surface catalogs (RMS, SQL, API/Apidog, Ignition, Stunnel, Event Viewer, Aveva, tipper WebVisu, hospital, ACB, site_interview, physical_floor) |
| [`sources/om_manual/`](sources/om_manual/) | Extracted OM VISU section text |
| [`sources/`](sources/) | Day1/Day2 packs reserved; OM VISU populated |
| [`support_roles_components_and_adjacency.md`](support_roles_components_and_adjacency.md) | Human adjacency seed |
| [`playbook_expects_guidance.md`](playbook_expects_guidance.md) | Stage 5 playbook `expects_*` disambiguation + dual-surface + audience (RMS≈operator; WCS≈L2/L3) |
| [`sme_component_access_matrix.md`](sme_component_access_matrix.md) | SME access matrix |

Normalize all surface catalogs: `python scripts/normalize_surface_catalogs.py`  
Rebuild capability cards: `python scripts/build_capability_catalog.py`  
Rebuild tipper/WebVisu: `python scripts/build_tipper_webvisu_catalog.py`  

Design: [`docs/design_decisions/ontology_surface_catalogs_and_stage6_rag.md`](../design_decisions/ontology_surface_catalogs_and_stage6_rag.md)  
Retrieval: `shared_pipeline_stages/ontology_rag.py`
