# CODEX DIRECTIVE --- Import Recovered Authoritative Cycle-1 Artifacts

Repository: `https://github.com/xApologies/_raeon`

Canonical/default branch: `main`

## Mission

The canonical repository currently preserves Cycle-1 counts and
interfaces but still marks the actual QMO/ Field Generator objects as
missing. This package contains the recovered original source artifacts.

Import them into the existing normalized repository so the project is
self-contained and recoverable from Git.

This is NOT permission to redesign raeon. This is NOT permission to
regenerate Cycle 1. This is NOT permission to fabricate mathematics.

## 1. Inspect before editing

Pull/fetch current `main`.

Read all existing current specifications, especially: -
`design/cards/cycle_01/field_generators/SYSTEM.md` -
`design/topology/field_generators/SYSTEM.md` -
`design/topology/manifolds/SYSTEM.md` -
`design/topology/fusion/SYSTEM.md` -
`design/topology/emergent_fields/SYSTEM.md` -
`design/cards/CYCLE_PRODUCTION.md` - `mathematics/README.md` -
`data/manifests/accepted-state.json` - `data/qmo/inventory.json` -
`data/cycles/cycle_01/field_generators/status.json` - current
validators/provenance

Then extract and inspect EVERY authoritative source ZIP in
`authoritative_sources/`.

Do not trust filenames alone. Validate internal manifests/tests/counts
and compute hashes.

## 2. Preserve source artifacts

Store the recovered original ZIPs in an appropriate
source/provenance/archive boundary in the repository if repository
size/policy permits.

If Git LFS is appropriate and already supported, use it for large/binary
source artifacts.

Do not rely only on the ZIPs, however: normalize the important
machine-readable Cycle-1 data into ordinary repository files so future
tools/threads can query them directly without unpacking archives.

Never discard the original source bytes after normalization.

## 3. Import actual Field Generator data

From the authoritative Closed Playfield/QMO source, import the actual
120 Field Generator records.

Canonical machine data must expose FG-001 through FG-120 directly.

Preserve source fields where present, including mathematical/QMO
identity, fractal address, occupancy/void configuration,
chirality/orientation information, face states/views,
resolution/bandwidth metadata, manifold memberships, compatibility
relationships, and render references.

Do not rename or reinterpret source fields without a documented schema
migration.

Update: `data/cycles/cycle_01/field_generators/status.json`

so it no longer falsely reports `objects: []` / source missing after
successful verified import.

Keep any genuinely missing components explicitly
OPEN/SOURCE_IMPORT_REQUIRED.

## 4. Import the 60 base manifolds

Normalize all 60 base Local Manifold records into `data/qmo/` or the
existing canonical Cycle-1 topology data boundary.

Verify distribution: 15 Red 13 Orange 11 Yellow 9 Green 7 Blue 5 Violet
= 60

Preserve exact Generator memberships and closure metadata from source.

## 5. Import fusion-derived and emergent atlas

Import the complete Cycle-1 closed atlas.

Verify: 60 base 343 fusion-derived 1,691 emergent 2,094 total

Import actual object/index records, not only counts.

Preserve explicit relation outcomes and provenance.

Do not convert missing/unknown data into TERMINATES.

## 6. Import closure / pair-relation data

Import the authoritative closure/playfield relations from the Closed
Playfield API.

Verify source-reported pair counts and outcome counts against source
tests/manifests.

Preserve distinctions such as VALID, TERMINATES, NOT_APPLICABLE, OPEN,
UNTESTED where present.

Do not infer relations absent from source.

## 7. Import the Cycle Generation Constitution

The reusable Cycle Generation Constitution is no longer
SOURCE_IMPORT_REQUIRED after verified import.

Integrate its readable
constitution/pipeline/schema/algorithm/validation/render-handoff
material into the appropriate repository
design/mathematics/tools/provenance boundaries while preserving the
original ZIP.

Do not let an older embedded Cycle-1 rules reference overwrite newer
accepted game design.

The Constitution governs reproducible future Cycle generation unless
later amended by explicit project decision.

## 8. Live Model reconciliation

