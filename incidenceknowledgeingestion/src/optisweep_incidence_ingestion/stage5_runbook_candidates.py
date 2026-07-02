"""Stage 5 - Incident-derived runbook and playbook candidate discovery.

This stage extracts lightweight, source-grounded procedure candidates from an
incident case and lightweight playbook candidates from the same evidence. It
does not create canonical runbooks, canonical playbooks, production workflows,
trigger logic, or cross-source merge decisions.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Protocol
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request

from dotenv import load_dotenv

from optisweep_incidence_ingestion.utils.json_utils import read_json, write_json
from optisweep_incidence_ingestion.utils.markdown_review import (
    write_stage5_playbook_candidate_review_markdown,
    write_stage5_runbook_candidate_review_markdown,
)

FOUNDRY_API_VERSION = "2025-04-01-preview"
CLASSIC_AZURE_OPENAI_API_VERSION = "2024-10-21"

ALLOWED_PROCEDURE_TYPES = {"operation", "diagnostic", "recovery", "reference"}
ALLOWED_ROLES = {"operator", "L1_support", "L2_support", "L3_support"}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
FORBIDDEN_FIELDS = {
    "trigger_conditions",
    "candidate_input_signals",
    "produces_signals",
    "resolved_signals",
    "playbook_id",
    "playbook_step_id",
    "playbook_node",
    "workflow_branch",
    "decision_node",
    "ml_label",
    "routing_key",
    "next_step_on_success",
    "next_step_on_failure",
    "workflow_id",
    "workflow_step_id",
}

MAX_CHARS = 900
MAX_PAGE_CHUNK_TEXT_CHARS = 5000
PROCEDURAL_ACTION_TERMS = {
    "open",
    "navigate",
    "select",
    "check",
    "compare",
    "restart",
    "reset",
    "wait",
    "verify",
    "confirm",
    "capture",
    "record",
    "review",
    "run",
    "send",
    "release",
    "stop",
    "start",
    "locate",
}
EVIDENCE_ONLY_TERMS = {
    "capture case evidence",
    "collect case evidence",
    "document incident evidence",
    "record abnormal",
    "capture screenshot evidence",
}


class Stage5RunbookCandidateClient(Protocol):
    def discover_runbook_candidates(self, packet: dict[str, Any]) -> dict[str, Any]:
        ...


class Stage5PlaybookCandidateClient(Protocol):
    def discover_playbook_candidates(self, packet: dict[str, Any]) -> dict[str, Any]:
        ...


class AzureOpenAIStage5RunbookCandidateClient:
    def __init__(
        self,
        endpoint: str | None = None,
        api_key: str | None = None,
        deployment: str | None = None,
        api_version: str | None = None,
        prompt_path: str | Path | None = None,
    ) -> None:
        load_dotenv()
        self.endpoint = _clean_env_value(endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")).rstrip("/")
        self.api_key = _clean_env_value(api_key or os.getenv("AZURE_OPENAI_API_KEY"))
        self.deployment = _clean_env_value(deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT"))
        env_api_version = _clean_env_value(os.getenv("AZURE_OPENAI_API_VERSION"))
        self.api_version = _clean_env_value(api_version) or self._default_api_version(env_api_version)
        default_prompt = Path(__file__).resolve().parent / "prompts" / "stage5_runbook_candidate_discovery_prompt.md"
        self.prompt = Path(prompt_path or default_prompt).read_text(encoding="utf-8")
        missing = [
            name
            for name, value in [
                ("AZURE_OPENAI_ENDPOINT", self.endpoint),
                ("AZURE_OPENAI_API_KEY", self.api_key),
                ("AZURE_OPENAI_DEPLOYMENT", self.deployment),
                ("AZURE_OPENAI_API_VERSION", self.api_version),
            ]
            if not value
        ]
        if missing:
            raise RuntimeError("Azure OpenAI is not configured. Set these environment variables: " + ", ".join(missing))

    def discover_runbook_candidates(self, packet: dict[str, Any]) -> dict[str, Any]:
        body = {
            "messages": [
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": json.dumps(packet, ensure_ascii=False)},
            ],
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
        }
        errors: list[str] = []
        for url, headers, include_model in self._candidate_requests(self.api_version):
            request_body = body | ({"model": self.deployment} if include_model else {})
            request = urllib.request.Request(
                url,
                data=json.dumps(request_body).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            try:
                with _urlopen_no_proxy(request, timeout=180) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                return parse_llm_response(payload["choices"][0]["message"]["content"])
            except urllib.error.HTTPError as exc:
                details = exc.read().decode("utf-8", errors="replace")
                errors.append(f"HTTP {exc.code}: {details}")
                if exc.code not in {400, 404}:
                    raise RuntimeError(f"Azure OpenAI request failed with HTTP {exc.code}: {details}") from exc
            except urllib.error.URLError as exc:
                raise RuntimeError(f"Azure OpenAI request failed: {exc.reason}") from exc
        raise RuntimeError("Azure OpenAI request failed for endpoint patterns tried: " + " | ".join(errors))

    def _candidate_requests(self, api_version: str) -> list[tuple[str, dict[str, str], bool]]:
        encoded_deployment = urllib.parse.quote(self.deployment, safe="")
        query = urllib.parse.urlencode({"api-version": api_version})
        headers = {"Content-Type": "application/json", "api-key": self.api_key}
        parsed = urllib.parse.urlparse(self.endpoint)
        if self._is_foundry_project_endpoint():
            foundry_base = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, "", "", "", "")).rstrip("/")
            return [(f"{foundry_base}/models/chat/completions?{query}", headers, True)]
        return [(f"{self.endpoint}/openai/deployments/{encoded_deployment}/chat/completions?{query}", headers, False)]

    def _is_foundry_project_endpoint(self) -> bool:
        parsed = urllib.parse.urlparse(self.endpoint)
        return parsed.netloc.endswith(".services.ai.azure.com") and "/api/projects/" in parsed.path

    def _default_api_version(self, env_api_version: str = "") -> str:
        parsed = urllib.parse.urlparse(self.endpoint)
        if parsed.netloc.endswith(".services.ai.azure.com") and "/api/projects/" in parsed.path:
            return FOUNDRY_API_VERSION
        return env_api_version or CLASSIC_AZURE_OPENAI_API_VERSION


def create_stage5_runbook_candidates(
    *,
    source_package_path: str | Path,
    canonical_incident_record_path: str | Path,
    timeline_events_path: str | Path,
    stage4_evidence_chunks_path: str | Path,
    source_artifacts_enriched_path: str | Path,
    output_dir: str | Path,
    llm_client: Stage5RunbookCandidateClient,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    package = read_json(source_package_path)
    canonical_record = read_json(canonical_incident_record_path)
    timeline = read_json(timeline_events_path)
    evidence_handoff = read_json(stage4_evidence_chunks_path)
    artifacts = read_json(source_artifacts_enriched_path)
    if not isinstance(artifacts, list):
        raise ValueError("source_artifacts_enriched.json must contain a list.")

    packet = build_stage5_packet(
        package=package,
        canonical_record=canonical_record,
        timeline=timeline,
        evidence_handoff=evidence_handoff,
        artifacts=artifacts,
    )
    response = llm_client.discover_runbook_candidates(packet)
    candidates = normalize_candidates(response, packet)
    candidates = merge_validation_diagnostics_into_recovery_candidates(candidates)
    known = _known_refs(packet, artifacts)
    candidates, report = validate_and_dedupe_candidates(candidates, packet, known)

    output_path = Path(output_dir)
    write_json(output_path / "stage5_runbook_candidate_packet.json", packet)
    write_json(output_path / "runbook_candidates.json", candidates)
    write_json(output_path / "runbook_candidate_extraction_report.json", report)
    write_stage5_runbook_candidate_review_markdown(
        output_path / "runbook_candidate_review.md",
        candidates,
        report,
        canonical_record,
    )
    write_json(output_path / "incident_source_package.json", _package_with_stage5_refs(package, output_path, report))
    return candidates, report


class AzureOpenAIStage5PlaybookCandidateClient:
    def __init__(
        self,
        endpoint: str | None = None,
        api_key: str | None = None,
        deployment: str | None = None,
        api_version: str | None = None,
        prompt_path: str | Path | None = None,
    ) -> None:
        load_dotenv()
        self.endpoint = _clean_env_value(endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")).rstrip("/")
        self.api_key = _clean_env_value(api_key or os.getenv("AZURE_OPENAI_API_KEY"))
        self.deployment = _clean_env_value(deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT"))
        env_api_version = _clean_env_value(os.getenv("AZURE_OPENAI_API_VERSION"))
        self.api_version = _clean_env_value(api_version) or self._default_api_version(env_api_version)
        default_prompt = Path(__file__).resolve().parent / "prompts" / "stage5_playbook_candidate_discovery_prompt.md"
        self.prompt = Path(prompt_path or default_prompt).read_text(encoding="utf-8")
        missing = [
            name
            for name, value in [
                ("AZURE_OPENAI_ENDPOINT", self.endpoint),
                ("AZURE_OPENAI_API_KEY", self.api_key),
                ("AZURE_OPENAI_DEPLOYMENT", self.deployment),
                ("AZURE_OPENAI_API_VERSION", self.api_version),
            ]
            if not value
        ]
        if missing:
            raise RuntimeError("Azure OpenAI is not configured. Set these environment variables: " + ", ".join(missing))

    def discover_playbook_candidates(self, packet: dict[str, Any]) -> dict[str, Any]:
        body = {
            "messages": [
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": json.dumps(packet, ensure_ascii=False)},
            ],
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
        }
        errors: list[str] = []
        for url, headers, include_model in self._candidate_requests(self.api_version):
            request_body = body | ({"model": self.deployment} if include_model else {})
            request = urllib.request.Request(
                url,
                data=json.dumps(request_body).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            try:
                with _urlopen_no_proxy(request, timeout=180) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                return parse_llm_response(payload["choices"][0]["message"]["content"])
            except urllib.error.HTTPError as exc:
                details = exc.read().decode("utf-8", errors="replace")
                errors.append(f"HTTP {exc.code}: {details}")
                if exc.code not in {400, 404}:
                    raise RuntimeError(f"Azure OpenAI request failed with HTTP {exc.code}: {details}") from exc
            except urllib.error.URLError as exc:
                raise RuntimeError(f"Azure OpenAI request failed: {exc.reason}") from exc
        raise RuntimeError("Azure OpenAI request failed for endpoint patterns tried: " + " | ".join(errors))

    def _candidate_requests(self, api_version: str) -> list[tuple[str, dict[str, str], bool]]:
        encoded_deployment = urllib.parse.quote(self.deployment, safe="")
        query = urllib.parse.urlencode({"api-version": api_version})
        headers = {"Content-Type": "application/json", "api-key": self.api_key}
        parsed = urllib.parse.urlparse(self.endpoint)
        if self._is_foundry_project_endpoint():
            foundry_base = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, "", "", "", "")).rstrip("/")
            return [(f"{foundry_base}/models/chat/completions?{query}", headers, True)]
        return [(f"{self.endpoint}/openai/deployments/{encoded_deployment}/chat/completions?{query}", headers, False)]

    def _is_foundry_project_endpoint(self) -> bool:
        parsed = urllib.parse.urlparse(self.endpoint)
        return parsed.netloc.endswith(".services.ai.azure.com") and "/api/projects/" in parsed.path

    def _default_api_version(self, env_api_version: str = "") -> str:
        parsed = urllib.parse.urlparse(self.endpoint)
        if parsed.netloc.endswith(".services.ai.azure.com") and "/api/projects/" in parsed.path:
            return FOUNDRY_API_VERSION
        return env_api_version or CLASSIC_AZURE_OPENAI_API_VERSION


def create_stage5_incident_candidates(
    *,
    source_package_path: str | Path,
    canonical_incident_record_path: str | Path,
    timeline_events_path: str | Path,
    stage4_evidence_chunks_path: str | Path,
    source_artifacts_enriched_path: str | Path,
    output_dir: str | Path,
    runbook_llm_client: Stage5RunbookCandidateClient,
    playbook_llm_clients: dict[str, Stage5PlaybookCandidateClient],
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, tuple[list[dict[str, Any]], dict[str, Any]]]]:
    package = read_json(source_package_path)
    canonical_record = read_json(canonical_incident_record_path)
    timeline = read_json(timeline_events_path)
    evidence_handoff = read_json(stage4_evidence_chunks_path)
    artifacts = read_json(source_artifacts_enriched_path)
    if not isinstance(artifacts, list):
        raise ValueError("source_artifacts_enriched.json must contain a list.")

    packet = build_stage5_packet(
        package=package,
        canonical_record=canonical_record,
        timeline=timeline,
        evidence_handoff=evidence_handoff,
        artifacts=artifacts,
    )
    known = _known_refs(packet, artifacts)

    runbook_response = runbook_llm_client.discover_runbook_candidates(packet)
    runbook_candidates = normalize_candidates(runbook_response, packet)
    runbook_candidates = merge_validation_diagnostics_into_recovery_candidates(runbook_candidates)
    runbook_candidates, runbook_report = validate_and_dedupe_candidates(runbook_candidates, packet, known)

    output_path = Path(output_dir)
    write_json(output_path / "stage5_runbook_candidate_packet.json", packet)
    write_json(output_path / "runbook_candidates.json", runbook_candidates)
    write_json(output_path / "runbook_candidate_extraction_report.json", runbook_report)
    write_stage5_runbook_candidate_review_markdown(
        output_path / "runbook_candidate_review.md",
        runbook_candidates,
        runbook_report,
        canonical_record,
    )

    playbook_results: dict[str, tuple[list[dict[str, Any]], dict[str, Any]]] = {}
    for mode_slug, playbook_llm_client in playbook_llm_clients.items():
        playbook_packet = _packet_for_playbook_discovery(packet, mode_slug)
        playbook_response = playbook_llm_client.discover_playbook_candidates(playbook_packet)
        playbook_candidates = normalize_playbook_candidates(playbook_response, packet)
        playbook_candidates, playbook_report = validate_and_dedupe_playbook_candidates(playbook_candidates, packet, known)
        playbook_report["prompt_variant"] = mode_slug
        playbook_output_path = output_path / mode_slug
        write_json(playbook_output_path / "stage5_playbook_candidate_packet.json", playbook_packet)
        write_json(playbook_output_path / "playbook_candidates.json", playbook_candidates)
        write_json(playbook_output_path / "playbook_candidate_extraction_report.json", playbook_report)
        write_stage5_playbook_candidate_review_markdown(
            playbook_output_path / "playbook_candidate_review.md",
            playbook_candidates,
            playbook_report,
            canonical_record,
        )
        playbook_results[mode_slug] = (playbook_candidates, playbook_report)

    write_json(
        output_path / "incident_source_package.json",
        _package_with_stage5_refs(
            package,
            output_path,
            runbook_report,
            {mode: report for mode, (_candidates, report) in playbook_results.items()},
        ),
    )
    return runbook_candidates, runbook_report, playbook_results


def build_stage5_packet(
    *,
    package: dict[str, Any],
    canonical_record: dict[str, Any],
    timeline: dict[str, Any],
    evidence_handoff: dict[str, Any],
    artifacts: list[dict[str, Any]],
) -> dict[str, Any]:
    source_bundle = package.get("source_bundle") or {}
    source_package = {
        "source_package_id": package.get("source_package_id"),
        "source_id": package.get("source_id"),
        "source_case_id": package.get("source_case_id") or canonical_record.get("source_case_id"),
        "source_title": package.get("source_title"),
        "source_type": package.get("source_type") or "incident_case",
        "ingestion_batch_id": package.get("ingestion_batch_id"),
        "source_metadata": package.get("source_metadata") or {},
    }
    return {
        "packet_type": "stage_5_incident_runbook_candidate_discovery_packet",
        "schema_version": "0.1",
        "source_package": source_package,
        "source_bundle_summary": {
            "stage_status": source_bundle.get("stage_status") or {},
            "file_refs": source_bundle.get("file_refs") or {},
            "warnings": source_bundle.get("warnings") or [],
        },
        "canonical_incident_record": _compact_canonical_record(canonical_record),
        "timeline_events": [_compact_event(event) for event in (timeline.get("events") or [])],
        "artifact_evidence": [_compact_artifact(artifact) for artifact in artifacts],
        "evidence_chunk_index": evidence_handoff.get("chunk_index") or [],
        "page_text_chunks": [_compact_page_text_chunk(chunk) for chunk in evidence_handoff.get("page_text_chunks") or []],
        "artifact_evidence_chunks": evidence_handoff.get("artifact_evidence_chunks") or [],
        "instructions": [
            "Extract only reusable incident-derived runbook/procedure candidates.",
            "Candidates are lightweight source-specific records, not canonical runbooks.",
            "Use only incident evidence from this packet.",
            "Do not create playbooks, workflows, trigger conditions, routing logic, decision trees, or ML labels.",
            "Do not infer root cause, commands, thresholds, system names, or outcomes not supported by evidence.",
        ],
    }


def normalize_candidates(response: dict[str, Any], packet: dict[str, Any]) -> list[dict[str, Any]]:
    raw_candidates = response.get("candidates") if isinstance(response.get("candidates"), list) else []
    source = packet.get("source_package") or {}
    canonical = packet.get("canonical_incident_record") or {}
    case_id = str(source.get("source_case_id") or canonical.get("source_case_id") or "").strip()
    normalized: list[dict[str, Any]] = []
    for index, candidate in enumerate(raw_candidates, start=1):
        if not isinstance(candidate, dict):
            continue
        record = dict(candidate)
        title = str(record.get("title") or f"Incident Procedure Candidate {index}").strip()
        record["candidate_id"] = _candidate_id(record.get("candidate_id"), case_id, title)
        record["title"] = title
        record["candidate_goal"] = str(record.get("candidate_goal") or record.get("summary") or "").strip()
        record["likely_procedure_type"] = _allowed(record.get("likely_procedure_type"), ALLOWED_PROCEDURE_TYPES, "diagnostic")
        record["likely_role_required"] = _allowed(record.get("likely_role_required"), ALLOWED_ROLES, "L2_support")
        record["support_safe"] = record.get("support_safe") if isinstance(record.get("support_safe"), bool) else None
        record["summary"] = str(record.get("summary") or "").strip()
        record["rough_steps"] = _string_list(record.get("rough_steps"))
        record["expected_result"] = str(record.get("expected_result") or "").strip()
        record["failure_or_escalation_notes"] = _string_list(record.get("failure_or_escalation_notes"))
        record["access_or_tools_needed"] = _string_list(record.get("access_or_tools_needed"))
        record["related_context_ids"] = []
        record["related_artifact_ids"] = _string_list(record.get("related_artifact_ids"))
        record["related_event_ids"] = _string_list(record.get("related_event_ids"))
        record["source_refs"] = _dict_list(record.get("source_refs"))
        if not record["source_refs"]:
            record["source_refs"] = _merge_source_refs(
                ref
                for node in record["nodes"]
                for ref in node.get("source_refs") or []
            )
        record["evidence_source_refs"] = _dict_list(record.get("evidence_source_refs")) or list(record["source_refs"])
        record["source_id"] = str(record.get("source_id") or source.get("source_id") or f"case_{case_id}").strip()
        record["source_type"] = "incident_case"
        record["source_title"] = str(record.get("source_title") or source.get("source_title") or "").strip()
        record["source_version"] = str(record.get("source_version") or "").strip()
        record["ingestion_batch_id"] = str(record.get("ingestion_batch_id") or source.get("ingestion_batch_id") or "").strip()
        record["confidence"] = _allowed(record.get("confidence"), ALLOWED_CONFIDENCE, "medium")
        record["candidate_status"] = "needs_review"
        record["extraction_notes"] = _string_list(record.get("extraction_notes"))
        metadata = record.get("metadata") if isinstance(record.get("metadata"), dict) else {}
        metadata["created_by"] = "incident_runbook_candidate_discovery_agent"
        metadata["source_quality"] = "incident_case"
        metadata["incident_context"] = {
            "case_id": case_id,
            "site": canonical.get("site_label") or "",
            "incident_start_time": canonical.get("reported_at") or "",
            "incident_resolved_time": canonical.get("resolved_at") or "",
            "time_to_resolve": canonical.get("resolution_time") or "",
            "resolution_confirmed": _resolution_confirmed(canonical),
        }
        record["metadata"] = metadata
        normalized.append(record)
    return normalized


def normalize_playbook_candidates(response: dict[str, Any], packet: dict[str, Any]) -> list[dict[str, Any]]:
    raw_candidates = response.get("playbook_candidates") if isinstance(response.get("playbook_candidates"), list) else []
    source = packet.get("source_package") or {}
    canonical = packet.get("canonical_incident_record") or {}
    case_id = str(source.get("source_case_id") or canonical.get("source_case_id") or "").strip()
    top_level_source_id = str(response.get("source_id") or "").strip()
    top_level_source_title = str(response.get("source_title") or "").strip()
    top_level_source_version = str(response.get("source_version") or "").strip()
    top_level_ingestion_batch_id = str(response.get("ingestion_batch_id") or "").strip()
    extraction_mode = str(response.get("extraction_mode") or "").strip()
    normalized: list[dict[str, Any]] = []
    for index, candidate in enumerate(raw_candidates, start=1):
        if not isinstance(candidate, dict):
            continue
        record = dict(candidate)
        for legacy_field in [
            "candidate_status",
            "incident_pattern",
            "likely_issue_category",
            "issue_category",
            "category",
            "metadata",
        ]:
            record.pop(legacy_field, None)
        title = str(record.get("title") or f"Incident Playbook Candidate {index}").strip()
        record["playbook_candidate_id"] = _playbook_candidate_id(record.get("playbook_candidate_id"), case_id, title)
        record["title"] = title
        summary = str(record.get("user_facing_summary") or record.get("summary") or "").strip()
        record["user_facing_summary"] = summary
        record["summary"] = summary
        record["playbook_goal"] = str(record.get("playbook_goal") or summary).strip()
        record["observed_entry_symptoms"] = _string_list(record.get("observed_entry_symptoms"))
        record["negative_or_absent_signals"] = _string_list(record.get("negative_or_absent_signals"))
        record["support_user_language_examples"] = _string_list(record.get("support_user_language_examples"))
        record["tentative_internal_patterns"] = _string_list(record.get("tentative_internal_patterns"))
        record["internal_pattern_notes"] = str(record.get("internal_pattern_notes") or "").strip()
        record["affected_systems_or_components"] = _string_list(record.get("affected_systems_or_components"))
        record["separability_reason"] = str(record.get("separability_reason") or "").strip()
        record["confidence"] = _allowed(record.get("confidence"), ALLOWED_CONFIDENCE, "medium")
        record["confidence_reason"] = str(record.get("confidence_reason") or "").strip()
        record["nodes"] = [_normalize_playbook_node(node, index) for index, node in enumerate(record.get("nodes") or [], start=1) if isinstance(node, dict)]
        node_roles = {
            role
            for node in record["nodes"]
            for role in _string_list(node.get("allowed_roles"))
            if role in ALLOWED_ROLES
        }
        record["likely_roles"] = sorted(node_roles) or [
            role for role in _string_list(record.get("likely_roles")) if role in ALLOWED_ROLES
        ] or ["L2_support"]
        record["branch_hints"] = _dict_list(record.get("branch_hints"))
        record["escalation_gates"] = _dict_list(record.get("escalation_gates"))
        record["validation_gates"] = _dict_list(record.get("validation_gates"))
        record["runbook_placeholders"] = _dict_list(record.get("runbook_placeholders"))
        record["ignored_non_playbook_content"] = _dict_list(record.get("ignored_non_playbook_content"))
        record["related_artifact_ids"] = _string_list(record.get("related_artifact_ids"))
        record["related_event_ids"] = _string_list(record.get("related_event_ids"))
        record["source_refs"] = _dict_list(record.get("source_refs"))
        record["evidence_source_refs"] = _dict_list(record.get("evidence_source_refs")) or list(record["source_refs"])
        record["source_id"] = str(record.get("source_id") or top_level_source_id or source.get("source_id") or f"case_{case_id}").strip()
        record["source_type"] = "incident_case"
        record["source_title"] = str(record.get("source_title") or top_level_source_title or source.get("source_title") or "").strip()
        record["source_version"] = str(record.get("source_version") or top_level_source_version or "").strip()
        record["ingestion_batch_id"] = str(record.get("ingestion_batch_id") or top_level_ingestion_batch_id or source.get("ingestion_batch_id") or "").strip()
        record["extraction_mode"] = str(record.get("extraction_mode") or extraction_mode or "").strip()
        record["extraction_notes"] = _string_list(record.get("extraction_notes"))
        record["incident_context"] = {
            "case_id": case_id,
            "site": canonical.get("site_label") or "",
            "incident_start_time": canonical.get("reported_at") or "",
            "incident_resolved_time": canonical.get("resolved_at") or "",
            "time_to_resolve": canonical.get("resolution_time") or "",
            "resolution_confirmed": _resolution_confirmed(canonical),
        }
        normalized.append(record)
    return normalized


def _normalize_playbook_node(node: dict[str, Any], index: int) -> dict[str, Any]:
    node_type = str(node.get("node_type") or "").strip()
    allowed_node_types = {
        "diagnostic_decision",
        "procedure_reference",
        "escalation_gate",
        "validation_gate",
        "branching_condition",
        "recovery_phase_marker",
    }
    intent = str(node.get("intent") or node.get("goal") or "").strip()
    return {
        "node_id": str(node.get("node_id") or f"node_{index}").strip(),
        "node_order": int(node.get("node_order") or index),
        "node_type": node_type if node_type in allowed_node_types else "diagnostic_decision",
        "title": str(node.get("title") or f"Node {index}").strip(),
        "intent": intent,
        "goal": intent,
        "runbook_placeholder": str(node.get("runbook_placeholder") or node.get("needed_runbook_capability") or "").strip(),
        "allowed_roles": [
            role for role in _string_list(node.get("allowed_roles")) if role in ALLOWED_ROLES
        ],
        "source_supported_description": str(node.get("source_supported_description") or "").strip(),
        "needed_runbook_capability": str(node.get("runbook_placeholder") or node.get("needed_runbook_capability") or "").strip(),
        "expected_or_observed_result": str(node.get("expected_or_observed_result") or "").strip(),
        "stop_or_escalation_note": str(node.get("stop_or_escalation_note") or "").strip(),
        "related_artifact_ids": _string_list(node.get("related_artifact_ids")),
        "related_event_ids": _string_list(node.get("related_event_ids")),
        "source_refs": _dict_list(node.get("source_refs")),
    }


def validate_and_dedupe_candidates(
    candidates: list[dict[str, Any]],
    packet: dict[str, Any],
    known: dict[str, set[str]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    warnings: list[str] = []
    validation_errors: list[str] = []
    accepted: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    dropped = 0
    deduped = 0
    for candidate in candidates:
        errors = validate_candidate(candidate, known)
        if errors:
            dropped += 1
            warnings.append(f"Dropped {candidate.get('candidate_id')}: " + "; ".join(errors))
            continue
        key = (_norm(candidate.get("title")), _norm(candidate.get("candidate_goal")))
        if key in seen:
            deduped += 1
            continue
        seen.add(key)
        accepted.append(candidate)
    counts_by_type = Counter(str(c.get("likely_procedure_type") or "unknown") for c in accepted)
    counts_by_role = Counter(str(c.get("likely_role_required") or "unknown") for c in accepted)
    report = {
        "stage": "stage_5_incident_runbook_candidate_discovery",
        "llm_used": True,
        "prompt": "stage5_runbook_candidate_discovery_prompt.md",
        "source_id": packet.get("source_package", {}).get("source_id"),
        "source_case_id": packet.get("source_package", {}).get("source_case_id"),
        "candidate_count": len(accepted),
        "candidate_counts_by_type": dict(sorted(counts_by_type.items())),
        "candidate_counts_by_role": dict(sorted(counts_by_role.items())),
        "candidates_with_artifacts": sum(1 for c in accepted if c.get("related_artifact_ids")),
        "candidates_with_events": sum(1 for c in accepted if c.get("related_event_ids")),
        "candidates_missing_source_refs": sum(1 for c in accepted if not c.get("source_refs")),
        "dropped_candidate_count": dropped,
        "deduped_candidate_count": deduped,
        "validation_errors": validation_errors,
        "warnings": warnings,
        "notes": [
            "Stage 5 creates incident-derived runbook candidates only.",
            "Stage 5 does not create playbooks, workflows, routing logic, trigger conditions, or decision trees.",
            "All candidates remain needs_review and require shared candidate-pool/canonical runbook stages before production use.",
        ],
        "built_at": datetime.now(timezone.utc).isoformat(),
    }
    return accepted, report


def validate_and_dedupe_playbook_candidates(
    candidates: list[dict[str, Any]],
    packet: dict[str, Any],
    known: dict[str, set[str]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    warnings: list[str] = []
    accepted: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    dropped = 0
    deduped = 0
    nodes_missing_runbook_placeholder = 0
    for candidate in candidates:
        errors = validate_playbook_candidate(candidate, known)
        if errors:
            dropped += 1
            warnings.append(f"Dropped {candidate.get('playbook_candidate_id')}: " + "; ".join(errors))
            continue
        if not candidate.get("source_refs") and not candidate.get("evidence_source_refs"):
            warnings.append(f"{candidate.get('playbook_candidate_id')} is missing candidate-level source_refs")
        for node in candidate.get("nodes") or []:
            if not str(node.get("runbook_placeholder") or node.get("needed_runbook_capability") or "").strip():
                nodes_missing_runbook_placeholder += 1
                warnings.append(
                    f"{candidate.get('playbook_candidate_id')} node {node.get('node_id')} is missing runbook_placeholder"
                )
        key = (_norm(candidate.get("title")), _norm(candidate.get("playbook_goal")))
        if key in seen:
            deduped += 1
            continue
        seen.add(key)
        accepted.append(candidate)
    report = {
        "stage": "stage_5_incident_playbook_candidate_discovery",
        "llm_used": True,
        "prompt": "stage5_playbook_candidate_discovery_prompt.md",
        "source_id": packet.get("source_package", {}).get("source_id"),
        "source_case_id": packet.get("source_package", {}).get("source_case_id"),
        "playbook_candidate_count": len(accepted),
        "candidate_count": len(accepted),
        "nodes_count": sum(len(candidate.get("nodes") or []) for candidate in accepted),
        "nodes_missing_runbook_placeholder": nodes_missing_runbook_placeholder,
        "candidates_with_artifacts": sum(1 for c in accepted if c.get("related_artifact_ids")),
        "candidates_with_events": sum(1 for c in accepted if c.get("related_event_ids")),
        "candidates_missing_source_refs": sum(1 for c in accepted if not c.get("source_refs")),
        "dropped_candidate_count": dropped,
        "deduped_candidate_count": deduped,
        "validation_errors": [],
        "warnings": warnings,
        "notes": [
            "Stage 5 creates incident-derived playbook candidates in a separate LLM call from runbook candidate discovery.",
            "Playbook candidates describe response logic and plain-text runbook placeholders, not canonical runbook IDs.",
            "Candidates require shared candidate-pool and canonical playbook stages before production use.",
        ],
        "built_at": datetime.now(timezone.utc).isoformat(),
    }
    return accepted, report


def validate_playbook_candidate(candidate: dict[str, Any], known: dict[str, set[str]]) -> list[str]:
    errors: list[str] = []
    for field in ["playbook_candidate_id", "title", "playbook_goal", "source_id", "ingestion_batch_id"]:
        if not str(candidate.get(field) or "").strip():
            errors.append(f"missing {field}")
    if not str(candidate.get("user_facing_summary") or candidate.get("summary") or "").strip():
        errors.append("missing user_facing_summary")
    nodes = candidate.get("nodes") or []
    if len(nodes) < 2:
        errors.append("playbook candidates need at least two source-supported nodes")
    for field in FORBIDDEN_FIELDS:
        if field in candidate:
            errors.append(f"forbidden field present: {field}")
    if _mentions_specific_runbook_binding(candidate):
        errors.append("playbook candidate appears to bind directly to a specific runbook ID")
    for artifact_id in candidate.get("related_artifact_ids") or []:
        if artifact_id not in known["artifact_ids"]:
            errors.append(f"unknown related_artifact_id: {artifact_id}")
    for event_id in candidate.get("related_event_ids") or []:
        if event_id not in known["event_ids"]:
            errors.append(f"unknown related_event_id: {event_id}")
    for node in nodes:
        if not str(node.get("title") or "").strip():
            errors.append("playbook node missing title")
        if not str(node.get("goal") or node.get("source_supported_description") or "").strip():
            errors.append(f"playbook node missing goal/description: {node.get('node_id')}")
        for artifact_id in node.get("related_artifact_ids") or []:
            if artifact_id not in known["artifact_ids"]:
                errors.append(f"unknown node related_artifact_id: {artifact_id}")
        for event_id in node.get("related_event_ids") or []:
            if event_id not in known["event_ids"]:
                errors.append(f"unknown node related_event_id: {event_id}")
        errors.extend(_validate_source_refs(node.get("source_refs") or [], known))
    errors.extend(_validate_source_refs([*(candidate.get("source_refs") or []), *(candidate.get("evidence_source_refs") or [])], known))
    return errors


def merge_validation_diagnostics_into_recovery_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    recovery_candidates = [candidate for candidate in candidates if candidate.get("likely_procedure_type") == "recovery"]
    if not recovery_candidates:
        return candidates
    primary_recovery = max(recovery_candidates, key=lambda candidate: len(candidate.get("rough_steps") or []))
    merged: list[dict[str, Any]] = []
    for candidate in candidates:
        if candidate is primary_recovery:
            merged.append(candidate)
            continue
        if candidate.get("likely_procedure_type") == "diagnostic" and _is_validation_followup_candidate(candidate):
            _merge_candidate_into(primary_recovery, candidate)
            continue
        merged.append(candidate)
    return merged


def _is_validation_followup_candidate(candidate: dict[str, Any]) -> bool:
    text = " ".join(
        [
            str(candidate.get("title") or ""),
            str(candidate.get("candidate_goal") or ""),
            str(candidate.get("summary") or ""),
            " ".join(str(step) for step in candidate.get("rough_steps") or []),
        ]
    ).lower()
    has_validation_language = any(term in text for term in ["validate", "verify", "confirm", "check"])
    has_response_target = any(term in text for term in ["api", "endpoint", "response", "status 200", "http 200"])
    return has_validation_language and has_response_target


def _merge_candidate_into(target: dict[str, Any], source: dict[str, Any]) -> None:
    if not _candidate_has_validation_steps(target):
        target["rough_steps"] = _merge_unique_values(target.get("rough_steps") or [], source.get("rough_steps") or [])
    target["failure_or_escalation_notes"] = _merge_unique_values(
        target.get("failure_or_escalation_notes") or [],
        source.get("failure_or_escalation_notes") or [],
    )
    target["access_or_tools_needed"] = _merge_unique_values(
        target.get("access_or_tools_needed") or [],
        source.get("access_or_tools_needed") or [],
    )
    target["related_artifact_ids"] = _merge_unique_values(
        target.get("related_artifact_ids") or [],
        source.get("related_artifact_ids") or [],
    )
    target["related_event_ids"] = _merge_unique_values(
        target.get("related_event_ids") or [],
        source.get("related_event_ids") or [],
    )
    target["source_refs"] = _merge_unique_values(target.get("source_refs") or [], source.get("source_refs") or [])
    target["evidence_source_refs"] = _merge_unique_values(
        target.get("evidence_source_refs") or [],
        source.get("evidence_source_refs") or [],
    )
    target["extraction_notes"] = _merge_unique_values(
        target.get("extraction_notes") or [],
        [
            *(source.get("extraction_notes") or []),
            f"Merged validation follow-up candidate into this recovery runbook: {source.get('candidate_id')}",
        ],
    )
    if source.get("expected_result") and source.get("expected_result") not in str(target.get("expected_result") or ""):
        target["expected_result"] = (str(target.get("expected_result") or "").rstrip(".") + ". " + str(source["expected_result"])).strip()


def _candidate_has_validation_steps(candidate: dict[str, Any]) -> bool:
    text = " ".join(str(step) for step in candidate.get("rough_steps") or []).lower()
    has_validation_language = any(term in text for term in ["validate", "verify", "confirm", "check"])
    has_response_target = any(term in text for term in ["api", "endpoint", "request", "response", "status 200", "http 200"])
    return has_validation_language and has_response_target


def _merge_unique_values(existing: list[Any], incoming: list[Any]) -> list[Any]:
    merged: list[Any] = []
    seen: set[str] = set()
    for value in [*existing, *incoming]:
        marker = json.dumps(value, sort_keys=True)
        if marker in seen:
            continue
        seen.add(marker)
        merged.append(value)
    return merged


def validate_candidate(candidate: dict[str, Any], known: dict[str, set[str]]) -> list[str]:
    errors: list[str] = []
    for field in ["candidate_id", "title", "candidate_goal", "summary", "source_id", "ingestion_batch_id"]:
        if not str(candidate.get(field) or "").strip():
            errors.append(f"missing {field}")
    if not candidate.get("rough_steps"):
        errors.append("missing rough_steps")
    errors.extend(_validate_procedural_substance(candidate))
    if not candidate.get("source_refs") and not candidate.get("evidence_source_refs"):
        errors.append("missing source_refs")
    for field in FORBIDDEN_FIELDS:
        if field in candidate:
            errors.append(f"forbidden field present: {field}")
    for artifact_id in candidate.get("related_artifact_ids") or []:
        if artifact_id not in known["artifact_ids"]:
            errors.append(f"unknown related_artifact_id: {artifact_id}")
    for event_id in candidate.get("related_event_ids") or []:
        if event_id not in known["event_ids"]:
            errors.append(f"unknown related_event_id: {event_id}")
    errors.extend(_validate_source_refs([*(candidate.get("source_refs") or []), *(candidate.get("evidence_source_refs") or [])], known))
    return errors


def _validate_source_refs(refs: list[Any], known: dict[str, set[str]]) -> list[str]:
    errors: list[str] = []
    for ref in refs:
        if not isinstance(ref, dict):
            errors.append("source ref must be an object")
            continue
        page_ref = ref.get("page_ref")
        artifact_id = ref.get("artifact_id")
        event_id = ref.get("event_id")
        chunk_id = ref.get("chunk_id")
        if page_ref and page_ref not in known["page_refs"]:
            errors.append(f"unknown page_ref: {page_ref}")
        if artifact_id and artifact_id not in known["artifact_ids"]:
            errors.append(f"unknown artifact_id in source ref: {artifact_id}")
        if event_id and event_id not in known["event_ids"]:
            errors.append(f"unknown event_id in source ref: {event_id}")
        if chunk_id and chunk_id not in known["chunk_ids"]:
            errors.append(f"unknown chunk_id: {chunk_id}")
    return errors


def _validate_procedural_substance(candidate: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    title_goal = f"{candidate.get('title') or ''} {candidate.get('candidate_goal') or ''}".lower()
    steps = [str(step or "").strip() for step in candidate.get("rough_steps") or [] if str(step or "").strip()]
    step_text = " ".join(steps).lower()
    action_step_count = sum(1 for step in steps if _starts_or_contains_action(step))
    if len(steps) < 3:
        errors.append("not enough procedural steps for a runbook candidate")
    if action_step_count < 2:
        errors.append("rough_steps do not contain enough concrete procedural actions")
    if any(term in title_goal for term in EVIDENCE_ONLY_TERMS) and not _has_recovery_or_validation_language(candidate):
        errors.append("candidate appears to be a passive evidence-capture card, not a runbook procedure")
    if "screenshot" in title_goal and not _has_recovery_or_validation_language(candidate):
        errors.append("screenshot-only candidates must be part of a broader diagnostic or recovery procedure")
    if _looks_like_vague_recovery_summary(candidate):
        errors.append("candidate appears to summarize a recovery without source-supported executable substeps")
    if candidate.get("related_artifact_ids") and not any("[Image support needed:" in step for step in steps):
        errors.append("image-supported candidates must include inline image support notes in rough_steps")
    if not _mentions_specific_operational_target(candidate):
        errors.append("candidate does not name a specific tool, screen, service, log, API, or operational target")
    if not str(candidate.get("expected_result") or "").strip():
        errors.append("missing expected_result")
    if not candidate.get("failure_or_escalation_notes"):
        errors.append("missing failure_or_escalation_notes")
    generic_phrases = ["review evidence", "investigate the issue", "document findings", "check everything"]
    if any(phrase in step_text for phrase in generic_phrases):
        errors.append("candidate contains generic non-procedural rough steps")
    return errors


def _looks_like_vague_recovery_summary(candidate: dict[str, Any]) -> bool:
    if candidate.get("likely_procedure_type") != "recovery":
        return False
    steps = [str(step or "").strip().lower() for step in candidate.get("rough_steps") or [] if str(step or "").strip()]
    if not steps:
        return True
    vague_action_count = sum(
        1
        for step in steps
        if re.search(r"\b(fix|correct|resolve|reset|repair)\b", step)
        and not re.search(
            r"\b(open|navigate|select|click|press|run|enter|command|wait|verify|confirm|check|status|log|event|service|api|response|field|button|control)\b",
            step,
        )
    )
    has_specific_execution = any(
        re.search(
            r"\b(command|run|click|press|select|navigate|status|event|log|api|response|field|button|control|wait|verify|confirm)\b",
            step,
        )
        for step in steps
    )
    return vague_action_count >= 1 and not has_specific_execution


def _starts_or_contains_action(step: str) -> bool:
    lowered = step.strip().lower()
    first = re.split(r"\W+", lowered, maxsplit=1)[0]
    return first in PROCEDURAL_ACTION_TERMS or any(f" {term} " in f" {lowered} " for term in PROCEDURAL_ACTION_TERMS)


def _has_recovery_or_validation_language(candidate: dict[str, Any]) -> bool:
    text = " ".join(
        [
            str(candidate.get("title") or ""),
            str(candidate.get("candidate_goal") or ""),
            str(candidate.get("summary") or ""),
            str(candidate.get("expected_result") or ""),
            " ".join(str(step) for step in candidate.get("rough_steps") or []),
        ]
    ).lower()
    return any(
        term in text
        for term in [
            "verify",
            "validate",
            "confirm",
            "restart",
            "reset",
            "recover",
            "service",
            "api",
            "status",
            "event viewer",
            "gateway",
            "rms",
            "hmi",
        ]
    )


def _mentions_specific_operational_target(candidate: dict[str, Any]) -> bool:
    text = " ".join(
        [
            str(candidate.get("title") or ""),
            str(candidate.get("candidate_goal") or ""),
            str(candidate.get("summary") or ""),
            " ".join(str(step) for step in candidate.get("rough_steps") or []),
            " ".join(str(tool) for tool in candidate.get("access_or_tools_needed") or []),
        ]
    ).lower()
    return any(
        term in text
        for term in [
            "gateway",
            "event viewer",
            "windows services",
            "service",
            "rms",
            "hmi",
            "api",
            "memory trend",
            "agv",
            "robot",
            "case",
            "salesforce",
            "log",
        ]
    )


def _mentions_specific_runbook_binding(candidate: dict[str, Any]) -> bool:
    text = " ".join(_iter_string_values(candidate)).lower()
    return bool(
        re.search(r"\b(proc|runbook|rb)_[a-z0-9_]+\b", text)
        or re.search(r"\buse\s+runbook\b", text)
        or re.search(r"\brunbook_id\b", text)
        or re.search(r"\bcanonical_runbook\b", text)
    )


def _iter_string_values(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from _iter_string_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_string_values(child)


def parse_llm_response(content: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(content, dict):
        return content
    text = content.strip()
    fence = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if fence:
        text = fence.group(1).strip()
    return json.loads(text)


def _compact_canonical_record(record: dict[str, Any]) -> dict[str, Any]:
    site = record.get("site") if isinstance(record.get("site"), dict) else {}
    return {
        "incident_id": record.get("incident_id"),
        "source_case_id": record.get("source_case_id"),
        "title": record.get("title"),
        "status": record.get("status"),
        "site_label": site.get("primary_label") or site.get("observed_location_text") or "",
        "reported_at": record.get("reported_at"),
        "resolved_at": record.get("resolved_at"),
        "resolution_time": record.get("resolution_time"),
        "downtime_minutes": record.get("downtime_minutes"),
        "incident_description": _truncate(record.get("incident_description"), MAX_CHARS),
        "customer_operational_impact": _truncate(record.get("customer_operational_impact"), MAX_CHARS),
        "what_resolved_it": _truncate(record.get("what_resolved_it"), MAX_CHARS),
        "symptoms": record.get("symptoms") or [],
        "systems_involved": record.get("systems_involved") or [],
        "source_refs": record.get("source_refs") or [],
    }


def _compact_event(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "event_id": event.get("event_id"),
        "event_order": event.get("event_order"),
        "timestamp": event.get("timestamp"),
        "timestamp_status": event.get("timestamp_status"),
        "event_type": event.get("event_type"),
        "actor_role": event.get("actor_role"),
        "summary": _truncate(event.get("summary"), MAX_CHARS),
        "details": _truncate(event.get("details"), MAX_CHARS),
        "systems": event.get("systems") or [],
        "source_refs": event.get("source_refs") or [],
        "artifact_refs": event.get("artifact_refs") or [],
        "evidence_chunk_refs": event.get("evidence_chunk_refs") or [],
        "confidence": event.get("confidence"),
        "uncertainties": event.get("uncertainties") or [],
    }


def _compact_page_text_chunk(chunk: dict[str, Any]) -> dict[str, Any]:
    return {
        "chunk_id": chunk.get("chunk_id"),
        "chunk_type": chunk.get("chunk_type"),
        "page_start": chunk.get("page_start"),
        "page_end": chunk.get("page_end"),
        "page_refs": chunk.get("page_refs") or [],
        "artifact_ids": chunk.get("artifact_ids") or [],
        "text": _truncate(chunk.get("text") or chunk.get("combined_text") or "", MAX_PAGE_CHUNK_TEXT_CHARS),
    }


def _compact_artifact(artifact: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_id": artifact.get("artifact_id"),
        "page_number": artifact.get("page_number"),
        "image_type": artifact.get("image_type"),
        "evidence_role": artifact.get("evidence_role"),
        "short_description": _truncate(artifact.get("short_description"), MAX_CHARS),
        "retrieval_text": _truncate(artifact.get("retrieval_text"), MAX_CHARS),
        "source_supported_claims": artifact.get("source_supported_claims") or [],
        "supports": artifact.get("supports") or {},
        "candidate_support_hints": artifact.get("candidate_support_hints") or {},
        "source_refs": artifact.get("source_refs") or [],
    }


def _known_refs(packet: dict[str, Any], artifacts: list[dict[str, Any]]) -> dict[str, set[str]]:
    page_refs: set[str] = set()
    artifact_ids = {str(a.get("artifact_id")) for a in artifacts if a.get("artifact_id")}
    event_ids = {str(e.get("event_id")) for e in packet.get("timeline_events") or [] if e.get("event_id")}
    chunk_ids: set[str] = set()
    for ref in packet.get("evidence_chunk_index") or []:
        if isinstance(ref, dict) and ref.get("chunk_id"):
            chunk_ids.add(str(ref["chunk_id"]))
        for page_ref in ref.get("page_refs") or []:
            page_refs.add(str(page_ref))
        for artifact_id in ref.get("artifact_ids") or []:
            artifact_ids.add(str(artifact_id))
    for chunk in packet.get("artifact_evidence_chunks") or []:
        if isinstance(chunk, dict) and chunk.get("chunk_id"):
            chunk_ids.add(str(chunk["chunk_id"]))
        for artifact_id in chunk.get("artifact_ids") or []:
            artifact_ids.add(str(artifact_id))
        for card in chunk.get("cards") or []:
            if not isinstance(card, dict):
                continue
            if card.get("page_ref"):
                page_refs.add(str(card["page_ref"]))
            for ref in card.get("source_refs") or []:
                if isinstance(ref, dict) and ref.get("page_ref"):
                    page_refs.add(str(ref["page_ref"]))
                if isinstance(ref, dict) and ref.get("artifact_id"):
                    artifact_ids.add(str(ref["artifact_id"]))
    for chunk in packet.get("page_text_chunks") or []:
        if isinstance(chunk, dict) and chunk.get("chunk_id"):
            chunk_ids.add(str(chunk["chunk_id"]))
        for page_ref in chunk.get("page_refs") or []:
            page_refs.add(str(page_ref))
        for artifact_id in chunk.get("artifact_ids") or []:
            artifact_ids.add(str(artifact_id))
    for item in [*packet.get("timeline_events", []), *packet.get("artifact_evidence", [])]:
        for ref in item.get("source_refs") or []:
            if isinstance(ref, dict) and ref.get("page_ref"):
                page_refs.add(str(ref["page_ref"]))
            if isinstance(ref, dict) and ref.get("chunk_id"):
                chunk_ids.add(str(ref["chunk_id"]))
    return {"page_refs": page_refs, "artifact_ids": artifact_ids, "event_ids": event_ids, "chunk_ids": chunk_ids}


def _package_with_stage5_refs(
    package: dict[str, Any],
    output_path: Path,
    report: dict[str, Any],
    playbook_reports: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    enriched_package = dict(package)
    source_bundle = dict(enriched_package.get("source_bundle") or {})
    stage_status = dict(source_bundle.get("stage_status") or {})
    stage_status.update(
        {
            "stage_5": "complete",
            "ready_for_shared_candidate_pool": not report.get("validation_errors")
            and not any((playbook_report or {}).get("validation_errors") for playbook_report in (playbook_reports or {}).values()),
        }
    )
    file_refs = dict(source_bundle.get("file_refs") or {})
    file_refs.update(
        {
            "runbook_candidates": str(output_path / "runbook_candidates.json"),
            "runbook_candidate_extraction_report": str(output_path / "runbook_candidate_extraction_report.json"),
            "runbook_candidate_review": str(output_path / "runbook_candidate_review.md"),
            "stage5_runbook_candidate_packet": str(output_path / "stage5_runbook_candidate_packet.json"),
        }
    )
    for mode_slug in sorted((playbook_reports or {}).keys()):
        mode_path = output_path / mode_slug
        file_refs.update(
            {
                f"playbook_candidates_{mode_slug}": str(mode_path / "playbook_candidates.json"),
                f"playbook_candidate_extraction_report_{mode_slug}": str(mode_path / "playbook_candidate_extraction_report.json"),
                f"playbook_candidate_review_{mode_slug}": str(mode_path / "playbook_candidate_review.md"),
                f"stage5_playbook_candidate_packet_{mode_slug}": str(mode_path / "stage5_playbook_candidate_packet.json"),
            }
        )
    source_bundle["stage_status"] = stage_status
    source_bundle["file_refs"] = file_refs
    enriched_package["source_bundle"] = source_bundle
    enriched_package["stage5_output_refs"] = file_refs
    return enriched_package


def _candidate_id(value: Any, case_id: str, title: str) -> str:
    existing = str(value or "").strip()
    prefix = f"candidate_incident_{case_id}_" if case_id else "candidate_incident_"
    if existing.startswith(prefix):
        return existing
    return prefix + _slug(title)


def _playbook_candidate_id(value: Any, case_id: str, title: str) -> str:
    existing = str(value or "").strip()
    prefix = f"playbook_candidate_incident_{case_id}_" if case_id else "playbook_candidate_incident_"
    if existing.startswith(prefix):
        return existing
    return prefix + _slug(title)


def _packet_for_playbook_discovery(packet: dict[str, Any], mode_slug: str) -> dict[str, Any]:
    playbook_packet = dict(packet)
    playbook_packet["packet_type"] = "stage_5_incident_playbook_candidate_discovery_packet"
    playbook_packet["prompt_variant"] = mode_slug
    playbook_packet["instructions"] = [
        "Extract incident-derived playbook candidates in a separate call from runbook candidate discovery.",
        "Playbook candidates describe response logic, checks, actions, validation, and needed runbook capabilities.",
        "Do not bind playbook nodes to specific runbook IDs.",
        "Use only incident evidence from this packet.",
        "Do not create canonical workflows, routing automation, issue categories, decision trees, or ML labels.",
    ]
    return playbook_packet


def _resolution_confirmed(canonical: dict[str, Any]) -> bool | None:
    status = str(canonical.get("status") or "").lower()
    resolved = canonical.get("resolved_at") or canonical.get("what_resolved_it")
    if "resolved" in status or resolved:
        return True
    if "open" in status or "unresolved" in status:
        return False
    return None


def _allowed(value: Any, allowed: set[str], default: str) -> str:
    text = str(value or "").strip()
    return text if text in allowed else default


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _dict_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _merge_source_refs(refs: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    seen: set[str] = set()
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        key = json.dumps(ref, sort_keys=True, ensure_ascii=False)
        if key in seen:
            continue
        seen.add(key)
        merged.append(ref)
    return merged


def _truncate(value: Any, max_chars: int) -> str:
    text = " ".join(str(value or "").split())
    if len(text) <= max_chars:
        return text
    return text[: max(0, max_chars - 3)].rstrip() + "..."


def _norm(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def _slug(value: str) -> str:
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")) or "procedure"


def _clean_env_value(value: str | None) -> str:
    cleaned = (value or "").strip().strip('"').strip("'")
    if cleaned in {"", "your-api-version", "your_api_version", "<api-version>"}:
        return ""
    return cleaned


def _urlopen_no_proxy(request: urllib.request.Request, timeout: int) -> Any:
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    return opener.open(request, timeout=timeout)
