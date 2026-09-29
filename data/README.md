# Machine data

Data encodes accepted upstream design/math; it never silently defines new rules. [accepted-state.json](manifests/accepted-state.json) is now a schema-4 high-level index, not the database. Its datasets and six Utility-family pointers lead to system encodings. [Authority map](manifests/authority-map.json) links design, implementation boundaries, tests and maturity.

- [Cycle 1](cycles/cycle_01/manifest.json): card categories and six Utility family datasets
- [QMO source inventory](qmo/inventory.json): 120 original FG records and the complete 2,094-object atlas imported
- [Black design data](black/design.json)
- [Collection/economy](collection/direction.json), [AI](ai/direction.json), [multiplayer](multiplayer/direction.json)
- [RenderSpec source boundary](render_specs/direction.json), [schemas](schemas/README.md)

The 2026-09-29 full migration applies explicit accepted design amendments; all unamended checkpoint values and original QMO data remain protected. [Schema migration](schemas/ACCEPTED_STATE_V4.md) describes pointers and lossless reconstruction. Historical manifests remain historical; do not use them as current runtime catalogs.

[Final continuity datasets](manifests/final-continuity-import.json) extend the preserved checkpoint-0004 payload with current Configuration Space, Generator interaction, board and relationship detail.


[Cycle-1 queries](qmo/README.md), [import manifest](manifests/cycle1-source-import.json) and [schema mapping](schemas/CYCLE1_IMPORT.md) expose the recovered source data directly from Git.


[Full migration manifest](manifests/full-migration-2026-09-29.json) links the 14-Prime catalog/H-C model, White Restore Prime, mutable Configuration Space, fixed top-down XY + 3D orientation, merge semantics and Genesis runtime direction. Ordinary Cycle 1 is 120 + 14 + 51 = 185.
