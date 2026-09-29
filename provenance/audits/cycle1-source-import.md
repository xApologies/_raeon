# Recovered original Cycle-1 import audit

Date: 2026-09-28. Starting main: `2e81478055483f1b86abff278b3cbc9109e61c9d`. Integration branch: `codex/authoritative-cycle1-import`; accepted destination: `main`.

The user-supplied `raeon_authoritative_cycle1_codex_import.zip` was extracted to an isolated temporary directory. All four original sources and their nested reference packages were inspected. No Cycle-1 builder/exporter was run to regenerate the data. Original sources and exact normalized machine files are preserved in ordinary Git; the existing Propagation LFS archive remains unchanged.

## Original artifact identity

| Original filename | SHA-256 |
| --- | --- |
| RAEON_CLOSED_PLAYFIELD_API_v1_0.zip | `18282091bffbf8ae51a600f23a359e0a0d13f3109287db6e80fbabf3253d266e` |
| RAEON_COMPLETE_QMO_ATLAS_CYCLE1.zip | `abc2b1e18f58b77184483923b0bbccc11886462f1cd6d7bdc5b73b044792ebcd` |
| RAEON_CYCLE_GENERATION_CONSTITUTION_v1_0.zip | `5e39897b70a52e0cdf5a74f80cece2cc6eae69cb880c0f50f06aebd0cd63cc9c` |
| RAEON_LIVE_MODEL_v0_1_2026-09-13.zip | `ba5758c7ab5fc9a6e1f9c634f8a0ac82432344bbf7234b601093f721978d3edf` |

Source date/version: September 13, 2026; locked Closed Playfield v1.0, Constitution v1.0, Live Model v0.1, complete Cycle-1 atlas. The [receipt](../sources/cycle1-originals/receipt.json), [408-member inventory](../sources/cycle1-originals/source-inventory.json), [file mappings](../sources/cycle1-originals/file-mappings.json), and [internal manifest results](../sources/cycle1-originals/internal-manifest-results.json) provide full provenance. All seven handoff manifest entries match. Latest locked manifests match: Closed Playfield 102, Constitution 22, Live Model 26. Older version manifests retain their documented stale hashes; they were not rewritten.

## Imported scope

| Verification | Result |
| --- | --- |
| Unique Field Generators | 120, exactly FG-001 through FG-120 |
| Base Local Manifolds | 60: Red 15, Orange 13, Yellow 11, Green 9, Blue 7, Violet 5 |
| Fusion-derived Local Manifolds | 343 |
| Emergent Fields | 1,691 |
| Complete field/manifold atlas | 2,094, with definitions directly present |
| Base-manifold pair space | 1,770 unique pairs, complete 60 choose 2 |
| Fusion outcomes | VALID 343; TERMINATES 825; NOT_APPLICABLE 602 |
| Emergent outcomes | VALID 1,691; TERMINATES 79 |
| Compatibility | 2,482 unique FG pairs with face matches and symmetric memberships |
| SQLite | Original bytes, integrity_check ok; all object/edge references resolve |
| Constitution | Readable design, math, schema, algorithm, validation and render handoff imported |
| RenderSpecs | 60 original base specs, catalog and schema; no Generator/derived specs invented |
| Live Model | Historical machine state and references preserved; newer main rules retained |

The [schema mapping](../../data/schemas/CYCLE1_IMPORT.md) records exact source names, filtered subsets and render path/64-bit seed handling. The [decision](../decisions/cycle1-source-import.md) documents source-label, historical-manifest, Live Model, runtime-copy, API-outcome and render-coverage conflicts. No Git merge conflict is anticipated from the clean starting main; final integration evidence is reported after push.

## Status migration and preservation

FG/base/fusion/emergent status files now contain actual IDs and object references. QMO inventory reports imported objects. The accepted-state and continuity manifests point to the [source import manifest](../../data/manifests/cycle1-source-import.json); authority map and current file inventory include the import. Cycle source status is IMPORTED_VALIDATED while full playable card definitions remain incomplete. Render status is partial with 60 concrete spec paths.

Cleared: FG QMO data, 60 base, 343 fusion, 1,691 emergent, complete 2,094 atlas, Cycle Generation Constitution. The Cycle-1 scope of QMO API, closure/pair data and base RenderSpecs/Blender references is now imported; broader requirements were narrowed instead of erased.

Remaining SOURCE_IMPORT_REQUIRED: Genesis; Chirality; Propagation mathematics; broader QMO definitions/API; closure beyond the imported game profile; transduction mathematics/API; Generator/derived RenderSpecs; unsupplied Generator/derived Blender geometry references; higher-dimensional projection mathematics.

OPEN: final Prime/Utility/card details, Generator printed-rank mapping, runtime admissible states and copy instances, resolved reopening/permanent-base fusion accounting, exact timing/overflow/hand limits, balance, engine/API, render integration, AI, multiplayer and broader research mapping. Production remains PREPRODUCTION; no gameplay mechanics redesigned or gameplay implementation claimed.

[Full changed-file ledger](cycle1-source-import-files.json) records created/modified paths; no existing file is moved or deleted. The [starting inventory](cycle1-source-import-baseline.json) protects historical provenance and runtime boundaries. Normalization regression compares the complete prior gameplay state after only the explicitly approved source-availability projection.

## Validation

Original extracted source tests: QMO 6/6, closure 6/6, render 4/4; historical Live Model 8/8. Historical test success does not promote its old rules to current canon. The commands were `python -B -m unittest discover -s tests -v`, with `tests_closure` and `tests_render` for the closed package, and `tests` within the isolated Live Model package. Source generation skeletons were not executed.

Repository validation passed before commit:

| Command | Result |
| --- | --- |
| `node tools/validators/validate-bootstrap.mjs` | PASS, 2,291 checks |
| `node tools/validators/validate-design-state.mjs` | PASS, 2,562 checks |
| `node tools/validators/validate-normalization.mjs` | PASS, 2,339 checks |
| `node tools/validators/validate-continuity.mjs` | PASS, 1,373 checks |
| `node tools/validators/validate-cycle1-import.mjs` | PASS, 100,085 checks |
| `node --test tests/regression/*.test.mjs` | PASS, 119 tests; zero failures/skips |
| `git diff --check` | PASS |

These are the final validator counts after documentation reconciliation. The staged source bytes and a fresh default-branch checkout are checked separately during promotion. Source integrity verifies original bytes, parsing, IDs, counts, references, SQL/JSON/atlas mirrors and known manifest snapshots. It does not prove theoretical mathematics or game-system correctness.
