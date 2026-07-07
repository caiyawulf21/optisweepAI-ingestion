from __future__ import annotations

import re
from typing import Any

from shared_pipeline_stages.stage_8.schemas import RunbookSearchMatch

PLACEHOLDER_BOILERPLATE = re.compile(
    r"^(procedure needed to|runbook needed to|steps needed to|check needed to)\s+",
    re.IGNORECASE,
)

CHECK_NODE_PATTERN = re.compile(
    r"\b(determine|check|whether|verify|inspect|review|confirm|assess|identify whether)\b",
    re.IGNORECASE,
)

RECOVERY_PREP_RUNBOOK_PATTERN = re.compile(
    r"\b("
    r"before entering|entering the grid|inside the grid|for agv recovery|"
    r"gather.*fault|prepare.*recovery|physical agv recovery|dance floor"
    r")\b",
    re.IGNORECASE,
)

STATUS_CHECK_RUNBOOK_PATTERN = re.compile(
    r"\b("
    r"check overall system|system fault|active agv fault|inspect.*rms|"
    r"review.*rms|determine whether.*fault|roster|map monitor|system errors"
    r")\b",
    re.IGNORECASE,
)

DOMAIN_ANCHORS: dict[str, tuple[str, ...]] = {
    "event viewer": ("event viewer", "7031", "service control manager", "application log", "system log"),
    "optisweep": ("optisweep", "getagvstatuses", "get agv status"),
    "ignition": ("ignition", "gateway", "systems overview"),
    "rms": ("rms", "geek+", "overall system", "robot roster", "agv fault", "system fault"),
    "hmi": ("hmi", ".net control", "question mark", "blank state"),
    "windows services": ("windows services", "services.msc", "service state"),
    "agv": ("agv", "robot", "fleet", "out of sync", "roster", "mapping"),
    "hospital": ("hospital", "tote", "hospital lane"),
    "api": ("api", "endpoint", "http", "response", "getagvstatuses"),
}

STOPWORDS = {
    "a",
    "an",
    "and",
    "for",
    "in",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
    "whether",
    "needed",
    "procedure",
    "runbook",
    "using",
    "approved",
    "support",
    "site",
    "check",
    "confirm",
    "inspect",
    "review",
    "determine",
}

PROCEDURE_TYPE_PREFERRED: dict[str, tuple[str, ...]] = {
    "diagnostic_decision": ("diagnostic", "reference", "monitoring"),
    "branching_condition": ("diagnostic", "reference", "monitoring"),
    "validation_gate": ("diagnostic", "monitoring", "reference"),
    "procedure_reference": ("recovery", "operation", "diagnostic"),
    "escalation_gate": ("reference", "diagnostic"),
    "recovery_phase_marker": ("reference", "monitoring", "recovery"),
}

INTENT_OVERRIDE_MARGIN = 0.08

CANONICAL_SOURCE_BOOST: dict[str, float] = {
    "manual": 0.08,
    "sop": 0.07,
    "sme": 0.06,
}

TRAINING_SOURCE_TYPES = frozenset(
    {"training_video", "training_slide", "training_transcript"}
)
TRAINING_SOURCE_PENALTY = -0.06


def normalize_placeholder_text(text: str) -> str:
    cleaned = PLACEHOLDER_BOILERPLATE.sub("", str(text or "").strip())
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def build_retrieval_query_text(
    node: dict[str, Any],
    *,
    affected_systems: list[str] | None = None,
) -> str:
    node_type = str(node.get("node_type") or "").strip()
    title = str(node.get("title") or "").strip()
    intent = str(node.get("intent") or node.get("goal") or "").strip()
    placeholder = normalize_placeholder_text(
        str(node.get("runbook_placeholder") or node.get("needed_runbook_capability") or "")
    )
    systems = " ".join(affected_systems or [])
    return re.sub(
        r"\s+",
        " ",
        " ".join(part for part in [node_type, title, intent, placeholder, systems] if part),
    ).strip()


def node_check_text(node: dict[str, Any]) -> str:
    return " ".join(
        part
        for part in [
            str(node.get("title") or ""),
            str(node.get("intent") or node.get("goal") or ""),
            normalize_placeholder_text(str(node.get("runbook_placeholder") or "")),
        ]
        if part
    )


def node_is_check_phase(node: dict[str, Any]) -> bool:
    node_type = str(node.get("node_type") or "")
    if node_type not in {"diagnostic_decision", "branching_condition", "validation_gate"}:
        return False
    text = node_check_text(node)
    return bool(CHECK_NODE_PATTERN.search(text))


def runbook_is_recovery_prep(runbook: dict[str, Any] | None, match: RunbookSearchMatch) -> bool:
    text = runbook_match_text(match, runbook)
    return bool(RECOVERY_PREP_RUNBOOK_PATTERN.search(text))


