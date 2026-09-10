# Gate phrase table (app load contract)

Published by Stage 11 cumulative publish into Cosmos container `gate_phrase_tables`.

## Document

| Field | Value |
|-------|-------|
| Container | `gate_phrase_tables` |
| Partition key | `/publish_version_id` (same as playbooks) |
| `id` | `gate_phrases` (stable; one doc per version) |
| `doc_type` | `gate_phrase_table` |

## Payload

```json
{
  "id": "gate_phrases",
  "doc_type": "gate_phrase_table",
  "publish_version_id": "publish_YYYYMMDD_HHMMSS_xxxxxxxx",
  "legacy_signal_phrases": {
    "agvs_stopped": ["agvs stopped", "agvs aren't moving", "..."],
    "no_rms_alarm": ["no rms alarms", "rms showing no alarms", "..."]
  },
  "canonical_signal_phrases": { "...": ["..."] },
  "component_phrases": { "...": ["..."] }
}
```

Phrases are lowercase. Cumulative: prior published table ∪ seed ∪ new playbook operator examples (classified onto CAT-1 / canonical keys).

## App load

On corpus reload for `publish_version_id`:

1. Read `gate_phrases` from `gate_phrase_tables` for that version.
2. If present → `KeywordSignalExtractor.from_phrases(legacy_signal_phrases=..., canonical_signal_phrases=..., component_phrases=...)`.
3. Else → local YAML fallback (dev/sample/tests only).

No per-request Cosmos sync. No app YAML PR for each new case.

## Smoke (ingest)

Query `agvs aren't moving, rms showing no alarms` must hit legacy keys `agvs_stopped` + `no_rms_alarm` against the published table before upload.
