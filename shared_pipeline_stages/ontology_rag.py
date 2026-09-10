"""Retrieve 1–3 ontology catalog snippets for Stage 5/6 mini-RAG enrichment."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOGS_DIR = REPO_ROOT / "docs" / "ontology" / "catalogs"
DEFAULT_MAX_SNIPPETS = 3
DEFAULT_CHAR_BUDGET = 1200
STAGE5_MAX_SNIPPETS = 2
STAGE5_CHAR_BUDGET = 800
STAGE5_PLAYBOOK_MAX_SNIPPETS = 5
STAGE5_PLAYBOOK_CHAR_BUDGET = 2200
STAGE6_MAX_SNIPPETS = 3
STAGE6_CHAR_BUDGET = 1200
PASCAL_MODEL_RE = re.compile(r"\b([A-Z][a-zA-Z0-9]*(?:Model|Database|Activity|Table))\b")
ACTION_VERB_RE = re.compile(
    r"\b(open|check|verify|inspect|navigate|restart|query|select|confirm|review|locate)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class OntologyQueryKeys:
    capability: str | None = None
    access_surface: str | None = None
    model_name: str | None = None
    database_id: str | None = None
    failure_pattern: str | None = None
    activity_id: str | None = None
    free_text: str | None = None

    def as_retrieval_kwargs(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value}


@lru_cache(maxsize=1)
def _load_index() -> dict[str, Any]:
    path = CATALOGS_DIR / "catalog_index.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=8)
def _load_catalog(name: str) -> dict[str, Any]:
    path = CATALOGS_DIR / name
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def infer_ontology_query(
    text: str,
    *,
    artifacts: list[dict[str, Any]] | None = None,
    explicit_surfaces: list[str] | None = None,
    explicit_capabilities: list[str] | None = None,
    free_text_limit: int = 1600,
) -> OntologyQueryKeys:
    """Derive retrieval keys from section/candidate text and compact artifacts."""
    from shared_pipeline_stages.runbook_tags import _infer_capabilities, _infer_failures, _infer_surfaces

    blob_parts = [str(text or "")]
    for artifact in artifacts or []:
        if not isinstance(artifact, dict):
            continue
        blob_parts.extend(
            [
                str(artifact.get("title") or ""),
                str(artifact.get("short_description") or ""),
                str(artifact.get("ocr_text") or "")[:800],
                str(artifact.get("nearby_text") or "")[:800],
                str(artifact.get("retrieval_text") or "")[:600],
            ]
        )
    blob = " ".join(blob_parts)
    surfaces = list(explicit_surfaces or []) or _infer_surfaces(blob)
    capabilities = list(explicit_capabilities or []) or _infer_capabilities(blob)
    failures = _infer_failures(blob)
    models = PASCAL_MODEL_RE.findall(blob)
    model_name = None
    if models:
        preferred = [
            name
            for name in models
            if re.search(r"command|error|robot|exchange|heartbeat|location|task", name, re.I)
        ]
        model_name = (preferred or models)[0]

    free = re.sub(r"\s+", " ", blob).strip()
    if len(free) > free_text_limit:
        free = free[:free_text_limit].rstrip() + "..."

    return OntologyQueryKeys(
        capability=(capabilities[0] if capabilities else None),
        access_surface=(surfaces[0] if surfaces else None),
        model_name=model_name,
        failure_pattern=(failures[0] if failures else None),
        free_text=free or None,
    )


def section_already_surface_grounded(text: str) -> bool:
    """True when text already names a live surface and an action verb."""
    from shared_pipeline_stages.runbook_tags import _infer_surfaces

    return bool(_infer_surfaces(text)) and bool(ACTION_VERB_RE.search(text or ""))


def retrieve_ontology_snippets(
    *,
    capability: str | None = None,
    access_surface: str | None = None,
    model_name: str | None = None,
    database_id: str | None = None,
    failure_pattern: str | None = None,
    activity_id: str | None = None,
    free_text: str | None = None,
    max_snippets: int = DEFAULT_MAX_SNIPPETS,
    char_budget: int = DEFAULT_CHAR_BUDGET,
) -> list[dict[str, Any]]:
    """Return ranked snippets `{id, title, text, score, source_refs}`."""
    query_tokens = _tokens(
        " ".join(
            x
            for x in [
                capability or "",
                access_surface or "",
                model_name or "",
                database_id or "",
                failure_pattern or "",
                activity_id or "",
                free_text or "",
            ]
            if x
        )
    )
    candidates: list[dict[str, Any]] = []

    caps_cat = _load_catalog("capability_catalog.json")
    for card in caps_cat.get("capabilities") or []:
        cid = str(card.get("id") or "")
        surfaces = [
            str(s)
            for s in (card.get("primary_access_surfaces") or []) + (card.get("secondary_access_surfaces") or [])
        ]
        models = [str(m) for m in card.get("primary_models") or []]
        for link in card.get("sql_model_links") or []:
            if isinstance(link, dict) and link.get("model"):
                mid = str(link.get("model"))
                if mid not in models:
                    models.append(mid)
        dbs = [str(d) for d in (card.get("primary_databases") or []) + (card.get("secondary_databases") or [])]
        fps = [str(f) for f in card.get("failure_patterns") or []]
        score = _score(
            query_tokens,
            [
                cid,
                card.get("label"),
                card.get("job"),
                card.get("when_to_use"),
                *surfaces,
                *models,
                *dbs,
                *fps,
                *(card.get("api_checks") or []),
            ],
        )
        if capability and capability == cid:
            score += 12
        if access_surface and access_surface in surfaces:
            score += 4
        if model_name and model_name in models:
            score += 4
        if database_id and database_id in dbs:
            score += 3
        if failure_pattern and failure_pattern in fps:
            score += 3
        if score <= 0:
            continue
        act_bits = []
        for act in card.get("activities") or []:
            act_bits.append(
                f"{act.get('access_surface')} ({act.get('role') or '?'}): {act.get('action') or act.get('id')}"
            )
        obs = card.get("observables") or {}
        field_bits = []
        for fh in card.get("field_highlights") or []:
            meaning = fh.get("meaning") or ("needs_sme" if fh.get("needs_sme") else "")
            field_bits.append(f"{fh.get('model')}.{fh.get('field')}: {meaning}")
        roles = card.get("role_paths") or {}
        role_bits = [f"{role}: {path}" for role, path in roles.items()]
        text = _clip(
            f"Capability {cid}: {card.get('job') or card.get('description') or ''}. "
            f"When: {card.get('when_to_use') or ''} Not for: {card.get('not_for') or ''}. "
            f"Surfaces: {', '.join(surfaces)}. "
            f"Support contract: {json.dumps(card.get('support_contract') or {}, ensure_ascii=False)}. "
            f"Backend mappings: {json.dumps(card.get('backend_mappings') or [], ensure_ascii=False)}. "
            f"DBs: {', '.join(dbs)}. Models: {', '.join(models)}. "
            f"APIs: {', '.join(str(a) for a in card.get('api_checks') or [])}. "
            f"Key fields: {'; '.join(field_bits)}. "
            f"Activities: {'; '.join(act_bits)}. "
            f"Healthy: {', '.join(obs.get('healthy') or [])}. "
            f"Degraded: {', '.join(obs.get('degraded') or [])}. "
            f"Escalate: {', '.join(obs.get('escalate') or [])}. "
            f"Roles: {'; '.join(role_bits)}. "
            f"Failures: {', '.join(fps)}.",
            char_budget,
        )
        candidates.append(
            {
                "id": f"capability:{cid}",
                "title": f"Capability — {card.get('label') or cid}",
                "text": text,
                "score": score,
                "source_refs": card.get("source_refs") or [],
            }
        )

    sql = _load_catalog("wcs_sql_catalog.json")
    if sql:
        for db in sql.get("databases") or []:
            score = _score(
                query_tokens,
                [
                    db.get("id"),
                    db.get("label"),
                    db.get("purpose"),
                    access_surface if access_surface == "wcs_sql" else "",
                    database_id,
                ],
            )
            if database_id and str(db.get("id") or "") == database_id:
                score += 5
            if score <= 0 and not (database_id and str(db.get("id") or "") == database_id):
                continue
            text = _clip(
                f"DB {db.get('label')}: {db.get('purpose') or ''} "
                f"When: {db.get('when_to_use') or ''} Not for: {db.get('not_for') or ''}",
                char_budget,
            )
            candidates.append(
                {
                    "id": f"db:{db.get('id')}",
                    "title": f"WCS SQL database — {db.get('label')}",
                    "text": text,
                    "score": score or 1,
                    "source_refs": db.get("evidence") or [],
                }
            )
        for model in sql.get("models") or []:
            name = str(model.get("name") or "")
            caps = [str(c) for c in model.get("capability_hints") or []]
            score = _score(query_tokens, [name, model.get("purpose"), model.get("database"), *caps])
            if model_name and name.lower() == model_name.lower():
                score += 8
            if capability and capability in caps:
                score += 4
            if access_surface == "wcs_sql":
                score += 1
            if score <= 0:
                continue
            field_bits = []
            for field in model.get("fields") or []:
                fname = field.get("name")
                meaning = field.get("meaning")
                if not fname:
                    continue
                if meaning:
                    field_bits.append(f"{fname}: {meaning}")
                else:
                    field_bits.append(f"{fname}: (needs_sme)")
            text = _clip(
                f"Model {name} ({model.get('database')}): {model.get('purpose') or ''}. "
                f"Fields: {'; '.join(field_bits)}"
                + (
                    f" Select template ({(model.get('select_template') or {}).get('provenance') or 'n/a'}): "
                    f"{(model.get('select_template') or {}).get('statement') or ''}"
                    if isinstance(model.get("select_template"), dict)
                    and (model.get("select_template") or {}).get("statement")
                    else ""
                ),
                char_budget,
            )
            candidates.append(
                {
                    "id": f"model:{name}",
                    "title": f"WCS model — {name}",
                    "text": text,
                    "score": score,
                    "source_refs": model.get("source_refs") or [],
                }
            )

    edges = _load_catalog("cross_links.json")
    for edge in edges.get("capability_failure_edges") or []:
        cap = str(edge.get("capability") or "")
        fps = [str(x) for x in edge.get("failure_patterns") or []]
        score = 0
        if capability and capability == cap:
            score += 5
        if failure_pattern and failure_pattern in fps:
            score += 5
        score += _score(query_tokens, [cap, *fps])
        if score <= 0:
            continue
        candidates.append(
            {
                "id": f"capfail:{cap}",
                "title": f"Capability↔failure — {cap}",
                "text": _clip(f"{cap} related failure_patterns: {', '.join(fps)}", char_budget),
                "score": score,
                "source_refs": [{"source": edge.get("source")}],
            }
        )

    for act in edges.get("surface_activities") or []:
        surface = str(act.get("access_surface") or "")
        aid = str(act.get("activity_id") or "")
        caps = [str(c) for c in act.get("capability_hints") or []]
        score = _score(query_tokens, [surface, aid, act.get("label"), *caps, *(act.get("observables") or [])])
        if access_surface and access_surface == surface:
            score += 3
        if activity_id and activity_id == aid:
            score += 6
        if capability and capability in caps:
            score += 3
        if score <= 0:
            continue
        candidates.append(
            {
                "id": f"activity:{surface}:{aid}",
                "title": f"{surface} — {act.get('label')}",
                "text": _clip(
                    f"Activity {aid} on {surface}. Observables: {', '.join(act.get('observables') or [])}. "
                    f"Capabilities: {', '.join(caps)}.",
                    char_budget,
                ),
                "score": score,
                "source_refs": [],
            }
        )

    for fname in (
        "rms_ui_catalog.json",
        "ignition_gateway_catalog.json",
        "stunnel_catalog.json",
        "event_viewer_catalog.json",
        "apidog_catalog.json",
        "aveva_hmi_catalog.json",
        "tipper_hmi_catalog.json",
        "hospital_hmi_catalog.json",
        "building_acb_hmi_catalog.json",
        "site_interview_catalog.json",
        "physical_floor_catalog.json",
        "wcs_api_catalog.json",
        "wcs_sql_catalog.json",
    ):
        cat = _load_catalog(fname)
        if not cat:
            continue
        sid = str(cat.get("access_surface") or "")
        score = _score(
            query_tokens,
            [
                sid,
                cat.get("title"),
                cat.get("purpose"),
                *(cat.get("aliases") or []),
                " ".join(cat.get("when_to_use") or [])
                if isinstance(cat.get("when_to_use"), list)
                else cat.get("when_to_use"),
                "webvisu" if sid == "tipper_hmi" else "",
                "visu" if sid == "tipper_hmi" else "",
            ],
        )
        if access_surface and access_surface == sid:
            score += 4
        if free_text and sid == "tipper_hmi" and re.search(r"web\s*visu|\bvisu\b|tipper", free_text or "", re.I):
            score += 5
        if capability and capability in (cat.get("related_capabilities") or []):
            score += 3
        if score <= 0:
            continue
        screen_bits = []
        for screen in cat.get("screens_or_views") or cat.get("screens") or []:
            screen_bits.append(
                f"{screen.get('id')}: {screen.get('purpose') or '; '.join(screen.get('key_points') or [])}"
            )
        act_bits = []
        for act in cat.get("activities") or []:
            act_bits.append(f"{act.get('id')}: {act.get('label')}")
        obj_bits = []
        for obj in (cat.get("objects") or [])[:12]:
            obj_bits.append(f"{obj.get('id') or obj.get('label')}")
        when = cat.get("when_to_use") or []
        when_txt = "; ".join(when) if isinstance(when, list) else str(when)
        not_for = cat.get("not_for") or []
        not_txt = "; ".join(not_for) if isinstance(not_for, list) else str(not_for)
        text = _clip(
            f"{cat.get('purpose') or ''} Aliases: {', '.join(cat.get('aliases') or [])}. "
            f"When: {when_txt}. Not for: {not_txt}. "
            f"Views: {'; '.join(screen_bits)}. "
            f"Objects: {', '.join(obj_bits)}. "
            f"Activities: {'; '.join(act_bits)}. "
            f"Architecture: {'; '.join(cat.get('architecture_notes') or [])}.",
            char_budget,
        )
        candidates.append(
            {
                "id": f"surface:{sid}",
                "title": str(cat.get("title") or sid),
                "text": text,
                "score": score,
                "source_refs": cat.get("source_refs") or [],
            }
        )

    candidates.sort(key=lambda row: (-float(row.get("score") or 0), str(row.get("id") or "")))
    return candidates[: max(1, max_snippets)]


def ontology_snippets_for_stage5(
    text: str,
    *,
    artifacts: list[dict[str, Any]] | None = None,
    skip_if_grounded: bool = True,
) -> list[dict[str, Any]]:
    """1–2 surface/capability snippets for Stage 5 discovery."""
    if skip_if_grounded and section_already_surface_grounded(text):
        return []
    keys = infer_ontology_query(text, artifacts=artifacts, free_text_limit=1200)
    if not keys.as_retrieval_kwargs():
        return []
    raw = retrieve_ontology_snippets(
        **keys.as_retrieval_kwargs(),
        max_snippets=6,
        char_budget=STAGE5_CHAR_BUDGET,
    )
    preferred = [row for row in raw if str(row.get("id") or "").startswith(("surface:", "capability:"))]
    chosen = (preferred or raw)[:STAGE5_MAX_SNIPPETS]
    return [_annotate_snippet(row, keys) for row in chosen]


def ontology_contracts_for_capabilities(
    capability_ids: list[str] | set[str] | None,
) -> list[dict[str, Any]]:
    requested = {
        str(value).split(":", 1)[1] if str(value).startswith("capability:") else str(value)
        for value in capability_ids or []
        if str(value).strip()
    }
    if not requested:
        return []
    catalog = _load_catalog("capability_catalog.json")
    contracts: list[dict[str, Any]] = []
    for card in catalog.get("capabilities") or []:
        capability_id = str(card.get("id") or "")
        if capability_id not in requested:
            continue
        contract = card.get("support_contract")
        if not isinstance(contract, dict):
            contract = {}
        backend_mappings = list(card.get("backend_mappings") or [])
        if not backend_mappings and card.get("primary_models"):
            field_by_model: dict[str, list[str]] = {}
            for field in card.get("field_highlights") or []:
                if not isinstance(field, dict):
                    continue
                model = str(field.get("model") or "")
                name = str(field.get("field") or "")
                if model and name:
                    field_by_model.setdefault(model, []).append(name)
            backend_mappings = [
                {
                    "operational_concept": capability_id,
                    "preferred_support_surface": "wcs_sql",
                    "support_read_sources": [
                        {
                            "surface": "wcs_sql",
                            "database": next(iter(card.get("primary_databases") or []), ""),
                            "model": model,
                            "fields": field_by_model.get(model, [])[:8],
                        }
                    ],
                }
                for model in list(card.get("primary_models") or [])[:3]
            ]
        contracts.append(
            {
                "id": f"capability:{capability_id}",
                "support_contract": contract,
                "backend_mappings": backend_mappings,
            }
        )
    return contracts


def ontology_snippets_for_stage5_playbook(
    text: str,
    *,
    artifacts: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Richer capability/model/surface snippets for Stage 5 playbook node authoring.

    Prefer DB models + capability cards so diagnostic nodes can ground healthy/unhealthy
    evidence in SSMS system state / active errors as well as RMS UI — not RMS-only.
    """
    keys = infer_ontology_query(text, artifacts=artifacts, free_text_limit=1800)
    if not keys.as_retrieval_kwargs():
        return []
    raw = retrieve_ontology_snippets(
        **keys.as_retrieval_kwargs(),
        max_snippets=12,
        char_budget=STAGE5_PLAYBOOK_CHAR_BUDGET,
    )

    def _rank_bucket(snippet_id: str) -> int:
        if snippet_id.startswith("model:"):
            return 0
        if snippet_id.startswith("capability:"):
            return 1
        if snippet_id.startswith("db:"):
            return 2
        if snippet_id.startswith("surface:"):
            return 3
        if snippet_id.startswith("activity:"):
            return 4
        return 5

    ranked = sorted(
        raw,
        key=lambda row: (
            _rank_bucket(str(row.get("id") or "")),
            -float(row.get("score") or 0),
            str(row.get("id") or ""),
        ),
    )
    chosen = ranked[:STAGE5_PLAYBOOK_MAX_SNIPPETS]
    return [_annotate_snippet(row, keys) for row in chosen]


