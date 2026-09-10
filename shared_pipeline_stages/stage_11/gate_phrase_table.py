from __future__ import annotations

import re
from typing import Any

GATE_PHRASE_DOC_ID = "gate_phrases"
GATE_PHRASE_DOC_TYPE = "gate_phrase_table"
GATE_PHRASE_DATASET = "gate_phrase_tables"
GATE_PHRASE_BUNDLE_REL = "gate_phrase_tables/documents.json"

# Seed CAT-1 / canonical keys. App KeywordSignalExtractor loads these from Cosmos.
SEED_LEGACY_SIGNAL_PHRASES: dict[str, list[str]] = {
    "agvs_stopped": [
        "agvs stopped",
        "agvs are stopped",
        "agvs aren't moving",
        "robots stopped",
        "nothing is moving",
        "robotic system is not responding",
        "small sort is not running",
    ],
    "no_rms_alarm": [
        "no rms alarms",
        "rms showing no alarms",
        "no alarms in rms",
        "rms no alarms",
    ],
    "bag_out_stopped": [
        "bag out stopped",
        "system stopped at bag-out",
        "manually bagging out",
        "bag out started and stopped again",
    ],
    "hospital_induct_blocked": [
        "hospital can't add totes",
        "can't induct totes",
        "hospital induct blocked",
        "hospital can't induct totes",
        "we can remove totes but can't add",
    ],
    "pairing_failure": [
        "zone unable to get a pair",
        "unable to get a pair",
        "pairing failure",
        "robot not mapped",
    ],
    "amr_hospital_diversion": [
        "every amr goes to the hospital",
        "amrs going to hospital",
        "going to the hospital lane",
    ],
    "hmi_fault": [
        "hospital hmi fault",
        "hmi is showing a fault",
        "question marks on the hmi",
    ],
    "web_app_fault": [
        "webapplication is faulted",
        "webservice application is faulted",
        "failed executing dbcommand",
    ],
}

SEED_CANONICAL_SIGNAL_PHRASES: dict[str, list[str]] = {
    "site_wide_motion_stoppage": list(SEED_LEGACY_SIGNAL_PHRASES["agvs_stopped"]),
    "rms_alarm_absence": list(SEED_LEGACY_SIGNAL_PHRASES["no_rms_alarm"]),
    "bagout_sequence_stoppage": list(SEED_LEGACY_SIGNAL_PHRASES["bag_out_stopped"]),
    "hospital_induct_blocked": list(SEED_LEGACY_SIGNAL_PHRASES["hospital_induct_blocked"]),
    "zone_pairing_failure": list(SEED_LEGACY_SIGNAL_PHRASES["pairing_failure"]),
    "hospital_lane_diversion": list(SEED_LEGACY_SIGNAL_PHRASES["amr_hospital_diversion"]),
    "hospital_hmi_fault": list(SEED_LEGACY_SIGNAL_PHRASES["hmi_fault"]),
    "wcs_webapplication_fault": list(SEED_LEGACY_SIGNAL_PHRASES["web_app_fault"]),
}

SEED_COMPONENT_PHRASES: dict[str, list[str]] = {
    "agv": ["agv", "agvs", "amr", "amrs", "robot", "robots"],
    "rms": ["rms", "fleet status"],
    "hospital": ["hospital", "hospital lane", "hospital hmi"],
    "hmi": ["hmi"],
    "bag_out": ["bag out", "bag-out", "bagging out"],
    "pairing": ["pair", "pairing", "mapped", "roster"],
}

# Rules used to attach free-form playbook operator examples onto CAT-1 / canonical keys.
_CLASSIFIER_RULES: list[tuple[str, str, tuple[str, ...]]] = [
    ("legacy", "agvs_stopped", ("aren't moving", "are stopped", "agvs stopped", "robots stopped", "nothing is moving", "not moving", "not responding", "small sort is not running")),
    ("legacy", "no_rms_alarm", ("no rms alarm", "rms showing no alarm", "no alarm", "rms no alarm")),
    ("legacy", "bag_out_stopped", ("bag out", "bag-out", "bagging out")),
    ("legacy", "hospital_induct_blocked", ("can't add tote", "cannot add tote", "can't induct", "cannot induct", "induct blocked", "unable to induct")),
    ("legacy", "pairing_failure", ("unable to get a pair", "get a pair", "pairing failure", "not mapped")),
    ("legacy", "amr_hospital_diversion", ("goes to the hospital", "going to hospital", "hospital lane")),
    ("legacy", "hmi_fault", ("hmi", "question mark")),
    ("legacy", "web_app_fault", ("webapplication", "web application", "webservice", "dbcommand", "event viewer")),
    ("canonical", "site_wide_motion_stoppage", ("aren't moving", "are stopped", "agvs stopped", "robots stopped", "nothing is moving", "not moving")),
    ("canonical", "rms_alarm_absence", ("no rms alarm", "rms showing no alarm", "no alarm")),
    ("canonical", "bagout_sequence_stoppage", ("bag out", "bag-out", "bagging out")),
    ("canonical", "hospital_induct_blocked", ("can't add tote", "cannot add tote", "can't induct", "induct blocked")),
    ("canonical", "zone_pairing_failure", ("unable to get a pair", "pairing failure", "not mapped")),
    ("canonical", "hospital_lane_diversion", ("goes to the hospital", "going to hospital", "hospital lane")),
    ("canonical", "hospital_hmi_fault", ("hmi", "question mark")),
    ("canonical", "wcs_webapplication_fault", ("webapplication", "web application", "webservice", "dbcommand")),
    ("component", "agv", ("agv", "amr", "robot")),
    ("component", "rms", ("rms",)),
    ("component", "hospital", ("hospital",)),
    ("component", "hmi", ("hmi",)),
    ("component", "bag_out", ("bag out", "bag-out", "bagging out")),
    ("component", "pairing", ("pair", "pairing", "mapped", "roster")),
]


