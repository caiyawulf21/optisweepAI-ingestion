"""Resolve shared stage prompt files from the repo-root stage_prompts folder."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STAGE_PROMPTS_ROOT = REPO_ROOT / "stage_prompts"

STAGE_6_DIR = STAGE_PROMPTS_ROOT / "stage_6"
STAGE_6_OPERATIONAL_PROMPT = STAGE_6_DIR / "stage6_operational_runbook_finalization_prompt.md"
STAGE_6_INCIDENT_PROMPT = STAGE_6_DIR / "stage6_incident_runbook_finalization_prompt.md"
STAGE_6_STRUCTURE_REFERENCE = STAGE_6_DIR / "stage6_runbook_finalization_structure_reference.md"


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


def compose_stage6_system_prompt(
    task_prompt: str,
    *,
    structure_reference_path: str | Path | None = None,
) -> str:
    task = task_prompt.strip()
    reference = load_stage6_structure_reference(structure_reference_path)
    return (
        f"{task}\n\n"
        "---\n\n"
        "# Appended Canonical Runbook Structure Reference\n\n"
        "The following structure reference is authoritative for Stage 6 output shape and required sections.\n\n"
        f"{reference}"
    )
