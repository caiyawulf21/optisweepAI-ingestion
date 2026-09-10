"""Normalize all access-surface catalogs to tipper_hmi-style schema + deepen content."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CAT = REPO / "docs/ontology/catalogs"
TAX = REPO / "docs/ontology/taxonomy/runbook_capability_taxonomy.json"
CROSS = REPO / "docs/ontology/catalogs/cross_links.json"
CAPS = REPO / "docs/ontology/catalogs/capability_catalog.json"
DAY2 = (
    REPO
    / "operationalknowledgeingestion/data/output/training_video_day2/stage_1_source_bundle/training_video_slide_segments.json"
)
DAY1 = (
    REPO
    / "operationalknowledgeingestion/data/output/training_video_day1/stage_1_source_bundle/training_video_slide_segments.json"
)

COMMON_KEYS = [
    "schema_version",
    "catalog_id",
    "access_surface",
    "title",
    "aliases",
    "purpose",
    "when_to_use",
    "not_for",
    "architecture_notes",
    "audience_roles_typical",
    "role_paths",
    "screens_or_views",
    "objects",
    "activities",
    "related_capabilities",
    "related_failure_patterns",
    "distinguish_from",
    "gaps",
    "evidence",
    "source_refs",
]


def _load(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8-sig" if path.suffix == ".json" else "utf-8"))


def _evidence_for(patterns: list[str], limit: int = 8) -> list[dict]:
    pat = re.compile("|".join(patterns), re.I)
    out: list[dict] = []
    for source, path in (("training_video_day2", DAY2), ("training_video_day1", DAY1)):
        if not path.exists():
            continue
        segs = _load(path)
        if not isinstance(segs, list):
            continue
        for seg in segs:
            transcript = str(seg.get("transcript_text") or "")
            ocr = str(seg.get("ocr_text") or "")
            blob = f"{transcript} {ocr}"
            if not pat.search(blob):
                continue
            snippet = re.sub(r"\s+", " ", (transcript or ocr).strip())[:320]
            if len(snippet) < 40:
                continue
            out.append({"source": source, "kind": "transcript" if transcript else "ocr", "snippet": snippet})
            if len(out) >= limit:
                return out
    return out


def _caps_touching(surface: str) -> tuple[list[str], list[str]]:
    caps_doc = _load(CAPS)
    caps: list[str] = []
    fails: list[str] = []
    for card in caps_doc.get("capabilities") or []:
        surfs = (card.get("primary_access_surfaces") or []) + (card.get("secondary_access_surfaces") or [])
        if surface in surfs:
            caps.append(card["id"])
            for fp in card.get("failure_patterns") or []:
                if fp not in fails:
                    fails.append(fp)
    return caps, fails


def _activities_from_cross(surface: str) -> list[dict]:
    cross = _load(CROSS)
    acts = []
    for act in cross.get("surface_activities") or []:
        if act.get("access_surface") != surface:
            continue
        acts.append(
            {
                "id": act.get("activity_id"),
                "label": act.get("label"),
                "observables": act.get("observables") or [],
                "capability_hints": act.get("capability_hints") or [],
                "audience_roles": act.get("audience_roles") or [],
            }
        )
    return acts


def _tax_surface(surface_id: str) -> dict:
    tax = _load(TAX)
    for row in tax.get("access_surfaces") or []:
        if row.get("id") == surface_id:
            return row
    return {"id": surface_id, "label": surface_id, "aliases": []}


def _base(
    surface: str,
    *,
    title: str,
    aliases: list[str],
    purpose: str,
    when_to_use: list[str],
    not_for: list[str],
    architecture_notes: list[str],
    audience_roles_typical: list[str],
    role_paths: dict[str, str],
    screens_or_views: list[dict],
    objects: list[dict],
    activities: list[dict],
    distinguish_from: dict[str, str],
    gaps: list[str],
    evidence_patterns: list[str],
    extra_evidence: list[dict] | None = None,
    source_refs: list[dict] | None = None,
) -> dict:
    tax = _tax_surface(surface)
    aliases = list(dict.fromkeys([*(tax.get("aliases") or []), *aliases, tax.get("label") or "", surface]))
    aliases = [a for a in aliases if a]
    rel_caps, rel_fails = _caps_touching(surface)
    cross_acts = _activities_from_cross(surface)
    # merge activities by id
    by_id = {a["id"]: a for a in cross_acts if a.get("id")}
    for act in activities:
        by_id[act["id"]] = {**by_id.get(act["id"], {}), **act}
    merged_acts = list(by_id.values()) or activities
    evidence = list(extra_evidence or []) + _evidence_for(evidence_patterns)
    # dedupe snippets
    seen = set()
    deduped = []
    for ev in evidence:
        key = ev.get("snippet", "")[:80]
        if key in seen:
            continue
        seen.add(key)
        deduped.append(ev)
    return {
        "schema_version": "0.4",
        "catalog_id": surface,
        "access_surface": surface,
        "title": title,
        "aliases": aliases,
        "purpose": purpose,
        "when_to_use": when_to_use,
        "not_for": not_for,
        "architecture_notes": architecture_notes,
        "audience_roles_typical": audience_roles_typical,
        "role_paths": role_paths,
        "screens_or_views": screens_or_views,
        "objects": objects,
        "activities": merged_acts,
        "related_capabilities": rel_caps,
        "related_failure_patterns": rel_fails,
        "distinguish_from": distinguish_from,
        "gaps": gaps,
        "evidence": deduped[:16],
        "source_refs": source_refs
        or [
            {"source": "training_video_day2"},
            {"source": "training_video_day1"},
            {"source": "support_roles_components_and_adjacency.md"},
            {"source": "docs/ontology/catalogs/capability_catalog.json"},
        ],
    }


def build_rms() -> dict:
    return _base(
        "rms_ui",
        title="Geek+ RMS (Robot Management System) web UI",
        aliases=["rms", "fleet_status_ui", "Geek+ RMS", "robotControl", "map monitor"],
        purpose=(
            "Web fleet / robot status UI at the site RMS IP. Primary site/operator surface for AGV "
            "alarms, roster/map, and overall fleet health; L1 may use the same overview remotely; "
            "L2/L3 use deeper RMS views plus WCS SQL/API corroboration. Not SSMS and not tipper WebVisu."
        ),
        when_to_use=[
            "AGV alarms / active error overview",
            "Roster / map / robotControl membership and disconnects",
            "Confirm loads before coaching master E-stop clear",
            "Blank or unreachable RMS as system-down symptom",
            "Orange/map collision or location cues mentioned in training",
        ],
        not_for=[
            "Deep SSMS SystemActiveError column interpretation (use wcs_sql)",
            "Tipper VISU alarms (use tipper_hmi)",
            "Physical E-stop reset (operator only)",
            "RMS soft stop mutate is L2/L3 only — not L1",
        ],
        architecture_notes=[
            "Same capability (e.g. agv_active_errors) may be done on rms_ui (operator/L1) and wcs_sql/wcs_api (L2/L3).",
            "Direct RMS/API bypass of OptiSweep can desync — prefer documented OptiSweep paths.",
            "Blank RMS often pairs with wcs_service_health / Event Viewer / unplanned restart trio.",
        ],
        audience_roles_typical=["operator", "L1_support", "L2_support", "L3_support"],
        role_paths={
            "operator": "Primary day-to-day RMS user on site (overview / AGV status / map).",
            "L1_support": "Remote overview / AGV status / map entry views; coach site; no soft-stop mutate.",
            "L2_support": "Deeper fleet views + corroborate with SSMS/API; PauseAGVs only if soft-stop capability.",
            "L3_support": "Persistent fleet issues / RCA.",
        },
        screens_or_views=[
            {
                "id": "rms_overview",
                "title": "RMS overview / AGV status",
                "purpose": "Fleet alarms and AGV status at a glance.",
                "aliases": ["AGV status", "overview"],
                "key_points": ["alarms present/clear", "RMS blank = escalate service health"],
            },
            {
                "id": "rms_map_robotcontrol",
                "title": "Map monitor / robotControl",
                "purpose": "Map locations, workstation IDs, disconnect / E-stop cues on map.",
                "aliases": ["robotControl", "map monitor"],
                "key_points": ["robot disconnected", "emergency stop trigger on map", "orange locations"],
            },
        ],
        objects=[
            {"id": "agv_alarm", "label": "AGV alarm / fault on overview", "capability_hints": ["agv_active_errors"]},
            {"id": "robot_roster", "label": "Robot roster / mapped membership", "capability_hints": ["device_roster_state"]},
            {"id": "robotcontrol_load", "label": "robotControl load before master E-stop clear", "capability_hints": ["e_stop_or_safety_stop"]},
        ],
        activities=[
            {
                "id": "rms_overview_agv_status",
                "label": "Open RMS overview / AGV status",
                "observables": ["alarms present", "alarms clear", "RMS blank"],
                "capability_hints": ["agv_active_errors", "fleet_system_status"],
                "audience_roles": ["operator", "L1_support", "L2_support", "L3_support"],
            },
            {
                "id": "rms_map_monitor",
                "label": "Map monitor / robotControl",
                "observables": ["robot disconnected", "emergency stop trigger on map", "workstation IDs", "orange locations"],
                "capability_hints": ["device_roster_state", "e_stop_or_safety_stop"],
                "audience_roles": ["operator", "L1_support", "L2_support", "L3_support"],
            },
            {
                "id": "rms_before_master_estop_clear",
                "label": "Confirm load / robots before master E-stop clear coaching",
                "observables": ["robotControl loads"],
                "capability_hints": ["e_stop_or_safety_stop", "wcs_service_health"],
                "audience_roles": ["L2_support", "L3_support"],
                "notes": "Physical E-stop clear remains operator-only.",
            },
        ],
        distinguish_from={
            "wcs_sql": "Authoritative AGV/system error rows and locations — corroborate, don't replace overview.",
            "tipper_hmi": "Tipper WebVisu station HMI — different job.",
            "aveva_hmi": "Site Aveva overall/totes — operator primary; not Geek+ RMS.",
        },
        gaps=["Full Geek+ RMS field dictionary per screen not in training corpus."],
        evidence_patterns=[r"\bRMS\b", r"robotControl", r"orange locations", r"log into rms"],
    )


def build_ignition() -> dict:
    return _base(
        "ignition_gateway",
        title="Ignition gateway / OPC server",
        aliases=["ignition", "OPC server", "OPC Connections", "gateway", "tag provider"],
        purpose=(
            "Ignition as OPC server to tippers/hospital and tag provider (SYS1 metrics) feeding Aveva. "
            "L2/L3 use Gateway UI for OPC Connections and performance; L1 only identifies role/symptoms."
        ),
        when_to_use=[
            "OPC tipper/hospital connections Faulted",
            "Gateway performance / memory issues",
            "Unplanned restart host path (Ignition lag → OptiSweep restart)",
            "Confirm tags readable (Designer / web view)",
        ],
        not_for=[
            "Tipper MCP/alarm screens (tipper_hmi WebVisu)",
            "Aveva operator pages (aveva_hmi)",
            "L1 admin recovery how-tos",
        ],
        architecture_notes=[
            "Day2: Config → OPC → OPC Connections; tippers powered off show Faulted.",
            "Heartbeat flatline on tippers after Ignition comes up late → restart OptiSweep.",
            "Same APIs Ignition calls also available in Apidog on primary.",
            "OPC COM module ties robotics path; XLE COM / Stunnel for UPS chat.",
        ],
        audience_roles_typical=["L2_support", "L3_support"],
        role_paths={
            "L1_support": "Identify Ignition role / symptoms only.",
            "L2_support": "OPC Connections + gateway performance + host restart path.",
            "L3_support": "Persistent OPC/gateway ownership; L4 if product defect.",
            "operator": "No Ignition admin; report tipper HMI symptoms.",
        },
        screens_or_views=[
            {
                "id": "opc_connections",
                "title": "Config → OPC → OPC Connections",
                "purpose": "Live OPC connection state to tippers/hospital.",
                "aliases": ["OPC Connections"],
                "key_points": ["Connected vs Faulted", "powered-off tipper example"],
            },
            {
                "id": "gateway_performance",
                "title": "Gateway performance / status",
                "purpose": "Gateway health and memory/performance trends.",
                "aliases": ["Gateway status"],
                "key_points": ["unreachable gateway", "performance degradation"],
            },
            {
                "id": "designer_or_web_tags",
                "title": "Designer / web view tags",
                "purpose": "Read tipper/hospital tags (training: web view can read tags).",
                "aliases": ["web view", "Designer"],
                "key_points": ["tags present", "not a substitute for station VISU alarms"],
            },
        ],
        objects=[
            {"id": "opc_tipper_connection", "label": "OPC connection to tipper", "capability_hints": ["opc_connection_or_tipper_heartbeat"]},
            {"id": "sys1_tags", "label": "SYS1 / tipper-hospital tags", "capability_hints": ["opc_connection_or_tipper_heartbeat"]},
        ],
        activities=[
            {
                "id": "opc_connections_view",
                "label": "Config → OPC → OPC Connections",
                "observables": ["connection Connected", "Faulted (e.g. tipper powered off)"],
                "capability_hints": ["opc_connection_or_tipper_heartbeat", "gateway_health"],
                "audience_roles": ["L2_support", "L3_support"],
            },
            {
                "id": "gateway_performance",
                "label": "Gateway performance / memory trend",
                "observables": ["memory spike to zero", "gateway unreachable"],
                "capability_hints": ["gateway_health"],
                "audience_roles": ["L2_support", "L3_support"],
            },
            {
                "id": "tag_provider_sys1",
                "label": "Tag provider / SYS1 metrics tags",
                "observables": ["tipper/hospital tags present", "Aveva request/response tags"],
                "capability_hints": ["opc_connection_or_tipper_heartbeat", "wcs_api_responsiveness"],
                "audience_roles": ["L2_support", "L3_support"],
            },
        ],
        distinguish_from={
            "tipper_hmi": "On-station WebVisu controls/alarms — Ignition corroborates OPC/heartbeat.",
            "aveva_hmi": "Consumes Ignition/API tags — not the gateway admin UI.",
            "wcs_api": "Apidog hits same OptiSweep APIs Ignition may call.",
        },
        gaps=["Full tag path inventory not mined; expand from Designer exports if available."],
        evidence_patterns=[r"Ignition", r"OPC Connections", r"heartbeat", r"Gateway"],
    )


def build_stunnel() -> dict:
    return _base(
        "stunnel",
        title="S-Tunnel / UPS Chat xLE path",
        aliases=["S-Tunnel", "Stunnel", "Chat xLE", "XLE chat", "SortationChat", "AI01", "AI02"],
        purpose=(
            "Stunnel on primary secures OTNet↔UPS chat (AI01, AI02, SortationChat). Used so OptiSweep "
            "XLE COM can exchange scan/sort/hot-bin messages with UPS chat."
        ),
        when_to_use=[
            "Scan/sort/hot-bin messages not flowing",
            "After unplanned restart — verify Stunnel connections",
            "L1 asks whether Chat messages are flowing",
        ],
        not_for=["RMS AGV alarms as substitute for message-path health", "Tipper VISU faults"],
        architecture_notes=[
            "Day2: File → Connections shows current Stunnel connections on bottom.",
            "XLE COM module manages SorterSweeper ↔ UPS chat server over this path.",
            "Part of unplanned-restart host checks with Ignition + OptiSweep.",
        ],
        audience_roles_typical=["L1_support", "L2_support", "L3_support"],
        role_paths={
            "L1_support": "Ask if Chat/sort messages flowing.",
            "L2_support": "Stunnel File → Connections (AI01/AI02/SortationChat).",
            "L3_support": "Persistent Stunnel/Chat ownership.",
            "operator": "Report site message-flow symptoms if observable.",
        },
        screens_or_views=[
            {
                "id": "stunnel_connections",
                "title": "File → Connections",
                "purpose": "List AI01 / AI02 / SortationChat connection state.",
                "aliases": ["connections list"],
                "key_points": ["connected vs missing", "check after restart"],
            }
        ],
        objects=[
            {"id": "ai01", "label": "Stunnel AI01", "capability_hints": ["ups_chat_or_stunnel_health"]},
            {"id": "ai02", "label": "Stunnel AI02", "capability_hints": ["ups_chat_or_stunnel_health"]},
            {"id": "sortation_chat", "label": "SortationChat", "capability_hints": ["ups_chat_or_stunnel_health"]},
        ],
        activities=[
            {
                "id": "stunnel_connections_list",
                "label": "File → Connections list",
                "observables": ["AI01/AI02/SortationChat connected", "connection missing"],
                "capability_hints": ["ups_chat_or_stunnel_health"],
                "audience_roles": ["L2_support", "L3_support"],
            },
            {
                "id": "ask_messages_flowing",
                "label": "Ask if Chat/sort messages flowing (L1)",
                "observables": ["site reports messages flowing / not"],
                "capability_hints": ["ups_chat_or_stunnel_health"],
                "audience_roles": ["L1_support"],
            },
        ],
        distinguish_from={
            "wcs_api": "Internal OptiSweep APIs — not UPS chat tunnel.",
            "ignition_gateway": "OPC/tags — parallel host check, different protocol.",
        },
        gaps=["Per-connection advanced Stunnel config fields not in training."],
        evidence_patterns=[r"tunnel", r"Stunnel", r"SortationChat", r"XLE chat", r"connections"],
    )


def build_event_viewer() -> dict:
    return _base(
        "event_viewer",
        title="Windows Event Viewer / Services MMC",
        aliases=["Event Viewer", "Services", "SCM", "7031", "OptiSweep service"],
        purpose=(
            "Host Windows logs and Services MMC for OptiSweep / WCSWebApplication crashes, 7031, "
            "restart storms, and confirming OptiSweep running after unplanned restart (with SQL Agent on backup)."
        ),
        when_to_use=[
            "Blank RMS / suspected service down",
            "Crash loops / 7031",
            "After Ignition lag — confirm OptiSweep restarted",
            "SQL Server Agent on backup after unplanned restart",
        ],
        not_for=["AGV active-error triage when service is healthy", "Operator access"],
        architecture_notes=[
            "Unplanned restart path: Ignition → Stunnel → OptiSweep service (+ tipper heartbeat, RMS loads).",
            "Few dedicated runbooks historically — allow honest unresolved in playbooks.",
        ],
        audience_roles_typical=["L2_support", "L3_support"],
        role_paths={
            "L1_support": "No Event Viewer how-to; escalate.",
            "L2_support": "Services + Event Viewer primary.",
            "L3_support": "Same + RCA.",
            "operator": "No access.",
        },
        screens_or_views=[
            {"id": "services_mmc", "title": "Services MMC", "purpose": "OptiSweep / related service Running vs Stopped.", "aliases": ["services.msc"], "key_points": ["Running", "Stopped", "restart storm"]},
            {"id": "event_viewer_app", "title": "Event Viewer Application/System", "purpose": "Crash and service control events.", "aliases": ["eventvwr"], "key_points": ["7031", "unexpected restarts"]},
        ],
        objects=[
            {"id": "optisweep_service", "label": "OptiSweep Windows service", "capability_hints": ["wcs_service_health"]},
            {"id": "wcs_web_app", "label": "WCSWebApplication", "capability_hints": ["windows_service_or_event_log"]},
            {"id": "sql_agent_backup", "label": "SQL Server Agent on backup", "capability_hints": ["wcs_service_health"]},
        ],
        activities=[
            {
                "id": "services_mmc",
                "label": "Services MMC — OptiSweep / related",
                "observables": ["Running", "Stopped", "restart required after Ignition lag"],
                "capability_hints": ["wcs_service_health", "windows_service_or_event_log"],
                "audience_roles": ["L2_support", "L3_support"],
            },
            {
                "id": "event_log_crash",
                "label": "Event Viewer crash / 7031",
                "observables": ["service crash events", "7031"],
                "capability_hints": ["windows_service_or_event_log"],
                "audience_roles": ["L2_support", "L3_support"],
            },
        ],
        distinguish_from={
            "ignition_gateway": "OPC/gateway — often the reason OptiSweep must be restarted.",
            "rms_ui": "Symptom surface when blank; not the host log.",
        },
        gaps=["Dedicated crash runbook catalog still thin."],
        evidence_patterns=[r"OptiSweep", r"restart", r"7031", r"service", r"Event Viewer"],
    )


def build_apidog() -> dict:
    api = _load(CAT / "wcs_api_catalog.json")
    objects = []
    activities = []
    for group in ("system", "agvs", "totes"):
        for row in api.get(group) or []:
            name = row.get("name")
            if not name:
                continue
            objects.append(
                {
                    "id": name,
                    "label": name,
                    "group": group,
                    "aliases": row.get("aliases") or [],
                    "capability_hints": row.get("capability_hints") or [],
                    "notes": row.get("notes"),
                }
            )
            activities.append(
                {
                    "id": f"apidog_{re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')}",
                    "label": f"Apidog — {name}",
                    "observables": ["success payload", "timeout/5xx", "unexpected empty"],
                    "capability_hints": row.get("capability_hints") or [],
                    "audience_roles": ["L2_support", "L3_support"],
                }
            )
    return _base(
        "apidog",
        title="Apidog — OptiSweep / WCS API client on primary",
        aliases=["API Dog", "Apidog", "WCS API client", "OptiSweep API"],
        purpose=(
            "Locally hosted API client on WCS primary for System/AGV/Tote APIs. Same APIs Ignition uses "
            "to feed Aveva. Primary L2/L3 surface for GetAGVStatuses, closeout, exchange, zone config, etc."
        ),
        when_to_use=[
            "Corroborate AGV/system state remotely",
            "API responsiveness checks",
            "Authorized CloseOut / Exchange / ResendGeekCommand / InitializeTote",
            "Unplanned restart — re-exec commands if OptiSweep missed Geek callbacks",
        ],
        not_for=["Operator access", "Inventing request bodies not in source", "L1 mutate"],
        architecture_notes=[
            "Day2: Apidog set up on primary servers.",
            "GetAGVStatuses shows AGV state, command vitals, AGV errors and system errors.",
            "Mutating APIs only when playbook/source authorizes.",
        ],
        audience_roles_typical=["L2_support", "L3_support"],
        role_paths={
            "L1_support": "Escalate to L2 for Apidog.",
            "L2_support": "Primary API client.",
            "L3_support": "Deeper API diagnostics / authorized mutates.",
            "operator": "No access.",
        },
        screens_or_views=[
            {"id": "apidog_collections", "title": "Apidog System / AGV / Tote collections", "purpose": "Grouped OptiSweep API requests.", "aliases": ["API Dog"], "key_points": ["primary host", "same APIs as Ignition→Aveva"]},
        ],
        objects=objects,
        activities=activities[:20],
        distinguish_from={
            "wcs_api": "Logical API surface; apidog is the client tool on primary.",
            "aveva_hmi": "Operator UI that may trigger same APIs via Ignition.",
            "wcs_sql": "DB truth for many of the same jobs.",
        },
        gaps=["Full request/response JSON schemas not in training OCR."],
        evidence_patterns=[r"API Dog", r"Apidog", r"GetAGVStatuses", r"Get AGV status"],
        extra_evidence=api.get("evidence") or [],
        source_refs=[{"source": "training_video_day2"}, {"source": "wcs_api_catalog.json"}, {"source": "support_roles_components_and_adjacency.md"}],
    )


def build_wcs_api_envelope() -> dict:
    """Rewrite wcs_api catalog with common envelope; keep API groups as objects."""
    old = _load(CAT / "wcs_api_catalog.json")
    # Prefer existing enriched apidog objects path — write full common structure
    doc = build_apidog()
    # Override id/surface for wcs_api logical catalog
    doc["catalog_id"] = "wcs_api"
    doc["access_surface"] = "wcs_api"
    doc["title"] = "OptiSweep / WCS APIs (System, AGVs, Totes)"
    doc["aliases"] = list(
        dict.fromkeys(
            [
                "wcs_api",
                "OptiSweep API",
                "WCS API",
                "GetAGVStatuses",
                *(doc.get("aliases") or []),
            ]
        )
    )
    doc["purpose"] = (
        "Logical catalog of OptiSweep System/AGV/Tote APIs. Executed via Apidog on primary or via "
        "Ignition for Aveva. Includes unplanned-restart host-service checklist."
    )
    doc["client_tools"] = ["apidog", "ignition_gateway"]
    doc["system"] = old.get("system") or []
    doc["agvs"] = old.get("agvs") or []
    doc["totes"] = old.get("totes") or []
    doc["host_services_unplanned_restart"] = old.get("host_services_unplanned_restart") or []
    doc["architecture_notes"] = [
        *(doc.get("architecture_notes") or []),
        "Host services unplanned restart: " + ", ".join(doc["host_services_unplanned_restart"]),
    ]
    return doc


def build_aveva() -> dict:
    return _base(
        "aveva_hmi",
        title="AVEVA site HMI",
        aliases=["Aveva", "AVEVA", "Viva", "Overall System", "Initialize Tote"],
        purpose=(
            "Site/customer HMI: Overall System, AGVs, Totes, metrics, Zone Config, Initialize Tote, "
            "Tote Tasks, Exchange Settings. Fed via Ignition calling OptiSweep APIs. FORTNA has no "
            "direct Aveva access in the locked matrix — coach operator."
        ),
        when_to_use=[
            "Operator overall system / bag-out views",
            "Initialize Tote / Tote Tasks / Exchange Settings",
            "Zone Config overview",
            "Site-visible system blank/down",
        ],
        not_for=[
            "Tipper WebVisu MCP/alarms (tipper_hmi)",
            "FORTNA direct Aveva login (No access)",
            "SSMS deep dives",
        ],
        architecture_notes=[
            "Training sometimes says 'Viva' for UPS building HMIs — OptiSweep Aveva is distinct from tipper VISU.",
            "Ignition exposes APIs so Aveva can request startup/shutdown/closeout/tote actions.",
            "Operator-only access per role matrix.",
        ],
        audience_roles_typical=["operator"],
        role_paths={
            "operator": "Primary Aveva user.",
            "L1_support": "Coach only; no Aveva access.",
            "L2_support": "No Aveva access — use Apidog/SSMS/RMS instead.",
            "L3_support": "No Aveva access.",
        },
        screens_or_views=[
            {"id": "aveva_overall", "title": "Overall System", "purpose": "System-wide status / bag-out related controls.", "aliases": ["Overall System"], "key_points": ["blank/down", "bag-out"]},
            {"id": "aveva_agvs", "title": "AGVs page", "purpose": "Site AGV visualizations.", "aliases": ["AGVs"], "key_points": ["site view only"]},
            {"id": "aveva_totes", "title": "Totes / Initialize / Tasks / Exchange", "purpose": "Tote lifecycle and exchange settings.", "aliases": ["Initialize Tote", "Tote Tasks", "Exchange Settings"], "key_points": ["operator tote actions"]},
            {"id": "aveva_zone_config", "title": "Zone Config", "purpose": "Zone configuration overview.", "aliases": ["Zone Config"], "key_points": ["read overview; mutate via API is L2 risk"]},
        ],
        objects=[
            {"id": "initialize_tote", "label": "Initialize Tote", "capability_hints": ["tote_lifecycle_state"]},
            {"id": "exchange_settings", "label": "Exchange Settings", "capability_hints": ["tote_exchange_sequence"]},
            {"id": "zone_config", "label": "Zone Config", "capability_hints": ["zone_config_state"]},
        ],
        activities=[
            {
                "id": "aveva_overall_system",
                "label": "Overall system / bag-out / related pages",
                "observables": ["system blank/down", "bag-out controls"],
                "capability_hints": ["fleet_system_status", "bag_out_or_closeout_state"],
                "audience_roles": ["operator"],
            },
            {
                "id": "aveva_api_pages",
                "label": "Aveva API-backed pages (system/AGV/tote)",
                "observables": ["startup/shutdown/closeout responses", "tote init/tasks/exchange settings"],
                "capability_hints": ["sort_lifecycle_state", "tote_lifecycle_state", "tote_exchange_sequence"],
                "audience_roles": ["operator"],
            },
        ],
        distinguish_from={
            "tipper_hmi": "Station WebVisu — not Aveva.",
            "rms_ui": "Geek+ fleet UI for FORTNA remote.",
            "apidog": "FORTNA API client equivalent to what Aveva triggers via Ignition.",
        },
        gaps=["Per-control field dictionary from Day1 OCR still partial."],
        evidence_patterns=[r"AVEVA", r"Aveva", r"Viva", r"Initialize Tote", r"Zone Config"],
    )


def build_hospital() -> dict:
    return _base(
        "hospital_hmi",
        title="Hospital HMI / lane / stacklight UI",
        aliases=["hospital HMI", "hospital lane", "hospital stacklight", "hospital controller"],
        purpose=(
            "Hospital station / lane / stacklight UI for diversion and lane alarms. Corroborate with "
            "RMS routing and SSMS Hospital*/HospitalTags/Location models."
        ),
        when_to_use=[
            "Hospital diversion suspected",
            "Stacklight color / lane alarm at hospital",
            "AGVs diverting to hospital unexpectedly",
        ],
        not_for=["Tipper VISU screens", "Building ACB overview alone without hospital context"],
        architecture_notes=[
            "Architecture overview includes Hospital Controller alongside tippers and Geek+ RMS.",
            "OPC path also connects hospital tags via Ignition.",
        ],
        audience_roles_typical=["operator", "L1_support", "L2_support", "L3_support"],
        role_paths={
            "operator": "Primary hospital HMI / stacklight.",
            "L1_support": "Ask stacklight/lane; RMS routing cues.",
            "L2_support": "Remote HMI if available + SSMS hospital models.",
            "L3_support": "Persistent diversion ownership.",
        },
        screens_or_views=[
            {"id": "hospital_lane_ui", "title": "Hospital lane / station UI", "purpose": "Lane alarms and hospital station state.", "aliases": ["hospital lane"], "key_points": ["lane alarm", "diversion active"]},
            {"id": "hospital_stacklight", "title": "Hospital stacklight", "purpose": "At-a-glance diversion/alarm color.", "aliases": ["stacklight"], "key_points": ["ask color if remote"]},
        ],
        objects=[
            {"id": "hospital_tags", "label": "HospitalTagsModel / hospital tags", "capability_hints": ["hospital_diversion"]},
            {"id": "hospital_db", "label": "HospitalDatabaseModel", "capability_hints": ["hospital_diversion"]},
        ],
        activities=[
            {
                "id": "hospital_stacklight_lane",
                "label": "Hospital stacklight / lane alarm",
                "observables": ["stacklight color", "lane alarm"],
                "capability_hints": ["hospital_diversion", "lane_or_chute_state"],
                "audience_roles": ["operator", "L1_support", "L2_support"],
            }
        ],
        distinguish_from={
            "tipper_hmi": "Operator tipper stations — different HMI family.",
            "building_acb_hmi": "Area/bin overview — don't confuse with hospital lane.",
            "rms_ui": "Fleet routing view vs hospital local UI.",
        },
        gaps=["Full hospital HMI screen dictionary thinner than tipper VISU — expand from OM if sections exist."],
        evidence_patterns=[r"hospital", r"stacklight", r"Hospital Controller", r"divert"],
    )


def build_building_acb() -> dict:
    return _base(
        "building_acb_hmi",
        title="Building / ACB overview HMI",
        aliases=["ACB", "building overview", "area overview", "bin overview"],
        purpose="Area/bin/smalls/message panel overview during outages — site primary; FORTNA via report when remote.",
        when_to_use=["Area status during outages", "Bin/smalls/message panel checks"],
        not_for=["Hospital lane UI", "Tipper VISU", "Aveva tote initialize"],
        architecture_notes=["Don't confuse with hospital lane UI.", "Access? historically SME-open for L1 — treat as Access with coaching."],
        audience_roles_typical=["operator", "L1_support", "L2_support", "L3_support"],
        role_paths={
            "operator": "Primary building/ACB viewer.",
            "L1_support": "Ask site what overview shows.",
            "L2_support": "Remote if reachable; else site report.",
            "L3_support": "Deeper outage correlation.",
        },
        screens_or_views=[
            {"id": "acb_overview", "title": "ACB / area overview", "purpose": "Area/bin/smalls/message panel.", "aliases": ["ACB overview"], "key_points": ["outage context"]},
        ],
        objects=[],
        activities=[
            {
                "id": "acb_area_status",
                "label": "Check building/ACB area status",
                "observables": ["area down", "bin/smalls messages"],
                "capability_hints": ["fleet_system_status", "site_stoppage"],
                "audience_roles": ["operator", "L1_support", "L2_support"],
            }
        ],
        distinguish_from={
            "hospital_hmi": "Hospital lane/stacklight — different panel.",
            "aveva_hmi": "OptiSweep Aveva pages — different product surface.",
        },
        gaps=["Thin source detail — needs Day1/OM mining."],
        evidence_patterns=[r"\bACB\b", r"building overview", r"area status"],
    )


def build_site_interview() -> dict:
    return _base(
        "site_interview",
        title="Site interview / customer report",
        aliases=["ask site", "customer report", "site report", "photo from site"],
        purpose="Remote FORTNA gathers observables the customer/client can see: stacklight color, E-stop depressed, tipper alarm text/photo, messages flowing, chute open/closed.",
        when_to_use=[
            "No remote view of HMI",
            "Physical E-stop / floor symptoms",
            "L1 triage before deeper tooling",
        ],
        not_for=["Substitute for SSMS when L2 already has access", "Inventing site answers"],
        architecture_notes=["operator executes physical actions; FORTNA interviews and coaches."],
        audience_roles_typical=["L1_support", "L2_support", "L3_support"],
        role_paths={
            "L1_support": "Primary interview role.",
            "L2_support": "Interview + deeper tools.",
            "operator": "Answers / provides photos; executes physical steps.",
        },
        screens_or_views=[],
        objects=[
            {"id": "stacklight_color", "label": "Reported stacklight color"},
            {"id": "estop_depressed", "label": "Reported E-stop state"},
            {"id": "alarm_photo", "label": "Photo of VISU/HMI alarm"},
        ],
        activities=[
            {
                "id": "ask_physical_estop",
                "label": "Ask if any E-stop depressed",
                "observables": ["E-stop yes/no"],
                "capability_hints": ["e_stop_or_safety_stop"],
                "audience_roles": ["L1_support", "L2_support"],
            },
            {
                "id": "ask_tipper_alarm_photo",
                "label": "Ask tipper alarm text/color/photo",
                "observables": ["alarm text", "photo"],
                "capability_hints": ["tipper_station_fault"],
                "audience_roles": ["L1_support", "L2_support"],
            },
            {
                "id": "ask_messages_flowing",
                "label": "Ask if Chat/sort messages flowing",
                "observables": ["flowing / not"],
                "capability_hints": ["ups_chat_or_stunnel_health"],
                "audience_roles": ["L1_support"],
            },
        ],
        distinguish_from={"physical_floor": "Interview is remote Q&A; physical_floor is on-site action."},
        gaps=[],
        evidence_patterns=[r"ask", r"stacklight", r"photo", r"E-stop"],
    )


def build_physical_floor() -> dict:
    return _base(
        "physical_floor",
        title="Physical floor / operator station hardware",
        aliases=["floor", "on-site", "operator station", "LOTO", "E-stop", "tipper hardware"],
        purpose="On-site physical work: E-stop, LOTO, tipper/AGV physical recovery, stacklights, curtains, push-buttons. Customer/client executes; FORTNA coaches.",
        when_to_use=[
            "Physical E-stop reset",
            "LOTO / energy isolation",
            "AGV bump / remove / add on floor",
            "Tipper mechanical work after VISU diagnosis",
        ],
        not_for=["Remote SSMS/API as substitute for required physical isolation", "FORTNA performing E-stop"],
        architecture_notes=[
            "Each station has two tippers; tipper clamps tote from AGV.",
            "Physical E-stop = operator only per access matrix.",
        ],
        audience_roles_typical=["operator"],
        role_paths={
            "operator": "Executes all physical actions.",
            "L1_support": "Coaches only.",
            "L2_support": "Coaches + system-side Recover/Remove after floor work.",
            "L3_support": "Complex recovery ownership.",
        },
        screens_or_views=[],
        objects=[
            {"id": "estop_button", "label": "Physical E-stop"},
            {"id": "loto_valve", "label": "Pneumatic shut-off / LOTO"},
            {"id": "tipper_hardware", "label": "Tipper mechanical/pneumatic hardware"},
            {"id": "agv_on_floor", "label": "AGV physical recovery"},
        ],
        activities=[
            {
                "id": "operator_floor_recovery",
                "label": "Execute physical AGV / tipper recovery",
                "observables": ["robot cleared", "tipper mechanically OK"],
                "capability_hints": ["agv_physical_recovery", "tipper_station_fault"],
                "audience_roles": ["operator"],
            },
            {
                "id": "physical_estop_reset",
                "label": "Physical E-stop reset (operator only)",
                "observables": ["E-stop cleared"],
                "capability_hints": ["e_stop_or_safety_stop"],
                "audience_roles": ["operator"],
            },
        ],
        distinguish_from={
            "site_interview": "Talk vs act.",
            "tipper_hmi": "VISU is HMI; physical_floor is hardware/LOTO.",
        },
        gaps=["OM mechanical procedures exist as runbooks — link by capability, not duplicated here."],
        evidence_patterns=[r"tipper will clamp", r"two tippers", r"E-stop", r"LOTO"],
    )


def wrap_wcs_sql() -> dict:
    old = _load(CAT / "wcs_sql_catalog.json")
    tax = _tax_surface("wcs_sql")
    rel_caps, rel_fails = _caps_touching("wcs_sql")
    db_objects = []
    for db in old.get("databases") or []:
        db_objects.append(
            {
                "id": db.get("id"),
                "label": db.get("label"),
                "kind": "database",
                "aliases": db.get("aliases") or [],
                "purpose": db.get("purpose"),
                "when_to_use": db.get("when_to_use"),
                "not_for": db.get("not_for"),
                "module": db.get("module"),
            }
        )
    envelope = {
        "schema_version": "0.4",
        "catalog_id": "wcs_sql",
        "access_surface": "wcs_sql",
        "title": "WCS / Helix databases (SSMS)",
        "aliases": list(
            dict.fromkeys([*(tax.get("aliases") or []), "SSMS", "Helix DB", "WCS DB", "Helix2x", "robotics", "SorterSweeper"])
        ),
        "purpose": (
            "Remote read-oriented OptiSweep/Helix SQL via SSMS: Audit, GeekAgv, OPCComms, Robotics, "
            "SorterSweeper, EntityLogs (+ site Helix2x_*). Authoritative models/fields for L2/L3 diagnostics."
        ),
        "when_to_use": [
            "AGV/system active errors",
            "Robot location / dwell / shutdown staging",
            "Tote/exchange/bag-out/item/lane state",
            "Command GUID ↔ Geek task mapping (Audit)",
            "Tipper/tag/bits corroboration with VISU",
        ],
        "not_for": [
            "L1 how-to / operator access",
            "Inventing SELECT text the source does not provide",
            "Replacing live VISU alarm reading for tipper faults",
        ],
        "architecture_notes": [
            "WCS defaults DataContainers/PLCCommunication unused by OptiSweep; EntityLogs used for logging.",
            "Same capability often pairs with rms_ui (operator/L1) and wcs_api/apidog (L2/L3).",
            f"{len(old.get('models') or [])} models with field meanings — see models[].fields.",
        ],
        "audience_roles_typical": ["L2_support", "L3_support"],
        "role_paths": {
            "L1_support": "No SSMS how-to; escalate.",
            "L2_support": "Primary SSMS reader.",
            "L3_support": "Deep SQL + RCA.",
            "operator": "No access.",
        },
        "screens_or_views": [
            {
                "id": "ssms_object_explorer",
                "title": "SSMS Object Explorer — Helix/OptiSweep DBs",
                "purpose": "Open site Helix2x_* / OptiSweep databases and models.",
                "aliases": ["SSMS", "Object Explorer"],
                "key_points": ["pick DB by job", "read-only first"],
            }
        ],
        "objects": db_objects,
        "activities": _activities_from_cross("wcs_sql")
        or [
            {
                "id": "ssms_open_db",
                "label": "Open SSMS and select Helix/OptiSweep database for the job",
                "observables": ["connected", "correct DB selected"],
                "capability_hints": rel_caps[:5],
                "audience_roles": ["L2_support", "L3_support"],
            }
        ],
        "related_capabilities": rel_caps,
        "related_failure_patterns": rel_fails,
        "distinguish_from": {
            "wcs_api": "Live API vs persisted DB state — corroborate both for AGV status.",
            "rms_ui": "Overview vs authoritative rows.",
            "tipper_hmi": "Live VISU vs Tipper* tables.",
        },
        "gaps": old.get("gaps")
        or [
            "OPCComms column semantics still thin",
            "Some ChargingThreshold/ItemModels PascalCase needs_sme",
        ],
        "evidence": _evidence_for([r"SSMS", r"Helix", r"Robotics", r"SorterSweeper", r"SystemActiveError"], limit=10),
        "source_refs": [
            {"source": "training_video_day2"},
            {"source": "active_agv_error_query_1"},
            {"source": "optisweep_training_slides"},
        ],
        # preserve deep body
        "wcs_default_databases": old.get("wcs_default_databases"),
        "databases": old.get("databases"),
        "sql_agent_jobs": old.get("sql_agent_jobs"),
        "models": old.get("models"),
        "description": old.get("description"),
    }
    return envelope


def build_tipper_passthrough() -> dict:
    """Align tipper catalog key name screens → screens_or_views without losing data."""
    old = _load(CAT / "tipper_hmi_catalog.json")
    if "screens_or_views" not in old and "screens" in old:
        old["screens_or_views"] = old["screens"]
    if "objects" not in old:
        old["objects"] = [
            {"id": s.get("id"), "label": s.get("title"), "kind": "visu_screen", "aliases": s.get("aliases") or []}
            for s in old.get("screens_or_views") or old.get("screens") or []
        ]
    # ensure common keys exist
    old.setdefault("related_capabilities", _caps_touching("tipper_hmi")[0])
    old.setdefault("related_failure_patterns", _caps_touching("tipper_hmi")[1])
    old.setdefault("distinguish_from", old.get("distinguish_from") or {})
    return old


def write_schema_doc() -> None:
    schema = {
        "schema_version": "0.4",
        "catalog_kind": "access_surface",
        "required_fields": COMMON_KEYS,
        "field_notes": {
            "aliases": "Human and source synonyms for retrieval",
            "when_to_use": "list of job triggers",
            "not_for": "anti-goals / wrong surfaces",
            "screens_or_views": "UI pages or tool views [{id,title,purpose,aliases,key_points}]",
            "objects": "DBs, APIs, hardware, named entities [{id,label,aliases,capability_hints}]",
            "activities": "Executable checks [{id,label,observables,capability_hints,audience_roles}]",
            "evidence": "[{source,kind,snippet}] — no invented meanings",
        },
    }
    (CAT / "surface_catalog_schema.json").write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    write_schema_doc()
    writers = {
        "rms_ui_catalog.json": build_rms,
        "ignition_gateway_catalog.json": build_ignition,
        "stunnel_catalog.json": build_stunnel,
        "event_viewer_catalog.json": build_event_viewer,
        "apidog_catalog.json": build_apidog,
        "wcs_api_catalog.json": build_wcs_api_envelope,
        "aveva_hmi_catalog.json": build_aveva,
        "hospital_hmi_catalog.json": build_hospital,
        "building_acb_hmi_catalog.json": build_building_acb,
        "site_interview_catalog.json": build_site_interview,
        "physical_floor_catalog.json": build_physical_floor,
        "wcs_sql_catalog.json": wrap_wcs_sql,
        "tipper_hmi_catalog.json": build_tipper_passthrough,
    }
    for name, fn in writers.items():
        doc = fn()
        path = CAT / name
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
        missing = [k for k in ("aliases", "when_to_use", "not_for", "activities", "role_paths") if k not in doc]
        print(f"wrote {name} missing={missing or 'none'} acts={len(doc.get('activities') or [])}")

    # update index
    index = _load(CAT / "catalog_index.json")
    index["surface_catalog_schema"] = "docs/ontology/catalogs/surface_catalog_schema.json"
    index["catalogs"]["building_acb_hmi"] = "docs/ontology/catalogs/building_acb_hmi_catalog.json"
    index["catalogs"]["site_interview"] = "docs/ontology/catalogs/site_interview_catalog.json"
    index["catalogs"]["physical_floor"] = "docs/ontology/catalogs/physical_floor_catalog.json"
    index["catalogs"]["schema"] = "docs/ontology/catalogs/surface_catalog_schema.json"
    index["description"] = (
        "Index of machine-retrievable system documentation catalogs for Stage 6 mini-RAG. "
        "All access-surface catalogs share surface_catalog_schema.json (aliases, when_to_use, "
        "activities, objects, evidence, …)."
    )
    (CAT / "catalog_index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    print("updated catalog_index.json")


if __name__ == "__main__":
    main()
