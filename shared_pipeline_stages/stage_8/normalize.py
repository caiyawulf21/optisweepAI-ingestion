from __future__ import annotations

import re
from typing import Any

from shared_pipeline_stages.stage_8.link_scoring import (
    anchor_overlap,
    boost_combined_score,
    build_retrieval_query_text,
    normalize_placeholder_text,
    node_is_check_phase,
    rank_matches_for_node,
    runbook_as_match,
    runbook_is_recovery_prep,
    runbook_is_status_check,
    runbook_match_text,
    INTENT_OVERRIDE_MARGIN,
    DOMAIN_ANCHORS,
)
from shared_pipeline_stages.stage_8.schemas import RunbookSearchMatch

MAX_RUNBOOKS_PER_NODE = 3
MIN_RETRIEVAL_FLOOR = 0.28
HIGH_CONFIDENCE_SCORE = 0.48
MEDIUM_CONFIDENCE_SCORE = 0.38
ANCHOR_MEDIUM_OVERLAP = 0.18
ANCHOR_HIGH_OVERLAP = 0.28

CONFIDENCE_RANK = {"unresolved": 0, "low": 1, "medium": 2, "high": 3}

DIAGNOSTIC_NODE_TYPES = {"diagnostic_decision", "branching_condition", "validation_gate"}
OUTCOME_NODE_TYPES = DIAGNOSTIC_NODE_TYPES

PROCEDURE_TYPE_ALLOWED: dict[str, set[str]] = {
    "diagnostic_decision": {"diagnostic", "reference", "monitoring", "operation"},
    "branching_condition": {"diagnostic", "reference", "monitoring", "operation"},
    "validation_gate": {"diagnostic", "monitoring", "reference", "operation"},
    "procedure_reference": {"diagnostic", "reference", "monitoring", "operation", "recovery"},
    "escalation_gate": {"reference", "diagnostic", "monitoring", "operation"},
    "recovery_phase_marker": {"reference", "diagnostic", "monitoring", "operation", "recovery"},
}

PROCEDURE_TYPE_BLOCKED: dict[str, set[str]] = {
    "diagnostic_decision": {"recovery"},
    "branching_condition": {"recovery"},
    "validation_gate": set(),
    "procedure_reference": set(),
    "escalation_gate": set(),
    "recovery_phase_marker": set(),
}

COMPOUND_PLACEHOLDER_PATTERN = re.compile(
    r"\b(then also|as well as|both .+ and|;\s|\. then\b|\band then\b)",
    re.IGNORECASE,
)

SECONDARY_RUNBOOK_MIN_BOOSTED = 0.42
SECONDARY_RUNBOOK_MIN_ANCHOR_OVERLAP = 0.15


def reconcile_link_confidence(
    *,
    llm_confidence: str | None,
    retrieval_score: float | None,
    boosted_score: float | None = None,
    node: dict[str, Any] | None = None,
    match: RunbookSearchMatch | None = None,
    runbook: dict[str, Any] | None = None,
    link_rank: int = 1,
    type_compatible: bool = True,
) -> str:
    effective_score = boosted_score if boosted_score is not None else (retrieval_score or 0.0)
    score_confidence = confidence_for_score(effective_score)
    llm_value = str(llm_confidence or "").strip().lower()
    if llm_value not in CONFIDENCE_RANK:
        llm_value = score_confidence

    overlap = 0.0
    if node and match:
        node_text = build_retrieval_query_text(node)
        overlap = anchor_overlap(node_text, runbook_match_text(match, runbook))

    elevated = score_confidence
    if link_rank == 1 and type_compatible:
        if overlap >= ANCHOR_HIGH_OVERLAP or effective_score >= HIGH_CONFIDENCE_SCORE:
            elevated = "high"
        elif overlap >= ANCHOR_MEDIUM_OVERLAP or effective_score >= MEDIUM_CONFIDENCE_SCORE or match and match.jaccard_score >= 0.20:
            elevated = "medium"

    if llm_value == "high" and link_rank == 1 and type_compatible and elevated != "unresolved":
        return "high"
    if llm_value == "medium" and CONFIDENCE_RANK[elevated] < CONFIDENCE_RANK["medium"]:
        elevated = "medium"

    return elevated if CONFIDENCE_RANK[elevated] >= CONFIDENCE_RANK[llm_value] else llm_value


