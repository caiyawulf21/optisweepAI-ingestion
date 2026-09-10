from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class PublishInventory:
    case_ids: set[str] = field(default_factory=set)
    playbook_ids: set[str] = field(default_factory=set)
    runbook_ids: set[str] = field(default_factory=set)
    embedding_ids: set[str] = field(default_factory=set)
    playbook_embedding_count: int = 0
    runbook_count: int = 0
    playbooks_prompt_a_count: int = 0
    playbooks_prompt_b_count: int = 0
    empty_example_playbook_ids: list[str] = field(default_factory=list)
    low_coverage_playbook_ids: list[str] = field(default_factory=list)
    canonical_image_count: int = 0
    canonical_images_with_storage_uri: int = 0
    images_missing_storage_uri: list[str] = field(default_factory=list)


@dataclass
class ManifestDiff:
    added: list[str] = field(default_factory=list)
    kept: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    deprecated: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "added": sorted(self.added),
            "kept": sorted(self.kept),
            "updated": sorted(self.updated),
            "removed": sorted(self.removed),
            "deprecated": sorted(self.deprecated),
        }


@dataclass
class PublishGateResult:
    passed: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    manifest_diff: ManifestDiff = field(default_factory=ManifestDiff)
    baseline_inventory: PublishInventory = field(default_factory=PublishInventory)
    candidate_inventory: PublishInventory = field(default_factory=PublishInventory)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "errors": self.errors,
            "warnings": self.warnings,
            "manifest_diff": self.manifest_diff.to_dict(),
            "baseline": _inventory_dict(self.baseline_inventory),
            "candidate": _inventory_dict(self.candidate_inventory),
        }


def inventory_from_bundle(bundle_dir: str | Path) -> PublishInventory:
    from shared_pipeline_stages.stage_8.support_language import symptom_example_coverage

    root = Path(bundle_dir)
    inventory = PublishInventory()

    for variant in ("playbooks_prompt_a", "playbooks_prompt_b"):
        for doc in _load_json_list(root / variant / "documents.json"):
            payload = doc.get("payload") if isinstance(doc.get("payload"), dict) else doc
            case_id = str(payload.get("case_id") or doc.get("case_id") or "").strip()
            playbook_id = str(
                payload.get("playbook_id") or doc.get("record_id") or doc.get("id") or ""
            ).strip()
            if case_id:
                inventory.case_ids.add(case_id)
            if playbook_id:
                inventory.playbook_ids.add(playbook_id)
            if variant == "playbooks_prompt_a":
                inventory.playbooks_prompt_a_count += 1
            else:
                inventory.playbooks_prompt_b_count += 1
            examples = payload.get("support_user_language_examples") or []
            symptoms = payload.get("observed_entry_symptoms") or []
            if playbook_id and not [item for item in examples if str(item).strip()]:
                inventory.empty_example_playbook_ids.append(playbook_id)
            elif playbook_id and symptom_example_coverage(symptoms, examples) < 0.5:
                inventory.low_coverage_playbook_ids.append(playbook_id)

        for doc in _load_json_list(root / variant / "embeddings.json"):
            emb_id = str(doc.get("id") or doc.get("record_id") or "").strip()
            if emb_id:
                inventory.embedding_ids.add(emb_id)
            inventory.playbook_embedding_count += 1

    for doc in _load_json_list(root / "runbooks" / "documents.json"):
        payload = doc.get("payload") if isinstance(doc.get("payload"), dict) else doc
        procedure_id = str(
            payload.get("procedure_id") or doc.get("record_id") or doc.get("id") or ""
        ).strip()
        if procedure_id:
            inventory.runbook_ids.add(procedure_id)
        inventory.runbook_count += 1

    for doc in _load_json_list(root / "runbooks" / "embeddings.json"):
        emb_id = str(doc.get("id") or doc.get("record_id") or "").strip()
        if emb_id:
            inventory.embedding_ids.add(emb_id)

    for doc in _load_json_list(root / "canonical_images" / "documents.json"):
        inventory.canonical_image_count += 1
        image_id = str(doc.get("image_id") or doc.get("id") or "").strip() or "unknown"
        storage_uri = str(doc.get("storage_uri") or "").strip()
        if storage_uri.startswith("http://") or storage_uri.startswith("https://"):
            inventory.canonical_images_with_storage_uri += 1
        else:
            inventory.images_missing_storage_uri.append(image_id)

    return inventory


