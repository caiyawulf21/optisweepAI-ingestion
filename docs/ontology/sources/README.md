# Ontology source packs

Provenance packs that feed machine-retrievable catalogs under `../catalogs/`.

```text
sources/
  day1/          # reserved — Day 1 training excerpts
  day2/          # reserved — Day 2 training excerpts
  om_manual/     # OM VISU section text extracts (populated)
```

## `om_manual/` (current)

Extracted from `manual_optisweep_om_v3` Stage 1 sections **4.1.2.1–4.1.2.6**:

| File pattern | Screen |
| --- | --- |
| `…visu_mcp_dual…` | Tipper Machine Control Panel |
| `…visu_data…` | VISU_DATA |
| `…visu_mancontrol…` | VISU_MANCONTROL |
| `…visu_mds…` | VISU_MDS (axis params) |
| `…visu_io_diag…` | VISU_IO_DIAG |
| `…visu_alarm…` | VISU_ALARM |

Rebuild projection: `python scripts/build_tipper_webvisu_catalog.py` → `../catalogs/tipper_hmi_catalog.json`.

Each pack should preserve `source_refs` / `evidence` snippets (OCR, transcript, nearby_text) rather than inventing field meanings.