def evaluate_link_confidence(
    node: dict[str, Any],
    match: RunbookSearchMatch,
    *,
    runbook: dict[str, Any] | None = None,
    llm_confidence: str | None = None,
    link_rank: int = 1,
) -> tuple[str, float, list[str]]:
    node_type = str(node.get("node_type") or "")
    type_ok = procedure_type_compatible(node_type, match.procedure_type)
    node_text = build_retrieval_query_text(node)
    boosted = boost_combined_score(
        match.combined_score,
        node=node,
        node_text=node_text,
        match=match,
        runbook=runbook,
        procedure_type_compatible=type_ok,
    )
    confidence = reconcile_link_confidence(
        llm_confidence=llm_confidence,
        retrieval_score=match.combined_score,
        boosted_score=boosted,
        node=node,
        match=match,
        runbook=runbook,
        link_rank=link_rank,
        type_compatible=type_ok,
    )
    gaps = _match_gaps(node, match, confidence, overlap=anchor_overlap(node_text, runbook_match_text(match, runbook)))
    if not type_ok:
        gaps.append(f"Procedure type '{match.procedure_type}' is not ideal for node type '{node_type}'.")
        if CONFIDENCE_RANK[confidence] > CONFIDENCE_RANK["low"]:
            confidence = "low"
    return confidence, boosted, gaps


def confidence_for_score(score: float) -> str:
    if score >= HIGH_CONFIDENCE_SCORE:
        return "high"
    if score >= MEDIUM_CONFIDENCE_SCORE:
        return "medium"
    if score >= MIN_RETRIEVAL_FLOOR:
        return "low"
    return "unresolved"


def procedure_type_compatible(node_type: str, procedure_type: str) -> bool:
    normalized_node = str(node_type or "").strip()
    normalized_type = str(procedure_type or "").strip().lower()
    if not normalized_type:
        return True
    blocked = PROCEDURE_TYPE_BLOCKED.get(normalized_node, set())
    if normalized_type in blocked:
        return False
    allowed = PROCEDURE_TYPE_ALLOWED.get(normalized_node)
    if allowed is None:
        return True
    return normalized_type in allowed


def filter_compatible_matches(node: dict[str, Any], matches: list[RunbookSearchMatch]) -> list[RunbookSearchMatch]:
    node_type = str(node.get("node_type") or "")
    return [
        match
        for match in matches
        if procedure_type_compatible(node_type, match.procedure_type)
    ]


def select_runbook_matches(
    node: dict[str, Any],
    matches: list[RunbookSearchMatch],
    *,
    runbooks_by_id: dict[str, dict[str, Any]] | None = None,
    max_runbooks: int = MAX_RUNBOOKS_PER_NODE,
) -> list[tuple[RunbookSearchMatch, str, list[str], float]]:
    if not matches:
        return []
    compatible = filter_compatible_matches(node, matches)
    if not compatible:
        return []
    ranked = [match for match, _ in rank_matches_for_node(node, compatible, runbooks_by_id=runbooks_by_id)]
    top = ranked[0]
    top_confidence, top_boosted, top_gaps = evaluate_link_confidence(
        node,
        top,
        runbook=(runbooks_by_id or {}).get(top.procedure_id),
        link_rank=1,
    )
    if top_confidence == "unresolved":
        return []

    selected: list[tuple[RunbookSearchMatch, str, list[str], float]] = [
        (top, top_confidence, top_gaps, top_boosted)
    ]
    placeholder = str(node.get("runbook_placeholder") or "")
    if not _allows_multiple_runbooks(node, placeholder) or max_runbooks <= 1:
        return selected

    for match in ranked[1:max_runbooks]:
        if match.procedure_id == top.procedure_id:
            continue
        if _too_similar_to_selected(match, selected):
            continue
        confidence, boosted, gaps = evaluate_link_confidence(
            node,
            match,
            runbook=(runbooks_by_id or {}).get(match.procedure_id),
            link_rank=len(selected) + 1,
        )
        if confidence == "unresolved":
            continue
        node_text = build_retrieval_query_text(node)
        overlap = anchor_overlap(node_text, runbook_match_text(match, (runbooks_by_id or {}).get(match.procedure_id)))
        if boosted < SECONDARY_RUNBOOK_MIN_BOOSTED or overlap < SECONDARY_RUNBOOK_MIN_ANCHOR_OVERLAP:
            continue
        selected.append((match, confidence, gaps, boosted))
        if len(selected) >= max_runbooks:
            break
    return selected