def inventory_from_datasets(datasets: dict[str, list[dict[str, Any]]]) -> PublishInventory:
    inventory = PublishInventory()
    for dataset in ("playbooks_prompt_a", "playbooks_prompt_b"):
        for doc in datasets.get(dataset) or []:
            if str(doc.get("doc_type") or "") == "embedding":
                emb_id = str(doc.get("id") or doc.get("record_id") or "").strip()
                if emb_id:
                    inventory.embedding_ids.add(emb_id)
                inventory.playbook_embedding_count += 1
                continue
            payload = doc.get("payload") if isinstance(doc.get("payload"), dict) else doc
            case_id = str(payload.get("case_id") or doc.get("case_id") or "").strip()
            playbook_id = str(
                payload.get("playbook_id") or doc.get("record_id") or doc.get("id") or ""
            ).strip()
            if case_id:
                inventory.case_ids.add(case_id)
            if playbook_id:
                inventory.playbook_ids.add(playbook_id)
            examples = payload.get("support_user_language_examples") or []
            if playbook_id and not [item for item in examples if str(item).strip()]:
                inventory.empty_example_playbook_ids.append(playbook_id)

    for doc in datasets.get("runbooks") or []:
        if str(doc.get("doc_type") or "") == "embedding":
            emb_id = str(doc.get("id") or doc.get("record_id") or "").strip()
            if emb_id:
                inventory.embedding_ids.add(emb_id)
            continue
        payload = doc.get("payload") if isinstance(doc.get("payload"), dict) else doc
        procedure_id = str(
            payload.get("procedure_id") or doc.get("record_id") or doc.get("id") or ""
        ).strip()
        if procedure_id:
            inventory.runbook_ids.add(procedure_id)
        inventory.runbook_count += 1

    return inventory


def load_deprecations(path: str | Path | None) -> set[str]:
    if path is None:
        return set()
    deprecation_path = Path(path)
    if not deprecation_path.exists():
        return set()
    payload = json.loads(deprecation_path.read_text(encoding="utf-8"))
    rows = payload.get("deprecated") if isinstance(payload, dict) else payload
    if not isinstance(rows, list):
        return set()
    deprecated: set[str] = set()
    for row in rows:
        if isinstance(row, str):
            deprecated.add(row.strip())
        elif isinstance(row, dict):
            for key in ("record_id", "playbook_id", "case_id", "procedure_id", "id"):
                value = str(row.get(key) or "").strip()
                if value:
                    deprecated.add(value)
    return {item for item in deprecated if item}


