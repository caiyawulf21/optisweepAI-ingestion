from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Literal

ScopeKind = Literal["all", "case", "source"]


@dataclass(frozen=True)
class PublishScope:
    kind: ScopeKind
    value: str | None = None

    @property
    def label(self) -> str:
        if self.kind == "all":
            return "all"
        return f"{self.kind}:{self.value}"


def parse_publish_scope(raw: str | None, *, default_case_id: str | None = None) -> PublishScope:
    text = (raw or "all").strip().lower()
    if text in {"", "all", "*"}:
        return PublishScope(kind="all")

    if text in {"case", "case:auto", "case:uploaded"}:
        if not default_case_id:
            raise ValueError(
                "publish-scope case/auto requires a case id from the uploaded file "
                "(e.g. Case 228086 Data.pdf) or an explicit case:<id>."
            )
        return PublishScope(kind="case", value=str(default_case_id))

    if text.startswith("case:"):
        case_id = text.split(":", 1)[1].strip()
        if not case_id:
            raise ValueError("publish-scope case:<id> requires a non-empty case id.")
        return PublishScope(kind="case", value=case_id.removeprefix("case_"))

    if text.startswith("source:"):
        source_id = text.split(":", 1)[1].strip()
        if not source_id:
            raise ValueError("publish-scope source:<id> requires a non-empty source id.")
        return PublishScope(kind="source", value=source_id)

    if re.fullmatch(r"\d{5,}", text):
        return PublishScope(kind="case", value=text)

    raise ValueError(
        f"Invalid publish-scope '{raw}'. Use all, case:<id>, case:auto, or source:<source_id>."
    )


def filter_upload_datasets(
    datasets: dict[str, list[dict[str, Any]]],
    scope: PublishScope,
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, int]]:
    if scope.kind == "all":
        counts = {name: len(rows) for name, rows in datasets.items()}
        return datasets, counts

    needle = _scope_needles(scope)
    kept_ids: set[str] = set()

    playbooks_a = _filter_docs(datasets.get("playbooks_prompt_a") or [], needle, kept_ids)
    playbooks_b = _filter_docs(datasets.get("playbooks_prompt_b") or [], needle, kept_ids)
    runbooks = _filter_docs(datasets.get("runbooks") or [], needle, kept_ids)
    ops_context = _filter_docs(datasets.get("operational_context") or [], needle, kept_ids)
    artifacts = _filter_docs(datasets.get("source_artifacts") or [], needle, kept_ids)
    images = _filter_docs(datasets.get("canonical_images") or [], needle, kept_ids)

    # Expand runbooks linked from kept playbooks via relationship shards.
    linked_procedure_ids = _collect_linked_procedure_ids(
        datasets.get("relationship_links") or [],
        kept_ids=kept_ids,
        needle=needle,
    )
    if linked_procedure_ids:
        for doc in datasets.get("runbooks") or []:
            record_id = str(doc.get("record_id") or "")
            procedure_id = str((doc.get("payload") or {}).get("procedure_id") or "")
            if record_id in linked_procedure_ids or procedure_id in linked_procedure_ids:
                if doc not in runbooks:
                    runbooks.append(doc)
                    _remember_ids(doc, kept_ids)

    relationship_shards = _filter_relationship_shards(
        datasets.get("relationship_links") or [],
        kept_ids=kept_ids,
        needle=needle,
    )

    filtered = {
        "runbooks": runbooks,
        "playbooks_prompt_a": playbooks_a,
        "playbooks_prompt_b": playbooks_b,
        "operational_context": ops_context,
        "source_artifacts": artifacts,
        "canonical_images": images,
        "relationship_links": relationship_shards,
        # Version-scoped config always rides with any upload so the app can load phrases.
        "gate_phrase_tables": list(datasets.get("gate_phrase_tables") or []),
    }
    counts = {name: len(rows) for name, rows in filtered.items()}
    return filtered, counts


def _scope_needles(scope: PublishScope) -> set[str]:
    value = str(scope.value or "").strip()
    if scope.kind == "case":
        case_id = value.removeprefix("case_")
        return {
            case_id,
            f"case_{case_id}",
            f"source_case_{case_id}",
            f"incident_{case_id}",
        }
    return {value, f"source_{value}"}


def _filter_docs(
    docs: list[dict[str, Any]],
    needle: set[str],
    kept_ids: set[str],
) -> list[dict[str, Any]]:
    kept: list[dict[str, Any]] = []
    for doc in docs:
        if _doc_matches(doc, needle):
            kept.append(doc)
            _remember_ids(doc, kept_ids)
    return kept


