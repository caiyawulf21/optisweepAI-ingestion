"""Stage 8 internal capability derivation and domain-rule scoring.

Stage 5 stays source-grounded: it records diagnostic objectives, evidence
concepts, and outcomes without any knowledge of the runbook catalog. Stage 8
is the only place that knows what procedures exist, so it is responsible for
deriving a small internal retrieval request per node (action family, required/
excluded capabilities, preferred surfaces/role) and using it as a *score
adjustment* that runs alongside semantic scoring and boosting -- never as a
hard veto. A strong enough semantic/RAG match can still win against a
domain-rule mismatch, and a weak match can still lose even when
domain-rule-compatible.

The existing `capability_tags` recorded on runbooks (and the `ontology_capabilities`
ids recorded on nodes) are too coarse to use as ground truth on their own --
e.g. both an OPC-COM tag-flow procedure and a generic Ignition gateway restart
procedure are tagged only ``gateway_health`` / ``wcs_api_responsiveness``.  This
module re-derives a finer-grained capability set from title/summary/when_to_use
text using keyword patterns, and unions it with any coarse tags already present.
This finer-grained vocabulary is necessarily incomplete relative to the full
runbook capability_tags taxonomy (docs/ontology/taxonomy/runbook_capability_taxonomy.json)
-- a capability with no fine-grained coverage here should only cost a mild
penalty (NO_REQUIRED_OVERLAP_PENALTY), not eliminate the candidate, since an
uncovered vocabulary gap is not evidence of a real domain conflict.
"""

from __future__ import annotations

import re
from typing import Any

# ---------------------------------------------------------------------------
# Controlled capability vocabulary (Section 7 of the fix plan). These are kept
# intentionally distinct -- related concepts are NOT synonyms.
# ---------------------------------------------------------------------------

CAPABILITIES = frozenset(
    {
        "ignition_gateway_health",
        "ignition_resource_health",
        "ignition_gateway_restart",
        "opc_tag_flow",
        "windows_service_health",
        "wcs_application_error_diagnostic",
        "optisweep_service_restart",
        "wcs_api_responsiveness",
        "agv_state_inspection",
        "agv_active_error_inspection",
        "agv_roster_mapping_validation",
        "agv_remove_recover",
        "multi_signal_recovery_validation",
        "shutdown_queue_transition",
    }
)

# Capability pairs that must never be treated as mutually satisfying for
# *eligibility* purposes -- a candidate offering only the excluded side must
# be rejected outright for a node whose action family is the other side.
MUTUALLY_EXCLUSIVE_GROUPS: tuple[frozenset[str], ...] = (
    frozenset({"opc_tag_flow", "ignition_gateway_health"}),
    frozenset({"agv_state_inspection", "multi_signal_recovery_validation"}),
    frozenset({"agv_remove_recover", "multi_signal_recovery_validation"}),
    # A shutdown/startup zone-cycling check (are AGVs transitioning out of the
    # shutdown queue into their assigned zones after startup?) answers a
    # different question than roster/mapping validation (is a specific robot
    # missing/unmapped/abnormal?) or remove/recover (take a specific robot out
    # of active participation). Both procedures previously shared only the
    # coarse "device_roster_state" tag, so the roster/mapping node in case
    # 228723 could select the shutdown-queue procedure purely because no
    # fine-grained pattern told them apart -- "zone" alone is not sufficient
    # signal for roster/mapping intent.
    frozenset({"shutdown_queue_transition", "agv_roster_mapping_validation"}),
    frozenset({"shutdown_queue_transition", "agv_remove_recover"}),
)

# Capability pairs that are related but must never be treated as synonyms when
# picking a *primary* procedure -- both sides remain independently eligible
# (e.g. an active-error query may corroborate an AGV-state inspection node),
# but neither should be selected as primary purely because it outscored the
# other; see _PRIMARY_CAPABILITY_PREFERENCE in normalize.py.
RELATED_NOT_SYNONYM_GROUPS: tuple[frozenset[str], ...] = (
    frozenset({"agv_active_error_inspection", "agv_state_inspection"}),
    frozenset({"agv_remove_recover", "agv_state_inspection"}),
)

