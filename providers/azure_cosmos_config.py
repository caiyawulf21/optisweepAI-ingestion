"""Brain-specific Cosmos settings and container plan (Part 1 §10.2,
extended in brain/AGENT_DESIGN_NOTES.md §14.3).

Deliberately separate from shared_pipeline_stages/stage_11/container_config.py's
DATASET_* constants -- those are the pre-Brain publish target (runbooks,
playbooks_prompt_a/b, operational_context, ...), a different set of
containers in the same Cosmos account. Brain's own containers are named
here with a brain_ prefix precisely so the two are never confused or
accidentally pointed at each other.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

from brain.schemas.common import RecordType

# One container per Brain record type, partitioned per Part 1 §10.2's own
# stated rationale (partition by the field a record is always looked up
# through) -- restated here, not re-derived, since the architecture lock
# already made this call:
#   brain_evidence        /source_id            (source-scoped ingest/reprocess)
#   brain_entities        /entity_type          (ontology lookups by type)
#   brain_claims          /subject_entity_id    ("what do we know about this entity")
#   brain_relationships   /from_id              (direct graph traversal from a node)
#   brain_capabilities    /capability_kind
#   brain_procedures      /capability_id        ("approved steps for capability X")
#   brain_playbooks       /entry_symptom_entity_ids[0]  (symptom-driven routing)
#   brain_reviews         /status               ("give me everything still open")
CONTAINER_BY_RECORD_TYPE: dict[RecordType, str] = {
    RecordType.EVIDENCE_UNIT: "brain_evidence",
    RecordType.ENTITY: "brain_entities",
    RecordType.CLAIM: "brain_claims",
    RecordType.RELATIONSHIP: "brain_relationships",
    RecordType.CAPABILITY: "brain_capabilities",
    RecordType.PROCEDURE: "brain_procedures",
    RecordType.PLAYBOOK: "brain_playbooks",
    RecordType.REVIEW: "brain_reviews",
}

PARTITION_KEY_FIELD_BY_RECORD_TYPE: dict[RecordType, str] = {
    RecordType.EVIDENCE_UNIT: "source_id",
    RecordType.ENTITY: "entity_type",
    RecordType.CLAIM: "subject_entity_id",
    RecordType.RELATIONSHIP: "from_id",
    RecordType.CAPABILITY: "capability_kind",
    RecordType.PROCEDURE: "capability_id",
    RecordType.PLAYBOOK: "entry_symptom_entity_ids",  # first element, see partition_key_value()
    RecordType.REVIEW: "status",
}

# Every Brain container is declared in Cosmos with THIS same partition key
# path, rather than each record type's own natural field name -- Cosmos
# partition keys must be a real top-level scalar JSON property, and
# Playbook's natural key (entry_symptom_entity_ids) is a list, which Cosmos
# cannot partition on directly. A synthetic top-level `_partition_key`
# field (added by partition_key_value()'s caller at write time -- see
# AzureStorageProvider.save_brain_records) holding the already-computed
# scalar value keeps one partition key SHAPE for every container while
# still partitioning by the semantically-meaningful field
# PARTITION_KEY_FIELD_BY_RECORD_TYPE names.
COSMOS_PARTITION_KEY_PATH = "/_partition_key"

INGESTION_RUNS_CONTAINER = "brain_ingestion_runs"
INGESTION_RUNS_PARTITION_KEY_FIELD = "run_id"

# One shared container for all record types' embeddings, partitioned by
# record_type (mirrors brain_entities' own partitioning rationale: lookups
# and re-embedding backfills are naturally scoped by type). Vectors are
# read corpus-wide for search (brain_service/retrieval.py), so a single
# container -- not one per record type -- keeps a full-corpus scan to one
# cross-partition query instead of 7.
EMBEDDINGS_CONTAINER = "brain_embeddings"

CONTAINER_ENV_KEYS: dict[str, str] = {
    container: f"COSMOS_CONTAINER_{container.upper()}"
    for container in [*CONTAINER_BY_RECORD_TYPE.values(), INGESTION_RUNS_CONTAINER, EMBEDDINGS_CONTAINER]
}


def _clean_env(value: str | None) -> str:
    return (value or "").strip().strip('"').strip("'")


@dataclass(frozen=True)
class BrainCosmosSettings:
    endpoint: str
    key: str
    database: str
    containers: dict[str, str]  # container role name -> actual Cosmos container name

    def is_complete(self) -> bool:
        return bool(self.endpoint and self.key and self.database and all(self.containers.values()))


def load_brain_cosmos_settings() -> BrainCosmosSettings:
    """Reads COSMOS_ENDPOINT/COSMOS_KEY/COSMOS_DATABASE -- the SAME account
    settings shared_pipeline_stages/stage_11/container_config.py already
    uses, since this is one Cosmos account with multiple container sets,
    not a separate account -- plus one COSMOS_CONTAINER_BRAIN_<NAME>
    override per Brain container, defaulting to the container's own role
    name (e.g. "brain_entities") if unset."""
    load_dotenv()
    containers = {
        role_name: _clean_env(os.getenv(env_key)) or role_name
        for role_name, env_key in CONTAINER_ENV_KEYS.items()
    }
    return BrainCosmosSettings(
        endpoint=_clean_env(os.getenv("COSMOS_ENDPOINT") or os.getenv("AZURE_COSMOS_ENDPOINT")),
        key=_clean_env(os.getenv("COSMOS_KEY") or os.getenv("AZURE_COSMOS_KEY")),
        database=_clean_env(os.getenv("COSMOS_DATABASE") or os.getenv("AZURE_COSMOS_DATABASE_NAME")),
        containers=containers,
    )


def partition_key_value(record) -> str:
    """Compute the actual partition key VALUE for one record, given
    PARTITION_KEY_FIELD_BY_RECORD_TYPE's field name. Playbook is the one
    irregular case (partitions by the first entry of a list field, per
    Part 1 §10.2's own stated design), handled explicitly rather than
    silently returning the whole list where Cosmos expects a scalar.

    Every partition key field here is either a plain str or a str Enum
    (e.g. Entity.entity_type, Capability.capability_kind, BrainReview.status)
    -- str(some_enum) returns "EntityType.SYSTEM", not "system", so enum
    values are unwrapped via .value explicitly rather than relying on
    str() to do the right thing."""
    field_name = PARTITION_KEY_FIELD_BY_RECORD_TYPE.get(record.type)
    if field_name is None:
        raise ValueError(f"No partition key mapping for record type {record.type!r}")
    value = getattr(record, field_name)
    if isinstance(value, list):
        if not value:
            raise ValueError(
                f"{record.id}: partition key field {field_name!r} is an empty list; "
                "cannot compute a partition key value"
            )
        value = value[0]
    return value.value if hasattr(value, "value") else str(value)