def _doc_matches(doc: dict[str, Any], needle: set[str]) -> bool:
    haystacks: list[str] = []
    for key in ("id", "record_id", "source_record_id", "case_id", "image_id"):
        value = doc.get(key)
        if value is not None:
            haystacks.append(str(value))

    payload = doc.get("payload")
    if isinstance(payload, dict):
        for key in ("case_id", "playbook_id", "procedure_id", "source_id", "incident_id"):
            if payload.get(key) is not None:
                haystacks.append(str(payload.get(key)))
        metadata = payload.get("metadata")
        if isinstance(metadata, dict):
            for key in ("source_id", "source_type"):
                if metadata.get(key) is not None:
                    haystacks.append(str(metadata.get(key)))
            incident_context = metadata.get("incident_context")
            if isinstance(incident_context, dict) and incident_context.get("case_id") is not None:
                haystacks.append(str(incident_context.get("case_id")))
        lineage = payload.get("source_lineage")
        if isinstance(lineage, list):
            for row in lineage:
                if isinstance(row, dict):
                    for key in ("source_id", "source_case_id", "incident_id", "candidate_id"):
                        if row.get(key) is not None:
                            haystacks.append(str(row.get(key)))

    metadata = doc.get("filter_metadata")
    if isinstance(metadata, dict):
        for key in ("source_id", "case_id", "artifact_id", "source_type"):
            if metadata.get(key) is not None:
                haystacks.append(str(metadata.get(key)))

    for key in ("linked_incident_ids", "source_artifact_ids", "linked_procedure_ids"):
        values = doc.get(key)
        if isinstance(values, list):
            haystacks.extend(str(v) for v in values)

    source_refs = doc.get("source_refs")
    if isinstance(source_refs, list):
        for ref in source_refs:
            if isinstance(ref, dict):
                for key in ("source_id", "source_document_id", "case_id", "source_type"):
                    if ref.get(key) is not None:
                        haystacks.append(str(ref.get(key)))

    lowered = " | ".join(haystacks).lower()
    return any(token.lower() in lowered for token in needle)


def _remember_ids(doc: dict[str, Any], kept_ids: set[str]) -> None:
    for key in ("id", "record_id", "source_record_id", "image_id"):
        value = doc.get(key)
        if value:
            kept_ids.add(str(value))
    payload = doc.get("payload")
    if isinstance(payload, dict):
        for key in ("playbook_id", "procedure_id", "playbook_candidate_id"):
            value = payload.get(key)
            if value:
                kept_ids.add(str(value))


def _collect_linked_procedure_ids(
    shards: list[dict[str, Any]],
    *,
    kept_ids: set[str],
    needle: set[str],
) -> set[str]:
    linked: set[str] = set()
    for shard in shards:
        for link in shard.get("links") or []:
            if not isinstance(link, dict):
                continue
            if str(link.get("link_type") or "") != "playbook_runbook":
                continue
            source_id = str(link.get("source_record_id") or "")
            target_id = str(link.get("target_record_id") or "")
            blob = f"{source_id} {target_id} {json_dumps_safe(link)}".lower()
            if any(token.lower() in blob for token in needle) or any(
                kept in source_id for kept in kept_ids if kept
            ):
                if target_id:
                    linked.add(target_id)
    return linked


def _filter_relationship_shards(
    shards: list[dict[str, Any]],
    *,
    kept_ids: set[str],
    needle: set[str],
) -> list[dict[str, Any]]:
    kept_links: list[dict[str, Any]] = []
    template: dict[str, Any] | None = None
    for shard in shards:
        if template is None:
            template = {
                key: value
                for key, value in shard.items()
                if key not in {"links", "link_count", "shard_index", "id"}
            }
        for link in shard.get("links") or []:
            if not isinstance(link, dict):
                continue
            source_id = str(link.get("source_record_id") or "")
            target_id = str(link.get("target_record_id") or "")
            blob = f"{source_id} {target_id} {json_dumps_safe(link)}".lower()
            if (
                source_id in kept_ids
                or target_id in kept_ids
                or any(token.lower() in blob for token in needle)
                or any(kept and kept in source_id for kept in kept_ids)
                or any(kept and kept in target_id for kept in kept_ids)
            ):
                kept_links.append(link)

    if not kept_links:
        return []

    base = template or {
        "doc_type": "relationship_link_shard",
        "publish_version_id": "",
        "generated_at": "",
    }
    return [
        {
            **base,
            "id": f"relationship_links_scoped_{index:03d}",
            "shard_index": index,
            "shard_count": 1,
            "link_count": len(kept_links),
            "links": kept_links,
        }
        # Keep one shard for scoped uploads; Stage 11 shard size is for full corpus.
        for index, _ in enumerate([kept_links])
    ]


def json_dumps_safe(value: Any) -> str:
    try:
        import json

        return json.dumps(value, ensure_ascii=False)
    except Exception:
        return str(value)
