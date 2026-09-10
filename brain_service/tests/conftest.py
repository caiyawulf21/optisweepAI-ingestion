from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from pydantic import BaseModel

from brain.id_generation import make_id
from brain.schemas.capability import Capability, CapabilityKind
from brain.schemas.common import Constraints
from brain.schemas.entity import Entity, EntityType
from brain.schemas.procedure import Procedure, ProcedureStep
from brain.schemas.relationship import Relationship, RelationshipType
from providers.llm import LLMProvider
from providers.local_storage import LocalStorageProvider


@pytest.fixture()
def storage(tmp_path: Path) -> LocalStorageProvider:
    return LocalStorageProvider(root=tmp_path)


def make_entity(
    entity_id: str,
    *,
    name: str | None = None,
    description: str = "test entity",
    entity_type: EntityType | None = None,
) -> Entity:
    if entity_type is None:
        # Infer from the id's own type segment (entity:<type>:<slug>) so a
        # test can write "entity:component:widget" and get a component, not
        # a hardcoded SYSTEM regardless of what the id says -- a fixture
        # that silently ignores its own id's type is exactly the kind of
        # bug that makes a cross-type test pass for the wrong reason.
        segments = entity_id.split(":")
        entity_type = EntityType(segments[1]) if len(segments) > 1 else EntityType.SYSTEM
    return Entity(
        id=entity_id,
        entity_type=entity_type,
        name=name or entity_id.rsplit(":", 1)[-1],
        description=description,
        source_refs=["evidence:test:seed"],
    )


def make_capability(
    capability_id: str,
    *,
    name: str | None = None,
    capability_kind: CapabilityKind = CapabilityKind.DIAGNOSTIC,
    target_entity_ids: list[str] | None = None,
    allowed_surface_entity_ids: list[str] | None = None,
    required_role_ids: list[str] | None = None,
) -> Capability:
    return Capability(
        id=capability_id,
        name=name or capability_id.rsplit(":", 1)[-1],
        capability_kind=capability_kind,
        target_entity_ids=target_entity_ids or [],
        allowed_surface_entity_ids=allowed_surface_entity_ids or [],
        required_role_ids=required_role_ids or [],
        source_refs=["evidence:test:seed"],
    )


def make_relationship(
    from_id: str,
    relationship_type: RelationshipType,
    to_id: str,
    *,
    note: str = "",
) -> Relationship:
    return Relationship(
        id=make_id("relationship", from_id, relationship_type.value, to_id),
        from_id=from_id,
        relationship_type=relationship_type,
        to_id=to_id,
        note=note,
        source_refs=["evidence:test:seed"],
    )


def make_procedure(
    procedure_id: str,
    *,
    capability_id: str,
    procedure_type: CapabilityKind = CapabilityKind.DIAGNOSTIC,
    title: str | None = None,
    summary: str = "",
) -> Procedure:
    return Procedure(
        id=procedure_id,
        capability_id=capability_id,
        procedure_type=procedure_type,
        title=title or procedure_id.rsplit(":", 1)[-1],
        summary=summary,
        steps=[
            ProcedureStep(
                step_number=1,
                title="Test step",
                instruction="Do the test thing.",
                source_refs=["evidence:test:seed"],
            )
        ],
        source_refs=["evidence:test:seed"],
    )


class ScriptedLLM(LLMProvider):
    """Returns pre-scripted responses keyed by schema class, in call order
    per schema. Raises AssertionError if a schema has no scripted response
    left -- makes an unexpected extra call fail loudly instead of silently
    reusing a stale response."""

    def __init__(self, responses: dict[type[BaseModel], list[BaseModel]]) -> None:
        self._responses = {schema: list(values) for schema, values in responses.items()}

    def generate_json(self, *, system_prompt: str, user_content: str, schema, label: str, max_attempts: int = 2):
        queue = self._responses.get(schema)
        if not queue:
            raise AssertionError(f"ScriptedLLM has no more responses for schema {schema.__name__} (label={label})")
        return queue.pop(0)

    def generate_text(self, *, system_prompt: str, user_content: str, label: str) -> str:
        raise NotImplementedError
