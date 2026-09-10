from __future__ import annotations

from dataclasses import dataclass, field

from brain.id_generation import entity_id, slugify
from brain.migration.merge import merge_record
from brain.schemas.entity import Entity, EntityType


@dataclass
class EntityRegistry:
    """Tracks entities created during a migration run so later steps resolve
    names to an existing entity instead of creating a duplicate.

    Part 1 §9: "Resolve referenced names to existing entities where possible.
    Create a new entity only when the referenced thing does not already exist."
    This is the migration-time implementation of that rule: a single registry
    shared across every source in a run, keyed by (entity_type, alias).
    """

    entities: dict[str, Entity] = field(default_factory=dict)
    _alias_index: dict[tuple[EntityType, str], str] = field(default_factory=dict)

    def _index_aliases(self, entity: Entity) -> None:
        for alias in [entity.name, *entity.aliases]:
            key = (entity.entity_type, slugify(alias))
            self._alias_index.setdefault(key, entity.id)

    def resolve(self, entity_type: EntityType, name: str) -> Entity | None:
        key = (entity_type, slugify(name))
        found_id = self._alias_index.get(key)
        return self.entities.get(found_id) if found_id else None

    def get_or_create(
        self,
        entity_type: EntityType,
        name: str,
        *,
        description: str = "",
        aliases: list[str] | None = None,
        payload: dict | None = None,
        source_refs: list[str] | None = None,
    ) -> Entity:
        """Return the existing entity for (entity_type, name/alias) or create one.

        When an entity already exists, every field a later source can
        strengthen — description, aliases, payload sub-fields, source_refs —
        is merged in via merge_record, not just source_refs. A later, richer
        source describing an already-known entity should make that entity
        more complete, per Part 1 §9 ("a later source strengthening an
        earlier one is the normal case") and the requirement that entities
        grow richer as more sources are ingested, not just accumulate
        citations.
        """
        existing = self.resolve(entity_type, name)
        if existing is not None:
            merged = merge_record(
                existing,
                {
                    "description": description,
                    "aliases": aliases or [],
                    "payload": payload,
                    "source_refs": source_refs or [],
                },
            )
            if merged is not existing:
                self.entities[merged.id] = merged
                self._index_aliases(merged)
            return merged

        new_id = entity_id(entity_type.value, name)
        entity = Entity(
            id=new_id,
            entity_type=entity_type,
            name=name,
            description=description,
            aliases=aliases or [],
            payload=payload or {},
            source_refs=source_refs or [],
        )
        self.entities[entity.id] = entity
        self._index_aliases(entity)
        return entity

    def all(self) -> list[Entity]:
        return list(self.entities.values())
