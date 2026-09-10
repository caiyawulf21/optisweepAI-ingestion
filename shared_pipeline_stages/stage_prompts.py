"""Resolve shared stage prompt files from the repo-root stage_prompts folder."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STAGE_PROMPTS_ROOT = REPO_ROOT / "stage_prompts"

STAGE_6_DIR = STAGE_PROMPTS_ROOT / "stage_6"
STAGE_7_DIR = STAGE_PROMPTS_ROOT / "stage_7"
STAGE_8_DIR = STAGE_PROMPTS_ROOT / "stage_8"
STAGE_SHARED_DIR = STAGE_PROMPTS_ROOT / "shared"
STAGE_6_OPERATIONAL_PROMPT = STAGE_6_DIR / "stage6_operational_runbook_finalization_prompt.md"
STAGE_6_INCIDENT_PROMPT = STAGE_6_DIR / "stage6_incident_runbook_finalization_prompt.md"
STAGE_6_STRUCTURE_REFERENCE = STAGE_6_DIR / "stage6_runbook_finalization_structure_reference.md"
STAGE_7_MERGE_PROMPT = STAGE_7_DIR / "stage7_runbook_merge_prompt.md"
STAGE_8_LINKING_PROMPT = STAGE_8_DIR / "stage8_playbook_linking_prompt.md"
ROLE_COMPONENT_ACCESS_MATRIX = STAGE_SHARED_DIR / "role_component_access_matrix.md"
PLAYBOOK_EXPECTS_GUIDANCE = REPO_ROOT / "docs" / "ontology" / "playbook_expects_guidance.md"
STAGE5_SURFACE_EVIDENCE_GUIDANCE = REPO_ROOT / "docs" / "ontology" / "stage5_surface_evidence_guidance.md"


def resolve_stage6_operational_prompt_path(path: str | Path | None = None) -> Path:
    if path is not None:
        return Path(path)
    return STAGE_6_OPERATIONAL_PROMPT


def resolve_stage6_incident_prompt_path(path: str | Path | None = None) -> Path:
    if path is not None:
        return Path(path)
    return STAGE_6_INCIDENT_PROMPT


def resolve_stage6_structure_reference_path(path: str | Path | None = None) -> Path:
    if path is not None:
        return Path(path)
    return STAGE_6_STRUCTURE_REFERENCE


def load_prompt_file(path: str | Path) -> str:
    prompt_path = Path(path)
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8").strip()


def load_stage6_structure_reference(path: str | Path | None = None) -> str:
    return load_prompt_file(resolve_stage6_structure_reference_path(path))


def resolve_role_component_access_matrix_path(path: str | Path | None = None) -> Path:
    if path is not None:
        return Path(path)
    return ROLE_COMPONENT_ACCESS_MATRIX


def load_role_component_access_matrix(path: str | Path | None = None) -> str:
    return load_prompt_file(resolve_role_component_access_matrix_path(path))


def resolve_playbook_expects_guidance_path(path: str | Path | None = None) -> Path:
    if path is not None:
        return Path(path)
    return PLAYBOOK_EXPECTS_GUIDANCE


def load_playbook_expects_guidance(path: str | Path | None = None) -> str:
    return load_prompt_file(resolve_playbook_expects_guidance_path(path))


def load_stage5_surface_evidence_guidance(path: str | Path | None = None) -> str:
    return load_prompt_file(path or STAGE5_SURFACE_EVIDENCE_GUIDANCE)


def _append_playbook_expects_guidance(prompt: str) -> str:
    guidance = load_playbook_expects_guidance()
    return (
        f"{prompt.rstrip()}\n\n"
        "---\n\n"
        "# Appended Playbook expects_* Guidance (ontology)\n\n"
        "Follow this ontology guidance when emitting `expects_capability`, "
        "`expects_surface`, and `preferred_audience`. Constrained IDs remain "
        "the taxonomy; this file is policy + disambiguation.\n\n"
        f"{guidance}"
    )


def _append_role_component_access_matrix(prompt: str) -> str:
    matrix = load_role_component_access_matrix()
    return (
        f"{prompt.rstrip()}\n\n"
        "---\n\n"
        "# Appended Role / Component Access Matrix\n\n"
        "When assigning roles (`role_required`, `responsible_role`, `supporting_roles`, "
        "or equivalent), follow this matrix.\n\n"
        f"{matrix}"
    )


def _append_capability_taxonomy(prompt: str) -> str:
    from shared_pipeline_stages.runbook_tags import taxonomy_prompt_appendix

    return f"{prompt.rstrip()}\n\n---\n\n{taxonomy_prompt_appendix()}"


def _append_stage5_surface_evidence_guidance(prompt: str) -> str:
    guidance = load_stage5_surface_evidence_guidance()
    return (
        f"{prompt.rstrip()}\n\n"
        "---\n\n"
        "# Appended Stage 5 Source-Grounded Surface and Evidence Rules\n\n"
        "These rules override any earlier surface examples or ontology "
        "suggestions in the task prompt.\n\n"
        f"{guidance}"
    )


def compose_stage5_playbook_system_prompt(task_prompt: str) -> str:
    composed = task_prompt.strip()
    composed = _append_playbook_expects_guidance(composed)
    composed = _append_role_component_access_matrix(composed)
    composed = _append_capability_taxonomy(composed)
    return _append_stage5_surface_evidence_guidance(composed)


def compose_stage6_system_prompt(
    task_prompt: str,
    *,
    structure_reference_path: str | Path | None = None,
) -> str:
    task = task_prompt.strip()
    reference = load_stage6_structure_reference(structure_reference_path)
    composed = (
        f"{task}\n\n"
        "---\n\n"
        "# Appended Canonical Runbook Structure Reference\n\n"
        "The following structure reference is authoritative for Stage 6 output shape and required sections.\n\n"
        f"{reference}"
    )
    composed = _append_role_component_access_matrix(composed)
    return _append_capability_taxonomy(composed)


def resolve_stage7_prompt_path(path: str | Path | None = None) -> Path:
    if path is not None:
        return Path(path)
    return STAGE_7_MERGE_PROMPT


def compose_stage7_system_prompt(
    task_prompt: str,
    *,
    structure_reference_path: str | Path | None = None,
) -> str:
    task = task_prompt.strip()
    reference = load_stage6_structure_reference(structure_reference_path)
    composed = (
        f"{task}\n\n"
        "---\n\n"
        "# Appended Canonical Runbook Structure Reference\n\n"
        "Stage 7 canonical runbooks must use the same field structure as Stage 6 finalized runbooks.\n\n"
        f"{reference}"
    )
    return _append_role_component_access_matrix(composed)


def resolve_stage8_prompt_path(path: str | Path | None = None) -> Path:
    if path is not None:
        return Path(path)
    return STAGE_8_LINKING_PROMPT


def compose_stage8_system_prompt(task_prompt: str) -> str:
    return task_prompt.strip()
