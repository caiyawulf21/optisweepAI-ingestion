"""Deterministic eligibility rules for Stage 5 candidates and Stage 6 runbooks."""

from __future__ import annotations

import re
from typing import Any

from shared_pipeline_stages.taxonomy import load_capability_taxonomy

META_SOURCE_RE = re.compile(
    r"\b("
    r"per the source|as (?:shown|described|stated|suggested) by the source|"
    r"from the (?:training|source)|in the source(?: segment| material)?|"
    r"source[- ]backed|documented (?:design )?intent|training material|"
    r"training (?:slide|video|playback|segment)|ocr text|ocr_text|"
    r"as shown in the source|referenced by the source|"
    r"listen to(?:/confirm)? the|quote or paraphrase the (?:contrast )?sentence|"
    r"record a clarification|point to the frame"
    r")\b",
    re.IGNORECASE,
)

ORIENTATION_RE = re.compile(
    r"\b("
    r"walkthrough|familiariz(?:e|ation)|get familiar|orientation|"
    r"clarify what a referenced|contrast (?:sentence|against)|"
    r"what a referenced .{0,40} differs|manual.{0,40}different from|"
    r"study guide|architecture overview only|identify the current .{0,40} meaning"
    r")\b",
    re.IGNORECASE,
)

VAGUE_OUTCOME_RE = re.compile(
    r"\b("
    r"ask controls|engage(?:d)? controls|route .{0,40} to controls|"
    r"controls are engaged|useful information|"
    r"documented intent|source text was recorded|"
    r"you can (?:point to|quote|paraphrase) the"
    r")\b",
    re.IGNORECASE,
)

INVENTED_UI_RE = re.compile(
    r"\b("
    r"bag[\s_-]?out control system|optisweep bag[\s_-]?out control|"
    r"control system (?:ui|screen|control)|"
    r"training video playback|source segment (?:ui|screen)"
    r")\b",
    re.IGNORECASE,
)

LIVE_SURFACE_TOKEN_RE = re.compile(
    r"\b("
    r"ignition|gateway|ssms|sql server(?: management)?|helix|"
    r"rms|apidog|api dog|aveva|event viewer|windows services?|"
    r"webvisu|visu_|operator station|optisweep service|"
    r"hospital(?:\s+hmi)?|tipper(?:\s+hmi)?|building(?:\s+acb)?\s+hmi|"
    r"stunnel|s-tunnel|wcs api|getagvstatuses|opc"
    r")\b",
    re.IGNORECASE,
)


def allowed_access_surfaces_packet() -> list[dict[str, str]]:
    data = load_capability_taxonomy()
    surfaces: list[dict[str, str]] = []
    for item in data.get("access_surfaces") or []:
        surface_id = str(item.get("id") or "").strip()
        if not surface_id:
            continue
        surfaces.append(
            {
                "id": surface_id,
                "label": str(item.get("label") or surface_id).strip(),
                "description": str(item.get("description") or "").strip()[:240],
            }
        )
    return surfaces


def collect_procedure_text(record: dict[str, Any]) -> str:
    parts = [
        str(record.get("title") or ""),
        str(record.get("summary") or ""),
        str(record.get("candidate_goal") or ""),
        str(record.get("when_to_use") or ""),
        " ".join(str(item) for item in record.get("access_or_tools_needed") or []),
        " ".join(str(item) for item in record.get("rough_steps") or []),
        " ".join(str(item) for item in record.get("expected_result") or [])
        if isinstance(record.get("expected_result"), list)
        else str(record.get("expected_result") or ""),
    ]
    for step in record.get("steps") or []:
        if not isinstance(step, dict):
            continue
        parts.extend(
            [
                str(step.get("title") or ""),
                str(step.get("instruction") or ""),
                str(step.get("expected_result") or ""),
                " ".join(str(item) for item in step.get("stop_or_escalate_if") or []),
            ]
        )
    return " ".join(parts)


def eligibility_errors_for_candidate(candidate: dict[str, Any]) -> list[str]:
    metadata = candidate.get("metadata") if isinstance(candidate.get("metadata"), dict) else {}
    if str(metadata.get("created_by") or "") == "stage_5_candidate_coverage_backfill":
        return []
    text = collect_procedure_text(candidate)
    errors: list[str] = []
    if META_SOURCE_RE.search(text):
        errors.append(
            "not a live runbook: steps/outcomes reference training source/OCR/playback "
            "instead of a live operator/support surface"
        )
    if ORIENTATION_RE.search(text):
        errors.append(
            "orientation/familiarization content belongs in operational context, not a runbook"
        )
    if INVENTED_UI_RE.search(text):
        errors.append(
            "invented or unverified UI/access surface (spoken product name without taxonomy surface)"
        )
    if VAGUE_OUTCOME_RE.search(text):
        errors.append("expected outcome is vague (ask/engage controls or meta source language)")
    if not LIVE_SURFACE_TOKEN_RE.search(text):
        errors.append(
            "no verified live access surface named (Ignition/SSMS/RMS/API Dog/AVEVA/Services/…)"
        )
    procedure_type = str(candidate.get("likely_procedure_type") or candidate.get("procedure_type") or "")
    if procedure_type == "reference" and ORIENTATION_RE.search(text):
        errors.append("reference/orientation candidate must not be finalized as a runbook")
    return errors


def eligibility_errors_for_runbook(runbook: dict[str, Any]) -> list[str]:
    text = collect_procedure_text(runbook)
    errors: list[str] = []
    if META_SOURCE_RE.search(text):
        errors.append(
            "not a live runbook: instructions cite source/OCR/training playback; "
            "end users do not have the training source"
        )
    if ORIENTATION_RE.search(text):
        errors.append("orientation/familiarization is not a troubleshooting or operations runbook")
    if INVENTED_UI_RE.search(text):
        errors.append("unverified access surface/UI named as if it were a live control")
    if VAGUE_OUTCOME_RE.search(text):
        errors.append("expected results are not concrete/observable on a live surface")
    surfaces = [str(item) for item in (runbook.get("access_surface") or []) if str(item).strip()]
    known_surfaces = {
        str(item.get("id") or "").strip() for item in allowed_access_surfaces_packet() if item.get("id")
    }
    tagged_live = bool(set(surfaces) & known_surfaces)
    if not LIVE_SURFACE_TOKEN_RE.search(text) and not tagged_live:
        errors.append("missing verified live access surface in title/steps/tools")
    if not surfaces and str(runbook.get("procedure_type") or "") in {"diagnostic", "operation", "recovery"}:
        errors.append("diagnostic/operation/recovery runbook requires taxonomy access_surface tags")
    ignition_only = bool(re.search(r"\bignition\b", text, re.IGNORECASE)) and not re.search(
        r"\b(tipper|webvisu|visu_|ssms|helix|rms|apidog)\b", text, re.IGNORECASE
    )
    if ignition_only and surfaces and set(surfaces).issubset({"tipper_hmi", "wcs_api", "wcs_sql"}):
        errors.append("access_surface tags do not match Ignition evidence (prefer ignition_gateway)")
    return errors