# Ordered (pattern, capability) rules used to classify free text (node or
# runbook). Order matters only for readability; all matching capabilities are
# collected, not just the first.
_TEXT_CAPABILITY_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (
        re.compile(r"\bopc\s*com\b|\btag subscription\b|\btag update\b|\bopc server\b|\bsorter sweeper\b|\btag provider\b", re.I),
        "opc_tag_flow",
    ),
    (
        re.compile(
            r"\bgateway\b\W*(?:\w+\W+){0,4}?\b(restart|recover\w*)\b"
            r"|\b(restart|recover\w*)\b\W*(?:\w+\W+){0,4}?\bgateway\b"
            r"|\bgwcmd\b",
            re.I,
        ),
        "ignition_gateway_restart",
    ),
    (
        re.compile(
            r"\bignition\b.*\b(response time|responsiveness|reachable|unreachable|crash(?:ed)?|slow.response)\b"
            r"|\bsystems overview\b|\bgateway health\b",
            re.I,
        ),
        "ignition_gateway_health",
    ),
    (
        re.compile(r"\bignition\b.*\b(memory|cpu|resource)\b|\b(memory|cpu)\b.*\bignition\b|\bmemory trend\b|\bcpu trend\b", re.I),
        "ignition_resource_health",
    ),
    (
        re.compile(r"\bwindows service\b|\bevent viewer\b|\bservice control manager\b|\bstartup type\b", re.I),
        "windows_service_health",
    ),
    (
        re.compile(r"\bwcswebapplication\b|\bapplication error\b|\bdbcommand\b|\bevent id 20102\b", re.I),
        "wcs_application_error_diagnostic",
    ),
    (
        re.compile(
            r"\boptisweep\b\W*(?:\w+\W+){0,4}?\b(restart|reset|recover\w*)\b"
            r"|\b(restart|reset|recover\w*)\b\W*(?:\w+\W+){0,4}?\boptisweep\b",
            re.I,
        ),
        "optisweep_service_restart",
    ),
    (
        re.compile(r"\bgetagvstatuses\b|\bwcs\s*/?\s*api\b.*\b(respon)|\bapi\b.*\bresponsiveness\b|\bapidog\b", re.I),
        "wcs_api_responsiveness",
    ),
    (
        re.compile(
            r"\bagv state\b|\bcurrent location\b|\bdestination\b|\bfleet consistency\b|\brobotdatabasemodel\b"
            r"|\brobotlocationdatabasemodel\b|\bssms\b.*\bagv\b|\bagv\b.*\bssms\b",
            re.I,
        ),
        "agv_state_inspection",
    ),
    (
        re.compile(
            r"\bactive agv error\b|\bagv active error\b|\bsystemactiveerrormodel\b|\bagvactiveerrordatabasemodel\b"
            r"|\bactive fault\b|\berror code\b",
            re.I,
        ),
        "agv_active_error_inspection",
    ),
    (
        re.compile(
            r"\broster\b|\bpair(?:ing)?\b.*\bagv\b|\bagv\b.*\bpair"
            # "mapping"/"map monitor" alone are too broad -- Map Monitor is
            # also used for charger IDs, station IDs, E-stop button state,
            # and generic map-object selection, none of which validate robot
            # roster/mapping state. Require robot/AGV context nearby.
            r"|\bmapping\b\W*(?:\w+\W+){0,5}?\b(agv|robot)\b|\b(agv|robot)\b\W*(?:\w+\W+){0,5}?\bmapping\b"
            r"|\bmap monitor\b\W*(?:\w+\W+){0,6}?\b(agv|robot)\b|\b(agv|robot)\b\W*(?:\w+\W+){0,6}?\bmap monitor\b"
            r"|\bunmapped\b|\bnot mapped\b",
            re.I,
        ),
        "agv_roster_mapping_validation",
    ),
    (
        re.compile(
            r"\bremove\s*/?\s*recover\b|\bremoveagv\b|\brecoveragv\b|\bremove.*agv\b.*\brobot id\b|\bgeek api\b"
            r"|\bcorrect\w*\b\W*(?:\w+\W+){0,5}?\b(agv|robot)\b\W*(?:\w+\W+){0,4}?\b(out.of.sync|abnormal|state)\b"
            r"|\b(agv|robot)\b\W*(?:\w+\W+){0,5}?\bcorrect\w*\b"
            # Plain-language isolate/remove-from-system phrasing (no API-specific
            # terms like "RemoveAgv"/"geek api"/"robot id" nearby) -- e.g. "isolate
            # or remove the affected robot from the operating system", "AGV
            # physical isolation and system removal". Requires both an
            # isolate/remove verb AND a robot/AGV noun so bare "remove" (e.g.
            # "remove a tote") does not match.
            r"|\b(isolat\w*|remov\w*)\b\W*(?:\w+\W+){0,6}?\b(agv|robot)\b\W*(?:\w+\W+){0,4}?\b(system|operating system|grid)\b"
            r"|\b(agv|robot)\b\W*(?:\w+\W+){0,6}?\b(isolat\w*|remov\w*)\b\W*(?:\w+\W+){0,4}?\b(system|operating system|grid)\b"
            r"|\b(agv|robot)\b.{0,30}\bphysical isolation\b|\bphysical isolation\b.{0,30}\b(agv|robot)\b",
            re.I,
        ),
        "agv_remove_recover",
    ),
    (
        re.compile(
            r"\bstable[- ]operation\b|\bmulti[- ]signal\b|\bvalidation checklist\b|\bobservation window\b"
            r"|\bconfirm.*resumed\b|\bresumed operation\b",
            re.I,
        ),
        "multi_signal_recovery_validation",
    ),
    (
        re.compile(
            r"\bshutdown queue\w*\b|\bshutdown[- ]staging\b"
            r"|\btransition\w*\b\W*(?:\w+\W+){0,4}?\bzone\w*\b\W*(?:\w+\W+){0,4}?\bshutdown\b"
            r"|\bshutdown\b\W*(?:\w+\W+){0,4}?\btransition\w*\b\W*(?:\w+\W+){0,4}?\bzone\w*\b"
            r"|\bstartup\b.*\bzone cycling\b|\bzone cycling\b"
            # Generic shutdown/startup lifecycle delay phrasing (same family,
            # different vocabulary than "shutdown queue" -- e.g. "waiting to
            # exchange during shutdown or startup delay", "charger-waiting
            # startup delay"). Requires an explicit shutdown/startup lifecycle
            # word combined with a wait/delay/transition word so it does not
            # match every mention of "startup" or "shutdown" alone.
            r"|\b(shutdown|startup)\b\W*(?:\w+\W+){0,4}?\b(delay|waiting|wait\w*|cycling|transition\w*|lifecycle)\b"
            r"|\b(delay|waiting|wait\w*|cycling|transition\w*|lifecycle)\b\W*(?:\w+\W+){0,4}?\b(shutdown|startup)\b",
            re.I,
        ),
        "shutdown_queue_transition",
    ),
)