def build_gate_phrase_table(
    *,
    publish_version_id: str,
    playbooks: list[dict[str, Any]],
    prior_table: dict[str, Any] | None = None,
    learned_phrases: list[str] | None = None,
) -> dict[str, Any]:
    legacy = _copy_phrase_map(SEED_LEGACY_SIGNAL_PHRASES)
    canonical = _copy_phrase_map(SEED_CANONICAL_SIGNAL_PHRASES)
    components = _copy_phrase_map(SEED_COMPONENT_PHRASES)

    if prior_table:
        _merge_phrase_map(legacy, prior_table.get("legacy_signal_phrases") or prior_table.get("payload", {}).get("legacy_signal_phrases") or {})
        _merge_phrase_map(canonical, prior_table.get("canonical_signal_phrases") or prior_table.get("payload", {}).get("canonical_signal_phrases") or {})
        _merge_phrase_map(components, prior_table.get("component_phrases") or prior_table.get("payload", {}).get("component_phrases") or {})

    for playbook in playbooks:
        phrases = [
            *[str(item) for item in playbook.get("support_user_language_examples") or []],
            *[str(item) for item in playbook.get("observed_entry_symptoms") or []],
        ]
        for phrase in phrases:
            _classify_and_add(phrase, legacy=legacy, canonical=canonical, components=components)

    for phrase in learned_phrases or []:
        _classify_and_add(phrase, legacy=legacy, canonical=canonical, components=components)

    payload = {
        "legacy_signal_phrases": _normalize_phrase_map(legacy),
        "canonical_signal_phrases": _normalize_phrase_map(canonical),
        "component_phrases": _normalize_phrase_map(components),
    }
    return {
        "id": GATE_PHRASE_DOC_ID,
        "doc_type": GATE_PHRASE_DOC_TYPE,
        "publish_version_id": publish_version_id,
        "record_id": GATE_PHRASE_DOC_ID,
        "payload": payload,
        **payload,
    }


def load_gate_phrase_table(doc_or_path_payload: dict[str, Any] | None) -> dict[str, Any] | None:
    if not doc_or_path_payload:
        return None
    if str(doc_or_path_payload.get("doc_type") or "") == GATE_PHRASE_DOC_TYPE:
        return doc_or_path_payload
    if doc_or_path_payload.get("legacy_signal_phrases") or doc_or_path_payload.get("payload"):
        return doc_or_path_payload
    return None


def match_query_against_gate_table(query: str, table: dict[str, Any]) -> set[str]:
    """Return legacy CAT-1 keys whose phrases are present in the query text."""
    legacy = table.get("legacy_signal_phrases") or (table.get("payload") or {}).get("legacy_signal_phrases") or {}
    query_l = _normalize_phrase(query)
    hits: set[str] = set()
    for key, phrases in legacy.items():
        for phrase in phrases or []:
            needle = _normalize_phrase(str(phrase))
            if needle and needle in query_l:
                hits.add(str(key))
                break
    return hits


def smoke_gate_phrase_table(table: dict[str, Any]) -> dict[str, Any]:
    query = "agvs aren't moving, rms showing no alarms"
    hits = match_query_against_gate_table(query, table)
    required = {"agvs_stopped", "no_rms_alarm"}
    missing = sorted(required - hits)
    return {
        "query": query,
        "hits": sorted(hits),
        "required": sorted(required),
        "missing": missing,
        "passed": not missing,
    }


def _classify_and_add(
    phrase: str,
    *,
    legacy: dict[str, list[str]],
    canonical: dict[str, list[str]],
    components: dict[str, list[str]],
) -> None:
    normalized = _normalize_phrase(phrase)
    if not normalized or len(normalized) < 3:
        return
    matched = False
    for family, key, needles in _CLASSIFIER_RULES:
        if any(needle in normalized for needle in needles):
            matched = True
            if family == "legacy":
                legacy.setdefault(key, []).append(normalized)
            elif family == "canonical":
                canonical.setdefault(key, []).append(normalized)
            else:
                components.setdefault(key, []).append(normalized)
    if not matched:
        # Keep unclassified operator speech under a catch-all canonical bucket for audit.
        canonical.setdefault("unmapped_operator_speech", []).append(normalized)


def _copy_phrase_map(source: dict[str, list[str]]) -> dict[str, list[str]]:
    return {key: list(values) for key, values in source.items()}


def _merge_phrase_map(target: dict[str, list[str]], incoming: dict[str, Any]) -> None:
    if not isinstance(incoming, dict):
        return
    for key, values in incoming.items():
        if not isinstance(values, list):
            continue
        target.setdefault(str(key), []).extend(str(item) for item in values if str(item).strip())


def _normalize_phrase_map(source: dict[str, list[str]]) -> dict[str, list[str]]:
    normalized: dict[str, list[str]] = {}
    for key, values in source.items():
        seen: set[str] = set()
        rows: list[str] = []
        for value in values:
            phrase = _normalize_phrase(value)
            if not phrase or phrase in seen:
                continue
            seen.add(phrase)
            rows.append(phrase)
        if rows:
            normalized[str(key)] = sorted(rows)
    return normalized


def _normalize_phrase(text: str) -> str:
    value = str(text or "").casefold().strip()
    value = re.sub(r"\s+", " ", value)
    return value.strip(" .,;:!?'\"")
