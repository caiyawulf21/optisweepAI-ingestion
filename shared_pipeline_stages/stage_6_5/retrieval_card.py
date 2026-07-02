from __future__ import annotations

import re
from typing import Any

from shared_pipeline_stages.stage_6_5.schemas import RetrievalCard

MAX_RETRIEVAL_TEXT_CHARS = 12000
MAX_STEP_SUMMARIES = 40

ACTION_VERB_PATTERN = re.compile(
    r"\b(check|verify|review|inspect|start|stop|add|remove|reset|recover|restart|install|replace|configure|download|upload|open|close|enable|disable)\b",
    re.IGNORECASE,
)


def build_retrieval_card(runbook: dict[str, Any]) -> RetrievalCard:
    metadata = runbook.get("metadata") or {}
    steps = runbook.get("steps") or []
    step_summaries = _step_summaries(steps)
    tools = _string_list(runbook.get("access_or_tools_needed"))
    success_criteria = _string_list(runbook.get("success_criteria"))
    failure_conditions = _string_list(runbook.get("failure_conditions"))
    action_verbs = _extract_action_verbs(runbook, step_summaries)
    card = RetrievalCard(
        finalized_runbook_id=str(runbook.get("procedure_id") or ""),
        candidate_id=str(runbook.get("candidate_id") or ""),
        title=str(runbook.get("title") or ""),
        summary=str(runbook.get("summary") or ""),
        when_to_use=str(runbook.get("when_to_use") or ""),
        procedure_type=str(runbook.get("procedure_type") or ""),
        role_required=str(runbook.get("role_required") or runbook.get("responsible_role") or ""),
        tools=tools,
        action_verbs=action_verbs,
        step_summaries=step_summaries,
        success_criteria=success_criteria,
        failure_conditions=failure_conditions,
        source_candidate_ids=[str(value) for value in runbook.get("source_candidate_ids") or []],
        source_id=str(metadata.get("source_id") or ""),
        source_type=str(metadata.get("source_type") or ""),
        validation_status=str(runbook.get("validation_status") or ""),
        source_path=str(runbook.get("_source_path") or ""),
    )
    card.retrieval_text = build_retrieval_text(card)
    return card


def build_retrieval_text(card: RetrievalCard) -> str:
    parts = [
        card.title,
        card.summary,
        card.when_to_use,
        card.procedure_type,
        card.role_required,
        " ".join(card.tools),
        " ".join(card.action_verbs),
        " ".join(card.step_summaries),
        " ".join(card.success_criteria),
        " ".join(card.failure_conditions),
    ]
    text = " ".join(part.strip() for part in parts if part and part.strip())
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > MAX_RETRIEVAL_TEXT_CHARS:
        return text[:MAX_RETRIEVAL_TEXT_CHARS]
    return text


def _step_summaries(steps: list[Any]) -> list[str]:
    summaries: list[str] = []
    for step in steps[:MAX_STEP_SUMMARIES]:
        if not isinstance(step, dict):
            continue
        title = str(step.get("title") or "").strip()
        instruction = str(step.get("instruction") or "").strip()
        if title and instruction:
            summaries.append(f"{title}: {instruction}")
        elif title:
            summaries.append(title)
        elif instruction:
            summaries.append(instruction)
    return summaries


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _extract_action_verbs(runbook: dict[str, Any], step_summaries: list[str]) -> list[str]:
    text = " ".join(
        [
            str(runbook.get("title") or ""),
            str(runbook.get("summary") or ""),
            " ".join(step_summaries),
        ]
    )
    seen: set[str] = set()
    verbs: list[str] = []
    for match in ACTION_VERB_PATTERN.finditer(text):
        verb = match.group(1).lower()
        if verb not in seen:
            seen.add(verb)
            verbs.append(verb)
    return verbs
