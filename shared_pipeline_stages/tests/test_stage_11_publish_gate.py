from shared_pipeline_stages.stage_11.publish_gate import (
    PublishInventory,
    validate_cumulative_publish,
)
from shared_pipeline_stages.stage_8.support_language import enrich_support_user_language_examples


def test_stoppage_examples_are_enriched() -> None:
    examples = enrich_support_user_language_examples(
        ["AGVs stopped"],
        case_id="228086",
        title="Site-wide motion stoppage recovery",
        observed_entry_symptoms=["AGVs are out of sync across the site"],
    )
    lowered = {item.casefold() for item in examples}
    assert "agvs aren't moving" in lowered
    assert "no rms alarms" in lowered


def test_pairing_case_gets_required_examples() -> None:
    examples = enrich_support_user_language_examples(
        ["The zone is unable to get a pair"],
        case_id="228723",
        title="Zone pairing hospitalized AMRs",
        observed_entry_symptoms=["Replacement or multiple AMRs reported as going to the hospital lane"],
    )
    lowered = {item.casefold() for item in examples}
    assert "pairing failure" in lowered
    assert any("hospital" in item for item in lowered)


def test_gate_fails_when_prior_case_missing() -> None:
    baseline = PublishInventory(
        case_ids={"228086", "218550"},
        playbook_ids={"playbook_a"},
        playbook_embedding_count=2,
        runbook_count=10,
        playbooks_prompt_b_count=7,
    )
    candidate = PublishInventory(
        case_ids={"218550"},
        playbook_ids={"playbook_a"},
        playbook_embedding_count=2,
        runbook_count=10,
        playbooks_prompt_b_count=7,
    )
    result = validate_cumulative_publish(candidate=candidate, baseline=baseline)
    assert not result.passed
    assert any("228086" in error for error in result.errors)


def test_gate_allows_embedding_drop_fully_accounted_for_by_deprecations() -> None:
    baseline = PublishInventory(
        case_ids={"228086"},
        playbook_ids={"playbook_incident_228086_sitewide_robotic_stoppage"},
        embedding_ids={
            "emb_playbook_prompt_a_playbook_incident_228086_sitewide_robotic_stoppage",
            "emb_playbook_prompt_a_playbook_incident_228086_site_stoppage_optisweep_recovery",
            "emb_playbook_prompt_a_playbook_incident_228086_wcswebapplication_fault_investigation",
        },
        playbook_embedding_count=3,
        runbook_count=5,
        playbooks_prompt_b_count=1,
    )
    candidate = PublishInventory(
        case_ids={"228086"},
        playbook_ids={"playbook_incident_228086_sitewide_robotic_stoppage"},
        embedding_ids={"emb_playbook_prompt_a_playbook_incident_228086_sitewide_robotic_stoppage"},
        playbook_embedding_count=1,
        runbook_count=5,
        playbooks_prompt_b_count=1,
    )
    deprecated = {
        "playbook_incident_228086_site_stoppage_optisweep_recovery",
        "playbook_incident_228086_wcswebapplication_fault_investigation",
    }
    result = validate_cumulative_publish(candidate=candidate, baseline=baseline, deprecated_ids=deprecated)
    assert result.passed, result.errors


def test_gate_still_fails_on_embedding_drop_not_covered_by_deprecations() -> None:
    baseline = PublishInventory(
        case_ids={"228086"},
        playbook_ids={"playbook_incident_228086_sitewide_robotic_stoppage"},
        embedding_ids={
            f"emb_playbook_prompt_a_playbook_incident_228086_variant_{i}" for i in range(20)
        },
        playbook_embedding_count=20,
        runbook_count=5,
        playbooks_prompt_b_count=1,
    )
    candidate = PublishInventory(
        case_ids={"228086"},
        playbook_ids={"playbook_incident_228086_sitewide_robotic_stoppage"},
        embedding_ids={"emb_playbook_prompt_a_playbook_incident_228086_variant_0"},
        playbook_embedding_count=1,
        runbook_count=5,
        playbooks_prompt_b_count=1,
    )
    # Only one of the 19 dropped embeddings is on the deprecation list — the other
    # 18 are an unexplained drop and must still fail the gate.
    deprecated = {"playbook_incident_228086_variant_1"}
    result = validate_cumulative_publish(candidate=candidate, baseline=baseline, deprecated_ids=deprecated)
    assert not result.passed
    assert any("embedding count dropped materially" in error for error in result.errors)


def test_gate_fails_on_empty_examples() -> None:
    baseline = PublishInventory(
        case_ids={"228086"},
        playbook_ids={"playbook_a"},
        playbook_embedding_count=1,
        runbook_count=5,
        playbooks_prompt_b_count=1,
    )
    candidate = PublishInventory(
        case_ids={"228086"},
        playbook_ids={"playbook_a"},
        playbook_embedding_count=1,
        runbook_count=5,
        playbooks_prompt_b_count=1,
        empty_example_playbook_ids=["playbook_a"],
    )
    result = validate_cumulative_publish(candidate=candidate, baseline=baseline)
    assert not result.passed
    assert any("support_user_language_examples" in error for error in result.errors)


def test_gate_fails_when_prompt_b_count_drops() -> None:
    baseline = PublishInventory(
        case_ids={"228086"},
        playbook_ids={"a", "b"},
        playbook_embedding_count=2,
        runbook_count=5,
        playbooks_prompt_b_count=7,
    )
    candidate = PublishInventory(
        case_ids={"228086"},
        playbook_ids={"a", "b"},
        playbook_embedding_count=2,
        runbook_count=5,
        playbooks_prompt_b_count=5,
    )
    result = validate_cumulative_publish(candidate=candidate, baseline=baseline)
    assert not result.passed
    assert any("Prompt B" in error for error in result.errors)


def test_gate_fails_when_images_missing_storage_uri() -> None:
    baseline = PublishInventory(
        case_ids={"228086"},
        playbook_ids={"playbook_a"},
        playbook_embedding_count=1,
        runbook_count=5,
        playbooks_prompt_b_count=1,
    )
    candidate = PublishInventory(
        case_ids={"228086"},
        playbook_ids={"playbook_a"},
        playbook_embedding_count=1,
        runbook_count=5,
        playbooks_prompt_b_count=1,
        canonical_image_count=2,
        canonical_images_with_storage_uri=0,
        images_missing_storage_uri=["artifact_a", "artifact_b"],
    )
    result = validate_cumulative_publish(candidate=candidate, baseline=baseline)
    assert not result.passed
    assert any("storage_uri" in error for error in result.errors)


def test_gate_passes_when_all_images_have_storage_uri() -> None:
    baseline = PublishInventory(
        case_ids={"228086"},
        playbook_ids={"playbook_a"},
        playbook_embedding_count=1,
        runbook_count=5,
        playbooks_prompt_b_count=1,
    )
    candidate = PublishInventory(
        case_ids={"228086"},
        playbook_ids={"playbook_a"},
        playbook_embedding_count=1,
        runbook_count=5,
        playbooks_prompt_b_count=1,
        canonical_image_count=2,
        canonical_images_with_storage_uri=2,
    )
    result = validate_cumulative_publish(candidate=candidate, baseline=baseline)
    assert result.passed