# Coarse legacy capability_tags -> plausible fine-grained capabilities they
# might represent. Used only to widen the *candidate* set considered during
# text classification, never trusted directly as a match.
_COARSE_TAG_HINTS: dict[str, tuple[str, ...]] = {
    "gateway_health": ("ignition_gateway_health", "ignition_gateway_restart", "opc_tag_flow"),
    "wcs_api_responsiveness": ("wcs_api_responsiveness",),
    "fleet_system_status": ("agv_state_inspection", "agv_roster_mapping_validation"),
    "agv_active_errors": ("agv_active_error_inspection",),
    "device_roster_state": ("agv_roster_mapping_validation", "agv_remove_recover"),
    "wcs_service_health": ("windows_service_health", "optisweep_service_restart"),
    "windows_service_or_event_log": ("windows_service_health", "wcs_application_error_diagnostic"),
}


def classify_text_capabilities(text: str) -> set[str]:
    """Derive fine-grained capabilities present in free text via keyword rules."""
    caps: set[str] = set()
    for pattern, capability in _TEXT_CAPABILITY_PATTERNS:
        if pattern.search(text or ""):
            caps.add(capability)
    return caps


def _runbook_text_blob(runbook: dict[str, Any] | None) -> str:
    if not isinstance(runbook, dict):
        return ""
    parts = [
        str(runbook.get("title") or ""),
        str(runbook.get("summary") or ""),
        str(runbook.get("when_to_use") or ""),
    ]
    parts.extend(str(item) for item in runbook.get("not_for") or [] if isinstance(item, str))
    return " ".join(parts)


def runbook_primary_capabilities(runbook: dict[str, Any] | None) -> set[str]:
    """Capabilities implied by the runbook's title alone.

    The title is the strongest signal of what a procedure is fundamentally
    *for*. A capability that only shows up deeper in the summary/when_to_use
    text (e.g. the OPC tag-flow procedure's "also confirm Ignition gateway
    health when needed" aside) is secondary, not primary -- it should not by
    itself veto eligibility for a node whose required capability the runbook
    otherwise satisfies via its primary function.
    """
    if not isinstance(runbook, dict):
        return set()
    return classify_text_capabilities(str(runbook.get("title") or ""))