def runbook_is_status_check(runbook: dict[str, Any] | None, match: RunbookSearchMatch) -> bool:
    text = runbook_match_text(match, runbook)
    return bool(STATUS_CHECK_RUNBOOK_PATTERN.search(text))


def canonical_source_adjustment(match: RunbookSearchMatch) -> float:
    source = str(match.source_type or "").strip().lower()
    if source in CANONICAL_SOURCE_BOOST:
        return CANONICAL_SOURCE_BOOST[source]
    if source in TRAINING_SOURCE_TYPES:
        return TRAINING_SOURCE_PENALTY
    return 0.0


def intent_alignment_adjustment(
    node: dict[str, Any],
    match: RunbookSearchMatch,
    runbook: dict[str, Any] | None,
) -> float:
    if not node_is_check_phase(node):
        return 0.0
    if runbook_is_status_check(runbook, match):
        return 0.12
    if runbook_is_recovery_prep(runbook, match):
        return -0.18
    return 0.0


def extract_anchor_terms(text: str) -> set[str]:
    lowered = text.lower()
    anchors: set[str] = set()
    for group in DOMAIN_ANCHORS.values():
        for term in group:
            if term in lowered:
                anchors.add(term)
    for token in re.findall(r"[a-z0-9]+", lowered):
        if len(token) > 2 and token not in STOPWORDS:
            anchors.add(token)
    return anchors


def anchor_overlap(node_text: str, runbook_text: str) -> float:
    node_anchors = extract_anchor_terms(node_text)
    runbook_anchors = extract_anchor_terms(runbook_text)
    if not node_anchors or not runbook_anchors:
        return 0.0
    return len(node_anchors & runbook_anchors) / len(node_anchors | runbook_anchors)


def runbook_match_text(match: RunbookSearchMatch, runbook: dict[str, Any] | None = None) -> str:
    parts = [match.title, match.procedure_type]
    if runbook:
        parts.extend(
            [
                str(runbook.get("summary") or ""),
                str(runbook.get("when_to_use") or ""),
                " ".join(str(item) for item in runbook.get("not_for") or []),
                " ".join(str(step.get("title") or "") for step in runbook.get("steps") or [] if isinstance(step, dict)),
            ]
        )
    return " ".join(parts)


def procedure_type_boost(node_type: str, procedure_type: str) -> float:
    preferred = PROCEDURE_TYPE_PREFERRED.get(str(node_type or "").strip())
    if not preferred:
        return 0.0
    normalized_type = str(procedure_type or "").strip().lower()
    if normalized_type == preferred[0]:
        return 0.08
    if normalized_type in preferred:
        return 0.05
    return 0.0


def boost_combined_score(
    base_score: float,
    *,
    node: dict[str, Any] | None = None,
    node_text: str = "",
    match: RunbookSearchMatch,
    runbook: dict[str, Any] | None,
    procedure_type_compatible: bool,
) -> float:
    overlap = anchor_overlap(node_text, runbook_match_text(match, runbook))
    boosted = base_score
    if overlap >= 0.12:
        boosted += min(0.12, overlap * 0.35)
    if overlap >= 0.25:
        boosted += 0.06
    if match.jaccard_score >= 0.18:
        boosted += 0.04
    if procedure_type_compatible:
        boosted += 0.05
    if match.cosine_score >= 0.50:
        boosted += 0.04
    if node is not None:
        boosted += intent_alignment_adjustment(node, match, runbook)
    boosted += canonical_source_adjustment(match)
    return round(min(max(boosted, 0.0), 1.0), 4)


def runbook_as_match(runbook: dict[str, Any]) -> RunbookSearchMatch:
    return RunbookSearchMatch(
        procedure_id=str(runbook.get("procedure_id") or ""),
        title=str(runbook.get("title") or ""),
        procedure_type=str(runbook.get("procedure_type") or ""),
        cosine_score=0.0,
        jaccard_score=0.0,
        combined_score=0.0,
    )


def rank_matches_for_node(
    node: dict[str, Any],
    matches: list[RunbookSearchMatch],
    *,
    runbooks_by_id: dict[str, dict[str, Any]] | None = None,
) -> list[tuple[RunbookSearchMatch, float]]:
    node_text = build_retrieval_query_text(node)
    ranked: list[tuple[RunbookSearchMatch, float]] = []
    for match in matches:
        runbook = (runbooks_by_id or {}).get(match.procedure_id)
        boosted = boost_combined_score(
            match.combined_score,
            node=node,
            node_text=node_text,
            match=match,
            runbook=runbook,
            procedure_type_compatible=True,
        )
        ranked.append((match, boosted))
    ranked.sort(key=lambda item: (-item[1], item[0].procedure_id))
    return ranked
