# Machine data

Data encodes accepted upstream design/math; it never silently defines new rules. [accepted-state.json](manifests/accepted-state.json) is now a schema-4 high-level index, not the database. Its datasets and six Utility-family pointers lead to system encodings. [Authority map](manifests/authority-map.json) links design, implementation boundaries, tests and maturity.

- [Cycle 1](cycles/cycle_01/manifest.json): card categories and six Utility family datasets
- [QMO source inventory](qmo/inventory.json): 120 original FG records and the complete 2,094-object atlas imported
- [Black design data](black/design.json)
- [Collection/economy](collection/direction.json), [AI](ai/direction.json), [multiplayer](multiplayer/direction.json)
- [RenderSpec source boundary](render_specs/direction.json), [schemas](schemas/README.md)

Detailed data preserves checkpoint-0003 gameplay values; the authorized Cycle-1 import updates only source-availability metadata. [Schema migration](schemas/ACCEPTED_STATE_V4.md) describes pointers and lossless reconstruction. Historical manifests remain historical; do not use them as current runtime catalogs.

[Final continuity datasets](manifests/final-continuity-import.json) extend the preserved checkpoint-0004 payload with current Configuration Space, Generator interaction, board and relationship detail.


[Cycle-1 queries](qmo/README.md), [import manifest](manifests/cycle1-source-import.json) and [schema mapping](schemas/CYCLE1_IMPORT.md) expose the recovered source data directly from Git.