def runbook_derived_capabilities(runbook: dict[str, Any] | None) -> set[str]:
    """Re-derive fine-grained capabilities for a runbook from its own text.

    Text classification is authoritative. A coarse legacy ``capability_tags``
    entry (e.g. "gateway_health") is only used as a fallback -- and only when
    text classification found *none* of that tag's plausible fine-grained
    capabilities -- so a coarse tag can never add an unrelated capability
    (such as ignition_gateway_restart) alongside one the text already
    positively identified (such as opc_tag_flow).
    """
    text = _runbook_text_blob(runbook)
    caps = classify_text_capabilities(text)
    if isinstance(runbook, dict):
        for tag in runbook.get("capability_tags") or []:
            hints = _COARSE_TAG_HINTS.get(str(tag).strip(), ())
            if not hints or caps & set(hints):
                continue
            for hinted in hints:
                if any(hinted in group and caps & group for group in MUTUALLY_EXCLUSIVE_GROUPS):
                    continue
                caps.add(hinted)
    return caps


def _node_text_blob(node: dict[str, Any]) -> str:
    parts = [
        str(node.get("title") or ""),
        str(node.get("intent") or ""),
        str(node.get("goal") or ""),
        str(node.get("runbook_placeholder") or ""),
        str(node.get("needed_runbook_capability") or ""),
        str(node.get("source_supported_description") or ""),
    ]
    for key in ("healthy_indicators", "unhealthy_indicators", "inconclusive_indicators"):
        value = node.get(key)
        if isinstance(value, list):
            parts.extend(str(item) for item in value if isinstance(item, str))
    return " ".join(parts)


_ACTION_FAMILY_BY_CAPABILITY_PRIORITY: tuple[str, ...] = (
    "opc_tag_flow",
    "agv_remove_recover",
    "ignition_gateway_restart",
    "optisweep_service_restart",
    "agv_active_error_inspection",
    "agv_roster_mapping_validation",
    "agv_state_inspection",
    "wcs_application_error_diagnostic",
    "windows_service_health",
    "ignition_gateway_health",
    "ignition_resource_health",
    "wcs_api_responsiveness",
    "multi_signal_recovery_validation",
)


def derive_retrieval_request(node: dict[str, Any]) -> dict[str, Any]:
    """Derive an internal-only retrieval request from a Stage 5 node.

    Built from node type, objective/intent text, and preferred audience --
    never from a runbook catalog lookup. This is retrieval metadata only and
    must not be rendered into the finalized playbook.
    """
    node_type = str(node.get("node_type") or "")
    text = _node_text_blob(node)
    text_caps = classify_text_capabilities(text)

    # Fold in explicit/ontology capability ids as *candidates* only -- they
    # are coarse (e.g. "gateway_health") and get resolved against the text
    # via the coarse-tag hint table, same as runbook-side handling.
    explicit_ids: set[str] = set()
    for item in node.get("ontology_capabilities") or []:
        if isinstance(item, dict) and item.get("id"):
            explicit_ids.add(str(item["id"]).strip())
    explicit_ids.update(str(item).strip() for item in node.get("expects_capability") or [] if str(item).strip())
    explicit_ids.update(str(item).strip() for item in node.get("required_evidence_concepts") or [] if str(item).strip())

    required = set(text_caps)
    for tag in explicit_ids:
        hints = _COARSE_TAG_HINTS.get(tag, ())
        if not hints or text_caps & set(hints):
            # Text classification already resolved this coarse tag to a
            # specific capability (or found nothing this tag can add beyond
            # what text already supports) -- do not widen further.
            continue
        for hinted in hints:
            if any(hinted in group and required & group for group in MUTUALLY_EXCLUSIVE_GROUPS):
                continue
            required.add(hinted)

    if node_type == "validation_gate":
        # Validation nodes corroborate multiple earlier signals; they should
        # not claim ownership of a single diagnostic capability such as
        # agv_state_inspection.
        required.discard("agv_state_inspection")
        required.discard("agv_active_error_inspection")
        required.add("multi_signal_recovery_validation")

    # A capability that is "related but not a synonym" of a required one
    # (Section 8) stays eligible as optional corroboration -- e.g. an
    # active-error query may corroborate an AGV-state node without being
    # promoted to primary (see _prefer_broader_primary_capability).
    optional: set[str] = set()
    for capability in required:
        for group in RELATED_NOT_SYNONYM_GROUPS:
            if capability in group:
                optional.update(group - {capability} - required)

    excluded: set[str] = set()
    for capability in required:
        for group in MUTUALLY_EXCLUSIVE_GROUPS:
            if capability in group:
                excluded.update(group - {capability})

    action_family = next(
        (capability for capability in _ACTION_FAMILY_BY_CAPABILITY_PRIORITY if capability in required),
        None,
    )

    preferred_surfaces = {
        str(item).strip()
        for item in (node.get("stage8_candidate_surfaces") or node.get("expects_surface") or [])
        if str(item).strip()
    }
    preferred_role = None
    preferred_audience = node.get("preferred_audience") or node.get("allowed_roles") or []
    for role in preferred_audience:
        role_str = str(role).strip()
        if role_str.lower() != "operator":
            preferred_role = role_str
            break

    return {
        "node_id": str(node.get("node_id") or ""),
        "node_type": node_type,
        "action_family": action_family,
        "required_capabilities": sorted(required),
        "optional_capabilities": sorted(optional - excluded),
        "excluded_capabilities": sorted(excluded - required),
        "preferred_surfaces": sorted(preferred_surfaces),
        "preferred_role": preferred_role,
        "derivation_source": "derived_from_node_text" if required else "no_signal",
    }


