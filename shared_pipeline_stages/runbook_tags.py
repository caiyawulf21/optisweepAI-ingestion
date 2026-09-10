"""Normalize and infer capability / surface / role / failure tags on runbooks."""

from __future__ import annotations

import re
from typing import Any

from shared_pipeline_stages.taxonomy import canonicalize_surface_id, taxonomy_id_sets

TAG_FIELDS = (
    "capability_tags",
    "access_surface",
    "audience_roles",
    "failure_pattern_tags",
)


def normalize_runbook_tags(runbook: dict[str, Any]) -> dict[str, Any]:
    """Filter tag fields to the frozen taxonomy; canonicalize surface aliases."""
    ids = taxonomy_id_sets()
    runbook["capability_tags"] = _filter_ids(runbook.get("capability_tags"), ids["capabilities"])
    surfaces = _filter_ids(runbook.get("access_surface"), ids["access_surfaces"])
    runbook["access_surface"] = list(
        dict.fromkeys(canonicalize_surface_id(item) for item in surfaces if canonicalize_surface_id(item))
    )
    audience = _filter_ids(runbook.get("audience_roles"), ids["audience_roles"])
    if not audience:
        primary = str(runbook.get("role_required") or runbook.get("responsible_role") or "").strip()
        if primary in ids["audience_roles"]:
            audience = [primary]
    runbook["audience_roles"] = audience
    runbook["failure_pattern_tags"] = _filter_ids(runbook.get("failure_pattern_tags"), ids["failure_patterns"])
    return runbook


def union_runbook_tags(primary: dict[str, Any], sources: list[dict[str, Any]]) -> dict[str, Any]:
    """Merge tag lists from primary + source runbooks (Stage 7)."""
    for field in TAG_FIELDS:
        merged: list[str] = []
        seen: set[str] = set()
        for record in [primary, *sources]:
            for item in _string_list(record.get(field)):
                token = str(item or "").strip()
                if not token or token in seen:
                    continue
                seen.add(token)
                merged.append(token)
        primary[field] = merged
    return normalize_runbook_tags(primary)


def infer_runbook_tags(runbook: dict[str, Any]) -> dict[str, Any]:
    """Heuristic tag fill for backfill when fields are empty (no LLM)."""
    text = " ".join(
        [
            str(runbook.get("title") or ""),
            str(runbook.get("summary") or ""),
            str(runbook.get("when_to_use") or ""),
            " ".join(_string_list(runbook.get("access_or_tools_needed"))),
            " ".join(_string_list(runbook.get("not_for"))),
        ]
    ).lower()

    capabilities = list(runbook.get("capability_tags") or [])
    surfaces = list(runbook.get("access_surface") or [])
    audience = list(runbook.get("audience_roles") or [])
    failures = list(runbook.get("failure_pattern_tags") or [])

    if not capabilities:
        capabilities = _infer_capabilities(text)
    if not surfaces:
        surfaces = _infer_surfaces(text)
    if not audience:
        role = str(runbook.get("role_required") or "").strip()
        if role:
            audience = [role]
        elif surfaces and set(surfaces) & {"wcs_sql", "wcs_api", "event_viewer", "ignition_gateway"}:
            audience = ["L2_support"] if "wcs_sql" in surfaces else ["L1_support"]
        else:
            audience = ["operator"]
    if not failures:
        failures = _infer_failures(text)

    runbook["capability_tags"] = capabilities
    runbook["access_surface"] = surfaces
    runbook["audience_roles"] = audience
    runbook["failure_pattern_tags"] = failures
    return normalize_runbook_tags(runbook)


def taxonomy_prompt_appendix() -> str:
    """Compact constrained-vocab block for Stage 6 system prompts."""
    data_ids = taxonomy_id_sets()
    lines = [
        "# Appended Capability Taxonomy (constrained IDs)",
        "",
        "When emitting runbook tags, use **only** these IDs (no free-text tags).",
        "",
        f"- `capability_tags[]`: {', '.join(sorted(data_ids['capabilities']))}",
        f"- `access_surface[]`: {', '.join(sorted(data_ids['access_surfaces']))}",
        f"- `audience_roles[]`: {', '.join(sorted(data_ids['audience_roles']))}",
        f"- `failure_pattern_tags[]`: {', '.join(sorted(data_ids['failure_patterns']))}",
        "",
        "Rules:",
        "- Prefer 1–3 capability tags that name the **job** (e.g. `agv_active_errors`).",
        "- Set `access_surface` to how the job is done (`rms_ui`, `wcs_sql`, …). Multi-surface allowed.",
        "- For remotely attainable diagnostics, emit surfaces the job needs; RMS is not preferred over SSMS (SSMS holds system state + errors). When both corroborate, list both.",
        "- Set `audience_roles` to who may execute; align with `role_required` and the Role / Component Access Matrix.",
        "- Prefer `operator` (and optional `L1_support`) for `rms_ui`; prefer `L2_support`/`L3_support` for `wcs_sql`.",
        "- `failure_pattern_tags` optional when the source names a failure pattern.",
        "- Same capability + different surface is valid and preferred for corroboration (RMS UI vs WCS/SSMS).",
    ]
    return "\n".join(lines)


