"""One-time (or idempotent re-run) provisioning of Brain's 9 Cosmos
containers, per providers/azure_cosmos_config.py's container/partition-key
plan (Part 1 §10.2, AGENT_DESIGN_NOTES.md §14.3).

Creates each container with NO explicit throughput header -- this Cosmos
account (optisweepsupportdev / optisweep_knowledge_phase0) is serverless
or uses shared database throughput (confirmed by the existing 10
pre-Brain containers, none of which were created with a per-container
throughput setting either); an explicit throughput request would either
be rejected or needlessly provision dedicated RU/s on a container that
doesn't need it yet.

Usage:
    python -m providers.scripts.provision_brain_cosmos_containers
    python -m providers.scripts.provision_brain_cosmos_containers --dry-run
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import urllib.error
import urllib.parse
import urllib.request
from email.utils import formatdate

from providers.azure_cosmos_config import (
    CONTAINER_BY_RECORD_TYPE,
    COSMOS_PARTITION_KEY_PATH,
    EMBEDDINGS_CONTAINER,
    INGESTION_RUNS_CONTAINER,
    load_brain_cosmos_settings,
)

_API_VERSION = "2018-12-31"


def _authorization_header(*, verb: str, resource_type: str, resource_id: str, key: str, date: str) -> str:
    string_to_sign = f"{verb.lower()}\n{resource_type.lower()}\n{resource_id}\n{date.lower()}\n\n"
    key_bytes = base64.b64decode(key)
    signature = base64.b64encode(hmac.new(key_bytes, string_to_sign.encode("utf-8"), hashlib.sha256).digest()).decode(
        "utf-8"
    )
    return f"type=master&ver=1.0&sig={urllib.parse.quote(signature, safe='')}"


def _list_existing_containers(endpoint: str, key: str, database: str) -> set[str]:
    resource_id = f"dbs/{database}"
    date = formatdate(timeval=None, localtime=False, usegmt=True)
    headers = {
        "Authorization": _authorization_header(verb="GET", resource_type="colls", resource_id=resource_id, key=key, date=date),
        "x-ms-date": date,
        "x-ms-version": _API_VERSION,
    }
    url = f"{endpoint.rstrip('/')}/{resource_id}/colls"
    request = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return {c["id"] for c in payload.get("DocumentCollections", [])}


def _create_container(endpoint: str, key: str, database: str, container_id: str, partition_key_path: str) -> None:
    resource_id = f"dbs/{database}"
    date = formatdate(timeval=None, localtime=False, usegmt=True)
    headers = {
        "Authorization": _authorization_header(verb="POST", resource_type="colls", resource_id=resource_id, key=key, date=date),
        "x-ms-date": date,
        "x-ms-version": _API_VERSION,
        "Content-Type": "application/json",
    }
    body = {"id": container_id, "partitionKey": {"paths": [partition_key_path], "kind": "Hash"}}
    url = f"{endpoint.rstrip('/')}/{resource_id}/colls"
    request = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=30):
        return


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="List what would be created without creating it.")
    args = parser.parse_args()

    settings = load_brain_cosmos_settings()
    if not (settings.endpoint and settings.key and settings.database):
        raise SystemExit("COSMOS_ENDPOINT / COSMOS_KEY / COSMOS_DATABASE must be set.")

    # Every container uses the SAME partition key path (see
    # azure_cosmos_config.COSMOS_PARTITION_KEY_PATH's docstring for why:
    # Playbook's natural partition field is a list, which Cosmos cannot
    # partition on directly, so every record type's document carries a
    # precomputed synthetic `_partition_key` scalar field instead).
    plan: list[tuple[str, str]] = [
        (container, COSMOS_PARTITION_KEY_PATH) for container in CONTAINER_BY_RECORD_TYPE.values()
    ]
    plan.append((INGESTION_RUNS_CONTAINER, COSMOS_PARTITION_KEY_PATH))
    plan.append((EMBEDDINGS_CONTAINER, COSMOS_PARTITION_KEY_PATH))

    existing = _list_existing_containers(settings.endpoint, settings.key, settings.database)
    print(f"Database {settings.database!r} currently has {len(existing)} containers.")

    for container_id, partition_key_path in plan:
        if container_id in existing:
            print(f"  SKIP  {container_id} (already exists)")
            continue
        if args.dry_run:
            print(f"  WOULD CREATE  {container_id}  partitionKey={partition_key_path}")
            continue
        _create_container(settings.endpoint, settings.key, settings.database, container_id, partition_key_path)
        print(f"  CREATED  {container_id}  partitionKey={partition_key_path}")


if __name__ == "__main__":
    main()
