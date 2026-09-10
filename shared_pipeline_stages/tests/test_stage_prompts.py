from shared_pipeline_stages.stage_prompts import (
    ROLE_COMPONENT_ACCESS_MATRIX,
    STAGE_6_STRUCTURE_REFERENCE,
    compose_stage6_system_prompt,
    compose_stage7_system_prompt,
    load_role_component_access_matrix,
    load_stage6_structure_reference,
    resolve_role_component_access_matrix_path,
    resolve_stage6_structure_reference_path,
)


def test_stage6_structure_reference_file_exists() -> None:
    path = resolve_stage6_structure_reference_path()
    assert path == STAGE_6_STRUCTURE_REFERENCE
    assert path.exists()


def test_role_component_access_matrix_file_exists() -> None:
    path = resolve_role_component_access_matrix_path()
    assert path == ROLE_COMPONENT_ACCESS_MATRIX
    assert path.exists()


def test_load_stage6_structure_reference_contains_json_contract() -> None:
    reference = load_stage6_structure_reference()
    assert "JSON Output Contract" in reference
    assert '"merge_status": "source_finalized"' in reference
    assert "proc_<slug>_v1" in reference


def test_load_role_component_access_matrix_contains_hard_rules() -> None:
    matrix = load_role_component_access_matrix()
    assert "E-stop (physical)" in matrix
    assert "RMS soft stop" in matrix
    assert "AVEVA HMI" in matrix


def test_compose_stage6_system_prompt_appends_reference_and_access_matrix() -> None:
    composed = compose_stage6_system_prompt("Task prompt body.")
    assert composed.startswith("Task prompt body.")
    assert "Appended Canonical Runbook Structure Reference" in composed
    assert "JSON Output Contract" in composed
    assert "Appended Role / Component Access Matrix" in composed
    assert "Appended Capability Taxonomy" in composed
    assert "E-stop (physical)" in composed


def test_compose_stage7_system_prompt_appends_access_matrix() -> None:
    composed = compose_stage7_system_prompt("Merge task body.")
    assert composed.startswith("Merge task body.")
    assert "Appended Role / Component Access Matrix" in composed
    assert "WCS / Helix DB (SSMS)" in composed