def _infer_capabilities(text: str) -> list[str]:
    caps: list[str] = []
    rules = [
        (
            r"active\s+agv\s+error|systemactiveerror|agvactiveerror|"
            r"active\s+(agv\s+)?(error|fault)s?|agv\s+(active\s+)?(error|fault)s?",
            "agv_active_errors",
        ),
        (r"roster|mapping|not mapped|robot roster", "device_roster_state"),
        (r"overall system|fleet status|system fault|system-down", "fleet_system_status"),
        (r"hospital diversion|hospital lane|stacklight", "hospital_diversion"),
        (r"pair(?:ing)?\s+fail|unable to get a pair|zone.*pair", "zone_pairing_state"),
        (r"tipper|webvisu|visu_", "tipper_station_fault"),
        (r"e-?stop|emergency stop", "e_stop_or_safety_stop"),
        (r"soft stop|rms pause", "rms_soft_stop"),
        (r"ignition|gateway", "gateway_health"),
        (r"windows service|event viewer|7031", "windows_service_or_event_log"),
        (r"getagvstatuses|wcs\s*api|optisweep api", "wcs_api_responsiveness"),
        (r"dwell|shutdown staging|robot state", "robot_dwell_or_shutdown_staging"),
        (r"sorter|scan data|itemsweeper|sortersweeper", "sorter_item_or_scan_state"),
        (r"tote exchange", "tote_exchange_sequence"),
        (r"bump fault|remove.*agv|physical.*agv", "agv_physical_recovery"),
        (r"wcs|optisweep.*service|webapplication", "wcs_service_health"),
    ]
    for pattern, cap in rules:
        if re.search(pattern, text, re.I):
            caps.append(cap)
    if not caps and re.search(r"\b(rms|agv|robot|fleet)\b", text, re.I):
        caps.append("fleet_system_status")
    return list(dict.fromkeys(caps))[:3]


def _infer_surfaces(text: str) -> list[str]:
    surfaces: list[str] = []
    rules = [
        (r"\b(ssms|sql|helix|wcs\s+database|dbo\.|systemactiveerror)\b", "wcs_sql"),
        (r"\b(rms|geek\+|overall system rms|agv status screen)\b", "rms_ui"),
        (r"\b(getagvstatuses|wcs\s*api|optisweep api)\b", "wcs_api"),
        (r"\b(event viewer|windows service)\b", "event_viewer"),
        (r"\bignition\b", "ignition_gateway"),
        (r"\b(hospital hmi|hospital lane)\b", "hospital_hmi"),
        (r"\b(tipper|webvisu|visu_)\b", "tipper_hmi"),
        (r"\baveva\b", "aveva_hmi"),
        (r"\b(grid|dance floor|physical)\b", "physical_floor"),
    ]
    for pattern, surface in rules:
        if re.search(pattern, text, re.I):
            surfaces.append(surface)
    return list(dict.fromkeys(surfaces))[:3]


def _infer_failures(text: str) -> list[str]:
    failures: list[str] = []
    rules = [
        (r"site.?stop|system.?down|stoppage", "site_stoppage"),
        (r"hospital diversion|hospital lane", "hospital_diversion"),
        (r"pair(?:ing)?\s+fail|unable to get a pair", "pairing_failure"),
        (r"mapping|roster.*abnormal|not mapped", "mapping_abnormal"),
        (r"bump", "bump_fault"),
        (r"gateway", "gateway_unhealthy"),
        (r"api.*(unresponsive|fail)|getagvstatuses", "api_unresponsive"),
        (r"tipper", "tipper_fault"),
        (r"service.*(crash|restart)|7031", "service_crash_or_restart"),
        (r"webapplication|web app", "web_app_fault"),
    ]
    for pattern, failure in rules:
        if re.search(pattern, text, re.I):
            failures.append(failure)
    return list(dict.fromkeys(failures))[:3]


def _filter_ids(value: Any, allowed: set[str]) -> list[str]:
    ordered: list[str] = []
    for item in _string_list(value):
        token = str(item or "").strip()
        if not token or token not in allowed:
            continue
        if token not in ordered:
            ordered.append(token)
    return ordered


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]
