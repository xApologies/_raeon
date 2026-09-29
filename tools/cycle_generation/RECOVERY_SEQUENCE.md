# Recovery Sequence

Follow this order exactly when rebuilding a new Cycle.

## Phase 0 — Integrity

1. Verify all source ZIP hashes if known.
2. Reassemble multipart Chirality Fabric before extraction.
3. Never edit source recovery archives in place.
4. Extract to read-only source directories.

## Phase 1 — Load mathematical sources

Load and index:
1. Genesis Field
2. Chirality Fabric
3. Propagation Engine

Recover the source definitions of:
- Resolution
- Bandwidth
- occupancy / cradle / void
- chirality
- projection
- inheritance/history
- recursive/closed domains
- update/propagation operators

## Phase 2 — Select Cycle seed

Choose one recovered closed recursive family or an explicitly documented
game-specialized family.

Cycle 1 used the hypercubic/dyadic family because it naturally supports a 2×2×2 byte.

Record:
- source family,
- seed equation,
- ambient dimension,
- refinement law,
- boundary law,
- any game specialization.

## Phase 3 — Generate Field Generator state space

Construct candidate Chirality Byte states under the Cycle rules.

For Cycle 1:
- eight fixed sites,
- exactly four cradle,
- exactly four void,
- orientation classes under proper cube rotations.

Assign deterministic QMO IDs:
FG-001 ... FG-120

Never assign compatibility manually as primary truth if it can be derived.

## Phase 4 — Derive Generator compatibility

Apply the Cycle compatibility operator to all relevant Generator pairs/orientations.

For each pair store:
- VALID compatibility edge(s), or
- TERMINATION evidence.

Cache compatibility for runtime speed.
The cache is downstream from the operator.

## Phase 5 — Generate base Local Manifold catalog

Search the Generator graph for valid closed substructures at each allowed size.

Cycle-1 target:
- 15 size-3
- 13 size-4
- 11 size-5
- 9 size-6
- 7 size-7
- 5 size-8

Prefer overlapping memberships so low-order and high-order strategies share
Generator vocabulary.

Reject:
- disconnected configurations,
- non-closing configurations,
- accidental duplicate manifold identities.

## Phase 6 — Close the playing field

Enumerate every unordered pair of base manifolds.

Evaluate independently:
1. Fusion
2. Emergent coupling

Store an explicit result for every pair.

For 60 base manifolds:
C(60,2) = 1770 pair records.

## Phase 7 — Generate derived QMOs

For each VALID relation:
- create a deterministic derived QMO address,
- record support QMOs,
- record operator,
- record result color/state,
- record derivation evidence.

## Phase 8 — Generate RenderSpecs

For every renderable QMO:
- derive anchors,
- topology graph,
- spline controls,
- chirality/winding data,
- Resolution parameters,
- Bandwidth parameters,
- field-shell parameters,
- animation constants,
- deterministic seed,
- projection parameters.

## Phase 9 — Validate

Run:
- QMO count tests,
- occupancy tests,
- manifold-size tests,
- color-distribution tests,
- pair-space tests,
- derived-QMO referential-integrity tests,
- deterministic RenderSpec tests,
- serialization tests.

## Phase 10 — Lock

Emit:
- CANON_LOCK.json
- full manifest
- hashes
- README
- open questions
- amendment file
- immutable release ZIP
