from __future__ import annotations

import re

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    """Normalize free text into a stable, lowercase, underscore-separated token."""
    slug = _SLUG_RE.sub("_", value.strip().lower()).strip("_")
    if not slug:
        raise ValueError(f"cannot slugify empty/invalid value: {value!r}")
    return slug


def make_id(*parts: str) -> str:
    """Build a stable, type-prefixed, colon-separated ID from ordered parts.

    Each part is slugified independently so raw titles never become foreign keys
    (Part 1 §3.1). Example: make_id("entity", "system", "WCS") -> "entity:system:wcs"
    """
    if len(parts) < 2:
        raise ValueError("make_id requires at least a type prefix and one segment")
    return ":".join(slugify(part) for part in parts)


def evidence_id(source_id: str, locator_token: str) -> str:
    return make_id("evidence", source_id, locator_token)


def entity_id(entity_type: str, name: str) -> str:
    return make_id("entity", entity_type, name)


def capability_id(name: str) -> str:
    return make_id("capability", name)


def claim_id(subject_token: str, predicate_token: str) -> str:
    return make_id("claim", subject_token, predicate_token)


def relationship_id(from_token: str, relationship_type: str, to_token: str) -> str:
    return make_id("relationship", from_token, relationship_type, to_token)


def procedure_id(capability_token: str, distinguishing_token: str) -> str:
    """A Procedure's id is anchored to the Capability it carries out, plus a
    token distinguishing it from other Procedures for the same Capability
    (e.g. a source id) — AGENT_DESIGN_NOTES.md §5 notes multiple Procedures
    may exist per Capability, drawn from different operational sources or
    incidents, so the id must not collapse them onto one another."""
    return make_id("procedure", capability_token, distinguishing_token)


def playbook_id(distinguishing_token: str) -> str:
    return make_id("playbook", distinguishing_token)


ID_TYPE_PREFIXES: dict[str, str] = {
    "evidence_unit": "evidence",
    "entity": "entity",
    "claim": "claim",
    "relationship": "relationship",
    "capability": "capability",
    "procedure": "procedure",
    "playbook": "playbook",
}


def is_well_formed_id(value: str, expected_prefix: str | None = None) -> bool:
    """Check that a string looks like a stable typed ID (`prefix:segment:...`)."""
    if not isinstance(value, str) or not value:
        return False
    parts = value.split(":")
    if len(parts) < 2:
        return False
    if any(not part for part in parts):
        return False
    if expected_prefix is not None and parts[0] != expected_prefix:
        return False
    return True
