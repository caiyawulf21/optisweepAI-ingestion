"""Tool 2 -- classify_candidate (AGENT_DESIGN_NOTES.md §4.2).

Given one raw claim candidate + surrounding Brain context, decides what
kind of Brain record this candidate should become, per the locked §2
boundary (Entity/Capability/Claim/Relationship). The boundary test is
applied by the LLM call itself, per §3's finding that this judgment
cannot be safely mechanized with keyword/regex heuristics -- no separate
Python function duplicates it here.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from brain_service.context import get_brain_context
from brain_service.types import ClassifiedCandidate
from providers.llm import LLMProvider
from providers.storage import StorageProvider

_PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "classify_candidate.md"


def _load_prompt() -> str:
    return _PROMPT_PATH.read_text(encoding="utf-8")


def classify_candidate(
    llm: LLMProvider,
    storage: StorageProvider,
    *,
    candidate_text: str,
    evidence_id: str,
    likely_entity_ids: list[str] | None = None,
) -> ClassifiedCandidate:
    context_packet = get_brain_context(
        storage,
        task={"tool": "classify_candidate", "candidate_text": candidate_text},
        entity_ids=likely_entity_ids,
        hops=1,
    )
    user_content = json.dumps(
        {
            "candidate_text": candidate_text,
            "evidence_id": evidence_id,
            "retrieved_context": context_packet.model_dump(mode="json"),
        },
        ensure_ascii=False,
    )
    return llm.generate_json(
        system_prompt=_load_prompt(),
        user_content=user_content,
        schema=ClassifiedCandidate,
        label="classify_candidate",
    )
