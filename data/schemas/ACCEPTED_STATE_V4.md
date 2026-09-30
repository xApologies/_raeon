# Accepted-state schema 4

Checkpoint 0004 is a lossless information-architecture migration from schema 3. No card IDs, rules, balance values or source objects are assigned.

Root accepted-state.json retains high-level authority, provenance sources, production status and OPEN/source-import lists. It adds datasets (root-relative file paths and exact top-level keys), utility_families (six root-relative family files), authority_map and migration metadata. Schema/checkpoint metadata advances to 4/0004.

Each dataset has schema_version, design (the upstream current-spec path), and values. Only listed keys enter the assembled semantic state; unrelated status metadata does not invent objects. Utility overview values contain utility_structure without families, plus utility_clarifications; the six family datasets supply the families object. Semantic reference strings such as sandbox.temporary_capacity address the assembled view, not filesystem locations.

The read-only tooling adapter tools/validators/load-design-state.mjs resolves pointers within the repository, rejects duplicate/unlisted keys or mismatched family names, and reconstructs the prior semantic shape. This is validation tooling, not game code. The migration validator compares all values to the historical source snapshot after excluding only schema/checkpoint metadata. Current data is always read from normalized datasets, never from that snapshot.

Cycle manifest schema 4 points directly to category/family datasets. Previous manifests/checkpoints remain byte-for-byte history. Update dataset and upstream specification together through a decision; this checkpoint changes storage only.

## Additive continuity import

The optional high-level `continuity_import` pointer now identifies recovered specifications and separate typed datasets. The checkpoint-0004 payload remains reconstructable without modification; its board vocabulary is a historical compatibility projection. The Genesis Horizon dataset is the current explicit board detail. This extension does not promote provisional Prime/research statements or erase missing-source categories. `data/manifests/current-files.json` is the maintained inventory; numbered checkpoint inventories remain immutable historical evidence.

## Recovered Cycle-1 availability migration

The `cycle1_source_import` pointer now records original imported objects, hashes, relations and render coverage. Four availability values and the explicitly scoped missing-source list change; gameplay semantics do not. The normalization validator projects only those documented availability fields back to the historical checkpoint before comparison, and separately verifies their current imported values. [Cycle-1 schema mapping](CYCLE1_IMPORT.md) documents actual records and preserved field names.


## Accepted full migration — 2026-09-29

The `full_migration` pointer and `runtime` dataset extend the existing schema-4 index. No parallel architecture is introduced. The [reviewed amendment ledger](../../provenance/audits/full-migration-2026-09-29-semantic-changes.json) records thirteen precise semantic before/after changes and the new supplemental dataset contracts. The validator pins its hash, checks actual current values against each accepted change before projecting them back, then compares all unamended values to the original checkpoint. A mismatch is rejected, not hidden by the projection.

Ordinary counts are 120/14/51 = 185. The six prior Utility families retain 50 unchanged slots; `additional_slots` references the separate White Restore Prime definition. No arbitrary final UT-051 ID is assigned. Prime `identity_key` is a structural family/rank lookup key, not a finalized printed ID. `working-model.json` retains its path but now holds the accepted ordinary Prime H/C constitution. The imported source build specification and old handoff manifests retain historical budgets; current Cycle design/data supersede those older design counts without modifying original source bytes.


## Game-definition reconciliation — 2026-09-30

The additive `game_definition_reconciliation` pointer reaches one coherent [decision/receipt](../../provenance/decisions/game-definition-2026-09-30.json), with [rationale and validation](../../provenance/decisions/game-definition-2026-09-30.md). The index remains schema 4; affected supplemental board, space, interaction, relationship, Prime, runtime and match datasets advance to schema 2. Match now separates `match_rules` from `turn_match_open`; maximum Hand capacity moves out of OPEN and is encoded as seven. Draw/Deck mirrors that accepted capacity while preserving its seven effects and unresolved overflow.

The pinned decision stores exact JSON-path before/after amendments, not a parallel current rules hierarchy. Validators verify current after-values before reversing them, then compare all unamended values with earlier snapshots. The 2026-09-29 manifest and earlier source/checkpoint OPEN lists are historical evidence; current accepted-state and current design/data govern. Prime normal H_max/0 start and Hand capacity seven explicitly supersede those older OPEN entries. Unchanged QMO catalog bytes and nine missing-source requirements remain protected.
