"""Load frozen runbook/playbook capability taxonomy from docs/ontology."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TAXONOMY_PATH = REPO_ROOT / "docs" / "ontology" / "taxonomy" / "runbook_capability_taxonomy.json"


@lru_cache(maxsize=4)
def load_capability_taxonomy(path: str | None = None) -> dict[str, Any]:
    taxonomy_path = Path(path) if path else DEFAULT_TAXONOMY_PATH
    if not taxonomy_path.exists():
        raise FileNotFoundError(f"Capability taxonomy not found: {taxonomy_path}")
    return json.loads(taxonomy_path.read_text(encoding="utf-8"))


def taxonomy_id_sets(path: str | None = None) -> dict[str, set[str]]:
    data = load_capability_taxonomy(path)
    return {
        "capabilities": {str(item.get("id") or "").strip() for item in data.get("capabilities") or [] if item.get("id")},
        "access_surfaces": _surface_ids_with_aliases(data),
        "audience_roles": {str(item.get("id") or "").strip() for item in data.get("audience_roles") or [] if item.get("id")},
        "failure_patterns": {
            str(item.get("id") or "").strip() for item in data.get("failure_patterns") or [] if item.get("id")
        },
        "procedure_intents": {
            str(item.get("id") or "").strip() for item in data.get("procedure_intents") or [] if item.get("id")
        },
    }


def _surface_ids_with_aliases(data: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for item in data.get("access_surfaces") or []:
        surface_id = str(item.get("id") or "").strip()
        if surface_id:
            ids.add(surface_id)
        for alias in item.get("aliases") or []:
            alias_id = str(alias or "").strip()
            if alias_id:
                ids.add(alias_id)
    return ids


def canonicalize_surface_id(value: str, path: str | None = None) -> str:
    raw = str(value or "").strip()
    if not raw:
        return ""
    data = load_capability_taxonomy(path)
    for item in data.get("access_surfaces") or []:
        surface_id = str(item.get("id") or "").strip()
        aliases = {str(alias).strip() for alias in item.get("aliases") or []}
        if raw == surface_id or raw in aliases:
            return surface_id
    return raw
