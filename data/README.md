# Machine data

Data encodes accepted upstream design/math; it never silently defines new rules. [accepted-state.json](manifests/accepted-state.json) is now a schema-4 high-level index, not the database. Its datasets and six Utility-family pointers lead to system encodings. [Authority map](manifests/authority-map.json) links design, implementation boundaries, tests and maturity.

- [Cycle 1](cycles/cycle_01/manifest.json): card categories and six Utility family datasets
- [QMO source inventory](qmo/inventory.json): no imported objects fabricated
- [Black design data](black/design.json)
- [Collection/economy](collection/direction.json), [AI](ai/direction.json), [multiplayer](multiplayer/direction.json)
- [RenderSpec source boundary](render_specs/direction.json), [schemas](schemas/README.md)

Detailed data preserves checkpoint-0003 values exactly. [Schema migration](schemas/ACCEPTED_STATE_V4.md) describes pointers and lossless reconstruction. Historical manifests remain historical; do not use them as current runtime catalogs.
