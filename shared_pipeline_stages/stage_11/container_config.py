from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

DATASET_RUNBOOKS = "runbooks"
DATASET_PLAYBOOKS_A = "playbooks_prompt_a"
DATASET_PLAYBOOKS_B = "playbooks_prompt_b"
DATASET_OPERATIONAL_CONTEXT = "operational_context"
DATASET_SOURCE_ARTIFACTS = "source_artifacts"
DATASET_RELATIONSHIP_LINKS = "relationship_links"
DATASET_CANONICAL_IMAGES = "canonical_images"
DATASET_GATE_PHRASE_TABLES = "gate_phrase_tables"

CONTAINER_ENV_KEYS = {
    DATASET_RUNBOOKS: "COSMOS_CONTAINER_RUNBOOKS",
    DATASET_PLAYBOOKS_A: "COSMOS_CONTAINER_PLAYBOOKS_A",
    DATASET_PLAYBOOKS_B: "COSMOS_CONTAINER_PLAYBOOKS_B",
    DATASET_OPERATIONAL_CONTEXT: "COSMOS_CONTAINER_OPERATIONAL_CONTEXT",
    DATASET_SOURCE_ARTIFACTS: "COSMOS_CONTAINER_SOURCE_ARTIFACTS",
    DATASET_RELATIONSHIP_LINKS: "COSMOS_CONTAINER_RELATIONSHIP_LINKS",
    DATASET_CANONICAL_IMAGES: "COSMOS_CONTAINER_CANONICAL_IMAGES",
    DATASET_GATE_PHRASE_TABLES: "COSMOS_CONTAINER_GATE_PHRASE_TABLES",
}

CONTAINER_DEFAULTS = {
    DATASET_RUNBOOKS: "runbooks",
    DATASET_PLAYBOOKS_A: "playbooks_prompt_a",
    DATASET_PLAYBOOKS_B: "playbooks_prompt_b",
    DATASET_OPERATIONAL_CONTEXT: "operational_context",
    DATASET_SOURCE_ARTIFACTS: "publish_source_artifacts",
    DATASET_RELATIONSHIP_LINKS: "relationship_links",
    DATASET_CANONICAL_IMAGES: "publish_canonical_images",
    DATASET_GATE_PHRASE_TABLES: "gate_phrase_tables",
}


@dataclass(frozen=True)
class CosmosSettings:
    endpoint: str
    key: str
    database: str
    containers: dict[str, str]

    def is_complete(self) -> bool:
        return bool(self.endpoint and self.key and self.database and all(self.containers.values()))


@dataclass(frozen=True)
class BlobImageSettings:
    connection_string: str
    container: str
    account_url: str

    def is_complete(self) -> bool:
        return bool(self.connection_string and self.container)


def load_cosmos_settings() -> CosmosSettings:
    load_dotenv()
    containers = {
        dataset: _clean_env(os.getenv(env_key)) or CONTAINER_DEFAULTS[dataset]
        for dataset, env_key in CONTAINER_ENV_KEYS.items()
    }
    return CosmosSettings(
        endpoint=_clean_env(os.getenv("COSMOS_ENDPOINT") or os.getenv("AZURE_COSMOS_ENDPOINT")),
        key=_clean_env(os.getenv("COSMOS_KEY") or os.getenv("AZURE_COSMOS_KEY")),
        database=_clean_env(os.getenv("COSMOS_DATABASE") or os.getenv("AZURE_COSMOS_DATABASE_NAME")),
        containers=containers,
    )


def load_blob_image_settings() -> BlobImageSettings:
    load_dotenv()
    connection_string = _clean_env(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
    container = _clean_env(os.getenv("AZURE_CANONICAL_IMAGES_CONTAINER")) or "canonical-images"
    account_url = _clean_env(os.getenv("AZURE_STORAGE_ACCOUNT_URL"))
    if not account_url and connection_string:
        account_name = _connection_string_value(connection_string, "AccountName")
        if account_name:
            account_url = f"https://{account_name}.blob.core.windows.net"
    return BlobImageSettings(
        connection_string=connection_string,
        container=container,
        account_url=account_url,
    )


def _connection_string_value(connection_string: str, key: str) -> str:
    for part in connection_string.split(";"):
        if "=" not in part:
            continue
        name, value = part.split("=", 1)
        if name.strip() == key:
            return value.strip()
    return ""


def _clean_env(value: str | None) -> str:
    return (value or "").strip().strip('"').strip("'")
