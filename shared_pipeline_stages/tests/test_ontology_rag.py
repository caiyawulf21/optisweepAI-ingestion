from shared_pipeline_stages.ontology_rag import (
    infer_ontology_query,
    ontology_prompt_snippets,
    ontology_snippets_for_stage5,
    ontology_snippets_for_stage5_playbook,
    ontology_snippets_for_stage6,
    retrieve_ontology_snippets,
)
from shared_pipeline_stages.taxonomy import taxonomy_id_sets


def test_taxonomy_0_4_constrained_ids():
    ids = taxonomy_id_sets()
    assert "agv_active_errors" in ids["capabilities"]
    assert "wcs_sql" in ids["access_surfaces"]
    assert "operator" in ids["audience_roles"]


def test_retrieve_system_active_error_model():
    hits = retrieve_ontology_snippets(model_name="SystemActiveErrorModel", access_surface="wcs_sql")
    assert hits
    assert any("SystemActiveErrorModel" in (h.get("title") or "") for h in hits)
    text = " ".join(h.get("text") or "" for h in hits)
    assert "SystemErrorDescription" in text or "Name" in text
    assert "SELECT TOP" in text or "SystemActiveErrorModel" in text


def test_retrieve_capability_fleet_has_sql_model_links():
    hits = retrieve_ontology_snippets(capability="fleet_system_status", max_snippets=3)
    assert hits
    text = " ".join(h.get("text") or "" for h in hits)
    assert "SystemDatabaseModel" in text or "system" in text.lower()


def test_retrieve_capability_agv_errors():
    hits = retrieve_ontology_snippets(capability="agv_active_errors", max_snippets=3)
    assert 1 <= len(hits) <= 3
    assert hits[0]["id"] == "capability:agv_active_errors"
    text = hits[0]["text"]
    assert "rms_ui" in text
    assert "wcs_sql" in text
    assert "AgvActiveError" in text or "SystemActiveError" in text
    assert "GetAGVStatuses" in text
    prompt = ontology_prompt_snippets(capability="agv_active_errors", access_surface="wcs_sql")
    assert "System reference snippets" in prompt
    assert "Capability —" in prompt


def test_retrieve_webvisu_tipper_catalog():
    hits = retrieve_ontology_snippets(free_text="WebVisu tipper alarm heartbeat", max_snippets=3)
    assert hits
    blob = " ".join(f"{h.get('id')} {h.get('title')} {h.get('text')}" for h in hits)
    assert "tipper_hmi" in blob or "WebVisu" in blob or "VISU" in blob
    assert "visu_alarm" in blob or "heartbeat" in blob.lower() or "VISU_ALARM" in blob


def test_infer_ontology_query_finds_model_and_surface():
    keys = infer_ontology_query(
        "Open RobotCommandDatabaseModel in SSMS and check sent versus in-progress",
        artifacts=[{"ocr_text": "Robot Command Database Model", "nearby_text": "Helix robotics"}],
    )
    assert keys.access_surface == "wcs_sql"
    assert keys.model_name == "RobotCommandDatabaseModel"


def test_stage5_snippets_prefer_surface_or_capability():
    snippets = ontology_snippets_for_stage5(
        "Trainer mentions bag out control and destinations closing on the sorter",
        artifacts=[{"nearby_text": "bag out destinations exchange totes"}],
        skip_if_grounded=False,
    )
    assert len(snippets) <= 2
    if snippets:
        assert all(str(s.get("id") or "").startswith(("surface:", "capability:")) for s in snippets)
        assert "retrieval_keys" in snippets[0]


def test_stage5_playbook_snippets_include_models_for_detailed_nodes():
    snippets = ontology_snippets_for_stage5_playbook(
        "AGVs stopped system down — check fleet status, active errors, SystemDatabaseModel / SystemActiveErrorModel in SSMS and Overall System RMS",
        artifacts=[{"nearby_text": "active AGV errors system state down"}],
    )
    assert 1 <= len(snippets) <= 5
    ids = [str(s.get("id") or "") for s in snippets]
    assert any(i.startswith(("model:", "capability:", "surface:", "db:")) for i in ids)
    joined = " ".join(str(s.get("text") or s.get("id") or "") for s in snippets).lower()
    assert "system" in joined or "error" in joined or "fleet" in joined or "rms" in joined


def test_stage5_skips_when_already_grounded():
    snippets = ontology_snippets_for_stage5(
        "In SSMS open Helix and check the tipper heartbeat table",
        skip_if_grounded=True,
    )
    assert snippets == []


def test_stage6_snippets_prefer_deep_model_grounding():
    candidate = {
        "title": "Check Robot Command Database Model active command status",
        "summary": "Use RobotCommandDatabaseModel to see sent vs in-progress commands.",
        "rough_steps": ["Open RobotCommandDatabaseModel in SSMS", "Check timing fields"],
        "access_or_tools_needed": ["SSMS", "Helix"],
        "access_surface": ["wcs_sql"],
        "capability_tags": ["robot_command_or_task_state"],
    }
    snippets = ontology_snippets_for_stage6(
        candidate,
        artifacts=[{"ocr_text": "RobotCommandDatabaseModel", "short_description": "command table"}],
    )
    assert 1 <= len(snippets) <= 3
    ids = [str(s.get("id") or "") for s in snippets]
    assert any(i.startswith(("model:", "capability:", "surface:", "activity:")) for i in ids)