def validate_cumulative_publish(
    *,
    candidate: PublishInventory,
    baseline: PublishInventory,
    deprecated_ids: set[str] | None = None,
    max_playbook_embedding_drop_ratio: float = 0.05,
    max_runbook_drop_ratio: float = 0.05,
    require_playbook_examples: bool = True,
    require_symptom_coverage: bool = True,
    require_image_storage_uri: bool = True,
    min_prompt_b_playbooks: int | None = None,
) -> PublishGateResult:
    deprecated = deprecated_ids or set()
    errors: list[str] = []
    warnings: list[str] = []
    diff = ManifestDiff()

    for case_id in sorted(baseline.case_ids | candidate.case_ids):
        in_base = case_id in baseline.case_ids
        in_cand = case_id in candidate.case_ids
        if in_base and in_cand:
            diff.kept.append(f"case:{case_id}")
        elif in_cand:
            diff.added.append(f"case:{case_id}")
        elif case_id in deprecated:
            diff.deprecated.append(f"case:{case_id}")
        else:
            diff.removed.append(f"case:{case_id}")
            errors.append(
                f"Previously published case_id {case_id} is missing without a deprecation entry."
            )

    for playbook_id in sorted(baseline.playbook_ids | candidate.playbook_ids):
        in_base = playbook_id in baseline.playbook_ids
        in_cand = playbook_id in candidate.playbook_ids
        if in_base and in_cand:
            diff.kept.append(f"playbook:{playbook_id}")
        elif in_cand:
            diff.added.append(f"playbook:{playbook_id}")
        elif playbook_id in deprecated:
            diff.deprecated.append(f"playbook:{playbook_id}")
        else:
            diff.removed.append(f"playbook:{playbook_id}")
            errors.append(
                f"Previously published playbook {playbook_id} is missing without a deprecation entry."
            )

    expected_prompt_b = min_prompt_b_playbooks
    if expected_prompt_b is None and baseline.playbooks_prompt_b_count:
        expected_prompt_b = baseline.playbooks_prompt_b_count
    if expected_prompt_b and candidate.playbooks_prompt_b_count < expected_prompt_b:
        errors.append(
            "Prompt B playbook count below required floor: "
            f"candidate={candidate.playbooks_prompt_b_count} required>={expected_prompt_b}."
        )

    if baseline.playbook_embedding_count:
        drop = baseline.playbook_embedding_count - candidate.playbook_embedding_count
        deprecated_embedding_count = sum(
            1
            for emb_id in baseline.embedding_ids
            if any(dep_id and dep_id in emb_id for dep_id in deprecated)
        )
        unexplained_drop = max(0, drop - deprecated_embedding_count)
        if unexplained_drop > 0 and unexplained_drop / baseline.playbook_embedding_count > max_playbook_embedding_drop_ratio:
            errors.append(
                "Playbook embedding count dropped materially beyond what the deprecation "
                f"list accounts for: baseline={baseline.playbook_embedding_count} "
                f"candidate={candidate.playbook_embedding_count} deprecated_accounted_for="
                f"{deprecated_embedding_count} unexplained_drop={unexplained_drop}."
            )
        elif drop > 0:
            warnings.append(
                f"Playbook embedding count dropped by {drop} "
                f"({baseline.playbook_embedding_count} -> {candidate.playbook_embedding_count}), "
                f"{deprecated_embedding_count} of which are accounted for by the deprecation list."
            )

    if baseline.runbook_count:
        drop = baseline.runbook_count - candidate.runbook_count
        if drop > 0 and drop / baseline.runbook_count > max_runbook_drop_ratio:
            errors.append(
                "Runbook count dropped materially: "
                f"baseline={baseline.runbook_count} candidate={candidate.runbook_count}."
            )
        elif drop > 0:
            warnings.append(
                f"Runbook count dropped by {drop} ({baseline.runbook_count} -> {candidate.runbook_count})."
            )

    if require_playbook_examples and candidate.empty_example_playbook_ids:
        sample = ", ".join(sorted(set(candidate.empty_example_playbook_ids))[:8])
        errors.append(
            "Playbooks used for retrieval have empty support_user_language_examples: "
            f"{sample}."
        )

    if require_symptom_coverage and candidate.low_coverage_playbook_ids:
        sample = ", ".join(sorted(set(candidate.low_coverage_playbook_ids))[:8])
        errors.append(
            "Playbooks have observed_entry_symptoms poorly covered by operator-language examples: "
            f"{sample}."
        )

    if require_image_storage_uri and candidate.canonical_image_count:
        missing = candidate.images_missing_storage_uri
        if missing:
            sample = ", ".join(sorted(set(missing))[:8])
            errors.append(
                "Canonical images missing HTTPS storage_uri "
                f"({len(missing)}/{candidate.canonical_image_count}): {sample}."
            )
        elif candidate.canonical_images_with_storage_uri < candidate.canonical_image_count:
            errors.append(
                "Canonical images missing HTTPS storage_uri: "
                f"{candidate.canonical_images_with_storage_uri}/{candidate.canonical_image_count} renderable."
            )

    return PublishGateResult(
        passed=not errors,
        errors=errors,
        warnings=warnings,
        manifest_diff=diff,
        baseline_inventory=baseline,
        candidate_inventory=candidate,
    )


def _inventory_dict(inventory: PublishInventory) -> dict[str, Any]:
    return {
        "case_ids": sorted(inventory.case_ids),
        "playbook_ids": sorted(inventory.playbook_ids),
        "runbook_count": inventory.runbook_count,
        "playbooks_prompt_a_count": inventory.playbooks_prompt_a_count,
        "playbooks_prompt_b_count": inventory.playbooks_prompt_b_count,
        "playbook_embedding_count": inventory.playbook_embedding_count,
        "empty_example_playbook_ids": sorted(set(inventory.empty_example_playbook_ids)),
        "low_coverage_playbook_ids": sorted(set(inventory.low_coverage_playbook_ids)),
        "canonical_image_count": inventory.canonical_image_count,
        "canonical_images_with_storage_uri": inventory.canonical_images_with_storage_uri,
        "images_missing_storage_uri": sorted(set(inventory.images_missing_storage_uri)),
    }


def _load_json_list(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in ("documents", "embeddings", "records", "playbooks", "runbooks"):
            rows = payload.get(key)
            if isinstance(rows, list):
                return [row for row in rows if isinstance(row, dict)]
    return []
