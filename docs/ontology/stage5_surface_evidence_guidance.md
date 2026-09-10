# Stage 5 source-grounded surface and evidence guidance

Stage 5 discovers troubleshooting playbook candidates from incident evidence. It
does not design the current support implementation. Stage 8 selects the
preferred diagnostic surface after Stage 5.

## Surface grounding

Do not add RMS, HMI, AVEVA, SQL/SSMS, API, Event Viewer, Windows Services, or
another technical surface unless:

- the original source explicitly names the surface;
- a readable source artifact visibly shows the surface; or
- the observation or action can only be understood from a surface explicitly
  present in the source.

AGV, fleet, pairing, location, mapping, and error language does not by itself
authorize RMS. Backend diagnostic usefulness does not by itself authorize
SQL/SSMS.

## Evidence versus future diagnostics

Every node separates:

- `observed_surfaces`: where the symptom was observed;
- `source_used_surfaces`: surfaces used during historical troubleshooting or
  recovery, each with provenance;
- `required_evidence_concepts`: operational concepts that must be determined;
- `recommended_diagnostic_surfaces`: normally empty at Stage 5;
- `stage8_candidate_surfaces`: optional future candidates that must not change
  Stage 5 actions, indicators, or branches.

Allowed source-surface provenance values are:

- `explicit_source`
- `strongly_implied_by_source`
- `source_artifact_visible`

Each `source_used_surfaces` item must include `surface`, `provenance`, and
source-grounded `source_evidence`. Do not include a surface whose provenance
would be `not_in_source`.

`required_evidence_concepts` describe state such as roster membership, pairing
state, location state, tote association, service health, or workflow state.
They are not SQL fields, table mappings, generated queries, or a preferred
support tool.

## Indicators and branches

The diagnostic reasoning must state:

- the question being answered;
- why the source supports the question;
- the evidence concepts needed;
- healthy, unhealthy, and inconclusive interpretations;
- source-supported branches; and
- any source-backed recovery action at a high level.

Healthy and unhealthy indicators describe operational state. A tool-specific
indicator is allowed only when the source makes the tool state relevant, such
as an explicitly reported blank RMS screen, an Event Viewer event, or an HMI
display.

Do not infer SQL fields, ontology table mappings, generated queries, runbook
links, detailed procedures, or a preferred RMS workflow. Stage 8 may later
select WCS/SSMS as the primary support diagnostic surface, with RMS as
corroboration when supported by the current catalog. If the source does not
dictate a required surface, Stage 5 leaves
`recommended_diagnostic_surfaces` empty.
