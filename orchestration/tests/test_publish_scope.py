from __future__ import annotations

from shared_pipeline_stages.stage_11.publish_scope import (
    PublishScope,
    filter_upload_datasets,
    parse_publish_scope,
)


def test_parse_publish_scope_variants() -> None:
    assert parse_publish_scope("all").kind == "all"
    assert parse_publish_scope("case:228086") == PublishScope(kind="case", value="228086")
    assert parse_publish_scope("case:auto", default_case_id="228723") == PublishScope(
        kind="case", value="228723"
    )
    assert parse_publish_scope("source:manual_optisweep_om_v3") == PublishScope(
        kind="source", value="manual_optisweep_om_v3"
    )


def test_filter_upload_datasets_case_scope() -> None:
    datasets = {
        "playbooks_prompt_a": [
            {
                "id": "playbook_a",
                "record_id": "playbook_incident_228086_x",
                "payload": {"playbook_id": "playbook_incident_228086_x", "case_id": "228086"},
            },
            {
                "id": "playbook_b",
                "record_id": "playbook_incident_228723_y",
                "payload": {"playbook_id": "playbook_incident_228723_y", "case_id": "228723"},
            },
        ],
        "playbooks_prompt_b": [],
        "runbooks": [
            {
                "id": "runbook_keep",
                "record_id": "proc_keep_v1",
                "payload": {
                    "procedure_id": "proc_keep_v1",
                    "metadata": {"source_id": "source_case_228086"},
                },
            },
            {
                "id": "runbook_drop",
                "record_id": "proc_drop_v1",
                "payload": {
                    "procedure_id": "proc_drop_v1",
                    "metadata": {"source_id": "manual_optisweep_om_v3"},
                },
            },
            {
                "id": "runbook_linked",
                "record_id": "proc_linked_v1",
                "payload": {"procedure_id": "proc_linked_v1", "metadata": {"source_id": "manual"}},
            },
        ],
        "operational_context": [],
        "source_artifacts": [
            {
                "id": "art_keep",
                "filter_metadata": {"source_id": "source_case_228086"},
            },
            {
                "id": "art_drop",
                "filter_metadata": {"source_id": "manual_optisweep_om_v3"},
            },
        ],
        "canonical_images": [],
        "relationship_links": [
            {
                "id": "shard_0",
                "doc_type": "relationship_link_shard",
                "links": [
                    {
                        "link_type": "playbook_runbook",
                        "source_record_id": "playbook_incident_228086_x:node_1",
                        "target_record_id": "proc_linked_v1",
                    },
                    {
                        "link_type": "playbook_runbook",
                        "source_record_id": "playbook_incident_228723_y:node_1",
                        "target_record_id": "proc_drop_v1",
                    },
                ],
            }
        ],
    }
    filtered, counts = filter_upload_datasets(datasets, PublishScope(kind="case", value="228086"))
    assert counts["playbooks_prompt_a"] == 1
    assert counts["source_artifacts"] == 1
    assert {row["record_id"] for row in filtered["runbooks"]} == {"proc_keep_v1", "proc_linked_v1"}
    assert filtered["relationship_links"][0]["link_count"] == 1
