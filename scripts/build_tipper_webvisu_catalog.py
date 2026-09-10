"""Mine WebVisu / VISU evidence from OM + Day2 into tipper_hmi_catalog.json."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OM_BUNDLE = (
    REPO
    / "operationalknowledgeingestion/data/output/manual_optisweep_om_v3/stage_1_source_bundle/source_bundle.json"
)
DAY2_SEGS = (
    REPO
    / "operationalknowledgeingestion/data/output/training_video_day2/stage_1_source_bundle/training_video_slide_segments.json"
)
SQL = REPO / "docs/ontology/catalogs/wcs_sql_catalog.json"
OUT = REPO / "docs/ontology/catalogs/tipper_hmi_catalog.json"
SRC_DIR = REPO / "docs/ontology/sources/om_manual"


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def _om_visu_sections() -> list[dict]:
    data = json.loads(OM_BUNDLE.read_text(encoding="utf-8"))
    screens = []
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    for section in data.get("sections") or []:
        sid = str(section.get("section_id") or "")
        if "visu" not in sid.lower() and "tipper_machine_control" not in sid.lower():
            continue
        title = section.get("title") or section.get("heading") or sid
        text = _clean(str(section.get("text") or section.get("text_preview") or ""))
        short = sid.replace(
            "optisweep_operation_and_maintenance_manual_final_1_", ""
        )
        (SRC_DIR / f"{short}.txt").write_text(text, encoding="utf-8")
        screen_id = "unknown"
        if "visu_mcp" in sid or "machine_control" in sid:
            screen_id = "visu_mcp_dual"
        elif "visu_data" in sid:
            screen_id = "visu_data"
        elif "visu_mancontrol" in sid:
            screen_id = "visu_mancontrol"
        elif "visu_mds" in sid:
            screen_id = "visu_mds"
        elif "visu_io" in sid:
            screen_id = "visu_io_diag"
        elif "visu_alarm" in sid:
            screen_id = "visu_alarm"
        # pull item descriptions when present
        items = []
        for match in re.finditer(
            r"(?:Item Description|\d+)\s+([A-Z][^.]{10,160}\.)",
            text,
        ):
            items.append(match.group(1).strip())
        purpose = text[:400]
        # better purpose: first substantive sentence after title cue
        for cue in (
            "The Tipper Machine Control Panel",
            'The "Machine Data" screen',
            'The "Visu_Alarm" screen',
            "NOTE:",
            "An informational banner",
        ):
            idx = text.find(cue)
            if idx >= 0:
                purpose = text[idx : idx + 450]
                break
        screens.append(
            {
                "id": screen_id,
                "om_section_id": sid,
                "title": title,
                "purpose": purpose,
                "aliases": _aliases_for(screen_id),
                "key_points": _keypoints(screen_id, text),
                "source_refs": [
                    {"source": "manual_optisweep_om_v3", "section_id": sid},
                    {"source": "docs/ontology/sources/om_manual/" + short + ".txt"},
                ],
            }
        )
    return screens


def _aliases_for(screen_id: str) -> list[str]:
    return {
        "visu_mcp_dual": ["VISU_MCP_DUAL", "Tipper Machine Control Panel", "MCP dual"],
        "visu_data": ["VISU_DATA", "Data screen"],
        "visu_mancontrol": ["VISU_MANCONTROL", "Manual Control", "ManControl"],
        "visu_mds": ["VISU_MDS", "Machine Data", "MDS"],
        "visu_io_diag": ["VISU_IO_DIAG", "IO Diagnostics", "visu_io"],
        "visu_alarm": ["VISU_ALARM", "Alarm screen"],
    }.get(screen_id, [])


def _keypoints(screen_id: str, text: str) -> list[str]:
    points: list[str] = []
    lower = text.lower()
    if screen_id == "visu_mcp_dual":
        points = [
            "Controls tipper movement and allows fault reset / cycle control on the dual MCP screen.",
            "Primary operator station tipper control surface (not Aveva).",
        ]
    elif screen_id == "visu_data":
        points = [
            "Informational banner displays alarms or informational messages.",
            "Operator station HMI data view for tipper/station status.",
        ]
    elif screen_id == "visu_mancontrol":
        points = [
            "Manual control screen; maintenance login sees deeper controls than operator.",
            "Used when stopping cycle for manual axis positioning (OM procedures).",
        ]
    elif screen_id == "visu_mds":
        points = [
            "Machine Data holds parameters for axes Z1, A1, Z2, A2.",
            "Do not change unless a motor is replaced; used for home offset / recommissioning.",
        ]
    elif screen_id == "visu_io_diag":
        points = [
            "Read-only IO diagnostics for troubleshooting tipper inputs/outputs.",
            "Use for L2/L3 deeper tipper IO when alarms are unclear.",
        ]
    elif screen_id == "visu_alarm":
        points = [
            "Lists tipper alarms with timestamps.",
            "SHOW HISTORY shows last 1500 alarm records.",
        ]
    if "read-only" in lower:
        points.append("Screen is read-only where noted in OM.")
    if "maintenance" in lower:
        points.append("Some views differ for maintenance login vs operator.")
    return points


def _day2_evidence() -> list[dict]:
    if not DAY2_SEGS.exists():
        return []
    segs = json.loads(DAY2_SEGS.read_text(encoding="utf-8-sig"))
    evidence = []
    patterns = [
        r"heartbeat",
        r"web\s*view",
        r"web\s*visu",
        r"tipper.*faulted",
        r"OPC Connections",
        r"ready to tip",
        r"two tippers",
        r"tipper count",
        r"operator stations",
    ]
    pat = re.compile("|".join(patterns), re.I)
    for seg in segs:
        transcript = str(seg.get("transcript_text") or "")
        ocr = str(seg.get("ocr_text") or "")
        blob = transcript + " " + ocr
        if not pat.search(blob):
            continue
        snippet = _clean(transcript)[:320] or _clean(ocr)[:320]
        if len(snippet) < 40:
            continue
        evidence.append(
            {
                "source": "training_video_day2",
                "kind": "transcript" if transcript else "ocr",
                "snippet": snippet,
            }
        )
        if len(evidence) >= 12:
            break
    return evidence


def _sql_tipper_models() -> list[dict]:
    sql = json.loads(SQL.read_text(encoding="utf-8"))
    out = []
    for model in sql.get("models") or []:
        name = str(model.get("name") or "")
        caps = [str(c) for c in model.get("capability_hints") or []]
        if "tipper_station_fault" not in caps and "Tipper" not in name and "Bits" not in name:
            if name not in {"TagModel", "TagReadWriteLogs"}:
                continue
        fields = [
            {"name": f.get("name"), "meaning": f.get("meaning"), "needs_sme": f.get("needs_sme")}
            for f in (model.get("fields") or [])[:10]
            if f.get("name")
        ]
        out.append(
            {
                "database": model.get("database"),
                "model": name,
                "purpose": model.get("purpose"),
                "capability_hints": caps,
                "fields_sample": fields,
            }
        )
    return out


def main() -> None:
    screens = _om_visu_sections()
    evidence = _day2_evidence()
    # ensure heartbeat evidence present
    evidence.insert(
        0,
        {
            "source": "training_video_day2",
            "kind": "transcript",
            "snippet": (
                "Check to make sure that tippers are getting heartbeats. If the heartbeats "
                "are flat lines ... If you're not getting heartbeats, you have to restart "
                "Opti Sweep because OPC is stupid."
            ),
        },
    )
    evidence.insert(
        1,
        {
            "source": "training_video_day2",
            "kind": "ocr+transcript",
            "snippet": (
                "Ignition Gateway UI — Config → OPC → OPC Connections: tipper 7 and 8 "
                "powered off show Faulted. Web view can read tags (Designer screenshots)."
            ),
        },
    )

    catalog = {
        "schema_version": "0.4",
        "catalog_id": "tipper_hmi",
        "access_surface": "tipper_hmi",
        "title": "Tipper station HMI — WebVisu / VISU (not Aveva)",
        "aliases": [
            "webvisu",
            "WebVisu",
            "VISU",
            "visu",
            "tipper HMI",
            "operator station HMI",
            "Visu_MCP_Dual",
        ],
        "purpose": (
            "Operator-station tipper HMI (CODESYS/WebVisu-style VISU screens at the machine). "
            "Primary for tipper faults, alarms, IO diagnostics, manual axis control, and "
            "machine-data parameters. Distinct from Aveva building HMI and from Ignition "
            "Gateway admin UI — though tipper heartbeats/OPC health are checked via Ignition "
            "and may require OptiSweep restart when flatlined."
        ),
        "when_to_use": [
            "Tipper alarm / fault at operator station",
            "Need alarm history or IO diagnostics on tipper",
            "Manual axis positioning / stop cycle (maintenance)",
            "Motor replace → VISU_MDS axis parameters / home offsets",
            "After unplanned restart: confirm tipper heartbeats (with Ignition OPC)",
        ],
        "not_for": [
            "Aveva Overall System / Zone Config / Initialize Tote (use aveva_hmi)",
            "RMS AGV fleet overview (use rms_ui)",
            "SSMS tipper tables as substitute for reading live VISU alarm text",
            "Physical E-stop (physical_floor / e_stop_or_safety_stop)",
        ],
        "architecture_notes": [
            "Each operator station has two tippers (Day2: 8 stations → 16 tippers).",
            "Ignition OPC reads/writes tipper tags; SorterSweeper tracks tote state at tipper.",
            "WebVisu/VISU is the on-station HMI; Ignition Designer/web view can also read tags.",
            "Heartbeat flatline after Ignition comes up late → restart OptiSweep (OPC path).",
            "Physical tipper actions and LOTO remain operator/customer; FORTNA coaches remotely.",
        ],
        "audience_roles_typical": ["operator", "L1_support", "L2_support", "L3_support"],
        "role_paths": {
            "operator": "Primary user of VISU screens; executes physical tipper/LOTO steps.",
            "L1_support": "Ask alarm text/color/photo or remote-view VISU if available; do not treat as SSMS how-to.",
            "L2_support": "Deeper VISU_IO_DIAG / alarm history + SSMS Tipper/Tag/Bits; Ignition OPC + heartbeat.",
            "L3_support": "Persistent tipper faults, axis/MDS parameter work with OM procedures.",
        },
        "screens": screens,
        "activities": [
            {
                "id": "visu_read_alarm",
                "label": "Open VISU_ALARM — read active tipper alarms + history",
                "screen": "visu_alarm",
                "observables": [
                    "alarm list with timestamps",
                    "SHOW HISTORY last 1500 records",
                    "no active alarms",
                ],
                "capability_hints": ["tipper_station_fault"],
                "audience_roles": ["operator", "L1_support", "L2_support"],
            },
            {
                "id": "visu_data_banner",
                "label": "VISU_DATA — check informational banner / station data",
                "screen": "visu_data",
                "observables": ["banner alarm or info message", "station data fields"],
                "capability_hints": ["tipper_station_fault"],
                "audience_roles": ["operator", "L1_support", "L2_support"],
            },
            {
                "id": "visu_mcp_fault_reset",
                "label": "VISU_MCP_DUAL — tipper movement control / fault reset",
                "screen": "visu_mcp_dual",
                "observables": ["tipper movement controls available", "fault reset succeeds"],
                "capability_hints": ["tipper_station_fault"],
                "audience_roles": ["operator", "L2_support"],
            },
            {
                "id": "visu_io_diag_troubleshoot",
                "label": "VISU_IO_DIAG — read-only IO troubleshooting",
                "screen": "visu_io_diag",
                "observables": ["IO points state", "mismatch vs expected"],
                "capability_hints": ["tipper_station_fault"],
                "audience_roles": ["L2_support", "L3_support", "operator"],
            },
            {
                "id": "visu_mancontrol_stop_cycle",
                "label": "VISU_MANCONTROL — stop cycle / manual axis (maintenance view)",
                "screen": "visu_mancontrol",
                "observables": ["cycle stopped", "manual axis positioning available"],
                "capability_hints": ["tipper_station_fault", "agv_physical_recovery"],
                "audience_roles": ["operator", "L2_support", "L3_support"],
            },
            {
                "id": "visu_mds_axis_params",
                "label": "VISU_MDS — axis parameters Z1/A1/Z2/A2 (motor replace / home offset)",
                "screen": "visu_mds",
                "observables": ["axis parameters", "home offset values"],
                "capability_hints": ["tipper_station_fault"],
                "audience_roles": ["L2_support", "L3_support", "operator"],
            },
            {
                "id": "webvisu_heartbeat_check",
                "label": "Confirm tipper WebVisu/OPC heartbeats (with Ignition)",
                "screen": None,
                "observables": [
                    "heartbeats present",
                    "heartbeat flatline",
                    "OPC tipper connection Faulted",
                ],
                "capability_hints": [
                    "opc_connection_or_tipper_heartbeat",
                    "gateway_health",
                    "wcs_service_health",
                ],
                "audience_roles": ["L2_support", "L3_support", "L1_support"],
                "related_surfaces": ["ignition_gateway"],
                "notes": "Flatline after Ignition late start → restart OptiSweep (Day2 unplanned restart).",
            },
            {
                "id": "ask_tipper_alarm_photo",
                "label": "Site interview — tipper alarm text/color/photo when VISU not remote",
                "screen": None,
                "observables": ["alarm text", "stacklight/alarm color", "photo of VISU"],
                "capability_hints": ["tipper_station_fault"],
                "audience_roles": ["L1_support", "L2_support"],
                "related_surfaces": ["site_interview"],
            },
        ],
        "corroborating_sql_models": _sql_tipper_models(),
        "related_capabilities": [
            "tipper_station_fault",
            "opc_connection_or_tipper_heartbeat",
            "gateway_health",
            "tote_exchange_sequence",
            "e_stop_or_safety_stop",
        ],
        "related_failure_patterns": [
            "tipper_fault",
            "opc_connection_faulted",
            "unplanned_restart",
        ],
        "distinguish_from": {
            "aveva_hmi": "Building/overall system HMI fed via Ignition APIs — not tipper VISU screens.",
            "ignition_gateway": "OPC Connections / gateway admin — corroborates tipper power/heartbeat, not MCP controls.",
            "hospital_hmi": "Hospital lane/stacklight UI — different station family.",
            "rms_ui": "Geek+ fleet UI — not tipper axis/IO.",
        },
        "gaps": [
            "Full tag-by-tag visu_io map beyond OM figure callouts not extracted.",
            "Exact WebVisu URL/IP per site not in corpus — site-specific.",
            "Day1 tipper hardware walkthrough OCR still noisy; prefer OM screen text.",
        ],
        "evidence": evidence,
        "source_refs": [
            {"source": "manual_optisweep_om_v3", "sections": "4.1.2.1–4.1.2.6 VISU_*"},
            {"source": "training_video_day2", "topics": "OPC tippers, heartbeat, unplanned restart"},
            {"source": "support_roles_components_and_adjacency.md"},
            {"source": "docs/ontology/sources/om_manual/"},
        ],
    }
    OUT.write_text(json.dumps(catalog, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} screens={len(screens)} activities={len(catalog['activities'])} evidence={len(evidence)}")


if __name__ == "__main__":
    main()
