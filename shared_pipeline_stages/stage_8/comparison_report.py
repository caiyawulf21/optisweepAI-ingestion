from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from shared_pipeline_stages.stage_8.schemas import VariantFinalizationReport


def build_variant_report(
    playbooks: list[dict[str, Any]],
    *,
    extraction_mode: str,
    case_ids: list[str],
    warnings: list[str],
) -> VariantFinalizationReport:
    node_count = 0
    high = medium = low = unresolved = 0
    multi_runbook_nodes = 0
    incident_pref = 0
    duplicate_refs = 0
    diagnostic_nodes = 0
    diagnostic_with_outcomes = 0
    branch_hints_total = 0
    branch_hints_confirmed = 0
    needs_graph_repair: list[str] = []

    for playbook in playbooks:
        if playbook.get("needs_graph_repair"):
            needs_graph_repair.append(str(playbook.get("playbook_id") or ""))
        branch_hints_total += len(playbook.get("branch_hints") or [])
        confirmed_edges = _confirmed_branch_edges(playbook)
        for hint in playbook.get("branch_hints") or []:
            if not isinstance(hint, dict):
                continue
            edge = (str(hint.get("from_node_id") or ""), str(hint.get("suggested_next_node_id") or ""))
            if edge in confirmed_edges:
                branch_hints_confirmed += 1

        procedure_ids_by_playbook: list[str] = []
        for node in playbook.get("nodes") or []:
            if not isinstance(node, dict):
                continue
            node_count += 1
            links = node.get("runbook_links") or []
            procedure_ids = [str(link.get("procedure_id") or "") for link in links if isinstance(link, dict)]
            procedure_ids_by_playbook.extend([item for item in procedure_ids if item])
            if len(procedure_ids) > 1:
                multi_runbook_nodes += 1
            for link in links:
                if not isinstance(link, dict):
                    continue
                confidence = str(link.get("link_confidence") or "")
                if confidence == "high":
                    high += 1
                elif confidence == "medium":
                    medium += 1
                elif confidence == "low":
                    low += 1
                else:
                    unresolved += 1
                if link.get("preferred_incident_source"):
                    incident_pref += 1
            if not links:
                unresolved += 1
            if str(node.get("node_type") or "") in {"diagnostic_decision", "branching_condition", "validation_gate"}:
                diagnostic_nodes += 1
                outcomes = node.get("decision_outcomes") or []
                labels = {str(item.get("outcome_label") or "") for item in outcomes if isinstance(item, dict)}
                if labels and ("healthy" in labels or "unhealthy" in labels or "inconclusive" in labels):
                    diagnostic_with_outcomes += 1
        duplicate_refs += sum(count - 1 for count in Counter(procedure_ids_by_playbook).values() if count > 1)

    total_links = high + medium + low + unresolved
    return VariantFinalizationReport(
        extraction_mode=extraction_mode,
        case_ids=case_ids,
        playbook_count=len(playbooks),
        node_count=node_count,
        high_confidence_link_rate=round(high / total_links, 4) if total_links else 0.0,
        high_confidence_link_count=high,
        medium_confidence_link_count=medium,
        low_confidence_link_count=low,
        unresolved_link_count=unresolved,
        multi_runbook_node_count=multi_runbook_nodes,
        diagnostic_outcome_coverage=round(diagnostic_with_outcomes / diagnostic_nodes, 4) if diagnostic_nodes else 0.0,
        branch_graph_completeness=round(branch_hints_confirmed / branch_hints_total, 4) if branch_hints_total else 1.0,
        incident_source_preference_applied_count=incident_pref,
        duplicate_runbook_ref_count=duplicate_refs,
        warnings=warnings,
        needs_graph_repair_playbook_ids=needs_graph_repair,
    )


def build_comparison_report(
    variant_reports: list[VariantFinalizationReport],
    *,
    case_ids: list[str],
    generated_at: str,
) -> dict[str, Any]:
    by_mode = {report.extraction_mode: report.model_dump() for report in variant_reports}
    per_case: dict[str, dict[str, Any]] = defaultdict(dict)
    for case_id in case_ids:
        per_case[case_id] = {
            "prompt_a_one_per_incident": _case_slice(by_mode.get("one_playbook_candidate_per_incident", {}), case_id),
            "prompt_b_multi_flow": _case_slice(by_mode.get("one_or_more_playbook_candidates_when_separable", {}), case_id),
        }
    return {
        "stage": "stage_8_playbook_ab_comparison",
        "generated_at": generated_at,
        "case_ids": case_ids,
        "metrics": [
            "high_confidence_link_rate",
            "unresolved_link_count",
            "low_confidence_link_count",
            "duplicate_runbook_ref_count",
            "diagnostic_outcome_coverage",
            "branch_graph_completeness",
            "incident_source_preference_applied_count",
            "multi_runbook_node_count",
        ],
        "variant_reports": [report.model_dump() for report in variant_reports],
        "per_case": dict(per_case),
        "sme_review_flags": _aggregate_sme_flags(variant_reports),
    }


def _confirmed_branch_edges(playbook: dict[str, Any]) -> set[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    for node in playbook.get("nodes") or []:
        if not isinstance(node, dict):
            continue
        node_id = str(node.get("node_id") or "")
        for branch in node.get("branches") or []:
            if isinstance(branch, dict):
                edges.add((node_id, str(branch.get("next_node_id") or "")))
    for branch in playbook.get("branches") or []:
        if isinstance(branch, dict):
            edges.add((str(branch.get("from_node_id") or ""), str(branch.get("next_node_id") or "")))
    return edges


def _case_slice(report: dict[str, Any], case_id: str) -> dict[str, Any]:
    if case_id not in (report.get("case_ids") or []):
        return {"present": False}
    return {
        "present": True,
        "playbook_count": report.get("playbook_count"),
        "node_count": report.get("node_count"),
        "high_confidence_link_rate": report.get("high_confidence_link_rate"),
        "unresolved_link_count": report.get("unresolved_link_count"),
        "diagnostic_outcome_coverage": report.get("diagnostic_outcome_coverage"),
        "branch_graph_completeness": report.get("branch_graph_completeness"),
    }


def _aggregate_sme_flags(variant_reports: list[VariantFinalizationReport]) -> list[str]:
    flags: list[str] = []
    for report in variant_reports:
        if report.unresolved_link_count:
            flags.append(f"{report.extraction_mode}: unresolved links={report.unresolved_link_count}")
        if report.low_confidence_link_count:
            flags.append(f"{report.extraction_mode}: low-confidence links={report.low_confidence_link_count}")
        if report.needs_graph_repair_playbook_ids:
            flags.append(
                f"{report.extraction_mode}: needs_graph_repair={','.join(report.needs_graph_repair_playbook_ids)}"
            )
        flags.extend(report.warnings[:10])
    return flags