def ontology_snippets_for_stage6(
    candidate: dict[str, Any],
    *,
    artifacts: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """1–3 deep snippets (capability/model/activity/surface) for Stage 6 finalize."""
    text = " ".join(
        [
            str(candidate.get("title") or ""),
            str(candidate.get("summary") or ""),
            str(candidate.get("candidate_goal") or ""),
            " ".join(str(step) for step in candidate.get("rough_steps") or []),
            " ".join(str(item) for item in candidate.get("access_or_tools_needed") or []),
        ]
    )
    keys = infer_ontology_query(
        text,
        artifacts=artifacts,
        explicit_surfaces=[str(s) for s in (candidate.get("access_surface") or []) if str(s).strip()],
        explicit_capabilities=[str(c) for c in (candidate.get("capability_tags") or []) if str(c).strip()],
        free_text_limit=1600,
    )
    if not keys.as_retrieval_kwargs():
        return []
    raw = retrieve_ontology_snippets(
        **keys.as_retrieval_kwargs(),
        max_snippets=8,
        char_budget=STAGE6_CHAR_BUDGET,
    )

    def _rank_bucket(snippet_id: str) -> int:
        if snippet_id.startswith("model:"):
            return 0
        if snippet_id.startswith("capability:"):
            return 1
        if snippet_id.startswith("activity:"):
            return 2
        if snippet_id.startswith("surface:"):
            return 3
        if snippet_id.startswith("db:"):
            return 4
        return 5

    ranked = sorted(
        raw,
        key=lambda row: (
            _rank_bucket(str(row.get("id") or "")),
            -float(row.get("score") or 0),
            str(row.get("id") or ""),
        ),
    )
    chosen = ranked[:STAGE6_MAX_SNIPPETS]
    return [_annotate_snippet(row, keys) for row in chosen]


def ontology_prompt_snippets(**kwargs: Any) -> str:
    """Format retrieved snippets for optional Stage 6 prompt appendix."""
    snippets = retrieve_ontology_snippets(**kwargs)
    if not snippets:
        return ""
    lines = ["# System reference snippets (mini-RAG; not new tag IDs)", ""]
    for i, snip in enumerate(snippets, start=1):
        lines.append(f"{i}. **{snip.get('title')}**")
        lines.append(str(snip.get("text") or ""))
        lines.append("")
    return "\n".join(lines).rstrip()


def _annotate_snippet(row: dict[str, Any], keys: OntologyQueryKeys) -> dict[str, Any]:
    annotated = dict(row)
    annotated["retrieval_keys"] = keys.as_retrieval_kwargs()
    return annotated


def _tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9_]+", (text or "").lower()) if len(t) > 2}


def _score(query: set[str], parts: list[Any]) -> float:
    if not query:
        return 0.0
    blob = _tokens(" ".join(str(p or "") for p in parts))
    if not blob:
        return 0.0
    return float(len(query & blob))


def _clip(text: str, budget: int) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    if len(text) <= budget:
        return text
    return text[: max(0, budget - 3)].rstrip() + "..."