Import the Live Model as historical/provenance evidence and useful
machine state.

Do NOT blindly replace current `main` with the September-13 state.

Use it to recover source history, rules provenance, timelines, tests,
schemas, and any still-missing accepted content.

Where Live Model conflicts with newer current specifications, preserve
the newer accepted state and document the historical difference.

## 9. Rendering assets/data

Import the source-backed RenderSpecs/catalog and Blender/runtime
construction material present in the recovered Cycle-1 artifacts into
appropriate `data/render_specs`, `content`, `tools`, or
source/provenance boundaries.

Do not claim the renderer is implemented merely because source/reference
scripts exist.

QMO remains authoritative over render.

## 10. Update source-status manifests

After verified import, update repository status honestly.

In particular, the following should no longer remain generically
SOURCE_IMPORT_REQUIRED if their actual source has now been imported and
validated: - Field Generator QMO data - 60 base Local Manifold QMOs -
343 fusion-derived Local Manifold QMOs - 1,691 Emergent Field QMOs -
complete 2,094-object Cycle-1 atlas - Cycle Generation Constitution -
Cycle-1 closure/playfield relation data - Cycle-1 RenderSpecs only to
the extent actually present in source

Do NOT clear unrelated missing sources such as broader Genesis/Chirality
mathematics, projection mathematics, or anything not actually
contained/validated in these artifacts.

## 11. Provenance

Create a clear source-recovery audit recording: - original uploaded
filenames - SHA-256 hashes - internal manifests/hashes if available -
source dates/versions - extracted record counts - schema mappings -
files normalized into Git - conflicts found - decisions made -
validation results

Record that these are recovered original Cycle-1 artifacts, not newly
generated replacements.

## 12. Repository architecture

Preserve the current normalized architecture: DESIGN -\> DATA -\> GAME
-\> TESTS

MATHEMATICS = legality/source formalism DEVELOPMENT = maturity
PROVENANCE = history/source chain

Do not create a parallel documentation tree.

## 13. Validation

Run all existing validators, including continuity validation.

Add source-import validation that checks at minimum: - exactly 120 FG
identities - FG identity uniqueness - exactly 60 base manifolds - base
color distribution 15/13/11/9/7/5 - exactly 343 fusion-derived objects -
exactly 1,691 emergent objects - exactly 2,094 total atlas objects - all
referenced Generator IDs exist - all referenced manifold/QMO IDs
resolve - imported hashes/source manifests match - machine data parses -
no duplicate IDs - source relation outcome vocabulary is preserved -
current design links resolve

Run regression tests and `git diff --check`.

Do not claim these validators prove the theoretical mathematics; they
verify source integrity and repository consistency.

## 14. Git workflow

Use a temporary import branch if needed.

After successful validation: - merge/promote into `main` - push `main` -
verify default GitHub checkout returns updated `main` - delete temporary
remote branch if safe and fully merged

Do not leave authoritative Cycle-1 data stranded on a feature branch.

## 15. Final report

Report: - starting main SHA - ending main SHA - source artifact hashes -
files imported - 120 FG verification - 60 base manifold verification -
343 fusion verification - 1,691 emergent verification - 2,094 atlas
verification - closure/pair relation verification - Constitution import
status - Live Model reconciliation result - RenderSpec import status -
manifest/status fields changed - SOURCE_IMPORT_REQUIRED items cleared -
SOURCE_IMPORT_REQUIRED items still remaining - conflicts -
validators/tests and results - default branch verification

Explicitly confirm only if true:

`THE ORIGINAL CYCLE-1 ARTIFACTS ARE NOW PRESERVED IN GIT`
`FG-001 THROUGH FG-120 ARE QUERYABLE FROM THE REPOSITORY`
`THE 2,094-OBJECT ATLAS IS QUERYABLE FROM THE REPOSITORY`
`THE CYCLE GENERATION CONSTITUTION IS PRESERVED`
`MAIN IS THE CANONICAL RAEON STATE`
`NO CYCLE-1 MATHEMATICS WAS REGENERATED OR FABRICATED`
`WHOLE-GAME PHASE REMAINS PREPRODUCTION`