# Domain-rule penalty magnitudes, calibrated against observed real scores
# (semantic combined_score ranges ~0.3-0.9; existing link_scoring.py bonuses
# are +0.06 to +0.10; existing penalties are -0.22 to -0.30).
PRIMARY_EXCLUSION_PENALTY = -0.35
SECONDARY_EXCLUSION_PENALTY = -0.20
NO_REQUIRED_OVERLAP_PENALTY = -0.15


def capability_domain_adjustment(
    retrieval_request: dict[str, Any],
    runbook: dict[str, Any] | None,
) -> tuple[float, str | None]:
    """Domain-rule score adjustment, never a hard filter.

    Returns (penalty, reason). penalty is <= 0; 0.0 means "no domain-rule
    objection". A candidate with an excluded capability *as its primary
    (title-level) function* gets the largest penalty (PRIMARY_EXCLUSION_PENALTY)
    -- large enough to lose against any same-domain competitor with a normal
    score gap, but not so large it is mathematically unbeatable when there is
    no competing candidate at all. When the excluded capability only appears
    as a secondary aside elsewhere in the runbook's text (e.g. a tag-flow
    procedure's "also confirm gateway health when needed" note) and the
    runbook's primary function already satisfies a required capability, the
    penalty is milder (SECONDARY_EXCLUSION_PENALTY) -- a procedure that
    legitimately touches two systems should not be penalized as heavily as one
    whose whole purpose conflicts. When the request has no required
    capabilities (derivation found no signal), no penalty applies. When
    required capabilities are set but this runbook's re-derived fine-grained
    capabilities share none of them, a mild penalty applies
    (NO_REQUIRED_OVERLAP_PENALTY) -- this is usually a vocabulary-coverage gap
    (see module docstring), not a genuine domain conflict, so it must not
    dominate a strong semantic match.
    """
    runbook_caps = runbook_derived_capabilities(runbook)
    primary_caps = runbook_primary_capabilities(runbook)
    required = set(retrieval_request.get("required_capabilities") or [])
    excluded = set(retrieval_request.get("excluded_capabilities") or [])

    primary_hit = excluded & primary_caps
    if primary_hit:
        return PRIMARY_EXCLUSION_PENALTY, f"excluded capability: {sorted(primary_hit)[0]}"

    secondary_hit = excluded & (runbook_caps - primary_caps)
    if secondary_hit and not (required & primary_caps):
        return SECONDARY_EXCLUSION_PENALTY, f"excluded capability: {sorted(secondary_hit)[0]}"

    if not required:
        return 0.0, None
    if runbook_caps & required:
        return 0.0, None
    optional = set(retrieval_request.get("optional_capabilities") or [])
    if runbook_caps & optional:
        return 0.0, None
    return NO_REQUIRED_OVERLAP_PENALTY, "no required-capability overlap"
