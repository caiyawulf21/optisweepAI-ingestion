"""Generic "grow richer, never regress" merge for Brain records re-encountered
across sources.

Part 1 §9 requires resolving to an existing record and reconciling new
evidence into it rather than creating a duplicate — but the original
migration only ever merged source_refs. A capability or entity mentioned by
five sources should end up describable by all five, not just cited by them:
a later source's richer description, additional aliases, or additional
target/allowed-surface IDs should all be picked up. Never regress: a
populated field is never overwritten by an empty one from a thinner source.
"""

from __future__ import annotations

import json
from typing import TypeVar

from pydantic import BaseModel

Model = TypeVar("Model", bound=BaseModel)


def _dedup_key(item):
    # Plain hashable values (str, int, ...) are used as-is. Pydantic model
    # list items (KeyField, SqlFieldNote, ...) and plain dicts (payload
    # sub-fields arrive as raw dicts before Entity's own validation parses
    # them) are not hashable, so dedupe by a stable serialized form instead.
    if isinstance(item, BaseModel):
        return item.model_dump_json()
    if isinstance(item, dict):
        return json.dumps(item, sort_keys=True, default=str)
    return item


def merge_list_field(existing: list, incoming: list) -> list:
    """Union two lists, preserving existing order, appending only new items."""
    if not incoming:
        return existing
    seen = {_dedup_key(item) for item in existing}
    merged = list(existing)
    for item in incoming:
        key = _dedup_key(item)
        if key not in seen:
            seen.add(key)
            merged.append(item)
    return merged


def merge_scalar_field(existing, incoming):
    """Fill an empty/None scalar from incoming; never overwrite a populated one."""
    if existing not in (None, "", 0, 0.0):
        return existing
    return incoming if incoming not in (None, "") else existing


def merge_record(existing: Model, incoming_fields: dict) -> Model:
    """Return a new copy of `existing` with `incoming_fields` merged in.

    For each field present in incoming_fields:
    - list values are unioned (merge_list_field)
    - dict/BaseModel values recurse one level (union list sub-fields, fill
      empty scalar sub-fields) so a richer nested object (e.g. Observables,
      SupportContract) is picked up without discarding what's already there
    - scalar values fill only if the existing value is empty (merge_scalar_field)

    Returns `existing` unchanged (same object) if nothing actually changed,
    so callers can cheaply check `result is existing` to skip a write.
    """
    updates: dict = {}
    for field_name, incoming_value in incoming_fields.items():
        if field_name not in type(existing).model_fields:
            continue
        current_value = getattr(existing, field_name)

        if isinstance(current_value, list):
            merged = merge_list_field(current_value, incoming_value or [])
            if merged != current_value:
                updates[field_name] = merged

        elif isinstance(current_value, BaseModel) and isinstance(incoming_value, (BaseModel, dict)):
            incoming_dict = (
                incoming_value.model_dump() if isinstance(incoming_value, BaseModel) else incoming_value
            )
            nested_updates: dict = {}
            for sub_name, sub_incoming in incoming_dict.items():
                if sub_name not in type(current_value).model_fields:
                    continue
                sub_current = getattr(current_value, sub_name)
                if isinstance(sub_current, list):
                    merged_sub = merge_list_field(sub_current, sub_incoming or [])
                    if merged_sub != sub_current:
                        nested_updates[sub_name] = merged_sub
                else:
                    merged_sub = merge_scalar_field(sub_current, sub_incoming)
                    if merged_sub != sub_current:
                        nested_updates[sub_name] = merged_sub
            if nested_updates:
                nested_merged_data = {**current_value.model_dump(mode="python"), **nested_updates}
                updates[field_name] = type(current_value).model_validate(nested_merged_data)

        elif current_value is None and incoming_value is not None:
            updates[field_name] = incoming_value

        else:
            merged = merge_scalar_field(current_value, incoming_value)
            if merged != current_value:
                updates[field_name] = merged

    if not updates:
        return existing
    # model_copy(update=...) does not re-validate, so a raw dict merged into
    # a list of typed sub-models (e.g. Capability.sql_field_notes,
    # Entity.payload.key_fields) would stay an unvalidated dict — harmless in
    # that model_dump_json() still serializes the right data, but the field
    # is no longer actually the declared type, which is exactly the kind of
    # quiet drift Part 1's strict schemas exist to prevent. Re-validating the
    # full merged state through the model closes that gap: every sub-item
    # ends up as its proper typed model, not just correctly-valued JSON.
    merged_data = {**existing.model_dump(mode="python"), **updates}
    return type(existing).model_validate(merged_data)
