from shared.stage_prompts import (
    STAGE_6_STRUCTURE_REFERENCE,
    compose_stage6_system_prompt,
    load_stage6_structure_reference,
    resolve_stage6_structure_reference_path,
)


def test_stage6_structure_reference_file_exists() -> None:
    path = resolve_stage6_structure_reference_path()
    assert path == STAGE_6_STRUCTURE_REFERENCE
    assert path.exists()


def test_load_stage6_structure_reference_contains_json_contract() -> None:
    reference = load_stage6_structure_reference()
    assert "JSON Output Contract" in reference
    assert '"merge_status": "source_finalized"' in reference
    assert "proc_<slug>_v1" in reference


def test_compose_stage6_system_prompt_appends_reference() -> None:
    composed = compose_stage6_system_prompt("Task prompt body.")
    assert composed.startswith("Task prompt body.")
    assert "Appended Canonical Runbook Structure Reference" in composed
    assert "JSON Output Contract" in composed
