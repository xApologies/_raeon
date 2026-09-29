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