def reconcile_llm_runbook_links(
    node: dict[str, Any],
    links: list[dict[str, Any]],
    retrieval_matches: list[Any],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    if not links or not retrieval_matches:
        return links
    ranked = rank_matches_for_node(
        node,
        list(retrieval_matches),
        runbooks_by_id=runbooks_by_id,
    )
    if not ranked:
        return links
    best_match, best_boosted = ranked[0]
    first = links[0]
    procedure_id = str(first.get("procedure_id") or "")
    chosen_match = next((match for match, _ in ranked if match.procedure_id == procedure_id), None)
    if not chosen_match:
        return links
    chosen_runbook = runbooks_by_id.get(procedure_id)
    if not runbook_is_recovery_prep(chosen_runbook, chosen_match) or runbook_is_status_check(chosen_runbook, chosen_match):
        return links
    if not runbook_is_status_check(runbooks_by_id.get(best_match.procedure_id), best_match):
        return links
    _, chosen_boosted = next((item for item in ranked if item[0].procedure_id == procedure_id), (None, 0.0))
    if chosen_boosted > best_boosted + INTENT_OVERRIDE_MARGIN:
        return links
    confidence, boosted, gaps = evaluate_link_confidence(
        node,
        best_match,
        runbook=runbooks_by_id.get(best_match.procedure_id),
        link_rank=1,
    )
    corrected = dict(first)
    corrected.update(
        {
            "procedure_id": best_match.procedure_id,
            "link_confidence": confidence,
            "link_rationale": (
                "Retrieval realigned to status-check runbook; recovery-prep runbook penalized for check-only node."
            ),
            "match_gaps": gaps,
            "retrieval_combined_score": best_match.combined_score,
            "boosted_score": boosted,
            "link_rank": 1,
        }
    )
    return [corrected, *links[1:]]


def build_decision_outcomes(
    node: dict[str, Any],
    runbooks_by_id: dict[str, dict[str, Any]],
    *,
    linked_runbook_ids: list[str],
    branch_hints: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    node_type = str(node.get("node_type") or "")
    if node_type not in OUTCOME_NODE_TYPES:
        return []
    outcomes: list[dict[str, Any]] = []
    for procedure_id in linked_runbook_ids:
        runbook = runbooks_by_id.get(procedure_id, {})
        outcomes.extend(_outcomes_from_runbook(node, runbook, procedure_id, branch_hints))
    if outcomes:
        return _ensure_outcome_coverage(
            outcomes,
            node,
            branch_hints,
            runbooks_by_id=runbooks_by_id,
            linked_runbook_ids=linked_runbook_ids,
        )
    return _fallback_outcomes_from_node(node, branch_hints)


def build_branches_from_hints(
    node: dict[str, Any],
    branch_hints: list[dict[str, Any]],
    *,
    llm_branches: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    node_id = str(node.get("node_id") or "")
    seeded = [
        hint
        for hint in branch_hints
        if str(hint.get("from_node_id") or "") == node_id
    ]
    if llm_branches:
        return llm_branches
    branches: list[dict[str, Any]] = []
    for index, hint in enumerate(seeded, start=1):
        branches.append(
            {
                "branch_id": f"{node_id}_branch_{index}",
                "condition_label": str(hint.get("condition_or_signal") or ""),
                "condition_descriptor": str(hint.get("condition_or_signal") or ""),
                "outcome": _infer_outcome_label(str(hint.get("condition_or_signal") or "")),
                "next_node_id": str(hint.get("suggested_next_node_id") or ""),
                "source_branch_hint_ids": [f"branch_hint_{index}"],
                "linked_runbook_step_ref": "",
                "source_refs": hint.get("source_refs") or [],
            }
        )
    return branches


def validate_finalized_playbook(
    playbook: dict[str, Any],
    *,
    runbooks_by_id: dict[str, dict[str, Any]],
    max_runbooks_per_node: int = MAX_RUNBOOKS_PER_NODE,
) -> list[str]:
    warnings: list[str] = []
    node_ids = {str(node.get("node_id") or "") for node in playbook.get("nodes") or [] if isinstance(node, dict)}
    for node in playbook.get("nodes") or []:
        if not isinstance(node, dict):
            continue
        links = node.get("runbook_links") or []
        procedure_ids = [str(link.get("procedure_id") or "") for link in links if isinstance(link, dict)]
        if len(procedure_ids) > max_runbooks_per_node:
            warnings.append(f"{node.get('node_id')}: more than {max_runbooks_per_node} runbook links")
        for procedure_id in procedure_ids:
            if procedure_id and procedure_id not in runbooks_by_id:
                warnings.append(f"{node.get('node_id')}: unknown procedure_id {procedure_id}")
            elif procedure_id and node_is_check_phase(node) and runbook_is_recovery_prep(
                runbooks_by_id.get(procedure_id),
                runbook_as_match(runbooks_by_id[procedure_id]),
            ):
                warnings.append(
                    f"{node.get('node_id')}: recovery-prep runbook linked to check-only node {procedure_id}"
                )
            elif procedure_id and not procedure_type_compatible(str(node.get("node_type") or ""), str(runbooks_by_id[procedure_id].get("procedure_type") or "")):
                warnings.append(
                    f"{node.get('node_id')}: procedure_type mismatch for {procedure_id}"
                )
        if str(node.get("node_type") or "") in OUTCOME_NODE_TYPES:
            outcomes = node.get("decision_outcomes") or []
            labels = {str(item.get("outcome_label") or "") for item in outcomes if isinstance(item, dict)}
            if "healthy" not in labels and not {"unhealthy", "inconclusive", "escalate"} & labels:
                warnings.append(f"{node.get('node_id')}: missing healthy/unhealthy decision outcomes")
        for branch in node.get("branches") or []:
            if not isinstance(branch, dict):
                continue
            next_node_id = str(branch.get("next_node_id") or "")
            if next_node_id and next_node_id not in node_ids:
                warnings.append(f"{node.get('node_id')}: branch next_node_id not found: {next_node_id}")
    for branch in playbook.get("branches") or []:
        if not isinstance(branch, dict):
            continue
        next_node_id = str(branch.get("next_node_id") or "")
        if next_node_id and next_node_id not in node_ids:
            warnings.append(f"playbook branch next_node_id not found: {next_node_id}")
    return warnings


def needs_graph_repair(playbook: dict[str, Any]) -> bool:
    hints = playbook.get("branch_hints") or []
    confirmed: set[tuple[str, str]] = set()
    for node in playbook.get("nodes") or []:
        if not isinstance(node, dict):
            continue
        node_id = str(node.get("node_id") or "")
        for branch in node.get("branches") or []:
            if isinstance(branch, dict):
                confirmed.add((node_id, str(branch.get("next_node_id") or "")))
    for hint in hints:
        if not isinstance(hint, dict):
            continue
        edge = (str(hint.get("from_node_id") or ""), str(hint.get("suggested_next_node_id") or ""))
        if edge[0] and edge[1] and edge not in confirmed:
            return True
    return False


def _allows_multiple_runbooks(node: dict[str, Any], placeholder: str) -> bool:
    node_type = str(node.get("node_type") or "")
    normalized = normalize_placeholder_text(placeholder)
    if node_type == "validation_gate":
        return bool(re.search(r"\b(and|also|both|;\s|then)\b", normalized, re.IGNORECASE))
    if not COMPOUND_PLACEHOLDER_PATTERN.search(normalized):
        return False
    distinct_domains = sum(1 for terms in DOMAIN_ANCHORS.values() if any(term in normalized.lower() for term in terms))
    return distinct_domains >= 2


def _too_similar_to_selected(
    match: RunbookSearchMatch,
    selected: list[tuple[RunbookSearchMatch, str, list[str], float]],
) -> bool:
    for existing, _, _, _ in selected:
        if existing.procedure_id == match.procedure_id:
            return True
        title_a = existing.title.lower()
        title_b = match.title.lower()
        if title_a and title_b and (title_a in title_b or title_b in title_a):
            return True
    return False


def _match_gaps(
    node: dict[str, Any],
    match: RunbookSearchMatch,
    confidence: str,
    *,
    overlap: float = 0.0,
) -> list[str]:
    if confidence in {"high", "medium"}:
        return []
    gaps: list[str] = []
    if match.combined_score < MEDIUM_CONFIDENCE_SCORE:
        gaps.append(f"Retrieval score {match.combined_score:.4f} below medium threshold.")
    if overlap < ANCHOR_MEDIUM_OVERLAP:
        gaps.append("Limited domain-term overlap between placeholder and runbook.")
    placeholder = normalize_placeholder_text(str(node.get("runbook_placeholder") or "")).lower()
    title = match.title.lower()
    if placeholder and title and token_overlap_ratio(placeholder, title) < 0.12:
        gaps.append("Placeholder wording differs materially from matched runbook title.")
    return gaps


def token_overlap_ratio(first: str, second: str) -> float:
    first_tokens = set(re.findall(r"[a-z0-9]+", first.lower()))
    second_tokens = set(re.findall(r"[a-z0-9]+", second.lower()))
    if not first_tokens or not second_tokens:
        return 0.0
    return len(first_tokens & second_tokens) / len(first_tokens | second_tokens)


def _outcomes_from_runbook(
    node: dict[str, Any],
    runbook: dict[str, Any],
    procedure_id: str,
    branch_hints: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    outcomes: list[dict[str, Any]] = []
    next_node_id = _next_node_from_hints(str(node.get("node_id") or ""), branch_hints)
    for condition in runbook.get("healthy_conditions") or []:
        if not isinstance(condition, dict):
            continue
        descriptor = str(condition.get("healthy_condition") or condition.get("description") or "").strip()
        if descriptor:
            outcomes.append(
                {
                    "outcome_label": "healthy",
                    "descriptor": descriptor,
                    "observable_signal": descriptor,
                    "source": "runbook_healthy_condition",
                    "linked_runbook_id": procedure_id,
                    "linked_step_number": condition.get("step_number"),
                    "next_node_id": next_node_id,
                }
            )
    for step in runbook.get("steps") or []:
        if not isinstance(step, dict):
            continue
        healthy = str(step.get("healthy_condition") or "").strip()
        expected = str(step.get("expected_result") or "").strip()
        descriptor = healthy or expected
        if not descriptor:
            continue
        outcomes.append(
            {
                "outcome_label": "healthy" if healthy else "inconclusive",
                "descriptor": descriptor,
                "observable_signal": descriptor,
                "source": "runbook_step",
                "linked_runbook_id": procedure_id,
                "linked_step_number": step.get("step_number"),
                "next_node_id": next_node_id,
            }
        )
    failure_conditions = runbook.get("failure_conditions") or []
    for item in failure_conditions[:3]:
        text = str(item).strip()
        if text:
            outcomes.append(
                {
                    "outcome_label": "unhealthy",
                    "descriptor": text,
                    "observable_signal": text,
                    "source": "runbook_step",
                    "linked_runbook_id": procedure_id,
                    "linked_step_number": None,
                    "next_node_id": next_node_id,
                }
            )
    return outcomes


def _fallback_outcomes_from_node(
    node: dict[str, Any],
    branch_hints: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    expected = str(node.get("expected_or_observed_result") or "").strip()
    if not expected:
        return []
    return [
        {
            "outcome_label": "inconclusive",
            "descriptor": expected,
            "observable_signal": expected,
            "source": "playbook_expected_result",
            "linked_runbook_id": "",
            "linked_step_number": None,
            "next_node_id": _next_node_from_hints(str(node.get("node_id") or ""), branch_hints),
        }
    ]


def _ensure_outcome_coverage(
    outcomes: list[dict[str, Any]],
    node: dict[str, Any],
    branch_hints: list[dict[str, Any]],
    *,
    runbooks_by_id: dict[str, dict[str, Any]] | None = None,
    linked_runbook_ids: list[str] | None = None,
) -> list[dict[str, Any]]:
    labels = {str(item.get("outcome_label") or "") for item in outcomes}
    next_node_id = _next_node_from_hints(str(node.get("node_id") or ""), branch_hints)
    if "healthy" not in labels:
        for procedure_id in linked_runbook_ids or []:
            runbook = (runbooks_by_id or {}).get(procedure_id, {})
            for item in runbook.get("success_criteria") or []:
                text = str(item).strip()
                if text:
                    outcomes.append(
                        {
                            "outcome_label": "healthy",
                            "descriptor": text,
                            "observable_signal": text,
                            "source": "runbook_step",
                            "linked_runbook_id": procedure_id,
                            "linked_step_number": None,
                            "next_node_id": next_node_id,
                        }
                    )
                    labels.add("healthy")
                    break
            if "healthy" in labels:
                break
    if "unhealthy" not in labels:
        for procedure_id in linked_runbook_ids or []:
            runbook = (runbooks_by_id or {}).get(procedure_id, {})
            for item in runbook.get("failure_conditions") or []:
                text = str(item).strip()
                if text:
                    outcomes.append(
                        {
                            "outcome_label": "unhealthy",
                            "descriptor": text,
                            "observable_signal": text,
                            "source": "runbook_step",
                            "linked_runbook_id": procedure_id,
                            "linked_step_number": None,
                            "next_node_id": next_node_id,
                        }
                    )
                    labels.add("unhealthy")
                    break
            if "unhealthy" in labels:
                break
    if "inconclusive" not in labels:
        expected = str(node.get("expected_or_observed_result") or "").strip()
        descriptor = expected or "Observed state is unclear or cannot be confirmed from available evidence."
        outcomes.append(
            {
                "outcome_label": "inconclusive",
                "descriptor": descriptor,
                "observable_signal": descriptor,
                "source": "playbook_expected_result",
                "linked_runbook_id": "",
                "linked_step_number": None,
                "next_node_id": next_node_id,
            }
        )
    return outcomes


def _next_node_from_hints(node_id: str, branch_hints: list[dict[str, Any]]) -> str:
    for hint in branch_hints:
        if str(hint.get("from_node_id") or "") == node_id:
            return str(hint.get("suggested_next_node_id") or "")
    return ""


def _infer_outcome_label(condition: str) -> str:
    lowered = condition.lower()
    if any(term in lowered for term in ["fail", "not responsive", "abnormal", "error", "blocked", "unable"]):
        return "unhealthy"
    if any(term in lowered for term in ["escalat", "unauthorized", "unsafe"]):
        return "escalate"
    if any(term in lowered for term in ["confirm", "healthy", "responsive", "recovered", "visible"]):
        return "healthy"
    return "inconclusive"
