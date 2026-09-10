from shared_pipeline_stages.stage_11.corpus_merge import (
    _merge_by_key,
    _merge_playbooks_by_case,
)


def _playbook_doc(doc_id: str, case_id: str, title: str) -> dict:
    return {
        "id": doc_id,
        "doc_type": "playbook",
        "record_id": doc_id,
        "payload": {"case_id": case_id, "playbook_id": doc_id, "title": title},
    }


def test_regenerated_candidate_replaces_stale_case_playbooks() -> None:
    baseline = [
        _playbook_doc("playbook_incident_228086_site_stoppage_optisweep_recovery", "228086", "old A"),
        _playbook_doc("playbook_incident_228086_site_wide_motion_stoppage_service_recovery", "228086", "old B"),
        _playbook_doc("playbook_incident_228086_wcswebapplication_fault_investigation", "228086", "old C"),
        _playbook_doc("playbook_incident_218550_bagout_agv_sequence", "218550", "untouched"),
    ]
    candidate = [
        _playbook_doc("playbook_incident_228086_sitewide_robotic_stoppage", "228086", "current"),
    ]

    merged, kept, added = _merge_playbooks_by_case(candidate, baseline, publish_version_id="publish_test")
    ids = sorted(row["id"] for row in merged)

    assert ids == [
        "playbook_incident_218550_bagout_agv_sequence",
        "playbook_incident_228086_sitewide_robotic_stoppage",
    ]
    assert kept == 1
    assert added == 1


def test_case_with_no_candidate_change_is_carried_forward_unmodified() -> None:
    baseline = [_playbook_doc("playbook_incident_218550_bagout_agv_sequence", "218550", "baseline title")]
    merged, kept, added = _merge_playbooks_by_case([], baseline, publish_version_id="publish_test")

    assert len(merged) == 1
    assert merged[0]["payload"]["title"] == "baseline title"
    assert kept == 0
    assert added == 1


def test_rows_missing_case_id_fall_back_to_id_merge_instead_of_dropping() -> None:
    malformed_baseline = [{"id": "orphan_doc", "doc_type": "playbook", "record_id": "orphan_doc", "payload": {}}]
    merged, _kept, _added = _merge_playbooks_by_case([], malformed_baseline, publish_version_id="publish_test")

    assert [row["id"] for row in merged] == ["orphan_doc"]


def test_merge_by_key_is_unaffected_for_non_playbook_datasets() -> None:
    baseline = [{"id": "runbook_1", "payload": {"title": "old"}}]
    candidate = [{"id": "runbook_2", "payload": {"title": "new"}}]

    merged, kept, added = _merge_by_key(candidate, baseline, id_key="id", publish_version_id="publish_test")

    assert {row["id"] for row in merged} == {"runbook_1", "runbook_2"}
    assert kept == 1
    assert added == 1
